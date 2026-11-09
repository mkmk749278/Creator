#!/usr/bin/env python3
"""Upload a finished film to YouTube from projects/<slug>/youtube/metadata.json, scheduled public (PLAYBOOK §15.1).

Steps (each can be run alone with --only): upload (resumable, private with publishAt, altered/synthetic = yes),
thumb (main thumbnail), captions (our English SRT), playlist (needs metadata "playlist_id"), comment (pinned-source
comment text is printed; the API cannot pin, so pinning stays a Studio tap).
Writes the video id back into metadata.json ("video_id"). Needs YT_CLIENT_ID, YT_CLIENT_SECRET and
YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE (youtube.force-ssl).

Usage: scripts/yt_upload.py projects/<slug> --video FILE --thumb FILE --srt FILE [--only upload,thumb,captions,playlist]
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

API = "https://www.googleapis.com"


def token() -> str:
    d = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d, timeout=30))["access_token"]


def call(method, url, at, body=None, headers=None, raw=False, timeout=120):
    h = {"Authorization": "Bearer " + at}
    h.update(headers or {})
    data = body
    if isinstance(body, (dict, list)):
        data = json.dumps(body).encode()
        h.setdefault("Content-Type", "application/json; charset=UTF-8")
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r if raw else json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        if raw and e.code == 308:
            return e
        sys.exit(f"{method} {url.split('?')[0]} -> {e.code}: {e.read().decode()[:600]}")


def upload(meta, video: Path, at: str) -> str:
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"], "tags": meta.get("tags", []),
                    "categoryId": str(meta.get("category_id", 28)), "defaultLanguage": "en",
                    "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": "private", "publishAt": meta["publish_at_utc"], "selfDeclaredMadeForKids": False,
                   "embeddable": True, "license": "youtube",
                   "containsSyntheticMedia": meta.get("altered_or_synthetic") == "Yes"},
    }
    size = video.stat().st_size
    url = f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status&notifySubscribers=true"
    r = call("POST", url, at, body, {"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)},
             raw=True)
    loc = r.headers["Location"]
    chunk = 64 * 1024 * 1024
    off = 0
    with open(video, "rb") as f:
        while off < size:
            f.seek(off)
            buf = f.read(chunk)
            end = off + len(buf) - 1
            for attempt in range(6):
                try:
                    req = urllib.request.Request(loc, data=buf, method="PUT", headers={
                        "Authorization": "Bearer " + at, "Content-Length": str(len(buf)),
                        "Content-Range": f"bytes {off}-{end}/{size}"})
                    with urllib.request.urlopen(req, timeout=600) as resp:
                        res = json.loads(resp.read())
                        print(f"uploaded {size} bytes: video {res['id']}", flush=True)
                        return res["id"]
                except urllib.error.HTTPError as e:
                    if e.code == 308:
                        rng = e.headers.get("Range")
                        off = int(rng.split("-")[1]) + 1 if rng else 0
                        print(f"  {off/size*100:.0f}%", flush=True)
                        break
                    if e.code in (500, 502, 503, 504) or e.code == 401:
                        if e.code == 401:
                            at = token()
                        time.sleep(2 ** attempt)
                        continue
                    sys.exit(f"upload chunk -> {e.code}: {e.read().decode()[:600]}")
                except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                    print("  retry:", e, flush=True)
                    time.sleep(2 ** attempt)
                    # ask the server where it stands
                    q = urllib.request.Request(loc, data=b"", method="PUT", headers={
                        "Authorization": "Bearer " + at, "Content-Range": f"bytes */{size}"})
                    try:
                        urllib.request.urlopen(q, timeout=60)
                    except urllib.error.HTTPError as e2:
                        if e2.code == 308:
                            rng = e2.headers.get("Range")
                            off = int(rng.split("-")[1]) + 1 if rng else 0
                            f.seek(off)
                            buf = f.read(chunk)
                            end = off + len(buf) - 1
            else:
                sys.exit("upload failed after retries")
    sys.exit("upload ended without a video id")


def multipart(at, url, meta_json: dict, file: Path, ctype: str):
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta_json)}\r\n"
            f"--{b}\r\nContent-Type: {ctype}\r\n\r\n").encode() + file.read_bytes() + f"\r\n--{b}--\r\n".encode()
    return call("POST", url, at, body, {"Content-Type": f"multipart/related; boundary={b}"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--video")
    ap.add_argument("--thumb")
    ap.add_argument("--srt")
    ap.add_argument("--only", default="upload,thumb,captions,playlist")
    a = ap.parse_args()
    mpath = Path(a.project) / "youtube" / "metadata.json"
    meta = json.loads(mpath.read_text())
    steps = a.only.split(",")
    at = token()
    vid = meta.get("video_id")
    if "upload" in steps:
        if vid:
            sys.exit(f"metadata already has video_id {vid}; refusing a second upload")
        vid = upload(meta, Path(a.video), at)
        meta["video_id"] = vid
        mpath.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        at = token()
        # videos.insert drops containsSyntheticMedia (seen 2026-11-09); videos.update keeps it.
        st = {"privacyStatus": "private", "publishAt": meta["publish_at_utc"], "license": "youtube",
              "embeddable": True, "publicStatsViewable": True, "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": meta.get("altered_or_synthetic") == "Yes"}
        r = call("PUT", f"{API}/youtube/v3/videos?part=status", at, {"id": vid, "status": st})
        print("altered or synthetic:", r["status"].get("containsSyntheticMedia"))
    if not vid:
        sys.exit("no video_id")
    if "thumb" in steps:
        b = Path(a.thumb).read_bytes()
        call("POST", f"{API}/upload/youtube/v3/thumbnails/set?videoId={vid}&uploadType=media", at, b,
             {"Content-Type": "image/jpeg"})
        print("thumbnail set:", a.thumb)
    if "captions" in steps:
        r = multipart(at, f"{API}/upload/youtube/v3/captions?part=snippet&uploadType=multipart",
                      {"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}},
                      Path(a.srt), "application/octet-stream")
        print("captions:", r.get("id"))
    if "playlist" in steps:
        pid = meta.get("playlist_id")
        if not pid:
            print("playlist: no playlist_id in metadata; skipped")
        else:
            call("POST", f"{API}/youtube/v3/playlistItems?part=snippet", at,
                 {"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
            print("added to playlist", pid)
    v = call("GET", f"{API}/youtube/v3/videos?part=status,snippet,processingDetails&id={vid}", at)
    it = v["items"][0]
    print(json.dumps({"id": vid, "title": it["snippet"]["title"], "status": it["status"],
                      "processing": it.get("processingDetails", {}).get("processingStatus")}, indent=1))


if __name__ == "__main__":
    main()
