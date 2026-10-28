// Pharma film runtime (copied from the rare earth film, video/rem): every element is emitted statically by build/make_film.py; this adds seek-safe tweens.
// Shots get a slow camera move; anything with data-at fades/pops in at that time and out at data-to;
// counters, taps, flicker and the phone's drift are pure functions of time (no repeat: -1, no randomness).
(function () {
  const E = "power3.out";
  const MOVES = {
    in: [{ scale: 1.0 }, { scale: 1.08 }], out: [{ scale: 1.1 }, { scale: 1.02 }],
    left: [{ scale: 1.08, xPercent: 2 }, { scale: 1.08, xPercent: -2 }], right: [{ scale: 1.08, xPercent: -2 }, { scale: 1.08, xPercent: 2 }],
    up: [{ scale: 1.08, yPercent: 2 }, { scale: 1.08, yPercent: -2 }], push: [{ scale: 1.0 }, { scale: 1.05 }],
    slow: [{ scale: 1.02 }, { scale: 1.06 }], none: [{ scale: 1.0 }, { scale: 1.0 }],
    zoomhome: [{ scale: 1.7 }, { scale: 1.9 }], zoomboard: [{ scale: 2.15 }, { scale: 2.35 }],
    crop: [{ scale: 1.26 }, { scale: 1.33 }],   // hides burned-in subtitles / tickers at the bottom (origin set per shot)
  };
  const fmt = (v, pre, suf, dec) => pre + (dec ? v.toFixed(dec) : Math.round(v).toLocaleString("en-IN")) + suf;
  window.PHA_animate = function (tl, D) {
    // ---- base shots
    document.querySelectorAll(".shot").forEach((sh) => {
      const timed = sh.dataset.start != null;
      const t = timed ? +sh.dataset.start : +sh.dataset.vs, d = timed ? +sh.dataset.duration : +sh.dataset.vd;
      if (!timed) { tl.set(sh, { visibility: "hidden" }, 0); tl.set(sh, { visibility: "visible" }, t); tl.set(sh, { visibility: "hidden" }, t + d); }
      sh.querySelectorAll(".m").forEach((m) => {
        const mv = MOVES[m.dataset.move || "push"];
        if (m.dataset.origin) m.style.transformOrigin = m.dataset.origin;
        tl.fromTo(m, mv[0], Object.assign({ duration: d, ease: "none", immediateRender: false }, mv[1]), t);
      });
      const fl = sh.dataset.flick;   // alternate .m.a / .m.b every `flick` seconds (the ₹0 / ₹840 doubt)
      if (fl) {
        const a = sh.querySelector(".m.a"), b = sh.querySelector(".m.b"); let on = false;
        for (let x = t; x < t + d - 1e-3; x += +fl) { tl.set(a, { visibility: on ? "hidden" : "visible" }, x); tl.set(b, { visibility: on ? "visible" : "hidden" }, x); on = !on; }
      }
    });
    document.querySelectorAll(".vover").forEach((o) => {
      const t = +o.dataset.vs, d = +o.dataset.vd;
      tl.set(o, { visibility: "hidden" }, 0); tl.set(o, { visibility: "visible" }, t); tl.set(o, { visibility: "hidden" }, t + d);
    });
    // ---- timed overlays
    document.querySelectorAll("[data-at]").forEach((el) => {
      const a = +el.dataset.at, b = el.dataset.to != null ? +el.dataset.to : null, fx = el.dataset.fx || "fade";
      // a window shorter than fade-in + fade-out squeezes both, or the fade-out lands first and the item never leaves
      const d = b != null ? Math.min(+(el.dataset.d || 0.35), Math.max(0.04, (b - a) / 2)) : +(el.dataset.d || 0.35);
      const fo = b != null ? Math.min(0.25, Math.max(0.04, (b - a) / 2)) : 0.25;
      tl.set(el, { autoAlpha: 0 }, 0);
      const go = (from, to) => tl.fromTo(el, Object.assign({ autoAlpha: 0 }, from), Object.assign({ autoAlpha: 1, duration: d, ease: E, immediateRender: false }, to), a);
      if (fx === "cut") tl.set(el, { autoAlpha: 1 }, a);
      else if (fx === "pop") go({ scale: 0.7 }, { scale: 1, ease: "back.out(2)" });
      else if (fx === "up") go({ y: 34 }, { y: 0 });
      else if (fx === "down") go({ y: -34 }, { y: 0 });
      else if (fx === "left") go({ x: -46 }, { x: 0 });
      else if (fx === "right") go({ x: 46 }, { x: 0 });
      else if (fx === "stamp") go({ scale: 2.4 }, { scale: 1, ease: "power4.in", duration: d });
      else if (fx === "grow") { tl.set(el, { autoAlpha: 1, scaleX: 0 }, a); tl.fromTo(el, { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power2.inOut", immediateRender: false }, a); }
      else if (fx === "fall") go({ y: -420 }, { y: 0, ease: "bounce.out", duration: Math.max(d, 0.7) });
      else if (fx === "rise") go({ y: 140 }, { y: 0, duration: Math.max(d, 0.6) });
      else if (fx === "tap") { tl.set(el, { autoAlpha: 1, scale: 0.3 }, a); tl.fromTo(el, { scale: 0.3, opacity: 0.9 }, { scale: 1.5, opacity: 0, duration: 0.55, ease: "power2.out", immediateRender: false }, a); }
      else if (fx === "flash") { tl.set(el, { autoAlpha: 1 }, a); tl.fromTo(el, { opacity: 1 }, { opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, a); }
      else go({}, {});
      if (b != null && fx !== "tap" && fx !== "flash") {
        if (el.dataset.cut != null) tl.set(el, { autoAlpha: 0 }, b);
        else tl.to(el, { autoAlpha: 0, duration: fo, ease: "power1.in" }, Math.max(0, b - fo));
      }
      if (el.dataset.pulse) {   // finite pulse (glow) between at and to
        const p = +el.dataset.pulse, end = b != null ? b : D;
        for (let x = a + d, i = 0; x < end - p; x += p, i++) tl.to(el, { opacity: i % 2 ? 1 : 0.45, duration: p, ease: "sine.inOut" }, x);
      }
    });
    // ---- counters: data-count="from,to,start,dur" data-pre data-suf
    document.querySelectorAll("[data-count]").forEach((el) => {
      const [f, to, s, d] = el.dataset.count.split(",").map(Number), pre = el.dataset.pre || "", suf = el.dataset.suf || "", dec = +(el.dataset.dec || 0), o = { v: f };
      el.textContent = fmt(f, pre, suf, dec);
      tl.fromTo(o, { v: f }, { v: to, duration: d, ease: el.dataset.ease || "none", immediateRender: false, onUpdate: () => { el.textContent = fmt(o.v, pre, suf, dec); } }, s);
    });
    // ---- the phone drifts like it's held (sine keyframes over its whole on-screen time)
    document.querySelectorAll(".phone[data-at]").forEach((p) => {
      const a = +p.dataset.at, b = p.dataset.to != null ? +p.dataset.to : D, n = Math.max(1, Math.floor((b - a) / 1.6));
      for (let i = 0; i < n; i++) tl.to(p, { y: i % 2 ? 0 : -9, rotation: (+(p.dataset.rot || 0)) + (i % 2 ? 0.4 : -0.4), duration: (b - a) / n, ease: "sine.inOut" }, a + i * (b - a) / n);
    });
    // ---- grain: shifted from time only
    const g = document.getElementById("grain");
    if (g) {
      const x = g.getContext("2d"); let s = 11; const r = () => (s = (s * 16807) % 2147483647) / 2147483647;
      const im = x.createImageData(500, 290); for (let i = 0; i < im.data.length; i += 4) { const v = 70 + r() * 185; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
      x.putImageData(im, 0, 0);
      const st = { v: 0 };
      tl.fromTo(st, { v: 0 }, { v: D, duration: D, ease: "none", immediateRender: false, onUpdate: () => {
        const f = Math.floor(st.v * 24) % 7; g.style.transform = `translate(${(f * 13) % 40 - 20}px, ${(f * 7) % 30 - 15}px) scale(4)`; } }, 0);
    }
  };
})();
