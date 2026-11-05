#!/usr/bin/env python3
# Reusable tool kept from an earlier film (repo slimmed 2026-11-05): adapt the paths at the top to the new film.
"""Snapshot the built parts at film times and lay them out as one labelled sheet (look before rendering).
usage: python3 build/snap.py OUT.jpg T1 T2 ...  (film seconds)"""
import json, subprocess, sys, glob, os, shutil, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]
parts = json.loads((P / "build/parts.json").read_text()); out = sys.argv[1]; ts = [float(x) for x in sys.argv[2:]]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
shots = []
by = {}
for t in ts:
    k = max(i for i in range(len(parts) - 1) if parts[i] <= t); by.setdefault(k, []).append(t)
tmp = Path(tempfile.mkdtemp())
for k, tl in by.items():
    d = ROOT / f"video/aig/p{k + 1}"; o = tmp / f"p{k + 1}"
    loc = ",".join(f"{t - parts[k]:.2f}" for t in tl)
    subprocess.run(["npx", "hyperframes", "snapshot", str(d), "--at", loc, "--no-end", "-o", str(o), "--timeout", "20000"], capture_output=True, cwd=d)
    fs = sorted(glob.glob(str(o / "frame-*.png")))
    shots += list(zip(tl, fs))
shots.sort()
th = [(t, Image.open(f).convert('RGB').resize((640, 360))) for t, f in shots]
sh = Image.new('RGB', (640 * 3, 370 * ((len(th) + 2) // 3)), 'black'); dr = ImageDraw.Draw(sh)
for i, (t, im) in enumerate(th):
    x, y = (i % 3) * 640, (i // 3) * 370; sh.paste(im, (x, y)); dr.text((x + 6, y + 6), f"{int(t // 60)}:{t % 60:04.1f}", fill='yellow', font=F)
sh.save(out, quality=80); shutil.rmtree(tmp); print(out, len(th))
