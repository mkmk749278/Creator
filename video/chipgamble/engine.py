"""Scene engine for the chip-gamble documentary.

A part spec (parts/<id>.py) lists timed scenes keyed to spoken phrases. This
module turns it into a standalone HyperFrames project:
video/chipgamble/<id>/index.html (+ media/, vendor/ via npm postinstall).

Layers, back to front:
  bg     real photos / footage (one .wrap per scene, crossfaded)
  map    one shared Natural Earth world SVG per part, camera driven by GSAP
  ov     motion-graphics overlays (stats, dials, docs, cards, lower thirds)
  credit bottom-right attribution tag for whatever real media is on screen
"""
import json, math, os, random, re, shutil, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
W, Hh = 1920, 1080
XFADE = 0.45

PAL = dict(bg="#111317", panel="#1a1d23", amber="#F59E0B", red="#EF4444", ink="#F5F5F4",
           dim="#A8A29E", teal="#2DD4BF", land="#1f242c", edge="#323a46")

# ---------------------------------------------------------------- words / cues
class Cues:
    def __init__(self, words_json, offset):
        self.w = json.load(open(words_json))
        self.off = offset
        self.toks = [re.sub(r"[^a-z0-9%$]", "", x["w"].lower()) for x in self.w]

    def _find(self, phrase, after=0.0):
        pt = [re.sub(r"[^a-z0-9%$]", "", p.lower()) for p in phrase.split()]
        pt = [p for p in pt if p]
        for i in range(len(self.toks) - len(pt) + 1):
            if self.w[i]["s"] + self.off < after - 0.01:
                continue
            if all(self.toks[i + j] == pt[j] for j in range(len(pt))):
                return i, i + len(pt) - 1
        raise KeyError(f"cue not found: {phrase!r} after {after}")

    def at(self, phrase, after=0.0):
        i, _ = self._find(phrase, after)
        return round(self.w[i]["s"] + self.off, 2)

    def end(self, phrase, after=0.0):
        _, j = self._find(phrase, after)
        return round(self.w[j]["e"] + self.off, 2)

    @property
    def last(self):
        return self.w[-1]["e"] + self.off


_LEN = {}
def clip_len(src):
    if src not in _LEN:
        import subprocess
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              os.path.join(ROOT, "assets", src)], capture_output=True, text=True).stdout
        _LEN[src] = float(out.strip())
    return _LEN[src]


# ---------------------------------------------------------------- geo helpers
def merc(lon, lat, Wm=8000.0):
    lat = max(-80, min(84, lat))
    x = (lon + 180) / 360 * Wm
    y = (1 - math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) / math.pi) / 2 * Wm
    return x, y

PLACES = {
    "Bengaluru": (77.59, 12.97), "Hyderabad": (78.49, 17.39), "Noida": (77.39, 28.54),
    "Dallas": (-96.80, 32.78), "Hsinchu": (120.97, 24.80), "Tainan": (120.23, 23.0),
    "Pyeongtaek": (127.11, 36.99), "Kumamoto": (130.71, 32.80), "Tokyo": (139.69, 35.69),
    "Mohali": (76.72, 30.70), "Dholera": (72.19, 22.25), "Sanand": (72.38, 22.99),
    "Jagiroad": (92.20, 26.12), "Penang": (100.33, 5.41), "Mumbai": (72.88, 19.08),
    "Chennai": (80.27, 13.08), "Odesa": (30.73, 46.48), "Washington": (-77.04, 38.91),
    "Brussels": (4.35, 50.85), "Beijing": (116.41, 39.90), "Seoul": (126.98, 37.57),
    "Veldhoven": (5.40, 51.42), "Taipei": (121.56, 25.03), "Shanghai": (121.47, 31.23),
    "Singapore": (103.82, 1.35), "Delhi": (77.21, 28.61), "Ahmedabad": (72.57, 23.02),
    "Guwahati": (91.74, 26.14), "Kolkata": (88.36, 22.57), "Phoenix": (-112.07, 33.45),
}

def bbox_view(lon0, lat0, lon1, lat1):
    x0, y1 = merc(lon0, lat0); x1, y0 = merc(lon1, lat1)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = min(W / (x1 - x0), Hh / (y1 - y0))
    return dict(cx=round(cx, 1), cy=round(cy, 1), s=round(s, 4))

# ---------------------------------------------------------------- builder
class Part:
    def __init__(self, pid, title, kicker, voice_src, words_json, offset=2.2, tail=1.8):
        self.pid, self.title, self.kicker = pid, title, kicker
        self.voice_src = voice_src
        self.c = Cues(words_json, offset)
        self.offset = offset
        self.duration = round(self.c.last + tail, 2)
        self.bg = []        # background scenes
        self.ov = []        # overlay html blocks
        self.js = []        # timeline js lines
        self.css = []
        self.sfx = []       # (name, t, vol)
        self.credits = []   # (t0, t1, text)
        self.maps = []      # map scene specs
        self.media = set()  # files to copy into media/
        self.n = 0

    def uid(self, p="e"):
        self.n += 1
        return f"{p}{self.n}"

    # ------------------------------------------------------------ backgrounds
    def photo(self, t0, t1, src, credit=None, kb="in", focus="50% 50%", grade=None, fg=None, shade=0.0):
        self.bg.append(dict(kind="img", t0=t0, t1=t1, src=src, kb=kb, focus=focus, grade=grade, fg=fg, shade=shade))
        self.media.add(src)
        if fg: self.media.add(fg)
        if credit: self.credits.append((t0, t1, credit))

    def video(self, t0, t1, src, credit=None, kb="in", grade=None, shade=0.0, rate=None):
        if rate is None:  # stretch short clips into slow motion so they fill the scene
            need = t1 - t0 + XFADE + 0.15
            have = clip_len(src)
            if have < need:
                rate = round(max(have / need, 0.25), 3)
                if have / need < 0.3:
                    print(f"  ! {self.pid}: {src} ({have:.1f}s) stretched hard for {need:.1f}s scene at {t0}")
        self.bg.append(dict(kind="video", t0=t0, t1=t1, src=src, kb=kb, grade=grade, shade=shade, rate=rate))
        self.media.add(src)
        if credit: self.credits.append((t0, t1, credit))

    def mapscene(self, t0, t1, view_from, view_to, hi=(), pins=(), routes=(), dim_others=False, labels=(), credit="Map: Natural Earth (public domain)"):
        self.maps.append(dict(t0=t0, t1=t1, a=view_from, b=view_to, hi=list(hi), pins=list(pins), routes=list(routes), labels=list(labels)))
        self.bg.append(dict(kind="map", t0=t0, t1=t1))
        if credit: self.credits.append((t0, t1, credit))

    # ------------------------------------------------------------ overlays
    def section(self, t0, t1, inner, cls="", style=""):
        sid = self.uid("o")
        self.ov.append(f'<section id="{sid}" class="ov clip {cls}" data-start="{t0}" data-duration="{round(t1 - t0, 2)}" data-track-index="3" style="{style}">{inner}</section>')
        return sid

    def pop(self, sel, t, dur=0.45, y=26, extra=""):
        self.js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{dur},ease:"power3.out"{extra}}},{t});')

    def fade_out(self, sel, t, dur=0.3):
        self.js.append(f'tl.to("{sel}",{{opacity:0,duration:{dur}}},{t});')

    def actcard(self, t0, t1, kicker, title, sub=None):
        k = self.uid("k")
        inner = f'''<div class="ac-bg" id="{k}bg"></div>
<div class="ac-wrap"><div class="ac-k" id="{k}k">{kicker}</div><div class="ac-t" id="{k}t">{title}</div>
<div class="ac-rule" id="{k}r"></div>{f'<div class="ac-s" id="{k}s">{sub}</div>' if sub else ''}</div>'''
        self.section(t0, t1, inner, "actcard")
        self.js.append(f'tl.fromTo("#{k}bg",{{opacity:0}},{{opacity:0.82,duration:0.4}},{t0});')
        self.pop(f"#{k}k", t0 + 0.1)
        self.js.append(f'tl.fromTo("#{k}t",{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:0.7,ease:"expo.out"}},{t0 + 0.25});')
        self.js.append(f'tl.fromTo("#{k}r",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power3.out"}},{t0 + 0.5});')
        if sub: self.pop(f"#{k}s", t0 + 0.7)
        self.js.append(f'tl.to("#{k}bg,#{k}k,#{k}t,#{k}r{"," + "#" + k + "s" if sub else ""}",{{opacity:0,duration:0.4}},{t1 - 0.4});')
        self.sfx.append(("boom", t0 + 0.2, 0.5))

    def lower(self, t0, t1, eyebrow, text, pos="bl"):
        k = self.uid("l")
        inner = f'<div class="lt lt-{pos}" id="{k}"><div class="lt-e">{eyebrow}</div><div class="lt-t">{text}</div></div>'
        self.section(t0, t1, inner)
        self.js.append(f'tl.fromTo("#{k}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.5,ease:"power3.out"}},{t0 + 0.05});')
        self.fade_out(f"#{k}", t1 - 0.3)

    def kinetic(self, t0, t1, lines, pos="center", size=120, color_last=True, plate=False):
        """lines: list of (text, t) appear in sequence."""
        k = self.uid("kn")
        spans = []
        for i, (txt, t) in enumerate(lines):
            c = "amber" if (color_last and i == len(lines) - 1) else ""
            spans.append(f'<div class="kn-l {c}" id="{k}_{i}" style="font-size:{size}px">{txt}</div>')
        inner = f'<div class="kn kn-{pos} {"plate" if plate else ""}" id="{k}">{"".join(spans)}</div>'
        self.section(t0, t1, inner)
        for i, (txt, t) in enumerate(lines):
            self.js.append(f'tl.fromTo("#{k}_{i}",{{opacity:0,y:40,scale:1.04}},{{opacity:1,y:0,scale:1,duration:0.5,ease:"expo.out"}},{t});')
        self.fade_out(f"#{k}", t1 - 0.35)

    def stat(self, t0, t1, value, label, pos="left", count=None, prefix="", suffix="", color="amber", eyebrow=None, foot=None, decimals=0, boom=True, size=230):
        k = self.uid("st")
        start_txt = f"{prefix}{count[0]:,.{decimals}f}{suffix}" if count else value
        inner = f'''<div class="stat stat-{pos}" id="{k}">{f'<div class="st-e">{eyebrow}</div>' if eyebrow else ''}
<div class="st-n {color}" id="{k}n" style="font-size:{size}px">{start_txt}</div><div class="st-l">{label}</div>
{f'<div class="st-f">{foot}</div>' if foot else ''}</div>'''
        self.section(t0, t1, inner)
        self.js.append(f'tl.fromTo("#{k}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{t0});')
        if count:
            a, b, d = count
            self.js.append(f'(function(){{const el=document.getElementById("{k}n"),o={{v:{a}}};tl.fromTo(o,{{v:{a}}},{{v:{b},duration:{d},ease:"power2.out",onUpdate:()=>{{el.textContent="{prefix}"+o.v.toLocaleString("en-US",{{minimumFractionDigits:{decimals},maximumFractionDigits:{decimals}}})+"{suffix}"}}}},{t0 + 0.2});}})();')
        if boom: self.sfx.append(("boom", t0 + 0.1, 0.45))
        self.fade_out(f"#{k}", t1 - 0.35)

    def bars(self, t0, t1, title, rows, unit_note=None, maxv=None):
        """rows: (label, value, display, color, t)"""
        k = self.uid("br")
        maxv = maxv or max(r[1] for r in rows)
        rh = "".join(f'''<div class="br-row" id="{k}r{i}"><div class="br-l">{r[0]}</div>
<div class="br-track"><div class="br-bar {r[3]}" id="{k}b{i}" style="width:{max(1.2, 100 * r[1] / maxv):.1f}%"></div></div><div class="br-v {r[3]}">{r[2]}</div></div>''' for i, r in enumerate(rows))
        inner = f'<div class="bars" id="{k}"><div class="br-t">{title}</div>{rh}{f"<div class=br-n>{unit_note}</div>" if unit_note else ""}</div>'
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k} .br-t", t0)
        for i, r in enumerate(rows):
            self.pop(f"#{k}r{i}", r[4], 0.35, 16)
            self.js.append(f'tl.fromTo("#{k}b{i}",{{scaleX:0}},{{scaleX:1,duration:0.9,ease:"power3.out"}},{r[4] + 0.1});')
        if unit_note: self.pop(f"#{k} .br-n", rows[-1][4] + 0.5)
        self.fade_out(f"#{k}", t1 - 0.35)

    def dial(self, t0, t1, v0, v1, t_drop, label, sub):
        k = self.uid("dl")
        R = 300
        def arc(v):
            a = math.pi * (1 - v / 100)
            return R * math.cos(a), -R * math.sin(a)
        inner = f'''<div class="dial" id="{k}"><svg viewBox="-360 -340 720 400" width="900" height="500">
<path d="M -300 0 A 300 300 0 0 1 300 0" class="dl-track"/>
<path id="{k}a" d="M -300 0 A 300 300 0 0 1 300 0" class="dl-arc" pathLength="100" style="stroke-dasharray:100 100;stroke-dashoffset:{100 - v0}"/>
<line id="{k}nd" x1="0" y1="0" x2="0" y2="-250" class="dl-needle"/><circle r="18" class="dl-hub"/></svg>
<div class="dl-v" id="{k}v">{v0}%</div><div class="dl-l">{label}</div><div class="dl-s">{sub}</div></div>'''
        self.section(t0, t1, inner, "dimbg")
        self.js.append(f'tl.fromTo("#{k}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5}},{t0});')
        rot0, rot1 = -90 + 180 * v0 / 100, -90 + 180 * v1 / 100
        self.js.append(f'tl.fromTo("#{k}nd",{{rotation:-90,svgOrigin:"0 0"}},{{rotation:{rot0},svgOrigin:"0 0",duration:0.9,ease:"power2.out"}},{t0 + 0.2});')
        self.js.append(f'tl.fromTo("#{k}a",{{strokeDashoffset:100}},{{strokeDashoffset:{100 - v0},duration:0.9,ease:"power2.out"}},{t0 + 0.2});')
        self.js.append(f'tl.to("#{k}nd",{{rotation:{rot1},svgOrigin:"0 0",duration:1.4,ease:"power3.in"}},{t_drop});')
        self.js.append(f'tl.to("#{k}a",{{strokeDashoffset:{100 - v1},stroke:"{PAL["red"]}",duration:1.4,ease:"power3.in"}},{t_drop});')
        self.js.append(f'(function(){{const el=document.getElementById("{k}v"),o={{v:{v0}}};tl.fromTo(o,{{v:{v0}}},{{v:{v1},duration:1.4,ease:"power3.in",immediateRender:false,onUpdate:()=>{{el.textContent=Math.round(o.v)+"%"}}}},{t_drop});}})();')
        self.js.append(f'tl.to("#{k}v",{{color:"{PAL["red"]}",duration:0.4}},{t_drop + 1.0});')
        self.sfx.append(("boom", t_drop + 1.4, 0.55))
        self.fade_out(f"#{k}", t1 - 0.35)

    def nmscale(self, t0, t1, rows, title):
        """rows: (label, nm, t, color) on a log scale."""
        k = self.uid("nm")
        lo, hi = math.log10(1), math.log10(100000)
        rh = "".join(f'''<div class="nm-row" id="{k}r{i}"><div class="nm-l">{r[0]}</div><div class="nm-track"><div class="nm-bar {r[3]}" id="{k}b{i}" style="width:{100 * (math.log10(r[1]) - lo) / (hi - lo):.1f}%"></div></div>
<div class="nm-v {r[3]}">{r[1]:,} nm</div></div>''' for i, r in enumerate(rows))
        ticks = "".join(f'<div class="nm-tick" style="left:{100 * (e) / 5:.0f}%">{10 ** e:,}</div>' for e in range(0, 6))
        inner = f'<div class="nmscale" id="{k}"><div class="br-t">{title}</div>{rh}<div class="nm-axis">{ticks}</div><div class="br-n">Logarithmic scale · nanometres</div></div>'
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k} .br-t", t0)
        self.pop(f"#{k} .nm-axis", t0 + 0.2)
        for i, r in enumerate(rows):
            self.pop(f"#{k}r{i}", r[2], 0.35, 16)
            self.js.append(f'tl.fromTo("#{k}b{i}",{{scaleX:0}},{{scaleX:1,duration:0.9,ease:"power3.out"}},{r[2] + 0.1});')
        self.fade_out(f"#{k}", t1 - 0.35)

    def donut(self, t0, t1, pct, label, sub, t_fill=None):
        k = self.uid("dn")
        t_fill = t_fill or t0 + 0.3
        inner = f'''<div class="donut" id="{k}"><div class="dn-ring"><svg viewBox="-150 -150 300 300" width="560" height="560">
<circle r="110" class="dn-track"/><circle id="{k}c" r="110" class="dn-arc" pathLength="100" transform="rotate(-90)" style="stroke-dasharray:{pct} 100;stroke-dashoffset:{pct}"/></svg>
<div class="dn-v" id="{k}v">{pct}%</div></div><div class="dn-txt"><div class="dn-l">{label}</div><div class="dn-s">{sub}</div></div></div>'''
        self.section(t0, t1, inner, "dimbg")
        self.js.append(f'tl.fromTo("#{k}",{{opacity:0}},{{opacity:1,duration:0.4}},{t0});')
        self.js.append(f'tl.fromTo("#{k}c",{{strokeDashoffset:{pct}}},{{strokeDashoffset:0,duration:1.2,ease:"power2.out"}},{t_fill});')
        self.js.append(f'tl.fromTo("#{k}v",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(2)"}},{t_fill + 0.6});')
        self.sfx.append(("boom", t_fill + 0.6, 0.45))
        self.fade_out(f"#{k}", t1 - 0.35)

    def timeline(self, t0, t1, title, y0, y1, marks, now=None):
        """marks: (year, label, t, color, side)"""
        k = self.uid("tln")
        def x(y): return 100 * (y - y0) / (y1 - y0)
        mh = "".join(f'''<div class="tl-m {m[4]}" id="{k}m{i}" style="left:{x(m[0]):.2f}%"><div class="tl-dot {m[3]}"></div>
<div class="tl-y {m[3]}">{m[0]}</div><div class="tl-lb">{m[1]}</div></div>''' for i, m in enumerate(marks))
        inner = f'<div class="tline" id="{k}"><div class="br-t">{title}</div><div class="tl-axis"><div class="tl-line" id="{k}ln"></div>{mh}</div></div>'
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k} .br-t", t0)
        self.js.append(f'tl.fromTo("#{k}ln",{{scaleX:0}},{{scaleX:1,duration:1.0,ease:"power2.inOut"}},{t0 + 0.1});')
        for i, m in enumerate(marks):
            self.pop(f"#{k}m{i}", m[2], 0.4, 20 if m[4] == "up" else -20)
        self.fade_out(f"#{k}", t1 - 0.35)

    def versus(self, t0, t1, left, right, title=None):
        """left/right: (eyebrow, big, label, color, t)"""
        k = self.uid("vs")
        def card(c, i):
            return f'<div class="vs-c" id="{k}c{i}"><div class="st-e">{c[0]}</div><div class="vs-n {c[3]}">{c[1]}</div><div class="st-l">{c[2]}</div></div>'
        inner = f'<div class="versus" id="{k}">{f"<div class=br-t>{title}</div>" if title else ""}<div class="vs-row">{card(left, 0)}<div class="vs-x">vs</div>{card(right, 1)}</div></div>'
        self.section(t0, t1, inner, "dimbg")
        if title: self.pop(f"#{k} .br-t", t0)
        self.pop(f"#{k}c0", left[4]); self.pop(f"#{k}c1", right[4])
        self.js.append(f'tl.fromTo("#{k} .vs-x",{{opacity:0}},{{opacity:1,duration:0.3}},{right[4] - 0.2});')
        self.sfx.append(("boom", right[4] + 0.1, 0.4))
        self.fade_out(f"#{k}", t1 - 0.35)

    def particles(self, t0, t1, t_left, t_right):
        k = self.uid("pt")
        rnd = random.Random(7)
        def field(n, cls):
            return "".join(f'<i class="{cls}" style="left:{rnd.uniform(3, 97):.1f}%;top:{rnd.uniform(4, 96):.1f}%;width:{rnd.uniform(4, 10):.0f}px;height:{rnd.uniform(4, 10):.0f}px"></i>' for _ in range(n))
        inner = f'''<div class="ptc" id="{k}"><div class="pt-p" id="{k}a"><div class="pt-h">Hospital operating room</div><div class="pt-f">{field(420, "pd")}</div><div class="pt-c">Thousands of particles / m³</div></div>
<div class="pt-p good" id="{k}b"><div class="pt-h">Fab cleanroom · ISO Class 1</div><div class="pt-f">{field(8, "pd ok")}</div><div class="pt-c">Fewer than 10 particles / m³ (≥0.1 µm)</div></div></div>'''
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k}a", t_left); self.pop(f"#{k}b", t_right)
        self.js.append(f'tl.fromTo("#{k}a .pd",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.6,stagger:0.002}},{t_left + 0.2});')
        self.js.append(f'tl.fromTo("#{k}b .pd",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.5,stagger:0.08}},{t_right + 0.3});')
        self.fade_out(f"#{k}", t1 - 0.35)

    def waveform(self, t0, t1, t_dip, label):
        k = self.uid("wf")
        pts = []
        for i in range(0, 1601, 8):
            x = i
            y = 200 + 70 * math.sin(i / 1600 * math.pi * 2 * 9)
            pts.append(f"{x},{y:.1f}")
        dip = []
        for i in range(0, 1601, 8):
            x = i
            amp = 70 * (0.25 if 760 <= i <= 840 else 1)
            dip.append(f"{x},{200 + amp * math.sin(i / 1600 * math.pi * 2 * 9):.1f}")
        inner = f'''<div class="wave" id="{k}"><div class="br-t">Grid voltage at the fab</div><svg viewBox="0 0 1600 400" width="1600" height="400">
<polyline id="{k}a" points="{' '.join(pts)}" class="wf-ok"/><polyline id="{k}b" points="{' '.join(dip)}" class="wf-bad" style="opacity:0"/>
<rect id="{k}z" x="740" y="40" width="120" height="320" class="wf-zone" style="opacity:0"/></svg>
<div class="wf-l" id="{k}l">{label}</div></div>'''
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k}", t0)
        self.js.append(f'tl.fromTo("#{k}a",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.4,ease:"none"}},{t0 + 0.1});')
        self.js.append(f'tl.set("#{k}a",{{opacity:0}},{t_dip});tl.set("#{k}b",{{opacity:1}},{t_dip});')
        self.js.append(f'tl.fromTo("#{k}z",{{opacity:0}},{{opacity:1,duration:0.2,repeat:3,yoyo:true}},{t_dip});')
        self.pop(f"#{k}l", t_dip + 0.2)
        self.sfx.append(("snap", t_dip, 0.55))
        self.fade_out(f"#{k}", t1 - 0.35)

    def water(self, t0, t1, t_count, liters=40_000_000):
        k = self.uid("wt")
        inner = f'''<div class="water" id="{k}"><div class="wt-tank"><div class="wt-fill" id="{k}f"></div></div>
<div class="wt-txt"><div class="st-e">Ultrapure water, per fab, per day</div><div class="st-n teal" id="{k}n" style="font-size:170px">0 L</div>
<div class="st-l">Up to {liters // 1_000_000} million litres, stripped of every mineral, ion and microbe</div></div></div>'''
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k}", t0)
        self.js.append(f'tl.fromTo("#{k}f",{{scaleY:0}},{{scaleY:1,duration:2.2,ease:"power2.out"}},{t_count});')
        self.js.append(f'(function(){{const el=document.getElementById("{k}n"),o={{v:0}};tl.fromTo(o,{{v:0}},{{v:{liters},duration:2.2,ease:"power2.out",onUpdate:()=>{{el.textContent=Math.round(o.v).toLocaleString("en-US")+" L"}}}},{t_count});}})();')
        self.sfx.append(("boom", t_count + 2.0, 0.45))
        self.fade_out(f"#{k}", t1 - 0.35)

    def tracker(self, t0, t1, total_label, segs, title):
        """segs: (label, pct, color, t)"""
        k = self.uid("tk")
        sh = "".join(f'<div class="tk-seg {s[2]}" id="{k}s{i}" style="width:{s[1]}%"><span>{s[0]}</span></div>' for i, s in enumerate(segs))
        inner = f'<div class="tracker" id="{k}"><div class="br-t">{title}</div><div class="tk-total">{total_label}</div><div class="tk-bar">{sh}</div></div>'
        self.section(t0, t1, inner, "dimbg")
        self.pop(f"#{k} .br-t", t0); self.pop(f"#{k} .tk-total", t0 + 0.2)
        for i, s in enumerate(segs):
            self.js.append(f'tl.fromTo("#{k}s{i}",{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:0.7,ease:"power3.out"}},{s[3]});')
        self.fade_out(f"#{k}", t1 - 0.35)

    def doc(self, t0, t1, png, highlights, stamp=None, credit=None, tilt=(14, -8), width=1180, focus_box=0, zoom=1.7):
        """Real document page on a dark desk, 2.5D tilt, camera push, highlighter swipes, optional ink stamp.
        highlights: list of (box_index, t). stamp: (text, t, color)."""
        k = self.uid("dc")
        meta = json.load(open(os.path.join(ROOT, "assets", png.replace(".png", ".json"))))
        sc = width / meta["img_w"]
        ph = meta["img_h"] * sc
        self.media.add(png)
        hl = ""
        for bi, t in highlights:
            b = meta["boxes"][bi]
            hl += f'<div class="hl" id="{k}h{bi}" style="left:{b["x"] * sc:.0f}px;top:{b["y"] * sc:.0f}px;width:{b["w"] * sc:.0f}px;height:{b["h"] * sc:.0f}px"></div>'
        st = ""
        if stamp:
            st = f'<div class="stamp {stamp[2]}" id="{k}st">{stamp[0]}</div>'
        fb = meta["boxes"][focus_box]
        fx = (fb["x"] + fb["w"] / 2) * sc - width / 2
        fy = (fb["y"] + fb["h"] / 2) * sc - ph / 2
        inner = f'''<div class="desk"></div><div class="doccam" id="{k}cam"><div class="paper" id="{k}p" style="width:{width}px;height:{ph:.0f}px">
<img src="media/{png}" style="width:{width}px;height:{ph:.0f}px" alt="">{hl}{st}</div></div>'''
        self.section(t0, t1, inner, "docscene")
        rx, ry = tilt
        self.js.append(f'tl.fromTo("#{k}p",{{rotationX:{rx},rotationY:{ry},rotationZ:-2,y:420,opacity:0,transformPerspective:1600}},{{rotationX:{rx * 0.4:.1f},rotationY:{ry * 0.4:.1f},rotationZ:-1,y:0,opacity:1,duration:0.9,ease:"power3.out"}},{t0});')
        push_d = max(1.0, (highlights[0][1] if highlights else t0 + 2) - t0 + 0.6)
        self.js.append(f'tl.fromTo("#{k}cam",{{scale:0.92,x:0,y:{ph / 2 - 470:.0f}}},{{scale:{zoom},x:{-fx * zoom:.0f},y:{-fy * zoom:.0f},duration:{push_d:.2f},ease:"power2.inOut"}},{t0 + 0.3});')
        drift_t = t0 + 0.3 + push_d
        if t1 - drift_t > 0.4:
            self.js.append(f'tl.to("#{k}cam",{{scale:{zoom * 1.05:.2f},duration:{t1 - drift_t:.2f},ease:"none"}},{drift_t:.2f});')
        for bi, t in highlights:
            self.js.append(f'tl.fromTo("#{k}h{bi}",{{scaleX:0}},{{scaleX:1,duration:0.55,ease:"power2.inOut"}},{t});')
            self.sfx.append(("marker", t, 0.5))
        if stamp:
            self.js.append(f'tl.fromTo("#{k}st",{{opacity:0,scale:2.6,rotation:-18}},{{opacity:0.92,scale:1,rotation:-11,duration:0.22,ease:"power4.in"}},{stamp[1]});')
            self.sfx.append(("stamp", stamp[1] + 0.2, 0.7))
        self.sfx.append(("paper", t0, 0.6))
        if credit: self.credits.append((t0, t1, credit))

    def cutline(self, t0, t1, text, t_show=None):
        """Small factual caption top-left (e.g. 'Illustrative', dates)."""
        k = self.uid("cl")
        self.section(t0, t1, f'<div class="cutline" id="{k}">{text}</div>')
        self.pop(f"#{k}", t_show or t0 + 0.2, 0.4, 10)

    def fire(self, t0, t1, intensity=1.0):
        """Illustrative heat + rising embers (deterministic), laid over a real photo."""
        k = self.uid("fi")
        rnd = random.Random(1989)
        embers = []
        for i in range(int(70 * intensity)):
            x = rnd.uniform(0, 100); s = rnd.uniform(3, 9); d = rnd.uniform(2.2, 4.5); dl = rnd.uniform(0, t1 - t0)
            embers.append((i, x, s, d, dl))
        eh = "".join(f'<i class="em" id="{k}e{i}" style="left:{x:.1f}%;width:{s:.0f}px;height:{s:.0f}px"></i>' for i, x, s, d, dl in embers)
        inner = f'<div class="heat" id="{k}h"></div><div class="glow" id="{k}g"></div>{eh}'
        self.section(t0, t1, inner, "fire")
        self.js.append(f'tl.fromTo("#{k}h",{{opacity:0}},{{opacity:{0.75 * intensity:.2f},duration:1.2}},{t0});')
        self.js.append(f'tl.fromTo("#{k}g",{{opacity:0.35}},{{opacity:0.8,duration:0.35,repeat:{int((t1 - t0) / 0.7)},yoyo:true,ease:"sine.inOut"}},{t0});')
        for i, x, s, d, dl in embers:
            st = t0 + (dl % max(0.5, (t1 - t0 - d)))
            self.js.append(f'tl.fromTo("#{k}e{i}",{{y:0,x:0,opacity:0}},{{y:-{rnd.uniform(500, 1100):.0f},x:{rnd.uniform(-120, 120):.0f},opacity:1,duration:{d:.2f},ease:"none"}},{st:.2f});tl.to("#{k}e{i}",{{opacity:0,duration:0.6}},{st + d - 0.6:.2f});')
        self.sfx.append(("boom", t0 + 0.1, 0.55))

    def checklist(self, t0, t1, items, pos="left", size=66, mark="✗", color="red"):
        """items: (text, t) — each line gets a coloured mark."""
        lines = [(f'<span class="{color}">{mark}</span> {txt}', t) for txt, t in items]
        self.kinetic(t0, t1, lines, pos=pos, size=size, color_last=False, plate=True)

    def sfx_at(self, name, t, vol=0.4):
        self.sfx.append((name, t, vol))

    # ------------------------------------------------------------ output
    def build(self):
        pdir = os.path.join(ROOT, self.pid)
        os.makedirs(os.path.join(pdir, "media"), exist_ok=True)
        for f in sorted(self.media):
            srcp = os.path.join(ROOT, "assets", f)
            if not os.path.exists(srcp):
                if os.environ.get("CG_STUB") and f.endswith(".jpg"):
                    print("  stub:", f); srcp = os.path.join(ROOT, "assets", "mcu_die.jpg")
                else:
                    raise FileNotFoundError(srcp)
            dst = os.path.join(pdir, "media", f)
            if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(srcp):
                shutil.copy2(srcp, dst)
        shutil.copy2(os.path.join(ROOT, "shared", "world.js"), os.path.join(pdir, "world.js"))
        shutil.copy2(os.path.join(ROOT, "shared", "theme.css"), os.path.join(pdir, "theme.css"))
        sfxdir = os.path.join(ROOT, "shared", "sfx")
        os.makedirs(os.path.join(pdir, "sfx"), exist_ok=True)
        for f in os.listdir(sfxdir):
            shutil.copy2(os.path.join(sfxdir, f), os.path.join(pdir, "sfx", f))
        shutil.copy2(self.voice_src, os.path.join(pdir, "voice.mp3"))

        bg_html, js_bg = [], []
        for i, b in enumerate(self.bg):
            if b["kind"] == "map":
                continue
            wid, mid = f"w{i}", f"m{i}"
            t0 = b["t0"]; dur = round(b["t1"] - t0 + XFADE, 2)
            grade = {"warm": "sepia(0.25) saturate(1.1)", "cold": "saturate(0.7) hue-rotate(-8deg) brightness(0.9)",
                     "bw": "grayscale(1) contrast(1.1)", "archival": "grayscale(0.85) sepia(0.35) contrast(1.05)"}.get(b.get("grade"), "")
            style = f'filter:{grade};' if grade else ""
            fgh = ""
            if b["kind"] == "img":
                media = f'<img id="{mid}" class="clip" src="media/{b["src"]}" style="object-position:{b["focus"]}" data-start="{t0}" data-duration="{dur}" data-track-index="{i % 2}" alt="">'
                if b.get("fg"):
                    fgh = f'<img id="{mid}fg" class="clip fg" src="media/{b["fg"]}" style="object-position:{b["focus"]}" data-start="{t0}" data-duration="{dur}" data-track-index="2" alt="">'
            else:
                rate = f' data-playback-rate="{b["rate"]}"' if b.get("rate") else ""
                media = f'<video id="{mid}" class="clip" src="media/{b["src"]}" muted playsinline data-start="{t0}" data-duration="{dur}" data-track-index="{i % 2}"{rate}></video>'
            shade = f'<div class="shade" style="opacity:{b["shade"]}"></div>' if b.get("shade") else ""
            bg_html.append(f'<div class="wrap" id="{wid}" style="{style}"><div class="kb" id="{wid}k">{media}</div>{f"<div class=kb id={wid}f>{fgh}</div>" if fgh else ""}{shade}</div>')
            d = b["t1"] - t0 + XFADE
            kb = b.get("kb", "in")
            fr, to = {"in": ("scale:1.0", "scale:1.12"), "out": ("scale:1.14", "scale:1.0"),
                      "left": ("scale:1.12,x:50", "scale:1.12,x:-50"), "right": ("scale:1.12,x:-50", "scale:1.12,x:50"),
                      "up": ("scale:1.12,y:40", "scale:1.12,y:-40"), "none": ("scale:1.0", "scale:1.0")}[kb]
            js_bg.append(f'tl.fromTo("#{wid}k",{{{fr}}},{{{to},duration:{d:.2f},ease:"none"}},{t0});')
            if fgh:  # 2.5D: subject layer moves more than the plate
                js_bg.append(f'tl.fromTo("#{wid}f",{{scale:1.04,x:-30}},{{scale:1.2,x:30,duration:{d:.2f},ease:"none"}},{t0});')
            if i > 0:
                js_bg.append(f'tl.fromTo("#{wid}",{{opacity:0}},{{opacity:1,duration:{XFADE},ease:"none"}},{t0});')

        # ---- maps: one SVG world, camera + per-scene layers
        map_html, js_map = "", []
        if self.maps:
            layers = []
            for mi, m in enumerate(self.maps):
                g = []
                s_end = m["b"]["s"]
                for iso, color, t in m["hi"]:
                    g.append(f'<path class="hi" id="mp{mi}_{iso}" data-iso="{iso}" fill="{color}" style="opacity:0"/>')
                    js_map.append(f'tl.fromTo("#mp{mi}_{iso}",{{opacity:0}},{{opacity:1,duration:0.6}},{t});')
                for ri, r in enumerate(m["routes"]):
                    (a, bname, t, color) = r[:4]
                    dur = r[4] if len(r) > 4 else 1.4
                    ax, ay = merc(*PLACES[a]); bx, by = merc(*PLACES[bname])
                    mx, my = (ax + bx) / 2, (ay + by) / 2
                    dx, dy = bx - ax, by - ay
                    ln = math.hypot(dx, dy)
                    cx_, cy_ = mx - dy * 0.25, my + dx * 0.25 * (-1)
                    cy_ = min(cy_, my - ln * 0.18)
                    pid = f"mr{mi}_{ri}"
                    g.append(f'<path id="{pid}" class="route" d="M{ax:.0f} {ay:.0f} Q{cx_:.0f} {cy_:.0f} {bx:.0f} {by:.0f}" pathLength="1" stroke="{color}" style="stroke-dasharray:1 1;stroke-dashoffset:1"/>')
                    g.append(f'<circle id="{pid}d" r="{9 / s_end:.2f}" fill="{color}" style="opacity:0" class="pkt"/>')
                    js_map.append(f'tl.fromTo("#{pid}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{t});')
                    js_map.append(f'(function(){{const c=document.getElementById("{pid}d"),o={{u:0}};tl.fromTo(o,{{u:0}},{{u:1,duration:{dur},ease:"power2.inOut",onUpdate:()=>{{const u=o.u,v=1-u;c.setAttribute("cx",v*v*{ax:.0f}+2*v*u*{cx_:.0f}+u*u*{bx:.0f});c.setAttribute("cy",v*v*{ay:.0f}+2*v*u*{cy_:.0f}+u*u*{by:.0f});}}}},{t});tl.fromTo(c,{{opacity:0}},{{opacity:1,duration:0.2}},{t});tl.to(c,{{opacity:0,duration:0.3}},{t + dur});}})();')
                for pi_, p in enumerate(m["pins"]):
                    name, t = p[0], p[1]
                    label = p[2] if len(p) > 2 else name
                    side = p[3] if len(p) > 3 else "r"
                    color = p[4] if len(p) > 4 else PAL["amber"]
                    x, y = merc(*PLACES[name])
                    fs = 36 / s_end
                    off = 18 / s_end
                    tx = x + off if side == "r" else x - off
                    anchor = "start" if side == "r" else "end"
                    pid = f"mp{mi}p{pi_}"
                    g.append(f'<g id="{pid}" style="opacity:0"><circle cx="{x:.1f}" cy="{y:.1f}" r="{30 / s_end:.2f}" class="pin-ring" id="{pid}r"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{8 / s_end:.2f}" fill="{color}"/>'
                             f'<text x="{tx:.1f}" y="{y + fs * 0.35:.1f}" font-size="{fs:.2f}" text-anchor="{anchor}" class="pin-t" style="stroke-width:{6 / s_end:.2f}px">{H.escape(label)}</text></g>')
                    js_map.append(f'tl.fromTo("#{pid}",{{opacity:0}},{{opacity:1,duration:0.35}},{t});')
                    js_map.append(f'tl.fromTo("#{pid}r",{{attr:{{r:{4 / s_end:.2f}}},opacity:1}},{{attr:{{r:{60 / s_end:.2f}}},opacity:0,duration:1.0,ease:"power1.out"}},{t});')
                for li, lb in enumerate(m["labels"]):
                    text, lon, lat, t = lb[:4]
                    size = lb[4] if len(lb) > 4 else 34
                    x, y = merc(lon, lat)
                    g.append(f'<text id="mp{mi}l{li}" x="{x:.1f}" y="{y:.1f}" font-size="{size / s_end:.2f}" text-anchor="middle" class="map-l" style="opacity:0;stroke-width:{6 / s_end:.2f}px">{H.escape(text)}</text>')
                    js_map.append(f'tl.fromTo("#mp{mi}l{li}",{{opacity:0}},{{opacity:1,duration:0.5}},{t});')
                layers.append(f'<g id="ml{mi}" style="opacity:0">{"".join(g)}</g>')
                # visibility of this scene's layer + map layer
                js_map.append(f'tl.set("#ml{mi}",{{opacity:1}},{m["t0"]});tl.set("#ml{mi}",{{opacity:0}},{m["t1"] + XFADE});')
                js_map.append(f'tl.fromTo("#maplayer",{{opacity:0}},{{opacity:1,duration:{XFADE},immediateRender:false}},{m["t0"]});')
                js_map.append(f'tl.to("#maplayer",{{opacity:0,duration:{XFADE}}},{m["t1"] + 0.01});')
                a, b = m["a"], m["b"]
                js_map.append(f'tl.fromTo(CAM,{{cx:{a["cx"]},cy:{a["cy"]},s:{a["s"]}}},{{cx:{b["cx"]},cy:{b["cy"]},s:{b["s"]},duration:{max(0.5, m["t1"] - m["t0"]):.2f},ease:"power2.inOut",immediateRender:false,onUpdate:camUpd}},{m["t0"]});')
            map_html = f'''<div id="maplayer" style="opacity:0"><div class="map-bg"></div><svg id="mapsvg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}">
<g id="cam"><g id="land"></g><g id="hil"></g>{"".join(layers)}</g></svg><div class="map-grain"></div></div>'''

        # ---- credits (dedupe consecutive identical)
        cr_html, js_cr = [], []
        merged = []
        for c in sorted(self.credits):
            if merged and merged[-1][2] == c[2] and c[0] - merged[-1][1] < 0.6:
                merged[-1] = (merged[-1][0], max(merged[-1][1], c[1]), c[2])
            else:
                merged.append(c)
        for i, (t0, t1, text) in enumerate(merged):
            cr_html.append(f'<div class="credit clip" id="cr{i}" data-start="{t0}" data-duration="{round(t1 - t0, 2)}" data-track-index="5">{text}</div>')

        # ---- audio
        import subprocess
        vlen = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", self.voice_src],
                                    capture_output=True, text=True).stdout)
        aud = [f'<audio id="vo" src="voice.mp3" data-start="{self.offset}" data-duration="{min(round(vlen - 0.02, 2), round(self.duration - self.offset, 2))}" data-track-index="10" data-volume="1"></audio>',
               f'<audio id="bed" src="sfx/drone.mp3" data-start="0" data-duration="{self.duration}" data-track-index="11" data-volume="0.13"></audio>']
        lens = {"boom": 1.6, "whoosh": 0.9, "stamp": 0.5, "snap": 0.4, "paper": 0.7, "marker": 0.6}
        lanes = {}
        for j, (name, t, vol) in enumerate(sorted(self.sfx, key=lambda x: x[1])):
            if t < 0 or t > self.duration - 0.2: continue
            lane = 12
            while lanes.get(lane, -9) > t: lane += 1
            lanes[lane] = t + lens[name]
            d = min(lens[name], self.duration - t)
            aud.append(f'<audio id="sx{j}" src="sfx/{name}.wav" data-start="{round(t, 2)}" data-duration="{round(d, 2)}" data-track-index="{lane}" data-volume="{vol}"></audio>')

        html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
<title>Chip gamble: {self.pid}</title>
<script src="vendor/gsap.min.js"></script>
<script src="world.js"></script>
<link rel="stylesheet" href="theme.css" />
<style>
@font-face {{ font-family: "Inter"; font-weight: 400; src: url("vendor/fonts/inter-latin-400-normal.woff2") format("woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }}
{"".join(self.css)}
</style>
</head>
<body>
<div id="root" data-composition-id="{self.pid}" data-start="0" data-width="1920" data-height="1080" data-duration="{self.duration}">
<div class="base"></div>
{chr(10).join(bg_html)}
{map_html}
{chr(10).join(self.ov)}
{chr(10).join(cr_html)}
<div class="vignette"></div>
{chr(10).join(aud)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{"" if not self.maps else """
const WD = window.WORLD;
const land = document.getElementById("land");
let s = "";
for (const iso in WD.paths) s += '<path class="cty" d="' + WD.paths[iso] + '"/>';
land.innerHTML = s;
document.querySelectorAll("path.hi").forEach(p => p.setAttribute("d", WD.paths[p.dataset.iso] || ""));
const camG = document.getElementById("cam");
const CAM = { cx: 4000, cy: 3000, s: 0.3 };
function camUpd() { camG.setAttribute("transform", "translate(960 540) scale(" + CAM.s + ") translate(" + (-CAM.cx) + " " + (-CAM.cy) + ")"); }
camUpd();
""" + f'tl.set(CAM,{{cx:{self.maps[0]["a"]["cx"]},cy:{self.maps[0]["a"]["cy"]},s:{self.maps[0]["a"]["s"]},onUpdate:camUpd}},0);'}
{chr(10).join(js_bg)}
{chr(10).join(js_map)}
{chr(10).join(self.js)}
window.__timelines["{self.pid}"] = tl;
</script>
</body>
</html>
'''
        open(os.path.join(pdir, "index.html"), "w").write(html)
        print(f"{self.pid}: {self.duration}s, {len(self.bg)} bg, {len(self.ov)} overlays, {len(self.maps)} maps, {len(self.sfx)} sfx")
        return pdir
