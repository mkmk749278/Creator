#!/usr/bin/env bash
# Copy Session B's shared lib.js and the film's jep.css into every B scene folder, then vendor three/pp/HDRI.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; top="$(dirname "$here")"
for d in "$top"/B[0-9]_*/; do cp "$here/lib.js" "$d/lib.js"; cp "$top/_shared/jep.css" "$d/jep.css"; done
cd "$top/../.." && node scripts/vendor-assets.mjs >/dev/null
