#!/usr/bin/env bash
# Cut each scene's full render into one clip per VO window (window + 0.25 s handle each side) and make a
# 4-frame contact sheet per clip. Output: ../_A/out/ (gitignored via *.mp4/*.jpg rules).
set -euo pipefail
cd "$(dirname "$0")/.."; OUT=_A/out; mkdir -p $OUT
FONT=$(fc-match -f '%{file}' "DejaVu Sans:bold" 2>/dev/null || true)
clip() { # scene id start dur
  local s=$1 id=$2 ss=$3 d=$4 o="$OUT/${1}_${2}.mp4" n
  [[ -f $s/renders/full.mp4 ]] || { echo "skip $s (no render)"; return; }
  n=$(python3 -c "print(round($d*30))")
  ffmpeg -v error -y -i $s/renders/full.mp4 -ss "$ss" -frames:v "$n" -an -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M \
    -pix_fmt yuv420p -r 30 -movflags +faststart "$o"
  local args=() f=""
  for k in 0 1 2 3; do t=$(python3 -c "print(round($d*(2*$k+1)/8,2))"); args+=(-ss "$t" -i "$o"); f+="[$k:v]scale=960:540,drawtext=fontfile=$FONT:text='${1}_${2}  t=${t}s':x=16:y=16:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8[v$k];"; done
  ffmpeg -v error -y "${args[@]}" -frames:v 1 -filter_complex "${f}[v0][v1]hstack[a];[v2][v3]hstack[b];[a][b]vstack" "$OUT/${1}_${2}_sheet.jpg"
  echo "$o $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$o")"
}
clip A1_staircase O002 0 21.70
clip A1_staircase O009 21.70 6.62
clip A2_three_doors O006 0 4.42
clip A2_three_doors O007 4.38 6.86
clip A2_three_doors O008 11.01 12.19
clip A2_three_doors O009 23.07 6.62
clip A2_three_doors O010 29.62 19.66
clip A3_claim_cut O005 0 13.21
clip A4_email_stamp O004 0 3.27
clip A4_email_stamp O025 3.27 6.11
clip A4_email_stamp O026 9.34 3.66
clip A5_bima_tracker O017 0 23.54
if [[ -f A1_staircase_corner/renders/full.mov ]]; then
  cp A1_staircase_corner/renders/full.mov $OUT/A1_staircase_corner.mov
  # preview of the alpha clip over a mid-grey plate, for the contact sheet
  ffmpeg -v error -y -f lavfi -i color=c=0x556070:s=1920x1080:r=30:d=6 -i $OUT/A1_staircase_corner.mov -filter_complex "[0][1]overlay=shortest=1" -c:v libx264 -crf 20 -pix_fmt yuv420p $OUT/.a1corner_prev.mp4
  args=(); f=""; for k in 0 1 2 3; do t=$(python3 -c "print(round(6*(2*$k+1)/8,2))"); args+=(-ss $t -i $OUT/.a1corner_prev.mp4); f+="[$k:v]scale=960:540,drawtext=fontfile=$FONT:text='A1_staircase_corner (alpha, over grey)  t=${t}s':x=16:y=16:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8[v$k];"; done
  ffmpeg -v error -y "${args[@]}" -frames:v 1 -filter_complex "${f}[v0][v1]hstack[a];[v2][v3]hstack[b];[a][b]vstack" $OUT/A1_staircase_corner_sheet.jpg
fi
