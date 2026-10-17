// "The third door" kit (Episode 02, session C). Builds on video/lib/fin (FIN.keys / bind / hook / grain / rng).
// Everything is a pure function of timeline time: per-frame values are computed in FIN hooks driven by the scene's one
// paused timeline (FIN.attach). No clocks, no unseeded random, no state carried between frames.
(function () {
  const IO = {};
  const $ = (id) => document.getElementById(id);
  IO.$ = $;
  const K = FIN.keys;
  IO.K = K;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  IO.clamp = clamp;
  // 0..1 ramp between t0 and t1 with sine easing
  IO.ramp = (t, t0, t1) => { const u = clamp((t - t0) / Math.max(1e-6, t1 - t0)); return 0.5 - 0.5 * Math.cos(Math.PI * u); };
  IO.lin = (t, t0, t1) => clamp((t - t0) / Math.max(1e-6, t1 - t0));

  // seeded paper fibre texture as a data URL (deterministic)
  IO.paperTex = (seed = 11) => {
    const c = document.createElement("canvas"); c.width = c.height = 256;
    const g = c.getContext("2d"), r = FIN.rng(seed), img = g.createImageData(256, 256);
    for (let i = 0; i < img.data.length; i += 4) { const v = 215 + r() * 40; img.data[i] = v; img.data[i + 1] = v - 3; img.data[i + 2] = v - 10; img.data[i + 3] = 255; }
    g.putImageData(img, 0, 0);
    g.globalAlpha = 0.06; g.strokeStyle = "#7a6a50";
    for (let k = 0; k < 90; k++) { g.beginPath(); const x = r() * 256, y = r() * 256; g.moveTo(x, y); g.lineTo(x + (r() - .5) * 40, y + (r() - .5) * 8); g.stroke(); }
    return c.toDataURL();
  };
  IO.texturePapers = () => { const u = IO.paperTex(); document.querySelectorAll(".paper").forEach((p) => {
    const d = document.createElement("div"); d.className = "tex"; d.style.backgroundImage = `url(${u})`; p.prepend(d); }); };

  // atmosphere: plate drift, window light breathing, light-leak sweeps, dust motes, grain
  IO.atmos = (opt = {}) => {
    const D = opt.duration, plate = $("plate-wrap"), key = $("io-key"), leak = $("io-leak"), dust = $("io-dust");
    const r = FIN.rng(opt.seed || 5), motes = [];
    for (let i = 0; i < 26; i++) {
      const m = document.createElement("i"); dust.appendChild(m);
      motes.push({ m, x: r() * 1920, y: r() * 1080, vx: 6 + r() * 14, vy: -4 - r() * 10, ph: r() * 6.28, s: .5 + r() * 1.3, a: .15 + r() * .45 });
    }
    const leaks = opt.leaks || [];
    FIN.grain($("grain"));
    FIN.hook((t) => {
      const u = t / Math.max(1, D);
      if (plate) plate.style.transform = `scale(${1.04 + 0.05 * u}) translate(${(opt.plateDx || -24) * u}px, ${(opt.plateDy || -10) * u}px)`;
      key.style.opacity = (0.85 + 0.15 * Math.sin(t * 0.7)).toFixed(3);
      key.style.transform = `translate(${Math.sin(t * 0.21) * 40}px, ${Math.cos(t * 0.17) * 26}px)`;
      let lo = 0, lx = -900;
      for (const L of leaks) { const p = IO.lin(t, L, L + 1.6); if (p > 0 && p < 1) { lo = Math.sin(Math.PI * p); lx = -900 + p * 2900; } }
      leak.style.opacity = lo.toFixed(3); leak.style.transform = `translateX(${lx}px)`;
      for (const d of motes) {
        const x = (d.x + d.vx * t + Math.sin(t * .6 + d.ph) * 18) % 1960, y = ((d.y + d.vy * t) % 1100 + 1100) % 1100;
        d.m.style.transform = `translate(${x}px, ${y}px) scale(${d.s})`; d.m.style.opacity = (d.a * (0.6 + 0.4 * Math.sin(t * 1.3 + d.ph))).toFixed(3);
      }
    });
  };

  // forensic magnifier over a document page.
  // o: { host, img, w, h, cam: {cx:[[t,v]..], cy, s, r}, lens: {x, y, on, m, R}, hl: [{boxes:[[x0,y0,x1,y1]..], t0, t1, cls}], boxes: [...] }
  IO.docRig = (o) => {
    const host = o.host, cam = document.createElement("div"); cam.className = "rig-cam"; host.appendChild(cam);
    const shadow = document.createElement("div"); shadow.className = "sheet-shadow"; shadow.style.width = o.w + "px"; shadow.style.height = o.h + "px"; cam.appendChild(shadow);
    const mkSheet = () => {
      const s = document.createElement("div"); s.className = "sheet"; s.style.width = o.w + "px"; s.style.height = o.h + "px";
      s.innerHTML = `<img class="pg" src="${o.img}" width="${o.w}" height="${o.h}" alt=""/><div class="warm"></div>`;
      const hls = [];
      for (const h of o.hl || []) {
        const total = h.boxes.reduce((a, b) => a + (b[2] - b[0]), 0); let acc = 0;
        for (const b of h.boxes) {
          const d = document.createElement("div"); d.className = "hl " + (h.cls || "");
          d.style.left = b[0] - 8 + "px"; d.style.top = b[1] - 6 + "px"; d.style.width = b[2] - b[0] + 16 + "px"; d.style.height = b[3] - b[1] + 12 + "px";
          s.appendChild(d); const f0 = acc / total; acc += b[2] - b[0];
          hls.push({ d, h, f0, f1: acc / total });
        }
      }
      return { s, hls };
    };
    const base = mkSheet(); cam.appendChild(base.s);
    const spot = document.createElement("div"); spot.className = "spot"; host.appendChild(spot);
    const L = o.lens || null; let lens, lensRing, handle, inner;
    if (L) {
      lens = document.createElement("div"); lens.className = "lens"; host.appendChild(lens);
      inner = mkSheet(); lens.appendChild(inner.s);
      const gl = document.createElement("div"); gl.className = "glass"; lens.appendChild(gl);
      handle = document.createElement("div"); handle.className = "lens-handle"; host.insertBefore(handle, lens);
      lensRing = document.createElement("div"); lensRing.className = "lens-ring"; host.appendChild(lensRing);
    }
    const f = (k, d) => (k ? K(k) : () => d);
    const CX = f(o.cam.cx), CY = f(o.cam.cy), S = f(o.cam.s), ROT = f(o.cam.r, 0), TX = f(o.cam.tx, 0), TY = f(o.cam.ty, 0);
    const LX = L && f(L.x), LY = L && f(L.y), LON = L && f(L.on, 0), LM = L && f(L.m, 1.8), R = L ? L.R || 210 : 0;
    const paintHl = (hls, t) => { for (const e of hls) {
      const p = (o.hlEase ? IO.ramp : IO.lin)(t, e.h.t0, e.h.t1), q = clamp((p - e.f0) / Math.max(1e-6, e.f1 - e.f0));
      e.d.style.transform = `scaleX(${q.toFixed(4)})`; e.d.style.opacity = q > 0 ? (e.h.out ? 1 - IO.ramp(t, e.h.out, e.h.out + .4) : 1) : 0; } };
    FIN.hook((t) => {
      const cx = CX(t), cy = CY(t), s = S(t), tx = 960 - cx * s + TX(t), ty = 540 - cy * s + TY(t);
      cam.style.transform = `rotate(${ROT(t).toFixed(3)}deg)`;
      const tr = `translate(${tx.toFixed(2)}px, ${ty.toFixed(2)}px) scale(${s.toFixed(5)})`;
      base.s.style.transform = tr; shadow.style.transform = tr; paintHl(base.hls, t);
      if (L) {
        const on = LON(t), lx = LX(t), ly = LY(t), m = LM(t), sx = tx + lx * s, sy = ty + ly * s, rr = R * (0.85 + 0.15 * on);
        const vis = on > 0.01 ? 1 : 0;
        lens.style.cssText = `left:${sx - rr}px; top:${sy - rr}px; width:${2 * rr}px; height:${2 * rr}px; opacity:${on.toFixed(3)}; display:${vis ? "block" : "none"}`;
        inner.s.style.transform = `translate(${(rr - lx * s * m).toFixed(2)}px, ${(rr - ly * s * m).toFixed(2)}px) scale(${(s * m).toFixed(5)})`;
        paintHl(inner.hls, t);
        lensRing.style.cssText = `left:${sx - rr - 16}px; top:${sy - rr - 16}px; width:${2 * rr + 32}px; height:${2 * rr + 32}px; opacity:${on.toFixed(3)}; display:${vis ? "block" : "none"}`;
        handle.style.cssText = `left:${sx + rr * 0.62 - 23}px; top:${sy + rr * 0.62}px; transform: rotate(-45deg); opacity:${on.toFixed(3)}; display:${vis ? "block" : "none"}`;
        spot.style.background = `radial-gradient(circle at ${sx}px ${sy}px, rgba(0,0,0,0) ${rr + 30}px, rgba(5,8,14,${(0.45 * on).toFixed(3)}) ${rr + 420}px)`;
      }
    });
    return { cam };
  };

  window.IO = IO;
})();
