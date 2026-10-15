#!/usr/bin/env bash
# Pull the parallel sessions' scene clips (Drive Creator/English/insurance-ombudsman/scenes/<A|B|C>/) into assets/scenes/
# (flat, names <scene>_<Oid>.mp4) for build/assemble.py. Uses the same rclone + GDRIVE_RCLONE_TOKEN setup as
# scripts/upload_gdrive.sh; prints which expected clips are still missing.
set -euo pipefail
cd "$(dirname "$0")/.."
RC=$(ls ../../.cache/rclone/rclone-*/rclone | head -1)
TOKEN=$(python3 - <<'PY'
import json, os, re
t = os.environ["GDRIVE_RCLONE_TOKEN"].strip()
try:
    json.loads(t); print(t)
except ValueError:
    rt = re.search(r'refresh_token"?\s*:\s*"?([^",}\s]+)', t)
    print(json.dumps({"access_token": "", "token_type": "Bearer", "refresh_token": rt.group(1), "expiry": "2000-01-01T00:00:00Z"}))
PY
)
export RCLONE_CONFIG_GD_TYPE=drive RCLONE_CONFIG_GD_SCOPE=drive RCLONE_CONFIG_GD_TOKEN="$TOKEN" RCLONE_CONFIG=/dev/null
export RCLONE_CONFIG_GD_ROOT_FOLDER_ID=${GDRIVE_CREATOR_FOLDER_ID:-1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M}
mkdir -p assets/scenes
for s in A B C; do
  "$RC" copy "gd:English/insurance-ombudsman/scenes/$s" assets/scenes --include "*.mp4" --include "*.jpg" --include "*.png" 2>/dev/null || true
done
python3 - <<'PY'
import re
from pathlib import Path
src = Path("build/assemble.py").read_text()
want = sorted(set(re.findall(r'SC\("([A-C]\d_\w+)", "(O\d+)"', src)))
have = {p.name for p in Path("assets/scenes").glob("*.mp4")}
miss = [f"{a}_{b}.mp4" for a, b in want if f"{a}_{b}.mp4" not in have]
print(f"{len(want) - len(miss)}/{len(want)} scene clips present; missing: {' '.join(miss) or 'none'}")
PY
