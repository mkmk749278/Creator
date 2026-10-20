#!/usr/bin/env bash
# Render film 01 Blender shots, encode each to MP4 and upload it to Drive (Creator/English/upi-money-deducted/renders).
# Usage: video/upi01/blender/render_shots.sh B09 B11 ...   (run from the repo root; resumable: finished frames are skipped)
# Start detached: setsid nohup video/upi01/blender/render_shots.sh B09 B11 > /tmp/render.log 2>&1 < /dev/null & disown
set -u
cd "$(git rev-parse --show-toplevel)"
V=${BPY_VENV:-$HOME/bpyenv}; OUT=${RENDER_OUT:-$HOME/upi01_renders}; SPP=${SPP:-6}; RES=${RES:-1280x720}
[ -x "$V/bin/python" ] || { python3 -m venv "$V" && "$V/bin/pip" install -q bpy==5.2.2; }
mkdir -p "$OUT"
for s in "$@"; do
  [ -f "$OUT/$s.uploaded" ] && { echo "SKIP $s (uploaded)"; continue; }
  echo "START $s $(date -u +%T)"
  nice -n 10 "$V/bin/python" -I video/upi01/blender/film.py -- "$s" "$SPP" "$OUT/$s" "$RES" 2>&1 | grep -E 'FILM|Traceback|Error:' | grep -v CUEW
  case "$s" in S*) cp "$OUT/$s/f_0001.png" "$OUT/$s.png"; f="$OUT/$s.png" ;;
    *) ffmpeg -hide_banner -loglevel error -y -framerate 24 -i "$OUT/$s/f_%04d.png" -c:v libx264 -pix_fmt yuv420p \
         -crf 12 -preset slow -maxrate 40M -bufsize 80M "$OUT/$s.mp4" && f="$OUT/$s.mp4" ;;
  esac
  if scripts/upload_gdrive.sh --sub English/upi-money-deducted/renders "$f"; then touch "$OUT/$s.uploaded"; fi
  echo "DONE $s $(date -u +%T)"
done
echo "ALL DONE"
