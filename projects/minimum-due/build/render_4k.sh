#!/usr/bin/env bash
# Native 3840x2160 renders of every HyperFrames animation the refined cut uses (boards + money scenes), via
# scripts/make_native_4k.mjs (canvas 4K, 1080p layout in a zoom:2 stage; never --resolution 4k, PLAYBOOK §21).
# Output: projects/minimum-due/assets/{boards4k,scenes4k}/<id>.mp4; skips finished ones. Run detached:
#   nohup bash projects/minimum-due/build/render_4k.sh > render_4k.log 2>&1 &
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK="${WORK_4K:-/tmp/minimumdue_4k}"
A="$ROOT/projects/minimum-due/assets"
mkdir -p "$WORK" "$A/boards4k" "$A/scenes4k"
IDS="s01_pay s02_timeline s03_allocation b01_how b02_numbers b04_rules b05_newswipe b06_slow b07_crif b08_maths b09_loop b10_postpone b11_steps12 b12_emi b13_recap b14_next"
for id in $IDS; do
  case $id in s*) OUT="$A/scenes4k/$id.mp4";; *) OUT="$A/boards4k/$id.mp4";; esac
  if [ -s "$OUT" ]; then echo "skip $id"; continue; fi
  rm -rf "$WORK/$id"
  node "$ROOT/scripts/make_native_4k.mjs" "$ROOT/video/minimumdue/$id" "$WORK/$id" >/dev/null || { echo "FAIL copy $id"; continue; }
  # board pages size #root in px; the 4K canvas needs it to fill (else the zoom:2 stage is cropped to a quarter)
  sed -i 's/#root { position: relative; width: 1920px; height: 1080px;/#root { position: relative; width: 100%; height: 100%;/' "$WORK/$id/index.html"
  rm -f "$WORK/$id/render.mp4"
  if (cd "$WORK/$id" && npx --prefix "$ROOT" hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1); then
    cp "$WORK/$id/render.mp4" "$OUT" && echo "done $id $(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$OUT" | head -1)"
  else
    echo "FAIL $id"; tail -5 "$WORK/$id/render.log"
  fi
done
echo ALL_DONE
