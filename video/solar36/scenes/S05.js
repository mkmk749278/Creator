// S05 · Power cut and the what-if (1:13.9–1:37.1). Lines 9–11. The board switches the street off: the substation breaker
// opens, wires go slate from the feeder end, the drum stops mid-beat. WHAT IF the box kept pushing: the dead wires relight
// red from the house outward. Cutaway: the pole transformer in reverse, 230 V in on the few-turn side, about 11,000 V out on
// the many-turn side. Back on the 11 kV line, a lineman who thinks it is off; the red creeps toward his gloves; freeze.
// Cues (local s): "Now the power cut comes" 0.77 · "switches off the supply" 2.56 · "Think about it" 5.83 · "kept pushing"
// 6.78 · "dead wire alive again" 7.91 · "transformer … in reverse" 11.62 · "two hundred and thirty volts" 14.52 ·
// "about eleven thousand volts" 16.77 · "the lineman thinks is switched off" 20.09.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg); document.getElementById("xray").setAttribute("opacity", 0);
  const world = L.world;
  K.hud([{ k: "grid", label: "GRID", v: "230 V · 50.0 Hz", cls: "cyan" }, { k: "box", label: "SOLAR BOX", v: "IN STEP ✓", cls: "green" },
         { k: "line", label: "LINE · WHAT IF", v: "230 V", cls: "red", hidden: true }]);
  tl.set("#slowTag", { opacity: 0 }, 0);
  K.tag(tl, 0, D, "ILLUSTRATION");

  // ---- 0:00 the street, still in step; the drum stops mid-beat on the cut ----
  K.cam(tl, 0, 1350, 470, 1.5);
  K.look(tl, 0.3, 2.0, 1180, 470, 1.0, "power2.inOut");                 // pull back to the whole street
  K.beats(tl, L, 0.1, 2.5);
  // the substation breaker at the feeder end (right edge), opens on "switches off the supply"
  const brk = el("g", { id: "brk" }, world);
  el("rect", { x: 1770, y: 300, width: 120, height: 120, rx: 10, fill: "#5E6A73", stroke: "#3E4A57", "stroke-width": 4 }, brk);
  el("circle", { cx: 1800, cy: 380, r: 9, fill: "#D5DBDB" }, brk); el("rect", { x: 1846, y: 368, width: 16, height: 22, rx: 3, fill: "#D5DBDB" }, brk);
  const lev = el("line", { id: "brkLev", x1: 1800, y1: 380, x2: 1852, y2: 380, stroke: "#3fb950", "stroke-width": 9, "stroke-linecap": "round" }, brk);
  el("rect", { x: 1786, y: 318, width: 88, height: 26, rx: 4, fill: "#1B2631" }, brk);
  el("text", { x: 1830, y: 338, "text-anchor": "middle", class: "w-tagM" }, brk).textContent = "11 kV";
  el("path", { d: "M 1830 300 L 1830 252", stroke: "#4a4a4a", "stroke-width": 4 }, brk);
  tl.to(lev, { rotation: -38, svgOrigin: "1800 380", duration: 0.18, ease: "power3.in" }, 2.7).to(lev, { attr: { stroke: "#f85149" }, duration: 0.05 }, 2.85);
  // wires go slate from the feeder end toward the house
  const wires = [...document.querySelectorAll(".wire")].map(w => { const b = w.getBBox(); return { w, x: b.x + b.width / 2 }; });
  wires.forEach(({ w, x }) => tl.to(w, { attr: { stroke: "#9aa0a6" }, duration: 0.25 }, 2.9 + (1920 - x) / 1920 * 1.0));
  tl.to("#dholBadge", { filter: "grayscale(1) brightness(0.8)", duration: 0.3 }, 2.6);
  K.hudSet(tl, 2.9, "grid", "0 V · —", "");
  tl.set("#r_box", { display: "none" }, 2.9);
  K.label(tl, 2.9, 5.5, "SUPPLY OFF", 1440, 470).classList.add("red");

  // ---- 5.83 WHAT IF: the box keeps pushing; the dead wires relight red from the house outward ----
  K.whatIf(tl, 5.8, D);
  K.look(tl, 5.8, 1.0, 1000, 640, 1.6, "power2.inOut");
  tl.to("#boxLed", { attr: { fill: "#f85149" }, duration: 0.1 }, 6.8);
  const push = [0, 1, 2].map(() => el("circle", { r: 10, fill: "#f85149", stroke: "#FFFFFF", "stroke-width": 3, opacity: 0 }, world));
  const ring = L.ring, len = ring.getTotalLength(), pp = { u: 1 };
  tl.fromTo(pp, { u: 1 }, { u: 0.1, duration: 3.6, ease: "power1.in", immediateRender: false, onUpdate: () => {
    push.forEach((c, k) => { const q = Math.min(1, pp.u + 0.03 * k), p = ring.getPointAtLength(q * len);
      c.setAttribute("cx", p.x); c.setAttribute("cy", p.y); c.setAttribute("opacity", pp.u > 0.105 ? 1 - 0.25 * k : 0); }); } }, 6.9);
  wires.forEach(({ w }) => { const b = w.getBBox(), d = Math.hypot(b.x + b.width / 2 - 924, b.y + b.height / 2 - 654);
    tl.to(w, { attr: { stroke: "#f85149" }, duration: 0.3 }, 7.0 + d / 1100 * 2.6); });
  K.look(tl, 7.9, 2.9, 1180, 470, 1.0, "sine.inOut");
  K.label(tl, 8.6, 11.0, "ALIVE AGAIN", 120, 860).classList.add("red");

  // ---- 11.62 the pole transformer works in reverse: cutaway ----
  K.look(tl, 11.0, 0.8, 1475, 560, 2.2, "power2.in");
  const tx = el("g", { id: "tx", "clip-path": "url(#txWipe)" }, svg);
  const cp = el("clipPath", { id: "txWipe" }, svg.querySelector("defs")); const wc = el("circle", { cx: 960, cy: 540, r: 0 }, cp);
  el("rect", { width: 1920, height: 1080, fill: "#0d1117" }, tx);
  for (let x = 0; x <= 1920; x += 48) el("line", { x1: x + 0.5, y1: 0, x2: x + 0.1, y2: 1080, stroke: x % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": x % 240 ? 1 : 2 }, tx);
  for (let y = 0; y <= 1080; y += 48) el("line", { x1: 0, y1: y + 0.5, x2: 1920, y2: y + 0.1, stroke: y % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": y % 240 ? 1 : 2 }, tx);
  const tc = el("g", { id: "txCam" }, tx);
  el("text", { x: 1250, y: 160, "text-anchor": "middle", class: "x-title" }, tc).textContent = "INSIDE THE POLE TRANSFORMER";
  // steel core: two limbs and yokes (laminations hinted)
  el("path", { d: "M 660 300 H 1260 V 860 H 660 Z M 740 380 V 780 H 1180 V 380 Z", fill: "#4B5563", "fill-rule": "evenodd", stroke: "#6B7280", "stroke-width": 3 }, tc);
  for (let k = 1; k < 4; k++) el("path", { d: `M ${660 + k * 20} ${300 + k * 20} H ${1260 - k * 20} V ${860 - k * 20} H ${660 + k * 20} Z`, fill: "none", stroke: "#3B4350", "stroke-width": 2 }, tc);
  const flux = el("path", { id: "flux", d: "M 700 340 H 1220 V 820 H 700 Z", fill: "none", stroke: "#9CC8FF", "stroke-width": 5, "stroke-dasharray": "22 18", opacity: 0 }, tc);
  // house side: few thick turns (left limb); line side: many thin turns (right limb)
  const lt = el("g", { id: "ltCoil" }, tc);
  for (let k = 0; k < 4; k++) el("rect", { x: 630, y: 470 + k * 56, width: 140, height: 30, rx: 12, fill: "#B87333", stroke: "#7A4A1E", "stroke-width": 3 }, lt);
  el("path", { d: "M 240 520 H 630 M 240 640 H 630", stroke: "#B87333", "stroke-width": 9, fill: "none" }, lt);
  const ht = el("g", { id: "htCoil" }, tc);
  for (let k = 0; k < 24; k++) el("rect", { x: 1160, y: 400 + k * 15.5, width: 130, height: 8, rx: 4, fill: "#B87333", stroke: "#7A4A1E", "stroke-width": 1.5 }, ht);
  el("path", { d: "M 1290 420 H 1680 M 1290 760 H 1680", stroke: "#B87333", "stroke-width": 4, fill: "none" }, ht);
  el("text", { x: 430, y: 470, "text-anchor": "middle", class: "x-lab" }, tc).textContent = "FEW TURNS";
  el("text", { x: 1490, y: 380, "text-anchor": "middle", class: "x-lab" }, tc).textContent = "MANY TURNS";
  el("text", { x: 430, y: 740, "text-anchor": "middle", class: "x-tag" }, tc).textContent = "HOUSE SIDE";
  el("text", { x: 1490, y: 830, "text-anchor": "middle", class: "x-tag" }, tc).textContent = "11 kV LINE";
  // direction arrows: normal (line → house, cyan) then reversed (house → line, red)
  const arN = el("path", { id: "arN", d: "M 1600 960 H 320 l 30 -22 M 320 960 l 30 22", stroke: "#58a6ff", "stroke-width": 8, fill: "none", "stroke-linecap": "round", opacity: 0 }, tc);
  const arR = el("path", { id: "arR", d: "M 320 960 H 1600 l -30 -22 M 1600 960 l -30 22", stroke: "#f85149", "stroke-width": 8, fill: "none", "stroke-linecap": "round", opacity: 0 }, tc);
  // the energy: dots in along the house-side wires, out (many, faster) on the line side
  const inD = [0, 1, 2, 3, 4].map(k => el("circle", { r: 9, fill: "#F2C14E", opacity: 0 }, tc));
  const outD = [...Array(10)].map(() => el("circle", { r: 6, fill: "#f85149", opacity: 0 }, tc));
  tl.set("#tx", { visibility: "hidden" }, 0).set("#tx", { visibility: "visible" }, 11.6);
  tl.fromTo(wc, { attr: { r: 0 } }, { attr: { r: 1150 }, duration: 0.5, ease: "power2.in", immediateRender: false }, 11.65);
  tl.to("#stage", { filter: "saturate(1) brightness(1)", duration: 0.2 }, 12.0);          // cutaway in full colour (WHAT IF frame stays)
  tl.set("#world", { visibility: "hidden" }, 12.2).set("#fg", { visibility: "hidden" }, 12.2);
  tl.fromTo("#txCam", { scale: 1.06, svgOrigin: "960 580" }, { scale: 1.0, duration: 8.0, ease: "sine.out", immediateRender: false }, 11.65);
  tl.to(arN, { opacity: 1, duration: 0.3 }, 12.4).to(arN, { opacity: 0, duration: 0.3 }, 13.4);
  K.label(tl, 12.5, 13.5, "NORMALLY", 120, 860);
  tl.to(arR, { opacity: 1, duration: 0.3 }, 13.6);
  K.label(tl, 13.7, 16.6, "IN REVERSE", 120, 860).classList.add("red");
  // 14.52 "Your two hundred and thirty volts…": energy comes in on the house side, the thick turns warm up
  const ep = { T: 0 };
  tl.fromTo(ep, { T: 0 }, { T: 6, duration: 6, ease: "none", immediateRender: false, onUpdate: () => {
    const T = ep.T;
    inD.forEach((c, k) => { const u = ((T * 0.9 + k * 0.2) % 1); c.setAttribute("cx", 240 + u * 390); c.setAttribute("cy", k % 2 ? 640 : 520); c.setAttribute("opacity", T > 0.05 ? 1 : 0); });
    outD.forEach((c, k) => { const u = ((T * 1.6 + k * 0.1) % 1), on = T > 2.3; c.setAttribute("cx", 1290 + u * 390); c.setAttribute("cy", k % 2 ? 760 : 420); c.setAttribute("opacity", on ? 1 : 0); });
  } }, 14.5);
  tl.to("#ltCoil rect", { attr: { fill: "#E59866" }, duration: 0.4 }, 14.6);
  K.hudShow(tl, 14.6, "line");
  K.label(tl, 14.6, 18.7, "230 V", 330, 330).classList.add("amber");
  tl.to(flux, { opacity: 1, duration: 0.3 }, 15.2).fromTo(flux, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -400 }, duration: 4.8, ease: "none", immediateRender: false }, 15.2);
  // 16.77 "becomes about eleven thousand volts…": the many thin turns glow red; HUD rolls up, settles on "≈ 11,000 V"
  tl.to("#htCoil rect", { attr: { fill: "#f85149", stroke: "#FFB4A8" }, duration: 0.5, stagger: 0.02 }, 16.8);
  const rv = { v: 230 }, hv = document.getElementById("h_line");
  tl.fromTo(rv, { v: 230 }, { v: 10400, duration: 1.4, ease: "power2.in", immediateRender: false, onUpdate: () => { hv.textContent = Math.round(rv.v / 10) * 10 + " V"; } }, 16.8);
  K.hudSet(tl, 18.25, "line", "≈ 11,000 V", "red");
  K.label(tl, 17.0, 18.7, "≈ 11,000 V", 1340, 860).classList.add("red");

  // ---- 20.09 "On a wire the lineman thinks is switched off": the 11 kV line upstream; the red creeps; freeze ----
  tl.to(wc, { attr: { r: 0 }, duration: 0.45, ease: "power2.out" }, 18.8);
  tl.set("#world", { visibility: "visible" }, 18.79).set("#fg", { visibility: "visible" }, 18.79);
  tl.to("#stage", { filter: "saturate(0.6) brightness(0.92)", duration: 0.2 }, 18.85);
  const pole = el("g", { id: "htPole" }, world);
  el("polygon", { points: "1679,880 1701,880 1697,232 1683,232", fill: "#B9B4A8" }, pole);
  el("rect", { x: 1640, y: 232, width: 100, height: 10, fill: "#8B8F94" }, pole);
  W36.lineman(world, 1690, 402, 1.0, "lmB");                               // gloves just below the wire: reaching, not touching
  wires.slice(0, 3).forEach(({ w }) => tl.set(w, { attr: { stroke: "#9aa0a6" } }, 18.79));  // 11 kV back to dead slate; only the creep is red
  tl.set("#brk", { visibility: "hidden" }, 18.79).set("#dholBadge", { opacity: 0 }, 18.79);
  tl.set("#htPole, #lmB", { visibility: "hidden" }, 0).set("#htPole, #lmB", { visibility: "visible" }, 18.79);
  const creep = el("path", { d: "M 1402 191 Q 1560 250 1682 238", fill: "none", stroke: "#f85149", "stroke-width": 7, "stroke-linecap": "round", opacity: 0.95 }, world);
  const cl = creep.getTotalLength();
  tl.set(creep, { attr: { "stroke-dasharray": `${cl} ${cl}`, "stroke-dashoffset": cl } }, 0);
  K.cam(tl, 18.79, 1560, 330, 2.3);
  tl.to(creep, { attr: { "stroke-dashoffset": cl * 0.1 }, duration: 2.6, ease: "power1.inOut" }, 19.1);    // stops short of his gloves
  K.label(tl, 19.2, D, "THINKS IT'S OFF", 120, 860).classList.add("red");
  // freeze before contact: everything holds, a slow push keeps the frame alive
  K.look(tl, 22.0, D - 22.0, 1610, 300, 2.45, "none");
  tl.to("#stage", { filter: "saturate(0.5) brightness(0.82)", duration: 0.15 }, 22.0);
};
