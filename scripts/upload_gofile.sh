#!/usr/bin/env bash
# Upload one file to Gofile as a guest and print the download page URL.
# Tries the global endpoint, then regional store servers (the global one is sometimes unreachable).
# Usage: scripts/upload_gofile.sh FILE
set -euo pipefail
f="$1"
for url in https://upload.gofile.io/uploadfile https://store-eu-par-1.gofile.io/uploadFile https://store1.gofile.io/uploadFile https://store-na-phx-1.gofile.io/uploadFile; do
  resp=$(curl -sS --max-time 1800 -F "file=@$f" "$url" 2>/dev/null) || continue
  echo "$resp" | grep -q '"status":"ok"' && break
done
echo "$resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["status"]=="ok", d; print(d["data"]["downloadPage"])'
