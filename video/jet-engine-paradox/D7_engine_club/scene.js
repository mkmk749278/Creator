import { THREE, Stage, PAL, E, K, seg, el, show, wipe, Callout } from "./jepd.js";
import { Globe, Marker } from "./globe.js";
const S = window.SCENE;
const st = new Stage({ bg: { glow: [0.58, 0.48], glowR: 0.75 }, dust: { count: 160, opacity: 0.35 } });
const gl = new Globe(st);
const ms = S.members.map((m) => ({ m, mk: new Marker(gl, m.at), c: new Callout(st.overlay, { title: m.name, sub: m.sub, side: m.side, dx: m.dx, dy: m.dy }) }));
const ind = new Marker(gl, S.india.at, { hollow: true, beam: 0 });
const lab = el(st.overlay, "jep-label", S.title);
function renderAt(t) {
  // north-Atlantic view holds USA, Britain, France and Russia; then the camera swings east for China, India appears empty
  const cam = K(t, [[0, [45, -40, 4.3]], [5.4, [52, -22, 3.55], E.sine], [8.9, [53, -14, 3.5], E.sine], [11.2, [40, 70, 3.7], E.inOut], [12.16, [38, 76, 3.6], E.out]]);
  gl.frame({ lat: cam[0], lon: cam[1], dist: cam[2], shiftX: 120, shiftY: 30 });
  for (const { m, mk, c } of ms) {
    const on = seg(t, m.t - 0.1, m.t + 0.35, E.out); mk.set(on, t - m.t);
    const s = gl.screen(mk.top); c.set(s.x, s.y, on * s.vis, seg(t, m.t, m.t + 0.55, E.out));
  }
  const io = seg(t, S.india.t, S.india.t + 0.8, E.out); ind.set(io * 0.8, -1);
  gl.spot(0, S.india.at, 13, PAL.amber, 0.7 * io);
  const lk = seg(t, S.t.title, S.t.title + 0.7, E.out); show(lab, lk); wipe(lab, lk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
