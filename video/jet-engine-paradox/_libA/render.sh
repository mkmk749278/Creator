#!/usr/bin/env bash
# Render Session A scenes one after another with the repo's pinned CLI: _libA/render.sh A6_spin_bus A5_thermal_reveal ...
cd "$(dirname "$0")/.."
HF=/home/user/Creator/node_modules/.bin/hyperframes
export HYPERFRAMES_RENDER_DETACHED=1   # the CLI otherwise aborts when any ancestor (the launching shell) exits
for id in "$@"; do
  t0=$(date +%s)
  ( cd "$id" && mkdir -p renders && echo "== $id start $(date +%T)" && "$HF" render --workers 3 --output "renders/$id.mp4" ) > "$id/render.log" 2>&1
  echo "$id wall $(( $(date +%s) - t0 ))s" >> _libA/render_status.txt
  echo "$id done $(date +%T) rc=$?" >> _libA/render_status.txt
done
