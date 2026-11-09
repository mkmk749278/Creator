#!/usr/bin/env python3
"""Read the channel's audience stats from the YouTube Analytics API, to pick a publish slot and track growth.

Needs YT_CLIENT_ID, YT_CLIENT_SECRET and a refresh token with yt-analytics.readonly
(default YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE). Prints a plain report; --json OUT also saves the raw tables.

The Analytics API has no hour-of-day dimension (Studio's "When your viewers are on YouTube" is not in the API), so the
slot comes from: country mix (time zone), weekday pattern of views and watch time, device mix, and subscriber share.

Usage: scripts/yt_audience.py [--days 365] [--json out.json] [--token-env NAME]
"""
import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from collections import defaultdict


def access_token(env: str) -> str:
    d = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[env], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d, timeout=30))["access_token"]


def report(at: str, start: str, end: str, metrics: str, dims: str = "", sort: str = "", extra: dict | None = None):
    q = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": metrics}
    if dims:
        q["dimensions"] = dims
    if sort:
        q["sort"] = sort
    q.update(extra or {})
    url = "https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + at})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()[:300]}
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return {"cols": cols, "rows": r.get("rows", [])}


def show(title: str, t: dict, n: int = 15):
    print(f"\n## {title}")
    if "error" in t:
        print("  (error)", t["error"])
        return
    print("  " + " | ".join(t["cols"]))
    for row in t["rows"][:n]:
        print("  " + " | ".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in row))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--json")
    ap.add_argument("--token-env", default="YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE")
    a = ap.parse_args()
    at = access_token(a.token_env)
    end = dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=a.days)
    s, e = start.isoformat(), end.isoformat()
    out = {}
    out["totals"] = report(at, s, e, "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost")
    out["country"] = report(at, s, e, "views,estimatedMinutesWatched", "country", "-views", {"maxResults": 15})
    out["device"] = report(at, s, e, "views,estimatedMinutesWatched", "deviceType", "-views")
    out["subscribed"] = report(at, s, e, "views,estimatedMinutesWatched,averageViewDuration", "subscribedStatus")
    out["age_gender"] = report(at, s, e, "viewerPercentage", "ageGroup,gender")
    out["traffic"] = report(at, s, e, "views,estimatedMinutesWatched", "insightTrafficSourceType", "-views")
    out["videos"] = report(at, s, e, "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,"
                           "subscribersGained", "video", "-views", {"maxResults": 15})
    out["day"] = report(at, s, e, "views,estimatedMinutesWatched,subscribersGained", "day")
    for k in ["totals", "country", "device", "subscribed", "age_gender", "traffic", "videos"]:
        show(k, out[k])
    d = out["day"]
    if "rows" in d and d["rows"]:
        by = defaultdict(lambda: [0, 0, 0.0, 0])
        for day, v, m, sg in d["rows"]:
            w = dt.date.fromisoformat(day).strftime("%a")
            by[w][0] += v; by[w][1] += sg; by[w][2] += m; by[w][3] += 1
        print("\n## weekday (all days in range; share of views and watch minutes)")
        tv = sum(x[0] for x in by.values()) or 1
        tm = sum(x[2] for x in by.values()) or 1
        for w in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            v, sg, m, n = by[w]
            print(f"  {w}: views {v} ({100*v/tv:.1f}%), minutes {m:.0f} ({100*m/tm:.1f}%), subs +{sg}, days {n}")
        active = [r for r in d["rows"] if r[1] > 0]
        print(f"  days with views: {len(active)} of {len(d['rows'])}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
