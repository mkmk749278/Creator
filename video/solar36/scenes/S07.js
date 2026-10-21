// S07 · The tricky case and the off-beat test (1:50.1–2:22.3). Lines 13–16.
// A: the whole street uses exactly what all its panels make (panels on every roof, a level balance); the supply is cut
//    and nothing changes: the wires stay live, inside the box the grid trace is untouched though the drummer is gone.
// B: so the box tests the drummer: its wave kicks a little ahead, again and again; a ping runs down to the transformer.
// C: split. GRID ON: each kick is pulled back onto the grid wave. GRID OFF: nobody pulls it back; the waves squeeze,
//    50.0 → 50.5 Hz, the trip line (CEA reg. 11(6)(b)); click, the box goes dark.
// Cues (local s): "tricky case" 0.71 · "whole street" 2.86 · "power cut changes nothing" 7.06 · "can't feel it" 9.16 ·
// "tests the drummer" 10.71 · "plays a little off-beat" 12.81 · "is the drummer still there" 17.53 ·
// "If the grid is there" 19.88 · "If the grid is gone" 24.40 · "keeps sliding" 27.10 · "the box knows" 28.80 · "Click" 30.15.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg);
  const world = L.world;
  K.hud([{ k: "grid", label: "GRID", v: "230 V · 50.0 Hz", cls: "cyan" }, { k: "box", label: "SOLAR BOX", v: "IN STEP ✓", cls: "green" },
         { k: "freq", label: "BOX FREQ", v: "50.0 Hz", cls: "", hidden: true }]);
  K.gridLive(tl, 0);
  tl.set("#slowTag", { opacity: 0 }, 0);
  K.tag(tl, 0, D, "ILLUSTRATION · SLOWED DOWN");

  // ================= A · the balanced street (0–10.3) =================
  K.cam(tl, 0, 1000, 560, 1.15);
  K.look(tl, 0.4, 2.2, 960, 540, 1.0, "power2.inOut");
  K.beats(tl, L, 0.2, 7.0, { noTravel: true });
  // solar on every roof of the street
  W36.panels(world, 1690, 478, 2, 1, 572);
  // the balance: what the street uses vs what all its panels make, level
  const bal = el("g", { id: "bal", opacity: 0 }, svg);
  const scrim = el("rect", { x: 590, y: 92, width: 540, height: 214, rx: 22, fill: "rgba(13,17,23,0.78)" }, bal);
  el("polygon", { points: "860,262 838,300 882,300", fill: "#C9D1D9" }, bal);
  const beam = el("g", { id: "beam" }, bal);
  el("line", { x1: 720, y1: 262, x2: 1000, y2: 262, stroke: "#C9D1D9", "stroke-width": 10, "stroke-linecap": "round" }, beam);
  [[740, "#58a6ff", "STREET USES"], [980, "#F2C14E", "PANELS MAKE"]].forEach(([x, c, t]) => {
    el("line", { x1: x, y1: 262, x2: x, y2: 214, stroke: "#C9D1D9", "stroke-width": 4 }, beam);
    el("path", { d: `M ${x - 62} 214 Q ${x} 242 ${x + 62} 214 Z`, fill: c, opacity: 0.9 }, beam);
    el("text", { x, y: 182, "text-anchor": "middle", class: "x-tag", style: "font-size: 27px" }, beam).textContent = t;
  });
  tl.to("#bal", { opacity: 1, duration: 0.4 }, 2.9);
  tl.fromTo("#beam", { rotation: -9, svgOrigin: "860 262" }, { rotation: 0, duration: 1.6, ease: "elastic.out(1, 0.45)", immediateRender: false }, 3.1);
  K.label(tl, 4.6, 6.9, "PERFECT BALANCE", 120, 860).classList.add("green");
  tl.to("#bal", { opacity: 0, duration: 0.3 }, 6.95);
  // 7.06 the supply is cut… and the wires stay live (the boxes hold them up); the drummer is gone
  const brk = el("g", { id: "brk" }, world);
  el("rect", { x: 1770, y: 300, width: 120, height: 120, rx: 10, fill: "#5E6A73", stroke: "#3E4A57", "stroke-width": 4 }, brk);
  el("circle", { cx: 1800, cy: 380, r: 9, fill: "#D5DBDB" }, brk); el("rect", { x: 1846, y: 368, width: 16, height: 22, rx: 3, fill: "#D5DBDB" }, brk);
  const lev = el("line", { x1: 1800, y1: 380, x2: 1852, y2: 380, stroke: "#3fb950", "stroke-width": 9, "stroke-linecap": "round" }, brk);
  el("rect", { x: 1786, y: 318, width: 88, height: 26, rx: 4, fill: "#1B2631" }, brk);
  el("text", { x: 1830, y: 338, "text-anchor": "middle", class: "w-tagM" }, brk).textContent = "11 kV";
  tl.to(lev, { rotation: -38, svgOrigin: "1800 380", duration: 0.18, ease: "power3.in" }, 7.1).to(lev, { attr: { stroke: "#f85149" }, duration: 0.05 }, 7.25);
  tl.to("#dholBadge", { filter: "grayscale(1) brightness(0.8)", duration: 0.3 }, 7.2);
  K.hudSet(tl, 7.2, "grid", "CUT · STILL 230 V", "amber");
  K.label(tl, 7.2, 8.0, "SUPPLY CUT", 1420, 470).classList.add("red");
  // 8.0 push into the box: the scope has not changed at all
  K.look(tl, 7.6, 0.4, 924, 654, 2.4, "power2.in");
  K.pushIn(tl, 8.0);
  K.xBuild(tl, 8.6, 0.05);
  tl.set(".x-title", { opacity: 1 }, 0).set("#inStep", { opacity: 0 }, 0);
  // the running machine for B as well: kicks (lockOff) on the box wave from 12.8, grid wave on screen throughout
  const kick = T => { if (T < 12.8 || T > 16.7) return 0; const p = (T - 12.8) % 1.2; return p < 0.12 ? 0.9 * p / 0.12 : 0.9 * Math.exp(-(p - 0.12) * 7); };
  K.xRun(tl, 0, 19.0, T => ({ grid: true, badge: T < 7.2, open: 0, driftInt: 0, lockOff: kick(T), dc: true }));
  K.hudSet(tl, 7.2, "box", "NO CHANGE", "amber");
  K.label(tl, 9.1, 10.5, "NO CHANGE", 120, 860).classList.add("amber");
  K.hudShow(tl, 9.2, "freq");

  // ================= B · the off-beat test (10.7–18.8) =================
  tl.to("#xcam", { scale: 1.2, x: 960 - 1.2 * 1020, y: 540 - 1.2 * 560, duration: 1.2, ease: "power2.inOut" }, 10.6);
  tl.to("#brain, #ctlBridge", { opacity: 1, duration: 0.2 }, 10.7).to("#xcam .x-title", { opacity: 0, duration: 0.3 }, 10.6);
  K.hudSet(tl, 10.7, "box", "TESTING", "amber");
  [12.8, 14.0, 15.2, 16.4].forEach(t => {
    tl.fromTo("#ctlBridge", { attr: { stroke: "#FFFFFF" } }, { attr: { stroke: "#c9d1d9" }, duration: 0.4, immediateRender: false }, t);
    K.hudSet(tl, t, "freq", "50.0 Hz ↗", "amber"); K.hudSet(tl, t + 0.35, "freq", "50.0 Hz", "");
  });
  K.label(tl, 12.9, 16.6, "TEST NUDGE", 120, 860).classList.add("amber");
  // 16.72 "to check… is the drummer still there": out to the street, a ping runs from the box to the transformer
  K.pullOut(tl, 16.6);
  K.look(tl, 17.4, 1.2, 1200, 520, 1.3, "power2.out");
  const ring = L.ring, len = ring.getTotalLength();
  const ping = el("circle", { r: 16, fill: "none", stroke: "#FFFFFF", "stroke-width": 6, opacity: 0 }, world);
  const pg = { u: 1 };
  tl.fromTo(pg, { u: 1 }, { u: 0.12, duration: 1.4, ease: "power1.inOut", immediateRender: false, onUpdate: () => {
    const p = ring.getPointAtLength(pg.u * len); ping.setAttribute("cx", p.x); ping.setAttribute("cy", p.y);
    ping.setAttribute("opacity", pg.u > 0.125 && pg.u < 0.999 ? 1 : 0); ping.setAttribute("r", 16 + 10 * Math.abs(Math.sin(pg.u * 30))); } }, 17.3);
  K.label(tl, 17.5, 18.9, "CHECKING", 1300, 860);

  // ================= C · split: GRID ON vs GRID OFF (19.0–end) =================
  const sp = el("g", { id: "split", "clip-path": "url(#spWipe)" }, svg);
  const cp = el("clipPath", { id: "spWipe" }, svg.querySelector("defs")); const wc = el("circle", { cx: 960, cy: 540, r: 0 }, cp);
  el("rect", { width: 1920, height: 1080, fill: "#0d1117" }, sp);
  for (let x = 0; x <= 1920; x += 48) el("line", { x1: x + 0.5, y1: 0, x2: x + 0.1, y2: 1080, stroke: x % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": x % 240 ? 1 : 2 }, sp);
  for (let y = 0; y <= 1080; y += 48) el("line", { x1: 0, y1: y + 0.5, x2: 1920, y2: y + 0.1, stroke: y % 240 ? "#1f2a38" : "#2a3a4e", "stroke-width": y % 240 ? 1 : 2 }, sp);
  const drum = (g, x, y, live) => { const d = el("g", { class: "sDrum" }, g);
    el("circle", { cx: x, cy: y, r: 50, fill: "#0d1117", stroke: live ? "#58a6ff" : "#8b949e", "stroke-width": 4 }, d);
    el("path", { d: `M ${x - 32} ${y - 17} Q ${x} ${y - 28} ${x + 32} ${y - 17} L ${x + 32} ${y + 17} Q ${x} ${y + 28} ${x - 32} ${y + 17} Z`, fill: live ? "#9C5A2E" : "#5a5f66", stroke: "#3a2a1a", "stroke-width": 3 }, d);
    return d; };
  const P = [{ x: 70, live: true, head: "GRID ON", col: "#58a6ff" }, { x: 990, live: false, head: "GRID OFF", col: "#8b949e" }];
  const parts = P.map((p, i) => {
    const g = el("g", { id: "pan" + i }, sp);
    el("rect", { x: p.x, y: 290, width: 860, height: 640, rx: 26, fill: "rgba(22,27,34,0.92)", stroke: "#30363d", "stroke-width": 3 }, g);
    el("text", { x: p.x + 40, y: 360, class: "x-title", fill: p.col }, g).textContent = p.head;
    const dr = drum(g, p.x + 780, 352, p.live);
    el("rect", { x: p.x + 40, y: 420, width: 780, height: 260, rx: 14, fill: "#0d1117", stroke: "#30363d", "stroke-width": 2 }, g);
    el("line", { x1: p.x + 60, y1: 550, x2: p.x + 800, y2: 550.2, stroke: "#30363d", "stroke-width": 2 }, g);
    const bw = el("path", { fill: "none", stroke: "rgba(255,255,255,0.55)", "stroke-width": 12, "stroke-linecap": "round" }, g);   // box: thick white, under
    const gw = el("path", { fill: "none", stroke: "#58a6ff", "stroke-width": 5 }, g);                                             // grid: thin blue, on top
    const fq = el("text", { x: p.x + 40, y: 760, class: "x-lab" }, g); fq.textContent = "BOX 50.0 Hz";
    return { g, gw, bw, fq, dr, x0: p.x + 60, x1: p.x + 800 };
  });
  // right panel: the frequency bar with the trip line at 50.5 Hz
  const bar = el("g", { id: "fbar" }, parts[1].g);
  const fx = f => 1050 + (f - 49.5) / 1.0 * 700;
  el("rect", { x: 1050, y: 820, width: 700, height: 22, rx: 11, fill: "#30363d" }, bar);
  el("rect", { x: fx(49.9), y: 820, width: fx(50.1) - fx(49.9), height: 22, fill: "rgba(63,185,80,0.45)" }, bar);
  el("line", { x1: fx(50.5), y1: 800, x2: fx(50.5), y2: 862, stroke: "#f85149", "stroke-width": 6 }, bar);
  el("text", { x: fx(50.5), y: 895, "text-anchor": "end", class: "x-tag", fill: "#f85149" }, bar).textContent = "TRIP 50.5 Hz";
  el("text", { x: 1050, y: 895, class: "x-tag" }, bar).textContent = "49.5";
  const mk = el("polygon", { points: "0,0 -14,-24 14,-24", fill: "#E6EDF3", transform: `translate(${fx(50)} 818)` }, bar);
  // the moving waves (pure function of time)
  const nudges = [24.9, 26.2, 27.5, 28.8, 30.05], tClick = 30.15;
  const fOff = T => 50 + 0.1 * nudges.filter(t => T >= t).length;
  const kickL = T => { const p = (T - 19.9) % 1.3; return T < 19.9 ? 0 : (p < 0.1 ? 0.9 * p / 0.1 : 0.9 * Math.exp(-(p - 0.1) * 9)); };
  const st = { T: 19 };
  tl.fromTo(st, { T: 19 }, { T: D, duration: D - 19, ease: "none", immediateRender: false, onUpdate: () => {
    const T = st.T, gp = -2 * Math.PI * T / K.BEAT;
    const L0 = parts[0], R0 = parts[1];
    L0.gw.setAttribute("d", W36.sinePath(L0.x0, L0.x1, 550, 90, 3, gp));
    L0.bw.setAttribute("d", W36.sinePath(L0.x0, L0.x1, 550, 90, 3, gp + kickL(T)));
    R0.gw.setAttribute("d", `M ${R0.x0} 550 L ${R0.x1} 550`); R0.gw.setAttribute("stroke", "#8b949e");
    const f = T < tClick ? fOff(T) : 50.5, cyc = 3 * (1 + (f - 50) * 1.6);
    R0.bw.setAttribute("d", T < tClick ? W36.sinePath(R0.x0, R0.x1, 550, 90, cyc, gp * (f / 50)) : `M ${R0.x0} 550 L ${R0.x1} 550`);
    R0.fq.textContent = T < tClick ? `BOX ${f.toFixed(1)} Hz` : "BOX OFF";
    mk.setAttribute("transform", `translate(${fx(f).toFixed(1)} 818)`);
    const bt = (T % K.BEAT) / K.BEAT; L0.dr.setAttribute("transform", `translate(${L0.x1 - 20} 352) scale(${(1 + 0.12 * Math.max(0, 1 - bt * 4)).toFixed(3)}) translate(${-(L0.x1 - 20)} -352)`);
  } }, 19);
  tl.set("#split", { visibility: "hidden" }, 0).set("#split", { visibility: "visible" }, 18.95);
  tl.fromTo(wc, { attr: { r: 0 } }, { attr: { r: 1150 }, duration: 0.5, ease: "power2.in", immediateRender: false }, 18.95);
  tl.set("#world, #fg", { visibility: "hidden" }, 19.5);                // fully under the split from here
  tl.set("#pan1", { opacity: 0.35 }, 0).set("#pan0", { opacity: 1 }, 0);
  K.label(tl, 20.0, 23.4, "PULLED BACK", 400, 306).classList.add("green");
  K.hudSet(tl, 19.9, "grid", "230 V · 50.0 Hz", "cyan"); K.hudSet(tl, 19.9, "box", "IN STEP ✓", "green");
  // 24.40 the grid is gone: the right panel takes over
  tl.to("#pan0", { opacity: 0.35, duration: 0.4 }, 24.3).to("#pan1", { opacity: 1, duration: 0.4 }, 24.3);
  K.hudSet(tl, 24.4, "grid", "OFF", ""); K.hudSet(tl, 24.4, "box", "TESTING", "amber");
  nudges.forEach(t => K.hudSet(tl, t, "freq", `${fOff(t).toFixed(1)} Hz`, t > 28 ? "red" : "amber"));
  K.label(tl, 25.7, 28.6, "NOBODY PULLS", 1320, 306).classList.add("red");
  K.label(tl, 28.85, 30.1, "THE BOX KNOWS", 1320, 306).classList.add("amber");
  // 30.15 click: flash, the box goes dark
  const fl = el("rect", { x: 990, y: 290, width: 860, height: 640, rx: 26, fill: "#FFFFFF", opacity: 0 }, sp);
  tl.fromTo(fl, { opacity: 0.8 }, { opacity: 0, duration: 0.35, immediateRender: false }, tClick);
  K.hudSet(tl, tClick, "box", "TRIPPED", "red");
  K.hudSet(tl, tClick, "freq", "50.5 Hz · TRIP", "red");
  K.label(tl, tClick + 0.1, D, "SWITCHES OFF", 1320, 306).classList.add("red");
};
