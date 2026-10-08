"""Fetch licence-checked photos via the Openverse API (Flickr, Wikimedia and other CC sources).

Usage: python scripts/openverse_fetch.py OUT_DIR NAME "query" [--n 6] [--min-width 1000] [--prefer flickr]
Keeps CC0 / PDM / CC BY / CC BY-SA only (commercial use + modification allowed), converts to
1920-wide JPEG, and appends to OUT_DIR/manifest.json with Openverse's attribution string.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

UA = {"User-Agent": "PhoneConsensusDocBot/0.1 (https://github.com/mkmk749278/Creator)"}
OK = {"cc0", "pdm", "by", "by-sa"}


def dl(url, dest):
    # curl: Flickr's CDN rejects python-requests but serves curl fine
    subprocess.run(["curl", "-sSfL", "--max-time", "60", "--retry", "1", "-o", str(dest), url], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("name"); ap.add_argument("query")
    ap.add_argument("--n", type=int, default=6); ap.add_argument("--min-width", type=int, default=1000)
    ap.add_argument("--prefer", default="flickr"); ap.add_argument("--must", help="regex the title must match")
    ap.add_argument("--allow-wikimedia", action="store_true", help="also try upload.wikimedia.org (often rate-limited)")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    mpath = out / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else []
    have = {m["source_page"] for m in manifest}
    res = []
    for page in (1, 2, 3):
        r = requests.get("https://api.openverse.org/v1/images/", headers=UA, timeout=60,
                         params={"q": a.query, "license": "cc0,pdm,by,by-sa", "page_size": 20, "page": page})
        if r.status_code != 200: break
        res += r.json().get("results", [])
    res = [x for x in res if x["license"] in OK and (x.get("width") or 0) >= a.min_width
           and (a.allow_wikimedia or "wikimedia.org" not in x["url"])]
    if a.must:
        res = [x for x in res if re.search(a.must, x["title"] or "", re.I)]
    res.sort(key=lambda x: (x["source"] != a.prefer, -(x.get("width") or 0)))
    got = 0
    for x in res:
        if got >= a.n: break
        page = x["foreign_landing_url"]
        if page in have: continue
        idx = len(manifest) + 1
        slug = re.sub(r"[^a-z0-9]+", "-", (x["title"] or "img").lower())[:36].strip("-")
        fn = f"{a.name}_{idx:02d}_{slug}.jpg"
        raw = out / f".raw_{idx}"
        try:
            dl(x["url"], raw)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", "scale='min(1920,iw)':-2", "-q:v", "3", str(out / fn)], check=True)
        except Exception as e:
            print("skip", x["title"], e, file=sys.stderr); raw.unlink(missing_ok=True); continue
        raw.unlink(missing_ok=True)
        lic = ("CC " + x["license"].upper() + " " + (x.get("license_version") or "")).strip() if x["license"] not in ("cc0", "pdm") else x["license"].upper()
        manifest.append({"file": fn, "name": a.name, "kind": "photo", "title": x["title"], "what_it_shows": x["title"],
                         "source_page": page, "file_url": x["url"], "author": x.get("creator") or "Unknown", "source": x["source"],
                         "licence": lic, "licence_url": x.get("license_url"), "share_alike": x["license"] == "by-sa",
                         "credit": f"\"{(x['title'] or '')[:50]}\" · {(x.get('creator') or 'Unknown')[:40]} · {lic} · {x['source']}"})
        have.add(page); got += 1
        print(f"+ {fn} [{lic}] {x['source']} {x['title'][:60]}")
        time.sleep(0.5)
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(f"{a.name}: {got} new (of {len(res)} candidates)")


if __name__ == "__main__":
    main()
