"""Generate the two-host voice track for one script part with Kokoro (local, free).

Reads runs/<slug>/script.json, synthesises every line of one part with the
speaker's voice, joins them with natural gaps, and writes:
  runs/<slug>/voice/<part>.wav          (48 kHz mono, loudness-normalised later)
  runs/<slug>/voice/<part>.timings.json (per-line start/end seconds)

Usage: python scripts/voice_part.py runs/pixel-11 p1 [p2 ...]
Needs: kokoro-onnx, soundfile, numpy; model files are fetched by
`npx hyperframes tts` into ~/.cache/hyperframes/tts.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import kokoro_onnx

CACHE = Path.home() / ".cache/hyperframes/tts"
MODEL = CACHE / "models/kokoro-v1.0.onnx"
VOICES = CACHE / "voices/voices-v1.0.bin"
SR = 24000
LEAD_IN = 0.5     # silence before the first line
TAIL = 0.9        # silence after the last line
GAP = 0.32        # default pause between lines
SAME_SPEAKER_GAP = 0.45


def synth(model: kokoro_onnx.Kokoro, text: str, voice: str, speed: float) -> np.ndarray:
    # Kokoro has a ~510-token limit per call: synthesise sentence by sentence.
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    chunks = []
    for i, s in enumerate(sentences):
        audio, sr = model.create(s, voice=voice, speed=speed, lang="en-us")
        assert sr == SR, sr
        chunks.append(audio)
        if i < len(sentences) - 1:
            chunks.append(np.zeros(int(0.12 * SR), dtype=np.float32))
    return trim(np.concatenate(chunks))


def trim(audio: np.ndarray, threshold: float = 0.004) -> np.ndarray:
    """Cut leading/trailing near-silence so our own gaps control the rhythm."""
    idx = np.where(np.abs(audio) > threshold)[0]
    if len(idx) == 0:
        return audio
    start = max(0, idx[0] - int(0.03 * SR))
    end = min(len(audio), idx[-1] + int(0.08 * SR))
    return audio[start:end]


def build_part(run: Path, part_id: str, model: kokoro_onnx.Kokoro) -> dict:
    script = json.loads((run / "script.json").read_text(encoding="utf-8"))
    hosts = script["hosts"]
    part = next(p for p in script["parts"] if p["id"] == part_id)

    out_dir = run / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    pieces = [np.zeros(int(LEAD_IN * SR), dtype=np.float32)]
    t = LEAD_IN
    timings = []
    prev_speaker = None
    for i, line in enumerate(part["lines"]):
        host = hosts[line["speaker"]]
        if i > 0:
            gap = line.get("gap_before", SAME_SPEAKER_GAP if line["speaker"] == prev_speaker else GAP)
            pieces.append(np.zeros(int(gap * SR), dtype=np.float32))
            t += gap
        audio = synth(model, line["say"] if "say" in line else line["text"], host["voice"],
                      line.get("speed", host.get("speed", 1.0)))
        dur = len(audio) / SR
        timings.append({"id": line["id"], "speaker": line["speaker"], "text": line["text"],
                        "start": round(t, 3), "end": round(t + dur, 3)})
        pieces.append(audio)
        t += dur
        prev_speaker = line["speaker"]
    pieces.append(np.zeros(int(TAIL * SR), dtype=np.float32))
    t += TAIL

    raw = out_dir / f"{part_id}.raw.wav"
    sf.write(raw, np.concatenate(pieces), SR)
    # Resample to 48 kHz and apply gentle EQ/compression so both voices sit together.
    wav = out_dir / f"{part_id}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,"
                           "aresample=48000",
                    "-ac", "1", str(wav)], check=True)
    raw.unlink()
    result = {"part": part_id, "duration": round(t, 3), "audio": f"voice/{part_id}.wav", "lines": timings}
    (out_dir / f"{part_id}.timings.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    run = Path(sys.argv[1])
    model = kokoro_onnx.Kokoro(str(MODEL), str(VOICES))
    for part_id in sys.argv[2:]:
        r = build_part(run, part_id, model)
        print(f"{part_id}: {r['duration']:.1f}s, {len(r['lines'])} lines")


if __name__ == "__main__":
    main()
