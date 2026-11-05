"""Fetch licence-checked media from Wikimedia Commons category pages when the Commons API rate-limits (429).

Usage: python scripts/commons_html_fetch.py OUT_DIR NAME "Category:HAL Tejas Mk1A" [--n 20] [--video] [--must REGEX]
Reads the category's HTML gallery (the website kept answering on 2026-10-23 while the API returned "too many
requests"), opens each File: page for its licence and author (licensetpl_* spans), keeps Public domain / CC0 /
CC BY / CC BY-SA / GODL-India only, downloads a standard 1920 px thumbnail (or the video), and appends to OUT_DIR/manifest.json in
the same format as scripts/commons_fetch.py.
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import requests

UA = {"User-Agent": "PhoneConsensusDocBot/0.1 (https://github.com/mkmk749278/Creator; documentary research)"}
OK = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?([- ][0-9.]+)?( [a-z]+)?|godl-india)$", re.I)  # GODL-India: commercial use with attribution
WIKI = "https://commons.wikimedia.org/wiki/"


def get(url, tries=5):
    for i in range(tries):
        r = requests.get(url, headers=UA, timeout=90)
        if r.status_code == 429:
            time.sleep(15 * (i + 1)); continue
        r.raise_for_status()
        return r.text
    raise RuntimeError("rate limited " + url)


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def span(page, cls):
    m = re.search(r'<span class="licensetpl_%s"[^>]*>(.*?)</span>' % cls, page, re.S)
    return strip(m.group(1)) if m else ""


def file_url(name, width=None):
    # upload.wikimedia.org path: md5 of the underscored file name
    n = name.replace(" ", "_"); h = hashlib.md5(n.encode()).hexdigest(); q = urllib.parse.quote(n)
    base = "https://upload.wikimedia.org/wikipedia/commons"
    return f"{base}/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}" if width else f"{base}/{h[0]}/{h[:2]}/{q}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("name"); ap.add_argument("category")
    ap.add_argument("--n", type=int, default=20); ap.add_argument("--video", action="store_true")
    ap.add_argument("--must", help="regex the file title must match"); ap.add_argument("--max-dur", type=float, default=30)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    mpath = out / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else []
    have = {m["source_page"] for m in manifest}
    cat = get(WIKI + urllib.parse.quote(a.category.replace(" ", "_")))
    titles = list(dict.fromkeys(html.unescape(t) for t in re.findall(r'class="galleryfilename[^"]*"[^>]*title="(File:[^"]+)"', cat)
                                or re.findall(r'title="(File:[^"]+)"', cat)))
    vid = re.compile(r"\.(webm|ogv|mp4|mpg)$", re.I)
    titles = [t for t in titles if bool(vid.search(t)) == a.video and not t.lower().endswith((".ogg", ".svg", ".pdf", ".tif", ".tiff"))]
    if a.must:
        titles = [t for t in titles if re.search(a.must, t, re.I)]
    got = 0
    for t in titles:
        if got >= a.n: break
        page_url = WIKI + urllib.parse.quote(t.replace(" ", "_"))
        if page_url in have: continue
        try:
            page = get(page_url)
        except Exception as e:
            print("skip", t, e, file=sys.stderr); continue
        lic = span(page, "short")
        if not OK.match(lic) or re.search(r"\b(nc|nd)\b", lic, re.I):
            print("skip licence", lic or "?", t, file=sys.stderr); continue
        author = span(page, "attr") or strip((re.search(r'id="fileinfotpl_aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', page, re.S) or [None, ""])[1]) or "Unknown"
        desc = strip((re.search(r'class="description[^"]*"[^>]*>(.*?)</div>', page, re.S) or [None, ""])[1])[:200]
        name = t[5:]; idx = len(manifest) + 1
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower())[:40].strip("-")
        raw = out / f".raw_{idx}"
        try:
            if a.video:
                src = re.search(r'<source src="(https://upload\.wikimedia\.org/[^"]+?\.(?:1080p|720p)\.[^"]+)"', page) or \
                      re.search(r'<source src="(https://upload\.wikimedia\.org/[^"]+)"', page)
                subprocess.run(["curl", "-sSfL", "--max-time", "300", "-A", UA["User-Agent"], "-o", str(raw),
                                html.unescape(src.group(1)) if src else file_url(name)], check=True)
                fn = f"{a.name}_{idx:02d}_{slug}.mp4"
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(a.max_dur), "-i", str(raw), "-an",
                                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1,fps=30,format=yuv420p",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-movflags", "+faststart", str(out / fn)], check=True)
            else:
                fn = f"{a.name}_{idx:02d}_{slug}.jpg"
                r = subprocess.run(["curl", "-sSfL", "--max-time", "120", "-A", UA["User-Agent"], "-o", str(raw), file_url(name, 1920)])
                if r.returncode:  # images narrower than 1920 have no 1920 thumb: take the original
                    subprocess.run(["curl", "-sSfL", "--max-time", "120", "-A", UA["User-Agent"], "-o", str(raw), file_url(name)], check=True)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", "scale='min(1920,iw)':-2",
                                "-q:v", "2", str(out / fn)], check=True)
        except Exception as e:  # fail soft per source
            print("skip", t, e, file=sys.stderr); raw.unlink(missing_ok=True); continue
        raw.unlink(missing_ok=True)
        lic_url = span(page, "link")
        manifest.append({"file": fn, "name": a.name, "kind": "video" if a.video else "photo", "title": t,
                         "what_it_shows": desc or name, "date": "", "source_page": page_url, "author": author[:120],
                         "licence": lic, "licence_url": lic_url, "share_alike": "sa" in lic.lower(),
                         "credit": f"{name.rsplit('.', 1)[0][:60]} · {author[:50]} · {lic} · Wikimedia Commons"})
        have.add(page_url); got += 1
        print(f"+ {fn}  [{lic}]  {(desc or name)[:70]}")
        mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
        time.sleep(2)
    print(f"{a.name}: {got} new (of {len(titles)} candidates)")


if __name__ == "__main__":
    main()
