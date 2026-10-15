#!/usr/bin/env python3
"""Search Openverse audio (commercial-use licences only), download the best short match per cue, log manifest rows.

  python3 tools/sfx_fetch.py      # cues below -> assets/sfx/<cue>.<ext>, rows appended to media_manifest.csv
"""
import csv, json, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path
P = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Creator-doc-sourcing/1.0 (Be Practical with Kishore)"}
CUES = {  # cue: (query, max seconds)
    "train_horn": ("train horn", 20), "train_pass": ("train passing", 40), "rail_clatter": ("train interior rhythm", 60),
    "brake_squeal": ("train brakes squeal", 20), "air_hiss": ("air brake hiss", 10), "phone_buzz": ("phone vibrate", 10),
    "stamp": ("rubber stamp", 5), "marker": ("marker whiteboard writing", 20), "braam": ("cinematic boom impact", 10),
    "power_down": ("power down", 8), "rain_window": ("rain on window", 60), "radio_beep": ("radio static beep", 10),
    "notification": ("notification ping", 5), "glass_crack": ("glass crack", 6), "whoosh": ("whoosh", 4),
}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
rows = []
for cue, (q, maxs) in CUES.items():
    u = "https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode({"q": q, "license_type": "commercial", "page_size": 20})
    try:
        res = [r for r in get(u)["results"] if r.get("duration") and r["duration"] / 1000 <= maxs and r.get("url")]
    except Exception as e:
        print(cue, "search failed", e); continue
    for r in res[:3]:
        ext = (r.get("filetype") or Path(urllib.parse.urlparse(r["url"]).path).suffix.lstrip(".") or "mp3")
        out = P / "assets/sfx" / f"{cue}.{ext}"
        try:
            urllib.request.urlretrieve(r["url"], out) if False else open(out, "wb").write(urllib.request.urlopen(urllib.request.Request(r["url"], headers=UA), timeout=60).read())
        except Exception as e:
            print(cue, "download failed", r["url"], e); continue
        rows.append([f"sfx/{out.name}", "audio", f"{r['title']} ({cue})", r["foreign_landing_url"], r["url"], r.get("creator") or "",
                     f"{r['license'].upper()} {r.get('license_version') or ''}".strip(), r.get("license_url") or "",
                     f"{r['title']} by {r.get('creator') or 'unknown'} ({r['license'].upper()})", "", "", "N22"])
        print(cue, "->", out.name, r["title"], r["license"], round(r["duration"] / 1000, 1), "s"); break
    else:
        print(cue, "no match")
csv.writer(open(P / "media_manifest.csv", "a", newline="")).writerows(rows)
