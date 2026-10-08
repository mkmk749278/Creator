#!/usr/bin/env bash
# 2.5D plate + subject cutout for a photo: <name>.jpg -> <name>_plate.jpg + <name>_fg.png
set -euo pipefail
cd "$(dirname "$0")/assets"
for n in "$@"; do
  [ -f "${n}_fgraw.png" ] || npx --prefix ../../.. hyperframes remove-background "$n.jpg" -o "${n}_fgraw.png" >/dev/null 2>&1
  ffmpeg -v error -y -i "${n}_fgraw.png" -vf "scale=1920:-2:flags=lanczos" "${n}_fg.png"
  ffmpeg -v error -y -i "$n.jpg" -vf "scale=1920:-2:flags=lanczos,gblur=sigma=14,eq=brightness=-0.08:saturation=0.8" -q:v 3 "${n}_plate.jpg"
  echo "parallax: $n"
done
