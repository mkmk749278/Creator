import { THREE, Stage, PAL, E, K, seg, el, show, mulberry32 } from "./jepd.js";
import { Globe, Marker, lineMaterial } from "./globe.js";
const S = window.SCENE, T = S.t;
const st = new Stage({ bg: { glow: [0.66, 0.5], glowR: 0.7 }, dust: { count: 160, opacity: 0.35 } });
const gl = new Globe(st);
const pulses = S.nuclear.at.map((a) => new Marker(gl, a, { color: PAL.red, size: 0.06, beam: 0.07 }));
const rnd = mulberry32(5);
const orbits = Array.from({ length: S.orbit.count }, (_, i) => {
  const r = 1.12 + 0.022 * i, { u, mat } = lineMaterial(i % 3 ? PAL.amber : PAL.amberHot, 1.0);
  const m = new THREE.Mesh(new THREE.TorusGeometry(r, 0.0035, 6, 360), mat);
  m.rotation.set(Math.PI / 2 + (rnd() - 0.5) * 1.9, (rnd() - 0.5) * 1.2, rnd() * 6.28); gl.group.add(m);
  const sat = new THREE.Mesh(new THREE.SphereGeometry(0.012, 12, 8), new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 2.4, 1.6) })); m.add(sat);
  return { m, u, sat, r, t0: T.ten + i * ((T.orbits1 - T.ten) / S.orbit.count), sp: 0.5 + rnd() * 0.4, ph: rnd() * 6.28 };
});
const big1 = el(st.overlay, "jd-big", `<span class="n">${S.nuclear.n}</span><small>${S.nuclear.label}</small>`);
const big2 = el(st.overlay, "jd-big", `<span class="n" style="color:var(--amber)">${S.orbit.n}</span><small>${S.orbit.label}</small>`);
for (const b of [big1, big2]) Object.assign(b.style, { left: "120px", top: "330px", fontSize: "200px" });
function renderAt(t) {
  const cam = K(t, [[0, [30, 38, 5.0]], [5.71, [26, 62, 4.6], E.sine]]);
  gl.frame({ lat: cam[0], lon: cam[1], dist: cam[2], shiftX: 380, shiftY: 0 });
  pulses.forEach((p, i) => { const t0 = T.nine + 0.12 * i; p.set(seg(t, t0, t0 + 0.3, E.out) * (1 - 0.6 * seg(t, T.ten, T.ten + 0.6)), t - t0); });
  for (const o of orbits) { const k = seg(t, o.t0, o.t0 + 0.9, E.inOut); o.u.uProg.value = k; o.u.uInt.value = 1.0 * seg(t, o.t0, o.t0 + 0.1);
    const a = o.ph + k * 6.283 * 0.999 + (t - o.t0) * o.sp; o.sat.position.set(Math.cos(a) * o.r, Math.sin(a) * o.r, 0); o.sat.visible = k > 0.02 && t >= o.t0;
    if (k < 1) { const ah = k * 6.283; o.sat.position.set(Math.cos(ah) * o.r, Math.sin(ah) * o.r, 0); } }
  const a1 = Math.min(seg(t, T.nine - 0.2, T.nine + 0.3, E.out), 1 - seg(t, T.ten - 0.25, T.ten));
  const a2 = seg(t, T.ten, T.ten + 0.35, E.out);
  show(big1, a1, 0, -30 * seg(t, T.ten - 0.25, T.ten)); show(big2, a2, 0, 30 * (1 - a2));
  st.render(t);
}
window.addEventListener("hf-seek", (ev) => renderAt(ev.detail.time));
THREE.DefaultLoadingManager.onLoad = () => renderAt(window.__hfThreeTime || 0);
renderAt(window.__hfThreeTime || 0);
