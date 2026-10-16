#!/usr/bin/env bash
# Prepare a scene folder: shared look + the world's library + cues.js from the real VO timing, then vendor assets.
#   video/kavach-railway-reality/_tools/setup_scene.sh <scene_id> [lib_dir_name]   (lib e.g. _C_lib)
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../.." && pwd); V=$ROOT/video/kavach-railway-reality; id=$1; lib=${2:-}
mkdir -p "$V/$id"
cp "$V/_shared/kav.css" "$V/_shared/kav.js" "$V/_shared/indsig.js" "$V/_shared/slate.jpg" "$V/$id/"
[ -n "$lib" ] && cp -r "$V/$lib/." "$V/$id/"
python3 "$ROOT/projects/kavach-railway-reality/tools/scene_params.py" "$id" >/dev/null
[ -f "$V/$id/index.html" ] && (cd "$ROOT" && node scripts/vendor-assets.mjs >/dev/null) || true
echo "ready: $V/$id"
