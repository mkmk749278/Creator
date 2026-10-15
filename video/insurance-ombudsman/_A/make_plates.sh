#!/usr/bin/env bash
# Session A backplates: the owner's Pexels clips (asset pack F02/F07/F09/F10, Pexels licence, FOOTAGE_REGISTER.csv),
# pre-blurred for shallow depth of field (PLAYBOOK §9: fake DOF with a pre-blurred plate), graded toward the film's
# navy/daylight look, 1920x1080 30 fps, bitrate-capped. Output: <scene>/media/*.mp4 (gitignored).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
PACK=${PACK:-$HERE/../../../projects/insurance-ombudsman/assets/owner/BP_HLTH02_Asset_Pack/footage}
V=$HERE/..
plate() { # src start dur speed sigma out
  local src=$1 ss=$2 dur=$3 sp=$4 sg=$5 out=$6
  mkdir -p "$(dirname "$out")"
  ffmpeg -v error -y -ss "$ss" -t "$dur" -i "$PACK/$src" -an -vf "setpts=${sp}*PTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=${sg},eq=brightness=-0.04:saturation=0.85:gamma=0.95,fps=30" \
    -c:v libx264 -preset medium -crf 20 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -movflags +faststart "$out"
}
plate F07_7685212.mp4 1.0 10.5 1.35 9  "$V/A3_claim_cut/media/desk_f07.mp4"      # 14.2 s plate for O005 (13.2 s)
plate F02_6963962.mp4 4.0 3.0  1.4  26 "$V/A4_email_stamp/media/kitchen_f02.mp4"  # 4.2 s, behind the phone (O004)
plate F09_6406171.mp4 2.0 8.0  1.35 12 "$V/A4_email_stamp/media/desk_f09.mp4"    # 10.8 s, O025-O026
plate F10_8480684.mp4 4.0 18.0 1.35 12 "$V/A5_bima_tracker/media/desk_f10.mp4"   # 24.3 s, O017
plate F07_7685212.mp4 12.0 10.0 1.4 10 "$V/A2_three_doors/media/desk_f07b.mp4"   # 14 s, beyond the third door (O010)
plate F10_8480684.mp4 18.0 20.0 1.35 14 "$V/A6_gro_email/media/desk_f10b.mp4"   # 27 s, laptop desk for O029-O031
