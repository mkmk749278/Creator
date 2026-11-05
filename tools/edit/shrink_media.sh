#!/bin/bash
# Reusable tool kept from an earlier film (repo slimmed 2026-11-05): adapt the paths at the top to the new film.
# Review cuts render at 720p, so a part's clips need no more than 720 lines. Shrinking them cuts a part's media from
# ~500-700 MB to ~1/3: the "Render film" check loads every clip at once, and parts p3/p4 (514/733 MB) lost their
# media requests with net::ERR_CONNECTION_RESET (r2, 2026-11-03) while the lighter parts passed.
# Same frame rate and timing (scale only), so data-media-start is unchanged. Never run before a 4K master.
# usage: bash projects/india-own-ai/build/shrink_media.sh 3 4
set -eu
cd "$(dirname "$0")/../../.."
for i in "$@"; do
  for f in video/aig/p$i/media/*.mp4; do
    h=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$f")
    [ "$h" -le 720 ] && continue
    ffmpeg -hide_banner -loglevel error -y -i "$f" -an -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 20 \
      -maxrate 8M -bufsize 16M -pix_fmt yuv420p "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f"
  done
  echo "p$i $(du -sh video/aig/p$i/media | cut -f1)"
done
