TITLE = "B4 Kavach knows the signal ahead and brakes early"
LIBS = ["fogview.js", "tele.js"]
BG = "none"
CSS = """
  #fog { position: absolute; left: 0; top: 0; width: 960px; height: 1080px; }
  #right { position: absolute; left: 960px; top: 0; width: 960px; height: 1080px; background: #0B1220 url(slate.jpg) center/cover; }
  #dmi { position: absolute; left: 1060px; top: 250px; width: 800px; height: 560px; }
  #seam { position: absolute; left: 958px; top: 0; width: 4px; height: 1080px; background: #000; }
  #xx { position: absolute; left: 330px; top: 300px; width: 300px; height: 300px; }
  #full { position: absolute; inset: 0; width: 1920px; height: 1080px; background: #0F172A url(slate.jpg) center/cover; clip-path: inset(0 0 0 100%); }
  .dl { font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #94A3B8; }
  .dn { font: 800 64px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
  .ax { font: 600 20px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.06em; }
  .fl { font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.14em; }
"""
BODY = """  <canvas id="fog" width="960" height="1080"></canvas>
  <img id="fogimg" src="fog.png" alt="" style="display:none" />
  <div id="right"></div>
  <svg id="dmi" viewBox="0 0 800 560" data-layout-allow-overflow>
    <rect id="dbez" x="4" y="4" width="792" height="552" rx="28" fill="rgba(8,12,20,0.95)" stroke="#1E293B" stroke-width="4"/>
    <g id="don" opacity="0">
      <text x="40" y="62" class="dl" style="fill:#7DD3FC">KAVACH · CAB DISPLAY</text>
      <path d="M 120 420 A 170 170 0 1 1 400 420" fill="none" stroke="#1E293B" stroke-width="22"/>
      <path id="perm" d="M 120 420 A 170 170 0 1 1 400 420" fill="none" stroke="#0284C7" stroke-width="22" stroke-dasharray="560 2000"/>
      <line id="needle" x1="260" y1="320" x2="260" y2="180" stroke="#F8FAFC" stroke-width="8" stroke-linecap="round"/>
      <circle cx="260" cy="320" r="14" fill="#F8FAFC"/>
      <text id="spd" x="260" y="410" text-anchor="middle" class="dn">110</text>
      <text x="260" y="450" text-anchor="middle" class="dl">KM/H</text>
      <rect x="520" y="110" width="92" height="210" rx="16" fill="#0B1220" stroke="#334155" stroke-width="3"/>
      <circle cx="566" cy="160" r="30" fill="#EF4444"/><circle cx="566" cy="230" r="30" fill="#2A2410"/><circle id="aspg" cx="566" cy="290" r="22" fill="#0E2416"/>
      <text x="566" y="370" text-anchor="middle" class="dl">SIGNAL</text>
      <text x="630" y="130" class="dl">TARGET</text>
      <text id="tgt" x="630" y="196" class="dn" style="font-size:50px">1,500</text>
      <text x="630" y="232" class="dl">METRES</text>
      <rect x="700" y="270" width="26" height="230" rx="8" fill="#1E293B"/>
      <rect id="tbar" x="700" y="270" width="26" height="230" rx="8" fill="#F59E0B"/>
    </g>
  </svg>
  <div id="seam"></div>
  <svg id="xx" viewBox="0 0 300 300"><path d="M 40 40 L 260 260 M 260 40 L 40 260" stroke="#DC2626" stroke-width="22" stroke-linecap="round"/></svg>
  <svg id="full" viewBox="300 150 1480 832" data-layout-allow-overflow></svg>
  <div class="kav-label" id="lab1">Target distance<small>KAVACH KNOWS THE SIGNAL AHEAD</small></div>"""
JS = """
  const FV = FogView(document.getElementById("fog"), document.getElementById("fogimg"));
  const V = 110 / 3.6, st = { travel: 300, zsig: 400, t: 0 }, clock = { t: 0 };
  tl.to(clock, { t: D, duration: D, ease: "none", onUpdate: () => { st.t = clock.t + 17; st.travel = 300 + V * clock.t; FV.draw(st); } }, 0);
  const tG = CUES.cues.V029.at, tK = at("V029", "it already knows"), tS = at("V029", "shows it on the screen"), tB = at("V029", "brakes early");
  tl.to("#xx", { opacity: 0, duration: 0.4 }, 0.2);
  // the cab display wakes up; target distance counts down while the fog still hides the signal
  tl.to("#dbez", { attr: { stroke: "#38BDF8" }, duration: 0.5 }, tG + 0.3);
  tl.to("#don", { opacity: 1, duration: 0.6 }, tG + 0.4);
  const needle = document.getElementById("needle");
  const setNeedle = (v) => { const a = (-135 + 270 * v / 160) * Math.PI / 180; needle.setAttribute("x2", 260 + 140 * Math.sin(a)); needle.setAttribute("y2", 320 - 140 * Math.cos(a)); document.getElementById("spd").textContent = Math.round(v); };
  setNeedle(110);
  const tg = { m: 1500 };
  const setT = () => { document.getElementById("tgt").textContent = Math.round(tg.m).toLocaleString("en-IN"); document.getElementById("tbar").setAttribute("height", 230 * tg.m / 1500); document.getElementById("tbar").setAttribute("y", 270 + 230 * (1 - tg.m / 1500)); };
  setT();
  tl.to(tg, { m: 1500 - V * (tB - tK + 0.5), duration: tB - tK + 0.5, ease: "none", onUpdate: setT }, tK);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tK);
  tl.to("#dbez", { attr: { "stroke-width": 9 }, duration: 0.4, yoyo: true, repeat: 3 }, tS);
  // brakes early: the split opens into a full-width view of the braking curve drawn ahead of the train
  const full = document.getElementById("full"), E = KT.el;
  KT.rail(full, 640);
  const sig = E("g", {}, full);
  E("line", { x1: 1660, y1: 640, x2: 1660.3, y2: 470, stroke: "#5B6B86", "stroke-width": 7 }, sig);
  E("rect", { x: 1634, y: 340, width: 52, height: 132, rx: 12, fill: "#0B1220", stroke: "#5B6B86", "stroke-width": 3 }, sig);
  E("circle", { cx: 1660, cy: 364, r: 15, fill: "#F87171" }, sig);
  const sl = E("text", { x: 1616, y: 360, "text-anchor": "end", class: "fl", fill: "#FCA5A5" }, sig); sl.textContent = "RED SIGNAL";
  const train = KT.trainset(full, "tr", 640);
  const curve = E("path", { d: "M 400 430 L 760 430 C 1000 430, 1260 480, 1430 600", fill: "none", stroke: "#38BDF8", "stroke-width": 6, "stroke-linecap": "round" }, full);
  const bp = E("g", { opacity: 0 }, full);
  E("circle", { cx: 760, cy: 430, r: 12, fill: "#38BDF8" }, bp);
  const bt = E("text", { x: 760, y: 400, "text-anchor": "middle", class: "fl", fill: "#7DD3FC" }, bp); bt.textContent = "KAVACH BRAKES";
  const stp = E("g", { opacity: 0 }, full);
  E("line", { x1: 1430, y1: 620, x2: 1430.3, y2: 700, stroke: "#38BDF8", "stroke-width": 4 }, stp);
  E("path", { d: "M 1440 690 L 1650 690.4", stroke: "#22C55E", "stroke-width": 4, "stroke-dasharray": "8 8" }, stp);
  const rt = E("text", { x: 1545, y: 730, "text-anchor": "middle", class: "fl", fill: "#86EFAC" }, stp); rt.textContent = "ROOM TO SPARE";
  const dim = E("g", { opacity: 0 }, full);
  E("path", { d: "M 760 760 L 1660 760.4 M 760 744 L 760 776 M 1660 744 L 1660 776", stroke: "#F59E0B", "stroke-width": 3, fill: "none" }, dim);
  E("path", { d: "M 760 760 L 780 750 L 780 770 Z M 1660 760 L 1640 750 L 1640 770 Z", fill: "#F59E0B" }, dim);
  const dt = E("text", { x: 1210, y: 806, "text-anchor": "middle", class: "fl", fill: "#FCD34D" }, dim); dt.textContent = "TARGET DISTANCE";
  const L = curve.getTotalLength(); curve.setAttribute("stroke-dasharray", L); curve.setAttribute("stroke-dashoffset", L);
  tl.to("#full", { clipPath: "inset(0 0 0 0%)", duration: 0.8, ease: "power3.inOut" }, tB - 1.2);
  tl.to("#dmi, #fog, #right", { opacity: 0, duration: 0.3 }, tB - 0.6);
  tl.fromTo(train, { x: 200 }, { x: 360, duration: 1.2, ease: "none" }, tB - 1.2);
  tl.to(curve, { attr: { "stroke-dashoffset": 0 }, duration: 1.6, ease: "power2.out" }, tB - 0.5);
  tl.to(bp, { opacity: 1, duration: 0.3 }, tB - 0.1);
  tl.fromTo(dim, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.5 }, tB + 0.3);
  tl.to(train, { x: 1390, duration: D - tB - 0.2, ease: "power2.out" }, tB);
  tl.to(stp, { opacity: 1, duration: 0.4 }, D - 1.4);
  tl.to("#lab1", { opacity: 0, duration: 0.3 }, tB - 1.2);
"""
