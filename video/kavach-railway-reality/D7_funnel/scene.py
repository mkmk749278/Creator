TITLE = "D7 Fitted is not working"
CSS = """
  #fn { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .ax { font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #94A3B8; }
  .bl { font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.14em; }
  .bn { font: 800 64px Inter, Arial, sans-serif; font-variant-numeric: tabular-nums; letter-spacing: -0.01em; }
  .strip { position: absolute; padding: 16px 18px 12px; background: #FBFAF7; border-radius: 4px; box-shadow: 0 18px 40px rgba(0,0,0,0.5); opacity: 0; }
  .strip img { display: block; width: 1500px; height: auto; }
  .strip .src { position: absolute; right: 14px; top: -34px; font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.14em; color: #CBD5E1; background: rgba(15,23,42,0.9); padding: 4px 10px; border-radius: 6px; }
  #s1 { left: 150px; top: 250px; transform: rotate(-1.2deg); } #s2 { left: 200px; top: 440px; transform: rotate(0.8deg); } #s3 { left: 170px; top: 630px; transform: rotate(-0.6deg); }
  #stamp { left: 1190px; top: 585px; font-size: 52px; opacity: 0; white-space: nowrap; }
  #loco { position: absolute; left: 1490px; top: 250px; width: 360px; opacity: 0; }
  #loco .k { font: 800 96px Inter, Arial, sans-serif; color: #F8FAFC; font-variant-numeric: tabular-nums; line-height: 1; margin-top: 18px; }
  #loco .u { font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #94A3B8; margin-top: 10px; }
"""
BODY = """  <svg id="fn" viewBox="0 0 1920 1080" data-layout-allow-overflow>
    <defs>
      <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <pattern id="hatch" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="22" height="22" fill="rgba(245,158,11,0.06)"/><line x1="0" y1="0" x2="0" y2="22" stroke="rgba(245,158,11,0.28)" stroke-width="6"/></pattern>
      <linearGradient id="steel" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#64748B"/><stop offset="1" stop-color="#334155"/></linearGradient>
      <linearGradient id="cy" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7DD3FC"/><stop offset="1" stop-color="#0284C7"/></linearGradient>
      <clipPath id="streamclip"><rect id="streamrect" x="0" y="0" width="0" height="0"/></clipPath>
    </defs>
    <g id="world">
      <g id="ghost" opacity="0"><path id="gA" fill="none" stroke="rgba(148,163,184,0.22)" stroke-width="2" stroke-dasharray="6 8"/><path id="gB" fill="none" stroke="rgba(148,163,184,0.22)" stroke-width="2" stroke-dasharray="6 8"/><rect id="gC" fill="none" stroke="rgba(148,163,184,0.22)" stroke-width="2" stroke-dasharray="6 8"/></g>
      <g id="bandA" opacity="0"><path id="pA" fill="url(#hatch)" stroke="#F59E0B" stroke-width="3" stroke-dasharray="14 10"/>
        <text id="lA" class="bl" text-anchor="middle" fill="#FCD34D">WORK STARTED</text>
        <text id="nA" class="bn" text-anchor="middle" fill="#F8FAFC">0</text></g>
      <g id="bandB" opacity="0"><path id="pB" fill="url(#steel)" stroke="#94A3B8" stroke-width="2"/>
        <text id="lB" class="bl" text-anchor="middle" fill="#E2E8F0">FITTED</text>
        <text id="nB" class="bn" text-anchor="middle" fill="#F8FAFC">0</text></g>
      <g id="bandC" opacity="0"><rect id="pC" fill="url(#cy)" filter="url(#glow)"/>
        <g id="flow" clip-path="url(#streamclip)"></g>
        <text id="lC" class="bl" fill="#7DD3FC">KAVACH 4.0 WORKING</text>
        <text id="nC" class="bn" fill="#F8FAFC">2,633</text>
        <text id="sC" class="ax" fill="#94A3B8">ROUTE KM · 31 JUL 2026</text></g>
      <g id="kmscale" opacity="0"><text id="kmu" class="ax">WIDTH = ROUTE KM</text></g>
      <g id="prot" opacity="0"><text id="tprot" class="bl" fill="#F87171">NOT YET PROTECTED</text></g>
    </g>
  </svg>
  <div class="strip" id="s1"><div class="src">PIB · 05 AUG 2026</div><img src="pib_row7726.jpg" alt="PIB release: Installation of Track side equipment 7,726 RKm"/></div>
  <div class="strip" id="s2"><div class="src">PIB · 05 AUG 2026</div><img src="pib_row6290.jpg" alt="PIB release: Provision of Kavach in Loco 6,290 Nos."/></div>
  <div class="strip" id="s3"><div class="src">PIB · 05 AUG 2026</div><img src="pib_line21794.jpg" alt="PIB release: work taken up on 21,794 RKM"/></div>
  <div id="loco">
    <svg width="360" height="120" viewBox="0 0 360 120" data-layout-allow-overflow>
      <path d="M20 30 L250 30 C300 30 330 55 340 92 L20 92 Z" fill="#1E293B" stroke="#94A3B8" stroke-width="3"/>
      <rect x="40" y="42" width="60" height="26" rx="4" fill="#0F172A" stroke="#64748B" stroke-width="2"/><rect x="120" y="42" width="60" height="26" rx="4" fill="#0F172A" stroke="#64748B" stroke-width="2"/>
      <path d="M250 40 C285 42 306 56 316 72 L250 72 Z" fill="#0F2A4A"/>
      <rect x="20" y="80" width="320" height="6" fill="#0284C7"/>
      <circle cx="70" cy="102" r="13" fill="#334155" stroke="#94A3B8" stroke-width="3"/><circle cx="120" cy="102" r="13" fill="#334155" stroke="#94A3B8" stroke-width="3"/>
      <circle cx="240" cy="102" r="13" fill="#334155" stroke="#94A3B8" stroke-width="3"/><circle cx="290" cy="102" r="13" fill="#334155" stroke="#94A3B8" stroke-width="3"/>
      <g id="lchip"><rect x="146" y="2" width="92" height="22" rx="5" fill="#0B2540" stroke="#38BDF8" stroke-width="2"/><text x="192" y="18" text-anchor="middle" style="font: 800 13px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #E0F2FE">KAVACH</text></g>
    </svg>
    <div class="k" id="nL">0</div><div class="u">ENGINES FITTED</div>
  </div>
  <div class="kav-stamp" id="stamp">FITTED ≠ WORKING</div>"""
JS = """
  // funnel widths are to scale: 1,300 px = 21,794 route km (PIB 05 Aug 2026 figures)
  const S = 1300 / 21794, CX = 760, wA = 21794 * S, wB = 7726 * S, wC = 2633 * S;
  const yA0 = 250, yA1 = 450, yB0 = 470, yB1 = 670, yC0 = 690, yC1 = 960;
  const trap = (y0, y1, w0, w1) => `M ${CX - w0 / 2} ${y0} L ${CX + w0 / 2} ${y0} L ${CX + w1 / 2} ${y1} L ${CX - w1 / 2} ${y1} Z`;
  const $ = (id) => document.getElementById(id), set = (id, a) => { for (const k in a) $(id).setAttribute(k, a[k]); };
  set("pA", { d: trap(yA0, yA1, wA, wB) }); set("lA", { x: CX, y: yA0 + 62 }); set("nA", { x: CX, y: yA0 + 136 });
  set("pB", { d: trap(yB0, yB1, wB, wC) }); set("lB", { x: CX, y: yB0 + 56 }); set("nB", { x: CX, y: yB0 + 126 });
  set("gA", { d: trap(yA0, yA1, wA, wB) }); set("gB", { d: trap(yB0, yB1, wB, wC) }); set("gC", { x: CX - wC / 2, y: yC0, width: wC, height: yC1 - yC0, rx: 6 });
  set("pC", { x: CX - wC / 2, y: yC0, width: wC, height: yC1 - yC0, rx: 6 });
  set("streamrect", { x: CX - wC / 2, y: yC0, width: wC, height: yC1 - yC0 });
  set("lC", { x: CX + wC / 2 + 36, y: yC0 + 50 }); set("nC", { x: CX + wC / 2 + 36, y: yC0 + 120 }); set("sC", { x: CX + wC / 2 + 40, y: yC0 + 160 });
  set("kmu", { x: CX - wA / 2, y: yA0 - 22 }); set("tprot", { x: CX + wA / 2 - 360, y: yA0 - 22 });
  // particles flowing down the working stream (positions are a pure function of time)
  const NS = "http://www.w3.org/2000/svg", flow = $("flow"), r = mulberry32(35), parts = [];
  for (let i = 0; i < 26; i++) { const c = document.createElementNS(NS, "rect"); c.setAttribute("width", 6); c.setAttribute("height", 26); c.setAttribute("rx", 3); c.setAttribute("fill", "#E0F2FE"); flow.appendChild(c); parts.push({ c, x: CX - wC / 2 + 12 + r() * (wC - 30), ph: r(), sp: 140 + r() * 80 }); }
  const fl = { t: 0 };
  tl.to(fl, { t: D, duration: D, ease: "none", onUpdate: () => { for (const p of parts) { const y = yC0 + ((p.ph * 300 + fl.t * p.sp) % (yC1 - yC0 + 30)) - 30; p.c.setAttribute("x", p.x); p.c.setAttribute("y", y); p.c.setAttribute("opacity", 0.55); } } }, 0);

  const tH = at("V035", "here's the trap"), tF = at("V035", "Track fitted"), tFn = at("V035", "seven thousand seven"), tE = at("V035", "engines fitted"),
        tEn = at("V035", "six thousand two"), tW = at("V035", "track where work"), tWn = at("V035", "twenty one thousand"),
        tB = at("V035", "but fitted"), tP = at("V035", "work started isn't");
  // 1) the real PIB lines behind the headline numbers slide in, then leave
  ["#s1", "#s2", "#s3"].forEach((s, i) => { tl.fromTo(s, { x: -900, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, Math.max(0.1, tH - 0.6) + i * 0.3);
    tl.to(s, { x: "+=60", duration: tF - tH + 0.3, ease: "none" }, tH + i * 0.3); });
  tl.to(["#s1", "#s2", "#s3"], { opacity: 0, y: -30, duration: 0.45, stagger: 0.08 }, tF - 0.35);
  // 2) fitted band, 3) engines, 4) work-started band (widest), 5) the thin working stream + stamp, 6) not protected
  const cnt = (id, v, t, d = 1.3) => { const o = { v: 0 }; tl.to(o, { v, duration: d, ease: "power2.out", onUpdate: () => $(id).textContent = Math.round(o.v).toLocaleString("en-IN") }, t); };
  tl.to("#ghost", { opacity: 1, duration: 0.8 }, tF - 0.6);
  tl.fromTo("#bandB", { opacity: 0, scale: 0.92, svgOrigin: `${CX} ${yB0}` }, { opacity: 1, scale: 1, duration: 0.6, ease: "power2.out" }, tF - 0.1);
  cnt("nB", 7726, tFn - 0.2);
  tl.fromTo("#loco", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, tE - 0.2);
  cnt("nL", 6290, tEn - 0.2);
  tl.fromTo("#bandA", { opacity: 0, scale: 0.9, svgOrigin: `${CX} ${yA1}` }, { opacity: 1, scale: 1, duration: 0.7, ease: "power2.out" }, tW - 0.1);
  tl.to("#kmscale", { opacity: 1, duration: 0.5 }, tW + 0.4);
  cnt("nA", 21794, tW + 0.1, Math.max(1.5, tWn - tW + 0.9));
  tl.fromTo("#bandC", { opacity: 0 }, { opacity: 1, duration: 0.5 }, tB - 0.5);
  tl.fromTo("#pC", { attr: { height: 0 } }, { attr: { height: yC1 - yC0 }, duration: 0.9, ease: "power2.inOut" }, tB - 0.5);
  tl.fromTo("#stamp", { opacity: 0, scale: 1.6, rotation: -14 }, { opacity: 0.94, scale: 1, rotation: -8, duration: 0.28, ease: "power4.in" }, tB + 0.5);
  tl.fromTo("#world", { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 3 }, tB + 0.78);
  tl.to("#prot", { opacity: 1, duration: 0.4 }, tP);
  tl.to("#pA", { attr: { "stroke-dashoffset": -96 }, duration: D - tP, ease: "none" }, tP);
  tl.to("#bandA", { opacity: 0.55, duration: 0.6 }, tP + 0.2);
  tl.fromTo("#fn", { transformOrigin: "760px 560px", scale: 1.0 }, { scale: 1.05, duration: D, ease: "sine.inOut" }, 0);
"""
