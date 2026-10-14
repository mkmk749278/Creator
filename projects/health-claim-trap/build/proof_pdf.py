#!/usr/bin/env python3
"""PROOF frames from source PDFs: render the page, highlight the exact phrase the VO reads (word boxes from
`pdftotext -bbox`), and lay the page on a dark desk at 3840x2160 so the edit can push 2-3x into the highlight.
Writes assets/proof/<id>.png + <id>.json (highlight box as fractions, read by assemble.py's proof_parts)."""
import json, re, subprocess, sys
from html import unescape
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

P = Path(__file__).resolve().parents[1]
A = P / "assets"; OUT = A / "proof"; OUT.mkdir(parents=True, exist_ok=True)
MC = A / "docs/irdai_master_circular_health_2024.pdf"
SHOTS = [
    ("mc_cover", MC, 1, "Master Circular on Health Insurance Business"),
    ("mc_ref", MC, 2, "Ref: IRDAI/HLT/CIR/PRO/84/5/ 2024"),
    ("mc_para13", MC, 8, "No policy and claim of health insurance shall be contestable on any grounds of non-disclosure and/or misrepresentation except for established fraud, after the completion of the Moratorium Period, i.e. 60 months of continuous coverage"),
    ("mc_fraud", MC, 8, "except for established fraud,"),
    ("mc_port", MC, 8, "accrued credits gained under the ported and migrated policies shall be counted"),
    ("mc_para16", MC, 9, "Insurer shall grant final authorization within three hours of the receipt of discharge authorization request from the hospital."),
    ("mc_para16b", MC, 9, "If there is any delay beyond three hours, the additional amount if any charged by the hospital shall be borne by the insurer from shareholder's fund."),
    ("mc_wait", MC, 9, "In no case, the policyholder shall be made to wait to be discharged from the Hospital."),
    ("mc_para17", MC, 9, "No claim shall be repudiated without the approval of PMC or a three- member sub-group of PMC called the Claims Review Committee (CRC)."),
]
W, H, DPI = 3840, 2160, 300


def words(pdf, page):
    x = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), str(pdf), "-"], capture_output=True, text=True).stdout
    pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).groups())
    ws = [(unescape(m.group(5)), *map(float, m.groups()[:4])) for m in
          re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x)]
    return pw, ph, ws


def norm(s):
    return re.sub(r"[’'`]", "'", s)


def find(ws, phrase):
    toks = norm(phrase).split()
    flat = [norm(w[0]) for w in ws]
    for i in range(len(flat)):
        j, k = i, 0
        while k < len(toks) and j < len(flat):
            if flat[j] == toks[k]:
                j += 1; k += 1
            elif toks[k].startswith(flat[j]) and k + 1 <= len(toks):   # hyphenated across lines
                rest = toks[k][len(flat[j]):]; j += 1
                if j < len(flat) and flat[j] == rest: j += 1; k += 1
                else: break
            else:
                break
        if k == len(toks):
            return ws[i:j]
    return None


def shot(sid, pdf, page, phrase):
    pw, ph, ws = words(pdf, page)
    hit = find(ws, phrase)
    if not hit:
        print(sid, "PHRASE NOT FOUND"); return
    png = OUT / f"_{sid}_page"
    subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), "-png", "-singlefile", str(pdf), str(png)], check=True)
    pg = Image.open(str(png) + ".png").convert("RGB"); s = pg.width / pw
    hl = Image.new("RGBA", pg.size, (0, 0, 0, 0)); d = ImageDraw.Draw(hl)
    lines = {}
    for w in hit:                       # merge words into one bar per text line
        key = round(w[2] / 3)
        a = lines.setdefault(key, [w[1], w[2], w[3], w[4]])
        a[0], a[1], a[2], a[3] = min(a[0], w[1]), min(a[1], w[2]), max(a[2], w[3]), max(a[3], w[4])
    for x0, y0, x1, y1 in lines.values():
        d.rounded_rectangle([x0 * s - 6, y0 * s - 4, x1 * s + 6, y1 * s + 6], radius=8, fill=(255, 214, 0, 110))
    pg = Image.alpha_composite(pg.convert("RGBA"), hl).convert("RGB")
    # desk: dark slate with a soft light pool; page fit to 94% of the frame height, slight shadow
    bg = Image.new("RGB", (W, H), (15, 23, 42))
    glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse([W * .15, -H * .2, W * .85, H * 1.1], fill=90)
    bg.paste(Image.new("RGB", (W, H), (40, 52, 76)), mask=glow.filter(ImageFilter.GaussianBlur(300)))
    k = H * 0.94 / pg.height; pgs = pg.resize((int(pg.width * k), int(pg.height * k)), Image.LANCZOS)
    ox, oy = (W - pgs.width) // 2, int(H * 0.03)
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle([ox + 18, oy + 24, ox + pgs.width + 18, oy + pgs.height + 24], fill=170)
    bg.paste((0, 0, 0), mask=sh.filter(ImageFilter.GaussianBlur(28)))
    bg.paste(pgs, (ox, oy))
    bx = [min(v[0] for v in lines.values()), min(v[1] for v in lines.values()), max(v[2] for v in lines.values()), max(v[3] for v in lines.values())]
    f = lambda x, y: ((ox + x * s * k) / W, (oy + y * s * k) / H)
    (x0, y0), (x1, y1) = f(bx[0], bx[1]), f(bx[2], bx[3])
    bg.save(OUT / f"{sid}.png", optimize=True)
    (OUT / f"{sid}.json").write_text(json.dumps(dict(x0=round(x0, 4), y0=round(y0, 4), x1=round(x1, 4), y1=round(y1, 4))))
    Path(str(png) + ".png").unlink()
    print(sid, "ok", len(hit), "words")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for s in SHOTS:
        if not only or s[0] in only:
            shot(*s)
