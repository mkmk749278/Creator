// jebTejas.js: procedural fighter (generic compound-delta light fighter, illustration) + hangar set for "The Blade That
// Should Melt". Nose = +Z, up = +Y, right = +X, units metres. Pure geometry, no textures except two tiny canvas maps.
import { THREE, mulberry32 } from "./jebA.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

// ---- canvas textures ---------------------------------------------------------------------------------------
export function panelTexture(seed = 5, size = 1024) {
  const c = document.createElement("canvas"); c.width = c.height = size; const g = c.getContext("2d"); const r = mulberry32(seed);
  g.fillStyle = "#808080"; g.fillRect(0, 0, size, size);
  g.strokeStyle = "#505050"; g.lineWidth = 2;
  for (let i = 0; i < 26; i++) { const x = r() * size, y = r() * size, w = 60 + r() * 260, h = 40 + r() * 180; g.strokeRect(x, y, w, h); }
  g.fillStyle = "#6f6f6f"; for (let i = 0; i < 160; i++) { g.fillRect(r() * size, r() * size, 2 + r() * 4, 2 + r() * 4); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.NoColorSpace; return t;
}
export function floorTexture(seed = 9) {
  const W = 1024, H = 2048, c = document.createElement("canvas"); c.width = W; c.height = H; const g = c.getContext("2d"); const r = mulberry32(seed);
  g.fillStyle = "#7d8187"; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 4200; i++) { const v = 100 + r() * 70; g.fillStyle = `rgba(${v},${v + 2},${v + 6},0.16)`; g.fillRect(r() * W, r() * H, 3 + r() * 26, 2 + r() * 14); }
  g.strokeStyle = "rgba(20,24,30,0.45)"; g.lineWidth = 3; for (let x = 0; x <= W; x += 256) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); }
  for (let y = 0; y <= H; y += 256) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
export function textDecal(text, { w = 1700, h = 256, font = "800 140px Inter", color = "#F8FAFC", bg = null } = {}) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  if (bg) { g.fillStyle = bg; g.fillRect(0, 0, w, h); }
  g.fillStyle = color; g.font = font; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, w / 2, h / 2);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// ---- loft ------------------------------------------------------------------------------------------------------
function loft(stations, nAng = 44, n = 2.4) {
  const pos = [], uv = [], idx = [];
  const e = 2 / n;
  stations.forEach((s, i) => {
    for (let k = 0; k <= nAng; k++) {
      const a = (k / nAng) * Math.PI * 2, ca = Math.cos(a), sa = Math.sin(a);
      const x = s.w * Math.sign(ca) * Math.pow(Math.abs(ca), e);
      const y = (s.yc || 0) + (sa >= 0 ? s.h : s.hb ?? s.h * 0.9) * Math.sign(sa) * Math.pow(Math.abs(sa), e);
      pos.push(x, y, s.z); uv.push(k / nAng, i / (stations.length - 1));
    }
  });
  for (let i = 0; i < stations.length - 1; i++) for (let k = 0; k < nAng; k++) {
    const a = i * (nAng + 1) + k, b = a + 1, c = a + nAng + 1, d = c + 1; idx.push(a, b, c, b, d, c);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals(); return g;
}
const planform = (pts, thick, bevel = 0.04) => {
  const s = new THREE.Shape(); pts.forEach(([x, z], i) => (i ? s.lineTo(x, -z) : s.moveTo(x, -z))); s.closePath();
  const g = new THREE.ExtrudeGeometry(s, { depth: thick, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 2 });
  g.rotateX(-Math.PI / 2); return g;   // shape (x, -z) -> world (x, ., z); thickness -> +Y
};

export const JET = { len: 13.4, span: 8.2, nozzleZ: -6.2, bayLen: 8.4, tubeR: 0.56 };

/** generic compound-delta light fighter. opts.detail 0..1 (gear, canopy, nozzle interior). */
export function makeJet({ detail = 1, seed = 1 } = {}) {
  const grp = new THREE.Group(); const air = new THREE.Group(); air.position.y = 1.62; grp.add(air);
  const paint = new THREE.MeshPhysicalMaterial({ color: 0x6c737c, roughness: 0.5, metalness: 0.2, clearcoat: 0.15, clearcoatRoughness: 0.5,
    bumpMap: panelTexture(seed), bumpScale: 1.2 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x14171c, roughness: 0.5, metalness: 0.4 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x0b1018, roughness: 0.04, metalness: 0.1, clearcoat: 1, clearcoatRoughness: 0.03, envMapIntensity: 2.2 });
  const radome = new THREE.MeshPhysicalMaterial({ color: 0x9aa195, roughness: 0.38, metalness: 0.05, clearcoat: 0.4 });
  // fuselage (nose +Z)
  const st = [
    { z: -6.2, w: 0.64, h: 0.64, yc: 0.0 }, { z: -5.7, w: 0.78, h: 0.8, yc: 0.02 }, { z: -4.6, w: 0.98, h: 0.98, yc: 0.06 },
    { z: -2.6, w: 1.12, h: 1.12, yc: 0.1 }, { z: -0.4, w: 1.16, h: 1.14, yc: 0.12 }, { z: 1.8, w: 1.04, h: 1.02, yc: 0.12 },
    { z: 3.4, w: 0.84, h: 0.84, yc: 0.1 }, { z: 4.8, w: 0.6, h: 0.6, yc: 0.06 }, { z: 5.9, w: 0.34, h: 0.34, yc: 0.02 }, { z: 6.7, w: 0.08, h: 0.08, yc: -0.02 },
  ];
  const fus = new THREE.Mesh(loft(st, 44), paint); air.add(fus);
  const nose = new THREE.Mesh(loft([{ z: 4.7, w: 0.62, h: 0.62, yc: 0.06 }, { z: 5.4, w: 0.5, h: 0.5, yc: 0.04 }, { z: 6.1, w: 0.26, h: 0.26, yc: 0.0 }, { z: 6.9, w: 0.0, h: 0.0, yc: -0.02 }], 36), radome);
  nose.scale.set(1.012, 1.012, 1); air.add(nose);
  // wings: compound delta
  const wingPts = [[0.8, 3.4], [2.7, 0.7], [4.1, -2.5], [4.1, -3.5], [0.8, -3.6]];
  const wL = new THREE.Mesh(planform(wingPts, 0.1), paint); wL.position.set(0, -0.2, 0); air.add(wL);
  const wR = new THREE.Mesh(planform(wingPts.map(([x, z]) => [-x, z]).reverse(), 0.1), paint); wR.position.set(0, -0.2, 0); air.add(wR);
  // wing-root strake blends
  const strake = new THREE.Mesh(planform([[0.4, 4.4], [1.2, 2.2], [0.9, 1.2], [0.2, 1.4]], 0.07), paint); strake.position.set(0, -0.06, 0); air.add(strake);
  const strakeR = strake.clone(); strakeR.scale.x = -1; air.add(strakeR);
  // intakes
  for (const sx of [-1, 1]) {
    const ib = new THREE.Mesh(loft([{ z: 0.4, w: 0.46, h: 0.34, yc: -0.28 }, { z: 1.6, w: 0.5, h: 0.4, yc: -0.3 }, { z: 2.8, w: 0.44, h: 0.42, yc: -0.26 }, { z: 3.5, w: 0.38, h: 0.36, yc: -0.2 }], 24, 3.2), paint);
    ib.position.x = sx * 0.98; air.add(ib);
    const mouth = new THREE.Mesh(new THREE.CircleGeometry(0.33, 20), dark); mouth.scale.set(1, 0.9, 1); mouth.position.set(sx * 0.98, -0.2, 3.52); air.add(mouth);
  }
  // canopy + spine
  const can = new THREE.Mesh(new THREE.SphereGeometry(1, 36, 20, 0, Math.PI * 2, 0, Math.PI / 2), glass); can.scale.set(0.56, 0.55, 1.5); can.position.set(0, 1.0, 3.05); air.add(can);
  const spine = new THREE.Mesh(loft([{ z: -4.8, w: 0.2, h: 0.2, yc: 1.0 }, { z: -2.4, w: 0.5, h: 0.4, yc: 1.18 }, { z: 0.2, w: 0.6, h: 0.45, yc: 1.2 }, { z: 1.8, w: 0.5, h: 0.36, yc: 1.22 }], 20), paint); air.add(spine);
  // vertical fin (tailless: single fin)
  const finG = (() => { const s = new THREE.Shape(); [[-5.7, 0.9], [-1.9, 1.1], [-4.1, 4.5], [-5.0, 4.5]].forEach(([z, y], i) => (i ? s.lineTo(z, y) : s.moveTo(z, y))); s.closePath();
    const g = new THREE.ExtrudeGeometry(s, { depth: 0.09, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 2 }); g.rotateY(-Math.PI / 2); g.translate(0.045, 0, 0); return g; })();
  air.add(new THREE.Mesh(finG, paint));
  // engine nozzle + hollow bay tunnel (the "empty tunnel" of the owner's script)
  const noz = new THREE.Group(); noz.position.set(0, 0.05, JET.nozzleZ);
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(0.66, 0.6, 0.9, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0x3b3e44, roughness: 0.5, metalness: 0.85, side: THREE.DoubleSide }));
  rim.rotation.x = Math.PI / 2; rim.position.z = -0.35; noz.add(rim);
  for (let i = 0; i < 18; i++) { const a = (i / 18) * Math.PI * 2; const p = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.015, 0.8), new THREE.MeshStandardMaterial({ color: 0x4a4c50, roughness: 0.4, metalness: 0.9 }));
    p.position.set(Math.cos(a) * 0.66, Math.sin(a) * 0.66, -0.7); p.rotation.z = a - Math.PI / 2; p.rotateX(0.0); noz.add(p); }
  air.add(noz);
  if (detail > 0.5) {
    const tube = new THREE.Mesh(new THREE.CylinderGeometry(JET.tubeR, JET.tubeR * 0.96, JET.bayLen, 36, 1, true),
      new THREE.MeshStandardMaterial({ color: 0x1b1d22, roughness: 0.6, metalness: 0.6, side: THREE.BackSide }));
    tube.rotation.x = Math.PI / 2; tube.position.set(0, 0.05, JET.nozzleZ + JET.bayLen / 2 - 0.2); air.add(tube);
    const ribMat = new THREE.MeshStandardMaterial({ color: 0x3d4047, roughness: 0.45, metalness: 0.85 });
    for (let i = 0; i < 9; i++) { const rib = new THREE.Mesh(new THREE.TorusGeometry(JET.tubeR * 0.97, 0.02, 8, 36), ribMat); rib.position.set(0, 0.05, JET.nozzleZ + 0.5 + i * 0.92); air.add(rib); }
    for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2 + 0.3; const pipe = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, JET.bayLen - 1.4, 8), ribMat);
      pipe.rotation.x = Math.PI / 2; pipe.position.set(Math.cos(a) * (JET.tubeR - 0.04), 0.05 + Math.sin(a) * (JET.tubeR - 0.04), JET.nozzleZ + JET.bayLen / 2 - 0.4); air.add(pipe); }
    const endwall = new THREE.Mesh(new THREE.CircleGeometry(JET.tubeR, 32), new THREE.MeshStandardMaterial({ color: 0x0a0b0d, roughness: 0.7, metalness: 0.3 }));
    endwall.position.set(0, 0.05, JET.nozzleZ + JET.bayLen - 0.35); endwall.rotation.y = Math.PI; air.add(endwall);
    // landing gear
    const gearMat = new THREE.MeshStandardMaterial({ color: 0xaab0b8, roughness: 0.35, metalness: 0.8 }); const tyre = new THREE.MeshStandardMaterial({ color: 0x0c0d0f, roughness: 0.9 });
    const gear = (x, z, h, r) => { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, h, 12), gearMat); s.position.set(x, r + h / 2, z); grp.add(s);
      const w = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.2, 24), tyre); w.rotation.z = Math.PI / 2; w.position.set(x, r, z); grp.add(w); };
    gear(0, 4.4, 0.95, 0.28); gear(-1.5, -0.6, 0.6, 0.34); gear(1.5, -0.6, 0.6, 0.34);
  }
  return grp;
}
