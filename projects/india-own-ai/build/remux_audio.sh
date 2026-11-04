#!/usr/bin/env bash
# Round 3 / 4K master: the picture changed, the VO timing did not, so the master audio is the approved r2 mix
# (−14.2 LUFS, peak −1.8 dBFS, measured in the r2 review) laid under the new parts unchanged. Use this when the
# session has no voice/ and audio/ stems (they live with the session that built r1); assemble.sh rebuilds the mix from stems.
# usage: PARTS_DIR=dir bash projects/india-own-ai/build/remux_audio.sh AUDIO_SOURCE.mp4 OUT.mp4
set -euo pipefail
src=${1:?r2 cut with the approved mix}; out=${2:?output}
tmp=$(mktemp -d); : > "$tmp/list.txt"
n=$(ls "$PARTS_DIR"/*p[0-9]*.mp4 | wc -l); for i in $(seq 1 "$n"); do f=$(ls "$PARTS_DIR"/*p$i.mp4 | head -1); echo "file '$(realpath "$f")'" >> "$tmp/list.txt"; done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$tmp/list.txt" -an -c copy "$tmp/video.mp4"
vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$tmp/video.mp4"); ad=$(ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 "$src")
echo "video $vd s, audio $ad s"
ffmpeg -y -loglevel error -i "$tmp/video.mp4" -i "$src" -map 0:v -map 1:a -c:v copy -c:a copy -movflags +faststart -shortest "$out"
ffmpeg -hide_banner -i "$out" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
rm -rf "$tmp"; echo "wrote $out"
