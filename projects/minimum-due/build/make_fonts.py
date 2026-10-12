#!/usr/bin/env python3
"""Label fonts for assemble.py (ffmpeg drawtext needs TTF): Bricolage Grotesque 800 (latin + latin-ext merged, for ₹) and
JetBrains Mono 700, converted from the pinned @fontsource packages into assets/fonts/. Needs fonttools + brotli (.venv)."""
from pathlib import Path
from fontTools.merge import Merger
from fontTools.ttLib import TTFont

P = Path(__file__).resolve().parents[1]; NM = P.parents[1] / "node_modules/@fontsource"; OUT = P / "assets/fonts"
OUT.mkdir(parents=True, exist_ok=True)


def ttf(src, dst):
    f = TTFont(src); f.flavor = None; f.save(dst); return str(dst)


parts = [ttf(NM / f"bricolage-grotesque/files/bricolage-grotesque-{s}-800-normal.woff2", OUT / f"_b_{s}.ttf") for s in ("latin", "latin-ext")]
Merger().merge(parts).save(OUT / "Bricolage-800.ttf")
for p in parts:
    Path(p).unlink()
ttf(NM / "jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2", OUT / "JetBrainsMono-700.ttf")
print("fonts in", OUT)
