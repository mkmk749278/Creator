#!/usr/bin/env python3
"""Thumbnails for aip-submarines (PLAYBOOK §4.5): our own Blender renders + at most 3 words.

  python3 projects/aip-submarines/youtube/make_thumbs.py --bg RENDER.png --out thumb_a.jpg --words "CUT IN|TWO"

Built at 2560x1440 and downsampled to 1280x720 (JPG q94, < 2 MB). Words sit on the left, the bottom-right corner is
kept clear for the time badge. '|' splits lines; the last line is in caution yellow, the others in white.
"""
import argparse
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 2560, 1440
BG = (13, 17, 23)            # bp_bg #0d1117
GRID = (48, 54, 61)          # bp_grid #30363d
WHITE = (244, 246, 251)
YELLOW = (255, 196, 0)       # caution yellow
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


def fit_font(draw, text, max_w, start):
    size = start
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 8
    return ImageFont.truetype(FONT, size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--shift", type=int, default=0, help="move the render right by N px (2560 scale)")
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--text_w", type=float, default=0.46, help="share of the width the words may use")
    ap.add_argument("--size", type=int, default=380)
    ap.add_argument("--lift", type=float, default=1.0, help="brightness multiplier for the render")
    ap.add_argument("--valign", type=float, default=0.47, help="vertical centre of the words, as a share of the height")
    ap.add_argument("--panel", type=int, default=225, help="darkness of the left panel, 0-255")
    a = ap.parse_args()

    src = Image.open(a.bg).convert("RGB")
    sw, sh = int(W * a.zoom), int(H * a.zoom)
    src = src.resize((sw, sh), Image.LANCZOS)
    if a.lift != 1.0:
        src = src.point(lambda v: min(255, int(v * a.lift)))
    canvas = Image.new("RGB", (W, H), BG)
    canvas.paste(src, ((W - sw) // 2 + a.shift, (H - sh) // 2))

    # a dark panel on the left so the words read, fading into the render
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    edge = int(W * (a.text_w + 0.1))
    for x in range(edge):
        t = 1.0 if x < W * a.text_w * 0.7 else max(0.0, 1 - (x - W * a.text_w * 0.7) / (edge - W * a.text_w * 0.7))
        sd.line([(x, 0), (x, H)], fill=int(a.panel * t))
    canvas = Image.composite(Image.new("RGB", (W, H), BG), canvas, shade)

    # a faint drafting grid on the panel (the film's blueprint base)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, edge, 80):
        gd.line([(x, 0), (x, H)], fill=GRID + (70,), width=2)
    for y in range(0, H, 80):
        gd.line([(0, y), (edge, y)], fill=GRID + (70,), width=2)
    mask = shade.point(lambda v: int(v * 0.9))
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gl.paste(grid, (0, 0), mask)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), gl)

    # the words: left aligned, stacked, with a hard shadow for depth
    lines = a.words.split("|")
    d = ImageDraw.Draw(canvas)
    x0, max_w = 150, int(W * a.text_w) - 150
    fonts = [fit_font(d, ln, max_w, a.size) for ln in lines]
    size = min(f.size for f in fonts)
    fonts = [ImageFont.truetype(FONT, size) for _ in lines]
    heights = [d.textbbox((0, 0), ln, font=f)[3] - d.textbbox((0, 0), ln, font=f)[1] for ln, f in zip(lines, fonts)]
    gap = int(size * 0.14)
    total = sum(heights) + gap * (len(lines) - 1)
    y = int(H * a.valign - total / 2)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdw = ImageDraw.Draw(shadow)
    pos = []
    for ln, f, h in zip(lines, fonts, heights):
        top = d.textbbox((0, 0), ln, font=f)[1]
        pos.append((ln, f, y - top))
        sdw.text((x0 + 14, y - top + 16), ln, font=f, fill=(0, 0, 0, 230))
        y += h + gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas = Image.alpha_composite(canvas, shadow)
    d = ImageDraw.Draw(canvas)
    for i, (ln, f, yy) in enumerate(pos):
        d.text((x0, yy), ln, font=f, fill=YELLOW if i == len(pos) - 1 else WHITE)

    out = canvas.convert("RGB").resize((1280, 720), Image.LANCZOS)
    out.save(a.out, "JPEG", quality=94, optimize=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
