// Whiteboard engine: real marker handwriting for HyperFrames scenes (video/lib/whiteboard, PLAYBOOK §4a-3, §9.1).
// Every glyph comes from a single-line pen font (wb-fonts.js), so text is *written* stroke by stroke: the ink grows
// along each stroke at pen speed, the marker's nib rides the exact point, and the pen lifts and travels between
// strokes. Shapes (underline, circle, arrow, box, tick, cross, strike, bars) and a duster wipe use the same machinery.
// Default font: "tech" (marker print). Everything is a pure function of the timeline's time: render(t) recomputes every stroke and the pen from scratch.
//
//   const b = WB.board(document.getElementById("stage"), { seed: 3 });
//   b.write("You paid ₹1,500", { x: 260, y: 330, size: 110, color: "green", at: 0.4 });
//   b.circle(1300, 470, 300, 95, { color: "red", at: 4.2 });
//   b.attach(tl);          // after all steps; drives ink, pen and duster from tl's time
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const INK = { black: "#1b2433", blue: "#1f4fb5", red: "#c8102e", green: "#13804a", orange: "#d4700a", purple: "#6a3fb0" };
  const ink = (c) => INK[c] || c || INK.black;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ss = (t) => t * t * (3 - 2 * t);
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  function rng(seed) { let s = (seed * 2654435761) % 2147483647 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }

  // ---- polyline helpers (lengths and points are computed here, not by the DOM: exact and seek-safe) ----
  function poly(pts) {
    const seg = [0];
    for (let i = 2; i < pts.length; i += 2) seg.push(seg[seg.length - 1] + Math.hypot(pts[i] - pts[i - 2], pts[i + 1] - pts[i - 1]));
    return { pts, seg, len: seg[seg.length - 1] };
  }
  function at(p, d) {
    const { pts, seg } = p;
    if (d <= 0) return [pts[0], pts[1], pts[2] - pts[0], pts[3] - pts[1]];
    for (let i = 1; i < seg.length; i++) {
      if (seg[i] >= d) {
        const u = (d - seg[i - 1]) / (seg[i] - seg[i - 1] || 1), j = (i - 1) * 2;
        return [pts[j] + (pts[j + 2] - pts[j]) * u, pts[j + 1] + (pts[j + 3] - pts[j + 1]) * u, pts[j + 2] - pts[j], pts[j + 3] - pts[j + 1]];
      }
    }
    const n = pts.length;
    return [pts[n - 2], pts[n - 1], pts[n - 2] - pts[n - 4], pts[n - 1] - pts[n - 3]];
  }
  const dOf = (pts) => "M" + pts.map((v, i) => (i % 2 ? "," : i ? " L" : "") + v.toFixed(1)).join("").replace("M,", "M");

  // ---- the board ----
  function board(stage, opts = {}) {
    const o = Object.assign({ seed: 1, surface: true, tray: true, ghost: true, w: 1920, h: 1080 }, opts);
    const r = rng(o.seed);
    stage.classList.add("wb-stage");
    if (o.surface) {
      const s = document.createElement("div"); s.className = "wb-surface"; stage.appendChild(s);
      if (o.ghost) { // faint traces of earlier, erased lessons: seeded smudges
        const c = document.createElement("canvas"); c.width = 900; c.height = 470; c.className = "wb-smudge"; s.appendChild(c);
        const x = c.getContext("2d");
        for (let i = 0; i < 26; i++) {
          const cx = r() * 900, cy = r() * 470, rad = 30 + r() * 110, g = x.createRadialGradient(cx, cy, 0, cx, cy, rad);
          g.addColorStop(0, `rgba(70,85,105,${0.025 + r() * 0.03})`); g.addColorStop(1, "rgba(70,85,105,0)");
          x.fillStyle = g; x.fillRect(cx - rad, cy - rad, rad * 2, rad * 2);
        }
      }
    }
    const svg = el("svg", { class: "wb-ink", viewBox: `0 0 ${o.w} ${o.h}` }, stage);
    const layer = el("g", {}, svg);
    if (o.tray) { // aluminium tray with a spare marker and the duster resting on it
      const t = el("g", { class: "wb-tray" }, svg);
      el("rect", { x: 70, y: 1008, width: 1780, height: 22, rx: 6, fill: "#aeb4bc" }, t);
      el("rect", { x: 70, y: 1008, width: 1780, height: 6, rx: 3, fill: "#d3d8de" }, t);
      el("rect", { x: 1240, y: 986, width: 150, height: 22, rx: 9, fill: INK.blue }, t);
      el("rect", { x: 1218, y: 989, width: 26, height: 16, rx: 4, fill: "#f2f2f2" }, t);
    }
    const pen = el("g", { class: "wb-pen" }, svg);   // nib at (0,0), body up and to the right
    el("rect", { x: 30, y: -12, width: 210, height: 24, rx: 12, fill: "rgba(20,30,45,.10)", transform: "translate(14 22) rotate(-34)", class: "wb-pen-shadow" }, pen);
    const pbody = el("g", { transform: "rotate(-34)" }, pen);
    el("path", { d: "M0 0 L22 -9 L22 9 Z", fill: "#222833" }, pbody);
    el("rect", { x: 22, y: -13, width: 34, height: 26, rx: 3, fill: "#f4f4f2", stroke: "#a9afb7", "stroke-width": 1.5 }, pbody);
    const pcol = el("rect", { x: 56, y: -16, width: 190, height: 32, rx: 11, fill: INK.black }, pbody);
    el("rect", { x: 78, y: -12, width: 140, height: 7, rx: 3.5, fill: "rgba(255,255,255,.32)" }, pbody);
    el("rect", { x: 236, y: -14, width: 18, height: 28, rx: 6, fill: "rgba(0,0,0,.25)" }, pbody);
    const duster = el("g", { class: "wb-duster" }, svg);
    el("rect", { x: -95, y: -42, width: 190, height: 84, rx: 14, fill: "#3c4452" }, duster);
    el("rect", { x: -95, y: 22, width: 190, height: 20, rx: 8, fill: "#e9e4d6" }, duster);
    el("rect", { x: -70, y: -34, width: 140, height: 10, rx: 5, fill: "rgba(255,255,255,.15)" }, duster);

    const B = { stage, svg, layer, items: [], erasers: [], pen, pcol, duster, rnd: r, last: 0 };

    // add one drawable item made of polylines (already in board coordinates)
    function add(lines, op) {
      const color = ink(op.color), size = op.size || 90;
      const width = op.width || Math.max(4, size * 0.085);
      const speed = op.speed || size * 17;             // px of ink per second (a brisk teacher's hand)
      const g = el("g", { class: "wb-item" }, layer);
      const strokes = [];
      // steps never overlap: one marker, one hand. A requested `at` earlier than the previous step's end waits for it.
      let t = op.at != null ? Math.max(op.at, B.last + 0.08) : B.last + 0.25, prev = null;
      if (op.at != null && op.at < B.last + 0.08) console.warn(`WB: step at ${op.at}s waits for the previous one (ends ${B.last.toFixed(2)}s)`);
      const t0 = t;
      for (const pts of lines) {
        if (pts.length < 4) continue;
        const p = poly(pts);
        if (prev) { const gap = Math.hypot(pts[0] - prev[0], pts[1] - prev[1]); t += 0.025 + gap / (speed * 4); }
        const dur = Math.max(0.035, p.len / speed);
        const path = el("path", { d: dOf(pts), fill: "none", stroke: color, "stroke-width": width, "stroke-linecap": "round",
          "stroke-linejoin": "round", "stroke-dasharray": `${(p.len + 2).toFixed(1)} ${(p.len + 2).toFixed(1)}`, opacity: 0 }, g);
        strokes.push({ p, path, t0: t, t1: t + dur });
        t += dur; prev = [pts[pts.length - 2], pts[pts.length - 1]];
      }
      if (op.dur && strokes.length) { // fit the writing to a given duration (e.g. the VO phrase)
        const k = op.dur / (t - t0);
        for (const s of strokes) { s.t0 = t0 + (s.t0 - t0) * k; s.t1 = t0 + (s.t1 - t0) * k; }
        t = t0 + op.dur;
      }
      const xs = lines.flat().filter((_, i) => i % 2 === 0), ys = lines.flat().filter((_, i) => i % 2 === 1);
      const item = { strokes, color, t0, t1: t, g, size, op, box: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)] };
      B.items.push(item); B.last = t;
      return item;
    }

    // handwriting: lay out pen glyphs, flip y, add a hand-made wobble per glyph
    B.measure = (text, op = {}) => {
      const F = WB_FONTS[op.font || "tech"], k = (op.size || 90) / F.cap;
      let w = 0; for (const ch of text) w += ((F.glyphs[ch] || F.glyphs["?"] || { w: F.def }).w) * k * (op.track || 1);
      return w;
    };
    B.write = (text, op = {}) => {
      // keep the line on the board: shrink the size if the text would run past the right edge (default x limit 1780)
      if (op.size !== 0) {
        const want = op.size || 90, w = B.measure(text, Object.assign({}, op, { size: want }));
        const left = op.x != null ? op.x : (op.cx != null ? op.cx - w / 2 : 200), room = (op.right || 1780) - left;
        if (w > room) op = Object.assign({}, op, { size: Math.floor(want * room / w) });
      }
      const F = WB_FONTS[op.font || "tech"], size = op.size || 90, k = size / F.cap, track = op.track || 1;
      const wob = op.wobble == null ? 1 : op.wobble;
      let x = op.x != null ? op.x : (op.cx != null ? op.cx - B.measure(text, op) / 2 : 200);
      const y0 = op.y != null ? op.y : 300, lines = [];
      let i = 0;
      for (const ch of text) {
        const g = F.glyphs[ch] || F.glyphs["?"];
        const dy = (B.rnd() - 0.5) * size * 0.05 * wob, rot = (B.rnd() - 0.5) * 0.06 * wob, sc = 1 + (B.rnd() - 0.5) * 0.05 * wob;
        const cxg = g.w * 0.5, cr = Math.cos(rot), sr = Math.sin(rot);
        for (const s of g.s) {
          const pts = [];
          for (let j = 0; j < s.length; j += 2) {
            const gx = (s[j] - cxg) * sc, gy = s[j + 1] * sc;
            const rx = gx * cr - gy * sr + cxg, ry = gx * sr + gy * cr;
            pts.push(x + rx * k, y0 - ry * k + dy + (op.slope || 0) * (x - (op.x || 0)));
          }
          lines.push(pts);
        }
        x += g.w * k * track; i++;
      }
      return add(lines, Object.assign({ size }, op));
    };

    // shapes (hand-drawn: slight wobble and overshoot)
    const wav = (x1, y1, x2, y2, amp, n = 16) => {
      const pts = [];
      for (let i = 0; i <= n; i++) { const u = i / n; pts.push(x1 + (x2 - x1) * u, y1 + (y2 - y1) * u + Math.sin(u * Math.PI * 1.3 + B.rnd()) * amp); }
      return pts;
    };
    // shapes can target the last item: underline/circle/strike/box with the first argument "last"
    const lastBox = (pad = 0) => { const b = B.items[B.items.length - 1].box; return [b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad]; };
    B.underlineLast = (op = {}) => { const b = lastBox(); return B.underline(b[0], b[2], b[3] + 18, op); };
    B.circleLast = (op = {}) => { const b = lastBox(); return B.circle((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, (b[2] - b[0]) / 2 + 70, (b[3] - b[1]) / 2 + 42, op); };
    B.strikeLast = (op = {}) => { const b = lastBox(); return B.strike(b[0] - 10, b[2] + 10, (b[1] + b[3]) / 2, op); };
    B.boxLast = (op = {}) => { const b = lastBox(24); return B.box(b[0], b[1], b[2] - b[0], b[3] - b[1], op); };
    B.underline = (x1, x2, y, op = {}) => add([wav(x1, y, x2, y - 4, 4)], Object.assign({ size: 70, speed: 1800 }, op));
    B.strike = (x1, x2, y, op = {}) => add([wav(x1, y, x2, y + 6, 3)], Object.assign({ size: 70, color: "red", speed: 2200 }, op));
    B.circle = (cx, cy, rx, ry, op = {}) => {
      const pts = [], a0 = -2.6 + B.rnd() * 0.3, sweep = Math.PI * 2 * 1.12, n = 64;
      for (let i = 0; i <= n; i++) {
        const u = i / n, a = a0 + sweep * u, k = 1 + 0.06 * Math.sin(u * 5.1 + 1) + 0.05 * u;
        pts.push(cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k);
      }
      return add([pts], Object.assign({ size: 80, speed: 2400 }, op));
    };
    B.arrow = (x1, y1, x2, y2, op = {}) => {
      const bend = op.bend == null ? 0.18 : op.bend, mx = (x1 + x2) / 2 - (y2 - y1) * bend, my = (y1 + y2) / 2 + (x2 - x1) * bend;
      const pts = [];
      for (let i = 0; i <= 24; i++) { const u = i / 24; pts.push((1 - u) * (1 - u) * x1 + 2 * (1 - u) * u * mx + u * u * x2, (1 - u) * (1 - u) * y1 + 2 * (1 - u) * u * my + u * u * y2); }
      const ang = Math.atan2(y2 - my, x2 - mx), hl = op.head || 46;
      const h1 = [x2 + Math.cos(ang + 2.6) * hl, y2 + Math.sin(ang + 2.6) * hl, x2, y2, x2 + Math.cos(ang - 2.6) * hl, y2 + Math.sin(ang - 2.6) * hl];
      return add([pts, h1], Object.assign({ size: 100, speed: 2000 }, op));
    };
    B.line = (pts, op = {}) => add([pts], Object.assign({ size: 80, speed: 1800 }, op));
    B.box = (x, y, w, h, op = {}) => add([[x, y, x + w, y + 2, x + w - 2, y + h, x + 3, y + h - 2, x - 2, y + 8]], Object.assign({ size: 80, speed: 2200 }, op));
    B.tick = (x, y, s = 60, op = {}) => add([[x, y, x + s * 0.35, y + s * 0.4, x + s, y - s * 0.55]], Object.assign({ size: 90, color: "green", speed: 900 }, op));
    B.cross = (x, y, s = 60, op = {}) => add([[x, y, x + s, y + s], [x + s, y, x, y + s]], Object.assign({ size: 90, color: "red", speed: 900 }, op));
    // marker bar: outline + hatching (for hand-drawn charts); grows bottom-up as it is drawn
    B.bar = (x, base, w, h, op = {}) => {
      const lines = [[x, base, x, base - h, x + w, base - h, x + w, base]];
      for (let yy = base - 16; yy > base - h + 8; yy -= 22) lines.push([x + 6, yy, x + w - 6, yy - 14]);
      return add(lines, Object.assign({ size: 80, speed: 2600 }, op));
    };
    // duster wipe over a region (default: whole board); ink under the duster's path fades as it passes
    B.erase = (op = {}) => {
      const reg = op.region || [60, 40, 1800, 950], dur = op.dur || 1.1;
      const at = op.at != null ? Math.max(op.at, B.last + 0.15) : B.last + 0.3;
      B.erasers.push({ reg, t0: at, t1: at + dur });
      B.last = at + dur;
      return { t0: at, t1: at + dur };
    };

    // ---- render at time t (pure) ----
    B.render = (t) => {
      let active = null, near = null;
      for (const it of B.items) {
        // eraser fade for this item
        let fade = 1;
        for (const e of B.erasers) {
          const [rx, ry, rw, rh] = e.reg, cx = (it.box[0] + it.box[2]) / 2, cy = (it.box[1] + it.box[3]) / 2;
          if (it.t0 >= e.t0 || cx < rx || cx > rx + rw || cy < ry || cy > ry + rh || t < e.t0) continue; // only ink already on the board
          const sweepX = rx + rw * clamp((t - e.t0) / (e.t1 - e.t0), 0, 1);
          fade = Math.min(fade, 1 - clamp((sweepX - it.box[0]) / Math.max(60, it.box[2] - it.box[0]), 0, 1));
        }
        it.g.setAttribute("opacity", fade.toFixed(3));
        for (let si = 0; si < it.strokes.length; si++) {
          const s = it.strokes[si], u = clamp((t - s.t0) / (s.t1 - s.t0), 0, 1);
          const f = u * 0.75 + ss(u) * 0.25, drawn = s.p.len * f;
          s.path.setAttribute("stroke-dashoffset", (s.p.len + 2 - drawn).toFixed(1));
          s.path.setAttribute("opacity", drawn > 0.5 ? 1 : 0);
          if (t >= s.t0 && t <= s.t1) active = { it, s, d: drawn };
          else if (!active && si + 1 < it.strokes.length && t > s.t1 && t < it.strokes[si + 1].t0) {
            const nx = it.strokes[si + 1], w = (t - s.t1) / (nx.t0 - s.t1);
            const a = at(s.p, s.p.len), b = at(nx.p, 0);
            near = { it, x: a[0] + (b[0] - a[0]) * ss(w), y: a[1] + (b[1] - a[1]) * ss(w) - Math.sin(Math.PI * w) * it.size * 0.18, lift: Math.sin(Math.PI * w) };
          }
        }
        if (!active && !near) {
          if (t >= it.t0 - 0.35 && t < it.t0) { // pen comes in to the first stroke
            const w = ss((t - (it.t0 - 0.35)) / 0.35), b = at(it.strokes[0].p, 0);
            near = { it, x: b[0] + (1 - w) * 520, y: b[1] + (1 - w) * 380, lift: 1 - w };
          } else if (t > it.t1 && t <= it.t1 + 0.35) { // and leaves after the last
            const w = ss((t - it.t1) / 0.35), ls = it.strokes[it.strokes.length - 1], a = at(ls.p, ls.p.len);
            near = { it, x: a[0] + w * 520, y: a[1] + w * 380, lift: w };
          }
        }
      }
      if (active) {
        const [x, y] = at(active.s.p, active.d);
        B.pen.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
        B.pen.setAttribute("opacity", 1); B.pcol.setAttribute("fill", active.it.color);
        B.pen.firstChild.setAttribute("opacity", 1);
      } else if (near) {
        B.pen.setAttribute("transform", `translate(${near.x.toFixed(1)} ${near.y.toFixed(1)}) scale(${(1 + 0.05 * near.lift).toFixed(3)})`);
        B.pen.setAttribute("opacity", 1); B.pcol.setAttribute("fill", near.it.color);
        B.pen.firstChild.setAttribute("opacity", (1 - 0.6 * near.lift).toFixed(2));
      } else B.pen.setAttribute("opacity", 0);
      // duster
      const e = B.erasers.find((e) => t >= e.t0 - 0.3 && t <= e.t1 + 0.3);
      if (e) {
        const [rx, ry, rw, rh] = e.reg, u = clamp((t - e.t0) / (e.t1 - e.t0), 0, 1);
        const x = rx + rw * u, y = ry + rh * (0.5 + 0.38 * Math.sin(u * Math.PI * 7));
        const inOut = t < e.t0 ? (e.t0 - t) / 0.3 : t > e.t1 ? (t - e.t1) / 0.3 : 0;
        B.duster.setAttribute("transform", `translate(${x.toFixed(1)} ${(y + inOut * 500).toFixed(1)}) rotate(${(Math.sin(u * 40) * 6).toFixed(1)})`);
        B.duster.setAttribute("opacity", 1);
      } else B.duster.setAttribute("opacity", 0);
    };
    // drive from a GSAP timeline: runs after the timeline's children have rendered, on every seek
    B.attach = (tl) => {
      const prev = tl.eventCallback("onUpdate");
      tl.eventCallback("onUpdate", function () { if (prev) prev.apply(this, arguments); B.render(tl.time()); });
      B.render(0);
      return B;
    };
    return B;
  }
  window.WB = { board, INK };
})();
