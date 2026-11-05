#!/usr/bin/env python3
"""Fetch Library of Congress Prints & Photographs items by id, largest image first (PLAYBOOK §11.1).

  python3 scripts/loc_fetch.py OUT_DIR ID:pk [ID:pk ...]      e.g. A001a:2014680360

For each item: reads https://www.loc.gov/pictures/item/<pk>/?fo=json, keeps it only if the rights statement says
"No known restrictions" (or public domain), downloads the largest JPEG/TIFF offered, converts it to a max-3840 px
JPEG, and appends title, date, rights, credit and source URL to OUT_DIR/manifest.json. Polite: 4 s between items.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

UA = "BuiltOnBharatDocBot/0.1 (https://github.com/mkmk749278/Built-on-Bharat; documentary research)"


def get_json(url: str) -> dict:
    r = subprocess.run(["curl", "-sSfL", "-m", "90", "-A", UA, url], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    mf = out / "manifest.json"
    man = json.loads(mf.read_text()) if mf.exists() else []
    for spec in sys.argv[2:]:
        aid, pk = spec.split(":", 1)
        try:
            d = get_json(f"https://www.loc.gov/pictures/item/{pk}/?fo=json")
        except Exception as e:  # fail soft per source
            print(f"FAIL {aid} {pk}: {e}")
            continue
        it = d.get("item", {})
        rights = " ".join(d.get("rights_information", "") if isinstance(d.get("rights_information"), list) else [str(d.get("rights_information", ""))])
        rights += " " + str(it.get("rights_information", ""))
        if not re.search(r"no known restrictions|public domain", rights, re.I):
            print(f"skip {aid} {pk}: rights {rights[:120]!r}")
            continue
        res = d.get("resources", [])
        urls = []
        for r in res:
            for k in ("larger", "large", "tiff", "medium"):
                if r.get(k):
                    urls.append(r[k])
        urls = sorted(set(urls), key=lambda u: (u.endswith(".tif"), "v.jpg" in u or "r.jpg" in u), reverse=True)
        if not urls:
            print(f"FAIL {aid} {pk}: no image")
            continue
        raw = out / f"{aid}.raw"
        ok = False
        for u in urls:
            u = "https:" + u if u.startswith("//") else u
            if subprocess.run(["curl", "-sSfL", "-m", "300", "-A", UA, "-o", str(raw), u]).returncode == 0:
                ok = True
                break
        if not ok:
            print(f"FAIL {aid} {pk}: download")
            continue
        dest = out / f"{aid}.jpg"
        if subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vf", "scale='min(3840,iw)':-2", "-q:v", "2",
                           str(dest)]).returncode != 0:
            try:  # some LoC TIFFs (16-bit, odd compression) only open in Pillow
                from PIL import Image
                im = Image.open(raw)
                im = im.convert("RGB") if im.mode not in ("I;16", "I") else im.point(lambda v: v / 256).convert("RGB")
                im.thumbnail((3840, 3840))
                im.save(dest, quality=93)
            except Exception as e:
                print(f"FAIL {aid} {pk}: convert {e}")
                raw.unlink()
                continue
        raw.unlink()
        wh = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(dest)],
                            capture_output=True, text=True).stdout.strip()
        man = [m for m in man if m["id"] != aid] + [{
            "id": aid, "file": dest.name, "title": it.get("title", ""), "date": it.get("created_published_date", ""),
            "creator": it.get("creator", ""), "rights": rights.strip()[:300], "size": wh,
            "source": f"https://www.loc.gov/pictures/item/{pk}/",
            "credit": f"Library of Congress, Prints & Photographs Division ({pk})"}]
        mf.write_text(json.dumps(man, indent=1, ensure_ascii=False))
        print(f"ok {aid} {pk} {wh} {it.get('title', '')[:70]}")
        time.sleep(4)


if __name__ == "__main__":
    main()
