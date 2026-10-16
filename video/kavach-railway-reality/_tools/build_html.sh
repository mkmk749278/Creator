#!/usr/bin/env bash
# Like build.sh, for scenes whose index.html is hand-written (no scene.py): copy shared files + library, vendor,
# hyperframes check, snapshots at the given times, one contact sheet.
#   video/kavach-railway-reality/_tools/build_html.sh <scene_id> <lib_dir|-> "t1,t2,..."
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../.." && pwd); V=$ROOT/video/kavach-railway-reality; id=$1; lib=$2; at=$3
[ "$lib" = "-" ] && lib=""
"$V/_tools/setup_scene.sh" "$id" $lib >/dev/null
cd "$V/$id"
npx hyperframes check 2>&1 | grep -E "✗|Check (passed|failed)" | head -12 || true
rm -rf snapshots && npx hyperframes snapshot --at "$at" --no-end >/dev/null 2>&1 || echo "snapshot failed"
rm -f snapshots/contact-sheet.jpg; python3 "$ROOT/scripts/contact_sheet.py" snapshots --out snapshots/sheet >/dev/null && echo "sheet: $V/$id/snapshots/sheet/sheet-01.jpg"
