#!/usr/bin/env bash
# After a scene render: probe it, make contact sheets + preview.jpg, upload MP4 + sheets to Drive (scenes/A).
set -euo pipefail
cd "$(dirname "$0")/.."; ROOT=/home/user/Creator
id=$1; mp4="$id/renders/$id.mp4"
spec=$(python3 -c "import json;print(json.load(open('$ROOT/projects/jet-engine-paradox/scenes.json'))['$id']['duration'])")
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration -of csv=p=0 "$mp4" | tr '\n' ' '; echo " (spec $spec s)"
rm -rf "$id/qa"; python3 "$ROOT/scripts/contact_sheet.py" "$mp4" --out "$id/qa" --every 1 >/dev/null
python3 -c "from PIL import Image; im=Image.open('$id/qa/sheet-01.jpg'); im.thumbnail((1200,1200)); im.save('$id/preview.jpg', quality=82)"
for f in "$id"/qa/sheet-*.jpg; do cp "$f" "/tmp/claude-0/${id}_$(basename "$f")"; done
"$ROOT/scripts/upload_gdrive.sh" --sub jet-engine-paradox/scenes/A "$mp4" /tmp/claude-0/${id}_sheet-*.jpg | tee -a _libA/links.txt
