#!/usr/bin/env python3
"""Splice the owner's Akash re-takes (2026-10-24) into the final voice-over and write the old->new time map.

Fixes from review_film_independent_v2.md: "forty-ton" removed (L17), "idle to full power in seconds" (L39), "have retired"
(L43), "two-thousand-crore" (L52). Each re-take replaces the old speech span (found with silencedetect at -32/-40 dB) and
keeps the old pauses around it; 15 ms fades at every join.
  python3 projects/jet-engine-bet/build/splice_vo.py  -> final/jeb_vo_v2.wav + final/splices.json
assemble_4k.py reads splices.json and maps every cut and label time through the same piecewise-linear map.
"""
import json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

P = Path(__file__).resolve().parents[1] / "final"
SR = 48000
# (old speech start, old speech end, re-take file, take speech start, take speech end), seconds
SPLICES = [
    (126.37, 138.28, "l17_blow.mp3", 0.108, 12.65),
    (297.83, 305.48, "l39_fighter.mp3", 0.063, 10.04),
    (338.76, 342.92, "l43_mig21.mp3", 0.064, 4.49),
    (431.40, 435.73, "l52_crore.mp3", 0.067, 4.23),
]

def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()

def fade(x, n=int(0.015 * SR)):
    x = x.copy(); n = min(n, len(x) // 2); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n); return x

def main():
    old = load(P / "jeb_vo_final.mp3")
    out, cur, tmap = [], 0, []
    for o0, o1, f, s0, s1 in SPLICES:
        i0, i1 = int(o0 * SR), int(o1 * SR)
        out.append(fade(old[cur:i0]))
        take = load(P / "retakes" / f)[int(s0 * SR):int(s1 * SR)]
        # match the old line's level (RMS over speech)
        g = np.sqrt(np.mean(old[i0:i1] ** 2)) / max(1e-9, np.sqrt(np.mean(take ** 2)))
        out.append(fade(take * g)); cur = i1
        tmap.append({"old": [o0, o1], "new_len": round(s1 - s0, 4), "gain": round(float(g), 3), "file": f})
    out.append(fade(old[cur:]))
    y = np.concatenate(out)
    sf.write(P / "jeb_vo_v2.wav", y, SR)
    (P / "splices.json").write_text(json.dumps({"old_duration": round(len(old) / SR, 4), "new_duration": round(len(y) / SR, 4), "splices": tmap}, indent=1) + "\n")
    print(f"old {len(old) / SR:.2f} s -> new {len(y) / SR:.2f} s")

if __name__ == "__main__":
    main()
