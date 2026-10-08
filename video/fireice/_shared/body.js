// Thermal-camera human figure on a canvas. Body parts are drawn as temperatures (0..1) into a low-resolution
// field, blurred so heat blends like a real thermogram, palette-mapped (ironbow) and masked by a soft silhouette.
// Deterministic: draw(temps, spots, frame) depends only on its arguments (grain is seeded by the frame number).
window.BODY = (() => {
  const STOPS = [[0, [10, 12, 60]], [0.14, [30, 40, 150]], [0.28, [40, 120, 230]], [0.4, [40, 200, 220]], [0.5, [70, 210, 120]],
    [0.6, [230, 225, 60]], [0.72, [255, 160, 40]], [0.84, [240, 70, 40]], [0.94, [255, 180, 150]], [1, [255, 250, 235]]];
  const LUT = new Uint8ClampedArray(256 * 3);
  for (let i = 0; i < 256; i++) {
    const t = i / 255;
    let k = 1;
    while (k < STOPS.length - 1 && STOPS[k][0] < t) k++;
    const [a, ca] = STOPS[k - 1], [b, cb] = STOPS[k], f = (t - a) / (b - a || 1);
    for (let j = 0; j < 3; j++) LUT[i * 3 + j] = ca[j] + (cb[j] - ca[j]) * Math.max(0, Math.min(1, f));
  }
  const color = t => { const i = Math.round(Math.max(0, Math.min(1, t)) * 255) * 3; return `rgb(${LUT[i]},${LUT[i + 1]},${LUT[i + 2]})`; };
  // limbs as tapered chains [[x,y,width],...]; blobs as [x,y,r]
  const STAND = {
    legL: [[-55, -150, 92], [-62, 120, 70], [-66, 395, 50]], legR: [[55, -150, 92], [62, 120, 70], [66, 395, 50]],
    footL: [[-66, 400, 40], [-105, 418, 34]], footR: [[66, 400, 40], [105, 418, 34]],
    hips: [[-70, -150, 110], [70, -150, 110]],
    torso: [[0, -430, 250], [0, -320, 230], [0, -200, 190], [0, -150, 200]],
    shoulders: [[-118, -430, 78], [118, -430, 78]],
    armL: [[-132, -425, 62], [-160, -270, 48], [-178, -105, 40]], armR: [[132, -425, 62], [160, -270, 48], [178, -105, 40]],
    handL: [[-180, -100, 40], [-184, -50, 34]], handR: [[180, -100, 40], [184, -50, 34]],
    neck: [[0, -500, 62], [0, -450, 74]], head: [[0, -585, 112], [0, -545, 118], [0, -515, 92]],
  };
  const SEAT = {
    legL: [[-40, -150, 100], [-245, -100, 84], [30, -62, 66]], legR: [[40, -150, 100], [245, -100, 84], [-30, -62, 66]],
    footL: [[30, -62, 50], [70, -72, 40]], footR: [[-30, -62, 50], [-70, -72, 40]],
    hips: [[-80, -160, 120], [80, -160, 120]],
    torso: [[0, -430, 250], [0, -320, 230], [0, -200, 196], [0, -150, 220]],
    shoulders: [[-118, -430, 78], [118, -430, 78]],
    armL: [[-132, -425, 62], [-172, -290, 48], [-212, -150, 40]], armR: [[132, -425, 62], [172, -290, 48], [212, -150, 40]],
    handL: [[-214, -148, 40], [-226, -112, 36]], handR: [[214, -148, 40], [226, -112, 36]],
    neck: [[0, -500, 62], [0, -450, 74]], head: [[0, -585, 112], [0, -545, 118], [0, -515, 92]],
  };
  function make(canvas, { pose = "stand", x = 960, y = 640, scale = 1, res = 3, blur = 4.5, bg = 0.0 } = {}) {
    const P = pose === "seat" ? SEAT : STAND;
    const W = canvas.width, H = canvas.height, w = Math.ceil(W / res), h = Math.ceil(H / res);
    const ctx = canvas.getContext("2d");
    const mk = () => { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; };
    const tc = mk(), mc = mk(), tb = mk(), mb = mk(), out = mk();
    const tx = tc.getContext("2d"), mx = mc.getContext("2d"), tbx = tb.getContext("2d"), mbx = mb.getContext("2d"), ox = out.getContext("2d");
    const tr = (px, py) => [(x + px * scale) / res, (y + py * scale) / res];
    function chain(g, pts, style) {
      g.strokeStyle = style; g.lineCap = "round"; g.lineJoin = "round";
      for (let i = 1; i < pts.length; i++) {
        const [ax, ay] = tr(pts[i - 1][0], pts[i - 1][1]), [bx, by] = tr(pts[i][0], pts[i][1]);
        const steps = 6;
        for (let s = 0; s < steps; s++) {   // tapered: short segments with interpolated width
          const k0 = s / steps, k1 = (s + 1) / steps, wd = pts[i - 1][2] + (pts[i][2] - pts[i - 1][2]) * (k0 + k1) / 2;
          g.lineWidth = wd * scale / res;
          g.beginPath(); g.moveTo(ax + (bx - ax) * k0, ay + (by - ay) * k0); g.lineTo(ax + (bx - ax) * k1, ay + (by - ay) * k1); g.stroke();
        }
      }
    }
    const order = ["legL", "legR", "footL", "footR", "hips", "armL", "armR", "handL", "handR", "torso", "shoulders", "neck", "head"];
    // temps: {part: 0..1}; spots: [{x, y, r, t}] extra heat sources in body coords (added on top, then blurred)
    function draw(temps, spots = [], frame = 0, opts = {}) {
      tx.clearRect(0, 0, w, h); mx.clearRect(0, 0, w, h);
      tx.fillStyle = "rgb(0,0,0)"; tx.fillRect(0, 0, w, h);
      for (const name of order) {
        const v = Math.round(255 * Math.max(0, Math.min(1, temps[name] ?? temps.default ?? 0.5)));
        chain(tx, P[name], `rgb(${v},${v},${v})`);
        chain(mx, P[name], "#fff");
      }
      for (const s of spots) {
        const [sx, sy] = tr(s.x, s.y), rr = s.r * scale / res, v = Math.round(255 * Math.max(0, Math.min(1, s.t)));
        const g = tx.createRadialGradient(sx, sy, 0, sx, sy, rr);
        g.addColorStop(0, `rgba(${v},${v},${v},${s.a ?? 1})`); g.addColorStop(1, `rgba(${v},${v},${v},0)`);
        tx.fillStyle = g; tx.beginPath(); tx.arc(sx, sy, rr, 0, Math.PI * 2); tx.fill();
      }
      tbx.clearRect(0, 0, w, h); tbx.filter = `blur(${blur}px)`; tbx.drawImage(tc, 0, 0); tbx.filter = "none";
      mbx.clearRect(0, 0, w, h); mbx.filter = `blur(${Math.max(0.8, blur * 0.3)}px)`; mbx.drawImage(mc, 0, 0); mbx.filter = "none";
      const T = tbx.getImageData(0, 0, w, h).data, M = mbx.getImageData(0, 0, w, h).data;
      const img = ox.createImageData(w, h), d = img.data;
      let a = (frame * 2654435761) >>> 0;
      const grain = opts.grain ?? 10;
      for (let i = 0; i < w * h; i++) {
        a = (a ^ (a << 13)) >>> 0; a = (a ^ (a >>> 17)) >>> 0; a = (a ^ (a << 5)) >>> 0;
        const m = M[i * 4] / 255;
        const tv = Math.max(0, Math.min(255, T[i * 4] / Math.max(0.35, m) + ((a & 255) / 255 - 0.5) * grain));
        const k = Math.round(tv) * 3;
        d[i * 4] = LUT[k]; d[i * 4 + 1] = LUT[k + 1]; d[i * 4 + 2] = LUT[k + 2]; d[i * 4 + 3] = Math.round(255 * Math.min(1, m * 1.15));
      }
      ox.putImageData(img, 0, 0);
      ctx.clearRect(0, 0, W, H);
      ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
      ctx.drawImage(out, 0, 0, W, H);
    }
    // body coords -> canvas pixels (for placing HTML/SVG overlays)
    const at = (px, py) => [x + px * scale, y + py * scale];
    return { draw, at };
  }
  return { make, color };
})();
