#!/usr/bin/env bash
# Copy Session A's shared 3D library and the film's shared CSS into every Session A scene folder.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
for d in "$here"/A*_*/; do
  cp "$here/_libA/jepA.js" "$d/jepA.js"
  cp "$here/_shared/jep.css" "$d/jep.css"
done
echo "synced into: $(ls -d "$here"/A*_*/ | xargs -n1 basename | tr '\n' ' ')"
