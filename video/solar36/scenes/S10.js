// S10 · The rule, say no, the drummer, the bridge (2:59.5–3:33.7). Lines 21–24 + 6 s end-screen tail.
// Rule: a plain on-grid box (no battery) goes silent when the grid goes, by design (shield). Ruin: if anyone offers to
// switch the safety off, say no (a raised palm stops the toggle); the lineman on your street is the one at risk.
// Reality: your solar never failed, it lost its drummer (the dhol fades, the sun badge bows). Bridge: push into the box,
// the converter glimpse → end screen under live VO: next film zone (the H-bridge teaser), subscribe zone, logo sting.
// Cues (local s): "Remember this" 0.29 · "on-grid solar box, no battery" 1.39 · "by design" 6.92 · "switch off this
// safety" 9.00 · "just say no" 11.63 · "the lineman fixing your street" 13.51 · "Your solar never failed" 17.84 ·
// "lost its drummer" 19.55 · bridge 21.29 · "Let's open it up next" 26.86 · VO ends 27.97.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg); document.getElementById("xray").setAttribute("opacity", 1);
  const world = L.world;
  const lm = W36.lineman(world, 1240, 760, 1.25, "lmA");
  K.hud([{ k: "grid", label: "GRID", v: "OFF", cls: "" }, { k: "box", label: "SOLAR BOX", v: "OFF", cls: "red" }]);
  K.gridDead(tl, 0);
  tl.set("#slowTag", { opacity: 0 }, 0).set("#boxLed", { attr: { fill: "#f85149" } }, 0);
  tl.set("#meter text, #meter > rect:nth-of-type(4)", { visibility: "hidden" }, 0);   // the labels sit where the meter tag would be
  tl.set("#badge circle:nth-of-type(2), #badge circle:nth-of-type(3)", { attr: { r: 0.8 } }, 0);     // eyes closed: tripped
  K.tag(tl, 0, 22.9, "ILLUSTRATION");

  // ================= Rule (0–8.9): no battery → silent when the grid goes, by design =================
  K.cam(tl, 0, 930, 650, 2.0);
  K.look(tl, 0.2, 8.6, 950, 630, 2.6, "sine.inOut");
  const sh = el("g", { id: "shield", opacity: 0 }, world);
  el("path", { d: "M 1010 548 L 1046 562 L 1046 594 Q 1046 620 1010 636 Q 974 620 974 594 L 974 562 Z", fill: "#0d1117", stroke: "#3fb950", "stroke-width": 5 }, sh);
  el("path", { d: "M 992 592 L 1006 606 L 1030 578", fill: "none", stroke: "#3fb950", "stroke-width": 6, "stroke-linecap": "round", "stroke-linejoin": "round" }, sh);
  tl.fromTo("#shield", { opacity: 0, scale: 0.6, svgOrigin: "1010 592" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }, 1.4);
  K.label(tl, 1.5, 4.2, "NO BATTERY", 120, 860).classList.add("amber");
  K.label(tl, 4.3, 6.8, "GOES SILENT", 120, 860);
  K.label(tl, 6.95, 8.9, "BY DESIGN", 120, 860).classList.add("green");
  K.hudSet(tl, 6.95, "box", "OFF · BY DESIGN", "green");

  // ================= Ruin (9.0–17.8): say no; the lineman is the one at risk =================
  const ov = el("g", { id: "tgl", opacity: 0 }, svg);
  el("rect", { x: 820, y: 385, width: 360, height: 170, rx: 85, fill: "#161b22", stroke: "#3fb950", "stroke-width": 6 }, ov);
  const knob = el("circle", { id: "knob", cx: 1095, cy: 470, r: 66, fill: "#3fb950" }, ov);
  el("text", { x: 1000, y: 610, "text-anchor": "middle", class: "x-tag" }, ov).textContent = "SAFETY ON";
  // a finger reaching for the toggle from the right
  const fin = el("g", { id: "finger", visibility: "hidden" }, ov);   // dropped after review v1 (read as a render bug)
  el("rect", { x: 1180, y: 446, width: 500, height: 48, rx: 24, fill: "#8D5524" }, fin);
  el("rect", { x: 1400, y: 424, width: 560, height: 92, rx: 30, fill: "#2E86C1" }, fin);
  // the raised palm that stops it
  const palm = el("g", { id: "palm", opacity: 0 }, el("g", { transform: "translate(330 0)" }, svg));
  el("rect", { x: 830, y: 520, width: 230, height: 250, rx: 70, fill: "#A0522D" }, palm);
  [[842, 360, 44, 200], [896, 330, 46, 220], [952, 340, 46, 210], [1006, 372, 42, 180]].forEach(([x, y, w, h]) => el("rect", { x, y, width: w, height: h, rx: 22, fill: "#A0522D" }, palm));
  el("rect", { x: 1040, y: 560, width: 120, height: 46, rx: 23, fill: "#A0522D", transform: "rotate(-35 1050 583)" }, palm);
  el("rect", { x: 850, y: 740, width: 190, height: 260, rx: 20, fill: "#2E86C1" }, palm);
  const ring = el("circle", { cx: 1275, cy: 560, r: 60, fill: "none", stroke: "#f85149", "stroke-width": 10, opacity: 0 }, svg);
  tl.to("#tgl", { opacity: 1, duration: 0.3 }, 9.1);
  tl.to("#world", { filter: "brightness(0.45)", duration: 0.4 }, 9.1);
  tl.fromTo("#palm", { opacity: 0, y: 220 }, { opacity: 1, y: 0, duration: 0.28, ease: "back.out(1.8)", immediateRender: false }, 11.6);
  tl.fromTo(ring, { opacity: 1, attr: { r: 60 } }, { opacity: 0, attr: { r: 420 }, duration: 0.6, ease: "power2.out", immediateRender: false }, 11.75);
  tl.fromTo("#palm", { scale: 1, svgOrigin: "945 640" }, { scale: 1.04, duration: 1.6, ease: "sine.inOut", immediateRender: false }, 11.9);
  K.label(tl, 11.7, 13.35, "SAY NO", 120, 860).classList.add("red");
  tl.to("#tgl, #palm", { opacity: 0, duration: 0.3 }, 13.3).to("#world", { filter: "brightness(1)", duration: 0.3 }, 13.3);
  // 13.51 the lineman fixing your street: respectful low angle, calm work
  K.look(tl, 13.2, 0.8, 1230, 600, 2.4, "power2.inOut", 1060, 520);
  tl.fromTo("#lmA", { y: 18 }, { y: 0, duration: 3.6, ease: "sine.inOut", immediateRender: false }, 13.5);
  K.look(tl, 14.0, 3.6, 1235, 590, 2.6, "none", 1060, 520);
  K.label(tl, 14.0, 17.4, "HIS SAFETY", 120, 860).classList.add("green");

  // ================= Reality (17.84–21.2): never failed, it lost its drummer =================
  K.look(tl, 17.5, 1.2, 1000, 520, 1.05, "power2.inOut");
  tl.to("#stage", { filter: "sepia(0.25) saturate(1.1) brightness(1.03)", duration: 1.0 }, 17.6);
  tl.to("#dholBadge", { opacity: 0, duration: 1.2, ease: "sine.in" }, 19.6);
  tl.to("#badge", { rotation: 18, svgOrigin: "0 10", duration: 0.5, ease: "sine.inOut" }, 19.8).to("#badge", { rotation: 0, duration: 0.6, ease: "sine.inOut" }, 20.5);

  // ================= Bridge (21.29–): into the box → end screen under live VO =================
  tl.to("#shield", { opacity: 0, duration: 0.2 }, 20.9);
  K.look(tl, 21.1, 0.6, 924, 654, 2.6, "power2.in");
  tl.to("#stage", { filter: "none", duration: 0.3 }, 21.2);
  K.pushIn(tl, 21.6);
  tl.set("#xInner", { opacity: 1 }, 0).set("#xray .x-title", { opacity: 1 }, 0).set("#scope", { opacity: 0 }, 0);
  tl.set(".b1, #xInner > line, #relay, #acPulses, #xInner > circle, #brain, #sense, #ctlRelay, #ctlBridge", { opacity: 0.12 }, 0);
  tl.fromTo("#xInner > rect, .swg", { opacity: 0.12 }, { opacity: 1, duration: 0.3, immediateRender: false }, 22.4);
  tl.to("#xcam", { scale: 1.6, x: 960 - 1.6 * 845, y: 540 - 1.6 * 620, duration: 1.0, ease: "power2.inOut" }, 22.1);
  // the end screen
  const es = el("g", { id: "endS", "clip-path": "url(#esWipe)" }, svg);
  const cp = el("clipPath", { id: "esWipe" }, svg.querySelector("defs")); const wc = el("circle", { cx: 960, cy: 540, r: 0 }, cp);
  el("rect", { width: 1920, height: 1080, fill: "#0d1117" }, es);
  for (let x = 0; x <= 1920; x += 48) el("line", { x1: x + 0.5, y1: 0, x2: x + 0.1, y2: 1080, stroke: x % 240 ? "#1a2330" : "#243246", "stroke-width": x % 240 ? 1 : 2 }, es);
  for (let y = 0; y <= 1080; y += 48) el("line", { x1: 0, y1: y + 0.5, x2: 1920, y2: y + 0.1, stroke: y % 240 ? "#1a2330" : "#243246", "stroke-width": y % 240 ? 1 : 2 }, es);
  // next-film zone (16:9) with the H-bridge teaser running inside
  el("text", { x: 160, y: 250, class: "x-tag", fill: "#58a6ff" }, es).textContent = "NEXT FILM";
  el("text", { x: 160, y: 300, class: "x-title" }, es).textContent = "HOW THE BOX MAKES A.C.";
  el("rect", { x: 160, y: 330, width: 864, height: 486, rx: 18, fill: "#161b22", stroke: "#58a6ff", "stroke-width": 4 }, es);
  const sws = [[470, 470], [600, 470], [470, 600], [600, 600]].map(([x, y]) => {
    el("circle", { cx: x, cy: y + 30, r: 8, fill: "#C9D1D9" }, es); el("circle", { cx: x + 50, cy: y + 30, r: 8, fill: "#C9D1D9" }, es);
    return el("line", { x1: x, y1: y + 30, x2: x + 48, y2: y, stroke: "#58a6ff", "stroke-width": 7, "stroke-linecap": "round" }, es); });
  el("rect", { x: 430, y: 440, width: 280, height: 240, rx: 14, fill: "none", stroke: "#C9D1D9", "stroke-width": 3 }, es);
  el("line", { x1: 200, y1: 560, x2: 430, y2: 560.2, stroke: "#F2C14E", "stroke-width": 8 }, es);
  const out = el("path", { fill: "none", stroke: "#58a6ff", "stroke-width": 6 }, es);
  // subscribe zone + logo sting (the channel is named only here)
  const lg = el("g", { id: "logoS", opacity: 0 }, es);
  el("circle", { cx: 1460, cy: 520, r: 170, fill: "#0d1117", stroke: "#C9D1D9", "stroke-width": 6 }, lg);
  el("text", { x: 1460, y: 508, "text-anchor": "middle", fill: "#E6EDF3", "font-family": "Inter", "font-weight": 800, "font-size": 46 }, lg).textContent = "BE";
  el("text", { x: 1460, y: 562, "text-anchor": "middle", fill: "#E6EDF3", "font-family": "Inter", "font-weight": 800, "font-size": 46 }, lg).textContent = "PRACTICAL";
  el("text", { x: 1460, y: 780, "text-anchor": "middle", class: "x-title" }, lg).textContent = "BE PRACTICAL WITH KISHORE";
  const burst = el("circle", { cx: 1460, cy: 520, r: 170, fill: "none", stroke: "#58a6ff", "stroke-width": 8, opacity: 0 }, es);
  const ep = { T: 0 };
  tl.fromTo(ep, { T: 0 }, { T: D - 23, duration: D - 23, ease: "none", immediateRender: false, onUpdate: () => {
    const T = ep.T, half = Math.floor(T / 0.6) % 2;
    sws.forEach((w, k) => { const c = (k === 0 || k === 3) ? half === 0 : half === 1; w.setAttribute("y2", +w.getAttribute("y1") - (c ? 0 : 30)); });
    out.setAttribute("d", W36.sinePath(710, 990, 560, 70, 2, -2 * Math.PI * T / 1.2));
  } }, 23);
  tl.set("#endS", { visibility: "hidden" }, 0).set("#endS", { visibility: "visible" }, 22.95);
  tl.fromTo(wc, { attr: { r: 0 } }, { attr: { r: 1150 }, duration: 0.55, ease: "power2.in", immediateRender: false }, 23.0);
  tl.set("#hud", { opacity: 1 }, 0).to("#hud", { opacity: 0, duration: 0.3 }, 23.2);
  tl.set("#bug", { opacity: 1 }, 0).to("#bug", { opacity: 0, duration: 0.3 }, 27.8);
  // logo sting after the last word
  tl.fromTo("#logoS", { opacity: 0, scale: 0.7, svgOrigin: "1460 520" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)", immediateRender: false }, 28.05);
  tl.fromTo(burst, { opacity: 1, attr: { r: 170 } }, { opacity: 0, attr: { r: 330 }, duration: 0.8, ease: "power2.out", immediateRender: false }, 28.1);
  tl.fromTo("#logoS", { scale: 1 }, { scale: 1.03, duration: D - 28.6, ease: "sine.inOut", immediateRender: false }, 28.6);
};
