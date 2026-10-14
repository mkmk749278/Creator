import { THREE, Stage, E, seg, el, show, wipe } from "./jepd.js";
import { Panel, loadFonts, HEX, jetPath, JET_LEN, enginePath, strokeK, fillP } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.45], glowR: 0.9, grid: 0.022 }, dust: { count: 120, opacity: 0.3 } });
const pn = new Panel(st, { drift: [[0, [2, -4, 1.05]], [9.7, [-1.5, 4, 0.99], E.sine]] });
const l1 = el(st.overlay, "jep-label", ""), l2 = el(st.overlay, "jep-label", "");
Object.assign(l1.style, { left: "110px", bottom: "150px" }); Object.assign(l2.style, { left: "1050px", bottom: "150px" });
const EC = 11, ex0 = 150, ey0 = 215, EDX = 76, EDY = 64, ES = 62;
const eng = Array.from({ length: S.engines }, (_, i) => ({ x: ex0 + (i % EC) * EDX, y: ey0 + Math.floor(i / EC) * EDY, i }));
const JC = 6, jx0 = 1110, jy0 = 225, JDX = 108, JDY = 112, JS = 92;
const jets = Array.from({ length: S.jets }, (_, i) => ({ x: jx0 + (i % JC) * JDX, y: jy0 + Math.floor(i / JC) * JDY, i }));
const ELEN = 3.3;
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  const flash = Math.exp(-Math.pow((t - T.all99 - 0.3) / 0.35, 2));      // "ninety nine": every slot flashes once
  let sentNow = 0;
  for (const e of eng) {
    const p = enginePath(e.x, e.y, ES), d0 = T.draw0 + (e.i / S.engines) * (T.draw1 - T.draw0 - 0.4), dk = seg(t, d0, d0 + 0.4, E.out);
    const lit = e.i < S.sent ? seg(t, T.sent0 + (e.i / S.sent) * (T.sent1 - T.sent0), T.sent0 + (e.i / S.sent) * (T.sent1 - T.sent0) + 0.18, E.out) : 0;
    if (lit > 0.5) sentNow++;
    fillP(g, p, "#4a5262", 0.85 * seg(t, d0 + 0.15, d0 + 0.5, E.out) * (1 - lit));
    strokeK(g, p, ES * ELEN, dk, { w: 2, color: HEX.white, alpha: (0.5 + 0.5 * flash) * (1 - lit) });
    if (e.i >= S.sent) strokeK(k, p, ES * ELEN, dk, { w: 2, color: HEX.white, alpha: 0.4 * flash });
    fillP(g, p, HEX.amber, 0.9 * lit); fillP(k, p, HEX.amber, 0.3 * lit); strokeK(k, p, ES * ELEN, lit, { w: 2, color: HEX.hot, alpha: 0.9 });
  }
  for (const j of jets) {
    const p = jetPath(j.x, j.y, JS), d0 = T.jets0 + (j.i / S.jets) * (T.jets1 - T.jets0 - 0.35), dk = seg(t, d0, d0 + 0.35, E.out);
    strokeK(g, p, JS * JET_LEN, dk, { w: 2, color: HEX.line });
    const wait = 0.5 + 0.5 * Math.cos((t - T.jets1) * 2 * Math.PI * 0.9 + j.i * 0.4);   // grey jets "waiting": slow breathing
    fillP(g, p, "#596273", 0.95 * seg(t, d0 + 0.2, d0 + 0.6, E.out));
    strokeK(k, p, JS * JET_LEN, dk, { w: 2, color: HEX.white, alpha: 0.12 * wait * seg(t, T.jets1, T.jets1 + 0.5) });
  }
  pn.end(t);
  const a1 = seg(t, T.sent0 - 0.3, T.sent0 + 0.2, E.out); l1.innerHTML = S.engLabel.replace("{n}", sentNow); show(l1, a1); wipe(l1, a1);
  const nj = jets.filter((j) => t >= T.jets0 + (j.i / S.jets) * (T.jets1 - T.jets0 - 0.35) + 0.2).length;
  const a2 = seg(t, T.jets0 - 0.2, T.jets0 + 0.3, E.out); l2.innerHTML = S.jetLabel.replace("{n}", nj); show(l2, a2); wipe(l2, a2);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
