#!/usr/bin/env bash
# Render Fire and Ice scenes at 1080p (pinned CLI) into projects/fire-and-ice/assets/hf/<scene>.mp4.
# Usage: video/fireice/render_all.sh [scene ...]  (default: every scene folder). Re-renders only when index.html is newer.
set -uo pipefail
cd "$(dirname "$0")"
OUT=../../projects/fire-and-ice/assets/hf; mkdir -p "$OUT"
scenes=("$@"); [ ${#scenes[@]} -eq 0 ] && scenes=($(for d in */; do [ -f "$d/index.html" ] && echo "${d%/}"; done))
for s in "${scenes[@]}"; do
  if [ -s "$OUT/$s.mp4" ] && [ "$OUT/$s.mp4" -nt "$s/index.html" ] && [ "$OUT/$s.mp4" -nt _shared/body.js ]; then echo "skip $s"; continue; fi
  start=$(date +%s)
  (cd "$s" && npx hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1) && cp "$s/render.mp4" "$OUT/$s.mp4" \
    && echo "done $s $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$s.mp4")s in $(( $(date +%s) - start ))s" \
    || { echo "FAIL $s"; tail -5 "$s/render.log"; }
done
echo ALL_DONE
