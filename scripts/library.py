#!/usr/bin/env python3
"""Shared asset library: licence-clean media reused across videos (PLAYBOOK §22.8).

library/manifest.csv is the single record. Small files (<= 5 MB) are committed under library/<kind>/;
larger ones live in library/_cache/ (gitignored) and are re-downloaded by `fetch` from file_url.

  python3 scripts/library.py add --kind hdri --id studio_small_09 --url URL --title T --source-page URL \
      --author A --licence CC0 --licence-url URL [--attribution TEXT] [--notes TEXT]
  python3 scripts/library.py fetch      # download every missing file, verify sha256
  python3 scripts/library.py check      # every row has a file, licence and matching hash
  python3 scripts/library.py list [--kind hdri]

Compositions use a library file by referencing "vendor/library/<kind>/<file>" in index.html;
scripts/vendor-assets.mjs copies it in. Only commercial-use licences (CC0, PD, CC BY, CC BY-SA, explicit
free-commercial licences) belong here; NC/ND never.
"""
import argparse
import csv
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
MANIFEST = LIB / "manifest.csv"
CACHE = LIB / "_cache"
GIT_LIMIT = 5 * 1024 * 1024
FIELDS = ["id", "kind", "file", "in_git", "title", "source_page", "file_url", "author", "licence", "licence_url",
          "attribution", "sha256", "bytes", "notes"]
ALLOWED = ("CC0", "PD", "Public domain", "CC BY", "CC BY-SA", "NASA", "Coverr", "Pexels", "Pixabay", "Unsplash")
UA = "Creator-library/1.0 (+https://github.com/mkmk749278/Creator)"


def rows():
    if not MANIFEST.exists():
        return []
    with MANIFEST.open(newline="") as f:
        return list(csv.DictReader(f))


def save(all_rows):
    LIB.mkdir(exist_ok=True)
    all_rows.sort(key=lambda r: (r["kind"], r["id"]))
    with MANIFEST.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(all_rows)


def path_of(r):
    return (LIB / r["kind"] / r["file"]) if r["in_git"] == "yes" else (CACHE / r["kind"] / r["file"])


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    # curl, not python-requests: some CDNs (Flickr) refuse python clients.
    subprocess.run(["curl", "-fsSL", "--retry", "3", "-A", UA, "-o", str(tmp), url], check=True)
    tmp.replace(dest)


def cmd_add(a):
    if not a.licence.startswith(ALLOWED):
        sys.exit(f"licence {a.licence!r} is not on the commercial-use list {ALLOWED}")
    all_rows = [r for r in rows() if r["id"] != a.id]
    name = a.file or a.url.split("?")[0].rsplit("/", 1)[-1]
    tmp = CACHE / a.kind / name
    download(a.url, tmp)
    size = tmp.stat().st_size
    r = {"id": a.id, "kind": a.kind, "file": name, "in_git": "yes" if size <= GIT_LIMIT else "no",
         "title": a.title, "source_page": a.source_page, "file_url": a.url, "author": a.author, "licence": a.licence,
         "licence_url": a.licence_url, "attribution": a.attribution or f"{a.title} by {a.author} ({a.licence})",
         "sha256": sha256(tmp), "bytes": str(size), "notes": a.notes or ""}
    if r["in_git"] == "yes":
        dest = LIB / a.kind / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp, dest)
    all_rows.append(r)
    save(all_rows)
    print(f"added {a.id}: {size / 1e6:.1f} MB, {'in git' if r['in_git'] == 'yes' else 'cache only'}")


def cmd_fetch(_):
    bad = 0
    for r in rows():
        p = path_of(r)
        if not p.exists():
            print(f"fetch {r['id']}")
            download(r["file_url"], p)
        if sha256(p) != r["sha256"]:
            print(f"HASH MISMATCH {r['id']} ({p})")
            bad += 1
    sys.exit(1 if bad else 0)


def cmd_check(_):
    problems = []
    for r in rows():
        p = path_of(r)
        if not r["licence"].startswith(ALLOWED):
            problems.append(f"{r['id']}: licence {r['licence']}")
        if not r["source_page"] or not r["attribution"]:
            problems.append(f"{r['id']}: missing source page or attribution")
        if r["in_git"] == "yes" and not p.exists():
            problems.append(f"{r['id']}: committed file missing ({p})")
        elif p.exists() and sha256(p) != r["sha256"]:
            problems.append(f"{r['id']}: hash mismatch")
    print("\n".join(problems) or f"library ok ({len(rows())} items)")
    sys.exit(1 if problems else 0)


def cmd_list(a):
    for r in rows():
        if not a.kind or r["kind"] == a.kind:
            print(f"{r['kind']:8} {r['id']:40} {r['licence']:10} {r['title']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    for f in ("kind", "id", "url", "title", "source-page", "author", "licence", "licence-url"):
        p.add_argument(f"--{f}", required=True)
    for f in ("file", "attribution", "notes"):
        p.add_argument(f"--{f}")
    sub.add_parser("fetch")
    sub.add_parser("check")
    p = sub.add_parser("list")
    p.add_argument("--kind")
    a = ap.parse_args()
    {"add": cmd_add, "fetch": cmd_fetch, "check": cmd_check, "list": cmd_list}[a.cmd](a)


if __name__ == "__main__":
    main()
