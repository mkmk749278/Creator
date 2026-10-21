// S06 · The box notices (1:37.1–1:50.1). Line 12. Push into the box: the eye watches the grid through the sensing line,
// the scope shows both waves in step. The beat goes missing (grid trace flat), or the voltage drifts (needle leaves the
// green band): the brain fires the safety switch, click, white flash. The rule: off within two seconds (ring, limit tick).
// Cues (local s): "built to notice" 0.79 · "If the beat goes missing" 3.36 · "or the voltage starts changing" 4.77 ·
// "it switches itself off" 6.55 · "click" 8.39 · "Safety rules say … within two seconds" 9.10.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg);
  K.hud([{ k: "grid", label: "GRID", v: "0 V · —", cls: "" }, { k: "box", label: "SOLAR BOX", v: "WATCHING", cls: "cyan" },
         { k: "timer", label: "TRIP TIMER", v: "≤ 2 s LIMIT", cls: "amber", hidden: true }]);
  K.gridDead(tl, 0);
  tl.set("#slowTag", { opacity: 0 }, 0);
  K.tag(tl, 0, D, "ILLUSTRATION · SLOWED DOWN");

  // ---- 0:00 normal colour, on the box; push in ----
  K.cam(tl, 0, 924, 654, 2.2);
  K.look(tl, 0, 0.8, 924, 654, 2.5, "sine.in");
  K.pushIn(tl, 0.8);
  K.xBuild(tl, 1.6, 0.12);
  tl.set(".x-title", { opacity: 1 }, 0);
  const tBeat = 3.4, tClick = 8.4;
  K.xRun(tl, 0, D, T => ({ grid: T < tBeat, open: T < tClick ? 0 : Math.min(1, (T - tClick) / 0.08), driftInt: 0, lockOff: 0, dc: T < tClick }));
  tl.set("#inStep", { opacity: 0 }, 0).to("#inStep", { opacity: 1, duration: 0.2 }, 1.9).set("#inStep", { opacity: 0 }, tBeat);
  K.label(tl, 1.9, 3.3, "ALWAYS WATCHING", 120, 860);

  // ---- 3.36 the beat goes missing: the grid trace goes flat, the sensing line dims ----
  K.label(tl, tBeat + 0.1, 4.7, "BEAT MISSING", 120, 860).classList.add("red");
  // 4.77 or the voltage starts changing: a needle leaves the green band
  const gz = el("g", { id: "gauge", opacity: 0 }, document.getElementById("xInner"));
  const cx = 1310, cy = 500, R = 58;
  const arc = (a0, a1, col, w) => { const p = a => [cx + R * Math.cos(a), cy + R * Math.sin(a)];
    const [x0, y0] = p(a0), [x1, y1] = p(a1); el("path", { d: `M ${x0} ${y0} A ${R} ${R} 0 0 1 ${x1} ${y1}`, fill: "none", stroke: col, "stroke-width": w }, gz); };
  el("circle", { cx, cy, r: R + 16, fill: "#161b22", stroke: "#30363d", "stroke-width": 3 }, gz);
  arc(Math.PI * 1.1, Math.PI * 1.9, "#30363d", 12);
  arc(Math.PI * 1.38, Math.PI * 1.62, "#3fb950", 12);                                 // the allowed band
  const ndl = el("line", { id: "ndl", x1: cx, y1: cy, x2: cx, y2: cy - R + 6, stroke: "#E6EDF3", "stroke-width": 5, "stroke-linecap": "round" }, gz);
  el("circle", { cx, cy, r: 7, fill: "#E6EDF3" }, gz);
  el("text", { x: cx, y: cy + 40, "text-anchor": "middle", class: "x-tag" }, gz).textContent = "VOLTS";
  tl.to("#gauge", { opacity: 1, duration: 0.3 }, 4.7);
  tl.fromTo(ndl, { rotation: 0, svgOrigin: `${cx} ${cy}` }, { rotation: 52, duration: 1.3, ease: "power1.in", immediateRender: false }, 4.9);
  tl.to(ndl, { attr: { stroke: "#f85149" }, duration: 0.1 }, 5.7);
  K.label(tl, 4.9, 6.4, "VOLTAGE DRIFTS", 120, 860).classList.add("red");

  // ---- 6.55 "it switches itself off": the brain fires the switch; 8.39 click + white flash ----
  tl.to("#xcam", { scale: 1.45, x: 960 - 1.45 * 1110, y: 540 - 1.45 * 560, duration: 1.4, ease: "power2.inOut" }, 6.5);
  tl.to("#xcam .x-title", { opacity: 0, duration: 0.3 }, 6.4);                           // clear of the HUD when zoomed
  tl.to("#gauge", { opacity: 0, duration: 0.3 }, 8.9);
  tl.to("#ctlRelay", { attr: { stroke: "#FFFFFF" }, duration: 0.2 }, 6.8);
  tl.fromTo("#pupil", { attr: { r: 10 } }, { attr: { r: 15 }, duration: 0.25, yoyo: true, repeat: 1, immediateRender: false }, 6.6);
  const flash = el("circle", { cx: 1125, cy: 615, r: 20, fill: "none", stroke: "#FFFFFF", "stroke-width": 10, opacity: 0 }, document.getElementById("xInner"));
  tl.fromTo(flash, { opacity: 1, attr: { r: 20 } }, { opacity: 0, attr: { r: 190 }, duration: 0.45, ease: "power2.out", immediateRender: false }, tClick);
  tl.fromTo("#xray", { filter: "brightness(1.6)" }, { filter: "brightness(1)", duration: 0.25, immediateRender: false }, tClick);
  K.hudSet(tl, tClick, "box", "TRIPPED", "red");
  K.label(tl, tClick + 0.05, 9.9, "SWITCH OPENS", 120, 860).classList.add("red");

  // ---- 9.10 "Safety rules say it must switch off within two seconds": a 2 s ring around the switch ----
  tl.to("#xcam", { scale: 1.2, x: 960 - 1.2 * 1060, y: 540 - 1.2 * 590, duration: 1.0, ease: "power2.inOut" }, 9.0);
  const rg = el("g", { id: "tRing", opacity: 0 }, document.getElementById("xInner"));
  const RR = 150, C = 2 * Math.PI * RR;
  el("circle", { cx: 1125, cy: 625, r: RR, fill: "none", stroke: "#30363d", "stroke-width": 12 }, rg);
  const sw = el("circle", { cx: 1125, cy: 625, r: RR, fill: "none", stroke: "#d29922", "stroke-width": 12, "stroke-dasharray": `${C} ${C}`, "stroke-dashoffset": C, transform: "rotate(-90 1125 625)" }, rg);
  el("line", { x1: 1125, y1: 625 - RR - 22, x2: 1125, y2: 625 - RR + 22, stroke: "#f85149", "stroke-width": 8 }, rg);   // the 2 s limit tick (full turn)
  el("text", { x: 1125, y: 625 - RR - 34, "text-anchor": "middle", class: "x-tag", fill: "#f85149" }, rg).textContent = "2 s";
  const offM = el("circle", { cx: 1125 + RR * Math.sin(2 * Math.PI * 0.35), cy: 625 - RR * Math.cos(2 * Math.PI * 0.35), r: 13, fill: "#3fb950", stroke: "#FFFFFF", "stroke-width": 4, opacity: 0 }, rg);
  tl.to("#tRing", { opacity: 1, duration: 0.3 }, 9.2);
  tl.fromTo(sw, { attr: { "stroke-dashoffset": C } }, { attr: { "stroke-dashoffset": C * 0.65 }, duration: 0.7, ease: "none", immediateRender: false }, 9.4);  // the box: off well before the limit
  tl.to(offM, { opacity: 1, duration: 0.1 }, 10.1);
  tl.to(sw, { attr: { stroke: "#3fb950" }, duration: 0.1 }, 10.1);
  K.hudShow(tl, 9.3, "timer");
  K.label(tl, 10.0, D, "UNDER 2 SECONDS", 120, 860).classList.add("green");
  // citation tag (journalistic, bottom right)
  const cite = document.createElement("div"); cite.className = "lab"; cite.textContent = "CEA REG. 11(6)(e) · IEEE 1547 · IS 16169";
  Object.assign(cite.style, { left: "auto", right: "50px", top: "452px", font: "700 32px Inter, Arial, sans-serif", borderLeftColor: "#8b949e" });
  document.getElementById("root").appendChild(cite);
  tl.set(cite, { opacity: 0 }, 0).to(cite, { opacity: 1, duration: 0.3 }, 9.3);
};
