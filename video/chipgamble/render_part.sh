#!/usr/bin/env bash
# Render one part to renders/<part>.mp4 (waits for any running render first).
set -euo pipefail
cd "$(dirname "$0")"
while pgrep -f "hyperframes render" >/dev/null; do sleep 15; done
cd "$1" && npx hyperframes render --workers 4 --quality high --output "../renders/$1.mp4" > "../renders/$1.log" 2>&1
echo "rendered $1"
