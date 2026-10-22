#!/usr/bin/env python3
"""Turn source screenshots and PDF pages (assets/docs) into 1920x1080 'paper on a dark desk' plates (assets/plates).

Each crop is a real page region (headline, photo, the quoted line); the film engine pushes in on it and draws the
highlighter on top. Crops are in full-resolution pixels of the source image.
usage: python3 projects/rare-earth-magnets/tools/make_plates.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent.parent
D, OUT = HERE / "assets/docs", HERE / "assets/plates"
CROPS = {   # name: (source file, crop box, tilt degrees)
    "P_autocar": ("autocar_chetak_july.png", (590, 140, 1330, 940), -1.2),
    "P_ather": ("ather_450x_spec.png", (370, 300, 1540, 600), -0.8),
    "P_ather_line": ("ather_450x_spec.png", (380, 488, 1530, 588), -0.5),
    "P_nexon": ("nexon_ev_spec.png", (395, 220, 1140, 800), 1.0),
    "P_nexon_row": ("nexon_ev_spec.png", (395, 410, 1140, 690), -0.6),
    "P_autocar_photo": ("autocar_chetak_july.png", (636, 350, 1284, 730), 0),
    "P_cnbc": ("cnbctv18_rajiv.png", (360, 500, 1200, 980), 1.0),
    "P_ddindia": ("ddindia_20_bids.png", (250, 370, 1330, 1075), -1.0),
    "P_ians": ("ians_licences.png", (290, 90, 1290, 920), 1.2),
    "P_pmindia": ("pmindia_cabinet_repm.png", (20, 430, 1260, 1075), -0.8),
    "P_technology": ("technology_org_nov10.png", (340, 30, 1220, 1060), 1.0),
    "P_technology_head": ("technology_org_nov10.png", (350, 70, 1200, 215), 0.6),
    "P_technology_keys": ("technology_org_nov10.png", (360, 845, 1200, 1075), -0.6),
    "P_pib_vizag": ("pib_2220295.png", (320, 30, 1640, 960), -0.8),
    "P_pib_reserves": ("pib_2238892.png", (320, 30, 1640, 960), 0.8),
    "P_pib_magnets": ("pib_2248182.png", (320, 30, 1640, 960), -0.8),
    "P_budget": ("budget2026_p-1.png", None, -1.0),
    "P_ibm_act": ("ibm_re2022_p-02.png", None, 0.8),
    "P_ibm_demand": ("ibm_re2022_p-11.png", None, -0.8),
    "P_usgs": ("usgs_mcs2026_p-1.png", None, 0.8),
    "P_iea": ("iea_gcmo2026_p-001.png", None, -1.0),
}


def desk():
    im = Image.new("RGB", (1920, 1080), (10, 14, 20))
    g = ImageDraw.Draw(im)
    for x in range(0, 1920, 48):
        g.line([(x, 0), (x, 1080)], fill=(22, 28, 36) if x % 240 else (34, 41, 51))
    for y in range(0, 1080, 48):
        g.line([(0, y), (1920, y)], fill=(22, 28, 36) if y % 240 else (34, 41, 51))
    return im


def plate(name, src, box, tilt):
    page = Image.open(D / src).convert("RGB")
    if box is None:   # PDF page: take the top half (title and first paragraphs)
        w, h = page.size
        box = (0, 0, w, int(h * 0.5))
    page = page.crop(box)
    s = min(1560 / page.width, 900 / page.height)
    page = page.resize((int(page.width * s), int(page.height * s)), Image.LANCZOS)
    bg = desk()
    sh = Image.new("RGBA", (page.width + 120, page.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([60, 70, 60 + page.width, 70 + page.height], fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    card = Image.new("RGBA", sh.size, (0, 0, 0, 0)); card.alpha_composite(sh)
    card.paste(page, (60, 60))
    card = card.rotate(tilt, resample=Image.BICUBIC, expand=True)
    bg.paste(card, ((1920 - card.width) // 2, (1080 - card.height) // 2), card)
    bg.save(OUT / f"{name}.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for n, (src, box, tilt) in CROPS.items():
        plate(n, src, box, tilt)
        print("plate", n)
