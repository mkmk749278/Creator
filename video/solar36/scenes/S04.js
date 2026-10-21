// S04 · Drummer and dancer (0:51.3–1:13.9). Lines 7–8. In the X-ray the box tries to draw its own wave and fails,
// then listens to the street wire. Pull out: the grid is the drummer (dhol on the transformer, a ring down the wire per
// beat), the box the dancer (its sun badge hops on each beat). A normal day: traces in step; the house uses what it
// needs; the extra goes out through the meter, along the street wire, up to the transformer.
// Cues (local s): "can't make that rhythm" 1.73 · "Think of the grid as a drummer" 5.56 · "the solar box as a dancer"
// 7.81 · "On a normal day" 11.64 · "Your house uses" 14.43 · "out through your meter" 16.37 · "street wire" 18.53 ·
// "up to the transformer" 19.91.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg);
  K.hud([{ k: "grid", label: "GRID", v: "230 V · 50.0 Hz", cls: "cyan" }, { k: "box", label: "SOLAR BOX", v: "IN STEP ✓", cls: "green" }]);
  K.gridLive(tl, 0);
  tl.set("#slowTag", { opacity: 0 }, 0);
  K.tag(tl, 0, D, "ILLUSTRATION · SLOWED DOWN");

  // ---- 0:00 X-ray, held from S03's framing on the converter ----
  tl.set("#xWipeC", { attr: { r: 1150 } }, 0).set("#world", { visibility: "hidden" }, 0).set("#fg", { visibility: "hidden" }, 0);
  tl.set("#xcam", { scale: 1.35, x: 960 - 1.35 * 820, y: 540 - 1.35 * 600, svgOrigin: "0 0" }, 0);
  tl.set("#xInner", { opacity: 1 }, 0).set("#brain, #sense, #ctlRelay, #ctlBridge", { opacity: 0.12 }, 0);
  tl.set(".x-title", { opacity: 0 }, 0).set("#tGrid", { opacity: 0 }, 0).set("#inStep", { opacity: 0 }, 0);
  tl.to("#xcam", { scale: 1, x: 0, y: 0, duration: 1.4, ease: "power2.inOut" }, 0.6);
  // 1.73 "can't make that back-and-forth rhythm on its own": its own wave stutters and collapses, twice
  const tB = document.getElementById("tBox");
  const fp = { T: 0 };
  tl.fromTo(fp, { T: 0 }, { T: 3.4, duration: 3.4, ease: "none", immediateRender: false, onUpdate: () => {
    const T = fp.T, k = (T % 1.7) / 1.7;                                   // two tries, 1.7 s each
    const amp = 52 * Math.sin(Math.PI * Math.min(1, k * 1.6)) * (k < 0.62 ? 1 : 0);
    const jit = Math.sin(T * 37) * 0.6 + Math.sin(T * 23) * 0.4;           // deterministic stutter
    tB.setAttribute("d", amp > 1 ? W36.sinePath(1350, 1350 + 500 * Math.min(1, k * 1.8), 350, amp * (0.7 + 0.3 * jit), 3, T * 4) : "M 1350 350 L 1850 350");
    tB.setAttribute("stroke", k < 0.62 ? "rgba(255,255,255,0.42)" : "rgba(248,81,73,0.6)");
  } }, 1.75);
  tl.set(tB, { attr: { d: "M 1350 350 L 1850 350" } }, 0);
  K.label(tl, 2.0, 3.9, "NO RHYTHM", 120, 860).classList.add("red");
  // 3.9 it listens to the street wire: the eye lights, the sensing line runs from the grid side
  tl.to("#brain, #sense", { opacity: 1, duration: 0.3 }, 3.9);
  tl.fromTo("#sense", { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -110 }, duration: 1.2, ease: "none", immediateRender: false }, 3.9);
  tl.fromTo("#pupil", { attr: { cx: 980 } }, { attr: { cx: 992 }, duration: 0.3, immediateRender: false }, 4.0);
  K.label(tl, 4.1, 5.0, "LISTENS", 120, 860);

  // ---- 5.0 pull out to the street: drummer and dancer ----
  K.pullOut(tl, 5.0);
  K.look(tl, 5.9, 1.3, 1080, 430, 1.25, "power2.inOut");
  K.beats(tl, L, 6.0, 16.2);
  K.beats(tl, L, 16.2, D, { noTravel: true });                             // export scene: keep the drum and the dance, no rings
  K.label(tl, 5.9, 11.3, "DRUMMER", 1240, 330).classList.add("amber");
  K.label(tl, 7.9, 11.3, "DANCER", 690, 640).classList.add("green");

  // ---- 11.64 "On a normal day, it follows every beat": the two traces lie on top of each other ----
  const sc = el("g", { id: "nScope", opacity: 0 }, svg);
  el("rect", { x: 1330, y: 230, width: 540, height: 205, rx: 14, fill: "#161b22", stroke: "#30363d", "stroke-width": 2 }, sc);
  el("rect", { x: 1352, y: 250, width: 22, height: 22, fill: "#58a6ff" }, sc); el("text", { x: 1384, y: 272, class: "x-tag cyan" }, sc).textContent = "GRID";
  el("rect", { x: 1500, y: 250, width: 22, height: 22, fill: "rgba(255,255,255,0.7)" }, sc); el("text", { x: 1532, y: 272, class: "x-tag" }, sc).textContent = "BOX";
  el("text", { x: 1846, y: 272, class: "x-tag green", "text-anchor": "end" }, sc).textContent = "IN STEP ✓";
  const nb = el("path", { fill: "none", stroke: "rgba(255,255,255,0.42)", "stroke-width": 12, "stroke-linecap": "round" }, sc);
  const ng = el("path", { fill: "none", stroke: "#58a6ff", "stroke-width": 4 }, sc);
  const sp = { T: 0 };
  tl.fromTo(sp, { T: 11.4 }, { T: 14.6, duration: 3.2, ease: "none", immediateRender: false, onUpdate: () => {
    const d = W36.sinePath(1350, 1850, 350, 52, 3, -2 * Math.PI * sp.T / K.BEAT); nb.setAttribute("d", d); ng.setAttribute("d", d); } }, 11.4);
  tl.to("#nScope", { opacity: 1, duration: 0.3 }, 11.5).to("#nScope", { opacity: 0, duration: 0.3 }, 14.3);
  K.look(tl, 11.3, 1.2, 1050, 470, 1.3, "power2.inOut");
  tl.fromTo("#box", { filter: "drop-shadow(0 0 0px #3fb950)" }, { filter: "drop-shadow(0 0 14px #3fb950)", duration: 0.4, immediateRender: false }, 11.8)
    .to("#box", { filter: "drop-shadow(0 0 0px #3fb950)", duration: 0.4 }, 14.2);

  // ---- 14.43 "Your house uses what it needs": fan, bulb and TV come alive in the windows, fed from the box ----
  K.look(tl, 14.1, 1.0, 800, 620, 1.7, "power2.inOut");
  const ap = el("g", { id: "appl", opacity: 0 }, L.world);
  const fan = el("g", { id: "fanI" }, ap);
  el("circle", { cx: 634, cy: 501, r: 6, fill: "#3E4A57" }, fan);
  [0, 120, 240].forEach(a => el("ellipse", { cx: 634, cy: 486, rx: 6, ry: 15, fill: "#3E4A57", transform: `rotate(${a} 634 501)` }, fan));
  el("circle", { cx: 784, cy: 492, r: 14, fill: "#FFE08A", stroke: "#B7950B", "stroke-width": 2, id: "bulbI" }, ap);
  el("rect", { x: 777, y: 506, width: 14, height: 10, fill: "#7F8C8D" }, ap);
  el("rect", { x: 906, y: 478, width: 56, height: 36, rx: 3, fill: "#1B2631", stroke: "#566573", "stroke-width": 3 }, ap);
  el("rect", { id: "tvI", x: 911, y: 483, width: 46, height: 26, fill: "#58a6ff", opacity: 0.8 }, ap);
  tl.to("#appl", { opacity: 1, duration: 0.3 }, 14.4);
  tl.fromTo("#fanI", { rotation: 0, svgOrigin: "634 501" }, { rotation: 900, duration: 1.9, ease: "power1.in", immediateRender: false }, 14.45);
  tl.fromTo("#bulbI", { attr: { fill: "#7F8C8D" } }, { attr: { fill: "#FFE08A" }, duration: 0.2, immediateRender: false }, 14.6);
  tl.fromTo("#tvI", { opacity: 0 }, { opacity: 0.85, duration: 0.2, immediateRender: false }, 14.8);
  const feed = [0, 1, 2].map(k => el("circle", { r: 7, fill: "#9CC8FF", opacity: 0 }, L.world));
  [[634, 0], [784, 0.2], [934, 0.4]].forEach(([wx, dl], k) => {               // a dot from the AC side of the box up into each window
    tl.fromTo(feed[k], { opacity: 1, attr: { cx: 1020, cy: 640 } }, { attr: { cx: wx, cy: 520 }, duration: 0.6, ease: "power1.inOut", immediateRender: false }, 14.45 + dl)
      .to(feed[k], { opacity: 0, duration: 0.1 }, 15.05 + dl);
  });
  K.label(tl, 14.6, 16.2, "HOUSE USES", 120, 860);

  // ---- 16.37 "The extra goes out through your meter… onto the street wire… and up to the transformer" (one move) ----
  const ring = L.ring, len = ring.getTotalLength();
  const ex = [0, 1, 2, 3].map(k => el("circle", { r: 12 - k * 2, fill: "#3fb950", stroke: "#FFFFFF", "stroke-width": k ? 0 : 4, opacity: 0 }, L.world));
  const xp = { u: 1 };
  tl.fromTo(xp, { u: 1 }, { u: 0.16, duration: 5.2, ease: "none", immediateRender: false, onUpdate: () => {   // backwards along the beat path
    ex.forEach((c, k) => { const q = Math.min(1, xp.u + 0.025 * k), p = ring.getPointAtLength(q * len);
      c.setAttribute("cx", p.x); c.setAttribute("cy", p.y); c.setAttribute("opacity", xp.u > 0.165 ? (1 - 0.2 * k).toFixed(2) : 0); });
  } }, 16.4);
  // the meter text sits under the foreground in the wide shots: show it only while the meter is framed
  tl.set("#meter text", { opacity: 0 }, 0).to("#meter text", { opacity: 1, duration: 0.3 }, 14.2).to("#meter text", { opacity: 0, duration: 0.3 }, 19.4);
  tl.to("#meterLed", { attr: { fill: "#3fb950" }, duration: 0.1 }, 16.4);
  K.look(tl, 16.1, 1.0, 780, 760, 2.0, "power2.inOut");
  K.look(tl, 17.2, 4.4, 1350, 470, 1.5, "sine.inOut");
  K.label(tl, 16.5, 18.4, "EXPORT", 120, 860).classList.add("green");
  K.label(tl, 18.6, 19.8, "STREET WIRE", 120, 860);
  K.label(tl, 20.0, D - 0.2, "TRANSFORMER", 1340, 590);
};
