#!/bin/bash
# Cloud sessions start ready to render: Node deps (HyperFrames, GSAP, Three.js, postprocessing; postinstall
# vendors them into every video/ project), the Python venv, and the shared asset library cache.
# Each parallel session is a fresh VM, so this runs once per session (PLAYBOOK §3).
set -euo pipefail
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi
cd "$CLAUDE_PROJECT_DIR"

# npm install (not ci) so the cached container state is reused when nothing changed.
npm install --no-audit --no-fund --loglevel=error

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install --quiet --disable-pip-version-check -e ".[collect,media]"

# Large library files are not in git; small ones are. Fetch soft-fails so a flaky host never blocks a session.
.venv/bin/python scripts/library.py fetch || echo "library fetch incomplete; run: python3 scripts/library.py fetch" >&2

echo 'export PATH="$CLAUDE_PROJECT_DIR/.venv/bin:$PATH"' >> "$CLAUDE_ENV_FILE"
