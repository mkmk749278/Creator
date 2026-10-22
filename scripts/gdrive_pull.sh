#!/usr/bin/env bash
# Pull a folder from the owner's Google Drive "Creator" folder into the cloud session (the counterpart of
# scripts/termux_fetch_to_drive.sh, which puts phone-downloaded clips in Creator/<Channel>/<slug>/footage/).
#
# Usage: scripts/gdrive_pull.sh English/rare-earth-magnets/footage projects/rare-earth-magnets/assets/yt
# Needs GDRIVE_RCLONE_TOKEN, exactly like scripts/upload_gdrive.sh (PLAYBOOK §1); reuses its pinned rclone.
set -euo pipefail
SRC="${1:?Drive path under Creator/, e.g. English/<slug>/footage}"; DST="${2:?local folder}"
RCLONE_VER=v1.71.1
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CACHE="$ROOT/.cache/rclone"
FOLDER_ID=${GDRIVE_CREATOR_FOLDER_ID:-1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M}
[[ -n ${GDRIVE_RCLONE_TOKEN:-} ]] || { echo "GDRIVE_RCLONE_TOKEN is not set (see PLAYBOOK §1, Google Drive setup)" >&2; exit 3; }
RCLONE="$CACHE/rclone-$RCLONE_VER-linux-amd64/rclone"
if [[ ! -x $RCLONE ]]; then
  mkdir -p "$CACHE"
  curl -sSL -m 300 -o "$CACHE/rclone.zip" "https://downloads.rclone.org/$RCLONE_VER/rclone-$RCLONE_VER-linux-amd64.zip"
  (cd "$CACHE" && unzip -q -o rclone.zip && rm rclone.zip)
fi
# Same token repair as upload_gdrive.sh: the Claude app's environment field strips parts of the JSON.
TOKEN=$(python3 - <<'EOF'
import json, os, re
t = os.environ["GDRIVE_RCLONE_TOKEN"].strip()
try:
    json.loads(t); print(t)
except ValueError:
    rt = re.search(r'refresh_token"?\s*:\s*"?([^",}\s]+)', t)
    at = re.match(r'[{\s"]*(?:access_token"?\s*:\s*"?)?(ya29[^",}\s]*)', t)
    if not rt:
        raise SystemExit("GDRIVE_RCLONE_TOKEN has no refresh_token; run rclone authorize again")
    print(json.dumps({"access_token": at.group(1) if at else "", "token_type": "Bearer",
                      "refresh_token": rt.group(1), "expiry": "2000-01-01T00:00:00Z"}))
EOF
)
export RCLONE_CONFIG_GD_TYPE=drive RCLONE_CONFIG_GD_SCOPE=drive RCLONE_CONFIG_GD_TOKEN="$TOKEN"
export RCLONE_CONFIG_GD_ROOT_FOLDER_ID="$FOLDER_ID" RCLONE_CONFIG=/dev/null
mkdir -p "$DST"
"$RCLONE" copy --retries 4 --stats-one-line --stats 30s "gd:$SRC" "$DST"
ls -la "$DST"
