#!/usr/bin/env python3
"""Patient Wikimedia Commons fetcher for a rate-limited cloud IP (PLAYBOOK §8.1: Commons 429s under load).

  python3 tools/commons_slow.py search OUT.jsonl "query" ["query" ...]     # file titles per query (12 each)
  python3 tools/commons_slow.py get OUTDIR "File:A.jpg" ["File:B.jpg" ...]  # licence + 1920 px thumb + manifest row

Every request waits at least GAP seconds after the previous one and backs off (60 s, 120 s, 240 s) on a 429 or an
HTML error page. `get` appends one JSON line per file to OUTDIR/manifest.jsonl (title, file, url, page, licence,
licence_url, artist, credit, description) and skips titles already there. Non-commercial or no-derivatives licences
are refused (CLAUDE.md rights rules).
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "CreatorDocBot/1.0 (documentary research for Be Practical with Kishore; github.com/mkmk749278)"
API = "https://commons.wikimedia.org/w/api.php"
GAP = 6.0
_last = [0.0]


def fetch(url, binary=False):
    for wait in (0, 60, 120, 240, 480):
        if wait:
            print(f"  backoff {wait}s", file=sys.stderr, flush=True)
            time.sleep(wait)
        time.sleep(max(0.0, GAP - (time.time() - _last[0])))
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90) as r:
                data, ctype = r.read(), r.headers.get("Content-Type", "")
        except Exception as e:  # 429, 5xx, resets
            print(f"  {type(e).__name__}: {str(e)[:80]}", file=sys.stderr, flush=True)
            continue
        if binary and "text/html" in ctype:
            continue
        if not binary:
            try:
                return json.loads(data)
            except ValueError:
                continue
        return data
    raise RuntimeError(f"gave up: {url}")


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def search(out, queries):
    with open(out, "a", encoding="utf-8") as f:
        for q in queries:
            d = fetch(f"{API}?action=query&list=search&srnamespace=6&srlimit=12&format=json&srsearch=" + urllib.parse.quote(q))
            titles = [x["title"] for x in d["query"]["search"]]
            f.write(json.dumps({"query": q, "titles": titles}, ensure_ascii=False) + "\n"); f.flush()
            print(q, "->", len(titles), flush=True)


def get(outdir, titles):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    man = outdir / "manifest.jsonl"
    done = {json.loads(l)["title"] for l in man.read_text().splitlines()} if man.exists() else set()
    for t in titles:
        if t in done:
            continue
        d = fetch(f"{API}?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1920&titles="
                  + urllib.parse.quote(t))
        page = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in page:
            print("missing", t, flush=True); continue
        ii = page["imageinfo"][0]; md = ii.get("extmetadata", {})
        lic = strip(md.get("LicenseShortName", {}).get("value"))
        if re.search(r"\bNC\b|\bND\b|non-?commercial|no ?deriv", lic, re.I):
            print("refused licence", lic, t, flush=True); continue
        src = ii.get("thumburl") if ii.get("width", 0) > 1920 else ii["url"]
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", t.split(":", 1)[1])
        (outdir / name).write_bytes(fetch(src, binary=True))
        row = dict(title=t, file=name, url=src, page=ii.get("descriptionurl"), licence=lic,
                   licence_url=strip(md.get("LicenseUrl", {}).get("value")), artist=strip(md.get("Artist", {}).get("value")),
                   credit=strip(md.get("Credit", {}).get("value"))[:300],
                   description=strip(md.get("ImageDescription", {}).get("value"))[:400], width=ii.get("width"),
                   height=ii.get("height"))
        with open(man, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print("got", name, lic, flush=True)


if __name__ == "__main__":
    mode, out, *rest = sys.argv[1:]
    (search if mode == "search" else get)(out, rest)
