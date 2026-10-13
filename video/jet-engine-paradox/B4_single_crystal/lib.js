// Session B shared library for "The Jet Engine Paradox" (thermal world, "The Hot Section").
// Source of truth: video/jet-engine-paradox/_b_lib/lib.js; `sync.sh` copies it into every B scene folder as lib.js.
// Everything here is a pure function of time t: seeded RNG, no Date.now, no state stepped between frames.
import * as THREE from "three";
import { HDRLoader } from "three/addons/loaders/HDRLoader.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer, RenderPass, EffectPass, BloomEffect, ToneMappingEffect, ToneMappingMode, VignetteEffect,
  Effect, EffectAttribute } from "postprocessing";

export { THREE };
// HyperFrames' three adapter waits on window.THREE.DefaultLoadingManager before capturing a frame.
window.THREE = THREE;

// ---------------------------------------------------------------- math helpers
export const mulberry32 = (s) => () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, k) => a + (b - a) * k;
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const sm = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const smr = (t, a, b) => sm(seg(t, a, b));
export const inOut = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const outC = (x) => 1 - Math.pow(1 - clamp(x), 3);
export const inC = (x) => Math.pow(clamp(x), 3);
export const inOutS = (x) => { x = clamp(x); return x < 0.5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2; };
// log-space interpolation: constant perceived speed for big zooms
export const logLerp = (a, b, k) => Math.exp(lerp(Math.log(a), Math.log(b), k));

export const PAL = {
  slate: 0x0b0e14, amber: 0xf97316, amberHot: 0xfdba74, red: 0xef4444, white: 0xf8fafc, cyan: 0x38bdf8,
  metal: 0x9b9a97,  // warm grey nickel superalloy
};
export const col = (hex, mul = 1) => new THREE.Color(hex).multiplyScalar(mul);

// ---------------------------------------------------------------- GLSL snippets
const GLSL_COMMON = /* glsl */ `
vec3 hash33(vec3 p){ p = fract(p * vec3(.1031, .1030, .0973)); p += dot(p, p.yxz + 33.33);
  return fract((p.xxy + p.yxx) * p.zyx); }
float hash13(vec3 p){ p = fract(p * .1031); p += dot(p, p.zyx + 31.32); return fract((p.x + p.y) * p.z); }
float vnoise3(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3. - 2. * f);
  return mix(mix(mix(hash13(i), hash13(i + vec3(1,0,0)), f.x), mix(hash13(i + vec3(0,1,0)), hash13(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hash13(i + vec3(0,0,1)), hash13(i + vec3(1,0,1)), f.x), mix(hash13(i + vec3(0,1,1)), hash13(i + vec3(1,1,1)), f.x), f.y), f.z); }
float fbm3(vec3 p){ float a = .5, s = 0.; for (int i = 0; i < 4; i++){ s += a * vnoise3(p); p = p * 2.03 + vec3(1.7, 9.2, 3.1); a *= .5; } return s; }
vec3 ironbow(float x){ x = clamp(x, 0., 1.);
  vec3 c = mix(vec3(.02, .0, .05), vec3(.30, .0, .35), smoothstep(.0, .22, x));
  c = mix(c, vec3(.80, .10, .06), smoothstep(.18, .45, x));
  c = mix(c, vec3(1., .42, .05), smoothstep(.42, .70, x));
  c = mix(c, vec3(1., .80, .40), smoothstep(.68, .92, x));
  return mix(c, vec3(1., 1., .92), smoothstep(.90, 1., x)); }
`;

// ---------------------------------------------------------------- post: lens (heat shimmer, CA, grain)
class LensEffect extends Effect {
  constructor() {
    super("JepLens", /* glsl */ `
      uniform float uT; uniform float uShimmer; uniform vec4 uShimBand; uniform float uCA; uniform float uGrain;
      float lh(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor){
        vec2 d = vec2(0.);
        if (uShimmer > 0.) {
          float m = smoothstep(uShimBand.x, uShimBand.y, uv.y) * (1. - smoothstep(uShimBand.z, uShimBand.w, uv.y));
          d = uShimmer * m * vec2(sin(uv.y * 85. + uT * 9.1) + .5 * sin(uv.x * 140. - uT * 6.3 + uv.y * 31.),
                                  cos(uv.x * 72. - uT * 7.7) + .5 * sin(uv.y * 118. + uT * 8.4)) * .0011;
        }
        vec2 c = uv - .5; vec2 off = c * uCA * dot(c, c);
        vec2 u2 = uv + d;
        vec4 g = texture2D(inputBuffer, u2);
        vec3 o = vec3(texture2D(inputBuffer, u2 + off).r, g.g, texture2D(inputBuffer, u2 - off).b);
        float n = lh(floor(uv * resolution) + vec2(fract(uT * 7.31) * 91.7, fract(uT * 3.17) * 37.3)) - .5;
        o += n * uGrain * (.35 + .65 * (1. - o));
        outputColor = vec4(o, g.a);
      }`, {
      attributes: EffectAttribute.CONVOLUTION,
      uniforms: new Map([["uT", new THREE.Uniform(0)], ["uShimmer", new THREE.Uniform(0)],
        ["uShimBand", new THREE.Uniform(new THREE.Vector4(-1, 0, 2, 3))], ["uCA", new THREE.Uniform(0.006)],
        ["uGrain", new THREE.Uniform(0.045)]]),
    });
  }
}

// ---------------------------------------------------------------- backdrop: dark slate with slow amber haze/smoke
function makeBackdrop(o = {}) {
  const u = {
    uT: { value: 0 }, uBase: { value: col(o.base ?? 0x1a2030) }, uTop: { value: col(o.top ?? 0x262d3e) },
    uGlow: { value: col(o.glow ?? 0xff8a2a) }, uGlowDir: { value: new THREE.Vector3(...(o.glowDir ?? [0.4, -0.3, -1])).normalize() },
    uGlowAmt: { value: o.glowAmt ?? 0.05 }, uLift: { value: o.lift ?? 1.0 }, uGlowPow: { value: o.glowPow ?? 6.0 },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms: u, side: THREE.BackSide, depthWrite: false, depthTest: false,
    vertexShader: `varying vec3 vDir; void main(){ vDir = position; vec4 p = projectionMatrix * modelViewMatrix * vec4(position, 1.); gl_Position = p.xyww; }`,
    fragmentShader: GLSL_COMMON + /* glsl */ `
      uniform float uT, uGlowAmt, uLift, uGlowPow; uniform vec3 uBase, uTop, uGlow, uGlowDir; varying vec3 vDir;
      void main(){ vec3 d = normalize(vDir);
        float n = fbm3(d * 2.4 + vec3(uT * .03, -uT * .07, uT * .02));
        float n2 = fbm3(d * 5.5 + vec3(-uT * .05, -uT * .13, uT * .01));
        float g = pow(max(dot(d, uGlowDir), 0.), uGlowPow);
        vec3 c = mix(uBase, uTop, smoothstep(-.7, .8, d.y)) * (.7 + .6 * n) * uLift;
        c += uGlow * uGlowAmt * g * (.35 + 1.4 * n * n2);
        gl_FragColor = vec4(c, 1.); }`,
  });
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(40, 48, 24), mat);
  mesh.renderOrder = -1000; mesh.frustumCulled = false;
  // haze anchored to the view: glowScreen = [right, up] offset from the view axis (camera-relative)
  const gs = o.glowScreen ?? [0.35, -0.25]; const f = new THREE.Vector3(), r = new THREE.Vector3(), up = new THREE.Vector3();
  return { mesh, u, update(t, cam) { u.uT.value = t; mesh.position.copy(cam.position);
    cam.getWorldDirection(f); r.crossVectors(f, cam.up).normalize(); up.crossVectors(r, f).normalize();
    if (o.glowScreen !== null) u.uGlowDir.value.copy(f).addScaledVector(r, gs[0]).addScaledVector(up, gs[1]).normalize(); } };
}

// ---------------------------------------------------------------- stage
export function createStage(o = {}) {
  const root = document.getElementById("root");
  const W = +root.dataset.width, H = +root.dataset.height;
  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("gl"), antialias: false, stencil: false,
    depth: false, powerPreference: "high-performance", preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.NoToneMapping;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0b0e14);
  const camera = new THREE.PerspectiveCamera(o.fov ?? 30, W / H, o.near ?? 0.02, o.far ?? 80);
  const backdrop = makeBackdrop(o.bg); scene.add(backdrop.mesh);

  const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType, multisampling: o.msaa ?? 4 });
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new BloomEffect({ intensity: o.bloom ?? 1.1, luminanceThreshold: o.bloomThreshold ?? 0.9,
    luminanceSmoothing: 0.25, mipmapBlur: true, radius: o.bloomRadius ?? 0.75 });
  const vignette = new VignetteEffect({ darkness: o.vignette ?? 0.42, offset: 0.3 });
  const tone = new ToneMappingEffect({ mode: o.tone === "agx" ? ToneMappingMode.AGX : ToneMappingMode.ACES_FILMIC });
  composer.addPass(o.noBloom ? new EffectPass(camera, vignette, tone) : new EffectPass(camera, bloom, vignette, tone));
  const lens = new LensEffect();
  composer.addPass(new EffectPass(camera, lens));
  composer.setSize(W, H);

  scene.environmentIntensity = o.envIntensity ?? 1.0;
  const hdri = new HDRLoader().loadAsync("vendor/library/hdri/studio_small_09_1k.hdr").then((tex) => {
    const pm = new THREE.PMREMGenerator(renderer);
    scene.environment = pm.fromEquirectangular(tex).texture;
    tex.dispose(); pm.dispose();
  });
  const waits = [hdri];
  if (o.fonts) waits.push(fontsReady(o.fonts));
  const ready = Promise.all(waits);
  const L = (k) => lens.uniforms.get(k);
  return {
    root, W, H, renderer, scene, camera, composer, bloom, vignette, tone, lens, backdrop, ready,
    shimmer(amount, band) { L("uShimmer").value = amount; if (band) L("uShimBand").value.set(...band); },
    render(t) { backdrop.update(t, camera); L("uT").value = t; composer.render(1 / 30); },
    start(renderAt) {
      let ok = false, last = window.__hfThreeTime || 0;
      window.addEventListener("hf-seek", (ev) => { last = ev.detail.time; if (ok) renderAt(last); });
      ready.then(() => { ok = true; renderAt(window.__hfThreeTime ?? last); if (window.__jepReady) window.__jepReady(); });
    },
  };
}

// Canvas text needs Inter loaded first; register with Three's default manager so HyperFrames waits for it.
export function fontsReady(specs) {
  const m = THREE.DefaultLoadingManager; m.itemStart("jep-fonts");
  return Promise.all(specs.map((s) => document.fonts.load(s))).then(() => m.itemEnd("jep-fonts"), () => m.itemEnd("jep-fonts"));
}

// Standard light rig for hot metal: warm key, amber rim from behind (heat), neutral soft fill. No cyan light (cyan = air only).
export function lightRig(scene, o = {}) {
  const key = new THREE.DirectionalLight(0xffffff, o.key ?? 1.6); key.position.set(3, 4, 5);
  const rim = new THREE.DirectionalLight(PAL.amber, o.rim ?? 2.4); rim.position.set(-4, -0.6, -4);
  const fill = new THREE.DirectionalLight(0xdfe6f0, o.fill ?? 0.35); fill.position.set(-3, -1, 4);
  scene.add(key, rim, fill);
  return { key, rim, fill };
}

export function orbit(camera, target, r, az, el, roll = 0) {
  camera.position.set(target.x + r * Math.cos(el) * Math.sin(az), target.y + r * Math.sin(el), target.z + r * Math.cos(el) * Math.cos(az));
  camera.up.set(Math.sin(roll), Math.cos(roll), 0);
  camera.lookAt(target);
}

// ---------------------------------------------------------------- particles: embers / dust (Points), f(t)
export function makeEmbers(o) {
  const N = o.count ?? 160, rng = mulberry32(o.seed ?? 11);
  const box = o.box ?? { min: [-3, -2, -3], size: [6, 4, 6] };
  const geo = new THREE.BufferGeometry();
  const pos = new Float32Array(N * 3), size = new Float32Array(N), bright = new Float32Array(N);
  const P = Array.from({ length: N }, () => ({ x: rng(), y: rng(), z: rng(), v: 0.4 + rng() * 0.8, s: rng(), f: rng() * 6.28,
    w: 0.5 + rng() * 2.0, a: 0.05 + rng() * 0.12 }));
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("aSize", new THREE.BufferAttribute(size, 1));
  geo.setAttribute("aBright", new THREE.BufferAttribute(bright, 1));
  const u = { uColor: { value: col(o.color ?? PAL.amberHot, o.intensity ?? 3.0) }, uScale: { value: o.scale ?? 900 }, uAmt: { value: 1 } };
  const mat = new THREE.ShaderMaterial({
    uniforms: u, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: `attribute float aSize; attribute float aBright; varying float vB; uniform float uScale;
      void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.); gl_Position = projectionMatrix * mv;
        gl_PointSize = clamp(aSize * uScale / -mv.z, 1.5, 90.); vB = aBright; }`,
    fragmentShader: `uniform vec3 uColor; uniform float uAmt; varying float vB;
      void main(){ float r = length(gl_PointCoord - .5) * 2.; float a = smoothstep(1., .0, r); a *= a;
        gl_FragColor = vec4(uColor * vB * uAmt, a); }`,
  });
  const pts = new THREE.Points(geo, mat); pts.frustumCulled = false;
  const dir = o.dir ?? [0, 1, 0];
  const speed = o.speed ?? 0.25, sMin = o.sizeMin ?? 0.012, sMax = o.sizeMax ?? 0.04;
  return {
    points: pts, u,
    update(t) {
      for (let i = 0; i < N; i++) {
        const p = P[i];
        let k = (p.y + p.v * speed * t / box.size[1]) % 1;  // travel along dir, wrapped
        const fade = Math.sin(Math.PI * k);
        const sway = Math.sin(t * p.w + p.f) * p.a;
        const x = box.min[0] + box.size[0] * p.x + sway * (1 - Math.abs(dir[0]));
        const y = box.min[1] + box.size[1] * (dir[1] !== 0 ? k : p.y) + Math.cos(t * p.w * 0.7 + p.f) * p.a * 0.5;
        const z = box.min[2] + box.size[2] * p.z;
        pos[i * 3] = dir[0] !== 0 ? box.min[0] + box.size[0] * k : x; pos[i * 3 + 1] = y; pos[i * 3 + 2] = z;
        size[i] = lerp(sMin, sMax, p.s * p.s);
        bright[i] = fade * (0.55 + 0.45 * Math.sin(t * (3 + p.w * 2) + p.f * 3)) * (0.35 + 0.65 * (1 - p.s));
      }
      geo.attributes.position.needsUpdate = true; geo.attributes.aSize.needsUpdate = true; geo.attributes.aBright.needsUpdate = true;
    },
  };
}

// ---------------------------------------------------------------- streak ribbons (camera-facing), set per frame
export class Streaks {
  constructor(N, o = {}) {
    this.N = N;
    const geo = new THREE.BufferGeometry();
    this.pos = new Float32Array(N * 12); this.uvA = new Float32Array(N * 8); this.al = new Float32Array(N * 4); this.cl = new Float32Array(N * 12);
    const idx = new Uint32Array(N * 6);
    for (let i = 0; i < N; i++) {
      this.uvA.set([0, -1, 0, 1, 1, -1, 1, 1], i * 8);
      idx.set([i * 4, i * 4 + 2, i * 4 + 1, i * 4 + 1, i * 4 + 2, i * 4 + 3], i * 6);
    }
    geo.setAttribute("position", new THREE.BufferAttribute(this.pos, 3));
    geo.setAttribute("aUv", new THREE.BufferAttribute(this.uvA, 2));
    geo.setAttribute("aA", new THREE.BufferAttribute(this.al, 1));
    geo.setAttribute("aC", new THREE.BufferAttribute(this.cl, 3));
    geo.setIndex(new THREE.BufferAttribute(idx, 1));
    this.geo = geo;
    this.mat = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: o.blending ?? THREE.AdditiveBlending, side: THREE.DoubleSide,
      depthTest: o.depthTest ?? true,
      vertexShader: `attribute vec2 aUv; attribute float aA; attribute vec3 aC; varying vec2 vUv; varying float vA; varying vec3 vC;
        void main(){ vUv = aUv; vA = aA; vC = aC; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
      fragmentShader: `varying vec2 vUv; varying float vA; varying vec3 vC;
        void main(){ float across = 1. - abs(vUv.y); float a = pow(across, 1.6) * pow(vUv.x, 1.3) * vA;
          gl_FragColor = vec4(vC, a); }`,
    });
    this.mesh = new THREE.Mesh(geo, this.mat); this.mesh.frustumCulled = false;
    this._s = new THREE.Vector3(); this._d = new THREE.Vector3(); this._v = new THREE.Vector3();
  }
  // tail -> head; uv.x = 0 at tail, 1 at head
  set(i, tail, head, width, alpha, c, camPos) {
    const d = this._d.subVectors(head, tail), v = this._v.subVectors(camPos, head);
    const s = this._s.crossVectors(d, v); const L = s.length() || 1; s.multiplyScalar(width / L);
    const p = this.pos, o = i * 12;
    p[o] = tail.x - s.x; p[o + 1] = tail.y - s.y; p[o + 2] = tail.z - s.z;
    p[o + 3] = tail.x + s.x; p[o + 4] = tail.y + s.y; p[o + 5] = tail.z + s.z;
    p[o + 6] = head.x - s.x; p[o + 7] = head.y - s.y; p[o + 8] = head.z - s.z;
    p[o + 9] = head.x + s.x; p[o + 10] = head.y + s.y; p[o + 11] = head.z + s.z;
    this.al.fill(alpha, i * 4, i * 4 + 4);
    for (let k = 0; k < 4; k++) { this.cl[i * 12 + k * 3] = c.r; this.cl[i * 12 + k * 3 + 1] = c.g; this.cl[i * 12 + k * 3 + 2] = c.b; }
  }
  hide(i) { this.al.fill(0, i * 4, i * 4 + 4); }
  commit() { const a = this.geo.attributes; a.position.needsUpdate = true; a.aA.needsUpdate = true; a.aC.needsUpdate = true; }
}

// Polyline with arc-length lookup (for particle paths)
export class Path {
  constructor(points) {
    this.p = points; this.cum = [0];
    for (let i = 1; i < points.length; i++) this.cum.push(this.cum[i - 1] + points[i].distanceTo(points[i - 1]));
    this.len = this.cum[this.cum.length - 1];
  }
  at(u, out = new THREE.Vector3()) {  // u in [0,1] by arc length
    const s = clamp(u) * this.len, c = this.cum;
    let lo = 0, hi = c.length - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (c[m] <= s) lo = m; else hi = m; }
    const k = (s - c[lo]) / ((c[hi] - c[lo]) || 1);
    return out.lerpVectors(this.p[lo], this.p[hi], k);
  }
}
export function smoothPath(ctrl, n = 200) {
  const curve = new THREE.CatmullRomCurve3(ctrl, false, "centripetal");
  return new Path(curve.getSpacedPoints(n));
}

// ---------------------------------------------------------------- metal material with optional features
// features: HOLES (film-cooling holes from aSurf), WORLEY (micro-grains on the blade), LATTICE (FCC atoms),
// BLOCK (Voronoi grain shading with neighbour seeds), SWEEP (light band), SCAN (clip by height), HEAT (ironbow emissive)
export function metalMaterial(features = [], o = {}) {
  const u = {
    uT: { value: 0 },
    uHoles: { value: 1 }, uHoleCyan: { value: 0 }, uHoleCyanCol: { value: col(PAL.cyan, 2.2) },
    uGrain: { value: 0 }, uGrainScale: { value: 90 }, uGrainLum: { value: 0.35 },
    uRot: { value: new THREE.Matrix3() }, uLatFreq: { value: 25 }, uAtoms: { value: 1 }, uAtomR: { value: 0.5 },
    uSelf: { value: new THREE.Vector3() }, uNb: { value: Array.from({ length: 20 }, () => new THREE.Vector3(99, 99, 99)) },
    uNbN: { value: 0 }, uBoundary: { value: 0 }, uGroove: { value: 1 }, uLineW: { value: 0.012 }, uEtch: { value: 0 },
    uRed: { value: col(0xff1c12, 2.4) },
    uSweepN: { value: new THREE.Vector3(1, 0, 0) }, uSweepPos: { value: -9 }, uSweepAmt: { value: 0 }, uSweepW: { value: 0.12 },
    uSweepCol: { value: col(0xfff3e0, 2.5) },
    uScanY: { value: 99 }, uScanDir: { value: 1 }, uScanEdge: { value: col(PAL.amberHot, 4) },
    uHeat: { value: 0 }, uHeatAxis: { value: new THREE.Vector3(0, -1, 0) }, uHeatOff: { value: 0 }, uHeatSpread: { value: 1 },
    uHeatGain: { value: 2.5 }, uCool: { value: 0 }, uCoolFront: { value: 0 },
    uDissR: { value: -1 }, uRes: { value: new THREE.Vector2(1920, 1080) }, uDissCol: { value: col(PAL.amberHot, 5) },
    ...(o.uniforms || {}),
  };
  const mat = new THREE.MeshPhysicalMaterial({
    color: col(o.color ?? PAL.metal), metalness: o.metalness ?? 1.0, roughness: o.roughness ?? 0.4,
    envMapIntensity: o.env ?? 1.0, clearcoat: o.clearcoat ?? 0, clearcoatRoughness: 0.35,
    transparent: !!o.transparent, opacity: o.opacity ?? 1, side: o.side ?? THREE.FrontSide,
  });
  if (o.anisotropy) { mat.anisotropy = o.anisotropy; mat.anisotropyRotation = o.anisotropyRotation ?? Math.PI / 2; }
  const F = new Set(features);
  mat.defines = {}; for (const f of F) mat.defines["F_" + f] = "";
  mat.customProgramCacheKey = () => "jepmetal:" + [...F].sort().join(",");
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, u);
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", `#include <common>
        attribute vec3 aSurf; attribute float aInt; varying vec3 vSurf; varying vec3 vRest; varying vec3 vRestN; varying float vInt; varying vec3 vWPos;`)
      .replace("#include <begin_vertex>", `#include <begin_vertex>
        vSurf = aSurf; vRest = position; vRestN = normal; vInt = aInt; vWPos = (modelMatrix * vec4(position, 1.)).xyz;`);
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", `#include <common>
        uniform mat3 normalMatrix;
        varying vec3 vSurf; varying vec3 vRest; varying vec3 vRestN; varying float vInt; varying vec3 vWPos;
        uniform float uT, uHoles, uHoleCyan, uGrain, uGrainScale, uGrainLum, uLatFreq, uAtoms, uAtomR;
        uniform vec3 uHoleCyanCol; uniform mat3 uRot; uniform vec3 uSelf; uniform vec3 uNb[20]; uniform int uNbN;
        uniform float uBoundary, uGroove, uLineW, uEtch; uniform vec3 uRed;
        uniform vec3 uSweepN; uniform float uSweepPos, uSweepAmt, uSweepW; uniform vec3 uSweepCol;
        uniform float uScanY, uScanDir; uniform vec3 uScanEdge;
        uniform float uHeat, uHeatOff, uHeatSpread, uHeatGain, uCool, uCoolFront; uniform vec3 uHeatAxis;
        uniform float uDissR; uniform vec2 uRes; uniform vec3 uDissCol;
        ${GLSL_COMMON}
        // film-cooling hole rows in surface coords p = (arc from leading edge, span y); returns normalised ellipse distance
        float holeRow(vec2 p, float arc0, float sp, float stag, float ra, float rs, float flare){
          float ys = (p.y - stag * sp) / sp; float cy = (floor(ys) + .5) * sp + stag * sp;
          if (cy < .07 || cy > 1.36) return 9.;
          float dx = p.x - arc0; float r = ra * (1. + flare * smoothstep(0., ra * 3., dx * sign(flare + 1e-4)));
          return length(vec2(dx / r, (p.y - cy) / rs)); }
        vec3 fccNearest(vec3 q){ vec3 r = floor(q + .5); if (mod(r.x + r.y + r.z, 2.) > .5) { vec3 d = q - r; vec3 a = abs(d);
          if (a.x >= a.y && a.x >= a.z) r.x += d.x >= 0. ? 1. : -1.; else if (a.y >= a.z) r.y += d.y >= 0. ? 1. : -1.; else r.z += d.z >= 0. ? 1. : -1.; }
          return r; }
        void voronoiEdge(vec3 x, out float edge, out vec3 cid){
          vec3 n = floor(x), f = fract(x); float f1 = 8., f2 = 8.; vec3 id = n;
          for (int k = -1; k <= 1; k++) for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) {
            vec3 g = vec3(float(i), float(j), float(k)); vec3 r = g + .1 + hash33(n + g) * .8 - f; float d = dot(r, r);
            if (d < f1) { f2 = f1; f1 = d; id = n + g; } else if (d < f2) f2 = d; }
          edge = (sqrt(f2) - sqrt(f1)) * .5; cid = id; }
      `)
      .replace("#include <clipping_planes_fragment>", `#include <clipping_planes_fragment>
        #ifdef F_SCAN
          float scanD = (vRest.y - uScanY) * uScanDir; if (scanD > 0.) discard;
          float scanEdge = exp(scanD / .012);
        #endif
        float dissEdge = 0.;
        #ifdef F_DISSOLVE
        { float dd = length((gl_FragCoord.xy - .5 * uRes) / uRes.y) + .12 * (fbm3(vec3(gl_FragCoord.xy / uRes.y * 9., 3.)) - .5);
          if (dd < uDissR) discard; dissEdge = 1. - smoothstep(0., .035, dd - uDissR); }
        #endif
        #ifdef F_REVEAL
        { float dd = length((gl_FragCoord.xy - .5 * uRes) / uRes.y) + .12 * (fbm3(vec3(gl_FragCoord.xy / uRes.y * 9., 3.)) - .5);
          if (dd > uDissR + .004) discard; }
        #endif
        float fHole = 0., fRim = 0.;
        #ifdef F_HOLES
        { vec2 p = vSurf.xy; float e = 9.;
          e = min(e, holeRow(p, -.048, .068, .0, .0075, .013, 0.));
          e = min(e, holeRow(p, .0, .068, .5, .0075, .013, 0.));
          e = min(e, holeRow(p, .048, .068, .0, .0075, .013, 0.));
          e = min(e, holeRow(p, .17, .075, .25, .0085, .011, 1.6));
          e = min(e, holeRow(p, -.15, .085, .5, .008, .010, -1.4));
          if (vSurf.x > 0. && vSurf.z < .2) e = min(e, holeRow(vec2(vSurf.z, vSurf.y), .06, .062, .0, .03, .011, 0.));
          float aa = fwidth(e) + 1e-3; fHole = (1. - smoothstep(1. - aa, 1. + aa, e)) * uHoles;
          fRim = smoothstep(.9, 1.15, e) * (1. - smoothstep(1.15, 1.7, e)) * uHoles; }
        #endif
        float fAtom = 0., fAtomVis = 0.; vec3 atomOt = vec3(0.);
        #ifdef F_LATTICE
        { vec3 q = uRot * (vRest * uLatFreq); vec3 c = fccNearest(q); vec3 o3 = q - c; float d = length(o3);
          float aa = fwidth(d) * 1.2 + 1e-4; fAtom = 1. - smoothstep(uAtomR - aa, uAtomR + aa, d);
          fAtomVis = uAtoms * (1. - smoothstep(.3, .65, length(fwidth(q))));
          vec3 oo = transpose(uRot) * o3 / uAtomR; vec3 nn = normalize(vRestN); atomOt = (oo - dot(oo, nn) * nn) * fAtom; }
        #endif
        float fBd = 1e3;
        #ifdef F_BLOCK
        for (int k = 0; k < 20; k++) { if (k >= uNbN) break; vec3 sj = uNb[k]; vec3 dv = sj - uSelf; float L = length(dv);
          fBd = min(fBd, dot((uSelf + sj) * .5 - vRest, dv / L)); }
        float bAA = fwidth(fBd) + 1e-4;
        float fGroove = (1. - smoothstep(uLineW * .5 - bAA, uLineW * .5 + bAA, fBd)) * (1. - vInt);
        float fGlow = exp(-max(fBd, 0.) / (uLineW * 1.3)) * (1. - vInt);
        #endif
        float fWorley = 0., fWEdge = 1.; vec3 wTint = vec3(1.);
        #ifdef F_WORLEY
        if (uGrain > .001) { vec3 cid; float ed; voronoiEdge(vRest * uGrainScale, ed, cid); vec3 h = hash33(cid * 1.31 + 7.);
          float wa = fwidth(ed) + 1e-3; fWEdge = smoothstep(.025 - wa, .025 + wa, ed);
          wTint = mix(vec3(.56, .57, .59), vec3(.70, .65, .58), h.y) * (.42 + .72 * h.x); fWorley = uGrain; }
        #endif
      `)
      .replace("#include <dithering_fragment>", `#include <dithering_fragment>
        if (any(isnan(gl_FragColor)) || any(isinf(gl_FragColor))) gl_FragColor = vec4(0., 0., 0., 1.);`)
      .replace("#include <color_fragment>", `#include <color_fragment>
        #ifdef F_HOLES
        float castN = fbm3(vRest * 13.) * .6 + fbm3(vRest * 47.) * .4;
        diffuseColor.rgb *= .86 + .24 * castN;
        if (vSurf.x < 90.) { diffuseColor.rgb *= mix(.42, 1., smoothstep(.0, .14, vRest.y));
          diffuseColor.rgb *= mix(vec3(1.), vec3(.86, .80, .74), .55 * smoothstep(.85, 1.45, vRest.y) + .25 * (1. - smoothstep(.0, .1, abs(vSurf.x)))); }
        #endif
        diffuseColor.rgb *= 1. - .93 * fHole;
        diffuseColor.rgb *= 1. + .25 * fRim;
        #ifdef F_LATTICE
          diffuseColor.rgb *= mix(1., mix(.3, 1.2, fAtom), fAtomVis);
        #endif
        #ifdef F_BLOCK
          diffuseColor.rgb *= 1. - .82 * fGroove * uGroove;
          diffuseColor.rgb *= mix(1., .45, vInt);
        #endif
        #ifdef F_WORLEY
          diffuseColor.rgb = mix(diffuseColor.rgb, wTint * mix(.12, 1., fWEdge), fWorley);
        #endif
      `)
      .replace("#include <roughnessmap_fragment>", `#include <roughnessmap_fragment>
        #ifdef F_HOLES
          roughnessFactor = clamp(roughnessFactor + .22 * (fbm3(vRest * 31.) - .5) + .1 * (fbm3(vRest * 90.) - .5), .2, .9);
        #endif
        roughnessFactor = mix(roughnessFactor, .85, fHole);
        #ifdef F_LATTICE
          roughnessFactor = mix(roughnessFactor, mix(.75, .3, fAtom), fAtomVis);
        #endif
        #ifdef F_WORLEY
          roughnessFactor = mix(roughnessFactor, .5, fWorley);
        #endif
      `)
      .replace("#include <normal_fragment_maps>", `#include <normal_fragment_maps>
        #ifdef F_LATTICE
          normal = normalize(mix(normal, normalize(normal * sqrt(max(1. - dot(atomOt, atomOt), .04)) + normalMatrix * atomOt), fAtomVis * fAtom));
        #endif
      `)
      .replace("#include <emissivemap_fragment>", `#include <emissivemap_fragment>
        totalEmissiveRadiance += uHoleCyanCol * uHoleCyan * fHole;
        #ifdef F_WORLEY
          totalEmissiveRadiance += wTint * uGrainLum * fWorley * fWEdge;
        #endif
        #ifdef F_BLOCK
          totalEmissiveRadiance += diffuseColor.rgb * uEtch;
          totalEmissiveRadiance += uRed * uBoundary * (fGlow * (1. - vInt) + vInt * (.75 + .25 * sin(uT * 6. + vRest.x * 9.)));
        #endif
        #ifdef F_SWEEP
        { float s = dot(vWPos, uSweepN) - uSweepPos; float band = exp(-s * s / (2. * uSweepW * uSweepW));
          totalEmissiveRadiance += uSweepCol * band * uSweepAmt * (.35 + .65 * fAtom); }
        #endif
        #ifdef F_HEAT
        { float hx = uHeatSpread < 0. ? 1. - smoothstep(0., -uHeatSpread, abs(vSurf.x)) : clamp((dot(vRest, uHeatAxis) - uHeatOff) / uHeatSpread, 0., 1.);
          float n = fbm3(vRest * 6. + vec3(0., -uT * .6, 0.));
          float cool = uCool * (1. - smoothstep(uCoolFront - .05, uCoolFront + .05, abs(vSurf.x)));
          float lvl = clamp(uHeat * (hx * .8 + .25 * n) * (1. - .85 * cool), 0., 1.);
          // hot metal glows red -> amber -> pale yellow (upper half of the ironbow ramp only: no purple on metal)
          totalEmissiveRadiance += ironbow(.42 + .5 * lvl) * uHeatGain * lvl * lvl; }
        #endif
        #ifdef F_DISSOLVE
          totalEmissiveRadiance += uDissCol * dissEdge * step(-.5, uDissR);
        #endif
        #ifdef F_SCAN
          totalEmissiveRadiance += uScanEdge * scanEdge;
        #endif
      `);
  };
  return { mat, u };
}

// ---------------------------------------------------------------- turbine blade (procedural)
// Coordinates: span along +y, platform top at y = 0, airfoil to y = SPAN; axial (gas flow) along +x; leading edge at -x.
// Suction (convex) side faces +z, pressure (concave) side faces -z.
export const SPAN = 1.45;
const K = 70;                      // points per side of the profile
function bez(P, s) { const a = 1 - s; return [a * a * a * P[0][0] + 3 * a * a * s * P[1][0] + 3 * a * s * s * P[2][0] + s * s * s * P[3][0],
  a * a * a * P[0][1] + 3 * a * a * s * P[1][1] + 3 * a * s * s * P[2][1] + s * s * s * P[3][1]]; }
function bezT(P, s) { const a = 1 - s; const dx = 3 * a * a * (P[1][0] - P[0][0]) + 6 * a * s * (P[2][0] - P[1][0]) + 3 * s * s * (P[3][0] - P[2][0]);
  const dz = 3 * a * a * (P[1][1] - P[0][1]) + 6 * a * s * (P[2][1] - P[1][1]) + 3 * s * s * (P[3][1] - P[2][1]); const L = Math.hypot(dx, dz); return [dx / L, dz / L]; }
const CAMBER = [[0, 0], [0.27, 0.23], [0.56, -0.24], [0.72, -0.64]];
const thick = (s) => { const f = 2.969 * Math.sqrt(s) - 1.26 * s - 3.516 * s * s + 2.843 * s ** 3 - 1.015 * s ** 4; return 0.175 * f / 0.6 + 0.008 * s; };

export function bladeParams() {
  // root-station camber centroid so the blade spins about its own axis
  let cx = 0, cz = 0; for (let k = 0; k <= 40; k++) { const c = bez(CAMBER, k / 40); cx += c[0]; cz += c[1]; } cx /= 41; cz /= 41;
  const station = (v) => ({ sc: 1.0 - 0.1 * v, tw: 0.1 - 0.32 * v, lean: 0.03 * v });
  // camber-space point -> world (x, z) at span fraction v, with offset along the local thickness normal (+ = suction side)
  const map = (s, v, off = 0) => {
    const c = bez(CAMBER, s), tg = bezT(CAMBER, s); const n = [-tg[1], tg[0]];
    let x = c[0] + n[0] * off - cx, z = c[1] + n[1] * off - cz; const st = station(v);
    x *= st.sc; z *= st.sc; const cs = Math.cos(st.tw), sn = Math.sin(st.tw);
    return [x * cs - z * sn + st.lean, x * sn + z * cs];
  };
  // local thickness direction (unit, in x-z) at camber s, span v
  const thickDir = (s, v) => { const a = map(s, v, 0), b = map(s, v, 0.01); const L = Math.hypot(b[0] - a[0], b[1] - a[1]); return [(b[0] - a[0]) / L, (b[1] - a[1]) / L]; };
  const halfThick = (s, v) => thick(s) * station(v).sc;
  return { map, thickDir, halfThick, station, cx, cz };
}

export function buildBlade(o = {}) {
  const BP = bladeParams();
  const NV = o.nv ?? 46, NU = 2 * K + 1;
  const prof = [];   // [s, side] around the loop: suction TE -> LE -> pressure TE
  for (let k = K; k >= 0; k--) prof.push([(1 - Math.cos(Math.PI * k / K)) / 2, +1]);
  for (let k = 1; k <= K; k++) prof.push([(1 - Math.cos(Math.PI * k / K)) / 2, -1]);
  const iLE = K;
  const pos = [], surf = [], uv = [], stations = [];
  for (let j = 0; j < NV; j++) {
    const v = j / (NV - 1), y = -0.03 + (SPAN + 0.03) * v;
    const pts = prof.map(([s, side]) => BP.map(s, v, side * thick(s)));
    const cum = [0]; for (let i = 1; i < NU; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const total = cum[NU - 1] + Math.hypot(pts[0][0] - pts[NU - 1][0], pts[0][1] - pts[NU - 1][1]);
    const aLE = cum[iLE], aP = cum[NU - 1] - aLE;
    stations.push({ y, pts, cum, aLE });
    for (let i = 0; i <= NU; i++) {
      const q = pts[i % NU]; const a = i === NU ? total : cum[i];
      pos.push(q[0], y, q[1]); surf.push(a - aLE, y, aP - (a - aLE)); uv.push(a * 2, y * 2);
    }
  }
  const idx = [];
  for (let j = 0; j < NV - 1; j++) for (let i = 0; i < NU; i++) {
    const a = j * (NU + 1) + i, b = a + 1, c = a + NU + 1, d = c + 1;
    idx.push(a, c, b, b, c, d);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("aSurf", new THREE.Float32BufferAttribute(surf, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setAttribute("aInt", new THREE.Float32BufferAttribute(new Float32Array(pos.length / 3), 1));
  g.setIndex(idx); g.computeVertexNormals();
  // make sure normals point outward (leading edge normal should point to -x)
  const nLE = g.attributes.normal.getX((NV >> 1) * (NU + 1) + iLE);
  if (nLE > 0) { for (let k = 0; k < idx.length; k += 3) { const t = idx[k + 1]; idx[k + 1] = idx[k + 2]; idx[k + 2] = t; } g.setIndex(idx); g.computeVertexNormals(); }

  // squealer tip: recessed floor with a thin rim, as on real HP blades (flat normals; triangles oriented explicitly)
  const top = stations[NV - 1], yT = top.y, yF = top.y - 0.045;
  let area = 0; for (let i = 0; i < NU; i++) { const a = top.pts[i], b = top.pts[(i + 1) % NU]; area += a[0] * b[1] - b[0] * a[1]; }
  const sgn = area > 0 ? 1 : -1;
  const inner = top.pts.map((p, i) => {
    const a = top.pts[(i - 1 + NU) % NU], b = top.pts[(i + 1) % NU]; let tx = b[0] - a[0], tz = b[1] - a[1]; const L = Math.hypot(tx, tz) || 1; tx /= L; tz /= L;
    const nx = -tz * sgn, nz = tx * sgn;  // inward
    const d = Math.min(0.02, 0.45 * thick(prof[i][0]) * BP.station(1).sc);
    return [p[0] + nx * d, p[1] + nz * d, nx, nz];
  });
  const cp = [];
  const tri = (A, B, C, n) => { const e1 = [B[0] - A[0], B[1] - A[1], B[2] - A[2]], e2 = [C[0] - A[0], C[1] - A[1], C[2] - A[2]];
    const c = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]];
    if (c[0] * n[0] + c[1] * n[1] + c[2] * n[2] < 0) cp.push(...A, ...C, ...B); else cp.push(...A, ...B, ...C); };
  const inTris = THREE.ShapeUtils.triangulateShape(inner.map((p) => new THREE.Vector2(p[0], p[1])), []);
  for (const t of inTris) tri([inner[t[0]][0], yF, inner[t[0]][1]], [inner[t[1]][0], yF, inner[t[1]][1]], [inner[t[2]][0], yF, inner[t[2]][1]], [0, 1, 0]);
  for (let i = 0; i < NU; i++) {
    const j = (i + 1) % NU, o0 = top.pts[i], o1 = top.pts[j], i0 = inner[i], i1 = inner[j];
    tri([o0[0], yT, o0[1]], [o1[0], yT, o1[1]], [i1[0], yT, i1[1]], [0, 1, 0]); tri([o0[0], yT, o0[1]], [i1[0], yT, i1[1]], [i0[0], yT, i0[1]], [0, 1, 0]);
    const wn = [(i0[2] + i1[2]) / 2, 0, (i0[3] + i1[3]) / 2];
    tri([i0[0], yF, i0[1]], [i1[0], yF, i1[1]], [i1[0], yT, i1[1]], wn); tri([i0[0], yF, i0[1]], [i1[0], yT, i1[1]], [i0[0], yT, i0[1]], wn);
  }
  const cap = new THREE.BufferGeometry();
  cap.setAttribute("position", new THREE.Float32BufferAttribute(cp, 3));
  const nCap = cp.length / 3, capSurf = new Float32Array(nCap * 3), capUv = new Float32Array(nCap * 2);
  for (let k = 0; k < nCap; k++) { capSurf[k * 3] = 99; capSurf[k * 3 + 1] = cp[k * 3 + 1]; capSurf[k * 3 + 2] = 99; capUv[k * 2] = cp[k * 3] * 2; capUv[k * 2 + 1] = cp[k * 3 + 2] * 2; }
  cap.setAttribute("aSurf", new THREE.BufferAttribute(capSurf, 3));
  cap.setAttribute("uv", new THREE.BufferAttribute(capUv, 2));
  cap.setAttribute("aInt", new THREE.BufferAttribute(new Float32Array(nCap), 1));
  cap.computeVertexNormals();

  // platform (rounded slab), shank, fir-tree root
  const plat = new RoundedBoxGeometry(1.34, 0.1, 0.84, 3, 0.022); plat.translate(-0.01, -0.05, 0.02);
  const shank = new RoundedBoxGeometry(1.02, 0.34, 0.25, 2, 0.02); shank.translate(0.0, -0.25, 0.0);
  const fir = new THREE.Shape();
  const R = [[0.12, 0], [0.17, -0.025], [0.208, -0.06], [0.198, -0.088], [0.142, -0.125], [0.168, -0.158], [0.162, -0.183],
    [0.112, -0.222], [0.128, -0.252], [0.12, -0.275], [0.078, -0.31], [0.07, -0.34], [0.0, -0.352]];
  const ptsR = R.map(([z, y]) => new THREE.Vector2(z, y));
  const ptsL = R.slice(0, -1).reverse().map(([z, y]) => new THREE.Vector2(-z, y));
  fir.moveTo(-0.12, 0.0); fir.lineTo(0.12, 0.0);
  fir.splineThru(ptsR.slice(1)); fir.splineThru(ptsL.slice(1)); fir.lineTo(-0.12, 0.0);
  const firG = new THREE.ExtrudeGeometry(fir, { depth: 0.9, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.01, bevelSegments: 2, curveSegments: 10, steps: 1 });
  firG.rotateY(Math.PI / 2); firG.translate(-0.45, -0.42, 0);
  for (const gg of [plat, shank, firG]) {
    const n = gg.attributes.position.count; const s = new Float32Array(n * 3); for (let i = 0; i < n; i++) { s[i * 3] = 99; s[i * 3 + 1] = gg.attributes.position.getY(i); s[i * 3 + 2] = 99; }
    gg.setAttribute("aSurf", new THREE.BufferAttribute(s, 3));
    gg.setAttribute("aInt", new THREE.BufferAttribute(new Float32Array(n), 1));
  }

  const { mat, u } = o.material ?? metalMaterial(o.features ?? ["HOLES"], o.matOpts ?? { anisotropy: 0.3, roughness: 0.5 });
  const group = new THREE.Group();
  const airfoil = new THREE.Mesh(g, mat), tip = new THREE.Mesh(cap, mat);
  const platform = new THREE.Mesh(plat, mat), shankM = new THREE.Mesh(shank, mat), root = new THREE.Mesh(firG, mat);
  const foil = new THREE.Group(); foil.add(airfoil, tip);
  group.add(foil, platform, shankM, root);

  // surface sampler: point + outward normal at (arc from LE, span y) — used to emit air from the hole rows
  const nrm = g.attributes.normal;
  function surfAt(arc, y, outP = new THREE.Vector3(), outN = new THREE.Vector3()) {
    const fj = clamp((y + 0.03) / (SPAN + 0.03)) * (NV - 1); const j0 = Math.min(NV - 2, Math.floor(fj)), kj = fj - j0;
    const P = [], N = [];
    for (const j of [j0, j0 + 1]) {
      const st = stations[j]; const target = st.aLE + arc; const c = st.cum;
      let i = 0; while (i < NU - 2 && c[i + 1] < target) i++;
      const k = clamp((target - c[i]) / ((c[i + 1] - c[i]) || 1));
      P.push(new THREE.Vector3(lerp(st.pts[i][0], st.pts[i + 1][0], k), st.y, lerp(st.pts[i][1], st.pts[i + 1][1], k)));
      const a = j * (NU + 1) + i;
      N.push(new THREE.Vector3(lerp(nrm.getX(a), nrm.getX(a + 1), k), lerp(nrm.getY(a), nrm.getY(a + 1), k), lerp(nrm.getZ(a), nrm.getZ(a + 1), k)));
    }
    outP.lerpVectors(P[0], P[1], kj); outN.lerpVectors(N[0], N[1], kj).normalize();
    return [outP, outN];
  }
  const arcLimits = (y) => { const fj = clamp((y + 0.03) / (SPAN + 0.03)) * (NV - 1); const st = stations[Math.round(fj)];
    return { suction: -st.aLE, pressure: st.cum[NU - 1] - st.aLE }; };
  return { group, foil, airfoil, tip, platform, shank: shankM, root, mat, u, surfAt, arcLimits, BP, geo: g };
}

// ---------------------------------------------------------------- Voronoi grains (convex polyhedra clipped from a box)
function clipPoly(faces, n, d, nb) {  // keep n.p <= d
  const out = [], cap = []; const eps = 1e-9;
  const addCap = (p) => { if (!cap.some((q) => q.distanceToSquared(p) < 1e-12)) cap.push(p); };
  for (const f of faces) {
    const vs = f.verts, res = [];
    for (let i = 0; i < vs.length; i++) {
      const a = vs[i], b = vs[(i + 1) % vs.length]; const da = n.dot(a) - d, db = n.dot(b) - d;
      if (da <= eps) { res.push(a); if (da > -eps) addCap(a); }
      if ((da < -eps && db > eps) || (da > eps && db < -eps)) { const p = a.clone().lerp(b, da / (da - db)); res.push(p); addCap(p); }
    }
    if (res.length >= 3) out.push({ verts: res, nb: f.nb });
  }
  if (cap.length >= 3) {
    const c = cap.reduce((s, p) => s.add(p), new THREE.Vector3()).multiplyScalar(1 / cap.length);
    const u = new THREE.Vector3().crossVectors(n, Math.abs(n.x) < 0.9 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0)).normalize();
    const v = new THREE.Vector3().crossVectors(n, u);
    cap.sort((a, b) => Math.atan2(a.clone().sub(c).dot(v), a.clone().sub(c).dot(u)) - Math.atan2(b.clone().sub(c).dot(v), b.clone().sub(c).dot(u)));
    out.push({ verts: cap, nb });
  }
  return out;
}
function boxFaces(mn, mx) {
  const V = (x, y, z) => new THREE.Vector3(x ? mx.x : mn.x, y ? mx.y : mn.y, z ? mx.z : mn.z);
  return [
    [V(1, 0, 0), V(1, 1, 0), V(1, 1, 1), V(1, 0, 1)], [V(0, 0, 0), V(0, 0, 1), V(0, 1, 1), V(0, 1, 0)],
    [V(0, 1, 0), V(0, 1, 1), V(1, 1, 1), V(1, 1, 0)], [V(0, 0, 0), V(1, 0, 0), V(1, 0, 1), V(0, 0, 1)],
    [V(0, 0, 1), V(1, 0, 1), V(1, 1, 1), V(0, 1, 1)], [V(0, 0, 0), V(0, 1, 0), V(1, 1, 0), V(1, 0, 0)],
  ].map((verts) => ({ verts, nb: -1 }));
}
export function jitterSeeds(nx, ny, nz, mn, mx, jitter, rng) {
  const s = [], d = new THREE.Vector3().subVectors(mx, mn);
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++)
    s.push(new THREE.Vector3(mn.x + d.x * (i + 0.5 + jitter * (rng() - 0.5)) / nx, mn.y + d.y * (j + 0.5 + jitter * (rng() - 0.5)) / ny,
      mn.z + d.z * (k + 0.5 + jitter * (rng() - 0.5)) / nz));
  return s;
}
export function randomRot(rng) {  // uniform random rotation (Shoemake)
  const u1 = rng(), u2 = rng() * 2 * Math.PI, u3 = rng() * 2 * Math.PI;
  const a = Math.sqrt(1 - u1), b = Math.sqrt(u1);
  return new THREE.Quaternion(a * Math.sin(u2), a * Math.cos(u2), b * Math.sin(u3), b * Math.cos(u3));
}
export function voronoiCells(seeds, mn, mx) {
  return seeds.map((si, i) => {
    let faces = boxFaces(mn, mx);
    for (let j = 0; j < seeds.length; j++) {
      if (j === i) continue; const sj = seeds[j];
      const n = new THREE.Vector3().subVectors(sj, si); const L = n.length(); n.multiplyScalar(1 / L);
      const d = n.dot(new THREE.Vector3().addVectors(si, sj).multiplyScalar(0.5));
      faces = clipPoly(faces, n, d, j);
    }
    const nbs = [...new Set(faces.filter((f) => f.nb >= 0).map((f) => f.nb))];
    const pos = [], nrm = [], int = []; const cen = new THREE.Vector3(); let area = 0;
    for (const f of faces) {
      const v = f.verts; const fn = new THREE.Vector3();
      for (let k = 1; k < v.length - 1; k++) {
        const e1 = v[k].clone().sub(v[0]), e2 = v[k + 1].clone().sub(v[0]); const cr = e1.clone().cross(e2); fn.add(cr);
        const a = cr.length() / 2; area += a; cen.addScaledVector(v[0].clone().add(v[k]).add(v[k + 1]), a / 3);
        pos.push(v[0].x, v[0].y, v[0].z, v[k].x, v[k].y, v[k].z, v[k + 1].x, v[k + 1].y, v[k + 1].z);
      }
      fn.normalize();
      for (let k = 1; k < v.length - 1; k++) for (let q = 0; q < 3; q++) { nrm.push(fn.x, fn.y, fn.z); int.push(f.nb >= 0 ? 1 : 0); }
    }
    cen.multiplyScalar(1 / (area || 1));
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute("normal", new THREE.Float32BufferAttribute(nrm, 3));
    g.setAttribute("aInt", new THREE.Float32BufferAttribute(int, 1));
    g.setAttribute("aSurf", new THREE.Float32BufferAttribute(new Float32Array(pos.length).fill(99), 3));
    return { i, seed: si, geo: g, nbs, centroid: cen };
  });
}

// Build grain meshes with per-grain metallic tint and lattice orientation.
export function grainMeshes(seeds, mn, mx, o = {}) {
  const rng = mulberry32(o.seed ?? 5);
  const cells = voronoiCells(seeds, mn, mx);
  const base = new THREE.Color(o.color ?? PAL.metal);
  const group = new THREE.Group();
  const grains = cells.map((c) => {
    const tintK = 0.32 + 0.85 * rng(), warm = rng();
    const color = base.clone().multiplyScalar(tintK).lerp(new THREE.Color(warm > 0.5 ? 0xb9a184 : 0x9aa0a6), 0.4 * Math.abs(warm - 0.5) * 2);
    const { mat, u } = metalMaterial(o.features ?? ["BLOCK", "LATTICE"], { color, roughness: 0.22 + 0.33 * rng(), anisotropy: 0, env: o.env ?? 1.0, uniforms: o.shared });
    u.uSelf.value.copy(c.seed); u.uNbN.value = Math.min(20, c.nbs.length);
    c.nbs.slice(0, 20).forEach((j, k) => u.uNb.value[k].copy(seeds[j]));
    const q = randomRot(rng);
    u.uRot.value.setFromMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(q));
    u.uLatFreq.value = o.latFreq ?? 25;
    const mesh = new THREE.Mesh(c.geo, mat);
    group.add(mesh);
    return { ...c, mesh, mat, u, q, color };
  });
  return { group, grains };
}

// ---------------------------------------------------------------- periodic-table style element tile (canvas text, lit)
export function elementTile(sym, name, o = {}) {
  const cw = 512, ch = 600, cv = document.createElement("canvas"); cv.width = cw; cv.height = ch;
  const x = cv.getContext("2d");
  const g = x.createLinearGradient(0, 0, 0, ch); g.addColorStop(0, "#1b2230"); g.addColorStop(1, "#0d1119");
  x.fillStyle = g; x.fillRect(0, 0, cw, ch);
  x.strokeStyle = o.hot ? "rgba(249,115,22,0.95)" : "rgba(248,250,252,0.42)"; x.lineWidth = 8; x.strokeRect(10, 10, cw - 20, ch - 20);
  x.fillStyle = o.hot ? "#F97316" : "#F8FAFC"; x.textAlign = "center"; x.textBaseline = "alphabetic";
  x.font = "800 270px Inter, Arial, sans-serif"; x.fillText(sym, cw / 2, 370);
  x.fillStyle = o.hot ? "#FDBA74" : "#B6C2D2"; x.font = "600 58px Inter, Arial, sans-serif";
  x.fillText(name.toUpperCase(), cw / 2, 520);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const face = new THREE.MeshStandardMaterial({ map: tex, emissiveMap: tex, emissive: 0xffffff, emissiveIntensity: 0.55,
    roughness: 0.35, metalness: 0.2, transparent: true });
  const frameM = new THREE.MeshStandardMaterial({ color: 0x8d8780, metalness: 1, roughness: 0.32, emissive: o.hot ? PAL.amber : 0xffffff,
    emissiveIntensity: 0, transparent: true });
  const w = 0.36, h = 0.42;
  const group = new THREE.Group();
  const frame = new THREE.Mesh(new RoundedBoxGeometry(w + 0.03, h + 0.03, 0.04, 2, 0.012), frameM);
  const plane = new THREE.Mesh(new THREE.PlaneGeometry(w, h), face); plane.position.z = 0.0215;
  group.add(frame, plane);
  return { group, setGlow(k, alpha = 1) {
    face.emissiveIntensity = 0.55 + 1.6 * k; frameM.emissiveIntensity = (o.hot ? 3.0 : 0.6) * k;
    face.opacity = alpha; frameM.opacity = alpha; group.visible = alpha > 0.003; } };
}

// ---------------------------------------------------------------- x-ray ghost of the blade (fresnel shell, clipped by a scan height)
export function ghostMaterial(o = {}) {
  const u = { uScanY: { value: 99 }, uAlpha: { value: 1 }, uTint: { value: col(o.tint ?? 0xc9c6c0, 1.0) }, uEdge: { value: col(PAL.amberHot, 1.0) } };
  const mat = new THREE.ShaderMaterial({
    uniforms: u, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
    vertexShader: `attribute vec3 aSurf; varying vec3 vN; varying vec3 vV; varying vec3 vRest; varying vec3 vSurf;
      void main(){ vRest = position; vSurf = aSurf; vec4 mv = modelViewMatrix * vec4(position, 1.); vV = -mv.xyz; vN = normalMatrix * normal; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform float uScanY, uAlpha; uniform vec3 uTint, uEdge; varying vec3 vN; varying vec3 vV; varying vec3 vRest; varying vec3 vSurf;
      void main(){ if (vRest.y > uScanY) discard;
        float f = 1. - abs(dot(normalize(vN), normalize(vV))); f = pow(f, 2.2);
        float edge = exp((vRest.y - uScanY) / .03) * step(uScanY, 50.);
        vec3 c = uTint * (.015 + .42 * f) + uEdge * edge * .8;
        gl_FragColor = vec4(c * uAlpha, 1.); }`,
  });
  return { mat, u };
}

// ---------------------------------------------------------------- internal cooling passages (param space s = camber fraction, y = height)
// Returns tube meshes (elliptical section filling the blade thickness) and particle paths that run on out through the exits.
export function buildChannels(BP, o = {}) {
  const vOf = (y) => clamp((y + 0.03) / (SPAN + 0.03));
  const pt3 = (s, y) => {           // camber point; below the platform the passage runs straight down the root (z -> 0)
    const m = BP.map(s, vOf(Math.max(y, 0)), 0); const k = sm(seg(y, -0.25, 0.0));
    return new THREE.Vector3(m[0], y, m[1] * k);
  };
  const dense = (ctrl, n) => new THREE.SplineCurve(ctrl.map(([s, y]) => new THREE.Vector2(s, y))).getSpacedPoints(n);
  function tube(ctrl, n = 160, seg = 14, wid = 0.045) {
    const P2 = dense(ctrl, n), P3 = P2.map((p) => pt3(p.x, p.y));
    const pos = [], aP = [], idx = []; let L = 0; const cum = [0];
    for (let i = 1; i < P3.length; i++) { L += P3[i].distanceTo(P3[i - 1]); cum.push(L); }
    for (let i = 0; i < P3.length; i++) {
      const p = P3[i], T = P3[Math.min(i + 1, P3.length - 1)].clone().sub(P3[Math.max(i - 1, 0)]).normalize();
      const s = P2[i].x, y = P2[i].y, v = vOf(Math.max(y, 0));
      const td = y >= 0 ? BP.thickDir(s, v) : [0, 1];
      const D = new THREE.Vector3(td[0], 0, td[1]); D.addScaledVector(T, -D.dot(T)).normalize();
      const Bv = new THREE.Vector3().crossVectors(T, D);
      const a = (y >= 0 ? 0.62 * BP.halfThick(s, v) : 0.07), b = wid;
      for (let j = 0; j <= seg; j++) { const th = (j / seg) * Math.PI * 2;
        const q = p.clone().addScaledVector(D, a * Math.cos(th)).addScaledVector(Bv, b * Math.sin(th)); pos.push(q.x, q.y, q.z); aP.push(cum[i] / L); }
    }
    for (let i = 0; i < P3.length - 1; i++) for (let j = 0; j < seg; j++) { const a = i * (seg + 1) + j, b = a + seg + 1; idx.push(a, b, a + 1, a + 1, b, b + 1); }
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("aPath", new THREE.Float32BufferAttribute(aP, 1));
    g.setIndex(idx); g.computeVertexNormals();
    return { geo: g, pts: P3, len: L };
  }
  const LE = [[0.13, -0.76], [0.13, -0.5], [0.115, -0.05], [0.1, 0.45], [0.09, 0.95], [0.09, 1.36]];
  const SERP = [[0.42, -0.76], [0.41, -0.45], [0.37, 0.0], [0.36, 0.6], [0.36, 1.22], [0.4, 1.35], [0.47, 1.36], [0.53, 1.24], [0.53, 0.65],
    [0.53, 0.14], [0.57, 0.05], [0.65, 0.06], [0.7, 0.16], [0.7, 0.7], [0.71, 1.3]];
  const tubes = [tube(LE, 120), tube(SERP, 300)];
  const exitsTE = [0.25, 0.48, 0.71, 0.94, 1.17].map((h) => tube([[0.7, h], [0.8, h - 0.005], [0.9, h - 0.01], [0.985, h - 0.015]], 24, 10, 0.022));
  // particle paths: through the passages, then out of a hole row (LE showerhead / TE slots) into the gas stream
  const paths = [];
  const sub = (ctrl, y1) => { const out = []; for (const c of ctrl) { if (c[1] >= y1) break; out.push(c); } out.push([ctrl[ctrl.length - 1][0], y1]); return out; };
  for (const h of [0.2, 0.42, 0.64, 0.86, 1.08, 1.3]) {
    const c = sub(LE, h); const inner = dense(c, 120).map((p) => pt3(p.x, p.y));
    const m0 = BP.map(0.0, vOf(h), 0), mN = BP.map(0.0, vOf(h), -0.02);
    const out = new THREE.Vector3(m0[0], h, m0[1]); const nrm = new THREE.Vector3(m0[0] - mN[0], 0, m0[1] - mN[1]).normalize();
    inner.push(out.clone(), out.clone().addScaledVector(nrm, 0.12).add(new THREE.Vector3(0, 0.02, 0)), out.clone().addScaledVector(nrm, 0.22).add(new THREE.Vector3(0.1, 0.05, 0)));
    inner.unshift(pt3(0.13, -1.25)); paths.push({ path: new Path(inner), kind: "le" });
  }
  for (const h of [0.25, 0.48, 0.71, 0.94, 1.17]) {
    const k = SERP.findIndex((c) => c[0] >= 0.69 && c[1] >= 0.15);
    const c = [...SERP.slice(0, k + 1).filter((c, i) => i < k || c[1] < h), [0.7, h], [0.8, h - 0.005], [0.9, h - 0.01], [0.985, h - 0.015]];
    const pts = dense(c, 260).map((p) => pt3(p.x, p.y));
    const te = pts[pts.length - 1], dirTE = te.clone().sub(pts[pts.length - 6]).setY(0).normalize();
    pts.push(te.clone().addScaledVector(dirTE, 0.15), te.clone().addScaledVector(dirTE, 0.32).add(new THREE.Vector3(0, 0.02, 0)));
    pts.unshift(pt3(0.42, -1.25)); paths.push({ path: new Path(pts), kind: "te" });
  }
  return { tubes, exitsTE, paths };
}

export function channelMaterial() {
  const u = { uScanY: { value: 99 }, uFront: { value: -1 }, uWall: { value: col(0xd9d2c8, 0.5) }, uAir: { value: col(PAL.cyan, 0.9) }, uT: { value: 0 }, uAmt: { value: 1 } };
  const mat = new THREE.ShaderMaterial({
    uniforms: u, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
    vertexShader: `attribute float aPath; varying float vP; varying vec3 vN; varying vec3 vV; varying float vY;
      void main(){ vP = aPath; vY = position.y; vec4 mv = modelViewMatrix * vec4(position, 1.); vV = -mv.xyz; vN = normalMatrix * normal; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform float uScanY, uFront, uT, uAmt; uniform vec3 uWall, uAir; varying float vP; varying vec3 vN; varying vec3 vV; varying float vY;
      void main(){ if (vY > uScanY) discard;
        float f = pow(1. - abs(dot(normalize(vN), normalize(vV))), 1.8);
        float fill = 1. - smoothstep(uFront - .04, uFront + .02, vP);
        float flow = .6 + .4 * sin(vP * 60. - uT * 9.);
        vec3 c = uWall * (.05 + .6 * f) * (1. - .6 * fill) + uAir * fill * (.3 + .8 * f) * flow;
        gl_FragColor = vec4(c * uAmt, 1.); }`,
  });
  return { mat, u };
}
