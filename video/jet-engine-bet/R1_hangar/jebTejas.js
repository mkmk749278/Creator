// jebTejas.js v2: procedural light fighter (generic compound-delta, single fin; illustration, not a manufacturer model) plus
// hangar texture helpers for "The Blade That Should Melt". Nose = +Z, up = +Y, right = +X, metres. Everything is
// deterministic (seeded). Realism pass after the independent review (review_R1_independent_v1.md): airfoil-section wing,
// teardrop canopy, cheek intakes, petal nozzle with heat gradient, irregular empty engine bay, panel/rivet atlas,
// proper landing gear and a fabric tag.
import { THREE, mulberry32 } from "./jebA.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

export const JET = { len: 13.4, span: 8.2, nozzleZ: -6.3, bayLen: 8.2, tubeR: 0.56, bodyY: 1.62 };
const sstep = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

// ---- canvas maps --------------------------------------------------------------------------------------------------
/** 2048 px panel atlas: gray bump/roughness map with panel lines, access doors, rivet rows, streaks. */
export function panelAtlas(seed = 5, size = 2048) {
  const c = document.createElement("canvas"); c.width = c.height = size; const g = c.getContext("2d"); const r = mulberry32(seed);
  g.fillStyle = "#8a8a8a"; g.fillRect(0, 0, size, size);
  // long streaks (airflow weathering)
  for (let i = 0; i < 320; i++) { const x = r() * size, y = r() * size, h = 80 + r() * 520, w = 1 + r() * 3; const a = 0.03 + r() * 0.06;
    g.fillStyle = r() > 0.5 ? `rgba(255,255,255,${a})` : `rgba(0,0,0,${a})`; g.fillRect(x, y, w, h); }
  // panel lines
  g.strokeStyle = "#3d3d3d"; g.lineWidth = 3;
  const vx = []; for (let x = 60; x < size; x += 150 + r() * 170) vx.push(x);
  const hy = []; for (let y = 50; y < size; y += 130 + r() * 190) hy.push(y);
  for (const x of vx) { const y0 = r() * size * 0.4, y1 = y0 + size * (0.35 + r() * 0.6); g.beginPath(); g.moveTo(x, y0); g.lineTo(x + (r() - 0.5) * 6, Math.min(size, y1)); g.stroke(); }
  for (const y of hy) { const x0 = r() * size * 0.4, x1 = x0 + size * (0.35 + r() * 0.6); g.beginPath(); g.moveTo(x0, y); g.lineTo(Math.min(size, x1), y + (r() - 0.5) * 6); g.stroke(); }
  // access doors with screws
  for (let i = 0; i < 34; i++) { const x = r() * (size - 260), y = r() * (size - 200), w = 70 + r() * 190, h = 50 + r() * 140;
    g.strokeStyle = "#2f2f2f"; g.lineWidth = 4; g.strokeRect(x, y, w, h);
    g.fillStyle = "#c8c8c8"; for (let sx = x + 10; sx < x + w - 6; sx += 22) { g.fillRect(sx, y + 8, 4, 4); g.fillRect(sx, y + h - 12, 4, 4); }
    for (let sy = y + 18; sy < y + h - 12; sy += 22) { g.fillRect(x + 8, sy, 4, 4); g.fillRect(x + w - 12, sy, 4, 4); } }
  // rivet rows along some panel lines
  g.fillStyle = "#b4b4b4"; for (const x of vx) { if (r() < 0.6) continue; for (let y = 20; y < size; y += 16) g.fillRect(x + 7, y, 3, 3); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.NoColorSpace; t.anisotropy = 8; t.generateMipmaps = true; return t;
}
export function textDecal(text, { w = 1700, h = 256, font = "800 140px Inter", color = "#F8FAFC", bg = null } = {}) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  if (bg) { g.fillStyle = bg; g.fillRect(0, 0, w, h); }
  g.fillStyle = color; g.font = font; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, w / 2, h / 2);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
export function radialTex(stops, size = 128) {
  const c = document.createElement("canvas"); c.width = c.height = size; const g = c.getContext("2d"); const gr = g.createRadialGradient(size / 2, size / 2, 2, size / 2, size / 2, size / 2 - 1);
  stops.forEach(([p, col]) => gr.addColorStop(p, col)); g.fillStyle = gr; g.fillRect(0, 0, size, size); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// ---- geometry helpers -----------------------------------------------------------------------------------------------
function loft(stations, nAng = 48, n = 2.5, colorFn = null) {
  const pos = [], uv = [], idx = [], col = [];
  const e = 2 / n;
  stations.forEach((s, i) => {
    for (let k = 0; k <= nAng; k++) {
      const a = (k / nAng) * Math.PI * 2, ca = Math.cos(a), sa = Math.sin(a);
      const x = s.w * Math.sign(ca) * Math.pow(Math.abs(ca), e);
      const y = (s.yc || 0) + (sa >= 0 ? s.h : s.hb ?? s.h * 0.92) * Math.sign(sa) * Math.pow(Math.abs(sa), e);
      pos.push(x, y, s.z); uv.push((k / nAng) * 2, (s.z + 7) / 4);
      if (colorFn) col.push(...colorFn(s.z, x, y));
    }
  });
  for (let i = 0; i < stations.length - 1; i++) for (let k = 0; k < nAng; k++) { const a = i * (nAng + 1) + k, b = a + 1, c = a + nAng + 1, d = c + 1; idx.push(a, b, c, b, d, c); }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  if (colorFn) g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  g.setIndex(idx); g.computeVertexNormals(); return g;
}
/** airfoil-section wing from a planform (x = span from root, z = chord line). sign mirrors left/right. */
function wingGeometry(sign, { LE = [[0.8, 3.3], [2.6, 0.4], [4.1, -2.7]], TE = [[0.8, -3.8], [4.1, -3.8]], t = 0.05, ns = 22, nu = 26 } = {}) {
  const interp = (poly, x) => { for (let i = 0; i < poly.length - 1; i++) if (x <= poly[i + 1][0] + 1e-6) { const f = (x - poly[i][0]) / (poly[i + 1][0] - poly[i][0]); return poly[i][1] + (poly[i + 1][1] - poly[i][1]) * f; } return poly[poly.length - 1][1]; };
  const x0 = LE[0][0], x1 = LE[LE.length - 1][0];
  const pos = [], uv = [], idx = []; const rows = ns + 1, cols = nu + 1;
  for (const surf of [1, -1]) {
    for (let i = 0; i <= ns; i++) {
      const s = i / ns, x = x0 + (x1 - x0) * s, zle = interp(LE, x), zte = interp(TE, x), c = zle - zte;
      for (let j = 0; j <= nu; j++) {
        const u = 0.5 - 0.5 * Math.cos((j / nu) * Math.PI);   // cosine spacing: dense at LE and TE
        const yt = 5 * t * c * (0.2969 * Math.sqrt(u) - 0.126 * u - 0.3516 * u * u + 0.2843 * u ** 3 - 0.1015 * u ** 4) * (1 - 0.5 * s);
        pos.push(sign * x, surf * yt - 0.035 * x, zle + (zte - zle) * u); uv.push(s * 2, u * 2);
      }
    }
  }
  const base = rows * cols;
  for (const off of [0, base]) for (let i = 0; i < ns; i++) for (let j = 0; j < nu; j++) { const a = off + i * cols + j, b = a + 1, c = a + cols, d = c + 1; idx.push(a, b, c, b, d, c); }
  // close LE/tip/TE seams cheaply: top and bottom share the chord ends (u=0,1) so only the tip needs a cap
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g;
}
function petalSet(Rb, len, count, seed, shade) {
  const r = mulberry32(seed); const pos = [], idx = [], col = []; const NV = 10, NW = 4;
  const radiusAt = (v) => (v < 0.5 ? Rb - (Rb - 0.5) * sstep(0, 0.5, v) : 0.5 + (0.6 - 0.5) * sstep(0.5, 1, v));
  const steel = new THREE.Color(0x4a4c50), bronze = new THREE.Color(0x6a4a2c), blue = new THREE.Color(0x32385a);
  for (let p = 0; p < count; p++) {
    const a0 = (p / count) * Math.PI * 2, half = (Math.PI / count) * 0.96, jitter = (r() - 0.5) * 0.02;
    const base = pos.length / 3;
    for (let vi = 0; vi <= NV; vi++) { const v = vi / NV; const rad = radiusAt(v) + shade;
      for (let wi = 0; wi <= NW; wi++) { const w = (wi / NW) * 2 - 1; const ang = a0 + w * half * (1 - 0.18 * v) + jitter;
        pos.push(Math.cos(ang) * rad, Math.sin(ang) * rad, -v * len);
        const c = steel.clone().lerp(bronze, sstep(0.25, 0.7, v)).lerp(blue, sstep(0.65, 1.0, v)); const k = 0.82 + 0.3 * r() * 0.3; col.push(c.r * k, c.g * k, c.b * k); } }
    for (let vi = 0; vi < NV; vi++) for (let wi = 0; wi < NW; wi++) { const a = base + vi * (NW + 1) + wi, b = a + 1, c = a + NW + 1, d = c + 1; idx.push(a, b, c, b, d, c); }
  }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3)); g.setIndex(idx); g.computeVertexNormals(); return g;
}

// shared materials (clone-safe: created once per page)
let M = null;
function mats(seed) {
  if (M) return M;
  const atlas = panelAtlas(seed);
  const grey = new THREE.Color(0x737b84), olive = new THREE.Color(0x4b5048);
  M = {
    grey, olive,
    paint: new THREE.MeshPhysicalMaterial({ color: 0xffffff, vertexColors: true, roughness: 0.62, metalness: 0.1, clearcoat: 0.22, clearcoatRoughness: 0.4, bumpMap: atlas, bumpScale: 1.6, roughnessMap: atlas, envMapIntensity: 0.9 }),
    paintFlat: new THREE.MeshPhysicalMaterial({ color: grey, roughness: 0.62, metalness: 0.1, clearcoat: 0.22, clearcoatRoughness: 0.4, bumpMap: atlas, bumpScale: 1.6, roughnessMap: atlas, envMapIntensity: 0.55, side: THREE.DoubleSide }),
    dark: new THREE.MeshStandardMaterial({ color: 0x0d0e11, roughness: 0.7, metalness: 0.3 }),
    glass: new THREE.MeshPhysicalMaterial({ color: 0x0b0f16, roughness: 0.03, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.02, envMapIntensity: 3.2, reflectivity: 0.9 }),
    frame: new THREE.MeshStandardMaterial({ color: 0x23262b, roughness: 0.5, metalness: 0.6 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0x9aa0a8, roughness: 0.3, metalness: 0.9 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x0b0b0c, roughness: 0.92, metalness: 0.0 }),
    metalDull: new THREE.MeshStandardMaterial({ color: 0x3a3c40, roughness: 0.62, metalness: 0.8, bumpMap: atlas, bumpScale: 0.8 }),
    petal: new THREE.MeshStandardMaterial({ color: 0xffffff, vertexColors: true, roughness: 0.55, metalness: 0.85, side: THREE.DoubleSide, bumpMap: atlas, bumpScale: 0.6 }),
    bay: new THREE.MeshStandardMaterial({ color: 0x1d1e22, roughness: 0.72, metalness: 0.6, side: THREE.DoubleSide, bumpMap: atlas, bumpScale: 1.2 }),
    tag: new THREE.MeshStandardMaterial({ color: 0xd8321c, roughness: 0.85, side: THREE.DoubleSide, emissive: 0x2a0905 }),
  };
  return M;
}

/** generic compound-delta light fighter. detail 0..1: >0.5 adds landing gear, the hollow engine bay and the nozzle petals. */
export function makeJet({ detail = 1, seed = 1 } = {}) {
  const m = mats(seed);
  const grp = new THREE.Group(); const air = new THREE.Group(); air.position.y = JET.bodyY; grp.add(air);
  const add = (mesh) => { air.add(mesh); return mesh; };
  // fuselage with a vertex-colour paint scheme: grey with a dark olive radome that blends over 0.5 m (no hard seam)
  const stations = [
    { z: -6.3, w: 0.66, h: 0.66, yc: 0.02 }, { z: -5.8, w: 0.8, h: 0.8, yc: 0.04 }, { z: -4.6, w: 1.0, h: 0.98, yc: 0.08 }, { z: -2.6, w: 1.14, h: 1.1, yc: 0.1 },
    { z: -0.4, w: 1.18, h: 1.12, yc: 0.12 }, { z: 1.8, w: 1.04, h: 1.0, yc: 0.12 }, { z: 3.3, w: 0.8, h: 0.8, yc: 0.1 }, { z: 4.4, w: 0.58, h: 0.58, yc: 0.07 },
    { z: 5.3, w: 0.4, h: 0.4, yc: 0.04 }, { z: 6.1, w: 0.22, h: 0.22, yc: 0.0 }, { z: 6.7, w: 0.06, h: 0.06, yc: -0.03 },
  ];
  const fusGeo = loft(stations, 52, 2.5, (z) => { const k = sstep(4.0, 4.5, z); const c = m.grey.clone().lerp(m.olive, k); return [c.r, c.g, c.b]; });
  add(new THREE.Mesh(fusGeo, m.paint));
  // wings (airfoil section, anhedral), wing-root strakes
  add(new THREE.Mesh(wingGeometry(1), m.paintFlat)).position.y = -0.2; add(new THREE.Mesh(wingGeometry(-1), m.paintFlat)).position.y = -0.2;
  const strake = (s) => { const g = wingGeometry(s, { LE: [[0.3, 4.6], [1.3, 2.4]], TE: [[0.3, 1.2], [1.3, 1.2]], t: 0.035, ns: 6, nu: 12 }); const me = new THREE.Mesh(g, m.paintFlat); me.position.y = -0.04; return me; };
  add(strake(1)); add(strake(-1));
  // cheek intakes with lips and dark throats
  for (const sx of [-1, 1]) {
    const ib = new THREE.Mesh(new RoundedBoxGeometry(0.74, 0.62, 2.7, 4, 0.2), m.paintFlat); ib.position.set(sx * 0.98, -0.2, 1.85); add(ib);
    const lip = new THREE.Mesh(new RoundedBoxGeometry(0.8, 0.68, 0.14, 4, 0.22), m.chrome); lip.position.set(sx * 0.98, -0.2, 3.25); add(lip);
    const th = new THREE.Mesh(new THREE.CircleGeometry(0.3, 24), new THREE.MeshBasicMaterial({ map: radialTex([[0, "#000"], [0.7, "#050506"], [1, "#16181b"]]) })); th.scale.set(1, 0.9, 1); th.position.set(sx * 0.98, -0.2, 3.33); add(th);
  }
  // canopy: teardrop glass, frame arcs, sill
  const cg = new THREE.SphereGeometry(1, 48, 28, 0, Math.PI * 2, 0, Math.PI / 2); { const p = cg.attributes.position; for (let i = 0; i < p.count; i++) { const z = p.getZ(i); p.setZ(i, z * (z > 0 ? 1.7 : 1.05)); p.setY(i, p.getY(i) * (1 - 0.22 * Math.max(0, z))); } cg.computeVertexNormals(); }
  const can = new THREE.Mesh(cg, m.glass); can.scale.set(0.5, 0.52, 1.32); can.position.set(0, 1.0, 2.55); add(can);
  for (const [z, s] of [[1.55, 0.97], [2.55, 1.05], [3.5, 0.62]]) { const arc = new THREE.Mesh(new THREE.TorusGeometry(0.5, 0.022, 8, 28, Math.PI), m.frame); arc.scale.set(s, 1.04, 1); arc.position.set(0, 1.0, z); add(arc); }
  const sill = new THREE.Mesh(new RoundedBoxGeometry(1.08, 0.06, 3.5, 2, 0.02), m.frame); sill.position.set(0, 0.98, 2.4); add(sill);
  const spine = new THREE.Mesh(loft([{ z: -5.2, w: 0.18, h: 0.16, yc: 0.98 }, { z: -3.0, w: 0.5, h: 0.4, yc: 1.16 }, { z: -0.6, w: 0.62, h: 0.44, yc: 1.2 }, { z: 1.2, w: 0.5, h: 0.34, yc: 1.2 }, { z: 1.7, w: 0.3, h: 0.2, yc: 1.12 }], 28, 2.6), m.paintFlat); add(spine);
  // fin (swept, section), pitot boom, antennae, sensor blisters
  const fin = (() => { const s = new THREE.Shape(); [[-5.9, 0.9], [-2.2, 1.2], [-3.9, 4.7], [-5.1, 4.7]].forEach(([z, y], i) => (i ? s.lineTo(z, y) : s.moveTo(z, y))); s.closePath();
    const g = new THREE.ExtrudeGeometry(s, { depth: 0.1, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 3 }); g.rotateY(-Math.PI / 2); g.translate(0.05, 0, 0); return g; })();
  add(new THREE.Mesh(fin, m.paintFlat));
  const pitot = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.02, 1.0, 8), m.chrome); pitot.rotation.x = Math.PI / 2; pitot.position.set(0, -0.02, 7.1); add(pitot);
  for (const [x, y, z, w, h, d] of [[0, 1.3, -1.0, 0.04, 0.22, 0.34], [0.3, -0.95, 0.6, 0.04, 0.2, 0.3], [-0.5, 1.25, -3.6, 0.04, 0.18, 0.28], [0, 3.7, -5.4, 0.08, 0.4, 0.5]]) { const a = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m.frame); a.position.set(x, y, z); a.rotation.x = 0.2; add(a); }
  const blister = new THREE.Mesh(new THREE.SphereGeometry(0.13, 14, 10), m.dark); blister.scale.set(1, 0.6, 1.4); blister.position.set(0, -1.06, 2.2); add(blister);
  // nozzle: 16 master petals + 16 seals with a heat gradient, base ring and actuators
  const noz = new THREE.Group(); noz.position.set(0, 0.04, JET.nozzleZ + 0.05); add(noz);
  noz.add(new THREE.Mesh(petalSet(0.66, 0.95, 16, seed + 1, 0.0), m.petal)); noz.add(new THREE.Mesh(petalSet(0.66, 0.92, 16, seed + 2, -0.014), m.petal));
  noz.children[1].rotation.z = Math.PI / 16;
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.67, 0.035, 10, 44), m.metalDull); noz.add(ring);
  for (let i = 0; i < 8; i++) { const a = (i / 8) * Math.PI * 2 + 0.2; const act = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.5, 8), m.chrome); act.rotation.x = Math.PI / 2; act.position.set(Math.cos(a) * 0.74, Math.sin(a) * 0.74, 0.22); noz.add(act); }
  if (detail > 0.5) {
    // the empty engine bay: irregular lathe wall, rails, uneven frames, cable looms, bulkhead with bolts, mount bracket, tag
    const r = mulberry32(seed + 30); const prof = [];
    for (let i = 0; i <= 40; i++) { const z = JET.nozzleZ + 0.1 + (i / 40) * JET.bayLen; prof.push(new THREE.Vector2(JET.tubeR + 0.035 * Math.sin(z * 2.3) + 0.03 * (r() - 0.5) + 0.04 * sstep(JET.bayLen - 1.5, JET.bayLen, z - JET.nozzleZ), z)); }
    const bayG = new THREE.LatheGeometry(prof, 40); bayG.rotateX(Math.PI / 2);
    const bay = new THREE.Mesh(bayG, m.bay); bay.position.y = 0.04; add(bay);
    for (const ang of [Math.PI * 0.62]) { const rail = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.09, JET.bayLen - 1.2), m.metalDull); rail.position.set(Math.cos(ang) * 0.51, 0.04 + Math.sin(ang) * 0.51, JET.nozzleZ + JET.bayLen / 2); rail.rotation.z = ang + Math.PI / 2; add(rail); }
    let zf = JET.nozzleZ + 0.7; while (zf < JET.nozzleZ + JET.bayLen - 0.5) { const th = 0.012 + r() * 0.03; const f = new THREE.Mesh(new THREE.TorusGeometry(JET.tubeR * 0.985, th, 8, 40), m.metalDull); f.position.set(0, 0.04, zf); add(f); zf += 0.35 + r() * 1.2; }
    for (let k = 0; k < 4; k++) { const pts = []; const ang0 = Math.PI * (1.45 + 0.07 * k); for (let i = 0; i < 8; i++) { const z = JET.nozzleZ + 0.8 + (i / 7) * (JET.bayLen - 1.6); const a = ang0 + 0.1 * Math.sin(i * 1.3 + k); pts.push(new THREE.Vector3(Math.cos(a) * (JET.tubeR - 0.045), 0.04 + Math.sin(a) * (JET.tubeR - 0.045), z)); }
      add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, 0.011 + 0.003 * k, 6), m.rubber)); }
    const zEnd = JET.nozzleZ + JET.bayLen - 0.3;
    const bulk = new THREE.Mesh(new THREE.CircleGeometry(JET.tubeR + 0.03, 40), new THREE.MeshStandardMaterial({ color: 0x0a0a0c, roughness: 0.8, metalness: 0.4, bumpMap: m.metalDull.bumpMap, bumpScale: 1.0 })); bulk.position.set(0, 0.04, zEnd); bulk.rotation.y = Math.PI; add(bulk);
    const bolt = new THREE.CylinderGeometry(0.014, 0.014, 0.02, 8); for (let i = 0; i < 28; i++) { const a = (i / 28) * Math.PI * 2 + 0.05; const b = new THREE.Mesh(bolt, m.chrome); b.rotation.x = Math.PI / 2; b.position.set(Math.cos(a) * 0.46, 0.04 + Math.sin(a) * 0.46, zEnd - 0.012); add(b); }
    const br1 = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.07, 0.22), m.metalDull); br1.position.set(0.04, 0.04 - 0.34, zEnd - 0.12); add(br1);
    const br2 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.2, 0.18), m.metalDull); br2.position.set(-0.05, 0.04 - 0.24, zEnd - 0.12); add(br2);
    const pipe = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.4, 10), m.chrome); pipe.rotation.z = Math.PI / 2; pipe.position.set(0.22, 0.04 + 0.12, zEnd - 0.2); add(pipe);
    const tagIn = new THREE.Mesh(new THREE.PlaneGeometry(0.1, 0.26, 1, 3), m.tag); tagIn.position.set(0.04, 0.04 - 0.46, zEnd - 0.24); tagIn.rotation.set(0.25, 0.4, 0.1); add(tagIn);
  }
  {
    // landing gear (ground-referenced: group coordinates, not air)
    const strut = (x, z, h, r, th) => {
      const up = new THREE.Mesh(new THREE.CylinderGeometry(th, th * 1.12, h * 0.55, 14), m.chrome); up.position.set(x, r + h * 0.72, z); grp.add(up);
      const lo = new THREE.Mesh(new THREE.CylinderGeometry(th * 0.7, th * 0.7, h * 0.5, 12), m.chrome); lo.position.set(x, r + h * 0.28, z); grp.add(lo);
      const tyre = new THREE.Mesh(new THREE.TorusGeometry(r - 0.085, 0.085, 14, 32), m.rubber); tyre.rotation.y = Math.PI / 2; tyre.position.set(x, r, z); grp.add(tyre);
      const hub = new THREE.Mesh(new THREE.CylinderGeometry(r - 0.12, r - 0.12, 0.13, 20), m.metalDull); hub.rotation.z = Math.PI / 2; hub.position.set(x, r, z); grp.add(hub);
      const link = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.2, 0.025), m.chrome); link.position.set(x + 0.07, r + h * 0.5, z); link.rotation.z = 0.35; grp.add(link);
    };
    strut(0, 4.4, 0.95, 0.27, 0.055); strut(-1.5, -0.6, 0.72, 0.34, 0.062); strut(1.5, -0.6, 0.72, 0.34, 0.062);
    for (const sx of [-1, 1]) { const door = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.5, 0.9), m.paintFlat); door.position.set(sx * 1.52, 0.9, -0.6); door.rotation.z = sx * 0.12; grp.add(door); }
  }
  return grp;
}
