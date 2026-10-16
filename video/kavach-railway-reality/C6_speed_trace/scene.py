TITLE = "C6 Goods train 78 km/h, impact at about 40"
HUD = "17.06.2024 · 08:50 · RANGAPANI–CHATTERHAT"
LIBS = ["kanchan.js"]
CSS = """
  #chart { position: absolute; left: 620px; top: 540px; width: 1080px; height: 356px; }
  .ax { font: 600 20px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.08em; }
  .big { font: 800 40px Inter, Arial, sans-serif; fill: #F8FAFC; }
  #flash { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: radial-gradient(circle at 1290px 400px, rgba(254,202,202,0.75), rgba(220,38,38,0.4) 12%, rgba(220,38,38,0) 32%); opacity: 0; }
"""
BODY = """  <svg id="schem" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="flash" data-layout-allow-occlusion></div>
  <svg id="chart" viewBox="0 0 1000 330" data-layout-allow-overflow>
    <rect x="0" y="0" width="1000" height="330" rx="16" fill="rgba(11,18,32,0.9)" stroke="#334155" stroke-width="2"/>
    <text x="30" y="44" class="ax">GOODS TRAIN SPEED</text>
    <text x="970" y="44" text-anchor="end" class="ax" style="font-size:22px">SHAPE ILLUSTRATIVE · CRS FIGURES</text>
    <line x1="80" y1="290" x2="960" y2="290" stroke="#475569" stroke-width="2"/>
    <line x1="80" y1="290" x2="80" y2="70" stroke="#475569" stroke-width="2"/>
    <line id="g78" x1="80" y1="103" x2="960" y2="103" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.6"/>
    <line id="g40" x1="80" y1="194" x2="960" y2="194" stroke="#F87171" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.0"/>
    <text x="68" y="109" text-anchor="end" class="ax">78</text><text x="68" y="200" text-anchor="end" class="ax">40</text><text x="68" y="296" text-anchor="end" class="ax">0</text>
    <path id="trace" d="M 80 250 C 200 230, 300 120, 420 104 L 680 103 C 720 104, 760 150, 800 194" fill="none" stroke="#F8FAFC" stroke-width="5" stroke-linecap="round"/>
    <circle id="dot" r="9" fill="#F8FAFC"/>
    <g id="imp" opacity="0"><circle cx="800" cy="194" r="16" fill="#DC2626"/><circle id="impr" cx="800" cy="194" r="16" fill="none" stroke="#DC2626" stroke-width="4"/></g>
    <text id="t78" x="440" y="88" class="big" opacity="0">78 KM/H</text>
    <text id="t40" x="830" y="180" class="big" style="fill:#FCA5A5" opacity="0">≈ 40</text>
  </svg>
  <div class="kav-label red" id="lab1">78 km/h<span id="l40" style="opacity:0"> → ≈ 40 km/h</span><small>GOODS TRAIN · <span id="lsub">TOP SPEED</span></small></div>
  <div class="kav-label red" id="lab2">No Kavach here<small>ON THAT SECTION</small></div>"""
JS = """
  const S = buildKanchan();
  tl.set(".asig .lamp-on", { opacity: 0 }, 0); tl.set(".asig rect", { attr: { stroke: "#7F1D1D" } }, 0); tl.set(".lbl", { opacity: 0 }, 0); tl.set(".asig text", { opacity: 0 }, 0);
  tl.fromTo("#world", { transformOrigin: "50% 50%", scale: 0.95, x: 0, y: -150 }, { scale: 1.0, x: -30, y: -160, duration: D, ease: "sine.inOut" }, 0);
  const t78 = at("V050", "seventy eight"), tHit = at("V050", "hit the Kanchanjunga"), t40 = at("V050", "at about forty"), tNo = at("V050", "And there was no working Kavach");
  // goods train closes the gap: fast run, braking late, contact at tHit + ~1.2 s (no wreck shown)
  tl.set("#pass", { x: 1300 }, 0);

  // contact lands exactly when the trace reaches "about forty" (tC)
  const tC = t40 + 0.2;
  tl.fromTo("#goods", { x: 300 }, { x: 1140, duration: tC - 1.65, ease: "power1.in" }, 0);
  tl.to("#goods", { x: 1300 + 96, duration: 1.65, ease: "power2.out" }, tC - 1.65);
  tl.to("#pass", { x: 1322, duration: 0.6, ease: "power2.out" }, tC);
  tl.to("#goods", { x: 1322 + 96, duration: 0.6, ease: "power2.out" }, tC);
  tl.to("#flash", { opacity: 1, duration: 0.08 }, tC).to("#flash", { opacity: 0, duration: 0.9 }, tC + 0.1);
  // speed trace drawn in step with the VO; dot rides the path as a pure function of time
  tl.from("#chart", { opacity: 0, y: 40, duration: 0.7, ease: "power3.out" }, 0.2);
  const p = document.getElementById("trace"), L = p.getTotalLength(); p.setAttribute("stroke-dasharray", L); p.setAttribute("stroke-dashoffset", L);
  const o = { u: 0 }, dot = document.getElementById("dot");
  const place = () => { const q = p.getPointAtLength(o.u * L); dot.setAttribute("cx", q.x); dot.setAttribute("cy", q.y); p.setAttribute("stroke-dashoffset", L * (1 - o.u)); };
  place();
  tl.to(o, { u: 0.62, duration: t78 + 0.6, ease: "none", onUpdate: place }, 0.3);
  tl.to(o, { u: 1, duration: (t40 + 0.2) - (t78 + 0.9), ease: "none", onUpdate: place }, t78 + 0.9);
  tl.to("#t78", { opacity: 1, duration: 0.3 }, t78);
  tl.to("#trace", { attr: { stroke: "#F87171" }, duration: 0.4 }, t40);
  tl.to("#g40", { opacity: 0.6, duration: 0.4 }, t40);
  tl.to("#imp", { opacity: 1, duration: 0.2 }, t40 + 0.2);
  tl.fromTo("#impr", { attr: { r: 16 }, opacity: 1 }, { attr: { r: 60 }, opacity: 0, duration: 0.9, repeat: 2 }, t40 + 0.2);
  tl.to("#t40", { opacity: 1, duration: 0.3 }, t40 + 0.2);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, t78);
  // the impact speed is revealed only at the impact
  tl.to("#l40", { opacity: 1, duration: 0.3 }, t40 + 0.2);
  tl.set("#lsub", { textContent: "AT IMPACT" }, t40 + 0.2);
  tl.to("#lab1", { opacity: 0, duration: 0.3 }, tNo - 0.2);
  tl.to("#lab2", { opacity: 1, duration: 0.5 }, tNo);
  tl.to("#chart", { opacity: 0.45, duration: 0.6 }, tNo);
  // the Kavach coverage that is not there: a dashed cyan bracket along the DN line, struck through in crimson
  const NSs = "http://www.w3.org/2000/svg", nk = document.createElementNS(NSs, "g"); nk.setAttribute("id", "nok");
  nk.innerHTML = `<path id="nkb" d="M 120 ${S.Y + 52} L 120 ${S.Y + 70} L 1800 ${S.Y + 70.5} L 1800 ${S.Y + 52}" fill="none" stroke="#38BDF8" stroke-width="4" stroke-dasharray="12 10"/>
    <text x="960" y="${S.Y + 124}" text-anchor="middle" style="font: 800 44px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #F87171">NO KAVACH ON THIS SECTION</text>
    <line id="nks" x1="660" y1="${S.Y + 108}" x2="1260" y2="${S.Y + 108.5}" stroke="#DC2626" stroke-width="0" stroke-linecap="round"/>`;
  S.q("#world").appendChild(nk);
  tl.set("#nok", { opacity: 0 }, 0);
  tl.to("#nok", { opacity: 1, duration: 0.4 }, tNo);
  tl.from("#nkb", { attr: { "stroke-dashoffset": 400 }, duration: 1.2, ease: "none" }, tNo);
  tl.from("#nks", { attr: { x2: 880 }, duration: 0.4, ease: "power2.out" }, tNo + 0.7);
  tl.to("#nkb", { attr: { stroke: "#475569" }, duration: 0.4 }, tNo + 0.9);
"""
