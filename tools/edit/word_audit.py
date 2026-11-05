#!/usr/bin/env python3
# Reusable tool kept from an earlier film (repo slimmed 2026-11-05): adapt the paths at the top to the new film.
"""Shot-by-word audit (CLAUDE.md semantic lock): one frame 0.45 s after every word-level cutaway in make_film.py,
labelled with the word and the picture, on sheets of 24 (qa/word_audit_N.jpg). usage: python3 build/word_audit.py"""
import json, re, subprocess, sys, glob, shutil, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]
sys.path.insert(0, str(P / "build"))
import make_film as M  # noqa: E402  (builds the cut in memory; emit() only runs as __main__)
src = (P / "build/make_film.py").read_text()
rows = []
for m in re.finditer(r'^\s*ins\(W\((\d+), "([^"]+)"(?:, (\d))?\), ("[^"]+"|[^,]+),', src, re.M):
    n, w, k = int(m.group(1)), m.group(2), int(m.group(3) or 0)
    rows.append((M.W(n, w, k) + 0.45, f"L{n} '{w}' -> {m.group(4).strip(chr(34))[:22]}"))
for lw in ["Hindi", "Marathi", "Telugu", "Bengali", "Odia"]:
    rows.append((M.W(83, lw) + 0.3, f"L83 '{lw}'"))
rows.sort()
parts = json.loads((P / "build/parts.json").read_text())
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
tmp = Path(tempfile.mkdtemp()); got = []
for k in range(len(parts) - 1):
    tl = [(t, lab) for t, lab in rows if parts[k] <= t < parts[k + 1]]
    if not tl: continue
    d = ROOT / f"video/aig/p{k + 1}"; o = tmp / f"p{k + 1}"
    subprocess.run(["npx", "hyperframes", "snapshot", str(d), "--at", ",".join(f"{t - parts[k]:.2f}" for t, _ in tl), "--no-end", "-o", str(o),
                    "--timeout", "20000"], capture_output=True, cwd=d)
    got += list(zip(tl, sorted(glob.glob(str(o / "frame-*.png")))))
(P / "qa").mkdir(exist_ok=True)
for s in range(0, len(got), 24):
    chunk = got[s:s + 24]; sh = Image.new('RGB', (480 * 4, 300 * ((len(chunk) + 3) // 4)), 'black'); dr = ImageDraw.Draw(sh)
    for i, ((t, lab), f) in enumerate(chunk):
        x, y = (i % 4) * 480, (i // 4) * 300; sh.paste(Image.open(f).convert('RGB').resize((480, 270)), (x, y))
        dr.text((x + 4, y + 272), f"{int(t // 60)}:{t % 60:04.1f} {lab}", fill='yellow', font=F)
    sh.save(P / f"qa/word_audit_{s // 24 + 1}.jpg", quality=78)
shutil.rmtree(tmp); print(len(got), "frames")
