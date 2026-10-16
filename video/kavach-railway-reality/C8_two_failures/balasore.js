/* Balasore (Bahanaga Bazar) forensic schematic for C1-C3: a generic top-down track diagram on an investigator's light
   table. NOT a traced station drawing (labelled ILLUSTRATION by the assembler). Facts it shows (CRS Abstracts 2024-25,
   Accident III): green home signal for run-through on the UP main; crossover 17A/B set towards the UP loop, where a goods
   train stood. Builds into <svg id="schem"> and returns handles for the scene's timeline. */
window.buildBalasore = function () {
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.getElementById("schem");
  // four lines as at Bahanaga Bazar (Commons "Odisha crash" diagram after the CRS report), drawn mirrored top-to-bottom:
  // up loop (goods train), up main (Coromandel), down main (SMVT Bengaluru-Howrah), down loop (goods train)
  const Y_MAIN = 560, Y_LOOP = 400, Y_DOWN = 700, Y_DLOOP = 840;
  const X_PTS = 820, X_LOOP0 = 1000, X_LOOP1 = 1700, X_PTS2 = 1880;
  // track = sleepers + two rails (a wide light stroke under a narrower slate stroke)
  const track = (d, dim = 1) => `
    <path d="${d}" fill="none" stroke="#2B3A57" stroke-width="30" stroke-dasharray="5 11" opacity="${0.9 * dim}"/>
    <path d="${d}" fill="none" stroke="#9FB0C8" stroke-width="15" opacity="${0.85 * dim}"/>
    <path d="${d}" fill="none" stroke="#13203A" stroke-width="9"/>`;
  const MAIN = `M -400 ${Y_MAIN} L 2400 ${Y_MAIN}`;
  const DOWN = `M -400 ${Y_DOWN} L 2400 ${Y_DOWN}`;
  const DLOOP = `M ${X_PTS + 60} ${Y_DOWN} L ${X_LOOP0 + 60} ${Y_DLOOP} L ${X_LOOP1 - 60} ${Y_DLOOP} L ${X_PTS2 - 60} ${Y_DOWN}`;
  const XOVER = `M ${X_PTS} ${Y_MAIN} L ${X_LOOP0} ${Y_LOOP}`;
  const LOOP = `M ${X_LOOP0} ${Y_LOOP} L ${X_LOOP1} ${Y_LOOP}`;
  const XOUT = `M ${X_LOOP1} ${Y_LOOP} L ${X_PTS2} ${Y_MAIN}`;
  // coaches: rounded segments along a horizontal line
  const rake = (x0, n, len, gap, y, fill, stroke, id) => {
    let s = `<g id="${id}">`;
    for (let i = 0; i < n; i++) s += `<rect x="${x0 + i * (len + gap)}" y="${y - 15}" width="${len}" height="30" rx="7" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
    return s + "</g>";
  };
  svg.innerHTML = `
  <defs>
    <filter id="glow" filterUnits="userSpaceOnUse" x="-600" y="-400" width="3400" height="2000"><feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="trainC" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#C62828"/><stop offset="0.42" stop-color="#C62828"/><stop offset="0.43" stop-color="#B8BEC6"/><stop offset="0.62" stop-color="#B8BEC6"/><stop offset="0.63" stop-color="#9E1C1C"/><stop offset="1" stop-color="#9E1C1C"/></linearGradient>
    <linearGradient id="trainB" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#1E3A8A"/><stop offset="0.5" stop-color="#2563EB"/><stop offset="1" stop-color="#1E3A8A"/></linearGradient>
    <linearGradient id="wagon" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7A2A22"/><stop offset="1" stop-color="#4A1712"/></linearGradient>
  </defs>
  <g id="world">
    <g id="grid" opacity="0.5">${Array.from({length: 44}, (_, i) => `<line x1="${-400 + i * 70}" y1="-200" x2="${-400 + i * 70}" y2="1300" stroke="rgba(148,163,184,0.07)" stroke-width="1"/>`).join("")}
      ${Array.from({length: 22}, (_, i) => `<line x1="-400" y1="${-200 + i * 70}" x2="2600" y2="${-200 + i * 70}" stroke="rgba(148,163,184,0.07)" stroke-width="1"/>`).join("")}</g>
    <g id="masts">${Array.from({length: 18}, (_, i) => `<g transform="translate(${-300 + i * 150} 0)"><rect x="-5" y="${Y_MAIN + 70}" width="10" height="10" fill="#5B6B86"/><line x1="0" y1="${Y_MAIN + 75}" x2="0" y2="${Y_MAIN - 40}" stroke="rgba(148,163,184,0.25)" stroke-width="2"/><rect x="-5" y="${Y_LOOP - 80}" width="10" height="10" fill="#5B6B86" opacity="${-300 + i * 150 > 980 && -300 + i * 150 < 1720 ? 1 : 0}"/></g>`).join("")}</g>
    <g id="platform"></g>
    <g id="tracks">
      <g id="t-down">${track(DOWN, 0.55)}</g>
      <g id="t-dloop">${track(DLOOP, 0.55)}</g>
      <g id="t-main">${track(MAIN)}</g>
      <g id="t-xover">${track(XOVER)}</g>
      <g id="t-loop">${track(LOOP)}</g>
      <g id="t-xout">${track(XOUT)}</g>
    </g>
    <text x="120" y="${Y_MAIN - 34}" class="tlabel">UP MAIN</text>
    <text x="1060" y="${Y_LOOP - 34}" class="tlabel">UP LOOP</text>
    <text id="lbl-down" x="1250" y="${Y_DOWN + 58}" class="tlabel" opacity="0.6">DOWN MAIN</text>
    <text x="1060" y="${Y_DLOOP + 62}" class="tlabel" opacity="0.6">DOWN LOOP</text>
    <!-- the route the signal promised (main) and the route the points actually set (loop) -->
    <path id="route-main" d="M 640 ${Y_MAIN} L 2300 ${Y_MAIN + 0.6}" fill="none" stroke="#22C55E" stroke-width="10" stroke-linecap="round" filter="url(#glow)" opacity="0"/>
    <path id="route-loop" d="M 640 ${Y_MAIN} L ${X_PTS} ${Y_MAIN} L ${X_LOOP0} ${Y_LOOP} L ${X_LOOP1 - 60} ${Y_LOOP}" fill="none" stroke="#DC2626" stroke-width="10" stroke-linecap="round" filter="url(#glow)" opacity="0"/>
    <!-- points 17A/B: a switch blade that swings from straight to diverging -->
    <g id="points" transform="translate(${X_PTS - 70} ${Y_MAIN})">
      <circle r="30" fill="none" stroke="#F59E0B" stroke-width="3" opacity="0.0" id="pts-ring"/>
      <line id="blade" x1="0" y1="0" x2="110" y2="0" stroke="#F59E0B" stroke-width="6" stroke-linecap="round"/>
      <circle r="8" fill="#F59E0B"/>
    </g>
    <text id="pts-label" x="${X_PTS + 30}" y="${Y_MAIN + 62}" class="tlabel amber" opacity="0">17A/B</text>
    ${rake(1130, 9, 50, 7, Y_LOOP, "url(#wagon)", "#DC2626", "goods")}
    <text id="goods-label" x="1130" y="${Y_LOOP + 58}" class="tlabel red" opacity="0">GOODS TRAIN · STANDING</text>
    ${rake(1130, 9, 50, 7, Y_DLOOP, "url(#wagon)", "#7C2D12", "goods2")}
    <g id="bnc">${rake(1500, 10, 74, 8, Y_DOWN, "url(#trainB)", "#93C5FD", "bnc-rake")}
      <path d="M 1500 ${Y_DOWN - 16} L 1440 ${Y_DOWN - 16} Q 1416 ${Y_DOWN} 1440 ${Y_DOWN + 16} L 1500 ${Y_DOWN + 16} Z" fill="#D9C27A" stroke="#F8FAFC" stroke-width="2"/>
      <text x="1420" y="${Y_DOWN - 30}" class="tlabel" style="font-size:18px" opacity="0.85">BENGALURU–HOWRAH EXP ←</text></g>
    <!-- home signal: mast + three-aspect head, side-on above the up main -->
    <g id="signal">${window.indianSignal(640, Y_MAIN - 26, { id: "hs", plate: "S12", scale: 1.15 }).replace('id="hs-g"', 'id="lamp-g-on"').replace('id="hs-r"', 'id="lamp-r-on"')}
      <text x="604" y="${Y_MAIN - 160}" text-anchor="end" class="tlabel">HOME</text></g>
    <!-- Coromandel Express: loco + coaches, running left to right on the up main -->
    <g id="coro">${rake(-1180, 12, 74, 8, Y_MAIN, "url(#trainC)", "#FCA5A5", "coro-rake")}
      <path d="M -180 ${Y_MAIN - 16} L -120 ${Y_MAIN - 16} Q -96 ${Y_MAIN} -120 ${Y_MAIN + 16} L -180 ${Y_MAIN + 16} Z" fill="#D9C27A" stroke="#F8FAFC" stroke-width="2"/>
      <circle cx="-108" cy="${Y_MAIN}" r="5" fill="#FDE68A" filter="url(#glow)"/>
    </g>
    <g id="speed" opacity="0"><rect x="-300" y="${Y_MAIN + 40}" width="210" height="58" rx="8" fill="rgba(15,23,42,0.85)" stroke="#38BDF8" stroke-width="2"/>
      <text x="-195" y="${Y_MAIN + 81}" text-anchor="middle" class="tnum">≈ 128 KM/H</text></g>
  </g>`;
  const q = (s) => svg.querySelector(s);
  return { svg, q, Y_MAIN, Y_LOOP, Y_DOWN, Y_DLOOP, X_PTS };
};

/* End state of C1 (points set to the loop, crimson route, train stopped short of the points) for C2/C3 openings. */
window.balasoreEndState = function (tl, S) {
  const L = S.q("#route-loop").getTotalLength();
  S.q("#route-loop").setAttribute("stroke-dasharray", L);
  tl.set("#route-loop", { opacity: 1, attr: { "stroke-dashoffset": 0 } }, 0);
  tl.set("#route-main", { opacity: 0.3, attr: { "stroke-dasharray": "none" } }, 0);
  tl.set("#lamp-r-on", { opacity: 0 }, 0); tl.set("#lamp-g-on", { opacity: 1 }, 0);
  tl.set("#blade", { rotation: -36, svgOrigin: "0 0" }, 0);
  tl.set("#pts-label", { opacity: 1 }, 0);
  tl.set("#coro", { x: 828 }, 0); tl.set("#lbl-down", { opacity: 0 }, 0);
};

/* A Kavach unit badge riding on the Coromandel's loco (loco nose sits at x = 732 after the C1 run). */
window.addKavachBadge = function (S) {
  // badge above the loco, right of the home signal (the four-line layout leaves no room below)
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  g.setAttribute("id", "kbadge");
  const bx = 850, by = S.Y_MAIN - 190;
  g.innerHTML = `
    <line x1="706" y1="${S.Y_MAIN - 16}" x2="${bx - 40}" y2="${by + 54}" stroke="#38BDF8" stroke-width="3"/>
    <circle id="kring" cx="${bx}" cy="${by + 27}" r="54" fill="none" stroke="#38BDF8" stroke-width="3" opacity="0.6"/>
    <rect x="${bx - 80}" y="${by}" width="160" height="54" rx="10" fill="#0B2540" stroke="#38BDF8" stroke-width="3" filter="url(#glow)"/>
    <text x="${bx}" y="${by + 36}" text-anchor="middle" style="font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #E0F2FE">KAVACH</text>`;
  S.q("#world").appendChild(g);
  g.bx = bx; g.by = by;
  return g;
};
