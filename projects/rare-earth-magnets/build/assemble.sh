#!/usr/bin/env bash
# Join the rendered parts (video/rem/p1..p5 -> assets/out/pN.mp4) and lay the master audio under them (CLAUDE.md audio):
# the VO leads (peaks about -2 dB), the bed is ducked under the voice by a sidechain compressor and swells back in the
# pauses, SFX sit about 9 dB down; then two-pass LINEAR loudnorm to -14 LUFS so pauses keep their contrast.
# usage: bash projects/rare-earth-magnets/build/assemble.sh OUT.mp4
set -euo pipefail
P=$(cd "$(dirname "$0")/.." && pwd); A=$P/assets; out=${1:-$A/out/rare_earth_magnets_preview.mp4}
tmp=$(mktemp -d); : > "$tmp/list.txt"
for i in 1 2 3 4 5; do echo "file '$A/out/p$i.mp4'" >> "$tmp/list.txt"; done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$tmp/list.txt" -an -c copy "$tmp/video.mp4"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$tmp/video.mp4")
mix="[0:a]aresample=48000,aformat=channel_layouts=mono,volume=1.0,apad=whole_dur=$dur,asplit=2[v][vsc];
[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-11dB,atrim=0:$dur[bedraw];
[bedraw][vsc]sidechaincompress=threshold=0.015:ratio=7:attack=40:release=650:makeup=1[bed];
[2:a]aresample=48000,aformat=channel_layouts=mono,volume=-9dB,atrim=0:$dur[fx];
[v][bed][fx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[m]"
ffmpeg -y -loglevel error -i "$A/vo/vo_full.wav" -i "$A/audio/bed.wav" -i "$A/audio/sfx.wav" -filter_complex "$mix" -map "[m]" -ar 48000 "$tmp/mix.wav"
# two-pass linear loudness normalisation to -14 LUFS / -1.5 dBTP
read -r I TP LRA TH < <(ffmpeg -hide_banner -i "$tmp/mix.wav" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 |
  python3 -c 'import sys,json,re; d=json.loads(re.search(r"\{[^{}]*\}", sys.stdin.read(), re.S).group(0)); print(d["input_i"], d["input_tp"], d["input_lra"], d["input_thresh"])')
ffmpeg -y -loglevel error -i "$tmp/mix.wav" -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$TH:linear=true" -ar 48000 "$tmp/master.wav"
mkdir -p "$(dirname "$out")"
ffmpeg -y -loglevel error -i "$tmp/video.mp4" -i "$tmp/master.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ac 2 -movflags +faststart -shortest "$out"
ffmpeg -hide_banner -i "$out" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
rm -rf "$tmp"; echo "wrote $out"
