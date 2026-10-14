import { THREE, Stage, E, seg, el, show, wipe, spring } from "./jepd.js";
import { Panel, loadFonts, HEX, jetPath, fillP, line } from "./kit.js";
const S = window.SCENE, T = S.t, [O1, O2] = S.orders;
loadFonts();
const st = new Stage({ bg: { glow: [0.62, 0.48], glowR: 0.85, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [2.5, -5, 1.07]], [10.91, [-1.5, 4, 0.99], E.sine]] });
const mkStamp = (o, top) => { const e = el(st.overlay, "jd-stamp", `<span style="font-size:30px;letter-spacing:0.14em;color:var(--dim);display:block;margin-bottom:8px">${o.year}</span><span class="c jd-num">${o.n}</span>`);
  Object.assign(e.style, { left: "110px", top: top + "px", fontSize: "96px", padding: "16px 30px 18px" }); return e; };
const s1 = mkStamp(O1, 200), s2 = mkStamp(O2, 470);
s2.style.borderColor = "var(--white)"; s2.style.color = "var(--white)";
const lab = el(st.overlay, "jep-label", "");
const COLS = 20, X0 = 640, Y0 = 240, DX = 57, DY = 72, SZ = 50;
const jets = Array.from({ length: S.total }, (_, i) => ({ x: X0 + (i % COLS) * DX, y: Y0 + Math.floor(i / COLS) * DY, i }));
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  for (const j of jets) {
    line(g, j.x - 7, j.y + 30, j.x + 7, j.y + 30, { w: 2, color: HEX.line, alpha: 0.6 * seg(t, 0.05 + (j.i % COLS) * 0.03, 0.4 + (j.i % COLS) * 0.03, E.out) });   // empty slot tick
    const first = j.i < O1.n, ii = first ? j.i / O1.n : (j.i - O1.n) / O2.n;
    const a = first ? T.o1 : T.o2, b = first ? T.o1fill : T.o2fill, t0 = a + ii * (b - a - 0.25), f = seg(t, t0, t0 + 0.25, E.out);
    if (f <= 0) continue;
    const p = jetPath(j.x, j.y + 8 * (1 - f), SZ);
    if (first) { fillP(g, p, HEX.amber, 0.92 * f); fillP(k, p, HEX.amber, 0.22 * f * (0.7 + 0.3 * Math.cos(t * 2.4 + j.i * 0.37))); }
    else { fillP(g, p, HEX.white, 0.92 * f); fillP(k, p, HEX.hot, 0.25 * f * Math.exp(-(t - t0) * 1.5)); }
  }
  pn.end(t);
  // stamp numbers count with the jets as they land
  let c1 = 0, c2 = 0;
  for (const j of jets) { const first = j.i < O1.n, ii = first ? j.i / O1.n : (j.i - O1.n) / O2.n, a = first ? T.o1 : T.o2, b = first ? T.o1fill : T.o2fill;
    if (t >= a + ii * (b - a - 0.25) + 0.12) first ? c1++ : c2++; }
  s1.querySelector(".c").textContent = c1; s2.querySelector(".c").textContent = c2;
  // order stamps drop in with a damped bounce
  const p1 = spring(t, T.o1, 2.0, 6.5), p2 = spring(t, T.o2, 2.0, 6.5);
  show(s1, seg(t, T.o1, T.o1 + 0.1), 0, 0, 1.5 - 0.5 * p1); show(s2, seg(t, T.o2, T.o2 + 0.1), 0, 0, 1.5 - 0.5 * p2);
  const n2 = t >= T.o2fill, sum = t >= T.sum;
  lab.innerHTML = `${O1.n}${n2 ? ` + ${O2.n}` : ""}${sum ? ` = ${S.total} ${S.unit}` : ""}`;
  const lk = seg(t, T.o1fill - 0.2, T.o1fill + 0.3, E.out); show(lab, lk); wipe(lab, lk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
