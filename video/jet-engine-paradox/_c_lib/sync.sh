#!/usr/bin/env bash
# Copy the Session C shared files into every C scene folder (run after editing _c_lib/ or _shared/jep.css).
set -euo pipefail
cd "$(dirname "$0")/.."
for d in C*_*/; do cp _shared/jep.css _c_lib/_bp.js _c_lib/_c.css "$d"; done
echo "synced into: $(ls -d C*_*/ | tr '\n' ' ')"
