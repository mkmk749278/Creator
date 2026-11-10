#!/usr/bin/env bash
# Collect one Blender hero shot from blender-render.yml: download its shard artifacts, check that every frame is there,
# encode a bitrate-capped 30 fps clip (frames rendered at step 2 of 60 fps), report the largest frame-to-frame
# brightness jump (flash check), make a contact sheet, upload the clip to Drive and delete the frames.
#
#   scripts/blender_collect.sh <slug> <shot> <clip-name> <expected-frames> URL [URL ...]
#   e.g. scripts/blender_collect.sh matsya-6000 seam H2_seam 480 "<artifact url>" "<artifact url>" ...
# The artifact URLs come from the GitHub tool download_workflow_run_artifact (they expire in about 10 minutes).
set -euo pipefail
slug=$1 shot=$2 clip=$3 want=$4
shift 4
ROOT=$(cd "$(dirname "$0")/.." && pwd)
dir="$ROOT/projects/$slug/assets/renders"
mkdir -p "$dir/$shot" "$dir/zips"
i=0
for u in "$@"; do
  i=$((i + 1))
  z="$dir/zips/${shot}_$i.zip"
  curl -sS -C - --retry 4 --retry-delay 2 -o "$z" "$u"
  unzip -q -o "$z" -d "$dir/$shot"
  rm -f "$z"
done
have=$(find "$dir/$shot" -name "${shot}_*.png" | wc -l)
echo "$shot: $have frames (want $want)"
[[ $have -eq $want ]] || { echo "frame count mismatch" >&2; exit 4; }
ffmpeg -v error -y -framerate 30 -pattern_type glob -i "$dir/$shot/${shot}_*.png" -c:v libx264 -preset slow -crf 14 \
  -maxrate 30M -bufsize 60M -pix_fmt yuv420p -movflags +faststart "$dir/$clip.mp4"
ffmpeg -v error -i "$dir/$clip.mp4" -vf signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=- -f null - \
  | grep YAVG | awk -F= '{print $2}' | python3 -c "
import sys
v = [float(x) for x in sys.stdin]
d = [abs(b - a) for a, b in zip(v, v[1:])]
print(f'{len(v)} frames, mean luma {sum(v)/len(v):.1f}, largest jump {max(d):.2f} at frame {d.index(max(d))}')"
python3 "$ROOT/scripts/contact_sheet.py" "$dir/$clip.mp4" --out "$dir/sheet_$shot" --every 1 >/dev/null
"$ROOT/scripts/upload_gdrive.sh" --sub "English/$slug/renders" "$dir/$clip.mp4" 2>/dev/null
rm -r "${dir:?}/${shot:?}"
