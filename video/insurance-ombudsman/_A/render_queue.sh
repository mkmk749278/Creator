#!/usr/bin/env bash
# Render session A scenes one after another (one render at a time per session; CLAUDE.md cloud traps).
cd "$(dirname "$0")/.."
for s in "$@"; do
  if [[ $s == A1_staircase_corner ]]; then
    (cd $s && npx hyperframes render --workers 4 --format mov --output renders/full.mov > render.log 2>&1)
  else
    (cd $s && npx hyperframes render --workers 4 --crf 18 --output renders/full.mp4 > render.log 2>&1)
  fi
  echo "$s exit=$?" >> _A/render_status.txt
done
echo DONE >> _A/render_status.txt
