#!/usr/bin/env bash
# Download one YouTube video for frame-by-frame study, then extract frames + contact sheets.
# Usage: scripts/fetch_video.sh URL OUT_DIR [FRAME_EVERY_SECONDS]
# Optional: YT_COOKIES_FILE=/path/cookies.txt (Netscape format, from a throwaway Google account)
# Writes OUT_DIR/fetch.log.md. Exits non-zero if the download fails (fail loud per stage).
# Downloads are for analysis only: never reuse other creators' footage in our videos (CLAUDE.md).
set -uo pipefail
url="${1:?url}"; out="${2:?out dir}"; every="${3:-2}"
mkdir -p "$out/frames"
log="$out/fetch.log.md"
ytlog="$out/yt-dlp.log"

args=(--js-runtimes node --no-playlist --restrict-filenames
      -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]/b"
      --merge-output-format mp4 --write-info-json
      -o "$out/video.%(ext)s")
auth="none"
if [[ -n "${YT_COOKIES_FILE:-}" && -s "${YT_COOKIES_FILE}" ]]; then
  # yt-dlp rewrites the cookie jar; work on a copy so the source file stays untouched.
  cp "$YT_COOKIES_FILE" "$out/.cookies.txt"
  args+=(--cookies "$out/.cookies.txt")
  auth="cookies"
fi

{
  echo "# Video fetch"
  echo
  echo "- URL: $url"
  echo "- Runner: \`${RUNNER_NAME:-local}\` · yt-dlp \`$(yt-dlp --version)\` · auth: $auth"
} > "$log"

yt-dlp "${args[@]}" "$url" >"$ytlog" 2>&1
status=$?
rm -f "$out/.cookies.txt"

if [[ $status -ne 0 || ! -s "$out/video.mp4" ]]; then
  if grep -qiE "not a bot|sign in to confirm|HTTP Error 429" "$ytlog"; then
    reason="blocked by YouTube (bot check / 429). Add the YT_COOKIES secret or use the VPS runner."
  else
    reason="$(grep -iE 'error' "$ytlog" | tail -1 | cut -c1-200)"
  fi
  echo "- Result: ⛔ download failed: $reason" >> "$log"
  cat "$log"
  exit 1
fi

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out/video.mp4" | cut -d. -f1)
title=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['title'])" "$out/video.info.json" 2>/dev/null || echo "?")
# One frame every N seconds, timestamp burned in so shots can be referenced.
ffmpeg -loglevel error -y -i "$out/video.mp4" \
  -vf "fps=1/${every},scale=480:-2,drawtext=text='%{pts\:hms}':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6" \
  "$out/frames/f%04d.jpg"
nframes=$(ls "$out/frames" | wc -l)
# Contact sheets: 5x6 = 30 frames each, phone-viewable.
ffmpeg -loglevel error -y -framerate 1 -i "$out/frames/f%04d.jpg" -vf "tile=5x6:padding=6:color=black" \
  "$out/sheet-%02d.jpg"

{
  echo "- Title: $title"
  echo "- Result: ✅ $(du -h "$out/video.mp4" | cut -f1) · ${dur}s · $nframes frames (every ${every}s) · $(ls "$out"/sheet-*.jpg | wc -l) contact sheets"
} >> "$log"
cat "$log"
