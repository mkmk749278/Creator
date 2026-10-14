#!/usr/bin/env bash
# Render Session D scenes one after another with the pinned CLI: _d_lib/tools/render.sh D1_globe_lynn [...]
cd "$(dirname "$0")/../.."
HF=/home/user/Creator/node_modules/.bin/hyperframes
export HYPERFRAMES_RENDER_DETACHED=1
for id in "$@"; do
  t0=$(date +%s); w=$(grep -q "vendor/three/" "$id/index.html" && echo 3 || echo 4)
  ( cd "$id" && mkdir -p renders && "$HF" render --workers $w --output "renders/$id.mp4" ) > "$id/render.log" 2>&1
  echo "$id rc=$? wall $(( $(date +%s) - t0 ))s $(date +%T)" >> _d_lib/render_status.txt
done
