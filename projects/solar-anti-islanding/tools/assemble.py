#!/usr/bin/env python3
"""Film 36 assembly: the ten rendered scenes, frame-exact, + burned captions + the master audio, in one capped encode.

Each scene render is a little longer than its slot (HyperFrames rounds up to whole frames), so every scene is trimmed
to the frames between round(start·30) and round(end·30) of the film timeline: the picture can never drift off the VO.

  python3 projects/solar-anti-islanding/tools/assemble.py [out.mp4]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects/solar-anti-islanding"
FILM = ROOT / "video/solar36"
FPS = 30
scenes = json.load(open(FILM / "scenes.json"))
out = Path(sys.argv[1]) if len(sys.argv) > 1 else FILM / "out/solar36_cut.mp4"

args, parts = [], []
for i, s in enumerate(scenes):
    n = round(s["end"] * FPS) - round(s["start"] * FPS)
    args += ["-i", str(FILM / "out" / f"{s['id']}.mp4")]
    parts.append(f"[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[p{i}]")
k = len(scenes)
fc = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[cat];" \
     f"[cat]subtitles={PROJ / 'captions.ass'},fade=t=in:st=0:d=0.3[v]"
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats", *args, "-i", str(PROJ / "assets/audio/master.wav"),
       "-filter_complex", fc, "-map", "[v]", "-map", f"{k}:a",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "14M", "-bufsize", "28M", "-profile:v", "high",
       "-r", str(FPS), "-g", "60", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout
print(f"wrote {out} ({float(d):.2f} s)")
