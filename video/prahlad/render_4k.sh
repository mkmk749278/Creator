#!/usr/bin/env bash
# Render every documentary insert at native 4K and copy it into the film's assets as hf_<scene>.mp4.
# Usage: video/prahlad/render_4k.sh [scene ...]   (default: all scenes)
set -euo pipefail
cd "$(dirname "$0")/../.."
ASSETS=projects/prahlad-jani-drdo/assets
scenes=("$@"); [ ${#scenes[@]} -eq 0 ] && scenes=(logo_sting end_card timeline_a timeline_b vitals kidney3d bladder3d autophagy3d dehydration_chart metabolism)
for s in "${scenes[@]}"; do
  out=video/prahlad_4k/$s/render.mp4
  if [ ! -s "$out" ] || [ video/prahlad/$s/index.html -nt "$out" ]; then
    rm -rf video/prahlad_4k/$s
    node scripts/make_native_4k.mjs video/prahlad/$s video/prahlad_4k/$s >/dev/null
    (cd video/prahlad_4k/$s && npx hyperframes render . --workers 4 -q high --output render.mp4 2>&1 | tail -2)
  fi
  cp "$out" "$ASSETS/hf_$s.mp4"
  echo "done $s $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")s"
done
echo ALL_DONE
