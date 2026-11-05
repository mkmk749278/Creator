#!/usr/bin/env bash
# Phase 0: can this machine pull YouTube subtitles with yt-dlp, or is it blocked?
# Usage: scripts/spike_ytdlp.sh OUT_DIR [VIDEO_ID ...]
# Writes OUT_DIR/ytdlp.md and exits 0 either way (the result is the report).
set -uo pipefail
out="${1:?out dir}"; shift
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=(jNQXAC9IVRw dQw4w9WgXcQ)
mkdir -p "$out/subs"
{
  echo "# yt-dlp transcript test"
  echo
  echo "Runner: \`${RUNNER_NAME:-local}\` · yt-dlp \`$(yt-dlp --version)\` · public IP \`$(curl -s --max-time 5 https://api.ipify.org || echo unknown)\`"
  echo
  echo "| video | result | detail |"
  echo "|---|---|---|"
} > "$out/ytdlp.md"
for id in "${ids[@]}"; do
  log="$out/subs/$id.log"
  yt-dlp --js-runtimes node --skip-download --write-subs --write-auto-subs --sub-langs "en.*,en" --sub-format vtt \
    -o "$out/subs/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=$id" >"$log" 2>&1
  if ls "$out/subs/$id".*.vtt >/dev/null 2>&1; then
    lines=$(cat "$out/subs/$id".*.vtt | wc -l)
    echo "| $id | ✅ subtitles | $lines vtt lines |" >> "$out/ytdlp.md"
  elif grep -qiE "not a bot|sign in to confirm|HTTP Error 429" "$log"; then
    echo "| $id | ⛔ blocked | $(grep -iE 'not a bot|sign in|429' "$log" | head -1 | cut -c1-120 | tr '|' '/') |" >> "$out/ytdlp.md"
  else
    echo "| $id | ⚠️ no subs | $(grep -iE 'error|warning' "$log" | head -1 | cut -c1-120 | tr '|' '/') |" >> "$out/ytdlp.md"
  fi
done
cat "$out/ytdlp.md"
