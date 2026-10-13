#!/usr/bin/env python3
"""Audio-synced review of one scene before rendering (owner: "self-review every frame; frames must suit the audio").
Snapshots the composition every --step seconds and captions each frame with its film time and the words heard then.
  python3 build/review_scene.py <id> [--step 1.0]      -> qa/scenes/<id>_NN.jpg (12 frames a sheet); read every sheet."""
import argparse, json, shutil, subprocess, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
from words import said                   # noqa: E402

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("id"); ap.add_argument("--step", type=float, default=1.0)
a = ap.parse_args()
d = ROOT / "video/cantpay" / a.id
js = (d / "params.js").read_text(); scene = json.loads(js[js.index("=") + 1:].strip().rstrip(";"))
start = float(js.split("(")[1].split("–")[0])
times = [round(t * a.step + 0.05, 2) for t in range(int(scene["duration"] / a.step) + 1) if t * a.step + 0.05 < scene["duration"]]
shutil.rmtree(d / "snapshots", ignore_errors=True)
subprocess.run(["npx", "--prefix", str(ROOT), "hyperframes", "snapshot", ".", "--at", ",".join(map(str, times)), "--no-end"], cwd=d, capture_output=True)
shots = sorted((d / "snapshots").glob("frame-*.png"), key=lambda f: int(f.name.split("-")[1]))
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
W, H, CAP = 560, 315, 92
qa = P / "qa/scenes"; qa.mkdir(parents=True, exist_ok=True)
for old in qa.glob(f"{a.id}_*.jpg"):
    old.unlink()
for k in range(0, len(shots), 12):
    sheet = Image.new("RGB", (W * 3, (H + CAP) * 4), (16, 16, 20)); dr = ImageDraw.Draw(sheet)
    for j, f in enumerate(shots[k:k + 12]):
        t = times[k + j]; ft = start + t; x, y = (j % 3) * W, (j // 3) * (H + CAP)
        sheet.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
        dr.text((x + 6, y + H + 4), f"{a.id} {t:5.2f}s  film {ft:6.2f}", font=F, fill=(250, 210, 80))
        for i, line in enumerate(textwrap.wrap(said(ft - a.step / 2, ft + a.step / 2) or "(no speech)", 58)[:3]):
            dr.text((x + 6, y + H + 26 + i * 21), line, font=FS, fill=(235, 235, 235))
    out = qa / f"{a.id}_{k // 12:02d}.jpg"; sheet.save(out, quality=80); print(out)
