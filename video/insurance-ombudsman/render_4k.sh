#!/usr/bin/env bash
# Native 3840x2160 renders of every Episode 02 scene (scripts/make_native_4k.mjs: 4K canvas, the 1080p layout in a
# zoom:2 stage; never --resolution 4k, PLAYBOOK §21), then split_4k.py cuts the per-window clips into
# projects/insurance-ombudsman/assets/scenes/. Skips scenes whose render is newer than their index.html.
# Run detached: setsid nohup video/insurance-ombudsman/render_4k.sh [scene ...] > render_4k.log 2>&1 < /dev/null & disown
set -uo pipefail
# detached renders: without this HyperFrames aborts (render_cancelled_parent_exited) when the launching shell exits
export HYPERFRAMES_RENDER_DETACHED=1
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
WORK="$HERE/_4k"; mkdir -p "$WORK"
scenes=("$@"); [ ${#scenes[@]} -eq 0 ] && scenes=(A1_staircase A2_three_doors A3_claim_cut A4_email_stamp A5_bima_tracker A6_gro_email
  B1_fee_split B2_two_step_clock B3_penalty_meter B4_time_stats C1_filing_stepper C2_offices_board C3_document_slots C4_binding_award
  C5_proof_magnifier C6_hearing)
for s in "${scenes[@]}"; do
  out="$WORK/$s.mp4"
  if [ -s "$out" ] && [ "$out" -nt "$HERE/$s/index.html" ]; then echo "skip $s"; continue; fi
  echo "== $s start $(date +%T)"
  rm -rf "$WORK/$s"
  node "$ROOT/scripts/make_native_4k.mjs" "$HERE/$s" "$WORK/$s" >/dev/null || { echo "== $s FAIL copy"; continue; }
  if (cd "$WORK/$s" && npx --prefix "$ROOT" hyperframes render . --workers 4 --crf 16 --output "$WORK/tmp_$s.mp4" > "$WORK/$s.render.log" 2>&1); then
    mv "$WORK/tmp_$s.mp4" "$out"
    python3 "$HERE/split_4k.py" "$s" "$out" || echo "== $s SPLIT FAILED"
    echo "== $s done $(date +%T)"
  else
    echo "== $s FAILED"; tail -5 "$WORK/$s.render.log"
  fi
done
echo "== ALL DONE $(date +%T)"
