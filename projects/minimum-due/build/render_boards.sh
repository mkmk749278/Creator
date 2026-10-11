#!/usr/bin/env bash
# Render every board scene (1080p, pinned CLI) into projects/minimum-due/assets/boards/<id>.mp4; skips up-to-date ones.
set -uo pipefail
cd "$(dirname "$0")/../../../video/minimumdue"
OUT=../../projects/minimum-due/assets/boards; mkdir -p "$OUT"
for d in b*/; do s=${d%/}
  if [ -s "$OUT/$s.mp4" ] && [ "$OUT/$s.mp4" -nt "$s/params.js" ]; then echo "skip $s"; continue; fi
  (cd "$s" && npx hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1) && cp "$s/render.mp4" "$OUT/$s.mp4" && echo "done $s" || { echo "FAIL $s"; tail -3 "$s/render.log"; }
done
echo ALL_DONE
