// Plates kit (video/lib/plates): desk scenes for big moments, built from photoreal stills rendered by the props studio
// (video/lib/props, desk mode) with the same camera. Plates stack and crossfade (a screen lights up, a stamp lands), the
// whole stage pushes in slowly, a buzz shakes it, film grain and a light leak keep every frame alive. 2D only, so it
// renders fast and stays sharp (plates are 4K for a 1080p film).
// window.SCENE = { duration, kicker, tag,
//   layers: [{ src, at, fade, out, outFade }],         // full-frame images, stacked in order; at/out in scene seconds
//   cam:    [[t, scale, x, y, dur, ease]],               // stage transform keys (px at 1920×1080, origin centre)
//   shake:  [[t, dur, amp]],                             // buzz: seeded jitter (px)
//   lower:  [{ at, out, k, t }],                         // lower-third kicker + title
//   chips:  [{ at, out, x, y, text, color }] }           // short typed paper chips placed on the desk (2–4 words)
(function () {
  const mulberry32 = (s) => () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const el = (tag, cls, parent, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.textContent = html; parent.appendChild(e); return e; };

  function grainURL(seed) {   // seeded monochrome grain tile
    const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d"), im = g.createImageData(256, 256), r = mulberry32(seed);
    for (let i = 0; i < 256 * 256; i++) { const v = 128 + (r() - 0.5) * 255; im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255; }
    g.putImageData(im, 0, 0); return c.toDataURL();
  }

  window.Plates = {
    run(S, id) {
      const tl = gsap.timeline({ paused: true }); tl.to({}, { duration: S.duration }, 0);
      const stage = document.getElementById("stage"), shake = document.getElementById("shake");
      (S.layers || []).forEach((L, i) => {
        const im = el("img", "plate", stage); im.src = L.src; im.style.zIndex = i;
        const at = L.at || 0;
        if (at > 0 || L.fade) { gsap.set(im, { opacity: 0 }); tl.to(im, { opacity: 1, duration: L.fade || 0.01, ease: "power1.inOut" }, at); }
        if (L.out != null) tl.to(im, { opacity: 0, duration: L.outFade || 0.01, ease: "power1.inOut" }, L.out);
      });
      // camera
      const C = S.cam && S.cam.length ? S.cam : [[0, 1.0, 0, 0], [0, 1.06, 0, 0, S.duration]];
      gsap.set(stage, { scale: C[0][1], x: C[0][2], y: C[0][3], transformOrigin: "50% 50%" });
      C.slice(1).forEach(([t, sc, x, y, d, ease]) => tl.to(stage, { scale: sc, x, y, duration: d || 0.01, ease: ease || (d > 0.5 ? "sine.inOut" : "none") }, t));
      // buzz: seeded jitter, 30 steps a second, settles at the end
      const r = mulberry32(7);
      (S.shake || []).forEach(([t, d, amp]) => { const n = Math.round(d * 30);
        for (let k = 0; k < n; k++) tl.set(shake, { x: (r() - 0.5) * 2 * amp, y: (r() - 0.5) * 2 * amp * 0.6, rotation: (r() - 0.5) * amp * 0.03 }, t + k / 30);
        tl.set(shake, { x: 0, y: 0, rotation: 0 }, t + n / 30); });
      // grain: tile jumps every frame (24 fps look)
      const gr = document.getElementById("grain"); gr.style.backgroundImage = `url(${grainURL(3)})`;
      const rg = mulberry32(11);
      for (let k = 0; k * (1 / 24) < S.duration; k++) tl.set(gr, { backgroundPosition: `${Math.floor(rg() * 256)}px ${Math.floor(rg() * 256)}px` }, k / 24);
      // warm light leak drifting across
      tl.fromTo("#leak", { x: -220, opacity: 0.0 }, { x: 260, opacity: 0.55, duration: S.duration, ease: "sine.inOut" }, 0);
      // lower-thirds
      const lt = document.getElementById("lt");
      (S.lower || []).forEach((L) => { const box = el("div", "lt", lt); el("span", "k", box, L.k || ""); el("span", "t", box, L.t || "");
        gsap.set(box, { opacity: 0 }); tl.fromTo(box.children[0], { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L.at);
        tl.fromTo(box.children[1], { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "expo.out" }, L.at + 0.1);
        tl.set(box, { opacity: 1 }, L.at); if (L.out != null) tl.to(box, { opacity: 0, duration: 0.35 }, L.out); });
      (S.chips || []).forEach((c) => { const ch = el("div", "chip", stage, c.text); ch.style.left = c.x + "px"; ch.style.top = c.y + "px"; ch.style.zIndex = 50;
        if (c.color) ch.style.borderLeftColor = c.color; ch.style.transform = `rotate(${c.rot || -2}deg)`;
        gsap.set(ch, { opacity: 0, y: -30, scale: 1.08 }); tl.to(ch, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, c.at);
        if (c.out != null) tl.to(ch, { opacity: 0, duration: 0.3 }, c.out); });
      const tag = document.getElementById("tag"); if (S.tag) tag.textContent = S.tag; else tag.remove();
      const kick = document.getElementById("kick"); if (S.kicker) kick.textContent = S.kicker; else kick.remove();
      return tl;
    },
  };
})();
