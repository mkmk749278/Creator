// Documentary runtime: all shots/overlays are emitted statically by build.mjs.
// DOC_animate(tl) adds seek-safe tweens: Ken Burns on every photo, slow push on video,
// lower-third reveals, the corner timer, and the end card. Deterministic, no repeats.
(function () {
  const E = "power3.out";
  const mmss = (s) => { s = Math.max(0, Math.round(s)); return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); };
  const MOVES = {
    in: [{ scale: 1.0 }, { scale: 1.12 }],
    out: [{ scale: 1.14 }, { scale: 1.02 }],
    left: [{ scale: 1.12, xPercent: 3 }, { scale: 1.12, xPercent: -3 }],
    right: [{ scale: 1.12, xPercent: -3 }, { scale: 1.12, xPercent: 3 }],
    up: [{ scale: 1.12, yPercent: 3 }, { scale: 1.12, yPercent: -3 }],
    face: [{ scale: 1.25 }, { scale: 1.45 }],          // tight push on a face
    pan: [{ scale: 1.25, xPercent: 9 }, { scale: 1.25, xPercent: -9 }], // wide horizontal pan (paintings)
    push: [{ scale: 1.0 }, { scale: 1.07 }],          // video: gentle push-in
    none: [{ scale: 1.0 }, { scale: 1.0 }],           // licensed video with burned-in label
  };
  window.DOC_animate = function (tl, opts) {
    document.querySelectorAll(".shot").forEach((sh) => {
      const timed = sh.dataset.start != null;
      const t = timed ? +sh.dataset.start : +sh.dataset.vs, d = timed ? +sh.dataset.duration : +sh.dataset.vd;
      if (!timed) {  // video shot: untimed wrapper, shown only during its slot
        tl.set(sh, { visibility: "hidden" }, 0);
        tl.set(sh, { visibility: "visible" }, t);
        tl.set(sh, { visibility: "hidden" }, t + d);
      }
      sh.querySelectorAll(".m").forEach((m) => {
        const mv = MOVES[m.dataset.move || sh.dataset.move || (m.tagName === "VIDEO" ? "push" : "in")];
        if (m.dataset.origin) m.style.transformOrigin = m.dataset.origin;
        tl.fromTo(m, mv[0], Object.assign({ duration: d, ease: "none", immediateRender: false }, mv[1]), t);
      });
      // dissolve in (optional) — hard cuts by default
      if (sh.dataset.fade) tl.fromTo(sh, { opacity: 0 }, { opacity: 1, duration: +sh.dataset.fade, ease: "none", immediateRender: false }, t);
      const tag = sh.querySelector(".tag");
      if (tag) tl.fromTo(tag, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: E, immediateRender: false }, t + 0.3);
    });
    document.querySelectorAll(".vover").forEach((o) => {
      const t = +o.dataset.vs, d = +o.dataset.vd;
      tl.set(o, { visibility: "hidden" }, 0);
      tl.set(o, { visibility: "visible" }, t);
      tl.set(o, { visibility: "hidden" }, t + d);
    });
    document.querySelectorAll(".l3").forEach((l) => {
      const t = +l.dataset.start, d = +l.dataset.duration;
      tl.fromTo(l, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5, ease: E, immediateRender: false }, t);
      tl.fromTo(l.querySelector(".bar"), { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: E, immediateRender: false }, t);
      tl.to(l, { opacity: 0, duration: 0.4, ease: "power1.in" }, t + d - 0.4);
    });
    // Corner timer: opts.timer = {keys: [[t, clockSec], ...], windows: [[a, b], ...]} in part time
    const tm = document.querySelector(".timer");
    if (tm && opts && opts.timer) {
      const v = tm.querySelector(".v"), keys = opts.timer.keys;
      for (let i = 0; i < keys.length - 1; i++) {
        const [a0, c0] = keys[i], [a1, c1] = keys[i + 1], o = { v: c0 };
        tl.call(() => { v.textContent = mmss(c0); }, null, Math.max(0, a0 - 0.01));
        if (c1 !== c0) tl.fromTo(o, { v: c0 }, { v: c1, duration: a1 - a0, ease: "none", immediateRender: false, onUpdate: () => { v.textContent = mmss(o.v); } }, a0);
      }
      (opts.timer.windows || []).forEach(([a, b]) => {
        tl.fromTo(tm, { opacity: 0 }, { opacity: 1, duration: 0.35, immediateRender: false }, a);
        tl.to(tm, { opacity: 0, duration: 0.35 }, b - 0.35);
      });
      (opts.timer.alarm || []).forEach(([a, b]) => {
        const n = Math.max(1, Math.floor((b - a) / 0.6));
        tl.fromTo(tm.querySelector(".dot"), { scale: 1 }, { scale: 1.6, duration: 0.3, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut", immediateRender: false }, a);
      });
    }
    const ec = document.querySelector(".endcard");
    if (ec) tl.fromTo(ec, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.8, ease: E, immediateRender: false }, +ec.dataset.start);
  };
})();
