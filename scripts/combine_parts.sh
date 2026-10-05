#!/usr/bin/env bash
# Join rendered parts into one video: concat, loudness-normalise the voice to
# YouTube's -14 LUFS, short fade in/out, H.264 High + AAC, faststart.
# Usage: scripts/combine_parts.sh OUT.mp4 part1.mp4 part2.mp4 ...
set -euo pipefail
out="$1"; shift
n=$#
inputs=(); filter=""
for i in $(seq 0 $((n-1))); do
  inputs+=(-i "${@:$((i+1)):1}")
  filter+="[$i:v:0][$i:a:0]"
done
total=$(for f in "$@"; do ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done | paste -sd+ | bc)
fade_out=$(echo "$total - 1.2" | bc)
filter+="concat=n=$n:v=1:a=1[v][a];"
filter+="[v]fade=t=in:st=0:d=0.6,fade=t=out:st=$fade_out:d=1.2,format=yuv420p[vo];"
filter+="[a]loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,afade=t=in:st=0:d=0.3,afade=t=out:st=$fade_out:d=1.2[ao]"
ffmpeg -y -loglevel error -stats "${inputs[@]}" -filter_complex "$filter" -map "[vo]" -map "[ao]" \
  -c:v libx264 -profile:v high -preset slow -crf 18 -r 30 -g 60 -c:a aac -b:a 192k -ac 2 \
  -movflags +faststart "$out"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height -of compact "$out"
