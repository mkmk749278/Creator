#!/data/data/com.termux/files/usr/bin/bash
# Search YouTube on the owner's phone and put the results (title, channel, length, date, URL and a thumbnail per
# video) in Google Drive, Creator/<Channel>/<slug>/search/, so a cloud session can vet them on a contact sheet and
# write the exact termux_fetch_to_drive.sh line for the clips worth using (PLAYBOOK §8.5). Nothing is downloaded but
# thumbnails. Why on the phone: YouTube answers 403 to the cloud container, and web search barely indexes YouTube.
#
# One command in Termux (the session writes it out for you):
#   curl -sL https://raw.githubusercontent.com/mkmk749278/Creator/main/scripts/termux_search_to_drive.sh | bash -s -- \
#     English/pharma-apis "first search words" "second search words"
#
# Arguments: <Channel>/<slug>, then one quoted search per argument (12 results each). Same first-run setup as
# termux_fetch_to_drive.sh (python, ffmpeg, nodejs, rclone, pinned yt-dlp, the rclone remote "creator").
set -uo pipefail
DEST="${1:?usage: termux_search_to_drive.sh <Channel>/<slug> \"search\" [\"search\" ...]}"; shift
[[ $# -ge 1 ]] || { echo "give at least one search" >&2; exit 2; }
CREATOR_FOLDER_ID=1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M   # the owner's Drive "Creator" folder (PLAYBOOK §1)
OUT="$HOME/creator_search/$(basename "$DEST")"
rm -rf "$OUT" && mkdir -p "$OUT" && cd "$OUT" || exit 1

command -v rclone >/dev/null && command -v ffmpeg >/dev/null && command -v node >/dev/null && command -v python3 >/dev/null \
  || pkg install -y python ffmpeg nodejs rclone
python3 -m pip show yt-dlp 2>/dev/null | grep -q "^Version: 2026.8.19" || python3 -m pip install -q "yt-dlp==2026.8.19"
if ! rclone listremotes | grep -q "^creator:$"; then
  echo "One-time Google Drive sign-in: a browser opens; choose the account that owns the Creator folder and tap Allow."
  rclone config create creator drive scope=drive root_folder_id="$CREATOR_FOLDER_ID" || { echo "rclone sign-in failed" >&2; exit 3; }
fi

echo "query,n,id,title,channel,duration_s,upload_date,url" > results.csv
q=0
for query in "$@"; do
  q=$((q + 1)); echo "== $q $query"
  yt-dlp --js-runtimes node --skip-download --no-warnings -q --ignore-errors \
    --write-thumbnail --convert-thumbnails jpg -o "thumbs/q${q}_%(playlist_index)02d_%(id)s.%(ext)s" \
    --print "$q,%(playlist_index)s,%(id)s,\"%(title)s\",\"%(channel)s\",%(duration)s,%(upload_date)s,%(webpage_url)s" \
    "ytsearch12:$query" >> results.csv || echo "   search $q had errors (kept what came back)" >&2
done
echo "$(($(wc -l < results.csv) - 1)) results. Uploading to Drive: Creator/$DEST/search/"
rclone copy --retries 4 . "creator:$DEST/search" && echo "Done. Tell Claude: search results are in Drive, Creator/$DEST/search."
