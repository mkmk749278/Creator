// Seeded helpers for the Fire and Ice inserts. Deterministic: every value is a function of the timeline time.
window.FX = {
  rng(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  },
  // Drifting particles (dust, snow or embers) with depth. dir: -1 rises, +1 falls.
  dust(tl, container, { seed = 1, count = 60, dur = 8, dir = -1, spread = 140, travel = 120, size = 7 } = {}) {
    const r = FX.rng(seed);
    for (let i = 0; i < count; i++) {
      const el = document.createElement("i");
      const z = r();
      const s = 2 + z * size;
      el.style.width = el.style.height = s + "px";
      el.style.left = r() * 100 + "%";
      el.style.top = r() * 100 + "%";
      el.style.opacity = (0.15 + z * 0.6).toFixed(2);
      el.style.filter = `blur(${((1 - z) * 2.5).toFixed(1)}px)`;
      container.appendChild(el);
      tl.fromTo(el, { x: 0, y: 0 }, { x: (r() - 0.5) * spread * (0.4 + z), y: dir * (30 + r() * travel) * (0.4 + z), duration: dur, ease: "none" }, 0);
    }
  },
  drift(tl, bg, dur, amt = 0.06) {
    tl.fromTo(bg, { scale: 1.0, x: 0 }, { scale: 1 + amt, x: -30, duration: dur, ease: "sine.inOut" }, 0);
  },
  // Draw an SVG path on over `dur` seconds starting at `at`.
  draw(tl, el, at, dur, ease = "power1.inOut") {
    const p = typeof el === "string" ? document.querySelector(el) : el;
    const L = p.getTotalLength();
    p.style.strokeDasharray = L;
    tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur, ease }, at);
  },
  // Count a number up/down into `el` (tabular), using a proxy tween (render-seek safe).
  count(tl, el, from, to, at, dur, { dec = 0, prefix = "", suffix = "", ease = "power1.inOut" } = {}) {
    const node = typeof el === "string" ? document.querySelector(el) : el;
    const o = { v: from };
    node.textContent = prefix + from.toFixed(dec) + suffix;
    tl.fromTo(o, { v: from }, { v: to, duration: dur, ease, onUpdate: () => { node.textContent = prefix + o.v.toFixed(dec) + suffix; } }, at);
  },
};
// One master proxy tween drives `fn(t)` for the whole scene, so every seek redraws from time alone.
FX.clock = (tl, dur, fn) => { const c = { t: 0 }; tl.fromTo(c, { t: 0 }, { t: dur, duration: dur, ease: "none", onUpdate: () => fn(c.t) }, 0); fn(0); };
FX.ss = (t, a, b) => { const x = Math.max(0, Math.min(1, (t - a) / (b - a))); return x * x * (3 - 2 * x); };  // smoothstep 0..1 between a and b
FX.lerp = (a, b, k) => a + (b - a) * k;
