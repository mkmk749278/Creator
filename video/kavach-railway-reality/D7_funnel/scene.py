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
  #stamp { left: 1180px; top: 700px; font-size: 56px; opacity: 0; white-space: nowrap; }
  #loco { position: absolute; left: 1330px; top: 650px; width: 360px; opacity: 0; }
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
      <text id="kmu" class="ax" x="150" y="226" opacity="0" style="font-size:24px">BAR LENGTH = ROUTE KM, TO SCALE</text>
      <g id="bandA" opacity="0"><rect id="gA" x="150" y="250" height="150" rx="10" fill="none" stroke="rgba(148,163,184,0.3)" stroke-width="2" stroke-dasharray="6 8"/>
        <rect id="pA" x="150" y="250" width="0" height="150" rx="10" fill="url(#hatch)" stroke="#F59E0B" stroke-width="3" stroke-dasharray="14 10"/>
        <text id="lA" class="bl" x="180" y="306" fill="#FCD34D">WORK STARTED</text>
        <text id="nA" class="bn" x="180" y="378" fill="#F8FAFC">0</text></g>
      <g id="bandB" opacity="0"><rect id="pB" x="150" y="470" width="0" height="150" rx="10" fill="url(#steel)" stroke="#94A3B8" stroke-width="2"/>
        <text id="lB" class="bl" x="180" y="526" fill="#E2E8F0">TRACK FITTED</text>
        <text id="nB" class="bn" x="180" y="598" fill="#F8FAFC">0</text></g>
      <g id="bandC" opacity="0"><rect id="pC" x="150" y="690" width="0" height="150" rx="10" fill="url(#cy)" filter="url(#glow)"/>
        <rect id="pC2" x="150" y="690" width="0" height="150" rx="10" fill="#B45309" opacity="0.85"/>
        <g id="flow" clip-path="url(#streamclip)"></g>
        <text id="lC" class="bl" fill="#7DD3FC">WORKING</text>
        <text id="nC" class="bn" fill="#F8FAFC">2,633</text>
        <text id="sC" class="ax" fill="#CBD5E1" style="font-size:24px">KAVACH 4.0 · 31 JUL 2026</text>
        <text id="sC2" class="ax" fill="#FCD34D" style="font-size:24px">+ 1,465 OLDER VERSION 3.2</text></g>
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
  // bars to scale: 1,500 px = 21,794 route km (PIB 05 Aug 2026 figures); working = Kavach 4.0 2,633 + version 3.2 1,465 (D6)
  const S = 1500 / 21794, X0 = 150, wA = 21794 * S, wB = 7726 * S, wC = 2633 * S, wC2 = 1465 * S, yC0 = 690, yC1 = 840;
  const $ = (id) => document.getElementById(id), set = (id, a) => { for (const k in a) $(id).setAttribute(k, a[k]); };
  set("gA", { width: wA }); set("streamrect", { x: X0, y: yC0, width: wC, height: yC1 - yC0 });
  set("lC", { x: X0 + wC + wC2 + 36, y: yC0 + 44 }); set("nC", { x: X0 + wC + wC2 + 36, y: yC0 + 112 }); set("sC", { x: X0 + wC + wC2 + 40, y: yC0 + 146 });
  set("sC2", { x: X0 + wC + wC2 + 40, y: yC0 + 178 });
  // particles flowing along the working bar (pure function of time)
  const NS = "http://www.w3.org/2000/svg", flow = $("flow"), r = mulberry32(35), parts = [];
  for (let i = 0; i < 18; i++) { const c = document.createElementNS(NS, "rect"); c.setAttribute("width", 26); c.setAttribute("height", 6); c.setAttribute("rx", 3); c.setAttribute("fill", "#E0F2FE"); flow.appendChild(c); parts.push({ c, y: yC0 + 14 + r() * (yC1 - yC0 - 30), ph: r(), sp: 120 + r() * 80 }); }
  const fl = { t: 0 };
  tl.to(fl, { t: D, duration: D, ease: "none", onUpdate: () => { for (const p of parts) { const x = X0 + ((p.ph * 300 + fl.t * p.sp) % (wC + 30)) - 30; p.c.setAttribute("x", x); p.c.setAttribute("y", p.y); p.c.setAttribute("opacity", 0.55); } } }, 0);

  const tH = at("V035", "here's the trap"), tF = at("V035", "Track fitted"), tFn = at("V035", "seven thousand seven"), tE = at("V035", "engines fitted"),
        tEn = at("V035", "six thousand two"), tW = at("V035", "track where work"), tWn = at("V035", "twenty one thousand"),
        tB = at("V035", "but fitted"), tP = at("V035", "work started isn't");
  // 1) the real PIB lines behind the headline numbers slide in, then leave
  ["#s1", "#s2", "#s3"].forEach((s, i) => { tl.fromTo(s, { x: -900, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, Math.max(0.1, tH - 0.6) + i * 0.3);
    tl.to(s, { x: "+=60", duration: tF - tH + 0.3, ease: "none" }, tH + i * 0.3); });
  tl.to(["#s1", "#s2", "#s3"], { opacity: 0, y: -30, duration: 0.45, stagger: 0.08 }, tF - 0.35);
  // 2) fitted bar grows, 3) engines, 4) work-started bar (longest), 5) the short working bar + stamp, 6) not protected
  const cnt = (id, v, t, d = 1.3) => { const o = { v: 0 }; tl.to(o, { v, duration: d, ease: "power2.out", onUpdate: () => $(id).textContent = Math.round(o.v).toLocaleString("en-IN") }, t); };
  tl.to("#kmu", { opacity: 1, duration: 0.5 }, tF);
  tl.to("#bandB", { opacity: 1, duration: 0.3 }, tF - 0.1);
  tl.to("#pB", { attr: { width: wB }, duration: tFn - tF + 1.0, ease: "power2.out" }, tF); cnt("nB", 7726, tF, tFn - tF + 1.0);
  tl.fromTo("#loco", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, tE - 0.2);
  cnt("nL", 6290, tEn - 0.2);
  tl.to("#bandA", { opacity: 1, duration: 0.3 }, tW - 0.1);
  tl.to("#pA", { attr: { width: wA }, duration: Math.max(1.5, tWn - tW + 0.9), ease: "power2.out" }, tW + 0.1); cnt("nA", 21794, tW + 0.1, Math.max(1.5, tWn - tW + 0.9));
  tl.to("#loco", { opacity: 0, duration: 0.4 }, tB - 0.9);
  tl.to("#bandC", { opacity: 1, duration: 0.3 }, tB - 0.5);
  tl.to("#pC", { attr: { width: wC }, duration: 0.8, ease: "power2.out" }, tB - 0.5);
  tl.to("#pC2", { attr: { x: X0 + wC, width: wC2 }, duration: 0.6, ease: "power2.out" }, tB + 0.1);
  tl.fromTo("#stamp", { opacity: 0, scale: 1.6, rotation: -14 }, { opacity: 0.94, scale: 1, rotation: -8, duration: 0.28, ease: "power4.in" }, tB + 0.5);
  tl.fromTo("#world", { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 3 }, tB + 0.78);
  // "work started isn't protected": the started bar's label turns red; one stamp stays the only punchline
  tl.to("#lA", { textContent: "WORK STARTED · NOT YET PROTECTED", fill: "#F87171", duration: 0.01 }, tP);
  tl.to("#pA", { attr: { "stroke-dashoffset": -96 }, duration: D - tP, ease: "none" }, tP);
  tl.to("#bandA", { opacity: 0.75, duration: 0.6 }, tP + 0.2);
  tl.fromTo("#fn", { transformOrigin: "760px 560px", scale: 1.0 }, { scale: 1.04, duration: D, ease: "sine.inOut" }, 0);
"""
