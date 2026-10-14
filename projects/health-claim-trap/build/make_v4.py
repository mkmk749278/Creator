#!/usr/bin/env python3
"""v4 scenes (owner, 2026-10-14): India map of the 18 Ombudsman offices, and browser clips for the two portals.

e21_india: India outline from DataMeet (india-composite.geojson, Survey of India-based, CC BY 4.0: credited on screen),
  projected once in Python with a tilted perspective camera (extruded edge, glowing rim), 18 office beams, arcs from the
  CIO head office in Mumbai. No AI map: an inaccurate outline of India is a legal risk (Survey of India rules).
e22_bima / e23_cio: a browser window types the exact URL in sync with the VO, the real page (full-page screenshot,
  build/web_full.js) loads and scrolls, the cursor clicks the complaint link; the URL also sits large above the window.
"""
import json, math, sys
sys.setrecursionlimit(20000)
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_scenes import page, put, OUT
from make_engines import bp_page, at, S, CITIES
from timing import L, sents

P = Path(__file__).resolve().parents[1]
A = P / "assets"


# ---------------- India map ----------------
def dp(pts, eps):
    """Douglas-Peucker simplification (no shapely in the container)."""
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy) or 1e-9
    i, dmax = 0, 0.0
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + x1 * y0 - y1 * x0) / n
        if d > dmax:
            i, dmax = k, d
    if dmax <= eps:
        return [pts[0], pts[-1]]
    return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)


def cam(lon, lat, z=0.0):
    """Lon/lat -> tilted screen point. Plane x right, y north; camera pitched 38° looking at India from the south."""
    x = (lon - 82.5) * math.cos(math.radians(22)) * 40.0
    y = (lat - 22.5) * 40.0
    pitch = math.radians(38)
    yy, zz = y * math.cos(pitch) - 0, y * math.sin(pitch) + z
    d = 2600.0
    s = d / (d + yy * 1.0)
    return 1010 + x * s, 600 - zz * s


def india_paths():
    g = json.load(open(A / "geo/india-composite.geojson"))["features"][0]["geometry"]["coordinates"]
    paths = []
    for poly in g:
        ring = poly[0]
        if len(ring) < 60:
            continue
        pts = [tuple(p) for p in ring][::max(1, len(ring) // 6000)]
        h = len(pts) // 2          # a closed ring has equal end points: simplify the two halves separately
        simp = dp(pts[:h + 1], 0.03)[:-1] + dp(pts[h:], 0.03)
        if len(simp) < 8:
            continue
        paths.append(simp)
    return paths


def e21_india():
    sid = "e21_india"
    start, end = S("E051")["start"] - 0.2, L("E052")[1] + 0.3
    rings = india_paths()
    def d_of(ring, z=0.0):
        pts = [cam(lo, la, z) for lo, la in ring]
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    top = "".join(f'<path d="{d_of(r)}"/>' for r in rings)
    sides = "".join(f'<path d="{d_of(r, -14 * k / 6)}"/>' for k in range(1, 7) for r in rings)
    hq = cam(72.84, 19.08)   # CIO head office, Santacruz (W), Mumbai (annual report cover)
    beams, arcs = [], []
    for i, (n, lo, la) in enumerate(CITIES):
        x, y = cam(lo, la)
        right = lo > 80 or n in ("Delhi", "Lucknow", "Patna", "Chandigarh")
        beams.append(f'<g class="pin" id="p{i}"><line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 90:.1f}" class="beam"/>'
                     f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="dot"/><circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="halo"/>'
                     f'<text x="{x + (12 if right else -12):.1f}" y="{y - 96:.1f}" text-anchor="{"start" if right else "end"}">{n}</text></g>')
        if n != "Mumbai":
            mx, my = (hq[0] + x) / 2, min(hq[1], y) - 110 - 0.15 * math.hypot(x - hq[0], y - hq[1])
            arcs.append(f'<path class="arc" id="a{i}" d="M{hq[0]:.1f} {hq[1]:.1f} Q{mx:.1f} {my:.1f} {x:.1f} {y:.1f}"/>')
    body = f"""
      <div id="map" style="position:absolute; inset:0; transform-origin:960px 600px">
        <svg viewBox="0 0 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px">
          <defs><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
          <g class="side">{sides}</g>
          <g class="top" id="top">{top}</g>
          <g class="rim" id="rim" filter="url(#glow)">{top}</g>
          <g id="arcs">{"".join(arcs)}</g>
          <g id="pins">{"".join(beams)}</g>
        </svg>
      </div>
      <div class="chip cyan" id="c1" style="left:90px; top:110px; opacity:0">Step 4 · Insurance Ombudsman</div>
      <div class="chip" id="c2" style="left:90px; top:200px; opacity:0">18 offices across India</div>
      <div class="chip green" id="c3" style="left:90px; top:820px; opacity:0">No consumer court case needed</div>
      <div class="chip green" id="c4" style="left:90px; top:910px; opacity:0">No expensive lawyer needed</div>"""
    css = """.side path { fill: #071226; stroke: rgba(56,189,248,.18); stroke-width: 1; }
.top path { fill: rgba(19,37,74,.92); stroke: none; } .rim path { fill: none; stroke: #38bdf8; stroke-width: 2.6; }
.arc { fill: none; stroke: rgba(125,211,252,.85); stroke-width: 2.5; } .beam { stroke: #facc15; stroke-width: 4; opacity: .85; filter: drop-shadow(0 0 8px #facc15); }
.dot { fill: #fde68a; } .halo { fill: none; stroke: #facc15; stroke-width: 3; transform-box: fill-box; transform-origin: center; }
.pin text { fill: #e2e8f0; font: 600 22px Inter, Arial, sans-serif; paint-order: stroke; stroke: rgba(2,6,15,.85); stroke-width: 5px; }"""
    s51, s52 = sents("E051"), sents("E052")
    cues = dict(step=s51[0]["start"], omb=s51[1]["start"], refuse=s52[0]["start"], court=at("E052", "consumer court"), lawyer=at("E052", "expensive lawyer"))
    js = """
      tl.fromTo($("map"), { scale: 0.86, y: 40, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 1.4, ease: "power2.out" }, 0);
      tl.to($("map"), { scale: 1.12, x: -40, y: -20, duration: D.duration - 1.4, ease: "none" }, 1.4);
      const rim = document.querySelectorAll("#rim path");
      rim.forEach((p) => { const n = p.getTotalLength(); gsap.set(p, { strokeDasharray: n, strokeDashoffset: n }); tl.to(p, { strokeDashoffset: 0, duration: 2.2, ease: "power1.inOut" }, 0.2); });
      for (let i = 0; i < 18; i++) tl.fromTo($("p" + i), { opacity: 0 }, { opacity: 1, duration: 0.25 }, C.omb + i * 0.16);
      document.querySelectorAll(".arc").forEach((p, i) => { const n = p.getTotalLength(); gsap.set(p, { strokeDasharray: n, strokeDashoffset: n });
        tl.to(p, { strokeDashoffset: 0, duration: 0.9, ease: "power2.out" }, C.refuse + 0.3 + i * 0.12); });
      FIN.hook((t) => document.querySelectorAll(".halo").forEach((h, i) => { const u = (t * 0.8 + i * 0.11) % 1; h.style.transform = `scale(${1 + u * 3.5})`; h.style.opacity = 1 - u; }));
      pop($("c1"), C.step); pop($("c2"), C.omb + 0.8); pop($("c3"), C.court); pop($("c4"), C.lawyer);
"""
    put(sid, bp_page(sid, "India: 18 Ombudsman offices", round(end - start, 2), body, js,
                     tag="CIO ANNUAL REPORT 2024-25 · MAP: DATAMEET INDIA BOUNDARIES, CC BY 4.0", css=css), start, end - start, cues)


# ---------------- browser clips ----------------
BROWSER_CSS = """
.win { position:absolute; left:90px; top:170px; width:1380px; height:870px; border-radius:16px; overflow:hidden; background:#f1f5f9;
  box-shadow:0 50px 100px rgba(0,0,0,.7), 0 0 0 1px rgba(255,255,255,.12); }
.bar { height:96px; background:#dfe3ea; border-bottom:1px solid #c5ccd6; }
.tabs { height:44px; display:flex; align-items:flex-end; padding-left:110px; } .tab { height:36px; width:330px; border-radius:10px 10px 0 0; background:#f8fafc; font:600 18px/36px Inter,Arial,sans-serif; padding-left:18px; color:#334155; }
.dots { position:absolute; left:22px; top:16px; } .dots i { display:inline-block; width:14px; height:14px; border-radius:50%; margin-right:8px; }
.omni { margin:6px 20px 0 140px; height:40px; border-radius:20px; background:#fff; display:flex; align-items:center; padding-left:18px; font:500 22px/40px Inter,Arial,sans-serif; color:#0f172a; }
.lock { color:#16a34a; margin-right:12px; font-size:18px; } .caret { display:inline-block; width:2px; height:24px; background:#0f172a; margin-left:2px; }
.load { position:absolute; left:0; top:94px; height:4px; width:100%; background:#0284c7; transform-origin:0 50%; transform:scaleX(0); }
.vp { position:absolute; left:0; top:96px; right:0; bottom:0; overflow:hidden; background:#fff; }
.vp img { position:absolute; left:0; top:0; width:1380px; }
.side2 { position:absolute; left:1500px; top:300px; width:390px; } .side2 .chip { position:relative; display:inline-flex; white-space:normal; font-size:32px; line-height:1.2; margin-bottom:22px; opacity:0; }
.cur { position:absolute; left:0; top:0; width:34px; height:34px; z-index:5; } .rip { position:absolute; left:0; top:0; width:60px; height:60px; margin:-30px 0 0 -30px; border-radius:50%; border:4px solid #0284c7; opacity:0; z-index:4; }
.url { position:absolute; left:90px; width:1380px; top:52px; text-align:center; font:800 64px/1 Inter,Arial,sans-serif; color:#f8fafc; letter-spacing:.01em; }
.url span { padding:10px 26px; border-radius:14px; background:rgba(2,132,199,.25); border:2px solid rgba(56,189,248,.7); }
.hl { position:absolute; border:5px solid #facc15; border-radius:12px; box-shadow:0 0 30px rgba(250,204,21,.6); opacity:0; }"""

CURSOR = '<svg class="cur" id="cur" viewBox="0 0 24 24"><path d="M3 2 L3 20 L8 15 L11.5 22 L14.5 20.5 L11 13.8 L18 13.8 Z" fill="#fff" stroke="#0f172a" stroke-width="1.6"/></svg>'


def browser(sid, img, url, title, start, end, cues, scroll, click, hls, chips, tag):
    """scroll: [[t, px], ...] page offset keys; click: (t, x, y) in window px; hls: [(t, x, y, w, h)] highlight boxes; chips: [(t, text, cls, top)]."""
    from PIL import Image
    d = OUT / sid / "img"; d.mkdir(parents=True, exist_ok=True)
    im = Image.open(A / "web" / img).convert("RGB")
    im = im.resize((1380, int(im.height * 1380 / im.width)))
    im.save(d / "page.jpg", quality=90)
    k = 1380 / 1520     # coordinates below were measured on a 1520-wide page; the window is 1380 wide
    hl = "".join(f'<div class="hl" id="h{i}" style="left:{x * k:.0f}px; top:{y * k:.0f}px; width:{w * k:.0f}px; height:{h * k:.0f}px"></div>' for i, (_, x, y, w, h) in enumerate(hls))
    ch = '<div class="side2">' + "".join(f'<div class="chip {c}" id="k{i}">{t}</div><br>' for i, (_, t, c, tp) in enumerate(chips)) + '</div>'
    scroll = [[a, b * k] for a, b in scroll]; click = (click[0], click[1] * k, click[2] * k)
    body = f"""
      <div class="url" id="big"><span id="bigt"></span></div>
      <div class="win" id="win">
        <div class="bar"><div class="dots"><i style="background:#ef4444"></i><i style="background:#f59e0b"></i><i style="background:#22c55e"></i></div>
          <div class="tabs"><div class="tab" id="tabt">New tab</div></div>
          <div class="omni"><span class="lock">🔒</span><span id="typed"></span><span class="caret" id="caret"></span></div></div>
        <div class="load" id="load"></div>
        <div class="vp" id="vp"><img id="pg" src="img/page.jpg" style="opacity:0"/>{hl}</div>
        {CURSOR}<div class="rip" id="rip"></div>
      </div>{ch}"""
    js = f"""
      const URL_ = {json.dumps(url)}, TITLE = {json.dumps(title)};
      pop($("win"), 0.05, {{ opacity: 0, y: 60, scale: 0.96 }});
      const typedK = FIN.keys([[C.type0, 0], [C.type1, URL_.length]]);
      FIN.bind($("typed"), typedK, (v) => URL_.slice(0, Math.round(v)));
      FIN.bind($("bigt"), typedK, (v) => URL_.slice(0, Math.round(v)) || " ");
      FIN.hook((t) => {{ $("caret").style.opacity = t < C.load && Math.floor(t * 2) % 2 === 0 ? 1 : 0;
        $("big").style.opacity = t < C.type0 ? 0 : 1; }});
      FIN.bind($("tabt"), (t) => t > C.load + 0.6 ? 1 : 0, (v) => v ? TITLE : "New tab");
      tl.fromTo($("load"), {{ scaleX: 0, opacity: 1 }}, {{ scaleX: 1, duration: 0.8, ease: "power2.out" }}, C.load);
      tl.to($("load"), {{ opacity: 0, duration: 0.2 }}, C.load + 0.85);
      tl.fromTo($("pg"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, C.load + 0.4);
      const sk = FIN.keys({json.dumps(scroll)});
      FIN.hook((t) => {{ const y = -sk(t); $("pg").style.transform = `translateY(${{y}}px)`;
        document.querySelectorAll(".hl").forEach((h) => h.style.transform = `translateY(${{y}}px)`); }});
      const cx = FIN.keys([[0, 1200], [{click[0] - 1.2}, 1200], [{click[0]}, {click[1]}]]), cy = FIN.keys([[0, 700], [{click[0] - 1.2}, 700], [{click[0]}, {click[2] + 96}]]);
      FIN.hook((t) => {{ $("cur").style.transform = `translate(${{cx(t)}}px, ${{cy(t)}}px)`; $("cur").style.opacity = t > C.load + 1 ? 1 : 0; }});
      gsap.set($("rip"), {{ x: {click[1]}, y: {click[2] + 96} }});
      tl.fromTo($("rip"), {{ opacity: 1, scale: 0.4 }}, {{ opacity: 0, scale: 2.4, duration: 0.6, ease: "power2.out", immediateRender: false }}, {click[0]});
      {"".join(f'tl.to($("h{i}"), {{ opacity: 1, duration: 0.3 }}, {t});' for i, (t, *_r) in enumerate(hls))}
      {"".join(f'pop($("k{i}"), {t}, {{ opacity: 0, x: 40 }});' for i, (t, *_r) in enumerate(chips))}
      tl.fromTo($("stage"), {{ scale: 1 }}, {{ scale: 1.03, duration: D.duration, ease: "none" }}, 0);
"""
    put(sid, bp_page(sid, f"Browser: {url}", round(end - start, 2), body, js, tag=tag, css=BROWSER_CSS),
        start, end - start, cues)


def rel(cues, start):
    return {k: v for k, v in cues.items()}


def e22_bima():
    s49, s50 = sents("E049"), sents("E050")
    start, end = at("E050", "go to") - 1.0, s50[1]["end"] + 0.4
    t = lambda v: round(v - start, 2)
    type0, type1 = at("E050", "Bima Bharosa dot"), s50[0]["end"]
    cues = dict(type0=type0, type1=type1, load=type1 + 0.15)
    # page px (1520-wide image): Register Complaint button ~ (300, 300), "attended within 14 days" ~ (95, 350, 400, 40)
    browser("e22_bima", "bima_full.png", "bimabharosa.irdai.gov.in", "Bima Bharosa | IRDAI", start, end, cues,
            scroll=[[0, 0], [t(s50[1]["start"]), 0]], click=(t(s50[1]["start"]) + 1.5, 300, 300),
            hls=[(t(s50[1]["start"]) + 2.2, 85, 340, 430, 40)],
            chips=[(t(s50[1]["start"]) + 0.3, "IRDAI's own complaint portal", "cyan", 600),
                   (t(at("E050", "tracked", k=1)), "Tracked by IRDAI", "amber", 680)],
            tag="BIMABHAROSA.IRDAI.GOV.IN · SCREEN RECORDING (REPLAYED)")


def e23_cio():
    s53, s54 = sents("E053"), sents("E054")
    start, end = s53[0]["start"] - 0.2, s54[3]["end"] + 0.4
    t = lambda v: round(v - start, 2)
    type0, type1 = at("E053", "c-i-o-i-n-s"), s53[0]["end"]
    cues = dict(type0=type0, type1=type1, load=type1 + 0.15)
    # 1520-wide page is ~1383 px tall; viewport 774 px: scroll to "Ways to submit" (~y 600 page) in the pause
    browser("e23_cio", "cio_full.png", "cioins.co.in", "Council for Insurance Ombudsmen", start, end, cues,
            scroll=[[0, 0], [t(type1 + 1.0), 0], [t(s54[0]["start"]), 560], [D_END := t(s54[3]["end"]), 600]],
            click=(t(s54[1]["start"]) + 0.3, 275, 357),
            hls=[(t(s54[1]["start"]) + 0.6, 228, 935, 270, 44)],
            chips=[(t(s54[0]["start"]) + 1.5, "Set up under the Ombudsman Rules", "cyan", 500),
                   (t(s54[1]["start"]), "File online", "cyan", 580), (t(s54[2]["start"]), "₹0 fee", "green", 660),
                   (t(s54[3]["start"]), "No lawyer needed", "green", 740)],
            tag="CIOINS.CO.IN · SCREEN RECORDING (REPLAYED)")


SCENES = [e21_india, e22_bima, e23_cio]
if __name__ == "__main__":
    only = set(sys.argv[1:])
    for f in SCENES:
        if not only or f.__name__ in only:
            f()
