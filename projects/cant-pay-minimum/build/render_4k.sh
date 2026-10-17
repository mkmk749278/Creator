#!/usr/bin/env bash
# Native 3840x2160 renders of the film's scenes (video/cantpay/<id>) via scripts/make_native_4k.mjs (4K canvas, 1080p
# layout in a zoom:2 stage; never --resolution 4k, PLAYBOOK §21) into projects/cant-pay-minimum/assets/scenes4k/<id>.mp4.
# IDS="..." renders a shard. Skips finished ones. Run detached:
#   IDS="a b" setsid nohup bash projects/cant-pay-minimum/build/render_4k.sh < /dev/null > /tmp/cpm4k.log 2>&1 & disown
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK="${WORK_4K:-/tmp/cantpay_4k}"; OUT="$ROOT/projects/cant-pay-minimum/assets/scenes4k"; mkdir -p "$WORK" "$OUT"
IDS="${IDS:-$(ls "$ROOT/video/cantpay")}"
for id in $IDS; do
  [ -s "$OUT/$id.mp4" ] && { echo "skip $id"; continue; }
  rm -rf "$WORK/$id"; t0=$(date +%s)
  node "$ROOT/scripts/make_native_4k.mjs" "$ROOT/video/cantpay/$id" "$WORK/$id" >/dev/null || { echo "FAIL copy $id"; continue; }
  # pages size #root in px; the 4K canvas needs it to fill (else the zoom:2 stage shows a quarter of the frame)
  sed -i 's/\(#root {[^}]*\)width: 1920px; height: 1080px;/\1width: 100%; height: 100%;/' "$WORK/$id/index.html"
  if (cd "$WORK/$id" && npx --prefix "$ROOT" hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1); then
    cp "$WORK/$id/render.mp4" "$OUT/$id.mp4" && echo "done $id $(( $(date +%s) - t0 ))s $(ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$OUT/$id.mp4" | head -1)"
  else echo "FAIL $id"; tail -5 "$WORK/$id/render.log"; fi
done
echo ALL_DONE
