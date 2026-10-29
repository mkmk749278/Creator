#!/bin/bash
# Package each film part's media (gitignored: footage, conformed clips, 4K scene renders) for the "Render film" workflow:
# one tar per part, uploaded to Drive Creator/English/pharma-apis/build/parts/pN/. The workflow pulls that folder and
# unpacks the tar in place (paths from the repo root), then renders the part (PLAYBOOK §3a).
# usage: bash projects/pharma-apis/build/pack_parts.sh [1 2 3 4 5]
set -euo pipefail
cd "$(dirname "$0")/../../.."
T=projects/pharma-apis/assets/out/tars; mkdir -p "$T"
for i in ${@:-1 2 3 4 5}; do
  tar cf "$T/p$i.tar" "video/pha/p$i/media" "video/pha/p$i/shared"
  echo "p$i $(du -h "$T/p$i.tar" | cut -f1)"
  bash scripts/upload_gdrive.sh --sub "English/pharma-apis/build/parts/p$i" "$T/p$i.tar" | tail -1
done
