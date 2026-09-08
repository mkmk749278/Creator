"""Easing and camera moves.

Every move in a reel is eased. Linear motion is the single clearest tell that a
video was assembled by a script rather than shot, and it costs one function to
avoid.
"""
from __future__ import annotations

import math


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if v < lo else hi if v > hi else v


def ease_out_cubic(t: float) -> float:
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def ease_out_back(t: float, s: float = 1.70158) -> float:
    """Slight overshoot -- used for a word popping onto screen."""
    t = clamp(t)
    return 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2


def ease_out_expo(t: float) -> float:
    t = clamp(t)
    return 1.0 if t >= 1 else 1 - math.pow(2, -10 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def ken_burns(img, t: float, *, zoom_from=1.14, zoom_to=1.0,
              pan_from=(0.5, 0.5), pan_to=(0.5, 0.5), size=(1080, 1920),
              ease=ease_in_out_cubic):
    """Crop `img` to `size` with an eased zoom + pan at progress `t` in [0,1].

    The image is first scaled to COVER the target at zoom 1.0, so any zoom >= 1
    still has real pixels to show and never letterboxes. Pan is expressed as the
    normalised centre of the crop, which keeps a subject's face anchored while
    the frame moves around it.
    """
    from PIL import Image

    tw, th = size
    e = ease(t)
    zoom = lerp(zoom_from, zoom_to, e)
    px = lerp(pan_from[0], pan_to[0], e)
    py = lerp(pan_from[1], pan_to[1], e)

    cover = max(tw / img.width, th / img.height) * zoom
    sw, sh = max(1, int(img.width * cover)), max(1, int(img.height * cover))
    scaled = img.resize((sw, sh), Image.LANCZOS)

    left = int((sw - tw) * clamp(px))
    top = int((sh - th) * clamp(py))
    return scaled.crop((left, top, left + tw, top + th))
