// Finance explainer kit (video/lib/fin): helpers shared by the money-mechanics scenes.
// Everything is a pure function of timeline time: counters and other per-frame values are computed in FIN.render(t),
// which the scene's single paused timeline calls from onUpdate (tl.call does not run on render seeks).
(function () {
  const FIN = {};

  // ₹ in Indian grouping: 30000 -> ₹30,000; 2481.4 -> ₹2,481.40 (dec = 2)
  FIN.inr = (v, dec = 0) => (v < 0 ? "−" : "") + "₹" + Math.abs(v).toLocaleString("en-IN", { minimumFractionDigits: dec, maximumFractionDigits: dec });

  // seeded RNG (mulberry32), never Math.random
  FIN.rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };

  // piecewise value over time: keys = [[t, v], ...] (sorted); eased between keys (sine in-out), held outside
  FIN.keys = (keys) => (t) => {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [t1, v1] = keys[i], [t0, v0] = keys[i - 1];
      if (t <= t1) { const u = (t - t0) / Math.max(1e-6, t1 - t0); return v0 + (v1 - v0) * (0.5 - 0.5 * Math.cos(Math.PI * u)); }
    }
    return keys[keys.length - 1][1];
  };

  // per-frame text bindings: FIN.bind(el, t => value, v => text)
  const binds = [], hooks = [];
  FIN.bind = (el, fn, fmt = (v) => String(v)) => binds.push({ el, fn, fmt, last: null });
  FIN.hook = (fn) => hooks.push(fn);   // any other per-frame drawing: fn(t)
  FIN.render = (t) => {
    for (const b of binds) { const s = b.fmt(b.fn(t)); if (s !== b.last) { b.el.textContent = s; b.last = s; } }
    for (const h of hooks) h(t);
  };

  // film grain: one seeded noise tile, shifted per frame (24 steps a second, cycle of 7)
  FIN.grain = (canvas, seed = 7) => {
    const g = canvas.getContext("2d"), w = canvas.width, h = canvas.height, img = g.createImageData(w, h), r = FIN.rng(seed);
    for (let i = 0; i < img.data.length; i += 4) { const v = 90 + r() * 120; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
    g.putImageData(img, 0, 0);
    FIN.hook((t) => { const f = Math.floor(t * 24) % 7; canvas.style.transform = `translate(${(f * 13) % 40 - 20}px, ${(f * 7) % 30 - 15}px) scale(4)`; });
  };

  // attach to the scene's timeline; render the first frame now
  FIN.attach = (tl) => { tl.eventCallback("onUpdate", () => FIN.render(tl.time())); FIN.render(0); };

  // small line icons (stroke = currentColor)
  const P = {
    check: '<path d="M10 25 L20 35 L38 13" />',
    cross: '<path d="M13 13 L35 35 M35 13 L13 35" />',
    clock: '<circle cx="24" cy="24" r="17" /><path d="M24 14 V24 L31 29" />',
    cal: '<rect x="8" y="11" width="32" height="29" rx="4" /><path d="M8 19 H40 M16 7 V14 M32 7 V14" />',
    card: '<rect x="5" y="12" width="38" height="25" rx="4" /><path d="M5 19 H43 M11 30 H20" />',
    warn: '<path d="M24 7 L43 40 H5 Z" /><path d="M24 19 V28 M24 33 V34" />',
    bill: '<path d="M12 5 H36 V43 L31 39 L26 43 L21 39 L16 43 L12 39 Z" /><path d="M18 15 H30 M18 22 H30 M18 29 H26" />',
    pay: '<rect x="5" y="12" width="38" height="25" rx="4" /><path d="M16 25 L22 31 L33 19" />',
  };
  FIN.icon = (name) => `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round">${P[name]}</svg>`;

  window.FIN = FIN;
})();
