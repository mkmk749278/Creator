#!/usr/bin/env python3
# Reusable tool kept from an earlier film (repo slimmed 2026-11-05): adapt the paths at the top to the new film.
"""Word times on the raw VO (no speech recognition): each aligned sentence's words are spread by letter count, then
each word start snaps to the nearest real pause in the voice (silencedetect -38 dB, >= 60 ms) within 0.35 s.
Writes align/words.json: [{line, sent, i, w, t}] (raw VO seconds). make_film.py maps them to film time with F()."""
import json, re, subprocess
from pathlib import Path
P = Path(__file__).resolve().parents[1]
S = json.loads((P / "align/sentences.json").read_text())
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(P / "voice/vo_full.wav"), "-af", "silencedetect=n=-38dB:d=0.06", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
out = []
for k, s in enumerate(S):
    ws = s["en"].split(); a, b = s["start"], s["end"]; tot = sum(len(w) + 1 for w in ws); acc = 0
    for i, w in enumerate(ws):
        t = a + (b - a) * acc / tot
        if i:
            near = [e for e in ends if a < e < b and abs(e - t) < 0.35]
            if near:
                t = min(near, key=lambda e: abs(e - t))
        out.append(dict(line=s["line"], sent=k, i=i, w=re.sub(r"[^\w'.-]", "", w), t=round(t, 3)))
        acc += len(w) + 1
(P / "align/words.json").write_text(json.dumps(out, ensure_ascii=False))
print(len(out), "words;", len(ends), "pauses")
