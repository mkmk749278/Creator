#!/usr/bin/env python3
"""Owner's Canva video templates (revision v2) -> assets/canva/IO-*.mp4 at 3840x2160.
Raw 4K exports (Canva MCP export-design, mp4 horizontal_4k) sit in assets/canva_raw/:
  hospital_corporate.mp4 (DAHYFiFlU7Y) -> IO-1 clinic helpdesk
  office_computer.mp4    (DAHYF-4b51s) -> IO-3 laptop loading spinner; IO-2 the same laptop with our cioins.co.in
                                          grievance-portal capture warped onto its screen (page loads at 0.8 s)
  medical_white_blue.mp4 (DAHYFnM0Kms) -> IO-5 doctor with papers, cropped clear of the template's text card
Usage: python3 tools/make_canva.py
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image

P = Path(__file__).resolve().parents[1]
RAW, OUT = P / "assets/canva_raw", P / "assets/canva"
ENC = ["-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "40M", "-bufsize", "80M", "-pix_fmt", "yuv420p", "-r", "30"]
# laptop screen corners in the 4K export (measured on the white screen: TL, TR, BR, BL)
QUAD = [(1073, 262), (2845, 262), (2826, 1292), (1082, 1292)]


def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


def coeffs(dst, src):
    """PIL perspective coefficients mapping output (dst quad) back to input (src quad)."""
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(m, float), np.array([c for p in src for c in p], float)).tolist()


def screen_overlay(page_png, out_png):
    pg = Image.open(page_png).convert("RGB")
    pg = pg.crop((0, 0, pg.width, min(pg.height, round(pg.width * 1030 / 1772))))
    full = Image.new("RGBA", (3840, 2160), (0, 0, 0, 0))
    src = [(0, 0), (pg.width, 0), (pg.width, pg.height), (0, pg.height)]
    warped = pg.convert("RGBA").transform((3840, 2160), Image.PERSPECTIVE, coeffs(QUAD, src), Image.BICUBIC)
    mask = Image.new("L", (3840, 2160), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).polygon(QUAD, fill=255)
    full.paste(warped, (0, 0), mask)
    full.save(out_png)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ff("-i", RAW / "hospital_corporate.mp4", "-vf", "scale=3840:2160,fps=30", *ENC, OUT / "IO-1.mp4")
    ff("-i", RAW / "office_computer.mp4", "-vf", "scale=3840:2160,fps=30", *ENC, OUT / "IO-3.mp4")
    ov = P / "assets/canva_raw/io2_screen.png"
    screen_overlay(P / "assets/web/cio_complaint_full.png", ov)
    ff("-i", RAW / "office_computer.mp4", "-loop", "1", "-i", ov, "-filter_complex",
       "[1:v]format=rgba,fade=t=in:st=0.8:d=0.3:alpha=1[s];[0:v]scale=3840:2160[b];[b][s]overlay=0:0:shortest=1,fps=30", *ENC, OUT / "IO-2.mp4")
    # IO-5: the template's white text card covers the left ~36%; crop the doctor clear of it
    ff("-i", RAW / "medical_white_blue.mp4", "-vf", "crop=2400:1350:1440:0,scale=3840:2160:flags=lanczos,unsharp=5:5:0.4,fps=30", *ENC, OUT / "IO-5.mp4")
    for f in sorted(OUT.glob("IO-*.mp4")):
        print(f.name, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())


if __name__ == "__main__":
    main()
