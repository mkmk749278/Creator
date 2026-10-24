// Stick-man character demo ("The Paper Plane", 17 s). One paused GSAP timeline drives a master clock; every frame is
// redrawn from t alone (pose tracks + procedural walk with planted feet, 2-bone IK for arms and legs, look-at, face,
// scarf from the neck's analytic velocity, 12 fps line boil from a hashed frame index). No state carried between frames.
window.__stickInit = function () {   // called from index.html once the DOM exists
  const NS = "http://www.w3.org/2000/svg";
  const DUR = 17;
  const INK = "#1f2430", INK2 = "#666d7c", RED = "#d62839", YEL = "#f6c453", PAPER = "#fbf8f1", SHEET = "#fffdf6";
  const GROUND = 862;
  const lerp = (a, b, p) => a + (b - a) * p, clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const sstep = (a, b, x) => { const p = clamp((x - a) / (b - a), 0, 1); return p * p * (3 - 2 * p); };
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const rot = (x, y, deg) => { const a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a); return [x * c - y * s, x * s + y * c]; };
  const add = (p, v) => [p[0] + v[0], p[1] + v[1]];
  const f1 = (n) => Math.round(n * 10) / 10;

  // keyframe track: [[t, value, ease-of-the-segment-ending-here], ...]
  function track(keys) {
    const ks = keys.map(([t, v, e]) => ({ t, v, e: gsap.parseEase(e || "sine.inOut") }));
    return (t) => {
      if (t <= ks[0].t) return ks[0].v;
      for (let i = 1; i < ks.length; i++) if (t <= ks[i].t) { const a = ks[i - 1], b = ks[i]; return lerp(a.v, b.v, b.e((t - a.t) / (b.t - a.t))); }
      return ks[ks.length - 1].v;
    };
  }
  const track2 = (keys) => { const x = track(keys.map((k) => [k[0], k[1], k[3]])), y = track(keys.map((k) => [k[0], k[2], k[3]])); return (t) => [x(t), y(t)]; };

  // ---------------- walk: hip travel, then feet planted on the ground (no sliding) ----------------
  const X0 = -80, V = 300, TD = 2.6, TS = 3.0, S = 210, STANCE = 0.6, LIFT = 30;
  const walkX = (t) => t < TD ? X0 + V * t : t < TS ? X0 + V * TD + V * (t - TD) - V * (t - TD) ** 2 / (2 * (TS - TD)) : X0 + V * TD + V * (TS - TD) / 2;
  const walkV = (t) => t < TD ? V : t < TS ? V * (1 - (t - TD) / (TS - TD)) : 0;
  const XSTOP = walkX(99);
  function walkFoot(d, off) {
    const u = d / S + off, c = Math.floor(u), l = u - c;
    if (l < STANCE) return { x: X0 + (c + 0.3 - off) * S, lift: 0, tilt: 0 };
    const s = (l - STANCE) / (1 - STANCE), e = s * s * (3 - 2 * s);
    return { x: X0 + (c + 0.3 + e - off) * S, lift: LIFT * Math.sin(Math.PI * s), tilt: -18 * Math.sin(Math.PI * s) };
  }
  const STOP_F = walkFoot(XSTOP - X0, 0).x, STOP_B = walkFoot(XSTOP - X0, 0.5).x;

  // ---------------- pose tracks (local frame: +x forward, +y down; hands relative to the shoulder) ----------------
  const hipDX = track([[3.3, 0], [8.3, 0], [8.65, -22, "power2.out"], [8.85, 30, "power3.out"], [9.4, 26], [9.9, 0], [12.4, 0], [12.6, -10], [13.6, -10], [14.0, 0]]);
  const hipDY = track([[3.85, 0], [4.1, -10, "power2.out"], [4.45, 0], [5.38, 0], [5.5, 14, "power2.in"], [5.58, 0, "power2.out"], [5.93, 0], [6.0, 12, "power2.out"], [6.22, 0],
    [8.3, 0], [8.65, 8], [8.85, 4], [9.4, 10], [9.9, 0], [12.42, 0], [12.6, 74, "power3.out"], [13.15, 72], [13.48, 0, "power2.inOut"],
    [14.58, 0], [14.66, 10, "power3.out"], [14.9, 0], [15.25, 0], [15.42, 16, "power2.in"], [15.52, 0, "power2.out"], [15.9, 0], [15.96, 10], [16.12, 0], [16.26, 6], [16.4, 0]]);
  const jump = track([[5.55, 0], [5.75, 46, "power2.out"], [5.95, 0, "power2.in"], [15.5, 0], [15.7, 44, "power2.out"], [15.92, 0, "power2.in"], [16.0, 0], [16.13, 16, "power2.out"], [16.26, 0, "power2.in"]]);
  const lean = track([[0, 6], [3.0, 6], [3.35, 0], [3.8, -4], [4.1, -8], [4.5, 2], [4.7, 5], [5.45, 5], [5.6, -6, "power3.out"], [6.0, 2], [6.4, 7], [7.75, 7], [8.0, -3], [8.3, 0],
    [8.65, -16, "power2.out"], [8.85, 22, "power3.out"], [9.4, 16], [9.9, 0], [10.3, -7], [11.4, -4], [12.2, 0], [12.4, -8, "power3.out"], [12.6, 32, "power3.out"],
    [13.15, 30], [13.48, 0], [13.65, -4], [14.4, 0], [14.6, 0], [14.68, 10, "power3.out"], [14.9, 4], [15.25, 0], [15.45, 6], [15.7, -6], [16.2, 0], [17, 0]]);
  const tiltX = track([[4.7, 0], [4.92, -13], [5.45, -13], [5.6, 0], [14.6, 0], [14.68, 16, "power3.out"], [15.05, 4], [15.3, 0]]);
  const handR = track2([[3.0, 10, 124], [3.5, 14, 120], [3.85, 30, -30], [4.1, 40, -116, "power2.out"], [4.5, 82, 18, "power2.inOut"], [5.45, 82, 16], [5.6, 86, -6, "power3.out"], [6.3, 72, 24],
    [7.75, 72, 24], [7.95, 78, -40, "power2.out"], [8.3, 78, -40], [8.65, -64, -90, "power2.out"], [8.75, 96, -62, "power2.in"], [8.95, 112, 36, "power2.out"], [9.4, 70, 100], [9.85, 12, 122],
    [10.0, 12, 122], [10.25, 84, -58, "power2.out"], [10.9, 86, -62], [11.3, 12, 122], [12.32, 12, 122], [12.42, 40, 30, "power2.out"], [12.6, 26, -112, "power3.out"], [13.15, 24, -108],
    [13.45, 40, 20], [13.6, 14, -76], [13.95, 52, -74], [14.1, 40, -40], [14.4, 12, 122], [14.6, 12, 122], [14.75, 34, 50, "power3.out"], [15.1, 14, 118], [15.32, 14, 116],
    [15.55, 70, -84, "back.out(1.7)"], [16.4, 66, -80], [17, 62, -74]]);
  const handL = track2([[3.0, -8, 124], [3.5, -6, 124], [4.1, -14, 118], [4.5, -10, 122], [4.62, -10, 120], [4.85, -18, -98, "power2.out"], [5.4, -18, -96], [5.6, -40, -50, "power3.out"],
    [6.25, 20, 40], [7.75, 20, 40], [7.95, -20, 110], [8.3, -20, 110], [8.65, 84, -36, "power2.out"], [8.78, 60, 24], [8.95, -40, 90], [9.4, -30, 110], [9.9, -8, 124],
    [12.32, -8, 124], [12.42, -10, 36, "power2.out"], [12.6, -12, -110, "power3.out"], [13.15, -12, -104], [13.45, -10, 100], [14.4, -8, 124], [14.6, -8, 124], [14.75, -26, 56, "power3.out"],
    [15.1, -8, 120], [15.32, -8, 118], [15.55, -66, -84, "back.out(1.7)"], [16.4, -62, -80], [17, -58, -74]]);
  const walkW = track([[3.0, 1], [3.35, 0]]);
  const foldW = track([[6.22, 0], [6.4, 1], [7.62, 1], [7.78, 0]]);
  const sep = track([[6.3, 36], [6.5, 12], [6.65, 38], [6.85, 12], [7.0, 36], [7.2, 10], [7.35, 30], [7.55, 8], [7.7, 16]]);
  const elbowOut = track([[12.36, 0], [12.5, 1], [13.35, 1], [13.5, 0], [15.3, 0], [15.42, 1], [17, 1]]);
  const footFdx = track([[8.7, 0], [8.9, 40, "power2.out"], [9.6, 40], [9.9, 0]]);
  const footFlift = track([[8.7, 0], [8.8, 18], [8.9, 0, "power2.in"], [9.6, 0], [9.75, 14], [9.9, 0]]);
  const footBlift = track([[8.82, 0], [8.95, 16], [9.4, 16], [9.7, 0]]);

  // face
  const smile = track([[0, 0.7], [3.0, 0.3], [3.4, 0.1], [4.1, 0.4], [4.6, -0.1], [5.5, -0.25], [5.6, 1, "power3.out"], [6.4, 0.6], [7.8, 0.6], [7.95, 1], [8.3, 0.2], [8.6, -0.35],
    [8.9, 0.6], [9.9, 0.5], [11.4, 0.5], [12.3, 0.4], [12.4, -0.9, "power3.out"], [13.4, -0.6], [13.6, 0.5], [14.4, 0.6], [14.62, -0.5, "power3.out"], [15.2, -0.2], [15.42, 1], [17, 1]]);
  const mopen = track([[0, 0.38], [2.85, 0.38], [3.1, 0], [3.95, 0], [4.1, 0.28], [4.35, 0], [5.55, 0], [5.62, 0.75, "power3.out"], [6.1, 0.2], [6.4, 0], [8.65, 0], [8.8, 0.5], [9.2, 0.15],
    [10.0, 0.15], [10.12, 0.55], [10.8, 0.5], [11.2, 0.1], [12.32, 0.1], [12.42, 0.85, "power3.out"], [13.4, 0.6], [13.6, 0.15], [14.4, 0], [14.62, 0.55, "power3.out"], [15.0, 0.2],
    [15.25, 0.2], [15.42, 0.95], [17, 0.85]]);
  const mwide = track([[0, 0.42], [2.85, 0.42], [3.1, 1], [10.0, 1], [10.12, 0.5], [10.85, 0.5], [11.2, 1], [14.6, 1], [14.62, 0.6], [15.0, 0.7], [15.3, 1.1], [17, 1.1]]);
  const brow = track([[0, 2], [2.8, 2], [3.0, 5], [4.6, 0], [4.8, -2], [5.5, -2], [5.6, 9, "power3.out"], [6.4, 3], [8.5, -4], [8.9, 3], [10.1, 7], [11, 3], [12.3, 3],
    [12.42, 10, "power3.out"], [13.4, 8], [13.6, 3], [14.58, 2], [14.64, 11, "power3.out"], [15.0, 5], [15.4, 6], [17, 6]]);
  const browT = track([[4.7, 0], [4.85, 18], [5.5, 18], [5.6, 0], [8.4, 0], [8.55, -14], [8.9, 0], [12.32, 0], [12.42, 22], [13.4, 22], [13.6, 10], [14.0, 0], [14.6, 0], [14.66, 16], [15.2, 0]]);
  const eyeS = track([[5.55, 1], [5.62, 1.3, "power3.out"], [6.2, 1], [12.34, 1], [12.44, 1.45, "power3.out"], [13.3, 1.4], [13.6, 1], [14.58, 1], [14.64, 1.4, "power3.out"], [15.0, 1.15], [15.3, 1]]);
  const happy = track([[13.62, 0], [13.68, 1], [13.98, 1], [14.04, 0], [15.36, 0], [15.44, 1], [17, 1]]);
  const front = track([[15.2, 0], [15.5, 1], [17, 1]]);
  const BLINKS = [1.7, 4.62, 6.36, 7.98, 9.95, 11.55, 14.32];
  const blink = (t) => BLINKS.reduce((m, b) => Math.max(m, 1 - Math.abs(t - b) / 0.075), 0);

  // camera (world point at screen centre, zoom) + bonk shake
  const camX = track([[0, 560], [3.0, 770], [5.6, 790], [8.3, 800], [8.75, 820], [9.6, 1150], [10.3, 1240], [11.2, 1100], [12.1, 820], [14.6, 790], [17, 780]]);
  const camY = track([[0, 640], [3.0, 630], [5.6, 600], [8.3, 630], [9.6, 470], [10.3, 420], [11.2, 500], [12.1, 640], [17, 630]]);
  const camZ = track([[0, 1.3], [3.0, 1.38], [4.6, 1.45], [5.58, 1.45], [5.75, 1.58, "power3.out"], [8.3, 1.45], [8.75, 1.38], [9.6, 0.92], [10.3, 0.86], [11.2, 0.95],
    [12.1, 1.3], [14.6, 1.36], [15.3, 1.36], [17, 1.5]]);

  // ---------------- 2-bone IK ----------------
  function ik(a, t, l1, l2, pref) {
    let dx = t[0] - a[0], dy = t[1] - a[1], d = Math.hypot(dx, dy) || 1e-3;
    const dc = clamp(d, Math.abs(l1 - l2) + 1, l1 + l2 - 0.5);
    const end = [a[0] + dx / d * dc, a[1] + dy / d * dc];
    const base = Math.atan2(dy, dx), ang = Math.acos(clamp((l1 * l1 + dc * dc - l2 * l2) / (2 * l1 * dc), -1, 1));
    const c1 = [a[0] + l1 * Math.cos(base + ang), a[1] + l1 * Math.sin(base + ang)], c2 = [a[0] + l1 * Math.cos(base - ang), a[1] + l1 * Math.sin(base - ang)];
    const dot = (c) => (c[0] - a[0]) * pref[0] + (c[1] - a[1]) * pref[1];
    return { joint: dot(c1) >= dot(c2) ? c1 : c2, end };
  }

  // ---------------- full pose at time t (pure) ----------------
  function pose(t) {
    const sp = walkV(t), d = walkX(t) - X0, u = d / S, jp = jump(t);
    const jv = (jump(t + 0.01) - jump(t - 0.01)) / 0.02;
    const hx = walkX(t) + hipDX(t);
    const hy = GROUND - 162 + 7 * (sp / V) * Math.cos(4 * Math.PI * u) + hipDY(t) - jp;
    let F, B;
    if (t < TS) { F = walkFoot(d, 0); B = walkFoot(d, 0.5); }
    else {
      const a = sstep(3.0, 3.3, t), b = sstep(3.12, 3.42, t);
      F = { x: lerp(STOP_F, XSTOP + 30, a), lift: 12 * Math.sin(Math.PI * a), tilt: -10 * Math.sin(Math.PI * a) };
      B = { x: lerp(STOP_B, XSTOP - 24, b), lift: 10 * Math.sin(Math.PI * b), tilt: -8 * Math.sin(Math.PI * b) };
      F.x += footFdx(t); F.lift += footFlift(t); B.lift += footBlift(t);
      if (footBlift(t) > 0) B.tilt = 24 * footBlift(t) / 16;   // heel up on the follow-through
    }
    const fy = (ft) => GROUND - 4 - ft.lift - jp;
    const ln = lean(t) + (t < TS ? 6 * (sp / V) - 6 : 0);
    const stretch = 1 + 0.07 * clamp(Math.abs(jv) / 420, 0, 1);
    const hip = [hx, hy], tl = 128 * stretch;
    const chest = add(hip, rot(0, -tl, ln)), shoulder = add(hip, rot(0, -(tl - 12), ln)), neck = add(hip, rot(0, -tl - 4, ln));
    // hands
    const sw = 28 * (sp / V) * Math.cos(2 * Math.PI * u);
    const wR = rot(0, 122, sw), wL = rot(0, 122, -sw);
    let hr = lerp2(handR(t), [wR[0] + 6, wR[1]], walkW(t)), hl = lerp2(handL(t), [wL[0] - 6, wL[1]], walkW(t));
    const fw = foldW(t);
    if (fw > 0) { const s = sep(t); hr = lerp2(hr, [72 + s, 24], fw); hl = lerp2(hl, [72 - s, 26], fw); }
    if (t > 4.85 && t < 5.42) hl = [hl[0] + 5 * Math.sin(2 * Math.PI * 9 * t), hl[1] + 3 * Math.cos(2 * Math.PI * 9 * t)];   // head scratch
    const eo = elbowOut(t);
    const armR = ik(shoulder, add(shoulder, rot(hr[0], hr[1], ln)), 68, 64, [lerp(-0.35, 1, eo), lerp(1, -0.2, eo)]);
    const armL = ik(add(shoulder, [-3, 2]), add(add(shoulder, [-3, 2]), rot(hl[0], hl[1], ln)), 68, 64, [lerp(-0.35, -1, eo), lerp(1, -0.2, eo)]);
    const legF = ik(add(hip, [3, 0]), [F.x, fy(F)], 86, 84, [1, 0.05]);
    const legB = ik(add(hip, [-3, 0]), [B.x, fy(B)], 86, 84, [1, 0.05]);
    // look-at target, then the head
    const lk = lookAt(t, neck, { armR, shoulder, ln });
    const hc0 = add(neck, rot(0, -48, ln));
    const ang = Math.atan2(lk.y - hc0[1], Math.max(60, Math.abs(lk.x - hc0[0]))) * 180 / Math.PI;
    const tilt = ln * 0.3 + clamp(ang * 0.45, -26, 18) * lk.w + tiltX(t);
    const head = add(neck, rot(0, -48, ln * 0.6 + tilt * 0.5));
    return { t, hip, chest, shoulder, neck, head, tilt, ln, armR, armL, legF, legB, F, B, jp, lk, sh2: add(shoulder, [-3, 2]) };
  }
  const lerp2 = (a, b, p) => [lerp(a[0], b[0], p), lerp(a[1], b[1], p)];

  // ---------------- props: paper, plane ----------------
  const PW = 88, PH = 112;
  let CATCH, RELEASE, IMPACT;   // filled at init from the pose itself
  const paperRot = track([[4.1, 8], [4.5, -4], [5.6, 4], [6.3, 0]]);
  const FOLD = [   // 6-point outlines (paper-local), sheet -> corners folded -> dart -> plane nose up
    [[-44, -56], [0, -56], [44, -56], [44, 56], [0, 56], [-44, 56]],
    [[-44, -14], [0, -58], [44, -14], [44, 56], [0, 56], [-44, 56]],
    [[-21, -24], [0, -60], [21, -24], [15, 56], [0, 56], [-15, 56]],
    [[-2, -58], [0, -60], [2, -58], [16, 36], [-4, 40], [-22, 46]],
  ];
  const FSTEP = [6.45, 6.8, 7.15, 7.5], FLEN = 0.2;
  function foldShape(t) {
    let k = 0, p = 0;
    for (let i = 0; i < 3; i++) if (t >= FSTEP[i]) { k = i; p = clamp((t - FSTEP[i]) / FLEN, 0, 1); }
    const e = p * p * (3 - 2 * p), A = FOLD[k], Bk = FOLD[Math.min(3, k + 1)];
    return { pts: A.map((a, i) => [lerp(a[0], Bk[i][0], e), lerp(a[1], Bk[i][1], e)]), sx: 1 - 0.35 * Math.sin(Math.PI * p), crease: t > FSTEP[0] + FLEN * 0.5 };
  }
  const planeHeld = track([[7.62, -80], [7.95, -8, "back.out(1.5)"], [8.3, -8], [8.65, -32, "power2.out"], [8.75, -22]]);
  let FLIGHT;
  function cr(p0, p1, p2, p3, s) {   // Catmull-Rom
    const s2 = s * s, s3 = s2 * s;
    return [0, 1].map((i) => 0.5 * ((2 * p1[i]) + (-p0[i] + p2[i]) * s + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * s2 + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * s3));
  }
  function flightAt(t) {
    const K = FLIGHT;
    if (t <= K[0][0]) return [K[0][1], K[0][2]];
    for (let i = 0; i < K.length - 1; i++) if (t <= K[i + 1][0]) {
      const s = (t - K[i][0]) / (K[i + 1][0] - K[i][0]);
      const g = (j) => { const k = K[clamp(j, 0, K.length - 1)]; return [k[1], k[2]]; };
      return cr(g(i - 1), g(i), g(i + 1), g(i + 2), s);
    }
    const k = K[K.length - 1]; return [k[1], k[2]];
  }
  const T_REL = 8.75, T_HIT = 14.6;

  function lookAt(t, neck, P) {
    const fwd = { x: neck[0] + 500, y: neck[1] + 30, w: 0.3 };
    if (t < 2.55) return fwd;
    if (t <= T_REL) { const pc = paperCenter(t, P); const w = sstep(2.55, 2.9, t); return { x: lerp(fwd.x, pc[0], w), y: lerp(fwd.y, pc[1], w), w: lerp(0.3, 1, w) }; }
    if (t < 15.2) { const pp = t < T_HIT ? flightAt(t) : IMPACT.c; return { x: pp[0], y: pp[1], w: 1 }; }
    return { x: neck[0] + 300, y: neck[1] - 60, w: lerp(1, 0, sstep(15.2, 15.45, t)) };
  }
  function paperCenter(t, P) {
    if (t < 4.1) {
      const t0 = 1.9, s = clamp((t - t0) / (4.1 - t0), 0, 1), om = 2 * Math.PI * 0.72;
      const amp = 90 * (1 - 0.75 * s);
      return [CATCH[0] + amp * Math.sin(om * (4.1 - t)), lerp(-170, CATCH[1], 1 - (1 - s) ** 1.25)];
    }
    const p = P || poseCache(t);
    if (t < 6.25) return add(p.armR.end, [6, -44]);
    return add(p.shoulder, rot(72, -12, p.ln));
  }
  function planeOnHead(t) {
    const p = poseCache(t), dt = t - T_HIT;
    const wob = 14 * Math.exp(-dt * 5) * Math.sin(dt * 34);
    const off = rot(IMPACT.off[0], IMPACT.off[1], p.tilt - IMPACT.tilt);
    return { c: add(p.head, off), a: IMPACT.ang + (p.tilt - IMPACT.tilt) + wob };
  }
  const cache = new Map();
  function poseCache(t) { const k = Math.round(t * 1000); if (!cache.has(k)) { if (cache.size > 400) cache.clear(); cache.set(k, pose(t)); } return cache.get(k); }

  // ---------------- DOM ----------------
  const svg = document.getElementById("s");
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const rc = rough.svg(svg);
  const defs = el("defs", {}, svg);
  const grad = el("radialGradient", { id: "glow" }, defs);
  el("stop", { offset: "0%", "stop-color": "#ffe9a3", "stop-opacity": "0.95" }, grad);
  el("stop", { offset: "55%", "stop-color": "#ffd666", "stop-opacity": "0.35" }, grad);
  el("stop", { offset: "100%", "stop-color": "#ffd666", "stop-opacity": "0" }, grad);
  const far = el("g", {}, svg), mid = el("g", {}, svg), world = el("g", {}, svg);
  const R = (seed, o = {}) => Object.assign({ seed, roughness: 1.3, bowing: 1.1, stroke: INK, strokeWidth: 3 }, o);
  // boiled background: 3 drawings of each piece, one shown per 12 fps frame
  const boils = [];
  function boiled(parent, draw) { const gs = [0, 1, 2].map((v) => { const g = el("g", {}, parent); draw(g, v); return g; }); boils.push(gs); }
  boiled(far, (g, v) => {   // sun + clouds (far layer)
    g.appendChild(rc.circle(2060, 150, 150, R(10 + v, { fill: YEL, fillStyle: "hachure", hachureGap: 9, fillWeight: 2, stroke: "#c9902a" })));
    for (const [cx, cy, s] of [[260, 260, 1], [1180, 200, 1.25], [1960, 380, 0.9], [-420, 340, 1.1], [2660, 240, 1]]) {
      const pts = [[-90, 20], [-70, -18], [-30, -40], [10, -46], [50, -30], [86, -8], [96, 22]].map(([x, y]) => [cx + x * s, cy + y * s]);
      const d = `M ${pts[0][0]} ${pts[0][1]} ` + pts.slice(1).map((p, i) => `Q ${(pts[i][0] + p[0]) / 2} ${Math.min(pts[i][1], p[1]) - 26 * s} ${p[0]} ${p[1]}`).join(" ") + ` Z`;
      g.appendChild(rc.path(d, R(30 + v * 7 + cx, { fill: "#ffffff", fillStyle: "solid", stroke: "#8c93a3", strokeWidth: 2.4 })));
    }
  });
  boiled(mid, (g, v) => {   // distant hills
    g.appendChild(rc.path("M -900 790 Q -500 640 -100 760 T 700 740 T 1500 720 T 2300 750 T 3200 730 L 3200 870 L -900 870 Z",
      R(50 + v, { fill: "#d9e3d1", fillStyle: "hachure", hachureAngle: -30, hachureGap: 14, fillWeight: 1.4, stroke: "#9aab92", strokeWidth: 2.2 })));
  });
  boiled(world, (g, v) => {   // tree, ground, grass, pebbles
    g.appendChild(rc.path("M 1700 862 C 1704 780 1696 720 1708 640 L 1736 640 C 1744 720 1738 790 1746 862 Z", R(70 + v, { fill: "#a7754b", fillStyle: "hachure", hachureGap: 6, stroke: INK })));
    for (const [x, y, r] of [[1660, 590, 150], [1790, 580, 160], [1720, 500, 170], [1640, 510, 110], [1810, 500, 120]])
      g.appendChild(rc.circle(x, y, r, R(80 + v * 5 + x, { fill: "#7cbf6e", fillStyle: "hachure", hachureGap: 8, fillWeight: 1.8, stroke: "#2f5d34", strokeWidth: 2.6 })));
    g.appendChild(rc.line(-900, GROUND, 3200, GROUND + 4, R(90 + v, { strokeWidth: 3.6, roughness: 1.6 })));
    for (let i = 0; i < 26; i++) {
      const x = -700 + i * 150 + (hash(i) - 0.5) * 80;
      if (x > 1650 && x < 1800) continue;
      g.appendChild(rc.linearPath([[x - 10, GROUND], [x - 4, GROUND - 16 - hash(i + 9) * 8], [x, GROUND], [x + 6, GROUND - 20 - hash(i + 3) * 8], [x + 12, GROUND]], R(200 + i * 3 + v, { strokeWidth: 2.4, stroke: "#3c6e46" })));
    }
    for (let i = 0; i < 12; i++) { const x = -500 + i * 300 + hash(i + 40) * 120; g.appendChild(rc.ellipse(x, GROUND + 22 + hash(i) * 30, 18, 9, R(300 + i + v, { strokeWidth: 1.8, stroke: INK2 }))); }
  });

  const shadow = el("ellipse", { cy: GROUND + 4, fill: INK, opacity: 0.16 }, world);
  const trail = [0, 1, 2, 3].map((i) => el("path", { fill: "none", stroke: INK2, "stroke-width": 3, "stroke-dasharray": "10 12", "stroke-linecap": "round", opacity: 0.15 * (i + 1) }, world));
  const fig = el("g", { "stroke-linecap": "round", "stroke-linejoin": "round", fill: "none" }, world);
  const legBp = el("path", { stroke: INK2, "stroke-width": 9 }, fig);
  const armLp = el("path", { stroke: INK2, "stroke-width": 9 }, fig);
  const handLp = el("circle", { r: 6.5, fill: INK2 }, fig);
  const scarfB = el("path", { stroke: "#a51f2d", "stroke-width": 9 }, fig);
  const scarfA = el("path", { stroke: RED, "stroke-width": 11 }, fig);
  const torso = el("path", { stroke: INK, "stroke-width": 10 }, fig);
  const legFp = el("path", { stroke: INK, "stroke-width": 9.5 }, fig);
  const knot = el("ellipse", { rx: 17, ry: 8, fill: RED, stroke: "#a51f2d", "stroke-width": 2 }, fig);
  const headG = el("g", {}, fig);
  el("circle", { r: 44, fill: PAPER, stroke: INK, "stroke-width": 8.5 }, headG);
  const cheek = [el("ellipse", { rx: 9, ry: 5, fill: "#f4a7a0", opacity: 0 }, headG), el("ellipse", { rx: 9, ry: 5, fill: "#f4a7a0", opacity: 0 }, headG)];
  const eyes = [el("ellipse", { fill: INK }, headG), el("ellipse", { fill: INK }, headG)];
  const hEyes = [el("path", { stroke: INK, "stroke-width": 4.5 }, headG), el("path", { stroke: INK, "stroke-width": 4.5 }, headG)];
  const brows = [el("path", { stroke: INK, "stroke-width": 4.5 }, headG), el("path", { stroke: INK, "stroke-width": 4.5 }, headG)];
  const mouth = el("path", { stroke: INK, "stroke-width": 4.5 }, headG);
  const tongue = el("path", { fill: "#e46a6a", stroke: "none" }, headG);
  const paperG = el("g", {}, world);
  const paperPoly = el("polygon", { fill: SHEET, stroke: INK, "stroke-width": 3.2, "stroke-linejoin": "round" }, paperG);
  const paperLines = [0, 1, 2].map((i) => el("line", { x1: -28, x2: 28 - i * 10, y1: -26 + i * 18, y2: -26 + i * 18, stroke: "#9aa6c4", "stroke-width": 3, "stroke-linecap": "round" }, paperG));
  const crease = el("line", { x1: 0, y1: -58, x2: 0, y2: 56, stroke: "#b9b2a2", "stroke-width": 2 }, paperG);
  const armRp = el("path", { stroke: INK, "stroke-width": 9.5, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, fig.parentNode);
  const handRp = el("circle", { r: 7, fill: INK }, fig.parentNode);
  const planeG = el("g", { "stroke-linejoin": "round" }, world);
  el("polygon", { points: "40,0 -30,-4 -26,12", fill: "#ece6d6", stroke: INK, "stroke-width": 2.6 }, planeG);
  el("polygon", { points: "40,0 -36,-18 -30,-4", fill: SHEET, stroke: INK, "stroke-width": 2.6 }, planeG);
  el("line", { x1: 40, y1: 0, x2: -30, y2: -4, stroke: INK, "stroke-width": 2 }, planeG);
  const fx = el("g", { "stroke-linecap": "round", "stroke-linejoin": "round" }, world);
  const smear = [0, 1, 2].map((i) => el("path", { fill: "none", stroke: i ? INK2 : "#c3c7d0", "stroke-width": i ? 3 : 22, opacity: 0 }, fx));
  const notes = [0, 1, 2, 3, 4, 5].map((i) => { const g = el("g", { opacity: 0 }, fx); el("ellipse", { cx: 0, cy: 0, rx: 9, ry: 7, transform: "rotate(-20)", fill: INK }, g);
    el("path", { d: "M 8 -2 L 8 -34" + (i % 2 ? " Q 18 -28 22 -16" : " L 26 -38 L 26 -8"), stroke: INK, "stroke-width": 3.5, fill: "none" }, g);
    if (i % 2 === 0) el("ellipse", { cx: 18, cy: -6, rx: 9, ry: 7, transform: "rotate(-20 18 -6)", fill: INK }, g); return g; });
  const qG = el("g", { opacity: 0 }, fx); const qT = el("text", { class: "lbl", "font-size": 92, fill: INK, "text-anchor": "middle", stroke: PAPER, "stroke-width": 8, "paint-order": "stroke" }, qG); qT.textContent = "?";
  const xG = el("g", { opacity: 0 }, fx); const xT = el("text", { class: "lbl", "font-size": 96, fill: RED, "text-anchor": "middle", stroke: PAPER, "stroke-width": 8, "paint-order": "stroke" }, xG); xT.textContent = "!";
  const bulbG = el("g", { opacity: 0 }, fx);
  el("circle", { r: 130, fill: "url(#glow)" }, bulbG);
  const rays = el("g", {}, bulbG);
  for (let i = 0; i < 8; i++) { const a = i * 45 - 90; if (a === 90) continue; const [x1, y1] = rot(0, -62, a), [x2, y2] = rot(0, -92, a);
    el("line", { x1, y1: y1 - 8, x2, y2: y2 - 8, stroke: "#d29a17", "stroke-width": 5, "stroke-linecap": "round" }, rays); }
  bulbG.appendChild(rc.path("M -26 18 C -46 -4 -40 -48 0 -50 C 40 -48 46 -4 26 18 L 22 30 L -22 30 Z", R(500, { fill: "#ffe27a", fillStyle: "solid", strokeWidth: 3.4 })));
  bulbG.appendChild(rc.rectangle(-20, 30, 40, 22, R(501, { fill: "#b8bcc6", fillStyle: "solid", strokeWidth: 3 })));
  bulbG.appendChild(rc.linearPath([[-10, 14], [-4, -6], [4, 6], [10, -14]], R(502, { stroke: "#c06a00", strokeWidth: 2.6 })));
  const spark = el("path", { d: "M 0 -22 L 5 -5 L 22 0 L 5 5 L 0 22 L -5 5 L -22 0 L -5 -5 Z", fill: YEL, stroke: INK, "stroke-width": 2.5, opacity: 0 }, fx);
  const drop = el("path", { d: "M 0 -16 C 8 -4 12 4 12 9 C 12 16 6 20 0 20 C -6 20 -12 16 -12 9 C -12 4 -8 -4 0 -16 Z", fill: "#7cc4ff", stroke: INK, "stroke-width": 2.5, opacity: 0 }, fx);
  const stars = [0, 1, 2].map(() => el("path", { d: "M 0 -14 L 4 -4 L 14 -4 L 6 3 L 9 13 L 0 7 L -9 13 L -6 3 L -14 -4 L -4 -4 Z", fill: YEL, stroke: INK, "stroke-width": 2.2, opacity: 0 }, fx));
  const burst = [0, 1, 2, 3, 4, 5].map(() => el("line", { stroke: INK, "stroke-width": 4, opacity: 0 }, fx));

  // ---------------- drawing helpers ----------------
  const J = (t, id, amp = 1.2) => { const fr = Math.floor(t * 12); return [(hash(fr * 13.1 + id) - 0.5) * 2 * amp, (hash(fr * 7.7 + id + 50) - 0.5) * 2 * amp]; };
  const jit = (p, t, id, amp) => add(p, J(t, id, amp));
  const limb = (a, b, c) => { const k = [2 * b[0] - (a[0] + c[0]) / 2, 2 * b[1] - (a[1] + c[1]) / 2]; return `M ${f1(a[0])} ${f1(a[1])} Q ${f1(k[0])} ${f1(k[1])} ${f1(c[0])} ${f1(c[1])}`; };
  const foot = (ankle, tilt) => { const [dx, dy] = rot(20, 0, tilt); return ` M ${f1(ankle[0] - 3)} ${f1(ankle[1])} L ${f1(ankle[0] + dx)} ${f1(ankle[1] + dy)}`; };
  const smoothPath = (pts) => { let d = `M ${f1(pts[0][0])} ${f1(pts[0][1])}`; for (let i = 1; i < pts.length - 1; i++) { const m = [(pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2]; d += ` Q ${f1(pts[i][0])} ${f1(pts[i][1])} ${f1(m[0])} ${f1(m[1])}`; } const l = pts[pts.length - 1]; return d + ` L ${f1(l[0])} ${f1(l[1])}`; };
  const show = (e, o) => e.setAttribute("opacity", f1(clamp(o, 0, 1) * 100) / 100);
  const place = (e, x, y, r = 0, s = 1, sy = s) => e.setAttribute("transform", `translate(${f1(x)} ${f1(y)}) rotate(${f1(r)}) scale(${Math.round(s * 1000) / 1000} ${Math.round(sy * 1000) / 1000})`);
  const life = (t, a, b, fi = 0.12, fo = 0.15) => Math.min(sstep(a, a + fi, t), 1 - sstep(b - fo, b, t));

  function render(t) {
    const fr = Math.floor(t * 12);
    // camera with parallax layers
    let cx = camX(t), cy = camY(t), z = camZ(t);
    if (t > T_HIT) { const d = t - T_HIT, k = 10 * Math.exp(-d * 7); cx += k * Math.sin(d * 83); cy += k * Math.cos(d * 71); }
    const camT = (p) => `translate(960 540) scale(${Math.round((1 + (z - 1) * p) * 10000) / 10000}) translate(${f1(-(960 + (cx - 960) * p))} ${f1(-(540 + (cy - 540) * p))})`;
    far.setAttribute("transform", camT(0.35) + ` translate(${f1(t * 9)} 0)`); mid.setAttribute("transform", camT(0.7)); world.setAttribute("transform", camT(1));
    boils.forEach((gs) => gs.forEach((g, i) => g.setAttribute("display", i === fr % 3 ? "inline" : "none")));
    document.getElementById("paper").style.transform = `translate(${f1((hash(fr) - 0.5) * 3)}px, ${f1((hash(fr + 99) - 0.5) * 3)}px)`;

    const P = poseCache(t), Pp = poseCache(Math.max(0, t - 1 / 30));
    // shadow
    shadow.setAttribute("cx", f1(P.hip[0] + 4)); shadow.setAttribute("rx", f1(72 - P.jp * 0.5)); shadow.setAttribute("ry", f1(9 - P.jp * 0.05));
    // legs + arms with boil
    const kF = jit(P.legF.joint, t, 1), aF = jit(P.legF.end, t, 2), kB = jit(P.legB.joint, t, 3), aB = jit(P.legB.end, t, 4);
    legFp.setAttribute("d", limb(P.hip, kF, aF) + foot(aF, P.F.tilt));
    legBp.setAttribute("d", limb(P.hip, kB, aB) + foot(aB, P.B.tilt));
    const eR = jit(P.armR.joint, t, 5), hR = jit(P.armR.end, t, 6), eL = jit(P.armL.joint, t, 7), hL = jit(P.armL.end, t, 8);
    armRp.setAttribute("d", limb(P.shoulder, eR, hR)); handRp.setAttribute("cx", f1(hR[0])); handRp.setAttribute("cy", f1(hR[1]));
    armLp.setAttribute("d", limb(P.sh2, eL, hL)); handLp.setAttribute("cx", f1(hL[0])); handLp.setAttribute("cy", f1(hL[1]));
    const nk = jit(P.neck, t, 9, 0.8);
    torso.setAttribute("d", `M ${f1(P.hip[0])} ${f1(P.hip[1])} Q ${f1((P.hip[0] + nk[0]) / 2 - P.ln * 0.25)} ${f1((P.hip[1] + nk[1]) / 2)} ${f1(nk[0])} ${f1(nk[1])}`);
    // scarf: tails trail against the neck's velocity, plus a breeze
    const vx = (P.neck[0] - Pp.neck[0]) * 30, vy = (P.neck[1] - Pp.neck[1]) * 30;
    const base = add(P.neck, rot(-6, 8, P.ln));
    const tail = (len, ph, n) => { const pts = [base]; let dir = [-(55 + vx * 0.16), 22 - vy * 0.12]; const m = Math.hypot(...dir); dir = [dir[0] / m, dir[1] / m];
      for (let i = 1; i <= n; i++) { const w = Math.sin(t * 8.5 - i * 1.1 + ph) * i * 2.4; pts.push([base[0] + dir[0] * len * i / n - dir[1] * w, base[1] + dir[1] * len * i / n + dir[0] * w + i * i * 0.6]); } return smoothPath(pts); };
    scarfA.setAttribute("d", tail(64, 0, 5)); scarfB.setAttribute("d", tail(46, 1.7, 4));
    knot.setAttribute("transform", `translate(${f1(P.neck[0])} ${f1(P.neck[1] + 4)}) rotate(${f1(P.ln)})`);
    // head + face
    const hd = jit(P.head, t, 10, 0.7);
    headG.setAttribute("transform", `translate(${f1(hd[0])} ${f1(hd[1])}) rotate(${f1(P.tilt)})`);
    const fo = 13 * (1 - front(t)), lk = P.lk;
    let ex = lk.x - P.head[0], ey = lk.y - P.head[1]; const em = Math.hypot(ex, ey) || 1; ex = ex / em * 7 * lk.w; ey = ey / em * 6 * lk.w;
    const es = eyeS(t), bl = blink(t), hp = happy(t);
    [[-12, 0], [13, 1]].forEach(([x0, i]) => {
      const x = fo + x0 + ex, y = -6 + ey;
      eyes[i].setAttribute("cx", f1(x)); eyes[i].setAttribute("cy", f1(y)); eyes[i].setAttribute("rx", f1(5 * es)); eyes[i].setAttribute("ry", f1(Math.max(0.6, 7.5 * es * (1 - bl) * (1 - hp))));
      show(eyes[i], 1 - hp); hEyes[i].setAttribute("d", `M ${f1(x - 7)} ${f1(y + 2)} Q ${f1(x)} ${f1(y - 9)} ${f1(x + 7)} ${f1(y + 2)}`); show(hEyes[i], hp);
      const by = y - 15 - brow(t), bt = browT(t) * (i ? 1 : -1);   // + lifts the inner ends (worried)
      const [dx, dy] = rot(8, 0, bt);
      brows[i].setAttribute("d", `M ${f1(x - dx)} ${f1(by - dy)} L ${f1(x + dx)} ${f1(by + dy)}`);
      cheek[i].setAttribute("cx", f1(x + (i ? 6 : -6))); cheek[i].setAttribute("cy", f1(y + 16)); show(cheek[i], 0.55 * Math.max(0, smile(t) - 0.5) * 2);
    });
    const sm = smile(t), op = mopen(t), w = 13 * mwide(t), mx = fo + 2 + ex * 0.4, my = 17;
    const cyc = my - sm * 6, mid1 = my + sm * 5;
    if (op > 0.05) {
      const low = mid1 + op * 22 * (0.6 + 0.4 * mwide(t));
      mouth.setAttribute("d", `M ${f1(mx - w)} ${f1(cyc)} Q ${f1(mx)} ${f1(2 * mid1 - (cyc + cyc) / 2 - (sm > 0 ? 0 : 0))} ${f1(mx + w)} ${f1(cyc)} Q ${f1(mx)} ${f1(2 * low - cyc)} ${f1(mx - w)} ${f1(cyc)} Z`);
      mouth.setAttribute("fill", "#3a1f24");
      tongue.setAttribute("d", `M ${f1(mx - w * 0.5)} ${f1(low - 1)} Q ${f1(mx)} ${f1(low - op * 9)} ${f1(mx + w * 0.5)} ${f1(low - 1)} Q ${f1(mx)} ${f1(low + 3)} ${f1(mx - w * 0.5)} ${f1(low - 1)} Z`); show(tongue, op > 0.3 ? 1 : 0);
    } else {
      mouth.setAttribute("d", `M ${f1(mx - w)} ${f1(cyc)} Q ${f1(mx)} ${f1(2 * mid1 - cyc)} ${f1(mx + w)} ${f1(cyc)}`); mouth.setAttribute("fill", "none"); show(tongue, 0);
    }

    // paper
    if (t < 7.66) {
      const pc = paperCenter(t);
      if (t < 4.1) {
        const om = 2 * Math.PI * 0.72, ph = om * (4.1 - t), a = 1 - 0.75 * clamp((t - 1.9) / 2.2, 0, 1);
        place(paperG, pc[0], pc[1], 30 * Math.cos(ph) * a + 8 * (1 - a), 0.82, 0.82 * (0.45 + 0.55 * Math.abs(Math.cos(ph * 0.9))));
        paperPoly.setAttribute("points", FOLD[0].map((p) => p.join(",")).join(" ")); show(crease, 0); paperLines.forEach((l) => show(l, 1));
      } else if (t < 6.25) {
        place(paperG, pc[0], pc[1], paperRot(t), 0.82); paperPoly.setAttribute("points", FOLD[0].map((p) => p.join(",")).join(" ")); show(crease, 0); paperLines.forEach((l) => show(l, 1));
      } else {
        const fs = foldShape(t);
        place(paperG, pc[0], pc[1], P.ln * 0.4, 0.82 * fs.sx, 0.82);
        paperPoly.setAttribute("points", fs.pts.map((p) => p.map(f1).join(",")).join(" "));
        show(crease, fs.crease && t < FSTEP[2] ? 0.8 : 0); paperLines.forEach((l, i) => show(l, 1 - sstep(FSTEP[0], FSTEP[0] + 0.12, t)));
      }
      show(paperG, Math.min(sstep(1.9, 2.0, t), 1 - sstep(7.6, 7.66, t)));
    } else show(paperG, 0);
    // plane
    if (t >= 7.6) {
      let c, a, s = 1.25;
      if (t < T_REL) { a = planeHeld(t); c = add(P.armR.end, rot(12, -8, a)); }
      else if (t < T_HIT) {
        c = flightAt(t); const c2 = flightAt(t + 0.01), c0 = flightAt(t - 0.01); a = Math.atan2(c2[1] - c0[1], c2[0] - c0[0]) * 180 / Math.PI;
        s = lerp(1.25, 2.1, sstep(T_REL, 9.4, t)) - 0.5 * sstep(11.9, 12.4, t);
      } else { const ph = planeOnHead(t); c = ph.c; a = ph.a; s = 1.6; }
      if (t > 11.6 && t < 13.7) place(planeG, c[0], c[1], a, s, -s);   // flying left: flip so it stays upright
      else place(planeG, c[0], c[1], a, s);
      show(planeG, sstep(7.6, 7.68, t));
    } else show(planeG, 0);
    // trail
    if (t > T_REL && t < T_HIT + 0.2) {
      const t0 = Math.max(T_REL, t - 0.62), t1 = Math.min(t, T_HIT);
      for (let k = 0; k < 4; k++) {
        const a = lerp(t0, t1, k / 4), b = lerp(t0, t1, (k + 1) / 4), pts = [];
        for (let i = 0; i <= 6; i++) pts.push(flightAt(lerp(a, b, i / 6)));
        trail[k].setAttribute("d", smoothPath(pts)); trail[k].setAttribute("display", "inline");
      }
    } else trail.forEach((p) => p.setAttribute("display", "none"));

    // fx: whistle notes
    notes.forEach((g, i) => {
      const t0 = 0.25 + i * 0.42, s = (t - t0) / 1.15;
      if (s < 0 || s > 1) return show(g, 0);
      const Pn = poseCache(t0), m = add(Pn.head, [48, 14]);
      place(g, m[0] + 60 * s + 10 * Math.sin(s * 9 + i), m[1] - 110 * s, -15 + 25 * Math.sin(s * 6 + i), 0.9 + 0.2 * s);
      show(g, Math.min(s / 0.15, (1 - s) / 0.3));
    });
    // ? and !
    { const o = life(t, 4.75, 5.56, 0.1, 0.08); show(qG, o); const pop = gsap.parseEase("back.out(3)")(clamp((t - 4.75) / 0.3, 0, 1));
      place(qG, P.head[0] + 58, P.head[1] - 62 + 4 * Math.sin(t * 7), 10 * Math.sin(t * 5), Math.max(0.01, pop)); }
    { const o = life(t, 12.36, 13.2, 0.06, 0.15); show(xG, o); const pop = gsap.parseEase("back.out(3)")(clamp((t - 12.36) / 0.22, 0, 1));
      place(xG, P.head[0] + 52, P.head[1] - 66, 8, Math.max(0.01, pop)); }
    // lightbulb
    { const o = life(t, 5.58, 6.6, 0.04, 0.2); show(bulbG, o); const pop = gsap.parseEase("back.out(2.4)")(clamp((t - 5.58) / 0.35, 0, 1));
      place(bulbG, P.head[0] + 6, P.head[1] - 124 + 3 * Math.sin(t * 6), 4 * Math.sin(t * 4), Math.max(0.01, pop * (1 - 0.4 * sstep(6.4, 6.6, t))));
      rays.setAttribute("transform", `scale(${Math.round((1 + 0.08 * Math.sin(t * 18)) * 1000) / 1000})`); }
    // sparkle when the plane is done
    { const s = clamp((t - 7.92) / 0.45, 0, 1); show(spark, s > 0 && s < 1 ? Math.sin(Math.PI * s) : 0);
      if (s > 0 && s < 1) { const c = add(P.armR.end, rot(44, -18, planeHeld(t))); place(spark, c[0], c[1], s * 90, 0.4 + 0.8 * Math.sin(Math.PI * s)); } }
    // throw smear
    if (t > 8.66 && t < 9.05) {
      const pts = []; for (let i = 0; i <= 8; i++) pts.push(poseCache(lerp(8.64, Math.min(t, 8.8), i / 8)).armR.end);
      const o = 1 - sstep(8.8, 9.05, t);
      smear.forEach((p, i) => { p.setAttribute("d", smoothPath(pts.map((q) => add(q, [0, (i - 1) * 14 * (i ? 1 : 0)])))); show(p, o * (i ? 0.8 : 0.45)); });
    } else smear.forEach((p) => show(p, 0));
    // sweat drop after the wipe
    { const s = (t - 13.88) / 0.55; if (s > 0 && s < 1) { const o0 = add(poseCache(13.88).head, [34, -26]); place(drop, o0[0] + 150 * s, o0[1] - 70 * s + 300 * s * s, 30 * s, 0.9); show(drop, Math.min(1, (1 - s) * 3)); } else show(drop, 0); }
    // bonk: burst + orbiting stars
    { const s = (t - T_HIT) / 0.28; const ip = IMPACT.at;
      burst.forEach((l, i) => { if (s < 0 || s > 1) return show(l, 0); const a = -150 + i * 34, [x1, y1] = rot(26 + 40 * s, 0, a), [x2, y2] = rot(46 + 60 * s, 0, a);
        l.setAttribute("x1", f1(ip[0] + x1)); l.setAttribute("y1", f1(ip[1] + y1)); l.setAttribute("x2", f1(ip[0] + x2)); l.setAttribute("y2", f1(ip[1] + y2)); show(l, 1 - s); }); }
    stars.forEach((st, i) => {
      const o = life(t, 14.66, 15.5, 0.1, 0.2); show(st, o); if (o <= 0) return;
      const a = (t - 14.66) * 7 + i * 2.094, c = add(P.head, [Math.cos(a) * 52, -58 + Math.sin(a) * 13]);
      place(st, c[0], c[1], t * 200, 0.8 + 0.25 * Math.sin(a));
    });
  }

  // ---------------- init: derive the catch, release and impact points from the pose itself ----------------
  CATCH = add(pose(4.1).armR.end, [6, -44]);
  { const p = pose(T_REL); RELEASE = add(p.armR.end, rot(12, -8, planeHeld(T_REL))); }
  IMPACT = { c: [XSTOP - 80, 420] };
  for (let it = 0; it < 4; it++) {
    const p = pose(T_HIT), nose = add(p.head, [-30, -34]), ang = 24;
    const c = add(nose, rot(-40 * 1.6, 0, ang));   // plane centre so its nose (local +40) sits on the head
    IMPACT = { at: nose, ang, tilt: p.tilt, c, off: [c[0] - p.head[0], c[1] - p.head[1]] };
    FLIGHT = [[T_REL, RELEASE[0], RELEASE[1]], [9.15, RELEASE[0] + 270, RELEASE[1] - 120], [9.6, 1430, 300], [9.95, 1600, 220], [10.25, 1585, 92], [10.55, 1440, 112],
      [10.8, 1412, 240], [11.1, 1560, 330], [11.5, 1900, 300], [11.85, 2560, 300], [12.0, 2400, 430], [12.35, 1720, 470], [12.65, 1160, 468], [12.85, 790, 452],
      [13.1, 380, 430], [13.4, -120, 400], [13.6, -560, 360], [13.75, -760, 240], [13.95, -180, 290], [14.3, 330, 370], [T_HIT, c[0], c[1]]];
  }
  cache.clear();
  const tl = gsap.timeline({ paused: true });
  // the clock's setter redraws: setters run on every seek, callbacks can be suppressed
  let now = -1;
  const clock = { get t() { return now; }, set t(v) { if (v !== now) { now = v; render(v); } } };
  tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none" }, 0);
  render(0);
  window.__stick = { pose, flightAt, FLIGHT, CATCH, RELEASE, IMPACT, XSTOP, render };
  return tl;
};
