#!/bin/bash
# Render the rare earth film's scenes one after another (one render at a time per session; CLAUDE.md traps).
# usage: HYPERFRAMES_RENDER_DETACHED=1 setsid nohup bash video/rem/render_all.sh motor siblings tanks grain > /tmp/rem_render.log 2>&1 < /dev/null & disown
cd "$(dirname "$0")"
OUT=../../projects/rare-earth-magnets/assets/renders
for s in "$@"; do
  echo "== $s $(date +%T)"
  (cd "$s" && npx hyperframes render --workers 3 --output "../$OUT/$s.mp4") 2>&1 | grep -v -E "^\s*$" | tail -3
  echo "done $s $(date +%T)"
done
echo ALLDONE
