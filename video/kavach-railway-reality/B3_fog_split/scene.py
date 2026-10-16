TITLE = "B3 Fog: 50 m in about 1.6 s"
LIBS = ["fogview.js"]
BG = "none"
CSS = """
  #fog { position: absolute; left: 0; top: 0; width: 960px; height: 1080px; }
  #right { position: absolute; left: 960px; top: 0; width: 960px; height: 1080px; background: #0B1220 url(slate.jpg) center/cover; }
  #dmi { position: absolute; left: 1150px; top: 300px; width: 600px; height: 400px; border-radius: 22px; border: 3px solid #1E293B; background: rgba(8,12,20,0.9); }
  #dmi .off { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.2em; color: #7C8BA1; }
  #seam { position: absolute; left: 958px; top: 0; width: 4px; height: 1080px; background: #000; }
  #watch { position: absolute; left: 650px; top: 130px; width: 220px; height: 220px; opacity: 0; }
  #wnum { position: absolute; left: 610px; top: 362px; width: 300px; text-align: center; font: 800 54px Inter, Arial, sans-serif; color: #F8FAFC; font-variant-numeric: tabular-nums; opacity: 0; background: rgba(15,23,42,0.88); border-radius: 14px; padding: 6px 0; }
  #react { position: absolute; left: 110px; top: 720px; width: 460px; height: 120px; opacity: 0; overflow: visible; }
  .rl { font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #E2E8F0; }
  #dim { position: absolute; left: 0; top: 0; width: 960px; height: 1080px; }
  #xx { position: absolute; left: 330px; top: 300px; width: 300px; height: 300px; opacity: 0; }
  #flash { position: absolute; left: 0; top: 0; width: 960px; height: 1080px; background: #F8FAFC; opacity: 0; }
"""
BODY = """  <canvas id="fog" width="960" height="1080"></canvas>
  <img id="fogimg" src="fog.png" alt="" style="display:none" />
  <div id="right"></div>
  <div id="dmi"><div class="off">CAB DISPLAY</div></div>
  <div id="seam"></div>
  <svg id="dim" viewBox="0 0 960 1080" data-layout-allow-overflow>
    <g id="dimg" opacity="0"><rect x="570" y="742" width="330" height="104" rx="12" fill="rgba(15,23,42,0.88)"/><line id="dl" x1="560" y1="980" x2="560" y2="560" stroke="#F59E0B" stroke-width="4" stroke-dasharray="10 8"/>
      <text x="580" y="790" style="font: 800 40px Inter, Arial, sans-serif; fill: #FCD34D">50 M</text>
      <text x="580" y="830" style="font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.16em; fill: #FDE68A">VISIBILITY · EXAMPLE</text></g>
  </svg>
  <svg id="watch" viewBox="0 0 220 220">
    <circle cx="110" cy="110" r="96" fill="rgba(15,23,42,0.85)" stroke="#F8FAFC" stroke-width="5"/>
    <path id="arc" d="M 110 110" fill="rgba(245,158,11,0.35)"/>
    <line id="hand" x1="110" y1="110" x2="110" y2="26" stroke="#F59E0B" stroke-width="6" stroke-linecap="round"/>
    <circle cx="110" cy="110" r="9" fill="#F8FAFC"/></svg>
  <div id="wnum">0.0 s</div>
  <svg id="react" viewBox="0 0 460 120">
    <rect x="-14" y="-6" width="488" height="128" rx="14" fill="rgba(15,23,42,0.88)"/><text x="0" y="22" class="rl">HUMAN REACTION</text>
    <rect x="0" y="40" width="460" height="34" rx="8" fill="rgba(15,23,42,0.85)" stroke="#64748B" stroke-width="2"/>
    <rect id="rfill" x="2" y="42" width="0" height="30" rx="6" fill="#F59E0B"/>
    <line id="pmark" x1="0" y1="34" x2="0.3" y2="82" stroke="#DC2626" stroke-width="4" opacity="0"/>
    <text id="ptxt" x="0" y="108" class="rl" style="fill:#FCA5A5" opacity="0">PASSED</text></svg>
  <svg id="xx" viewBox="0 0 300 300"><path d="M 40 40 L 260 260 M 260 40 L 40 260" stroke="#DC2626" stroke-width="22" stroke-linecap="round"/></svg>
  <div id="flash" data-layout-allow-occlusion></div>
  <div class="kav-label amber" id="lab1">Visibility 50 m · example<small>110 KM/H ≈ 1.6 S</small></div>"""
JS = """
  const FV = FogView(document.getElementById("fog"), document.getElementById("fogimg"));
  const V = 110 / 3.6;                                        // 30.6 m/s
  const tS = at("V028", "Suppose"), t50 = at("V028", "fifty metres ahead"), tC = at("V028", "the train crosses"), tR = at("V028", "even an alert person"), tE = at("V028", "On eyes alone");
  const st = { travel: 0, zsig: 400, t: 0 };
  const draw = () => FV.draw(st);
  const clock = { t: 0 };
  tl.to(clock, { t: D, duration: D, ease: "none", onUpdate: () => { st.t = clock.t; draw(); } }, 0);
  // 1) running in fog; the signal resolves at the visibility limit and the picture freezes at 50 m
  tl.to(st, { travel: V * (t50 + 0.4), duration: t50 + 0.4, ease: "none", onUpdate: draw }, 0);
  tl.fromTo(st, { zsig: 50 + V * 1.6 }, { zsig: 50, duration: 1.6, ease: "none", onUpdate: draw }, t50 + 0.4 - 1.6);
  tl.to("#dimg", { opacity: 1, duration: 0.4 }, t50 + 0.4);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, t50 + 0.4);
  // 2) real time: 50 m at 110 km/h; the stopwatch stops at about 1.6 s
  const T = 50 / V, sw = { s: 0 };
  const watch = () => {
    const a = (sw.s / 2) * 2 * Math.PI, x = 110 + 84 * Math.sin(a), y = 110 - 84 * Math.cos(a);
    document.getElementById("hand").setAttribute("x2", x); document.getElementById("hand").setAttribute("y2", y);
    document.getElementById("arc").setAttribute("d", sw.s <= 0 ? "M 110 110" : `M 110 110 L 110 26 A 84 84 0 ${a > Math.PI ? 1 : 0} 1 ${x} ${y} Z`);
    document.getElementById("wnum").textContent = `${sw.s.toFixed(1)} s`;
  };
  watch();
  tl.to("#watch, #wnum", { opacity: 1, duration: 0.3 }, tC - 0.4);
  tl.to("#dimg", { opacity: 0, duration: 0.3 }, tC + 0.1);
  tl.to(st, { zsig: 50 - V * 2.2, travel: V * (t50 + 0.4) + V * 2.2, duration: 2.2, ease: "none", onUpdate: draw }, tC + 0.2);
  tl.to(sw, { s: T, duration: T, ease: "none", onUpdate: watch }, tC + 0.2);
  tl.to("#wnum", { color: "#FCD34D", duration: 0.2 }, tC + 0.2 + T);
  tl.to(st, { travel: "+=" + (V * (tR - tC - 2.6)), duration: Math.max(0.3, tR - tC - 2.6), ease: "none", onUpdate: draw }, tC + 2.4);
  // 3) replay: a reaction of a second or two is still running when the signal has gone past
  tl.to("#flash", { opacity: 0.6, duration: 0.06 }, tR - 0.1).to("#flash", { opacity: 0, duration: 0.3 }, tR - 0.04);
  tl.set(st, { zsig: 50, onUpdate: draw }, tR);
  tl.to("#watch, #wnum", { opacity: 0, duration: 0.2 }, tR);
  tl.to("#react", { opacity: 1, duration: 0.3 }, tR);
  tl.to(st, { zsig: 50 - V * 2.4, travel: "+=" + V * 2.4, duration: 2.4, ease: "none", onUpdate: draw }, tR + 0.1);
  tl.to("#rfill", { attr: { width: 456 }, duration: 2.0, ease: "none" }, tR + 0.1);
  const px = 456 * (T / 2.0);
  tl.set("#pmark", { attr: { x1: px, x2: px + 0.3 } }, 0); tl.set("#ptxt", { attr: { x: px - 40 } }, 0);
  tl.to("#pmark, #ptxt", { opacity: 1, duration: 0.15 }, tR + 0.1 + T);
  tl.to(st, { travel: "+=" + V * Math.max(0.3, D - tR - 2.5), duration: Math.max(0.3, D - tR - 2.5), ease: "none", onUpdate: draw }, tR + 2.5);
  // 4) on eyes alone, the maths does not work
  tl.fromTo("#xx", { opacity: 0, scale: 1.4, transformOrigin: "50% 50%" }, { opacity: 0.9, scale: 1, duration: 0.35, ease: "back.out(2)" }, tE);
  tl.to("#lab1", { opacity: 0, duration: 0.3 }, tE);
  draw();
"""
