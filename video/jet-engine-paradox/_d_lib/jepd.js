// Session D shared core ("The Hot Section", globe + data world). Master copy lives in video/jet-engine-paradox/_d_lib/;
// tools/sync.sh copies it into every D scene folder (scenes must be self-contained). Do not edit the copies.
// Everything here is a pure function of the time t the scene passes in: seeded RNG, no clocks, no stepped state.
import * as THREE from "three";
import { EffectComposer, RenderPass, EffectPass, BloomEffect, ToneMappingEffect, ToneMappingMode, Effect, BlendFunction, FXAAEffect } from "postprocessing";

export { THREE };
export const PAL = { slate: 0x0B0E14, slate2: 0x121826, amber: 0xF97316, amberHot: 0xFDBA74, red: 0xEF4444,
  white: 0xF8FAFC, dim: 0x94A3B8, cyan: 0x38BDF8 };
export const col = (hex) => new THREE.Color(hex);  // sRGB hex -> linear working colour

// ---------- math, easing, keyframes ----------
export const mulberry32 = (s) => () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, k) => a + (b - a) * k;
export const E = {
  lin: (x) => x,
  inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  inOutQ: (x) => (x < 0.5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2),
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
  out: (x) => 1 - Math.pow(1 - x, 3),
  outQ: (x) => 1 - Math.pow(1 - x, 5),
  in: (x) => x * x * x,
  outBack: (x) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
};
/** eased 0..1 progress of t through [a, b] */
export const seg = (t, a, b, ease = E.inOut) => ease(clamp((t - a) / (b - a)));
/** fade in over [a, a+fi], hold, fade out over [b-fo, b] */
export const window01 = (t, a, b, fi = 0.35, fo = 0.35) => Math.min(seg(t, a, a + fi, E.out), 1 - seg(t, b - fo, b, E.in));
/** keyframes [[time, value(s), ease?], ...]; the ease of a key shapes the segment that ends on it */
export function K(t, ks) {
  if (t <= ks[0][0]) return ks[0][1];
  for (let i = 1; i < ks.length; i++) {
    const [t1, v1, ez] = ks[i];
    if (t <= t1) {
      const [t0, v0] = ks[i - 1], k = (ez || E.inOut)((t - t0) / (t1 - t0));
      return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], k)) : lerp(v0, v1, k);
    }
  }
  return ks[ks.length - 1][1];
}
/** damped spring step from 0 to 1 starting at t0: needles and stamps with inertia (overshoot, settle) */
export function spring(t, t0, freq = 1.6, damp = 5.5) {
  const x = t - t0; if (x <= 0) return 0;
  return 1 - Math.exp(-damp * x) * (Math.cos(2 * Math.PI * freq * x) + (damp / (2 * Math.PI * freq)) * Math.sin(2 * Math.PI * freq * x));
}
export const fmt = (n) => Math.round(n).toLocaleString("en-US");

// ---------- post: grain + vignette (deterministic: frame index, not clock) ----------
class FilmEffect extends Effect {
  constructor({ grain = 0.05, vignette = 0.3 } = {}) {
    super("JepFilm", /* glsl */`
      uniform float uFrame; uniform float uGrain; uniform float uVig; uniform vec2 uRes;
      float hash(vec3 p) { p = fract(p * vec3(0.1031, 0.1030, 0.0973)); p += dot(p, p.yxz + 33.33); return fract((p.x + p.y) * p.z); }
      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
        vec2 px = floor(uv * uRes);
        float n = hash(vec3(px, uFrame)) + hash(vec3(px + 17.0, uFrame + 3.0)) - 1.0;   // triangular grain
        vec3 c = inputColor.rgb; if (any(isnan(c)) || any(isinf(c))) c = vec3(0.0);
        float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
        c += n * uGrain * (0.25 + 0.75 * sqrt(clamp(l, 0.0, 1.0)));
        vec2 q = (uv - 0.5) * vec2(uRes.x / uRes.y, 1.0);
        c *= 1.0 - uVig * smoothstep(0.35, 1.15, length(q));
        outputColor = vec4(max(c, 0.0), inputColor.a);
      }`, { blendFunction: BlendFunction.NORMAL, uniforms: new Map([["uFrame", new THREE.Uniform(0)],
      ["uGrain", new THREE.Uniform(grain)], ["uVig", new THREE.Uniform(vignette)], ["uRes", new THREE.Uniform(new THREE.Vector2(1920, 1080))]]) });
  }
}

// ---------- background plate: titanium slate, brushed, slow light sweep, optional drafting grid ----------
const BG_VERT = `varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position.xy, 0.9999, 1.0); }`;
const BG_FRAG = /* glsl */`
  varying vec2 vUv; uniform float uTime; uniform vec2 uGlow; uniform float uGlowR; uniform vec3 uBase; uniform vec3 uLift;
  uniform vec3 uWarm; uniform float uGrid; uniform vec2 uShift; uniform vec2 uRes;
  float h2(vec2 p) { vec3 q = fract(vec3(p.xyx) * 0.1031); q += dot(q, q.yzx + 33.33); return fract((q.x + q.y) * q.z); }  // no sin(): precise on software GL
  float vn(vec2 p) { vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
    return mix(mix(h2(i), h2(i + vec2(1, 0)), f.x), mix(h2(i + vec2(0, 1)), h2(i + vec2(1, 1)), f.x), f.y); }
  void main() {
    vec2 p = vUv * uRes;
    vec2 q = (vUv - uGlow) * vec2(uRes.x / uRes.y, 1.0);
    float g = exp(-dot(q, q) / (uGlowR * uGlowR));
    vec3 c = mix(uBase, uLift, 0.85 * g + 0.15);
    // brushed titanium: long horizontal streaks, very low amplitude
    float br = vn(vec2(p.x * 0.004, p.y * 0.9)) * 0.6 + vn(vec2(p.x * 0.02, p.y * 2.3)) * 0.4;
    c *= 0.93 + 0.12 * br;
    // slow diagonal light sweep (warm)
    float sw = vUv.x * 0.8 + vUv.y * 0.35 - uTime * 0.035;
    c += uWarm * 0.03 * exp(-pow((fract(sw) - 0.5) * 3.2, 2.0));
    // drafting grid (instrument scenes), drifts with the camera
    if (uGrid > 0.0) {
      vec2 gp = p + uShift;
      vec2 a = abs(fract(gp / 64.0 - 0.5) - 0.5) * 64.0, b = abs(fract(gp / 320.0 - 0.5) - 0.5) * 320.0;
      float l = (1.0 - smoothstep(0.0, 1.1, min(a.x, a.y))) * 0.5 + (1.0 - smoothstep(0.0, 1.3, min(b.x, b.y)));
      c += vec3(0.75, 0.8, 0.9) * l * uGrid * (0.4 + 0.6 * g);
    }
    gl_FragColor = vec4(c, 1.0);
  }`;

function dustSprite() {
  const c = document.createElement("canvas"); c.width = c.height = 64; const g = c.getContext("2d");
  const r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, "rgba(255,255,255,1)"); r.addColorStop(0.25, "rgba(255,255,255,0.55)"); r.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = r; g.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export class Stage {
  /** opts: fov, bloom {intensity, threshold, smoothing, radius}, grain, vignette, bg {glow:[u,v], glowR, base, lift, grid}, dust {count, color, size} */
  constructor(opts = {}) {
    const root = this.root = document.getElementById("root");
    this.W = +root.dataset.width; this.H = +root.dataset.height; this.DUR = +root.dataset.duration;
    const B = window.BENCH || {};
    const r = this.renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("gl"), antialias: false, stencil: false,
      depth: false, powerPreference: "high-performance", preserveDrawingBuffer: true });
    r.setPixelRatio(1); r.setSize(this.W, this.H, false); r.toneMapping = THREE.NoToneMapping;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(opts.fov || 30, this.W / this.H, 0.01, 100);
    // background plate
    const bg = opts.bg || {};
    this.bgU = { uTime: { value: 0 }, uGlow: { value: new THREE.Vector2(...(bg.glow || [0.6, 0.5])) }, uGlowR: { value: bg.glowR || 0.75 },
      uBase: { value: col(bg.base || 0x0d1119) }, uLift: { value: col(bg.lift || 0x1c2433) }, uWarm: { value: col(0xffb27a) },
      uGrid: { value: bg.grid || 0 }, uShift: { value: new THREE.Vector2() }, uRes: { value: new THREE.Vector2(this.W, this.H) } };
    const bgm = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ vertexShader: BG_VERT, fragmentShader: BG_FRAG,
      uniforms: this.bgU, depthWrite: false, depthTest: false }));
    bgm.frustumCulled = false; bgm.renderOrder = -1000; this.scene.add(bgm);
    // dust motes (camera space, seeded; positions are a function of t)
    const d = opts.dust || {}; const N = d.count ?? 260, rnd = mulberry32(d.seed || 11);
    this.dustSeed = Array.from({ length: N }, () => [rnd() * 2 - 1, rnd() * 2 - 1, rnd(), rnd(), rnd()]);
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(N * 3), 3));
    this.dust = new THREE.Points(g, new THREE.PointsMaterial({ map: dustSprite(), color: col(d.color || 0xffd7b0), size: d.size || 0.02,
      transparent: true, opacity: d.opacity ?? 0.5, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true }));
    this.dust.frustumCulled = false; this.camera.add(this.dust); this.scene.add(this.camera);
    // post
    this.composer = new EffectComposer(r, { frameBufferType: THREE.HalfFloatType, multisampling: B.msaa ?? (opts.msaa ?? 0) });  // MSAA is 2.4x slower on software GL (PLAYBOOK §15): FXAA instead
    this.composer.addPass(new RenderPass(this.scene, this.camera));
    const fx = [];
    const bl = opts.bloom || {};
    if (B.bloom !== 0) fx.push(this.bloom = new BloomEffect({ blendFunction: BlendFunction.ADD,  // default SCREEN goes negative on HDR (>1) pixels: dark bands
      intensity: bl.intensity ?? 1.0, luminanceThreshold: bl.threshold ?? 0.55,
      luminanceSmoothing: bl.smoothing ?? 0.25, mipmapBlur: true, radius: bl.radius ?? 0.72 }));
    fx.push(new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL }));  // AgX outset matrix darkened the bg around saturated amber bloom
    if (B.fxaa !== 0) fx.push(new FXAAEffect());
    fx.push(this.film = new FilmEffect({ grain: opts.grain ?? 0.045, vignette: opts.vignette ?? 0.3 }));
    this.composer.addPass(new EffectPass(this.camera, ...fx));
    this.composer.setSize(this.W, this.H);
    this.film.uniforms.get("uRes").value.set(this.W, this.H);
    this.overlay = document.getElementById("ov");
    this._v = new THREE.Vector3();
  }
  /** world point -> {x, y} in composition px (respects view offset) */
  toScreen(p) { const v = this._v.copy(p).project(this.camera); return { x: (v.x + 1) / 2 * this.W, y: (1 - v.y) / 2 * this.H, z: v.z }; }
  updateDust(t, depth = [1.2, 5.0]) {
    const a = this.dust.geometry.attributes.position, cam = this.camera, th = Math.tan(cam.fov * Math.PI / 360);
    this.dustSeed.forEach(([x, y, z, s, w], i) => {
      const zz = -lerp(depth[0], depth[1], z), hh = -zz * th, ww = hh * cam.aspect;
      // slow upward drift + sideways wander; wraps inside the view volume (pure function of t)
      let yy = ((y * 0.5 + 0.5 + t * (0.012 + 0.02 * s)) % 1) * 2 - 1;
      const xx = x + 0.04 * Math.sin(t * (0.3 + w * 0.5) + i);
      a.setXYZ(i, xx * ww * 1.1, yy * hh * 1.1, zz);
    });
    a.needsUpdate = true;
  }
  render(t) {
    this.bgU.uTime.value = t;
    this.film.uniforms.get("uFrame").value = Math.round(t * 30) % 977;
    this.updateDust(t);
    this.composer.render();
  }
}

// ---------- DOM overlay helpers ----------
/** Inter's vendored subsets have no "→" (U+2192): draw it as an inline SVG arrow */
export const arrows = (h) => h.replace(/→/g, '<svg class="arr" viewBox="0 0 40 20"><path d="M2 10H34M24 2L36 10L24 18" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="square"/></svg>');
export function el(parent, cls, html = "") { const e = document.createElement("div"); e.className = cls; e.innerHTML = arrows(html); parent.appendChild(e); return e; }
export function show(e, a, dx = 0, dy = 0, s = 1) {
  e.style.opacity = a.toFixed(3); e.style.visibility = a > 0.002 ? "visible" : "hidden";
  e.style.transform = `translate(${dx.toFixed(1)}px, ${dy.toFixed(1)}px) scale(${s.toFixed(4)})`;
}
/** text reveal: clip a single line from the left (no letter-spacing tweens) */
export function wipe(e, k) { e.style.clipPath = `inset(-20% ${(100 - 100 * clamp(k)).toFixed(2)}% -20% 0)`; }

/** a map/instrument callout: anchor dot, hairline leader, title + sub */
export class Callout {
  constructor(parent, { title, sub = "", side = 1, dx = 70, dy = -60, tone = "amber", cls = "" }) {
    this.e = el(parent, `jd-call ${tone} ${cls}`, `<div class="lead"></div><div class="dot"></div><div class="txt"><b>${arrows(title)}</b>${sub ? `<small>${sub}</small>` : ""}</div>`);
    this.lead = this.e.querySelector(".lead"); this.txt = this.e.querySelector(".txt"); this.side = side; this.dx = dx; this.dy = dy;
    if (side < 0) this.txt.style.transform = "translate(-100%, -50%)";
  }
  set(x, y, a, k = 1) {
    const e = this.e; e.style.left = x.toFixed(1) + "px"; e.style.top = y.toFixed(1) + "px";
    e.style.opacity = a.toFixed(3); e.style.visibility = a > 0.002 ? "visible" : "hidden";
    const dx = this.dx * this.side, dy = this.dy, L = Math.hypot(dx, dy) * clamp(k * 1.6), ang = Math.atan2(dy, dx);
    this.lead.style.width = L.toFixed(1) + "px"; this.lead.style.transform = `rotate(${ang}rad)`;
    const tk = clamp(k * 1.6 - 0.6);
    this.txt.style.left = (dx + 10 * this.side) + "px"; this.txt.style.top = dy + "px";
    this.txt.style.opacity = tk.toFixed(3);
    wipe(this.txt, tk);
  }
}
