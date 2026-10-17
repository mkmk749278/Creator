#!/usr/bin/env python3
"""Cut a native 4K scene render into the per-VO-window clips build/assemble.py expects
(projects/insurance-ombudsman/assets/scenes/<scene>_<Oid>.mp4, window + 0.25 s handles, 3840x2160, bitrate-capped).
The window tables are the ones each session used at 1080p: session A's _A/cut_clips.sh, session B's K.layout in the
scene's index.html (b_kit/split.py), session C's windows.json. Usage: python3 split_4k.py <scene> <render.mp4>"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "projects/insurance-ombudsman/assets/scenes"
FPS = 30


def sections(scene):
    """[(clip_id, first_frame, n_frames)]"""
    W = json.load(open(HERE / "windows.json"))
    if scene in W:
        return [(x["clip"].split("_")[-1], x["frame0"], x["frames"]) for x in W[scene]["sections"]]
    html = (HERE / scene / "index.html").read_text()
    if "K.layout(" in html:
        sys.path.insert(0, str(HERE / "b_kit"))
        from split import layout
        return [(s["id"], s["f0"], s["nf"]) for s in layout(html)]
    rows = re.findall(rf"^clip {scene} (O\d+) ([\d.]+) ([\d.]+)$", (HERE / "_A/cut_clips.sh").read_text(), re.M)
    return [(oid, round(float(ss) * FPS), round(float(d) * FPS)) for oid, ss, d in rows]


def main():
    scene, render = sys.argv[1], Path(sys.argv[2])
    OUT.mkdir(parents=True, exist_ok=True)
    secs = sections(scene)
    if not secs:
        sys.exit(f"no window table for {scene}")
    for oid, f0, n in secs:
        clip = OUT / f"{scene}_{oid}.mp4"; tmp = clip.with_name("tmp_" + clip.name)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(render), "-vf", f"trim=start_frame={f0}:end_frame={f0 + n},setpts=PTS-STARTPTS",
                        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-maxrate", "40M", "-bufsize", "80M", "-pix_fmt", "yuv420p",
                        "-r", str(FPS), "-movflags", "+faststart", str(tmp)], check=True)
        tmp.rename(clip)
        got = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,nb_frames", "-of", "csv=p=0", str(clip)],
                             capture_output=True, text=True).stdout.strip()
        print(f"{clip.name}: {n} frames wanted, got {got}")


if __name__ == "__main__":
    main()
