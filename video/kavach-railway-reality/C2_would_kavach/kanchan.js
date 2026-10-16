/* Kanchanjunga (Rangapani-Chatterhat) forensic schematic for C4-C7: a generic double-line automatic-signalling section
   (labelled ILLUSTRATION / SIMULATION by the assembler; not a traced drawing). Facts it shows (CRS Abstracts 2024-25,
   Accident XI): automatic signals failed; trains ran on paper authority; DN GFCJ container train reached 78 km/h and hit
   DN 13174 Kanchanjunga Express from behind at about 40 km/h; no working Kavach on the section (Railway Board, Jun 2024). */
window.buildKanchan = function (opts = {}) {
  const svg = document.getElementById("schem");
  const Y = 560, Y_UP = 700, SIGX = [260, 600, 940, 1280, 1620, 1960];
  const track = (d, dim = 1) => `
    <path d="${d}" fill="none" stroke="#2B3A57" stroke-width="30" stroke-dasharray="5 11" opacity="${0.9 * dim}"/>
    <path d="${d}" fill="none" stroke="#9FB0C8" stroke-width="15" opacity="${0.85 * dim}"/>
    <path d="${d}" fill="none" stroke="#13203A" stroke-width="9"/>`;
  const rake = (x0, n, len, gap, y, fill, stroke, cls) => {
    let s = "";
    for (let i = 0; i < n; i++) s += `<rect class="${cls}" x="${x0 + i * (len + gap)}" y="${y - 15}" width="${len}" height="30" rx="6" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
    return s;
  };
  // automatic signals, Indian style (white post, black head, hooded lamps, white "A" disc); one lit lamp each (.lamp-on)
  let sigs = "";
  SIGX.forEach((x, i) => {
    const lit = i % 2 ? "y2" : "g";
    sigs += `<g class="asig">${window.indianSignal(x, Y - 26, { id: "as" + i, plate: String(i + 1), auto: true, scale: 0.85 })
      .replace(`id="as${i}-${lit}" class="lit"`, `id="as${i}-${lit}" class="lit lamp-on"`).replace(/(class="lit lamp-on"[^>]*?)opacity="0"/, "$1opacity=\"1\"")}</g>`;
  });
  svg.innerHTML = `
  <defs>
    <filter id="glow" filterUnits="userSpaceOnUse" x="-600" y="-400" width="3400" height="2000"><feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="trainP" x1="0" x2="1"><stop offset="0" stop-color="#E9F4FF"/><stop offset="1" stop-color="#9ED8FF"/></linearGradient>
  </defs>
  <g id="world">
    <g id="grid" opacity="0.5">${Array.from({length: 44}, (_, i) => `<line x1="${-400 + i * 70}" y1="-200" x2="${-400 + i * 70}" y2="1300" stroke="rgba(148,163,184,0.07)"/>`).join("")}
      ${Array.from({length: 22}, (_, i) => `<line x1="-400" y1="${-200 + i * 70}" x2="2600" y2="${-200 + i * 70}" stroke="rgba(148,163,184,0.07)"/>`).join("")}</g>
    <g id="t-up">${track(`M -600 ${Y_UP} L 2600 ${Y_UP}`, 0.55)}</g>
    <g id="t-dn">${track(`M -600 ${Y} L 2600 ${Y}`)}</g>
    <text x="1400" y="${Y + 70}" class="tlabel lbl">DN LINE</text>
    <text id="lbl-up" x="900" y="${Y_UP + 70}" class="tlabel lbl" opacity="0.6">UP LINE</text>
    <g id="sigs">${sigs}</g>
    <g id="pass"><g id="pass-k" opacity="0"></g>
      ${rake(0, 9, 70, 8, Y, "url(#trainP)", "#38BDF8", "pc")}
      <path d="M 702 ${Y - 16} L 760 ${Y - 16} Q 784 ${Y} 760 ${Y + 16} L 702 ${Y + 16} Z" fill="#F8FAFC" stroke="#38BDF8" stroke-width="2"/>
      <text x="-24" y="${Y - 34}" text-anchor="end" class="tlabel lbl" style="fill:#BAE6FD">KANCHANJUNGA EXPRESS</text></g>
    <g id="goods">
      ${rake(-1460, 12, 96, 10, Y, "#5A2620", "#DC2626", "gw")}
      ${Array.from({length: 12}, (_, i) => `<rect x="${-1452 + i * 106}" y="${Y - 11}" width="80" height="22" rx="2" fill="#9A3B2E" opacity="0.9"/>`).join("")}
      <path d="M -190 ${Y - 17} L -120 ${Y - 17} Q -96 ${Y} -120 ${Y + 17} L -190 ${Y + 17} Z" fill="#1F7A3E" stroke="#4ADE80" stroke-width="2"/>
      <text x="-110" y="${Y - 34}" text-anchor="end" class="tlabel lbl" style="fill:#FCA5A5">GOODS TRAIN · CONTAINERS</text></g>
  </g>`;
  const q = (s) => svg.querySelector(s);
  return { svg, q, Y, Y_UP, SIGX };
};

/* Kavach unit badge on a train group (used in the C7 simulation). */
window.kanchanBadge = function (S, groupSel, x, label) {
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  g.setAttribute("class", "kb");
  g.innerHTML = `<line x1="${x}" y1="${S.Y + 18}" x2="${x}" y2="${S.Y + 62}" stroke="#38BDF8" stroke-width="3"/>
    <rect x="${x - 74}" y="${S.Y + 62}" width="148" height="46" rx="9" fill="#0B2540" stroke="#38BDF8" stroke-width="3" filter="url(#glow)"/>
    <text x="${x}" y="${S.Y + 93}" text-anchor="middle" style="font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #E0F2FE">${label}</text>`;
  S.q(groupSel).appendChild(g);
  return g;
};
