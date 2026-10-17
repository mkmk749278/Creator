#!/usr/bin/env python3
"""Re-download the film's stock clips and Commons photos into assets/ from media_manifest.csv (assets/ is gitignored, so a
fresh cloud session starts without them). Pixabay/Coverr: the logged CDN URL. Commons: Special:FilePath at 1920 px with
a User-Agent (PLAYBOOK §8.1), resized to 1920 wide like scripts/commons_fetch.py did. Skips files already present.
Usage: python3 projects/minimum-due/build/fetch_assets.py
"""
import csv, subprocess, sys, time, urllib.parse
from pathlib import Path

P = Path(__file__).resolve().parents[1]
A = P / "assets"
UA = "PhoneConsensusDocBot/0.1 (https://github.com/mkmk749278/Creator; documentary research)"
EXTRA = {"pixabay_38084.mp4": ["broll_new"]}   # assemble.py reads this one from broll_new/


def curl(url, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".part")
    r = subprocess.run(["curl", "-sSL", "-m", "300", "-A", UA, "-o", str(tmp), "-w", "%{http_code}", url], capture_output=True, text=True)
    if r.stdout.strip() == "200" and tmp.stat().st_size > 10000:
        tmp.rename(out); return True
    tmp.unlink(missing_ok=True); print("FAIL", r.stdout.strip(), url, file=sys.stderr); return False


ok = fail = 0
for row in csv.DictReader(open(P / "media_manifest.csv")):
    f = row["file"]
    if f.startswith("commons"):
        dest = A / f
        if dest.exists():
            continue
        name = urllib.parse.unquote(row["source_page"].split("File:")[1])
        url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(name) + "?width=1920"
        raw = dest.with_suffix(".src")
        if curl(url, raw):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vf", "scale='min(1920,iw)':-2", "-q:v", "2", str(dest)])
            raw.unlink(); ok += 1
        else:
            fail += 1
        time.sleep(12)   # Commons rate-limits (429 at 2 s spacing on 2026-10-12); be polite
    elif row["file_url"]:
        targets = [A / "broll" / f] + [A / d / f for d in EXTRA.get(f, [])]
        if all(t.exists() for t in targets):
            continue
        if curl(row["file_url"], targets[0]):
            for t in targets[1:]:
                t.parent.mkdir(parents=True, exist_ok=True); t.write_bytes(targets[0].read_bytes())
            ok += 1
        else:
            fail += 1
print(f"fetched {ok}, failed {fail}")
