#!/usr/bin/env bash
# Render the film's HyperFrames scenes (video/cantpay/<id>) to projects/cant-pay-minimum/assets/scenes/<id>.mp4 (1080p).
# Skips a scene whose render is newer than its params.js and images. IDS="..." renders a subset. Run detached:
#   setsid nohup bash projects/cant-pay-minimum/build/render_scenes.sh < /dev/null > /tmp/cpm_render.log 2>&1 & disown
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT="$ROOT/projects/cant-pay-minimum/assets/scenes"; mkdir -p "$OUT"
IDS="${IDS:-$(ls "$ROOT/video/cantpay")}"
for id in $IDS; do
  d="$ROOT/video/cantpay/$id"; [ -f "$d/params.js" ] || continue
  if [ -s "$OUT/$id.mp4" ] && [ -z "$(find "$d/params.js" "$d/img" "$ROOT/video/lib/doodle/doodle.js" "$ROOT/video/lib/plates/plates.js" -newer "$OUT/$id.mp4" 2>/dev/null | head -1)" ]; then echo "skip $id"; continue; fi
  t0=$(date +%s)
  if (cd "$d" && npx --prefix "$ROOT" hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1); then
    cp "$d/render.mp4" "$OUT/$id.mp4" && echo "done $id $(( $(date +%s) - t0 ))s"
  else echo "FAIL $id"; tail -3 "$d/render.log"; fi
done
echo ALL_DONE
