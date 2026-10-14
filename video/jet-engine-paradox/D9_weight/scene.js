import { THREE, Stage, E, seg, el, show, wipe, spring, fmt } from "./jepd.js";
import { Panel, loadFonts, HEX, line, scale } from "./kit.js";
const S = window.SCENE, T = S.t, [V0, V1] = S.range;
loadFonts();
const st = new Stage({ bg: { glow: [0.4, 0.55], glowR: 0.8, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [-3, 7, 1.1]], [4.7, [1, -2, 0.97], E.sine]] });
const CX = 720, CY = 640, R = 400, A0 = -210, A1 = 30;   // dial sweep (deg, 0 = east, clockwise on screen)
const ang = (v) => (A0 + (v - V0) / (V1 - V0) * (A1 - A0)) * Math.PI / 180;
const pt = (v, r) => [CX + Math.cos(ang(v)) * r, CY + Math.sin(ang(v)) * r];
const read = el(st.overlay, "jd-big", `<span class="n"></span><small>${S.unit}</small>`); Object.assign(read.style, { left: "620px", top: "720px", fontSize: "96px" });
const cT = el(st.overlay, "jd-chip", S.targetLabel), cA = el(st.overlay, "jd-chip", S.actualLabel);
Object.assign(cT.style, { left: "1260px", top: "330px" }); Object.assign(cA.style, { left: "1260px", top: "430px", borderColor: "var(--red)" });
function arc(x, v0, v1, r, w, color, alpha = 1) { x.save(); x.globalAlpha = alpha; x.strokeStyle = color; x.lineWidth = w; x.beginPath(); x.arc(CX, CY, r, ang(v0), ang(v1)); x.stroke(); x.restore(); }
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  const dk = seg(t, 0, 0.5, E.out);
  arc(g, V0, V0 + (V1 - V0) * dk, R + 18, 3, HEX.line);
  arc(g, V0, V0 + (V1 - V0) * dk, R - 60, 1.5, HEX.faint);
  scale(g, (v) => { const a = ang(v); return [CX + Math.cos(a) * R, CY + Math.sin(a) * R, -Math.cos(a), -Math.sin(a)]; }, V0, V1, 10, 100,
    { len: 16, lenMaj: 38, k: dk, size: 30, label: (v) => fmt(v), color: "rgba(248,250,252,0.8)" });
  // target mark and the overweight band
  const tk = seg(t, T.target, T.target + 0.3, E.out);
  if (tk > 0) { const [a, b] = pt(S.target, R + 72), [c, d] = pt(S.target, R - 4); line(g, a, b, c, d, { w: 6, color: HEX.amber, alpha: tk }); line(k, a, b, c, d, { w: 6, color: HEX.amber, alpha: 0.6 * tk }); }
  const bk = seg(t, T.swing2 + 0.2, T.actual, E.out);
  if (bk > 0) { const v = S.target + (S.actual - S.target) * bk; arc(g, S.target, v, R + 46, 26, HEX.red, 0.9); arc(k, S.target, v, R + 46, 26, HEX.red, 0.35 + 0.15 * Math.sin(t * 9)); }
  // needle with inertia: two damped swings
  const v = V0 + (S.target - V0) * spring(t, T.swing1, 1.3, 4.2) + (S.actual - S.target) * spring(t, T.swing2, 1.5, 4.6);
  const a = ang(v), nx = Math.cos(a), ny = Math.sin(a), px = -ny, py = nx;
  for (const [x, al] of [[g, 1], [k, 0.5]]) { x.save(); x.globalAlpha = al; x.fillStyle = x === g ? HEX.white : HEX.hot; x.beginPath();
    x.moveTo(CX + nx * (R - 8), CY + ny * (R - 8)); x.lineTo(CX + px * 12 - nx * 60, CY + py * 12 - ny * 60); x.lineTo(CX - px * 12 - nx * 60, CY - py * 12 - ny * 60); x.closePath(); x.fill(); x.restore(); }
  g.save(); g.fillStyle = "#1a2030"; g.strokeStyle = HEX.line; g.lineWidth = 3; g.beginPath(); g.arc(CX, CY, 34, 0, 7); g.fill(); g.stroke(); g.restore();
  pn.end(t);
  read.querySelector(".n").textContent = fmt(v);
  show(read, seg(t, 0.2, 0.6, E.out));
  const ck = seg(t, T.target, T.target + 0.4, E.out); show(cT, ck); wipe(cT, ck);
  const ak = seg(t, T.actual, T.actual + 0.4, E.out); show(cA, ak); wipe(cA, ak);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
