"""Search and download openly licensed media into assets/, logging every file in media_manifest.csv.

Sources that work from a datacenter IP: Coverr (real stock video, free licence), NASA Images, Wellcome
Collection, Openverse (CC images/audio, e.g. Flickr, Freesound), Internet Archive, Wikimedia Commons search
(file downloads from upload.wikimedia.org are often rate-limited, 429). YouTube video, Pexels, Pixabay and
Mixkit block datacenter IPs.

  python tools/fetch_assets.py search commons "hospital corridor" [--video]
  python tools/fetch_assets.py search coverr "hospital"
  python tools/fetch_assets.py search openverse "kidney" [--audio]
  python tools/fetch_assets.py search nasa "astronaut ISS"
  python tools/fetch_assets.py search wellcome "kidney"
  python tools/fetch_assets.py get commons "File:Foo.webm" cctv_camera.mp4 [--start 3 --dur 8]
  python tools/fetch_assets.py get nasa <nasa_id> astronaut_iss.mp4
  python tools/fetch_assets.py get wellcome <image_id> kidney_anatomy.jpg
  python tools/fetch_assets.py get url <direct-url> name.ext --owner X --licence Y --page Z
Videos are normalised to H.264 1080p30 (trimmed with --start/--dur); images are saved as JPEG ≤ 4K.
"""
import argparse
import csv
import datetime
import html
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = HERE / "assets"
MANIFEST = HERE / "media_manifest.csv"
UA = "PhoneConsensusDoc/1.0 (https://github.com/mkmk749278/Creator; documentary research)"
FIELDS = ["asset_id", "file_name", "url", "owner", "licence", "downloaded", "edl_slots", "notes"]


def fetch(url, binary=False, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            return data if binary else json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                time.sleep(int(e.headers.get("retry-after") or 5) + 2 * i)
                continue
            raise


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


# ---------- search ----------
def search_commons(q, video):
    ns = "6"
    query = f"{q} filetype:{'video' if video else 'bitmap'}"
    d = fetch("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(
        action="query", generator="search", gsrsearch=query, gsrnamespace=ns, gsrlimit=20, prop="imageinfo",
        iiprop="url|size|extmetadata|mediatype", format="json")))
    for p in sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        print(f"{p['title']} | {ii.get('width')}x{ii.get('height')} | {m.get('LicenseShortName', {}).get('value')} | "
              f"{strip(m.get('Artist', {}).get('value'))[:40]} | dur={ii.get('duration', '')}")


def search_coverr(q, _video):
    req = urllib.request.Request("https://coverr.co/s?" + urllib.parse.urlencode(dict(q=q)),
                                 headers={"User-Agent": "Mozilla/5.0"})
    page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    seen = []
    for u in re.findall(r'"mp4":"(https://cdn\.coverr\.co/videos/coverr-[^"/]+)/1080p\.mp4"', page):
        if u not in seen:
            seen.append(u)
    for u in seen[:25]:  # real footage only (AI clips live under user-ai-generation-*)
        print(f"{u}/1080p.mp4 | {u.rsplit('/', 1)[1]}")


def search_openverse(q, audio):
    kind = "audio" if audio else "images"
    d = fetch(f"https://api.openverse.org/v1/{kind}/?" + urllib.parse.urlencode(
        dict(q=q, license_type="commercial", page_size=20)))
    for it in d["results"]:
        print(f"{it['url']} | {it.get('license')} {it.get('license_version')} | {it.get('creator')} | "
              f"{it.get('source')} | {(it.get('title') or '')[:60]} | {it.get('foreign_landing_url')} | "
              f"{it.get('width', '')}x{it.get('height', '')} dur={it.get('duration', '')}")


def search_nasa(q, video):
    d = fetch("https://images-api.nasa.gov/search?" + urllib.parse.urlencode(
        dict(q=q, media_type="video" if video else "image")))
    for it in d["collection"]["items"][:20]:
        m = it["data"][0]
        print(f"{m['nasa_id']} | {m.get('date_created', '')[:10]} | {m.get('title', '')[:90]}")


def search_wellcome(q, _video):
    d = fetch("https://api.wellcomecollection.org/catalogue/v2/images?" + urllib.parse.urlencode(
        dict(query=q, pageSize=20, include="source.contributors")))
    for it in d["results"]:
        lic = (it.get("locations") or [{}])[0].get("license", {}).get("id")
        print(f"{it['id']} | {lic} | {it.get('source', {}).get('title', '')[:90]}")


# ---------- get ----------
def normalise(raw, out, start, dur):
    if out.suffix.lower() in (".mp3", ".wav", ".m4a"):
        cmd = ["ffmpeg", "-y", "-loglevel", "error"] + (["-ss", str(start)] if start else []) + ["-i", str(raw)]
        cmd += (["-t", str(dur)] if dur else []) + ["-vn", "-ar", "48000", str(out)]
    elif out.suffix.lower() in (".jpg", ".jpeg", ".png"):
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf",
               "scale='min(3840,iw)':-2", "-frames:v", "1", "-q:v", "2", str(out)]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error"] + (["-ss", str(start)] if start else []) + ["-i", str(raw)]
        cmd += (["-t", str(dur)] if dur else []) + [
            "-vf", "scale=-2:'min(1080,ih)',fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18",
            "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-1500:])


def log(name, url, owner, licence, notes=""):
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8"))) if MANIFEST.exists() else []
    rows = [r for r in rows if r["file_name"] != name]
    rows.append(dict(asset_id="", file_name=name, url=url, owner=owner, licence=licence,
                     downloaded=datetime.date.today().isoformat(), edl_slots="", notes=notes))
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["file_name"]))


def get(source, ref, name, a):
    ASSETS.mkdir(exist_ok=True)
    tmp = ASSETS / f".dl_{name}"
    if source == "commons":
        title = ref if ref.startswith("File:") else f"File:{ref}"
        d = fetch("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(
            action="query", titles=title, prop="imageinfo", iiprop="url|extmetadata", format="json")))
        ii = next(iter(d["query"]["pages"].values()))["imageinfo"][0]
        m = ii.get("extmetadata", {})
        url, page = ii["url"], ii["descriptionurl"]
        owner = strip(m.get("Artist", {}).get("value")) or "unknown"
        lic = m.get("LicenseShortName", {}).get("value", "")
    elif source == "nasa":
        files = fetch(f"https://images-api.nasa.gov/asset/{ref}")["collection"]["items"]
        hrefs = [f["href"] for f in files]
        pick = [h for h in hrefs if h.endswith("~large.mp4")] or [h for h in hrefs if h.endswith("~orig.mp4")] or \
               [h for h in hrefs if h.endswith(".mp4")] or \
               [h for h in hrefs if h.endswith("~orig.jpg")] or [h for h in hrefs if h.endswith(".jpg")]
        url, page, owner, lic = pick[0].replace("http://", "https://"), f"https://images.nasa.gov/details/{ref}", "NASA", "Public domain (NASA)"
    elif source == "wellcome":
        it = fetch(f"https://api.wellcomecollection.org/catalogue/v2/images/{ref}?include=source.contributors")
        loc = it["locations"][0]
        base = loc["url"].replace("/info.json", "")
        url, page = f"{base}/full/3000,/0/default.jpg", f"https://wellcomecollection.org/works/{it['source']['id']}"
        owner, lic = "Wellcome Collection", loc.get("license", {}).get("id", "")
    else:
        url, page, owner, lic = ref, a.page or ref, a.owner or "", a.licence or ""
    tmp.write_bytes(fetch(url, binary=True))
    normalise(tmp, ASSETS / name, a.start, a.dur)
    tmp.unlink()
    log(name, page, owner, lic, a.notes or "")
    print(f"saved assets/{name} | {lic} | {owner[:50]} | {page}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "get"])
    ap.add_argument("source", choices=["commons", "nasa", "wellcome", "coverr", "openverse", "url"])
    ap.add_argument("ref")
    ap.add_argument("name", nargs="?")
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--audio", action="store_true")
    ap.add_argument("--start", type=float)
    ap.add_argument("--dur", type=float)
    ap.add_argument("--owner")
    ap.add_argument("--licence")
    ap.add_argument("--page")
    ap.add_argument("--notes")
    a = ap.parse_args()
    if a.cmd == "search":
        fn = {"commons": search_commons, "nasa": search_nasa, "wellcome": search_wellcome, "coverr": search_coverr,
              "openverse": search_openverse}[a.source]
        fn(a.ref, a.audio if a.source == "openverse" else a.video)
    else:
        get(a.source, a.ref, a.name, a)


if __name__ == "__main__":
    main()
