#!/usr/bin/env bash
# Cut the Episode 01 glimpses (PLAYBOOK §4a-4: 2-4 s, labelled FROM EPISODE 1) from the owner's v5 cut in Drive
# (Creator/English/health-claim-trap/health-claim-trap-preview-v5-2160p.mp4 -> assets/episode1/ep01-v5-2160p.mp4).
# Video only (Episode 02 has its own VO and music); 4K kept, bitrate capped.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=assets/episode1/ep01-v5-2160p.mp4
OUT=assets/episode1/glimpses; mkdir -p "$OUT"
# name start duration   (Episode 01 EDL rows; used under O001-O002)
while read -r name ss dur; do
  [[ -z $name || $name == \#* ]] && continue
  ffmpeg -nostdin -v error -y -ss "$ss" -i "$SRC" -t "$dur" -an -c:v libx264 -preset slow -crf 18 -maxrate 45M -bufsize 90M \
    -pix_fmt yuv420p "$OUT/$name.mp4"
  echo "$OUT/$name.mp4"
done <<'LIST'
g1_counter     21.40 3.0
g2_bill        28.05 3.0
g3_denied      38.40 3.5
g4_step1       344.0 2.5
g5_step2       383.0 2.5
g6_step3_bima  399.5 2.5
g7_step4_cio   419.0 2.5
LIST
