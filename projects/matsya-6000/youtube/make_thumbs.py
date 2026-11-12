#!/usr/bin/env python3
"""Thumbnails for matsya-6000 (PLAYBOOK §4.5): a generated picture + at most 3 words.

  python3 projects/matsya-6000/youtube/make_thumbs.py --bg gen_a.png --out thumb_a.jpg --words "6 KM|DOWN"

The pictures were made with Canva's image generator (owner, 2026-11-12: "use image generation tools"); the prompts
are in metadata.json. No real person, no face. Built at 2560x1440, saved at 1280x720 (JPG, under 2 MB). '|' splits
lines; the last line takes the accent colour. The bottom-right corner stays clear for the time badge.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 2560, 1440
ANTON = str(Path(__file__).resolve().parents[3] / "library/fonts/Anton-Regular.woff")
WHITE = (255, 255, 255)
COLOURS = {"yellow": (255, 214, 0), "orange": (255, 122, 0), "red": (255, 59, 48)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--accent", default="yellow", choices=list(COLOURS))
    ap.add_argument("--size", type=int, default=430, help="height of the letters, px at 2560")
    ap.add_argument("--x", type=int, default=110)
    ap.add_argument("--y", type=int, default=120)
    ap.add_argument("--shade", type=int, default=120, help="darkness behind the words, 0-255")
    ap.add_argument("--shade_w", type=float, default=0.42)
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--shift", default="0,0", help="move the picture, px at 2560")
    ap.add_argument("--sat", type=float, default=1.12)
    ap.add_argument("--contrast", type=float, default=1.06)
    ap.add_argument("--gamma", type=float, default=1.0, help="below 1 lifts the dark parts")
    a = ap.parse_args()

    src = Image.open(a.bg).convert("RGB")
    sw, sh = int(W * a.zoom), int(H * a.zoom)
    src = src.resize((sw, sh), Image.LANCZOS)
    dx, dy = map(int, a.shift.split(","))
    canvas = Image.new("RGB", (W, H))
    canvas.paste(src, ((W - sw) // 2 + dx, (H - sh) // 2 + dy))
    if a.gamma != 1.0:
        canvas = canvas.point(lambda v: int(255 * (v / 255) ** a.gamma))
    canvas = ImageEnhance.Color(canvas).enhance(a.sat)
    canvas = ImageEnhance.Contrast(canvas).enhance(a.contrast)

    # a soft shade behind the words only, so the picture stays bright
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    edge = int(W * a.shade_w)
    for x in range(edge):
        sd.line([(x, 0), (x, H)], fill=int(a.shade * (1 - x / edge) ** 1.3))
    canvas = Image.composite(Image.new("RGB", (W, H), (0, 10, 30)), canvas, shade).convert("RGBA")

    lines = a.words.split("|")
    font = ImageFont.truetype(ANTON, a.size)
    d = ImageDraw.Draw(canvas)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdw = ImageDraw.Draw(shadow)
    y = a.y
    pos = []
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        pos.append((ln, y - bb[1]))
        sdw.text((a.x + 16, y - bb[1] + 20), ln, font=font, fill=(0, 0, 0, 255), stroke_width=14,
                 stroke_fill=(0, 0, 0, 255))
        y += (bb[3] - bb[1]) + int(a.size * 0.1)
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(canvas)
    for i, (ln, yy) in enumerate(pos):
        d.text((a.x, yy), ln, font=font, fill=COLOURS[a.accent] if i == len(pos) - 1 else WHITE, stroke_width=12,
               stroke_fill=(0, 0, 0))
    out = canvas.convert("RGB").resize((1280, 720), Image.LANCZOS)
    out.save(a.out, "JPEG", quality=93, optimize=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
