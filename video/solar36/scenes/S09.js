// S09 · Hybrid (2:40.7–2:59.5). Lines 19–20. The fans are still dead; the on-grid box slides out, a hybrid box and a
// battery slide in; it works with the grid (street wire lights) and with a battery (battery cable lights). Inset: when the
// grid dies, a contact inside first cuts the house off from the street (visible gap); the drum flies from the street to
// the battery; the backed-up circuit (the fan) runs again, the rest of the house stays dark; the panels dance again.
// Cues (local s): "keep your fans running" 0.74 · "a different box" 2.67 · "a hybrid inverter" 4.44 · "works with the
// grid" 5.87 · "and with a battery" 8.60 · "When the grid dies" 9.85 · "cuts your house off from the street" 11.08 ·
// "the battery becomes the drummer" 14.75 · "the panels dance again" 17.10.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg); document.getElementById("xray").setAttribute("opacity", 0);
  const world = L.world;
  K.hud([{ k: "grid", label: "GRID", v: "OFF", cls: "" }, { k: "box", label: "SOLAR BOX", v: "TRIPPED", cls: "red" },
         { k: "bk", label: "BACKUP", v: "GRID ✕", cls: "red", hidden: true }]);
  K.gridDead(tl, 0);
  tl.set("#slowTag", { opacity: 0 }, 0).set("#boxLed", { attr: { fill: "#f85149" } }, 0).set("#dholBadge", { opacity: 0.35 }, 0);
  K.tag(tl, 0, D, "ILLUSTRATION");

  // ---- 0:00 the fans are still dead ----
  const fan = el("g", { id: "wFan" }, world);
  el("circle", { cx: 634, cy: 501, r: 6, fill: "#3E4A57" }, fan);
  [0, 120, 240].forEach(a => el("ellipse", { cx: 634, cy: 486, rx: 6, ry: 15, fill: "#3E4A57", transform: `rotate(${a} 634 501)` }, fan));
  K.cam(tl, 0, 640, 520, 2.6);
  K.label(tl, 0.8, 2.6, "FANS OFF", 120, 860).classList.add("red");
  K.look(tl, 2.3, 1.0, 900, 660, 2.3, "power2.inOut");

  // ---- 2.67 a different box: the on-grid box slides out, the hybrid + battery slide in ----
  tl.to("#box", { x: -40, opacity: 0, duration: 0.45, ease: "power2.in" }, 2.8);
  const hy = el("g", { id: "hyb", opacity: 0 }, world);
  el("rect", { x: 860, y: 732, width: 132, height: 10, fill: "rgba(60,40,20,0.22)" }, hy);
  el("rect", { x: 854, y: 576, width: 140, height: 154, rx: 12, fill: "#2C3E50", stroke: "#1B2631", "stroke-width": 3 }, hy);
  el("rect", { x: 872, y: 594, width: 104, height: 44, rx: 4, fill: "#0E3B2E" }, hy);
  el("rect", { x: 884, y: 604, width: 40, height: 22, rx: 3, fill: "none", stroke: "#7CF0B5", "stroke-width": 3 }, hy);  // battery glyph
  el("rect", { x: 924, y: 610, width: 5, height: 10, fill: "#7CF0B5" }, hy);
  el("rect", { id: "hyFill", x: 887, y: 607, width: 34, height: 16, fill: "#7CF0B5", opacity: 0.3 }, hy);
  const hb = el("g", { id: "hyBadgePos", transform: "translate(924 680)" }, hy);
  const hbg = el("g", { id: "hyBadge" }, hb);
  el("circle", { r: 16, fill: "none", stroke: "#E67E22", "stroke-width": 4 }, hbg);
  for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; el("line", { x1: Math.cos(a) * 21, y1: Math.sin(a) * 21, x2: Math.cos(a) * 26, y2: Math.sin(a) * 26, stroke: "#E67E22", "stroke-width": 3.5, "stroke-linecap": "round" }, hbg); }
  el("circle", { id: "hyLed", cx: 976, cy: 714, r: 5, fill: "#d29922" }, hy);
  // the battery: floor-standing, white case, four charge bars
  const bat = el("g", { id: "bat", opacity: 0 }, world);
  el("rect", { x: 1000, y: 760, width: 90, height: 122, rx: 10, fill: "#ECF0F1", stroke: "#AEB6BF", "stroke-width": 3 }, bat);
  [0, 1, 2, 3].forEach(k => el("rect", { class: "bBar", x: 1016, y: 852 - k * 22, width: 58, height: 14, rx: 3, fill: "#3fb950", opacity: 0.25 }, bat));
  const bcab = el("path", { id: "bCab", d: "M 1045 760 L 1045 742 L 960 742 L 960 730", fill: "none", stroke: "#3fb950", "stroke-width": 6, opacity: 0.35 }, bat);
  tl.fromTo("#hyb", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, 3.4);
  tl.fromTo("#bat", { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, 3.7);
  K.label(tl, 4.45, 5.8, "HYBRID INVERTER", 1150, 300).classList.add("green");
  tl.set("#r_box .k", { textContent: "HYBRID BOX" }, 4.45); K.hudSet(tl, 4.45, "box", "READY", "amber");
  // 5.87 works with the grid (street wire lights cyan) … 8.60 and with a battery (battery cable + bars light green)
  K.look(tl, 5.6, 1.0, 1000, 600, 1.5, "power2.inOut");
  tl.to(".wire", { attr: { stroke: "#58a6ff" }, duration: 0.3 }, 5.9).to(".wire", { attr: { stroke: "#9aa0a6" }, duration: 0.4 }, 8.3);
  tl.to("#bCab", { opacity: 1, duration: 0.3 }, 8.6).to(".bBar", { opacity: 1, duration: 0.2, stagger: 0.12 }, 8.6);
  K.label(tl, 5.95, 9.5, "GRID + BATTERY", 120, 860);

  // ---- 9.85 when the grid dies: inset inside the hybrid ----
  K.look(tl, 9.6, 0.8, 924, 653, 3.0, "power2.in");
  const hx = el("g", { id: "hx", "clip-path": "url(#hxWipe)" }, svg);
  const cp = el("clipPath", { id: "hxWipe" }, svg.querySelector("defs")); const wc = el("circle", { cx: 960, cy: 540, r: 0 }, cp);
  el("rect", { width: 1920, height: 1080, fill: "#0d1117" }, hx);
  for (let x = 0; x <= 1920; x += 48) el("line", { x1: x + 0.5, y1: 0, x2: x + 0.1, y2: 1080, stroke: x % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": x % 240 ? 1 : 2 }, hx);
  for (let y = 0; y <= 1080; y += 48) el("line", { x1: 0, y1: y + 0.5, x2: 1920, y2: y + 0.1, stroke: y % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": y % 240 ? 1 : 2 }, hx);
  const hc = el("g", { id: "hxCam" }, hx);
  el("rect", { x: 600, y: 230, width: 720, height: 680, rx: 40, fill: "rgba(22,27,34,0.9)", stroke: "#C9D1D9", "stroke-width": 3, "stroke-dasharray": "14 8" }, hc);
  el("text", { x: 636, y: 290, class: "x-title" }, hc).textContent = "INSIDE THE HYBRID";
  // street side (left): pole + slate line; house side (right): the house bus with two loads
  const pole = el("g", {}, hc);
  el("rect", { x: 222, y: 430, width: 16, height: 200, fill: "#8b949e" }, pole); el("rect", { x: 186, y: 438, width: 88, height: 10, fill: "#8b949e" }, pole);
  el("text", { x: 230, y: 690, "text-anchor": "middle", class: "x-lab" }, hc).textContent = "STREET";
  el("line", { x1: 238, y1: 520, x2: 760, y2: 520.2, stroke: "#8b949e", "stroke-width": 7, "stroke-linecap": "round" }, hc);
  el("rect", { x: 740, y: 520, width: 20, height: 40, fill: "#8b949e" }, hc);                       // contact posts
  el("rect", { x: 840, y: 520, width: 20, height: 40, fill: "#8b949e" }, hc);
  const ctc = el("line", { id: "ctc", x1: 760, y1: 520, x2: 846, y2: 512, stroke: "#3fb950", "stroke-width": 10, "stroke-linecap": "round" }, hc);
  el("text", { x: 800, y: 610, "text-anchor": "middle", class: "x-tag" }, hc).textContent = "GRID SWITCH";
  const bus = el("line", { id: "bus", x1: 846, y1: 520, x2: 1770, y2: 520.2, stroke: "#58a6ff", "stroke-width": 7, "stroke-linecap": "round", opacity: 0.35 }, hc);
  // loads: backed-up fan (lights up later) and a non-backup load (stays dark)
  const ldF = el("g", { id: "ldFan" }, hc);
  el("line", { x1: 1460, y1: 520, x2: 1460.2, y2: 640, stroke: "#58a6ff", "stroke-width": 6, opacity: 0.35, class: "fanWire" }, ldF);
  el("circle", { cx: 1460, cy: 700, r: 58, fill: "#161b22", stroke: "#30363d", "stroke-width": 4 }, ldF);
  const fb = el("g", { id: "fanBl" }, ldF);
  [0, 120, 240].forEach(a => el("ellipse", { cx: 1460, cy: 672, rx: 11, ry: 28, fill: "#8b949e", transform: `rotate(${a} 1460 700)` }, fb));
  el("circle", { cx: 1460, cy: 700, r: 9, fill: "#C9D1D9" }, ldF);
  el("text", { x: 1460, y: 800, "text-anchor": "middle", class: "x-tag" }, ldF).textContent = "BACKUP FAN";
  const ldX = el("g", { id: "ldX", opacity: 0.45 }, hc);
  el("line", { x1: 1770, y1: 520, x2: 1770.2, y2: 640, stroke: "#30363d", "stroke-width": 6 }, ldX);
  el("rect", { x: 1720, y: 640, width: 100, height: 110, rx: 10, fill: "#161b22", stroke: "#30363d", "stroke-width": 4 }, ldX);
  el("text", { x: 1770, y: 800, "text-anchor": "middle", class: "x-tag" }, ldX).textContent = "NO BACKUP";
  // battery (below) and panels (top) feed the house bus through the hybrid
  const bt = el("g", { id: "hxBat" }, hc);
  el("rect", { x: 1000, y: 680, width: 120, height: 150, rx: 12, fill: "#ECF0F1", stroke: "#AEB6BF", "stroke-width": 3 }, bt);
  [0, 1, 2, 3].forEach(k => el("rect", { x: 1020, y: 800 - k * 30, width: 80, height: 20, rx: 3, fill: "#3fb950" }, bt));
  el("line", { x1: 1060, y1: 680, x2: 1060.2, y2: 520, stroke: "#3fb950", "stroke-width": 7 }, bt);
  el("text", { x: 1060, y: 872, "text-anchor": "middle", class: "x-tag", fill: "#3fb950" }, hc).textContent = "BATTERY";
  const pvI = el("g", {}, hc);
  el("rect", { x: 1170, y: 330, width: 110, height: 70, rx: 4, fill: "#1F3A5F", stroke: "#AEB6BF", "stroke-width": 3 }, pvI);
  el("line", { x1: 1225, y1: 400, x2: 1225.2, y2: 520, stroke: "#F2C14E", "stroke-width": 7 }, pvI);
  const pvd = [0, 1, 2].map(() => el("circle", { r: 7, fill: "#F2C14E", opacity: 0 }, hc));
  // the drummer: a dhol that flies from the street to the battery
  const dr = el("g", { id: "hxDrum" }, hc);
  el("circle", { cx: 0, cy: 0, r: 46, fill: "#0d1117", stroke: "#8b949e", "stroke-width": 4, class: "drRing" }, dr);
  el("path", { d: "M -30 -16 Q 0 -26 30 -16 L 30 16 Q 0 26 -30 16 Z", fill: "#5a5f66", stroke: "#3a2a1a", "stroke-width": 3, class: "drBody" }, dr);
  const hxBadge = el("g", { transform: "translate(1225 300)" }, hc); const hxb = el("g", { id: "hxB" }, hxBadge);
  el("circle", { r: 18, fill: "none", stroke: "#E67E22", "stroke-width": 4 }, hxb);
  for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; el("line", { x1: Math.cos(a) * 23, y1: Math.sin(a) * 23, x2: Math.cos(a) * 29, y2: Math.sin(a) * 29, stroke: "#E67E22", "stroke-width": 4, "stroke-linecap": "round" }, hxb); }
  tl.set(dr, { x: 230, y: 380 }, 0);
  tl.set("#hx", { visibility: "hidden" }, 0).set("#hx", { visibility: "visible" }, 10.25);
  tl.fromTo(wc, { attr: { r: 0 } }, { attr: { r: 1150 }, duration: 0.5, ease: "power2.in", immediateRender: false }, 10.3);
  tl.set("#world, #fg", { visibility: "hidden" }, 10.85);
  tl.fromTo("#hxCam", { scale: 1.05, svgOrigin: "960 560" }, { scale: 1.0, duration: 8.4, ease: "sine.out", immediateRender: false }, 10.3);
  // 11.6 the grid switch opens: a visible gap, the street stays slate
  tl.to(ctc, { rotation: -32, svgOrigin: "760 520", duration: 0.16, ease: "power3.in" }, 12.3).to(ctc, { attr: { stroke: "#f85149" }, duration: 0.05 }, 12.46);
  const fl = el("circle", { cx: 800, cy: 515, r: 20, fill: "none", stroke: "#FFFFFF", "stroke-width": 8, opacity: 0 }, hc);
  tl.fromTo(fl, { opacity: 1, attr: { r: 20 } }, { opacity: 0, attr: { r: 160 }, duration: 0.45, ease: "power2.out", immediateRender: false }, 12.46);
  K.hudShow(tl, 12.5, "bk");
  K.label(tl, 12.5, 14.3, "STREET CUT OFF", 120, 860).classList.add("red");
  // 14.75 the battery becomes the drummer: the dhol flies to the battery and comes alive
  tl.to(dr, { x: 1060, y: 640, duration: 0.9, ease: "power2.inOut" }, 14.3);
  tl.to("#hxDrum .drRing", { attr: { stroke: "#3fb950" }, duration: 0.2 }, 15.6).to("#hxDrum .drBody", { attr: { fill: "#9C5A2E" }, duration: 0.2 }, 15.6);
  K.hudSet(tl, 15.6, "bk", "BATTERY ✓", "green"); K.hudSet(tl, 15.6, "box", "ON BATTERY", "green");
  K.label(tl, 14.4, 16.8, "BATTERY = DRUMMER", 120, 860).classList.add("green");
  tl.to("#bus, .fanWire", { opacity: 1, duration: 0.3 }, 15.7);
  // 17.10 the panels dance again: beats from the battery, the badge hops, the backed-up fan spins; the rest stays dark
  for (let t = 15.7; t < D - 0.1; t += K.BEAT) {
    tl.fromTo(dr, { scale: 1.12 }, { scale: 1, duration: 0.25, ease: "sine.out", immediateRender: false }, t);
    if (t > 17.0) tl.to(hxb, { y: -12, duration: 0.09, ease: "power2.out" }, t + 0.1).to(hxb, { y: 0, duration: 0.2, ease: "sine.in" }, t + 0.19);
  }
  tl.fromTo(fb, { rotation: 0, svgOrigin: "1460 700" }, { rotation: 1080, duration: D - 16.0, ease: "power1.in", immediateRender: false }, 16.0);
  tl.to("#fanBl ellipse", { attr: { fill: "#58a6ff" }, duration: 0.3 }, 16.0);
  const pp = { T: 0 };
  tl.fromTo(pp, { T: 0 }, { T: D - 17.1, duration: D - 17.1, ease: "none", immediateRender: false, onUpdate: () => {
    pvd.forEach((c, k) => { const u = (pp.T * 1.2 + k / 3) % 1; c.setAttribute("cx", 1225); c.setAttribute("cy", 400 + u * 120); c.setAttribute("opacity", 1); }); } }, 17.1);
  K.label(tl, 17.15, D, "PANELS DANCE AGAIN", 120, 860).classList.add("amber");
};
