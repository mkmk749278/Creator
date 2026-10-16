#!/usr/bin/env bash
# Wait until a queue log says QUEUE FINISHED, then run render_queue.sh with the given scenes into a new log.
#   after.sh <wait_log> <new_log> scene...
w=$1; n=$2; shift 2
until grep -q "QUEUE FINISHED" "$w" 2>/dev/null; do sleep 5; done
"$(dirname "$0")/render_queue.sh" "$@" > "$n" 2>&1
