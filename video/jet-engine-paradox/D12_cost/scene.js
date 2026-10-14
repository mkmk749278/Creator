import { THREE, Stage, E, seg, el, show, wipe, fmt } from "./jepd.js";
import { Panel, loadFonts, HEX, text, scale, line } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.5], glowR: 0.9, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [3, -6, 1.08]], [7.66, [-1, 5, 0.99], E.sine]] });
const XA = 220, XB = 1640, X = (v) => XA + v / S.max * (XB - XA), YE = 470, YS = 650, H = 84;
const big = el(st.overlay, "jd-big", `<span class="n"></span><small>${S.estimateName}</small>`); Object.assign(big.style, { left: "220px", top: "150px", fontSize: "110px" });
const cS = el(st.overlay, "jd-chip", S.spentLabel); cS.style.borderColor = "var(--red)";
const lab = el(st.overlay, "jep-label", S.line);
function bar(g, k, y, v, c0, c1, glow) {
  const gr = g.createLinearGradient(XA, 0, X(v), 0); gr.addColorStop(0, c0); gr.addColorStop(1, c1); g.fillStyle = gr; g.fillRect(XA, y - H / 2, X(v) - XA, H);
  k.save(); k.globalAlpha = glow; k.fillStyle = c1; k.fillRect(X(v) - 24, y - H / 2, 24, H); k.restore();
}
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  const dk = seg(t, 0, 0.6, E.out);
  scale(g, (v) => [X(v), YS + H / 2 + 10, 0, 1], 0, S.max, 100, 500, { len: 10, lenMaj: 24, k: dk, size: 28, label: (v) => fmt(v), color: "rgba(248,250,252,0.8)" });
  for (const y of [YE, YS]) { g.save(); g.strokeStyle = HEX.faint; g.lineWidth = 2; g.strokeRect(XA, y - H / 2, (XB - XA) * dk, H); g.restore(); }
  const e = S.first + (S.estimate - S.first) * seg(t, T.grow0, T.grow1, E.inOut), ea = seg(t, T.bars, T.bars + 0.5, E.out);
  if (ea > 0) bar(g, k, YE, S.first * Math.min(1, ea * 1.2) + (e - S.first), "#7a2f08", HEX.amber, 0.45);
  const ok = seg(t, T.grow0, T.grow0 + 0.4);   // where the first estimate stood
  if (ok > 0) { g.save(); g.globalAlpha = ok; g.strokeStyle = HEX.white; g.lineWidth = 4; g.setLineDash([10, 8]); g.beginPath(); g.moveTo(X(S.first), YE - H / 2 - 16); g.lineTo(X(S.first), YE + H / 2 + 16); g.stroke(); g.restore(); }
  const s = S.spent * seg(t, T.spent0, T.spent1, E.out);
  if (s > 0) bar(g, k, YS, s, "#5c1414", HEX.red, 0.4);
  text(g, "SPENT", XA, YS - H / 2 - 14, { size: 24, weight: 700, color: HEX.dim, track: 0.12, alpha: seg(t, T.spent0, T.spent0 + 0.4) });
  pn.end(t);
  big.querySelector(".n").textContent = "₹" + fmt(Math.round(e)) + " CR"; show(big, ea);
  const sp = st.toScreen(new THREE.Vector3((X(S.spent) - 960) / 1000, -(YS - 540) / 1000, 0));
  Object.assign(cS.style, { left: (sp.x + 24) + "px", top: (sp.y - 28) + "px" });
  const ck = seg(t, T.spent1 - 0.2, T.spent1 + 0.3, E.out); show(cS, ck); wipe(cS, ck);
  const lk = seg(t, T.line, T.line + 0.5, E.out); show(lab, lk); wipe(lab, lk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
