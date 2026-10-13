#!/usr/bin/env bash
# Upload files to the owner's Google Drive "Creator" folder and print a shareable view link for each.
# Replaces scripts/upload_gofile.sh for delivery (owner, 2026-10-13: "use Google Drive from now instead of Gofile").
#
# Usage: scripts/upload_gdrive.sh [--sub <subfolder>] FILE [FILE ...]
#   --sub jet-engine-paradox   puts the files in Creator/<subfolder>/ (created if missing)
#
# Needs the environment variable GDRIVE_RCLONE_TOKEN: the JSON line that `rclone authorize "drive"` prints
# (one-time setup on the phone in Termux, PLAYBOOK §1). Optional GDRIVE_CREATOR_FOLDER_ID (default: the Creator
# folder found on 2026-10-13). rclone itself is a pinned binary fetched into .cache/ on first use.
# Small text files (description, SRT, review.md) can also go up through the Google Drive connector without a token;
# the connector cannot carry video-sized files.
set -euo pipefail
RCLONE_VER=v1.71.1
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CACHE="$ROOT/.cache/rclone"
FOLDER_ID=${GDRIVE_CREATOR_FOLDER_ID:-1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M}
SUB=""
if [[ ${1:-} == --sub ]]; then SUB=$2; shift 2; fi
[[ $# -ge 1 ]] || { sed -n 2,12p "$0"; exit 2; }
[[ -n ${GDRIVE_RCLONE_TOKEN:-} ]] || { echo "GDRIVE_RCLONE_TOKEN is not set (see PLAYBOOK §1, Google Drive setup)" >&2; exit 3; }

RCLONE="$CACHE/rclone-$RCLONE_VER-linux-amd64/rclone"
if [[ ! -x $RCLONE ]]; then
  mkdir -p "$CACHE"
  curl -sSL -m 300 -o "$CACHE/rclone.zip" "https://downloads.rclone.org/$RCLONE_VER/rclone-$RCLONE_VER-linux-amd64.zip"
  (cd "$CACHE" && unzip -q -o rclone.zip && rm rclone.zip)
fi

export RCLONE_CONFIG_GD_TYPE=drive RCLONE_CONFIG_GD_SCOPE=drive RCLONE_CONFIG_GD_TOKEN="$GDRIVE_RCLONE_TOKEN"
export RCLONE_CONFIG_GD_ROOT_FOLDER_ID="$FOLDER_ID" RCLONE_CONFIG=/dev/null
DEST="gd:${SUB}"
for f in "$@"; do
  name=$(basename "$f")
  "$RCLONE" copyto --drive-chunk-size 64M --retries 4 --low-level-retries 10 --stats-one-line --stats 30s \
    "$f" "$DEST/$name" >&2
  # anyone with the link can view (the owner opens it on the phone; nothing is listed publicly)
  link=$("$RCLONE" link "$DEST/$name")
  echo "$name  $link"
done
