TITLE = "C7 Simulation: with Kavach, held to a slow speed"
HUD = "SIMULATION · IF KAVACH HAD BEEN WORKING"
LIBS = ["kanchan.js"]
CSS = """
  #scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(248,250,252,0.06) 0 2px, rgba(0,0,0,0) 2px 7px); opacity: 0; }
  #rw { position: absolute; left: 96px; top: 130px; font: 800 44px Inter, Arial, sans-serif; letter-spacing: 0.12em; color: #F8FAFC; opacity: 0; }
  #spd { position: absolute; left: 0; top: 0; }
"""
BODY = """  <svg id="schem" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="scan" data-layout-allow-occlusion></div>
  <div id="rw">◀◀ REWIND</div>
  <div class="kav-label" id="lab1">Simulation<small>BOTH TRAINS FITTED · SECTION WORKING</small></div>"""
JS = """
  const S = buildKanchan();
  tl.set(".asig .lamp-on", { opacity: 0 }, 0); tl.set(".asig rect", { attr: { stroke: "#7F1D1D" } }, 0); tl.set(".lbl", { opacity: 0 }, 0); tl.set(".asig text", { opacity: 0 }, 0);
  tl.fromTo("#world", { transformOrigin: "50% 50%", scale: 1.15, x: 40, y: 60 }, { scale: 1.24, x: -40, y: 50, duration: D, ease: "sine.inOut" }, 0);
  // open on C6's last frame (contact), then rewind fast with scan lines
  tl.set("#pass", { x: 1322 }, 0); tl.set("#goods", { x: 1418 }, 0);
  tl.to("#scan", { opacity: 1, duration: 0.1 }, 0.15);
  tl.to("#rw", { opacity: 1, duration: 0.1 }, 0.15);
  tl.to("#goods", { x: 620, duration: 1.4, ease: "power2.inOut" }, 0.25);
  tl.to("#pass", { x: 1300, duration: 0.3 }, 0.25);
  tl.to("#scan", { y: 14, duration: 1.4, ease: "steps(20)" }, 0.25);
  tl.to("#scan, #rw", { opacity: 0, duration: 0.2 }, 1.65);
  // Kavach on both trains and on the section
  const tF = at("V051", "With both trains fitted"), tW = at("V051", "the section working"), tH = at("V051", "it could have held");
  const kg = kanchanBadge(S, "#goods", -150, "KAVACH"), kp = kanchanBadge(S, "#pass", 150, "KAVACH");
  tl.set([kg, kp], { opacity: 0 }, 0);
  tl.fromTo(kg, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(2)" }, tF);
  tl.fromTo(kp, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(2)" }, tF + 0.35);
  const NSs = "http://www.w3.org/2000/svg", sec = document.createElementNS(NSs, "g"); sec.setAttribute("id", "sec");
  sec.innerHTML = `<path id="secb" d="M 120 ${S.Y - 248} L 120 ${S.Y - 266} L 1800 ${S.Y - 266.5} L 1800 ${S.Y - 248}" fill="none" stroke="#38BDF8" stroke-width="5"/>
    <text x="960" y="${S.Y - 284}" text-anchor="middle" style="font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.16em; fill: #7DD3FC">KAVACH SECTION</text>`;
  S.q("#world").appendChild(sec);
  const Ls = S.q("#secb").getTotalLength(); S.q("#secb").setAttribute("stroke-dasharray", Ls); S.q("#secb").setAttribute("stroke-dashoffset", Ls);
  tl.set("#sec", { opacity: 0 }, 0);
  tl.to("#sec", { opacity: 1, duration: 0.3 }, tW);
  tl.to("#secb", { attr: { "stroke-dashoffset": 0 }, duration: 1.2, ease: "power2.out" }, tW);
  tl.to(".asig rect", { attr: { stroke: "#0E7490" }, duration: 0.6 }, tW + 0.4);
  // held to a slow speed past the failed signals; its braking curve ends short of the express
  tl.to("#goods", { x: 960, duration: D - tH, ease: "none" }, tH);
  const cv = document.createElementNS(NSs, "path"); cv.setAttribute("id", "curve");
  cv.setAttribute("d", `M 0 ${S.Y - 26} C 120 ${S.Y - 26}, 230 ${S.Y - 22}, 300 ${S.Y - 2}`);
  cv.setAttribute("fill", "none"); cv.setAttribute("stroke", "#38BDF8"); cv.setAttribute("stroke-width", "5");
  const cvg = document.createElementNS(NSs, "g"); cvg.setAttribute("id", "cvg"); cvg.appendChild(cv);
  cvg.insertAdjacentHTML("beforeend", `<line x1="300" y1="${S.Y - 40}" x2="300" y2="${S.Y + 36}" stroke="#38BDF8" stroke-width="4"/>
    <text x="310" y="${S.Y - 48}" style="font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #7DD3FC">STOPS SHORT</text>`);
  S.q("#goods").appendChild(cvg);
  const Lc = cv.getTotalLength(); cv.setAttribute("stroke-dasharray", Lc); cv.setAttribute("stroke-dashoffset", Lc);
  tl.set("#cvg", { opacity: 0, x: -96 }, 0);
  tl.to("#cvg", { opacity: 1, duration: 0.3 }, tH + 1.0);
  tl.to(cv, { attr: { "stroke-dashoffset": 0 }, duration: 1.4, ease: "power2.out" }, tH + 1.0);
  tl.to("#lab1", { opacity: 1, duration: 0.6 }, 1.8);
  // live speed tag on the goods train: 78 km/h in the real run, held slow here (what Kavach enforces depends on its set-up)
  const tag = document.createElementNS(NSs, "g"); tag.setAttribute("id", "gtag");
  tag.innerHTML = `<rect x="-300" y="${S.Y - 120}" width="300" height="62" rx="12" fill="rgba(15,23,42,0.94)" stroke="#38BDF8" stroke-width="3"/>
    <text id="gt1" x="-150" y="${S.Y - 78}" text-anchor="middle" style="font: 800 30px Inter, Arial, sans-serif; fill: #FCA5A5">78 KM/H</text>
    <line id="gts" x1="-218" y1="${S.Y - 88}" x2="-218" y2="${S.Y - 88}" stroke="#DC2626" stroke-width="5"/>
    <text id="gt2" x="-150" y="${S.Y - 78}" text-anchor="middle" style="font: 800 30px Inter, Arial, sans-serif; fill: #7DD3FC" opacity="0">HELD SLOW</text>`;
  S.q("#goods").appendChild(tag);
  tl.fromTo("#gtag", { opacity: 0 }, { opacity: 1, duration: 0.3 }, tF);
  tl.to("#gts", { attr: { x2: -82 }, duration: 0.3 }, tH);
  tl.to("#gt1, #gts", { opacity: 0, duration: 0.3 }, tH + 0.5);
  tl.to("#gt2", { opacity: 1, duration: 0.3 }, tH + 0.6);
"""
