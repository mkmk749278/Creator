"""Scene renderers. Each returns one finished 1080x1920 RGB frame.

A scene is a pure function of (spec, local time). Nothing is stateful between
frames, so any frame can be re-rendered on its own -- which is what makes it
cheap to dump a single frame and actually look at it while building a reel,
rather than encoding 25 seconds to find out a headline is clipped.
"""
from __future__ import annotations

import functools
import pathlib

from PIL import Image, ImageDraw, ImageFilter

from . import brand, draw, motion


@functools.lru_cache(maxsize=32)
def load(path: str) -> Image.Image:
    return Image.open(path).convert("RGB")


@functools.lru_cache(maxsize=8)
def backdrop(seed: int = 0) -> Image.Image:
    """Brand background: deep navy with two soft accent glows.

    Cached because it is identical on every frame -- regenerating the glows per
    frame costs more than everything else in the renderer combined.
    """
    bg = Image.new("RGB", (brand.W, brand.H), brand.BG_DEEP)
    bg = bg.convert("RGBA")
    bg.alpha_composite(draw.radial_glow((brand.W, brand.H), (250, 420), 780,
                                        brand.ACCENT, peak_alpha=58))
    bg.alpha_composite(draw.radial_glow((brand.W, brand.H), (900, 1520), 720,
                                        brand.ACCENT_MUTED, peak_alpha=48))
    return bg.convert("RGB")


def _pills(img: Image.Image, labels, y: int, *, gap: int = 18):
    if not labels:
        return
    tiles = [draw.pill(l) for l in labels]
    total = sum(t.width for t in tiles) + gap * (len(tiles) - 1)
    x = (brand.W - total) // 2
    for t in tiles:
        img.alpha_composite(t, (x, y))
        x += t.width + gap


def _kicker(img: Image.Image, text: str, y: int):
    f = draw.font(brand.BODY_BOLD, 34)
    d = ImageDraw.Draw(img)
    w = f.getlength(text)
    d.text(((brand.W - w) / 2, y), text, font=f, fill=brand.ACCENT + (255,))


def character(spec: dict, t: float, dur: float) -> Image.Image:
    """Full-bleed portrait with an eased camera move and a readable scrim."""
    img = load(str(brand.CHARACTER_DIR / spec["image"]))
    p = t / max(1e-6, dur)
    # Default framing is deliberately WIDE. The first cut used zoom 1.15 with a
    # low pan, which sliced the top of the subject's head off -- the classic
    # tell of an auto-cropped portrait. The source is 2:3 and the frame is 9:16,
    # so the cover scale is already 1.25x before any zoom is applied.
    zf, zt = spec.get("zoom", [1.06, 1.0])
    pf, pt = spec.get("pan", [[0.5, 0.22], [0.5, 0.27]])
    frame = motion.ken_burns(img, p, zoom_from=zf, zoom_to=zt,
                             pan_from=tuple(pf), pan_to=tuple(pt),
                             size=(brand.W, brand.H)).convert("RGBA")

    if spec.get("scrim", True):
        frame.alpha_composite(draw.vertical_scrim(
            (brand.W, brand.H), bottom_alpha=spec.get("scrim_alpha", 232),
            start=spec.get("scrim_start", 0.34)))
        # Top scrim: keeps the kicker and any top headline legible. Its depth is
        # tunable because a two-line headline and a three-line one need very
        # different amounts of cover, and a headline running onto a lit face is
        # the fastest way to make a reel look thrown together.
        top = draw.vertical_scrim(
            (brand.W, spec.get("scrim_top_h", 460)),
            top_alpha=spec.get("scrim_top_alpha", 185), bottom_alpha=0, start=0.0)
        frame.alpha_composite(top, (0, 0))

    if spec.get("kicker"):
        _kicker(frame, spec["kicker"], spec.get("kicker_y", 250))
    if spec.get("headline"):
        draw.draw_block(frame, spec["headline"], path=brand.DISPLAY,
                        box=(brand.SAFE_X, spec.get("headline_y", 300),
                             brand.W - brand.SAFE_X * 2, 430),
                        start=spec.get("headline_size", 92),
                        align=spec.get("align", "left"))
    if spec.get("sub"):
        draw.draw_block(frame, spec["sub"], path=brand.BODY,
                        box=(brand.SAFE_X, spec.get("sub_y", 600),
                             brand.W - brand.SAFE_X * 2, 200),
                        start=40, fill=brand.TEXT_SECONDARY,
                        align=spec.get("align", "left"))
    _pills(frame, spec.get("pills"), spec.get("pills_y", 1420))
    return frame.convert("RGB")


def phone(spec: dict, t: float, dur: float) -> Image.Image:
    """App screen in a phone body over the brand backdrop.

    Multiple `screens` crossfade across the scene, which is how a scroll or a
    tab change reads without faking a scroll the capture cannot support.
    """
    p = t / max(1e-6, dur)
    frame = backdrop().copy().convert("RGBA")

    names = spec.get("screens") or [spec["screen"]]
    plates = [load(str(brand.CAPTURE_DIR / "screens" / n)) for n in names]
    if len(plates) == 1:
        plate = plates[0]
    else:
        seg = 1.0 / (len(plates) - 1)
        i = min(len(plates) - 2, int(p / seg))
        local = (p - i * seg) / seg
        # Hold, then a quick dissolve -- a slow crossfade of two near-identical
        # screens looks like a rendering fault rather than an edit.
        a = motion.ease_in_out_cubic(min(1.0, max(0.0, (local - 0.62) / 0.30)))
        plate = Image.blend(plates[i], plates[i + 1], a)

    zf, zt = spec.get("push", [1.0, 1.06])
    scale = motion.lerp(zf, zt, motion.ease_in_out_cubic(p))
    width = int(spec.get("width", 640) * scale)
    body = draw.phone_mockup(plate, width=width, scroll=spec.get("scroll", 0.0))

    # Gentle vertical drift so a static screenshot is never truly still.
    drift = int(motion.lerp(0, spec.get("drift", -26), motion.ease_in_out_cubic(p)))
    cx = brand.W // 2 - body.width // 2
    cy = spec.get("y", 470) - int((body.height - 1372) / 2) + drift
    frame.alpha_composite(body, (cx, cy))

    if spec.get("kicker"):
        _kicker(frame, spec["kicker"], spec.get("kicker_y", 250))
    if spec.get("headline"):
        draw.draw_block(frame, spec["headline"], path=brand.DISPLAY,
                        box=(brand.SAFE_X, spec.get("headline_y", 300),
                             brand.W - brand.SAFE_X * 2, 220),
                        start=spec.get("headline_size", 74), align="center")
    _pills(frame, spec.get("pills"), spec.get("pills_y", 1450))
    return frame.convert("RGB")


def duo(spec: dict, t: float, dur: float) -> Image.Image:
    """Character and app in one frame -- the shot that ties a face to a product."""
    p = t / max(1e-6, dur)
    frame = backdrop().copy().convert("RGBA")

    portrait = load(str(brand.CHARACTER_DIR / spec["image"]))
    zf, zt = spec.get("zoom", [1.06, 1.0])
    pf, pt = spec.get("pan", [[0.34, 0.20], [0.40, 0.25]])
    plate = motion.ken_burns(portrait, p, zoom_from=zf, zoom_to=zt,
                             pan_from=tuple(pf), pan_to=tuple(pt),
                             size=(brand.W, brand.H)).convert("RGBA")
    plate.alpha_composite(draw.vertical_scrim((brand.W, brand.H),
                                              bottom_alpha=238, start=0.24))
    plate.alpha_composite(draw.vertical_scrim(
        (brand.W, spec.get("scrim_top_h", 470)),
        top_alpha=spec.get("scrim_top_alpha", 190), bottom_alpha=0, start=0.0), (0, 0))
    frame.alpha_composite(plate)

    screen = load(str(brand.CAPTURE_DIR / "screens" / spec["screen"]))
    slide = motion.ease_out_expo(min(1.0, p / 0.42))
    body = draw.phone_mockup(screen, width=spec.get("width", 476),
                             scroll=spec.get("scroll", 0.0))
    x = int(motion.lerp(brand.W + 40, spec.get("x", 548), slide))
    frame.alpha_composite(body, (x, spec.get("y", 700)))

    if spec.get("kicker"):
        _kicker(frame, spec["kicker"], spec.get("kicker_y", 240))
    if spec.get("headline"):
        draw.draw_block(frame, spec["headline"], path=brand.DISPLAY,
                        box=(brand.SAFE_X, spec.get("headline_y", 300), 600, 360),
                        start=spec.get("headline_size", 76))
    return frame.convert("RGB")


def card(spec: dict, t: float, dur: float) -> Image.Image:
    """Full-bleed statement card -- hooks and turns."""
    p = t / max(1e-6, dur)
    frame = backdrop().copy().convert("RGBA")

    rise = motion.ease_out_expo(min(1.0, p / 0.34))
    dy = int((1 - rise) * 44)

    y = spec.get("headline_y", 700) + dy
    if spec.get("kicker"):
        _kicker(frame, spec["kicker"], y - 110)
    used = draw.draw_block(frame, spec["headline"], path=brand.DISPLAY_HEAVY,
                           box=(brand.SAFE_X, y, brand.W - brand.SAFE_X * 2, 620),
                           start=spec.get("headline_size", 116), align="center",
                           leading=1.06)
    if spec.get("sub"):
        draw.draw_block(frame, spec["sub"], path=brand.BODY,
                        box=(brand.SAFE_X + 30, y + used + 36,
                             brand.W - (brand.SAFE_X + 30) * 2, 220),
                        start=42, fill=brand.TEXT_SECONDARY, align="center")
    _pills(frame, spec.get("pills"), spec.get("pills_y", 1400))
    return frame.convert("RGB")


def end(spec: dict, t: float, dur: float) -> Image.Image:
    """Closing frame: mark, one instruction, one handle, the risk line."""
    p = t / max(1e-6, dur)
    frame = backdrop().copy().convert("RGBA")

    pop = motion.ease_out_back(min(1.0, p / 0.42))
    size = int(210 * motion.clamp(pop, 0.2, 1.25))
    # The REAL app icon, taken from the built web bundle, not a redrawn "L".
    # An ad that ends on an approximation of the icon teaches the viewer to look
    # for the wrong thing in the Play Store.
    icon_path = pathlib.Path(brand.CHARACTER_DIR).parent / "brand" / "lumin_icon_512.png"
    if icon_path.exists():
        mark = load(str(icon_path)).convert("RGBA").resize((size, size), Image.LANCZOS)
        rounded = Image.new("L", (size, size), 0)
        ImageDraw.Draw(rounded).rounded_rectangle(
            [0, 0, size - 1, size - 1], radius=int(size * 0.24), fill=255)
        mark.putalpha(rounded)
    else:
        mark = draw.rounded_rect((size, size), int(size * 0.30), brand.ACCENT + (255,))
        d = ImageDraw.Draw(mark)
        f = draw.font(brand.DISPLAY_HEAVY, int(size * 0.62))
        box = f.getbbox("L")
        d.text(((size - (box[2] - box[0])) / 2 - box[0],
                (size - (box[3] - box[1])) / 2 - box[1]), "L", font=f,
               fill=brand.BG_DEEP + (255,))
    glow = mark.filter(ImageFilter.GaussianBlur(30))
    frame.alpha_composite(glow, ((brand.W - size) // 2, 470))
    frame.alpha_composite(mark, ((brand.W - size) // 2, 470))

    draw.draw_block(frame, spec.get("headline", "Lumin"), path=brand.DISPLAY_HEAVY,
                    box=(brand.SAFE_X, 740, brand.W - brand.SAFE_X * 2, 240),
                    start=104, align="center")
    if spec.get("sub"):
        draw.draw_block(frame, spec["sub"], path=brand.BODY,
                        box=(brand.SAFE_X + 20, 960, brand.W - (brand.SAFE_X + 20) * 2, 190),
                        start=44, fill=brand.TEXT_SECONDARY, align="center")
    if spec.get("cta"):
        tile = draw.pill(spec["cta"], path=brand.BODY_BOLD, size=40,
                         fg=brand.BG_DEEP, bg=brand.ACCENT + (255,), pad=(46, 22))
        frame.alpha_composite(tile, ((brand.W - tile.width) // 2, 1190))
    if spec.get("handle"):
        f = draw.font(brand.BODY_SEMI, 40)
        d = ImageDraw.Draw(frame)
        w = f.getlength(spec["handle"])
        d.text(((brand.W - w) / 2, 1330), spec["handle"], font=f,
               fill=brand.TEXT_SECONDARY + (255,))
    # The risk line is not decoration. This is a financial product, the wording
    # is the app's OWN consent copy, and it belongs on the frame a viewer is
    # still looking at when the reel loops -- not only in the caption, which is
    # collapsed behind "more" on most feeds.
    if spec.get("disclaimer"):
        draw.draw_block(frame, spec["disclaimer"], path=brand.BODY,
                        box=(brand.SAFE_X + 40, 1430,
                             brand.W - (brand.SAFE_X + 40) * 2, 130),
                        start=27, min_size=21, fill=brand.TEXT_MUTED,
                        align="center", shadow=False)
    return frame.convert("RGB")


def screen(spec: dict, t: float, dur: float) -> Image.Image:
    """Full-bleed app screen with an eased push -- for showing DETAIL.

    The phone mockup is the right frame for "here is the product"; it is the
    wrong one for "read this row", because the UI ends up ~600px wide on a
    1080px canvas and the numbers are unreadable on a phone. This crops into the
    plate itself so a signal's entry, stop and targets are legible.
    """
    p = t / max(1e-6, dur)
    plate = load(str(brand.CAPTURE_DIR / "screens" / spec["screen"]))
    zf, zt = spec.get("zoom", [1.25, 1.45])
    pf, pt = spec.get("pan", [[0.5, 0.42], [0.5, 0.52]])
    frame = motion.ken_burns(plate, p, zoom_from=zf, zoom_to=zt,
                             pan_from=tuple(pf), pan_to=tuple(pt),
                             size=(brand.W, brand.H)).convert("RGBA")

    # Darken the top and bottom so a kicker and the captions stay readable over
    # a bright card without dimming the UI being demonstrated.
    frame.alpha_composite(draw.vertical_scrim((brand.W, 400), top_alpha=200,
                                              bottom_alpha=0, start=0.0), (0, 0))
    frame.alpha_composite(draw.vertical_scrim((brand.W, 640), top_alpha=0,
                                              bottom_alpha=225, start=0.0),
                          (0, brand.H - 640))
    if spec.get("kicker"):
        _kicker(frame, spec["kicker"], spec.get("kicker_y", 210))
    if spec.get("headline"):
        draw.draw_block(frame, spec["headline"], path=brand.DISPLAY,
                        box=(brand.SAFE_X, spec.get("headline_y", 268),
                             brand.W - brand.SAFE_X * 2, 200),
                        start=spec.get("headline_size", 70), align="center")
    return frame.convert("RGB")


RENDERERS = {"character": character, "phone": phone, "duo": duo,
             "card": card, "end": end, "screen": screen}


def render(spec: dict, t: float, dur: float) -> Image.Image:
    kind = spec.get("type", "card")
    if kind not in RENDERERS:
        raise KeyError(f"unknown scene type {kind!r}; have {sorted(RENDERERS)}")
    return RENDERERS[kind](spec, t, dur)
