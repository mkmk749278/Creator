#!/usr/bin/env python3
"""Crop raw sources to the usable picture (films/<slug>/media/crops.json) → films/<slug>/assets/media/<id>.jpg.

  python3 scripts/media_prep.py films/tata-history
Stereo cards keep one frame inside the arch; scans lose their borders. Output is never upscaled (a crop narrower than
1920 px is reported, so the scene can use it smaller or not at all).
"""
import json
import sys
from pathlib import Path

from PIL import Image

film = Path(sys.argv[1])
crops = json.loads((film / "media/crops.json").read_text())
src_root = film / "assets/media"
for aid, spec in crops.items():
    if aid.startswith("_"):
        continue
    src, (x0, y0, x1, y1) = spec
    im = Image.open(src_root / src).convert("RGB")
    w, h = im.size
    c = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    c.save(src_root / f"{aid}.jpg", quality=94)
    flag = "  (narrow for 4K)" if c.size[0] < 1920 else ""
    print(f"{aid}: {c.size[0]}x{c.size[1]}{flag}")
