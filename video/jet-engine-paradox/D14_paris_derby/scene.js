import { THREE, Stage, PAL, E, K, seg, el, show, wipe, Callout, spring } from "./jepd.js";
import { Globe, Arc, Marker } from "./globe.js";
const S = window.SCENE, T = S.t;
const st = new Stage({ bg: { glow: [0.6, 0.5], glowR: 0.75 }, dust: { count: 160, opacity: 0.35 } });
const gl = new Globe(st);
const a1 = new Arc(gl, S.safran.at, S.gtre.at, { lift: 0.09 }), a2 = new Arc(gl, S.rr.from, S.rr.to, { lift: 0.11, color: PAL.amberHot });
const mP = new Marker(gl, S.safran.at), mB = new Marker(gl, S.gtre.at), mD = new Marker(gl, S.rr.from, { color: PAL.amberHot }), mI = new Marker(gl, S.rr.to, { hollow: true, beam: 0 });
const cP = new Callout(st.overlay, { title: S.safran.name, side: -1, dx: 80, dy: 70 });
const cB = new Callout(st.overlay, { title: S.gtre.name, side: 1, dx: 70, dy: 70 });
const cD = new Callout(st.overlay, { title: S.rr.name, sub: S.rr.sub, side: -1, dx: 110, dy: -80, tone: "white" });
const lab = el(st.overlay, "jep-label", S.selected);
const stamp = el(st.overlay, "jd-stamp", S.stamp);
const chip = el(st.overlay, "jd-chip", `<i></i>${S.status}`); Object.assign(chip.style, { left: "96px", bottom: "120px" });
const dot = chip.querySelector("i");
function renderAt(t) {
  const cam = K(t, [[0, [49, 6, 3.25]], [T.arc0, [47, 14, 3.4], E.sine], [T.arc1 + 0.3, [32, 46, 3.85], E.inOut], [9.6, [19, 74, 2.85], E.inOut],
    [13.4, [27, 58, 3.65], E.inOut], [16.4, [36, 38, 4.0], E.inOut], [19.56, [33, 46, 3.9], E.sine]]);
  gl.frame({ lat: cam[0], lon: cam[1], dist: cam[2], shiftX: 150, shiftY: 20 });
  const pP = seg(t, T.paris - 0.1, T.paris + 0.4, E.out), pB = seg(t, T.arc1 - 0.1, T.arc1 + 0.4, E.out), pD = seg(t, T.derby - 0.1, T.derby + 0.4, E.out);
  mP.set(pP, t - T.paris); mB.set(pB, t - T.arc1); mD.set(pD, t - T.derby); mI.set(seg(t, T.arc2b - 0.2, T.arc2b + 0.4, E.out) * 0.8, -1);
  // after "waiting for final approval" the Safran link turns into a dashed, pending line
  const pend = seg(t, T.chip - 0.2, T.chip + 0.6);
  a1.set(seg(t, T.arc0, T.arc1, E.inOut), { dash: pend, dashOff: t * 0.8, alpha: 1 - 0.45 * pend });
  a2.set(seg(t, T.arc2a, T.arc2b, E.inOut));
  const india = seg(t, T.stamp - 0.6, T.stamp + 0.4) * (1 - 0.5 * seg(t, 10.2, 11));
  gl.spot(0, S.gtre.at, 16, PAL.amber, 0.35 * pB + 0.65 * india);
  const sP = gl.screen(mP.top), sB = gl.screen(mB.top), sD = gl.screen(mD.top);
  cP.set(sP.x, sP.y, pP * sP.vis, seg(t, T.paris, T.paris + 0.6, E.out));
  cB.set(sB.x, sB.y, pB * sB.vis, seg(t, T.arc1, T.arc1 + 0.6, E.out));
  cD.set(sD.x, sD.y, pD * sD.vis, seg(t, T.derby, T.derby + 0.6, E.out));
  const lk = Math.min(seg(t, T.label, T.label + 0.6, E.out), 1 - seg(t, 5.2, 5.6)); show(lab, lk); wipe(lab, seg(t, T.label, T.label + 0.6, E.out));
  // stamp: drops onto India with a damped bounce, then lifts away when the deal is "still waiting"
  const sI = gl.screen(mB.n.clone().multiplyScalar(1.0)), sp = spring(t, T.stamp, 2.2, 7);
  stamp.style.left = (sI.x - 520) + "px"; stamp.style.top = (sI.y - 260) + "px";
  show(stamp, Math.min(seg(t, T.stamp, T.stamp + 0.12), 1 - seg(t, 10.0, 10.5)), 0, 0, 1.6 - 0.6 * sp);
  stamp.style.transform += " rotate(-4deg)";
  const ck = seg(t, T.chip, T.chip + 0.5, E.out); show(chip, ck, 0, -10 * (1 - ck)); wipe(chip, ck);
  dot.style.opacity = (0.35 + 0.65 * (0.5 + 0.5 * Math.cos((t - T.chip) * Math.PI * 2 * 0.8))).toFixed(3);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
