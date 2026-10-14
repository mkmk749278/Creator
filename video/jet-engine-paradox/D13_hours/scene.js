import { THREE, Stage, E, seg, el, show, wipe, spring } from "./jepd.js";
import { Panel, loadFonts, HEX, line, text, scale } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.5], glowR: 0.9, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [3, -5, 1.07]], [3.51, [-1, 4, 1.0], E.sine]] });
const c1 = el(st.overlay, "jd-chip", S.rocket), c2 = el(st.overlay, "jd-chip", S.engine);
Object.assign(c1.style, { left: "250px", top: "790px", borderColor: "var(--dim)" }); Object.assign(c2.style, { left: "860px", top: "790px" });
const plus = el(st.overlay, "jd-big", S.plus); Object.assign(plus.style, { left: "1740px", top: "395px", fontSize: "170px", color: "var(--amber)" });
const SX = 470, SY = 480, SR = 230;            // stopwatch
const DX = 900, DY = 360, DW = 190, DH = 250;  // 4 drums
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  // stopwatch: one sweep, then it stops with a small recoil
  g.save(); g.strokeStyle = HEX.line; g.lineWidth = 4; g.beginPath(); g.arc(SX, SY, SR, 0, 7); g.stroke(); g.restore();
  scale(g, (v) => { const a = v / 60 * 2 * Math.PI - Math.PI / 2; return [SX + Math.cos(a) * SR, SY + Math.sin(a) * SR, -Math.cos(a), -Math.sin(a)]; }, 0, 59, 1, 5, { len: 12, lenMaj: 28 });
  const sw = seg(t, T.sweep0, T.sweep1, E.out) * 0.82 + 0.02 * (spring(t, T.sweep1, 3, 6) - (t > T.sweep1 ? 1 : 0)) * -1;
  const a = sw * 2 * Math.PI - Math.PI / 2, stop = seg(t, T.sweep1, T.sweep1 + 0.5);
  line(g, SX, SY, SX + Math.cos(a) * (SR - 30), SY + Math.sin(a) * (SR - 30), { w: 6, color: HEX.white, cap: "round" });
  line(k, SX, SY, SX + Math.cos(a) * (SR - 30), SY + Math.sin(a) * (SR - 30), { w: 6, color: HEX.white, alpha: 0.5 * (1 - stop), cap: "round" });
  g.save(); g.fillStyle = HEX.white; g.beginPath(); g.arc(SX, SY, 14, 0, 7); g.fill(); g.fillRect(SX - 22, SY - SR - 44, 44, 24); g.restore();
  // odometer drums roll to 4,000 hours
  const v = S.hours * seg(t, T.drum0, T.drum1, E.inOut);
  for (let i = 0; i < 4; i++) {
    const x = DX + i * (DW + 18), p = 10 ** (3 - i), pos = (v / p) % 10;
    g.save(); g.fillStyle = "#151b27"; g.strokeStyle = HEX.line; g.lineWidth = 3; g.fillRect(x, DY, DW, DH); g.strokeRect(x, DY, DW, DH);
    g.beginPath(); g.rect(x, DY, DW, DH); g.clip();
    for (let d = -1; d <= 1; d++) { const n = (Math.floor(pos) + d + 10) % 10, y = DY + DH / 2 + (d - (pos % 1)) * DH * 0.9;
      text(g, String(n), x + DW / 2, y + 62, { size: 180, weight: 800, align: "center", color: i === 0 ? HEX.amber : HEX.white, track: 0 }); }
    const sh = g.createLinearGradient(0, DY, 0, DY + DH); sh.addColorStop(0, "rgba(11,14,20,0.85)"); sh.addColorStop(0.3, "rgba(11,14,20,0)"); sh.addColorStop(0.7, "rgba(11,14,20,0)"); sh.addColorStop(1, "rgba(11,14,20,0.85)");
    g.fillStyle = sh; g.fillRect(x, DY, DW, DH); g.restore();
    if (i === 0) { text(g, ",", x + DW + 2, DY + DH - 30, { size: 90, weight: 800, color: HEX.white }); }
  }
  k.save(); k.globalAlpha = 0.5 * seg(t, T.drum1, T.drum1 + 0.3); k.strokeStyle = HEX.amber; k.lineWidth = 5; k.strokeRect(DX, DY, DW, DH); k.restore();
  pn.end(t);
  const a1 = seg(t, 0.1, 0.5, E.out); show(c1, a1); wipe(c1, a1);
  const a2 = seg(t, T.drum0 + 0.2, T.drum0 + 0.7, E.out); show(c2, a2); wipe(c2, a2);
  const pk = spring(t, T.drum1, 2.2, 6); show(plus, seg(t, T.drum1, T.drum1 + 0.1), 0, 0, 1.4 - 0.4 * pk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
