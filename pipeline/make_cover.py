#!/usr/bin/env python3
"""Compose the ad's opening hero plate from a character still.

Why this exists: the supplied hero stills frame Lia with her head about 2% from
the top edge, so EVERY crop of them puts her face in the top third -- which is
exactly where a reel's hook headline goes. Reels 01 and 02 both ended up
setting type over her forehead. Rather than accept that, this builds a
1080x1920 plate with real headroom: the portrait sits lower on a brand
backdrop, its top edge feathered into the navy, so the headline lands in clean
space above her face instead of on it.

The grade is deliberately mild -- warm mids, a small contrast lift, a bloom on
the highlights and a vignette. It is a beauty pass, not a re-render: the face
is the owner's supplied character and must stay recognisably the same person.

    python3 pipeline/make_cover.py
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reelkit import brand, draw  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "character"


def grade(img: Image.Image) -> Image.Image:
    """Warm, lift, bloom. Mild by design -- see the module docstring."""
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0

    # Warm the mid-tones: push R up and B down, weighted by how mid a pixel is.
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    mid = (1.0 - np.abs(lum - 0.5) * 2.0)[..., None]          # 1 at mid, 0 at ends
    a[..., 0] += 0.030 * mid[..., 0]
    a[..., 2] -= 0.018 * mid[..., 0]

    # Gentle S-curve for contrast without crushing the shadows.
    a = np.clip(a, 0, 1)
    a = a * a * (3.0 - 2.0 * a) * 0.34 + a * 0.66
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

    img = ImageEnhance.Color(img).enhance(1.07)

    # Bloom: blur the top end of the range back over the image. This is what
    # makes skin read as lit rather than merely bright.
    hi = img.point(lambda v: max(0, v - 168) * 3)
    img = Image.blend(img, Image.blend(img, hi.filter(
        ImageFilter.GaussianBlur(26)), 0.5), 0.26)
    return img


def vignette(img: Image.Image, strength: float = 0.42) -> Image.Image:
    w, h = img.size
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((x / w - 0.5) / 0.62) ** 2 + ((y / h - 0.52) / 0.70) ** 2)
    m = np.clip(1.0 - strength * np.clip(r - 0.55, 0, None) ** 1.5 * 3.0, 0.28, 1.0)
    a = np.asarray(img.convert("RGB")).astype(np.float32) * m[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def build(src_name: str, out_name: str, *, face_y: int, scale_w: int,
          shift_x: int = 0, feather: int = 260) -> pathlib.Path:
    """Place `src_name` on a 1080x1920 brand plate with headroom above the face.

    `face_y` is where the subject's eyeline should land in the final frame;
    `scale_w` how wide the portrait is drawn. Both are picked by eye from the
    preview, which is the only honest way to frame a face.
    """
    src = Image.open(SRC / src_name).convert("RGB")

    # Eyeline in the source, measured once from the supplied still.
    EYE = {"lia_hero_laptop.png": (0.255, 0.121),
           "lia_hero_desk.png": (0.470, 0.235)}[src_name]

    s = scale_w / src.width
    port = src.resize((scale_w, int(src.height * s)), Image.LANCZOS)
    port = grade(port)

    px = int(EYE[0] * scale_w)
    py = int(EYE[1] * port.height)
    ox = (brand.W - scale_w) // 2 + shift_x - (px - scale_w // 2)
    oy = face_y - py
    # The portrait must COVER the canvas horizontally. Centring on the eyeline
    # alone slid the laptop still 251px to the right and left a hard navy band
    # down the left edge -- a pasted-on look that no grade rescues.
    ox = min(0, max(brand.W - layer_w, ox)) if (layer_w := scale_w) >= brand.W else ox

    base = Image.new("RGB", (brand.W, brand.H), brand.BG_DEEP).convert("RGBA")
    base.alpha_composite(draw.radial_glow((brand.W, brand.H), (250, 430), 820,
                                          brand.ACCENT, peak_alpha=62))
    base.alpha_composite(draw.radial_glow((brand.W, brand.H), (880, 1560), 760,
                                          brand.ACCENT_MUTED, peak_alpha=50))

    # Feather the portrait's top edge into the backdrop so the added headroom
    # reads as atmosphere rather than as a photo pasted onto a gradient.
    layer = port.convert("RGBA")
    mask = Image.new("L", layer.size, 255)
    if oy < 0:
        pass
    grad = Image.new("L", (1, max(1, feather)), 0)
    gp = grad.load()
    for i in range(max(1, feather)):
        gp[0, i] = int(255 * (i / max(1, feather - 1)) ** 0.85)
    mask.paste(grad.resize((layer.width, max(1, feather))), (0, 0))
    layer.putalpha(mask)

    base.alpha_composite(layer, (ox, oy))
    out = vignette(base.convert("RGB"))

    dst = SRC / out_name
    out.save(dst)
    print(f"  {src_name} -> {out_name}  eyeline y={face_y}  width={scale_w}")
    return dst


def main() -> int:
    print("composing cover plates")
    build("lia_hero_laptop.png", "lia_cover_open.png",
          face_y=660, scale_w=1420, shift_x=150)
    build("lia_hero_desk.png", "lia_cover_close.png",
          face_y=700, scale_w=1210, shift_x=30)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
