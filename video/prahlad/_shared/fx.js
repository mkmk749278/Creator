// Seeded helpers shared by the documentary inserts. Deterministic: no clocks, no unseeded random.
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
  // Drifting dust particles with depth (size, blur, opacity) added to `tl` for `dur` seconds.
  dust(tl, container, { seed = 1, count = 60, dur = 8 } = {}) {
    const r = FX.rng(seed);
    for (let i = 0; i < count; i++) {
      const el = document.createElement("i");
      const z = r();
      const size = 2 + z * 7;
      el.style.width = el.style.height = size + "px";
      el.style.left = r() * 100 + "%";
      el.style.top = r() * 100 + "%";
      el.style.opacity = (0.15 + z * 0.55).toFixed(2);
      el.style.filter = `blur(${((1 - z) * 2.5).toFixed(1)}px)`;
      container.appendChild(el);
      tl.fromTo(el, { x: 0, y: 0 }, { x: (r() - 0.5) * 140 * (0.4 + z), y: -(30 + r() * 120) * (0.4 + z), duration: dur, ease: "none" }, 0);
    }
  },
  // Slow background drift so no frame is static.
  drift(tl, bg, dur) {
    tl.fromTo(bg, { scale: 1.0, x: 0 }, { scale: 1.06, x: -30, duration: dur, ease: "sine.inOut" }, 0);
  },
};
