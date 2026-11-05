#!/usr/bin/env python3
"""List and fetch the images a Wikipedia article uses, with licence, size and date (PLAYBOOK §11.1, §11.3).

Commons category pages often miss the best archive photo; the article about the subject usually carries it. One API
call per article lists every file with its Commons extmetadata (licence, author, date, description), so we choose by
reading, then download only the chosen files, slowly (Commons answers 429 after ~5 files a minute).

  python3 scripts/wiki_images.py list "Dorabji Tata" "Jubilee Diamond"          # prints candidates (no download)
  python3 scripts/wiki_images.py get OUT_DIR ID "File:Name.jpg" [ID "File:..."]  # downloads ≤ 3840 px, appends manifest.json

Keeps only Public domain / CC0 / CC BY / CC BY-SA / GODL-India (no NC/ND, no fair use). get waits 15 s between files and
retries a 429 after 90 s, twice.
"""
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

API = "https://en.wikipedia.org/w/api.php"
UA = "BuiltOnBharatDocBot/0.1 (https://github.com/mkmk749278/Built-on-Bharat; documentary research)"
OK = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?([- ][0-9.]+)?( [a-z]+)?|godl-india)", re.I)


def api(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def strip(s: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def info(titles: list[str]) -> list[dict]:
    out = []
    for i in range(0, len(titles), 40):
        d = api({"action": "query", "titles": "|".join(titles[i:i + 40]), "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 3840})
        for p in d["query"]["pages"]:
            ii = (p.get("imageinfo") or [{}])[0]
            m = ii.get("extmetadata", {})
            g = lambda k: strip(m.get(k, {}).get("value", ""))
            out.append({"title": p["title"], "w": ii.get("width"), "h": ii.get("height"), "mime": ii.get("mime"),
                        "licence": g("LicenseShortName"), "author": g("Artist"), "date": g("DateTimeOriginal") or g("DateTime"),
                        "desc": g("ImageDescription")[:220], "credit": g("Credit")[:120], "page": ii.get("descriptionurl"),
                        "thumb": ii.get("thumburl") or ii.get("url"), "url": ii.get("url")})
    return out


def cmd_list(articles: list[str]) -> None:
    for a in articles:
        d = api({"action": "query", "titles": a, "prop": "images", "imlimit": 100, "redirects": 1})
        files = [im["title"] for p in d["query"]["pages"] for im in p.get("images", [])]
        files = [f for f in files if not re.search(r"\.svg$|Commons-logo|Wiki|Edit-clear|Question_book|Flag_of|icon|Symbol", f, re.I)]
        print(f"## {a}: {len(files)} files")
        for x in info(files):
            ok = "OK " if OK.match(x["licence"] or "") else "-- "
            print(f"  {ok}{x['title']} | {x['w']}x{x['h']} | {x['licence']} | {x['date'][:30]} | {x['author'][:40]} | {x['desc'][:120]}")
        time.sleep(2)


def cmd_get(out: Path, pairs: list[str]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    mf = out / "manifest.json"
    man = json.loads(mf.read_text()) if mf.exists() else []
    for k in range(0, len(pairs), 2):
        aid, title = pairs[k], pairs[k + 1]
        x = info([title])[0]
        if not OK.match(x["licence"] or ""):
            print(f"skip {title}: licence {x['licence']!r}")
            continue
        ext = ".jpg" if "jpeg" in (x["mime"] or "") or (x["mime"] or "").startswith("image/") else Path(x["url"]).suffix
        dest = out / f"{aid}{'.jpg' if (x['mime'] or '').startswith('image/') else ext}"
        src = x["thumb"] if (x["w"] or 0) > 3840 else x["url"]
        for attempt in range(3):
            r = subprocess.run(["curl", "-sSfL", "--max-time", "180", "-A", UA, "-o", str(dest) + ".raw", src])
            if r.returncode == 0:
                break
            print(f"  {aid}: retry in 90 s")
            time.sleep(90)
        else:
            print(f"FAIL {aid} {title}")
            continue
        if (x["mime"] or "").startswith("image/"):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(dest) + ".raw", "-q:v", "2", str(dest)], check=True)
            Path(str(dest) + ".raw").unlink()
        else:
            Path(str(dest) + ".raw").rename(dest)
        man = [m for m in man if m["id"] != aid] + [{"id": aid, "file": dest.name, **x}]
        mf.write_text(json.dumps(man, indent=1, ensure_ascii=False))
        print(f"ok {aid} {title} {x['w']}x{x['h']} {x['licence']}")
        time.sleep(15)


if __name__ == "__main__":
    if sys.argv[1] == "list":
        cmd_list(sys.argv[2:])
    else:
        cmd_get(Path(sys.argv[2]), sys.argv[3:])
