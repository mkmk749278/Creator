"""Build the master audio for a narrated documentary from one continuous voiceover.

1. Splits the voiceover at the given points and inserts "live pauses" (silence in
   the voice track) where the picture holds on a dramatic moment.
2. Writes the voice track with pauses, plus a pause map so subtitle and scene
   times can be shifted from voiceover time to video time.

Usage: python scripts/mix_master.py VOICE.mp3 pauses.json OUT_DIR
pauses.json: [{"at": 126.4, "len": 4.0, "why": "shankha"}, ...]  (voiceover seconds)
Writes OUT_DIR/voice_paused.wav (48 kHz mono) and OUT_DIR/pause_map.json.
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000


def main():
    voice, pauses_path, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    raw = out / "voice48.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", voice, "-ar", str(SR), "-ac", "1", str(raw)], check=True)
    a, _ = sf.read(raw, dtype="float32")
    raw.unlink()
    pauses = sorted(json.loads(pauses_path.read_text()), key=lambda p: p["at"])
    pieces, prev = [], 0
    for p in pauses:
        i = int(p["at"] * SR)
        pieces += [a[prev:i], np.zeros(int(p["len"] * SR), dtype=np.float32)]
        prev = i
    pieces.append(a[prev:])
    y = np.concatenate(pieces)
    sf.write(out / "voice_paused.wav", y, SR)
    pmap = {"voice_duration": round(len(a) / SR, 3), "video_duration": round(len(y) / SR, 3), "pauses": pauses}
    (out / "pause_map.json").write_text(json.dumps(pmap, indent=2) + "\n")
    print(f"voice {pmap['voice_duration']}s -> {pmap['video_duration']}s with {len(pauses)} pauses")


def shift(t: float, pauses: list) -> float:
    """Voiceover time -> video time."""
    return t + sum(p["len"] for p in pauses if p["at"] <= t)


if __name__ == "__main__":
    main()
