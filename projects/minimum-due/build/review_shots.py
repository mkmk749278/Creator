#!/usr/bin/env python3
"""Per-shot review sheets: for every shot in assemble.py, 3 frames of the finished film (start/middle/end) beside the
VO words spoken during it, so semantic lock, legibility and motion can be judged shot by shot.

Usage: python3 projects/minimum-due/build/review_shots.py [--video FILE] [--per 8]
Writes qa/review/shots_NN.jpg (committed: small) and prints the shot table.
"""
import argparse, json, subprocess, sys, tempfile, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
import assemble as asm
from timing import END, GAP_B2

P = asm.P
FONT = ImageFont.truetype(asm.FONT, 15)
FONT_B = ImageFont.truetype(asm.FONT, 17)


def vo_lines():
    out = []
    for b, off in ((1, 0.0), (2, GAP_B2)):
        for i, l in enumerate(json.load(open(P / f"align/block{b}/align.json")), 1):
            text = l["te"] if (P / "lang.txt").read_text().strip() == "en" else l["en"]   # aligner stored the VO column first
            out.append((f"{b}.{i:02d}", off + l["start"], off + l["end"], text))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=str(asm.A / "minimum-due-preview-720p.mp4"))
    ap.add_argument("--per", type=int, default=8)
    a = ap.parse_args()
    shots = asm.split_long(sorted(asm.SHOTS, key=lambda s: s["t"]), END)
    lines = vo_lines()
    qa = P / "qa/review"; qa.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    rows = []
    for i, s in enumerate(shots):
        t0 = s["t"]; t1 = shots[i + 1]["t"] if i + 1 < len(shots) else END
        frames = []
        for j, f in enumerate((0.12, 0.5, 0.92)):
            t = t0 + (t1 - t0) * f; p = tmp / f"{i:03d}_{j}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", a.video, "-frames:v", "1", "-vf", "scale=400:-2", str(p)])
            frames.append(p)
        said = " / ".join(f"[{k}] {txt}" for k, s0, s1, txt in lines if s1 > t0 + 0.2 and s0 < t1 - 0.2)
        rows.append((i, t0, t1, s, frames, said))
        print(f"{i:03d} {t0:7.2f}-{t1:7.2f} {s['kind']:6s} {s.get('label') or s.get('id') or ''} | {said[:110]}")
    for n in range(0, len(rows), a.per):
        chunk = rows[n:n + a.per]
        sheet = Image.new("RGB", (1200 + 520, 225 * len(chunk)), (20, 20, 24)); d = ImageDraw.Draw(sheet)
        for r, (i, t0, t1, s, frames, said) in enumerate(chunk):
            y = r * 225
            for j, f in enumerate(frames):
                if f.exists():
                    sheet.paste(Image.open(f), (j * 400, y))
            x = 1210
            d.text((x, y + 6), f"#{i:03d}  {t0:.1f}-{t1:.1f}s ({t1 - t0:.1f}s)  {s['kind']}", font=FONT_B, fill=(255, 220, 80))
            d.text((x, y + 30), (s.get("label") or s.get("id") or "")[:48], font=FONT, fill=(150, 220, 255))
            for k, ln in enumerate(textwrap.wrap(said, 58)[:9]):
                d.text((x, y + 54 + k * 18), ln, font=FONT, fill=(235, 235, 235))
        sheet.save(qa / f"shots_{n // a.per:02d}.jpg", quality=80)
    print("sheets in", qa)


if __name__ == "__main__":
    main()
