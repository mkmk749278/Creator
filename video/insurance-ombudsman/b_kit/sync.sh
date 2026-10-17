#!/usr/bin/env bash
# Copy the session B kit (kit.css, kit.js, plates) into each B scene's kit/ folder. Run after editing b_kit/.
set -euo pipefail
cd "$(dirname "$0")"
for d in ../B1_fee_split ../B2_two_step_clock ../B3_penalty_meter ../B4_time_stats; do
  [[ -d $d ]] || continue
  mkdir -p "$d/kit"; cp kit.css kit.js plates/desk.jpg plates/light.png plates/paper.jpg "$d/kit/"
done
