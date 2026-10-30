#!/usr/bin/env python3
"""Shot-by-word audit (owner's review, 2026-10-30: "narration to scene, every second, word by word"). Lists every shot
of the built parts with the words spoken over it, pulls one frame per shot from a rendered cut, and tiles labelled
sheets (12 shots each) to read against the words. Word times are spread over each aligned sentence by letter count,
so treat them as +-0.3 s; for exact cuts measure the voice's own gaps (silencedetect on voice/vo_film.wav).
Usage: python3 projects/pharma-apis/build/shot_word_audit.py CUT.mp4 OUTDIR   (after make_film.py)"""
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

B = Path(__file__).resolve().parent; P = B.parent; ROOT = P.parents[1]
src = (B / "make_film.py").read_text().split("FOOT = {")[0].replace("__file__", repr(str(B / "make_film.py")))
ns = {}; exec(src, ns)
cut, out = Path(sys.argv[1]), Path(sys.argv[2]); (out / "f").mkdir(parents=True, exist_ok=True)
parts = json.loads((B / "parts.json").read_text())
shots = []
for k, t0 in enumerate(parts[:-1]):
    h = (ROOT / f"video/pha/p{k + 1}/index.html").read_text()
    for m in re.finditer(r'<div id="p\d-s\d+" class="shot"([^>]*)>(.*?)</div>', h, re.S):
        a = m.group(1) + m.group(2)
        st = float(re.search(r'data-(?:vs|start)="([\d.]+)"', a).group(1)); du = float(re.search(r'data-(?:vd|duration)="([\d.]+)"', a).group(1))
        shots.append(dict(t=round(t0 + st, 2), d=round(du, 2), src=re.search(r'src="media/([^"]+)"', a).group(1)))
shots.sort(key=lambda x: x["t"])
W = []
for s in ns["SENTS"]:
    a, b = ns["F"](s["start"]), ns["F"](s["end"]); ws = s["en"].split(); tot = sum(map(len, ws)); acc = 0
    for w in ws:
        W.append((a + (b - a) * acc / tot, w)); acc += len(w)
for i, sh in enumerate(shots):
    sh["words"] = " ".join(w for t, w in W if sh["t"] <= t < sh["t"] + sh["d"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sh['t'] + min(sh['d'] / 2, sh['d'] - 0.1):.2f}", "-i", str(cut),
                    "-frames:v", "1", "-vf", "scale=480:-2", str(out / "f" / f"{i:03d}.jpg")], check=True)
    print(f"{i:3d} {int(sh['t']) // 60}:{sh['t'] % 60:05.2f} {sh['d']:5.2f} {sh['src'][:34]:34s} | {sh['words']}")
(out / "shots.json").write_text(json.dumps(shots, indent=0))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
for p in range(0, len(shots), 12):
    S = Image.new("RGB", (1920, 1020), "black"); d = ImageDraw.Draw(S)
    for k, i in enumerate(range(p, min(p + 12, len(shots)))):
        s = shots[i]; x, y = (k % 4) * 480, (k // 4) * 340
        S.paste(Image.open(out / "f" / f"{i:03d}.jpg"), (x, y))
        d.text((x + 4, y + 272), f"#{i} {int(s['t']) // 60}:{s['t'] % 60:04.1f} {s['src'][:28]}", fill="yellow", font=font)
        for j, line in enumerate(textwrap.wrap(s["words"], 56)[:3]):
            d.text((x + 4, y + 290 + j * 16), line, fill="white", font=font)
    S.save(out / f"sheet_{p // 12:02d}.jpg", quality=80)
