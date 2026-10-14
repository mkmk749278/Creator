#!/usr/bin/env python3
"""Visual engines v2 (owner's "Visual Engine Upgrade", 2026-10-14): programmatic scenes replace generic stock b-roll.

Six engines, each a set of HyperFrames compositions timed to the VO (build/timing.py):
  1 isometric hospital cutaway (Fern-style), 2 document x-ray rig with laser thread (Vox-style),
  3 proportionate-deduction bill slicer, 4 60-month moratorium shield, 5 discharge stopwatch + ledger,
  6 escalation war-room (circuit board, 4 nodes, Ombudsman constellation, CIO data, penalty meter) + cheat-sheet card.
Every number traces to claims.csv or tools/claim_math.py; invented family figures carry ILLUSTRATIVE.
Shared page shell, fonts, palette and helpers come from make_scenes.py.
Run: python3 projects/health-claim-trap/build/make_engines.py [ids...]; npm run vendor; lint/check/snapshot; render.
"""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_scenes import at, page, put, svg, OUT
from timing import L, sents

BP = """
.bp { position: absolute; inset: -60px; background:
  repeating-linear-gradient(0deg, rgba(56,189,248,.06) 0 1px, transparent 1px 60px),
  repeating-linear-gradient(90deg, rgba(56,189,248,.06) 0 1px, transparent 1px 60px),
  radial-gradient(ellipse at 50% 40%, rgba(19,37,74,.35) 0%, rgba(11,21,48,.7) 50%, rgba(5,10,24,.92) 100%); }
.glass { position: absolute; background: linear-gradient(160deg, rgba(30,41,59,.82), rgba(15,23,42,.9)); border: 2px solid rgba(56,189,248,.35);
  border-radius: 18px; box-shadow: 0 30px 70px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.08); color: var(--white); }
.t-k { font: 600 22px/1.2 Inter, Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); }
.t-v { font: 800 56px/1.05 Inter, Arial, sans-serif; color: var(--white); }
.mono { font-family: Inter, Arial, sans-serif; font-variant-numeric: tabular-nums; }
.ill { position: absolute; left: 64px; top: 48px; font: 800 20px/1 Inter, Arial, sans-serif; letter-spacing: .14em; color: #facc15;
  background: rgba(2,6,15,.7); padding: 10px 14px; border-radius: 6px; border-left: 4px solid #facc15; }
"""


def bp_page(sid, title, dur, body, js, tag="", css="", ill=""):
    """Blueprint grid over a blurred, slowly drifting hospital backdrop (owner review 2026-10-14: no flat blue voids);
    grain + vignette from the shell."""
    import shutil
    d = OUT / sid / "img"; d.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path(__file__).resolve().parents[1] / "assets/owner/backdrop_blur.jpg", d / "back.jpg")
    body = ('<div id="bimg" style="position:absolute; inset:-80px; background:url(img/back.jpg) center/cover; opacity:.6"></div>'
            '<div class="bp" id="bp" style="opacity:.85"></div>' + (f'<div class="ill">{ill}</div>' if ill else "") + body)
    js = 'tl.fromTo($("bimg"), { scale: 1.0, x: 0 }, { scale: 1.08, x: -40, duration: D.duration, ease: "none" }, 0);\n' + js
    js = 'tl.fromTo($("bp"), { x: 0, y: 0 }, { x: -60, y: -30, duration: D.duration, ease: "none" }, 0);\n' + js
    html = page(sid, title, dur, body, js, tag=tag, bg="", css=BP + css)
    return html.replace('<div class="fin-bg" style="background-image: url(\'\')"></div>\n      <div class="hc-grade"></div>', "")


def inr(v):
    """Indian digit grouping: 120000 -> ₹1,20,000."""
    s = str(int(v)); head, tail = s[:-3], s[-3:]
    while len(head) > 2:
        tail = head[-2:] + "," + tail; head = head[:-2]
    return "₹" + (head + "," + tail if head else tail)


def S(eid, k=0):
    return sents(eid)[k]


# ---------------- ENGINE 1: isometric hospital cutaway ----------------
C30, S30 = math.cos(math.pi / 6), 0.5


def iso(x, y, z):
    return (x - y) * C30, (x + y) * S30 - z


def poly(pts, **a):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    attrs = " ".join(f'{k.rstrip("_").replace("_", "-")}="{v}"' for k, v in a.items())
    return f'<polygon points="{d}" {attrs}/>'


def box(x, y, z, w, d, h, cls, idp=""):
    """Iso box faces (left, right, top) as SVG polygons, wireframe-styled by class."""
    P = lambda a, b, c: iso(x + a, y + b, z + c)
    left = [P(0, d, 0), P(w, d, 0), P(w, d, h), P(0, d, h)]
    right = [P(w, 0, 0), P(w, d, 0), P(w, d, h), P(w, 0, h)]
    top = [P(0, 0, h), P(w, 0, h), P(w, d, h), P(0, d, h)]
    g = f'<g class="{cls}" id="{idp}">' if idp else f'<g class="{cls}">'
    g += poly(left, class_="fl") + poly(right, class_="fr") + poly(top, class_="ft")
    # windows on both visible faces
    for i in range(6):
        wx = 18 + i * (w - 36) / 6
        g += poly([P(wx, d, 26), P(wx + 40, d, 26), P(wx + 40, d, h - 30), P(wx, d, h - 30)], class_="win")
    for i in range(4):
        wy = 18 + i * (d - 36) / 4
        g += poly([P(w, wy, 26), P(w, wy + 40, 26), P(w, wy + 40, h - 30), P(w, wy, h - 30)], class_="win")
    return g + "</g>"


def e1_hospital():
    sid = "e1_hospital"
    start, end = 0.0, L("E004")[1] + 0.3
    W, Dp, H = 560, 380, 120
    floors = "".join(box(0, 0, i * H, W, Dp, H - 8, f"floor f{i}", f"fl{i}") for i in range(4))
    # roof sign + ground grid
    gx = "".join(f'<line x1="{iso(-400, j, 0)[0]:.0f}" y1="{iso(-400, j, 0)[1]:.0f}" x2="{iso(1700, j, 0)[0]:.0f}" y2="{iso(1700, j, 0)[1]:.0f}"/>' for j in range(-400, 1300, 100))
    gy = "".join(f'<line x1="{iso(j, -400, 0)[0]:.0f}" y1="{iso(j, -400, 0)[1]:.0f}" x2="{iso(j, 1300, 0)[0]:.0f}" y2="{iso(j, 1300, 0)[1]:.0f}"/>' for j in range(-400, 1700, 100))
    hub = box(1100, -40, 0, 200, 200, 420, "hub", "hub")
    pipe_pts = [iso(W, Dp * 0.5, 40), iso(900, Dp * 0.5, 40), iso(900, 60, 40), iso(1100, 60, 40)]
    pipe = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pipe_pts)
    lab = lambda i, txt, col: (f'<g id="lab{i}" opacity="0"><line x1="{iso(0, Dp, i * H + 60)[0]:.0f}" y1="{iso(0, Dp, i * H + 60)[1]:.0f}" '
                               f'x2="{iso(0, Dp, i * H + 60)[0] - 160:.0f}" y2="{iso(0, Dp, i * H + 60)[1]:.0f}" stroke="{col}" stroke-width="3"/>'
                               f'<text x="{iso(0, Dp, i * H + 60)[0] - 170:.0f}" y="{iso(0, Dp, i * H + 60)[1] + 9:.0f}" text-anchor="end" fill="{col}" '
                               f'font-family="Inter, Arial, sans-serif" font-weight="800" font-size="30" letter-spacing="2">{txt}</text></g>')
    hx, hy = iso(1200, 60, 430)
    import random
    rnd = random.Random(7)
    stars = "".join(f'<circle cx="{rnd.uniform(-1400, 1600):.0f}" cy="{rnd.uniform(-1300, -500):.0f}" r="{rnd.uniform(1, 2.6):.1f}" fill="#cbd5e1" opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(90))
    body = f"""
      <svg id="world" viewBox="-960 -700 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px">
        <g id="cam">
          {stars}
          <g stroke="rgba(56,189,248,.12)" stroke-width="2">{gx}{gy}</g>
          <path id="pipe" d="{pipe}" fill="none" stroke="rgba(56,189,248,.35)" stroke-width="10" stroke-linecap="round"/>
          <path id="pulse" d="{pipe}" fill="none" stroke="#38bdf8" stroke-width="10" stroke-linecap="round" stroke-dasharray="30 170"/>
          {hub}
          <text x="{hx:.0f}" y="{hy - 20:.0f}" text-anchor="middle" fill="#f59e0b" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="30" letter-spacing="3">TPA PROCESSING HUB</text>
          {floors}
          
          <path id="ecg" d="" fill="none" stroke="#f87171" stroke-width="6" stroke-linejoin="round"/>
        </g>
      </svg>
      <div class="glass" id="inv" style="left:1180px; top:250px; width:600px; padding:30px 36px; opacity:0">
        <div class="t-k">Final bill · Sample City Hospital</div>
        <div class="t-v mono" id="amt" style="font-size:88px; margin-top:14px">₹0</div>
        <div class="t-k" style="margin-top:16px; color:#f59e0b">21:00 HRS · discharge papers ready</div>
      </div>
      <div class="chip amber" id="icu" style="left:1180px; top:200px; opacity:0">3F · Emergency · admitted</div>
      <div class="chip amber" id="lab3" style="left:1180px; top:120px; opacity:0">ICU / WARD</div>
      <div class="chip cyan" id="lab0" style="left:1180px; top:120px; opacity:0">1F · Billing · TPA desk</div>"""
    css = """
.floor .fl { fill: rgba(15,23,42,.92); stroke: rgba(56,189,248,.55); stroke-width: 2; }
.floor .fr { fill: rgba(19,37,74,.92); stroke: rgba(56,189,248,.55); stroke-width: 2; }
.floor .ft { fill: rgba(30,58,95,.6); stroke: rgba(56,189,248,.7); stroke-width: 2; }
.win { fill: rgba(56,189,248,.16); stroke: none; }
.hub .fl { fill: rgba(30,20,6,.9); stroke: rgba(245,158,11,.6); stroke-width: 2; } .hub .fr { fill: rgba(45,30,8,.9); stroke: rgba(245,158,11,.6); stroke-width: 2; }
.hub .ft { fill: rgba(245,158,11,.25); stroke: rgba(245,158,11,.8); stroke-width: 2; } .hub .win { fill: rgba(245,158,11,.2); }
"""
    s3 = S("E003"); s4 = sents("E004")
    cues = dict(icu=s3["start"], adm=S("E003", 1)["start"], bill=s4[0]["start"], ready=s4[1]["start"], amt=s4[2]["start"], amt_end=s4[2]["end"])
    # camera targets (world coords of floor centres): floor i centre
    fc = lambda i: iso(W / 2, Dp / 2, i * H + H / 2)
    f3, f0 = fc(3), fc(0)
    tr = lambda f, s, tx, ty: (tx / s - f[0], ty / s - f[1])      # world point f to screen (tx, ty) at scale s
    wide = (-380, -60)
    a3 = tr(f3, 1.7, 0, -160); a0 = tr(f0, 1.45, -230, -40); a0b = tr(f0, 1.55, -240, -40)
    js = f"""
      const cam = $("cam");
      const keyS = FIN.keys([[0, 0.5], [6, 0.7], [C.icu, 0.75], [C.icu + 1.6, 1.7], [C.bill - 0.2, 1.7], [C.bill + 1.8, 1.45], [D.duration, 1.55]]);
      const keyX = FIN.keys([[0, {wide[0]}], [C.icu, {wide[0] + 40}], [C.icu + 1.6, {a3[0]:.0f}], [C.bill - 0.2, {a3[0]:.0f}], [C.bill + 1.8, {a0[0]:.0f}], [D.duration, {a0b[0]:.0f}]]);
      const keyY = FIN.keys([[0, 380], [5, {wide[1]}], [C.icu, {wide[1] + 20}], [C.icu + 1.6, {a3[1]:.0f}], [C.bill - 0.2, {a3[1]:.0f}], [C.bill + 1.8, {a0[1]:.0f}], [D.duration, {a0b[1]:.0f}]]);
      FIN.hook((t) => {{ cam.setAttribute("transform", `scale(${{keyS(t)}}) translate(${{keyX(t)}} ${{keyY(t)}})`);
        $("pulse").setAttribute("stroke-dashoffset", String(-t * 260));
        // ICU telemetry line drawn from time only
        if (t > C.icu) {{ const [cx, cy] = [{f3[0] - 140:.0f}, {f3[1] - 170:.0f}]; let d = "";
          for (let i = 0; i <= 60; i++) {{ const x = cx + i * 5, ph = (i + t * 30) % 20; const y = cy - (ph > 9 && ph < 11 ? 60 * Math.sin((ph - 9) * Math.PI) : 0) * (t < C.adm + 2 ? 1 : 0.5);
            d += (i ? " L" : "M") + x.toFixed(1) + " " + y.toFixed(1); }} $("ecg").setAttribute("d", d); }} }});
      // ICU floor glows amber, billing floor cyan
      tl.to("#fl3 .ft, #fl3 .fl, #fl3 .fr", {{ fill: "rgba(245,158,11,.55)", duration: 0.4, yoyo: true, repeat: 5 }}, C.icu);
      tl.to("#fl3 .win", {{ fill: "rgba(245,158,11,.75)", duration: 0.4 }}, C.icu);
      pop($("lab3"), C.icu + 0.3, {{ opacity: 0 }}); pop($("icu"), C.adm);
      out($("icu"), C.bill - 0.5); out($("lab3"), C.bill);
      tl.to("#fl0 .win", {{ fill: "rgba(56,189,248,.8)", duration: 0.4 }}, C.bill + 0.6);
      tl.to("#fl0 .ft", {{ fill: "rgba(56,189,248,.45)", duration: 0.4 }}, C.bill + 0.6);
      pop($("lab0"), C.bill + 0.8, {{ opacity: 0 }});
      pop($("inv"), C.ready, {{ opacity: 0, y: 40, rotationY: -30 }});
      FIN.bind($("amt"), FIN.keys([[C.amt, 0], [C.amt_end, 450000]]), (v) => FIN.inr(Math.round(v / 1000) * 1000));
"""
    put(sid, bp_page(sid, "Isometric hospital cutaway", round(end - start, 2), body, js, tag="ILLUSTRATIVE · SAMPLE HOSPITAL", css=css,
                     ill="ILLUSTRATION"), start, end - start, cues)


def e0_ledger():
    sid = "e0_ledger"; s = sents("E002")
    start, end = s[0]["start"] - 0.25, s[2]["end"] + 0.4
    yrs = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    cards = "".join(f"""
        <div class="glass pc" id="c{i}" style="left:{70 + i * 300}px; top:330px; width:280px; height:380px; padding:28px">
          <div class="t-k" style="font-size:22px">Policy year</div><div style="font:800 46px/1.1 Inter,Arial,sans-serif; margin-top:10px">{y}</div>
          <div style="font:800 54px/1 Inter,Arial,sans-serif; color:#38bdf8; margin-top:60px">₹35,000</div>
          <div class="t-k" id="ok{i}" style="margin-top:50px; color:#4ade80; opacity:0; font-size:24px">✓ Renewed</div>
        </div>""" for i, y in enumerate(yrs))
    links = "".join(f'<div class="lk" id="l{i}" style="left:{345 + i * 300}px"></div>' for i in range(5))
    body = cards + links + """
        <div class="glass" style="left:70px; top:110px; padding:26px 34px" id="tot"><div class="t-k">Total premium paid</div><div class="t-v mono" id="sum" style="font-size:80px">₹0</div></div>
        <div class="chip green" id="lapse" style="left:1440px; top:150px; opacity:0; font-size:52px">0 LAPSES</div>"""
    css = ".lk { position: absolute; top: 515px; width: 40px; height: 12px; border-radius: 6px; background: #38bdf8; box-shadow: 0 0 20px #38bdf8; transform-origin: 0 50%; }"
    cues = dict(amt=s[0]["start"], yrs=s[1]["start"], paid=s[2]["start"])
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
      pop($("tot"), C.amt);
      for (let i = 0; i < 6; i++) pop($("c" + i), C.amt + 0.6 + i * 0.45, { opacity: 0, y: 80, rotationX: 40 });
      for (let i = 0; i < 5; i++) tl.fromTo($("l" + i), { scaleX: 0 }, { scaleX: 1, duration: 0.25 }, C.yrs + i * 0.4);
      for (let i = 0; i < 6; i++) pop($("ok" + i), C.yrs + i * 0.4, { opacity: 0 });
      FIN.bind($("sum"), FIN.keys([[C.amt + 0.6, 0], [C.amt + 3.3, 210000]]), (v) => FIN.inr(Math.round(v / 5000) * 5000));
      pop($("lapse"), C.paid, { opacity: 0, scale: 1.6 });
"""
    put(sid, bp_page(sid, "Six years, zero lapses", round(end - start, 2), body, js, tag="ILLUSTRATIVE FAMILY", css=css), start, end - start, cues)


def e2_shock():
    """E006 shockwave over the bill: family balance vs midnight shortfall (illustrative family)."""
    sid = "e2_shock"; s = sents("E006")
    start, end = s[0]["start"] - 0.3, s[1]["end"] + 0.4
    body = """
        <div class="glass" id="bill" style="left:660px; top:330px; width:600px; padding:30px; text-align:center; border-color:rgba(220,38,38,.7)">
          <div class="t-k">Hospital bill</div><div class="t-v mono" style="font-size:96px; color:#f87171">₹4,50,000</div></div>
        <div class="ring" id="r1"></div><div class="ring" id="r2"></div>
        <div class="glass" id="bal" style="left:160px; top:700px; width:520px; padding:24px"><div class="t-k">In the bank tonight</div><div class="t-v mono" style="color:#4ade80">₹62,000</div></div>
        <div class="glass" id="gap" style="left:1240px; top:700px; width:520px; padding:24px; border-color:rgba(220,38,38,.7)"><div class="t-k">Short by midnight</div><div class="t-v mono" id="g" style="color:#f87171">₹0</div></div>"""
    css = ".ring { position:absolute; left:960px; top:430px; width:40px; height:40px; margin:-20px; border-radius:50%; border:6px solid rgba(220,38,38,.8); opacity:0; }"
    cues = dict(drop=s[0]["start"], panic=s[1]["start"])
    js = """
      tl.fromTo($("stage"), { scale: 1.08 }, { scale: 1, duration: D.duration, ease: "none" }, 0);
      pop($("bill"), 0.05, { opacity: 0, scale: 1.3 });
      ["r1", "r2"].forEach((id, i) => tl.fromTo($(id), { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 40, duration: 1.4, ease: "power2.out" }, C.drop + i * 0.5));
      pop($("bal"), 0.15, { opacity: 0, x: -60 }); pop($("gap"), 0.3, { opacity: 0, x: 60 });
      FIN.bind($("g"), FIN.keys([[C.drop, 0], [C.drop + 1.2, 388000]]), (v) => FIN.inr(Math.round(v / 1000) * 1000));
"""
    put(sid, bp_page(sid, "The midnight shortfall", round(end - start, 2), body, js, tag="ILLUSTRATIVE FAMILY", css=css), start, end - start, cues)


def e2_drain():
    sid = "e2_drain"; s = S("E007")
    start, end = s["start"] - 0.3, L("E007")[1] + 0.35
    cues = dict(banks=at("E007", "banks"), fd=at("E007", "break your"), borrow=at("E007", "borrow"), card=at("E007", "swipe"), out=at("E007", "just to get"))
    body = """
        <div class="glass col" id="p1" style="left:110px"><div class="t-k">1 · Fixed deposit</div>
          <div class="t-v mono" id="fd" style="margin-top:20px">₹1,50,000</div><div class="t-k" id="fdx" style="color:#f87171; margin-top:18px; opacity:0">Broken early · penalty</div>
          <div class="bar"><div class="fill" id="fdb"></div></div></div>
        <div class="glass col" id="p2" style="left:690px"><div class="t-k">2 · Message to a relative</div>
          <div class="msg" id="m1">Anna, can you send money tonight? Hospital bill. Will return soon.</div>
          <div class="msg me" id="m2">Sending ₹1,00,000 now</div></div>
        <div class="glass col" id="p3" style="left:1270px"><div class="t-k">3 · Credit card</div>
          <div class="card" id="cc"><div style="font:800 24px Inter,Arial,sans-serif; letter-spacing:.2em">•••• •••• •••• 4821</div><div style="margin-top:56px" class="t-k">Hospital payment</div></div>
          <div class="t-v mono" id="ccv" style="margin-top:22px; color:#f87171; opacity:0">− ₹1,38,000</div><div class="t-k" id="cci" style="color:#f59e0b; opacity:0">Card interest starts</div></div>
        <div class="chip red" id="night" style="left:740px; top:110px">Night · banks closed</div>"""
    css = """.col { top: 230px; width: 540px; height: 620px; padding: 32px; }
.bar { position: absolute; left: 32px; right: 32px; bottom: 50px; height: 18px; border-radius: 9px; background: rgba(148,163,184,.2); overflow: hidden; }
.fill { width: 100%; height: 100%; background: #4ade80; transform-origin: 0 50%; }
.msg { margin-top: 30px; padding: 20px 24px; border-radius: 20px 20px 20px 4px; background: #1e293b; font: 600 30px/1.35 Inter, Arial, sans-serif; color: #e2e8f0; }
.msg.me { margin-left: 120px; border-radius: 20px 20px 4px 20px; background: #0e7490; }
.card { margin-top: 28px; height: 250px; border-radius: 22px; padding: 30px; background: linear-gradient(135deg, #1e3a5f, #0f172a); border: 2px solid rgba(255,255,255,.18); }"""
    js = """
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.04, duration: D.duration, ease: "none" }, 0);
      pop($("night"), 0.05);
      pop($("p1"), C.fd - 0.2, { opacity: 0, y: 60 }); pop($("fdx"), C.fd + 0.6, { opacity: 0 });
      tl.to($("fdb"), { scaleX: 0.08, background: "#f87171", duration: 0.9 }, C.fd + 0.4);
      FIN.bind($("fd"), FIN.keys([[C.fd + 0.4, 150000], [C.fd + 1.3, 12000]]), (v) => FIN.inr(Math.round(v / 1000) * 1000));
      pop($("p2"), C.borrow - 0.2, { opacity: 0, y: 60 }); pop($("m1"), C.borrow + 0.2); pop($("m2"), C.borrow + 1.2);
      pop($("p3"), C.card - 0.2, { opacity: 0, y: 60 });
      tl.fromTo($("cc"), { rotationY: 0 }, { rotationY: 360, duration: 0.8, ease: "power2.inOut" }, C.card + 0.1);
      pop($("ccv"), C.card + 0.8, { opacity: 0 }); pop($("cci"), C.out, { opacity: 0 });
"""
    put(sid, bp_page(sid, "Three ways the savings drain", round(end - start, 2), body, js, tag="SIMULATION · ILLUSTRATIVE FAMILY", css=css), start, end - start, cues)


def e3_scale():
    sid = "e3_scale"; s = S("E008")
    start, end = s["start"] - 0.3, s["end"] + 0.9
    blocks = "".join(f'<div class="blk" id="b{i}" style="left:{20 + (i % 3) * 120}px; top:{-100 - (i // 3) * 74}px">₹35K</div>' for i in range(6))
    body = f"""
        <div id="beam" style="position:absolute; left:460px; top:520px; width:1000px; height:16px; border-radius:8px; background:#94a3b8; transform-origin:50% 50%">
          <div class="pan" style="left:-40px">{blocks}<div class="lbl" style="color:#4ade80">6 years · ₹2,10,000</div></div>
          <div class="pan" style="left:680px"><div class="blk red" id="den" style="left:40px; top:-150px; width:280px; height:130px">DENIED</div><div class="lbl" style="color:#f87171">One letter</div></div>
        </div>
        <div style="position:absolute; left:944px; top:528px; width:32px; height:330px; background:linear-gradient(#94a3b8,#475569); border-radius:6px"></div>
        <div style="position:absolute; left:820px; top:850px; width:280px; height:26px; background:#475569; border-radius:10px"></div>"""
    css = """.pan { position: absolute; top: 16px; width: 360px; height: 0; }
.blk { position: absolute; width: 110px; height: 66px; border-radius: 10px; background: linear-gradient(#22c55e, #15803d); color: #fff;
  font: 800 26px/66px Inter, Arial, sans-serif; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,.4); }
.blk.red { background: linear-gradient(#ef4444, #991b1b); font-size: 54px; line-height: 130px; letter-spacing: .08em; }
.lbl { position: absolute; top: 30px; width: 400px; font: 800 30px/1 Inter, Arial, sans-serif; letter-spacing: .06em; }"""
    cues = dict(ask=s["start"], need=at("E008", "abandon"))
    js = """
      for (let i = 0; i < 6; i++) pop($("b" + i), 0.1 + i * 0.18, { opacity: 0, y: -200 });
      tl.fromTo($("beam"), { rotation: -9 }, { rotation: -9, duration: 0.1 }, 0);
      tl.fromTo($("den"), { opacity: 0, y: -500 }, { opacity: 1, y: 0, duration: 0.45, ease: "power4.in" }, C.need - 0.2);
      tl.to($("beam"), { rotation: 14, duration: 0.6, ease: "back.out(2)" }, C.need + 0.25);
      tl.fromTo($("stage"), { y: 0 }, { y: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.need + 0.25);
"""
    put(sid, bp_page(sid, "The six-year paradox", round(end - start, 2), body, js, tag="ILLUSTRATIVE FAMILY", css=css), start, end - start, cues)


def e4_pillars():
    sid = "e4_pillars"; s = sents("E011")
    start, end = s[0]["start"] - 0.3, L("E012")[1] + 0.4
    F = [("1", "Who really says no", "The TPA middleman"), ("2", "The 5-year rule", "IRDAI · 2024"), ("3", "The Ombudsman", "76% of settled or decided cases")]
    body = "".join(f"""
        <div class="glass fo" id="f{i}" style="left:{90 + i * 590}px">
          <div class="tab"></div><div style="font:800 120px/1 Inter,Arial,sans-serif; color:rgba(56,189,248,.35)">{n}</div>
          <div style="font:800 58px/1.1 Inter,Arial,sans-serif; margin-top:30px">{a}</div><div class="t-k" style="margin-top:22px; color:#38bdf8; font-size:28px">{b}</div></div>"""
                   for i, (n, a, b) in enumerate(F)) + '<div class="glass nx" id="nos" style="left:300px"><div class="xx">✕</div><div class="nxt">No shouting</div></div><div class="glass nx" id="nos2" style="left:1020px"><div class="xx">✕</div><div class="nxt">No policy selling</div></div>'
    css = ".nx { top: 300px; width: 600px; height: 420px; text-align: center; padding-top: 50px; } .xx { font: 800 170px/1 Inter,Arial,sans-serif; color: #f87171; } .nxt { margin-top: 30px; font: 800 56px/1 Inter,Arial,sans-serif; } .fo { top: 270px; width: 560px; height: 560px; padding: 46px; transform-style: preserve-3d; } .tab { position:absolute; left:30px; top:-30px; width:160px; height:34px; border-radius:10px 10px 0 0; background:rgba(56,189,248,.35); }"
    cues = dict(nos=s[0]["start"], real=at("E011", "real", k=1), who=at("E011", "who really", k=1), step=at("E011", "step-by-step", k=1), dive=L("E012")[0])
    js = """
      pop($("nos"), C.nos + 0.2, { opacity: 0, scale: 0.8 }); pop($("nos2"), C.nos + 1.6, { opacity: 0, scale: 0.8 }); out($("nos"), C.real - 0.3); out($("nos2"), C.real - 0.3);
      [C.real, C.who + 0.6, C.step].forEach((t, i) => pop($("f" + i), t, { opacity: 0, y: 120, rotationX: 55 }));
      tl.to([$("f1"), $("f2")], { opacity: 0, duration: 0.4 }, C.dive);
      tl.to($("stage"), { scale: 2.6, x: 1450, y: 150, duration: 1.8, ease: "power3.in" }, C.dive + 0.4);
      tl.to($("f0"), { opacity: 0, duration: 0.4 }, D.duration - 0.45);
"""
    put(sid, bp_page(sid, "Three files: the blueprint", round(end - start, 2), body, js, tag="IRDAI RULES · CIO ANNUAL REPORT 2024-25", css=css), start, end - start, cues)


def e1b_overstamp():
    """E009: cyan laser slices the denial stamp, revealing the gold moratorium core (replaces s01b)."""
    sid = "e1b_overstamp"; s = S("E009")
    start, end = s["start"] - 0.3, s["end"] + 0.5
    body = """
        <div id="paper" style="position:absolute; left:410px; top:90px; width:1100px; height:900px; background:#f3efe6; border-radius:8px; box-shadow:0 40px 90px rgba(0,0,0,.7); transform:rotate(2deg); padding:60px 70px; color:#334155">
          <div style="font:800 34px/1 Inter,Arial,sans-serif; letter-spacing:.08em; color:#0f172a">SAMPLE HEALTH INSURANCE CO. · CLAIM DECISION</div>
          <div style="margin-top:18px; height:4px; background:#0f172a"></div>
          <div style="font:600 28px/1.6 Inter,Arial,sans-serif; margin-top:30px">Policy in force since 2020 · Cashless request: hospitalisation<br>Decision: <b style="color:#b91c1c">not approved</b><br>Reason: non-disclosure of a pre-existing condition</div>
          <div class="ln" style="width:92%"></div><div class="ln" style="width:84%"></div><div class="ln" style="width:88%"></div><div class="ln" style="width:60%"></div>
          <div class="ln" style="width:90%; margin-top:260px"></div><div class="ln" style="width:40%"></div></div>
        <div class="stampx" id="top">CASHLESS DENIED</div><div class="stampx" id="bot">CASHLESS DENIED</div>
        <div id="laser" style="position:absolute; left:-200px; top:532px; width:2400px; height:8px; background:#38bdf8; box-shadow:0 0 30px 8px #38bdf8; opacity:0; transform:rotate(-8deg)"></div>
        <div id="core" style="position:absolute; left:360px; top:430px; width:1200px; text-align:center; opacity:0">
          <div style="font:800 86px/1.05 Inter,Arial,sans-serif; color:#facc15; text-shadow:0 0 40px rgba(250,204,21,.6)">60-MONTH MORATORIUM</div>
          <div class="t-k" style="margin-top:22px; font-size:30px; color:#fde68a">After 5 years: not contestable for non-disclosure</div>
          <div style="display:flex; gap:4px; margin:40px auto 0; width:1100px">""" + "".join(f'<div class="mo" id="mo{i}"></div>' for i in range(60)) + """</div>
          <div class="t-k" style="margin-top:14px; color:#fde68a">60 months · your policy since 2020</div></div>"""
    css = """.stampx { position: absolute; left: 360px; top: 400px; width: 1200px; height: 270px; border: 14px solid #dc2626; border-radius: 22px; color: #dc2626;
  font: 800 118px/242px Inter, Arial, sans-serif; text-align: center; letter-spacing: .02em; white-space: nowrap; transform: rotate(-8deg); background: rgba(40,6,6,.4); }
#top { clip-path: polygon(0 0, 100% 0, 100% 50%, 0 50%); } #bot { clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%); }
.ln { height:16px; margin-top:22px; border-radius:8px; background:rgba(51,65,85,.18); }
.mo { flex:1; height:40px; border-radius:4px; background:rgba(250,204,21,.18); }"""
    cues = dict(rule=at("E009", "legal rule"), illegal=at("E009", "illegal"), five=at("E009", "five years"))
    js = """
      pop($("top"), 0.1, { opacity: 0, scale: 1.4 }); pop($("bot"), 0.1, { opacity: 0, scale: 1.4 });
      tl.fromTo($("laser"), { opacity: 0, scaleX: 0, transformOrigin: "0 50%" }, { opacity: 1, scaleX: 1, duration: 0.5, ease: "power2.in" }, C.rule);
      tl.to($("top"), { y: -260, rotation: -14, opacity: 0.25, duration: 0.9, ease: "power2.out" }, C.illegal);
      tl.to($("bot"), { y: 260, rotation: -2, opacity: 0.25, duration: 0.9, ease: "power2.out" }, C.illegal);
      tl.to($("laser"), { opacity: 0, duration: 0.4 }, C.illegal + 0.4);
      pop($("paper"), 0.05, { opacity: 0, y: 80, rotation: 6 });
      tl.to($("paper"), { opacity: 0.18, scale: 0.94, duration: 0.8 }, C.illegal + 0.2);
      pop($("core"), C.illegal + 0.3, { opacity: 0, scale: 0.8 });
      for (let i = 0; i < 60; i++) tl.to($("mo" + i), { background: "#facc15", boxShadow: "0 0 14px rgba(250,204,21,.7)", duration: 0.05 }, C.five + i * 0.04);
      tl.fromTo($("stage"), { scale: 1.12, x: 40 }, { scale: 1.0, x: 0, duration: D.duration, ease: "power1.out" }, 0);
"""
    put(sid, bp_page(sid, "The moratorium core", round(end - start, 2), body, js, tag="SIMULATED LETTER · IRDAI INSURANCE PRODUCTS REGULATIONS | 2024", css=css), start, end - start, cues)


CH1 = [e1_hospital, e0_ledger, e2_shock, e2_drain, e3_scale, e1b_overstamp, e4_pillars]
ENGINES = list(CH1)


# ---------------- CHAPTER 2 ----------------
def e5_funnel():
    """E013-E016: claims leave hospitals; 69 of 100 route through the amber TPA hub; the 'govt doctor' badge peels off."""
    sid = "e5_funnel"
    start, end = S("E013")["start"] - 0.25, L("E016")[1] + 0.3
    import random
    rnd = random.Random(11)
    dots = []
    for i in range(100):
        tpa = i < 69
        dots.append(dict(tpa=tpa, d=round(rnd.uniform(0, 1), 3), y=round(rnd.uniform(-60, 60), 1)))
    body = f"""
      <svg viewBox="0 0 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px">
        <path d="M330 540 C 700 540, 760 330, 1080 330" stroke="rgba(245,158,11,.35)" stroke-width="70" fill="none" stroke-linecap="round"/>
        <path d="M330 540 C 700 540, 760 760, 1080 760" stroke="rgba(56,189,248,.25)" stroke-width="40" fill="none" stroke-linecap="round"/>
        <path d="M1240 330 C 1400 330, 1450 540, 1600 540" stroke="rgba(245,158,11,.35)" stroke-width="40" fill="none"/>
        <path d="M1240 760 C 1400 760, 1450 540, 1600 540" stroke="rgba(56,189,248,.25)" stroke-width="30" fill="none"/>
        <g id="dots"></g>
      </svg>
      <div class="node2" id="h" style="left:150px; top:420px">{svg("hosp", 120)}<div class="t-k" style="margin-top:12px">Hospital</div></div>
      <div class="node2 amberb" id="tp" style="left:1060px; top:210px">{svg("file", 120)}<div class="t-k" style="margin-top:12px; color:#f59e0b">TPA</div></div>
      <div class="node2" id="ih" style="left:1060px; top:640px; transform:scale(.8)">{svg("person", 100)}<div class="t-k" style="margin-top:12px">Insurer's own team</div></div>
      <div class="node2 cyanb" id="ins" style="left:1600px; top:420px">{svg("bank", 120)}<div class="t-k" style="margin-top:12px; color:#38bdf8">Insurance company</div></div>
      <div class="chip amber" id="mid" style="left:1290px; top:120px; opacity:0">Middleman: Third Party Administrator</div>
      <div class="badge" id="badge"><span id="bt">GOVT MEDICAL BOARD?</span></div>
      <div class="chip cyan" id="real" style="left:700px; top:120px; opacity:0">A company hired &amp; paid by the insurer</div>
      <div class="glass" id="stat" style="left:640px; top:860px; padding:20px 30px; opacity:0"><span class="t-v mono" id="n" style="color:#f59e0b">0</span>
        <span class="t-k" style="margin-left:14px">of 100 claims settled via TPAs (69%)</span></div>"""
    css = """.node2 { position:absolute; width:260px; text-align:center; color:var(--white); padding:30px 0; border-radius:26px; background:rgba(15,23,42,.9); border:3px solid rgba(148,163,184,.4); }
.amberb { border-color: rgba(245,158,11,.8); color:#f59e0b; box-shadow: 0 0 60px rgba(245,158,11,.25); } .cyanb { border-color: rgba(56,189,248,.7); color:#38bdf8; }
.badge { position:absolute; left:1000px; top:150px; padding:16px 24px; border-radius:12px; background:#e2e8f0; color:#0f172a; font:800 30px/1 Inter,Arial,sans-serif; letter-spacing:.06em; opacity:0; transform-origin: 0 0; }"""
    s15 = sents("E015")
    cues = dict(q=S("E013")["start"], think=S("E014")["start"], tpa=S("E014", 1)["start"], myth=s15[0]["start"], no=s15[1]["start"],
                paid=s15[2]["start"], seven=S("E016")["start"])
    js = f"""
      const DOTS = {json.dumps(dots)}, g = $("dots");
      const P0 = [330, 540], A = [[700, 540], [760, 330], [1080, 330]], B = [[700, 540], [760, 760], [1080, 760]];
      const bez = (p, q, r, s, u) => p.map((_, i) => (1-u)**3*p[i] + 3*(1-u)**2*u*q[i] + 3*(1-u)*u*u*r[i] + u**3*s[i]);
      const els = DOTS.map((d) => {{ const c = document.createElementNS("http://www.w3.org/2000/svg", "circle"); c.setAttribute("r", 7);
        c.setAttribute("fill", d.tpa ? "#f59e0b" : "#38bdf8"); g.appendChild(c); return c; }});
      FIN.hook((t) => {{ DOTS.forEach((d, i) => {{ const t0 = C.think + 0.2 + d.d * 4; const u = Math.min(1, Math.max(0, (t - t0) / 1.6));
        const path = d.tpa ? A : B; const [x, y] = bez(P0, path[0], path[1], path[2], u);
        els[i].setAttribute("cx", x.toFixed(1)); els[i].setAttribute("cy", (y + d.y * (1 - Math.abs(2*u - 1))).toFixed(1));
        els[i].setAttribute("opacity", t < t0 ? 0 : (u >= 1 ? 0.0 : 0.9)); }}); }});
      ["h", "ins"].forEach((id, i) => pop($(id), 0.1 + i * 0.3, {{ opacity: 0, scale: 0.7 }}));
      pop($("tp"), C.think + 0.6, {{ opacity: 0, scale: 0.7 }}); pop($("ih"), C.think + 0.9, {{ opacity: 0 }});
      tl.to($("ins"), {{ boxShadow: "0 0 80px rgba(56,189,248,.6)", duration: 0.5, yoyo: true, repeat: 1 }}, C.think + 0.3);
      tl.to($("tp"), {{ scale: 1.12, duration: 0.4 }}, C.tpa); pop($("mid"), C.tpa + 0.4, {{ opacity: 0 }});
      out($("mid"), C.myth - 0.3);
      tl.fromTo($("badge"), {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4 }}, C.myth);
      tl.to($("badge"), {{ rotation: 18, y: 300, opacity: 0, duration: 0.7, ease: "power2.in" }}, C.no + 0.1);
      pop($("real"), C.paid, {{ opacity: 0 }}); out($("real"), C.seven - 0.2);
      pop($("stat"), C.seven, {{ opacity: 0 }});
      FIN.bind($("n"), FIN.keys([[C.seven + 0.1, 0], [C.seven + 1.6, 69]]), (v) => Math.round(v));
      tl.fromTo($("stage"), {{ scale: 1 }}, {{ scale: 1.04, duration: D.duration, ease: "none" }}, 0);
"""
    put(sid, bp_page(sid, "The 70 percent middleman funnel", round(end - start, 2), body, js, tag="IRDAI ANNUAL REPORT 2024-25 · IRDAI TPA REGULATIONS", css=css), start, end - start, cues)


def e6_lock():
    sid = "e6_lock"; s = S("E017")
    start, end = s["start"] - 0.25, s["start"] + 4.6
    body = f"""
      <div class="glass" style="left:200px; top:300px; width:560px; height:480px; padding:40px; text-align:center" id="desk">
        <div class="t-k">TPA desk</div><div style="color:#f59e0b; margin-top:30px">{svg("file", 120)}</div>
        <div id="btn" style="margin:40px auto 0; width:300px; padding:26px; border-radius:18px; background:#991b1b; font:800 44px/1 Inter,Arial,sans-serif; letter-spacing:.1em">REJECT</div></div>
      <svg viewBox="0 0 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px"><path id="wire" d="M760 540 L1150 540" stroke="#f87171" stroke-width="8" stroke-dasharray="20 16" fill="none"/></svg>
      <div class="lock" id="lock"><div class="shackle"></div><div class="lbody">🔒</div></div>
      <div class="glass" id="crc" style="left:1260px; top:330px; width:520px; padding:34px; border-color:rgba(56,189,248,.7); opacity:0">
        <div class="t-k" style="color:#38bdf8">Para 17(a)</div><div style="font:800 40px/1.2 Inter,Arial,sans-serif; margin-top:14px">Rejection needs the insurer's Claims Review Committee</div></div>"""
    css = """.lock { position:absolute; left:1080px; top:440px; width:150px; height:190px; opacity:0; }
.shackle { position:absolute; left:30px; top:0; width:90px; height:100px; border:16px solid #38bdf8; border-bottom:0; border-radius:50px 50px 0 0; }
.lbody { position:absolute; left:0; top:80px; width:150px; height:110px; border-radius:18px; background:#0284c7; font-size:0; box-shadow:0 0 50px rgba(56,189,248,.6); }"""
    cues = dict(rule=s["start"], cr=at("E017", "approval"))
    js = """
      pop($("desk"), 0.1, { opacity: 0, x: -60 });
      tl.to($("btn"), { scale: 0.92, duration: 0.12, yoyo: true, repeat: 1 }, C.rule + 0.6);
      tl.fromTo($("wire"), { strokeDashoffset: 300, opacity: 0 }, { strokeDashoffset: 0, opacity: 1, duration: 0.6 }, C.rule + 0.8);
      tl.fromTo($("lock"), { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power4.in" }, C.cr - 0.6);
      tl.to($("wire"), { stroke: "#64748b", duration: 0.3 }, C.cr - 0.3);
      tl.to($("btn"), { background: "#334155", duration: 0.3 }, C.cr - 0.3);
      pop($("crc"), C.cr, { opacity: 0, x: 60 });
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "The rejection lock", round(end - start, 2), body, js, tag="IRDAI MASTER CIRCULAR | PARA 17", css=css), start, end - start, cues)


XRAY = """<svg viewBox="0 0 300 600" width="300" height="600"><defs><filter id="gl"><feGaussianBlur stdDeviation="3"/></filter></defs>
  <rect width="300" height="600" fill="#020617"/><g fill="none" stroke="#cbd5e1" stroke-width="22" stroke-linecap="round" opacity=".85" filter="url(#gl)">
  <path d="M130 40 C 120 160, 128 250, 132 290"/><path d="M140 330 C 150 420, 146 500, 150 570"/><path d="M190 60 C 185 200, 190 400, 196 560" stroke-width="12"/></g>
  <path d="M110 300 L150 310 L128 322 L165 330" stroke="#f87171" stroke-width="5" fill="none"/></svg>"""


def e7_dossier():
    sid = "e7_dossier"
    start, end = S("E017", 1)["start"] - 0.25, L("E021")[1] + 0.3
    s18, s19, s20, s21 = sents("E018"), sents("E019"), sents("E020"), sents("E021")
    clip = lambda i, code, name: f"""<div class="clip" id="k{i}" style="left:{180 + i * 560}px"><div class="clamp"></div>
        <div class="t-k" style="color:#f87171">Excuse {i + 1}</div><div style="font:800 40px/1.15 Inter,Arial,sans-serif; margin-top:16px; color:#0f172a">{name}</div>
        <div class="lines"></div></div>"""
    body = f"""
      <div id="sec1">{clip(0, "", "Non-disclosure")}{clip(1, "", "Not medically necessary")}{clip(2, "", "Room rent limit")}</div>
      <div id="sec2" style="opacity:0">
        <div class="glass" id="xr" style="left:120px; top:180px; padding:20px">{XRAY}<div class="t-k" style="margin-top:10px">Fracture · right leg</div></div>
        <div class="paper2" id="sheet" style="left:560px; top:140px; width:620px; height:780px; transform: perspective(1400px) rotateY(-10deg) rotateX(6deg)">
          <div class="t-k" style="color:#334155">Case sheet · admission notes</div>
          <div class="row2">Complaint: fall, right leg pain</div><div class="row2">Diagnosis: fracture, right tibia</div>
          <div class="row2" style="margin-top:30px">Past history:</div><div class="hand2" id="typed"></div>
          <div id="scan" style="position:absolute; left:0; right:0; top:0; height:6px; background:#f87171; box-shadow:0 0 24px #f87171; opacity:0"></div></div>
        <div class="paper2" id="form" style="left:1260px; top:240px; width:560px; height:600px; opacity:0; transform: perspective(1400px) rotateY(12deg)">
          <div class="t-k" style="color:#334155">Proposal form · 2020</div>
          <div class="row2 sm">Diabetes <b>☐ Yes ☑ No</b></div><div class="row2 sm" id="htn">High blood pressure <b>☐ Yes ☑ No</b></div><div class="row2 sm">Thyroid <b>☐ Yes ☑ No</b></div>
          <div id="ring" style="position:absolute; left:20px; top:138px; width:520px; height:70px; border:6px solid #f87171; border-radius:40px; opacity:0"></div>
          <div class="stamp red" id="den" style="left:50px; top:380px; font-size:46px; transform:rotate(-10deg); opacity:0">Cashless denied</div></div>
        <svg viewBox="0 0 1920 1080" style="position:absolute; inset:0; width:1920px; height:1080px; pointer-events:none">
          <path id="thread" d="M1000 520 C 1150 380, 1200 330, 1300 420" stroke="#f87171" stroke-width="6" fill="none" style="filter: drop-shadow(0 0 10px #f87171)"/></svg>
      </div>
      <div id="sec3" style="opacity:0">
        <div class="gate" style="left:220px">Mild BP</div><div class="neq" id="neq">≠</div><div class="gate" style="left:1180px">Broken leg · dengue</div>
        <div class="glass" id="yrs" style="left:360px; top:720px; width:1200px; padding:26px 34px; opacity:0">
          <div style="display:flex; gap:10px" id="ybar">{"".join(f'<div class="yc" id="y{i}">Year {i + 1}</div>' for i in range(6))}</div>
          <div class="t-k" style="margin-top:18px">Years 1–5: can be questioned · after 60 months: not for non-disclosure</div></div>
      </div>"""
    css = """.clip { position:absolute; top:220px; width:480px; height:640px; padding:70px 40px; border-radius:20px; background:#f1ede4; box-shadow:0 40px 80px rgba(0,0,0,.6); }
.clamp { position:absolute; left:160px; top:-26px; width:160px; height:56px; border-radius:12px; background:linear-gradient(#94a3b8,#475569); }
.lines { margin-top:40px; height:300px; background: repeating-linear-gradient(0deg, transparent 0 44px, rgba(15,23,42,.12) 44px 46px); }
.paper2 { position:absolute; padding:40px; border-radius:10px; background:#f4f1ea; color:#1f2937; box-shadow:0 40px 90px rgba(0,0,0,.7); overflow:hidden; }
.row2 { font:600 30px/1.4 Inter,Arial,sans-serif; border-bottom:1px solid #d6d0c2; padding:12px 0; }
.row2.sm { font-size:26px; display:flex; justify-content:space-between; } .row2.sm b { font-weight:800; }
.hand2 { font: italic 44px/1.4 Georgia, serif; color:#1d3c8f; min-height:70px; margin-top:12px; }
.gate { position:absolute; top:330px; width:520px; padding:60px 0; text-align:center; border-radius:24px; background:rgba(15,23,42,.9); border:3px solid rgba(148,163,184,.5); font:800 54px/1 Inter,Arial,sans-serif; color:#f8fafc; }
.neq { position:absolute; left:880px; top:300px; width:160px; text-align:center; font:800 180px/1 Inter,Arial,sans-serif; color:#f87171; }
.yc { flex:1; padding:22px 0; text-align:center; border-radius:10px; background:rgba(245,158,11,.25); font:800 26px/1 Inter,Arial,sans-serif; color:#f59e0b; }
#y5 { background: rgba(56,189,248,.3); color:#38bdf8; }"""
    cues = dict(three=S("E017", 1)["start"], one=s18[0]["start"], ped=s18[1]["start"], leg=s19[0]["start"], doc=s19[1]["start"], bp=s19[2]["start"],
                rev=s20[0]["start"], form=s20[1]["start"], said=s20[2]["start"], den=s20[3]["start"], why=s21[0]["start"], no=s21[1]["start"],
                five=s21[2]["start"], after=s21[3]["start"])
    js = """
      for (let i = 0; i < 3; i++) pop($("k" + i), C.three + 0.2 + i * 0.4, { opacity: 0, y: 200, rotation: (i - 1) * 6 });
      tl.to([$("k1"), $("k2")], { opacity: 0, duration: 0.3 }, C.one);
      tl.to($("k0"), { scale: 1.2, x: 560, rotation: 0, duration: 0.8, ease: "power2.inOut" }, C.one);
      tl.to($("sec1"), { opacity: 0, duration: 0.4 }, C.leg - 0.4); tl.to($("sec2"), { opacity: 1, duration: 0.4 }, C.leg - 0.3);
      pop($("xr"), C.leg - 0.2, { opacity: 0, x: -80 }); pop($("sheet"), C.leg + 0.4, { opacity: 0, y: 80 });
      const TXT = "k/c/o mild HTN (BP)";
      FIN.bind($("typed"), FIN.keys([[C.doc + 0.4, 0], [C.bp + 1.2, TXT.length]]), (v) => TXT.slice(0, Math.round(v)));
      tl.fromTo($("scan"), { opacity: 1, y: 0 }, { y: 470, duration: 1.0, ease: "none" }, C.rev);
      tl.to($("typed"), { backgroundColor: "rgba(248,113,113,.3)", duration: 0.2 }, C.rev + 1.0);
      tl.to($("scan"), { opacity: 0, duration: 0.2 }, C.rev + 1.1);
      pop($("form"), C.form - 0.1, { opacity: 0, x: 80 });
      const th = $("thread"), n = th.getTotalLength(); gsap.set(th, { strokeDasharray: n, strokeDashoffset: n });
      tl.to(th, { strokeDashoffset: 0, duration: 0.7, ease: "power2.out" }, C.form + 0.4);
      tl.to($("ring"), { opacity: 1, duration: 0.3 }, C.said);
      tl.fromTo($("den"), { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, C.den);
      tl.to($("sec2"), { opacity: 0, duration: 0.4 }, C.why - 0.3); tl.to($("sec3"), { opacity: 1, duration: 0.4 }, C.why - 0.2);
      tl.fromTo($("neq"), { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }, C.no - 0.2);
      pop($("yrs"), C.five, { opacity: 0, y: 40 });
      for (let i = 0; i < 5; i++) tl.to($("y" + i), { background: "rgba(245,158,11,.6)", duration: 0.1 }, C.five + 0.4 + i * 0.25);
      tl.to($("y5"), { background: "rgba(56,189,248,.7)", color: "#f8fafc", boxShadow: "0 0 40px rgba(56,189,248,.7)", duration: 0.3 }, C.after);
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.04, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "Excuse one: the x-ray rig", round(end - start, 2), body, js, tag="SIMULATION · ILLUSTRATIVE CASE · IRDAI MASTER CIRCULAR | PARA 13", css=css),
        start, end - start, cues)


def e8_opd():
    sid = "e8_opd"
    start, end = S("E022")["start"] - 0.25, L("E023")[1] + 0.25
    s22, s23 = sents("E022"), sents("E023")
    body = f"""
      <div class="glass" id="ipd" style="left:160px; top:240px; width:740px; height:560px; padding:40px">
        <div class="t-k" style="color:#4ade80">Treating doctor</div><div style="font:800 52px/1.1 Inter,Arial,sans-serif; margin-top:16px">Admit: in-patient care</div>
        <div class="drip"><div class="drop" id="drop"></div></div><div class="t-k" style="margin-top:20px">Fever · IV drip · observation</div></div>
      <div class="glass" id="opd" style="left:1020px; top:240px; width:740px; height:560px; padding:40px; border-color:rgba(220,38,38,.6)">
        <div class="t-k" style="color:#f87171">Claim reviewer</div><div style="font:800 52px/1.1 Inter,Arial,sans-serif; margin-top:16px">"Could be an OPD visit"</div>
        <div class="stamp red" id="nn" style="left:80px; top:300px; font-size:52px; transform:rotate(-8deg); opacity:0">Not necessary?</div></div>
      <div id="ex3" style="position:absolute; inset:0; opacity:0">
        <div class="chip amber" style="left:120px; top:110px; font-size:34px">Excuse 3 · room rent limit</div>
        <div class="glass room" id="rA" style="left:160px; border-color:rgba(74,222,128,.7)"><div class="t-k" style="color:#4ade80">Room your policy allows</div>
          <div class="bed"></div><div class="t-v mono" style="font-size:84px">₹5,000<span style="font-size:36px">/day</span></div></div>
        <div class="glass room" id="rB" style="left:1000px; border-color:rgba(245,158,11,.8)"><div class="t-k" style="color:#f59e0b">Room you took</div>
          <div class="bed wide"></div><div class="t-v mono" style="font-size:84px; color:#f59e0b">₹8,000<span style="font-size:36px">/day</span></div></div>
        <div id="lim" style="position:absolute; left:100px; top:500px; width:1720px; height:6px; background:#f87171; box-shadow:0 0 24px 4px rgba(248,113,113,.8)"></div>
        <div class="chip red" id="pd" style="left:640px; top:900px; opacity:0; font-size:38px">Proportionate deduction ↓ the whole bill</div></div>"""
    css = """.drip { position:relative; margin:40px 0 0 40px; width:90px; height:160px; border-radius:20px 20px 40px 40px; border:5px solid #94a3b8; }
.drop { position:absolute; left:36px; top:150px; width:14px; height:20px; border-radius:50%; background:#38bdf8; }
.room { top:260px; width:760px; height:580px; padding:40px; }
.bed { margin:40px 0 50px; width:300px; height:150px; border-radius:18px; background:linear-gradient(#e2e8f0 0 30%, #38bdf8 30%); box-shadow:0 20px 40px rgba(0,0,0,.4); }
.bed.wide { width:520px; background:linear-gradient(#e2e8f0 0 30%, #f59e0b 30%); }"""
    cues = dict(two=s22[0]["start"], nn=s22[1]["start"], opd=s22[2]["start"], three=s23[0]["start"], rr=s23[1]["start"])
    js = """
      pop($("ipd"), C.two, { opacity: 0, x: -60 }); pop($("opd"), C.nn - 0.2, { opacity: 0, x: 60 });
      FIN.hook((t) => { const u = (t * 1.3) % 1; $("drop").style.transform = `translateY(${u * 60}px)`; $("drop").style.opacity = 1 - u; });
      tl.fromTo($("nn"), { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, C.opd + 1.2);
      tl.to([$("ipd"), $("opd")], { opacity: 0, scale: 0.9, duration: 0.4 }, C.three - 0.3);
      tl.to($("ex3"), { opacity: 1, duration: 0.3 }, C.three - 0.1);
      pop($("rA"), C.three, { opacity: 0, y: 80 }); pop($("rB"), C.three + 0.5, { opacity: 0, y: 80 });
      tl.fromTo($("lim"), { scaleX: 0, transformOrigin: "0 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.in" }, C.rr);
      tl.to($("rB"), { y: 60, rotation: 2, duration: 0.3, ease: "power4.in" }, C.rr + 0.6);
      pop($("pd"), C.rr + 0.9, { opacity: 0, y: 40 });
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "Excuse two and three", round(end - start, 2), body, js, tag="SIMULATION · ILLUSTRATIVE CASE", css=css), start, end - start, cues)


def e9_slicer():
    """E024-E025 four-tower bill guillotine. Numbers from tools/claim_math.py: limit 5,000, room 8,000, 3 days; the
    room-linked towers lose 3/8 (37.5%, OUR CALCULATION; VO "about thirty-seven percent"); medicines untouched."""
    sid = "e9_slicer"
    start, end = S("E024")["start"] - 0.25, L("E025")[1] + 0.35
    s24, s25 = sents("E024"), sents("E025")
    towers = [("Room · 3 days", 24000, True), ("Surgeon and doctor", 120000, True), ("Nursing", 15000, True), ("Medicines", 121000, False)]
    base, hmax, tw = 900, 470, 250
    html = ""
    for i, (n, v, cut) in enumerate(towers):
        cx = 330 + i * 420; h = max(70, v / 121000 * hmax); hk = h * 0.625
        col = "#0284c7" if cut else "#16a34a"
        html += f"""<div class="tw" id="tw{i}" style="left:{cx - tw / 2:.0f}px; top:{base - h:.0f}px; width:{tw}px; height:{h:.0f}px">
          <div class="keep" style="height:{hk if cut else h:.0f}px; background:linear-gradient({col}, {col}cc)"></div>
          {f'<div class="slice" id="sl{i}" style="height:{h - hk:.0f}px; background:{col}"></div>' if cut else ''}
</div>
        <div class="tn" style="left:{cx - 200:.0f}px">{n}<div class="mono" id="tv{i}" style="font-size:36px; margin-top:8px; color:#f8fafc">{inr(v)}</div></div>"""
        if cut:
            ext = min(260, base - h - 300)
            html += f"""<div class="gl" id="gl{i}" style="left:{cx - tw / 2 - 30:.0f}px; top:{base - h - ext:.0f}px; width:{tw + 60}px; height:{h - hk + ext:.0f}px">
              <div class="post" style="left:0"></div><div class="post" style="right:0"></div><div class="blade" id="bl{i}"></div></div>
            <div class="pc" id="pc{i}" style="left:{cx - 110:.0f}px; top:{base - h - ext - 70:.0f}px">−37.5%</div>"""
        else:
            html += f'<div class="chip green" id="safe" style="left:{cx - 200:.0f}px; top:{base - h - 110:.0f}px; opacity:0">PROTECTED · 0% CUT</div>'
    body = f"""
      <div class="glass" id="tog" style="left:120px; top:60px; width:1680px; padding:20px 34px; display:flex; align-items:center; gap:40px">
        <div><div class="t-k">Policy room limit</div><div class="t-v mono" style="font-size:44px">₹5,000/day</div></div>
        <div class="sw"><div class="knob" id="knob"></div></div>
        <div><div class="t-k">Room taken</div><div class="t-v mono" id="room" style="font-size:44px; color:#f59e0b">₹5,000/day</div></div>
        <div style="margin-left:auto; text-align:right"><div class="t-k">Total cut</div><div class="t-v mono" id="cut" style="font-size:56px; color:#f87171; opacity:0">₹9,000?</div></div></div>
      <div id="floor" style="position:absolute; left:100px; top:{base}px; width:1720px; height:6px; background:rgba(148,163,184,.5)"></div>
      {html}"""
    css = """.tw { position:absolute; } .keep { position:absolute; left:0; right:0; bottom:0; border-radius:0 0 8px 8px; box-shadow:0 0 40px rgba(2,132,199,.35); }
.slice { position:absolute; left:0; right:0; top:0; border-radius:8px 8px 0 0; }
.tv { position:absolute; left:-40px; right:-40px; bottom:-150px; text-align:center; font:800 40px/1 Inter,Arial,sans-serif; color:#f8fafc; }
.tn { position:absolute; top:914px; width:400px; text-align:center; font:800 28px/1 Inter,Arial,sans-serif; letter-spacing:.04em; color:#cbd5e1; }
.gl { position:absolute; opacity:0; } .post { position:absolute; top:0; bottom:0; width:16px; background:linear-gradient(90deg,#64748b,#cbd5e1,#64748b); border-radius:4px; }
.blade { position:absolute; left:16px; right:16px; top:0; height:60px; background:linear-gradient(170deg,#e2e8f0,#94a3b8 60%,#f87171 100%);
  clip-path:polygon(0 0, 100% 0, 100% 40%, 0 100%); filter:drop-shadow(0 0 12px rgba(248,113,113,.7)); }
.pc { position:absolute; width:220px; text-align:center; font:800 54px/1 Inter,Arial,sans-serif; color:#f87171; opacity:0; }
.sw { width:120px; height:56px; border-radius:28px; background:#334155; position:relative; } .knob { position:absolute; left:6px; top:6px; width:44px; height:44px; border-radius:50%; background:#f8fafc; }"""
    cues = dict(lim=s24[0]["start"], took=at("E024", "eight thousand"), notjust=s24[1]["start"], five8=s25[0]["start"], surg=at("E025", "surgery"),
                pct=s25[1]["start"])
    js = """
      pop($("tog"), 0.1, { opacity: 0, y: -40 });
      for (let i = 0; i < 4; i++) tl.fromTo($("tw" + i), { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.6, ease: "power3.out" }, C.lim + 0.4 + i * 0.3);
      tl.to($("knob"), { x: 64, background: "#f59e0b", duration: 0.3 }, C.took);
      FIN.bind($("room"), FIN.keys([[C.took, 5000], [C.took + 0.5, 8000]]), (v) => FIN.inr(Math.round(v / 100) * 100) + "/day");
      pop($("cut"), C.notjust, { opacity: 0 });
      [0, 1, 2].forEach((i) => tl.to($("gl" + i), { opacity: 1, duration: 0.3 }, C.five8 + 0.2 + i * 0.2));
      const hit = [C.five8 + 1.4, C.surg + 0.6, C.surg + 1.6];
      [0, 1, 2].forEach((i) => {
        const g = $("gl" + i);
        tl.fromTo($("bl" + i), { y: 0 }, { y: parseFloat(g.style.height) - 60, duration: 0.18, ease: "power4.in", immediateRender: false }, hit[i] - 0.18);
        tl.to($("sl" + i), { background: "#dc2626", duration: 0.05 }, hit[i]);
        tl.to($("sl" + i), { x: 140 + i * 20, y: -60, rotation: 28 + i * 8, opacity: 0, duration: 1.1, ease: "power2.out" }, hit[i] + 0.05);
        tl.to($("bl" + i), { y: 0, duration: 0.5, ease: "power2.inOut" }, hit[i] + 0.5);
        pop($("pc" + i), hit[i] + 0.1, { opacity: 0, y: 30, scale: 1.4 });
        tl.fromTo($("stage"), { y: 0 }, { y: 8, duration: 0.04, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, hit[i]);
      });
      pop($("safe"), C.pct + 0.8, { opacity: 0, y: 30 });
      FIN.bind($("cut"), FIN.keys([[C.notjust, 8999], [hit[0], 8999], [hit[0] + 0.01, 9000], [hit[1], 9000], [hit[1] + 0.3, 54000], [hit[2], 54000], [hit[2] + 0.3, 59625]]),
        (v) => v < 9000 ? "₹9,000?" : FIN.inr(Math.round(v)));
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.04, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "The four-tower bill guillotine", round(end - start, 2), body, js,
                     tag="OUR CALCULATION · ILLUSTRATIVE BILL · AROGYA SANJEEVANI POLICY WORDING", css=css), start, end - start, cues)


def e10_wall():
    sid = "e10_wall"
    start, end = S("E026")["start"] - 0.25, L("E028")[1] + 0.3
    s26, s27, s28 = sents("E026"), sents("E027"), sents("E028")
    body = f"""
      <div id="secA">
        <div class="node2" id="fam" style="left:140px; top:400px">{svg("person", 110)}<div class="t-k" style="margin-top:12px">Family</div></div>
        <div class="node2 cyanb" id="pool" style="left:1520px; top:400px">{svg("bank", 110)}<div class="t-k" style="margin-top:12px; color:#38bdf8">₹4.5 lakh claim</div></div>
        {"".join(f'<div class="wb" id="w{i}" style="top:{220 + i * 220}px">{t}</div>' for i, t in enumerate(["Non-disclosure", "Not necessary", "Room rent cut"]))}
      </div>
      <div id="secB" style="opacity:0">
        <div class="lane" id="l1" style="top:300px; border-color:rgba(220,38,38,.6)"><span class="t-k" style="color:#f87171">Lane 1</span> &nbsp; Cashless at the desk <span class="st" style="color:#f87171">BLOCKED</span></div>
        <div class="lane" id="l2" style="top:560px; border-color:rgba(74,222,128,.7)"><span class="t-k" style="color:#4ade80">Lane 2</span> &nbsp; Reimbursement claim · grievance · Ombudsman <span class="st" style="color:#4ade80">OPEN</span></div>
      </div>
      <div class="glass" id="key" style="left:560px; top:820px; width:800px; padding:22px 30px; text-align:center; opacity:0; border-color:rgba(250,204,21,.7)">
        <div class="t-k" style="color:#facc15">IRDAI Master Circular · 29 May 2024</div></div>"""
    css = """.node2 { position:absolute; width:260px; text-align:center; color:var(--white); padding:30px 0; border-radius:26px; background:rgba(15,23,42,.9); border:3px solid rgba(148,163,184,.4); }
.cyanb { border-color: rgba(56,189,248,.7); color:#38bdf8; }
.wb { position:absolute; left:760px; width:400px; height:190px; border-radius:16px; background:#f1ede4; color:#991b1b; font:800 40px/190px Inter,Arial,sans-serif; text-align:center; box-shadow:0 30px 60px rgba(0,0,0,.6); }
.lane { position:absolute; left:160px; width:1600px; padding:44px 50px; border-radius:22px; border:4px solid; background:rgba(15,23,42,.88); font:800 46px/1.2 Inter,Arial,sans-serif; color:#f8fafc; }
.st { float:right; letter-spacing:.1em; }"""
    cues = dict(fam=s26[0]["start"], closed=s26[1]["start"], no=s27[0]["start"], cd=s27[1]["start"], right=s27[2]["start"], listen=s28[0]["start"], rule=s28[1]["start"])
    js = """
      pop($("fam"), 0.1, { opacity: 0, x: -60 }); pop($("pool"), 0.3, { opacity: 0, x: 60 });
      for (let i = 0; i < 3; i++) pop($("w" + i), C.fam + 0.6 + i * 0.4, { opacity: 0, y: -300 });
      tl.to($("fam"), { borderColor: "#f87171", duration: 0.3 }, C.closed);
      tl.to($("secA"), { opacity: 0, duration: 0.4 }, C.no + 0.2); tl.to($("secB"), { opacity: 1, duration: 0.3 }, C.no + 0.3);
      pop($("l1"), C.cd, { opacity: 0, x: -80 }); pop($("l2"), C.cd + 1.4, { opacity: 0, x: -80 });
      tl.to($("l2"), { boxShadow: "0 0 70px rgba(74,222,128,.5)", duration: 0.4 }, C.right);
      pop($("key"), C.listen, { opacity: 0, y: 60 });
      tl.to($("secB"), { opacity: 0.15, duration: 0.5 }, C.rule);
      tl.to($("key"), { y: -380, scale: 1.4, duration: 1.4, ease: "power2.inOut" }, C.rule);
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.04, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "The wall and the two lanes", round(end - start, 2), body, js, tag="AROGYA SANJEEVANI POLICY WORDING · IRDAI MASTER CIRCULAR", css=css),
        start, end - start, cues)


CH2 = [e5_funnel, e6_lock, e7_dossier, e8_opd, e9_slicer, e10_wall]
ENGINES += CH2


# ---------------- CHAPTER 3 ----------------
def months_html(n, x0=120, x1=1800, y=520, h=90, pref="m"):
    w = (x1 - x0) / n
    cells = "".join(f'<div class="mc" id="{pref}{i}" style="left:{x0 + i * w:.1f}px; top:{y}px; width:{w - 3:.1f}px; height:{h}px"></div>' for i in range(n))
    ticks = "".join(f'<div class="yl" style="left:{x0 + (k * 12 - 6) * w:.0f}px; top:{y + h + 16}px">Y{k}</div>' for k in range(1, n // 12 + 1))
    return cells + ticks, w


def emblem(idp, x, y, wpx=300, op=1):
    """Titanium shield emblem: brushed-metal heater shield with the 60-month count."""
    return f"""<svg id="{idp}" viewBox="0 0 200 240" style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{wpx}px; height:{wpx * 1.2:.0f}px; opacity:{op}; overflow:visible">
      <defs><linearGradient id="{idp}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1f5f9"/><stop offset=".35" stop-color="#94a3b8"/>
        <stop offset=".55" stop-color="#e2e8f0"/><stop offset="1" stop-color="#475569"/></linearGradient>
        <linearGradient id="{idp}c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0ea5e9"/><stop offset="1" stop-color="#075985"/></linearGradient></defs>
      <path d="M100 6 L190 36 C190 120 160 190 100 234 C40 190 10 120 10 36 Z" fill="url(#{idp}g)" stroke="#e2e8f0" stroke-width="4" style="filter:drop-shadow(0 0 24px rgba(56,189,248,.8))"/>
      <path d="M100 26 L172 50 C172 118 148 174 100 210 C52 174 28 118 28 50 Z" fill="url(#{idp}c)"/>
      <text x="100" y="128" text-anchor="middle" fill="#f8fafc" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="70">60</text>
      <text x="100" y="162" text-anchor="middle" fill="#e0f2fe" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="20" letter-spacing="3">MONTHS</text></svg>"""


MC_CSS = """.mc { position:absolute; border-radius:3px; background:rgba(245,158,11,.35); }
.yl { position:absolute; width:60px; margin-left:-30px; text-align:center; font:800 24px/1 Inter,Arial,sans-serif; color:#94a3b8; }
.shield { position:absolute; width:46px; border-radius:10px; background:linear-gradient(#7dd3fc,#0284c7); box-shadow:0 0 60px 12px rgba(56,189,248,.65); }
.shield span { position:absolute; left:60px; top:-6px; white-space:nowrap; font:800 28px/1 Inter,Arial,sans-serif; letter-spacing:.08em; color:#38bdf8; }"""


def e11_shield():
    sid = "e11_shield"
    start, end = S("E029")["start"] - 0.25, L("E031")[1] + 0.35
    cells, w = months_html(96, y=600, h=220)
    sx = 120 + 60 * w - 23
    body = cells + f"""
      <div class="glass" id="lab" style="left:120px; top:150px; padding:26px 34px"><div class="t-k" style="font-size:28px">The moratorium period</div><div class="t-v mono" id="yrs" style="font-size:120px">8 years</div></div>
      <div class="shield" id="sh" style="left:{sx:.0f}px; top:540px; height:340px; opacity:0"></div>
      {emblem("emb", sx - 127, 150, 280, 0)}
      <div class="chip cyan" id="nb" style="left:120px; top:900px; opacity:0; font-size:36px">60 continuous months · no break</div>"""
    s30 = sents("E030")
    cues = dict(mor=S("E029")["start"], eight=s30[0]["start"], down=at("E030", "brought it down", k=1), five=at("E030", "five years", k=1), sixty=S("E031")["start"])
    js = """
      pop($("lab"), C.mor, { opacity: 0, x: -40 });
      for (let i = 0; i < 96; i++) pop($("m" + i), C.mor + 0.2 + i * 0.012, { opacity: 0, y: 30 });
      for (let i = 60; i < 96; i++) tl.to($("m" + i), { y: 220 + (i % 5) * 40, rotation: (i % 2 ? 40 : -30), opacity: 0, duration: 0.7, ease: "power2.in" }, C.down + (i - 60) * 0.025);
      FIN.bind($("yrs"), (t) => t < C.five ? 0 : 1, (v) => v ? "5 years" : "8 years");
      tl.to($("yrs"), { color: "#38bdf8", duration: 0.3 }, C.five);
      tl.fromTo($("sh"), { opacity: 0, y: -500 }, { opacity: 1, y: 0, duration: 0.45, ease: "power4.in" }, C.five + 0.1);
      tl.fromTo($("emb"), { opacity: 0, y: -400, scale: 1.4 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power4.in" }, C.five + 0.2);
      tl.fromTo($("stage"), { y: 0 }, { y: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.five + 0.7);
      for (let i = 0; i < 60; i++) tl.to($("m" + i), { background: "#0284c7", duration: 0.06 }, C.sixty + i * 0.05);
      tl.to($("emb"), { scale: 1.08, duration: 0.4, yoyo: true, repeat: 1 }, C.sixty + 3.0);
      pop($("nb"), C.sixty + 1.0, { opacity: 0 });
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "The 60 month shield", round(end - start, 2), body, js, tag="IRDAI INSURANCE PRODUCTS REGULATIONS | 2024", css=MC_CSS), start, end - start, cues)


def shield_world(n=72):
    cells, w = months_html(n, y=660, h=120)
    sx = 120 + 60 * w - 23
    fx = 120 + 66 * w
    return cells + f"""
      <div class="shield" id="sh" style="left:{sx:.0f}px; top:560px; height:300px"><span style="left:-330px; top:320px">MONTH 60 SHIELD</span></div>
      {emblem("emb", sx - 147, 170, 300)}
      <div class="fam" id="fam" style="left:{fx + 10:.0f}px; top:300px">{svg("person", 90)}<div class="t-k" style="margin-top:8px; color:#f8fafc">Year 6 · our family</div></div>""", sx, w


FAM_CSS = MC_CSS + """.fam { position:absolute; width:220px; text-align:center; color:#38bdf8; padding:18px 0; border-radius:20px; background:rgba(15,23,42,.92); border:3px solid #38bdf8; }
.proj { position:absolute; padding:18px 26px; border-radius:14px; background:#991b1b; color:#fff; font:800 32px/1 Inter,Arial,sans-serif; letter-spacing:.06em; box-shadow:0 0 40px rgba(220,38,38,.7); white-space:nowrap; }
.frag { position:absolute; width:46px; height:40px; background:#ef4444; clip-path:polygon(50% 0, 100% 100%, 0 80%); opacity:0; }
.arrow { position:absolute; height:110px; padding:0 120px 0 40px; background:linear-gradient(90deg, rgba(153,27,27,.2), #b91c1c 40%, #dc2626);
  clip-path:polygon(0 25%, calc(100% - 110px) 25%, calc(100% - 110px) 0, 100% 50%, calc(100% - 110px) 100%, calc(100% - 110px) 75%, 0 75%);
  color:#fff; font:800 34px/110px Inter,Arial,sans-serif; letter-spacing:.06em; white-space:nowrap; filter:drop-shadow(0 0 30px rgba(220,38,38,.8)); }"""


def _fill_js(n=72):
    return f"for (let i = 0; i < {n}; i++) gsap.set($('m' + i), {{ background: i < 60 ? '#0284c7' : 'rgba(56,189,248,.55)' }});"


def e12_history():
    sid = "e12_history"
    start, end = S("E034")["start"] - 0.25, L("E034")[1] + 0.35
    world, sx, w = shield_world()
    body = world + f"""<div class="proj" id="pj" style="left:140px; top:620px; background:#475569; box-shadow:none">Old health history</div>"""
    cues = dict(read=S("E034")["start"], hit=S("E034", 1)["start"] + 1.6)
    js = _fill_js() + f"""
      tl.fromTo($("pj"), {{ x: 0 }}, {{ x: {sx - 520:.0f}, duration: C.hit - 0.6, ease: "power1.in" }}, 0.4);
      tl.to($("pj"), {{ x: {sx - 760:.0f}, y: 140, rotation: -18, opacity: 0.3, duration: 0.8, ease: "power2.out" }}, C.hit);
      tl.to($("sh"), {{ boxShadow: "0 0 120px 30px rgba(56,189,248,.95)", duration: 0.15, yoyo: true, repeat: 1 }}, C.hit);
      tl.fromTo($("stage"), {{ scale: 1.05 }}, {{ scale: 1, duration: D.duration, ease: "none" }}, 0);
"""
    put(sid, bp_page(sid, "Old history bounces off", round(end - start, 2), body, js, tag="IRDAI MASTER CIRCULAR | PARA 13", css=FAM_CSS), start, end - start, cues)


def e15_impact():
    sid = "e15_impact"; s = sents("E037")
    start, end = s[0]["start"] - 0.25, s[3]["end"] + 0.35
    world, sx, w = shield_world()
    hx, hy = sx - 130, 330                    # impact point: left face of the emblem
    frags = "".join(f'<div class="frag" id="fr{i}" style="left:{hx:.0f}px; top:{hy:.0f}px"></div>' for i in range(24))
    body = world + frags + f'''<div class="arrow" id="pj" style="left:-40px; top:{hy - 55:.0f}px; width:760px">TPA DENIAL · NON-DISCLOSURE</div>
      <div class="glass" id="v" style="left:120px; top:900px; padding:18px 30px; opacity:0; border-color:rgba(56,189,248,.8)"><span class="t-v" style="font-size:44px; color:#38bdf8">Against the IRDAI rule</span></div>'''
    cues = dict(fam=s[0]["start"], six=s[1]["start"], letter=s[2]["start"], viol=s[3]["start"])
    js = """
      for (let i = 0; i < 72; i++) pop($("m" + i), 0.1 + i * 0.01, { opacity: 0 });
      for (let i = 0; i < 72; i++) tl.to($("m" + i), { background: i < 60 ? "#0284c7" : "rgba(56,189,248,.55)", duration: 0.05 }, C.six + i * 0.022);
      pop($("fam"), C.fam + 0.3, { opacity: 0, y: -40 }); pop($("sh"), C.six + 1.3, { opacity: 0, y: -300 });
      pop($("emb"), C.six + 1.4, { opacity: 0, y: -300, scale: 1.3 });
      tl.fromTo($("pj"), { opacity: 0, x: -400 }, { opacity: 1, x: 0, duration: 0.4 }, C.letter);
      tl.to($("pj"), { x: """ + f"{hx - 720 + 40:.0f}" + """, duration: 1.4, ease: "power3.in" }, C.letter + 0.5);
      tl.to($("pj"), { opacity: 0, scaleX: 0.2, transformOrigin: "100% 50%", duration: 0.12 }, C.letter + 1.9);
      for (let i = 0; i < 24; i++) tl.fromTo($("fr" + i), { opacity: 1, x: 0, y: 0, rotation: 0, scale: 1 },
        { opacity: 0, x: -80 - (i * 47) % 520, y: ((i * 83) % 640) - 320, rotation: i * 95, scale: 0.6 + (i % 3) * 0.3, duration: 1.2, ease: "power2.out", immediateRender: false }, C.letter + 1.9);
      tl.fromTo($("emb"), { scale: 1 }, { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }, C.letter + 1.9);
      tl.to($("sh"), { boxShadow: "0 0 140px 40px rgba(56,189,248,1)", duration: 0.15, yoyo: true, repeat: 1 }, C.letter + 1.9);
      tl.fromTo($("stage"), { x: 0 }, { x: 14, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.letter + 1.9);
      pop($("v"), C.viol, { opacity: 0, y: 30 });
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.05, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "The shield impact", round(end - start, 2), body, js, tag="IRDAI MASTER CIRCULAR | PARA 13 · ILLUSTRATIVE FAMILY", css=FAM_CSS), start, end - start, cues)


GLYPH = {
    "thermo": '<path d="M20 8a4 4 0 0 1 8 0v20a8 8 0 1 1-8 0z"/><path d="M24 18v14"/>',
    "ache": '<circle cx="24" cy="12" r="6"/><path d="M14 44V28a10 10 0 0 1 20 0v16"/><path d="M20 26l4 4 4-4"/>',
    "pen": '<path d="M10 38l4-12 18-18 8 8-18 18z"/><path d="M28 12l8 8"/>',
    "lens": '<circle cx="20" cy="20" r="12"/><path d="M29 29l12 12"/>',
    "gavel": '<path d="M18 10l12 12M12 16l12 12M15 13l9-9 12 12-9 9z"/><path d="M27 25l14 14"/><path d="M6 42h20"/>',
}


def glyph(name, size=80, color="currentColor"):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{GLYPH[name]}</svg>')


def e13_burden():
    sid = "e13_burden"; s = sents("E035")
    start, end = s[0]["start"] - 0.25, s[2]["end"] + 0.4
    honest = [("thermo", "A forgotten fever"), ("ache", "An undiagnosed ache"), ("pen", "An honest miss")]
    body = f"""
      <div id="ex" style="position:absolute; left:0; top:90px; width:1920px; text-align:center">
        <div class="t-k" style="color:#facc15; font-size:30px">The only exception</div>
        <div style="font:800 96px/1.05 Inter,Arial,sans-serif; margin-top:12px; color:#f8fafc">Proven fraud</div></div>
      <div class="glass" id="ok" style="left:120px; top:340px; width:800px; height:600px; padding:40px; border-color:rgba(74,222,128,.7)">
        <div class="t-k" style="color:#4ade80; font-size:30px">Not fraud · cannot be used after 5 years</div>
        {"".join(f'<div class="hr" id="h{i}">{glyph(g, 78, "#4ade80")}<span>{t}</span></div>' for i, (g, t) in enumerate(honest))}</div>
      <div class="glass" id="fr" style="left:1000px; top:340px; width:800px; height:600px; padding:40px; border-color:rgba(220,38,38,.8)">
        <div class="t-k" style="color:#f87171; font-size:30px">Fraud · the company must prove it</div>
        <div class="hr" style="margin-top:50px">{glyph("lens", 90, "#f87171")}<span>Active, deliberate lie</span></div>
        <div class="hr">{glyph("gavel", 90, "#f87171")}<span>Burden of proof: the insurer</span></div>
        <div class="seal" id="seal">PROOF<br>NEEDED</div></div>"""
    css = """.hr { display:flex; align-items:center; gap:28px; margin-top:44px; font:800 50px/1.1 Inter,Arial,sans-serif; color:#f8fafc; }
.seal { position:absolute; right:40px; bottom:40px; width:190px; height:190px; border-radius:50%; border:8px solid #dc2626; color:#dc2626; text-align:center;
  font:800 34px/1.1 Inter,Arial,sans-serif; padding-top:52px; transform:rotate(-12deg); opacity:0; }"""
    cues = dict(one=s[0]["start"], est=s[1]["start"], notf=s[2]["start"], act=at("E035", "active", k=2))
    js = """
      pop($("ex"), 0.1, { opacity: 0, y: -40 });
      pop($("ok"), C.one + 0.4, { opacity: 0, x: -80 }); pop($("fr"), C.one + 0.7, { opacity: 0, x: 80 });
      for (let i = 0; i < 3; i++) pop($("h" + i), C.notf + i * 1.2, { opacity: 0, x: -40 });
      tl.fromTo($("seal"), { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }, C.est + 1.2);
      tl.to($("fr"), { boxShadow: "0 0 80px rgba(220,38,38,.55)", duration: 0.4 }, C.act);
      tl.to($("ok"), { boxShadow: "0 0 80px rgba(74,222,128,.45)", duration: 0.4 }, C.notf);
      tl.fromTo($("stage"), { scale: 1.06 }, { scale: 1, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "Burden of proof", round(end - start, 2), body, js, tag="IRDAI MASTER CIRCULAR | PARA 13 · STANDARD POLICY WORDING", css=css), start, end - start, cues)


def e14_port():
    sid = "e14_port"; s = sents("E036")
    start, end = s[0]["start"] - 0.25, s[1]["end"] + 0.4
    body = """
      <div class="chip amber" id="lim" style="left:160px; top:120px">Normal limits &amp; exclusions still apply</div>
      <div class="glass trk" id="t1" style="top:300px"><div class="t-k" style="color:#4ade80">Port · Insurer A → Insurer B</div>
        <div class="pb"><div class="pf" id="p1" style="background:#0284c7"></div></div><div class="cnt mono" id="c1">0/60</div></div>
      <div class="glass trk" id="t2" style="top:600px; border-color:rgba(220,38,38,.6)"><div class="t-k" style="color:#f87171">Cancel and buy new</div>
        <div class="pb"><div class="pf" id="p2" style="background:#0284c7"></div></div><div class="cnt mono" id="c2">60/60</div></div>"""
    css = """.trk { left:160px; width:1600px; height:230px; padding:34px 40px; }
.pb { margin-top:30px; width:1250px; height:56px; border-radius:28px; background:rgba(148,163,184,.2); overflow:hidden; } .pf { height:100%; width:100%; transform-origin:0 50%; }
.cnt { position:absolute; right:40px; top:96px; font:800 64px/1 Inter,Arial,sans-serif; }"""
    cues = dict(lim=s[0]["start"], port=at("E036", "port"), years=at("E036", "years move"), cancel=s[1]["start"], zero=at("E036", "zero", k=1))
    js = """
      pop($("lim"), C.lim);
      pop($("t1"), C.port - 0.2, { opacity: 0, x: -60 });
      FIN.bind($("c1"), FIN.keys([[C.port, 60], [C.port + 0.1, 60]]), (v) => Math.round(v) + "/60");
      tl.fromTo($("p1"), { scaleX: 0 }, { scaleX: 1, duration: 0.8 }, C.port); tl.to($("t1"), { boxShadow: "0 0 60px rgba(74,222,128,.45)", duration: 0.4 }, C.years);
      pop($("t2"), C.cancel - 0.2, { opacity: 0, x: -60 });
      tl.to($("p2"), { scaleX: 0, background: "#dc2626", duration: 0.8, ease: "power2.in" }, C.zero - 0.6);
      FIN.bind($("c2"), FIN.keys([[C.zero - 0.6, 60], [C.zero + 0.2, 0]]), (v) => Math.round(v) + "/60");
      tl.to($("c2"), { color: "#f87171", duration: 0.2 }, C.zero);
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.04, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "Port, do not cancel", round(end - start, 2), body, js, tag="IRDAI MASTER CIRCULAR | PARA 13 NOTE", css=css), start, end - start, cues)


def e16_stopwatch():
    sid = "e16_stopwatch"
    start, end = S("E038")["start"] - 0.25, L("E041")[1] + 0.35
    s40 = sents("E040")
    body = """
      <div class="glass" id="clk" style="left:100px; top:120px; width:860px; height:860px; padding:30px; text-align:center">
        <div class="t-k">Since the discharge request</div>
        <svg viewBox="0 0 600 600" style="width:600px; height:600px; margin-top:14px; overflow:visible">
          <rect x="270" y="-22" width="60" height="30" rx="8" fill="#94a3b8"/><circle cx="300" cy="300" r="250" fill="rgba(2,6,15,.75)" stroke="#94a3b8" stroke-width="10"/>
          <circle cx="300" cy="300" r="222" fill="none" stroke="rgba(148,163,184,.18)" stroke-width="26"/>
          <circle id="ring" cx="300" cy="300" r="222" fill="none" stroke="#f59e0b" stroke-width="26" stroke-dasharray="1394.9" stroke-dashoffset="1394.9" transform="rotate(-90 300 300)"/>
          <circle id="ring2" cx="300" cy="300" r="250" fill="none" stroke="#dc2626" stroke-width="14" stroke-dasharray="1570.8" stroke-dashoffset="1570.8" transform="rotate(-90 300 300)" style="filter:drop-shadow(0 0 14px rgba(220,38,38,.9))"/>
          <line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(0 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(6 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(12 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(18 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(24 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(30 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(36 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(42 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(48 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(54 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(60 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(66 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(72 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(78 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(84 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(90 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(96 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(102 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(108 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(114 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(120 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(126 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(132 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(138 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(144 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(150 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(156 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(162 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(168 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(174 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(180 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(186 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(192 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(198 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(204 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(210 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(216 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(222 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(228 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(234 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(240 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(246 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(252 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(258 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(264 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(270 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(276 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(282 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(288 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(294 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(300 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(306 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(312 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(318 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(324 300 300)"/><line x1="300" y1="70" x2="300" y2="100" stroke="#f8fafc" stroke-width="6" transform="rotate(330 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(336 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(342 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(348 300 300)"/><line x1="300" y1="84" x2="300" y2="100" stroke="#64748b" stroke-width="3" transform="rotate(354 300 300)"/><text x="445" y="398" text-anchor="middle" fill="#cbd5e1" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="36">1H</text><text x="155" y="398" text-anchor="middle" fill="#cbd5e1" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="36">2H</text><text x="300" y="146" text-anchor="middle" fill="#cbd5e1" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="36">3H</text>
          <line id="hand" x1="300" y1="330" x2="300" y2="96" stroke="#f87171" stroke-width="8" stroke-linecap="round"/><circle cx="300" cy="300" r="16" fill="#f87171"/></svg>
        <div class="mono" id="t" style="font:800 84px/1 Inter,Arial,sans-serif; margin-top:-6px">00:00:00</div>
        <div class="limit" style="display:none"><div class="lf" id="lf"></div></div><div class="t-k" id="st" style="margin-top:14px; color:#f59e0b; font-size:26px">Final approval due within 3 hours</div></div>
      <div class="glass" id="led" style="left:1010px; top:200px; width:800px; height:640px; padding:44px">
        <div style="display:flex; gap:30px"><div class="colx" id="wal"><div class="t-k">Your wallet</div></div><div class="colx" id="fund" style="border-color:rgba(56,189,248,.6)"><div class="t-k" style="color:#38bdf8">Insurer's shareholders' fund</div><div class="t-k" style="margin-top:6px; font-size:18px">Para 16(b)</div></div></div>
        <div class="chg" id="chg">Extra delay charge · ₹4,000</div></div>
      <div class="chip amber" id="ask" style="left:640px; top:900px; opacity:0">Ask for the 3-hour rule</div>"""
    css = """.limit { margin:50px auto 0; width:640px; height:26px; border-radius:13px; background:rgba(148,163,184,.25); overflow:hidden; } .lf { width:100%; height:100%; background:#f59e0b; transform-origin:0 50%; transform:scaleX(0); }
.colx { flex:1; height:420px; padding:24px; border-radius:16px; border:3px dashed rgba(148,163,184,.4); }
.chg { position:absolute; left:80px; top:330px; width:310px; padding:22px; border-radius:14px; background:#991b1b; font:800 28px/1.25 Inter,Arial,sans-serif; text-align:center; opacity:0; }"""
    cues = dict(clock=S("E038")["start"], req=S("E039")["start"], three=at("E039", "three hours"), wait=s40[0]["start"], late=s40[1]["start"],
                extra=at("E040", "extra amount", k=1), pays=at("E040", "paid by", k=1), ask=S("E041")["start"])
    js = """
      pop($("clk"), C.clock, { opacity: 0, x: -60 }); pop($("led"), C.wait, { opacity: 0, x: 60 });
      const secs = FIN.keys([[C.req, 0], [C.three + 1.0, 10800], [C.late, 10800], [C.extra + 0.6, 16200], [D.duration, 17400]]);
      FIN.bind($("t"), secs, (v) => { const s = Math.floor(v), h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
        return [h, m, x].map((n) => String(n).padStart(2, "0")).join(":"); });
      FIN.hook((t) => { const v = secs(t); $("lf").style.transform = `scaleX(${Math.min(1, v / 10800)})`;
        $("ring").setAttribute("stroke-dashoffset", String(1394.9 * (1 - Math.min(1, v / 10800))));
        $("ring2").setAttribute("stroke-dashoffset", String(1570.8 * (1 - Math.min(1, Math.max(0, v - 10800) / 10800))));
        $("hand").setAttribute("transform", `rotate(${(v / 10800) * 360} 300 300)`);
        const over = v > 10801; $("t").style.color = over ? "#f87171" : "#f8fafc"; $("lf").style.background = over ? "#dc2626" : "#f59e0b"; });
      FIN.bind($("st"), (t) => secs(t) > 10801 ? 1 : 0, (v) => v ? "Over 3 hours: delay" : "Final approval due within 3 hours");
      tl.to($("chg"), { opacity: 1, duration: 0.3 }, C.extra);
      tl.to($("chg"), { x: 370, background: "#0284c7", duration: 1.0, ease: "power2.inOut" }, C.pays);
      pop($("ask"), C.ask, { opacity: 0 });
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.03, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "The discharge stopwatch", round(end - start, 2), body, js, tag="IRDAI MASTER CIRCULAR | PARA 16 · ILLUSTRATIVE AMOUNT", css=css),
        start, end - start, cues)


CH3 = [e11_shield, e12_history, e13_burden, e14_port, e15_impact, e16_stopwatch]
ENGINES += CH3


# ---------------- CHAPTER 4: escalation war-room ----------------
CITIES = [("Ahmedabad", 72.6, 23.0), ("Bengaluru", 77.6, 12.97), ("Bhopal", 77.4, 23.26), ("Bhubaneswar", 85.8, 20.3), ("Chandigarh", 76.8, 30.7),
          ("Chennai", 80.27, 13.08), ("Delhi", 77.2, 28.6), ("Guwahati", 91.7, 26.1), ("Hyderabad", 78.5, 17.4), ("Jaipur", 75.8, 26.9),
          ("Kochi", 76.3, 9.93), ("Kolkata", 88.36, 22.57), ("Lucknow", 80.9, 26.85), ("Mumbai", 72.88, 19.08), ("Noida", 77.39, 28.54),
          ("Patna", 85.1, 25.6), ("Pune", 73.86, 18.52), ("Thane", 72.97, 19.2)]   # CIO Annual Report 2024-25: 18 Ombudsman offices


def e17_warroom():
    sid = "e17_warroom"
    start, end = S("E042")["start"] - 0.3, L("E056")[1] + 0.4
    N = {1: (700, 700), 2: (2300, 520), 3: (3900, 900), 4: (2700, 1950)}
    trace = lambda a, b, i: f'<path id="tr{i}" d="M{N[a][0]} {N[a][1]} L{(N[a][0] + N[b][0]) / 2:.0f} {N[a][1]} L{(N[a][0] + N[b][0]) / 2:.0f} {N[b][1]} L{N[b][0]} {N[b][1]}" stroke="rgba(56,189,248,.18)" stroke-width="10" fill="none"/>'
    cx = lambda lon: N[4][0] - 120 + (lon - 82) * 52
    cy = lambda lat: N[4][1] + 40 - (lat - 21) * 52
    import random
    rnd = random.Random(3)
    city = "".join(f'<g class="city" id="cy{i}"><circle cx="{cx(lo):.0f}" cy="{cy(la):.0f}" r="10" fill="#38bdf8"/><circle class="halo" cx="{cx(lo):.0f}" cy="{cy(la):.0f}" r="10" fill="none" stroke="#38bdf8" stroke-width="3"/>'
                   f'<text x="{cx(lo) + (16 if n not in ("Thane", "Noida") else -16):.0f}" y="{cy(la) + (7 if n not in ("Thane", "Noida") else 26):.0f}" text-anchor="{"start" if n not in ("Thane", "Noida") else "end"}" '
                   f'fill="#cbd5e1" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="22">{n}</text></g>' for i, (n, lo, la) in enumerate(CITIES))
    grid = "".join(f'<line x1="{rnd.randint(0, 3600)}" y1="{y}" x2="{rnd.randint(0, 3600)}" y2="{y}" stroke="rgba(56,189,248,.07)" stroke-width="3"/>' for y in range(100, 2700, 140))
    badge = lambda n: f'<div class="nb" id="nb{n}" style="left:{N[n][0] - 60}px; top:{N[n][1] - 60}px">{n}</div>'
    slots = ["Discharge summary", "Final itemised bill", "Test reports", "Pharmacy receipts", "Written denial letter"]
    body = f"""
      <div id="world" style="position:absolute; left:0; top:0; width:4800px; height:2700px; transform-origin:0 0">
        <svg viewBox="0 0 4800 2700" style="position:absolute; inset:0; width:4800px; height:2700px">{grid}{trace(1, 2, 1)}{trace(2, 3, 2)}{trace(3, 4, 3)}
          <circle id="rad1" cx="{N[3][0]}" cy="{N[3][1]}" r="40" fill="none" stroke="#38bdf8" stroke-width="5" opacity="0"/>
          <circle id="rad2" cx="{N[3][0]}" cy="{N[3][1]}" r="40" fill="none" stroke="#38bdf8" stroke-width="5" opacity="0"/>
          <g id="cities" opacity="0">{city}</g></svg>
        {"".join(badge(n) for n in N)}
        <div class="glass vault" id="vault" style="left:{N[1][0] + 90}px; top:{N[1][1] - 260}px">
          <div class="t-k" style="color:#38bdf8">Evidence pack</div>
          {"".join(f'<div class="slot" id="sl{i}"><span class="ck" id="ck{i}">✓</span>{t}</div>' for i, t in enumerate(slots))}</div>
        <div class="glass" id="tmpl" style="left:{N[1][0] + 90}px; top:{N[1][1] + 340}px; width:700px; padding:26px; opacity:0">
          <div class="t-k" style="color:#f59e0b">Doctor's letter · sample wording</div>
          <div style="font:600 28px/1.4 Inter,Arial,sans-serif; margin-top:12px">This patient needed in-patient admission for [diagnosis] because [clinical reason].</div></div>
        <div class="glass" id="rf" style="left:{N[2][0] + 90}px; top:{N[2][1] - 200}px; width:760px; padding:30px; opacity:0">
          <div class="t-k" style="color:#4ade80">Reimbursement claim · file it yourself</div>
          {"".join(f'<div class="ml rfr" id="rf{i}"><span style="color:#4ade80">✓</span> {t}</div>' for i, t in enumerate(["Claim form, signed", "Final bill and payment receipt", "Discharge summary and reports", "Copy of the cashless denial letter"]))}
          <div style="font:800 48px/1 Inter,Arial,sans-serif; margin-top:22px; color:#f59e0b">Within 15–30 days</div></div>
        <div class="glass" id="mail" style="left:{N[2][0] + 90}px; top:{N[2][1] - 200}px; width:760px; padding:30px; opacity:0">
          <div class="t-k" style="color:#38bdf8">To: Grievance Redressal Officer</div>
          <div class="ml" id="ml0">Policy no · claim no · amount</div><div class="ml" id="ml1">Policy running since 2020 (over 5 years)</div>
          <div class="ml" id="ml2">IRDAI moratorium, para 13: not contestable for non-disclosure</div><div class="ml" id="ml3">Please review and settle</div></div>
        <div class="glass" id="dl" style="left:{N[2][0] - 520}px; top:{N[2][1] + 160}px; padding:20px 26px; opacity:0"><div class="t-k" style="color:#f59e0b">Reimbursement claim</div>
          <div style="font:800 40px/1.1 Inter,Arial,sans-serif; margin-top:6px">15–30 days of discharge</div><div class="t-k" style="margin-top:6px">Check your policy</div></div>
        <svg id="ringw" viewBox="0 0 200 200" style="position:absolute; left:{N[2][0] + 300}px; top:{N[2][1] + 330}px; width:240px; height:240px; opacity:0">
          <circle cx="100" cy="100" r="80" fill="none" stroke="rgba(148,163,184,.25)" stroke-width="16"/>
          <circle id="ring14" cx="100" cy="100" r="80" fill="none" stroke="#38bdf8" stroke-width="16" stroke-dasharray="503" stroke-dashoffset="503" transform="rotate(-90 100 100)"/>
          <text x="100" y="96" text-anchor="middle" fill="#f8fafc" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="54">14</text>
          <text x="100" y="134" text-anchor="middle" fill="#94a3b8" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="22">DAYS</text></svg>
        <div class="glass" id="bb" style="left:{N[3][0] - 330}px; top:{N[3][1] - 330}px; width:660px; padding:24px; text-align:center">
          <div class="t-k" style="color:#38bdf8">bimabharosa.irdai.gov.in</div><div style="font:800 40px/1.2 Inter,Arial,sans-serif; margin-top:8px">IRDAI's own complaint portal</div></div>
        <div class="node3" id="n3a" style="left:{N[3][0] - 520}px; top:{N[3][1] + 220}px">Insurer</div>
        <div class="node3" id="n3b" style="left:{N[3][0] + 220}px; top:{N[3][1] + 220}px">IRDAI tracks it</div>
        <div class="glass" id="nolaw" style="left:{N[4][0] - 1500}px; top:{N[4][1] - 420}px; width:620px; padding:26px">
          <div class="t-k" style="color:#4ade80">Insurance Ombudsman · 18 offices</div><div style="font:800 38px/1.35 Inter,Arial,sans-serif; margin-top:10px">No court case<br>No lawyer needed<br>Online · ₹0 fee</div></div>
        <div class="glass" id="data" style="left:{N[4][0] + 480}px; top:{N[4][1] - 400}px; width:880px; padding:30px; opacity:0">
          <div class="t-k">Health complaints · 2024-25</div>
          {"".join(f'<div class="fr2" id="fn{i}"><div class="fb" style="width:{w}%; background:{c}"></div><span class="mono">{v}</span> {t}</div>' for i, (w, c, v, t) in enumerate([
              (100, "#334155", "32,503", "received"), (89, "#475569", "29,017", "closed"), (63, "#0369a1", "20,440", "settled or decided"), (48, "#22c55e", "15,543", "for the policyholder")]))}
          <div class="big2"><span class="mono" id="pct" style="color:#4ade80">0%</span><span class="t-k" style="margin-left:16px">of settled or decided</span></div>
          <div class="gauge"><div class="gf" id="gf"></div></div><div class="t-k" style="margin-top:10px">78.5% closed within 3 months</div></div>
        <div class="glass" id="aw" style="left:{N[4][0] - 1500}px; top:{N[4][1] + 340}px; width:1000px; padding:28px; opacity:0">
          <div style="display:flex; gap:30px"><div style="flex:1"><div class="t-k" style="color:#38bdf8">Insurer</div><div style="font:800 36px/1.25 Inter,Arial,sans-serif">Bound by the award · up to ₹50 lakh</div></div>
          <div style="flex:1"><div class="t-k" style="color:#4ade80">You</div><div style="font:800 36px/1.25 Inter,Arial,sans-serif">Free to go to a consumer commission</div></div></div></div>
        <div class="glass" id="pen" style="left:{N[4][0] + 480}px; top:{N[4][1] + 340}px; width:880px; padding:28px; opacity:0">
          <div class="t-k" style="color:#f59e0b">Late payment after 30 days · unless the insurer appeals</div>
          <div style="font:800 54px/1.2 Inter,Arial,sans-serif; margin-top:10px">Day <span class="mono" id="day">30</span> · <span class="mono" id="pv" style="color:#4ade80">₹0</span> to you</div></div>
      </div>
      <div class="chip" id="dn" style="left:120px; top:120px; opacity:0">Don't shout · don't panic</div>
      <div class="chip amber" id="fs" style="left:120px; top:120px; opacity:0">4 steps</div>"""
    css = """.nb { position:absolute; width:120px; height:120px; border-radius:50%; background:#0f172a; border:5px solid rgba(56,189,248,.5); color:#38bdf8;
  font:800 64px/110px Inter,Arial,sans-serif; text-align:center; box-shadow:0 0 50px rgba(56,189,248,.3); }
.vault { width:640px; padding:28px; } .slot { margin-top:14px; padding:16px 20px; border-radius:12px; border:2px dashed rgba(148,163,184,.4); font:600 30px/1 Inter,Arial,sans-serif; color:#94a3b8; }
.ck { display:inline-block; width:40px; color:#4ade80; opacity:0; } .ml { margin-top:16px; padding-bottom:12px; border-bottom:1px solid rgba(148,163,184,.25); font:600 30px/1.3 Inter,Arial,sans-serif; opacity:0; }
.node3 { position:absolute; width:300px; padding:26px 0; text-align:center; border-radius:18px; background:rgba(15,23,42,.92); border:3px solid rgba(56,189,248,.5); font:800 34px/1 Inter,Arial,sans-serif; opacity:0; }
.fr2 { position:relative; margin-top:14px; height:52px; font:600 28px/52px Inter,Arial,sans-serif; padding-left:18px; } .fr2 .fb { position:absolute; left:0; top:0; height:52px; border-radius:8px; z-index:-1; transform-origin:0 50%; }
.fr2 span { font-weight:800; } .big2 { margin-top:20px; } .big2 .mono { font:800 96px/1 Inter,Arial,sans-serif; }
.gauge { margin-top:16px; height:22px; border-radius:11px; background:rgba(148,163,184,.25); overflow:hidden; } .gf { height:100%; width:78.5%; background:#38bdf8; transform-origin:0 50%; }
.city .halo { transform-box: fill-box; transform-origin: center; }"""
    s43, s45, s48, s54, s55 = sents("E043"), sents("E045"), sents("E048"), sents("E054"), sents("E055")
    cues = dict(q=S("E042")["start"], dn=s43[0]["start"], four=s43[2]["start"], s1=S("E044")["start"], pay=s45[0]["start"], copies=s45[1]["start"],
                cend=s45[1]["end"], doc=S("E046")["start"], s2=S("E047")["start"], days=S("E047", 1)["start"], gro=s48[0]["start"], state=s48[1]["start"],
                five=at("E048", "crossed five", k=1), d14=s48[2]["start"], s3=S("E049")["start"], bb=S("E050")["start"], track=S("E050", 1)["start"],
                s4=S("E051")["start"], nolaw=S("E052")["start"], cio=S("E053")["start"], body=s54[0]["start"], free=s54[2]["start"],
                rec=s55[0]["start"], dec=s55[1]["start"], three=s55[2]["start"], aw=S("E056")["start"])
    # camera: world point (x, y) centred at scale s  -> translate = screen_centre/s - point
    def camk(x, y, sc):
        return (960 / sc - x, 540 / sc - y)
    keys = [("0", (2400, 1350, 0.38)), ("C.s1 - 0.3", (2400, 1350, 0.4)), ("C.s1 + 0.9", (N[1][0] + 420, N[1][1] + 80, 1.15)),
            ("C.s2 - 0.4", (N[1][0] + 440, N[1][1] + 100, 1.22)), ("C.s2 + 1.0", (N[2][0] + 320, N[2][1] + 120, 1.05)),
            ("C.s3 - 0.4", (N[2][0] + 340, N[2][1] + 140, 1.12)), ("C.s3 + 1.0", (N[3][0], N[3][1] + 60, 1.05)),
            ("C.s4 - 0.4", (N[3][0], N[3][1] + 80, 1.12)), ("C.s4 + 1.2", (N[4][0] - 560, N[4][1], 0.72)),
            ("C.rec - 0.3", (N[4][0] - 380, N[4][1] + 60, 0.86)), ("C.rec + 1.0", (N[4][0] + 920, N[4][1] - 20, 0.95)),
            ("C.aw - 0.3", (N[4][0] + 920, N[4][1] - 20, 0.95)), ("C.aw + 1.0", (N[4][0] - 80, N[4][1] + 420, 0.6)), ("D.duration", (N[4][0] - 80, N[4][1] + 420, 0.62))]
    kx = ", ".join(f"[{t}, {camk(x, y, sc)[0]:.0f}]" for t, (x, y, sc) in keys)
    ky = ", ".join(f"[{t}, {camk(x, y, sc)[1]:.0f}]" for t, (x, y, sc) in keys)
    ks = ", ".join(f"[{t}, {sc}]" for t, (x, y, sc) in keys)
    js = f"""
      const kX = FIN.keys([{kx}]), kY = FIN.keys([{ky}]), kS = FIN.keys([{ks}]);
      FIN.hook((t) => {{ $("world").style.transform = `scale(${{kS(t)}}) translate(${{kX(t)}}px, ${{kY(t)}}px)`;
        document.querySelectorAll(".halo").forEach((h, i) => {{ const u = ((t * 0.7 + i * 0.13) % 1); h.style.transform = `scale(${{1 + u * 3}})`; h.style.opacity = 1 - u; }}); }});
      pop($("dn"), C.dn); out($("dn"), C.four - 0.2); pop($("fs"), C.four); out($("fs"), C.s1 + 0.5);
      [1, 2, 3, 4].forEach((n, i) => tl.to($("nb" + n), {{ borderColor: "#38bdf8", color: "#f8fafc", boxShadow: "0 0 80px rgba(56,189,248,.8)", duration: 0.25 }}, C.four + i * 0.25));
      const sl = [0.0, 0.25, 0.45, 0.62, 0.82].map((f) => C.copies + f * (C.cend - C.copies));
      sl.forEach((t, i) => {{ tl.to($("sl" + i), {{ borderColor: "#4ade80", color: "#f8fafc", borderStyle: "solid", duration: 0.2 }}, t); tl.to($("ck" + i), {{ opacity: 1, duration: 0.2 }}, t); }});
      pop($("tmpl"), C.doc + 0.4, {{ opacity: 0, y: 40 }});
      ["tr1", "tr2", "tr3"].forEach((id, i) => tl.to($(id), {{ stroke: "#38bdf8", duration: 0.6 }}, [C.s2, C.s3, C.s4][i] - 0.4));
      pop($("rf"), C.s2 - 0.2, {{ opacity: 0, y: 40 }});
      for (let i = 0; i < 4; i++) pop($("rf" + i), C.s2 + 0.3 + i * 0.7, {{ opacity: 0, x: -20 }});
      tl.to($("rf"), {{ opacity: 0, y: -40, duration: 0.35 }}, C.gro - 0.5); pop($("mail"), C.gro - 0.2, {{ opacity: 0, y: 40 }});
      pop($("dl"), C.days, {{ opacity: 0, x: -40 }});
      [C.gro, C.state, C.five, C.state + 6.5].forEach((t, i) => pop($("ml" + i), t, {{ opacity: 0, x: -20 }}));
      tl.to($("ringw"), {{ opacity: 1, duration: 0.3 }}, C.d14); tl.to($("ring14"), {{ strokeDashoffset: 0, duration: 2.0, ease: "none" }}, C.d14 + 0.2);
      ["rad1", "rad2"].forEach((id, i) => {{ for (let k = 0; k < 4; k++) tl.fromTo($(id), {{ attr: {{ r: 40 }}, opacity: 0.9 }}, {{ attr: {{ r: 520 }}, opacity: 0, duration: 1.6, ease: "power1.out", immediateRender: false }}, C.bb + i * 0.8 + k * 1.6); }});
      pop($("n3a"), C.bb + 2.5, {{ opacity: 0, y: 30 }}); pop($("n3b"), C.track + 1.5, {{ opacity: 0, y: 30 }});
      tl.to($("cities"), {{ opacity: 1, duration: 0.8 }}, C.s4 + 0.3); pop($("data"), C.rec, {{ opacity: 0, x: 60 }});
      for (let i = 0; i < 18; i++) tl.fromTo($("cy" + i), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, C.s4 + 0.4 + i * 0.12);
      for (let i = 0; i < 4; i++) tl.fromTo($("fn" + i).querySelector(".fb"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5 }}, C.rec + 0.4 + i * (i < 2 ? 1.4 : 1.6));
      FIN.bind($("pct"), FIN.keys([[C.dec + 0.6, 0], [C.dec + 2.4, 76]]), (v) => Math.round(v) + "%");
      tl.fromTo($("gf"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2 }}, C.three + 0.2);
      pop($("aw"), C.aw + 0.6, {{ opacity: 0, y: 30 }}); pop($("pen"), C.aw + 2.6, {{ opacity: 0, y: 30 }});
      const dayk = FIN.keys([[C.aw + 3.2, 30], [D.duration - 0.3, 60]]);
      FIN.bind($("day"), dayk, (v) => Math.round(v)); FIN.bind($("pv"), dayk, (v) => FIN.inr(Math.max(0, Math.round(v) - 30) * 5000));
"""
    put(sid, bp_page(sid, "The escalation war-room", round(end - start, 2), body, js,
                     tag="IRDAI PPI MASTER CIRCULAR 2024 · INSURANCE OMBUDSMAN RULES · CIO ANNUAL REPORT 2024-25 · OUR CALCULATION", css=css), start, end - start, cues)


def e18_checklist():
    sid = "e18_checklist"
    start, end = S("E057")["start"] - 0.3, L("E060")[1] + 0.4
    s58, s59, s60 = sents("E058"), sents("E059"), sents("E060")
    body = """
      <div class="glass ck2" id="k1" style="left:100px"><div class="nb2">1</div><div class="t-k">Proposal form</div>
        <div class="row3">High BP (on medicine) <b id="y1">☐</b></div><div class="row3">Tobacco (occasional) <b id="y2">☐</b></div>
        <div class="stp" id="dec">DECLARED</div></div>
      <div class="glass ck2" id="k2" style="left:690px"><div class="nb2">2</div><div class="t-k">Room rent clause</div>
        <div class="big3 mono" id="rr" style="color:#f87171">1% cap</div><div class="t-k" id="rrs" style="color:#f87171">Danger: proportionate cut</div>
        <div class="t-k" id="cb" style="margin-top:26px; opacity:0">Our example: <span style="color:#f87171">₹59,625</span> cut</div></div>
      <div class="glass ck2" id="k3" style="left:1280px"><div class="nb2">3</div><div class="t-k">Consumables</div>
        <div class="tray"><span>Gloves</span><span>Masks</span><span>Syringes</span></div>
        <div class="big3 mono" id="cp" style="font-size:64px; opacity:0">5–15%</div><div class="t-k" id="cps" style="opacity:0">of a bill · as reported</div>
        <div class="t-k" id="rid" style="margin-top:20px; color:#f59e0b; opacity:0">Add-on cover: check price &amp; limit</div></div>"""
    css = """.ck2 { top:200px; width:540px; height:680px; padding:40px; } .nb2 { font:800 90px/1 Inter,Arial,sans-serif; color:rgba(56,189,248,.4); margin-bottom:10px; }
.row3 { display:flex; justify-content:space-between; margin-top:24px; font:600 30px/1.3 Inter,Arial,sans-serif; } .row3 b { color:#4ade80; }
.stp { margin-top:60px; display:inline-block; padding:12px 26px; border:7px solid #38bdf8; border-radius:12px; color:#38bdf8; font:800 52px/1 Inter,Arial,sans-serif; transform:rotate(-6deg); opacity:0; }
.big3 { margin-top:40px; font:800 90px/1 Inter,Arial,sans-serif; } .tray { margin-top:30px; display:flex; gap:12px; } .tray span { padding:14px 18px; border-radius:10px; background:#1e293b; font:600 26px/1 Inter,Arial,sans-serif; }"""
    cues = dict(q=S("E057")["start"], r1=s58[0]["start"], disc=s58[1]["start"], smoke=s58[2]["start"], paper=s58[3]["start"],
                r2=s59[0]["start"], nocap=s59[1]["start"], ex=s59[2]["start"], r3=s60[0]["start"], rep=s60[2]["start"], some=s60[3]["start"], chk=s60[4]["start"])
    js = """
      for (let i = 1; i <= 3; i++) pop($("k" + i), 0.05 + (i - 1) * 0.25, { opacity: 0, y: 60 });
      tl.to([$("k2"), $("k3")], { opacity: 0.3, duration: 0.3 }, C.r1);
      tl.to($("k1"), { scale: 1.05, boxShadow: "0 0 60px rgba(56,189,248,.4)", duration: 0.3 }, C.r1);
      FIN.bind($("y1"), (t) => t > C.smoke + 0.8 ? 1 : 0, (v) => v ? "☑ Yes" : "☐"); FIN.bind($("y2"), (t) => t > C.smoke + 1.6 ? 1 : 0, (v) => v ? "☑ Yes" : "☐");
      tl.fromTo($("dec"), { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, C.paper + 0.5);
      tl.to($("k1"), { scale: 1, opacity: 0.3, boxShadow: "none", duration: 0.3 }, C.r2); tl.to($("k2"), { opacity: 1, scale: 1.05, duration: 0.3 }, C.r2);
      FIN.bind($("rr"), (t) => t > C.nocap + 0.8 ? 1 : 0, (v) => v ? "No cap" : "1% cap");
      FIN.bind($("rrs"), (t) => t > C.nocap + 0.8 ? 1 : 0, (v) => v ? "Safe: no proportionate cut" : "Danger: proportionate cut");
      tl.to([$("rr"), $("rrs")], { color: "#4ade80", duration: 0.2 }, C.nocap + 0.8);
      pop($("cb"), C.ex + 1.5, { opacity: 0 });
      tl.to($("k2"), { scale: 1, opacity: 0.3, duration: 0.3 }, C.r3); tl.to($("k3"), { opacity: 1, scale: 1.05, duration: 0.3 }, C.r3);
      pop($("cp"), C.rep + 1.5, { opacity: 0 }); pop($("cps"), C.rep + 1.8, { opacity: 0 }); pop($("rid"), C.some, { opacity: 0 });
      tl.to([$("k1"), $("k2")], { opacity: 1, duration: 0.4 }, C.chk + 0.4); tl.to($("k3"), { scale: 1, duration: 0.4 }, C.chk + 0.4);
      tl.fromTo($("stage"), { scale: 1 }, { scale: 1.03, duration: D.duration, ease: "none" }, 0);
"""
    put(sid, bp_page(sid, "Before you buy: policy x-ray", round(end - start, 2), body, js,
                     tag="SIMULATION · OUR CALCULATION · OUTLOOK MONEY | BUSINESS STANDARD", css=css), start, end - start, cues)


def e19_cheatsheet():
    sid = "e19_cheatsheet"
    start, end = S("E061")["start"] - 0.3, L("E062")[1] + 0.4
    s61 = sents("E061")
    blocks = [("5-year rule", "After 60 months of continuous cover, no rejection for non-disclosure (only established fraud)"),
              ("3-hour clock", "Final discharge approval within 3 hours; delay charges paid by the insurer"),
              ("4 steps", "Papers → reimbursement + grievance officer (14 days) → Bima Bharosa → Ombudsman (free)"),
              ("Before you buy", "Declare everything · no room rent cap · ask about consumables cover")]
    body = """
      <div id="card" style="position:absolute; left:360px; top:90px; width:1200px; height:900px; border-radius:18px; background:#f4f1ea; color:#0f172a; padding:50px 60px;
        box-shadow:0 60px 120px rgba(0,0,0,.7); transform: perspective(1600px) rotateX(14deg) rotateZ(-2deg)">
        <div style="display:flex; justify-content:space-between; align-items:baseline"><div style="font:800 46px/1 Inter,Arial,sans-serif">Cashless denied? Keep this.</div>
          <div style="font:800 22px/1 Inter,Arial,sans-serif; letter-spacing:.14em; color:#0284c7">BE PRACTICAL WITH KISHORE</div></div>
        """ + "".join(f'<div class="cb" id="cb{i}"><div class="ch">{h}</div><div class="cd">{d}</div></div>' for i, (h, d) in enumerate(blocks)) + """
        <div style="margin-top:22px; font:600 20px/1.3 Inter,Arial,sans-serif; color:#64748b">Educational only · not insurance advice · read your policy wording · sources in the description</div></div>
      <div class="chip cyan" id="ss" style="left:760px; top:40px; opacity:0">Screenshot this</div>"""
    css = """.cb { margin-top:26px; padding:20px 26px; border-left:10px solid #0284c7; background:#fff; border-radius:10px; opacity:0; }
.ch { font:800 34px/1.1 Inter,Arial,sans-serif; } .cd { margin-top:8px; font:600 26px/1.35 Inter,Arial,sans-serif; color:#334155; }"""
    cues = dict(peace=s61[0]["start"], five=s61[1]["start"], omb=s61[2]["start"], prot=s61[3]["start"], smart=S("E062")["start"])
    js = """
      tl.fromTo($("card"), { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: "power3.out" }, 0.1);
      [C.peace + 0.4, C.five, C.omb - 0.4, C.omb + 0.5].forEach((t, i) => pop($("cb" + i), t, { opacity: 0, x: -30 }));
      pop($("ss"), C.prot, { opacity: 0, y: -20 });
      tl.to($("card"), { rotationX: 4, rotationZ: 0, scale: 1.04, duration: D.duration - 1, ease: "sine.inOut" }, 0.5);
"""
    put(sid, bp_page(sid, "The citizen cheat-sheet", round(end - start, 2), body, js, tag="IRDAI · CIO · SOURCES IN DESCRIPTION", css=css), start, end - start, cues)


# ---------------- 3D document rig for real source pages ----------------
DOCS = [  # (sid, proof png, film start, film end, scan label)
    ("d_para17", "mc_para17", lambda: (S("E017")["start"] + 4.35, S("E017")["end"] + 0.45)),
    ("d_para13", "mc_para13", lambda: (S("E032")["start"] - 0.2, L("E033")[1] + 0.35)),
    ("d_para16", "mc_wait", lambda: (S("E040")["start"] - 0.2, S("E040")["end"] + 0.4)),
    ("d_para16b", "mc_para16b", lambda: (at("E040", "paid by", k=1) - 1.6, S("E040", 1)["end"] + 0.4)),
    ("d_bima", "bima_register", lambda: (S("E049")["start"] - 0.2, S("E050")["start"] + 3.0)),
    ("d_cio", "cio_online", lambda: (S("E053")["start"] - 0.2, S("E054")["start"] - 0.1)),
    ("d_h3", "cio_h3", lambda: (S("E055")["start"] - 0.2, S("E055")["start"] + 4.0)),
    ("d_50l", "cio_50lakh", lambda: (S("E056")["start"] - 0.2, S("E056")["start"] + 2.8)),
]


def docrig(sid, png, win):
    import json as _j, shutil
    start, end = win()
    d = OUT / sid / "img"; d.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parents[1] / "assets/proof" / f"{png}.png"
    from PIL import Image
    im = Image.open(src).convert("RGB")
    if im.width > 2600:
        im = im.resize((im.width // 2, im.height // 2))
    im.save(d / "page.jpg", quality=90)
    b = _j.loads((src.with_suffix(".json")).read_text())
    cx, cy = (b["x0"] + b["x1"]) / 2, (b["y0"] + b["y1"]) / 2
    bw = b["x1"] - b["x0"]
    zt = max(1.8, min(3.0, 0.85 / max(0.2, bw)))
    dur = end - start
    body = f"""
      <div id="rig" style="position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:{cx * 1920:.0f}px {cy * 1080:.0f}px">
        <img src="img/page.jpg" style="position:absolute; inset:0; width:1920px; height:1080px"/>
        <div id="scan" style="position:absolute; left:{b['x0'] * 1920 - 30:.0f}px; width:{bw * 1920 + 60:.0f}px; top:{b['y0'] * 1080 - 40:.0f}px; height:4px;
          background:#38bdf8; box-shadow:0 0 24px 6px rgba(56,189,248,.8); opacity:0"></div>
      </div>
      <div id="spot" style="position:absolute; inset:0; background: radial-gradient(circle at {cx * 100:.1f}% {cy * 100:.1f}%, rgba(0,0,0,0) 18%, rgba(2,6,15,.55) 60%); opacity:0"></div>"""
    js = f"""
      tl.fromTo($("rig"), {{ rotationX: 16, rotationY: -10, scale: 0.92, transformPerspective: 1800 }},
        {{ rotationX: 0, rotationY: 0, scale: {zt:.2f}, duration: Math.min(2.6, D.duration * 0.55), ease: "power2.inOut" }}, 0);
      tl.to($("rig"), {{ scale: {zt * 1.06:.2f}, x: -20, duration: Math.max(0.5, D.duration - 2.6), ease: "none" }}, Math.min(2.6, D.duration * 0.55));
      tl.to($("spot"), {{ opacity: 1, duration: 0.8 }}, 0.6);
      tl.fromTo($("scan"), {{ opacity: 0.95, y: 0 }}, {{ y: {(b['y1'] - b['y0']) * 1080 + 80:.0f}, duration: 1.1, ease: "power1.inOut" }}, Math.min(1.4, D.duration * 0.35));
      tl.to($("scan"), {{ opacity: 0, duration: 0.3 }}, Math.min(2.6, D.duration * 0.35 + 1.1));
"""
    html = page(sid, f"Document rig: {png}", round(dur, 2), body, js, tag="", bg="", css="")
    html = html.replace('<div class="fin-bg" style="background-image: url(\'\')"></div>\n      <div class="hc-grade"></div>', '<div style="position:absolute; inset:0; background:#0b1530"></div>')
    put(sid, html, start, dur, {})


def make_docs():
    for sid, png, win in DOCS:
        docrig(sid, png, win)


CH4 = [e17_warroom, e18_checklist, e19_cheatsheet, make_docs]
ENGINES += CH4

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for f in ENGINES:
        if not only or f.__name__ in only:
            f()
