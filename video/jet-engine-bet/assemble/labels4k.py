"""4K overlay graphics for the jet-engine-bet assembly (PIL, native 3840x2160 RGBA PNGs).

The film's label language from R1/R2 (jep.css), drawn at true 4K so text is sharp: an uppercase 2-4 word label on a dark
scrim with an amber left rule, lower-left; an optional small grey second line; corner tags (source credit, ILLUSTRATION);
the logo bug top-right; a big centred line for the question and the end card.
All functions return a PIL RGBA image of the full frame; assemble_4k.py overlays them with timed fades.
"""
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
ROOT = Path(__file__).resolve().parents[3]
SLATE = (11, 14, 20); AMBER = (249, 115, 22); WHITE = (248, 250, 252); DIM = (148, 163, 184); RED = (239, 68, 68); CYAN = (56, 189, 248)
COLORS = {"amber": AMBER, "white": WHITE, "red": RED, "cyan": CYAN, "dim": DIM}


@lru_cache(None)
def font(weight="ExtraBold", size=80):
    return ImageFont.truetype(str(FONT_DIR / f"Inter-{weight}.otf"), size)


def _spaced(d, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def _width(d, text, f, tracking):
    return sum(d.textlength(ch, font=f) for ch in text) + tracking * max(0, len(text) - 1)


def label(text, sub=None, *, pos="ll", accent="amber", hi=None, size=80, x=192, y=None):
    """Lower-left label (jep.css .jep-label at 2x). `hi` = substring drawn in the accent colour (numbers)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("ExtraBold", size); fs = font("SemiBold", int(size * 0.55)); tr = size * 0.04
    text = text.upper(); sub = sub.upper() if sub else None
    tw = _width(d, text, f, tr); sw = _width(d, sub, fs, size * 0.08) if sub else 0
    padx, pady = int(size * 0.55), int(size * 0.36)
    bw = int(max(tw, sw) + 2 * padx); bh = int(size * 1.12 + (size * 0.75 if sub else 0) + 2 * pady)
    if y is None:
        y = H - 240 - bh
    if pos == "lr":
        x = W - 192 - bw
    d.rectangle([x, y, x + bw, y + bh], fill=SLATE + (184,))
    d.rectangle([x, y, x + 8, y + bh], fill=COLORS[accent] + (255,))
    tx, ty = x + padx, y + pady - int(size * 0.08)
    if hi and hi.upper() in text:
        a = text.index(hi.upper()); parts = [(text[:a], WHITE), (text[a:a + len(hi)], COLORS[accent]), (text[a + len(hi):], WHITE)]
        for s, c in parts:
            tx = _spaced(d, (tx, ty), s, f, c, tr) + (tr if s else 0)
    else:
        _spaced(d, (tx, ty), text, f, WHITE, tr)
    if sub:
        _spaced(d, (x + padx, y + pady + int(size * 1.12)), sub, fs, DIM, size * 0.08)
    return img


def tag(text, *, corner="br", color="dim", size=34):
    """Small corner tag: source credit (bottom-right) or ILLUSTRATION (top-left)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("SemiBold", size); tr = size * 0.12; t = text.upper(); tw = _width(d, t, f, tr)
    padx, pady = 22, 12; bw, bh = int(tw + 2 * padx), int(size * 1.25 + 2 * pady)
    x = {"br": W - 120 - bw, "bl": 120, "tl": 120, "tr": W - 120 - bw}[corner]
    y = {"br": H - 96 - bh, "bl": H - 96 - bh, "tl": 96, "tr": 96}[corner]
    d.rectangle([x, y, x + bw, y + bh], fill=SLATE + (150,))
    _spaced(d, (x + padx, y + pady - 4), t, f, COLORS[color], tr)
    return img


def big(text, sub=None, *, y=None, size=150, color="white", scrim=True):
    """Centred big line (the comment question, chapter-style reveals)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("ExtraBold", size); fs = font("SemiBold", int(size * 0.42))
    lines = text.split("\n"); lh = int(size * 1.15)
    tws = [d.textlength(l, font=f) for l in lines]; sw = d.textlength(sub, font=fs) if sub else 0
    th = lh * len(lines) + (int(size * 0.7) if sub else 0)
    y0 = (H - th) // 2 if y is None else y
    if scrim:
        pad = 70; bw = max(max(tws), sw) + 2 * pad
        d.rectangle([(W - bw) // 2, y0 - pad, (W + bw) // 2, y0 + th + pad // 2], fill=SLATE + (176,))
    for i, l in enumerate(lines):
        d.text(((W - tws[i]) // 2, y0 + i * lh), l, font=f, fill=COLORS[color])
    if sub:
        d.text(((W - sw) // 2, y0 + lh * len(lines) + int(size * 0.15)), sub, font=fs, fill=DIM)
    return img


def logo_bug(size=150, opacity=0.55):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lg = Image.open(ROOT / "assets/brand/logo_square.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    a = lg.getchannel("A").point(lambda v: int(v * opacity)); lg.putalpha(a)
    img.alpha_composite(lg, (W - 120 - size, 96))
    return img


def end_card():
    """Full-frame end card: logo + channel name on the slate (the only place the channel is named, CLAUDE.md)."""
    img = Image.new("RGBA", (W, H), SLATE + (255,)); d = ImageDraw.Draw(img)
    lg = Image.open(ROOT / "assets/brand/logo_square.png").convert("RGBA").resize((900, 900), Image.LANCZOS)
    img.alpha_composite(lg, ((W - 900) // 2, 330))
    f = font("SemiBold", 70); t = "STAY PRACTICAL"; tw = _width(d, t, f, 14)
    _spaced(d, ((W - tw) // 2, 1340), t, f, DIM, 14)
    return img


def grid_bar(on, total=99, title="Engines sent", hi="14", *, x=192, cols=33):
    """'ENGINES SENT 14 OF 99' with a 99-cell grid (R1 #bar at 2x); `on` cells lit amber."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    size = 80; f = font("ExtraBold", size); tr = size * 0.04
    text = f"{title} {hi} of {total}".upper()
    cell, gap = 32, 8; rows = (total + cols - 1) // cols
    gw = cols * cell + (cols - 1) * gap; gh = rows * cell + (rows - 1) * gap
    padx, pady = 44, 36; bw = max(gw, _width(d, text, f, tr)) + 2 * padx; bh = size * 1.1 + 24 + gh + 2 * pady
    y = H - 240 - bh
    d.rectangle([x, y, x + bw, y + bh], fill=SLATE + (184,)); d.rectangle([x, y, x + 8, y + bh], fill=AMBER + (255,))
    tx = x + padx; ty = y + pady - 6
    a = text.index(hi)
    for s, c in [(text[:a], WHITE), (text[a:a + len(hi)], AMBER), (text[a + len(hi):], WHITE)]:
        tx = _spaced(d, (tx, ty), s, f, c, tr) + (tr if s else 0)
    gy = y + pady + size * 1.1 + 24
    for i in range(total):
        cx = x + padx + (i % cols) * (cell + gap); cy = gy + (i // cols) * (cell + gap)
        d.rectangle([cx, cy, cx + cell, cy + cell], fill=(AMBER + (255,)) if i < on else (148, 163, 184, 64))
    return img
