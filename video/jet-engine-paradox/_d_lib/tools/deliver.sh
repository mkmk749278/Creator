#!/usr/bin/env bash
# Check a rendered D scene (duration, size, fps), make its contact sheet and upload both to Drive: deliver.sh D1_globe_lynn
cd "$(dirname "$0")/../.."
id=$1; mp4="$id/renders/$id.mp4"; [ -s "$mp4" ] || { echo "missing $mp4"; exit 1; }
want=$(grep -oP 'duration:\s*\K[\d.]+' "$id/params.js")
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:format=duration -of csv=p=0 "$mp4" | tr '\n' ' '; echo " (spec $want s)"
mkdir -p "$id/renders/sheet" && python3 /home/user/Creator/scripts/contact_sheet.py "$mp4" --out "$id/renders/sheet" --every 1 >/dev/null
sheet=$(ls "$id"/renders/sheet/*.jpg | head -1); cp "$sheet" "$id/renders/${id}_sheet.jpg"
/home/user/Creator/scripts/upload_gdrive.sh --sub jet-engine-paradox/scenes/D "$mp4" "$id/renders/${id}_sheet.jpg"
