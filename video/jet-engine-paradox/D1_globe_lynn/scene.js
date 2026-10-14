import { THREE, Stage, PAL, E, K, seg, clamp, fmt, el, show, wipe, Callout } from "./jepd.js";
import { Globe, Arc, Marker, dir } from "./globe.js";
const S = window.SCENE, T = S.t;
const st = new Stage({ bg: { glow: [0.62, 0.5], glowR: 0.7 }, dust: { count: 160, opacity: 0.35 } });
const gl = new Globe(st);
const arc = new Arc(gl, S.from.at, S.to.at, { lift: 0.085 });
const mA = new Marker(gl, S.from.at), mB = new Marker(gl, S.to.at);
const cA = new Callout(st.overlay, { title: S.from.name, sub: S.from.sub, side: -1, dx: 80, dy: -70 });
const cB = new Callout(st.overlay, { title: S.to.name, sub: S.to.sub, side: 1, dx: 80, dy: -80 });
const big = el(st.overlay, "jd-big", `<span class="n"></span><small>${S.note}</small>`);
big.style.left = "96px"; big.style.top = "360px"; big.style.fontSize = "112px";
const num = big.querySelector(".n");
const lab = el(st.overlay, "jep-label", S.route);
gl.spot(0, S.to.at, 14, PAL.amber, 0);

function renderAt(t) {
  // camera: wide over the Atlantic, settle on New England for "Lynn", then travel with the arc to India
  const cam = K(t, [[0, [27, -38, 4.9]], [T.lynn + 0.3, [37, -62, 3.9], E.sine], [T.arc0 + 0.2, [38, -57, 3.95]],
    [6.6, [40, 15, 4.7], E.inOut], [8.22, [22, 62, 4.1], E.out]]);
  gl.frame({ lat: cam[0], lon: cam[1], dist: cam[2], shiftX: 330, shiftY: 0 });
  const pa = seg(t, T.lynn - 0.15, T.lynn + 0.45, E.out), pb = seg(t, T.arc1 - 0.15, T.arc1 + 0.4, E.out);
  mA.set(pa, t - T.lynn); mB.set(pb, t - T.arc1);
  gl.spot(0, S.to.at, 14, PAL.amber, 0.9 * pb);
  const k = seg(t, T.arc0, T.arc1, E.inOut);
  arc.set(k);
  const sA = gl.screen(mA.top), sB = gl.screen(mB.top);
  cA.set(sA.x, sA.y, pa * sA.vis, seg(t, T.lynn, T.lynn + 0.6, E.out));
  cB.set(sB.x, sB.y, pb * sB.vis, seg(t, T.arc1, T.arc1 + 0.6, E.out));
  // distance counter rides the arc; lands on "away"
  const kc = k;
  num.textContent = `${S.kmPrefix}${fmt(Math.round(S.km * kc / 100) * 100)} ${S.kmUnit}`;
  show(big, seg(t, T.count0 - 0.3, T.count0 + 0.2, E.out), 0, 12 * (1 - seg(t, T.count0 - 0.3, T.count0 + 0.3, E.out)));
  const lk = seg(t, T.arc0 + 0.2, T.arc0 + 0.8, E.out); show(lab, lk); wipe(lab, lk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
