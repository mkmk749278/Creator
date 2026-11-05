#!/usr/bin/env python3
"""Word-to-scene sheets for the picture gate (PLAYBOOK §14.2): two frames a second of a rendered cut, each with the
words heard in that second under it, 24 seconds to a sheet. Read every sheet; every frame must show what is said.

Usage: scripts/word_sheets.py CUT.mp4 films/<slug>/vo/timing.json OUT_DIR
"""
import json
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

cut, timing, out = sys.argv[1:4]
frames = os.path.join(out, 'frames')
os.makedirs(frames, exist_ok=True)
if not os.listdir(frames):
    subprocess.run(['ffmpeg', '-v', 'error', '-i', cut, '-vf', 'fps=2,scale=384:216', '-q:v', '4', f'{frames}/f%05d.jpg'], check=True)
t = json.load(open(timing))
words, dur = t['words'], int(t['duration'])
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
W, H, TH, C, R = 384, 216, 62, 4, 6
for first in range(0, dur + 1, C * R):
    img = Image.new('RGB', (C * W, R * (H + TH)), (20, 20, 20))
    d = ImageDraw.Draw(img)
    for k in range(C * R):
        s = first + k
        if s > dur:
            break
        x, y = (k % C) * W, (k // C) * (H + TH)
        f = f'{frames}/f{2 * s + 2:05d}.jpg'  # the frame at s + 0.5 s
        if os.path.exists(f):
            img.paste(Image.open(f), (x, y))
        said = ' '.join(w['w'] for w in words if s <= w['start'] < s + 1)
        d.text((x + 4, y + H + 2), f'{s // 60}:{s % 60:02d}', font=bold, fill=(255, 200, 80))
        for i, line in enumerate(textwrap.wrap(said, 40)[:3]):
            d.text((x + 60 if i == 0 else x + 4, y + H + 2 + i * 19), line, font=font, fill=(235, 235, 235))
    img.save(os.path.join(out, f's{first // 60:02d}m{first % 60:02d}.jpg'), quality=82)
print(f'{(dur + C * R) // (C * R)} sheets in {out}')
