"""Cut a scene master into one clip per VO window (frame-exact, windows.json), bitrate-capped, plus a 4-frame
contact sheet per clip. Usage: python3 split_clips.py <scene>"""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
scene = sys.argv[1]
W = json.load(open(HERE / "windows.json"))[scene]
src = HERE / "renders" / f"{scene}.master.mp4"
for x in W["sections"]:
    out = HERE / "renders" / f"{x['clip']}.mp4"
    f0, n = x["frame0"], x["frames"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"trim=start_frame={f0}:end_frame={f0 + n},setpts=PTS-STARTPTS",
                    "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "18M", "-bufsize", "36M", "-pix_fmt", "yuv420p",
                    "-r", "30", "-movflags", "+faststart", str(out)], check=True)
    got = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                          "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
    # contact sheet: 4 frames at 10/37/63/90 %, timecode-labelled
    sheet = HERE / "renders" / f"{x['clip']}_sheet.jpg"
    ts = [n * p / 30 for p in (0.1, 0.37, 0.63, 0.9)]
    sel = "+".join(f"eq(n\\,{int(t * 30)})" for t in ts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf",
                    f"select='{sel}',scale=960:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{x['clip']}  %{{pts\\:hms}}':x=12:y=12:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,tile=2x2",
                    "-frames:v", "1", "-vsync", "vfr", str(sheet)], check=True)
    print(f"{x['clip']}: {n} frames wanted, {got} written, {n / 30:.3f} s")
