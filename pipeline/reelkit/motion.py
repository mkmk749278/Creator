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


def handheld(t: float, *, seed: int = 0, amp: float = 1.0
             ) -> tuple[float, float, float]:
    """A camera operator's breathing, as (dx_px, dy_px, dzoom) at time `t`.

    A still portrait held for four seconds under a smooth Ken Burns move reads
    as a slideshow, and the tell is that the motion is perfectly monotonic --
    nothing a hand holds ever moves in one direction at a constant rate. Three
    sines at deliberately incommensurate frequencies never repeat inside a
    reel's length, so the shot does not visibly loop.

    Amplitudes are in PIXELS rather than in normalised pan units on purpose: a
    normalised offset means a different distance on every source image, so the
    same number would read as a twitch on one portrait and as nothing at all on
    another. `ken_burns` clamps these to the real headroom, which is why the
    caller must also pass a `zoom_floor` -- see that argument.
    """
    ph = seed * 1.7
    dx = amp * (3.4 * math.sin(2 * math.pi * 0.23 * t + ph)
                + 1.6 * math.sin(2 * math.pi * 0.41 * t + ph * 2.1))
    dy = amp * (4.1 * math.sin(2 * math.pi * 0.19 * t + ph * 1.3)
                + 1.9 * math.sin(2 * math.pi * 0.31 * t + ph * 0.7))
    dz = amp * 0.004 * math.sin(2 * math.pi * 0.13 * t + ph * 1.9)
    return dx, dy, dz


def ken_burns(img, t: float, *, zoom_from=1.14, zoom_to=1.0,
              pan_from=(0.5, 0.5), pan_to=(0.5, 0.5), size=(1080, 1920),
              ease=ease_in_out_cubic, jitter=(0.0, 0.0), zoom_floor=1.0):
    """Crop `img` to `size` with an eased zoom + pan at progress `t` in [0,1].

    The image is first scaled to COVER the target at zoom 1.0, so any zoom >= 1
    still has real pixels to show and never letterboxes. Pan is expressed as the
    normalised centre of the crop, which keeps a subject's face anchored while
    the frame moves around it.

    `zoom_floor` exists because COVER is not the same amount of headroom on both
    axes. A 2:3 portrait into a 9:16 frame scales by 1.25 to cover, which leaves
    200px spare horizontally and **exactly zero** vertically -- so at zoom 1.0 a
    vertical pan silently does nothing, and so does a vertical `jitter`. A floor
    just above 1.0 buys the few pixels the wobble needs. Clamping the jitter to
    the headroom that does exist is deliberate: this is a decorative move, so a
    frame edge should cost amplitude rather than refuse the shot.
    """
    from PIL import Image

    tw, th = size
    e = ease(t)
    zoom = max(zoom_floor, lerp(zoom_from, zoom_to, e))
    px = lerp(pan_from[0], pan_to[0], e)
    py = lerp(pan_from[1], pan_to[1], e)

    cover = max(tw / img.width, th / img.height) * zoom
    sw, sh = max(1, int(img.width * cover)), max(1, int(img.height * cover))
    scaled = img.resize((sw, sh), Image.LANCZOS)

    left = int((sw - tw) * clamp(px) + jitter[0])
    top = int((sh - th) * clamp(py) + jitter[1])
    left = max(0, min(sw - tw, left))
    top = max(0, min(sh - th, top))
    return scaled.crop((left, top, left + tw, top + th))
