#!/usr/bin/env python3
"""Render every proof region so the crops can be READ, not trusted.

A region that has slid half a row off its claim after a re-capture still
renders a perfectly convincing card -- of the wrong sentence. So this writes
one PNG per claim and a contact sheet, and looking at the sheet is the check.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from PIL import Image                              # noqa: E402
from reelkit import brand, draw, proof             # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "capture" / "app" / "proofs"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cards = []
    for key, (screen, region, label) in sorted(proof.PROOF.items()):
        path = brand.CAPTURE_DIR / "screens" / screen
        if not path.exists():
            print(f"  ! {key}: missing plate {screen}")
            return 1
        card = draw.plate_card(Image.open(path), region, width=520,
                               label=f"{key}  ·  {label}")
        card.save(OUT / f"{key}.png")
        cards.append(card)
        print(f"  {key:<20} {screen:<28} {region}")

    w = max(c.width for c in cards)
    sheet = Image.new("RGB", (w, sum(c.height for c in cards)), brand.BG_DEEP)
    y = 0
    for c in cards:
        sheet.paste(c, (0, y), c)
        y += c.height
    sheet.save(OUT / "_contact_sheet.jpg", quality=92)
    print(f"\n  -> {OUT/'_contact_sheet.jpg'}  ({len(cards)} claims) -- LOOK AT IT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
