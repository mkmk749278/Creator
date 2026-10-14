// Session D land-only globe: Natural Earth land as a signed distance field (library/geo/land_sdf_4k.png; merged
// landmasses, so there is no political border anywhere), night-side lighting, amber atmosphere rim, great-circle arcs,
// reticle markers. Master copy in video/jet-engine-paradox/_d_lib/ (synced into scene folders).
import { THREE, col, PAL, clamp, lerp } from "./jepd.js";
// additive colour that leaves the buffer alpha at 1 (plain AdditiveBlending also adds alpha, which darkened a band
// beside every arc once the bloom mip chain read it)
const ADD = { transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendEquation: THREE.AddEquation,
  blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendSrcAlpha: THREE.ZeroFactor, blendDstAlpha: THREE.OneFactor };

const D2R = Math.PI / 180;
/** unit vector for [lat, lon] in globe space (lon 0 faces +z, north is +y) */
export function dir(lat, lon) {
  const a = lat * D2R, b = lon * D2R;
  return new THREE.Vector3(Math.cos(a) * Math.sin(b), Math.sin(a), Math.cos(a) * Math.cos(b));
}
export const PLACES = {
  lynn: [42.47, -70.95], bengaluru: [12.97, 77.59], paris: [48.86, 2.35], derby: [52.92, -1.48],
  zhukovsky: [55.6, 38.12], moscow: [55.75, 37.62], india: [22.5, 79.0],
};

const NOISE = /* glsl */`
  float h3(vec3 p) { p = fract(p * vec3(0.1031, 0.1030, 0.0973)); p += dot(p, p.yxz + 33.33); return fract((p.x + p.y) * p.z); }
  float vn3(vec3 x) { vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
    return mix(mix(mix(h3(i), h3(i + vec3(1,0,0)), f.x), mix(h3(i + vec3(0,1,0)), h3(i + vec3(1,1,0)), f.x), f.y),
               mix(mix(h3(i + vec3(0,0,1)), h3(i + vec3(1,0,1)), f.x), mix(h3(i + vec3(0,1,1)), h3(i + vec3(1,1,1)), f.x), f.y), f.z); }
  float fbm(vec3 p) { return 0.55 * vn3(p) + 0.3 * vn3(p * 2.03 + 7.1) + 0.15 * vn3(p * 4.1 + 3.3); }`;

const GLOBE_VERT = `varying vec3 vP; varying vec3 vW; void main() { vP = position; vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`;
const GLOBE_FRAG = /* glsl */`
  uniform sampler2D uSdf; uniform vec3 uLight; uniform float uRange;
  uniform vec3 uLand; uniform vec3 uLandHi; uniform vec3 uOcean; uniform vec3 uOceanHi; uniform vec3 uCoast; uniform vec3 uRim;
  uniform vec4 uSpot[4]; uniform vec4 uSpotCol[4]; uniform float uGrat; uniform float uBright;
  varying vec3 vP; varying vec3 vW;
  ${NOISE}
  const float PI = 3.14159265;
  void main() {
    vec3 n = normalize(vP);
    float lat = asin(clamp(n.y, -1.0, 1.0)), lon = atan(n.x, n.z);
    vec2 uv = vec2(0.5 + lon / (2.0 * PI), 0.5 + lat / PI);
    float sd = (texture2D(uSdf, uv).r - 0.5) * 2.0 * uRange;      // texels (~9.8 km), positive on land
    float aa = clamp(fwidth(sd), 0.02, 6.0);
    float land = smoothstep(-0.7 * aa, 0.7 * aa, sd);
    vec3 V = normalize(cameraPosition - vW);
    // relief: noise bump inland (screen-space derivative bump)
    float hgt = (0.35 + 0.65 * fbm(n * 26.0)) * smoothstep(0.0, 14.0, sd);
    vec3 dpx = dFdx(vW), dpy = dFdy(vW); float dhx = dFdx(hgt), dhy = dFdy(hgt);
    vec3 r1 = cross(dpy, n), r2 = cross(n, dpx); float det = dot(dpx, r1);
    vec3 nb0 = abs(det) * n - 0.006 * sign(det) * (dhx * r1 + dhy * r2); vec3 nb = dot(nb0, nb0) > 1e-12 ? normalize(nb0) : n;
    float ndl = dot(mix(n, nb, land), uLight);
    float lit = 0.32 + 0.68 * smoothstep(-0.35, 0.9, ndl);          // night side stays readable
    float fres = pow(1.0 - max(dot(n, V), 0.0), 2.6);
    // ocean
    vec3 oc = mix(uOcean, uOceanHi, 0.35 * fres + 0.25 * smoothstep(0.0, 1.0, ndl));
    vec3 hv = normalize(uLight + V); oc += vec3(0.55, 0.6, 0.7) * 0.10 * pow(max(dot(n, hv), 0.0), 60.0);
    oc += uCoast * 0.06 * exp(-max(-sd, 0.0) / 5.0);               // shelf glow along coasts
    // land
    vec3 ld = mix(uLand, uLandHi, 0.4 + 0.2 * hgt) * lit;
    vec3 c = mix(oc * (0.55 + 0.45 * lit), ld, land);
    // focus spots: warm land tint + amber coast (e.g. India); no border lines, only coasts
    vec3 coastC = uCoast; float coastA = 0.42;
    for (int i = 0; i < 4; i++) {
      float w = uSpotCol[i].a * (1.0 - smoothstep(uSpot[i].w * 0.2, uSpot[i].w, acos(clamp(dot(n, uSpot[i].xyz), -1.0, 1.0))));
      c += uSpotCol[i].rgb * w * land * 0.12;
      coastC = mix(coastC, uSpotCol[i].rgb * 2.2, clamp(w, 0.0, 1.0)); coastA = mix(coastA, 1.0, clamp(w, 0.0, 1.0));
    }
    float line = 1.0 - smoothstep(0.35 * aa, 1.35 * aa, abs(sd));
    c += coastC * line * coastA * (0.55 + 0.45 * lit);
    // graticule every 15 degrees
    vec2 g = vec2(lat, lon) / (15.0 * PI / 180.0); vec2 gd = abs(fract(g - 0.5) - 0.5) / max(fwidth(g), vec2(1e-4));
    c += vec3(0.7, 0.75, 0.85) * uGrat * (1.0 - smoothstep(0.0, 1.2, min(gd.x, gd.y))) * (1.0 - 0.6 * land);
    // atmosphere rim (amber, stronger on the lit limb)
    c += uRim * pow(fres, 1.8) * (0.25 + 0.75 * smoothstep(-0.4, 0.8, dot(n, uLight)));
    c *= uBright;
    if (any(isnan(c))) c = vec3(0.0);
    gl_FragColor = vec4(clamp(c, 0.0, 30.0), 1.0);
  }`;
const ATMO_VERT = `varying vec3 vN; varying vec3 vW; void main() { vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`;
const ATMO_FRAG = `uniform vec3 uRim; uniform vec3 uLight; varying vec3 vN; varying vec3 vW;
  void main() { vec3 V = normalize(vW - cameraPosition);
    float b = length(cross(V, -cameraPosition));             // closest approach of the view ray to the centre
    float i = b < 1.0 ? 0.0 : exp(-(b - 1.0) / 0.018) * 0.9 + exp(-(b - 1.0) / 0.07) * 0.22;
    vec3 P = cameraPosition + V * dot(-cameraPosition, V);   // limb point the ray grazes
    float l = 0.06 + 1.3 * smoothstep(-0.3, 0.75, dot(normalize(P), uLight));
    vec3 c = uRim * i * l * 1.4; if (any(isnan(c))) c = vec3(0.0);
    gl_FragColor = vec4(clamp(c, 0.0, 30.0), 1.0); }`;

// arcs: tube with s along the path; head glow, fading tail, optional dashed "pending" state
const ARC_VERT = `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;
const ARC_FRAG = `uniform float uProg; uniform float uTail; uniform vec3 uColor; uniform float uInt; uniform float uDash; uniform float uDashOff; varying vec2 vUv;
  void main() { float s = vUv.x; if (s > uProg || s < uTail) discard;
    float head = exp(-(uProg - s) * 38.0) * step(uProg, 0.999);
    float body = 0.55 + 0.45 * smoothstep(uTail, uTail + 0.25, s);
    float dash = mix(1.0, step(0.45, fract(s * 46.0 - uDashOff)), uDash);
    gl_FragColor = vec4(clamp(uColor * uInt * (body * dash + 3.0 * head), 0.0, 30.0), 1.0); }`;

export class Arc {
  constructor(globe, a, b, { lift = 0.16, color = PAL.amber, width = 0.0042, glow = 3.2 } = {}) {
    this.g = globe; const A = dir(...a), B = dir(...b), ang = A.angleTo(B), N = 180; this.N = N;
    const q0 = new THREE.Quaternion(), q = new THREE.Quaternion().setFromUnitVectors(A, B);
    this.pts = Array.from({ length: N + 1 }, (_, i) => { const s = i / N; const p = A.clone().applyQuaternion(q0.clone().slerp(q, s));
      return p.multiplyScalar(1.003 + lift * (ang / Math.PI) * 2.2 * Math.sin(Math.PI * s)); });
    this.ground = Array.from({ length: N + 1 }, (_, i) => A.clone().applyQuaternion(q0.clone().slerp(q, i / N)).multiplyScalar(1.0015));
    const curve = new THREE.CatmullRomCurve3(this.pts), gcurve = new THREE.CatmullRomCurve3(this.ground);
    const mk = (c, w, k) => { const u = { uProg: { value: 0 }, uTail: { value: 0 }, uColor: { value: col(color) }, uInt: { value: k }, uDash: { value: 0 }, uDashOff: { value: 0 } };
      const m = new THREE.Mesh(new THREE.TubeGeometry(c, 360, w, 8, false), new THREE.ShaderMaterial({ vertexShader: ARC_VERT, fragmentShader: ARC_FRAG,
        uniforms: u, ...ADD })); globe.group.add(m); return u; };
    this.u = [mk(curve, width, glow), mk(curve, width * 3.2, 0.22), mk(gcurve, width * 0.45, 0.5)];
    this.u[2].uDash.value = 1;
    this.head = new THREE.Sprite(new THREE.SpriteMaterial({ map: globe.glowTex, color: col(PAL.amberHot), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
    this.head.scale.setScalar(0.07); globe.group.add(this.head);
  }
  point(s) { const i = clamp(s) * this.N, k = Math.floor(Math.min(i, this.N - 1)); return this.pts[k].clone().lerp(this.pts[k + 1], i - k); }
  /** prog 0..1 head position; tail 0..1 erase from start; alpha; dash (pending look) */
  set(prog, { tail = 0, alpha = 1, dash = 0, dashOff = 0 } = {}) {
    this.u.forEach((u, j) => { u.uProg.value = prog; u.uTail.value = tail; u.uDash.value = j === 2 ? 1 : dash; u.uDashOff.value = dashOff;
      u.uInt.value = [3.2, 0.22, 0.5][j] * alpha; });
    this.head.position.copy(this.point(prog)); this.head.material.opacity = alpha * (prog > 0.001 && prog < 0.999 ? 1 : 0);
  }
}

const RET_FRAG = `uniform float uAge; uniform vec3 uColor; uniform float uOn; uniform float uHollow; varying vec2 vUv;
  float ring(float r, float R, float w) { return 1.0 - smoothstep(0.0, w, abs(r - R)); }
  void main() { vec2 p = vUv * 2.0 - 1.0; float r = length(p), a = atan(p.y, p.x);
    float c = ring(r, 0.42, 0.035) * uOn;
    float ticks = step(0.86, abs(cos(a * 2.0))) * step(0.55, r) * step(r, 0.74) * uOn;     // 4 reticle ticks
    float core = (1.0 - smoothstep(0.1, 0.16, r)) * uOn * (1.0 - uHollow);
    float waves = 0.0;
    for (int k = 0; k < 2; k++) { float ph = fract(uAge / 1.7 + float(k) * 0.5); waves += ring(r, 0.42 + ph * 0.55, 0.03) * (1.0 - ph) * (1.0 - ph) * step(0.0, uAge); }
    float dashed = mix(1.0, step(0.0, sin(a * 10.0)), uHollow);
    float v = (c * dashed + 0.8 * ticks + 1.6 * core + 0.8 * waves * uOn);
    if (v < 0.003) discard;
    gl_FragColor = vec4(clamp(uColor * v * 2.2, 0.0, 30.0), 1.0); }`;

export class Marker {
  constructor(globe, at, { color = PAL.amber, size = 0.075, hollow = false, beam = 0.11 } = {}) {
    this.n = dir(...at); this.u = { uAge: { value: -1 }, uColor: { value: col(color) }, uOn: { value: 0 }, uHollow: { value: hollow ? 1 : 0 } };
    const m = this.mesh = new THREE.Mesh(new THREE.PlaneGeometry(size * 2, size * 2), new THREE.ShaderMaterial({ vertexShader: ARC_VERT, fragmentShader: RET_FRAG,
      uniforms: this.u, ...ADD }));
    m.position.copy(this.n).multiplyScalar(1.002); m.lookAt(this.n.clone().multiplyScalar(3)); globe.group.add(m);
    this.beamH = beam;
    if (beam) { const bu = this.bu = { uColor: { value: col(color) }, uOn: { value: 0 } };
      const bm = new THREE.Mesh(new THREE.CylinderGeometry(0.0016, 0.0016, beam, 8, 1, true), new THREE.ShaderMaterial({ vertexShader: ARC_VERT,
        fragmentShader: `uniform vec3 uColor; uniform float uOn; varying vec2 vUv; void main() { gl_FragColor = vec4(uColor * uOn * 2.5 * pow(1.0 - vUv.y, 1.6), 1.0); }`,
        uniforms: bu, ...ADD }));
      bm.position.copy(this.n).multiplyScalar(1 + beam / 2); bm.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), this.n); globe.group.add(bm); }
    this.top = this.n.clone().multiplyScalar(1 + (beam || 0.02));
  }
  /** on 0..1 (fade/scale-in), age = seconds since it appeared (drives the pulse waves) */
  set(on, age) { this.u.uOn.value = on; this.u.uAge.value = age; this.mesh.scale.setScalar(lerp(0.4, 1, on));
    if (this.bu) this.bu.uOn.value = on; }
}

export class Globe {
  constructor(stage, { range = 32, sdf = "vendor/library/geo/land_sdf_4k.png" } = {}) {
    this.stage = stage; this.group = new THREE.Group(); stage.scene.add(this.group);
    const tex = new THREE.TextureLoader().load(sdf);   // default loading manager: HyperFrames waits for it
    tex.colorSpace = THREE.NoColorSpace; tex.generateMipmaps = false; tex.minFilter = THREE.LinearFilter; tex.magFilter = THREE.LinearFilter;
    tex.wrapS = THREE.RepeatWrapping;
    this.light = new THREE.Vector3(-0.55, 0.55, 0.62).normalize();
    this.u = { uSdf: { value: tex }, uLight: { value: new THREE.Vector3() }, uRange: { value: range },
      uLand: { value: col(0x262a33) }, uLandHi: { value: col(0x464c58) }, uOcean: { value: col(0x0c121c) }, uOceanHi: { value: col(0x1d2a3d) },
      uCoast: { value: col(0xd9dee6) }, uRim: { value: col(PAL.amber).multiplyScalar(0.55) },
      uSpot: { value: [0, 1, 2, 3].map(() => new THREE.Vector4(0, 1, 0, 0.1)) }, uSpotCol: { value: [0, 1, 2, 3].map(() => new THREE.Vector4(0, 0, 0, 0)) },
      uGrat: { value: 0.07 }, uBright: { value: 1 } };
    this.mesh = new THREE.Mesh(new THREE.SphereGeometry(1, 192, 96), new THREE.ShaderMaterial({ vertexShader: GLOBE_VERT, fragmentShader: GLOBE_FRAG, uniforms: this.u, extensions: { derivatives: true } }));
    this.group.add(this.mesh);
    this.au = { uRim: { value: col(PAL.amber).multiplyScalar(0.75) }, uLight: { value: new THREE.Vector3() } };
    const atmo = new THREE.Mesh(new THREE.SphereGeometry(1.16, 96, 48), new THREE.ShaderMaterial({ vertexShader: ATMO_VERT, fragmentShader: ATMO_FRAG,
      uniforms: this.au, side: THREE.BackSide, ...ADD }));
    this.group.add(atmo);
    const c = document.createElement("canvas"); c.width = c.height = 64; const g = c.getContext("2d"), r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    r.addColorStop(0, "rgba(255,255,255,1)"); r.addColorStop(0.2, "rgba(255,220,180,0.6)"); r.addColorStop(1, "rgba(255,160,80,0)"); g.fillStyle = r; g.fillRect(0, 0, 64, 64);
    this.glowTex = new THREE.CanvasTexture(c);
    this._q = new THREE.Vector3();
  }
  spot(i, at, radiusDeg, color, amount) { this.u.uSpot.value[i].set(...dir(...at).toArray(), radiusDeg * Math.PI / 180);
    const c = col(color); this.u.uSpotCol.value[i].set(c.r, c.g, c.b, amount); }
  /** camera on the ray through [lat, lon] at distance dist; look target pulled toward `look` (k 0..1); screen shift in px */
  frame({ lat, lon, dist, look = null, k = 0, shiftX = 0, shiftY = 0, roll = 0 }) {
    const cam = this.stage.camera, p = dir(lat, lon).multiplyScalar(dist);
    cam.position.copy(p); cam.up.set(0, 1, 0);
    const tgt = look ? dir(...look).multiplyScalar(k) : new THREE.Vector3();
    cam.lookAt(tgt); if (roll) cam.rotateZ(roll * Math.PI / 180);
    cam.setViewOffset(this.stage.W, this.stage.H, -shiftX, -shiftY, this.stage.W, this.stage.H);
    cam.updateMatrixWorld();
    // light fixed relative to the camera: key from upper-left behind the viewer, limb glows on the left
    const L = this.light.clone().applyQuaternion(cam.quaternion).normalize();
    this.u.uLight.value.copy(L); this.au.uLight.value.copy(L);
  }
  /** screen position of a globe point and whether it faces the camera (0..1 visibility) */
  screen(p) { const s = this.stage.toScreen(p), cp = this.stage.camera.position;
    const vis = clamp((p.clone().normalize().dot(cp.clone().sub(p).normalize()) - 0.22) * 5); return { ...s, vis }; }
}
