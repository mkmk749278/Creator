#!/usr/bin/env bash
# Render every HyperFrames scene and board for the film, one after another (PLAYBOOK §13: one render per session).
# Usage: setsid nohup bash projects/health-claim-trap/build/render_scenes.sh [ids...] > log 2>&1 < /dev/null & disown
set -u
ROOT=$(cd "$(dirname "$0")/../../.." && pwd); OUT=$ROOT/projects/health-claim-trap/assets/scenes; mkdir -p "$OUT"
IDS=${*:-"s00_receipts s01_letter s01b_overstamp s02_flow s03_ring s03b_family s04_clock b01_room b02_ombud b03_callback"}
for id in $IDS; do
  cd "$ROOT/video/healthclaim/$id" || continue
  echo "== $id $(date +%T)"
  npx hyperframes render --workers 4 --video-bitrate 12M --output "$OUT/$id.mp4" 2>&1 | tail -2
done
echo "ALL DONE $(date +%T)"
