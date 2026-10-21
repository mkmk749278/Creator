// S01 · Hook (0:00–0:20.9). Lines 1–3. Real footage first (rooftop, fan), then the daylight world:
// the paradox (sun full, fan stops), the box switching itself off, the lineman it protects, the two questions.
window.SCENE = function (tl, ctx) {
  const { V, D } = ctx, L0 = ctx.LINES;
  const svg = document.getElementById("stage");
  const L = W36.lane(svg); W36.xray(svg); document.getElementById("xray").setAttribute("opacity", 0);
  const lm = W36.lineman(L.world, 1240, 760, 1.25, "lmA");
  K.hud([{ k: "grid", label: "GRID", v: "230 V · 50.0 Hz", cls: "cyan" }, { k: "box", label: "SOLAR BOX", v: "TRIPPED", cls: "red", hidden: true }]);

  // 0:00 rooftop footage, slow push; 2:00 PM chip
  tl.fromTo("#v0", { scale: 1.0 }, { scale: 1.08, duration: 3.2, ease: "none" }, 0);
  K.label(tl, 0.3, 2.5, "2:00 PM", 96, 820);
  K.tag(tl, 2.6, 6.0, "ILLUSTRATIVE FOOTAGE");                 // the fan clip is a stand-in
  K.tag(tl, 6.4, D, "ILLUSTRATION");
  // 2.6 fan at speed, the room dims on "power cut"
  const tCut = V(4.4);
  tl.fromTo("#shot1", { filter: "brightness(1)" }, { filter: "brightness(0.72)", duration: 0.25, immediateRender: false }, tCut);
  K.label(tl, tCut, 6.1, "POWER CUT", 96, 820).classList.add("red");
  K.hudSet(tl, tCut, "grid", "0 V · —", "");
  // 6.3 split: the lane (sun blazing on the panels) above, the fan coasting to a stop below
  const tSplit = V(6.3);
  K.cam(tl, 0, 790, 330, 1.6, 960, 300);
  tl.fromTo("#shot1", { clipPath: "inset(0% 0 0 0)" }, { clipPath: "inset(50% 0 0 0)", duration: 0.5, ease: "power2.inOut", immediateRender: false }, tSplit);
  tl.fromTo("#sunGlow", { scale: 1, svgOrigin: "1000 120" }, { scale: 1.25, duration: 2.6, ease: "sine.inOut", immediateRender: false }, tSplit);
  tl.fromTo("#glint", { x: 0 }, { x: 560, duration: 1.6, ease: "power1.inOut", immediateRender: false }, tSplit + 0.4);
  K.label(tl, tSplit + 0.4, V(8.9), "STILL SUNNY", 96, 420).classList.add("amber");
  K.gridDead(tl, 0);
  tl.set("#slowTag", { opacity: 0 }, 0);                       // no beat in this scene: the grid is down
  tl.set("#dholBadge", { visibility: "hidden" }, 0);          // the drummer is introduced in S04
  tl.set("#world", { visibility: "hidden" }, 0).set("#world", { visibility: "visible" }, tSplit - 0.05);
  // 9.0 the box: green LED goes dark, a white flash ring, "not broken"
  const tBox = V(9.0);
  tl.to("#shot1", { opacity: 0, duration: 0.3 }, tBox - 0.2);
  K.look(tl, tBox - 0.2, 0.6, 924, 654, 2.4, "power2.inOut");
  K.tripBox(tl, tBox + 0.6);
  K.hudShow(tl, tBox + 0.6, "box");
  K.label(tl, tBox + 0.8, V(11.5), "NOT BROKEN", 1180, 860).classList.add("green");
  // 11.6 the lineman it protects: low angle on the LT pole, calm work, no harm
  const tLm = V(12.1);                                   // "— to protect a lineman's life" (measured)
  K.look(tl, tLm, 0.8, 1220, 660, 2.6, "power2.inOut", 1150, 600);
  tl.fromTo("#lmA", { y: 30 }, { y: 0, duration: 2.6, ease: "sine.out", immediateRender: false }, tLm);
  K.label(tl, tLm + 0.6, V(14.6), "LINEMAN", 120, 820);
  // 15.2 where does the sunshine go? sunbeams pour onto the panels; heat shimmer
  const tQ = V(15.2);
  K.look(tl, tQ - 0.3, 0.9, 760, 330, 2.1, "power2.inOut");
  const beams = W36.el("g", { id: "beams", opacity: 0 }, L.world);
  for (let i = 0; i < 6; i++) W36.el("line", { x1: 1000 - i * 10, y1: 120, x2: 600 + i * 70, y2: 300, stroke: "#FFE08A", "stroke-width": 10, "stroke-linecap": "round", opacity: 0.7 }, beams);
  tl.to("#beams", { opacity: 1, duration: 0.5 }, tQ).to("#beams line", { attr: { "stroke-dasharray": "40 30" }, duration: 0.01 }, tQ);
  tl.fromTo("#beams line", { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -280 }, duration: 2.5, ease: "none", immediateRender: false }, tQ);
  // 17.6 and how do you keep the fans running? dive down to the house door → S02 (under the stairs)
  const tDive = V(17.6);
  tl.to("#beams", { opacity: 0, duration: 0.4 }, tDive);
  K.look(tl, tDive, 2.6, 633, 816, 3.2, "power2.in");
  tl.to("#stage", { filter: "brightness(0.55)", duration: 0.6 }, D - 0.6);
};
