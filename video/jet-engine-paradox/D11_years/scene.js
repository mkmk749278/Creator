import { THREE, Stage, E, seg, clamp } from "./jepd.js";
import { Panel, loadFonts, HEX, FONT } from "./kit.js";
const S = window.SCENE, T = S.t, N = S.to - S.from;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.42], glowR: 0.55, lift: 0x2a2620 }, dust: { count: 420, opacity: 0.65, size: 0.016, color: 0xffcf9a }, vignette: 0.45 });
const pn = new Panel(st, { drift: [[0, [4, -4, 1.1]], [3.6, [1, 3, 0.98], E.sine]] });
const CW = 250, CH = 340, GAP = 26, X0 = 960 - 2 * CW - 1.5 * GAP, Y0 = 540 - CH / 2;
function half(g, x, d, top, sy) {   // one half card of digit d, scaled about the hinge
  const hy = Y0 + CH / 2; g.save(); g.translate(0, hy); g.scale(1, sy); g.translate(0, -hy);
  g.beginPath(); top ? g.rect(x, Y0, CW, CH / 2 - 2) : g.rect(x, hy + 2, CW, CH / 2 - 2); g.clip();
  const gr = g.createLinearGradient(0, Y0, 0, Y0 + CH); gr.addColorStop(0, "#232a36"); gr.addColorStop(0.5, "#1a202b"); gr.addColorStop(1, "#141922");
  g.fillStyle = gr; g.fillRect(x, Y0, CW, CH);
  g.font = `800 280px ${FONT}`; g.fillStyle = HEX.white; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(String(d), x + CW / 2, hy + 12);
  const sh = Math.abs(1 - Math.abs(sy)); g.fillStyle = `rgba(0,0,0,${(0.6 * sh).toFixed(3)})`; g.fillRect(x, Y0, CW, CH);   // flap shading
  g.restore();
}
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  // warm work light from above
  const cone = g.createRadialGradient(960, 120, 20, 960, 520, 900); cone.addColorStop(0, "rgba(255,190,130,0.22)"); cone.addColorStop(1, "rgba(255,190,130,0)");
  g.fillStyle = cone; g.fillRect(0, 0, 1920, 1080);
  const step = (T.flip1 - T.flip0) / N, i = clamp(Math.floor((t - T.flip0) / step), -1, N - 1);
  const p = i < 0 ? 1 : clamp((t - T.flip0 - i * step) / T.flipDur), cur = S.from + Math.max(0, i) + (i >= 0 ? 1 : 0), prev = i < 0 ? S.from : cur - 1;
  const cs = String(cur).split(""), ps = String(prev).split("");
  for (let j = 0; j < 4; j++) {
    const x = X0 + j * (CW + GAP), a = +ps[j], b = +cs[j];
    if (a === b || p >= 1) { half(g, x, b, true, 1); half(g, x, b, false, 1); }
    else if (p < 0.5) { half(g, x, b, true, 1); half(g, x, a, false, 1); half(g, x, a, true, Math.cos(p * Math.PI)); }
    else { half(g, x, b, true, 1); half(g, x, a, false, 1); half(g, x, b, false, -Math.cos(p * Math.PI)); }
    g.fillStyle = "rgba(0,0,0,0.7)"; g.fillRect(x, Y0 + CH / 2 - 2, CW, 4);
  }
  k.save(); k.globalAlpha = 0.08; k.fillStyle = HEX.hot; k.fillRect(X0, Y0, 4 * CW + 3 * GAP, CH / 2); k.restore();
  pn.end(t); st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
