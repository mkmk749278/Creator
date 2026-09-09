#!/usr/bin/env python3
"""Render one reel, or every reel, from its script.json.

    python3 pipeline/render_reel.py reels/01_what_is_lumin
    python3 pipeline/render_reel.py --all
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from reelkit.build import build           # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reel", nargs="?", help="path to a reel directory")
    ap.add_argument("--all", action="store_true", help="render every reel")
    args = ap.parse_args()

    if args.all:
        targets = sorted(p for p in (ROOT / "reels").iterdir()
                         if (p / "script.json").exists())
    elif args.reel:
        targets = [pathlib.Path(args.reel)]
    else:
        ap.error("give a reel directory or --all")

    if not targets:
        print("no reel scripts found", file=sys.stderr)
        return 2
    for t in targets:
        build(t / "script.json" if t.is_dir() else t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
