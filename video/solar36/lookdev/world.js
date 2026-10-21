// Film 36 shared world: daylight Indian lane + blueprint X-ray of the solar box (lookdev v2).
// v2 applies projects/solar-anti-islanding/review_lookdev_v1.md (independent panel incl. a DISCOM line engineer):
// dressed DP structure (HT in, AB switch, HG fuses, LAs, conservator, LT box, danger board), 4-wire LT line with a live
// blue core, service drop → wall bracket → ground-floor meter box by the door, DCDB/ACDB wired, finned inverter,
// 8 panels + mumty + DTH dish, real washing, foreground parallax, a portrait X-ray that matches the box outline, a
// "brain" chip with a sensing loop, a lever relay, a travelling AC wave to a socket, and a two-trace scope.
// Built once at load as plain SVG; all motion lives on the paused GSAP timeline.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };
  const txt = (parent, x, y, s, cls, extra) => { const t = el("text", { x, y, class: cls, ...(extra || {}) }, parent); t.textContent = s; return t; };
  const C = {
    skyTop: "#8EC5E8", skyLow: "#F7D9AE", haze: "#E9D6BC", ground: "#B9A68A", road: "#8C7B66", kerb: "#7A6B58",
    conc: "#B9B3A8", concD: "#8F897F", steel: "#5E5A55", rust: "#7E5236", porcelain: "#7A4A2E",
    amber: "#d29922", cyan: "#58a6ff", slate: "#8b949e", red: "#f85149", green: "#3fb950",
    bg: "#0d1117", panel: "#161b22", grid: "#30363d", read: "#e6edf3", label: "#C9D1D9",
  };
  const sag = (x1, y1, x2, y2, s) => `M ${x1} ${y1} Q ${(x1 + x2) / 2} ${Math.max(y1, y2) + s} ${x2} ${y2}`;

  // ---------------- daylight lane ----------------
  function house(g, x, w, floors, wall, trim, skip) {
    const fh = 150, base = 880, top = base - floors * fh;
    el("rect", { x, y: top, width: w, height: base - top, fill: wall }, g);
    el("rect", { x: x - 8, y: top - 16, width: w + 16, height: 18, fill: trim }, g);
    el("rect", { x, y: top, width: w, height: 18, fill: "rgba(0,0,0,0.10)" }, g);
    el("rect", { x: x + w - 26, y: top, width: 26, height: base - top, fill: "rgba(0,0,0,0.08)" }, g);
    for (let f = 0; f < floors; f++) {
      const y = top + 34 + f * fh;
      for (let i = 0; i < Math.floor(w / 150); i++) {
        if (skip && skip(f, i)) continue;
        const wx = x + 34 + i * 150;
        el("rect", { x: wx, y, width: 86, height: 78, fill: "#6F8592", rx: 2 }, g);
        el("polygon", { points: `${wx},${y + 78} ${wx + 40},${y} ${wx + 62},${y} ${wx + 22},${y + 78}`, fill: "rgba(255,245,225,0.28)" }, g);
        for (let b = 1; b < 4; b++) el("rect", { x: wx + b * 21.5, y, width: 2, height: 78, fill: "rgba(35,40,42,0.55)" }, g);
        el("rect", { x: wx + 2, y: y + 38, width: 82, height: 2, fill: "rgba(35,40,42,0.45)" }, g);
        el("polygon", { points: `${wx - 10},${y - 4} ${wx + 96},${y - 4} ${wx + 88},${y - 16} ${wx - 2},${y - 16}`, fill: trim }, g); // chajja
        el("rect", { x: wx - 10, y: y - 4, width: 106, height: 7, fill: "rgba(0,0,0,0.13)" }, g);
      }
      if (f > 0) el("rect", { x, y: top + f * fh - 4, width: w, height: 8, fill: "rgba(0,0,0,0.07)" }, g);
    }
    return { top, x, w };
  }

  function waterTank(g, x, y) {
    el("rect", { x, y: y - 74, width: 66, height: 74, rx: 8, fill: "#1E1E1E" }, g);
    el("ellipse", { cx: x + 33, cy: y - 74, rx: 33, ry: 8, fill: "#2E2E2E" }, g);
    for (let i = 1; i < 4; i++) el("rect", { x, y: y - 74 + i * 18, width: 66, height: 3, fill: "#2F2F2F" }, g);
  }

  function mumty(g, x, y) {
    // staircase headroom block on the roof, with a door and a DTH dish
    el("rect", { x, y: y - 96, width: 120, height: 96, fill: "#E3CC98" }, g);
    el("rect", { x: x - 6, y: y - 104, width: 132, height: 10, fill: "#CDB37E" }, g);
    el("rect", { x: x + 18, y: y - 70, width: 40, height: 70, fill: "#6B4A2E" }, g);
    const d = el("g", { transform: `translate(${x + 96} ${y - 104})` }, g);
    el("line", { x1: 0, y1: 0, x2: 0, y2: -24, stroke: "#9AA0A6", "stroke-width": 4 }, d);
    el("ellipse", { cx: -6, cy: -38, rx: 22, ry: 16, fill: "#ECEFF1", stroke: "#AEB6BF", "stroke-width": 2, transform: "rotate(-25 -6 -38)" }, d);
  }

  function panels(g, x, y, cols, rows, roofY) {
    // 8 modules on an elevated GI frame, tilted toward the sun; cells drawn; a glint sweeps across (#glint)
    const pg = el("g", { id: "panels" }, g);
    const fr = el("g", {}, g);                                                                     // GI elevated frame (~2 m)
    el("rect", { x: x - 6, y: y + 54, width: cols * 104 + 40, height: 6, fill: "#A6ACAF" }, fr);
    el("rect", { x: x + 20, y: y + 6, width: cols * 104 + 20, height: 5, fill: "#A6ACAF" }, fr);
    for (let i = 0; i <= cols; i++) { const lx = x + i * 104; el("rect", { x: lx, y: y + 56, width: 6, height: roofY - y - 56, fill: "#9AA0A6" }, fr);
      el("rect", { x: lx + 28, y: y + 8, width: 6, height: roofY - y - 8, fill: "#9AA0A6" }, fr);
      el("line", { x1: lx + 3, y1: roofY - 2, x2: lx + 31, y2: y + 60, stroke: "#9AA0A6", "stroke-width": 3 }, fr); }
    for (let r = 0; r < rows; r++) for (let i = 0; i < cols; i++) {
      const px = x + i * 104 + r * 26, py = y - r * 40;
      el("line", { x1: px + 12, y1: py + 6, x2: px + 12, y2: py + 66, stroke: "#9AA0A6", "stroke-width": 5 }, pg);
      el("line", { x1: px + 86, y1: py - 18, x2: px + 86, y2: py + 36, stroke: "#9AA0A6", "stroke-width": 5 }, pg);
      el("polygon", { points: `${px},${py + 10} ${px + 98},${py - 22} ${px + 98},${py + 14} ${px},${py + 46}`, fill: "#1F3A5F", stroke: "#D5DEE6", "stroke-width": 2 }, pg);
      for (let k = 1; k < 6; k++) el("line", { x1: px + k * 16.3, y1: py + 10 - k * 5.3, x2: px + k * 16.3, y2: py + 46 - k * 5.3, stroke: "#3E6A96", "stroke-width": 1.2 }, pg);
      el("line", { x1: px, y1: py + 28, x2: px + 98, y2: py - 4, stroke: "#3E6A96", "stroke-width": 1.2 }, pg);
    }
    const clip = el("clipPath", { id: "pvClip" }, g);
    pg.querySelectorAll("polygon").forEach(p => el("polygon", { points: p.getAttribute("points") }, clip));
    const gl = el("g", { "clip-path": "url(#pvClip)" }, g);
    el("rect", { id: "glint", x: x - 120, y: y - 120, width: 60, height: 260, fill: "rgba(255,255,255,0.55)", transform: `skewX(-30)` }, gl);
    return pg;
  }

  function washing(g, x1, x2, y) {
    el("rect", { x: x1 - 2, y: y - 6, width: 4, height: 70, fill: "#6E6258" }, g);
    el("rect", { x: x2 - 2, y: y - 6, width: 4, height: 70, fill: "#6E6258" }, g);
    el("path", { d: sag(x1, y, x2, y, 12), fill: "none", stroke: "#5C5047", "stroke-width": 2.5 }, g);
    // saree (long drape with a border), shirt, towel
    const s = el("g", { class: "cloth" }, g);
    el("path", { d: `M ${x1 + 30} ${y + 4} L ${x1 + 150} ${y + 9} L ${x1 + 146} ${y + 70} Q ${x1 + 90} ${y + 80} ${x1 + 34} ${y + 66} Z`, fill: "#C2185B" }, s);
    el("path", { d: `M ${x1 + 36} ${y + 58} Q ${x1 + 90} ${y + 70} ${x1 + 146} ${y + 62}`, stroke: "#F4C430", "stroke-width": 7, fill: "none" }, s);
    const sh = el("g", { class: "cloth" }, g);
    el("path", { d: `M ${x1 + 190} ${y + 10} l 22 -2 l 12 10 l 12 -10 l 22 2 l 12 22 l -14 8 l 0 40 l -64 0 l 0 -40 l -14 -8 Z`, fill: "#2E86C1" }, sh);
    const tw = el("g", { class: "cloth" }, g);
    el("rect", { x: x1 + 290, y: y + 11, width: 46, height: 54, fill: "#FDFEFE" }, tw);
    el("rect", { x: x1 + 290, y: y + 50, width: 46, height: 6, fill: "#E74C3C" }, tw);
  }

  function ltPole(g, x) {
    // PSC pole with a 4-pin cross-arm (R Y B N) and the service-wire tangle
    el("polygon", { points: `${x - 11},880 ${x + 11},880 ${x + 6},280 ${x - 6},280`, fill: C.conc }, g);
    el("polygon", { points: `${x + 3},880 ${x + 11},880 ${x + 6},280 ${x + 2},280`, fill: C.concD }, g);
    el("rect", { x: x - 72, y: 298, width: 144, height: 10, fill: C.steel }, g);
    [-60, -24, 24, 60].forEach(dx => el("rect", { x: x + dx - 5, y: 284, width: 10, height: 16, fill: "#ECE6DA" }, g));
    for (let i = 0; i < 5; i++) el("path", { d: `M ${x - 6} ${350 + i * 20} q ${-38 - i * 8} 16 ${-10} ${42 + i * 6}`, fill: "none", stroke: "#2B2B2B", "stroke-width": 3 }, g);
  }

  function dpStructure(g, x) {
    // Indian 11 kV double-pole (DP) substation, from the TNEB / Rajasthan Commons references
    const tg = el("g", { id: "xfmr" }, g), p2 = x + 160;
    [x, p2].forEach(px => {
      el("polygon", { points: `${px - 11},880 ${px + 11},880 ${px + 7},190 ${px - 7},190`, fill: C.conc }, tg);
      el("polygon", { points: `${px + 3},880 ${px + 11},880 ${px + 7},190 ${px + 2},190`, fill: C.concD }, tg);
    });
    const arm = (y, c) => el("rect", { x: x - 26, y, width: 212, height: 9, fill: c || C.rust }, tg);
    arm(206); [12, 80, 148].forEach(dx => { el("ellipse", { cx: x + dx, cy: 198, rx: 14, ry: 7, fill: "#4A4440" }, tg); el("ellipse", { cx: x + dx, cy: 191, rx: 10, ry: 5, fill: "#5A534D" }, tg); });
    // AB switch (gang-operated) with the handle rod down the pole
    arm(262); [12, 80, 148].forEach(dx => {
      el("rect", { x: x + dx - 4, y: 240, width: 8, height: 22, fill: "#5A534D" }, tg);
      el("line", { x1: x + dx - 14, y1: 244, x2: x + dx + 14, y2: 238, stroke: "#C0C4C8", "stroke-width": 4, class: "abBlade" }, tg);
    });
    el("line", { x1: x + 14, y1: 270, x2: x + 14.3, y2: 760, stroke: "#9AA0A6", "stroke-width": 3 }, tg);
    el("rect", { x: x + 6, y: 750, width: 34, height: 8, fill: "#9AA0A6" }, tg);
    // HG drop-out fuses (angled tubes) and lightning arresters
    arm(330); [20, 80, 140].forEach(dx => {
      el("line", { x1: x + dx - 6, y1: 300, x2: x + dx + 6, y2: 330, stroke: "#3D3A37", "stroke-width": 7, "stroke-linecap": "round" }, tg);
      el("line", { x1: x + dx, y1: 262, x2: x + dx - 6, y2: 300, stroke: "#3B3B3B", "stroke-width": 2 }, tg);
    });
    arm(380); [28, 80, 132].forEach(dx => { el("rect", { x: x + dx - 7, y: 352, width: 14, height: 28, rx: 3, fill: "#9AA3A8" }, tg); for (let k = 0; k < 3; k++) el("rect", { x: x + dx - 9, y: 356 + k * 8, width: 18, height: 3, fill: "#7E878C" }, tg); });
    // transformer on its platform: tank, side radiator fins, conservator, HT bushings on top, LT bushings on the side
    arm(570);
    el("rect", { x: x + 22, y: 452, width: 116, height: 118, rx: 4, fill: "#8D9695" }, tg);
    for (let i = 0; i < 3; i++) { el("rect", { x: x + 8 - i * 0, y: 466 + i * 30, width: 14, height: 22, fill: "#727B7A" }, tg); el("rect", { x: x + 138, y: 466 + i * 30, width: 14, height: 22, fill: "#727B7A" }, tg); }
    for (let i = 0; i < 6; i++) el("rect", { x: x + 30 + i * 18, y: 462, width: 8, height: 100, fill: "#7B8483" }, tg);
    el("rect", { x: x + 46, y: 410, width: 76, height: 24, rx: 12, fill: "#7E8786" }, tg);           // conservator
    el("rect", { x: x + 76, y: 434, width: 8, height: 18, fill: "#6B7473" }, tg);
    [44, 80, 116].forEach(dx => { for (let k = 0; k < 3; k++) el("rect", { x: x + dx - 7 + k, y: 424 + k * 9, width: 14 - 2 * k, height: 7, rx: 3, fill: C.porcelain }, tg);
      el("line", { x1: x + dx, y1: 330, x2: x + dx, y2: 424, stroke: "#3B3B3B", "stroke-width": 2 }, tg); });
    [0, 1, 2, 3].forEach(k => el("rect", { x: x + 138, y: 500 + k * 14, width: 12, height: 8, rx: 2, fill: "#3D3A37" }, tg)); // LT bushings
    el("rect", { x: x + 40, y: 520, width: 54, height: 26, fill: "#1C2833" }, tg);
    txt(tg, x + 67, 538, "11 kV / 433 V", "w-plate", { "text-anchor": "middle" });
    // LT distribution box on the pole, danger board
    el("rect", { x: p2 - 40, y: 630, width: 80, height: 96, rx: 4, fill: "#7F8C8D", stroke: "#5D6D7E", "stroke-width": 3 }, tg);
    el("path", { d: `M ${x + 150} 520 Q ${p2 + 30} 560 ${p2 + 8} 630`, fill: "none", stroke: "#2B2B2B", "stroke-width": 5 }, tg);
    const db = el("g", { id: "danger", transform: `translate(${x + 30} 610)` }, tg);
    el("rect", { x: -40, y: 0, width: 80, height: 82, rx: 5, fill: "#FDFEFE", stroke: "#B03A2E", "stroke-width": 4 }, db);
    el("rect", { x: -36, y: 4, width: 72, height: 16, fill: "#B03A2E" }, db);
    txt(db, 0, 17, "DANGER", "w-dangerW", { "text-anchor": "middle" });
    el("line", { x1: -14, y1: 30, x2: 14, y2: 58, stroke: "#1C1C1C", "stroke-width": 4, "stroke-linecap": "round" }, db);
    el("line", { x1: 14, y1: 30, x2: -14, y2: 58, stroke: "#1C1C1C", "stroke-width": 4, "stroke-linecap": "round" }, db);
    el("circle", { cx: 0, cy: 40, r: 9, fill: "#1C1C1C" }, db);
    el("circle", { cx: -3.5, cy: 39, r: 2.2, fill: "#FDFEFE" }, db); el("circle", { cx: 3.5, cy: 39, r: 2.2, fill: "#FDFEFE" }, db);
    txt(db, 0, 76, "11000 V", "w-danger", { "text-anchor": "middle" });
    return { tg, p2 };
  }

  function dhol(parent, cx, cy) {
    // The drummer: a dhol icon (barrel, two heads, zig-zag lacing, strap, curved stick). Squash on each hit.
    const g = el("g", { id: "dholPos", transform: `translate(${cx} ${cy})` }, parent);
    el("circle", { id: "dholShock", r: 70, fill: "none", stroke: C.cyan, "stroke-width": 6, opacity: 0 }, g);
    const d = el("g", { id: "dhol" }, g);
    el("circle", { id: "dholFlash", r: 80, fill: "#FFFFFF", opacity: 0 }, g);
    el("path", { d: "M -64 -40 Q 0 -84 64 -40", fill: "none", stroke: "#8E44AD", "stroke-width": 7, "stroke-linecap": "round" }, d); // strap
    el("rect", { x: -64, y: -38, width: 128, height: 76, rx: 34, fill: "#C2652B", stroke: "#6E3414", "stroke-width": 4 }, d);
    el("polyline", { points: "-48,-34 -32,34 -16,-34 0,34 16,-34 32,34 48,-34", fill: "none", stroke: "#F7EBD3", "stroke-width": 4, "stroke-linejoin": "round" }, d);
    el("ellipse", { cx: -64, cy: 0, rx: 15, ry: 38, fill: "#F2E3C6", stroke: "#6E3414", "stroke-width": 4 }, d);
    el("ellipse", { cx: 64, cy: 0, rx: 15, ry: 38, fill: "#F2E3C6", stroke: "#6E3414", "stroke-width": 4 }, d);
    el("path", { id: "dholStick", d: "M 112 -70 Q 96 -30 74 -8", fill: "none", stroke: "#5D3A1A", "stroke-width": 8, "stroke-linecap": "round" }, d);
    return g;
  }

  function solarBox(parent, x, y) {
    // Wall-mount on-grid inverter: light-grey, heat-sink fins, small LCD, cable glands, sun-badge "dancer"
    const g = el("g", { id: "box" }, parent);
    el("rect", { x: x + 6, y: y + 150, width: 120, height: 10, fill: "rgba(60,40,20,0.22)" }, g);           // contact shadow
    [x - 14, x + 120].forEach(fx => { el("rect", { x: fx, y: y + 8, width: 14, height: 124, rx: 3, fill: "#BFC6CD" }, g);
      for (let k = 0; k < 4; k++) el("rect", { x: fx + 2 + k * 3, y: y + 12, width: 1.6, height: 116, fill: "#9AA3AC" }, g); }); // ribbed heat-sink
    el("rect", { id: "boxCase", x, y, width: 120, height: 140, rx: 10, fill: "#F4F6F7", stroke: "#AEB6BF", "stroke-width": 3 }, g);
    el("rect", { x: x + 30, y: y + 18, width: 60, height: 22, rx: 3, fill: "#1B2631" }, g);
    el("circle", { id: "boxLed", cx: x + 102, cy: y + 124, r: 6, fill: C.green }, g);
    [[x + 22, C.amber], [x + 44, C.amber], [x + 76, C.cyan], [x + 98, C.cyan]].forEach(([gx, c]) => {
      el("rect", { x: gx - 7, y: y + 140, width: 14, height: 10, rx: 3, fill: "#5D6D7E" }, g);                 // cable gland
      el("path", { d: `M ${gx} ${y + 150} q 0 12 ${gx < x + 60 ? -10 : 10} 18`, fill: "none", stroke: c, "stroke-width": 5 }, g); });
    const sb = el("g", { id: "badgePos", transform: `translate(${x + 60} ${y + 86})` }, g);
    const b = el("g", { id: "badge" }, sb);
    el("circle", { r: 20, fill: "none", stroke: "#E67E22", "stroke-width": 4 }, b);
    for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; el("line", { x1: Math.cos(a) * 25, y1: Math.sin(a) * 25, x2: Math.cos(a) * 31, y2: Math.sin(a) * 31, stroke: "#E67E22", "stroke-width": 4, "stroke-linecap": "round" }, b); }
    el("circle", { cx: -7, cy: -3, r: 3, fill: "#5D4037" }, b);
    el("circle", { cx: 7, cy: -3, r: 3, fill: "#5D4037" }, b);
    return g;
  }

  function dbBox(parent, x, y, label) {
    const g = el("g", {}, parent);
    el("rect", { x: x + 5, y: y + 84, width: 70, height: 8, fill: "rgba(60,40,20,0.22)" }, g);
    el("rect", { x, y, width: 70, height: 84, rx: 6, fill: "#A6ACAF", stroke: "#717D7E", "stroke-width": 3 }, g);
    el("rect", { x: x + 12, y: y + 12, width: 46, height: 30, rx: 3, fill: "rgba(210,230,240,0.85)" }, g);
    el("rect", { x: x + 29, y: y + 18, width: 12, height: 18, fill: "#2C3E50" }, g);
    txt(g, x + 35, y + 72, label, "w-db", { "text-anchor": "middle" });
    return g;
  }

  function foreground(parent) {
    // parallax layer: compound wall + gate, a parked scooter, a neem branch (moves faster than the world)
    const fg = el("g", { id: "fg" }, parent);
    el("rect", { x: -200, y: 956, width: 2400, height: 70, fill: "#D9C7A6" }, fg);
    el("rect", { x: -200, y: 948, width: 2400, height: 12, fill: "#C4B08C" }, fg);
    for (let i = 0; i < 26; i++) el("rect", { x: -200 + i * 96, y: 956, width: 4, height: 70, fill: "rgba(0,0,0,0.08)" }, fg);
    const gate = el("g", { transform: "translate(600 900)" }, fg);
    el("rect", { x: 0, y: 0, width: 150, height: 126, fill: "none", stroke: "#2C3E50", "stroke-width": 6 }, gate);
    for (let k = 1; k < 8; k++) el("line", { x1: k * 18.75, y1: 0, x2: k * 18.75 + 0.2, y2: 126, stroke: "#2C3E50", "stroke-width": 4 }, gate);
    const sc = el("g", { transform: "translate(1240 940)" }, fg);
    el("circle", { cx: 0, cy: 50, r: 24, fill: "#222" }, sc); el("circle", { cx: 120, cy: 50, r: 24, fill: "#222" }, sc);
    el("path", { d: "M -10 40 Q 10 -10 60 6 L 110 6 Q 140 10 140 40 Z", fill: "#C0392B" }, sc);
    el("rect", { x: 40, y: -16, width: 50, height: 14, rx: 6, fill: "#1C1C1C" }, sc);
    el("line", { x1: 0, y1: 20, x2: -14, y2: -26, stroke: "#555", "stroke-width": 6 }, sc);
    const br = el("g", { id: "neem", transform: "translate(1980 990)", opacity: 0.92 }, fg);
    el("path", { d: "M 0 0 Q -120 -60 -260 -40", stroke: "#3E2C1C", "stroke-width": 10, fill: "none" }, br);
    for (let k = 0; k < 14; k++) { const t = k / 13, px = -260 * t, py = -40 * t - 40 * Math.sin(Math.PI * t);
      el("ellipse", { cx: px, cy: py - 12, rx: 22, ry: 8, fill: k % 2 ? "#3F6E2A" : "#4F8434", transform: `rotate(${-30 + k * 9} ${px} ${py - 12})` }, br);
      el("ellipse", { cx: px, cy: py + 12, rx: 22, ry: 8, fill: k % 2 ? "#4F8434" : "#3F6E2A", transform: `rotate(${30 - k * 9} ${px} ${py + 12})` }, br); }
    return fg;
  }

  function lane(svg) {
    const defs = el("defs", {}, svg);
    const sky = el("linearGradient", { id: "sky", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    el("stop", { offset: "0", "stop-color": C.skyTop }, sky);
    el("stop", { offset: "0.75", "stop-color": C.skyLow }, sky);
    const sun = el("radialGradient", { id: "sun" }, defs);
    el("stop", { offset: "0", "stop-color": "#FFFBEA" }, sun);
    el("stop", { offset: "0.22", "stop-color": "#FFE9A8", "stop-opacity": 0.95 }, sun);
    el("stop", { offset: "1", "stop-color": "#FFE9A8", "stop-opacity": 0 }, sun);
    const world = el("g", { id: "world" }, svg);
    el("rect", { x: -400, y: -400, width: 2720, height: 1880, fill: "url(#sky)" }, world);
    el("circle", { id: "sunGlow", cx: 1000, cy: 120, r: 240, fill: "url(#sun)" }, world);
    el("circle", { cx: 1000, cy: 120, r: 44, fill: "#FFF8DC" }, world);
    const sky2 = el("g", { id: "skyline" }, world);
    for (let i = 0; i < 16; i++) el("rect", { x: -200 + i * 150, y: 700 - (i * 37 % 90), width: 132, height: 200, fill: C.haze, opacity: 0.9 }, sky2);
    el("rect", { x: -400, y: 880, width: 2720, height: 600, fill: C.ground }, world);
    el("rect", { x: -400, y: 900, width: 2720, height: 60, fill: C.road }, world);
    [[40, 470], [560, 560], [1660, 420]].forEach(([hx, hw]) =>
      el("polygon", { points: `${hx},880 ${hx + hw},880 ${hx + hw - 50},905 ${hx - 50},905`, fill: "rgba(50,35,20,0.2)" }, world));
    const h1 = house(world, 40, 470, 2, "#E2A27A", "#C98762");
    const h2 = house(world, 560, 560, 3, "#EED9A8", "#D6BC85", (f, i) => f === 2 || (f === 1 && i >= 1));
    const h3 = house(world, 1660, 420, 2, "#B8CDB0", "#9DB494");
    washing(world, h1.x + 50, h1.x + 410, h1.top - 74);
    el("rect", { x: h3.x + 40, y: h3.top - 40, width: 40, height: 26, rx: 6, fill: "#C0392B" }, world);
    el("ellipse", { cx: h3.x + 60, cy: h3.top - 52, rx: 26, ry: 18, fill: "#4E7D3A" }, world);
    mumty(world, h2.x + 420, h2.top - 16);
    waterTank(world, h2.x + 330, h2.top - 16);
    panels(world, h2.x + 20, h2.top - 150, 3, 2, h2.top - 16);
    // door, meter box by the door (ground floor), DCDB · inverter · ACDB on the first floor
    el("rect", { x: 590, y: 752, width: 86, height: 128, rx: 3, fill: "#7A4E2D" }, world);
    el("rect", { x: 596, y: 758, width: 74, height: 118, rx: 2, fill: "none", stroke: "#5C3A21", "stroke-width": 3 }, world);
    const meter = el("g", { id: "meter" }, world);
    el("rect", { x: 700, y: 760, width: 78, height: 96, rx: 6, fill: "#B3B9BC", stroke: "#717D7E", "stroke-width": 3 }, meter);
    el("rect", { x: 710, y: 770, width: 58, height: 52, rx: 4, fill: "rgba(225,240,248,0.9)" }, meter);
    el("rect", { x: 716, y: 778, width: 46, height: 18, fill: "#1D2A35" }, meter);
    txt(meter, 739, 792, "EXP", "w-lcd", { "text-anchor": "middle" });
    el("circle", { id: "meterLed", cx: 756, cy: 810, r: 4, fill: C.red }, meter);
    dbBox(world, 760, 602, "DCDB");
    const box = solarBox(world, 864, 584);
    dbBox(world, 1020, 602, "ACDB");
    // wiring: amber DC roof → DCDB → inverter; blue inverter → ACDB → meter; service drop → bracket → meter
    const dc = el("path", { id: "pvCable", d: `M ${h2.x + 150} ${h2.top - 100} L ${h2.x + 150} 640 L 760 640`, fill: "none", stroke: C.amber, "stroke-width": 6 }, world);
    el("path", { d: "M 830 640 L 848 640", stroke: C.amber, "stroke-width": 6 }, world);
    el("path", { d: "M 1000 640 L 1020 640", stroke: C.cyan, "stroke-width": 6 }, world);
    el("path", { d: "M 1055 686 L 1055 800 L 778 800", fill: "none", stroke: C.cyan, "stroke-width": 6 }, world);
    ltPole(world, 1240);
    const dp = dpStructure(world, 1390);
    // HT line in from the right (3 conductors), LT 4-wire from the DP LT box → LT pole → off left above the roofs
    const lines = el("g", { id: "lines" }, world);
    // the 11 kV line from the horizon: a far substation silhouette, the HT tower, 3 conductors to the DP top
    el("rect", { x: 1830, y: 600, width: 120, height: 80, fill: "#C9B8A0" }, lines);
    for (let k = 0; k < 4; k++) el("rect", { x: 1840 + k * 28, y: 560, width: 6, height: 40, fill: "#B3A288" }, lines);
    el("polygon", { points: "1678,880 1702,880 1694,400 1688,400", fill: "#A9A196" }, lines);
    el("rect", { x: 1648, y: 400, width: 86, height: 8, fill: C.rust }, lines);
    [0, 1, 2].forEach(k => el("path", { d: sag(1660 + k * 30, 400, 1390 + [12, 80, 148][k], 191, 10), fill: "none", stroke: "#333", "stroke-width": 2.6 }, lines));
    [0, 1, 2].forEach(k => el("path", { d: sag(1660 + k * 30, 400, 1390 + [12, 80, 148][k], 191, 10), fill: "none", stroke: C.cyan, "stroke-width": 1.2, class: "ltCore", opacity: 0.7 }, lines));
    [0, 1, 2].forEach(k => el("path", { d: sag(2000, 380 + k * 12, 1660 + k * 30, 400, 14), fill: "none", stroke: "#333", "stroke-width": 2.6 }, lines));
    const ltG = el("g", { id: "lt" }, lines);
    [-60, -24, 24, 60].forEach((dx, k) => {
      const d = `M 1556 630 L ${1556 + (k - 1.5) * 6} 300 ` + sag(1556 + (k - 1.5) * 6, 300, 1240 + dx, 284, 14).replace("M", "L") + " " + sag(1240 + dx, 284, -200, 250 + k * 8, 26).replace("M", "L");
      el("path", { d, fill: "none", stroke: "#2B2B2B", "stroke-width": 3.5 }, ltG);
      el("path", { d, fill: "none", stroke: C.cyan, "stroke-width": 1.4, class: "ltCore", opacity: 0.7 }, ltG);
    });
    // service drop: LT pole → wall bracket → down the wall → meter
    el("rect", { x: 1108, y: 586, width: 22, height: 12, fill: "#5E5A55" }, world);
    const svc = el("path", { id: "svc", d: `${sag(1240 - 24, 300, 1120, 592, 36)} L 1120 820 L 778 820`, fill: "none", stroke: "#2B2B2B", "stroke-width": 4 }, world);
    el("path", { d: `${sag(1240 - 24, 300, 1120, 592, 36)} L 1120 820 L 778 820`, fill: "none", stroke: C.cyan, "stroke-width": 1.6, class: "ltCore", opacity: 0.7 }, world);
    // ring path: DP LT box → LT pole → service drop → meter → up to the inverter
    const ring = el("path", { id: "ringPath", d: `${sag(1690, 400, 1470, 191, 10)} L 1470 440 L 1556 630 L 1556 300 ${sag(1556, 300, 1216, 284, 14).replace("M", "L")} ${sag(1216, 300, 1120, 592, 36).replace("M", "L")} L 1120 820 L 778 820 L 740 820`, fill: "none", stroke: "none" }, world);
    const dh = dhol(world, 1690, 300);
    const gt = el("g", { transform: "translate(1690 176)" }, world);
    el("rect", { x: -48, y: 0, width: 96, height: 36, rx: 8, fill: "rgba(13,17,23,0.82)" }, gt);
    txt(gt, 0, 27, "GRID", "w-grid", { "text-anchor": "middle" });
    foreground(svg);
    return { world, ring, box, dc, dp };
  }

  // ---------------- blueprint X-ray (portrait frame matching the box outline) ----------------
  // The real box (120×140 at 864,584) scaled ×5.5 about its centre lands on FRAME below.
  const FRAME = { x: 630, y: 155, w: 660, h: 770 };
  function xray(svg) {
    const defs = svg.querySelector("defs");
    const cp = el("clipPath", { id: "xWipe" }, defs);
    el("circle", { id: "xWipeC", cx: 960, cy: 540, r: 0 }, cp);
    el("rect", { id: "morph", x: FRAME.x, y: FRAME.y, width: FRAME.w, height: FRAME.h, rx: 46, fill: "none", stroke: "#58a6ff", "stroke-width": 6, "stroke-dasharray": 2860, opacity: 0 }, svg);
    const g = el("g", { id: "xray", "clip-path": "url(#xWipe)" }, svg);
    el("rect", { x: 0, y: 0, width: 1920, height: 1080, fill: C.bg }, g);
    const grid = el("g", {}, g);
    for (let x = 0; x <= 1920; x += 48) el("line", { x1: x + 0.5, y1: 0, x2: x + 0.1, y2: 1080, stroke: x % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": x % 240 ? 1 : 2 }, grid);
    for (let y = 0; y <= 1080; y += 48) el("line", { x1: 0, y1: y + 0.5, x2: 1920, y2: y + 0.1, stroke: y % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": y % 240 ? 1 : 2 }, grid);
    const cam = el("g", { id: "xcam" }, g);
    const F = FRAME;
    el("rect", { id: "xFrame", x: F.x, y: F.y, width: F.w, height: F.h, rx: 46, fill: "rgba(22,27,34,0.88)", stroke: C.label, "stroke-width": 3, "stroke-dasharray": "14 8" }, cam);
    txt(cam, F.x + 40, F.y + 58, "INSIDE THE SOLAR BOX", "x-tag");
    const inner = el("g", { id: "xInner" }, cam);
    // panel + sun icon outside left, DC in through the left wall
    const pv = el("g", { transform: "translate(250 600)" }, inner);
    el("rect", { x: -70, y: -10, width: 130, height: 90, rx: 4, fill: "#1F3A5F", stroke: "#AEB6BF", "stroke-width": 4 }, pv);
    for (let i = 1; i < 3; i++) el("line", { x1: -70 + i * 43.3, y1: -10, x2: -70 + i * 43.3 + 0.2, y2: 80, stroke: "#5D86B0", "stroke-width": 2 }, pv);
    el("line", { x1: -70, y1: 35, x2: 60, y2: 35.2, stroke: "#5D86B0", "stroke-width": 2 }, pv);
    el("circle", { cx: -20, cy: -80, r: 22, fill: "none", stroke: C.amber, "stroke-width": 4 }, pv);
    for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; el("line", { x1: -20 + Math.cos(a) * 30, y1: -80 + Math.sin(a) * 30, x2: -20 + Math.cos(a) * 40, y2: -80 + Math.sin(a) * 40, stroke: C.amber, "stroke-width": 4, "stroke-linecap": "round" }, pv); }
    txt(inner, 250, 720, "PANELS", "x-tag", { "text-anchor": "middle" });
    el("line", { x1: 320, y1: 620, x2: 760, y2: 620.3, stroke: C.amber, "stroke-width": 8, "stroke-linecap": "round" }, inner);
    for (let i = 0; i < 10; i++) el("circle", { cx: 320 + i * 44, cy: 620, r: 7, fill: "#F2C14E", class: "dcdot" }, inner);
    // H-bridge (4 switches) + filter coil
    el("rect", { x: 760, y: 540, width: 170, height: 160, rx: 12, fill: "none", stroke: C.read, "stroke-width": 3 }, inner);
    [[790, 566], [870, 566], [790, 644], [870, 644]].forEach(([sx, sy], k) => {                    // four switch symbols (H-bridge)
      const sg = el("g", { class: "swg", "data-k": k }, inner);
      el("circle", { cx: sx, cy: sy + 30, r: 6, fill: C.read }, sg); el("circle", { cx: sx + 36, cy: sy + 30, r: 6, fill: C.read }, sg);
      el("line", { class: "sw", x1: sx, y1: sy + 30, x2: sx + 34, y2: sy + 8, stroke: C.cyan, "stroke-width": 5, "stroke-linecap": "round" }, sg); });
    txt(inner, 845, 736, "D.C. → A.C.", "x-tag", { "text-anchor": "middle" });
    let coil = "M 930 620"; for (let k = 0; k < 5; k++) coil += ` q 8 -26 16 0`;
    el("path", { d: coil, fill: "none", stroke: C.read, "stroke-width": 4 }, inner);
    el("line", { x1: 1010, y1: 620, x2: 1072, y2: 620.3, stroke: C.cyan, "stroke-width": 7, "stroke-linecap": "round" }, inner);
    // relay as a lever switch (closed = green bridge)
    const relay = el("g", { id: "relay" }, inner);
    el("circle", { cx: 1080, cy: 620, r: 9, fill: C.read }, relay);
    el("circle", { cx: 1170, cy: 620, r: 9, fill: C.read }, relay);
    el("line", { id: "lever", x1: 1080, y1: 620, x2: 1170, y2: 620.3, stroke: C.green, "stroke-width": 9, "stroke-linecap": "round" }, relay);
    txt(relay, 1125, 680, "SWITCH", "x-tag", { "text-anchor": "middle" });
    // the brain: a chip with an ear icon, a sensing line from the grid side, a control line to the relay
    const brain = el("g", { id: "brain" }, inner);
    el("rect", { x: 900, y: 300, width: 160, height: 100, rx: 10, fill: C.panel, stroke: C.read, "stroke-width": 3 }, brain);
    for (let k = 0; k < 5; k++) { el("rect", { x: 914 + k * 30, y: 290, width: 10, height: 10, fill: C.read }, brain); el("rect", { x: 914 + k * 30, y: 400, width: 10, height: 10, fill: C.read }, brain); }
    el("path", { d: "M 940 350 Q 980 318 1020 350 Q 980 382 940 350 Z", fill: "none", stroke: C.cyan, "stroke-width": 5, "stroke-linejoin": "round" }, brain); // eye
    el("circle", { id: "pupil", cx: 980, cy: 350, r: 10, fill: C.cyan }, brain);
    txt(brain, 980, 272, "WATCHES THE GRID", "x-tag", { "text-anchor": "middle" });
    el("path", { id: "sense", d: "M 1200 620 L 1230 620 L 1230 350 L 1060 350", fill: "none", stroke: C.cyan, "stroke-width": 5, "stroke-dasharray": "10 8" }, inner);
    el("path", { id: "ctlRelay", d: "M 1040 410 L 1040 560 L 1125 600", fill: "none", stroke: C.read, "stroke-width": 3, "stroke-dasharray": "4 8" }, inner);
    el("path", { id: "ctlBridge", d: "M 920 410 L 920 470 L 845 470 L 845 540", fill: "none", stroke: C.read, "stroke-width": 3, "stroke-dasharray": "4 8" }, inner);
    // AC wave out through the relay to the house: socket icon outside right
    el("line", { x1: 1180, y1: 620, x2: 1584, y2: 620.3, stroke: C.cyan, "stroke-width": 7, "stroke-linecap": "round", opacity: 0.55 }, inner);
    const acp = el("g", { id: "acPulses" }, inner);
    for (let i = 0; i < 8; i++) el("circle", { cx: 1180, cy: 620, r: 9, fill: "#9CC8FF", class: "acp" }, acp);
    const sk = el("g", { transform: "translate(1640 620)" }, inner);
    el("rect", { x: -56, y: -60, width: 150, height: 120, rx: 14, fill: "#F4F6F7", stroke: C.cyan, "stroke-width": 4 }, sk);   // Indian 3-pin + switch
    el("circle", { cx: 0, cy: -26, r: 12, fill: "#2C3E50" }, sk); el("circle", { cx: -20, cy: 18, r: 8, fill: "#2C3E50" }, sk); el("circle", { cx: 20, cy: 18, r: 8, fill: "#2C3E50" }, sk);
    el("rect", { x: 52, y: -30, width: 28, height: 52, rx: 5, fill: "#D5DBDB", stroke: "#99A3A4", "stroke-width": 2 }, sk);
    el("rect", { x: 56, y: -26, width: 20, height: 22, rx: 3, fill: "#C0392B" }, sk);
    txt(inner, 1640, 720, "TO HOUSE", "x-tag", { "text-anchor": "middle" });
    // scope: grid trace (blue, 4 px) + box trace (white dashed, 2 px)
    const scope = el("g", { id: "scope" }, g);
    el("rect", { x: 1330, y: 230, width: 540, height: 230, rx: 14, fill: C.panel, stroke: C.grid, "stroke-width": 2 }, scope);
    txt(scope, 1354, 270, "GRID", "x-tag cyan");
    txt(scope, 1474, 270, "· BOX", "x-tag");
    txt(scope, 1846, 270, "IN STEP ✓", "x-tag green", { "text-anchor": "end", id: "inStep", opacity: 0 });
    el("path", { id: "tGrid", fill: "none", stroke: C.cyan, "stroke-width": 4 }, scope);
    el("path", { id: "tBox", fill: "none", stroke: C.read, "stroke-width": 2.5, "stroke-dasharray": "9 6" }, scope);
    return { g, cam, inner };
  }

  function sinePath(x0, x1, yc, amp, cycles, phase, n) {
    n = n || 120; let d = "";
    for (let i = 0; i <= n; i++) {
      const x = x0 + (x1 - x0) * i / n, y = yc - amp * Math.sin(phase + 2 * Math.PI * cycles * i / n);
      d += (i ? " L " : "M ") + x.toFixed(1) + " " + y.toFixed(1);
    }
    return d;
  }

  window.W36 = { el, txt, C, lane, xray, sinePath, FRAME };
})();
