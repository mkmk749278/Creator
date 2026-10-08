#!/usr/bin/env bash
# Copy _shared/ into every Fire and Ice scene (shared/ copies are gitignored) and vendor GSAP/fonts/Three.
# Scenes with an OWN_SHARED file (logo sting, end card) use the channel brand theme from video/prahlad/_shared.
set -euo pipefail
cd "$(dirname "$0")"
for d in */; do
  d=${d%/}; [ "$d" = _shared ] && continue; [ -f "$d/index.html" ] || continue
  mkdir -p "$d/shared"
  if [ -f "$d/OWN_SHARED" ]; then cp -r ../prahlad/_shared/. "$d/shared/"; else cp -r _shared/. "$d/shared/"; fi
done
(cd ../.. && node scripts/vendor-assets.mjs)
