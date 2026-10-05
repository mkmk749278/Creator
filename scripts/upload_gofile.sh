#!/usr/bin/env bash
# Upload one file to Gofile as a guest and print the download page URL.
# Usage: scripts/upload_gofile.sh FILE
set -euo pipefail
f="$1"
for attempt in 1 2 3; do
  resp=$(curl -sS --fail --max-time 1800 -F "file=@$f" https://upload.gofile.io/uploadfile) && break
  sleep $((attempt * 5))
done
echo "$resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["status"]=="ok", d; print(d["data"]["downloadPage"])'
