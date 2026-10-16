#!/usr/bin/env bash
# Native 4K renders (CLAUDE.md: never --resolution 4k). For each scene: copy it with scripts/make_native_4k.mjs into
# $OUT/<scene> (3840x2160 root, the 1080p layout zoomed 2x), render there, verify. One render at a time. Start detached:
#   OUT=/path setsid nohup video/kavach-railway-reality/_tools/render_4k.sh A1_atp_watch ... < /dev/null > q.log 2>&1 & disown
V=$(cd "$(dirname "$0")/.." && pwd); R=$(cd "$V/../.." && pwd); OUT=${OUT:?set OUT}
# Resumable: a scene with a .done marker is skipped, so after a VM pause or reclaim just start the same command again.
for id in "$@"; do
  d="$OUT/$id"
  if [ -f "$d/renders/.done" ]; then echo "SKIP $id (done)"; continue; fi
  rm -rf "$d"
  node "$R/scripts/make_native_4k.mjs" "$V/$id" "$d" > /dev/null || { echo "FAILED $id: make_native_4k"; continue; }
  rm -rf "$d/renders" "$d/snapshots"; mkdir -p "$d/renders"
  # 3D: keep the WebGL buffer and the DOM pins in the 1080p layout space (the zoom stage scales them up 2x);
  # a true 3840x2160 buffer costs ~12 s a frame and puts pins at 4K coordinates inside the 1080p stage
  [ -f "$d/kav3d.js" ] && sed -i 's/const W = +root.dataset.width, H = +root.dataset.height/const W = 1920, H = 1080/' "$d/kav3d.js"
  w=4; grep -q "vendor/three/" "$d/index.html" && w=2
  s=$(date +%s)
  (cd "$d" && npx hyperframes render --workers $w --output "renders/$id.mp4" > renders/render.log 2>&1)
  f="$d/renders/$id.mp4"
  if [ -f "$f" ]; then
    touch "$d/renders/.done"
    echo "DONE $id $(ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 "$f" | tr '\n' ' ') $(( $(date +%s) - s ))s"
  else
    echo "FAILED $id: $(tail -3 "$d/renders/render.log" | tr '\n' ' ')"
  fi
done
echo "QUEUE FINISHED"
