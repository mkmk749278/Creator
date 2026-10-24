// jepA.js: Session A's shared 3D world for "The Jet Engine Paradox" ("The Hot Section", thermal world).
// One procedural model set (HP turbine blade, disc, nozzle guide vanes, combustor, cutaway turbofan) plus the
// render stack (HDRI, bloom on hot parts, heat shimmer, film grain, ACES) reused by every Session A scene, so the
// science sequence reads as one continuous world. Master copy: video/jet-engine-paradox/_libA/jepA.js; `sync.sh`
// copies it into each scene folder. Everything is a pure function of time t (seeded RNG, no clocks, no stepped state).
import * as THREE from "three";
import { HDRLoader } from "three/addons/loaders/HDRLoader.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import {
  EffectComposer, RenderPass, EffectPass, BloomEffect, ToneMappingEffect, ToneMappingMode, VignetteEffect, Effect, FXAAEffect,
  DepthOfFieldEffect, EffectAttribute, VignetteTechnique,
} from "postprocessing";
import { N8AOPostPass } from "n8ao";

export { THREE };

// ---------------------------------------------------------------------------------------------------------------
// Math helpers (all pure)
export const mulberry32 = (s) => () => {
  s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const sstep = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
export const ease = {
  inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  inOut2: (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  out: (t) => 1 - Math.pow(1 - t, 3),
  out5: (t) => 1 - Math.pow(1 - t, 5),
  in: (t) => t * t * t,
  in2: (t) => t * t,
  lin: (t) => t,
};
/** eased progress of t through [a, b] */
export const seg = (t, a, b, fn = ease.inOut) => fn(clamp((t - a) / (b - a)));
/** smooth deterministic wobble (sum of sines), amplitude ~1 */
export const wob = (t, s = 0) => 0.5 * Math.sin(t * 0.73 + s * 1.7) + 0.3 * Math.sin(t * 1.31 + s * 4.1) + 0.2 * Math.sin(t * 2.17 + s * 2.3);

// World dimensions (engine axis = +Z, flow direction; blade local frame: Y radial, Z axial, X tangential)
export const DIM = { R: 1.05, H: 0.40, N: 48, chord: 0.27 };

// ---------------------------------------------------------------------------------------------------------------
// GLSL shared: ironbow thermal ramp (sRGB stops, also used by the HTML scales), blackbody glow, noise
export const IRONBOW_STOPS = [
  [0.0, "#05030f"], [0.14, "#1d0b5a"], [0.3, "#5a0f8c"], [0.46, "#a8155e"], [0.6, "#e0401e"],
  [0.74, "#f88a12"], [0.87, "#fcd34d"], [1.0, "#fffbea"],
];
const hexToLin = (h) => { const c = new THREE.Color(h); return c; }; // THREE.Color(hex) converts sRGB -> linear
const IRONBOW_GLSL = (() => {
  const s = IRONBOW_STOPS.map(([p, h]) => { const c = hexToLin(h); return [p, c.r, c.g, c.b]; });
  let code = "vec3 ironbow(float x){ x = clamp(x, 0.0, 1.0);\n";
  for (let i = 0; i < s.length - 1; i++) {
    const [p0, r0, g0, b0] = s[i], [p1, r1, g1, b1] = s[i + 1];
    code += `  if (x <= ${p1.toFixed(4)}) return mix(vec3(${r0.toFixed(5)},${g0.toFixed(5)},${b0.toFixed(5)}), vec3(${r1.toFixed(5)},${g1.toFixed(5)},${b1.toFixed(5)}), (x - ${p0.toFixed(4)}) / ${(p1 - p0).toFixed(4)});\n`;
  }
  const l = s[s.length - 1];
  return code + `  return vec3(${l[1].toFixed(5)},${l[2].toFixed(5)},${l[3].toFixed(5)});\n}\n`;
})();
export const GLSL_COMMON = `
${IRONBOW_GLSL}
// temperature (0 cold .. 1 = alloy melting point .. 1.25 top of scale) -> ironbow ramp position
vec3 thermalColor(float T){ return ironbow(T / 1.25); }
// blackbody-ish glow for "hot metal" look: k in 0..1
vec3 blackbody(float k){ k = clamp(k, 0.0, 1.2);
  return vec3(1.0, 0.12 + 0.55 * smoothstep(0.45, 1.05, k), 0.02 + 0.5 * smoothstep(0.85, 1.2, k)) * (k * k); }
float hash13(vec3 p){ p = fract(p * 0.1031); p += dot(p, p.zyx + 31.32); return fract((p.x + p.y) * p.z); }
float vnoise(vec3 p){ vec3 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(hash13(i), hash13(i + vec3(1,0,0)), f.x), mix(hash13(i + vec3(0,1,0)), hash13(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hash13(i + vec3(0,0,1)), hash13(i + vec3(1,0,1)), f.x), mix(hash13(i + vec3(0,1,1)), hash13(i + vec3(1,1,1)), f.x), f.y), f.z); }
float fbm(vec3 p){ float a = 0.5, s = 0.0; for (int i = 0; i < 4; i++){ s += a * vnoise(p); p = p * 2.03 + 7.1; a *= 0.5; } return s; }
`;

// Temperature fields (normalised: 1.0 = alloy melting point). The metal always stays below 1 (it is cooled);
// only the gas goes above it. Proportions follow the fact-check note (gas ~1.15, metal ~0.72 of the melt line).
const TEMP_BLADE = `
float filmMask(vec2 uv){
  float v = uv.y, u = uv.x, m = 0.0;
  float streak = 0.75 + 0.25 * cos(v * 6.2831 * 15.0);
  // showerhead rows at the leading edge (u = 0.5) wash both sides
  float dp = 0.47 - u; m += step(0.0, dp) * exp(-dp / 0.10);
  float ds = u - 0.53; m += step(0.0, ds) * exp(-ds / 0.09);
  // pressure-side rows (flow toward u = 0) and one suction-side row (flow toward u = 1)
  float d1 = 0.31 - u; m += 0.8 * step(0.0, d1) * exp(-d1 / 0.10);
  float d2 = 0.19 - u; m += 0.8 * step(0.0, d2) * exp(-d2 / 0.10);
  float d3 = u - 0.70; m += 0.7 * step(0.0, d3) * exp(-d3 / 0.12);
  return clamp(m * streak, 0.0, 1.0) * smoothstep(0.0, 0.06, v);
}
float tempField(vec3 p, vec2 uv, float part){
  if (part < 0.5) {             // airfoil
    float span = clamp(p.y / ${DIM.H.toFixed(3)}, 0.0, 1.0);
    float le = exp(-pow((uv.x - 0.5) / 0.08, 2.0));
    float te = exp(-pow(min(uv.x, 1.0 - uv.x) / 0.07, 2.0));
    float prof = 1.0 - 0.35 * pow(abs(span - 0.6) / 0.6, 2.0);
    float T = 0.56 + 0.10 * prof + 0.09 * le + 0.07 * te + 0.05 * smoothstep(0.82, 1.0, span);
    return T - 0.035 * filmMask(uv) + 0.012 * (vnoise(p * vec3(30.0, 8.0, 30.0)) - 0.5);
  }
  if (part < 1.5) return 0.50 + 0.02 * (vnoise(p * 50.0) - 0.5);   // platform
  if (part < 2.5) return mix(0.16, 0.44, smoothstep(-0.30, -0.02, p.y)); // shank + fir-tree root
  return 0.74;                                                       // squealer tip
}`;
const TEMP_DISC = `float filmMask(vec2 uv){ return 0.0; }
float tempField(vec3 p, vec2 uv, float part){ float r = length(p.xy); return mix(0.12, 0.40, smoothstep(0.3, 0.95, r)); }`;
const TEMP_VANE = `float filmMask(vec2 uv){ return 0.0; }
float tempField(vec3 p, vec2 uv, float part){ return 0.70 + 0.05 * sin(uv.y * 3.14159) + 0.03 * (vnoise(p * 40.0) - 0.5); }`;
const TEMP_CONST = (v) => `float filmMask(vec2 uv){ return 0.0; } float tempField(vec3 p, vec2 uv, float part){ return ${v.toFixed(3)}; }`;
export const TEMP = { blade: TEMP_BLADE, disc: TEMP_DISC, vane: TEMP_VANE, const: TEMP_CONST };

// ---------------------------------------------------------------------------------------------------------------
// Procedural surface textures (seeded, built once)
function makeRoughnessTexture(seed = 11) {
  const n = 256, data = new Uint8Array(n * n * 4), rnd = mulberry32(seed);
  const cols = Array.from({ length: n }, () => rnd());
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
    // streaks run along v (span): value varies across u (x) only, plus a soft blotch
    const streak = 0.5 * cols[x] + 0.5 * cols[(x + 1) % n];
    const blot = 0.5 + 0.5 * Math.sin(x * 0.07 + Math.sin(y * 0.05) * 2) * Math.sin(y * 0.031 + 1.3);
    const v = 0.78 + 0.16 * (streak - 0.5) + 0.10 * (blot - 0.5);
    const i = (y * n + x) * 4; data[i] = data[i + 1] = data[i + 2] = Math.round(clamp(v) * 255); data[i + 3] = 255;
  }
  const t = new THREE.DataTexture(data, n, n); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.needsUpdate = true;
  t.magFilter = THREE.LinearFilter; t.minFilter = THREE.LinearMipmapLinearFilter; t.generateMipmaps = true;
  return t;
}
let _rough = null;
const roughTex = () => (_rough ||= makeRoughnessTexture());

// ---------------------------------------------------------------------------------------------------------------
// Hot metal material: physically based superalloy + an emissive heat field + a thermal-camera (ironbow) mode.
// Shared uniforms let a scene drive every hot part from one place.
export const U = {
  uTime: { value: 0 }, uHeat: { value: 0 }, uThermal: { value: 0 }, uFilm: { value: 0 }, uExposureT: { value: 1.0 },
  uSweep: { value: 1e4 }, uSweepOn: { value: 0 },
};
export function hotMetal({ color = 0x9a958c, roughness = 0.42, metalness = 1.0, temp = TEMP_BLADE, heatScale = 1.0,
  anisotropy = 0.0, envMapIntensity = 0.6, sweep = true, tint = true } = {}) {
  const m = new THREE.MeshPhysicalMaterial({ color, roughness, metalness, envMapIntensity, roughnessMap: roughTex(),
    clearcoat: 0, clearcoatRoughness: 0.5 });  // clearcoat measured +16% render cost, invisible at this roughness
  if (anisotropy > 0) { m.anisotropy = anisotropy; m.anisotropyRotation = Math.PI / 2; }
  m.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, U, { uHeatScale: { value: heatScale } });
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", `#include <common>
        attribute float part; varying vec3 vLoc; varying vec2 vUvT; varying float vPart; varying vec3 vWPos;`)
      .replace("#include <begin_vertex>", `#include <begin_vertex>
        vLoc = position; vUvT = uv; vPart = part;`)
      .replace("#include <worldpos_vertex>", `#include <worldpos_vertex>
        { vec4 wp = vec4(transformed, 1.0);
          #ifdef USE_INSTANCING
            wp = instanceMatrix * wp;
          #endif
          vWPos = (modelMatrix * wp).xyz; }`);
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", `#include <common>
        uniform float uTime, uHeat, uThermal, uFilm, uHeatScale, uExposureT, uSweep, uSweepOn;
        varying vec3 vLoc; varying vec2 vUvT; varying float vPart; varying vec3 vWPos;
        ${GLSL_COMMON}
        ${temp}`)
      .replace("#include <clipping_planes_fragment>", `#include <clipping_planes_fragment>
        ${sweep ? "if (uSweepOn > 0.5 && vWPos.z > uSweep) discard;" : ""}
        float Tm = tempField(vLoc, vUvT, vPart);`)
      .replace("#include <color_fragment>", `#include <color_fragment>
        ${tint ? `// heat tint of oxidised superalloy: straw -> bronze toward the hottest zones
        { float k = smoothstep(0.45, 0.80, Tm); diffuseColor.rgb *= mix(vec3(1.0), vec3(1.06, 0.90, 0.72), k * 0.35); }` : ""}`)
      .replace("#include <opaque_fragment>", `
        { float k = clamp(Tm * uHeatScale, 0.0, 1.2);
          float gl = pow(smoothstep(0.58, 0.84, k), 1.5) * (0.9 + 0.2 * vnoise(vLoc * vec3(9.0, 4.0, 9.0) + vec3(0.0, -uTime * 0.25, 0.0)));
          outgoingLight += blackbody(k) * uHeat * 4.0 * gl;
          ${sweep ? "float seam = exp(-pow((vWPos.z - uSweep) / 0.35, 2.0)) * uSweepOn; outgoingLight += vec3(1.0, 0.42, 0.08) * seam * 2.5;" : ""}
          float film = filmMask(vUvT) * step(vPart, 0.5);
          vec3 th = thermalColor(Tm) * uExposureT;
          vec3 nV = normalize(vViewPosition);
          float facing = abs(dot(normal, nV));
          th *= 0.5 + 0.62 * facing;               // emissivity falls off at grazing angles: form still reads
          th = mix(th, vec3(0.10, 0.55, 0.95) * 0.95, smoothstep(0.55, 0.95, film) * uFilm * 0.6);
          outgoingLight = mix(outgoingLight, th, uThermal);
          if (any(isnan(outgoingLight))) outgoingLight = vec3(0.0);
          outgoingLight = clamp(outgoingLight, 0.0, 24.0); }
        #include <opaque_fragment>`);
  };
  m.customProgramCacheKey = () => "hot" + temp.length + (sweep ? "s" : "") + (tint ? "t" : "");
  return m;
}

// ---------------------------------------------------------------------------------------------------------------
// Geometry helpers
const addPart = (g, p) => { const n = g.attributes.position.count; g.setAttribute("part", new THREE.Float32BufferAttribute(new Float32Array(n).fill(p), 1)); return g; };
const ensureUV = (g) => { if (!g.attributes.uv) g.setAttribute("uv", new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); return g; };
const clean = (g, p) => { g = g.index ? g.toNonIndexed() : g; ensureUV(g); if (!g.attributes.normal) g.computeVertexNormals();
  for (const k of Object.keys(g.attributes)) if (!["position", "normal", "uv"].includes(k)) g.deleteAttribute(k);
  return addPart(g, p); };

/** flat triangles from a position list, each oriented so its normal agrees with refFn(centroid) */
function orientedTris(tris, refFn) {
  const pos = [];
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3(), n = new THREE.Vector3(), m = new THREE.Vector3();
  for (const [p0, p1, p2] of tris) {
    a.copy(p0); b.copy(p1); c.copy(p2);
    n.subVectors(b, a).cross(m.subVectors(c, a));
    const ctr = new THREE.Vector3().add(a).add(b).add(c).multiplyScalar(1 / 3);
    if (n.dot(refFn(ctr)) < 0) pos.push(a.x, a.y, a.z, c.x, c.y, c.z, b.x, b.y, b.z);
    else pos.push(a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
  return g;
}

// ---------------------------------------------------------------------------------------------------------------
// Airfoil section in chord space: camber = quadratic Bezier (0,0)-(0.42,cam)-(1,0), NACA-like thickness.
// Returns loop TE->pressure->LE->suction->TE (+ duplicate first point), with per-point side info.
function sectionLoop(M, T, cam) {
  const P1 = [0.42, cam];
  const pts = [];
  const camberAt = (s) => {
    const x = 2 * (1 - s) * s * P1[0] + s * s, y = 2 * (1 - s) * s * P1[1];
    const dx = 2 * (1 - s) * P1[0] + 2 * s * (1 - P1[0]), dy = 2 * (1 - s) * P1[1] - 2 * s * P1[1];
    const L = Math.hypot(dx, dy); return { x, y, nx: -dy / L, ny: dx / L };
  };
  const yt = (s) => Math.max(0.006, 5 * T * (0.2969 * Math.sqrt(s) - 0.126 * s - 0.3516 * s * s + 0.2843 * s ** 3 - 0.1036 * s ** 4));
  const S = [];
  for (let k = 0; k <= M; k++) S.push((1 - Math.cos((Math.PI * k) / M)) / 2);
  for (let k = M; k >= 0; k--) { const c = camberAt(S[k]), t = yt(S[k]); pts.push({ a: c.x - c.nx * t, n: c.y - c.ny * t, k, side: -1 }); }
  for (let k = 1; k <= M; k++) { const c = camberAt(S[k]), t = yt(S[k]); pts.push({ a: c.x + c.nx * t, n: c.y + c.ny * t, k, side: 1 }); }
  pts.push({ ...pts[0] });
  return { pts, camberAt };
}

/**
 * HP turbine blade (local frame: Y radial from the platform top, Z axial/flow, X tangential).
 * Returns { geometry, holes, airfoilAt(u,v) } where holes are film-cooling hole decals (position, normal, tangents).
 */
export function makeBlade(o = {}) {
  const P = Object.assign({ H: DIM.H, chord: DIM.chord, T: 0.30, cam: 0.46, stagger: -0.16, twist: 0.32, M: 34, S: 20,
    pitch: (2 * Math.PI * DIM.R) / DIM.N, tip: true, platform: true, root: true, holes: true, flip: false, lod: false }, o);
  const vMin = -0.06;
  const ring = (v) => {
    const vv = Math.max(0, v);
    const c = P.chord * (1 - 0.10 * vv), ang = P.stagger + P.twist * (vv - 0.25), cam = P.cam * (1 - 0.15 * vv);
    const { pts } = sectionLoop(P.M, P.T * (1 - 0.12 * vv), cam);
    const ca = Math.cos(ang), sa = Math.sin(ang), fl = P.flip ? -1 : 1;
    return pts.map((q) => { const xc = (q.a - 0.45) * c, nc = q.n * c; return new THREE.Vector3(fl * (xc * sa + nc * ca), v * P.H, xc * ca - nc * sa); });
  };
  const rings = []; const vs = [];
  for (let j = 0; j <= P.S; j++) { const v = vMin + (1 - vMin) * (j / P.S); vs.push(v); rings.push(ring(v)); }
  const L = rings[0].length;
  // u = normalised arc length (from the hub ring; reused for all rings)
  const uArr = [0]; for (let i = 1; i < L; i++) uArr.push(uArr[i - 1] + rings[0][i].distanceTo(rings[0][i - 1]));
  const per = uArr[L - 1]; for (let i = 0; i < L; i++) uArr[i] /= per;
  const pos = [], uv = [], idx = [];
  for (let j = 0; j <= P.S; j++) for (let i = 0; i < L; i++) { const p = rings[j][i]; pos.push(p.x, p.y, p.z); uv.push(uArr[i], Math.max(0, vs[j])); }
  for (let j = 0; j < P.S; j++) for (let i = 0; i < L - 1; i++) {
    const a = j * L + i, b = j * L + i + 1, c = (j + 1) * L + i + 1, d = (j + 1) * L + i;
    idx.push(a, b, c, a, c, d);
  }
  let air = new THREE.BufferGeometry();
  air.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  air.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  air.setIndex(idx); air.computeVertexNormals();
  // orientation check: the normal at the leading edge (index M on ring 2) must point upstream (-Z)
  { const n = air.attributes.normal; if (n.getZ(2 * L + P.M) > 0) { for (let q = 0; q < idx.length; q += 3) { const t = idx[q + 1]; idx[q + 1] = idx[q + 2]; idx[q + 2] = t; } air.setIndex(idx); air.computeVertexNormals(); } }
  const nrm = air.attributes.normal;
  const airfoilAt = (u, v) => {           // bilinear sample on the loft grid: position + normal + tangents
    const vv = vMin + 0; const jf = ((v - vMin) / (1 - vMin)) * P.S; const j0 = clamp(Math.floor(jf), 0, P.S - 1), fj = jf - j0;
    let i0 = 0; while (i0 < L - 2 && uArr[i0 + 1] < u) i0++; const fi = clamp((u - uArr[i0]) / (uArr[i0 + 1] - uArr[i0]));
    const P_ = (j, i) => new THREE.Vector3(pos[(j * L + i) * 3], pos[(j * L + i) * 3 + 1], pos[(j * L + i) * 3 + 2]);
    const N_ = (j, i) => new THREE.Vector3(nrm.getX(j * L + i), nrm.getY(j * L + i), nrm.getZ(j * L + i));
    const bl = (F) => F(j0, i0).multiplyScalar((1 - fi) * (1 - fj)).add(F(j0, i0 + 1).multiplyScalar(fi * (1 - fj)))
      .add(F(j0 + 1, i0).multiplyScalar((1 - fi) * fj)).add(F(j0 + 1, i0 + 1).multiplyScalar(fi * fj));
    const p = bl(P_), n = bl(N_).normalize();
    const tu = P_(j0, i0 + 1).sub(P_(j0, i0)).normalize();
    const tv = new THREE.Vector3().crossVectors(n, tu).normalize();
    return { p, n, tu, tv, vv };
  };
  const parts = [clean(air, 0)];

  // squealer tip: rim + recessed floor
  if (P.tip) {
    const top = rings[P.S].slice(0, L - 1), M = P.M, w = 0.010, d = 0.018, yT = P.H;
    const inner = top.map((p, i) => {
      const k = i <= M ? M - i : i - M;           // chordwise station index
      const other = i <= M ? top[M + k] : top[M - k];
      const dir = new THREE.Vector3(other.x - p.x, 0, other.z - p.z);
      const dist = dir.length();
      let off = Math.min(w, 0.42 * dist);
      if (k === 0) { // leading-edge point: step toward the camber
        const nxt = top[M + 2], prv = top[M - 2]; dir.set((nxt.x + prv.x) / 2 - p.x, 0, (nxt.z + prv.z) / 2 - p.z); off = w; }
      if (dist < 1e-6 && k !== 0) return p.clone();
      return p.clone().add(dir.normalize().multiplyScalar(off));
    });
    const tris = [];
    const n = top.length;
    for (let i = 0; i < n; i++) { const i1 = (i + 1) % n; tris.push([top[i], top[i1], inner[i1]], [top[i], inner[i1], inner[i]]); }
    const rim = orientedTris(tris, () => new THREE.Vector3(0, 1, 0));
    const wall = [];
    const innerLow = inner.map((p) => new THREE.Vector3(p.x, yT - d, p.z));
    const ctr = inner.reduce((a, p) => a.add(p), new THREE.Vector3()).multiplyScalar(1 / n);
    for (let i = 0; i < n; i++) { const i1 = (i + 1) % n; wall.push([inner[i], inner[i1], innerLow[i1]], [inner[i], innerLow[i1], innerLow[i]]); }
    // inner wall faces into the cavity: reference = from the wall toward the matching opposite point
    const walls = orientedTris(wall, (c) => {
      let best = null, bd = 1e9; for (const q of inner) { const dd = (q.x - c.x) ** 2 + (q.z - c.z) ** 2; if (dd > 4e-4 && dd < bd) { bd = dd; best = q; } }
      return best ? new THREE.Vector3(best.x - c.x, 0, best.z - c.z) : new THREE.Vector3().subVectors(ctr, c).setY(0);
    });
    const shape2 = innerLow.map((p) => new THREE.Vector2(p.x, p.z));
    const ft = THREE.ShapeUtils.triangulateShape(shape2, []);
    const floor = orientedTris(ft.map(([a, b, c]) => [innerLow[a], innerLow[b], innerLow[c]]), () => new THREE.Vector3(0, 1, 0));
    parts.push(clean(rim, 3), clean(walls, 3), clean(floor, 3));
  }

  // platform following the hub camber line, shank, fir-tree root
  let platformBox = null;
  if (P.platform) {
    const hub = rings[Math.round((-vMin / (1 - vMin)) * P.S)];
    // camber line x(z) at the hub: midpoints of matching pressure/suction points
    const M = P.M, cam = [];
    for (let k = 0; k <= M; k++) { const a = hub[M - k], b = hub[M + k]; cam.push(new THREE.Vector2((a.x + b.x) / 2, (a.z + b.z) / 2)); }
    cam.sort((p, q) => p.y - q.y);
    const zLE = cam[0].y - 0.03, zTE = cam[cam.length - 1].y + 0.02;
    const xAt = (z) => { if (z <= cam[0].y) { const s = (cam[1].x - cam[0].x) / (cam[1].y - cam[0].y); return cam[0].x + s * (z - cam[0].y); }
      if (z >= cam[cam.length - 1].y) { const a = cam[cam.length - 2], b = cam[cam.length - 1]; const s = (b.x - a.x) / (b.y - a.y); return b.x + s * (z - b.y); }
      for (let i = 0; i < cam.length - 1; i++) if (z <= cam[i + 1].y) { const f = (z - cam[i].y) / (cam[i + 1].y - cam[i].y); return lerp(cam[i].x, cam[i + 1].x, f); } return 0; };
    // smooth the edge: platform edges follow the camber line, softened toward a straight line
    const lin = (z) => lerp(xAt(zLE), xAt(zTE), (z - zLE) / (zTE - zLE));
    const edge = (z) => lerp(lin(z), xAt(clamp(z, cam[0].y, cam[cam.length - 1].y)), 0.35);
    const hw = P.pitch / 2, steps = P.lod ? 12 : 36, sh = new THREE.Shape();
    for (let s = 0; s <= steps; s++) { const z = lerp(zLE, zTE, s / steps); const x = edge(z) - hw; s ? sh.lineTo(x, z) : sh.moveTo(x, z); }
    for (let s = steps; s >= 0; s--) { const z = lerp(zLE, zTE, s / steps); sh.lineTo(edge(z) + hw, z); }
    const pg = new THREE.ExtrudeGeometry(sh, { depth: 0.020, bevelEnabled: true, bevelThickness: 0.004, bevelSize: 0.004, bevelSegments: 2, curveSegments: 4 });
    pg.rotateX(Math.PI / 2); pg.translate(0, -0.004, 0);
    parts.push(clean(pg, 1));
    platformBox = { zLE, zTE };
    // shank (neck) with a small "angel wing" seal lip front and back
    const zc = (zLE + zTE) / 2, zl = (zTE - zLE) * 0.86;
    const shank = new THREE.BoxGeometry(0.064, 0.10, zl, 1, 1, 1); shank.translate(0, -0.074, zc);
    parts.push(clean(shank, 2));
    for (const sgn of [-1, 1]) { const wing = new THREE.BoxGeometry(0.05, 0.010, 0.03); wing.translate(0, -0.06, zc + sgn * (zl / 2 + 0.013)); parts.push(clean(wing, 2)); }
    if (P.root) {
      const ft = new THREE.Shape();
      // fir-tree: three rounded serrations each side, tapering toward the bottom
      const prof = [], y0 = -0.118, y1 = -0.300, nL = 3;
      const nR = P.lod ? 30 : 72;
      for (let i = 0; i <= nR; i++) {
        const f = i / nR, y = lerp(y0, y1, f);
        const ph = f * nL + 0.18;                             // lobe phase
        const tooth = Math.pow(0.5 + 0.5 * Math.cos(2 * Math.PI * ph), 1.6);
        const base = lerp(0.031, 0.016, f), amp = lerp(0.024, 0.016, f);
        prof.push([base + amp * tooth * (f < 0.95 ? 1 : 0), y]);
      }
      prof.push([0.010, y1 - 0.004]);
      ft.moveTo(-prof[0][0], prof[0][1]);
      for (const [x, y] of prof) ft.lineTo(x, y);
      for (let i = prof.length - 1; i >= 0; i--) ft.lineTo(-prof[i][0], prof[i][1]);
      const rg = new THREE.ExtrudeGeometry(ft, { depth: zl * 1.02, bevelEnabled: true, bevelThickness: 0.002, bevelSize: 0.002, bevelSegments: 1, curveSegments: 2 });
      rg.translate(0, 0, zc - (zl * 1.02) / 2);
      parts.push(clean(rg, 2));
    }
  }
  const geometry = mergeGeometries(parts, false);
  geometry.computeBoundingSphere();

  // film-cooling hole decals (u = arc position, v = span): showerhead on the LE, shaped rows on the pressure side,
  // one suction-side row, trailing-edge slots
  const holes = [];
  if (P.holes) {
    const rows = [
      { u: 0.455, k: "sh" }, { u: 0.478, k: "sh" }, { u: 0.50, k: "sh" }, { u: 0.522, k: "sh" }, { u: 0.545, k: "sh" },
      { u: 0.31, k: "ps" }, { u: 0.19, k: "ps" }, { u: 0.70, k: "ss" }, { u: 0.035, k: "te" },
    ];
    rows.forEach((r, ri) => {
      const nH = r.k === "te" ? 12 : r.k === "sh" ? 15 : 14;
      for (let h = 0; h < nH; h++) {
        const v = 0.08 + (0.86 * (h + (ri % 2) * 0.5)) / nH;
        if (v > 0.95) continue;
        const s = airfoilAt(r.u, v);
        const su = r.k === "sh" ? 0.0036 : r.k === "te" ? 0.004 : 0.0062, sv = r.k === "sh" ? 0.0036 : r.k === "te" ? 0.0115 : 0.0042;
        holes.push({ ...s, u: r.u, v, su, sv, kind: r.k });
      }
    });
  }
  return { geometry, holes, airfoilAt, P };
}

/** Instanced dark film-cooling hole decals, with a cyan glow in the thermal view */
export function holeDecals(holes) {
  const g = new THREE.CircleGeometry(1, 14);
  const mat = new THREE.MeshBasicMaterial({ color: 0x050403, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
  const mesh = new THREE.InstancedMesh(g, mat, holes.length);
  const m = new THREE.Matrix4(), b = new THREE.Matrix4();
  holes.forEach((h, i) => {
    b.makeBasis(h.tu.clone().multiplyScalar(h.su), h.tv.clone().multiplyScalar(h.sv), h.n.clone());
    b.setPosition(h.p.clone().addScaledVector(h.n, 0.0007)); mesh.setMatrixAt(i, b);
  });
  mesh.instanceMatrix.needsUpdate = true;
  mesh.userData.setThermal = (k) => { mat.color.setRGB(lerp(0.004, 0.10, k), lerp(0.003, 0.75, k), lerp(0.002, 1.4, k)); };
  return mesh;
}

/** Cyan cooling-film particles that leave each hole and hug the surface downstream (thermal reveal) */
export function filmParticles(blade, { perHole = 10, seed = 5 } = {}) {
  const rnd = mulberry32(seed), A = [];
  const pa = [], pb = [], pc = [], pd = [], sd = [];
  for (const h of blade.holes) {
    if (h.kind === "te") continue;
    const dir = h.u < 0.5 ? -1 : 1;   // pressure side flows toward u = 0, suction side toward u = 1
    const len = h.kind === "sh" ? 0.16 : 0.13;
    const pts = [0, 1 / 3, 2 / 3, 1].map((f) => { const s = blade.airfoilAt(clamp(h.u + dir * len * f, 0.004, 0.996), Math.min(0.97, h.v + 0.03 * f));
      return s.p.addScaledVector(s.n, 0.004 + 0.003 * f); });
    for (let q = 0; q < perHole; q++) { pa.push(...pts[0].toArray()); pb.push(...pts[1].toArray()); pc.push(...pts[2].toArray()); pd.push(...pts[3].toArray());
      sd.push(rnd(), rnd(), rnd(), rnd()); }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pa, 3));
  g.setAttribute("aB", new THREE.Float32BufferAttribute(pb, 3)); g.setAttribute("aC", new THREE.Float32BufferAttribute(pc, 3));
  g.setAttribute("aD", new THREE.Float32BufferAttribute(pd, 3)); g.setAttribute("aSeed", new THREE.Float32BufferAttribute(sd, 4));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: U.uTime, uAmt: { value: 0 }, uSize: { value: 26 } }, // uTime may be replaced by a scene clock
    vertexShader: `attribute vec3 aB, aC, aD; attribute vec4 aSeed; uniform float uTime, uSize; varying float vA;
      void main(){ float s = fract(aSeed.x + uTime * (0.55 + 0.35 * aSeed.y)); float r = 1.0 - s;
        vec3 p = r*r*r*position + 3.0*r*r*s*aB + 3.0*r*s*s*aC + s*s*s*aD;
        vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv;
        gl_PointSize = uSize * (0.6 + 0.6 * aSeed.z) * (1.0 - 0.5 * s) / -mv.z; vA = sin(3.14159 * s); }`,
    fragmentShader: `uniform float uAmt; varying float vA; void main(){ vec2 d = gl_PointCoord - 0.5; float f = exp(-dot(d, d) * 14.0);
      gl_FragColor = vec4(vec3(0.15, 0.62, 1.0) * 1.6 * f * vA * uAmt, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  const pts = new THREE.Points(g, mat); pts.frustumCulled = false;
  return pts;
}

// ---------------------------------------------------------------------------------------------------------------
// Turbine disc + blade ring (instanced), nozzle guide vanes, casing
export function makeDiscGeometry({ rBore = 0.24, rRim = DIM.R - 0.125 } = {}) {
  // (r, z) profile: bore, thick hub, thin web, thick rim, revolved around the engine axis
  const pr = [[rBore, -0.10], [rBore + 0.02, -0.17], [0.40, -0.18], [0.46, -0.07], [0.68, -0.05], [0.76, -0.12], [rRim - 0.04, -0.14],
    [rRim, -0.135], [rRim, 0.135], [rRim - 0.04, 0.14], [0.76, 0.12], [0.68, 0.05], [0.46, 0.07], [0.40, 0.18], [rBore + 0.02, 0.17], [rBore, 0.10], [rBore, -0.10]];
  const g = new THREE.LatheGeometry(pr.map(([r, z]) => new THREE.Vector2(r, z)), 160);
  g.rotateX(Math.PI / 2); // lathe axis Y -> engine axis Z
  return g;
}
export function bladeRing(bladeGeo, material, { N = DIM.N, R = DIM.R, z = 0, phase = 0 } = {}) {
  const mesh = new THREE.InstancedMesh(bladeGeo, material, N);
  const m = new THREE.Matrix4(), r = new THREE.Matrix4(), tr = new THREE.Matrix4();
  for (let i = 0; i < N; i++) { const a = phase + (i / N) * Math.PI * 2; r.makeRotationZ(a); tr.makeTranslation(0, R, z); m.multiplyMatrices(r, tr); mesh.setMatrixAt(i, m); }
  mesh.instanceMatrix.needsUpdate = true; mesh.frustumCulled = false;
  return mesh;
}
/** NGV: stationary vanes ahead of the rotor, between an inner and an outer band */
export function makeNGV({ N = 30, z = -0.55, R = DIM.R, span = 0.42, mat } = {}) {
  const vane = makeBlade({ H: span, chord: 0.30, T: 0.34, cam: 0.42, stagger: 0.55, twist: 0.0, M: 16, S: 6, tip: false, platform: false, root: false, holes: false, flip: true });
  const grp = new THREE.Group();
  grp.add(bladeRing(vane.geometry, mat, { N, R: R - 0.01, z }));
  const bandMat = mat;
  const inner = new THREE.CylinderGeometry(R, R - 0.02, 0.36, 128, 1, true); inner.rotateX(Math.PI / 2); inner.translate(0, 0, z);
  const outer = new THREE.CylinderGeometry(R + span + 0.03, R + span + 0.06, 0.36, 128, 1, true); outer.rotateX(Math.PI / 2); outer.translate(0, 0, z);
  const mi = new THREE.Mesh(inner, bandMat); const mo = new THREE.Mesh(outer, new THREE.MeshPhysicalMaterial({ color: 0x6d6a66, metalness: 1, roughness: 0.5, side: THREE.DoubleSide }));
  grp.add(mi); grp.userData.outer = mo;
  return grp;
}

// ---------------------------------------------------------------------------------------------------------------
// Particles: embers (rising sparks), hot gas stream through the stage
export function embers({ count = 260, box = [2.4, 1.6, 1.6], center = [0, 0, 0], seed = 21, size = 30, rise = 0.25 } = {}) {
  const rnd = mulberry32(seed), p = [], s = [];
  for (let i = 0; i < count; i++) { p.push(center[0] + (rnd() - 0.5) * box[0], center[1] + (rnd() - 0.5) * box[1], center[2] + (rnd() - 0.5) * box[2]); s.push(rnd(), rnd(), rnd(), rnd()); }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("aSeed", new THREE.Float32BufferAttribute(s, 4));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: U.uTime, uAmt: { value: 1 }, uSize: { value: size }, uRise: { value: rise }, uH: { value: box[1] }, uThermal: U.uThermal },
    vertexShader: `attribute vec4 aSeed; uniform float uTime, uSize, uRise, uH; varying float vA; varying float vK;
      void main(){ float life = 2.5 + 3.0 * aSeed.x; float age = fract(aSeed.y + uTime / life);
        vec3 p = position; p.y += (age - 0.5) * uH * 0.9 * (0.6 + aSeed.z) * uRise / 0.25;
        p.x += 0.06 * sin(uTime * (0.7 + aSeed.w) + aSeed.x * 20.0); p.z += 0.06 * cos(uTime * (0.6 + aSeed.z) + aSeed.y * 17.0);
        vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv;
        float tw = 0.65 + 0.35 * sin(uTime * (6.0 + 9.0 * aSeed.w) + aSeed.x * 40.0);
        gl_PointSize = uSize * (0.35 + aSeed.w) / -mv.z; vA = smoothstep(0.0, 0.15, age) * (1.0 - smoothstep(0.6, 1.0, age)) * tw; vK = aSeed.z; }`,
    fragmentShader: `uniform float uAmt, uThermal; varying float vA; varying float vK; ${GLSL_COMMON}
      void main(){ vec2 d = gl_PointCoord - 0.5; float f = exp(-dot(d, d) * 18.0);
        vec3 c = mix(vec3(1.0, 0.36, 0.06), vec3(1.0, 0.72, 0.30), vK) * 3.0;
        c = mix(c, thermalColor(1.12 + 0.1 * vK) * 2.0, uThermal);
        gl_FragColor = vec4(c * f * vA * uAmt, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  const pts = new THREE.Points(g, mat); pts.frustumCulled = false; return pts;
}

/**
 * Hot gas particles flowing through the annulus along +Z (combustor -> NGV -> rotor -> exit), swirled by the vanes.
 * Each particle draws a short trail (trail copies at earlier times). uSpin = rotor angle so the gas follows it.
 */
export function gasStream({ count = 2600, trail = 4, z0 = -2.5, z1 = 1.2, seed = 33, size = 34, thetaRange = [0, Math.PI * 2], rIn = DIM.R + 0.02, rOut = DIM.R + DIM.H - 0.02 } = {}) {
  const rnd = mulberry32(seed), pos = [], s = [], tr = [];
  for (let i = 0; i < count; i++) { const a = [rnd(), rnd(), rnd(), rnd()]; for (let k = 0; k < trail; k++) { pos.push(0, 0, 0); s.push(...a); tr.push(k); } }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("aSeed", new THREE.Float32BufferAttribute(s, 4));
  g.setAttribute("aTrail", new THREE.Float32BufferAttribute(tr, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: U.uTime, uClock: { value: 0 }, uThermal: U.uThermal, uAmt: { value: 1 }, uSize: { value: size }, uSpeed: { value: 0.55 }, uZ0: { value: z0 }, uZ1: { value: z1 },
      uTh0: { value: thetaRange[0] }, uTh1: { value: thetaRange[1] }, uRin: { value: rIn }, uRout: { value: rOut }, uFill: { value: 1 }, uSlow: { value: 1 } },
    vertexShader: `attribute vec4 aSeed; attribute float aTrail; uniform float uTime, uClock, uSpeed, uZ0, uZ1, uTh0, uTh1, uRin, uRout, uSize, uFill, uSlow;
      varying float vA; varying float vHot;
      void main(){
        float tt = uClock - aTrail * 0.012 * uSlow;
        float s = fract(aSeed.x + tt * uSpeed * (0.8 + 0.4 * aSeed.y));
        float z = mix(uZ0, uZ1, s);
        // combustor exit funnels into the stage annulus
        float fr = smoothstep(-0.9, -0.5, z);
        float r = mix(mix(uRin - 0.05, uRout + 0.10, aSeed.z), mix(uRin, uRout, aSeed.z), fr);
        r += 0.03 * sin(z * 6.0 + aSeed.w * 30.0 + uTime * 2.0) * (1.0 - fr);
        float th = mix(uTh0, uTh1, aSeed.w);
        // vanes turn the flow (swirl), the rotor takes it back out
        th += 0.22 * smoothstep(-0.75, -0.35, z) - 0.20 * smoothstep(-0.05, 0.25, z);
        th += 0.05 * sin(z * 4.0 + aSeed.x * 12.0 + uTime * 1.5);
        vec3 p = vec3(sin(th) * r, -cos(th) * r, z);
        vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv;
        gl_PointSize = min(uSize * (0.5 + 0.7 * aSeed.y) * (1.0 - 0.18 * aTrail) / -mv.z, 9.0);
        float fade = smoothstep(0.0, 0.08, s) * (1.0 - smoothstep(0.85, 1.0, s));
        vA = fade * (1.0 - 0.22 * aTrail) * step(aSeed.x, uFill);
        vHot = 1.0 - 0.35 * smoothstep(0.0, 1.2, z); }`,
    fragmentShader: `uniform float uAmt, uThermal; varying float vA; varying float vHot; ${GLSL_COMMON}
      void main(){ vec2 d = gl_PointCoord - 0.5; float f = exp(-dot(d, d) * 12.0);
        vec3 c = blackbody(0.75 + 0.35 * vHot) * 1.6;
        c = mix(c, thermalColor(1.06 + 0.12 * vHot) * 1.15, uThermal);
        gl_FragColor = vec4(c * f * vA * uAmt * 0.55, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  const pts = new THREE.Points(g, mat); pts.frustumCulled = false;
  pts.onBeforeRender = () => { if (!pts.userData.manualClock) mat.uniforms.uClock.value = U.uTime.value; };
  return pts;
}

// ---------------------------------------------------------------------------------------------------------------
// Combustor: annular liner (inner + outer walls with dilution holes), dome with fuel nozzles, flame shader cones.
export function makeCombustor({ thetaLen = Math.PI * 2, thetaStart = 0, nNoz = 20, mat, z0 = -2.55, z1 = -0.72 } = {}) {
  const grp = new THREE.Group();
  const lathe = (pr, seg = 140) => { const g = new THREE.LatheGeometry(pr.map(([r, z]) => new THREE.Vector2(r, z)), seg, thetaStart, thetaLen); g.rotateX(Math.PI / 2); return g; };
  // outer liner: from dome (r 1.62) converging to the NGV outer band; inner liner from 0.92 to the inner band
  const outerPr = [], innerPr = [];
  for (let i = 0; i <= 24; i++) { const f = i / 24, z = lerp(z0, z1, f), e = sstep(0.45, 1.0, f);
    outerPr.push([lerp(1.66, DIM.R + DIM.H + 0.05, e) + 0.02 * Math.sin(f * 40) * (1 - e) * 0.3, z]); innerPr.push([lerp(0.86, DIM.R - 0.01, e), z]); }
  const linerMat = mat || hotMetal({ color: 0x8c8780, roughness: 0.5, temp: TEMP_CONST(0.62), anisotropy: 0.2 });
  linerMat.side = THREE.DoubleSide;
  const og = lathe(outerPr), ig = lathe(innerPr);
  grp.add(new THREE.Mesh(og, linerMat), new THREE.Mesh(ig, linerMat));
  // dome: annular wall at z0 with swirler cups + fuel nozzle stems
  const dome = new THREE.RingGeometry(0.86, 1.66, 140, 1, thetaStart, thetaLen); dome.translate(0, 0, z0);
  // RingGeometry lies in XY with angle measured from +X; lathe measures from +Z rotated... align by rotation
  grp.add(new THREE.Mesh(dome, linerMat));
  const noz = [], cupMat = new THREE.MeshPhysicalMaterial({ color: 0x8a8580, metalness: 1, roughness: 0.38 });
  const flames = [];
  for (let i = 0; i < nNoz; i++) {
    const a = thetaStart + ((i + 0.5) / nNoz) * thetaLen;
    // lathe angle a puts a point at (sin a * r, ., cos a * r) before rotateX; after rotateX(pi/2): (r sin a, -r cos a?, z)
    noz.push(a);
  }
  return { grp, linerMat, nozAngles: noz, z0, z1 };
}

/** flame jets (additive shader cones), one per nozzle; uIgn 0..1 lights them in sequence */
export function makeFlames(angles, { z0 = -2.55, len = 1.5, r = 1.26, seed = 3 } = {}) {
  const grp = new THREE.Group();
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: U.uTime, uIgn: { value: 1 }, uThermal: U.uThermal, uAmt: { value: 1 } },
    vertexShader: `attribute float aIdx; varying vec3 vP; varying float vIdx; varying vec3 vN; varying vec3 vV;
      void main(){ vP = position; vIdx = aIdx; vec4 mv = modelViewMatrix * vec4(position, 1.0);
        vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform float uTime, uIgn, uThermal, uAmt; varying vec3 vP; varying float vIdx; varying vec3 vN; varying vec3 vV; ${GLSL_COMMON}
      void main(){ float h = clamp(vP.y, 0.0, 1.0);   // 0 at the nozzle, 1 at the tip of the jet (local cone axis)
        float ign = smoothstep(vIdx * 0.04, vIdx * 0.04 + 0.35, uIgn);
        float reach = ign;
        float n = fbm(vec3(vP.x * 7.0, vP.y * 5.0 - uTime * 6.0, vP.z * 7.0 + vIdx * 3.1));
        float body = smoothstep(reach + 0.05, reach - 0.25, h) * smoothstep(0.0, 0.06, h);
        float fres = pow(abs(dot(vN, vV)), 1.5);
        float a = body * (0.35 + 0.9 * n) * fres;
        vec3 c = mix(vec3(1.0, 0.85, 0.55), vec3(1.0, 0.36, 0.05), smoothstep(0.1, 0.8, h)) * (1.3 + 1.5 * n);
        c = mix(c, thermalColor(1.18 - 0.1 * h) * 1.4, uThermal);
        gl_FragColor = vec4(c * a * uAmt, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  });
  angles.forEach((a, i) => {
    for (const [rad, sc] of [[0.16, 1.0], [0.09, 0.8]]) {
      const g = new THREE.ConeGeometry(rad, 1, 20, 8, true); // apex at +y=0.5
      g.rotateZ(Math.PI); g.translate(0, 0.5, 0);               // base (wide) at y=1? keep narrow at nozzle: flip
      const idx = new Float32Array(g.attributes.position.count).fill(i); g.setAttribute("aIdx", new THREE.BufferAttribute(idx, 1));
      const m = new THREE.Mesh(g, mat);
      // cone local +Y -> engine +Z; place at radius r, angle a (engine frame: x = -sin a r, y = cos a r)
      m.scale.set(1, len * sc, 1); m.rotation.x = Math.PI / 2; m.position.set(Math.sin(a) * r, -Math.cos(a) * r, z0 + 0.05);
      const holder = new THREE.Group(); holder.add(m); grp.add(holder);
    }
  });
  grp.userData.mat = mat;
  return grp;
}

// ---------------------------------------------------------------------------------------------------------------
// Background: a large inverted sphere with a slow drifting haze (never a flat canvas), slate -> ember glow,
// optional drafting grid (blueprint world) and thermal mode.
export function backdrop({ glowDir = [0.2, 0.1, -1], glow = 0.6 } = {}) {
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: U.uTime, uThermal: U.uThermal, uGlowDir: { value: new THREE.Vector3(...glowDir).normalize() }, uGlow: { value: glow },
      uGrid: { value: 0 }, uLift: { value: 1 }, uCool: { value: 0 }, uHotBg: { value: 0 } },
    vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform float uTime, uThermal, uGlow, uGrid, uLift, uCool, uHotBg; uniform vec3 uGlowDir; varying vec3 vD; ${GLSL_COMMON}
      void main(){ vec3 d = normalize(vD);
        float n = fbm(d * 2.2 + vec3(0.0, uTime * 0.03, uTime * 0.015));
        float n2 = fbm(d * 6.0 - vec3(uTime * 0.02, 0.0, uTime * 0.12));
        vec3 slate = vec3(0.0026, 0.0034, 0.0056) * (1.2 * uLift);
        float g = pow(max(dot(d, uGlowDir), 0.0), 5.0);
        vec3 col = slate * (0.7 + 0.9 * n) + vec3(0.045, 0.014, 0.0035) * uGlow * g * (0.6 + 0.8 * n2);
        col += vec3(0.010, 0.018, 0.028) * uCool * (0.5 + n);
        // drafting grid on the sphere (lat/long lines), blueprint world
        vec2 sp = vec2(atan(d.x, d.z), asin(clamp(d.y, -1.0, 1.0))) * 22.0;
        vec2 gl = abs(fract(sp) - 0.5); float line = smoothstep(0.47, 0.5, max(gl.x, gl.y));
        vec2 gm = abs(fract(sp / 5.0) - 0.5); float major = smoothstep(0.485, 0.5, max(gm.x, gm.y));
        col += vec3(0.20, 0.08, 0.02) * (0.25 * line + 0.5 * major) * uGrid;
        vec3 th = thermalColor(0.10 + 0.10 * n + 0.06 * g * uGlow) * 0.55;
        th = mix(th, thermalColor(0.86 + 0.32 * n + 0.12 * n2) * 0.85, uHotBg * smoothstep(-0.6, 0.3, d.y + 0.4 * n));
        gl_FragColor = vec4(mix(col, th, uThermal), 1.0); }`,
    side: THREE.BackSide, depthWrite: false,
  });
  const m = new THREE.Mesh(new THREE.SphereGeometry(80, 48, 32), mat); m.frustumCulled = false; m.renderOrder = -10;
  return m;
}

// ---------------------------------------------------------------------------------------------------------------
// Post: heat shimmer (UV distortion, own pass), then bloom + vignette + ACES + grain/lift (one merged pass)
class ShimmerEffect extends Effect {
  constructor() {
    super("ShimmerEffect", `uniform float uT, uAmp; uniform vec4 uRect;
      void mainUv(inout vec2 uv){ vec2 d = (uv - uRect.xy) / uRect.zw; float m = exp(-dot(d, d)) * uAmp;
        float a = sin(uv.y * 46.0 - uT * 6.0 + 1.5 * sin(uv.x * 23.0 + uT * 1.7));
        float b = sin(uv.x * 31.0 + uv.y * 52.0 - uT * 5.0);
        uv += vec2(a * 0.0005, b * 0.0008) * m; }`,
      { uniforms: new Map([["uT", new THREE.Uniform(0)], ["uAmp", new THREE.Uniform(0)], ["uRect", new THREE.Uniform(new THREE.Vector4(0.5, 0.5, 0.3, 0.3))]]) });
  }
}
export class WhipEffect extends Effect {
  constructor() {
    super("WhipEffect", `uniform vec2 uDir; uniform float uAmt;
      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor){
        if (uAmt < 0.0001) { outputColor = inputColor; return; }
        vec4 c = vec4(0.0); float tw = 0.0;
        for (int i = -10; i <= 10; i++) { float w = 1.0 - abs(float(i)) / 11.0; c += texture2D(inputBuffer, uv + uDir * uAmt * float(i) / 10.0) * w; tw += w; }
        outputColor = c / tw; }`,
      { attributes: EffectAttribute.CONVOLUTION, uniforms: new Map([["uDir", new THREE.Uniform(new THREE.Vector2(1, 0))], ["uAmt", new THREE.Uniform(0)]]) });
  }
}
class GrainEffect extends Effect {
  constructor() {
    super("GrainEffect", `uniform float uT, uGrain, uLift;
      float h2(vec2 p){ vec3 p3 = fract(vec3(p.xyx) * 0.1031); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.x + p3.y) * p3.z); }
      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor){
        vec2 px = uv * resolution; float fr = floor(uT * 30.0 + 0.5);
        float n = h2(px + fr * vec2(37.0, 17.0)) + h2(px * 1.7 + fr * vec2(11.0, 53.0)) - 1.0;
        vec3 c = inputColor.rgb; float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
        c += n * uGrain * (0.25 + 1.6 * l * (1.0 - l));
        c = c * (1.0 - uLift) + uLift * vec3(0.55, 0.60, 0.72);   // lifted, slate-tinted blacks (never crushed)
        outputColor = vec4(c, inputColor.a); }`,
      { uniforms: new Map([["uT", new THREE.Uniform(0)], ["uGrain", new THREE.Uniform(0.045)], ["uLift", new THREE.Uniform(0.018)]]) });
  }
}

/**
 * Stage: renderer + scene + camera + HDRI + post stack. Calls build(stage) after the HDRI is ready, then renders
 * frames on hf-seek. update(t) must set the whole scene state from t alone.
 */
export function createStage({ fov = 32, near = 0.02, far = 200, bloom = { intensity: 0.8, threshold: 1.3, smoothing: 0.3, radius: 0.7 },
  vignette = 0.42, exposure = 1.0, hdri = "vendor/library/hdri/studio_small_09_1k.hdr", envRotation = 0, ao = null, dof = null, whip = false } = {}) {
  const root = document.getElementById("root");
  const W = +root.dataset.width, H = +root.dataset.height, DUR = +root.dataset.duration;
  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("gl"), antialias: false, stencil: false, depth: false,
    powerPreference: "high-performance", preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.NoToneMapping; renderer.toneMappingExposure = exposure;
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x020306);
  const camera = new THREE.PerspectiveCamera(fov, W / H, near, far);
  const B = window.BENCH || {};
  const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType, multisampling: B.msaa ?? 0 });  // 4x MSAA costs 2.4x on the software GL (measured); FXAA instead
  composer.addPass(new RenderPass(scene, camera));
  let aoPass = null, dofFx = null, whipFx = null;
  if (ao) { aoPass = new N8AOPostPass(scene, camera, W, H); aoPass.configuration.aoRadius = ao.radius ?? 1.2; aoPass.configuration.distanceFalloff = ao.falloff ?? 1.0;
    aoPass.configuration.intensity = ao.intensity ?? 2.4; aoPass.configuration.color = new THREE.Color(0, 0, 0); aoPass.setQualityMode(ao.quality ?? "Performance"); aoPass.configuration.halfRes = true; composer.addPass(aoPass); }
  const shimmer = new ShimmerEffect();
  if (!B.noShimmer) composer.addPass(new EffectPass(camera, shimmer));
  if (dof) { dofFx = new DepthOfFieldEffect(camera, { focusDistance: dof.distance ?? 6, focusRange: dof.range ?? 3, bokehScale: dof.bokeh ?? 2.2, resolutionScale: 0.5 }); composer.addPass(new EffectPass(camera, dofFx)); }
  if (whip) { whipFx = new WhipEffect(); composer.addPass(new EffectPass(camera, whipFx)); }
  const bloomFx = new BloomEffect({ intensity: bloom.intensity, luminanceThreshold: bloom.threshold, luminanceSmoothing: bloom.smoothing, mipmapBlur: true, radius: bloom.radius });
  const vig = new VignetteEffect({ technique: VignetteTechnique.ESKIL, darkness: vignette, offset: 0.3 });
  const tone = new ToneMappingEffect({ mode: ToneMappingMode.ACES_FILMIC });
  const grain = new GrainEffect();
  const post = [bloomFx, vig, tone]; if (B.bloom === 0) post.shift();
  if (!B.noFxaa) post.push(new FXAAEffect());
  post.push(grain);
  composer.addPass(new EffectPass(camera, ...post));
  composer.setSize(W, H);
  const stage = { root, W, H, DUR, renderer, scene, camera, composer, fx: { shimmer, bloom: bloomFx, vig, tone, grain, dof: dofFx, whip: whipFx, ao: aoPass } };
  stage.setShimmer = (amp, cx = 0.5, cy = 0.5, rx = 0.3, ry = 0.3) => { const u = shimmer.uniforms; u.get("uAmp").value = amp; u.get("uRect").value.set(cx, cy, rx, ry); };
  stage.ready = new HDRLoader().loadAsync(hdri).then((tex) => {
    const pm = new THREE.PMREMGenerator(renderer);
    scene.environment = pm.fromEquirectangular(tex).texture; scene.environmentRotation = new THREE.Euler(0, envRotation, 0);
    tex.dispose(); pm.dispose();
  });
  stage.frame = (t) => {
    shimmer.uniforms.get("uT").value = t; grain.uniforms.get("uT").value = t;
    composer.render(0);
  };
  stage.run = (update) => {
    stage.ready.then(() => {
      const draw = (t) => { U.uTime.value = t; update(t); stage.frame(t); };
      window.addEventListener("hf-seek", (ev) => draw(ev.detail.time));
      draw(window.__hfThreeTime || 0);
    });
  };
  return stage;
}

/** standard 3-point light rig: warm key, amber rim from behind (the "furnace"), cool low fill */
export function lightRig(scene, { key = 2.2, rim = 5.0, fill = 0.5, rimColor = 0xff8a3a } = {}) {
  const k = new THREE.DirectionalLight(0xf4f1ec, key); k.position.set(3, 4, 4); scene.add(k);
  const r = new THREE.DirectionalLight(rimColor, rim); r.position.set(-2.5, 1.5, -4); scene.add(r);
  const r2 = new THREE.DirectionalLight(rimColor, rim * 0.6); r2.position.set(3, 0.5, -3.5); scene.add(r2);
  const f = new THREE.DirectionalLight(0x9fb4d8, fill); f.position.set(-3, -2, 3); scene.add(f);
  return { key: k, rim: r, rim2: r2, fill: f };
}

/** place the camera on a path: position + look target */
export function aim(camera, p, look, roll = 0) {
  camera.position.set(p[0], p[1], p[2]); camera.up.set(Math.sin(roll), Math.cos(roll), 0); camera.lookAt(look[0], look[1], look[2]);
}

/** format an integer with thousands separators (tabular counters) */
export const fmt = (n) => Math.round(n).toLocaleString("en-US");

// ---------------------------------------------------------------------------------------------------------------
// The hot section assembly shared by A2 (end), A4, A5, A6, A7, A8: rotor (disc + 48 blades + all cooling holes),
// nozzle guide vanes, cutaway combustor with nozzles and flames, outer casing. Lathe angle phi maps to
// (x, y) = (r sin phi, -r cos phi); the cutaway keeps the sector [cutStart, cutStart + cutLen].
const ringMatrices = (N, R, z = 0, phase = 0) => { const out = [], r = new THREE.Matrix4(), tr = new THREE.Matrix4();
  for (let i = 0; i < N; i++) { const a = phase + (i / N) * Math.PI * 2; r.makeRotationZ(a); tr.makeTranslation(0, R, z); out.push(new THREE.Matrix4().multiplyMatrices(r, tr)); } return out; };
export function buildHotSection(scene, { combustor = true, ngv = true, casing = true, cutStart = -Math.PI * 0.08, cutLen = Math.PI * 1.16,
  nNoz = 20, holes = true, bladeMat, discMat, lod = true } = {}) {
  const hs = { group: new THREE.Group() };
  scene.add(hs.group);
  const blade = makeBlade();
  hs.blade = blade;
  // ring LOD: same blade, coarser tessellation (the hero blade / holes still use the full model)
  const lodB = lod ? makeBlade({ M: 16, S: 9, holes: false, lod: true }) : blade;
  hs.bladeLod = lodB;
  hs.bladeMat = bladeMat || hotMetal({ roughness: 0.4 });
  hs.discMat = discMat || hotMetal({ color: 0x8e8a84, roughness: 0.46, temp: TEMP_DISC });
  const rotor = new THREE.Group(); hs.rotor = rotor; hs.group.add(rotor);
  const disc = new THREE.Mesh(makeDiscGeometry(), hs.discMat); rotor.add(disc);
  hs.ring = bladeRing(lodB.geometry, hs.bladeMat); rotor.add(hs.ring);
  const mats = ringMatrices(DIM.N, DIM.R);
  if (holes) {
    const g = new THREE.CircleGeometry(1, 10);
    const hm = new THREE.MeshBasicMaterial({ color: 0x050403, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
    const inst = new THREE.InstancedMesh(g, hm, blade.holes.length * DIM.N);
    const b = new THREE.Matrix4(), m = new THREE.Matrix4(); let k = 0;
    for (const M of mats) for (const h of blade.holes) {
      b.makeBasis(h.tu.clone().multiplyScalar(h.su), h.tv.clone().multiplyScalar(h.sv), h.n.clone()); b.setPosition(h.p.clone().addScaledVector(h.n, 0.0007));
      m.multiplyMatrices(M, b); inst.setMatrixAt(k++, m); }
    inst.instanceMatrix.needsUpdate = true; inst.frustumCulled = false; rotor.add(inst); hs.holes = inst;
    hs.setHoleThermal = (q) => hm.color.setRGB(lerp(0.004, 0.10, q), lerp(0.003, 0.75, q), lerp(0.002, 1.4, q));
  }
  // shaft cone behind the disc
  const shaft = new THREE.CylinderGeometry(0.2, 0.26, 2.4, 64, 1, true); shaft.rotateX(Math.PI / 2); shaft.translate(0, 0, -1.0);
  hs.group.add(new THREE.Mesh(shaft, hs.discMat));
  if (ngv) {
    hs.ngvMat = hotMetal({ color: 0x8f8a83, roughness: 0.44, temp: TEMP_VANE });
    const vane = makeBlade({ H: DIM.H + 0.02, chord: 0.30, T: 0.36, cam: 0.40, stagger: 0.62, twist: 0.0, M: 18, S: 6, tip: false, platform: false, root: false, holes: false, flip: true });
    const nv = 32, z = -0.50, R = DIM.R - 0.01, all = ringMatrices(nv, R, z, 0.04);
    const inCut = (phi) => { const d = (((phi - cutStart) % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2); return d < cutLen; };
    const keep = all.filter((M, i) => inCut(0.04 + (i / nv) * Math.PI * 2 + Math.PI));
    const im = new THREE.InstancedMesh(vane.geometry, hs.ngvMat, keep.length); keep.forEach((M, i) => im.setMatrixAt(i, M)); im.instanceMatrix.needsUpdate = true; im.frustumCulled = false;
    hs.group.add(im); hs.ngv = im;
    const lathe = (pr, a0 = 0, al = Math.PI * 2) => { const g = new THREE.LatheGeometry(pr.map(([r, zz]) => new THREE.Vector2(r, zz)), 160, a0, al); g.rotateX(Math.PI / 2); return g; };
    const band = (r0, r1) => lathe([[r0, -0.70], [r0, -0.32], [r1, -0.30]]);
    const ib = new THREE.Mesh(lathe([[DIM.R - 0.06, -0.72], [DIM.R - 0.005, -0.70], [DIM.R - 0.005, -0.31], [DIM.R - 0.05, -0.28]]), hs.ngvMat);
    hs.group.add(ib);
    hs.lathe = lathe;
  }
  const lathe = (pr, a0 = 0, al = Math.PI * 2, segs = 160) => { const g = new THREE.LatheGeometry(pr.map(([r, zz]) => new THREE.Vector2(r, zz)), segs, a0, al); g.rotateX(Math.PI / 2); return g; };
  hs.lathe = lathe;
  if (casing) {
    hs.caseMat = hotMetal({ color: 0x5f5d5a, roughness: 0.52, temp: TEMP_CONST(0.5), heatScale: 0.6 }); hs.caseMat.side = THREE.DoubleSide;
    // outer flow-path wall over NGV + rotor tips (cutaway like the combustor)
    const R1 = DIM.R + DIM.H;
    const shroud = lathe([[R1 + 0.06, -0.74], [R1 + 0.05, -0.32], [R1 + 0.012, -0.2], [R1 + 0.012, 0.2], [R1 + 0.05, 0.5]], cutStart, cutLen);
    hs.group.add(new THREE.Mesh(shroud, hs.caseMat));
    // engine outer case (dark, thick) further out
    const oc = lathe([[2.02, -3.4], [2.02, -0.9], [1.9, -0.3], [1.86, 0.8]], cutStart, cutLen);
    const ocm = hotMetal({ color: 0x3b3b3c, roughness: 0.6, temp: TEMP_CONST(0.3), heatScale: 0.3 }); ocm.side = THREE.DoubleSide;
    hs.group.add(new THREE.Mesh(oc, ocm)); hs.outerCaseMat = ocm;
  }
  if (combustor) {
    const z0 = -2.55, z1 = -0.72;
    hs.linerMat = hotMetal({ color: 0x8c8780, roughness: 0.5, temp: TEMP_CONST(0.62), heatScale: 0.8, envMapIntensity: 0.4 }); hs.linerMat.side = THREE.DoubleSide;
    const outerPr = [], innerPr = [];
    for (let i = 0; i <= 28; i++) { const f = i / 28, z = lerp(z0, z1, f), e = sstep(0.4, 1.0, f);
      // louvred liner: small steps every few stations (cooling rings)
      const step = 0;
      outerPr.push([lerp(1.68, DIM.R + DIM.H + 0.05, e) + step * (1 - e), z]); innerPr.push([lerp(0.84, DIM.R - 0.01, e) - step * (1 - e), z]); }
    hs.group.add(new THREE.Mesh(lathe(outerPr, cutStart, cutLen), hs.linerMat), new THREE.Mesh(lathe(innerPr, cutStart, cutLen), hs.linerMat));
    hs.group.add(new THREE.Mesh(lathe([[0.84, z0], [1.0, z0 - 0.12], [1.52, z0 - 0.12], [1.68, z0]], cutStart, cutLen), hs.linerMat));
    // nozzles: one per sector angle; stems come in through the outer case, swirler cups sit in the dome
    const ang = []; for (let i = 0; i < nNoz; i++) ang.push((i + 0.5) / nNoz * Math.PI * 2);
    const vis = ang.filter((a) => { let d = ((a - cutStart) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2); return d > 0.05 && d < cutLen - 0.05; });
    const cupMat = hotMetal({ color: 0x9a948c, roughness: 0.36, temp: TEMP_CONST(0.45), heatScale: 0.5 });
    const rm = 1.26;
    for (const a of vis) {
      const cup = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.03, 12, 28), cupMat);
      cup.position.set(Math.sin(a) * rm, -Math.cos(a) * rm, z0 - 0.05); hs.group.add(cup);
      const stem = new THREE.CylinderGeometry(0.035, 0.035, 0.9, 16); stem.translate(0, 0.45, 0);
      const sm = new THREE.Mesh(stem, cupMat); sm.position.set(Math.sin(a) * rm, -Math.cos(a) * rm, z0 - 0.22);
      sm.rotation.z = a + Math.PI; hs.group.add(sm);
      const arm = new THREE.CylinderGeometry(0.032, 0.032, 0.2, 12); arm.rotateX(Math.PI / 2);
      const amm = new THREE.Mesh(arm, cupMat); amm.position.set(Math.sin(a) * rm, -Math.cos(a) * rm, z0 - 0.13); hs.group.add(amm);
    }
    hs.flames = makeFlames(vis, { z0, len: 1.25, r: rm }); hs.group.add(hs.flames);
    // dilution holes on both liners (dark ellipses; cooling/dilution air enters here)
    const dg = new THREE.CircleGeometry(1, 14), dm = new THREE.MeshBasicMaterial({ color: 0x060504, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
    const list = [];
    for (const [zf, n, rr] of [[0.30, 40, 0.05], [0.52, 40, 0.04]]) for (let i = 0; i < n; i++) {
      const a = (i + 0.5 * (zf > 0.4 ? 1 : 0)) / n * Math.PI * 2; let d = ((a - cutStart) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2); if (d < 0.03 || d > cutLen - 0.03) continue;
      const z = lerp(z0, z1, zf), e = sstep(0.4, 1.0, zf);
      for (const R of [lerp(1.68, DIM.R + DIM.H + 0.05, e), lerp(0.84, DIM.R - 0.01, e)]) list.push({ a, z, R, rr });
    }
    const di = new THREE.InstancedMesh(dg, dm, list.length); const q = new THREE.Matrix4(), sc = new THREE.Matrix4();
    list.forEach((h, i) => { const n = new THREE.Vector3(Math.sin(h.a), -Math.cos(h.a), 0), up = new THREE.Vector3(0, 0, 1), side = new THREE.Vector3().crossVectors(up, n);
      q.makeBasis(side.multiplyScalar(h.rr), up.clone().multiplyScalar(h.rr * 0.8), n); q.setPosition(n.clone().multiplyScalar(h.R)); q.elements[14] = h.z; di.setMatrixAt(i, q); });
    di.instanceMatrix.needsUpdate = true; hs.group.add(di);
  }
  hs.spin = (ang) => { rotor.rotation.z = ang; };
  return hs;
}

/** set envMapIntensity on every lit material in a subtree (scene-level exposure of reflections) */
export function setEnv(obj, k) { if (obj.isScene) obj.environmentIntensity = k; obj.traverse((o) => { const ms = Array.isArray(o.material) ? o.material : [o.material];
  for (const m of ms) if (m && "envMapIntensity" in m) { m.userData.env0 ??= m.envMapIntensity; m.envMapIntensity = m.userData.env0 * k; } }); }

/**
 * Volumetric-looking fire filling the combustor liner: nested additive lathe shells with swirling fbm.
 * uFront (engine z) is how far the flame front has advanced from the dome.
 */
export function fireVolume({ cutStart = -Math.PI * 0.08, cutLen = Math.PI * 1.16, z0 = -2.5, z1 = -0.75, layers = 5, rA = [0.9, 1.62], rB = [DIM.R + 0.02, DIM.R + DIM.H], gain = 0.2 } = {}) {
  const grp = new THREE.Group();
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: U.uTime, uFront: { value: z0 }, uAmt: { value: 1 }, uThermal: U.uThermal, uZ0: { value: z0 }, uZ1: { value: z1 }, uGain: { value: gain } },
    vertexShader: `varying vec3 vP; varying vec3 vN; varying vec3 vV; void main(){ vP = position; vec4 mv = modelViewMatrix * vec4(position, 1.0);
      vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform float uTime, uFront, uAmt, uThermal, uZ0, uZ1, uGain; varying vec3 vP; varying vec3 vN; varying vec3 vV; ${GLSL_COMMON}
      void main(){ float r = length(vP.xy); float th = atan(vP.x, -vP.y);
        float f = clamp((vP.z - uZ0) / (uZ1 - uZ0), 0.0, 1.0);
        float n = fbm(vec3(th * 3.0 + vP.z * 0.8, r * 4.0, vP.z * 2.2 - uTime * 3.2));
        float n2 = fbm(vec3(th * 7.0 - uTime * 0.6, vP.z * 5.0 - uTime * 5.0, r * 9.0));
        float front = smoothstep(uFront + 0.05, uFront - 0.35, vP.z);
        float edge = smoothstep(0.0, 0.08, f) * (1.0 - smoothstep(0.85, 1.0, f));
        float a = front * edge * smoothstep(0.35, 0.85, n + 0.35 * n2) * (0.35 + 0.65 * abs(dot(vN, vV)));
        vec3 c = mix(vec3(1.0, 0.82, 0.5), vec3(1.0, 0.34, 0.05), smoothstep(0.2, 0.9, f + 0.3 * (n2 - 0.5))) * (1.2 + 1.6 * n2);
        c = mix(c, thermalColor(1.2 - 0.12 * f) * 1.2, uThermal);
        gl_FragColor = vec4(c * a * uAmt * uGain, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
  });
  for (let i = 0; i < layers; i++) {
    const q = (i + 0.5) / layers, pr = [];
    for (let j = 0; j <= 20; j++) { const f = j / 20, z = lerp(z0, z1, f), e = sstep(0.4, 1.0, f);
      pr.push(new THREE.Vector2(lerp(lerp(rA[0], rA[1], q), lerp(rB[0], rB[1], q), e), z)); }
    const g = new THREE.LatheGeometry(pr, 96, cutStart, cutLen); g.rotateX(Math.PI / 2);
    grp.add(new THREE.Mesh(g, mat));
  }
  grp.userData.mat = mat;
  return grp;
}

/**
 * Motion blur for a spinning rotor: K translucent ghost copies of the blade ring (and disc), trailing the rotor by
 * fractions of the shutter angle. setBlur(omega) takes the angular speed (rad/s) and spreads the ghosts over
 * omega * shutter (capped at one blade pitch * 2.2 so a fast rotor becomes a continuous smeared ring).
 */
export function rotorBlur(hs, { K = 7, shutter = 1 / 48, opacity = 0.32 } = {}) {
  if ((window.BENCH || {}).noBlur) K = 0;
  const ghosts = [];
  for (let k = 1; k <= K; k++) {
    const m = hotMetal({ roughness: 0.42 }); m.transparent = true; m.depthWrite = false; m.opacity = opacity;
    const g = new THREE.InstancedMesh(hs.ring.geometry, m, hs.ring.count);
    for (let i = 0; i < hs.ring.count; i++) { const M = new THREE.Matrix4(); hs.ring.getMatrixAt(i, M); g.setMatrixAt(i, M); }
    g.instanceMatrix.needsUpdate = true; g.frustumCulled = false; g.renderOrder = 2;
    const holder = new THREE.Group(); holder.add(g); hs.rotor.add(holder); ghosts.push({ holder, m });
  }
  const pitch = (Math.PI * 2) / DIM.N;
  return {
    ghosts,
    setBlur(omega, ringOpacity = 1) {
      const spread = Math.min(Math.abs(omega) * shutter, pitch * 2.2), on = spread > 0.004;
      ghosts.forEach((q, i) => { const f = (i + 1) / K; q.holder.visible = on; q.holder.rotation.z = -Math.sign(omega) * spread * f;
        q.m.opacity = opacity * (1 - 0.6 * f) * clamp(spread / 0.05) ; });
      hs.bladeMat.transparent = ringOpacity < 0.999; hs.bladeMat.opacity = ringOpacity;
    },
  };
}

/** Stylised low-poly red double-decker bus (no branding), length along X, wheels on y = 0 */
export function makeBus() {
  const grp = new THREE.Group();
  const L = 1.5, H = 0.6, W = 0.36;
  const paint = new THREE.MeshPhysicalMaterial({ color: 0xc81e1e, roughness: 0.38, metalness: 0.1, clearcoat: 0.8, clearcoatRoughness: 0.25 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x0b0f16, roughness: 0.12, metalness: 0.4, clearcoat: 1.0 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x111214, roughness: 0.8 });
  const body = new THREE.Mesh(new RoundedBoxGeometry(L, H, W, 3, 0.05), paint); body.position.y = 0.07 + H / 2; grp.add(body);
  for (const [y, h] of [[0.07 + 0.24, 0.13], [0.07 + 0.47, 0.12]]) for (const zs of [-1, 1]) {
    const win = new THREE.Mesh(new THREE.BoxGeometry(L * 0.86, h, 0.01), glass); win.position.set(-0.02, y, zs * (W / 2 + 0.002)); grp.add(win);
    // window pillars
    for (let i = 0; i < 7; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.018, h + 0.004, 0.014), paint); p.position.set(-L * 0.43 + (i + 0.5) * (L * 0.86 / 7), y, zs * (W / 2 + 0.004)); grp.add(p); }
  }
  for (const y of [0.07 + 0.24, 0.07 + 0.47]) { const ws = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.13, W * 0.82), glass); ws.position.set(L / 2 + 0.002, y, 0); grp.add(ws); }
  const band = new THREE.Mesh(new THREE.BoxGeometry(L * 1.002, 0.03, W * 1.01), new THREE.MeshPhysicalMaterial({ color: 0xe8e2d6, roughness: 0.5 })); band.position.y = 0.07 + 0.375; grp.add(band);
  for (const x of [-L * 0.32, L * 0.3]) for (const zs of [-1, 1]) {
    const wg = new THREE.CylinderGeometry(0.075, 0.075, 0.06, 20); wg.rotateX(Math.PI / 2);
    const w = new THREE.Mesh(wg, dark); w.position.set(x, 0.075, zs * (W / 2 - 0.02)); grp.add(w);
  }
  grp.userData.size = { L, H: H + 0.07, W };
  return grp;
}

/** translucent trailing copies of any mesh (for motion blur of a rotating part); returns setSpread(angle about Z) */
export function ghostTrail(mesh, parent, { K = 6, opacity = 0.3 } = {}) {
  const out = [];
  for (let k = 1; k <= K; k++) {
    const src = mesh.material; const m = src.clone(); if (src.onBeforeCompile) { m.onBeforeCompile = src.onBeforeCompile; m.customProgramCacheKey = src.customProgramCacheKey; }
    m.transparent = true; m.depthWrite = false; m.opacity = opacity;
    const g = mesh.isInstancedMesh ? new THREE.InstancedMesh(mesh.geometry, m, mesh.count) : new THREE.Mesh(mesh.geometry, m);
    if (mesh.isInstancedMesh) { for (let i = 0; i < mesh.count; i++) { const M = new THREE.Matrix4(); mesh.getMatrixAt(i, M); g.setMatrixAt(i, M); } g.instanceMatrix.needsUpdate = true; }
    g.frustumCulled = false; g.renderOrder = 2;
    const h = new THREE.Group(); h.add(g); parent.add(h); out.push({ h, m });
  }
  return { setSpread(a) { out.forEach((q, i) => { const f = (i + 1) / K; q.h.rotation.z = -a * f; q.h.visible = Math.abs(a) > 0.003; q.m.opacity = opacity * (1 - 0.6 * f); }); } };
}

// ---------------------------------------------------------------------------------------------------------------
// A2: generic cutaway low-bypass military turbofan with afterburner (illustration, not a specific engine):
// spinner, 3-stage fan, 7-stage HP compressor, annular combustor + HP turbine stage (the shared hot section),
// 2-stage LP turbine, afterburner duct with flame holders, convergent nozzle. Solids are cut away (sector kept as in
// buildHotSection); amber blueprint lines show the whole engine and fade once the metal sweep passes.
export const lineMat = () => new THREE.ShaderMaterial({
  uniforms: { uSweep: U.uSweep, uSweepOn: U.uSweepOn, uAmt: { value: 1 }, uColor: { value: new THREE.Color(0xf97316) } },
  vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
  fragmentShader: `uniform float uSweep, uSweepOn, uAmt; uniform vec3 uColor; varying vec3 vW;
    void main(){ float behind = uSweepOn > 0.5 ? smoothstep(uSweep - 0.2, uSweep - 1.6, vW.z) : 0.0;
      float seam = uSweepOn > 0.5 ? exp(-pow((vW.z - uSweep) / 0.4, 2.0)) : 0.0;
      gl_FragColor = vec4(uColor * (0.55 + 2.5 * seam) * (1.0 - behind) * uAmt, 1.0); }`,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
});
function edgeLines(geo, matrices, mat, deg = 28) {
  const e = new THREE.EdgesGeometry(geo, deg).attributes.position.array, out = new Float32Array(e.length * matrices.length), v = new THREE.Vector3();
  let o = 0; for (const M of matrices) for (let i = 0; i < e.length; i += 3) { v.set(e[i], e[i + 1], e[i + 2]).applyMatrix4(M); out[o++] = v.x; out[o++] = v.y; out[o++] = v.z; }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(out, 3));
  const l = new THREE.LineSegments(g, mat); l.frustumCulled = false; return l;
}
function latheLines(pr, mat, nLong = 24, nSeg = 96) {
  const pos = [];
  for (const [r, z] of pr) for (let i = 0; i < nSeg; i++) { const a0 = (i / nSeg) * Math.PI * 2, a1 = ((i + 1) / nSeg) * Math.PI * 2;
    pos.push(r * Math.sin(a0), -r * Math.cos(a0), z, r * Math.sin(a1), -r * Math.cos(a1), z); }
  for (let k = 0; k < nLong; k++) { const a = (k / nLong) * Math.PI * 2; for (let i = 0; i < pr.length - 1; i++) {
    const [r0, z0] = pr[i], [r1, z1] = pr[i + 1]; pos.push(r0 * Math.sin(a), -r0 * Math.cos(a), z0, r1 * Math.sin(a), -r1 * Math.cos(a), z1); } }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  const l = new THREE.LineSegments(g, mat); l.frustumCulled = false; return l;
}
export function buildEngine(scene, { cutStart = -Math.PI * 0.08, cutLen = Math.PI * 1.16 } = {}) {
  const E = { group: new THREE.Group(), rotors: [], lines: new THREE.Group() };
  scene.add(E.group); scene.add(E.lines);
  const LM = lineMat(); E.lineMat = LM;
  const hs = buildHotSection(E.group, { casing: false, cutStart, cutLen }); E.hs = hs;
  E.lines.add(edgeLines(makeBlade({ M: 14, S: 6, holes: false }).geometry, ringMatrices(DIM.N, DIM.R), LM, 30));
  const metal = (c = 0x8f8b85, r = 0.42, T = 0.3) => hotMetal({ color: c, roughness: r, temp: TEMP_CONST(T), heatScale: 0.5 });
  const bladeMat = metal(0x9a968f, 0.38, 0.25), caseMat = metal(0x5d5b58, 0.5, 0.2), darkMat = metal(0x3c3c3d, 0.6, 0.15);
  caseMat.side = THREE.DoubleSide; darkMat.side = THREE.DoubleSide;
  const lathe = (pr, a0 = cutStart, al = cutLen, segs = 128) => { const g = new THREE.LatheGeometry(pr.map(([r, z]) => new THREE.Vector2(r, z)), segs, a0, al); g.rotateX(Math.PI / 2); return g; };
  const ring = (z, rHub, rTip, N, chord, { flip = false, stagger = flip ? 0.55 : -0.5, cam = 0.22, twist = flip ? 0 : 0.5, T = 0.12, rotor = true } = {}) => {
    const b = makeBlade({ H: rTip - rHub, chord, T, cam, stagger, twist, M: 12, S: 6, tip: false, platform: false, root: false, holes: false, flip });
    const M = ringMatrices(N, rHub, z, flip ? 0.05 : 0);
    const im = new THREE.InstancedMesh(b.geometry, bladeMat, N); M.forEach((m, i) => im.setMatrixAt(i, m)); im.instanceMatrix.needsUpdate = true; im.frustumCulled = false;
    const holder = new THREE.Group(); holder.add(im); E.group.add(holder); if (rotor) E.rotors.push({ g: holder, z });
    E.lines.add(edgeLines(b.geometry, M, LM, 35));
    return holder;
  };
  // spinner + fan (3 stages, wide chord, strong twist) with stators between
  const spin = [[0.0, -11.2], [0.25, -11.0], [0.45, -10.7], [0.58, -10.35], [0.62, -10.1]];
  E.group.add(new THREE.Mesh(lathe(spin, 0, Math.PI * 2, 64), bladeMat)); E.lines.add(latheLines(spin, LM, 16));
  [[-9.9, 0.62, 2.35, 22, 0.9], [-9.15, 0.72, 2.2, 26, 0.75], [-8.45, 0.82, 2.05, 30, 0.65]].forEach(([z, a, b, n, c], i) => {
    ring(z, a, b, n, c, { twist: 0.9, cam: 0.18, stagger: -0.7, T: 0.09 });
    ring(z + 0.38, a + 0.05, b - 0.03, n + 10, c * 0.55, { flip: true, rotor: false }); });
  // HP compressor: 7 stages, annulus narrowing toward the combustor
  for (let i = 0; i < 7; i++) { const f = i / 6, z = lerp(-7.7, -3.5, f), hub = lerp(0.95, 1.18, f), tip = lerp(1.78, 1.42, f);
    ring(z, hub, tip, Math.round(lerp(36, 60, f)), lerp(0.42, 0.24, f), { twist: 0.35, cam: 0.2, stagger: -0.65, T: 0.1 });
    ring(z + 0.3, hub + 0.01, tip - 0.01, Math.round(lerp(44, 70, f)), lerp(0.32, 0.2, f), { flip: true, rotor: false, stagger: 0.6 }); }
  // LP turbine: 2 stages behind the HP stage
  for (let i = 0; i < 2; i++) { const z = 0.75 + i * 0.6; ring(z, 1.02, 1.62 + 0.08 * i, 64, 0.26, { twist: 0.2, cam: 0.42, stagger: -0.2, T: 0.25 });
    ring(z - 0.3, 1.02, 1.58 + 0.08 * i, 56, 0.26, { flip: true, rotor: false, stagger: 0.55, cam: 0.38, T: 0.25 }); }
  // inner drum (hub), core casing, bypass duct + outer casing, afterburner, nozzle
  const hub = [[0.62, -10.1], [0.8, -8.4], [0.95, -7.9], [1.18, -3.4], [1.0, -2.8], [0.84, -2.6]];
  E.group.add(new THREE.Mesh(lathe(hub), darkMat)); E.lines.add(latheLines(hub, LM));
  const core = [[1.92, -8.2], [1.8, -7.6], [1.46, -3.3], [1.72, -2.6], [2.02, -2.4], [2.02, -0.9], [1.9, -0.3], [1.84, 0.4], [1.84, 1.9]];
  E.group.add(new THREE.Mesh(lathe(core), caseMat)); E.lines.add(latheLines(core, LM));
  const outer = [[2.45, -10.6], [2.5, -9.6], [2.42, -8.2], [2.38, -4], [2.36, 1.8], [2.3, 7.4], [2.12, 8.6], [1.72, 9.5]];
  E.group.add(new THREE.Mesh(lathe(outer), darkMat)); E.lines.add(latheLines(outer, LM, 28));
  const ab = [[1.86, 1.9], [1.95, 3], [1.98, 7.3], [1.62, 9.3]];
  E.group.add(new THREE.Mesh(lathe(ab), caseMat)); E.lines.add(latheLines(ab, LM, 20));
  const cone = [[1.0, 1.9], [0.7, 2.6], [0.25, 3.4], [0.0, 3.6]];
  E.group.add(new THREE.Mesh(lathe(cone), darkMat)); E.lines.add(latheLines(cone, LM, 12));
  for (const [r, z] of [[0.9, 3.5], [1.45, 3.7]]) { const tg = new THREE.TorusGeometry(r, 0.05, 8, 96); tg.translate(0, 0, z); E.group.add(new THREE.Mesh(tg, caseMat)); E.lines.add(latheLines([[r, z]], LM, 0)); }
  return E;
}
