/* The Jet Engine Paradox, Session C: the "blueprint world".
   One shared renderer for every C scene (copied into each scene folder by _c_lib/sync.sh; edit it here only).
   Canvas 2D with our own perspective camera, so wireframes have true depth and parallax but stay crisp, precise
   line work. Everything is a pure function of the scene time t: seeded hashes, no state carried between frames.

   Pieces:
     BP.Stage(canvas)           paper, parallax grid, lamp light, bloom, dust, grain; lines go on stage.L (layer ctx)
     BP.camera({...})           perspective projection (yaw/pitch orbit around a target, roll, screen offset)
     BP.draw(ctx, cam, strokes, opts)   stroke-by-stroke line drawing with a hot pen tip, fog, flicker, dissolve
     BP.fighter(), BP.stealth(), BP.engineBlock(), BP.engineSection()   the reusable generic drawings
   Units are metres; x runs nose to tail, y up, z to the right wing. Generic shapes, not a copy of any maker's drawing. */
(function () {
  "use strict";
  const BP = {};
  BP.C = { amber: "#F97316", hot: "#FDBA74", red: "#EF4444", white: "#F8FAFC", dim: "#94A3B8", slate: "#0B0E14", paper: "#121826" };

  // ---------- math ----------
  const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
  BP.clamp = clamp;
  BP.lerp = (a, b, t) => a + (b - a) * t;
  BP.ss = (e0, e1, x) => { const t = clamp((x - e0) / (e1 - e0)); return t * t * (3 - 2 * t); };
  BP.eio = (e0, e1, x) => { const t = clamp((x - e0) / (e1 - e0)); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  BP.eout = (e0, e1, x) => { const t = clamp((x - e0) / (e1 - e0)); return 1 - Math.pow(1 - t, 3); };
  BP.ein = (e0, e1, x) => { const t = clamp((x - e0) / (e1 - e0)); return t * t * t; };
  BP.hash = (a, b = 0) => {
    let h = (Math.imul(a | 0, 374761393) + Math.imul(b | 0, 668265263)) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  };
  BP.rng = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  // smooth value noise in 1D (seeded), for organic drift as f(t)
  BP.noise1 = (x, seed = 1) => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return BP.lerp(BP.hash(i, seed), BP.hash(i + 1, seed), u) * 2 - 1; };
  // keyframes: [[t, value or array], ...], eased in-out between keys
  BP.keys = (k, t, ease = BP.eio) => {
    if (t <= k[0][0]) return k[0][1];
    for (let i = 1; i < k.length; i++) {
      if (t <= k[i][0]) {
        const a = k[i - 1], b = k[i], e = ease(a[0], b[0], t);
        return Array.isArray(a[1]) ? a[1].map((v, j) => v + (b[1][j] - v) * e) : a[1] + (b[1] - a[1]) * e;
      }
    }
    return k[k.length - 1][1];
  };
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const norm = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };

  // ---------- camera ----------
  // yaw 0 = looking from the +z side (a side view of an aircraft along x); pitch > 0 = looking down.
  BP.camera = (o) => {
    const W = o.W || 1920, H = o.H || 1080, d2r = Math.PI / 180;
    const yaw = (o.yaw || 0) * d2r, pitch = (o.pitch || 0) * d2r, T = o.target || [0, 0, 0];
    const eye = [T[0] + o.dist * Math.cos(pitch) * Math.sin(yaw), T[1] + o.dist * Math.sin(pitch), T[2] + o.dist * Math.cos(pitch) * Math.cos(yaw)];
    const f = norm(sub(T, eye)), r = norm(cross(f, [0, 1, 0])), u = cross(r, f);
    const focal = H / 2 / Math.tan(((o.fov || 30) * d2r) / 2);
    const cx = (o.cx != null ? o.cx : W / 2), cy = (o.cy != null ? o.cy : H / 2);
    const roll = (o.roll || 0) * d2r, cr = Math.cos(roll), sr = Math.sin(roll);
    return {
      eye, focal, dist: o.dist,
      proj(p) {
        const d = sub(p, eye), zc = dot(d, f);
        if (zc < 0.05) return null;
        const x = (dot(d, r) / zc) * focal, y = (-dot(d, u) / zc) * focal;
        return [cx + x * cr - y * sr, cy + x * sr + y * cr, zc];
      },
    };
  };

  // model transform: scale, rotate X, Y, Z (degrees), then translate
  BP.xf = (o = {}) => {
    const d2r = Math.PI / 180, s = o.s == null ? 1 : o.s, P = o.pos || [0, 0, 0];
    const ax = (o.rx || 0) * d2r, ay = (o.ry || 0) * d2r, az = (o.rz || 0) * d2r;
    const cx = Math.cos(ax), sx = Math.sin(ax), cy = Math.cos(ay), sy = Math.sin(ay), cz = Math.cos(az), sz = Math.sin(az);
    const piv = o.pivot || [0, 0, 0];
    return (p) => {
      let x = (p[0] - piv[0]) * s, y = (p[1] - piv[1]) * s, z = (p[2] - piv[2]) * s, t;
      t = y * cx - z * sx; z = y * sx + z * cx; y = t;
      t = x * cy + z * sy; z = -x * sy + z * cy; x = t;
      t = x * cz - y * sz; y = x * sz + y * cz; x = t;
      return [x + P[0], y + P[1], z + P[2]];
    };
  };

  // ---------- strokes ----------
  // a stroke: { p: [[x,y,z]...], len: cumulative lengths, L, w, a, g (group), col }
  BP.stroke = (pts, o = {}) => {
    const len = [0];
    for (let i = 1; i < pts.length; i++) len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1], pts[i][2] - pts[i - 1][2]));
    return Object.assign({ p: pts, len, L: len[len.length - 1] || 1e-6, w: 1.6, a: 1, g: "main" }, o);
  };
  // progress of item i of n inside a group drawn over global progress p (overlap 0..1 = how many draw at once)
  BP.seq = (p, i, n, overlap = 0.25) => {
    if (n <= 1) return clamp(p);
    const win = Math.max(overlap, 1 / n), start = (i / (n - 1)) * (1 - win);
    return clamp((p - start) / win);
  };
  BP.group = (strokes, g) => strokes.filter((s) => s.g === g);
  BP.groups = (strokes, gs) => strokes.filter((s) => gs.includes(s.g));
  BP.box3 = (strokes, xf) => { // model-space bounds (after xf)
    const lo = [1e9, 1e9, 1e9], hi = [-1e9, -1e9, -1e9];
    for (const s of strokes) for (const q of s.p) { const v = xf ? xf(q) : q; for (let k = 0; k < 3; k++) { lo[k] = Math.min(lo[k], v[k]); hi[k] = Math.max(hi[k], v[k]); } }
    return { lo, hi, c: [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2] };
  };

  /* Draw strokes onto ctx.
     opts: xf, prog (number | (i, s) => 0..1), col, alpha, w (width multiplier), fog [near, far, minAlpha],
           pen (true: hot tip on unfinished strokes), flicker {t, amt, rate}, dissolve 0..1 (+ t), jitter px,
           colFn (i, s) => colour, alphaFn (i, s) => mult, shift [dx, dy] screen offset, heads (array to collect pen tips) */
  BP.draw = (ctx, cam, strokes, o = {}) => {
    const xf = o.xf || ((p) => p), heads = o.heads || [];
    const n = strokes.length, fog = o.fog, sh = o.shift || [0, 0];
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    for (let i = 0; i < n; i++) {
      const s = strokes[i];
      let p = typeof o.prog === "function" ? o.prog(i, s) : (o.prog == null ? 1 : o.prog);
      if (p <= 0) continue;
      p = Math.min(p, 1);
      let a = (s.a == null ? 1 : s.a) * (o.alpha == null ? 1 : o.alpha) * (o.alphaFn ? o.alphaFn(i, s) : 1);
      if (o.flicker) {
        const f = o.flicker, k = Math.floor(f.t * (f.rate || 18));
        const h = BP.hash(i * 7919 + 13, k);
        a *= 1 - f.amt * (h > 0.72 ? 1 : h * 0.35);
      }
      if (a <= 0.003) continue;
      const pts = s.p, target = p * s.L;
      const scr = [];
      let zsum = 0, zc = 0, head = null;
      for (let j = 0; j < pts.length; j++) {
        let q = pts[j];
        if (s.len[j] > target) { // partial: interpolate into the last segment
          const t0 = s.len[j - 1], t1 = s.len[j], u = (target - t0) / Math.max(1e-9, t1 - t0), a0 = pts[j - 1];
          q = [a0[0] + (q[0] - a0[0]) * u, a0[1] + (q[1] - a0[1]) * u, a0[2] + (q[2] - a0[2]) * u];
          const v = cam.proj(xf(q)); if (v) { scr.push(v); head = v; }
          break;
        }
        const v = cam.proj(xf(q));
        if (v) { scr.push(v); zsum += v[2]; zc++; }
      }
      if (scr.length < 2) continue;
      if (fog) { const z = zsum / Math.max(1, zc); a *= BP.lerp(1, fog[2], clamp((z - fog[0]) / (fog[1] - fog[0]))); }
      const col = o.colFn ? o.colFn(i, s) : (o.col || s.col || BP.C.amber);
      const lw = (s.w || 1.6) * (o.w || 1);
      if (o.dissolve > 0) { drawDissolve(ctx, cam, xf, s, i, o, a, col, lw, sh); continue; }
      ctx.globalAlpha = clamp(a);
      ctx.strokeStyle = col;
      ctx.lineWidth = lw;
      if (s.dash) ctx.setLineDash(s.dash); else ctx.setLineDash([]);
      ctx.beginPath();
      const jit = o.jitter || 0;
      for (let j = 0; j < scr.length; j++) {
        let x = scr[j][0] + sh[0], y = scr[j][1] + sh[1];
        if (jit) { x += (BP.hash(i * 31 + j, 5) - 0.5) * jit; y += (BP.hash(i * 31 + j, 9) - 0.5) * jit; }
        if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      if (s.closed && p >= 1) ctx.closePath();
      ctx.stroke();
      if (head && o.pen !== false && p < 1) heads.push([head[0] + sh[0], head[1] + sh[1], clamp(a)]);
    }
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
    return heads;
  };
  // break a stroke into drifting, fading fragments (the "dissolve" of an engine)
  function drawDissolve(ctx, cam, xf, s, i, o, a, col, lw, sh) {
    const k = clamp(o.dissolve), pts = s.p;
    ctx.strokeStyle = col; ctx.lineWidth = lw;
    for (let j = 1; j < pts.length; j++) {
      const h = BP.hash(i * 977 + j, 3);
      const kk = clamp((k - h * 0.35) / 0.65); // fragments leave at different moments
      if (kk >= 1) continue;
      const dx = (BP.hash(i * 977 + j, 4) - 0.5) * 1.6, dy = 0.4 + BP.hash(i * 977 + j, 6) * 1.6, dz = (BP.hash(i * 977 + j, 7) - 0.5) * 1.6;
      const m = kk * kk * 1.4;
      const A = pts[j - 1], B = pts[j];
      const off = [dx * m, dy * m, dz * m];
      const pa = cam.proj(xf([A[0] + off[0], A[1] + off[1], A[2] + off[2]])), pb = cam.proj(xf([B[0] + off[0], B[1] + off[1], B[2] + off[2]]));
      if (!pa || !pb) continue;
      // fragments shrink toward their midpoint as they go
      const mx = (pa[0] + pb[0]) / 2, my = (pa[1] + pb[1]) / 2, sc = 1 - kk * 0.85;
      ctx.globalAlpha = clamp(a * (1 - kk) * (1 + kk));
      ctx.beginPath();
      ctx.moveTo(mx + (pa[0] - mx) * sc + sh[0], my + (pa[1] - my) * sc + sh[1]);
      ctx.lineTo(mx + (pb[0] - mx) * sc + sh[0], my + (pb[1] - my) * sc + sh[1]);
      ctx.stroke();
      if (kk > 0.05 && h > 0.6) { // embers
        ctx.globalAlpha = clamp(a * (1 - kk) * 1.4);
        ctx.fillStyle = BP.C.hot;
        ctx.fillRect(mx + sh[0] - 1.5, my + sh[1] - 1.5, 3, 3);
      }
    }
    ctx.globalAlpha = 1;
  }
  // hot pen tips (drawing heads)
  BP.pens = (ctx, heads, col = BP.C.hot) => {
    for (const h of heads) {
      ctx.globalAlpha = 0.9 * h[2];
      ctx.fillStyle = "#FFF4E6";
      ctx.beginPath(); ctx.arc(h[0], h[1], 2.6, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = 0.35 * h[2];
      ctx.fillStyle = col;
      ctx.beginPath(); ctx.arc(h[0], h[1], 7, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1;
  };
  // soft additive glow blob (projected point)
  BP.glow = (ctx, x, y, r, col, a) => {
    if (a <= 0) return;
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, col); g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = clamp(a); ctx.fillStyle = g;
    ctx.fillRect(x - r, y - r, 2 * r, 2 * r); ctx.restore();
  };
  // 2D helpers on screen coordinates
  BP.line2 = (ctx, a, b, col, w, alpha, dash, dashOff) => {
    ctx.save(); ctx.globalAlpha = clamp(alpha); ctx.strokeStyle = col; ctx.lineWidth = w;
    if (dash) { ctx.setLineDash(dash); ctx.lineDashOffset = dashOff || 0; }
    ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); ctx.restore();
  };
  // partial 2D line (draw-on from a to b)
  BP.line2p = (ctx, a, b, p, col, w, alpha, dash, dashOff) => {
    if (p <= 0) return null;
    const e = [a[0] + (b[0] - a[0]) * clamp(p), a[1] + (b[1] - a[1]) * clamp(p)];
    BP.line2(ctx, a, e, col, w, alpha, dash, dashOff);
    return e;
  };
  // dimension line between two screen points, offset by n px along the normal; ticks + arrowheads, no text
  BP.dim = (ctx, A, B, off, p, col, alpha) => {
    if (!A || !B || p <= 0) return;
    const dx = B[0] - A[0], dy = B[1] - A[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
    const a = [A[0] + nx * off, A[1] + ny * off], b = [B[0] + nx * off, B[1] + ny * off];
    const e1 = clamp(p * 2), e2 = clamp(p * 2 - 1);
    BP.line2p(ctx, A, [A[0] + nx * (off + Math.sign(off) * 12), A[1] + ny * (off + Math.sign(off) * 12)], e1, col, 1, alpha * 0.7);
    BP.line2p(ctx, B, [B[0] + nx * (off + Math.sign(off) * 12), B[1] + ny * (off + Math.sign(off) * 12)], e1, col, 1, alpha * 0.7);
    if (e2 <= 0) return;
    const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    BP.line2p(ctx, m, a, e2, col, 1.2, alpha); BP.line2p(ctx, m, b, e2, col, 1.2, alpha);
    if (e2 >= 1) for (const [P, s] of [[a, 1], [b, -1]]) {
      const ux = (dx / l) * s, uy = (dy / l) * s;
      ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = col; ctx.beginPath();
      ctx.moveTo(P[0], P[1]); ctx.lineTo(P[0] + ux * 14 + nx * 4, P[1] + uy * 14 + ny * 4); ctx.lineTo(P[0] + ux * 14 - nx * 4, P[1] + uy * 14 - ny * 4);
      ctx.closePath(); ctx.fill(); ctx.restore();
    }
  };
  // construction lines: long faint lines through screen points, racing dashes
  BP.construct = (ctx, pts, t, o = {}) => {
    const W = 1920, H = 1080, col = o.col || "rgba(248,250,252,1)", a = o.alpha == null ? 0.1 : o.alpha, speed = o.speed || 60;
    for (let i = 0; i < pts.length; i++) {
      const P = pts[i]; if (!P) continue;
      const p = o.prog ? o.prog(i) : 1; if (p <= 0) continue;
      const hz = BP.hash(i, 77) > 0.5;
      // horizontal and vertical guides grow out from the point
      BP.line2(ctx, [P[0] - (P[0] + 40) * p, P[1]], [P[0] + (W - P[0] + 40) * p, P[1]], col, 1, a * (hz ? 1 : 0.6), [14, 10], -t * speed * (1 + i % 3));
      BP.line2(ctx, [P[0], P[1] - (P[1] + 40) * p], [P[0], P[1] + (H - P[1] + 40) * p], col, 1, a * (hz ? 0.6 : 1), [4, 9], t * speed * 0.7);
      // registration cross at the point
      ctx.save(); ctx.globalAlpha = a * 3 * p; ctx.strokeStyle = o.crossCol || BP.C.hot; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(P[0], P[1], 7, 0, Math.PI * 2); ctx.moveTo(P[0] - 12, P[1]); ctx.lineTo(P[0] + 12, P[1]); ctx.moveTo(P[0], P[1] - 12); ctx.lineTo(P[0], P[1] + 12); ctx.stroke(); ctx.restore();
    }
  };

  // ---------- stage: paper, grid, light, bloom, dust, grain ----------
  BP.Stage = function (canvas, o = {}) {
    const W = 1920, H = 1080, seed = o.seed || 7;
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext("2d");
    const mk = (w, h) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; };
    const Lc = mk(W, H), L = Lc.getContext("2d");
    const G1c = mk(480, 270), G1 = G1c.getContext("2d");
    const G2c = mk(240, 135), G2 = G2c.getContext("2d");
    // paper plate: lifted slate, mottled, with fibres (pre-rendered once, 8% margin for drift)
    const PW = 2080, PH = 1170, paperC = mk(PW, PH), pc = paperC.getContext("2d");
    const R = BP.rng(seed);
    pc.fillStyle = o.paper || "#141B28"; pc.fillRect(0, 0, PW, PH);
    for (let i = 0; i < 70; i++) { // low-frequency mottling
      const x = R() * PW, y = R() * PH, r = 120 + R() * 380, l = R() < 0.5;
      const g = pc.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, l ? "rgba(160,180,210,0.035)" : "rgba(0,0,0,0.07)"); g.addColorStop(1, "rgba(0,0,0,0)");
      pc.fillStyle = g; pc.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
    pc.lineWidth = 1;
    for (let i = 0; i < 2600; i++) { // paper fibres
      const x = R() * PW, y = R() * PH, a = R() * Math.PI, l = 4 + R() * 18;
      pc.strokeStyle = R() < 0.5 ? "rgba(220,230,245,0.035)" : "rgba(0,0,0,0.08)";
      pc.beginPath(); pc.moveTo(x, y); pc.quadraticCurveTo(x + Math.cos(a) * l * 0.5 + (R() - 0.5) * 4, y + Math.sin(a) * l * 0.5 + (R() - 0.5) * 4, x + Math.cos(a) * l, y + Math.sin(a) * l); pc.stroke();
    }
    // grain tiles
    const tiles = [];
    for (let k = 0; k < 4; k++) {
      const c = mk(256, 256), g = c.getContext("2d"), id = g.createImageData(256, 256), r = BP.rng(seed * 31 + k);
      for (let i = 0; i < id.data.length; i += 4) { const v = r() < 0.5 ? 0 : 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = Math.floor(r() * 26); }
      g.putImageData(id, 0, 0); tiles.push(c);
    }
    // dust / bokeh specks (foreground layer, strongest parallax)
    const dust = [];
    const RD = BP.rng(seed * 17 + 3);
    for (let i = 0; i < 70; i++) dust.push({ x: RD() * W, y: RD() * H, r: RD() < 0.85 ? 0.8 + RD() * 1.8 : 6 + RD() * 18, a: 0.05 + RD() * 0.22, vx: (RD() - 0.5) * 14, vy: -4 - RD() * 10, ph: RD() * 6.28 });

    const S = { ctx, L, W, H, canvas };
    // begin a frame. o: t, paper (alpha), shift [x,y] camera drift in px (parallax source), zoom, grid alpha, light [x,y]
    S.begin = (f) => {
      S.f = f;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1;
      ctx.clearRect(0, 0, W, H);
      L.setTransform(1, 0, 0, 1, 0, 0); L.globalCompositeOperation = "source-over"; L.globalAlpha = 1;
      L.clearRect(0, 0, W, H);
      const pa = f.paper == null ? 1 : f.paper, sh = f.shift || [0, 0];
      if (pa > 0) {
        ctx.save();
        if (f.clip) { ctx.beginPath(); f.clip(ctx); ctx.clip(); }
        ctx.globalAlpha = pa;
        ctx.drawImage(paperC, -80 + sh[0] * 0.15, -45 + sh[1] * 0.15);
        // drafting lamp: a slow, warm light pool
        const lx = f.light ? f.light[0] : 760, ly = f.light ? f.light[1] : 430;
        const g = ctx.createRadialGradient(lx, ly, 0, lx, ly, 1250);
        g.addColorStop(0, "rgba(255,190,140,0.075)"); g.addColorStop(0.45, "rgba(150,170,210,0.03)"); g.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
        // grid (parallax 0.35 of the camera drift)
        S.grid(ctx, f, pa);
        ctx.restore();
      }
    };
    S.grid = (c, f, pa) => {
      const ga = (f.grid == null ? 1 : f.grid) * pa;
      if (ga <= 0) return;
      const sh = f.shift || [0, 0], z = f.zoom || 1, minor = 32 * z, major = minor * 5;
      const ox = ((sh[0] * 0.35) % major + major) % major, oy = ((sh[1] * 0.35) % major + major) % major;
      c.lineWidth = 1;
      for (const [step, a] of [[minor, 0.035], [major, 0.075]]) {
        c.strokeStyle = `rgba(226,232,240,${a * ga})`;
        c.beginPath();
        for (let x = (ox % step) - step; x < W + step; x += step) { const X = Math.round(x) + 0.5; c.moveTo(X, 0); c.lineTo(X, H); }
        for (let y = (oy % step) - step; y < H + step; y += step) { const Y = Math.round(y) + 0.5; c.moveTo(0, Y); c.lineTo(W, Y); }
        c.stroke();
      }
    };
    // composite the line layer with bloom, then dust, grain
    S.end = (f2 = {}) => {
      const f = Object.assign({}, S.f, f2);
      const bloom = f.bloom == null ? 1 : f.bloom;
      ctx.save();
      if (f.clip) { ctx.beginPath(); f.clip(ctx); ctx.clip(); }
      if (bloom > 0) {
        G1.clearRect(0, 0, 480, 270); G1.filter = "blur(2px)"; G1.drawImage(Lc, 0, 0, 480, 270); G1.filter = "none";
        G2.clearRect(0, 0, 240, 135); G2.filter = "blur(3px)"; G2.drawImage(G1c, 0, 0, 240, 135); G2.filter = "none";
        ctx.globalCompositeOperation = "lighter";
        ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
        ctx.globalAlpha = 0.95 * bloom; ctx.drawImage(G1c, 0, 0, W, H);
        ctx.globalAlpha = 0.85 * bloom; ctx.drawImage(G2c, 0, 0, W, H);
      }
      ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1;
      ctx.drawImage(Lc, 0, 0);
      ctx.restore();
      S.dust(f);
      S.grain(f);
    };
    S.dust = (f) => {
      const t = f.t || 0, sh = f.shift || [0, 0], da = f.dust == null ? 1 : f.dust;
      if (da <= 0) return;
      ctx.save(); ctx.globalCompositeOperation = "lighter";
      for (const d of dust) {
        let x = d.x + d.vx * t + sh[0] * (d.r > 4 ? 0.9 : 0.6), y = d.y + d.vy * t + Math.sin(t * 0.7 + d.ph) * 6 + sh[1] * (d.r > 4 ? 0.9 : 0.6);
        x = ((x % (W + 80)) + W + 80) % (W + 80) - 40; y = ((y % (H + 80)) + H + 80) % (H + 80) - 40;
        const tw = 0.6 + 0.4 * Math.sin(t * 1.3 + d.ph * 3);
        if (d.r > 4) {
          const g = ctx.createRadialGradient(x, y, 0, x, y, d.r);
          g.addColorStop(0, `rgba(253,186,116,${0.05 * da * tw})`); g.addColorStop(1, "rgba(0,0,0,0)");
          ctx.fillStyle = g; ctx.fillRect(x - d.r, y - d.r, 2 * d.r, 2 * d.r);
        } else {
          ctx.globalAlpha = d.a * da * tw; ctx.fillStyle = "#E8EEF6";
          ctx.beginPath(); ctx.arc(x, y, d.r, 0, Math.PI * 2); ctx.fill(); ctx.globalAlpha = 1;
        }
      }
      ctx.restore();
    };
    S.grain = (f) => {
      const fr = Math.floor((f.t || 0) * 30), tile = tiles[fr % 4];
      const ox = Math.floor(BP.hash(fr, 1) * 256), oy = Math.floor(BP.hash(fr, 2) * 256);
      ctx.save(); ctx.globalAlpha = f.grain == null ? 1 : f.grain;
      ctx.translate(-ox, -oy);
      ctx.fillStyle = ctx.createPattern(tile, "repeat");
      ctx.fillRect(0, 0, W + 256, H + 256);
      ctx.restore();
    };
    return S;
  };

  // ---------- geometry helpers ----------
  const spow = (v, e) => Math.sign(v) * Math.pow(Math.abs(v), e);
  // superellipse ring in the y-z plane at x
  BP.ring = (x, hw, hh, yc = 0, n = 32, e = 0.8, zc = 0) => {
    const pts = [];
    for (let i = 0; i <= n; i++) { const a = (i / n) * Math.PI * 2; pts.push([x, yc + hh * spow(Math.sin(a), e), zc + hw * spow(Math.cos(a), e)]); }
    return pts;
  };
  BP.circleYZ = (x, r, yc = 0, zc = 0, n = 40, a0 = 0, a1 = Math.PI * 2) => {
    const pts = [];
    for (let i = 0; i <= n; i++) { const a = a0 + (i / n) * (a1 - a0); pts.push([x, yc + r * Math.sin(a), zc + r * Math.cos(a)]); }
    return pts;
  };
  const interpProfile = (tab, x) => { // tab rows [x, ...values]
    if (x <= tab[0][0]) return tab[0].slice(1);
    for (let i = 1; i < tab.length; i++) if (x <= tab[i][0]) {
      const a = tab[i - 1], b = tab[i], u = (x - a[0]) / (b[0] - a[0]), s = u * u * (3 - 2 * u) * 0.35 + u * 0.65;
      return a.slice(1).map((v, k) => v + (b[k + 1] - v) * s);
    }
    return tab[tab.length - 1].slice(1);
  };
  const poly = (pts, closed) => (closed ? pts.concat([pts[0]]) : pts);
  const seg = (a, b, n = 1) => { const r = []; for (let i = 0; i <= n; i++) r.push([a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n, a[2] + (b[2] - a[2]) * i / n]); return r; };
  BP.seg = seg;
  // a lofted body: rings at stations + stringers along it
  function loft(out, tab, stations, ringFn, g, o = {}) {
    const rings = stations.map((x) => ringFn(x, interpProfile(tab, x)));
    rings.forEach((r, i) => out.push(BP.stroke(r, { g: g + "_rings", w: o.wr || 1.3, a: o.ar || 0.8, closed: false, k: i })));
    const n = rings[0].length - 1, every = o.every || 4;
    // dense stringers sampled along a finer station list for smooth curves
    const fine = []; for (let x = stations[0]; x <= stations[stations.length - 1] + 1e-6; x += o.fineStep || 0.25) fine.push(x);
    if (fine[fine.length - 1] < stations[stations.length - 1]) fine.push(stations[stations.length - 1]);
    const fr = fine.map((x) => ringFn(x, interpProfile(tab, x)));
    for (let k = 0; k < n; k += every) out.push(BP.stroke(fr.map((r) => r[k]), { g: g + "_long", w: o.wl || 1.5, a: o.al || 0.9, k }));
    return rings;
  }

  // ---------- model 1: generic single-engine tailless delta light fighter ----------
  // ~13.2 m long, 8.2 m span; side intakes, one engine, one fin. Groups: fuse_rings, fuse_long, canopy, wing, wing_detail,
  // fin, intake, bay (the engine cavity), probe. bay info: { x0, x1, r, yc } for placing an engine.
  BP.fighter = (o = {}) => {
    const S = [];
    const tab = [ // x, half-width, half-height, y-centre
      [0.0, 0.02, 0.02, 0.0], [0.45, 0.2, 0.2, 0.0], [1.2, 0.36, 0.36, 0.02], [2.0, 0.47, 0.46, 0.04], [3.0, 0.55, 0.53, 0.06],
      [4.0, 0.62, 0.57, 0.06], [5.0, 0.7, 0.6, 0.04], [6.5, 0.75, 0.62, 0.04], [8.0, 0.75, 0.62, 0.04], [9.5, 0.7, 0.6, 0.04],
      [11.0, 0.61, 0.56, 0.04], [12.2, 0.54, 0.52, 0.03], [12.9, 0.48, 0.47, 0.02],
    ];
    const ringFn = (x, v) => BP.ring(x, v[0], v[1], v[2], 32, 0.85);
    loft(S, tab, [0.45, 1.2, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 12.9], ringFn, "fuse", { every: 4, ar: 0.55 });
    // nose tip stringers start at the tip
    // canopy: arcs over the top from x 2.3 to 5.2, plus frame lines
    const can = (x) => { const u = clamp((x - 2.3) / 2.9); return 0.44 * Math.pow(Math.sin(Math.PI * Math.pow(u, 0.8)), 0.75); };
    const cy = (x) => { const v = interpProfile(tab, x); return v[2] + v[1] * 0.82; };
    const cw = 0.34;
    const canArc = (x) => { const h = can(x), pts = []; for (let i = 0; i <= 16; i++) { const a = Math.PI * i / 16; pts.push([x, cy(x) + h * Math.sin(a), cw * Math.cos(a) * (0.55 + 0.45 * Math.min(1, h / 0.3))]); } return pts; };
    for (const x of [2.6, 3.1, 3.7, 4.3, 4.85]) S.push(BP.stroke(canArc(x), { g: "canopy", w: 1.3, a: 0.85 }));
    const cl = []; for (let x = 2.3; x <= 5.2001; x += 0.1) cl.push([x, cy(x) + can(x), 0]);
    S.push(BP.stroke(cl, { g: "canopy", w: 1.7 }));
    for (const s of [1, -1]) { const l = []; for (let x = 2.3; x <= 5.2001; x += 0.1) l.push([x, cy(x) + can(x) * 0.12, s * cw * (0.55 + 0.45 * Math.min(1, can(x) / 0.3))]); S.push(BP.stroke(l, { g: "canopy", w: 1.4 })); }
    // dorsal spine to the fin
    const sp = []; for (let x = 5.2; x <= 9.2; x += 0.2) sp.push([x, cy(x) + 0.16 * Math.sin(Math.PI * (x - 5.2) / 8), 0]);
    S.push(BP.stroke(sp, { g: "canopy", w: 1.4, a: 0.8 }));
    // wing: compound delta (half planform), y slightly below the centreline
    const wy = -0.12, LE = [[3.9, 0.72], [7.1, 2.05], [10.7, 4.1]], TT = [11.85, 4.1], TR = [12.5, 0.7];
    const leX = (z) => (z <= 2.05 ? BP.lerp(3.9, 7.1, (z - 0.72) / (2.05 - 0.72)) : BP.lerp(7.1, 10.7, (z - 2.05) / (4.1 - 2.05)));
    const teX = (z) => BP.lerp(12.5, 11.85, (z - 0.7) / (4.1 - 0.7));
    const th = (z) => 0.09 * (1 - (z - 0.7) / 4.4);
    for (const s of [1, -1]) {
      const up = [[3.9, wy + th(0.72), 0.72 * s], [7.1, wy + th(2.05), 2.05 * s], [10.7, wy + th(4.1), 4.1 * s], [TT[0], wy + th(4.1), 4.1 * s], [TR[0], wy + th(0.7), 0.7 * s]];
      S.push(BP.stroke(subdiv(up, 6), { g: "wing", w: 1.8 }));
      const lo = up.map((p) => [p[0], wy - (p[1] - wy) * 0.7, p[2]]);
      S.push(BP.stroke(subdiv(lo, 6), { g: "wing", w: 1.1, a: 0.5 }));
      // spars and ribs
      for (const f of [0.18, 0.62]) { const l = []; for (let z = 0.75; z <= 4.05; z += 0.25) { const xl = leX(z), xt = teX(z); l.push([xl + (xt - xl) * f, wy + th(z), z * s]); } S.push(BP.stroke(l, { g: "wing_detail", w: 1, a: 0.55 })); }
      for (const z of [1.2, 1.75, 2.3, 2.85, 3.4, 3.85]) { const xl = leX(z), xt = teX(z); S.push(BP.stroke(seg([xl, wy + th(z), z * s], [xt, wy + th(z), z * s], 6), { g: "wing_detail", w: 1, a: 0.5 })); }
      // elevons (inboard and outboard) along the trailing edge
      const hinge = (z) => teX(z) - 0.75;
      S.push(BP.stroke([[hinge(0.95), wy + th(0.95), 0.95 * s], [hinge(2.45), wy + th(2.45), 2.45 * s], [teX(2.45), wy + th(2.45), 2.45 * s]], { g: "wing_detail", w: 1.3, a: 0.8 }));
      S.push(BP.stroke([[teX(2.55), wy + th(2.55), 2.55 * s], [hinge(2.55), wy + th(2.55), 2.55 * s], [hinge(3.95), wy + th(3.95), 3.95 * s], [teX(3.95), wy + th(3.95), 3.95 * s]], { g: "wing_detail", w: 1.3, a: 0.8 }));
      // leading-edge slat line
      S.push(BP.stroke([[leX(2.3) + 0.3, wy + th(2.3), 2.3 * s], [leX(3.9) + 0.25, wy + th(3.9), 3.9 * s]], { g: "wing_detail", w: 1, a: 0.6 }));
      // side intakes (Y-duct), under the wing root
      const ix = 4.35, iz = 0.86 * s, iyc = -0.18;
      const mouth = []; for (let i = 0; i <= 20; i++) { const a = (i / 20) * Math.PI * 2; mouth.push([ix + 0.06 * Math.cos(a), iyc + 0.3 * spow(Math.sin(a), 0.7), iz + 0.17 * spow(Math.cos(a), 0.7)]); }
      S.push(BP.stroke(mouth, { g: "intake", w: 1.6 }));
      for (const [dy, dz] of [[0.3, 0], [-0.3, 0], [0, 0.17 * s]]) S.push(BP.stroke(curve3([ix, iyc + dy, iz + dz], [6.6, iyc * 0.5 + dy * 0.6, iz * 0.9 + dz], [8.1, 0.04 + dy * 0.4, 0.3 * s + dz * 0.3], 10), { g: "intake", w: 1.1, a: 0.6 }));
    }
    // fin
    const fin = [[8.8, 0.62, 0], [11.55, 3.15, 0], [12.45, 3.15, 0], [12.95, 0.55, 0]];
    for (const dz of [0.035, -0.035]) S.push(BP.stroke(subdiv(fin.map((p) => [p[0], p[1], dz]), 4), { g: "fin", w: dz > 0 ? 1.8 : 1, a: dz > 0 ? 1 : 0.5 }));
    S.push(BP.stroke([[11.95, 3.1, 0], [12.25, 0.75, 0]], { g: "fin", w: 1.2, a: 0.8 })); // rudder hinge
    for (const yy of [1.3, 2.0, 2.6]) { const u = (yy - 0.6) / 2.55; S.push(BP.stroke(seg([BP.lerp(8.8, 11.55, u), yy, 0], [BP.lerp(12.95, 12.45, u), yy, 0], 3), { g: "fin", w: 1, a: 0.45 })); }
    // nose probe
    S.push(BP.stroke([[-1.0, 0, 0], [0.0, 0, 0]], { g: "probe", w: 1.3 }));
    S.push(BP.stroke([[0, 0, 0], [0.45, 0.2, 0], [1.2, 0.38, 0]], { g: "fuse_long", w: 1.2, a: 0.7 }));
    // engine bay: the empty cavity in the rear fuselage
    const bay = { x0: 8.15, x1: 12.85, r: 0.44, yc: 0.03 };
    for (const x of [8.15, 9.1, 10.05, 11.0, 11.95, 12.85]) S.push(BP.stroke(BP.circleYZ(x, bay.r, bay.yc, 0, 36), { g: "bay", w: 1.5, a: 0.95 }));
    for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2 + 0.2; S.push(BP.stroke(seg([8.15, bay.yc + bay.r * Math.sin(a), bay.r * Math.cos(a)], [12.85, bay.yc + bay.r * Math.sin(a), bay.r * Math.cos(a)], 4), { g: "bay", w: 1.2, a: 0.75 })); }
    return { strokes: S, bay, len: 13.2 };
  };
  function subdiv(pts, n) { const r = []; for (let i = 0; i < pts.length - 1; i++) for (let k = 0; k < n; k++) { const u = k / n; r.push([pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u, pts[i][2] + (pts[i + 1][2] - pts[i][2]) * u]); } r.push(pts[pts.length - 1]); return r; }
  function curve3(a, b, c, n) { const r = []; for (let i = 0; i <= n; i++) { const u = i / n, v = 1 - u; r.push([v * v * a[0] + 2 * v * u * b[0] + u * u * c[0], v * v * a[1] + 2 * v * u * b[1] + u * u * c[1], v * v * a[2] + 2 * v * u * b[2] + u * u * c[2]]); } return r; }
  BP.subdiv = subdiv; BP.curve3 = curve3;

  // ---------- model 2: generic twin-engine stealth fighter (AMCA-like planform, not a copy of any drawing) ----------
  // ~17.6 m long, 11.1 m span; chined faceted body, caret intakes, canted twin fins, two engines side by side.
  // Groups: fuse_rings, fuse_long, canopy, wing, wing_detail, tail, fin, intake, bays. engines: [{x0,x1,r,yc,zc}]
  BP.stealth = (o = {}) => {
    const S = [];
    const tab = [ // x, half-width (chine), top height, bottom depth
      [0.0, 0.02, 0.02, 0.02], [1.0, 0.42, 0.26, 0.2], [2.5, 0.78, 0.42, 0.34], [4.0, 1.05, 0.55, 0.44], [5.6, 1.5, 0.6, 0.55],
      [7.2, 1.8, 0.6, 0.6], [9.2, 1.9, 0.58, 0.6], [11.2, 1.88, 0.55, 0.58], [13.2, 1.8, 0.5, 0.54], [15.2, 1.66, 0.45, 0.5], [17.1, 1.42, 0.4, 0.44],
    ];
    const ringFn = (x, v) => { // faceted chined section
      const w = v[0], h = v[1], b = v[2];
      const half = [[0, h], [0.5 * w, 0.82 * h], [w, 0.04 * h], [0.82 * w, -0.45 * b], [0.4 * w, -b], [0, -b]];
      const pts = half.map((q) => [x, q[0] === 0 && q[1] === h ? h : q[1], q[0]]);
      const mir = half.slice(1, -1).reverse().map((q) => [x, q[1], -q[0]]);
      const ring = pts.concat([[x, -b, 0]]).concat(mir.reverse().reverse()).concat([[x, h, 0]]);
      return ring;
    };
    // ring order: top, upper-chine R, chine R, lower R, bottom R, bottom, bottom L..., keep consistent length per x
    const ringFn2 = (x, v) => {
      const w = v[0], h = v[1], b = v[2];
      return [[x, h, 0], [x, 0.82 * h, 0.5 * w], [x, 0.04 * h, w], [x, -0.45 * b, 0.82 * w], [x, -b, 0.4 * w], [x, -b, -0.4 * w], [x, -0.45 * b, -0.82 * w], [x, 0.04 * h, -w], [x, 0.82 * h, -0.5 * w], [x, h, 0]];
    };
    void ringFn;
    loft(S, tab, [1.0, 2.5, 4.0, 5.6, 7.2, 9.2, 11.2, 13.2, 15.2, 17.1], ringFn2, "fuse", { every: 1, fineStep: 0.3, ar: 0.55, wl: 1.3, al: 0.75 });
    S.push(BP.stroke([[0, 0, 0], [1.0, 0.04 * 0.26, 0.42], [2.5, 0.04 * 0.42, 0.78]], { g: "fuse_long", w: 1.2 }));
    S.push(BP.stroke([[0, 0, 0], [1.0, 0.04 * 0.26, -0.42], [2.5, 0.04 * 0.42, -0.78]], { g: "fuse_long", w: 1.2 }));
    // canopy
    const ctop = (x) => interpProfile(tab, x)[1];
    const can = (x) => 0.42 * Math.pow(Math.sin(Math.PI * clamp((x - 2.6) / 3.6)), 0.7);
    for (const x of [3.0, 3.6, 4.3, 5.0, 5.7]) { const pts = []; const h = can(x); for (let i = 0; i <= 14; i++) { const a = Math.PI * i / 14; pts.push([x, ctop(x) + h * Math.sin(a) * 0.95, 0.42 * Math.cos(a)]); } S.push(BP.stroke(pts, { g: "canopy", w: 1.2, a: 0.85 })); }
    const cl = []; for (let x = 2.6; x <= 6.2001; x += 0.1) cl.push([x, ctop(x) + can(x), 0]); S.push(BP.stroke(cl, { g: "canopy", w: 1.7 }));
    for (const s of [1, -1]) {
      // wing (y at the chine)
      const W = [[7.0, 0.03, 1.8 * s], [12.5, 0.03, 5.55 * s], [13.75, 0.03, 5.55 * s], [15.3, 0.03, 1.75 * s]];
      S.push(BP.stroke(subdiv(W, 6), { g: "wing", w: 1.8 }));
      S.push(BP.stroke(subdiv(W.map((p) => [p[0], -0.06, p[2]]), 6), { g: "wing", w: 1, a: 0.45 }));
      const le = (z) => BP.lerp(7.0, 12.5, (z - 1.8) / 3.75), te = (z) => BP.lerp(15.3, 13.75, (z - 1.75) / 3.8);
      for (const f of [0.2, 0.65]) { const l = []; for (let z = 1.85; z <= 5.5; z += 0.3) l.push([le(z) + (te(z) - le(z)) * f, 0.03, z * s]); S.push(BP.stroke(l, { g: "wing_detail", w: 1, a: 0.55 })); }
      for (const z of [2.5, 3.2, 3.9, 4.6, 5.2]) S.push(BP.stroke(seg([le(z), 0.03, z * s], [te(z), 0.03, z * s], 5), { g: "wing_detail", w: 1, a: 0.45 }));
      S.push(BP.stroke([[te(2.0) - 0.7, 0.03, 2.0 * s], [te(4.9) - 0.6, 0.03, 4.9 * s], [te(4.9), 0.03, 4.9 * s]], { g: "wing_detail", w: 1.3, a: 0.8 }));
      // horizontal tail
      S.push(BP.stroke(subdiv([[14.7, 0.0, 1.62 * s], [16.55, 0.0, 3.75 * s], [17.35, 0.0, 3.75 * s], [17.65, 0.0, 1.55 * s]], 4), { g: "tail", w: 1.6 }));
      // canted fin (25 degrees outward)
      const cant = (25 * Math.PI) / 180, root = [0, 0.48, 1.25 * s];
      const fp = [[13.3, 0], [15.9, 2.5], [16.75, 2.5], [17.2, 0]].map(([x, h]) => [x, root[1] + h * Math.cos(cant), root[2] + s * h * Math.sin(cant)]);
      S.push(BP.stroke(subdiv(fp, 4), { g: "fin", w: 1.7 }));
      for (const hh of [0.8, 1.6]) { const u = hh / 2.5; S.push(BP.stroke(seg([BP.lerp(13.3, 15.9, u), root[1] + hh * Math.cos(cant), root[2] + s * hh * Math.sin(cant)], [BP.lerp(17.2, 16.75, u), root[1] + hh * Math.cos(cant), root[2] + s * hh * Math.sin(cant)], 3), { g: "fin", w: 1, a: 0.5 })); }
      // caret intake (parallelogram mouth) on each side
      const ix = 5.4, m = [[ix, 0.38, 1.12 * s], [ix + 0.35, 0.36, 1.62 * s], [ix + 0.6, -0.42, 1.6 * s], [ix + 0.2, -0.45, 1.08 * s]];
      S.push(BP.stroke(m.concat([m[0]]), { g: "intake", w: 1.6 }));
      for (const q of [m[0], m[3]]) S.push(BP.stroke(curve3(q, [8.0, q[1] * 0.6, 1.1 * s], [10.0, 0.0, 0.62 * s + (q[1] > 0 ? 0.25 : -0.25) * s], 10), { g: "intake", w: 1.1, a: 0.55 }));
    }
    // engine bays (two cavities)
    const engines = [-1, 1].map((s) => ({ x0: 10.1, x1: 17.15, r: 0.46, yc: 0.0, zc: 0.62 * s }));
    for (const e of engines) {
      for (const x of [10.1, 11.5, 12.9, 14.3, 15.7, 17.15]) S.push(BP.stroke(BP.circleYZ(x, e.r, e.yc, e.zc, 32), { g: "bays", w: 1.3, a: 0.8 }));
      for (let k = 0; k < 6; k++) { const a = (k / 6) * Math.PI * 2 + 0.5; S.push(BP.stroke(seg([e.x0, e.yc + e.r * Math.sin(a), e.zc + e.r * Math.cos(a)], [e.x1, e.yc + e.r * Math.sin(a), e.zc + e.r * Math.cos(a)], 4), { g: "bays", w: 1, a: 0.6 })); }
    }
    return { strokes: S, engines, len: 17.6 };
  };

  // ---------- model 3: generic engine block (3D), placed by bay {x0, x1, r, yc, zc} ----------
  // Groups: eng_case, eng_face, eng_noz, eng_detail. o.variant changes the detailing so two engines read as different.
  BP.engineBlock = (bay, o = {}) => {
    const S = [], v = o.variant || 0, zc = bay.zc || 0, yc = bay.yc || 0;
    const x0 = bay.x0 + 0.08, x1 = bay.x1 - 0.05, L = x1 - x0, R = bay.r * 0.93;
    const prof = v === 0
      ? [[0, 0.9], [0.06, 1.0], [0.3, 1.0], [0.45, 0.93], [0.62, 0.95], [0.82, 0.9], [1.0, 0.8]]
      : v === 1
        ? [[0, 0.95], [0.05, 1.0], [0.22, 1.0], [0.35, 0.88], [0.58, 0.88], [0.7, 0.94], [0.88, 0.94], [1.0, 0.86]]
        : [[0, 0.92], [0.08, 1.0], [0.4, 0.97], [0.55, 0.9], [0.75, 0.92], [1.0, 0.82]];
    const rAt = (u) => { for (let i = 1; i < prof.length; i++) if (u <= prof[i][0]) { const a = prof[i - 1], b = prof[i]; return R * BP.lerp(a[1], b[1], (u - a[0]) / (b[0] - a[0])); } return R * prof[prof.length - 1][1]; };
    const st = v === 1 ? [0, 0.05, 0.14, 0.22, 0.35, 0.47, 0.58, 0.7, 0.8, 0.88, 0.95, 1] : [0, 0.06, 0.16, 0.3, 0.38, 0.45, 0.55, 0.62, 0.72, 0.82, 0.92, 1];
    for (const u of st) S.push(BP.stroke(BP.circleYZ(x0 + u * L, rAt(u), yc, zc, 40), { g: "eng_case", w: 1.4, a: 0.9 }));
    const nl = v === 1 ? 10 : 12;
    for (let k = 0; k < nl; k++) { const a = (k / nl) * Math.PI * 2 + 0.13; const pts = []; for (let i = 0; i <= 24; i++) { const u = i / 24; pts.push([x0 + u * L, yc + rAt(u) * Math.sin(a), zc + rAt(u) * Math.cos(a)]); } S.push(BP.stroke(pts, { g: "eng_case", w: 1.2, a: 0.75 })); }
    // fan face: hub, spinner and blades (swept radial lines)
    const fx = x0 + 0.02, nb = v === 1 ? 18 : v === 2 ? 22 : 16;
    S.push(BP.stroke(BP.circleYZ(fx, R * 0.28, yc, zc, 24), { g: "eng_face", w: 1.3 }));
    for (let k = 0; k < nb; k++) { const a = (k / nb) * Math.PI * 2; const pts = []; for (let i = 0; i <= 6; i++) { const rr = R * (0.28 + 0.68 * i / 6), aa = a + 0.35 * (i / 6) * (v === 2 ? 1.3 : 1); pts.push([fx + 0.04 * i / 6, yc + rr * Math.sin(aa), zc + rr * Math.cos(aa)]); } S.push(BP.stroke(pts, { g: "eng_face", w: 1.1, a: 0.85 })); }
    S.push(BP.stroke([[fx - 0.25, yc, zc], [fx, yc + R * 0.28, zc]], { g: "eng_face", w: 1.1, a: 0.7 }));
    S.push(BP.stroke([[fx - 0.25, yc, zc], [fx, yc - R * 0.28, zc]], { g: "eng_face", w: 1.1, a: 0.7 }));
    S.push(BP.stroke([[fx - 0.25, yc, zc], [fx, yc, zc + R * 0.28]], { g: "eng_face", w: 1.1, a: 0.7 }));
    // nozzle petals
    const np = v === 1 ? 12 : 14, xr = x1, rr = rAt(1);
    for (let k = 0; k < np; k++) { const a = (k / np) * Math.PI * 2; S.push(BP.stroke([[xr - L * 0.1, yc + rr * 1.05 * Math.sin(a), zc + rr * 1.05 * Math.cos(a)], [xr, yc + rr * Math.sin(a), zc + rr * Math.cos(a)]], { g: "eng_noz", w: 1.1, a: 0.8 })); }
    S.push(BP.stroke(BP.circleYZ(xr, rr * 0.82, yc, zc, 30), { g: "eng_noz", w: 1.2, a: 0.7 }));
    // detail: gearbox box underneath and pipe runs
    const gb = [[0.25, 0.4]].map(([a, b]) => [x0 + a * L, x0 + b * L]);
    for (const [xa, xb] of gb) {
      const y = yc - R * 1.02, h = R * 0.22, w = R * 0.32;
      const c = [[xa, y, zc - w], [xb, y, zc - w], [xb, y, zc + w], [xa, y, zc + w], [xa, y, zc - w], [xa, y - h, zc - w], [xb, y - h, zc - w], [xb, y - h, zc + w], [xa, y - h, zc + w], [xa, y - h, zc - w]];
      S.push(BP.stroke(c, { g: "eng_detail", w: 1, a: 0.7 }));
    }
    const pa = v === 1 ? 2.2 : 1.1;
    S.push(BP.stroke([0, 0.2, 0.4, 0.6, 0.8, 1].map((u) => [x0 + (0.12 + u * 0.7) * L, yc + R * 1.06 * Math.sin(pa), zc + R * 1.06 * Math.cos(pa)]), { g: "eng_detail", w: 1, a: 0.6 }));
    return { strokes: S, front: [fx, yc, zc], rear: [xr, yc, zc], R };
  };

  // ---------- model 4: afterburning twin-spool turbofan, side section (GTX-35VS-style layout, generic) ----------
  // Drawn as a half-section mirrored about the centreline in the z=0 plane, with revolved station rings for depth.
  // ~4.25 m long, 0.92 m casing diameter. Groups: center, case, hatch, fan, hpc, comb, turb, shaft, ab, rings,
  // ab_case, ab_hatch, ab_rings (everything aft of the turbine, so the afterburner can slide off), drynoz (Dry Kaveri nozzle).
  BP.engineSection = (o = {}) => {
    const S = [], ab = o.ab !== false;
    const both = (pts, opt) => { S.push(BP.stroke(pts, opt)); S.push(BP.stroke(pts.map((p) => [p[0], -p[1], p[2]]), Object.assign({}, opt, { mirror: true }))); };
    const P = (x, r) => [x, r, 0];
    S.push(BP.stroke([P(-0.35, 0), P(4.75, 0)], { g: "center", w: 1, a: 0.5, dash: [26, 6, 4, 6] }));
    // outer casing: intake lip to turbine exit, then the afterburner duct and nozzle
    const caseF = [P(0.18, 0.43), P(0.24, 0.462), P(0.4, 0.468), P(1.0, 0.468), P(1.9, 0.455), P(2.75, 0.448)];
    const caseA = [P(2.75, 0.448), P(3.85, 0.44), P(4.03, 0.36), P(4.25, 0.385)];
    both(subdiv(caseF, 3), { g: "case", w: 2 });
    both(subdiv(caseA, 3), { g: "ab_case", w: 2 });
    // inner wall of the bypass duct (thickness line) and flanges
    both(subdiv([P(0.26, 0.44), P(1.0, 0.445), P(1.9, 0.432), P(2.75, 0.425)], 3), { g: "case", w: 1.1, a: 0.7 });
    both(subdiv([P(2.75, 0.425), P(3.82, 0.418)], 3), { g: "ab_case", w: 1.1, a: 0.7 });
    for (const x of [1.0, 1.9]) both([P(x, 0.445), P(x, 0.49)], { g: "case", w: 1.3 });
    for (const x of [2.75]) both([P(x, 0.425), P(x, 0.49)], { g: "case", w: 1.3 });
    both([P(3.85, 0.418), P(3.85, 0.47)], { g: "ab_case", w: 1.3 });
    // section hatching inside the casing wall (cut faces)
    for (let x = 0.3; x < 2.72; x += 0.055) both([P(x, 0.446), P(x + 0.03, 0.466)], { g: "hatch", w: 0.9, a: 0.55 });
    for (let x = 2.78; x < 3.8; x += 0.055) both([P(x, 0.42), P(x + 0.03, 0.444)], { g: "ab_hatch", w: 0.9, a: 0.55 });
    // spinner and fan hub
    both(subdiv([P(0.0, 0.0), P(0.08, 0.06), P(0.2, 0.11), P(0.3, 0.13)], 3), { g: "fan", w: 1.6 });
    both([P(0.3, 0.13), P(0.98, 0.17)], { g: "fan", w: 1.4 });
    // 3 fan stages: rotor (blade outline) + stator
    const fanX = [0.32, 0.55, 0.77];
    fanX.forEach((x, i) => {
      const hub = BP.lerp(0.135, 0.165, i / 2), tip = 0.438;
      both([P(x, hub), P(x + 0.02, tip), P(x + 0.1, tip), P(x + 0.085, hub), P(x, hub)], { g: "fan", w: 1.4 });
      both([P(x + 0.04, hub + 0.02), P(x + 0.055, tip - 0.02)], { g: "fan", w: 0.9, a: 0.5 });
      both([P(x + 0.13, hub + 0.005), P(x + 0.14, tip), P(x + 0.18, tip), P(x + 0.17, hub + 0.005)], { g: "fan", w: 1.1, a: 0.75 });
    });
    // splitter between bypass and core
    both(subdiv([P(1.0, 0.3), P(1.04, 0.318), P(1.9, 0.31), P(2.75, 0.33)], 3), { g: "hpc", w: 1.5 });
    both([P(1.04, 0.318), P(1.04, 0.296)], { g: "hpc", w: 1.1 });
    // 6-stage HP compressor: blades shrink toward the combustor
    both([P(1.04, 0.172), P(1.88, 0.205)], { g: "hpc", w: 1.3 });
    both([P(1.04, 0.296), P(1.88, 0.262)], { g: "hpc", w: 1.3 });
    for (let i = 0; i < 6; i++) {
      const x = 1.08 + i * 0.13, hub = BP.lerp(0.174, 0.2, i / 5), tip = BP.lerp(0.294, 0.265, i / 5);
      both([P(x, hub), P(x + 0.012, tip), P(x + 0.055, tip), P(x + 0.048, hub), P(x, hub)], { g: "hpc", w: 1.2 });
      both([P(x + 0.075, hub + 0.004), P(x + 0.08, tip - 0.002), P(x + 0.1, tip - 0.002), P(x + 0.098, hub + 0.004)], { g: "hpc", w: 0.9, a: 0.6 });
    }
    // annular combustor: liner, dome, injector, dilution holes
    both(subdiv([P(1.95, 0.215), P(2.0, 0.205), P(2.3, 0.205), P(2.36, 0.212)], 3), { g: "comb", w: 1.4 });
    both(subdiv([P(1.95, 0.262), P(2.0, 0.278), P(2.3, 0.282), P(2.36, 0.27)], 3), { g: "comb", w: 1.4 });
    both(curveArc(1.95, 0.2385, 0.0235, Math.PI / 2, 1.5 * Math.PI), { g: "comb", w: 1.4 });
    both([P(1.9, 0.24), P(1.975, 0.24)], { g: "comb", w: 1.6 });
    for (const x of [2.08, 2.16, 2.24]) { both(curveArc(x, 0.2, 0.006, 0, Math.PI * 2, 10), { g: "comb", w: 0.9, a: 0.7 }); both(curveArc(x, 0.284, 0.006, 0, Math.PI * 2, 10), { g: "comb", w: 0.9, a: 0.7 }); }
    // turbines: HP NGV + rotor, LP NGV + rotor (blades grow aft)
    const tb = [[2.38, 0.2, 0.29, 0.9], [2.44, 0.2, 0.295, 1.4], [2.53, 0.195, 0.31, 0.9], [2.6, 0.19, 0.318, 1.4]];
    for (const [x, hub, tip, w] of tb) both([P(x, hub), P(x + 0.008, tip), P(x + 0.045, tip), P(x + 0.04, hub), P(x, hub)], { g: "turb", w });
    both([P(2.36, 0.2), P(2.7, 0.188)], { g: "turb", w: 1.2 });
    both([P(2.36, 0.296), P(2.7, 0.325)], { g: "turb", w: 1.2 });
    // shafts: LP (long, inner) and HP (outer, short)
    both([P(0.3, 0.04), P(2.68, 0.04)], { g: "shaft", w: 1.2, a: 0.85 });
    both([P(1.04, 0.075), P(2.5, 0.075)], { g: "shaft", w: 1.2, a: 0.85 });
    both([P(1.04, 0.075), P(1.04, 0.17)], { g: "shaft", w: 1, a: 0.6 });
    both([P(2.48, 0.075), P(2.48, 0.2)], { g: "shaft", w: 1, a: 0.6 });
    both([P(2.66, 0.04), P(2.66, 0.19)], { g: "shaft", w: 1, a: 0.6 });
    for (const x of [0.45, 1.2, 2.55]) both(curveArc(x, 0.057, 0.012, 0, Math.PI * 2, 10), { g: "shaft", w: 0.9, a: 0.7 }); // bearings
    // tail cone and mixer
    both(subdiv([P(2.7, 0.188), P(2.85, 0.15), P(3.0, 0.07), P(3.08, 0.0)], 3), { g: "turb", w: 1.4 });
    both(subdiv([P(2.7, 0.325), P(2.8, 0.36), P(2.88, 0.37)], 2), { g: "turb", w: 1.2, a: 0.8 });
    if (ab) {
      // afterburner: spray bars, V-gutter flame holders, liner
      for (const r of [0.12, 0.25, 0.35]) both([P(3.12, r + 0.025), P(3.06, r), P(3.12, r - 0.025)], { g: "ab", w: 1.5 });
      both([P(2.96, 0.06), P(2.96, 0.39)], { g: "ab", w: 1.0, a: 0.75 });
      for (let i = 0; i < 6; i++) both(curveArc(2.96, 0.09 + i * 0.055, 0.006, 0, Math.PI * 2, 8), { g: "ab", w: 0.9, a: 0.7 });
      both(subdiv([P(2.95, 0.4), P(3.85, 0.4)], 4), { g: "ab", w: 1.1, a: 0.7, dash: [10, 6] });
      // convergent-divergent nozzle flaps
      both([P(3.85, 0.4), P(4.03, 0.335), P(4.24, 0.36)], { g: "ab", w: 1.6 });
      both([P(4.03, 0.335), P(4.03, 0.37)], { g: "ab", w: 1, a: 0.7 });
    }
    // a short fixed nozzle for the Dry Kaveri (drawn when the afterburner is removed)
    both(subdiv([P(2.75, 0.448), P(2.95, 0.43), P(3.1, 0.36)], 3), { g: "drynoz", w: 2 });
    both([P(2.88, 0.37), P(3.1, 0.34)], { g: "drynoz", w: 1.2, a: 0.8 });
    // revolved station rings (depth): faint circles in the y-z plane
    for (const [x, r, g] of [[0.24, 0.462, "rings"], [1.0, 0.468, "rings"], [1.9, 0.455, "rings"], [2.75, 0.448, "rings"], [3.3, 0.444, "ab_rings"], [3.85, 0.44, "ab_rings"], [4.25, 0.385, "ab_rings"]]) {
      S.push(BP.stroke(BP.circleYZ(x, r, 0, 0, 56), { g, w: 1.1, a: 0.42 }));
    }
    for (const [x, r] of [[0.55, 0.438], [1.47, 0.29]]) S.push(BP.stroke(BP.circleYZ(x, r, 0, 0, 48), { g: "rings", w: 1, a: 0.28 }));
    // longitudinal casing lines on the far side (give the section a body)
    for (const a of [0.7, 2.4, 3.9, 5.5]) {
      const pts = [[0.24, 0.462], [1.0, 0.468], [1.9, 0.455], [2.75, 0.448]].map(([x, r]) => [x, r * Math.sin(a), r * Math.cos(a)]);
      S.push(BP.stroke(pts, { g: "rings", w: 1, a: 0.25 }));
      S.push(BP.stroke([[2.75, 0.448], [3.85, 0.44], [4.25, 0.385]].map(([x, r]) => [x, r * Math.sin(a), r * Math.cos(a)]), { g: "ab_rings", w: 1, a: 0.25 }));
    }
    return { strokes: S, len: 4.25, nozzle: [4.25, 0, 0], dryNozzle: [3.1, 0, 0], turbineExit: 2.75 };
  };
  function curveArc(cx, cy, r, a0, a1, n = 12) { const pts = []; for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a), 0]); } return pts; }

  // ---------- DOM helpers ----------
  // place a DOM element at a screen point (absolute px)
  BP.place = (el, x, y) => { el.style.left = x + "px"; el.style.top = y + "px"; };
  // leader line from a label anchor to a target point, drawn on the line layer
  BP.leader = (ctx, from, to, p, col = BP.C.white, alpha = 0.9) => {
    if (!from || !to || p <= 0) return;
    const mid = [to[0] + (from[0] - to[0]) * 0.0, from[1]];
    const e1 = clamp(p * 2), e2 = clamp(p * 2 - 1);
    BP.line2p(ctx, from, mid, e1, col, 1.4, alpha);
    if (e2 > 0) BP.line2p(ctx, mid, to, e2, col, 1.4, alpha);
    if (e2 >= 1) { ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = col; ctx.beginPath(); ctx.arc(to[0], to[1], 4, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }
  };

  window.BP = BP;
})();
