#!/usr/bin/env python3
"""Batch candidate search for word-level pictures: Pixabay videos (API, AI-tagged hidden) and Openverse photos
(commercial CC licences). Downloads small previews to assets/cand/<key>_<n>.(mp4|jpg) and writes assets/cand/cand.json
with source page, licence and author for every candidate. usage: tools/cand_fetch.py"""
import json, os, re, urllib.parse, urllib.request
from pathlib import Path
P = Path(__file__).resolve().parents[1]; D = P / "assets/cand"; D.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Creator-stock/1.0 (+https://github.com/mkmk749278/Creator)"}
VID = {"gpu": "graphics card", "wallst": "wall street new york", "appstore": "app store iphone", "dollars": "us dollar bills",
       "parliament": "indian parliament", "delhi": "new delhi india gate", "internet": "internet network globe", "taipei": "taipei taiwan city",
       "whitehouse": "white house washington", "usflag": "american flag waving", "cnflag": "china flag", "beijing": "beijing city",
       "engineers": "engineers team discussion office", "dcbuild": "data center construction", "paris": "paris eiffel tower",
       "dial": "knob dial turning", "download": "download progress", "konark": "odisha temple", "kolkata": "kolkata howrah bridge",
       "hyderabad": "hyderabad charminar", "pune": "pune city", "varanasi": "varanasi ghat", "chennai": "chennai city",
       "satellite": "satellite orbit earth", "gpsmap": "phone navigation map", "inflag": "indian flag waving", "calendar": "calendar pages",
       "notify": "smartphone notification", "teacher": "teacher classroom india", "coding": "programmer coding laptop",
       "books": "stack of books", "padlock": "padlock lock", "magnify": "magnifying glass document", "applause": "audience applause conference",
       "wafer": "silicon wafer", "mumbai": "mumbai skyline", "farmerphone": "indian farmer phone", "speakphone": "woman talking phone india",
       "students": "indian students classroom", "money": "rupee money", "handshake": "business handshake", "bridge": "bharat flag crowd india",
       "clock": "clock ticking", "question": "thinking man", "scale": "balance scale", "grow": "plant growing timelapse"}
PHO = {"nvidiahq": "Nvidia headquarters", "nyse": "New York Stock Exchange", "constitution": "Constitution of India", "tsmc": "TSMC fab",
       "metahq": "Meta headquarters", "aadhaar": "Aadhaar card", "mantralaya": "Mantralaya Mumbai", "mandapam": "Bharat Mandapam",
       "iitb": "IIT Bombay", "h100": "Nvidia H100", "isro": "ISRO launch", "budget": "Union Budget India", "sarvam": "Sarvam AI",
       "mistral": "Mistral AI", "deepseek": "DeepSeek", "chatgpt": "ChatGPT", "appleapp": "Apple App Store"}
meta = json.loads((D / "cand.json").read_text()) if (D / "cand.json").exists() else {}
import sys
ONLY = set(sys.argv[1:])
def get(url, dst):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(dst, "wb") as f:
        f.write(r.read())
key = os.environ["PIXABAY_API_KEY"]
for k, q in VID.items():
    if ONLY and "vid" not in ONLY: break
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(f"https://pixabay.com/api/videos/?key={key}&q={urllib.parse.quote(q)}&per_page=12&safesearch=true", headers=UA), timeout=60))
    except Exception as e:
        print(k, "ERR", e); continue
    n = 0
    for h in j.get("hits", []):
        if "ai generated" in (h.get("tags") or "").lower() or h.get("isAiGenerated"):
            continue
        v = h["videos"].get("small") or h["videos"].get("tiny")
        if not v or not v.get("url"):
            continue
        dst = D / f"{k}_{n}.mp4"; get(v["url"], dst)
        meta[dst.name] = dict(kind="video", id=h["id"], page=h["pageURL"], author=h["user"], tags=h["tags"], licence="Pixabay Content License",
                              large=(h["videos"].get("large") or {}).get("url") or (h["videos"].get("medium") or {}).get("url"))
        n += 1
        if n == 3:
            break
    print(k, n)
for k, q in PHO.items():
    if ONLY and "pho" not in ONLY: break
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&license_type=commercial&page_size=6", headers=UA), timeout=60))
    except Exception as e:
        print(k, "ERR", e); continue
    n = 0
    for r in j.get("results", []):
        u = r.get("thumbnail") or r.get("url")
        try:
            dst = D / f"{k}_{n}.jpg"; get(u, dst)
        except Exception:
            continue
        meta[dst.name] = dict(kind="photo", page=r.get("foreign_landing_url"), url=r.get("url"), author=r.get("creator"), title=r.get("title"),
                              licence=f"{r.get('license')} {r.get('license_version')}", source=r.get("source"))
        n += 1
        if n == 4:
            break
    print(k, n)
(D / "cand.json").write_text(json.dumps(meta, indent=1))
