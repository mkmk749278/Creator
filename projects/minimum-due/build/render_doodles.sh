#!/usr/bin/env bash
# Render the doodle scenes that replace the whiteboard boards (1080p) into projects/minimum-due/assets/boards/<id>.mp4,
# and write each scene's sound-effect track (video/lib/doodle/make_sfx.py) to assets/boards/<id>.sfx.wav.
# Run detached: setsid nohup bash projects/minimum-due/build/render_doodles.sh > /tmp/doodles.log 2>&1 < /dev/null & disown
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT="$ROOT/projects/minimum-due/assets/boards"; mkdir -p "$OUT"
PY="$ROOT/.venv/bin/python"; [ -x "$PY" ] || PY=python3
for id in b01_how b02_numbers b05_newswipe b07_crif b08_maths b09_loop b10_postpone b11_steps12 b12_emi b13_recap b14_next; do
  d="$ROOT/video/minimumdue/$id"
  if [ -s "$OUT/$id.mp4" ] && [ "$OUT/$id.mp4" -nt "$d/params.js" ] && [ "$OUT/$id.mp4" -nt "$ROOT/video/lib/doodle/doodle.js" ]; then echo "skip $id"; continue; fi
  "$PY" "$ROOT/video/lib/doodle/make_sfx.py" "$d/params.js" "$OUT/$id.sfx.wav" >/dev/null
  if (cd "$d" && npx --prefix "$ROOT" hyperframes render . --workers 4 --output render.mp4 > render.log 2>&1); then
    cp "$d/render.mp4" "$OUT/$id.mp4" && echo "done $id"
  else echo "FAIL $id"; tail -3 "$d/render.log"; fi
done
echo ALL_DONE
