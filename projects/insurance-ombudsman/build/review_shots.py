#!/usr/bin/env python3
"""Per-shot review sheets (PLAYBOOK §14): for every shot in assemble.py, 3 frames of the finished film (start/middle/end)
beside the VO words spoken during it, so semantic lock, legibility and motion can be judged shot by shot.
Usage: python3 build/review_shots.py --video CUT.mp4 [--out DIR] [--per 8]
"""
import argparse, subprocess, sys, tempfile, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
import assemble as asm

FONT = ImageFont.truetype(asm.FONT, 15)
FONT_B = ImageFont.truetype(asm.FONT, 17)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--video", required=True)
    ap.add_argument("--out", default=str(asm.ROOT / "runs/insurance-ombudsman/review")); ap.add_argument("--per", type=int, default=8)
    a = ap.parse_args()
    shots = asm.shot_list(); END = asm.END
    qa = Path(a.out); qa.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp()); rows = []
    for i, s in enumerate(shots):
        t0 = s["t"]; t1 = shots[i + 1]["t"] if i + 1 < len(shots) else END
        frames = []
        for j, f in enumerate((0.12, 0.5, 0.92)):
            p = tmp / f"{i:03d}_{j}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0 + (t1 - t0) * f:.2f}", "-i", a.video, "-frames:v", "1", "-vf", "scale=400:-2", str(p)])
            frames.append(p)
        said = " / ".join(f"[{x['id']}] {x['text']}" for x in asm.SN if x["end"] > t0 + 0.2 and x["start"] < t1 - 0.2)
        name = s.get("label") or s.get("name") or Path(str(s.get("src", s["kind"]))).name
        rows.append((i, t0, t1, s, name, frames, said))
        print(f"{i:03d} {t0:7.2f}-{t1:7.2f} {s['kind']:6s} {name} | {said[:110]}")
    for n in range(0, len(rows), a.per):
        chunk = rows[n:n + a.per]
        sheet = Image.new("RGB", (1720, 225 * len(chunk)), (20, 20, 24)); d = ImageDraw.Draw(sheet)
        for r, (i, t0, t1, s, name, frames, said) in enumerate(chunk):
            y = r * 225
            for j, f in enumerate(frames):
                if f.exists():
                    sheet.paste(Image.open(f), (j * 400, y))
            d.text((1210, y + 6), f"#{i:03d}  {t0:.1f}-{t1:.1f}s ({t1 - t0:.1f}s)  {s['kind']}", font=FONT_B, fill=(255, 220, 80))
            d.text((1210, y + 30), name[:48], font=FONT, fill=(150, 220, 255))
            for k, ln in enumerate(textwrap.wrap(said, 58)[:9]):
                d.text((1210, y + 54 + k * 18), ln, font=FONT, fill=(235, 235, 235))
        sheet.save(qa / f"shots_{n // a.per:02d}.jpg", quality=82)
    print("sheets in", qa)


if __name__ == "__main__":
    main()
