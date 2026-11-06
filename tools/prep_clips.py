#!/usr/bin/env python3
"""Cut a film's footage spans into Remotion-ready clips (PLAYBOOK §13.1 judder, §14.2 bitrate caps).

  python3 tools/prep_clips.py projects/<slug> [--only NAME,NAME] [--jobs 3]

Reads projects/<slug>/media/clips.tsv (name, source in assets/footage/, start, end, crop w:h:x:y or V for vertical,
note). Writes assets/media/clips/<name>.mp4: only the seconds used, cropped (watermarks, captions, letterbox), scaled
to 1920x1080 (vertical sources to 608x1080 x 1.0 height), motion-interpolated to 60 fps when the source is not a
divisor of 60, H.264 CRF 18 capped at 16 Mb/s, no audio. Skips clips already made unless --force.
"""
import argparse
import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def fps_of(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
    a, b = r.split("/")
    return float(a) / float(b)


def make(film, row, force):
    name, src, t0, t1, crop = row[0], row[1], float(row[2]), float(row[3]), (row[4] if len(row) > 4 else "").strip()
    out = film / "assets/media/clips" / f"{name}.mp4"
    if out.exists() and not force:
        return f"{name}: kept"
    srcp = film / "assets/footage" / src
    vf = []
    if crop and crop != "V":
        vf.append(f"crop={crop}")
    if crop == "V":
        vf.append("scale=-2:1080:flags=lanczos")
    else:
        vf.append("scale=1920:1080:flags=lanczos,setsar=1")
    fr = fps_of(srcp)
    if abs(60 / fr - round(60 / fr)) > 1e-3:
        vf.append("minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    else:
        vf.append("fps=60")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-to", f"{t1}", "-i", str(srcp), "-an",
                    "-vf", ",".join(vf), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "16M",
                    "-bufsize", "32M", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
    return f"{name}: {t1 - t0:.1f}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film", type=Path)
    ap.add_argument("--only")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    rows = [r for r in csv.reader((a.film / "media/clips.tsv").open(), delimiter="\t") if r and not r[0].startswith("#")]
    if a.only:
        keep = set(a.only.split(","))
        rows = [r for r in rows if r[0] in keep]
    with ThreadPoolExecutor(a.jobs) as ex:
        for msg in ex.map(lambda r: make(a.film, r, a.force), rows):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
