"""PROOF shots of PDF sources (Chromium cannot highlight inside a PDF).

Renders the page with pdftoppm (about 266 dpi), finds the quoted words with `pdftotext -bbox-layout`, paints a
highlighter (multiply blend, so the ink stays dark) over them, and lays the page on a 3840x2160 frame like Chrome's PDF
viewer at 2x (grey surround, page centred, the highlight centred vertically), so these match proof_shots.js output.
Writes <id>.png and <id>.json (highlight box as fractions of the frame, same format as proof_shots.js).

Usage: python3 -I proof_pdf.py <pdf dir> <out dir> [id,id,...] [--list]
The pdf dir holds the downloaded files named as in SHOTS (download commands: projects/cant-pay-minimum/proofs.md).
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

W, H = 3840, 2160
BG = (82, 86, 89)  # Chrome PDF viewer grey
YELLOW = (255, 230, 0)

# phrases: each is matched on its own (first hit after the previous phrase's hit unless anywhere=True)
SHOTS = [
    dict(id='hdfc_mitc_late_fee', pdf='hdfc_mitc.pdf', page=13,
         phrases=['Charges in case of default (no payment or delayed payment): Basis Credit Card bill amount',
                  '₹5,001 to ₹10,000', '₹750/-', 'More than ₹50,000', '₹1300/-']),
    dict(id='hdfc_mitc_rate_375', pdf='hdfc_mitc.pdf', page=10,
         phrases=['All other variants', '3.75%', '45.0%']),
    dict(id='pnb_commission_slabs', pdf='pnb.pdf', page=8,
         phrases=['The Agency will be paid commission on the amounts recovered as under:',
                  'upto Rs 1 lac', 'Upto 3 years', '7.5 %', 'Above 3 years upto 5', '10.0 %', 'Beyond 5 years', '15.0 %']),
    dict(id='pnb_trace_7500', pdf='pnb.pdf', page=22,
         phrases=['On receipt of information about whereabouts of the missing/absconding', 'Rs. 7,500/- per person',
                  'subject to maximum', 'fee of Rs. 45,000/-']),
    dict(id='onecard_ap_tg_agencies', pdf='onecard.pdf', page=3,
         # the six AP/Telangana places on this page (rows 22, 24, 25, 28, 29) and the full row 28 (the claims.csv quote)
         phrases=['Hyderabad, KarimNagar, Warangal', 'Vizag', 'Vijaywada',
                  ('Hyderabad', 3), ('CollMan Services', 5), ('Tirupathi', 0), ('Andhra', 2), ('Pradesh', 2),
                  'NO.19-12-356 BAIRAGIPETTADA', ',OPP TO PADMAVATHI PARK', ',NEAR INDIAN', 'BANK,TIRUPATHI-517501']),
    dict(id='hdfc_cma_setoff', pdf='hdfc_cma.pdf', page=15,
         phrases=['It is agreed that the Bank, at any time and without notice, will have a lien and right of set-off on all monies '
                  'belonging to the Cardmember and/or Add-on Cardmember standing to their credit in any account whatsoever with the Bank']),
    dict(id='indusind_bcsbi_3days', pdf='indusind.pdf', page=52,
         phrases=['We will send you intimation to this effect by e-mail on your registered e-mail id / registered mobile number or '
                  'letter within three days from placing lien / hold on your deposit account.']),
    dict(id='sc_2019_not_cheating', pdf='sc2019.pdf', page=[8, 9],  # the sentence runs over the page break
         phrases=['The mere inability of the appellant to return the loan amount cannot give rise to a criminal prosecution for '
                  'cheating unless fraudulent or', 'dishonest intention is shown right at the beginning of the transaction, as it is '
                  'this mens rea which is the crux of the offence.']),
]

CANON = {'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-'}


def norm(t):
    return ''.join(CANON.get(c, c) for c in t if not c.isspace()).lower()


def page_words(pdf, page):
    xml = subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-bbox-layout', str(pdf), '-'],
                         capture_output=True, text=True, check=True).stdout
    xml = re.sub(r'<!DOCTYPE[^>]*>', '', xml)
    xml = xml.replace(' xmlns="http://www.w3.org/1999/xhtml"', '')
    root = ET.fromstring(xml)
    pg = root.find('.//page')
    pw, ph = float(pg.get('width')), float(pg.get('height'))
    words = [(w.text or '', float(w.get('xMin')), float(w.get('yMin')), float(w.get('xMax')), float(w.get('yMax')))
             for w in pg.iter('word')]
    return pw, ph, words


def occurrences(words, phrase):
    """All hits of the phrase in the flattened (whitespace-free) word text: list of (start char, word indexes)."""
    flat, owner = '', []
    for i, w in enumerate(words):
        t = norm(w[0])
        flat += t
        owner += [i] * len(t)
    n, out, k = norm(phrase), [], -1
    while (k := flat.find(n, k + 1)) >= 0:
        out.append((k, sorted(set(owner[k:k + len(n)]))))
    return out


def line_rects(boxes):
    """Merge word boxes that share a line into one rectangle per line."""
    rows = []
    for b in sorted(boxes, key=lambda b: (round(b[1]), b[0])):
        for r in rows:
            if abs(r[1] - b[1]) < 0.5 * (b[3] - b[1]) and b[0] - r[2] < 40:
                r[0], r[1], r[2], r[3] = min(r[0], b[0]), min(r[1], b[1]), max(r[2], b[2]), max(r[3], b[3])
                break
        else:
            rows.append(list(b))
    return rows


def shoot(s, pdf_dir, out_dir, listing=False):
    pdf = Path(pdf_dir) / s['pdf']
    pages = s['page'] if isinstance(s['page'], list) else [s['page']]
    gap = 12  # points between stacked pages, like a PDF viewer in continuous scroll
    words, sizes, yoff = [], [], 0.0
    for pg in pages:
        pw, ph, ws = page_words(pdf, pg)
        words += [(t, x0, y0 + yoff, x1, y1 + yoff) for t, x0, y0, x1, y1 in ws]
        sizes.append((pw, ph, yoff))
        yoff += ph + gap
    pw = max(sz[0] for sz in sizes)
    hits, pos, missing = [], -1, []
    for item in s['phrases']:
        text, nth = (item, None) if isinstance(item, str) else item
        occ = occurrences(words, text)
        if listing:
            print(f'  {text!r}:', [(i, round(words[o[1][0]][1]), round(words[o[1][0]][2])) for i, o in enumerate(occ)])
        if not occ:
            missing.append(text)
            continue
        if nth is not None:
            k, idx = occ[nth]
        else:  # the first hit after the previous phrase, else the first hit
            k, idx = next((o for o in occ if o[0] > pos), occ[0])
        pos = k
        hits += idx
    if listing:
        return 'listed'
    if not hits:
        return 'TEXT NOT FOUND'
    portrait = sizes[0][1] >= sizes[0][0]
    disp_w = 2200 if portrait else 3600  # page width on the 3840 frame
    dpi = disp_w / pw * 72
    sc = dpi / 72
    canvas = Image.new('RGB', (round(pw * sc), round(yoff * sc)), BG)
    for pg, (w_, h_, off) in zip(pages, sizes):
        tmp = Path(out_dir) / f'.{s["id"]}_p{pg}'
        subprocess.run(['pdftoppm', '-f', str(pg), '-l', str(pg), '-r', f'{dpi:.2f}', '-png', '-singlefile', str(pdf), str(tmp)],
                       check=True)
        canvas.paste(Image.open(f'{tmp}.png').convert('RGB'), (0, round(off * sc)))
        Path(f'{tmp}.png').unlink()
    img = canvas
    pad = 4
    rects = [[r[0] * sc - pad, r[1] * sc - pad, r[2] * sc + pad, r[3] * sc + pad]
             for r in line_rects([words[i][1:] for i in hits])]
    layer = Image.new('RGB', img.size, (255, 255, 255))
    d = ImageDraw.Draw(layer)
    for r in rects:
        d.rounded_rectangle(r, radius=6, fill=YELLOW)
    # the gap between stacked pages stays grey
    img = ImageChops.multiply(img, layer)
    # place on the frame: page centred horizontally, highlight centred vertically (clamped to the page)
    x0, y0 = min(r[0] for r in rects), min(r[1] for r in rects)
    x1, y1 = max(r[2] for r in rects), max(r[3] for r in rects)
    ox = (W - img.width) // 2
    oy = int(H / 2 - (y0 + y1) / 2)
    oy = max(min(oy, 40), H - img.height - 40) if img.height + 80 > H else (H - img.height) // 2
    frame = Image.new('RGB', (W, H), BG)
    frame.paste(img, (ox, oy))
    frame.save(Path(out_dir) / f'{s["id"]}.png', optimize=True)
    box = dict(x0=(x0 + ox) / W, y0=(y0 + oy) / H, x1=(x1 + ox) / W, y1=(y1 + oy) / H)
    (Path(out_dir) / f'{s["id"]}.json').write_text(json.dumps(box))
    return ('ok' if not missing else f'PARTIAL, missing {missing}') + f' page {pages} dpi {dpi:.0f} {json.dumps(box)}'


if __name__ == '__main__':
    pdf_dir, out_dir = sys.argv[1], sys.argv[2]
    listing = '--list' in sys.argv  # print every hit of each phrase (index, x, y) to pick (text, nth) for tables
    args = [a for a in sys.argv[3:] if a != '--list']
    only = args[0].split(',') if args else None
    for s in SHOTS:
        if only and s['id'] not in only:
            continue
        try:
            print(s['id'], shoot(s, pdf_dir, out_dir, listing))
        except Exception as e:  # fail soft per source
            print(s['id'], 'FAIL', str(e)[:160])
