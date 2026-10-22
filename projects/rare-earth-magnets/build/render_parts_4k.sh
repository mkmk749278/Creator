#!/bin/bash
# Native 4K master (CLAUDE.md: never --resolution 4k): each 1080p part (video/rem/pN, written by make_film.py) is copied
# to a 3840x2160 project by scripts/make_native_4k.mjs and rendered one at a time; then assemble.sh lays the same
# master audio under the 4K parts. Footage stays 1080p (upscaled by the browser); text, vectors and HUD are native 4K.
# usage: HYPERFRAMES_RENDER_DETACHED=1 setsid nohup bash projects/rare-earth-magnets/build/render_parts_4k.sh > /tmp/rem_4k.log 2>&1 < /dev/null & disown
cd "$(dirname "$0")/../../.."
OUT=$PWD/projects/rare-earth-magnets/assets/out/4k; mkdir -p $OUT
for i in ${PARTS:-1 2 3 4 5}; do
  echo "== p$i $(date +%T)"
  rm -rf video/rem/p${i}_4k && node scripts/make_native_4k.mjs video/rem/p$i video/rem/p${i}_4k
  (cd video/rem/p${i}_4k && npx hyperframes render --workers ${WORKERS:-4} --output $OUT/p$i.mp4) 2>&1 | grep -v -E "^\s*$" | tail -3
  rm -rf video/rem/p${i}_4k
  echo "done p$i $(date +%T)"
done
PARTS_DIR=$OUT bash projects/rare-earth-magnets/build/assemble.sh projects/rare-earth-magnets/assets/out/rare_earth_magnets_4k_master.mp4 && echo ALLDONE
