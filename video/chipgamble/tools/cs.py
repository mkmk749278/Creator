import sys, json, urllib.request, urllib.parse, urllib.error, re, time
UA={"User-Agent":"CreatorEpisodeBot/0.1 (https://github.com/mkmk749278/Creator)"}
def api(p):
    p.update(format="json")
    r=urllib.request.Request("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p),headers=UA)
    for i in range(7):
        try: return json.load(urllib.request.urlopen(r,timeout=30))
        except urllib.error.HTTPError as e:
            if e.code!=429: raise
            w=int(e.headers.get("Retry-After") or 0) or 5*2**i
            print(f"  (429, wait {min(w,60)}s)",file=sys.stderr,flush=True); time.sleep(min(w,60))
    raise SystemExit("rate limited")
kind=sys.argv[1]
for q in sys.argv[2:]:
    print("==",q,flush=True)
    d=api(dict(action="query",generator="search",gsrsearch=f"{q} filetype:{kind}",gsrnamespace=6,gsrlimit=10,prop="imageinfo",iiprop="url|size|extmetadata|mime",iiurlwidth=1920))
    for p in (d.get("query",{}).get("pages",{}) or {}).values():
        ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
        lic=m.get("LicenseShortName",{}).get("value","?")
        art=re.sub("<[^>]+>","",m.get("Artist",{}).get("value","?")).strip()[:40]
        print(f"  {p['title'][5:95]} | {ii['width']}x{ii['height']} {ii.get('duration','')} | {lic} | {art}",flush=True)
    time.sleep(4)
