// Film 36 daylight lane + blueprint X-ray builders (lookdev; shared by the scenes later).
// Everything is plain SVG built once at load; animation lives on the paused GSAP timeline.
// Hardware drawn from the Commons references in projects/solar-anti-islanding/assets/ref/
// (TNEB double-pole transformer, Rajasthan double-pole structure).
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };
  const C = {
    sky0: "#F3C98B", sky1: "#FBE9CC", haze: "#F7DDB0", ground: "#CDB89A", road: "#B7A386", kerb: "#9C8A70",
    ink: "#3B342C", conc: "#B9B3A8", concD: "#8F897F", steel: "#6B6660", rust: "#8A5A3C",
    amber: "#d29922", cyan: "#58a6ff", slate: "#8b949e", red: "#f85149", green: "#3fb950",
    bg: "#0d1117", panel: "#161b22", grid: "#30363d", read: "#e6edf3",
  };

  // A sagging wire between two points (quadratic), returned as a path string.
  const sag = (x1, y1, x2, y2, s) => `M ${x1} ${y1} Q ${(x1 + x2) / 2} ${Math.max(y1, y2) + s} ${x2} ${y2}`;

  function house(g, x, w, floors, wall, trim, skip) {
    const fh = 150, base = 880, top = base - floors * fh;
    el("rect", { x, y: top, width: w, height: base - top, fill: wall }, g);
    el("rect", { x: x - 8, y: top - 14, width: w + 16, height: 16, fill: trim }, g);              // RCC parapet
    el("rect", { x, y: top, width: w, height: 18, fill: "rgba(0,0,0,0.10)" }, g);                // parapet shade
    el("rect", { x: x + w - 26, y: top, width: 26, height: base - top, fill: "rgba(0,0,0,0.07)" }, g);   // corner shade
    for (let f = 0; f < floors; f++) {
      const y = top + 34 + f * fh;
      for (let i = 0; i < Math.floor(w / 150); i++) {
        const wx = x + 34 + i * 150;
        if (skip && skip(f, i)) continue;
        el("rect", { x: wx, y, width: 86, height: 78, fill: "#7C8C94", rx: 2 }, g);                // window glass
        el("polygon", { points: `${wx},${y + 78} ${wx + 40},${y} ${wx + 62},${y} ${wx + 22},${y + 78}`, fill: "rgba(255,240,210,0.25)" }, g);
        for (let b = 1; b < 4; b++) el("rect", { x: wx + b * 21.5, y, width: 2, height: 78, fill: "rgba(40,44,46,0.55)" }, g); // light grill
        el("rect", { x: wx - 6, y: y - 10, width: 98, height: 10, fill: trim }, g);                  // chajja
        el("rect", { x: wx - 6, y, width: 98, height: 8, fill: "rgba(0,0,0,0.12)" }, g);
      }
      if (f > 0) el("rect", { x, y: top + f * fh - 4, width: w, height: 8, fill: "rgba(0,0,0,0.07)" }, g);
    }
    return { top, x, w };
  }

  function waterTank(g, x, y) {
    el("rect", { x, y: y - 74, width: 66, height: 74, rx: 8, fill: "#1E1E1E" }, g);
    el("ellipse", { cx: x + 33, cy: y - 74, rx: 33, ry: 8, fill: "#2B2B2B" }, g);
    for (let i = 1; i < 4; i++) el("rect", { x, y: y - 74 + i * 18, width: 66, height: 3, fill: "#2E2E2E" }, g);
    el("rect", { x: x + 8, y, width: 6, height: 10, fill: C.steel }, g);
    el("rect", { x: x + 52, y, width: 6, height: 10, fill: C.steel }, g);
  }

  function panels(g, x, y, n) {
    // Elevated GI frame (Indian flat-roof style), panels tilted toward the sun.
    const pg = el("g", { id: "panels" }, g);
    for (let i = 0; i < n; i++) {
      const px = x + i * 98;
      el("line", { x1: px + 10, y1: y, x2: px + 10, y2: y + 56, stroke: "#9AA0A6", "stroke-width": 5 }, pg);
      el("line", { x1: px + 80, y1: y, x2: px + 80, y2: y + 30, stroke: "#9AA0A6", "stroke-width": 5 }, pg);
      const p = el("polygon", { points: `${px},${y + 8} ${px + 92},${y - 22} ${px + 92},${y + 14} ${px},${y + 44}`, fill: "#1F3A5F", stroke: "#C9D3DC", "stroke-width": 2 }, pg);
      for (let k = 1; k < 4; k++) el("line", { x1: px + k * 23, y1: y + 8 - k * 7.5, x2: px + k * 23, y2: y + 44 - k * 7.5, stroke: "#3E6A96", "stroke-width": 1.5 }, pg);
      el("line", { x1: px, y1: y + 26, x2: px + 92, y2: y - 4, stroke: "#3E6A96", "stroke-width": 1.5 }, pg);
      p.classList.add("pv");
    }
    return pg;
  }

  function clothesLine(g, x1, x2, y) {
    el("path", { d: sag(x1, y, x2, y, 10), fill: "none", stroke: "#6E6258", "stroke-width": 2 }, g);
    const cols = ["#C0392B", "#2E86C1", "#F4D03F", "#FDFEFE"];
    for (let i = 0; i < 4; i++) {
      const cx = x1 + 30 + i * ((x2 - x1 - 60) / 3);
      el("rect", { x: cx - 14, y: y + 6, width: 28, height: 40, fill: cols[i], class: "cloth", "data-i": i }, g);
    }
  }

  function ltPole(g, x) {
    // PSC concrete LT pole, tapered, with a channel cross-arm and pin insulators.
    el("polygon", { points: `${x - 11},880 ${x + 11},880 ${x + 6},330 ${x - 6},330`, fill: C.conc }, g);
    el("polygon", { points: `${x + 3},880 ${x + 11},880 ${x + 6},330 ${x + 2},330`, fill: C.concD }, g);
    el("rect", { x: x - 70, y: 352, width: 140, height: 10, fill: C.steel }, g);
    [-58, -22, 22, 58].forEach(dx => el("rect", { x: x + dx - 4, y: 340, width: 8, height: 14, fill: "#E8E2D6" }, g));
    // the usual cable spaghetti
    for (let i = 0; i < 5; i++) el("path", { d: `M ${x - 6} ${420 + i * 22} q ${-40 - i * 8} 18 ${-12} ${46 + i * 6}`, fill: "none", stroke: "#2B2B2B", "stroke-width": 3 }, g);
  }

  function transformer(g, x) {
    // Double-pole structure (two PSC poles, channel platform), grey tank with radiator fins, three HT bushings,
    // AB switch + drop-out fuses above (from the TNEB / Rajasthan references).
    const tg = el("g", { id: "xfmr" }, g);
    [x, x + 150].forEach(px => {
      el("polygon", { points: `${px - 10},880 ${px + 10},880 ${px + 6},250 ${px - 6},250`, fill: C.conc }, tg);
      el("polygon", { points: `${px + 3},880 ${px + 10},880 ${px + 6},250 ${px + 2},250`, fill: C.concD }, tg);
    });
    el("rect", { x: x - 24, y: 262, width: 198, height: 9, fill: C.rust }, tg);                     // HT cross-arm
    [10, 75, 140].forEach(dx => el("ellipse", { cx: x + dx, cy: 255, rx: 13, ry: 8, fill: "#4A4440" }, tg));
    el("rect", { x: x - 18, y: 388, width: 186, height: 8, fill: C.rust }, tg);                     // fuse arm
    [20, 75, 130].forEach(dx => {
      el("rect", { x: x + dx - 5, y: 362, width: 10, height: 28, fill: "#5A534D" }, tg);
      el("line", { x1: x + dx, y1: 262, x2: x + dx, y2: 362, stroke: "#3B3B3B", "stroke-width": 2 }, tg);
    });
    el("rect", { x: x - 20, y: 610, width: 190, height: 10, fill: C.rust }, tg);                    // platform
    el("rect", { x: x + 18, y: 498, width: 114, height: 112, rx: 4, fill: "#77807F" }, tg);         // tank
    for (let i = 0; i < 7; i++) el("rect", { x: x + 24 + i * 15, y: 506, width: 7, height: 96, fill: "#5F6867" }, tg); // fins
    el("rect", { x: x + 40, y: 470, width: 70, height: 22, rx: 11, fill: "#6B7473" }, tg);          // conservator
    [42, 75, 108].forEach(dx => {
      el("rect", { x: x + dx - 5, y: 472, width: 10, height: 28, fill: "#3D3A37" }, tg);
      el("line", { x1: x + dx, y1: 396, x2: x + dx, y2: 472, stroke: "#3B3B3B", "stroke-width": 2 }, tg);
    });
    el("text", { x: x + 75, y: 650, "text-anchor": "middle", class: "w-tag" }, tg).textContent = "11 kV / 433 V";
    return tg;
  }

  function dhol(parent, cx, cy) {
    // The drummer: a stylised dhol icon (no human character), cyan glow ring when it beats.
    const g = el("g", { id: "dhol", transform: `translate(${cx} ${cy})` }, parent);
    el("circle", { r: 62, fill: "rgba(88,166,255,0.16)", id: "dholGlow" }, g);
    el("rect", { x: -40, y: -24, width: 80, height: 48, rx: 22, fill: "#C2652B", stroke: "#7A3A16", "stroke-width": 3 }, g);
    el("ellipse", { cx: -40, cy: 0, rx: 10, ry: 24, fill: "#F2E3C6", stroke: "#7A3A16", "stroke-width": 3 }, g);
    el("ellipse", { cx: 40, cy: 0, rx: 10, ry: 24, fill: "#F2E3C6", stroke: "#7A3A16", "stroke-width": 3 }, g);
    el("polyline", { points: "-30,-22 -20,22 -10,-22 0,22 10,-22 20,22 30,-22", fill: "none", stroke: "#F2E3C6", "stroke-width": 3, "stroke-linejoin": "round", opacity: 0.9 }, g); // dhol lacing (zig-zag)
    el("line", { x1: 46, y1: -40, x2: 18, y2: -6, stroke: "#6B4423", "stroke-width": 5, "stroke-linecap": "round" }, g); // stick
    return g;
  }

  function solarBox(parent, x, y) {
    // Wall-mounted on-grid inverter: white box, display, sun badge (the dancer), DC + AC isolator boxes below.
    const g = el("g", { id: "box" }, parent);
    el("rect", { x, y, width: 120, height: 150, rx: 10, fill: "#F4F6F7", stroke: "#AEB6BF", "stroke-width": 3 }, g);
    el("rect", { x: x + 20, y: y + 22, width: 80, height: 30, rx: 4, fill: "#1B2631" }, g);
    el("circle", { cx: x + 100, cy: y + 130, r: 7, fill: C.green, id: "boxLed" }, g);
    const sb = el("g", { id: "badge", transform: `translate(${x + 60} ${y + 95})` }, g);
    el("circle", { r: 20, fill: "#F5B041" }, sb);
    for (let i = 0; i < 8; i++) {
      const a = i * Math.PI / 4;
      el("line", { x1: Math.cos(a) * 24, y1: Math.sin(a) * 24, x2: Math.cos(a) * 32, y2: Math.sin(a) * 32, stroke: "#F5B041", "stroke-width": 4, "stroke-linecap": "round" }, sb);
    }
    el("circle", { cx: -7, cy: -4, r: 3, fill: "#5D4037" }, sb);
    el("circle", { cx: 7, cy: -4, r: 3, fill: "#5D4037" }, sb);
    el("path", { d: "M -8 6 Q 0 13 8 6", fill: "none", stroke: "#5D4037", "stroke-width": 3, "stroke-linecap": "round" }, sb);
    el("rect", { x: x - 6, y: y + 176, width: 56, height: 64, rx: 4, fill: "#ECEFF1", stroke: "#AEB6BF", "stroke-width": 2 }, g);
    el("rect", { x: x + 70, y: y + 176, width: 56, height: 64, rx: 4, fill: "#ECEFF1", stroke: "#AEB6BF", "stroke-width": 2 }, g);
    el("text", { x: x + 22, y: y + 214, "text-anchor": "middle", class: "w-mini" }, g).textContent = "DC";
    el("text", { x: x + 98, y: y + 214, "text-anchor": "middle", class: "w-mini" }, g).textContent = "AC";
    return g;
  }

  function lane(svg) {
    const defs = el("defs", {}, svg);
    const sky = el("linearGradient", { id: "sky", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    el("stop", { offset: "0", "stop-color": C.sky0 }, sky);
    el("stop", { offset: "1", "stop-color": C.sky1 }, sky);
    const sun = el("radialGradient", { id: "sun" }, defs);
    el("stop", { offset: "0", "stop-color": "#FFF8E1" }, sun);
    el("stop", { offset: "0.25", "stop-color": "#FFE7A3", "stop-opacity": 0.9 }, sun);
    el("stop", { offset: "1", "stop-color": "#FFE7A3", "stop-opacity": 0 }, sun);
    const world = el("g", { id: "world" }, svg);
    el("rect", { x: -200, y: -200, width: 2320, height: 1480, fill: "url(#sky)" }, world);
    el("circle", { cx: 1650, cy: 150, r: 260, fill: "url(#sun)", id: "sunGlow" }, world);
    el("circle", { cx: 1650, cy: 150, r: 46, fill: "#FFF6D5" }, world);
    // distant skyline in haze
    for (let i = 0; i < 14; i++) el("rect", { x: -100 + i * 160, y: 690 - (i * 37 % 90), width: 140, height: 200, fill: C.haze, opacity: 0.85 }, world);
    el("rect", { x: -200, y: 880, width: 2320, height: 400, fill: C.ground }, world);
    el("rect", { x: -200, y: 930, width: 2320, height: 160, fill: C.road }, world);
    el("rect", { x: -200, y: 926, width: 2320, height: 6, fill: C.kerb }, world);
    [[90, 470], [600, 520], [1560, 420]].forEach(([hx, hw]) =>
      el("polygon", { points: `${hx},880 ${hx + hw},880 ${hx + hw - 60},930 ${hx - 60},930`, fill: "rgba(60,40,20,0.16)" }, world));
    const h1 = house(world, 90, 470, 2, "#E2A27A", "#C98762");
    const h2 = house(world, 600, 520, 3, "#EED9A8", "#D6BC85", (f, i) => f === 2 || (f === 1 && i >= 1));
    el("rect", { x: 640, y: 752, width: 86, height: 128, rx: 3, fill: "#7A4E2D" }, world);            // door
    el("rect", { x: 646, y: 758, width: 74, height: 118, rx: 2, fill: "none", stroke: "#5C3A21", "stroke-width": 3 }, world);
    const h3 = house(world, 1560, 420, 2, "#B8CDB0", "#9DB494");
    waterTank(world, h2.x + 420, h2.top - 14);
    const pv = panels(world, h2.x + 40, h2.top - 74, 4);
    clothesLine(world, h1.x + 60, h1.x + 400, h1.top - 70);
    el("rect", { x: h1.x + 60, y: h1.top - 74, width: 4, height: 60, fill: "#6E6258" }, world);
    el("rect", { x: h1.x + 398, y: h1.top - 74, width: 4, height: 60, fill: "#6E6258" }, world);
    el("rect", { x: h3.x + 30, y: h3.top - 40, width: 40, height: 26, rx: 6, fill: "#C0392B" }, world);  // tulsi pot
    el("ellipse", { cx: h3.x + 50, cy: h3.top - 52, rx: 26, ry: 18, fill: "#4E7D3A" }, world);
    ltPole(world, 1230);
    const xf = transformer(world, 1330);
    // LT wires: transformer → LT pole → house 2 (the service wire)
    const wires = el("g", { id: "wires" }, world);
    const W1 = sag(1340, 396, 1230, 356, 26), W2 = sag(1230, 356, 1105, 560, 40), W3 = sag(1230, 340, -100, 120, 30);
    [W3].forEach(d => el("path", { d, fill: "none", stroke: "#2B2B2B", "stroke-width": 3 }, wires));
    const main = el("path", { id: "wireMain", d: `${W1} ${W2.replace("M", "L")}`, fill: "none", stroke: "#2B2B2B", "stroke-width": 4 }, wires);
    // house 2 wall: net meter + solar box, cable from the panels
    el("rect", { x: 1090, y: 560, width: 30, height: 30, fill: "#2B2B2B" }, world);
    const meter = el("g", { id: "meter" }, world);
    el("rect", { x: 980, y: 640, width: 74, height: 96, rx: 6, fill: "#E5E8E8", stroke: "#99A3A4", "stroke-width": 2 }, meter);
    el("rect", { x: 990, y: 654, width: 54, height: 22, fill: "#1D2A35" }, meter);
    el("text", { x: 1017, y: 671, "text-anchor": "middle", class: "w-lcd" }, meter).textContent = "→ EXP";
    const box = solarBox(world, 800, 610);
    const cable = el("path", { id: "pvCable", d: `M ${h2.x + 200} ${h2.top - 30} L ${h2.x + 200} ${h2.top + 6} L 1100 ${h2.top + 6} L 1100 590 L 860 590 L 860 610`, fill: "none", stroke: C.amber, "stroke-width": 5, opacity: 0.95 }, world);
    el("path", { d: "M 920 690 L 980 690", stroke: C.cyan, "stroke-width": 5 }, world);
    el("path", { d: "M 1054 690 L 1105 690 L 1105 590", fill: "none", stroke: C.cyan, "stroke-width": 5 }, world);
    const dh = dhol(world, 1405, 200);
    return { world, main, cable, box, dhol: dh, pv };
  }

  // ---------- blueprint X-ray ----------
  function xray(svg) {
    const g = el("g", { id: "xray", opacity: 0 }, svg);
    el("rect", { x: 0, y: 0, width: 1920, height: 1080, fill: C.bg }, g);
    const grid = el("g", { opacity: 0.9 }, g);
    for (let x = 0; x <= 1920; x += 48) el("line", { x1: x + 0.5, y1: 0, x2: x + 0.1, y2: 1080, stroke: C.grid, "stroke-width": x % 240 ? 1 : 2 }, grid);
    for (let y = 0; y <= 1080; y += 48) el("line", { x1: 0, y1: y + 0.5, x2: 1920, y2: y + 0.1, stroke: C.grid, "stroke-width": y % 240 ? 1 : 2 }, grid);
    // box outline (cutaway)
    const cam = el("g", { id: "xcam" }, g);
    el("rect", { x: 560, y: 220, width: 800, height: 520, rx: 26, fill: "rgba(22,27,34,0.85)", stroke: C.slate, "stroke-width": 3 }, cam);
    el("text", { x: 590, y: 262, class: "x-tag" }, cam).textContent = "SOLAR BOX · CUTAWAY";
    // DC bus in (flat amber), H-bridge block, AC out (cyan sine)
    el("line", { x1: 120, y1: 480, x2: 700, y2: 480.3, stroke: C.amber, "stroke-width": 8, "stroke-linecap": "round" }, cam);
    const dots = el("g", { id: "dcDots" }, cam);
    for (let i = 0; i < 12; i++) el("circle", { cx: 120 + i * 48, cy: 480, r: 7, fill: "#F2C14E", class: "dcdot" }, dots);
    el("rect", { x: 720, y: 380, width: 220, height: 200, rx: 12, fill: "none", stroke: C.read, "stroke-width": 3 }, cam);
    [[760, 420], [860, 420], [760, 520], [860, 520]].forEach(([sx, sy]) => {
      el("rect", { x: sx, y: sy, width: 40, height: 40, rx: 4, fill: "none", stroke: C.cyan, "stroke-width": 3, class: "sw" }, cam);
    });
    el("text", { x: 830, y: 612, "text-anchor": "middle", class: "x-tag" }, cam).textContent = "D.C. → A.C.";
    const sine = el("path", { id: "acOut", fill: "none", stroke: C.cyan, "stroke-width": 8, "stroke-linecap": "round" }, cam);
    // relay
    const relay = el("g", { id: "relay" }, cam);
    el("rect", { x: 1180, y: 430, width: 120, height: 100, rx: 10, fill: "none", stroke: C.slate, "stroke-width": 3 }, relay);
    el("line", { x1: 1200, y1: 480, x2: 1280, y2: 480.3, stroke: C.green, "stroke-width": 6, id: "contact" }, relay);
    el("text", { x: 1240, y: 556, "text-anchor": "middle", class: "x-tag" }, relay).textContent = "RELAY";
    // scope strip: grid trace + box trace overlap
    const scope = el("g", { id: "scope" }, g);
    el("rect", { x: 420, y: 760, width: 1080, height: 190, rx: 14, fill: C.panel, stroke: C.grid, "stroke-width": 2 }, scope);
    el("text", { x: 446, y: 796, class: "x-tag" }, scope).textContent = "SCOPE · GRID vs BOX";
    const tGrid = el("path", { id: "tGrid", fill: "none", stroke: C.cyan, "stroke-width": 5 }, scope);
    const tBox = el("path", { id: "tBox", fill: "none", stroke: C.green, "stroke-width": 3, "stroke-dasharray": "10 6" }, scope);
    el("text", { x: 1476, y: 796, "text-anchor": "end", class: "x-tag green" }, scope).textContent = "IN STEP";
    el("text", { x: 1880, y: 1050, "text-anchor": "end", class: "x-tag" }, g).textContent = "ILLUSTRATION · SLOWED DOWN";
    return { g, sine, tGrid, tBox, dots, cam };
  }

  // sine path between x0..x1 around yc, `cycles` cycles, phase in radians
  function sinePath(x0, x1, yc, amp, cycles, phase) {
    let d = "";
    for (let i = 0; i <= 120; i++) {
      const x = x0 + (x1 - x0) * i / 120;
      const y = yc - amp * Math.sin(phase + 2 * Math.PI * cycles * i / 120);
      d += (i ? " L " : "M ") + x.toFixed(1) + " " + y.toFixed(1);
    }
    return d;
  }

  window.W36 = { el, C, lane, xray, sinePath };
})();
