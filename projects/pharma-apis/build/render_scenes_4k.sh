#!/bin/bash
# Native 3840x2160 renders of the animated scenes for the 4K master (text and lines stay sharp, not upscaled 1080p).
# usage: HYPERFRAMES_RENDER_DETACHED=1 setsid nohup bash projects/pharma-apis/build/render_scenes_4k.sh [scene...] > log 2>&1 < /dev/null & disown
cd "$(dirname "$0")/../../.."
OUT=projects/pharma-apis/assets/renders4k; mkdir -p "$OUT"
for s in ${@:-capsule_open cipla fermenter fermenter_lit map_home map_hubei map_india map_stream map_trade mipgate tablet tanks}; do
  [ -f "$OUT/video_pha_$s.mp4" ] && { echo "have $s"; continue; }
  rm -rf "video/pha/${s}_4k"; node scripts/make_native_res.mjs "video/pha/$s" "video/pha/${s}_4k" 3840 >/dev/null
  (cd "video/pha/${s}_4k" && npx hyperframes render --workers 4 --video-bitrate 40M --output "$PWD/../../../$OUT/video_pha_$s.mp4" 2>&1 | grep -E "rendered in|rror" | tail -1)
  rm -rf "video/pha/${s}_4k"; echo "done $s $(date +%T)"
done
echo SCENES4K-DONE
