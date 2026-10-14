import { THREE, Stage, E, K, seg, clamp, el, show } from "./jepd.js";
import { Panel, loadFonts, HEX, jetPath, JET_LEN, strokeK, fillP } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.62, 0.5], glowR: 0.8, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [3, -5, 1.06]], [5.82, [-1, 4, 1.0], E.sine]] });
const big1 = el(st.overlay, "jd-big", `<span class="n"></span><small>${S.sanctionedLabel}</small>`);
const big2 = el(st.overlay, "jd-big", `<span class="n" style="color:var(--amber)"></span><small>${S.actualLabel}</small>`);
Object.assign(big1.style, { left: "110px", top: "250px" }); Object.assign(big2.style, { left: "110px", top: "560px" });
const COLS = 7, ROWS = Math.ceil(S.sanctioned / COLS), X0 = 830, Y0 = 205, DX = 142, DY = 124, SZ = 108;
const slots = Array.from({ length: S.sanctioned }, (_, i) => ({ x: X0 + (i % COLS) * DX, y: Y0 + Math.floor(i / COLS) * DY, i }));
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  for (const s of slots) {
    const p = jetPath(s.x, s.y, SZ), d0 = T.draw0 + (s.i / S.sanctioned) * (T.draw1 - T.draw0 - 0.5);
    const dk = seg(t, d0, d0 + 0.5, E.out);
    const filled = s.i < S.actual;
    const f0 = T.fill0 + (s.i / S.actual) * (T.fill1 - T.fill0 - 0.25), fk = filled ? seg(t, f0, f0 + 0.25, E.out) : 0;
    if (filled) {
      fillP(g, p, "#2e3644", 0.7 * dk * (1 - fk)); strokeK(g, p, SZ * JET_LEN, dk, { w: 2.6, color: HEX.white, alpha: 0.9 * (1 - fk) });
      fillP(g, p, HEX.amber, 0.85 * fk); fillP(k, p, HEX.amber, 0.28 * fk);
      strokeK(k, p, SZ * JET_LEN, fk, { w: 2.2, color: HEX.hot, alpha: 0.9 });
    } else {
      // empty slots: after the fill, they turn red and pulse
      const r = seg(t, T.fill1 - 0.1, T.fill1 + 0.3, E.out), pulse = 0.55 + 0.45 * Math.cos((t - T.fill1) * 2 * Math.PI * 1.4);
      fillP(g, p, "#2e3644", 0.7 * dk); strokeK(g, p, SZ * JET_LEN, dk, { w: 2.6, color: HEX.white, alpha: 0.9 * (1 - r) });
      strokeK(g, p, SZ * JET_LEN, dk, { w: 2.6, color: HEX.red, alpha: r });
      strokeK(k, p, SZ * JET_LEN, dk, { w: 3, color: HEX.red, alpha: r * 0.6 * pulse });
    }
  }
  pn.end(t);
  const a1 = seg(t, T.n42 - 0.4, T.n42 + 0.1, E.out), c1 = seg(t, T.draw0, T.n42, E.out);
  big1.querySelector(".n").textContent = String(Math.round(S.sanctioned * c1)); show(big1, a1, 0, 14 * (1 - a1));
  const a2 = seg(t, T.fill0 - 0.2, T.fill0 + 0.3, E.out);
  const nf = slots.filter((s) => s.i < S.actual && t >= T.fill0 + (s.i / S.actual) * (T.fill1 - T.fill0 - 0.25) + 0.12).length;
  big2.querySelector(".n").textContent = S.actualPrefix + nf; show(big2, a2, 0, 14 * (1 - a2));
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
