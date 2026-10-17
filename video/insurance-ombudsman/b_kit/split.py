"""Split a session B scene render into one clip per VO window, and make a 4-frame contact sheet per clip.

usage: python3 split.py <scene_dir> <render.mp4> <out_dir>
Reads the K.layout([...]) window table from <scene_dir>/index.html, rounds each window + 0.5 s to whole frames exactly
as kit.js does, cuts <scene>_<id>.mp4 frame-accurately (libx264 CRF 18, maxrate-capped) and <scene>_<id>_sheet.jpg.
Also checks that the root data-duration matches the table.
"""
import json, math, re, subprocess, sys
from pathlib import Path

FPS = 30


def layout(html):
    rows = re.search(r"K\.layout\(\[(.*?)\]\)", html, re.S).group(1)
    segs, f = [], 0
    for m in re.finditer(r'id:\s*"(\w+)",\s*ws:\s*([\d.]+),\s*we:\s*([\d.]+)', rows):
        sid, ws, we = m.group(1), float(m.group(2)), float(m.group(3))
        n = math.floor((we - ws + 0.5) * FPS - 1e-6 + 0.5)   # Math.round(x - 1e-6)
        segs.append(dict(id=sid, ws=ws, we=we, f0=f, nf=n)); f += n
    return segs


def main():
    scene, render, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    html = (scene / "index.html").read_text()
    segs = layout(html)
    total = sum(s["nf"] for s in segs) / FPS
    dd = float(re.search(r'data-duration="([\d.]+)"', html).group(1))
    if abs(dd - total) > 0.02:
        sys.exit(f"data-duration {dd} != window table {total:.3f}")
    name = scene.resolve().name
    for s in segs:
        clip = out / f"{name}_{s['id']}.mp4"
        a, b = s["f0"], s["f0"] + s["nf"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(render), "-vf",
                        f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS", "-an", "-c:v", "libx264", "-preset", "slow",
                        "-crf", "18", "-maxrate", "16M", "-bufsize", "32M", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        "-movflags", "+faststart", str(clip)], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clip)],
                                   capture_output=True, text=True).stdout)
        # contact sheet: 4 frames at 12%, 37%, 62%, 87%, film timecode burned in
        n = s["nf"]
        picks = [int(n * p) for p in (0.12, 0.37, 0.62, 0.87)]
        sel = "+".join(f"eq(n\\,{p})" for p in picks)
        sheet = out / f"{name}_{s['id']}_sheet.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf",
                        f"select='{sel}',scale=960:-1,tile=2x2:padding=6:color=black", "-frames:v", "1", "-q:v", "3", str(sheet)], check=True)
        print(json.dumps(dict(clip=clip.name, window=f"{s['ws']}-{s['we']}", frames=n, seconds=round(dur, 3),
                              film_in=round(s["ws"] - 0.25, 2), sheet=sheet.name)))


if __name__ == "__main__":
    main()
