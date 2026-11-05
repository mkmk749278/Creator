#!/usr/bin/env python3
"""Append media_manifest.csv rows for every prepared crop (media/crops.json) and every listed raw file not yet logged
(PLAYBOOK §11: every asset with its licence). Licence and credit come from the fetch manifests (Commons:
assets/media/raw/wm/manifest.json, Library of Congress: assets/media/loc/manifest.json).

Usage: scripts/manifest_rows.py films/<slug> [ID=raw/wm/FILE ...]   (extra IDs for raw files used without a crop)
"""
import csv
import json
import re
import sys
from pathlib import Path

from PIL import Image


def clean(a: str) -> str:
    return re.sub(r"(Unknown author)+", "Unknown author", re.sub(r"(Anonymous)?Unknown author", "Unknown author", a or ""))


def main() -> None:
    film = Path(sys.argv[1])
    media = film / "assets/media"
    crops = json.loads((film / "media/crops.json").read_text())
    wm = {x["file"]: x for x in json.loads((media / "raw/wm/manifest.json").read_text())}
    loc = {x["file"]: x for x in json.loads((media / "loc/manifest.json").read_text())}
    path = film / "media_manifest.csv"
    rows = list(csv.DictReader(path.open()))
    have = {r["id"] for r in rows}
    items = [(k, v[0], f"assets/media/{k}.jpg") for k, v in crops.items() if not k.startswith("_")]
    items += [(a.split("=")[0], a.split("=")[1], f"assets/media/{a.split('=')[1]}") for a in sys.argv[2:]]
    new = []
    for k, src, out in items:
        if k in have:
            continue
        fn = src.split("/")[-1]
        try:
            w, h = Image.open(film / out).size
        except OSError:
            w = h = ""
        if src.startswith("loc/"):
            x = loc.get(fn)
            if not x:
                print("missing loc entry", k, fn)
                continue
            r = dict(id=k, file=out, what_it_shows=x["title"], date_of_subject=x.get("date", "").strip("."), source_url=x["source"],
                     licence="No known restrictions on publication (Library of Congress)", credit=x["credit"])
        else:
            x = wm.get(fn)
            if not x:
                print("missing Commons entry", k, fn)
                continue
            name = x["title"].replace("File:", "").rsplit(".", 1)[0]
            r = dict(id=k, file=out, what_it_shows=x["title"].replace("File:", ""), date_of_subject=x.get("date", ""), source_url=x["source_page"],
                     licence=x["licence"], credit=f"{name[:70]} · {clean(x['author'])[:60]} · {x['licence']} · Wikimedia Commons")
        r.update(width=w, height=h, duration_s="", use_note="film 1",
                 status="ok" if "BY" not in r["licence"] else "ok (credit + share-alike noted in description)")
        new.append(r)
    with path.open("a", newline="") as f:
        csv.DictWriter(f, fieldnames=list(rows[0].keys())).writerows(new)
    print(len(new), "rows:", " ".join(r["id"] for r in new))


if __name__ == "__main__":
    main()
