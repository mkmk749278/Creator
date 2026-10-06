#!/usr/bin/env bash
# Join hook + acts into the master: re-encode once, normalise loudness to -14 LUFS.
set -euo pipefail
cd "$(dirname "$0")/renders"
printf "file '%s'\n" p0_hook.mp4 p1.mp4 p2.mp4 p3.mp4 > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 -movflags +faststart \
  -af "aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k chip-gamble-master-1080p.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 chip-gamble-master-1080p.mp4
