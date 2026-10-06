"""Voice a short two-host dialogue with Kokoro (local, free) and derive lip-sync mouth keys.

Reads <dir>/dialogue.json and writes:
  <dir>/voice.wav      (24 kHz mono)
  <dir>/lipsync.json   (per-line timings + mouth keyframes at 12 fps)

Mouth shapes come from the audio itself: loudness picks closed/slightly open/open/wide,
and the spectral centroid turns open vowels into "O" (dark, low) or "E" (bright, high).
Usage: python scripts/make_lipsync.py video/duo-talk
Needs: kokoro-onnx, soundfile, numpy; model files are fetched by `npx hyperframes tts`.
"""

import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import kokoro_onnx

sys.path.insert(0, str(Path(__file__).parent))
from voice_part import MODEL, SR, VOICES, synth  # noqa: E402

LEAD_IN = 0.6
GAP = 0.35
TAIL = 1.0
FPS = 12  # mouth updates per second (cartoon "on twos" feel at 24-30 fps)


def mouth_keys(audio: np.ndarray, start: float) -> list[dict]:
    hop = SR // FPS
    frames = [audio[i:i + hop] for i in range(0, len(audio) - hop // 2, hop)]
    rms = np.array([np.sqrt(np.mean(f ** 2)) for f in frames])
    ref = np.percentile(rms, 95) or 1.0
    keys, last = [], None
    for i, f in enumerate(frames):
        level = rms[i] / ref
        spec = np.abs(np.fft.rfft(f * np.hanning(len(f))))
        freqs = np.fft.rfftfreq(len(f), 1 / SR)
        centroid = float((spec * freqs).sum() / (spec.sum() or 1))
        if level < 0.12:
            shape = "X"
        elif level < 0.35:
            shape = "E" if centroid > 2600 else "A"
        elif level < 0.7:
            shape = "O" if centroid < 900 else ("E" if centroid > 2600 else "B")
        else:
            shape = "O" if centroid < 900 else "C"
        if shape != last:
            keys.append({"t": round(start + i / FPS, 3), "shape": shape})
            last = shape
    if last != "X":
        keys.append({"t": round(start + len(audio) / SR, 3), "shape": "X"})
    return keys


def main(out: Path) -> None:
    dialogue = json.loads((out / "dialogue.json").read_text(encoding="utf-8"))
    model = kokoro_onnx.Kokoro(str(MODEL), str(VOICES))
    parts = [np.zeros(int(LEAD_IN * SR), dtype=np.float32)]
    t = LEAD_IN
    lines = []
    for i, line in enumerate(dialogue["lines"]):
        host = dialogue["hosts"][line["speaker"]]
        audio = synth(model, line["text"], host["voice"], host.get("speed", 1.0))
        dur = len(audio) / SR
        lines.append({**line, "start": round(t, 3), "end": round(t + dur, 3), "mouth": mouth_keys(audio, t)})
        parts.append(audio)
        t += dur
        gap = GAP if i < len(dialogue["lines"]) - 1 else TAIL
        parts.append(np.zeros(int(gap * SR), dtype=np.float32))
        t += gap
    sf.write(out / "voice.wav", np.concatenate(parts), SR)
    result = {"duration": round(t, 3), "fps": FPS, "lines": lines}
    (out / "lipsync.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    shapes = [k["shape"] for ln in lines for k in ln["mouth"]]
    print(f"wrote {out}/voice.wav ({t:.2f}s) and lipsync.json:",
          {s: shapes.count(s) for s in "XABCOEH" if s in shapes})


if __name__ == "__main__":
    main(Path(sys.argv[1]))
