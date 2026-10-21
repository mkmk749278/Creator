#!/usr/bin/env python3
"""Build the edited VO for film 36 from take 1 + three re-generated lines, adding the pauses in edit_fixes.md.

Every cut sits inside a measured pause (silencedetect d=0.15 on the source), at the pause's midpoint, so no word is
clipped. The inserted room tone is digital silence: the ElevenLabs pauses measure -75 to -83 dB RMS, already
silent, and the BGM sits under the VO in the mix.

  python3 tools/assemble_vo.py   (from projects/solar-anti-islanding) -> voice/vo_v10_edit.wav + voice/vo_v10_edit.mp3
"""
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 44100
V = Path("voice")


def load(name, af="anull"):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(V / name), "-af", af, "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16)


SEGS = []


def cut(x, t0, t1):
    SEGS.append((NAMES[id(x)], t0, t1)) if id(x) in NAMES else None
    return x[int(round(t0 * SR)):int(round(t1 * SR))]


def gap(sec):
    SEGS.append(("gap", 0.0, sec))
    return np.zeros(int(round(sec * SR)), dtype=np.int16)


T15 = 0.9                      # line 15 still read at 220 wpm after re-generation: pitch-safe slow-down
take, f34, f15, f22 = load("vo_v10_take1.mp3"), load("fix_03_04.mp3"), load("fix_15.mp3", f"atempo={T15}"), load("fix_22.mp3")
NAMES = {id(take): "take", id(f34): "f34", id(f15): "f15", id(f22): "f22"}

# Cut points: midpoints of the pauses between lines (align/align.json) or inside a line (silencedetect).
mid = lambda a, b: (a + b) / 2
L2_3 = mid(14.599, 15.186)     # end of line 2 / start of line 3 (replaced)
L4_5 = mid(28.82, 29.262)      # end of line 4 (replaced) / line 5
L6_7 = mid(47.502, 47.95)
L7_drum = mid(53.90, 54.27)    # line 7, after "as a drummer..."
L8_9 = mid(67.883, 68.327)
L11_230 = mid(83.43, 83.61)    # line 11, after "two hundred and thirty volts..."
L11_11k = mid(85.96, 86.27)    # line 11, after "eleven thousand volts."
L11_12 = mid(88.577, 89.083)
L12_13 = mid(100.325, 100.699)
L14_15 = mid(117.287, 117.649) # line 15 replaced
L15_16 = mid(120.354, 120.706)
L16_17 = mid(127.799, 128.281)
L18_19 = mid(146.127, 146.812)
L21_22 = mid(172.694, 173.198) # line 22 replaced
L22_23 = mid(180.296, 181.072)
END = len(take) / SR

# Re-generated clips: inner pause midpoints (silencedetect on each file).
F34_L3 = mid(4.86, 5.45)       # end of line 3
F34_home = mid(8.97, 9.37)     # "... you keep at home."
F34_grid = mid(14.21, 14.62)   # "... on-grid inverter."
F22_no = mid(3.89, 4.36)       # "... just say no."

pad = lambda: gap(0.22)        # half a typical pause, before/after a re-generated clip that starts/ends on speech

parts = [
    cut(take, 0, L2_3), pad(),
    cut(f34, 0, F34_L3), gap(1.0),                         # 1  after line 3, end of hook
    cut(f34, F34_L3, F34_home), gap(0.5),                  # 2  after "at home."
    cut(f34, F34_home, F34_grid), gap(0.6),                # 3  after "on-grid inverter."
    cut(f34, F34_grid, 16.26), pad(),
    cut(take, L4_5, L6_7), gap(1.0),                       # 4  after line 6
    cut(take, L6_7, L7_drum), gap(0.5),                    # 5  after "as a drummer..."
    cut(take, L7_drum, L8_9), gap(1.0),                    # 6  after line 8 (music silent 1.5 s, then thud)
    cut(take, L8_9, L11_230), gap(0.5),                    # 7  after "thirty volts..."
    cut(take, L11_230, L11_11k), gap(0.8),                 # 8  after "eleven thousand volts."
    cut(take, L11_11k, L11_12), gap(1.0),                  # 9  after "switched off."
    cut(take, L11_12, L12_13), gap(1.0),                   # 10 after line 12 (first click)
    cut(take, L12_13, L14_15), gap(0.6),                   # 11 after "is the drummer still there?"
    pad(), cut(f15, 0, 3.27 / T15), pad(), gap(0.5),                 # 12 line 15 re-generated, then 0.5 s
    cut(take, L15_16, L16_17), gap(1.0),                   # 13 after line 16 (second click)
    cut(take, L16_17, L18_19), gap(1.0),                   # 14 after line 18
    cut(take, L18_19, L21_22), gap(0.7),                   # 15 before line 22
    pad(), cut(f22, 0, F22_no), gap(0.6),                 # 16 after "just say no."
    cut(f22, F22_no, 7.86), pad(), gap(0.6),                 # 17 before line 23
    cut(take, L22_23, END),
]
out = np.concatenate(parts)

# Exact per-line times in the edit, mapped through the cut list (the aligner's long-pause preference misreads the
# inserted pauses as line ends, so these replace align_edit for screenplay timing).
import json
SPANS = {"f34": [(3, 0.0, 4.86), (4, 5.45, 16.26)], "f15": [(15, 0.0, 3.27 / T15)], "f22": [(22, 0.0, 7.86)]}
orig = json.load(open("align/align.json"))
orig = orig if isinstance(orig, list) else orig["lines"]
SPANS["take"] = [(r["line"], r["start"], r["end"]) for r in orig if r["line"] not in (3, 4, 15, 22)]
segs, t = [], 0.0
for src, a, b in SEGS:
    segs.append((src, a, b, t)); t += b - a
def to_out(src, x):
    for s, a, b, o in segs:
        if s == src and a - 1e-6 <= x <= b + 1e-6:
            return round(o + x - a, 3)
    raise ValueError((src, x))
text = [l.strip() for l in open("align_lines.txt") if l.strip()]
lines = sorted((n, to_out(src, a), to_out(src, b)) for src, sp in SPANS.items() for n, a, b in sp)
json.dump([{"line": n, "start": a, "end": b, "en": text[n - 1]} for n, a, b in lines],
          open("align_edit/lines_exact.json", "w"), indent=1)
with wave.open(str(V / "vo_v10_edit.wav"), "wb") as w:
    w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(out.tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "vo_v10_edit.wav"), "-b:a", "192k",
                str(V / "vo_v10_edit.mp3")], check=True)
print(f"vo_v10_edit: {len(out) / SR:.2f} s (take 1: {END:.2f} s)")
