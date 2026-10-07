#!/usr/bin/env bash
# Final picture + sound: concat rendered parts, then lay the master audio under them:
# voice (with live pauses) on top, music bed ducked under the voice by a sidechain
# compressor (bed ~18-23 dB below narration, swelling back up in the pauses).
# Loudness: two-pass LINEAR normalisation to YouTube's -14 LUFS (one static gain
# + peak limiter), so the pauses keep their contrast instead of being pumped up.
# Usage: [LIVE=live.wav] scripts/final_mix.sh OUT.mp4 VOICE.wav BED.wav part1.mp4 part2.mp4 ...
# LIVE: optional real-world audio (e.g. the conch in a voice pause), mixed on top at full presence.
set -euo pipefail
out="$1"; voice="$2"; bed="$3"; shift 3
tmp=$(mktemp -d)
for f in "$@"; do echo "file '$(realpath "$f")'" >> "$tmp/list.txt"; done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$tmp/list.txt" -an -c copy "$tmp/video.mp4"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$tmp/video.mp4")
fo=$(echo "$dur - 1.5" | bc)

# 1) mix voice + ducked bed
# The bed ducks under the voice AND under any live (original) audio.
live_in=(); live_fc="[vsc]anull[sc];"; n=2
if [ -n "${LIVE:-}" ] && [ -f "$LIVE" ]; then
  live_in=(-i "$LIVE"); live_fc="[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=-14dB,asplit=2[lv][lsc];[vsc][lsc]amix=inputs=2:normalize=0[sc];"; n=3
fi
ffmpeg -y -loglevel error -i "$voice" -i "$bed" "${live_in[@]}" -filter_complex "
  [0:a]aresample=48000,highpass=f=70,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=150,aformat=channel_layouts=stereo,asplit=2[v][vsc];
  $live_fc
  [1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-15dB[b];
  [b][sc]sidechaincompress=threshold=0.015:ratio=10:attack=30:release=600:makeup=1[bd];
  [v][bd]$([ $n -eq 3 ] && echo '[lv]')amix=inputs=$n:duration=first:normalize=0[a]" -map "[a]" -c:a pcm_f32le "$tmp/mix.wav"

# 2) measure, then one linear gain to -14 LUFS; limiter catches peaks (-1.5 dBFS)
I=$(ffmpeg -hide_banner -i "$tmp/mix.wav" -af ebur128 -f null - 2>&1 | grep -A2 "Integrated loudness" | grep "I:" | awk '{print $2}')
gain=$(echo "-14 - ($I)" | bc -l)
echo "mix integrated loudness $I LUFS -> gain $gain dB"

ffmpeg -y -loglevel error -stats -i "$tmp/video.mp4" -i "$tmp/mix.wav" -filter_complex "
  [1:a]volume=${gain}dB,alimiter=limit=0.84:attack=5:release=50:level=false,
  afade=t=in:st=0:d=0.4,afade=t=out:st=$fo:d=1.5,aresample=48000[a];
  [0:v]fade=t=in:st=0:d=0.6,fade=t=out:st=$fo:d=1.5,format=yuv420p[vo]" \
  -map "[vo]" -map "[a]" -c:v libx264 -profile:v high -preset slow -crf 18 -r 30 -g 60 \
  -c:a aac -b:a 192k -ac 2 -shortest -movflags +faststart "$out"
rm -rf "$tmp"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height -of compact "$out"
