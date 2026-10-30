#!/data/data/com.termux/files/usr/bin/bash
# Download YouTube (or Dailymotion, archive.org…) clips on the owner's phone and put them straight into Google Drive,
# in Creator/<Channel>/<slug>/footage/, where a cloud session pulls them with scripts/gdrive_pull.sh (PLAYBOOK §8.5).
# Why on the phone: YouTube answers 403 to the cloud container and the VPS runner is often offline; the phone's mobile
# IP works. Only footage we may use: short, credited excerpts of official or news footage, owner-cleared (PLAYBOOK §8.6).
#
# One command in Termux (copy the whole line; the session that needs the clips writes it out for you):
#   curl -sL https://raw.githubusercontent.com/mkmk749278/Creator/main/scripts/termux_fetch_to_drive.sh | bash -s -- \
#     English/rare-earth-magnets "https://www.youtube.com/watch?v=ID" "https://www.youtube.com/watch?v=ID2@01:10-01:40"
#
# Arguments: <Channel>/<slug>, then URLs; URL@MM:SS-MM:SS downloads only that range. Max 1080p MP4.
# First run only: installs python, ffmpeg, nodejs, rclone and a pinned yt-dlp, then creates the rclone remote
# "creator" (Google Drive): a browser opens, sign in with the account that owns the Creator folder, tap Allow.
set -uo pipefail
DEST="${1:?usage: termux_fetch_to_drive.sh <Channel>/<slug> URL [URL@START-END ...]}"; shift
[[ $# -ge 1 ]] || { echo "give at least one URL" >&2; exit 2; }
CREATOR_FOLDER_ID=1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M   # the owner's Drive "Creator" folder (PLAYBOOK §1)
SLUG=$(basename "$DEST")
OUT="$HOME/creator_fetch/$SLUG"
mkdir -p "$OUT" && cd "$OUT" || exit 1

command -v rclone >/dev/null && command -v ffmpeg >/dev/null && command -v node >/dev/null && command -v python3 >/dev/null \
  || pkg install -y python ffmpeg nodejs rclone
python3 -m pip show yt-dlp 2>/dev/null | grep -q "^Version: 2026.8.19" || python3 -m pip install -q "yt-dlp==2026.8.19"

if ! rclone listremotes | grep -q "^creator:$"; then
  echo "One-time Google Drive sign-in: a browser opens; choose the account that owns the Creator folder and tap Allow."
  rclone config create creator drive scope=drive root_folder_id="$CREATOR_FOLDER_ID" || { echo "rclone sign-in failed" >&2; exit 3; }
fi

# "Sign in to confirm you're not a bot" (seen on the mobile IP, 2026-10-30): sign in with a THROWAWAY Google account's
# cookies (never the channel or main account, PLAYBOOK §8.5). Export cookies.txt (Netscape format) from youtube.com in a
# private window of Firefox for Android (add-on "cookies.txt"), save it to Downloads as youtube_cookies.txt, run
# termux-setup-storage once; this script then passes it to yt-dlp. Switching to Wi-Fi often clears the check too.
COOKIES="${YT_COOKIES_FILE:-$HOME/storage/downloads/youtube_cookies.txt}"
[[ -f "$COOKIES" ]] && echo "Using cookies: $COOKIES" || COOKIES=""
echo "file,url,section,title,uploader,duration_s" > fetched.csv
n=0; ok=0
for entry in "$@"; do
  n=$((n + 1)); url="${entry%@*}"; sec=""
  [[ "$entry" == *@*-* ]] && sec="${entry##*@}"
  args=(--js-runtimes node --no-playlist --restrict-filenames --no-progress -q --no-warnings
        --sleep-requests 1.5 --sleep-interval 8 --max-sleep-interval 20
        -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]/b" --merge-output-format mp4
        --print-to-file "%(title)s|%(uploader)s|%(duration)s" meta.txt
        -o "$(printf %02d $n)_%(id)s.%(ext)s")
  [[ -n "$sec" ]] && args+=(--download-sections "*$sec" --force-keyframes-at-cuts)
  [[ -n "$COOKIES" ]] && args+=(--cookies "$COOKIES")
  echo "== $n $entry"
  rm -f meta.txt
  if yt-dlp "${args[@]}" "$url"; then
    f=$(ls -t "$(printf %02d $n)"_*.mp4 2>/dev/null | head -1)
    IFS='|' read -r title upl dur < meta.txt
    echo "$f,$url,$sec,\"${title//\"/\'}\",\"$upl\",$dur" >> fetched.csv
    ok=$((ok + 1))
  else
    echo "$n,$url,$sec,FAILED,," >> fetched.csv
    echo "   failed (try again later or on Wi-Fi)" >&2
  fi
done
echo "$ok of $n downloaded. Uploading to Drive: Creator/$DEST/footage/"
rclone copy --drive-chunk-size 64M --retries 4 --stats-one-line --stats 20s \
  --include "*.mp4" --include "fetched.csv" . "creator:$DEST/footage" && {
  echo "Done. Tell Claude: footage is in Drive, Creator/$DEST/footage ($ok clips)."
  rclone link "creator:$DEST/footage" 2>/dev/null || true
}
