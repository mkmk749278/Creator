#!/usr/bin/env python3
"""Search Openverse (Flickr, Commons and other CC sources) and contact-sheet the candidates before downloading anything.

Usage: python scripts/candidates.py OUT_DIR "query" [--n 20] [--min-width 2400] [--source flickr,wikimedia]

Only licences we may use commercially and modify (CC0, PDM, CC BY, CC BY-SA; PLAYBOOK §11.3). Writes
OUT_DIR/<slug>.jpg (numbered thumbnails with size and licence) and OUT_DIR/<slug>.json (id, title, creator, licence,
page URL, original URL, size) so a pick can be fetched at full size with `--get N`. Thumbnails come from Openverse's
own thumb endpoint, which does not count against Commons' rate limit.
  python scripts/candidates.py OUT "query" --get 3,7 --to films/<slug>/assets/media/raw/ov
"""
import argparse
import io
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import requests
from PIL import Image, ImageDraw

API = 'https://api.openverse.org/v1/images/'
UA = {'User-Agent': 'BuiltOnBharatDocBot/0.1 (https://github.com/mkmk749278/Built-on-Bharat; documentary research)'}
OK = {'cc0', 'pdm', 'by', 'by-sa'}


def slug(q: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')[:60]


def search(q: str, n: int, min_w: int, sources: str | None) -> list[dict]:
    out: list[dict] = []
    page = 1
    while len(out) < n and page <= 6:
        params = {'q': q, 'license': 'cc0,pdm,by,by-sa', 'page_size': 20, 'page': page, 'mature': 'false'}
        if sources:
            params['source'] = sources
        r = requests.get(API, params=params, headers=UA, timeout=40)
        r.raise_for_status()
        res = r.json().get('results', [])
        if not res:
            break
        for x in res:
            if x.get('license') not in OK or (x.get('width') or 0) < min_w:
                continue
            out.append({k: x.get(k) for k in ('id', 'title', 'creator', 'license', 'license_version', 'foreign_landing_url', 'url', 'width', 'height', 'source', 'thumbnail', 'attribution')})
            if len(out) >= n:
                break
        page += 1
    return out


COMMONS = 'https://commons.wikimedia.org/w/api.php'
CC_OK = re.compile(r'^(public domain|pd|cc0|cc[- ]by(-sa)?([- ][0-9.]+)?( [a-z]+)?|godl-india)$', re.I)


def commons(q: str, n: int, min_w: int) -> list[dict]:
    """Commons file search through the website's own search page (the API answered 429 for this IP on 2026-10-28
    while the website kept serving). The licence is read from the File: page only for picks (`--get`)."""
    url = 'https://commons.wikimedia.org/w/index.php?' + urllib.parse.urlencode({'search': f'{q} filetype:bitmap', 'ns6': 1, 'fulltext': 1, 'limit': 100})
    page = requests.get(url, headers=UA, timeout=60).text
    out: list[dict] = []
    for m in re.finditer(r'<li class="mw-search-result mw-search-result-ns-6">.*?href="/wiki/(File:[^"]+)".*?src="([^"]+)".*?data-file-width="(\d+)" data-file-height="(\d+)"', page, re.S):
        title, thumb, w, h = urllib.parse.unquote(m.group(1)), html_unescape(m.group(2)), int(m.group(3)), int(m.group(4))
        if w < min_w:
            continue
        out.append({'id': title, 'title': title[5:].replace('_', ' '), 'creator': '', 'license': '?', 'license_version': '',
                    'foreign_landing_url': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title), 'url': None,
                    'width': w, 'height': h, 'source': 'commons', 'thumbnail': thumb, 'attribution': ''})
        if len(out) >= n:
            break
    return out


def html_unescape(s: str) -> str:
    import html
    return html.unescape(s)


def commons_file(title: str) -> dict:
    """Licence, author and original URL from a File: page (licensetpl spans), as commons_html_fetch.py does."""
    import html
    p = requests.get('https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title), headers=UA, timeout=60).text
    lic = re.search(r'class="licensetpl(?:_|&#95;)short[^"]*"[^>]*>(.*?)</span>', p, re.S)
    lic = re.sub(r'<[^>]+>', '', html.unescape(lic.group(1))).strip() if lic else ''
    au = re.search(r'id="fileinfotpl(?:_|&#95;)aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', p, re.S) or re.search(r'class="licensetpl(?:_|&#95;)attr"[^>]*>(.*?)</span>', p, re.S)
    au = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(au.group(1)))).strip() if au else ''
    orig = re.search(r'href="(https://upload\.wikimedia\.org/wikipedia/commons/[0-9a-f]/[0-9a-f]{2}/[^"?]+)\?[^"]*utm_content=original"', p)
    return {'license': lic, 'creator': au[:200], 'url': orig.group(1) if orig else None}


def commons_api(q: str, n: int, min_w: int) -> list[dict]:
    """Commons file search via the API (kept for when it answers). Licence from extmetadata."""
    params = {
        'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': f'{q} filetype:bitmap', 'gsrnamespace': 6,
        'gsrlimit': 50, 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 330,
    }
    r = requests.get(COMMONS, params=params, headers=UA, timeout=60)
    r.raise_for_status()
    pages = sorted(r.json().get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 0))
    out: list[dict] = []
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]
        md = ii.get('extmetadata', {})
        lic = re.sub(r'<[^>]+>', '', md.get('LicenseShortName', {}).get('value', '')).strip()
        if not CC_OK.match(lic) or ii.get('width', 0) < min_w:
            continue
        artist = re.sub(r'<[^>]+>', '', md.get('Artist', {}).get('value', '')).strip()
        out.append({
            'id': p['title'], 'title': p['title'][5:], 'creator': artist, 'license': lic, 'license_version': '',
            'foreign_landing_url': ii.get('descriptionurl'), 'url': ii.get('url'), 'width': ii.get('width'), 'height': ii.get('height'),
            'source': 'commons', 'thumbnail': ii.get('thumburl'),
            'attribution': f"{p['title'][5:]} by {artist or 'unknown'}, {lic}, via Wikimedia Commons",
            'date': re.sub(r'<[^>]+>', '', md.get('DateTimeOriginal', {}).get('value', ''))[:40],
        })
        if len(out) >= n:
            break
    return out


def sheet(items: list[dict], path: Path) -> None:
    C, tw, th = 5, 360, 240
    R = (len(items) + C - 1) // C
    im = Image.new('RGB', (C * tw, max(1, R) * (th + 30)), 'black')
    d = ImageDraw.Draw(im)
    for i, it in enumerate(items):
        x, y = (i % C) * tw, (i // C) * (th + 30)
        try:
            for _ in range(4):
                rr = requests.get(it['thumbnail'], headers=UA, timeout=30)
                if rr.status_code != 429:
                    break
                time.sleep(45)  # Commons: back off, never burst
            t = Image.open(io.BytesIO(rr.content)).convert('RGB')
            t.thumbnail((tw - 4, th))
            im.paste(t, (x + 2, y + 30))
        except Exception as e:  # fail soft per source
            d.text((x + 4, y + 60), f'thumb failed {e}'[:40], fill='red')
        d.text((x + 4, y + 2), f"{i}  {it['width']}x{it['height']}  {it['license']} {it['source']}", fill='yellow')
        d.text((x + 4, y + 15), (it['title'] or '')[:48], fill='white')
        time.sleep(4 if it['source'] == 'commons' else 0.2)
    im.save(path, quality=85)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('query')
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--min-width', type=int, default=2400)
    ap.add_argument('--source')
    ap.add_argument('--get')
    ap.add_argument('--to')
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    js = out / f'{slug(a.query)}.json'
    if a.get:
        items = json.loads(js.read_text())
        to = Path(a.to)
        to.mkdir(parents=True, exist_ok=True)
        for k in a.get.split(','):
            it = items[int(k)]
            if it['source'] == 'commons':
                it.update(commons_file(it['id']))
                if not CC_OK.match(it['license'] or '') or not it['url']:
                    print('SKIP (licence not usable or no original):', it['title'], it['license'])
                    continue
                it['attribution'] = f"{it['title']} by {it['creator'] or 'unknown'}, {it['license']}, via Wikimedia Commons"
            ext =Path(urllib.parse.urlparse(it['url']).path).suffix.lower() or '.jpg'
            dest = to / (f"cm_{slug(it['title'])[:40]}{ext}" if it['source'] == 'commons' else f"ov_{it['id'][:8]}{ext}")
            urls = [it['url']]
            if it['source'] == 'commons':
                # Originals on upload.wikimedia.org answer 429 for long stretches; standard-width thumbnails on
                # thumb.wikimedia.org keep serving (2026-10-28). Largest standard width not above the original.
                path = urllib.parse.urlparse(it['url']).path.replace('/wikipedia/commons/', '/wikipedia/commons/thumb/')
                name = path.rsplit('/', 1)[1]
                urls = [f'https://thumb.wikimedia.org{path}/{w}px-{name}' for w in (3840, 1920, 1280) if w <= it['width']] + urls
            for u in urls:
                if subprocess.run(['curl', '-sSfL', '-m', '300', '-A', UA['User-Agent'], '-o', str(dest), u]).returncode == 0:
                    print('  from', u)
                    break
            else:
                print('FAILED', it['title'])
                continue
            print(dest, it['width'], it['height'], it['license'], it['license_version'], it['foreign_landing_url'])
            with open(to / 'manifest.jsonl', 'a') as mf:  # for media_manifest.csv rows (licence and credit per file)
                mf.write(json.dumps({'file': dest.name, **{k: it.get(k) for k in ('title', 'creator', 'license', 'license_version', 'foreign_landing_url', 'url', 'width', 'height', 'attribution')}}) + '\n')
            print('  credit:', it['attribution'])
            time.sleep(3)
        return
    items = commons(a.query, a.n, a.min_width) if a.source == 'commons' else search(a.query, a.n, a.min_width, a.source)
    js.write_text(json.dumps(items, indent=1))
    sheet(items, out / f'{slug(a.query)}.jpg')
    print(f'{len(items)} candidates -> {out / slug(a.query)}.jpg')


if __name__ == '__main__':
    sys.exit(main())
