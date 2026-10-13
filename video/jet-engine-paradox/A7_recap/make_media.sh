#!/usr/bin/env bash
# Cut the three recap panels from this session's own renders (run after A5, A6, A8 are rendered).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p media
R=..; enc=(-an -c:v libx264 -preset medium -crf 16 -maxrate 30M -bufsize 60M -pix_fmt yuv420p -r 30)
ffmpeg -y -loglevel error -ss 8.9 -t 6.6 -i "$R/A5_thermal_reveal/renders/A5_thermal_reveal.mp4" "${enc[@]}" media/p1.mp4   # gas above the melt line
ffmpeg -y -loglevel error -ss 8.2 -t 4.15 -i "$R/A6_spin_bus/renders/A6_spin_bus.mp4" "${enc[@]}" media/p2.mp4             # bus hanging from one blade
ffmpeg -y -loglevel error -ss 4.3 -t 2.0 -i "$R/A8_verdict_blade/renders/A8_verdict_blade.mp4" "${enc[@]}" media/p3.mp4     # hours counter to 4,000+
ls -la media
