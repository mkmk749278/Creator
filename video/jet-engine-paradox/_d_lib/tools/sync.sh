#!/usr/bin/env bash
# Copy the Session D shared files into every D scene folder (scenes stay self-contained): tools/sync.sh [scene ...]
cd "$(dirname "$0")/../.."
for d in ${@:-D*_*/}; do d=${d%/}; [ -d "$d" ] || continue
  cp _shared/jep.css _d_lib/jepd.css _d_lib/jepd.js _d_lib/globe.js _d_lib/kit.js "$d/" 2>/dev/null; done
