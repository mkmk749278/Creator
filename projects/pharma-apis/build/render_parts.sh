#!/bin/bash
# Fallback: render the five parts one after another in a cloud session (normally the "Render film" workflow does this
# on GitHub's runners: PLAYBOOK §3a), then assemble the cut.
# usage: [RES=720] HYPERFRAMES_RENDER_DETACHED=1 setsid nohup bash projects/pharma-apis/build/render_parts.sh [3 4 5] > /tmp/pha_parts.log 2>&1 < /dev/null & disown
# (part numbers default to all five; parts already rendered are kept). RES=720 renders native 1280x720 copies for
# review rounds (owner, 2026-10-29: review cuts 720p, 4K only after finalising) into assets/out/720/.
cd "$(dirname "$0")/../../.."
RES=${RES:-1080}
if [ "$RES" = 720 ]; then OUT=projects/pharma-apis/assets/out/720; RATE=5M; else OUT=projects/pharma-apis/assets/out; RATE=12M; fi
mkdir -p "$OUT"
for i in ${@:-1 2 3 4 5}; do
  echo "== p$i $(date +%T)"
  dir=video/pha/p$i
  if [ "$RES" = 720 ]; then rm -rf "video/pha/p${i}_720"; node scripts/make_native_res.mjs "$dir" "video/pha/p${i}_720" 1280 >/dev/null; dir=video/pha/p${i}_720; fi
  (cd "$dir" && npx hyperframes render --workers 4 --video-bitrate $RATE --output "$PWD/../../../$OUT/p$i.mp4") 2>&1 | grep -v -E "^\s*$" | tail -3
  echo "done p$i $(date +%T)"
done
if [ "$RES" = 720 ]; then
  PARTS_DIR=$PWD/$OUT bash projects/pharma-apis/build/assemble.sh "$PWD/projects/pharma-apis/assets/out/pharma_apis_720.mp4" && echo ALLDONE
else
  bash projects/pharma-apis/build/assemble.sh && echo ALLDONE
fi
