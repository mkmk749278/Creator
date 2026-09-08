#!/usr/bin/env python3
"""Turn raw captures into clean screen plates for the reels.

The only transformation is a crop of the PWA "Install Lumin on your iPhone"
banner from the top of every frame. That banner is a WEB-channel artefact -- it
does not exist in the Play Store build the reels are advertising, so leaving it
in would put a install-the-web-app prompt in an ad for the Android app.

Nothing else is retouched. These plates are real screens from a real signed-in
session; no number in them is redrawn.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

from PIL import Image

BANNER_H = 225          # measured on the 1290x2790 (DSF 3) captures
SRC = pathlib.Path("/home/user/Creator/capture/app/shots")
DST = pathlib.Path("/home/user/Creator/capture/app/screens")

# The plates worth keeping, and what each is for. Deliberately EXCLUDES the
# Pulse P&L panels: they carry a live realised-P&L figure, and putting a
# performance number in an ad is both a claim we would have to stand behind and
# a thing 360-v2's own doctrine forbids fabricating or implying.
KEEP = {
    "02_onboard_1.png": "onboard_how_it_works",
    "03_onboard_2.png": "onboard_funds_safe",
    "04_onboard_3.png": "onboard_consent",
    "14_tab_signals.png": "signals_list",
    "15_tab_signals_scrolled.png": "signals_list_scrolled",
    "18_tab_trade.png": "trade_connect",
    "20_tab_menu.png": "menu_controls",
    "21_tab_menu_scrolled.png": "menu_controls_scrolled",
    "12_tab_pulse.png": "pulse_dashboard",
}


def main() -> int:
    if not SRC.exists():
        print(f"no captures at {SRC} -- run pipeline/capture_app.py first", file=sys.stderr)
        return 2
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    n = 0
    for src_name, out_name in KEEP.items():
        f = SRC / src_name
        if not f.exists():
            print(f"  missing {src_name} (skipped)")
            continue
        im = Image.open(f).convert("RGB")
        im = im.crop((0, BANNER_H, im.width, im.height))
        im.save(DST / f"{out_name}.png")
        print(f"  {src_name:32s} -> {out_name}.png  {im.size}")
        n += 1
    print(f"\n{n} screen plates -> {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
