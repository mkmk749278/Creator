#!/bin/bash
# Fallback: render the five parts one after another in a cloud session (normally the "Render film" workflow does this
# on GitHub's runners: PLAYBOOK §3a), then assemble the preview.
# usage: HYPERFRAMES_RENDER_DETACHED=1 setsid nohup bash projects/pharma-apis/build/render_parts.sh > /tmp/pha_parts.log 2>&1 < /dev/null & disown
cd "$(dirname "$0")/../../.."
mkdir -p projects/pharma-apis/assets/out
for i in 1 2 3 4 5; do
  echo "== p$i $(date +%T)"
  (cd video/pha/p$i && npx hyperframes render --workers 4 --video-bitrate 12M --output ../../../projects/pharma-apis/assets/out/p$i.mp4) 2>&1 | grep -v -E "^\s*$" | tail -3
  echo "done p$i $(date +%T)"
done
bash projects/pharma-apis/build/assemble.sh && echo ALLDONE
