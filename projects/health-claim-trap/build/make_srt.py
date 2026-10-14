#!/usr/bin/env python3
"""youtube/subtitles.en.srt on the film timeline (sentence cues from build/timing.py; VO hyphen-spellings undone for reading)."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import SENT
P = Path(__file__).resolve().parents[1]
FIX = {"I-R-D-A-I": "IRDAI", "T-P-As": "TPAs", "T-P-A": "TPA", "B-P": "BP", "c-i-o-i-n-s dot co dot in": "cioins.co.in",
       "Bima Bharosa dot I-R-D-A-I dot gov dot in": "bimabharosa.irdai.gov.in"}
def ts(t):
    ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
out = []
for i, s in enumerate(SENT):
    txt = s["text"]
    for a, b in sorted(FIX.items(), key=lambda x: -len(x[0])):
        txt = txt.replace(a, b)
    end = s["end"] + 0.25
    if i + 1 < len(SENT) and SENT[i + 1]["start"] - s["end"] < 1.0:
        end = SENT[i + 1]["start"] - 0.02
    lines, cur = [], ""
    for w in txt.split():   # two lines of at most ~42 characters
        if len(cur) + len(w) + 1 > 42 and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    out.append(f"{i + 1}\n{ts(s['start'])} --> {ts(end)}\n" + "\n".join(lines) + "\n")
(P / "youtube").mkdir(exist_ok=True)
(P / "youtube/subtitles.en.srt").write_text("\n".join(out))
print(len(out), "cues")
