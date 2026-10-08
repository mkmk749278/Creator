#!/usr/bin/env python3
"""Fetch a list of video URLs (optionally just a time range) for a documentary, with a manifest and contact sheet.

Runs where downloads work: the VPS self-hosted runner or GitHub's runner with YT_COOKIES (the "Fetch media"
workflow), or Termux on the phone. Only fetch what may be used: official channels, footage the owner cleared, CC
licences. Every file still needs a credit and a licence row in the project's media_manifest.csv (PLAYBOOK §8, §12).

  python3 scripts/fetch_media.py OUT_DIR "URL" "URL@00:30-00:45" ... [--max-height 1080] [--cookies cookies.txt]

Writes OUT_DIR/<nn>_<id>.mp4, OUT_DIR/fetched.csv (file, url, section, title, uploader, licence, source_duration, height),
OUT_DIR/sheets/ (timecoded contact sheets) and OUT_DIR/fetch.log.md. Fails soft per URL, loud if all fail.
"""
import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse(entry: str):
    if "@" in entry and entry.rsplit("@", 1)[1][:1].isdigit():
        url, section = entry.rsplit("@", 1)
        return url, section
    return entry, ""


def fetch(url: str, section: str, out: Path, n: int, max_h: int, cookies: Path | None, log: list[str]):
    stem = f"{n:02d}"
    args = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node", "--no-playlist", "--restrict-filenames", "--write-info-json",
            "-f", f"bv*[height<={max_h}][ext=mp4]+ba[ext=m4a]/b[height<={max_h}]/b", "--merge-output-format", "mp4",
            "-o", str(out / f"{stem}_%(id)s.%(ext)s")]
    if section:
        args += ["--download-sections", f"*{section}", "--force-keyframes-at-cuts"]
    if cookies:
        args += ["--cookies", str(cookies)]
    r = subprocess.run(args + [url], capture_output=True, text=True)
    files = sorted(out.glob(f"{stem}_*.mp4"))
    if r.returncode != 0 or not files:
        err = next((l for l in reversed(r.stderr.splitlines()) if "ERROR" in l), r.stderr[-200:])
        hint = " (bot check: add YT_COOKIES or use the VPS runner)" if "bot" in err.lower() or "429" in err else ""
        log.append(f"- ⛔ {url} {section}: {err[:200]}{hint}")
        return None
    info_files = sorted(out.glob(f"{stem}_*.info.json"))
    info = json.loads(info_files[0].read_text()) if info_files else {}
    row = {"file": files[0].name, "url": url, "section": section, "title": info.get("title", ""),
           "uploader": info.get("uploader", ""), "licence": info.get("license") or "uploader's copyright (check)",
           "source_duration": f"{float(info.get('duration') or 0):.1f}", "height": str(info.get("height", ""))}
    log.append(f"- ✅ {row['file']}: {row['title'][:70]} · {row['uploader']} · {row['height']}p · {row['licence']}")
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    ap.add_argument("entries", nargs="+", help='URL or "URL@START-END" (e.g. @00:30-00:45)')
    ap.add_argument("--max-height", type=int, default=1080)
    ap.add_argument("--cookies", type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    cookies = None
    if a.cookies and a.cookies.exists() and a.cookies.stat().st_size:
        # yt-dlp rewrites the cookie jar; work on a copy outside the output dir.
        cookies = Path(tempfile.mkdtemp()) / "cookies.txt"
        shutil.copy(a.cookies, cookies)
    log = ["# Media fetch", ""]
    rows = []
    for n, e in enumerate(a.entries, 1):
        url, section = parse(e.strip())
        if url and (row := fetch(url, section, a.out, n, a.max_height, cookies, log)):
            rows.append(row)
    if cookies:
        shutil.rmtree(cookies.parent, ignore_errors=True)
    if rows:
        with (a.out / "fetched.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        frames = a.out / ".frames"
        frames.mkdir(exist_ok=True)
        for r in rows:  # first frame of every 5 s window per clip, named file@time for the sheet labels
            stem = Path(r["file"]).stem
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(a.out / r["file"]), "-vf", "fps=1/5,scale=512:-2",
                            str(frames / f"{stem}@%03d.jpg")], check=False)
        subprocess.run([sys.executable, str(ROOT / "scripts/contact_sheet.py"), str(frames), "--out",
                        str(a.out / "sheets")], check=False)
        shutil.rmtree(frames, ignore_errors=True)
    log.append("")
    log.append(f"{len(rows)} of {len(a.entries)} fetched. Each file still needs a licence row and an on-screen credit.")
    (a.out / "fetch.log.md").write_text("\n".join(log) + "\n")
    print("\n".join(log))
    sys.exit(0 if rows else 1)


if __name__ == "__main__":
    main()
