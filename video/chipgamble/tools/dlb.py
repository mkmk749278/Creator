import sys, json, urllib.request, urllib.parse, urllib.error, re, time, os
UA = {"User-Agent": "CreatorEpisodeBot/0.2 (https://github.com/mkmk749278/Creator; documentary research)"}
def get(url, raw=False, tries=12):
    for i in range(tries):
        try:
            x = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            return x if raw else json.loads(x)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503): raise
            w = min(30 * (i + 1), 120)
            print(f"  {e.code} wait {w}", flush=True); time.sleep(w)
        except Exception as e:
            print("  err", e, flush=True); time.sleep(20)
    return None
out, items = sys.argv[1], json.load(open(sys.argv[2]))
man_p = os.path.join(out, "manifest.json")
man = json.load(open(man_p)) if os.path.exists(man_p) else {}
todo = {k: v for k, v in items.items() if not (os.path.exists(os.path.join(out, k + ".jpg")) and os.path.getsize(os.path.join(out, k + ".jpg")) > 0)}
titles = list(todo.values())
meta = {}
for i in range(0, len(titles), 40):
    q = dict(action="query", titles="|".join(titles[i:i+40]), prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1920, format="json")
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q))
    norm = {n["to"]: n["from"] for n in d["query"].get("normalized", [])}
    for pg in d["query"]["pages"].values():
        if "imageinfo" not in pg: print("missing", pg.get("title")); continue
        meta[norm.get(pg["title"], pg["title"])] = pg["imageinfo"][0]
for k, title in todo.items():
    ii = meta.get(title)
    if not ii: print("no meta", k); continue
    m = ii["extmetadata"]
    url = ii.get("thumburl") or ii["url"]
    print("get", k, flush=True)
    data = get(url, raw=True)
    if not data: print("FAILED", k, flush=True); continue
    open(os.path.join(out, k + ".jpg"), "wb").write(data)
    man[k] = dict(title=title, page="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                  license=m.get("LicenseShortName", {}).get("value"), author=re.sub(r"<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip())
    json.dump(man, open(man_p, "w"), indent=1, ensure_ascii=False)
    time.sleep(8)
print("DONE", flush=True)
