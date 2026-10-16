// kav3d.js: the 3D railway world shared by the Kavach A scenes (A1–A9). Every model is drawn from the reference photos
// in projects/kavach-railway-reality/design-reference.md: broad-gauge track (1,676 mm) on grey PSC sleepers 600 mm apart,
// rusty rails with a bright running top, grey ballast; a WAP-style electric loco in cream with an orange-red band
// (Co-Co bogies, two pantographs, black Kavach dome antennas on the roof); red-and-grey LHB coaches; an Indian 4-aspect
// colour-light signal (hooded lamps Y-G-Y-R, white post with ladder, number plate); OHE masts and wires; grey Kavach
// cabinets with the red INDIAN RAILWAY PROPERTY plate; the grey RFID tag clamped to the centre of a sleeper; a lattice
// radio tower. Units are metres; rail top is y = 0; track runs along z and trains run toward -z.
// Everything is a pure function of time t: seeded RNG, no clocks, no state carried between frames.
import * as THREE from "three";
import { HDRLoader } from "three/addons/loaders/HDRLoader.js";
import { mergeGeometries, mergeVertices } from "three/addons/utils/BufferGeometryUtils.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer, RenderPass, EffectPass, BloomEffect, ToneMappingEffect, ToneMappingMode, VignetteEffect, VignetteTechnique, Effect, FXAAEffect, BlendFunction } from "postprocessing";

export { THREE };
window.THREE = window.THREE || THREE;   // HyperFrames' Three adapter waits on window.THREE.DefaultLoadingManager

// ------------------------------------------------------------------------------------------------ math (all pure)
export const mulberry32 = (s) => () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const ease = {
  inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  inOut2: (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  out: (t) => 1 - Math.pow(1 - t, 3), in: (t) => t * t * t, lin: (t) => t,
};
export const seg = (t, a, b, fn = ease.inOut) => fn(clamp((t - a) / (b - a)));
export const wob = (t, s = 0) => 0.5 * Math.sin(t * 0.73 + s * 1.7) + 0.3 * Math.sin(t * 1.31 + s * 4.1) + 0.2 * Math.sin(t * 2.17 + s * 2.3);
/** keyed camera: keys [[t, [px,py,pz], [lx,ly,lz]], ...] → smooth (Catmull-Rom) position and target at time t */
export function camPath(keys) {
  const P = new THREE.CatmullRomCurve3(keys.map((k) => new THREE.Vector3(...k[1])), false, "centripetal");
  const L = new THREE.CatmullRomCurve3(keys.map((k) => new THREE.Vector3(...k[2])), false, "centripetal");
  const n = keys.length - 1;
  return (t) => { let u = 1; for (let i = 0; i < n; i++) if (t <= keys[i + 1][0]) { u = (i + ease.inOut2(clamp((t - keys[i][0]) / (keys[i + 1][0] - keys[i][0])))) / n; break; }
    if (t <= keys[0][0]) u = 0; return { p: P.getPoint(u), l: L.getPoint(u) }; };
}
export function aim(camera, p, l, roll = 0) { camera.position.copy(p); camera.up.set(Math.sin(roll), Math.cos(roll), 0); camera.lookAt(l); }

// ------------------------------------------------------------------------------------------------ canvas textures
function canvasTex(w, h, draw, { repeat = [1, 1], srgb = true, aniso = 8 } = {}) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); t.anisotropy = aniso; return t;
}
const grey = (v, a = 1, tint = [0, 0, 0]) => `rgba(${clamp(v + tint[0], 0, 255) | 0},${clamp(v + tint[1], 0, 255) | 0},${clamp(v + tint[2], 0, 255) | 0},${a})`;
function stones(g, w, h, seed, n, base, spread, rmin, rmax) {
  const r = mulberry32(seed);
  for (let i = 0; i < n; i++) {
    const x = r() * w, y = r() * h, rad = rmin + r() * (rmax - rmin), v = base + (r() - 0.5) * spread, k = 5 + ((r() * 4) | 0), rot = r() * 6.3;
    const tint = [(r() - 0.5) * 18, (r() - 0.5) * 10, (r() - 0.5) * 14];
    for (const [dx, dy] of [[0, 0], [w, 0], [-w, 0], [0, h], [0, -h]]) {
      g.beginPath();
      for (let j = 0; j < k; j++) { const a = rot + (j / k) * 6.283, rr = rad * (0.7 + 0.3 * r()); g.lineTo(x + dx + Math.cos(a) * rr, y + dy + Math.sin(a) * rr * 0.85); }
      g.closePath(); g.fillStyle = grey(v * 0.55, 0.9); g.save(); g.translate(1.5, 2); g.fill(); g.restore();
      g.fillStyle = grey(v, 1, tint); g.fill();
      g.fillStyle = grey(v + 28, 0.35); g.beginPath(); g.ellipse(x + dx - rad * 0.2, y + dy - rad * 0.25, rad * 0.45, rad * 0.3, rot, 0, 6.283); g.fill();
    }
  }
}
export const TEX = {};
function makeTextures() {
  TEX.ballast = canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = "#4b4844"; g.fillRect(0, 0, w, h); stones(g, w, h, 11, 5200, 128, 70, 7, 17); }, { repeat: [1, 1] });
  TEX.concrete = canvasTex(512, 128, (g, w, h) => { g.fillStyle = "#a8a6a0"; g.fillRect(0, 0, w, h); const r = mulberry32(5);
    for (let i = 0; i < 4000; i++) { g.fillStyle = grey(150 + (r() - 0.5) * 70, 0.35); g.fillRect(r() * w, r() * h, 1 + r() * 2, 1 + r() * 2); }
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(255,255,255,0.08)"); gr.addColorStop(1, "rgba(40,30,20,0.25)"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 30; i++) { g.fillStyle = "rgba(90,60,40,0.10)"; g.beginPath(); g.ellipse(r() * w, r() * h, 6 + r() * 20, 3 + r() * 8, 0, 0, 6.3); g.fill(); } });
  TEX.ground = canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = "#5d5040"; g.fillRect(0, 0, w, h); const r = mulberry32(21);
    for (let i = 0; i < 260; i++) { const c = r() < 0.55 ? [78, 86, 48] : [104, 88, 66]; g.fillStyle = `rgba(${c[0]},${c[1]},${c[2]},${0.25 + r() * 0.35})`;
      g.beginPath(); g.ellipse(r() * w, r() * h, 20 + r() * 90, 12 + r() * 50, r() * 3, 0, 6.3); g.fill(); }
    for (let i = 0; i < 9000; i++) { g.fillStyle = r() < 0.5 ? "rgba(120,130,70,0.35)" : "rgba(60,50,38,0.4)"; g.fillRect(r() * w, r() * h, 1, 2 + r() * 4); } }, { repeat: [60, 60] });
  TEX.louvre = canvasTex(256, 256, (g, w, h) => { g.fillStyle = "#b9b4a2"; g.fillRect(0, 0, w, h); g.fillStyle = "#8e8a7c"; g.fillRect(4, 4, w - 8, h - 8);
    for (let y = 10; y < h - 8; y += 12) { g.fillStyle = "#5d5a52"; g.fillRect(10, y, w - 20, 5); g.fillStyle = "#cfcab8"; g.fillRect(10, y + 5, w - 20, 2); } }, { repeat: [1, 1] });
  TEX.coachSide = canvasTex(2048, 256, (g, w, h) => {
    // LHB coach side: red upper body, grey lower body, dark tinted windows, doors at both ends (reference LHB_coaches_3.jpg)
    g.fillStyle = "#a3262c"; g.fillRect(0, 0, w, h); g.fillStyle = "#8f9398"; g.fillRect(0, h * 0.70, w, h * 0.30);
    g.fillStyle = "#e8e2d8"; g.fillRect(0, h * 0.68, w, h * 0.022);
    const door = (x) => { g.fillStyle = "#8d1f24"; g.fillRect(x, h * 0.08, 74, h * 0.86); g.fillStyle = "#15191d"; g.fillRect(x + 18, h * 0.16, 38, h * 0.22);
      g.strokeStyle = "#5c1418"; g.lineWidth = 3; g.strokeRect(x, h * 0.08, 74, h * 0.86); g.fillStyle = "#c9c9c9"; g.fillRect(x + 60, h * 0.5, 5, 26); };
    door(36); door(w - 110);
    for (let i = 0; i < 12; i++) { const x = 190 + i * 140; g.fillStyle = "#11161b"; g.beginPath(); g.roundRect(x, h * 0.26, 104, h * 0.30, 10); g.fill();
      g.fillStyle = "rgba(160,190,210,0.18)"; g.fillRect(x + 6, h * 0.28, 40, h * 0.08); g.strokeStyle = "#cfd3d6"; g.lineWidth = 3; g.beginPath(); g.roundRect(x, h * 0.26, 104, h * 0.30, 10); g.stroke(); }
    g.fillStyle = "rgba(0,0,0,0.25)"; g.fillRect(0, 0, w, 6); }, { repeat: [1, 1] });
  TEX.plate = canvasTex(512, 128, (g, w, h) => { g.fillStyle = "#c81e1e"; g.fillRect(0, 0, w, h); g.strokeStyle = "#f3f3f3"; g.lineWidth = 6; g.strokeRect(6, 6, w - 12, h - 12);
    g.fillStyle = "#ffffff"; g.font = "800 46px Inter, Arial"; g.textAlign = "center"; g.fillText("INDIAN RAILWAY PROPERTY", w / 2, 62);
    g.font = "600 24px Inter, Arial"; g.fillText("TRAIN COLLISION AVOIDANCE SYSTEM", w / 2, 102); }, { repeat: [1, 1] });
  TEX.cards = canvasTex(512, 256, (g, w, h) => { g.fillStyle = "#24272b"; g.fillRect(0, 0, w, h); const r = mulberry32(9);
    for (let i = 0; i < 22; i++) { const x = 10 + i * 22.6; g.fillStyle = "#d9dcdf"; g.fillRect(x, 14, 18, h - 28); g.fillStyle = "#9ea3a8"; g.fillRect(x + 3, 30, 12, 6); g.fillRect(x + 3, h - 50, 12, 6);
      for (let k = 0; k < 4; k++) { g.fillStyle = r() < 0.6 ? "#22c55e" : r() < 0.5 ? "#f59e0b" : "#ef4444"; g.fillRect(x + 6, 60 + k * 14, 5, 5); } } }, { repeat: [1, 1] });
  TEX.tagTop = canvasTex(512, 192, (g, w, h) => { g.fillStyle = "#b7bcc1"; g.fillRect(0, 0, w, h); const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "rgba(255,255,255,0.25)"); gr.addColorStop(1, "rgba(0,0,0,0.15)"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "#f2c200"; g.beginPath(); g.moveTo(w / 2 - 26, 70); g.lineTo(w / 2 + 26, 70); g.lineTo(w / 2, 26); g.closePath(); g.fill();
    g.fillStyle = "#2a2d31"; g.font = "600 22px Inter, Arial"; g.textAlign = "center"; g.fillText("RFID ID-4C1A   TYPE-N   ABS   LOCATION-112.400 KM", w / 2, 128); }, { repeat: [1, 1] });
}

// ------------------------------------------------------------------------------------------------ post effects
class GrainEffect extends Effect {
  constructor() {
    super("GrainEffect", `uniform float uT, uGrain, uVig;
      float h2(vec2 p){ vec3 p3 = fract(vec3(p.xyx) * 0.1031); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.x + p3.y) * p3.z); }
      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor){
        vec2 px = uv * resolution; float fr = floor(uT * 30.0 + 0.5);
        float n = h2(px + fr * vec2(37.0, 17.0)) + h2(px * 1.7 + fr * vec2(11.0, 53.0)) - 1.0;
        vec3 c = inputColor.rgb; float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
        c += n * uGrain * (0.25 + 1.6 * l * (1.0 - l));
        vec2 q = (uv - 0.5) * vec2(1.0, 0.82); float r = length(q) * 1.55;   // smooth radial vignette (no hard ellipse edge)
        c *= 1.0 - uVig * smoothstep(0.35, 1.15, r); outputColor = vec4(max(c, 0.0), inputColor.a); }`,
      { uniforms: new Map([["uT", new THREE.Uniform(0)], ["uGrain", new THREE.Uniform(0.04)], ["uVig", new THREE.Uniform(0.5)]]) });
  }
}

// ------------------------------------------------------------------------------------------------ sky + light presets
export const SKY = {
  dusk:  { top: "#0f1d3d", hor: "#d98a52", bot: "#2a2420", sun: [-0.55, 0.10, -0.83], sunCol: "#ffae6a", sunI: 2.6, glow: 0.9, hemiS: "#6a7aa8", hemiG: "#3a2a1c", hemiI: 0.7, fog: "#7a6458", fogD: 0.0017, env: 0.35, stars: 0.0 },
  night: { top: "#02050c", hor: "#0d1a30", bot: "#05070b", sun: [0.4, 0.5, -0.7], sunCol: "#9db8ff", sunI: 0.55, glow: 0.05, hemiS: "#2a3a60", hemiG: "#0a0a10", hemiI: 0.35, fog: "#0b1424", fogD: 0.006, env: 0.12, stars: 1.0 },
  dawn:  { top: "#29406e", hor: "#f0b48c", bot: "#33302c", sun: [0.6, 0.12, -0.78], sunCol: "#ffd2a0", sunI: 2.4, glow: 0.8, hemiS: "#8aa0c8", hemiG: "#40342a", hemiI: 0.8, fog: "#a3928a", fogD: 0.0036, env: 0.45, stars: 0.0 },
  void:  { top: "#04060c", hor: "#0b1322", bot: "#020306", sun: [0.4, 0.8, 0.45], sunCol: "#dfe8ff", sunI: 1.4, glow: 0.0, hemiS: "#3a4c70", hemiG: "#05070a", hemiI: 0.5, fog: "#070b14", fogD: 0.010, env: 0.5, stars: 0.0 },
};
function skyDome(p) {
  const mat = new THREE.ShaderMaterial({
    uniforms: { uTop: { value: new THREE.Color(p.top) }, uHor: { value: new THREE.Color(p.hor) }, uBot: { value: new THREE.Color(p.bot) },
      uSun: { value: new THREE.Vector3(...p.sun).normalize() }, uSunCol: { value: new THREE.Color(p.sunCol) }, uGlow: { value: p.glow }, uStars: { value: p.stars }, uDim: { value: 1 } },
    vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); vec4 p = projectionMatrix * modelViewMatrix * vec4(position, 1.0); gl_Position = p.xyww; }`,
    fragmentShader: `uniform vec3 uTop, uHor, uBot, uSun, uSunCol; uniform float uGlow, uStars, uDim; varying vec3 vD;
      float h(vec3 p){ return fract(sin(dot(p, vec3(12.9898, 78.233, 37.719))) * 43758.5453); }
      void main(){ vec3 d = normalize(vD); float y = d.y;
        vec3 c = y > 0.0 ? mix(uHor, uTop, pow(clamp(y * 1.6, 0.0, 1.0), 0.55)) : mix(uHor, uBot, clamp(-y * 6.0, 0.0, 1.0));
        float s = max(dot(d, uSun), 0.0); c += uSunCol * uGlow * (0.35 * pow(s, 6.0) + 1.2 * pow(s, 90.0) + 4.0 * pow(s, 2200.0));
        vec3 q = floor(d * 420.0); float st = step(0.9975, h(q)) * smoothstep(0.05, 0.4, y) * uStars; c += vec3(0.8, 0.85, 1.0) * st * (0.4 + 0.6 * h(q + 1.0));
        gl_FragColor = vec4(c * uDim, 1.0); }`,
    side: THREE.BackSide, depthWrite: false, depthTest: false, fog: false,
  });
  const m = new THREE.Mesh(new THREE.SphereGeometry(1500, 48, 24), mat); m.frustumCulled = false; m.renderOrder = -10; return m;
}

/**
 * Stage: renderer, scene, camera, sky, sun with soft shadows, HDRI reflections and the post stack (bloom, vignette,
 * ACES, FXAA, grain). run(build, update) waits for the HDRI and fonts, calls build() once, then update(t, ctx) per frame.
 */
export function createStage({ fov = 35, near = 0.05, far = 2000, sky = "dusk", exposure = 1.0, shadows = true, shadowSize = 2048,
  bloom = { intensity: 0.9, threshold: 0.9, smoothing: 0.25, radius: 0.75 }, vignette = 0.5, grain = 0.04 } = {}) {
  const mgr = THREE.DefaultLoadingManager; mgr.itemStart("kav3d-build");
  const root = document.getElementById("root");
  const W = +root.dataset.width, H = +root.dataset.height, DUR = +root.dataset.duration;
  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("gl"), antialias: false, stencil: false, depth: false,
    powerPreference: "high-performance", preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.toneMapping = THREE.NoToneMapping; renderer.toneMappingExposure = exposure;
  renderer.shadowMap.enabled = shadows; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const P = SKY[sky];
  const scene = new THREE.Scene(); scene.background = new THREE.Color(P.bot); scene.fog = new THREE.FogExp2(new THREE.Color(P.fog), P.fogD);
  const camera = new THREE.PerspectiveCamera(fov, W / H, near, far);
  const dome = skyDome(P); scene.add(dome);
  const sun = new THREE.DirectionalLight(new THREE.Color(P.sunCol), P.sunI);
  sun.position.set(...P.sun).multiplyScalar(-1).normalize();  // placeholder; follow() aims it
  sun.castShadow = shadows; sun.shadow.mapSize.set(shadowSize, shadowSize); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03;
  Object.assign(sun.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30, near: 1, far: 260 }); scene.add(sun, sun.target);
  const hemi = new THREE.HemisphereLight(new THREE.Color(P.hemiS), new THREE.Color(P.hemiG), P.hemiI); scene.add(hemi);
  const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType });
  composer.addPass(new RenderPass(scene, camera));
  const bloomFx = new BloomEffect({ blendFunction: BlendFunction.ADD, intensity: bloom.intensity, luminanceThreshold: bloom.threshold, luminanceSmoothing: bloom.smoothing, mipmapBlur: false, kernelSize: 4 });   // the mipmap blur left dark halos on SwiftShader; Kawase does not
  const vig = new VignetteEffect({ technique: VignetteTechnique.ESKIL, darkness: vignette, offset: 0.45 }), tone = new ToneMappingEffect({ mode: ToneMappingMode.AGX });   // ACES pushed saturated cyan bloom below zero (dark halos); AgX does not
  const gr = new GrainEffect(); gr.uniforms.get("uGrain").value = grain;
  gr.uniforms.get("uVig").value = vignette;
  composer.addPass(new EffectPass(camera, bloomFx, tone, new FXAAEffect(), gr));
  composer.setSize(W, H);
  const sunDir = new THREE.Vector3(...P.sun).normalize();
  const st = { root, W, H, DUR, renderer, scene, camera, sun, hemi, dome, preset: P, fx: { bloom: bloomFx, vig, grain: gr } };
  /** keep the shadow frustum centred on the action */
  st.follow = (x, y, z, span = 30) => { sun.target.position.set(x, y, z); sun.position.set(x - sunDir.x * 120, y + Math.max(0.25, sunDir.y) * 120, z - sunDir.z * 120);
    Object.assign(sun.shadow.camera, { left: -span, right: span, top: span, bottom: -span }); sun.shadow.camera.updateProjectionMatrix(); };
  const hdr = new HDRLoader().loadAsync("vendor/library/hdri/kloofendal_48d_partly_cloudy_puresky_1k.hdr").then((tex) => {
    const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromEquirectangular(tex).texture; scene.environmentIntensity = P.env; tex.dispose(); pm.dispose(); });
  const fonts = Promise.all(["800 40px Inter", "600 24px Inter"].map((f) => document.fonts.load(f))).catch(() => {});
  st.ready = Promise.all([hdr, fonts]).then(() => makeTextures());
  st.run = (build, update) => {
    st.ready.then(() => {
      const ctx = build ? build(st) : {};
      const draw = (t) => { gr.uniforms.get("uT").value = t; update(t, ctx); composer.render(0); };
      window.addEventListener("hf-seek", (ev) => draw(ev.detail.time));
      draw(window.__hfThreeTime || 0);
      mgr.itemEnd("kav3d-build");
    });
  };
  /** world position → CSS pixels; returns {x, y, z} (z > 1 means behind the camera) */
  const v = new THREE.Vector3();
  st.project = (p) => { v.copy(p).project(camera); return { x: (v.x * 0.5 + 0.5) * W, y: (-v.y * 0.5 + 0.5) * H, z: v.z }; };
  /** place a DOM element (absolutely positioned at left/top 0) at a world point, with a pixel offset */
  st.pin = (el, p, dx = 0, dy = 0) => { if (!el) return; const s = st.project(p); el.style.transform = `translate(${(s.x + dx).toFixed(1)}px, ${(s.y + dy).toFixed(1)}px)`;
    el.style.visibility = s.z < 1 ? "visible" : "hidden"; return s; };
  return st;
}

// ------------------------------------------------------------------------------------------------ materials
export function mats() {
  return {
    concrete: new THREE.MeshStandardMaterial({ map: TEX.concrete, roughness: 0.92, metalness: 0 }),
    rail: new THREE.MeshStandardMaterial({ color: 0x5b3e2c, roughness: 0.85, metalness: 0.35 }),
    railTop: new THREE.MeshStandardMaterial({ color: 0xd6d9dc, roughness: 0.22, metalness: 1.0 }),
    clip: new THREE.MeshStandardMaterial({ color: 0x2a2624, roughness: 0.6, metalness: 0.6 }),
    ballast: new THREE.MeshStandardMaterial({ map: TEX.ballast, bumpMap: TEX.ballast, bumpScale: 2.5, roughness: 0.95, metalness: 0 }),
    ground: new THREE.MeshStandardMaterial({ map: TEX.ground, roughness: 1, metalness: 0 }),
    steel: new THREE.MeshStandardMaterial({ color: 0x8a9096, roughness: 0.5, metalness: 0.8 }),
    darkSteel: new THREE.MeshStandardMaterial({ color: 0x24272b, roughness: 0.6, metalness: 0.6 }),
    galv: new THREE.MeshStandardMaterial({ color: 0x9ea4a8, roughness: 0.45, metalness: 0.85 }),
    white: new THREE.MeshStandardMaterial({ color: 0xe9e9e4, roughness: 0.55, metalness: 0.1 }),
    black: new THREE.MeshStandardMaterial({ color: 0x0d0e10, roughness: 0.5, metalness: 0.2 }),
    cabinet: new THREE.MeshStandardMaterial({ color: 0xd7d8d2, roughness: 0.55, metalness: 0.15 }),
  };
}

// ------------------------------------------------------------------------------------------------ track
export const GAUGE = 1.676, RAIL_X = GAUGE / 2 + 0.036;   // rail centre lines (head 72 mm wide)
function railShape() {
  const s = new THREE.Shape(), p = [[-0.075, 0], [0.075, 0], [0.075, 0.012], [0.014, 0.03], [0.009, 0.115], [0.036, 0.132], [0.036, 0.172], [-0.036, 0.172], [-0.036, 0.132], [-0.009, 0.115], [-0.014, 0.03], [-0.075, 0.012]];
  s.moveTo(p[0][0], p[0][1]); p.slice(1).forEach((q) => s.lineTo(q[0], q[1])); return s;
}
/**
 * One straight broad-gauge track from z0 to z1 at x = cx: PSC sleepers every 0.6 m, two 60 kg rails with a bright
 * running top, elastic clips, and a ballast bed with sloped shoulders. Rail top is y = 0.
 */
export function buildTrack(M, { cx = 0, z0 = -400, z1 = 200, clips = true, bed = true, sleeperEvery = 0.6 } = {}) {
  const g = new THREE.Group(), L = z1 - z0, RH = 0.172, SH = 0.21, sy = -RH - 0.012 - SH / 2;   // sleeper centre
  const n = Math.floor(L / sleeperEvery);
  const sg = new RoundedBoxGeometry(2.75, SH, 0.25, 2, 0.02);
  const sl = new THREE.InstancedMesh(sg, M.concrete, n); const m4 = new THREE.Matrix4(), r = mulberry32(31);
  for (let i = 0; i < n; i++) { const z = z0 + (i + 0.5) * sleeperEvery; m4.makeRotationY((r() - 0.5) * 0.012); m4.setPosition(cx + (r() - 0.5) * 0.02, sy, z); sl.setMatrixAt(i, m4); }
  sl.castShadow = true; sl.receiveShadow = true; g.add(sl);
  const rg = new THREE.ExtrudeGeometry(railShape(), { depth: L, bevelEnabled: false }); rg.translate(0, -RH, z0);
  const topG = new THREE.PlaneGeometry(0.058, L); topG.rotateX(-Math.PI / 2); topG.translate(0, 0.0015, z0 + L / 2);
  for (const sx of [-1, 1]) { const rm = new THREE.Mesh(rg, M.rail); rm.position.x = cx + sx * RAIL_X; rm.castShadow = rm.receiveShadow = true; g.add(rm);
    const tp = new THREE.Mesh(topG, M.railTop); tp.position.x = cx + sx * RAIL_X; tp.receiveShadow = true; g.add(tp); }
  if (clips) {
    const cg = new THREE.TorusGeometry(0.04, 0.009, 5, 10, Math.PI * 1.3); cg.rotateY(Math.PI / 2);
    const cm = new THREE.InstancedMesh(cg, M.clip, n * 4); let k = 0;
    for (let i = 0; i < n; i++) { const z = z0 + (i + 0.5) * sleeperEvery;
      for (const sx of [-1, 1]) for (const side of [-1, 1]) { m4.makeRotationZ(side > 0 ? 0.3 : Math.PI - 0.3); m4.setPosition(cx + sx * RAIL_X + side * 0.085, -RH + 0.02, z); cm.setMatrixAt(k++, m4); } }
    cm.castShadow = true; g.add(cm);
  }
  if (bed) {
    // ballast cross-section: top 4.0 m wide just under the sleeper top, shoulders down to the formation
    const s = new THREE.Shape(); const top = -RH - 0.012 - 0.06, base = -0.75;
    s.moveTo(-2.0, top); s.lineTo(2.0, top); s.lineTo(2.35, top - 0.05); s.lineTo(3.6, base); s.lineTo(-3.6, base); s.lineTo(-2.35, top - 0.05); s.closePath();
    const bg = new THREE.ExtrudeGeometry(s, { depth: L, bevelEnabled: false }); bg.translate(cx, 0, z0);
    // world-space UVs: x across, z along, 1 texture tile per 1.4 m
    const pos = bg.attributes.position, uv = bg.attributes.uv; for (let i = 0; i < pos.count; i++) uv.setXY(i, (pos.getX(i) + pos.getY(i) * 0.6) / 1.4, pos.getZ(i) / 1.4);
    const bm = new THREE.Mesh(bg, M.ballast); bm.receiveShadow = true; g.add(bm);
  }
  g.userData = { sleeperY: sy, sleeperTop: sy + SH / 2 };
  return g;
}
/** loose ballast stones for close-ups (instanced), inside [z0, z1] around track centre cx */
export function buildStones(M, { cx = 0, z0 = -10, z1 = 10, n = 2500, seed = 3 } = {}) {
  const geo = new THREE.DodecahedronGeometry(0.03, 0); const mat = new THREE.MeshStandardMaterial({ color: 0x8b8781, roughness: 0.95 });
  const im = new THREE.InstancedMesh(geo, mat, n), r = mulberry32(seed), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), s = new THREE.Vector3(), p = new THREE.Vector3(), c = new THREE.Color();
  for (let i = 0; i < n; i++) { const x = (r() - 0.5) * 3.8, z = z0 + r() * (z1 - z0); const inS = Math.abs(((z % 0.6) + 0.6) % 0.6 - 0.3) > 0.17 && Math.abs(x) < 1.4;
    p.set(cx + x, -0.172 - 0.012 - 0.07 + (inS ? -0.04 : 0) + r() * 0.04, z); e.set(r() * 6, r() * 6, r() * 6); q.setFromEuler(e); const k = 0.6 + r() * 0.9; s.set(k, k * (0.6 + r() * 0.4), k);
    m4.compose(p, q, s); im.setMatrixAt(i, m4); const v = 0.42 + r() * 0.35; c.setRGB(v, v * 0.97, v * 0.93); im.setColorAt(i, c); }
  im.castShadow = true; im.receiveShadow = true; return im;
}
export function buildGround(M, { y = -0.75, size = 3000 } = {}) {
  const g = new THREE.Mesh(new THREE.PlaneGeometry(size, size), M.ground); g.rotation.x = -Math.PI / 2; g.position.y = y; g.receiveShadow = true; return g;
}
/** distant tree line and nearer bushes (seeded instanced blobs), kept clear of the corridor |x| < clear */
export function buildTrees({ n = 520, clear = 16, z0 = -900, z1 = 400, seed = 77, far = 260 } = {}) {
  const g = new THREE.Group(), r = mulberry32(seed);
  let crown = mergeVertices(new THREE.IcosahedronGeometry(1, 3).deleteAttribute("normal").deleteAttribute("uv")), trunk = new THREE.CylinderGeometry(0.12, 0.18, 1, 5);
  { const pa = crown.attributes.position, rr = mulberry32(5); const v = new THREE.Vector3(); for (let i = 0; i < pa.count; i++) { v.fromBufferAttribute(pa, i); const k = 1 + 0.18 * Math.sin(v.x * 5.1 + v.y * 3.3) * Math.cos(v.z * 4.7 - v.y * 2.1) + 0.08 * Math.sin(v.x * 11 + v.z * 9); pa.setXYZ(i, v.x * k, v.y * k * 0.85, v.z * k); } crown.computeVertexNormals(); }
  const cm = new THREE.MeshStandardMaterial({ color: 0x4a5a30, roughness: 1 }), tm = new THREE.MeshStandardMaterial({ color: 0x3a2e22, roughness: 1 });
  const C = new THREE.InstancedMesh(crown, cm, n * 2), T = new THREE.InstancedMesh(trunk, tm, n), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), s = new THREE.Vector3(), p = new THREE.Vector3(), c = new THREE.Color();
  for (let i = 0; i < n; i++) {
    const side = r() < 0.5 ? -1 : 1, x = side * (clear + Math.pow(r(), 1.6) * far), z = z0 + r() * (z1 - z0), h = 4 + r() * 7, w = 2 + r() * 3.5;
    p.set(x, -0.75 + h * 0.5, z); s.set(1, h, 1); m4.compose(p, q.identity(), s); T.setMatrixAt(i, m4);
    for (let k = 0; k < 2; k++) { e.set(r(), r() * 6, r()); q.setFromEuler(e); p.set(x + (r() - 0.5) * w * 0.6, -0.75 + h + (k ? w * 0.4 : 0), z + (r() - 0.5) * w * 0.6); s.set(w * (k ? 0.75 : 1), w * 0.8 * (k ? 0.75 : 1), w * (k ? 0.75 : 1));
      m4.compose(p, q, s); C.setMatrixAt(i * 2 + k, m4); const v = 0.75 + r() * 0.5; c.setRGB(v * (0.9 + r() * 0.2), v, v * 0.85); C.setColorAt(i * 2 + k, c); }
  }
  C.castShadow = true; g.add(C, T); return g;
}

// ------------------------------------------------------------------------------------------------ OHE
/** overhead line: masts every `span` m at x = mx (cantilever toward the track at cx), contact wire 5.5 m, messenger 6.9 m */
export function buildOHE(M, { cx = 0, mx = 3.3, z0 = -400, z1 = 200, span = 60, phase = 0 } = {}) {
  const g = new THREE.Group(), parts = [], dir = Math.sign(cx - mx);
  for (let z = z0 + phase; z <= z1; z += span) {
    const mast = new THREE.BoxGeometry(0.22, 9.6, 0.3); mast.translate(mx, -0.75 + 4.8, z); parts.push(mast);
    const flange = new THREE.BoxGeometry(0.34, 9.6, 0.04); flange.translate(mx, -0.75 + 4.8, z - 0.15); parts.push(flange);
    const f2 = flange.clone(); f2.translate(0, 0, 0.3); parts.push(f2);
    const armL = Math.abs(cx - mx) + 0.5;
    const arm = new THREE.CylinderGeometry(0.035, 0.035, armL, 6); arm.rotateZ(Math.PI / 2); arm.translate((mx + cx) / 2 + dir * 0.25, 5.75, z); parts.push(arm);
    const stay = new THREE.CylinderGeometry(0.03, 0.03, armL * 1.04, 6); stay.rotateZ(Math.PI / 2 - dir * 0.27); stay.translate((mx + cx) / 2 + dir * 0.2, 6.55, z); parts.push(stay);
    const ins = new THREE.CylinderGeometry(0.08, 0.08, 0.5, 8); ins.rotateZ(Math.PI / 2); ins.translate(mx + dir * 0.45, 5.75, z); parts.push(ins);
    const drop = new THREE.CylinderGeometry(0.012, 0.012, 1.4, 4); drop.translate(cx, 6.2, z); parts.push(drop);
  }
  const mm = new THREE.Mesh(mergeGeometries(parts), M.galv); mm.castShadow = true; g.add(mm);
  const L = z1 - z0, wire = new THREE.CylinderGeometry(0.008, 0.008, L, 4); wire.rotateX(Math.PI / 2);
  const wm = new THREE.MeshStandardMaterial({ color: 0x6b4a32, roughness: 0.5, metalness: 0.8 });
  const cw = new THREE.Mesh(wire, wm); cw.position.set(cx, 5.5, z0 + L / 2); g.add(cw);
  const ms = new THREE.Mesh(wire, wm); ms.position.set(cx, 6.9, z0 + L / 2); g.add(ms);
  return g;
}

// ------------------------------------------------------------------------------------------------ signal (Indian 4-aspect)
/** Indian colour-light signal at (x, 0, z) facing +z (toward an approaching train): lamps top→bottom Y, G, Y, R */
export function buildSignal(M, { x = 2.6, z = 0, plate = true, auto = false, faceZ = 1 } = {}) {
  const g = new THREE.Group(); g.position.set(x, -0.75, z); if (faceZ < 0) g.rotation.y = Math.PI;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.09, 5.6, 12), M.white); post.position.y = 2.8; post.castShadow = true; g.add(post);
  const base = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.35, 0.6), M.concrete); base.position.y = 0.17; g.add(base);
  // ladder
  const lad = []; for (const sx of [-0.18, 0.18]) { const r = new THREE.CylinderGeometry(0.015, 0.015, 4.6, 5); r.translate(sx, 2.6, -0.22); lad.push(r); }
  for (let y = 0.6; y < 4.8; y += 0.3) { const r = new THREE.CylinderGeometry(0.012, 0.012, 0.36, 4); r.rotateZ(Math.PI / 2); r.translate(0, y, -0.22); lad.push(r); }
  const ladder = new THREE.Mesh(mergeGeometries(lad), M.galv); g.add(ladder);
  // head: black backplate with four hooded lamps
  const head = new THREE.Group(); head.position.set(0, 6.25, 0.05); g.add(head);
  const bp = new THREE.Mesh(new RoundedBoxGeometry(0.62, 1.75, 0.16, 3, 0.06), M.black); bp.castShadow = true; head.add(bp);
  const lamps = [], cols = [0xffb21a, 0x1fe07a, 0xffb21a, 0xff2a1a];
  for (let i = 0; i < 4; i++) {
    const y = 0.62 - i * 0.41;
    const hood = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.26, 16, 1, true, -Math.PI / 2 - 0.9, Math.PI + 1.8), M.black); hood.rotation.x = Math.PI / 2; hood.position.set(0, y, 0.19); head.add(hood);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.14, 0.018, 6, 20), M.darkSteel); ring.position.set(0, y, 0.085); head.add(ring);
    const lm = new THREE.MeshStandardMaterial({ color: 0x0c0c0c, emissive: new THREE.Color(cols[i]), emissiveIntensity: 0, roughness: 0.2, metalness: 0.1 });
    const lens = new THREE.Mesh(new THREE.CircleGeometry(0.13, 24), lm); lens.position.set(0, y, 0.09); head.add(lens);
    const glow = new THREE.Mesh(new THREE.CircleGeometry(0.42, 24), new THREE.MeshBasicMaterial({ color: cols[i], transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
    glow.position.set(0, y, 0.12); head.add(glow);
    lamps.push({ lm, glow, col: new THREE.Color(cols[i]) });
  }
  // platform under the head, number plate (and the "A" disc of an automatic signal)
  const plat = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.05, 0.7), M.galv); plat.position.set(0, 5.25, -0.1); g.add(plat);
  if (plate) { const pl = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.24, 0.02), M.white); pl.position.set(0, 4.85, 0.1); g.add(pl);
    const num = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.14), new THREE.MeshBasicMaterial({ color: 0x111111 })); num.position.set(0, 4.85, 0.112); g.add(num); }
  if (auto) { const d = new THREE.Mesh(new THREE.CircleGeometry(0.16, 24), M.white); d.position.set(0, 4.45, 0.1); g.add(d); }
  /** aspect intensities 0..1 for [Y1, G, Y2, R] */
  g.userData.set = (a) => lamps.forEach((l, i) => { const k = a[i] || 0; l.lm.emissiveIntensity = 9 * k; l.glow.material.opacity = 0.45 * k; });
  g.userData.lampWorld = (i) => { const v = new THREE.Vector3(0, 0.62 - i * 0.41, 0.1); head.localToWorld(v); return v; };
  g.userData.set([0, 0, 0, 0]);
  return g;
}

// ------------------------------------------------------------------------------------------------ rolling stock
const WR_LOCO = 0.546, WR_COACH = 0.4575;
function wheelset(M, r, { brake = null } = {}) {
  const g = new THREE.Group();
  const axle = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, GAUGE + 0.5, 10), M.darkSteel); axle.rotation.z = Math.PI / 2; g.add(axle);
  const wg = mergeGeometries([new THREE.CylinderGeometry(r, r, 0.135, 28).rotateZ(Math.PI / 2), new THREE.CylinderGeometry(r + 0.03, r + 0.03, 0.03, 28).rotateZ(Math.PI / 2).translate(-0.08, 0, 0)]);
  const spokes = new THREE.BoxGeometry(0.02, r * 1.5, 0.12);
  for (const sx of [-1, 1]) {
    const w = new THREE.Mesh(wg, M.wheel); w.position.x = sx * RAIL_X; w.scale.x = sx; w.castShadow = true; g.add(w);
    const sp = new THREE.Mesh(spokes, M.darkSteel); sp.position.x = sx * (RAIL_X + 0.07); g.add(sp);   // a mark that shows rotation
  }
  g.position.y = r; return g;
}
/** Co-Co loco bogie (3 axles) or LHB bogie (2 axles); returns { g, wheels:[wheelsetGroups], blocks:[brake block meshes] } */
function bogie(M, { axles = 3, pitch = 1.95, r = WR_LOCO, frameY = 0.75, blockMat = null } = {}) {
  const g = new THREE.Group(), wheels = [], blocks = [];
  const span = pitch * (axles - 1);
  for (let i = 0; i < axles; i++) { const w = wheelset(M, r); w.position.z = -span / 2 + i * pitch; g.add(w); wheels.push(w);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.32, 0.09), blockMat || M.darkSteel);
      b.position.set(sx * RAIL_X, r, w.position.z + sz * (r + 0.05)); g.add(b); blocks.push(b); } }
  for (const sx of [-1, 1]) {
    const fr = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.38, span + 1.6), M.bogie); fr.position.set(sx * (RAIL_X + 0.26), frameY, 0); fr.castShadow = true; g.add(fr);
    for (let i = 0; i < axles; i++) { const z = -span / 2 + i * pitch;
      const ab = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.3, 0.34), M.bogie); ab.position.set(sx * (RAIL_X + 0.2), r, z); g.add(ab);
      const sp = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.32, 10), M.spring); sp.position.set(sx * (RAIL_X + 0.2), r + 0.3, z + (i % 2 ? 0.2 : -0.2)); g.add(sp); }
  }
  const tb = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.3, 0.5), M.bogie); tb.position.set(0, frameY, 0); g.add(tb);
  return { g, wheels, blocks };
}
/**
 * WAP-style electric loco, 20.6 m, cream with an orange-red band (reference Indian_railway_loco_pilot_signalling.JPG,
 * no livery text). Local frame: nose at z = 0, body along +z, rail top y = 0. userData: wheels, blocks, parts (Kavach
 * computer, RFID readers, wheel sensors, cab screen, brake link), xray(k), setS(s) for wheel rotation.
 */
export function buildLoco(M0) {
  const M = Object.assign({}, M0, {
    body: new THREE.MeshPhysicalMaterial({ color: 0xe6d7a6, roughness: 0.42, metalness: 0.05, clearcoat: 0.4, clearcoatRoughness: 0.35 }),
    band: new THREE.MeshPhysicalMaterial({ color: 0xd2501f, roughness: 0.42, metalness: 0.05, clearcoat: 0.4, clearcoatRoughness: 0.35 }),
    glass: new THREE.MeshPhysicalMaterial({ color: 0x0b1015, roughness: 0.08, metalness: 0.6, clearcoat: 1 }),
    bogie: new THREE.MeshStandardMaterial({ color: 0x2b2d30, roughness: 0.7, metalness: 0.4 }),
    under: new THREE.MeshStandardMaterial({ color: 0x323538, roughness: 0.75, metalness: 0.35 }),
    spring: new THREE.MeshStandardMaterial({ color: 0x6b2620, roughness: 0.6, metalness: 0.4 }),
    wheel: new THREE.MeshStandardMaterial({ color: 0x55585c, roughness: 0.45, metalness: 0.9 }),
    blockHot: new THREE.MeshStandardMaterial({ color: 0x2a2624, emissive: new THREE.Color(0xff6a1a), emissiveIntensity: 0, roughness: 0.7, metalness: 0.4 }),
    roof: new THREE.MeshStandardMaterial({ color: 0x8e9196, roughness: 0.6, metalness: 0.5 }),
    louvre: new THREE.MeshStandardMaterial({ map: TEX.louvre, roughness: 0.7, metalness: 0.4 }),
    lamp: new THREE.MeshStandardMaterial({ color: 0x222222, emissive: new THREE.Color(0xfff2d0), emissiveIntensity: 6 }),
  });
  const g = new THREE.Group(), L = 20.6, BW = 3.1;
  // body: side profile extruded across the width, with rounded edges
  const s = new THREE.Shape(); const pr = [[0.32, 1.25], [0.2, 2.15], [0.55, 3.55], [1.0, 4.08], [1.45, 4.2], [L - 1.45, 4.2], [L - 1.0, 4.08], [L - 0.55, 3.55], [L - 0.2, 2.15], [L - 0.32, 1.25]];
  s.moveTo(pr[0][0], pr[0][1]); pr.slice(1).forEach((p) => s.lineTo(p[0], p[1])); s.closePath();
  const bt = 0.06, bgeo = new THREE.ExtrudeGeometry(s, { depth: BW - 2 * bt, bevelEnabled: true, bevelThickness: bt, bevelSize: 0.05, bevelSegments: 3, curveSegments: 4 });
  bgeo.rotateY(-Math.PI / 2); bgeo.translate(BW / 2 - bt, 0, 0);
  const body = new THREE.Mesh(bgeo, M.body); body.castShadow = true; body.receiveShadow = true; g.add(body);
  const shell = [body];
  // orange-red band along both sides and across both noses
  for (const sx of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.3, L - 0.7), M.band); b.position.set(sx * (BW / 2 + 0.008), 2.05, L / 2); g.add(b); shell.push(b); }
  for (const [z, f] of [[0.18, 1], [L - 0.18, -1]]) { const b = new THREE.Mesh(new THREE.BoxGeometry(BW + 0.06, 0.3, 0.012), M.band); b.position.set(0, 2.05, z - f * 0.02); b.rotation.x = -f * 0.12; g.add(b); shell.push(b); }
  // windscreens (two panes per cab on the sloped front), cab side windows and doors
  const tilt = Math.atan2(0.35, 1.4);
  for (const [z0, f] of [[0, 1], [L, -1]]) {
    for (const sx of [-1, 1]) { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.28, 0.78), M.glass); w.position.set(sx * 0.7, 3.05, z0 + f * 0.35); w.rotation.set(f * tilt, f > 0 ? Math.PI : 0, 0); g.add(w); shell.push(w);
      const sw = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 0.62), M.glass); sw.position.set(sx * (BW / 2 + 0.006), 3.2, z0 + f * 1.25); sw.rotation.y = sx * Math.PI / 2; g.add(sw); shell.push(sw);
      const dr = new THREE.Mesh(new THREE.BoxGeometry(0.01, 2.0, 0.75), M.under); dr.position.set(sx * (BW / 2 + 0.005), 2.55, z0 + f * 2.2); g.add(dr); shell.push(dr);
      const dw = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.5), M.glass); dw.position.set(sx * (BW / 2 + 0.012), 3.15, z0 + f * 2.2); dw.rotation.y = sx * Math.PI / 2; g.add(dw); shell.push(dw); }
    // headlights (twin, top centre) and marker lamps
    const hl = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.24, 0.1), M.black); hl.position.set(0, 3.86, z0 + f * 0.72); g.add(hl); shell.push(hl);
    for (const sx of [-0.17, 0.17]) { const l = new THREE.Mesh(new THREE.CircleGeometry(0.085, 16), M.lamp); l.position.set(sx, 3.86, z0 + f * 0.665); if (f > 0) l.rotation.y = Math.PI; g.add(l); }
    for (const sx of [-1.15, 1.15]) { const l = new THREE.Mesh(new THREE.CircleGeometry(0.07, 12), new THREE.MeshStandardMaterial({ color: 0x220000, emissive: f > 0 ? 0xfff0d0 : 0xff2a10, emissiveIntensity: 3 }));
      l.position.set(sx, 1.65, z0 + f * 0.13); if (f > 0) l.rotation.y = Math.PI; g.add(l); }
    // pilot (cow-catcher) and centre buffer coupler
    const pg = new THREE.BufferGeometry(); const pv = [-1.45, 0.18, 0.15, 1.45, 0.18, 0.15, 1.5, 1.2, 0.35, -1.5, 1.2, 0.35, -1.45, 0.18, 0.75, 1.45, 0.18, 0.75, 1.5, 1.2, 0.8, -1.5, 1.2, 0.8];
    pg.setAttribute("position", new THREE.Float32BufferAttribute(pv, 3)); pg.setIndex([0, 1, 2, 0, 2, 3, 4, 6, 5, 4, 7, 6, 0, 4, 5, 0, 5, 1, 3, 2, 6, 3, 6, 7, 0, 3, 7, 0, 7, 4, 1, 5, 6, 1, 6, 2]); pg.computeVertexNormals();
    const pilot = new THREE.Mesh(pg, M.under); if (f < 0) { pilot.scale.z = -1; pilot.position.z = L; } g.add(pilot); shell.push(pilot);
    const cbc = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.3, 0.6), M.darkSteel); cbc.position.set(0, 0.95, z0 - f * 0.05); g.add(cbc);
  }
  // machine-room louvres along both sides
  for (const sx of [-1, 1]) for (let i = 0; i < 6; i++) { const lv = new THREE.Mesh(new THREE.PlaneGeometry(1.7, 1.0), M.louvre); lv.position.set(sx * (BW / 2 + 0.005), 3.15, 4.6 + i * 2.25); lv.rotation.y = sx * Math.PI / 2; g.add(lv); shell.push(lv); }
  // underframe skirt, transformer tank between bogies
  const sk = new THREE.Mesh(new THREE.BoxGeometry(BW, 0.32, L - 0.9), M.under); sk.position.set(0, 1.1, L / 2); sk.castShadow = true; g.add(sk); shell.push(sk);
  const tank = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.6, 5.2), M.under); tank.position.set(0, 0.66, L / 2); g.add(tank); shell.push(tank);
  // roof: equipment hatch, two pantographs, insulators, Kavach dome antennas near the leading cab
  const rf = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.12, L - 4.2), M.roof); rf.position.set(0, 4.26, L / 2); g.add(rf); shell.push(rf);
  const panto = (z, up) => { const p = new THREE.Group(); p.position.set(0, 4.32, z);
    const base = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.12, 1.3), M.darkSteel); p.add(base);
    for (const sx of [-0.45, 0.45]) { const ins = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.28, 8), new THREE.MeshStandardMaterial({ color: 0x8a3a2a, roughness: 0.4 })); ins.position.set(sx, -0.08, 0); p.add(ins); }
    const h = up ? 5.5 - 4.32 - 0.1 : 0.25, la = Math.hypot(1.0, h * 0.5), ang = Math.atan2(h * 0.5, 1.0);
    const a1 = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, la, 6), M.galv); a1.rotation.x = Math.PI / 2 - ang; a1.position.set(0, h * 0.25 + 0.06, -0.5 + 0.0); p.add(a1);
    const a2 = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, la, 6), M.galv); a2.rotation.x = -(Math.PI / 2 - ang); a2.position.set(0, h * 0.75 + 0.06, -0.5); p.add(a2);
    const head = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.06, 0.12), M.darkSteel); head.position.set(0, h + 0.08, -0.5); p.add(head);
    g.add(p); return p; };
  panto(4.6, false); panto(L - 4.6, true);
  const domes = []; const dg = new THREE.SphereGeometry(0.14, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2); dg.scale(1, 0.9, 1);
  for (const [x, z] of [[-0.6, 2.0], [0.6, 2.0], [-0.6, 2.7], [0.6, 2.7]]) { const d = new THREE.Mesh(dg, M.black); d.position.set(x, 4.27, z); g.add(d); domes.push(d);
    const st = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.08, 8), M.black); st.position.set(x, 4.23, z); g.add(st); }
  // bogies
  const B = [bogie(M, { axles: 3, pitch: 1.95, r: WR_LOCO, blockMat: M.blockHot }), bogie(M, { axles: 3, pitch: 1.95, r: WR_LOCO, blockMat: M.blockHot })];
  B[0].g.position.z = 4.6; B[1].g.position.z = L - 4.6; g.add(B[0].g, B[1].g);
  // Kavach parts (visible in X-ray): loco computer in the machine room, RFID readers under the frame, wheel sensors, cab screen, brake link
  const glowMat = (c) => new THREE.MeshStandardMaterial({ color: 0x1a1d20, emissive: new THREE.Color(c), emissiveIntensity: 0, roughness: 0.5, metalness: 0.3 });
  const comp = new THREE.Group(); comp.position.set(0.55, 2.0, 3.4);
  const cbox = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.75, 0.6), M.cabinet); comp.add(cbox);
  const cpl = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.15), new THREE.MeshStandardMaterial({ map: TEX.plate, roughness: 0.5 })); cpl.position.set(0, 0.25, 0.302); comp.add(cpl);
  const ccard = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.42), new THREE.MeshStandardMaterial({ map: TEX.cards, roughness: 0.5, emissive: 0xffffff, emissiveMap: TEX.cards, emissiveIntensity: 0.15 })); ccard.position.set(0, -0.08, 0.302); comp.add(ccard);
  const cglow = new THREE.Mesh(new THREE.BoxGeometry(1.16, 0.81, 0.66), glowMat(0x38bdf8)); cglow.material.transparent = true; cglow.material.opacity = 0; comp.add(cglow);
  g.add(comp);
  const readers = [1.7, L - 1.7].map((z) => { const r = new THREE.Mesh(new RoundedBoxGeometry(0.5, 0.1, 0.32, 2, 0.02), glowMat(0x38bdf8)); r.position.set(0, 0.24, z); g.add(r); return r; });
  const sensors = [B[0], B[1]].map((b) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.14, 12), glowMat(0x38bdf8)); m.rotation.z = Math.PI / 2;
    m.position.set(RAIL_X + 0.4, WR_LOCO, b.g.position.z - 1.95); g.add(m); return m; });
  const screen = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.3, 0.06), glowMat(0x38bdf8)); screen.position.set(-0.55, 2.55, 0.85); screen.rotation.x = -0.5; g.add(screen);
  const linkPts = [new THREE.Vector3(0.55, 1.65, 3.4), new THREE.Vector3(0.55, 1.35, 3.8), new THREE.Vector3(0.3, 1.0, 4.0), new THREE.Vector3(0.3, 0.95, 5.8)];
  const brake = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(linkPts), 24, 0.04, 6), glowMat(0x38bdf8)); g.add(brake);
  const bpipe = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, L - 0.4, 6).rotateX(Math.PI / 2), glowMat(0x38bdf8)); bpipe.position.set(0.95, 0.92, L / 2); g.add(bpipe);
  // X-ray: shell fades to a ghost with cyan edges
  const edgeMat = new THREE.LineBasicMaterial({ color: 0x5fd4ff, transparent: true, opacity: 0, fog: false });
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(bgeo, 25), edgeMat); g.add(edges);
  const ghostMats = [M.body, M.band, M.glass, M.under, M.louvre, M.roof];
  ghostMats.forEach((m) => { m.transparent = true; });
  g.userData = {
    L, wheels: B.flatMap((b) => b.wheels), blocks: B.flatMap((b) => b.blocks), blockMat: M.blockHot, domes, bogies: B,
    parts: { computer: { g: comp, glow: cglow }, readers, sensors, screen, brake, bpipe },
    xray(k) { ghostMats.forEach((m) => { m.opacity = lerp(1, 0.06, k); m.depthWrite = k < 0.5; }); edgeMat.opacity = 0.8 * k; },
    setS(s) { for (const w of this.wheels) w.rotation.x = -s / WR_LOCO; },
  };
  g.userData.xray(0);
  return g;
}
/** LHB coach (red upper, grey lower), 23.54 m over couplers; local nose at z = 0 */
export function buildCoach(M0) {
  const M = Object.assign({}, M0, {
    side: new THREE.MeshPhysicalMaterial({ map: TEX.coachSide, roughness: 0.45, metalness: 0.15, clearcoat: 0.3 }),
    shell: new THREE.MeshStandardMaterial({ color: 0x9a2329, roughness: 0.5, metalness: 0.2 }),
    roofC: new THREE.MeshStandardMaterial({ color: 0x8e9196, roughness: 0.6, metalness: 0.4 }),
    bogie: new THREE.MeshStandardMaterial({ color: 0x1f2124, roughness: 0.7, metalness: 0.4 }),
    spring: new THREE.MeshStandardMaterial({ color: 0x2e3135, roughness: 0.6, metalness: 0.5 }),
    wheel: new THREE.MeshStandardMaterial({ color: 0x55585c, roughness: 0.45, metalness: 0.9 }),
    under: new THREE.MeshStandardMaterial({ color: 0x2c2e31, roughness: 0.8, metalness: 0.3 }),
  });
  const g = new THREE.Group(), L = 23.54, BL = 23.0, W = 3.24;
  const cs = new THREE.Shape(); cs.moveTo(-W / 2, 1.1); cs.lineTo(W / 2, 1.1); cs.lineTo(W / 2, 3.55); cs.quadraticCurveTo(W / 2, 3.95, 1.1, 4.0); cs.lineTo(-1.1, 4.0); cs.quadraticCurveTo(-W / 2, 3.95, -W / 2, 3.55); cs.closePath();
  const bg = new THREE.ExtrudeGeometry(cs, { depth: BL, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.03, bevelSegments: 2, curveSegments: 6 }); bg.translate(0, 0, (L - BL) / 2);
  const body = new THREE.Mesh(bg, M.shell); body.castShadow = true; body.receiveShadow = true; g.add(body);
  for (const sx of [-1, 1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(BL - 0.1, 2.44), M.side); p.position.set(sx * (W / 2 + 0.034), 2.33, L / 2); p.rotation.y = sx * Math.PI / 2; if (sx < 0) p.scale.x = -1; g.add(p); }
  const roof = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.08, BL - 1), M.roofC); roof.position.set(0, 4.04, L / 2); g.add(roof);
  const sk = new THREE.Mesh(new THREE.BoxGeometry(W - 0.4, 0.5, BL - 2), M.under); sk.position.set(0, 0.92, L / 2); g.add(sk);
  for (const z of [0.12, L - 0.12]) { const gw = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.3, 0.3), M.bogie); gw.position.set(0, 2.3, z); g.add(gw); }
  const B = [bogie(M, { axles: 2, pitch: 2.56, r: WR_COACH, frameY: 0.62 }), bogie(M, { axles: 2, pitch: 2.56, r: WR_COACH, frameY: 0.62 })];
  B[0].g.position.z = L / 2 - 7.45; B[1].g.position.z = L / 2 + 7.45; g.add(B[0].g, B[1].g);
  const bpipe = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, L - 0.2, 6).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x1a1d20, emissive: new THREE.Color(0x38bdf8), emissiveIntensity: 0 })); bpipe.position.set(0.95, 0.72, L / 2); g.add(bpipe);
  g.userData = { L, wheels: B.flatMap((b) => b.wheels), blocks: B.flatMap((b) => b.blocks), bpipe, setS(s) { for (const w of this.wheels) w.rotation.x = -s / WR_COACH; } };
  return g;
}
/** loco + n coaches, coupled with 0.6 m gaps; userData.place(zNose, s) puts the nose at zNose and turns the wheels */
export function buildTrain(M, { coaches = 4 } = {}) {
  const g = new THREE.Group(), loco = buildLoco(M); g.add(loco); const cars = [loco]; let z = loco.userData.L + 0.6;
  for (let i = 0; i < coaches; i++) { const c = buildCoach(M); c.position.z = z; g.add(c); cars.push(c); z += c.userData.L + 0.6; }
  g.userData = { loco, cars, length: z - 0.6, place(zNose, s = 0) { g.position.z = zNose; for (const c of cars) c.userData.setS(s); } };
  return g;
}

// ------------------------------------------------------------------------------------------------ station equipment
/** station Kavach cabinet: tall light-grey cabinet, four lifting eyes, glass door over card racks, red plate (TCAS_Stationary_Master_Computer.jpg) */
export function buildStationKavach(M) {
  const g = new THREE.Group();
  const box = new THREE.Mesh(new RoundedBoxGeometry(1.0, 1.6, 0.8, 3, 0.03), M.cabinet); box.position.y = 0.8; box.castShadow = true; box.receiveShadow = true; g.add(box);
  for (const [x, z] of [[-0.38, -0.3], [0.38, -0.3], [-0.38, 0.3], [0.38, 0.3]]) { const e = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.014, 6, 14), M.galv); e.position.set(x, 1.66, z); g.add(e); }
  const rack = new THREE.Mesh(new THREE.PlaneGeometry(0.78, 0.9), new THREE.MeshStandardMaterial({ map: TEX.cards, emissive: 0xffffff, emissiveMap: TEX.cards, emissiveIntensity: 0.25, roughness: 0.4 }));
  rack.position.set(0, 0.62, 0.402); g.add(rack);
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.94), new THREE.MeshPhysicalMaterial({ color: 0x223040, roughness: 0.05, metalness: 0.2, transparent: true, opacity: 0.25 })); glass.position.set(0, 0.62, 0.41); g.add(glass);
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.155), new THREE.MeshStandardMaterial({ map: TEX.plate, roughness: 0.5 })); pl.position.set(0, 1.32, 0.405); g.add(pl);
  const glow = new THREE.Mesh(new THREE.BoxGeometry(1.06, 1.66, 0.86), new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); glow.position.y = 0.8; g.add(glow);
  g.userData = { glow, port: new THREE.Vector3(0, 1.0, 0) }; return g;
}
/** relay room rack: a tall frame full of plug-in relays (interlocking) */
export function buildRelayRack(M, { w = 1.0, h = 2.3, seed = 1 } = {}) {
  const g = new THREE.Group(), r = mulberry32(seed);
  const fr = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.5), new THREE.MeshStandardMaterial({ color: 0x3c4f63, roughness: 0.6, metalness: 0.5 })); fr.position.y = h / 2; fr.castShadow = true; g.add(fr);
  const n = Math.floor((w - 0.1) / 0.11) * Math.floor((h - 0.3) / 0.2), rg = new THREE.BoxGeometry(0.09, 0.15, 0.08);
  const rm = new THREE.InstancedMesh(rg, new THREE.MeshStandardMaterial({ color: 0xc9ccd0, roughness: 0.5, metalness: 0.2 }), n), m4 = new THREE.Matrix4(); let k = 0;
  const leds = []; const lg = new THREE.CircleGeometry(0.012, 6);
  for (let y = 0.25; y < h - 0.1 && k < n; y += 0.2) for (let x = -w / 2 + 0.08; x < w / 2 - 0.05 && k < n; x += 0.11) { m4.makeTranslation(x, y, 0.28); rm.setMatrixAt(k++, m4);
    if (r() < 0.25) { const l = new THREE.Mesh(lg, new THREE.MeshBasicMaterial({ color: r() < 0.6 ? 0x22c55e : 0xf59e0b })); l.position.set(x + 0.03, y + 0.05, 0.322); g.add(l); leds.push(l); } }
  g.add(rm); g.userData = { leds }; return g;
}
/** lattice telecom tower (four tapering legs with cross bracing), panel antennas and whips on top, red aviation lamp */
export function buildTower(M, { h = 40, base = 6, top = 1.2 } = {}) {
  const g = new THREE.Group(), parts = [], leg = (y) => (base + (top - base) * (y / h)) / 2;
  const P = (sx, sz, y) => new THREE.Vector3(sx * leg(y), y, sz * leg(y));
  const bar = (a, b, r) => { const d = new THREE.Vector3().subVectors(b, a), L = d.length(), c = new THREE.CylinderGeometry(r, r, L, 5);
    c.translate(0, L / 2, 0); c.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize())); c.translate(a.x, a.y, a.z); parts.push(c); };
  const C = [[-1, -1], [1, -1], [1, 1], [-1, 1]], step = 2.5;
  for (const [sx, sz] of C) bar(P(sx, sz, 0), P(sx, sz, h), 0.07);
  for (let y = 0; y < h - 0.1; y += step) for (let i = 0; i < 4; i++) { const [ax, az] = C[i], [bx, bz] = C[(i + 1) % 4];
    bar(P(ax, az, y), P(bx, bz, y), 0.03); bar(P(ax, az, y), P(bx, bz, y + step), 0.022); bar(P(bx, bz, y), P(ax, az, y + step), 0.022); }
  const plat = new THREE.BoxGeometry(top + 1.2, 0.08, top + 1.2); plat.translate(0, h - 2.4, 0); parts.push(plat);
  const mast = new THREE.CylinderGeometry(0.05, 0.05, 4.5, 6); mast.translate(0, h + 2.2, 0); parts.push(mast);
  const tm = new THREE.Mesh(mergeGeometries(parts), M.galv); tm.castShadow = true; g.add(tm);
  const ant = []; const am = new THREE.MeshStandardMaterial({ color: 0xe5e5e0, roughness: 0.6 });
  for (let i = 0; i < 3; i++) { const a = new THREE.Mesh(new THREE.BoxGeometry(0.35, 1.6, 0.14), am); const ang = i * 2.094; a.position.set(Math.sin(ang) * (top / 2 + 0.35), h - 1.0, Math.cos(ang) * (top / 2 + 0.35)); a.rotation.y = ang; g.add(a); ant.push(a); }
  const whip = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 3.0, 6), am); whip.position.set(0.5, h + 1.5, 0); g.add(whip);
  const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.14, 10, 8), new THREE.MeshStandardMaterial({ color: 0x300000, emissive: 0xff2010, emissiveIntensity: 0 })); lamp.position.set(0, h + 4.5, 0); g.add(lamp);
  const hut = new THREE.Mesh(new THREE.BoxGeometry(2.6, 2.4, 2.0), M.cabinet); hut.position.set(base / 2 + 2.2, -0.75 + 1.2, 0); hut.castShadow = true; g.add(hut);
  g.position.y = -0.75; g.userData = { lamp, top: new THREE.Vector3(0, h - 1.0, 0), h }; return g;
}
/** small Indian wayside station building with the front wall and roof cut away (relay room inside) */
export function buildStationRoom(M, { w = 9, d = 6, h = 3.6 } = {}) {
  const g = new THREE.Group();
  const wallM = new THREE.MeshStandardMaterial({ color: 0xe2c27a, roughness: 0.9 }), trimM = new THREE.MeshStandardMaterial({ color: 0x7a2a1e, roughness: 0.8 }), floorM = new THREE.MeshStandardMaterial({ color: 0x8c8a84, roughness: 0.85 });
  const fl = new THREE.Mesh(new THREE.BoxGeometry(w, 0.2, d), floorM); fl.position.y = 0.1; fl.receiveShadow = true; g.add(fl);
  const back = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.25), wallM); back.position.set(0, h / 2 + 0.2, -d / 2); back.receiveShadow = true; g.add(back);
  for (const sx of [-1, 1]) { const s = new THREE.Mesh(new THREE.BoxGeometry(0.25, h, d), wallM); s.position.set(sx * w / 2, h / 2 + 0.2, 0); s.receiveShadow = s.castShadow = true; g.add(s); }
  const trim = new THREE.Mesh(new THREE.BoxGeometry(w + 0.3, 0.3, 0.3), trimM); trim.position.set(0, h + 0.2, -d / 2); g.add(trim);
  const cut = new THREE.Mesh(new THREE.BoxGeometry(w + 0.3, 0.3, 0.3), trimM); cut.position.set(0, 0.35, d / 2); g.add(cut);
  const lamp = new THREE.PointLight(0xfff1d6, 6, 14, 1.6); lamp.position.set(0, h - 0.2, 0); g.add(lamp);
  const tube = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.05, 0.08), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff4e0, emissiveIntensity: 4 })); tube.position.set(0, h + 0.05, -d / 2 + 0.25); g.add(tube);
  g.userData = { lamp }; return g;
}

// ------------------------------------------------------------------------------------------------ effects
/** a glowing tube along points; set(u0, u1, amt) lights the stretch between u0 and u1 (0..1 along the path) */
export function flowLine(points, { color = 0x38bdf8, radius = 0.03, base = 0.12 } = {}) {
  const curve = new THREE.CatmullRomCurve3(points), geo = new THREE.TubeGeometry(curve, Math.max(24, points.length * 16), radius, 6);
  const mat = new THREE.ShaderMaterial({ uniforms: { uC: { value: new THREE.Color(color) }, uA: { value: 0 }, uB: { value: 0 }, uAmt: { value: 0 }, uBase: { value: base } },
    vertexShader: `varying float vU; void main(){ vU = uv.x; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform vec3 uC; uniform float uA, uB, uAmt, uBase; varying float vU;
      void main(){ float on = smoothstep(uA - 0.03, uA, vU) * (1.0 - smoothstep(uB, uB + 0.03, vU)); float head = exp(-pow((vU - uB) * 30.0, 2.0));
        vec3 c = uC * (uBase + on * 1.6 + head * 5.0) * uAmt; gl_FragColor = vec4(c, 1.0); }`, transparent: false });
  const m = new THREE.Mesh(geo, mat); m.userData = { curve, set(a, b, amt = 1) { mat.uniforms.uA.value = a; mat.uniforms.uB.value = b; mat.uniforms.uAmt.value = amt; } }; return m;
}
/** expanding ring pulse (additive); at(k) with k = 0..1 through its life */
export function ringPulse({ color = 0x38bdf8, r0 = 0.2, r1 = 6, thick = 0.06 } = {}) {
  const m = new THREE.Mesh(new THREE.TorusGeometry(1, thick, 6, 64), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
  m.userData.at = (k) => { const s = lerp(r0, r1, ease.out(clamp(k))); m.scale.set(s, s, s); m.material.opacity = k <= 0 || k >= 1 ? 0 : 0.9 * Math.sin(Math.PI * clamp(k)); }; m.userData.at(0); return m;
}
/** a chain link (stadium torus) for the "four links" motif */
export function chainLink({ color = 0x38bdf8, size = 1 } = {}) {
  const s = new THREE.Shape(), r = 0.35 * size, l = 0.55 * size; s.absarc(-l / 2, 0, r, Math.PI / 2, Math.PI * 1.5); s.absarc(l / 2, 0, r, -Math.PI / 2, Math.PI / 2);
  const pts = s.getPoints(48).map((p) => new THREE.Vector3(p.x, p.y, 0)).filter((p, i, a) => i === 0 || p.distanceTo(a[i - 1]) > 1e-4);
  if (pts.length > 1 && pts[0].distanceTo(pts[pts.length - 1]) < 1e-4) pts.pop();   // no zero-length segment (NaN normals bloom into black blobs)
  const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 96, 0.07 * size, 10, true);
  // unlit shader glow (a lit/fogged material bloomed into dark halos on the software renderer); a soft rim keeps the 3D read
  const mat = new THREE.ShaderMaterial({ uniforms: { uC: { value: new THREE.Color(color) }, uK: { value: 0 } },
    vertexShader: `varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform vec3 uC; uniform float uK; varying vec3 vN; varying vec3 vV;
      void main(){ float ln = length(vN); float f = ln > 1e-4 ? clamp(abs(dot(vN / ln, normalize(vV))), 0.0, 1.0) : 1.0; vec3 base = vec3(0.03, 0.09, 0.13);
        gl_FragColor = vec4(base * (0.4 + 0.6 * f) + uC * uK * (0.55 + 0.45 * f), 1.0); }` });
  const m = new THREE.Mesh(geo, mat); m.userData.light = (k) => { mat.uniforms.uK.value = 2.6 * k; }; return m;
}
/** sparks at the brake blocks: seeded points whose positions are a pure function of t */
export function sparks({ n = 600, color = 0xffb060 } = {}) {
  const geo = new THREE.BufferGeometry(), pos = new Float32Array(n * 3), seeds = Array.from({ length: n }, (_, i) => mulberry32(1000 + i));
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({ color, size: 0.06, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false });
  const pts = new THREE.Points(geo, mat); pts.frustumCulled = false; const S = seeds.map((r) => [r(), r(), r(), r(), r(), r()]);
  /** emitters: array of world Vector3; amt 0..1 */
  pts.userData.at = (t, emitters, amt) => { mat.opacity = amt; for (let i = 0; i < n; i++) { const s = S[i], e = emitters[i % emitters.length], life = 0.5, a = ((t * (1.4 + s[0]) + s[1]) % life) / life;
      const vx = (s[2] - 0.5) * 2.0, vy = 1.0 + s[3] * 1.5, vz = 2 + s[4] * 4;
      pos[i * 3] = e.x + vx * a * 0.6; pos[i * 3 + 1] = e.y + (vy * a - 4.9 * a * a) * 0.6; pos[i * 3 + 2] = e.z + vz * a * 0.6; }
    geo.attributes.position.needsUpdate = true; };
  return pts;
}
/** 2D canvas DMI texture (simplified LP-OCIP layout) for the cab screen in close-ups; redraw(state) per frame */
export function dmiTexture() {
  const c = document.createElement("canvas"); c.width = 512; c.height = 384; const g = c.getContext("2d"), tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  tex.userData.redraw = ({ v = 0, vp = 110, asp = 1, sd = 1200, warn = 0 }) => {
    g.fillStyle = "#050607"; g.fillRect(0, 0, 512, 384); const cx = 150, cy = 170, R = 110, a = (x) => (-210 + 240 * x / 200) * Math.PI / 180;
    g.lineWidth = 10; g.strokeStyle = "#22c55e"; g.beginPath(); g.arc(cx, cy, R + 6, a(0), a(vp)); g.stroke();
    g.strokeStyle = "#e5e7eb"; g.lineWidth = 2; for (let x = 0; x <= 200; x += 20) { const q = a(x); g.beginPath(); g.moveTo(cx + Math.cos(q) * R, cy + Math.sin(q) * R); g.lineTo(cx + Math.cos(q) * (R - 14), cy + Math.sin(q) * (R - 14)); g.stroke(); }
    const q = a(v); g.lineWidth = 5; g.strokeStyle = "#f8fafc"; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.cos(q) * 92, cy + Math.sin(q) * 92); g.stroke();
    g.fillStyle = v > vp + 2 ? "#f59e0b" : "#f8fafc"; g.beginPath(); g.arc(cx, cy, 26, 0, 6.3); g.fill(); g.fillStyle = "#050607"; g.font = "800 22px Inter, Arial"; g.textAlign = "center"; g.fillText(String(Math.round(v)), cx, cy + 8);
    g.fillStyle = "#38bdf8"; const mf = clamp(sd / 2000); g.fillRect(320, 60 + 220 * (1 - mf), 18, 220 * mf);
    g.strokeStyle = "#e5e7eb"; g.lineWidth = 3; g.beginPath(); g.roundRect(380, 60, 70, 200, 32); g.stroke();
    ["#facc15", "#22c55e", "#facc15", "#ef4444"].forEach((col, i) => { g.beginPath(); g.arc(415, 92 + i * 46, 17, 0, 6.3); g.fillStyle = i === asp ? col : "#0a0a0a"; g.fill(); g.stroke(); });
    g.fillStyle = warn > 0 ? "#713f12" : "#0b0c0e"; g.fillRect(0, 320, 512, 40); g.fillStyle = "#f8fafc"; g.font = "600 20px Inter, Arial"; g.textAlign = "left";
    g.fillText(warn > 0 ? "Signal at Danger · Reduce Speed" : `Signal in ${String(Math.round(sd)).padStart(4, "0")} m`, 12, 347);
    tex.needsUpdate = true; };
  tex.userData.redraw({}); return tex;
}

// ------------------------------------------------------------------------------------------------ RFID tag + the four-link rig
/** RFID tag after TCAS_RFID_Tag.jpg: grey metal/FRP box with rounded corners, yellow triangle and printed ID on top,
 *  two stainless clamps wrapping the sleeper; place on a sleeper centre (x across the track) */
export function buildRFIDTag(M) {
  const g = new THREE.Group();
  const box = new THREE.Mesh(new RoundedBoxGeometry(0.46, 0.075, 0.17, 3, 0.02), new THREE.MeshStandardMaterial({ color: 0xaeb4ba, roughness: 0.35, metalness: 0.75 }));
  box.position.y = 0.0375; box.castShadow = true; g.add(box);
  const top = new THREE.Mesh(new THREE.PlaneGeometry(0.44, 0.15), new THREE.MeshStandardMaterial({ map: TEX.tagTop, roughness: 0.4, metalness: 0.5 }));
  top.rotation.x = -Math.PI / 2; top.position.y = 0.0757; g.add(top);
  const steel = new THREE.MeshStandardMaterial({ color: 0xd0d4d8, roughness: 0.25, metalness: 1 });
  for (const sx of [-0.15, 0.15]) for (const sz of [-1, 1]) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.25, 0.008), steel); c.position.set(sx, -0.08, sz * 0.13); g.add(c); }
  const glow = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.09, 0.2), new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); glow.position.y = 0.04; g.add(glow);
  g.userData = { glow }; return g;
}
export const sleeperZ = (z0, target) => z0 + (Math.round((target - z0) / 0.6 - 0.5) + 0.5) * 0.6;
export const SLEEPER_TOP = -0.172 - 0.012;
/**
 * The four-link rig shared by A2, A7, A9: track (RFID tag on a sleeper ahead of the train), the station relay room with
 * interlocking racks and the station Kavach cabinet, a lattice radio tower, and the train (loco cab). P holds the four
 * link anchors in world space: track, station, tower, cab.
 */
export function buildRig(M, S, { coaches = 2, trees = true } = {}) {
  const Z0 = -260;
  S.add(buildGround(M));
  S.add(buildTrack(M, { cx: 0, z0: Z0, z1: 140 }), buildTrack(M, { cx: 5.3, z0: Z0, z1: 140 }));
  S.add(buildOHE(M, { cx: 0, mx: -3.4, z0: Z0, z1: 140, phase: 25 }), buildOHE(M, { cx: 5.3, mx: 8.7, z0: Z0, z1: 140, phase: 55 }));
  if (trees) S.add(buildTrees({ clear: 34, n: 420 }));
  const train = buildTrain(M, { coaches }); train.userData.place(0, 0); S.add(train);
  const zt = sleeperZ(Z0, -9); const tag = buildRFIDTag(M); tag.position.set(0, SLEEPER_TOP, zt); S.add(tag);
  // station relay room, open side toward a camera ahead of the train (rotated half a turn); racks and cabinet inside
  const room = buildStationRoom(M, { w: 9, d: 6, h: 3.6 }); room.position.set(-12, -0.75, 6); room.rotation.y = Math.PI; S.add(room);
  const racks = [0, 1, 2].map((i) => { const r = buildRelayRack(M, { seed: i + 2 }); r.position.set(-3.3 + i * 1.15, 0.2, -2.6); room.add(r); return r; });
  const cab = buildStationKavach(M); cab.position.set(2.6, 0.2, -2.4); room.add(cab);
  const tower = buildTower(M, { h: 30, base: 5, top: 1.1 }); tower.position.set(14, -0.75, 34); S.add(tower);
  room.updateMatrixWorld(true);
  const P = { track: new THREE.Vector3(0, SLEEPER_TOP + 0.9, zt), station: room.localToWorld(new THREE.Vector3(-1, 4.6, 0)), tower: new THREE.Vector3(14, 25.5, 34), cab: new THREE.Vector3(0, 5.6, 1.4),
    rack: room.localToWorld(new THREE.Vector3(-2.15, 1.6, -2.3)), kav: room.localToWorld(new THREE.Vector3(2.6, 1.2, -2.0)) };
  return { train, loco: train.userData.loco, tag, room, racks, cab, tower, P, zt };
}
