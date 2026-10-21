// Film 36 scene kit: the motion vocabulary approved in lookdev v6 (projects/solar-anti-islanding/review_lookdev_v1–v5.md),
// shared by every scene. All helpers add tweens to the scene's paused timeline; nothing reads the clock.
// Scene times are local seconds; V(t) converts a VO time (seconds in the final edit) to local time.
(function () {
  const BEAT = 0.6;                         // one drum beat = one wave crest, slowed down (tag SLOWED DOWN on screen)
  const $ = s => document.querySelector(s);

  // ---------- HUD (top-left, persistent; rows appear when the VO first needs them) ----------
  function hud(rows) {
    const h = $("#hud");
    rows.forEach(r => {
      const d = document.createElement("div"); d.className = "row"; d.id = "r_" + r.k;
      d.innerHTML = `<span class="k">${r.label}</span><span class="v ${r.cls || ""}" id="h_${r.k}">${r.v}</span>`;
      if (r.hidden) d.style.display = "none";
      h.appendChild(d);
    });
  }
  function hudSet(tl, t, k, text, cls) {
    tl.set("#h_" + k, { textContent: text, className: "v " + (cls || "") }, t);
    tl.fromTo("#r_" + k, { backgroundColor: "rgba(230,237,243,0.22)" }, { backgroundColor: "rgba(230,237,243,0)", duration: 0.6, immediateRender: false }, t);
  }
  function hudShow(tl, t, k) { tl.set("#r_" + k, { display: "flex" }, t); hudSet(tl, t, k, $("#h_" + k).textContent, $("#h_" + k).className.replace("v ", "")); }
  function tag(tl, t0, t1, text) {                       // top-right honesty tag (ILLUSTRATION, SLOWED DOWN, WHAT IF …)
    tl.set("#tag", { textContent: text }, t0).to("#tag", { opacity: 1, duration: 0.25 }, t0).to("#tag", { opacity: 0, duration: 0.25 }, t1);
  }
  function label(tl, t0, t1, text, x, y) {              // a ≤ 3-word kinetic label on a dark chip
    const d = document.createElement("div"); d.className = "lab"; d.textContent = text;
    d.style.left = x + "px"; d.style.top = y + "px"; $("#root").appendChild(d);
    tl.fromTo(d, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, t0)
      .to(d, { opacity: 0, duration: 0.25 }, t1);
    tl.set(d, { opacity: 0 }, 0);
    return d;
  }

  // ---------- the beat (drummer → wires → dancer) ----------
  function beats(tl, L, t0, t1, o) {
    o = o || {};
    const E = W36.el, ringPath = L.ring, len = ringPath.getTotalLength(), TR = o.travel || 0.95;
    tl.set("#dhol", { scaleX: 1, scaleY: 1, svgOrigin: "0 0" }, 0).set("#badge", { y: 0 }, 0).set("#dholShock", { opacity: 0, attr: { r: 60 } }, 0)
      .set(".ltCore", { opacity: 0 }, 0).set("#meterLed", { opacity: 0.25 }, 0).set("#dholBadge", { scale: 1, svgOrigin: "1230 200" }, 0);
    for (let t = t0; t < t1 - 0.05; t += BEAT) {
      tl.to("#dhol", { scaleX: 1.15, scaleY: 0.85, duration: 0.06, ease: "power2.out" }, t)
        .to("#dhol", { scaleX: 0.96, scaleY: 1.05, duration: 0.10, ease: "sine.out" }, t + 0.06)
        .to("#dhol", { scaleX: 1, scaleY: 1, duration: 0.14, ease: "sine.inOut" }, t + 0.16);
      tl.fromTo("#dholShock", { opacity: 0.95, attr: { r: 60 } }, { opacity: 0, attr: { r: 140 }, duration: 0.42, ease: "power2.out", immediateRender: false }, t);
      tl.fromTo("#dholPos .skin", { fill: "#FFFFFF" }, { fill: "#F4E6C8", duration: 0.12, immediateRender: false }, t);
      tl.fromTo("#dholBadge", { scale: 1.08 }, { scale: 1, duration: 0.25, ease: "sine.out", immediateRender: false }, t);
      if (o.noTravel) continue;
      tl.fromTo(".ltCore", { opacity: 0.95 }, { opacity: 0, duration: 0.55, immediateRender: false }, t + 0.12);
      const trail = [0, 1, 2].map(k => E("circle", { r: 20 - k * 5, fill: "#58a6ff", opacity: 0 }, L.world));
      const glow = E("circle", { r: 44, fill: "rgba(88,166,255,0.35)", opacity: 0 }, L.world);
      const ring = E("circle", { r: 22, fill: "#9CC8FF", stroke: "#FFFFFF", "stroke-width": 6, opacity: 0 }, L.world);
      const p = { u: 0 };
      tl.fromTo(p, { u: 0 }, { u: 1, duration: TR, ease: "power1.in", immediateRender: false, onUpdate: () => {
        const pt = ringPath.getPointAtLength(p.u * len), op = p.u <= 0 || p.u >= 1 ? 0 : Math.min(1, 8 * p.u, 4 * (1 - p.u) + 0.15);
        ring.setAttribute("cx", pt.x); ring.setAttribute("cy", pt.y); ring.setAttribute("opacity", op); ring.setAttribute("r", 22 - 6 * p.u);
        glow.setAttribute("cx", pt.x); glow.setAttribute("cy", pt.y); glow.setAttribute("opacity", op); glow.setAttribute("r", 44 - 10 * p.u);
        trail.forEach((c, k) => { const q = Math.max(0, p.u - 0.035 * (k + 1)), tp = ringPath.getPointAtLength(q * len);
          c.setAttribute("cx", tp.x); c.setAttribute("cy", tp.y); c.setAttribute("opacity", (q > 0 && p.u < 1 ? 0.6 - 0.15 * k : 0).toFixed(2)); });
      } }, t);
      if (!o.noDance) tl.to("#badge", { y: -12, scaleY: 1.08, duration: 0.09, ease: "power2.out" }, t + TR).to("#badge", { y: 0, scaleY: 1, duration: 0.2, ease: "sine.in" }, t + TR + 0.09);
      tl.to("#meterLed", { opacity: 1, duration: 0.05 }, t + TR - 0.05).to("#meterLed", { opacity: 0.25, duration: 0.25 }, t + TR);
    }
  }
  // grid cut: the drummer stops and greys, wires go slate
  function gridDead(tl, t) {
    tl.to("#dholBadge", { filter: "grayscale(1) brightness(0.8)", duration: 0.3 }, t);
    tl.to(".wire", { attr: { stroke: "#9aa0a6" }, duration: 0.3 }, t);
  }
  function gridLive(tl, t) {
    tl.to("#dholBadge", { filter: "grayscale(0) brightness(1)", duration: 0.3 }, t);
    tl.to(".wire", { attr: { stroke: "#3a3a3a" }, duration: 0.3 }, t);
  }
  function tripBox(tl, t) {                                // world box trips: LED red, white flash ring, sun badge eyes close
    tl.to("#boxLed", { attr: { fill: "#f85149" }, duration: 0.05 }, t);
    const r = W36.el("circle", { cx: 924, cy: 654, r: 20, fill: "none", stroke: "#FFFFFF", "stroke-width": 8, opacity: 0 }, $("#world"));
    tl.fromTo(r, { opacity: 1, attr: { r: 20 } }, { opacity: 0, attr: { r: 150 }, duration: 0.45, ease: "power2.out", immediateRender: false }, t);
    tl.to("#badge circle:nth-of-type(2), #badge circle:nth-of-type(3)", { attr: { r: 0.8 }, duration: 0.1 }, t);
  }
  // hypothetical scenes: dashed border, desaturation, WHAT IF tag
  function whatIf(tl, t0, t1) {
    tl.to("#stage", { filter: "saturate(0.35) brightness(0.92)", duration: 0.3 }, t0).to("#stage", { filter: "saturate(1) brightness(1)", duration: 0.3 }, t1);
    tl.to("#whatif", { opacity: 1, duration: 0.3 }, t0).to("#whatif", { opacity: 0, duration: 0.3 }, t1);
  }

  // ---------- camera: push into the box (world → X-ray) and back out ----------
  function pushIn(tl, t, X) {
    tl.to("#world", { scale: 5.5, x: 960 - 5.5 * 924, y: 540 - 5.5 * 654, duration: 0.7, ease: "power2.inOut" }, t);
    tl.to("#fg", { x: -900, y: 260, opacity: 0, duration: 0.5, ease: "power2.in" }, t);
    tl.fromTo("#veil", { opacity: 0 }, { opacity: 0.32, duration: 0.3, immediateRender: false }, t + 0.25);
    tl.fromTo("#brackets", { opacity: 0, scale: 1.15, svgOrigin: "960 540" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)", immediateRender: false }, t + 0.3);
    tl.fromTo("#xWipeC", { attr: { r: 0 } }, { attr: { r: 1150 }, duration: 0.45, ease: "power2.in", immediateRender: false }, t + 0.55);
    tl.to("#brackets", { opacity: 0, duration: 0.25 }, t + 0.9).set("#veil", { opacity: 0 }, t + 1.0);
    tl.set("#world", { visibility: "hidden" }, t + 1.05).set("#fg", { visibility: "hidden" }, t + 1.05);
  }
  function pullOut(tl, t) {
    tl.set("#world", { visibility: "visible", scale: 5.5, x: 960 - 5.5 * 924, y: 540 - 5.5 * 654 }, t).set("#fg", { visibility: "visible" }, t);
    tl.to("#xWipeC", { attr: { r: 0 }, duration: 0.45, ease: "power2.out" }, t);
    tl.to("#world", { scale: 1, x: 0, y: 0, duration: 0.7, ease: "power2.inOut" }, t + 0.25);
    tl.to("#fg", { x: 0, y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }, t + 0.35);
  }
  // world camera: put world point (cx,cy) at screen (sx,sy) at scale s. Origin stays 0 0 (GSAP compensates origin changes).
  const camAt = (cx, cy, s, sx, sy) => ({ scale: s, x: (sx === undefined ? 960 : sx) - s * cx, y: (sy === undefined ? 540 : sy) - s * cy, svgOrigin: "0 0" });
  function look(tl, t, dur, cx, cy, s, ease, sx, sy) {
    const { svgOrigin, ...to } = camAt(cx, cy, s, sx, sy);   // never put svgOrigin in a tween: GSAP then re-offsets x/y
    tl.to("#world", { ...to, duration: dur, ease: ease || "sine.inOut" }, t);
  }
  function cam(tl, t, cx, cy, s, sx, sy) {             // svgOrigin only on the first set (t = 0): later it would re-offset x/y
    const { svgOrigin, ...to } = camAt(cx, cy, s, sx, sy); tl.set("#world", t === 0 ? { ...to, svgOrigin } : to, t); }

  // ---------- X-ray: staged reveal + the running machine ----------
  const STAGES = [[".b1", "#xInner > line:nth-of-type(1)", ".dcdot"], ["#xInner > rect", ".swg"], ["#relay"], ["#acPulses", "#xInner > circle"], ["#brain", "#sense", "#ctlRelay", "#ctlBridge"]];
  function xBuild(tl, t, step) {
    tl.set("#xInner", { opacity: 1 }, 0);
    tl.set(STAGES.flat().join(","), { opacity: 0.12 }, 0);
    STAGES.forEach((sel, i) => tl.to(sel.join(","), { opacity: 1, duration: 0.3 }, t + i * (step || 0.32)));
  }
  // st(T) → { grid: bool, drift: Hz offset of the box, open: 0..1 lever, ac: bool }
  function xRun(tl, t0, t1, st) {
    const dots = document.querySelectorAll(".dcdot"), sws = document.querySelectorAll(".sw"), acps = document.querySelectorAll(".acp");
    const tGrid = $("#tGrid"), tBox = $("#tBox"), lever = $("#lever"), sense = $("#sense");
    let lastT = null, boxPh = 0;
    const pr = { T: t0 };
    tl.fromTo(pr, { T: t0 }, { T: t1, duration: t1 - t0, ease: "none", immediateRender: false, onUpdate: () => {
      const T = pr.T, s = st(T);
      // phase of the box = integral of its frequency; computed in closed form from st's drift (pure function of T)
      const gp = -2 * Math.PI * T / BEAT, bp = -2 * Math.PI * (T / BEAT + (s.driftInt || 0));
      dots.forEach((d, i) => d.setAttribute("cx", 320 + ((i * 44 + (s.dc === false ? 0 : T * 150)) % 440)));
      const half = Math.floor(T / (BEAT / 2)) % 2, on = s.open < 0.5;
      sws.forEach((w, k) => { const c = on && ((k === 0 || k === 3) ? half === 0 : half === 1);
        w.setAttribute("x2", +w.getAttribute("x1") + 34); w.setAttribute("y2", +w.getAttribute("y1") - (c ? 0 : 22)); w.setAttribute("stroke", c ? "#9CC8FF" : "#58a6ff"); });
      acps.forEach(c => { const x0 = +c.getAttribute("data-x"); c.setAttribute("cx", (x0 + (on || x0 < 1170 ? 15 * Math.sin(-bp) : 0)).toFixed(1));
        c.setAttribute("opacity", on || x0 < 1170 ? 1 : 0.15); });
      lever.setAttribute("x2", (1080 + 86 * Math.cos(-0.7 * s.open)).toFixed(1)); lever.setAttribute("y2", (612 - 8 + 86 * Math.sin(-0.7 * s.open) + 8 * (1 - s.open)).toFixed(1));
      lever.setAttribute("stroke", s.open > 0.5 ? "#f85149" : "#3fb950");
      sense.setAttribute("stroke-dashoffset", (-T * 90).toFixed(1)); sense.setAttribute("opacity", s.grid ? 1 : 0.3);
      $("#ctlBridge").setAttribute("stroke-dashoffset", (-T * 60).toFixed(1)); $("#ctlRelay").setAttribute("stroke-dashoffset", (-T * 60).toFixed(1));
      tGrid.setAttribute("d", s.grid ? W36.sinePath(1350, 1850, 350, 52, 3, gp) : "M 1350 350 L 1850 350");
      tGrid.setAttribute("stroke", s.grid ? "#58a6ff" : "#8b949e");
      tBox.setAttribute("d", on ? W36.sinePath(1350, 1850, 350, 52, 3, bp + (s.lockOff || 0)) : "M 1350 350 L 1850 350");
      const bt = (T % BEAT) / BEAT; const xb = $("#xBadge");
      if (xb) { xb.setAttribute("transform", `translate(0 -118) scale(${(1 + (s.grid ? 0.1 : 0) * Math.max(0, 1 - bt * 4)).toFixed(3)})`); xb.setAttribute("opacity", (s.badge !== undefined ? s.badge : s.grid) ? 1 : 0.35); }   // badge: the drummer itself (can differ from the voltage seen)
    } }, t0);
  }

  // re-time a scene after re-measuring its cues: every position argument goes through a piecewise-linear map
  function warp(tl, from, to) {
    const W = t => { if (t <= from[0]) return t; for (let i = 1; i < from.length; i++) if (t <= from[i]) return to[i - 1] + (t - from[i - 1]) * (to[i] - to[i - 1]) / (from[i] - from[i - 1]); return t; };
    const P = new Proxy(tl, { get(o, k) { const v = o[k];
      if (["to", "from", "fromTo", "set"].includes(k)) return (...a) => { const i = a.length - 1; if (typeof a[i] === "number") a[i] = W(a[i]); o[k](...a); return P; };
      return typeof v === "function" ? v.bind(o) : v; } });
    P.W = W; return P;
  }
  window.K = { warp, BEAT, hud, hudSet, hudShow, tag, label, beats, gridDead, gridLive, tripBox, whatIf, pushIn, pullOut, look, cam, xBuild, xRun };
})();
