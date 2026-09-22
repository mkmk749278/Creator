#!/usr/bin/env python3
"""Render a reel's opening scene as a CLEAN cover still -- no burned captions.

The pipeline's own `_poster.jpg` is grabbed after the caption layer is
composited, so it always carries a half-spoken line across the bottom. That is
right for a feed thumbnail of an organic reel and wrong for a paid placement,
where the cover is uploaded separately and is the first thing a cold viewer
sees. This re-renders scene 0 through the same renderer with the caption layer
simply not applied, so the cover is pixel-identical to the frame the ad opens
on, minus the text.

    python3 pipeline/make_ad_cover.py reels/10_meta_ad_signals [--at 0.9]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reelkit import scenes  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reel")
    ap.add_argument("--at", type=float, default=0.9,
                    help="seconds into the opening scene")
    ap.add_argument("--dur", type=float, default=2.1,
                    help="the opening scene's resolved duration, for the camera move")
    args = ap.parse_args()

    reel = pathlib.Path(args.reel)
    script = json.loads((reel / "script.json").read_text(encoding="utf-8"))
    frame = scenes.render(script["scenes"][0], args.at, args.dur)

    out = reel / "out" / f"{script['id']}_cover.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    frame.save(out, quality=95, subsampling=0)
    print(f"  -> {out}  {frame.size[0]}x{frame.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
