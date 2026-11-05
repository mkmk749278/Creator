"""Fetch licence-checked media from Wikimedia Commons into an asset folder.

Usage: python scripts/commons_fetch.py OUT_DIR NAME "search query" [--n 6] [--video] [--min-width 1200]
Keeps only Public domain / CC0 / CC BY / CC BY-SA (no NC/ND), reads the licence from each
file's own extmetadata, converts images to 1920-wide JPEG and video to silent 1080p H.264
(<= 20 s), and appends to OUT_DIR/manifest.json with a ready-to-print credit line.
"""
import argparse
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "PhoneConsensusDocBot/0.1 (https://github.com/mkmk749278/Creator; documentary research)"}
OK = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?([- ][0-9.]+)?( [a-z]+)?)$", re.I)


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def get(params, tries=6):
    for i in range(tries):
        r = requests.get(API, params={**params, "format": "json"}, headers=UA, timeout=60)
        if r.status_code == 429 or "ratelimited" in r.text[:300]:
            time.sleep(10 * (i + 1)); continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limited")


def download(url, dest, tries=6):
    for i in range(tries):
        r = requests.get(url, headers=UA, timeout=300, stream=True)
        if r.status_code == 429:
            time.sleep(15 * (i + 1)); continue
        r.raise_for_status()
        with open(dest, "wb") as f:
            for c in r.iter_content(1 << 20):
                f.write(c)
        return
    raise RuntimeError("download rate limited " + url)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("name"); ap.add_argument("query")
    ap.add_argument("--n", type=int, default=6); ap.add_argument("--video", action="store_true")
    ap.add_argument("--min-width", type=int, default=1200); ap.add_argument("--max-dur", type=float, default=20)
    ap.add_argument("--titles", help="exact File: titles separated by |, instead of search")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    mpath = out / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else []
    have = {m["source_page"] for m in manifest}

    if a.titles:
        titles = a.titles.split("|")
    else:
        q = a.query + (" filetype:video" if a.video else " filetype:bitmap")
        res = get({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": 40})
        titles = [x["title"] for x in res["query"]["search"]]
    got = 0
    for i in range(0, len(titles), 20):
        if got >= a.n: break
        info = get({"action": "query", "titles": "|".join(titles[i:i + 20]), "prop": "imageinfo",
                    "iiprop": "url|size|extmetadata|mediatype|mime", "iiurlwidth": 1920})
        for p in info["query"]["pages"].values():
            if got >= a.n: break
            ii = (p.get("imageinfo") or [None])[0]
            if not ii: continue
            md = ii.get("extmetadata", {})
            lic = strip(md.get("LicenseShortName", {}).get("value"))
            if not OK.match(lic) or re.search(r"\b(nc|nd)\b", lic, re.I): continue
            page = ii.get("descriptionurl")
            if page in have: continue
            is_vid = ii.get("mediatype") == "VIDEO"
            if a.video != is_vid: continue
            if not is_vid and ii.get("width", 0) < a.min_width: continue
            idx = len(manifest) + 1
            slug = re.sub(r"[^a-z0-9]+", "-", p["title"][5:].lower())[:40].strip("-")
            raw = out / f".raw_{idx}"
            try:
                download(ii["thumburl"] if not is_vid and ii.get("thumburl") else ii["url"], raw)
                if is_vid:
                    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)],
                                               capture_output=True, text=True).stdout.strip() or 0)
                    ss = max(0.0, min(dur * 0.15, dur - a.max_dur))
                    fn = f"{a.name}_{idx:02d}_{slug}.mp4"
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ss:.2f}", "-t", str(a.max_dur), "-i", str(raw), "-an",
                                    "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p",
                                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-movflags", "+faststart", str(out / fn)], check=True)
                else:
                    fn = f"{a.name}_{idx:02d}_{slug}.jpg"
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", "scale='min(1920,iw)':-2",
                                    "-q:v", "3", str(out / fn)], check=True)
            except Exception as e:  # fail soft per source
                print("skip", p["title"], e, file=sys.stderr); raw.unlink(missing_ok=True); continue
            raw.unlink(missing_ok=True)
            author = strip(md.get("Artist", {}).get("value")) or "Unknown"
            desc = strip(md.get("ImageDescription", {}).get("value"))[:200]
            date = strip(md.get("DateTimeOriginal", {}).get("value"))[:20]
            manifest.append({"file": fn, "name": a.name, "kind": "video" if is_vid else "photo", "title": p["title"],
                             "what_it_shows": desc or p["title"][5:], "date": date, "source_page": page, "author": author[:120],
                             "licence": lic, "licence_url": strip(md.get("LicenseUrl", {}).get("value")),
                             "share_alike": "sa" in lic.lower(),
                             "credit": f"{p['title'][5:].rsplit('.', 1)[0][:60]} · {author[:50]} · {lic} · Wikimedia Commons"})
            have.add(page); got += 1
            print(f"+ {fn}  [{lic}]  {desc[:70]}")
            time.sleep(1.5)
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(f"{a.name}: {got} new")


if __name__ == "__main__":
    main()
