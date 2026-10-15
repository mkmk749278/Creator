#!/usr/bin/env bash
# Render every session-C scene (1920x1080, 30 fps) one after another, then split into per-VO-window clips.
# Start detached:  setsid nohup ./render_all.sh > renders/render.log 2>&1 < /dev/null & disown
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p renders
for s in ${SCENES:-C1_filing_stepper C2_offices_board C3_document_slots C4_binding_award C5_proof_magnifier}; do
  echo "== $s start $(date +%T)"
  ( cd "$s" && npx hyperframes render --workers 4 --quality looks --output "../renders/$s.master.mp4" ) || { echo "== $s FAILED"; continue; }
  echo "== $s done $(date +%T)"
  python3 split_clips.py "$s" || echo "== $s SPLIT FAILED"
done
echo "== ALL DONE $(date +%T)"
