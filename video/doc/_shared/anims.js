// Full-screen animated science shots, drawn on <canvas> from the timeline time (deterministic:
// seeded RNG, no Date/Math.random, every frame is a pure function of t).
// Usage in markup: <div class="shot anim" data-anim="blood" data-opts='{"co2":1}'><canvas class="cv"></canvas></div>
// doc.js calls DOC_ANIMS[name](ctx, t, d, opts) on every timeline update.
(function () {
  const W = 1920, H = 1080;
  const rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const sprites = {};
  // Pre-rendered blurred sprites (blur once, reuse every frame).
  const sprite = (key, size, blur, paint) => {
    const k = key + "|" + size + "|" + blur;
    if (sprites[k]) return sprites[k];
    const pad = Math.ceil(blur * 3) + 2, c = document.createElement("canvas");
    c.width = c.height = size + pad * 2;
    const g = c.getContext("2d");
    if (blur > 0.3) g.filter = `blur(${blur}px)`;
    g.translate(pad + size / 2, pad + size / 2);
    paint(g, size / 2);
    return (sprites[k] = c);
  };

  // ------------------------------------------------ red blood cell (biconcave disc)
  const rbc = (g, r) => {
    const body = g.createRadialGradient(-r * 0.25, -r * 0.3, r * 0.1, 0, 0, r);
    body.addColorStop(0, "#ff6a5c"); body.addColorStop(0.55, "#c4121c"); body.addColorStop(1, "#5a0208");
    g.fillStyle = body; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill();
    const dimple = g.createRadialGradient(0, 0, 0, 0, 0, r * 0.62);
    dimple.addColorStop(0, "rgba(70,0,6,0.75)"); dimple.addColorStop(0.7, "rgba(120,0,10,0.25)"); dimple.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = dimple; g.beginPath(); g.arc(0, 0, r * 0.62, 0, Math.PI * 2); g.fill();
    g.strokeStyle = "rgba(255,170,150,0.35)"; g.lineWidth = r * 0.08; g.beginPath(); g.arc(0, 0, r * 0.9, Math.PI * 1.05, Math.PI * 1.7); g.stroke();
  };
  const bubble = (g, r) => {
    const b = g.createRadialGradient(-r * 0.3, -r * 0.3, r * 0.05, 0, 0, r);
    b.addColorStop(0, "rgba(220,235,255,0.9)"); b.addColorStop(0.5, "rgba(120,150,210,0.35)"); b.addColorStop(1, "rgba(80,110,180,0.05)");
    g.fillStyle = b; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill();
    g.strokeStyle = "rgba(200,220,255,0.6)"; g.lineWidth = Math.max(1, r * 0.08); g.stroke();
  };
  const glow = (color) => (g, r) => {
    const b = g.createRadialGradient(0, 0, 0, 0, 0, r);
    b.addColorStop(0, color); b.addColorStop(0.35, color.replace(/[\d.]+\)$/, "0.35)")); b.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = b; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill();
  };

  const A = {};

  // ------------------------------------------------ BLOOD: flythrough inside a vessel; CO2 rises, plasma acidifies
  A.blood = (ctx, t, d, o) => {
    const p = clamp(t / d, 0, 1), co2 = o.co2 ?? 1, acid = o.acid ?? 1, speed = o.speed ?? 1;
    // vessel wall + plasma
    const bg = ctx.createRadialGradient(W * 0.5, H * 0.5, 80, W * 0.5, H * 0.5, W * 0.75);
    bg.addColorStop(0, "#7a0a12"); bg.addColorStop(0.45, "#3d0208"); bg.addColorStop(1, "#0c0002");
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    // wall texture bands (slow drift)
    for (let i = 0; i < 7; i++) {
      const y = ((i / 7) * H + t * 40 * speed) % (H + 200) - 100;
      ctx.fillStyle = `rgba(255,90,90,${0.035 + 0.02 * Math.sin(i)})`;
      ctx.beginPath(); ctx.ellipse(W * 0.5, y, W * 0.9, 60, 0, 0, Math.PI * 2); ctx.fill();
    }
    const R = rng(o.seed || 7), N = 140, cells = [];
    for (let i = 0; i < N; i++) {
      const z = 0.15 + 0.85 * R();                   // depth: 0.15 far .. 1 near
      cells.push({ z, x0: R() * (W + 600), y0: R() * H, ph: R() * 6.28, spin: 0.3 + R() * 1.2, k: R() });
    }
    cells.sort((a, b) => a.z - b.z);
    for (const c of cells) {
      const size = lerp(26, 190, c.z * c.z);
      const blur = c.z > 0.8 ? (c.z - 0.8) * 40 : c.z < 0.35 ? (0.35 - c.z) * 14 : 0;   // shallow depth of field
      const s = sprite("rbc", Math.round(size / 8) * 8, Math.round(blur), rbc);
      const x = ((c.x0 + t * (160 + 520 * c.z) * speed) % (W + 600)) - 300;
      const y = c.y0 + Math.sin(t * 0.7 + c.ph) * 40 * c.z;
      const sq = 0.45 + 0.55 * Math.abs(Math.cos(t * c.spin + c.ph));   // tumbling disc
      ctx.save(); ctx.translate(x, y); ctx.rotate(c.ph + t * 0.2 * c.spin); ctx.scale(1, sq);
      ctx.globalAlpha = lerp(0.55, 1, c.z);
      ctx.drawImage(s, -s.width / 2, -s.height / 2); ctx.restore();
    }
    // CO2 microbubbles accumulate over the shot
    const nb = Math.floor(lerp(o.co2From ?? 8, 8 + 90 * co2, p)), RB = rng((o.seed || 7) + 99);
    for (let i = 0; i < nb; i++) {
      const z = 0.2 + 0.8 * RB(), x0 = RB() * (W + 400), y0 = RB() * H, r = lerp(5, 26, z);
      const s = sprite("bub", Math.round(r * 2 / 4) * 4, z > 0.85 ? 3 : 0, bubble);
      const x = ((x0 + t * (120 + 380 * z) * speed) % (W + 400)) - 200, y = y0 - t * 18 * z;
      ctx.globalAlpha = 0.85; ctx.drawImage(s, x - s.width / 2, ((y % H) + H) % H - s.height / 2);
    }
    ctx.globalAlpha = 1;
    // acidification: plasma shifts toward violet-blue as CO2 → carbonic acid
    if (acid) { ctx.fillStyle = `rgba(70,20,140,${0.32 * acid * p * p})`; ctx.fillRect(0, 0, W, H); }
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.7);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.75)");
    ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  };

  // ------------------------------------------------ LUNGS: bronchial tree breathing, then the hold; CO2 builds; optional spasm
  const tree = (R, x, y, ang, len, w, depth, out) => {
    const x2 = x + Math.cos(ang) * len, y2 = y + Math.sin(ang) * len;
    out.push([x, y, x2, y2, w, depth]);
    if (depth >= 8) return;
    const n = 2, spread = 0.42 + R() * 0.25;
    for (let i = 0; i < n; i++) tree(R, x2, y2, ang + (i ? spread : -spread) + (R() - 0.5) * 0.3, len * (0.72 + R() * 0.1), w * 0.7, depth + 1, out);
  };
  let lungCache = null;
  const lungGeo = () => {
    if (lungCache) return lungCache;
    const R = rng(11), segs = [];
    tree(R, W / 2, 170, Math.PI / 2, 150, 40, 0, segs);              // trachea
    const L = [], Rt = [];
    tree(R, W / 2 - 10, 320, Math.PI * 0.72, 130, 26, 1, L);
    tree(R, W / 2 + 10, 320, Math.PI * 0.28, 130, 26, 1, Rt);
    const pts = [];
    const RA = rng(12);
    for (let i = 0; i < 900; i++) {                                   // alveoli cloud inside each lung lobe
      const side = i % 2 ? 1 : -1, a = RA() * Math.PI * 2, rr = Math.sqrt(RA());
      const cx = W / 2 + side * 330, cy = 600;
      const x = cx + Math.cos(a) * rr * 270, y = cy + Math.sin(a) * rr * 360;
      if (Math.abs(x - W / 2) > 70) pts.push([x, y, RA()]);
    }
    return (lungCache = { trunk: segs.slice(0, 1), segs: segs.concat(L, Rt), pts });
  };
  A.lungs = (ctx, t, d, o) => {
    const p = clamp(t / d, 0, 1), g = lungGeo();
    const bg = ctx.createRadialGradient(W / 2, H * 0.55, 100, W / 2, H * 0.55, W * 0.7);
    bg.addColorStop(0, "#14223a"); bg.addColorStop(1, "#03060c");
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    // breathing: full cycles that die out into the hold
    const hold = o.hold ?? 0.25, amp = p < hold ? 1 - p / hold : 0;
    const breath = 1 + 0.06 * amp * Math.sin(t * 2.2);
    const spasm = o.spasm ? (p > (o.spasmAt ?? 0.4) ? Math.max(0, Math.sin(t * 19)) ** 6 * 0.035 : 0) : 0;
    const sc = breath + spasm, cx = W / 2, cy = 560;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(sc * (o.zoom ?? 1) * (1 + 0.04 * p), sc * (o.zoom ?? 1) * (1 + 0.04 * p)); ctx.translate(-cx, -cy);
    // lobes: soft tissue glow
    for (const side of [-1, 1]) {
      const lg = ctx.createRadialGradient(cx + side * 330, 600, 40, cx + side * 330, 600, 420);
      const hot = clamp((o.co2 ?? 1) * p, 0, 1);
      lg.addColorStop(0, `rgba(${Math.round(lerp(255, 255, hot))},${Math.round(lerp(150, 110, hot))},${Math.round(lerp(160, 60, hot))},0.55)`);
      lg.addColorStop(0.7, "rgba(160,60,80,0.18)"); lg.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = lg; ctx.beginPath(); ctx.ellipse(cx + side * 330, 600, 300, 400, 0, 0, Math.PI * 2); ctx.fill();
    }
    // alveoli
    for (const [x, y, k] of g.pts) {
      const s = sprite("alv", 18, 0, glow("rgba(255,170,175,0.9)"));
      ctx.globalAlpha = 0.25 + 0.35 * k; ctx.drawImage(s, x - 9, y - 9);
    }
    // bronchial tree
    ctx.globalAlpha = 1; ctx.lineCap = "round";
    for (const [x1, y1, x2, y2, w, dep] of g.segs) {
      ctx.strokeStyle = `rgba(${dep < 2 ? "235,225,230" : "250,190,200"},${0.95 - dep * 0.08})`;
      ctx.lineWidth = Math.max(1.2, w); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    // CO2 particles collecting during the hold
    const RB = rng(31), n = Math.floor(lerp(0, 260, clamp((p - hold * 0.5) / (1 - hold * 0.5), 0, 1)) * (o.co2 ?? 1));
    for (let i = 0; i < n; i++) {
      const side = i % 2 ? 1 : -1, a = RB() * 6.283, rr = Math.sqrt(RB());
      const x = cx + side * 330 + Math.cos(a + t * 0.2) * rr * 260, y = 600 + Math.sin(a + t * 0.2) * rr * 340;
      const s = sprite("co2", 22, 1, glow("rgba(255,150,40,0.95)"));
      ctx.globalAlpha = 0.8; ctx.drawImage(s, x - s.width / 2, y - s.height / 2);
    }
    ctx.globalAlpha = 1;
    // diaphragm dome
    const dy = 990 - 25 * amp * Math.sin(t * 2.2) - spasm * 900;
    ctx.strokeStyle = o.spasm && spasm > 0.005 ? "rgba(255,80,90,0.95)" : "rgba(240,190,120,0.85)";
    ctx.lineWidth = 22; ctx.beginPath(); ctx.moveTo(cx - 640, dy + 60); ctx.quadraticCurveTo(cx, dy - 140, cx + 640, dy + 60); ctx.stroke();
    ctx.restore();
    // urgency: red pulse late in the hold
    const alarm = o.alarm ? clamp((p - 0.5) * 2, 0, 1) * (0.5 + 0.5 * Math.sin(t * 6)) : 0;
    if (alarm) { ctx.fillStyle = `rgba(200,20,30,${0.18 * alarm})`; ctx.fillRect(0, 0, W, H); }
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.4, W / 2, H / 2, W * 0.75);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.8)"); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  };

  // ------------------------------------------------ NEURAL: chemoreceptor alarm racing through a neuron network
  let netCache = null;
  const netGeo = () => {
    if (netCache) return netCache;
    const R = rng(21), nodes = [];
    for (let i = 0; i < 230; i++) nodes.push({ x: R() * W * 1.2 - W * 0.1, y: R() * H * 1.2 - H * 0.1, z: 0.2 + 0.8 * R(), ph: R() * 6.28 });
    const edges = [];
    nodes.forEach((a, i) => {
      const near = nodes.map((b, j) => [j, (a.x - b.x) ** 2 + (a.y - b.y) ** 2]).filter(([j]) => j !== i).sort((u, v) => u[1] - v[1]).slice(0, 3);
      near.forEach(([j]) => { if (i < j) edges.push([i, j, R()]); });
    });
    return (netCache = { nodes, edges });
  };
  A.neural = (ctx, t, d, o) => {
    const p = clamp(t / d, 0, 1), g = netGeo(), heat = clamp((o.heat ?? 1) * (0.3 + p), 0, 1);
    ctx.fillStyle = "#04030a"; ctx.fillRect(0, 0, W, H);
    for (const [nx, ny, nr, nc] of [[0.3, 0.4, 700, "rgba(90,40,160,0.35)"], [0.72, 0.62, 650, `rgba(${Math.round(lerp(60, 170, heat))},20,${Math.round(lerp(140, 60, heat))},0.35)`]]) {
      const ng = ctx.createRadialGradient(W * nx, H * ny, 0, W * nx, H * ny, nr); ng.addColorStop(0, nc); ng.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = ng; ctx.fillRect(0, 0, W, H);
    }
    const z = 1 + 0.12 * p;
    ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.rotate(0.03 * p); ctx.translate(-W / 2, -H / 2);
    // dendrites
    for (const [i, j] of g.edges) {
      const a = g.nodes[i], b = g.nodes[j], dz = (a.z + b.z) / 2;
      ctx.strokeStyle = `rgba(170,140,255,${0.18 + 0.42 * dz})`; ctx.lineWidth = 1 + 3.2 * dz;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.quadraticCurveTo((a.x + b.x) / 2 + 30 * Math.sin(a.ph), (a.y + b.y) / 2 + 30 * Math.cos(b.ph), b.x, b.y); ctx.stroke();
    }
    // action potentials: pulses travel along edges, faster and redder as the alarm grows
    const rate = lerp(0.35, 1.6, heat);
    for (const [i, j, k] of g.edges) {
      const a = g.nodes[i], b = g.nodes[j], f = ((t * rate + k * 3) % 1.6) / 1.6;
      if (k > 0.55 + 0.45 * heat) continue;
      const x = lerp(a.x, b.x, f), y = lerp(a.y, b.y, f), col = heat > 0.6 ? "rgba(255,70,60,0.95)" : "rgba(255,190,90,0.95)";
      const s = sprite("pulse" + (heat > 0.6), 70, 2, glow(col));
      ctx.globalAlpha = 0.9; ctx.drawImage(s, x - s.width / 2, y - s.height / 2);
    }
    // somas
    for (const n of g.nodes) {
      const fire = 0.5 + 0.5 * Math.sin(t * lerp(1.5, 7, heat) + n.ph);
      const s = sprite("soma", Math.round(lerp(18, 80, n.z) / 4) * 4, n.z > 0.85 ? 4 : 0, glow("rgba(190,170,255,0.95)"));
      ctx.globalAlpha = 0.5 + 0.5 * fire; ctx.drawImage(s, n.x - s.width / 2, n.y - s.height / 2);
    }
    ctx.restore(); ctx.globalAlpha = 1;
    if (heat > 0.6) { ctx.fillStyle = `rgba(180,0,20,${0.14 * (0.5 + 0.5 * Math.sin(t * 7))})`; ctx.fillRect(0, 0, W, H); }
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, W * 0.7);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.85)"); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  };

  // ------------------------------------------------ ECG: hospital monitor, heart rate falling
  const ecgWave = (ph) => {        // one beat, ph 0..1
    const g = (c, w, a) => a * Math.exp(-(((ph - c) / w) ** 2));
    return g(0.18, 0.035, 0.12) - g(0.335, 0.012, 0.14) + g(0.36, 0.012, 1.0) - g(0.385, 0.012, 0.3) + g(0.6, 0.06, 0.28);
  };
  A.ecg = (ctx, t, d, o) => {
    const p = clamp(t / d, 0, 1), b0 = o.from ?? 72, b1 = o.to ?? 44;
    ctx.fillStyle = "#020805"; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = "rgba(40,120,70,0.18)"; ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 48) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
    for (let y = 0; y < H; y += 48) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
    // scrolling monitor: the window shows the last `win` seconds; beat spacing follows the falling BPM
    const win = 4.0, x0 = 120, x1 = W - 520, base = 560, amp = 300;
    const phaseAt = (tt) => { const k = (b1 - b0) / d; return (b0 * tt + 0.5 * k * tt * tt) / 60; };   // integral of bpm/60
    ctx.lineWidth = 5; ctx.strokeStyle = "#3dff8a"; ctx.shadowColor = "#3dff8a"; ctx.shadowBlur = 18;
    ctx.beginPath();
    const steps = 1100;
    for (let i = 0; i <= steps; i++) {
      const fx = i / steps, tt = t - (1 - fx) * win, x = lerp(x0, x1, fx);
      const y = tt < 0 ? base : base - ecgWave(phaseAt(tt) % 1) * amp;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    // bright write-head dot
    ctx.stroke(); ctx.shadowBlur = 0;
    // numeric panel
    const bpm = Math.round(lerp(b0, b1, p));
    const beat = phaseAt(t) % 1, flash = Math.exp(-(((beat - 0.36) / 0.05) ** 2));
    ctx.fillStyle = "#3dff8a"; ctx.font = "700 44px Inter, Arial, sans-serif"; ctx.fillText("HR", W - 440, 330);
    ctx.font = "800 210px Inter, Arial, sans-serif"; ctx.fillText(String(bpm), W - 450, 540);
    ctx.font = "700 40px Inter, Arial, sans-serif"; ctx.fillText("bpm", W - 440, 600);
    ctx.fillStyle = `rgba(255,80,90,${0.35 + 0.65 * flash})`; ctx.beginPath(); ctx.arc(W - 150, 315, 22, 0, Math.PI * 2); ctx.fill();
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, W * 0.75);
    vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.7)"); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  };

  // ------------------------------------------------ EEG: 8 channels, beta chaos settling into alpha rhythm
  A.eeg = (ctx, t, d, o) => {
    const p = clamp(t / d, 0, 1), settle = clamp((p - (o.settleAt ?? 0.35)) / 0.4, 0, 1);
    ctx.fillStyle = "#04060c"; ctx.fillRect(0, 0, W, H);
    const labels = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "O1", "O2"], top = 130, gap = 110, R = rng(5);
    const ph = labels.map(() => [R() * 6, R() * 6, R() * 6, R() * 6]);
    for (let c = 0; c < 8; c++) {
      const y0 = top + c * gap;
      ctx.fillStyle = "rgba(160,190,255,0.75)"; ctx.font = "700 30px Inter, Arial, sans-serif"; ctx.fillText(labels[c], 60, y0 + 10);
      ctx.strokeStyle = "rgba(120,150,220,0.12)"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(170, y0); ctx.lineTo(W - 60, y0); ctx.stroke();
      ctx.strokeStyle = settle > 0.5 ? "rgba(120,200,255,0.95)" : "rgba(255,170,90,0.95)"; ctx.lineWidth = 2.6;
      ctx.shadowColor = ctx.strokeStyle; ctx.shadowBlur = 8; ctx.beginPath();
      for (let x = 170; x <= W - 60; x += 3) {
        const tt = t - (W - 60 - x) / 420, [a, b, e, f] = ph[c];
        const beta = Math.sin(tt * 2 * Math.PI * 21 + a) * 0.5 + Math.sin(tt * 2 * Math.PI * 27 + b) * 0.35 + Math.sin(tt * 2 * Math.PI * 15 + e) * 0.3;
        const alpha = Math.sin(tt * 2 * Math.PI * 10 + f) * (c >= 6 ? 1.25 : 0.9);
        const v = lerp(beta * 0.55, alpha * 0.8, settle) * 34;
        if (x === 170) ctx.moveTo(x, y0 + v); else ctx.lineTo(x, y0 + v);
      }
      ctx.stroke(); ctx.shadowBlur = 0;
    }
  };

  window.DOC_ANIMS = A;
})();
