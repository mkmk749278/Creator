#!/usr/bin/env python3
"""See thumbnails the way viewers do before choosing one (PLAYBOOK §13b).

Draws (1) a YouTube mobile home feed in dark mode, 1080 px wide (a phone at 3x), each thumbnail full width with the
duration badge bottom right, channel avatar, two-line title and meta line; and (2) the small "Up next" size, 168x94
thumbnails with their titles beside them, which is where most suggested-video clicks happen. Both images go to --out.

  python3 scripts/thumb_feed.py --out qa/feed --duration 11:09 \
      "youtube/thumbnail_g.jpg::India Has the Sand. So Why Do Its Magnets Come From China?" \
      "youtube/thumbnail_h.jpg::India Has the Sand. So Why Do Its Magnets Come From China?"
Each argument is IMAGE::TITLE. Order is kept, so put rivals or older thumbnails between candidates to judge contrast.
"""
import argparse
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
BG, FG, SUB = (15, 15, 15), (241, 241, 241), (170, 170, 170)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def badge(d, x1, y1, text, f):
    w = d.textlength(text, font=f) + 18
    d.rounded_rectangle((x1 - w, y1 - 40, x1, y1), 6, fill=(0, 0, 0, 210))
    d.text((x1 - w + 9, y1 - 37), text, font=f, fill=(255, 255, 255))


def feed(items, duration, channel):
    W, TH = 1080, 608
    f_t, f_m, f_b = font(FONT, 40), font(FONT, 31), font(FONT_B, 28)
    rows = []
    for img, title in items:
        tile = Image.new("RGB", (W, TH + 230), BG)
        tile.paste(Image.open(img).convert("RGB").resize((W, TH), Image.LANCZOS), (0, 0))
        d = ImageDraw.Draw(tile, "RGBA")
        badge(d, W - 18, TH - 18, duration, f_b)
        d.ellipse((30, TH + 34, 120, TH + 124), fill=(40, 56, 90))
        d.text((52, TH + 58), "BE", font=font(FONT_B, 34), fill=(255, 210, 60))
        lines = textwrap.wrap(title, 42)[:2]
        for i, line in enumerate(lines):
            d.text((150, TH + 30 + i * 52), line, font=f_t, fill=FG)
        d.text((150, TH + 40 + len(lines) * 52), f"{channel} · 1.2K views · 2 hours ago", font=f_m, fill=SUB)
        rows.append(tile)
    out = Image.new("RGB", (W, sum(r.height for r in rows)), BG)
    y = 0
    for r in rows:
        out.paste(r, (0, y)); y += r.height
    return out


def small(items, duration, channel):
    tw, th, W = 168, 94, 560
    f_t, f_m, f_b = font(FONT, 15), font(FONT, 13), font(FONT_B, 11)
    out = Image.new("RGB", (W, (th + 16) * len(items) + 16), BG)
    d = ImageDraw.Draw(out, "RGBA")
    for i, (img, title) in enumerate(items):
        y = 16 + i * (th + 16)
        out.paste(Image.open(img).convert("RGB").resize((tw, th), Image.LANCZOS), (12, y))
        w = d.textlength(duration, font=f_b) + 8
        d.rounded_rectangle((12 + tw - 4 - w, y + th - 18, 12 + tw - 4, y + th - 4), 3, fill=(0, 0, 0, 210))
        d.text((12 + tw - w, y + th - 17), duration, font=f_b, fill=(255, 255, 255))
        for j, line in enumerate(textwrap.wrap(title, 40)[:2]):
            d.text((192, y + 2 + j * 19), line, font=f_t, fill=FG)
        d.text((192, y + 44), channel, font=f_m, fill=SUB)
    return out.resize((W * 2, out.height * 2), Image.NEAREST)   # 2x so it can be read on a phone screen


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("items", nargs="+", help="IMAGE::TITLE")
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", default="10:00")
    ap.add_argument("--channel", default="Be Practical with Kishore")
    a = ap.parse_args()
    items = [tuple(x.split("::", 1)) if "::" in x else (x, "") for x in a.items]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    feed(items, a.duration, a.channel).save(out / "feed_mobile.jpg", quality=90)
    small(items, a.duration, a.channel).save(out / "feed_small.png")
    print("wrote", out / "feed_mobile.jpg", out / "feed_small.png")


if __name__ == "__main__":
    main()
