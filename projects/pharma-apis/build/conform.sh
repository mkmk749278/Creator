#!/bin/bash
# Conform every footage/stock source the film uses to exactly 30 fps CFR (owner's review, 2026-10-29: 24/25 fps clips in a
# 30 fps timeline doubled every 5th-6th frame, so pans juddered). Every source frame is shown exactly once at 30 fps:
# 25 fps plays 1.2x, 24 fps 1.25x, 29.97 fps 1.001x faster (invisible on aerials and slow pans; motion-compensated
# interpolation measured ~30x slower than real time here and can warp). make_film.py maps in-points by the same
# factor (speed()). Output: assets/conformed/<same name>.mp4
# usage: bash projects/pharma-apis/build/conform.sh FILE...
set -u
OUT=$(cd "$(dirname "$0")/.." && pwd)/assets/conformed; mkdir -p "$OUT"
for f in "$@"; do
  n=$(basename "$f"); [ -f "$OUT/$n" ] && { echo "have $n"; continue; }
  r=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$f")
  h=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$f")
  [ "$h" -gt 1440 ] && sc=",scale=-2:1440" || sc=""
  ffmpeg -hide_banner -loglevel error -y -i "$f" -an -vf "setpts=PTS*($r)/30$sc" -r 30 -c:v libx264 -preset medium -crf 17 \
    -maxrate 30M -bufsize 60M -pix_fmt yuv420p -f mp4 "$OUT/.$n" && mv "$OUT/.$n" "$OUT/$n" && echo "done $n ($r)"
done
echo CONFORM-DONE
