#!/usr/bin/env bash
# Render scenes one after another (one render at a time per CLAUDE.md), each to <scene>/renders/<scene>.mp4,
# then verify duration and size. Start detached:
#   setsid nohup video/kavach-railway-reality/_tools/render_queue.sh C5_wrong_form C7_rewind_sim < /dev/null > /tmp/q.log 2>&1 & disown
V=$(cd "$(dirname "$0")/.." && pwd)
for id in "$@"; do
  w=4; grep -q "vendor/three/" "$V/$id/index.html" && w=3
  mkdir -p "$V/$id/renders"
  (cd "$V/$id" && npx hyperframes render --workers $w --output "renders/$id.mp4" > renders/render.log 2>&1)
  f="$V/$id/renders/$id.mp4"
  if [ -f "$f" ]; then
    echo "DONE $id $(ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of csv=p=0 "$f" | tr '\n' ' ') spec=$(grep -o 'data-duration="[0-9.]*"' "$V/$id/index.html")"
  else
    echo "FAILED $id: $(tail -3 "$V/$id/renders/render.log" | tr '\n' ' ')"
  fi
done
echo "QUEUE FINISHED"
