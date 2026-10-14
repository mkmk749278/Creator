#!/usr/bin/env bash
# Native 3840x2160 renders of the film's HyperFrames scenes (scripts/make_native_4k.mjs; never --resolution 4k, PLAYBOOK §21).
# Output: projects/health-claim-trap/assets/scenes4k/<id>.mp4; skips finished ones. Run detached (setsid nohup ... & disown).
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK="${WORK_4K:-/tmp/healthclaim_4k}"
OUTD="$ROOT/projects/health-claim-trap/assets/scenes4k"
mkdir -p "$WORK" "$OUTD"
for id in "$@"; do
  OUT="$OUTD/$id.mp4"
  if [ -s "$OUT" ]; then echo "skip $id"; continue; fi
  rm -rf "$WORK/$id"
  node "$ROOT/scripts/make_native_4k.mjs" "$ROOT/video/healthclaim/$id" "$WORK/$id" >/dev/null || { echo "FAIL copy $id"; continue; }
  sed -i 's/#root { position: relative; width: 1920px; height: 1080px;/#root { position: relative; width: 100%; height: 100%;/' "$WORK/$id/index.html"
  echo "== $id $(date +%T)"
  if (cd "$WORK/$id" && npx --prefix "$ROOT" hyperframes render . --workers 4 --video-bitrate 40M --output render.mp4 > render.log 2>&1); then
    cp "$WORK/$id/render.mp4" "$OUT" && echo "done $id $(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$OUT" | head -1) $(grep -o 'rendered in [0-9ms. ]*' "$WORK/$id/render.log")"
  else
    echo "FAIL $id"; tail -5 "$WORK/$id/render.log"
  fi
  rm -rf "$WORK/$id"
done
echo ALL_DONE
