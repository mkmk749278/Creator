import { THREE, Stage, E, seg, el, show, wipe, lerp, mulberry32 } from "./jepd.js";
import { Panel, loadFonts, HEX, line, text } from "./kit.js";
const S = window.SCENE, T = S.t;
loadFonts();
const st = new Stage({ bg: { glow: [0.5, 0.45], glowR: 0.9 }, dust: { count: 90, opacity: 0.25 }, vignette: 0.35 });
const pn = new Panel(st, { drift: [[0, [1.5, -3, 1.03]], [10.49, [-0.5, 2, 1.0], E.sine]] });
let img = null;
if (S.photo) { const m = THREE.DefaultLoadingManager; m.itemStart(S.photo); img = new Image(); img.onload = img.onerror = () => m.itemEnd(S.photo); img.src = S.photo; }
// neutral placeholder plate (slate + grain + "PHOTO SLOT"), pre-rendered once
const ph = document.createElement("canvas"); ph.width = 1920; ph.height = 1080;
{ const x = ph.getContext("2d"), r = mulberry32(3), gr = x.createRadialGradient(960, 480, 100, 960, 540, 1100);
  gr.addColorStop(0, "#2a3140"); gr.addColorStop(1, "#0e121a"); x.fillStyle = gr; x.fillRect(0, 0, 1920, 1080);
  for (let i = 0; i < 60000; i++) { x.fillStyle = `rgba(255,255,255,${(r() * 0.05).toFixed(3)})`; x.fillRect(r() * 1920, r() * 1080, 2, 2); }
  x.strokeStyle = "rgba(248,250,252,0.25)"; x.lineWidth = 3; x.setLineDash([18, 12]); x.strokeRect(120, 90, 1680, 900);
  x.font = "800 72px Inter, Arial, sans-serif"; x.fillStyle = "rgba(248,250,252,0.35)"; x.textAlign = "center"; x.fillText("PHOTO SLOT", 960, 470); }
const lead = el(st.overlay, "jep-label", S.lead); Object.assign(lead.style, { bottom: "auto", top: "110px" });
const row = el(st.overlay, "jd-row", ""); Object.assign(row.style, { position: "absolute", left: "120px", top: "800px", display: "flex", alignItems: "center", gap: "22px" });
const arrs = [];
const chips = S.chips.map((c, i) => { if (i) arrs.push(el(row, "jd-arr", "→"));
  const e = el(row, "jd-chip", c); Object.assign(e.style, { position: "relative", fontSize: "34px" }); return e; });
arrs.forEach((a) => Object.assign(a.style, { font: "800 40px var(--font)", color: "var(--amber)" }));
const RY = 760, CX = [120, 590, 1060];
function renderAt(t) {
  pn.begin(); const g = pn.g, k = pn.k;
  // photo (or placeholder) with a slow push-in toward the focus point
  const src = img && img.naturalWidth ? img : ph, s = lerp(1.06, 1.16, t / S.duration);
  const iw = src.naturalWidth || src.width, ih = src.naturalHeight || src.height, cs = Math.max(1920 / iw, 1080 / ih) * s;
  const fx = S.focus[0] * iw * cs, fy = S.focus[1] * ih * cs, k2 = t / S.duration;
  g.drawImage(src, lerp(960 - iw * cs / 2, 960 - fx, k2 * 0.4), lerp(540 - ih * cs / 2, 540 - fy, k2 * 0.4), iw * cs, ih * cs);
  const sc = g.createLinearGradient(0, 560, 0, 1080); sc.addColorStop(0, "rgba(11,14,20,0)"); sc.addColorStop(1, "rgba(11,14,20,0.85)"); g.fillStyle = sc; g.fillRect(0, 560, 1920, 520);
  // years axis (no dates): ticks stream left during "decades, and many failures"
  const rk = seg(t, T.rail0, T.rail0 + 0.8, E.out), off = (Math.max(0, t - T.decades0) * 160) % 60;
  line(g, 120, RY, 120 + 1240 * rk, RY, { w: 3, color: HEX.white, alpha: 0.8 });
  for (let x = 120 + 60 - off; x < 120 + 1240 * rk; x += 60) line(g, x, RY - 8, x, RY + 8, { w: 2, color: HEX.white, alpha: 0.6 });
  const lit = [T.c0, T.c1, T.c2].map((c) => seg(t, c, c + 0.3, E.out));
  // progress along the rail to the newest lit chip
  const prog = lit[2] > 0 ? 1 : lit[1] > 0 ? lerp(0.38, 0.76, lit[1]) : lerp(0, 0.38, lit[0]);
  line(g, 120, RY, 120 + 1240 * prog, RY, { w: 6, color: HEX.amber }); line(k, 120, RY, 120 + 1240 * prog, RY, { w: 6, color: HEX.amber, alpha: 0.6 });
  pn.end(t);
  chips.forEach((c, i) => { show(c, lit[i]); wipe(c, lit[i]);
    const on = i === 2 ? 1 : 1 - 0.55 * (i === 0 ? lit[1] : lit[2]);   // earlier engines dim as China moves on
    c.style.opacity = (lit[i] * on).toFixed(3); c.style.borderColor = i === 0 ? "var(--dim)" : "var(--amber)"; });
  arrs.forEach((a, i) => show(a, lit[i + 1]));
  const lk = seg(t, T.lead, T.lead + 0.5, E.out); show(lead, lk); wipe(lead, lk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
