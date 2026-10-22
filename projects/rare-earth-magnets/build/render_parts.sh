#!/bin/bash
# Render the film's parts one after another (one render at a time; CLAUDE.md traps), then assemble the preview.
# usage: HYPERFRAMES_RENDER_DETACHED=1 setsid nohup bash projects/rare-earth-magnets/build/render_parts.sh > /tmp/rem_parts.log 2>&1 < /dev/null & disown
cd "$(dirname "$0")/../../.."
mkdir -p projects/rare-earth-magnets/assets/out
for i in 1 2 3 4 5; do
  echo "== p$i $(date +%T)"
  (cd video/rem/p$i && npx hyperframes render --workers 4 --output ../../../projects/rare-earth-magnets/assets/out/p$i.mp4) 2>&1 | grep -v -E "^\s*$" | tail -3
  echo "done p$i $(date +%T)"
done
bash projects/rare-earth-magnets/build/assemble.sh && echo ALLDONE
