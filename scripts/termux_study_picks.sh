#!/data/data/com.termux/files/usr/bin/bash
# Competitor study kit, run on the owner's phone in Termux (mobile IP; PLAYBOOK §4a item 4, §8.5 option 2).
# For each of the 18 picks: Telugu/English captions, full audio (opus ~50 kb/s) and the first 3 minutes at 360p.
# Zips everything (about 150-250 MB) and uploads it to Gofile; paste the printed link to Claude.
# Study only: none of this footage or audio ever goes into our videos.
# Usage: bash termux_study_picks.sh
set -u
OUT="$HOME/study_picks"
mkdir -p "$OUT" && cd "$OUT"

pkg install -y python ffmpeg nodejs zip curl >/dev/null
pip install -q "yt-dlp==2026.8.19"

IDS="tKOC-Jlrc90 ikEyiQACJvM cTI-ojHmlEU Lkk3yhbNBkE P_O5GAmBTOM ge-W1iXWfQs kw48eN8X7ac P-hQglhBIEo Jim1lPVScDI
w2W-vMSjbe0 sPI12Rxr6Sk XjbSmMdl_d4 1TPkHPc0Mc8 L5Wvt_-4VWY FemVwIP9Vqk cDsM3zCs-no MNffEaWs9kE ZAgOCewk-IM"
Y="yt-dlp --js-runtimes node --sleep-requests 1 --no-progress -q"

for id in $IDS; do
  u="https://www.youtube.com/watch?v=$id"
  echo "== $id"
  $Y --skip-download --write-subs --write-auto-subs --sub-langs "te,te-orig,en,en-orig" --sub-format vtt \
     --write-info-json -o "$id.%(ext)s" "$u" || echo "   captions failed"
  $Y -f "249/250/ba" -o "$id.audio.%(ext)s" "$u" || echo "   audio failed"
  $Y -f "bv*[height<=360]+ba/b[height<=360]/b" --download-sections "*0-180" --merge-output-format mp4 \
     -o "$id.open180.%(ext)s" "$u" || echo "   video failed"
  sleep 5
done

ls -la
zip -q -r "$HOME/study_picks.zip" .
echo "Uploading $(du -h "$HOME/study_picks.zip" | cut -f1) ..."
for url in https://upload.gofile.io/uploadfile https://store1.gofile.io/uploadFile https://store-eu-par-1.gofile.io/uploadFile; do
  resp=$(curl -sS --max-time 1800 -F "file=@$HOME/study_picks.zip" "$url") && echo "$resp" | grep -q '"status":"ok"' && break
done
echo "$resp" | python -c 'import json,sys; d=json.load(sys.stdin); print("\nSEND THIS LINK TO CLAUDE:", d["data"]["downloadPage"])'
