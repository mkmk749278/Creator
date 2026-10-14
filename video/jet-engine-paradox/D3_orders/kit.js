// Session D instrument kit: precision instruments drawn on a 2D canvas each frame and shown on a plane in the shared
// 3D stage (same slate, grain, bloom and dust as the globe), with a slow camera drift so nothing is ever flat.
// Two layers: `g` (base: line work, engraved scales, numbers) and `k` (glow: lit parts, x2.4 into bloom).
// Master copy in video/jet-engine-paradox/_d_lib/ (synced into scene folders).
import { THREE, PAL, clamp, lerp, K, E } from "./jepd.js";

export const CW = 2880, CH = 1620, SC = CW / 1920;   // canvas is 1.5x the frame; draw in frame px via ctx scale
export const HEX = { slate: "#0B0E14", amber: "#F97316", hot: "#FDBA74", red: "#EF4444", white: "#F8FAFC", dim: "#94A3B8", line: "rgba(248,250,252,0.55)", faint: "rgba(248,250,252,0.16)" };
export const FONT = "Inter, Arial, sans-serif";

/** wait for the vendored Inter faces before the first canvas draw (HyperFrames waits for the default manager) */
export function loadFonts() {
  const m = THREE.DefaultLoadingManager; m.itemStart("inter-fonts");
  Promise.all(["600 40px Inter", "800 40px Inter", "800 40px Inter"].map((f) => document.fonts.load(f, "0123456789₹,~"))).finally(() => m.itemEnd("inter-fonts"));
}

export class Panel {
  /** stage: jepd Stage; opts.drift: [[t, [rx, ry, z]], ...] camera keyframes (deg, deg, distance factor) */
  constructor(stage, { drift = null } = {}) {
    this.st = stage; this.drift = drift;
    const mk = () => { const c = document.createElement("canvas"); c.width = CW; c.height = CH; const x = c.getContext("2d"); x.setTransform(SC, 0, 0, SC, 0, 0); return [c, x]; };
    [this.cb, this.g] = mk(); [this.ck, this.k] = mk();
    const tex = (c) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter; t.premultiplyAlpha = true; return t; };
    this.tb = tex(this.cb); this.tk = tex(this.ck);
    const cam = stage.camera; cam.fov = 30; cam.updateProjectionMatrix();
    this.D = (1080 / 2) / Math.tan(15 * Math.PI / 180) / 1000;   // distance at which a 1.92 x 1.08 plane fills the frame
    const geo = new THREE.PlaneGeometry(1.92, 1.08);
    this.base = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: this.tb, transparent: true, premultipliedAlpha: true, depthWrite: false, toneMapped: false }));
    this.glow = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: this.tk, transparent: true, depthWrite: false, toneMapped: false,
      blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
      blendSrcAlpha: THREE.ZeroFactor, blendDstAlpha: THREE.OneFactor, color: new THREE.Color(2.4, 2.4, 2.4) }));
    this.glow.position.z = 0.0005; stage.scene.add(this.base, this.glow);
  }
  begin() { for (const x of [this.g, this.k]) { x.save(); x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, CW, CH); x.restore(); } }
  end(t) {
    this.tb.needsUpdate = true; this.tk.needsUpdate = true;
    const d = this.drift ? K(t, this.drift) : [0, 0, 1];
    const cam = this.st.camera, r = this.D * d[2];
    const ry = d[1] * Math.PI / 180, rx = d[0] * Math.PI / 180;
    cam.position.set(Math.sin(ry) * Math.cos(rx) * r, Math.sin(rx) * r, Math.cos(ry) * Math.cos(rx) * r);
    cam.lookAt(0, 0, 0); cam.updateMatrixWorld();
    // background grid drifts against the panel for parallax
    this.st.bgU.uShift.value.set(-d[1] * 22, d[0] * 22);
  }
}

// ---------- drawing primitives (frame px) ----------
export function text(x, s, px, py, { size = 32, weight = 800, color = HEX.white, align = "left", base = "alphabetic", track = 0.04, alpha = 1 } = {}) {
  if (alpha <= 0.002) return; x.save(); x.globalAlpha *= alpha; x.font = `${weight} ${size}px ${FONT}`; x.fillStyle = color; x.textAlign = align; x.textBaseline = base;
  if ("letterSpacing" in x) x.letterSpacing = `${(track * size).toFixed(1)}px`;
  x.fillText(s, px, py); x.restore();
}
export function line(x, x0, y0, x1, y1, { w = 2, color = HEX.line, dash = null, alpha = 1, cap = "butt" } = {}) {
  if (alpha <= 0.002) return; x.save(); x.globalAlpha *= alpha; x.strokeStyle = color; x.lineWidth = w; x.lineCap = cap; if (dash) x.setLineDash(dash);
  x.beginPath(); x.moveTo(x0, y0); x.lineTo(x1, y1); x.stroke(); x.restore();
}
/** draw a path partially (k 0..1) using dash offset; path given as Path2D and its length */
export function strokeK(x, p, L, k, { w = 2, color = HEX.line, alpha = 1 } = {}) {
  if (k <= 0 || alpha <= 0.002) return; x.save(); x.globalAlpha *= alpha; x.strokeStyle = color; x.lineWidth = w; x.lineJoin = "round"; x.lineCap = "round";
  x.setLineDash([L * k, L * 2]); x.stroke(p); x.restore();
}
export function fillP(x, p, color, alpha = 1) { if (alpha <= 0.002) return; x.save(); x.globalAlpha *= alpha; x.fillStyle = color; x.fill(p); x.restore(); }

// ---------- icons (generic, not any manufacturer's drawing) ----------
/** top view of a generic delta-wing light fighter, nose up, unit height 1 centred on 0,0 */
export function jetPath(cx, cy, s) {
  const P = [[0, -0.5], [0.045, -0.38], [0.06, -0.12], [0.37, 0.25], [0.37, 0.31], [0.08, 0.31], [0.07, 0.38], [0.15, 0.47], [0.15, 0.5],
    [0.04, 0.5], [0, 0.46]];
  const p = new Path2D(); const all = [...P, ...P.slice(0, -1).reverse().map(([a, b]) => [-a, b])];
  all.forEach(([a, b], i) => (i ? p.lineTo(cx + a * s, cy + b * s) : p.moveTo(cx + a * s, cy + b * s))); p.closePath(); return p;
}
export const JET_LEN = 3.05;   // perimeter of jetPath per unit size (for stroke draw-on)
/** side view of a generic turbofan: nacelle, fan face line, nozzle; unit width 1 centred */
export function enginePath(cx, cy, s) {
  const p = new Path2D(), X = (v) => cx + v * s, Y = (v) => cy + v * s;
  p.moveTo(X(-0.5), Y(-0.17)); p.lineTo(X(0.26), Y(-0.17)); p.lineTo(X(0.42), Y(-0.1)); p.lineTo(X(0.5), Y(-0.08));
  p.lineTo(X(0.5), Y(0.08)); p.lineTo(X(0.42), Y(0.1)); p.lineTo(X(0.26), Y(0.17)); p.lineTo(X(-0.5), Y(0.17)); p.closePath();
  p.moveTo(X(-0.38), Y(-0.17)); p.lineTo(X(-0.38), Y(0.17)); p.moveTo(X(0.26), Y(-0.17)); p.lineTo(X(0.26), Y(0.17));
  return p;
}
/** engraved scale: ticks from v0..v1 every `minor`, labels every `major`, along a line or arc via map(v)->[x,y,nx,ny] */
export function scale(x, map, v0, v1, minor, major, { len = 14, lenMaj = 28, color = HEX.line, label = null, size = 22, k = 1 } = {}) {
  const n = Math.round((v1 - v0) / minor);
  for (let i = 0; i <= n; i++) {
    const v = v0 + i * minor; if ((i / n) > k) break;
    const [px, py, nx, ny] = map(v), maj = Math.abs(v / major - Math.round(v / major)) < 1e-6, L = maj ? lenMaj : len;
    line(x, px, py, px + nx * L, py + ny * L, { w: maj ? 2.4 : 1.4, color });
    if (maj && label) text(x, label(v), px + nx * (L + 12 + size * 0.5), py + ny * (L + 12 + size * 0.5) + size * 0.36, { size, weight: 600, color: HEX.dim, align: "center", track: 0.02 });
  }
}
export { clamp, lerp, E };
