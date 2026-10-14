import { THREE, Stage, E, seg, el, show, wipe, spring } from "./jepd.js";
import { Panel, loadFonts, HEX, line, text, scale } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.5], glowR: 0.9, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [3, -6, 1.08]], [6.23, [-1, 5, 1.0], E.sine]] });
const Y = 600, X = (y) => 260 + (y - S.years[0]) * 290;
const MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
const cP = el(st.overlay, "jd-chip", S.promised.label), cF = el(st.overlay, "jd-chip", "");
cF.style.borderColor = "var(--red)";
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  // owner review 2026-10-14: fill the empty upper frame; a large faint year follows the delivery cursor (no new data)
  const cur = t < T.slide0 ? S.promised.at : S.promised.at + (S.first.at - S.promised.at) * seg(t, T.slide0, T.slide1, E.inOut);
  const wy = Math.floor(cur + 1e-6), wa = seg(t, T.promised - 0.2, T.promised + 0.6, E.out);
  text(g, String(wy), 960 + 40 * Math.sin(t * 0.35), 440, { size: 300, weight: 800, color: HEX.white, align: "center", alpha: 0.4 * wa, track: 0.02 });
  const rk = seg(t, T.rail, T.rail + 1.0, E.out), x0 = X(S.years[0]) - 60, x1 = X(S.years[1]) + 60;
  line(g, x0, Y, x0 + (x1 - x0) * rk, Y, { w: 5, color: HEX.white, alpha: 0.75 });
  scale(g, (v) => [X(v), Y + 24, 0, 1], S.years[0], S.years[1], 1 / 12, 1, { len: 14, lenMaj: 40, k: rk, label: (v) => String(Math.round(v)), size: 44 });
  // promised pin (amber) and the delivery marker sliding month by month to MAR 2025; the gap fills red
  const pp = spring(t, T.promised, 1.8, 6), xp = X(S.promised.at);
  if (t > T.promised) { line(g, xp, Y - 220 * pp, xp, Y, { w: 6, color: HEX.amber }); line(k, xp, Y - 220 * pp, xp, Y, { w: 6, color: HEX.amber, alpha: 0.6 }); }
  const sk = seg(t, T.slide0, T.slide1, E.inOut), at = S.promised.at + (S.first.at - S.promised.at) * sk, xf = X(at);
  if (t > T.slide0 - 0.3) {
    const a = seg(t, T.slide0 - 0.3, T.slide0, E.out);
    g.save(); g.globalAlpha = 0.85 * a; g.fillStyle = HEX.red; g.fillRect(xp, Y - 22, xf - xp, 44); g.restore();
    k.save(); k.globalAlpha = 0.35 * a; k.fillStyle = HEX.red; k.fillRect(xp, Y - 22, xf - xp, 44); k.restore();
    line(g, xf, Y + 0, xf, Y + 220, { w: 6, color: HEX.white, alpha: a }); line(k, xf, Y, xf, Y + 220, { w: 6, color: HEX.white, alpha: 0.4 * a });
  }
  pn.end(t);
  const sp = st.toScreen(new THREE.Vector3((xp - 960) / 1000, -(Y - 220 - 540) / 1000, 0));
  Object.assign(cP.style, { left: (sp.x - 20) + "px", top: (sp.y - 70) + "px" });
  const pk = seg(t, T.promised + 0.1, T.promised + 0.5, E.out); show(cP, pk); wipe(cP, pk);
  const m = Math.round((at - 2023) * 12), mo = MON[(m % 12 + 12) % 12] + " " + (2023 + Math.floor(m / 12));
  cF.innerHTML = t >= T.slide1 ? `${S.first.label} ${S.first.month}` : mo;
  const sf = st.toScreen(new THREE.Vector3((xf - 960) / 1000, -(Y + 220 - 540) / 1000, 0));
  Object.assign(cF.style, { left: (sf.x + 20 - cF.offsetWidth) + "px", top: (sf.y + 12) + "px" });
  const fk = seg(t, T.slide0, T.slide0 + 0.3, E.out); show(cF, fk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
