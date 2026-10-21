// S03 · D.C. and A.C. (0:34.1–0:51.3). Lines 5–6. Push into the box (X-ray). Panels: amber charges stream one way,
// a flat trace. House: not the air conditioner (it shakes off), the wall socket. A.C.: charges jiggle in place, a sine,
// fifty swings in a one-second ring (slowed down). Then the whole box: D.C. in on the left, A.C. out on the right.
// Cues (local s): "Your panels give D.C." 0.24 · "one way" 2.23 · "Your house runs on A.C." 4.05 · "not the air
// conditioner" 5.19 · "wall-socket kind" 6.21 · "swings forward and back" 7.38 · "fifty full swings" 8.86 ·
// "The solar box turns…" 10.70 · "…wall-socket power" 13.21.
window.SCENE = function (tl0, ctx) {
  const { D } = ctx, el = W36.el;
  // cue times below are the first estimates; the warp moves them onto the measured phrase starts (2026-10-21)
  const tl = K.warp(tl0, [4.0, 5.19, 6.21, 7.38, 8.86, 10.70, 13.21, D], [4.0, 6.03, 7.56, 8.65, 10.32, 13.02, 14.53, D]);
  const svg = document.getElementById("stage");
  W36.lane(svg); W36.xray(svg);
  K.hud([{ k: "grid", label: "GRID", v: "230 V · 50.0 Hz", cls: "cyan" }, { k: "box", label: "SOLAR BOX", v: "IN STEP ✓", cls: "green" }]);
  tl.set("#slowTag", { opacity: 0 }, 0).set("#scope", { opacity: 0 }, 0);
  K.gridLive(tl, 0);
  const xcamAt = (cx, cy, s) => ({ scale: s, x: 960 - s * cx, y: 540 - s * cy, svgOrigin: "0 0" });
  const xlook = (t, dur, cx, cy, s, ease) => tl.to("#xcam", { scale: s, x: 960 - s * cx, y: 540 - s * cy, duration: dur, ease: ease || "power2.inOut" }, t);

  // 0:00 from S02's framing on the box, push through the case into the X-ray
  K.cam(tl, 0, 924, 654, 2.48);
  tl.set("#xcam", xcamAt(540, 620, 1.5), 0);
  K.pushIn(tl, 0.05);
  // stage the inside: everything dim, then light what the VO names
  tl.set("#xInner", { opacity: 1 }, 0).set(".b1, #xInner > line, #xInner > rect, .swg, #relay, #acPulses, #xInner > circle, #brain, #sense, #ctlRelay, #ctlBridge", { opacity: 0.12 }, 0);
  tl.to(".b1, #xInner > line:nth-of-type(1), .dcdot", { opacity: 1, duration: 0.3 }, 0.9);
  K.tag(tl, 1.0, D, "ILLUSTRATION · SLOWED DOWN");
  // the running machine: D.C. charges march one way; A.C. charges jiggle at the (slowed) beat
  K.xRun(tl, 0, D, () => ({ grid: true, open: 0, driftInt: 0, lockOff: 0, dc: true }));

  // trace panel (fixed, top right): flat amber for D.C., cyan sine for A.C.
  const tr = el("g", { id: "trace", opacity: 0 }, document.getElementById("xray"));
  el("rect", { x: 1330, y: 230, width: 540, height: 205, rx: 14, fill: "#161b22", stroke: "#30363d", "stroke-width": 2 }, tr);
  const tt = W36.el("text", { x: 1352, y: 274, class: "x-tag", fill: "#F2C14E" }, tr); tt.textContent = "D.C. · ONE WAY";
  const tp = el("path", { fill: "none", stroke: "#F2C14E", "stroke-width": 5, "stroke-linecap": "round" }, tr);
  el("line", { x1: 1350, y1: 360, x2: 1850, y2: 360.2, stroke: "#30363d", "stroke-width": 2 }, tr);              // zero line
  const pr = { T: 0 };
  tl.fromTo(pr, { T: 0 }, { T: D, duration: D, ease: "none", immediateRender: false, onUpdate: () => {
    const ac = pr.T >= tl.W(7.3);
    tp.setAttribute("d", ac ? W36.sinePath(1350, 1850, 360, 56, 3, -2 * Math.PI * pr.T / K.BEAT) : "M 1350 318 L 1850 318");
    tp.setAttribute("stroke", ac ? "#58a6ff" : "#F2C14E");
    tt.textContent = ac ? "A.C. · FORWARD AND BACK" : "D.C. · ONE WAY"; tt.setAttribute("fill", ac ? "#58a6ff" : "#F2C14E");
  } }, 0);
  tl.to("#trace", { opacity: 1, duration: 0.3 }, 1.3).to("#trace", { opacity: 0, duration: 0.25 }, 3.9)
    .to("#trace", { opacity: 1, duration: 0.3 }, 7.38).to("#trace", { opacity: 0, duration: 0.3 }, 10.4);
  K.label(tl, 2.2, 3.9, "ONE WAY", 120, 860).classList.add("amber");

  // 4.05 "Your house runs on A.C. power": over to the house socket; 5.19 "not the air conditioner" — a split A.C. unit
  // sits over the socket, shakes no and slides off; 6.21 "the wall-socket kind" — the socket glows
  xlook(4.0, 0.9, 1430, 760, 1.7);
  tl.to("#acPulses, #xInner > circle, #xInner > line", { opacity: 1, duration: 0.3 }, 4.1);
  const acu = el("g", { id: "acUnit", opacity: 0 }, document.getElementById("xInner"));
  el("rect", { x: 1290, y: 800, width: 300, height: 104, rx: 22, fill: "#F4F6F7", stroke: "#AEB6BF", "stroke-width": 4 }, acu);
  el("rect", { x: 1310, y: 874, width: 260, height: 12, rx: 6, fill: "#C8CED3" }, acu);
  el("circle", { cx: 1560, cy: 828, r: 6, fill: "#3fb950" }, acu);
  const xx = el("g", { id: "acX", opacity: 0 }, acu);
  el("path", { d: "M 1300 790 L 1580 914 M 1580 790 L 1300 914", stroke: "#f85149", "stroke-width": 14, "stroke-linecap": "round" }, xx);
  tl.fromTo("#acUnit", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, 5.1);
  tl.set("#acX", { opacity: 1 }, 5.55);
  [0, 1, 2].forEach(k => tl.to("#acUnit", { rotation: k % 2 ? 4 : -4, svgOrigin: "1440 852", duration: 0.09 }, 5.55 + k * 0.1));
  tl.to("#acUnit", { rotation: 0, duration: 0.08 }, 5.85).to("#acUnit", { x: 700, opacity: 0, duration: 0.4, ease: "power2.in" }, 5.95);
  const glow = el("circle", { id: "skGlow", cx: 1452, cy: 857, r: 90, fill: "none", stroke: "#58a6ff", "stroke-width": 6, opacity: 0 }, document.getElementById("xInner"));
  tl.fromTo(glow, { opacity: 0.9, attr: { r: 70 } }, { opacity: 0, attr: { r: 150 }, duration: 0.8, ease: "power2.out", immediateRender: false }, 6.25);
  K.label(tl, 6.3, 7.25, "WALL SOCKET", 120, 860);

  // 7.38 "It swings forward and back": the wire to the house, charges jiggle in place; 8.86 "fifty full swings every second"
  xlook(7.25, 0.9, 1400, 520, 1.25);     // keeps the grid badge clear of the trace panel
  tl.to("#xcam .x-title", { opacity: 0, duration: 0.3 }, 7.2).to("#xcam .x-title", { opacity: 1, duration: 0.3 }, 10.6).to("#xcam .x-title", { opacity: 0, duration: 0.4 }, 13.4); // clear of the HUD when zoomed
  const ring = el("g", { id: "secRing", opacity: 0 }, document.getElementById("xInner"));
  el("circle", { cx: 1330, cy: 470, r: 56, fill: "#0d1117", stroke: "#30363d", "stroke-width": 8 }, ring);
  const arc = el("circle", { cx: 1330, cy: 470, r: 56, fill: "none", stroke: "#58a6ff", "stroke-width": 8, "stroke-dasharray": 352, "stroke-dashoffset": 352, transform: "rotate(-90 1330 470)" }, ring);
  const num = el("text", { x: 1330, y: 486, "text-anchor": "middle", fill: "#E6EDF3", "font-family": "Inter", "font-weight": 800, "font-size": 44 }, ring); num.textContent = "1";
  const cnt = { n: 1 };
  tl.to("#secRing", { opacity: 1, duration: 0.25 }, 8.7);
  tl.fromTo(arc, { attr: { "stroke-dashoffset": 352 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.0, ease: "none", immediateRender: false }, 8.9);
  tl.fromTo(cnt, { n: 1 }, { n: 50, duration: 1.0, ease: "none", immediateRender: false, onUpdate: () => { num.textContent = Math.round(cnt.n); } }, 8.9);
  K.label(tl, 9.0, 10.5, "50 PER SECOND", 120, 860);
  tl.fromTo("#secRing", { scale: 1, svgOrigin: "1330 470" }, { scale: 1.12, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, 9.9);
  tl.to("#secRing", { opacity: 0, duration: 0.3 }, 10.5);

  // 10.70 "The solar box turns panel power into wall-socket power": the whole box; the converter lights
  xlook(10.45, 1.0, 960, 560, 1.0);
  tl.to("#xInner > rect, .swg, #xInner > line", { opacity: 1, duration: 0.35 }, 10.9).to("#relay", { opacity: 1, duration: 0.3 }, 11.3);
  K.label(tl, 11.0, D - 0.2, "D.C. → A.C.", 120, 860);
  // 13.21 "…wall-socket power": push in on the converter, its four switches flicking
  xlook(13.1, 3.6, 820, 600, 1.35, "sine.inOut");
  tl.fromTo("#xInner > rect", { attr: { stroke: "#c9d1d9" } }, { attr: { stroke: "#58a6ff" }, duration: 0.3, yoyo: true, repeat: 1, immediateRender: false }, 13.3);
};
