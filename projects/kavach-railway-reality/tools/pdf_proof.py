#!/usr/bin/env python3
"""PROOF frame from a PDF page (the HTML twin of tools/proof_shots.js, for sources that only exist as PDFs).

  python3 tools/pdf_proof.py SRC.pdf PAGE "exact quote on one line" OUT_ID

Renders PAGE at 300 dpi (pdftoppm), finds the quote's words with pdftotext -bbox, highlights them in the same yellow as
proof_shots.js, centres the page on a 3840×2160 slate canvas around the highlight, and writes assets/proof/OUT_ID.png
plus OUT_ID.json (the highlight box as frame fractions, used by assemble.py for the push-in).
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

pdf, page, quote, out_id = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
OUT = Path(__file__).resolve().parent.parent / "assets" / "proof"
tmp = Path(tempfile.mkdtemp())
subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox", pdf, str(tmp / "b.html")], check=True)
subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "300", "-png", "-singlefile", pdf, str(tmp / "p")], check=True)
s = (tmp / "b.html").read_text()
pw = float(re.search(r'<page width="([\d.]+)"', s).group(1))
words = [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in
         re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', s)]
target = quote.split()
hit = next((words[i:i + len(target)] for i in range(len(words)) if [w[4] for w in words[i:i + len(target)]] == target), None)
if not hit:
    sys.exit(f"quote not found on page {page}")
im = Image.open(tmp / "p.png").convert("RGBA")
k = im.width / pw
x0, y0 = min(w[0] for w in hit) * k - 6, min(w[1] for w in hit) * k - 4
x1, y1 = max(w[2] for w in hit) * k + 6, max(w[3] for w in hit) * k + 4
ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
ImageDraw.Draw(ov).rounded_rectangle([x0, y0, x1, y1], 8, fill=(255, 230, 0, 150))
im = Image.alpha_composite(im, ov).convert("RGB")
W, H = 3840, 2160
pgw = int(W * 0.62); sc = pgw / im.width
pg = im.resize((pgw, int(im.height * sc)), Image.LANCZOS)
top = max(min(int(H / 2 - (y0 + y1) / 2 * sc), 0), H - pg.height)
px = (W - pgw) // 2
bg = Image.new("RGB", (W, H), (11, 14, 20)); bg.paste(pg, (px, top))
bg.save(OUT / f"{out_id}.png")
box = dict(x0=(px + x0 * sc) / W, y0=(top + y0 * sc) / H, x1=(px + x1 * sc) / W, y1=(top + y1 * sc) / H)
(OUT / f"{out_id}.json").write_text(json.dumps(box))
print(out_id, box)
