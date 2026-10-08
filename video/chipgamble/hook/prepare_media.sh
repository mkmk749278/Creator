#!/usr/bin/env bash
# Rebuild the gitignored media for the hook composition: Commons video cuts,
# the freeze frame, and the synthesized SFX. Images and voice.mp3 are committed.
# Sources and licences: episodes/india-semiconductor-gamble/05-media-credits.md
set -euo pipefail
cd "$(dirname "$0")"
UA="CreatorEpisodeBot/0.1 (https://github.com/mkmk749278/Creator)"
TMP=$(mktemp -d)
# Commons 1080p transcodes (originals are rate-limited; derivatives are not).
# Resolve each file's 1080p transcode via the Commons API (originals are rate-limited).
fetch() {
  local url
  url=$(python3 -I - "$2" <<'PY'
import json, sys, urllib.parse, urllib.request
q = urllib.parse.urlencode(dict(action="query", titles=sys.argv[1], prop="videoinfo", viprop="derivatives", format="json"))
r = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": "CreatorEpisodeBot/0.1"})
page = next(iter(json.load(urllib.request.urlopen(r))["query"]["pages"].values()))
ders = [d for d in page["videoinfo"][0]["derivatives"] if d.get("height") == 1080 and "transcoded" in d["src"]]
print(sorted(ders, key=lambda d: "vp9" not in d.get("transcodekey", ""))[0]["src"])
PY
)
  curl -sSfL -A "$UA" --retry 8 --retry-delay 30 -o "$TMP/$1" "$url"
}
fetch st.webm   "File:How ST designs and manufactures semiconductor devices.webm"
fetch ibm.webm  "File:JSR and IBM Quantum envision a revolution in semiconductor manufacturing.webm"
fetch port.webm "File:Aerial views of a container terminal at the Port of Cork, Cork, Ireland.webm"
enc="-an -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 -g 15 -movflags +faststart"
IBM="crop=iw*0.733:ih*0.733,scale=1920:1080:flags=lanczos,setsar=1"   # IBM film is letterboxed 2.4:1
cut() { ffmpeg -v error -y -ss "$2" -t "$3" -i "$TMP/$1" -vf "$4" $enc "media/$5.mp4"; }
cut st.webm   112.0 5.5 "scale=1920:1080,setsar=1" st_chips
cut ibm.webm  30.0  6.5 "$IBM" ibm_die
cut ibm.webm  22.6  4.0 "$IBM" ibm_board
cut ibm.webm  45.6  3.5 "$IBM" ibm_yellowfab
cut ibm.webm  81.0  4.0 "$IBM" ibm_corridor
cut port.webm 13.8  4.0 "scale=1920:1080,setsar=1" port_top
cut port.webm 78.0  4.0 "scale=1920:1080,setsar=1" port_crane
ffmpeg -v error -y -sseof -0.1 -i media/port_crane.mp4 -frames:v 1 -update 1 media/port_crane_last.jpg
# Synthesized sound design (no third-party audio).
mkdir -p sfx; A="-ar 48000 -ac 2"
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.9*sin(2*PI*(40+80*exp(-t*18))*t)*exp(-t*2.6)':s=48000:d=1.6" $A sfx/boom.wav
ffmpeg -v error -y -f lavfi -i "anoisesrc=d=0.9:c=pink:a=0.6,highpass=f=300,lowpass=f=5000,afade=t=in:d=0.45:curve=exp,afade=t=out:st=0.45:d=0.45" $A sfx/whoosh.wav
ffmpeg -v error -y -f lavfi -i "aevalsrc='(0.8*sin(2*PI*90*t)+0.5*(random(0)*2-1))*exp(-t*14)':s=48000:d=0.5" -af lowpass=f=2500 $A sfx/stamp.wav
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.22*(sin(2*PI*55*t)+0.6*sin(2*PI*82.41*t)+0.4*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.15*t)))':s=48000:d=52" -af "lowpass=f=600,afade=t=in:d=3,afade=t=out:st=48:d=4" $A sfx/drone.wav
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.7*(random(0)*2-1)*exp(-t*30)+0.5*sin(2*PI*1800*t)*exp(-t*25)':s=48000:d=0.4" -af highpass=f=800 $A sfx/snap.wav
rm -rf "$TMP"
echo "media ready"
