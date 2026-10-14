import { THREE, Stage, E, seg, el, show, wipe, clamp } from "./jepd.js";
import { Panel, loadFonts, HEX, line, scale } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.52], glowR: 0.9, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [4, -6, 1.08]], [5.72, [-1, 4, 0.99], E.sine]] });
const XA = 220, XB = 1640, Y = 560, H = 90, X = (v) => XA + v / S.max * (XB - XA);
const cT = el(st.overlay, "jd-chip", S.targetLabel), cR = el(st.overlay, "jd-chip", S.reportedLabel);
cR.style.borderColor = "var(--red)";
const read = el(st.overlay, "jd-big", `<span class="n"></span><small>THRUST</small>`); Object.assign(read.style, { left: "220px", top: "250px", fontSize: "110px" });
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  const dk = seg(t, 0, 0.6, E.out);
  g.save(); g.strokeStyle = HEX.line; g.lineWidth = 2.5; g.strokeRect(XA, Y - H / 2, (XB - XA) * dk, H); g.restore();
  scale(g, (v) => [X(v), Y + H / 2 + 6, 0, 1], 0, S.max, 1, 10, { len: 10, lenMaj: 24, k: dk, size: 28, label: (v) => String(v), color: "rgba(248,250,252,0.8)" });
  // fill rises, stalls at ~70 with a shudder that dies out
  const f = seg(t, T.fill0, T.fill1, E.out), sh = t > T.fill1 - 0.4 ? 0.6 * Math.exp(-(t - T.fill1 + 0.4) * 3) * Math.sin((t - T.fill1) * 40) : 0;
  const v = clamp(S.reported * f + sh, 0, S.max), xv = X(v);
  if (v > 0) { const gr = g.createLinearGradient(XA, 0, xv, 0); gr.addColorStop(0, "#9a3b0c"); gr.addColorStop(1, HEX.amber);
    g.fillStyle = gr; g.fillRect(XA + 4, Y - H / 2 + 4, xv - XA - 4, H - 8);
    k.save(); k.globalAlpha = 0.5; k.fillStyle = HEX.amber; k.fillRect(xv - 30, Y - H / 2 + 4, 30, H - 8); k.restore(); }
  // the gap to the target: red hatching
  const gk = seg(t, T.reported, T.reported + 0.4, E.out);
  if (gk > 0) { g.save(); g.beginPath(); g.rect(X(S.reported), Y - H / 2 + 4, (X(S.target) - X(S.reported)) * gk, H - 8); g.clip();
    g.strokeStyle = HEX.red; g.lineWidth = 5; g.globalAlpha = 0.9; for (let x = X(S.reported) - H; x < X(S.target) + H; x += 18) { g.beginPath(); g.moveTo(x, Y + H); g.lineTo(x + H * 1.2, Y - H); g.stroke(); } g.restore(); }
  // dashed target line rises on "eighty one"
  const tk = seg(t, T.target, T.target + 0.5, E.out), xt = X(S.target);
  if (tk > 0) { line(g, xt, Y + H / 2 + 30, xt, Y + H / 2 + 30 - (H + 170) * tk, { w: 5, color: HEX.white, dash: [16, 10] }); line(k, xt, Y + H / 2 + 30, xt, Y + H / 2 + 30 - (H + 170) * tk, { w: 5, color: HEX.white, dash: [16, 10], alpha: 0.4 }); }
  pn.end(t);
  const p1 = st.toScreen(new THREE.Vector3((xt - 960) / 1000, -(Y - H / 2 - 150 - 540) / 1000, 0));
  Object.assign(cT.style, { left: (p1.x - cT.offsetWidth + 12) + "px", top: (p1.y - 64) + "px" });
  const ck = seg(t, T.target + 0.2, T.target + 0.6, E.out); show(cT, ck); wipe(cT, ck);
  const p2 = st.toScreen(new THREE.Vector3((X(S.reported) - 960) / 1000, -(Y + H / 2 + 80 - 540) / 1000, 0));
  Object.assign(cR.style, { left: (p2.x - cR.offsetWidth / 2) + "px", top: (p2.y) + "px" });
  const rk = seg(t, T.reported, T.reported + 0.4, E.out); show(cR, rk); wipe(cR, rk);
  read.querySelector(".n").textContent = (t >= T.reported ? "~" : "") + Math.round(Math.max(0, S.reported * f)) + " " + S.unit;
  show(read, seg(t, T.fill0 - 0.3, T.fill0, E.out));
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
