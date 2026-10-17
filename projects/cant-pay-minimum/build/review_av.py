#!/usr/bin/env python3
"""Audio-synced frame review (owner, 2026-10-12: "frames must suit the audio; self-review every frame"): one frame every
`--step` seconds of the finished film, each captioned with its timecode, the shot it belongs to and the exact words
heard in that second (build/words.py), 12 frames per sheet. Read every sheet and check each frame against its words:
does the picture show what is being said right then? Is anything unreadable, empty, covered or off-frame?

Usage: python3 projects/cant-pay-minimum/build/review_av.py [--video FILE] [--step 1.0] [--from 0] [--to END]
Writes qa/review_av/av_NNN.jpg.
"""
import argparse, subprocess, sys, tempfile, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
import assemble as asm
from timing import END
from words import said

ap = argparse.ArgumentParser()
ap.add_argument("--video", default=str(asm.A / "cant-pay-minimum-preview-720p.mp4"))
ap.add_argument("--step", type=float, default=1.0)
ap.add_argument("--from", dest="t0", type=float, default=0.0)
ap.add_argument("--to", dest="t1", type=float, default=END)
a = ap.parse_args()

shots = asm.expand(sorted(asm.SHOTS, key=lambda s: s["t"]), END)
def shot_at(t):
    cur = shots[0]
    for s in shots:
        if s["t"] <= t: cur = s
    return f"{cur['kind']} {cur.get('id') or cur.get('label') or ''}"[:40]

qa = asm.PR_ / "qa/review_av"; qa.mkdir(parents=True, exist_ok=True)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
W, H, CAP = 560, 315, 92
times = []
t = a.t0
while t < min(a.t1, END):
    times.append(round(t, 2)); t += a.step
with tempfile.TemporaryDirectory() as td:
    for k in range(0, len(times), 12):
        sheet = Image.new("RGB", (W * 3, (H + CAP) * 4), (16, 16, 20)); d = ImageDraw.Draw(sheet)
        for j, t in enumerate(times[k:k + 12]):
            f = Path(td) / f"{t:.2f}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", a.video, "-frames:v", "1", "-vf", f"scale={W}:{H}", str(f)])
            x, y = (j % 3) * W, (j // 3) * (H + CAP)
            if f.exists():
                sheet.paste(Image.open(f), (x, y))
            d.text((x + 6, y + H + 4), f"{t:7.2f}s  {shot_at(t)}", font=F, fill=(250, 210, 80))
            words = said(t - a.step / 2, t + a.step / 2) or "(no speech)"
            for i, line in enumerate(textwrap.wrap(words, 58)[:3]):
                d.text((x + 6, y + H + 26 + i * 21), line, font=FS, fill=(235, 235, 235))
        out = qa / f"av_{k // 12:03d}.jpg"; sheet.save(out, quality=80); print(out)
