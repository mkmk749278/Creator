#!/usr/bin/env python3
"""Search YouTube from a cloud session with the channel's own API access (YouTube Data API v3, search.list = 100
quota units, videos.list = 1), and write a contact sheet of thumbnails per search so footage can be vetted before the
phone downloads it (termux_fetch_to_drive.sh). The container cannot download from YouTube; the API and the thumbnail
host answer. Needs YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE (environment).
usage: python3 scripts/yt_search.py OUT_DIR "search one" "search two" ... [--n 8]
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def token():
    d = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                "refresh_token": os.environ["YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE"],
                                "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d))["access_token"]


def api(tok, path, **q):
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/{path}?{urllib.parse.urlencode(q)}",
                                 headers={"Authorization": "Bearer " + tok})
    return json.load(urllib.request.urlopen(req))


def main():
    args = [a for a in sys.argv[1:]]
    n = 8
    if "--n" in args:
        i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
    out = Path(args[0]); out.mkdir(parents=True, exist_ok=True); tok = token(); rows = []
    for qi, q in enumerate(args[1:], 1):
        items = api(tok, "search", part="snippet", q=q, type="video", maxResults=n)["items"]
        ids = [it["id"]["videoId"] for it in items]
        dur = {v["id"]: v["contentDetails"]["duration"] for v in api(tok, "videos", part="contentDetails", id=",".join(ids))["items"]}
        tiles = []
        for k, it in enumerate(items, 1):
            vid, sn = it["id"]["videoId"], it["snippet"]
            f = out / f"q{qi:02d}_{k:02d}_{vid}.jpg"
            urllib.request.urlretrieve(sn["thumbnails"]["medium"]["url"], f)
            label = f"q{qi} #{k} {vid} {dur.get(vid, '')[2:]}".replace(":", r"\:")
            t = out / f"t_{f.name}"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf",
                            f"scale=320:180,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{label}':x=4:y=4:fontsize=13:fontcolor=yellow:box=1:boxcolor=black",
                            str(t)], check=True)
            tiles.append(t)
            rows.append({"q": q, "n": k, "id": vid, "title": sn["title"], "channel": sn["channelTitle"],
                         "published": sn["publishedAt"][:10], "duration": dur.get(vid, "")})
        inputs = sum([["-i", str(t)] for t in tiles], [])
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                        "".join(f"[{i}]" for i in range(len(tiles))) + f"xstack=inputs={len(tiles)}:layout=" +
                        "|".join(f"{(i % 4) * 320}_{(i // 4) * 180}" for i in range(len(tiles))), str(out / f"sheet_q{qi:02d}.jpg")], check=True)
        for t in tiles:
            t.unlink()
    (out / "results.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    for r in rows:
        print(f"q{args.index(r['q'])} #{r['n']} {r['id']} {r['duration']:>10} {r['published']} {r['channel'][:22]:22} | {r['title'][:70]}")


if __name__ == "__main__":
    main()
