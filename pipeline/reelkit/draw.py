"""Drawing primitives: type setting, scrims, glows, and the phone mockup.

Two rules this module exists to enforce:

  * **Text is laid out, never positioned by hand.** Every string is wrapped to a
    pixel width and auto-shrunk until it fits its box, so a longer headline in a
    script file cannot silently run off the edge of the frame.
  * **Anything drawn over a photograph gets a scrim.** White type straight onto
    a bright patch of a portrait is unreadable on a phone in daylight, and it is
    the commonest reason a reel looks amateur.
"""
from __future__ import annotations

import functools
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import brand


@functools.lru_cache(maxsize=128)
def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_size(txt: str, f: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = f.getbbox(txt)
    return box[2] - box[0], box[3] - box[1]


def wrap(txt: str, f: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Greedy word wrap to a pixel width."""
    words, lines, cur = txt.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if f.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(txt: str, path: str, max_w: int, max_h: int,
              start: int, min_size: int = 28, leading: float = 1.12):
    """Shrink until the wrapped block fits `max_w` x `max_h`.

    Returns (font, lines, line_height). Guarantees a headline never overflows
    however long the script writes it.
    """
    size = start
    while size > min_size:
        f = font(path, size)
        lines = wrap(txt, f, max_w)
        lh = int(size * leading)
        if len(lines) * lh <= max_h and all(f.getlength(l) <= max_w for l in lines):
            return f, lines, lh
        size -= 2
    f = font(path, min_size)
    return f, wrap(txt, f, max_w), int(min_size * leading)


def draw_block(img: Image.Image, txt: str, *, path: str, box, start: int,
               fill=brand.TEXT_PRIMARY, align: str = "left", leading: float = 1.12,
               min_size: int = 28, shadow: bool = True):
    """Draw a wrapped, auto-fitted text block inside `box` = (x, y, w, h)."""
    x, y, w, h = box
    f, lines, lh = fit_lines(txt, path, w, h, start, min_size, leading)
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        lw = f.getlength(line)
        lx = x if align == "left" else x + (w - lw) / 2 if align == "center" else x + w - lw
        ly = y + i * lh
        if shadow:
            d.text((lx + 3, ly + 4), line, font=f, fill=(0, 0, 0, 160))
        d.text((lx, ly), line, font=f, fill=fill)
    return len(lines) * lh


def vertical_scrim(size, *, top_alpha=0, bottom_alpha=235, start=0.35,
                   colour=(6, 9, 18)) -> Image.Image:
    """A transparent-to-dark gradient, so type over a photo stays readable."""
    w, h = size
    grad = Image.new("L", (1, h), 0)
    px = grad.load()
    for y in range(h):
        t = (y / h - start) / max(1e-6, 1 - start)
        t = 0.0 if t < 0 else 1.0 if t > 1 else t
        px[0, y] = int(top_alpha + (bottom_alpha - top_alpha) * (t ** 1.5))
    alpha = grad.resize((w, h))
    layer = Image.new("RGBA", (w, h), colour + (255,))
    layer.putalpha(alpha)
    return layer


def radial_glow(size, centre, radius, colour, peak_alpha=90) -> Image.Image:
    """Soft brand glow. Built small and upscaled -- drawing it at full
    resolution costs ~40x more for a result nobody can tell apart."""
    w, h = size
    sw, sh = max(2, w // 8), max(2, h // 8)
    small = Image.new("L", (sw, sh), 0)
    d = ImageDraw.Draw(small)
    cx, cy = centre[0] * sw / w, centre[1] * sh / h
    r = radius * sw / w
    steps = 26
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(peak_alpha * (1 - i / steps) ** 1.7)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=a)
    small = small.filter(ImageFilter.GaussianBlur(sw / 22))
    layer = Image.new("RGBA", (w, h), colour + (255,))
    layer.putalpha(small.resize((w, h), Image.BILINEAR))
    return layer


def rounded_rect(size, radius, fill, *, outline=None, width=2) -> Image.Image:
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius,
                        fill=fill, outline=outline, width=width)
    return img


def drop_shadow(layer: Image.Image, *, blur=28, offset=(0, 16),
                colour=(0, 0, 0, 170)) -> Image.Image:
    """Return a canvas-sized shadow for `layer`'s alpha."""
    pad = blur * 3
    sh = Image.new("RGBA", (layer.width + pad * 2, layer.height + pad * 2), (0, 0, 0, 0))
    solid = Image.new("RGBA", layer.size, colour)
    sh.paste(solid, (pad + offset[0], pad + offset[1]), layer.split()[-1])
    return sh.filter(ImageFilter.GaussianBlur(blur))


def phone_mockup(screen: Image.Image, *, width: int = 620, radius: int = 54,
                 bezel: int = 12, glow: bool = True, aspect: float | None = None,
                 scroll: float = 0.0) -> Image.Image:
    """Put an app screen plate in a phone body.

    `aspect` is height/width of the INNER screen. It defaults to the plate's own
    aspect so the whole real screen is shown: the captures are 1290x2565 (1:1.99)
    which is RELATIVELY WIDER than a 19.5:9 handset, so forcing a handset aspect
    would crop live UI off the sides of a screenshot whose content is the point
    of the shot. Pass an aspect only when you want a deliberate crop.

    `scroll` in [0,1] picks the vertical crop offset when the plate is taller
    than the frame -- 0 is the top of the screen, 1 the bottom.
    """
    src = screen.convert("RGB")
    if aspect is None:
        aspect = src.height / src.width
    height = int(width * aspect)
    inner_w, inner_h = width - bezel * 2, height - bezel * 2

    cover = max(inner_w / src.width, inner_h / src.height)
    src = src.resize((max(1, int(src.width * cover)), max(1, int(src.height * cover))),
                     Image.LANCZOS)
    left = (src.width - inner_w) // 2
    top = int((src.height - inner_h) * min(1.0, max(0.0, scroll)))
    src = src.crop((left, top, left + inner_w, top + inner_h))

    inner = Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 0))
    inner.paste(src, (0, 0))
    mask = Image.new("L", (inner_w, inner_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, inner_w - 1, inner_h - 1], radius=max(2, radius - bezel), fill=255)
    inner.putalpha(mask)

    body = rounded_rect((width, height), radius, (18, 22, 34, 255),
                        outline=(58, 70, 92, 255), width=2)
    body.paste(inner, (bezel, bezel), inner)

    if not glow:
        return body
    pad = 70
    out = Image.new("RGBA", (width + pad * 2, height + pad * 2), (0, 0, 0, 0))
    halo = rounded_rect((width + 22, height + 22), radius + 11, brand.ACCENT + (58,))
    halo = halo.filter(ImageFilter.GaussianBlur(26))
    out.alpha_composite(halo, (pad - 11, pad - 11))
    out.alpha_composite(body, (pad, pad))
    return out


def pill(text: str, *, path: str = brand.BODY_BOLD, size: int = 30,
         fg=brand.ACCENT, bg=(19, 28, 50, 230), pad=(26, 14), radius=None):
    f = font(path, size)
    tw, th = text_size(text, f)
    w, h = tw + pad[0] * 2, th + pad[1] * 2 + 6
    img = rounded_rect((w, h), radius if radius is not None else h // 2, bg,
                       outline=brand.ACCENT + (70,), width=2)
    d = ImageDraw.Draw(img)
    box = f.getbbox(text)
    d.text((pad[0] - box[0], (h - th) / 2 - box[1]), text, font=f, fill=fg)
    return img


def plate_card(plate: Image.Image, region, *, width: int = 470, radius: int = 26,
               label: str | None = None, glow: bool = True) -> Image.Image:
    """A CROPPED REGION of an app screen, as a small card.

    The inset on a `talk` scene cannot be a whole phone. A 1290x2565 screenshot
    shrunk to inset width puts the app's body text at about six pixels, so the
    viewer sees a phone-shaped blur and takes the claim on trust -- which is the
    one thing `COMPLIANCE.md` exists to stop, since the whole point of pointing
    at a screen is that the viewer can read it.

    So the inset shows ONE row of the screen at a legible size. `region` is
    (x0, y0, x1, y1) normalised on the plate, which survives a re-capture at a
    different device resolution; pixel coordinates would not.
    """
    x0, y0, x1, y1 = region
    box = (int(x0 * plate.width), int(y0 * plate.height),
           int(x1 * plate.width), int(y1 * plate.height))
    crop = plate.convert("RGB").crop(box)
    h = max(1, int(width * crop.height / crop.width))
    crop = crop.resize((width, h), Image.LANCZOS)

    card = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    card.paste(crop, (0, 0))
    mask = Image.new("L", (width, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, width - 1, h - 1],
                                           radius=radius, fill=255)
    card.putalpha(mask)
    frame = rounded_rect((width, h), radius, (0, 0, 0, 0),
                         outline=brand.ACCENT + (110,), width=2)
    card.alpha_composite(frame)

    if label:
        f = font(brand.BODY_BOLD, 26)
        tw, th = text_size(label, f)
        strip = rounded_rect((tw + 34, th + 22), (th + 22) // 2,
                             brand.BG_DEEP + (238,), outline=brand.ACCENT + (90,))
        d = ImageDraw.Draw(strip)
        bb = f.getbbox(label)
        d.text((17 - bb[0], (th + 22 - th) / 2 - bb[1]), label, font=f,
               fill=brand.ACCENT + (255,))
        out = Image.new("RGBA", (max(width, strip.width), h + strip.height + 14),
                        (0, 0, 0, 0))
        out.alpha_composite(card, (0, strip.height + 14))
        out.alpha_composite(strip, (0, 0))
        card = out

    if not glow:
        return card
    pad = 60
    out = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    out.alpha_composite(drop_shadow(card, blur=30, offset=(0, 14)),
                        (pad - 90, pad - 90))
    out.alpha_composite(card, (pad, pad))
    return out
