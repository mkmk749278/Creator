#!/data/data/com.termux/files/usr/bin/bash
# Download Pexels stock clips on the owner's phone and put them in Google Drive, in
# Creator/<Channel>/<slug>/footage/pexels/, where a cloud session pulls them (owner, 2026-11-03).
# Why on the phone: the Pexels website refuses the cloud container (docs/archive/PLAYBOOK_2026-11-05.md §8.3) and Pexels paused new API keys.
# Licence: Pexels licence (free to use, no attribution needed; we credit anyway in the description).
#
# One command in Termux (the session that needs the clips writes it out for you):
#   curl -sL https://raw.githubusercontent.com/mkmk749278/Creator/main/scripts/termux_pexels_to_drive.sh | bash -s -- \
#     English/india-own-ai 29081675:01_monsoon_pune 8829016:02_hands_typing ...
#
# Arguments: <Channel>/<slug>, then ID:name pairs (the number at the end of the Pexels video URL). Each file is saved
# as pexels_<name>_<ID>.mp4, the best rendition up to 3840 px wide. pexels_fetched.csv records the clip page's real
# title, so the session can check that every ID is the clip it was meant to be.
# First run only: installs curl, python and rclone, then creates the rclone remote "creator" (Google Drive): a browser
# opens, sign in with the account that owns the Creator folder, tap Allow (same remote as termux_fetch_to_drive.sh).
set -uo pipefail
DEST="${1:?usage: termux_pexels_to_drive.sh <Channel>/<slug> ID:name [ID:name ...]}"; shift
[[ $# -ge 1 ]] || { echo "give at least one ID:name" >&2; exit 2; }
CREATOR_FOLDER_ID=1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M   # the owner's Drive "Creator" folder (docs/archive/PLAYBOOK_2026-11-05.md §1)
SLUG=$(basename "$DEST")
OUT="$HOME/creator_fetch/$SLUG/pexels"
mkdir -p "$OUT" && cd "$OUT" || exit 1
command -v rclone >/dev/null && command -v python3 >/dev/null && command -v curl >/dev/null || pkg install -y curl python rclone
if ! rclone listremotes | grep -q "^creator:$"; then
  echo "One-time Google Drive sign-in: a browser opens; choose the account that owns the Creator folder and tap Allow."
  rclone config create creator drive scope=drive root_folder_id="$CREATOR_FOLDER_ID" || { echo "rclone sign-in failed" >&2; exit 3; }
fi
UA="Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36"
echo "file,id,name,page_title,width,source_url" > pexels_fetched.csv
n=0; ok=0
for entry in "$@"; do
  n=$((n + 1)); id="${entry%%:*}"; name="${entry#*:}"; f="pexels_${name}_${id}.mp4"
  echo "== $n $id $name"
  page=$(curl -sL -A "$UA" "https://www.pexels.com/video/$id/")
  # the page lists every rendition as videos.pexels.com/video-files/<id>/<id>-<quality>_<w>_<h>_<fps>fps.mp4
  pick=$(printf '%s' "$page" | python3 -c '
import re, sys
t = sys.stdin.read(); vid = sys.argv[1]
title = re.search(r"<title>(.*?)</title>", t, re.S)
title = (title.group(1).strip() if title else "").replace(",", " ").replace("\"", "")
urls = set(re.findall(r"https://videos\.pexels\.com/video-files/%s/[^\"\x27 ]+?\.mp4" % vid, t))
best = None
for u in urls:
    m = re.search(r"_(\d{3,4})_(\d{3,4})_", u)
    w = int(m.group(1)) if m else 0
    if w <= 3840 and (best is None or w > best[0]):
        best = (w, u)
print(title); print(best[0] if best else 0); print(best[1] if best else "")
' "$id")
  title=$(sed -n 1p <<<"$pick"); width=$(sed -n 2p <<<"$pick"); url=$(sed -n 3p <<<"$pick")
  [[ -z "$url" ]] && url="https://www.pexels.com/download/video/$id/"   # fallback: Pexels' own download link
  if curl -sSL -A "$UA" -o "$f" "$url" && [[ $(stat -c %s "$f" 2>/dev/null || echo 0) -gt 200000 ]] \
     && head -c 64 "$f" | grep -qa "ftyp"; then
    echo "$f,$id,$name,\"$title\",$width,$url" >> pexels_fetched.csv; ok=$((ok + 1))
    echo "   ok  $(du -h "$f" | cut -f1)  $title"
  else
    rm -f "$f"; echo "-,$id,$name,\"$title\",FAILED,$url" >> pexels_fetched.csv
    echo "   failed (wrong ID, or the page blocked the phone; try Wi-Fi)" >&2
  fi
  sleep 2
done
echo "Uploading $ok of $n clips to Drive: Creator/$DEST/footage/pexels/"
rclone copy "$OUT" "creator:$DEST/footage/pexels" --include "*.mp4" --include "pexels_fetched.csv" --stats-one-line --stats 20s
echo "Done: $ok of $n downloaded. Tell the session: pexels clips are in Drive."
