import { THREE, Stage, PAL, E, K, seg, el, show, wipe, Callout, col } from "./jepd.js";
import { Globe, Arc, Marker } from "./globe.js";
const S = window.SCENE, T = S.t;
const st = new Stage({ bg: { glow: [0.55, 0.5], glowR: 0.75 }, dust: { count: 160, opacity: 0.35 } });
const gl = new Globe(st);
const arc = new Arc(gl, S.from.at, S.to.at, { lift: 0.1 });
const mA = new Marker(gl, S.from.at), mB = new Marker(gl, S.to.at);
const cA = new Callout(st.overlay, { title: S.from.name, side: 1, dx: 70, dy: 70 });
const cB = new Callout(st.overlay, { title: S.to.name, side: -1, dx: 80, dy: -80 });
// shipping crate riding the arc: dark faces, amber edges
const crate = new THREE.Group(), cg = new THREE.BoxGeometry(0.05, 0.034, 0.034);
crate.add(new THREE.Mesh(cg, new THREE.MeshBasicMaterial({ color: col(0x2a2f3a) })));
crate.add(new THREE.LineSegments(new THREE.EdgesGeometry(cg), new THREE.LineBasicMaterial({ color: new THREE.Color(2.2, 0.8, 0.2) })));
const slat = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(0.05, 0.012, 0.0345)), new THREE.LineBasicMaterial({ color: new THREE.Color(1.4, 0.5, 0.12) }));
crate.add(slat); gl.group.add(crate);
// altitude test chamber icon (generic), struck through in red
const icon = el(st.overlay, "jd-icon", `<svg width="300" height="190" viewBox="0 0 300 190">
  <rect x="20" y="40" width="230" height="110" rx="55" fill="rgba(11,14,20,0.75)" stroke="#F8FAFC" stroke-width="5"/>
  <path d="M60 80 H170 L200 88 V102 L170 110 H60 Z M80 80 V110" fill="none" stroke="#94A3B8" stroke-width="4"/>
  <path d="M250 95 H285 M270 70 V120" stroke="#F8FAFC" stroke-width="5"/>
  <path class="x1" d="M30 20 L270 170" stroke="#EF4444" stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1"/>
  <path class="x2" d="M270 20 L30 170" stroke="#EF4444" stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1"/></svg>`);
icon.style.position = "absolute";
const x1 = icon.querySelector(".x1"), x2 = icon.querySelector(".x2");
const chip = el(st.overlay, "jd-chip", S.noFacility); chip.style.borderColor = "var(--red)";
const lab = el(st.overlay, "jep-label", S.route);
function renderAt(t) {
  const cam = K(t, [[0, [16, 82, 2.9]], [4.6, [19, 74, 2.7], E.sine], [7.4, [36, 58, 3.7], E.inOut], [8.88, [40, 52, 3.75], E.out]]);
  gl.frame({ lat: cam[0], lon: cam[1], dist: cam[2], shiftX: 120, shiftY: 0 });
  const pa = seg(t, T.bengaluru, T.bengaluru + 0.4, E.out), pb = seg(t, T.arc1 - 0.1, T.arc1 + 0.4, E.out);
  mA.set(pa, t - T.bengaluru); mB.set(pb, t - T.arc1);
  gl.spot(0, S.from.at, 14, PAL.amber, 0.6 * pa);
  const k = seg(t, T.arc0, T.arc1, E.inOut); arc.set(k);
  arc.head.material.opacity = 0;
  crate.visible = k > 0.01 && k < 0.995;
  const p = arc.point(k), q = arc.point(Math.min(1, k + 0.01)); crate.position.copy(p); crate.lookAt(q); crate.rotateY(Math.PI / 2);
  const sA = gl.screen(mA.top), sB = gl.screen(mB.top);
  cA.set(sA.x, sA.y, pa * sA.vis * (1 - seg(t, 6.8, 7.3)), seg(t, T.bengaluru, T.bengaluru + 0.6, E.out));
  cB.set(sB.x, sB.y, pb * sB.vis, seg(t, T.arc1, T.arc1 + 0.6, E.out));
  // chamber icon sits beside India, then lifts away as the route begins
  const ia = Math.min(seg(t, T.icon, T.icon + 0.4, E.out), 1 - seg(t, T.arc0 - 0.4, T.arc0));
  Object.assign(icon.style, { left: (sA.x - 560) + "px", top: (sA.y - 300) + "px" }); show(icon, ia, 0, 16 * (1 - ia));
  const c1 = seg(t, T.cross, T.cross + 0.25, E.out), c2 = seg(t, T.cross + 0.15, T.cross + 0.4, E.out);
  x1.setAttribute("stroke-dashoffset", (1 - c1).toFixed(3)); x2.setAttribute("stroke-dashoffset", (1 - c2).toFixed(3));
  Object.assign(chip.style, { left: (sA.x - 600) + "px", top: (sA.y - 90) + "px" });
  const ck = Math.min(seg(t, T.label, T.label + 0.4, E.out), 1 - seg(t, T.arc0 - 0.4, T.arc0)); show(chip, ck); wipe(chip, seg(t, T.label, T.label + 0.4, E.out));
  const lk = seg(t, T.routeLabel, T.routeLabel + 0.6, E.out); show(lab, lk); wipe(lab, lk);
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
