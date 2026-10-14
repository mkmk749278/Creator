#!/usr/bin/env python3
"""Write the film's animated HyperFrames scenes: video/healthclaim/<id>/{index.html, data.js, img/}.

Art direction "the file at night" (README): carbon slate, analytical cyan for the law and our proof, amber for clocks
and the TPA, crimson only for the denial stamp and myths. Every cue time comes from the VO alignment (build/timing.py),
so each beat lands on the word that names it. Documents are SIMULATIONS (no real insurer, TPA or hospital).
Run: python3 projects/health-claim-trap/build/make_scenes.py, then npm run vendor, then lint/check/snapshot/render.
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import L, sents

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
OUT = ROOT / "video/healthclaim"
BR = P / "assets/broll"


def at(eid, word=None, k=0, frac=None):
    """Film time of a word inside a line's k-th sentence (speech assumed even across the sentence's letters)."""
    s = sents(eid)[k]
    if word is None and frac is None:
        return s["start"]
    if frac is None:
        i = s["text"].lower().find(word.lower())
        assert i >= 0, (eid, word)
        frac = i / max(1, len(s["text"]))
    return s["start"] + (s["end"] - s["start"]) * frac


FONTS = "".join(
    f'@font-face {{ font-family: "Inter"; font-weight: {w}; src: url("vendor/fonts/inter-{sub}-{w}-normal.woff2") format("woff2"); unicode-range: {rng}; }}\n'
    for w in (400, 600, 800) for sub, rng in (("latin", "U+0000-00FF, U+2000-206F, U+2190-21FF, U+2700-27BF"), ("latin-ext", "U+0100-02FF, U+20A0-20CF")))

CSS = """
:root { --slate: #0f172a; --slate-2: #1e293b; --cyan: #0284c7; --cyan-hi: #38bdf8; --amber: #f59e0b; --crimson: #dc2626;
  --white: #f8fafc; --dim: #94a3b8; --gold: #facc15; }
#stage { position: absolute; inset: 0; transform-origin: 50% 50%; }
.hc-grade { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 40%, rgba(15,23,42,.55), rgba(2,6,15,.92) 75%); }
.chip { position: absolute; display: flex; align-items: center; gap: 16px; padding: 16px 26px; border-radius: 14px;
  font: 800 38px/1 Inter, Arial, sans-serif; letter-spacing: .02em; background: rgba(2, 6, 15, .82); border: 2px solid rgba(255,255,255,.14); color: var(--white); white-space: nowrap; }
.chip.cyan { color: var(--cyan-hi); border-color: rgba(56,189,248,.55); }
.chip.amber { color: var(--amber); border-color: rgba(245,158,11,.55); }
.chip.red { color: #f87171; border-color: rgba(220,38,38,.6); }
.chip.green { color: #4ade80; border-color: rgba(74,222,128,.5); }
.chip svg { width: 44px; height: 44px; flex: none; }
.lab { position: absolute; font: 600 24px/1.2 Inter, Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); text-align: center; }
.big { position: absolute; font: 800 96px/1 Inter, Arial, sans-serif; color: var(--white); text-align: center; letter-spacing: -.01em; }
.sim-mark { position: absolute; font: 800 22px/1 Inter, Arial, sans-serif; letter-spacing: .3em; color: rgba(15,23,42,.18); transform: rotate(-24deg); }
/* paper documents */
.paper { position: absolute; background: #f4f1ea; color: #1f2937; border-radius: 6px; box-shadow: 0 40px 80px rgba(0,0,0,.65), 0 0 0 1px rgba(0,0,0,.2);
  font: 400 22px/1.45 Inter, Arial, sans-serif; overflow: hidden; }
.paper .hd { background: #e7e2d6; padding: 22px 34px; border-bottom: 3px solid #cbc3b1; }
.paper .co { font: 800 26px/1.2 Inter, Arial, sans-serif; letter-spacing: .04em; color: #1e3a5f; }
.paper .sub { font: 600 17px/1.3 Inter, Arial, sans-serif; color: #6b7280; letter-spacing: .06em; text-transform: uppercase; margin-top: 4px; }
.paper .bd { padding: 26px 34px; }
.paper .t { font: 800 25px/1.2 Inter, Arial, sans-serif; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 16px; color: #111827; }
.paper .row { display: flex; justify-content: space-between; border-bottom: 1px solid #d6d0c2; padding: 8px 0; }
.paper .row b { font-weight: 800; }
.paper .note { font-size: 19px; color: #4b5563; margin-top: 16px; }
.stamp { position: absolute; padding: 14px 30px; border: 9px solid currentColor; border-radius: 14px; font: 800 74px/1 Inter, Arial, sans-serif;
  letter-spacing: .06em; text-transform: uppercase; white-space: nowrap; mix-blend-mode: multiply; }
.stamp.red { color: rgba(205, 30, 30, .9); }
.stamp.cyan { color: rgba(2, 132, 199, .95); mix-blend-mode: normal; background: rgba(240, 249, 255, .82); }
"""


def page(sid, title, dur, body, js, tag="", bg="img/bg.jpg", css=""):
    tag_html = f'<div class="fin-tag" id="tag">{tag}</div>' if tag else ""
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>{title}</title>
    <script src="vendor/gsap.min.js"></script>
    <script src="vendor/fin/fin.js"></script>
    <script src="data.js"></script>
    <link rel="stylesheet" href="vendor/fin/fin.css" />
    <style>
{FONTS}{CSS}{css}
    </style>
  </head>
  <body>
    <div id="root" class="fin-root" data-composition-id="{sid}" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
      <div class="fin-bg" style="background-image: url('{bg}')"></div>
      <div class="hc-grade"></div>
      <div id="stage">
{body}
      </div>
      {tag_html}
      <canvas class="fin-grain" id="grain" width="500" height="290"></canvas>
      <div class="fin-vig"></div>
    </div>
    <script>
      const D = window.DATA, C = D.cues, $ = (id) => document.getElementById(id);
      FIN.grain($("grain"));
      const tl = gsap.timeline({{ paused: true }});
      const pop = (el, t, from = {{ opacity: 0, y: 26 }}) => tl.fromTo(el, from, {{ opacity: 1, y: 0, x: 0, scale: 1, duration: 0.45, ease: "power3.out" }}, t);
      const out = (el, t) => tl.to(el, {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, t);
{js}
      tl.to({{}}, {{ duration: 0.01 }}, D.duration - 0.01);
      FIN.attach(tl);
      window.__timelines["{sid}"] = tl;
    </script>
  </body>
</html>
"""


def bg_frame(sid, src, ss, blur=6, bright=-0.12):
    d = OUT / sid / "img"; d.mkdir(parents=True, exist_ok=True)
    out = d / "bg.jpg"
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", str(src), "-frames:v", "1", "-vf",
                        f"scale=1980:-2,boxblur={blur},eq=brightness={bright}", "-q:v", "3", str(out)], check=True)


def put(sid, html, start, dur, cues):
    d = OUT / sid; d.mkdir(parents=True, exist_ok=True)
    data = dict(id=sid, start=round(start, 3), duration=round(dur, 2), cues={k: round(v - start, 3) for k, v in cues.items()})
    for f, txt in (("index.html", html), ("data.js", "// Generated by projects/health-claim-trap/build/make_scenes.py from the VO alignment. Do not edit.\n"
                                                        f"window.DATA = {json.dumps(data, sort_keys=True)};\n")):
        p = d / f
        if not p.exists() or p.read_text() != txt:
            p.write_text(txt)
    print(f"{sid:16s} start {start:7.2f} dur {dur:5.2f}  " + " ".join(f"{k}={v:.2f}" for k, v in sorted(data['cues'].items(), key=lambda x: x[1])))


LETTER = """
        <div class="paper" id="letter" style="left: 560px; top: 70px; width: 800px; height: 960px; transform: rotate(-1.5deg)">
          <div class="hd"><div class="co">SAMPLE HEALTH INSURANCE CO. LTD.</div><div class="sub">Third Party Administrator: Sample Health TPA</div></div>
          <div class="bd">
            <div class="t">Cashless authorisation: decision</div>
            <div class="row"><span>Patient</span><b>R. K****</b></div>
            <div class="row"><span>Hospital</span><b>Sample City Hospital</b></div>
            <div class="row"><span>Policy in force since</span><b>2020</b></div>
            <div class="row"><span>Amount requested</span><b>₹4,50,000</b></div>
            <div class="row"><span>Decision</span><b style="color:#b91c1c">Cashless denied</b></div>
            <div class="row" style="border:0"><span>Reason</span></div>
            <div style="font-weight:600">Non-disclosure of pre-existing disease (hypertension) at proposal stage.</div>
            <div class="note">You may submit the claim for reimbursement as per policy terms and conditions.</div>
            <div class="note" style="margin-top: 40px">Authorised signatory · Claims team</div>
          </div>
          <div class="sim-mark" style="left: 210px; top: 560px">SIMULATION</div>
        </div>"""
COUNTER = '<div style="position:absolute; left:-40px; right:-40px; top:760px; height:420px; background:linear-gradient(#3a2f26,#1c1612); box-shadow: 0 -20px 60px rgba(0,0,0,.6)"></div>'


def s00_receipts():
    s = sents("E002"); start, end = s[0]["start"] - 0.25, s[2]["end"] + 0.4
    bg_frame("s00_receipts", BR / "pixabay_34258.mp4", 3)
    years = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    rec = "".join(f"""
        <div class="paper rc" id="rc{i}" style="left:{90 + i * 295}px; top:270px; width:280px; height:400px; font-size:18px">
          <div class="hd" style="padding:14px 18px"><div class="co" style="font-size:19px">PREMIUM RECEIPT</div><div class="sub" style="font-size:15px; margin-top:8px">Policy year {y}</div></div>
          <div class="bd" style="padding:16px 18px"><div style="font:800 48px/1 Inter,Arial,sans-serif;color:#111">₹35,000</div>
          <div style="margin-top:14px;color:#6b7280">Family health cover</div>
          <div class="stamp" id="pd{i}" style="left:40px;top:250px;font-size:38px;border-width:5px;padding:6px 14px;color:rgba(22,130,60,.9)">Paid ✓</div></div>
          <div class="sim-mark" style="left:30px; top:150px; font-size:14px">SIMULATION</div>
        </div>""" for i, y in enumerate(years))
    body = rec + """
        <div class="chip cyan" id="amt" style="left:140px; top:140px">₹35,000 every year</div>
        <div class="chip amber" id="yrs" style="left:140px; top:720px">Renewed on time · <span id="n">0</span> years</div>
        <div class="chip green" id="miss" style="left:860px; top:720px">Never missed a payment</div>"""
    cues = dict(amt=s[0]["start"], deal=s[1]["start"], paid=s[2]["start"])
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
      pop($("amt"), C.amt + 0.2);
      for (let i = 0; i < 6; i++) pop($("rc" + i), C.deal + i * 0.42, { opacity: 0, y: -260, rotation: (i % 2 ? 6 : -5) });
      pop($("yrs"), C.deal + 0.2);
      FIN.bind($("n"), FIN.keys([[C.deal, 0], [C.deal + 2.3, 6]]), (v) => Math.round(v));
      for (let i = 0; i < 6; i++) tl.fromTo($("pd" + i), { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, C.paid + i * 0.18);
      pop($("miss"), C.paid + 0.3);
"""
    put("s00_receipts", page("s00_receipts", "Six years of premiums", round(end - start, 2), body, js, tag="SIMULATION · ILLUSTRATIVE FAMILY"), start, end - start, cues)


def s01_letter():
    start, end = at("E005") - 0.3, L("E006")[1] + 0.35
    bg_frame("s01_letter", BR / "coverr-iv-in-hospital-room-5485.mp4", 2, blur=10, bright=-0.2)
    body = COUNTER + LETTER + """
        <div class="stamp red" id="stamp" style="left: 700px; top: 470px; transform: rotate(-12deg)">Cashless denied</div>
        <div id="flash" style="position:absolute; inset:0; background: radial-gradient(ellipse at center, rgba(220,38,38,0) 40%, rgba(220,38,38,.45) 100%); opacity:0"></div>"""
    cues = dict(hand=at("E005", "hands you"), stamp=at("E005", "rejected"), drop=at("E006"), panic=at("E006", k=1))
    js = """
      tl.fromTo($("letter"), { y: 700, rotation: 4 }, { y: 0, rotation: -1.5, duration: 1.1, ease: "power3.out" }, Math.max(0, C.hand - 0.4));
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.06, duration: C.stamp, ease: "none" }, 0);
      tl.fromTo($("stamp"), { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, C.stamp);
      tl.fromTo($("stage"), { x: 0 }, { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.stamp + 0.2);
      tl.to($("stage"), { scale: 1.5, x: 0, y: 60, duration: 2.6, ease: "power2.inOut" }, C.drop - 0.3);
      tl.fromTo($("flash"), { opacity: 0 }, { opacity: 1, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, C.drop);
"""
    put("s01_letter", page("s01_letter", "The cashless denial letter", round(end - start, 2), body, js, tag="SIMULATION · ILLUSTRATIVE LETTER"), start, end - start, cues)


def s01b_overstamp():
    start, end = at("E009") - 0.3, L("E009")[1] + 0.5
    bg_frame("s01b_overstamp", BR / "coverr-iv-in-hospital-room-5485.mp4", 2, blur=10, bright=-0.2)
    body = COUNTER + LETTER + """
        <div class="stamp red" id="stamp" style="left: 700px; top: 470px; transform: rotate(-12deg)">Cashless denied</div>
        <svg id="crack" viewBox="0 0 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px" fill="none" stroke="#f8fafc" stroke-width="5" stroke-linecap="round">
          <path id="c1" d="M760 470 L840 540 L820 600 L910 650" /><path id="c2" d="M1180 500 L1120 560 L1160 620 L1090 690" /><path id="c3" d="M980 520 L1000 600 L960 650" />
        </svg>
        <div class="stamp cyan" id="over" style="left: 610px; top: 690px; transform: rotate(4deg); font-size: 64px">Not allowed after 5 years</div>"""
    cues = dict(rule=at("E009", "legal rule"), illegal=at("E009", "illegal"), five=at("E009", "five years"))
    js = """
      gsap.set($("stamp"), { opacity: 1 });
      tl.fromTo($("stage"), { scale: 1.12, y: 30 }, { scale: 1.0, y: 0, duration: C.illegal, ease: "sine.inOut" }, 0);
      ["c1", "c2", "c3"].forEach((id, i) => { const p = $(id), n = p.getTotalLength();
        gsap.set(p, { strokeDasharray: n, strokeDashoffset: n });
        tl.to(p, { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, C.rule + 0.1 + i * 0.12); });
      tl.to($("stamp"), { opacity: 0.35, filter: "grayscale(1)", duration: 0.6 }, C.illegal - 0.2);
      tl.fromTo($("over"), { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }, C.illegal + 0.1);
      tl.fromTo($("stage"), { x: 0 }, { x: 8, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.illegal + 0.32);
      tl.to($("stage"), { scale: 1.12, duration: D.duration - C.illegal - 0.4, ease: "sine.inOut" }, C.illegal + 0.4);
"""
    put("s01b_overstamp", page("s01b_overstamp", "Not allowed after five years", round(end - start, 2), body, js,
                               tag="IRDAI INSURANCE PRODUCTS REGULATIONS | 2024"), start, end - start, cues)


ICON = {
    "person": '<circle cx="24" cy="15" r="8"/><path d="M8 42 C8 30 16 26 24 26 C32 26 40 30 40 42"/>',
    "hosp": '<rect x="8" y="10" width="32" height="32" rx="3"/><path d="M24 17 V35 M15 26 H33"/>',
    "file": '<path d="M13 5 H30 L38 13 V43 H13 Z"/><path d="M30 5 V13 H38 M19 23 H32 M19 30 H32 M19 37 H27"/>',
    "bank": '<path d="M6 18 L24 7 L42 18 Z"/><path d="M10 22 V36 M19 22 V36 M29 22 V36 M38 22 V36 M6 41 H42"/>',
}


def svg(name, size=96, color="currentColor"):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def s02_flow():
    s14, s15, s16 = sents("E014"), sents("E015"), sents("E016")
    start, end = s14[0]["start"] - 0.3, s16[0]["end"] + 0.4
    bg_frame("s02_flow", BR / "pixabay_142528.mp4", 2, blur=12, bright=-0.25)
    nodes = [("n0", "Patient", "person", 250), ("n1", "Hospital", "hosp", 720), ("n2", "TPA", "file", 1190), ("n3", "Insurance company", "bank", 1660)]
    body = "".join(f"""
        <div class="node" id="{i}" style="left:{x - 105}px; top:300px">{svg(ic, 104)}</div>
        <div class="lab" id="{i}l" style="left:{x - 170}px; top:530px; width:340px">{name}</div>""" for i, name, ic, x in nodes)
    body += "".join(f'<div class="arrow" id="a{k}" style="left:{x0 + 120}px; top:403px; width:{x1 - x0 - 240}px"></div>'
                    for k, ((_, _, _, x0), (_, _, _, x1)) in enumerate(zip(nodes, nodes[1:])))
    body += "".join(f'<div class="doc" id="d{k}">{svg("file", 44, "#f8fafc")}</div>' for k in range(3))
    body += """
        <div class="chip amber" id="mid" style="left:1030px; top:180px">Middleman</div>
        <div class="lab" id="full" style="left:990px; top:580px; width:400px; color:#f59e0b">Third Party Administrator</div>
        <div class="chip red" id="myth" style="left:900px; top:150px">Neutral govt doctor?</div>
        <div id="strike" style="position:absolute; left:890px; top:183px; width:0; height:7px; background:#dc2626; border-radius:4px"></div>
        <div class="pay" id="pay"><div class="arc"></div><div class="chip cyan" style="position:relative; left:0; top:0">Hired and paid by the insurer</div></div>
        <div id="files" style="position:absolute; left:360px; top:740px; width:1200px; height:160px"></div>
        <div class="chip amber" id="seven" style="left:600px; top:930px">7 in 10 claims settled via TPAs</div>"""
    css = """
.node { position: absolute; width: 210px; height: 210px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  color: var(--white); background: rgba(15,23,42,.88); border: 4px solid rgba(148,163,184,.5); box-shadow: 0 20px 50px rgba(0,0,0,.5); }
.arrow { position: absolute; height: 4px; background: repeating-linear-gradient(90deg, rgba(148,163,184,.8) 0 18px, transparent 18px 30px); }
.arrow::after { content: ""; position: absolute; right: -6px; top: -9px; border: 11px solid transparent; border-left: 16px solid rgba(148,163,184,.9); }
.doc { position: absolute; top: 380px; opacity: 0; }
.pay { position: absolute; left: 1260px; top: 640px; opacity: 0; }
.fi { position: absolute; top: 0; width: 90px; height: 120px; }
"""
    cues = dict(ins=s14[0]["start"], tpa=s14[1]["start"] + 1.2, full=s14[2]["start"], myth=s15[0]["start"] + 0.3,
                no=s15[1]["start"], paid=at("E015", "hired", k=2), seven=s16[0]["start"])
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
      ["n0", "n1", "n2", "n3"].forEach((id, i) => { pop($(id), 0.1 + i * 0.2, { opacity: 0, scale: 0.6 }); pop($(id + "l"), 0.3 + i * 0.2); });
      ["a0", "a1", "a2"].forEach((id, i) => tl.fromTo($(id), { opacity: 0, scaleX: 0, transformOrigin: "0 50%" }, { opacity: 1, scaleX: 1, duration: 0.5 }, 0.5 + i * 0.2));
      // files travel patient -> hospital -> TPA -> insurer, a pure function of time
      const xs = [250, 720, 1190, 1660];
      for (let k = 0; k < 3; k++) { const el = $("d" + k);
        FIN.hook((t) => { if (t < 1.2) { el.style.opacity = 0; return; } const u = ((t - 1.2) / 4.5 + k / 3) % 1, seg = Math.floor(u * 3), f = u * 3 - seg;
          el.style.opacity = Math.min(1, (t - 1.2) * 2) * (f < 0.12 ? f / 0.12 : f > 0.88 ? (1 - f) / 0.12 : 1);
          el.style.left = (xs[seg] + 110 + (xs[seg + 1] - xs[seg] - 220) * f - 22) + "px"; }); }
      tl.to($("n3"), { borderColor: "#38bdf8", boxShadow: "0 0 60px rgba(56,189,248,.6)", duration: 0.4 }, C.ins + 0.5);
      tl.to($("n3"), { borderColor: "rgba(148,163,184,.5)", boxShadow: "0 20px 50px rgba(0,0,0,.5)", duration: 0.4 }, C.tpa - 0.3);
      tl.to([$("n0"), $("n1"), $("n3")], { opacity: 0.45, duration: 0.4 }, C.tpa);
      tl.to($("n2"), { borderColor: "#f59e0b", color: "#f59e0b", scale: 1.15, boxShadow: "0 0 80px rgba(245,158,11,.55)", duration: 0.45 }, C.tpa);
      pop($("mid"), C.tpa + 0.1);
      tl.to($("n2l"), { opacity: 0, duration: 0.2 }, C.full - 0.1); pop($("full"), C.full);
      out($("mid"), C.myth - 0.4);
      pop($("myth"), C.myth);
      tl.fromTo($("strike"), { width: 0 }, { width: 470, duration: 0.3, ease: "power2.out" }, C.no + 0.1);
      tl.to([$("myth"), $("strike")], { opacity: 0, duration: 0.4 }, C.no + 1.1);
      tl.to($("n3"), { opacity: 1, borderColor: "#38bdf8", duration: 0.4 }, C.paid - 0.2);
      pop($("pay"), C.paid);
      // seven of ten claim files go through the TPA
      const box = $("files");
      for (let i = 0; i < 10; i++) { const f = document.createElement("div"); f.className = "fi"; f.style.left = (i * 120) + "px";
        f.innerHTML = '""" + svg("file", 90, "#94a3b8").replace("'", "\\'") + """'; box.appendChild(f);
        pop(f, C.seven + 0.1 + i * 0.08, { opacity: 0, y: 40 });
        if (i < 7) tl.to(f, { color: "#f59e0b", duration: 0.2, onStart: null }, C.seven + 1.4 + i * 0.12);
        if (i < 7) tl.to(f.querySelector("svg"), { stroke: "#f59e0b", duration: 0.2 }, C.seven + 1.4 + i * 0.12); }
      out($("pay"), C.seven - 0.2);
      pop($("seven"), C.seven + 2.4);
"""
    put("s02_flow", page("s02_flow", "Who really says no: the TPA", round(end - start, 2), body, js,
                         tag="IRDAI ANNUAL REPORT 2024-25 · IRDAI TPA REGULATIONS", css=css), start, end - start, cues)


def ring_svg(n, r=320, cx=960, cy=500, w=42, gap=0.012, prefix="g"):
    import math
    out = []
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n + gap - math.pi / 2, 2 * math.pi * (i + 1) / n - gap - math.pi / 2
        p = lambda a, rr: (cx + rr * math.cos(a), cy + rr * math.sin(a))
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(a0, r), p(a1, r), p(a1, r - w), p(a0, r - w)
        out.append(f'<path id="{prefix}{i}" d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} A{r - w} {r - w} 0 0 0 {x3:.1f} {y3:.1f} Z" />')
    return "".join(out)


def s03_ring():
    s30, s31 = sents("E030"), sents("E031")
    start, end = s30[0]["start"] - 0.3, s31[0]["end"] + 0.5
    bg_frame("s03_ring", BR / "pixabay_87146.mp4", 2, blur=14, bright=-0.3)
    body = f"""
        <svg viewBox="0 0 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px" fill="rgba(148,163,184,.55)">{ring_svg(96)}</svg>
        <div class="big" id="t8" style="left:660px; top:420px; width:600px">8 years</div>
        <div class="lab" id="m8" style="left:660px; top:530px; width:600px">96 months</div>
        <div class="big" id="t5" style="left:660px; top:420px; width:600px; color:#38bdf8; opacity:0">5 years</div>
        <div class="lab" id="m5" style="left:660px; top:530px; width:600px; opacity:0">60 months</div>
        <div class="chip cyan" id="nob" style="left:760px; top:900px; opacity:0">No break in your policy</div>"""
    cues = dict(eight=s30[0]["start"], down=at("E030", "brought it down", k=1), five=at("E030", "to five years", k=1), fill=s31[0]["start"])
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.06, duration: D.duration, ease: "none" }, 0);
      for (let i = 0; i < 96; i++) pop($("g" + i), 0.05 + i * 0.012, { opacity: 0, scale: 0.9, transformOrigin: "960px 500px" });
      pop($("t8"), C.eight + 0.2); pop($("m8"), C.eight + 0.4);
      for (let i = 60; i < 96; i++) tl.to($("g" + i), { opacity: 0, y: 140 + (i % 7) * 20, duration: 0.6, ease: "power2.in" }, C.down + (i - 60) * 0.03);
      out($("t8"), C.five - 0.3); out($("m8"), C.five - 0.3);
      tl.to($("t5"), { opacity: 1, duration: 0.4 }, C.five); tl.to($("m5"), { opacity: 1, duration: 0.4 }, C.five + 0.1);
      for (let i = 0; i < 60; i++) tl.to($("g" + i), { fill: (i % 12 === 11) ? "#f8fafc" : "#0284c7", duration: 0.08 }, C.fill + i * 0.055);
      pop($("nob"), C.fill + 2.6);
"""
    put("s03_ring", page("s03_ring", "The moratorium: eight years to five", round(end - start, 2), body, js,
                         tag="IRDAI INSURANCE PRODUCTS REGULATIONS | 2024"), start, end - start, cues)


def s03b_family():
    s = sents("E037"); start, end = s[0]["start"] - 0.3, s[3]["end"] + 0.4
    bg_frame("s03b_family", BR / "pixabay_10874.mp4", 3, blur=12, bright=-0.2)
    cells = "".join(f'<div class="mo" id="m{i}" style="left:{140 + i * 22}px"></div>' for i in range(72))
    body = cells + """
        <div class="lab" style="left:140px; top:330px; width:1310px; text-align:left" id="lm">Moratorium: 60 months</div>
        <div class="lab" style="left:1460px; top:330px; width:300px; text-align:left; color:#facc15" id="ly">Year 6</div>
        <div class="chip cyan" id="six" style="left:140px; top:520px">Our family: 6 years of continuous policy</div>
        <div class="paper" id="mini" style="left:1080px; top:600px; width:560px; height:300px; transform: rotate(3deg)">
          <div class="hd" style="padding:14px 22px"><div class="co" style="font-size:20px">CASHLESS AUTHORISATION</div></div>
          <div class="bd" style="padding:16px 22px; font-size:20px">Reason: non-disclosure of pre-existing disease</div>
          <div class="stamp red" style="left:40px; top:160px; font-size:38px; transform: rotate(-8deg)">Cashless denied</div>
          <div class="sim-mark" style="left:120px; top:190px; font-size:16px">SIMULATION</div>
        </div>
        <div id="gstrike" style="position:absolute; left:1050px; top:760px; width:0; height:12px; background:#facc15; border-radius:6px; transform: rotate(-8deg); transform-origin: 0 50%"></div>
        <div class="chip amber" id="against" style="left:140px; top:780px; color:#facc15; border-color:rgba(250,204,21,.6)">Against the IRDAI rule</div>"""
    css = ".mo { position: absolute; top: 400px; width: 18px; height: 70px; border-radius: 4px; background: rgba(148,163,184,.35); }"
    cues = dict(fam=s[0]["start"], six=s[1]["start"], letter=s[2]["start"], viol=s[3]["start"])
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
      for (let i = 0; i < 72; i++) pop($("m" + i), 0.1 + i * 0.01, { opacity: 0, y: 20 });
      for (let i = 0; i < 72; i++) tl.to($("m" + i), { background: i < 60 ? "#0284c7" : "#facc15", duration: 0.06 }, C.six + i * 0.022);
      pop($("lm"), C.six + 0.3); pop($("ly"), C.six + 1.5); pop($("six"), C.six + 0.4);
      pop($("mini"), C.letter, { opacity: 0, y: 200, rotation: 10 });
      tl.fromTo($("gstrike"), { width: 0 }, { width: 620, duration: 0.35, ease: "power2.out" }, C.viol + 0.5);
      pop($("against"), C.viol + 0.6);
"""
    put("s03b_family", page("s03b_family", "Our family: six years", round(end - start, 2), body, js,
                            tag="IRDAI MASTER CIRCULAR | PARA 13", css=css), start, end - start, cues)


def s04_clock():
    s38, s39, s40 = sents("E038"), sents("E039"), sents("E040")
    start, end = s38[0]["start"] - 0.3, s40[1]["end"] + 0.4
    bg_frame("s04_clock", BR / "pixabay_326937.mp4", 2, blur=14, bright=-0.3)
    ticks = "".join(f'<line x1="0" y1="-300" x2="0" y2="{-270 if i % 3 else -250}" transform="rotate({i * 30})" />' for i in range(12))
    body = f"""
        <svg id="clock" viewBox="-340 -340 680 680" style="position:absolute; left:180px; top:200px; width:680px; height:680px">
          <circle r="320" fill="rgba(15,23,42,.9)" stroke="rgba(148,163,184,.6)" stroke-width="6" />
          <path id="arcA" fill="rgba(245,158,11,.45)" d="" /><path id="arcR" fill="rgba(220,38,38,.55)" d="" />
          <g stroke="#f8fafc" stroke-width="8" stroke-linecap="round">{ticks}</g>
          <line id="hand" x1="0" y1="20" x2="0" y2="-250" stroke="#f8fafc" stroke-width="12" stroke-linecap="round" />
          <circle r="18" fill="#f59e0b" />
        </svg>
        <div class="chip" id="req" style="left:980px; top:240px">Discharge request sent</div>
        <div class="chip amber" id="three" style="left:980px; top:380px">Final approval: within 3 hours</div>
        <div class="chip cyan" id="wait" style="left:980px; top:520px">Patient should not be made to wait</div>
        <div class="chip red" id="late" style="left:980px; top:660px">Later than 3 hours?</div>
        <div class="chip cyan" id="pays" style="left:980px; top:800px">Extra charges: insurer pays, not you</div>
        <div class="lab" id="clk" style="left:300px; top:900px; width:440px; font-size:30px; color:#f8fafc">9:00 PM</div>"""
    cues = dict(clock=s38[0]["start"], req=s39[0]["start"] + 0.5, three=at("E039", "three hours"), wait=s40[0]["start"],
                late=s40[1]["start"], extra=at("E040", "extra amount", k=1), pays=at("E040", "paid by", k=1))
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
      pop($("clock"), C.clock, { opacity: 0, scale: 0.7 }); pop($("clk"), C.clock + 0.3);
      // clock reading in minutes after 9:00 PM (the hook's billing counter), a function of time: 180 at "three hours", 225 when late
      const mins = FIN.keys([[C.req, 0], [C.three + 1.2, 180], [C.late, 180], [C.extra, 225]]);
      const th = (m) => (270 + m / 2) * Math.PI / 180;   // clock angle from 12 o'clock, clockwise
      const sector = (m0, m1) => { if (m1 <= m0 + 0.1) return "";
        const p = (m) => [300 * Math.sin(th(m)), -300 * Math.cos(th(m))], [x0, y0] = p(m0), [x1, y1] = p(m1);
        return `M0 0 L${x0.toFixed(1)} ${y0.toFixed(1)} A300 300 0 ${m1 - m0 > 360 ? 1 : 0} 1 ${x1.toFixed(1)} ${y1.toFixed(1)} Z`; };
      FIN.hook((t) => { const m = mins(t);
        $("hand").setAttribute("transform", `rotate(${270 + m / 2})`);
        $("arcA").setAttribute("d", sector(0, Math.min(m, 180)));
        $("arcR").setAttribute("d", sector(180, Math.max(180, m)));
        const h = 21 + Math.floor(m / 60), mm = Math.floor(m % 60), hh = h % 12 || 12;
        $("clk").textContent = `${hh}:${String(mm).padStart(2, "0")} ${h >= 24 || h < 12 ? "AM" : "PM"}`; });
      pop($("req"), C.req); pop($("three"), C.three); pop($("wait"), C.wait); pop($("late"), C.late); pop($("pays"), C.pays);
"""
    put("s04_clock", page("s04_clock", "The three hour discharge clock", round(end - start, 2), body, js,
                          tag="IRDAI MASTER CIRCULAR | PARA 16 · ILLUSTRATIVE TIMES"), start, end - start, cues)


SCENES = [s00_receipts, s01_letter, s01b_overstamp, s02_flow, s03_ring, s03b_family, s04_clock]

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for f in SCENES:
        if not only or f.__name__ in only:
            f()
