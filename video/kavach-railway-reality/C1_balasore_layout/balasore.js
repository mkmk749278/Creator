/* Balasore (Bahanaga Bazar) forensic schematic for C1-C3: a generic top-down track diagram on an investigator's light
   table. NOT a traced station drawing (labelled ILLUSTRATION by the assembler). Facts it shows (CRS Abstracts 2024-25,
   Accident III): green home signal for run-through on the UP main; crossover 17A/B set towards the UP loop, where a goods
   train stood. Builds into <svg id="schem"> and returns handles for the scene's timeline. */
window.buildBalasore = function () {
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.getElementById("schem");
  const Y_MAIN = 600, Y_LOOP = 430, Y_DOWN = 770;
  const X_PTS = 820, X_LOOP0 = 1000, X_LOOP1 = 1700, X_PTS2 = 1880;
  // track = sleepers + two rails (a wide light stroke under a narrower slate stroke)
  const track = (d, dim = 1) => `
    <path d="${d}" fill="none" stroke="#2B3A57" stroke-width="30" stroke-dasharray="5 11" opacity="${0.9 * dim}"/>
    <path d="${d}" fill="none" stroke="#9FB0C8" stroke-width="15" opacity="${0.85 * dim}"/>
    <path d="${d}" fill="none" stroke="#13203A" stroke-width="9"/>`;
  const MAIN = `M -400 ${Y_MAIN} L 2400 ${Y_MAIN}`;
  const DOWN = `M -400 ${Y_DOWN} L 2400 ${Y_DOWN}`;
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
    <linearGradient id="trainC" x1="0" x2="1"><stop offset="0" stop-color="#E9F4FF"/><stop offset="1" stop-color="#9ED8FF"/></linearGradient>
    <linearGradient id="wagon" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7A2A22"/><stop offset="1" stop-color="#4A1712"/></linearGradient>
  </defs>
  <g id="world">
    <g id="grid" opacity="0.5">${Array.from({length: 44}, (_, i) => `<line x1="${-400 + i * 70}" y1="-200" x2="${-400 + i * 70}" y2="1300" stroke="rgba(148,163,184,0.07)" stroke-width="1"/>`).join("")}
      ${Array.from({length: 22}, (_, i) => `<line x1="-400" y1="${-200 + i * 70}" x2="2600" y2="${-200 + i * 70}" stroke="rgba(148,163,184,0.07)" stroke-width="1"/>`).join("")}</g>
    <g id="masts">${Array.from({length: 18}, (_, i) => `<g transform="translate(${-300 + i * 150} 0)"><rect x="-5" y="${Y_MAIN + 70}" width="10" height="10" fill="#5B6B86"/><line x1="0" y1="${Y_MAIN + 75}" x2="0" y2="${Y_MAIN - 40}" stroke="rgba(148,163,184,0.25)" stroke-width="2"/><rect x="-5" y="${Y_LOOP - 80}" width="10" height="10" fill="#5B6B86" opacity="${-300 + i * 150 > 980 && -300 + i * 150 < 1720 ? 1 : 0}"/></g>`).join("")}</g>
    <g id="platform" opacity="0.55">
      <rect x="1040" y="${Y_MAIN + 52}" width="760" height="58" rx="4" fill="#1C2A45" stroke="#2E4268" stroke-width="2"/>
      <text x="1420" y="${Y_MAIN + 90}" text-anchor="middle" class="tlabel" opacity="0.8">PLATFORM</text>
    </g>
    <g id="tracks">
      <g id="t-down">${track(DOWN, 0.55)}</g>
      <g id="t-main">${track(MAIN)}</g>
      <g id="t-xover">${track(XOVER)}</g>
      <g id="t-loop">${track(LOOP)}</g>
      <g id="t-xout">${track(XOUT)}</g>
    </g>
    <text x="120" y="${Y_MAIN - 34}" class="tlabel">UP MAIN</text>
    <text x="1060" y="${Y_LOOP - 34}" class="tlabel">UP LOOP</text>
    <text id="lbl-down" x="1240" y="${Y_DOWN - 34}" class="tlabel" opacity="0.6">DOWN MAIN</text>
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
    <!-- home signal: mast + three-aspect head, side-on above the up main -->
    <g id="signal" transform="translate(640 ${Y_MAIN - 30})">
      <line x1="0" y1="0" x2="0" y2="-120" stroke="#5B6B86" stroke-width="7"/>
      <rect x="-26" y="-246" width="52" height="132" rx="12" fill="#0B1220" stroke="#5B6B86" stroke-width="3"/>
      <circle id="lamp-r" cx="0" cy="-222" r="15" fill="#3A1414"/>
      <circle id="lamp-y" cx="0" cy="-180" r="15" fill="#3A2E10"/>
      <circle id="lamp-g" cx="0" cy="-138" r="15" fill="#10331D"/>
      <circle id="lamp-g-on" cx="0" cy="-138" r="15" fill="#4ADE80" filter="url(#glow)" opacity="0"/>
      <circle id="lamp-r-on" cx="0" cy="-222" r="15" fill="#F87171" filter="url(#glow)" opacity="1"/>
      <text x="40" y="-170" class="tlabel">HOME</text>
    </g>
    <!-- Coromandel Express: loco + coaches, running left to right on the up main -->
    <g id="coro">${rake(-1180, 12, 74, 8, Y_MAIN, "url(#trainC)", "#38BDF8", "coro-rake")}
      <path d="M -180 ${Y_MAIN - 16} L -120 ${Y_MAIN - 16} Q -96 ${Y_MAIN} -120 ${Y_MAIN + 16} L -180 ${Y_MAIN + 16} Z" fill="#F8FAFC" stroke="#38BDF8" stroke-width="2"/>
      <circle cx="-108" cy="${Y_MAIN}" r="5" fill="#FDE68A" filter="url(#glow)"/>
    </g>
    <g id="speed" opacity="0"><rect x="-300" y="${Y_MAIN + 40}" width="210" height="58" rx="8" fill="rgba(15,23,42,0.85)" stroke="#38BDF8" stroke-width="2"/>
      <text x="-195" y="${Y_MAIN + 81}" text-anchor="middle" class="tnum">≈ 128 KM/H</text></g>
  </g>`;
  const q = (s) => svg.querySelector(s);
  return { svg, q, Y_MAIN, Y_LOOP, X_PTS };
};
