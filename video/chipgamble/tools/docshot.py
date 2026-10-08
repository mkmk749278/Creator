# Render a PDF page to PNG and locate phrases -> highlight boxes in image pixels.
import sys, json, subprocess, re, html, os
pdf, page, out_png, out_json = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
phrases = json.loads(sys.argv[5])
W = 1600
subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-png", "-singlefile", "-scale-to-x", str(W), "-scale-to-y", "-1", pdf, out_png[:-4]], check=True)
x = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
pw = float(re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).group(1)); ph = float(re.search(r'<page width="[\d.]+" height="([\d.]+)"', x).group(1))
sc = W / pw
words = [(float(a), float(b), float(c), float(d), html.unescape(w)) for a, b, c, d, w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x)]
toks = [w[4] for w in words]
boxes = []
for ph_ in phrases:
    pt = ph_.split()
    hit = None
    for i in range(len(toks) - len(pt) + 1):
        if all(toks[i + j].strip(".,;:()") == pt[j].strip(".,;:()") for j in range(len(pt))):
            hit = words[i:i + len(pt)]; break
    if not hit: print("NOT FOUND:", ph_, file=sys.stderr); continue
    # split per line (y)
    lines = {}
    for w in hit: lines.setdefault(round(w[1]), []).append(w)
    for ws in lines.values():
        x0 = min(w[0] for w in ws); y0 = min(w[1] for w in ws); x1 = max(w[2] for w in ws); y1 = max(w[3] for w in ws)
        boxes.append({"phrase": ph_, "x": round(x0 * sc - 6), "y": round(y0 * sc - 4), "w": round((x1 - x0) * sc + 12), "h": round((y1 - y0) * sc + 8)})
json.dump({"img_w": W, "img_h": round(ph * sc), "boxes": boxes}, open(out_json, "w"), indent=1)
print(out_png, round(ph * sc), boxes)
