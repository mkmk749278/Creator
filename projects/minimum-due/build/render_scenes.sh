#!/usr/bin/env bash
# Render the three money-mechanics scenes (1080p) into projects/minimum-due/assets/scenes/<id>.mp4 for the preview cut.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"; OUT="$ROOT/projects/minimum-due/assets/scenes"; mkdir -p "$OUT"
for id in s01_pay s02_timeline s03_allocation; do
  [ -s "$OUT/$id.mp4" ] && { echo "skip $id"; continue; }
  if (cd "$ROOT/video/minimumdue/$id" && npx --prefix "$ROOT" hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1); then
    cp "$ROOT/video/minimumdue/$id/render.mp4" "$OUT/$id.mp4" && echo "done $id"; else echo "FAIL $id"; tail -3 "$ROOT/video/minimumdue/$id/render.log"; fi
done
echo ALL_DONE
