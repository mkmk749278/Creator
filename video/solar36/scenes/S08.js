// S08 · The panels (2:22.3–2:40.7). Lines 17–18. Up on the roof with the box tripped: the charges in the panel cable
// slow and stop (nowhere to go, nothing out); the sunlight just warms the panels (heat shimmer); but the cable still
// carries voltage: it pulses, a hand reaches in and pulls back; real footage of a trained technician with a clamp meter.
// Cues (local s): "What happens to your panels" 0.82 · "nowhere to go" 2.46 · "Nothing comes out" 5.65 · "turns into heat"
// 6.93 · "built for that" 9.95 · "still have voltage" 11.56 · "don't touch them yourself" 14.39 · "a trained person" 16.21.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg); document.getElementById("xray").setAttribute("opacity", 0);
  const world = L.world;
  K.hud([{ k: "grid", label: "GRID", v: "OFF", cls: "" }, { k: "box", label: "SOLAR BOX", v: "TRIPPED", cls: "red" },
         { k: "pv", label: "PANELS", v: "0 A · 0 W", cls: "amber", hidden: true }]);
  K.gridDead(tl, 0);
  tl.set("#dholBadge, #meter text, #fg", { visibility: "hidden" }, 0);   // the foreground scooter would cover the box                    // the drummer is gone (and it would crowd the tag)
  tl.set("#slowTag", { opacity: 0 }, 0).set("#boxLed", { attr: { fill: "#f85149" } }, 0);
  K.tag(tl, 0, 15.7, "ILLUSTRATION");
  K.tag(tl, 16.1, D, "ILLUSTRATIVE FOOTAGE");

  // ---- 0:00 the roof: panels in full sun, the cable down to the box ----
  K.cam(tl, 0, 760, 420, 1.9);
  K.look(tl, 0.2, 5.0, 740, 450, 2.1, "sine.inOut");
  const pv = document.getElementById("pvCable"), plen = pv.getTotalLength();
  const dots = [...Array(9)].map(() => el("circle", { r: 7, fill: "#F2C14E", opacity: 0.95 }, world));
  // charges move along the cable, slow and stop between 2.5 s and 5.3 s (closed-form position: pure function of T)
  const pos = T => T < 2.5 ? T * 120 : (T < 5.3 ? 300 + 120 * (T - 2.5) - 120 * (T - 2.5) ** 2 / (2 * 2.8) : 300 + 120 * 2.8 / 2);
  const dp = { T: 0 };
  tl.fromTo(dp, { T: 0 }, { T: 7, duration: 7, ease: "none", immediateRender: false, onUpdate: () => {
    dots.forEach((c, k) => { const s = (pos(dp.T) + k * (plen / 9)) % plen, p = pv.getPointAtLength(s); c.setAttribute("cx", p.x); c.setAttribute("cy", p.y); });
  } }, 0);
  tl.to(dots, { opacity: 0.45, duration: 0.6 }, 5.4);
  K.label(tl, 2.5, 5.4, "NOWHERE TO GO", 120, 860).classList.add("amber");
  K.hudShow(tl, 5.7, "pv");
  K.label(tl, 5.7, 6.9, "NO CURRENT", 120, 860);

  // ---- 6.93 the sunlight just turns into heat (panels are built for it) ----
  const heat = el("g", { id: "heat", opacity: 0 }, world);
  el("rect", { x: 560, y: 280, width: 460, height: 110, rx: 8, fill: "#FFB347", opacity: 0.13 }, heat);   // warm, not burnt
  const waves = [...Array(7)].map((_, k) => el("path", { fill: "none", stroke: "#FFB347", "stroke-width": 4, "stroke-linecap": "round", opacity: 0.7 }, heat));
  const hp = { T: 0 };
  tl.fromTo(hp, { T: 0 }, { T: 4.6, duration: 4.6, ease: "none", immediateRender: false, onUpdate: () => {
    waves.forEach((w, k) => { const x = 590 + k * 64, y0 = 290 - ((hp.T * 40 + k * 17) % 90);
      let d = `M ${x} ${y0}`; for (let j = 1; j <= 6; j++) d += ` Q ${x + (j % 2 ? 9 : -9)} ${y0 - j * 9 + 4.5} ${x} ${y0 - j * 9}`; w.setAttribute("d", d); });
  } }, 6.9);
  tl.to("#heat", { opacity: 1, duration: 0.5 }, 7.0).to("#heat", { opacity: 0, duration: 0.4 }, 11.3);
  K.look(tl, 6.8, 1.0, 790, 330, 2.5, "power2.inOut");
  K.label(tl, 7.1, 9.8, "JUST HEAT", 120, 860).classList.add("amber");
  K.label(tl, 10.0, 11.3, "BUILT FOR IT", 120, 860).classList.add("green");

  // ---- 11.56 but the panel wires are still live ----
  K.look(tl, 11.2, 1.0, 720, 480, 2.1, "power2.inOut");
  const live = el("path", { d: pv.getAttribute("d"), fill: "none", stroke: "#FFD35A", "stroke-width": 16, "stroke-linecap": "round", opacity: 0 }, world);
  [11.7, 12.5, 13.3, 14.1, 14.9].forEach(t => tl.fromTo(live, { opacity: 0.85 }, { opacity: 0.1, duration: 0.7, ease: "sine.out", immediateRender: false }, t));
  K.hudSet(tl, 11.7, "pv", "LIVE · 0 A", "red");
  K.label(tl, 11.7, 14.3, "STILL LIVE", 120, 860).classList.add("red");
  // 14.39 don't touch them yourself: a hand reaches toward the cable and pulls back
  const hand = el("g", { id: "hand" }, el("g", { transform: "translate(704 640) scale(1.5) translate(-704 -640)" }, world));
  el("rect", { x: 680, y: 600, width: 46, height: 260, rx: 22, fill: "#8D5524" }, hand);
  el("ellipse", { cx: 703, cy: 594, rx: 30, ry: 36, fill: "#8D5524" }, hand);
  [-20, -7, 6, 19].forEach(dx => el("rect", { x: 699 + dx - 5, y: 548, width: 11, height: 40, rx: 5, fill: "#8D5524" }, hand));
  el("rect", { x: 676, y: 700, width: 54, height: 160, rx: 10, fill: "#2E86C1" }, hand);           // shirt sleeve
  tl.set("#hand", { y: 420 }, 0);
  tl.to("#hand", { y: 70, duration: 0.6, ease: "power2.out" }, 14.4).to("#hand", { y: 420, duration: 0.5, ease: "power2.in" }, 15.15);
  const stop = el("circle", { cx: 704, cy: 606, r: 26, fill: "none", stroke: "#f85149", "stroke-width": 8, opacity: 0 }, world);
  tl.fromTo(stop, { opacity: 1, attr: { r: 26 } }, { opacity: 0, attr: { r: 110 }, duration: 0.5, ease: "power2.out", immediateRender: false }, 14.95);
  K.look(tl, 14.1, 0.6, 730, 600, 2.5, "power2.out");
  K.label(tl, 14.45, 15.95, "DON'T TOUCH", 120, 860).classList.add("red");

  // ---- 16.21 leave that to a trained person: real footage ----
  tl.fromTo("#shot0", { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, 16.05);
  tl.fromTo("#v0", { scale: 1.0 }, { scale: 1.06, duration: 2.4, ease: "none", immediateRender: false }, 16.05);
  K.label(tl, 16.3, D, "TRAINED HANDS", 120, 860).classList.add("green");
};
