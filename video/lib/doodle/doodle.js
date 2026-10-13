// Doodle kit (video/lib/doodle): sketched objects that draw on or pop in, for explaining beats (owner, 2026-10-12:
// desk for big moments, doodle for explaining). Objects and metaphors, short typed labels, no handwriting, no characters.
// Everything is scheduled on one paused GSAP timeline (seek-safe). Rough.js shapes use fixed seeds (deterministic).
// Scene format (params.js): window.SCENE = { duration, tag, kicker, items: [ { kind, x, y, s, rot, at, dur, in, exit,
// moves: [{ at, dur, x, y, s, rot, ease }], ...kind props } ] }. Sound cues are written by the generator (SCENE.sfx).
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const C = { ink: "#1f2430", red: "#d62839", green: "#1f9d6b", blue: "#2563eb", amber: "#e09f1f", paper: "#fbf8f1",
    dim: "#6b6f78", yel: "#f6c453", note: "#fff3b0" };
  const col = (c) => C[c] || c || C.ink;
  let seed = 11, DUR = 10;
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };

  function Kit(svg, tl) {
    const rc = rough.svg(svg);
    const R = (o = {}) => Object.assign({ seed: seed++, roughness: 1.3, bowing: 1.1, stroke: C.ink, strokeWidth: 3.2 }, o);
    const add = (g, node) => (g.appendChild(node), node);
    const text = (g, str, x, y, size, color, o = {}) => {
      const t = el("text", { x, y, "font-size": size, fill: col(color), class: o.mono ? "mono" : "lbl", "text-anchor": o.anchor || "start" }, g);
      t.textContent = str;
      if (o.outline) { t.setAttribute("stroke", C.ink); t.setAttribute("stroke-width", o.outline); t.setAttribute("paint-order", "stroke"); t.setAttribute("stroke-linejoin", "round"); }
      return t;
    };
    const tw = (str, size, mono) => str.length * size * (mono ? 0.62 : 0.6);   // width estimate (fonts may load late)

    // ---------- objects: draw into g at local origin ----------
    const K = {
      label(g, it) {   // typed label, optional highlighter swipe behind
        const size = it.size || 56, w = tw(it.text, size, it.mono);
        const ax = it.anchor === "middle" ? -w / 2 : it.anchor === "end" ? -w : 0;
        if (it.hl) { const r = el("rect", { x: ax - 12, y: -size * 0.82, width: w + 24, height: size * 1.12, rx: 6, fill: col(it.hl), opacity: 0.8, class: "hl" }, g); r.dataset.hl = 1; }
        text(g, it.text, 0, 0, size, it.color, { mono: it.mono, anchor: it.anchor });
      },
      tag(g, it) {     // price tag with a string hole
        const size = it.size || 64, w = Math.max(160, it.text.length * size * 0.68 + 80), h = size * 1.5;
        add(g, rc.path(`M 0 ${h / 2} L 34 0 L ${w} 0 L ${w} ${h} L 34 ${h} Z`, R({ fill: col(it.color), fillStyle: "solid", stroke: C.ink })));
        add(g, rc.circle(30, h / 2, 14, R({ fill: C.paper, fillStyle: "solid", strokeWidth: 2 })));
        text(g, it.text, 52, h / 2 + size * 0.36, size, "#fff");
        if (it.sub) text(g, it.sub, 52, h + 34, 26, it.color, { mono: true });
      },
      sticky(g, it) {  // numbered sticky note
        const w = it.w || 300, h = it.h || 220;
        add(g, rc.rectangle(0, 0, w, h, R({ fill: C.note, fillStyle: "solid", strokeWidth: 2.4, stroke: C.paperEdge || C.ink })));
        text(g, String(it.n), 24, 84, 76, it.color || "green");
        (it.lines || []).forEach((s, i) => text(g, s, 24, 136 + i * 40, 34, C.paperInk || "ink"));
      },
      badge(g, it) {   // tick or cross in a circle, label to the right
        const ok = it.ok !== false, c = ok ? C.green : C.red;
        add(g, rc.circle(0, 0, 76, R({ stroke: c, strokeWidth: 4, fill: ok ? "#d9f2e6" : "#fbdde1", fillStyle: "solid" })));
        add(g, ok ? rc.linearPath([[-18, 2], [-4, 18], [22, -16]], R({ stroke: c, strokeWidth: 7 }))
                  : rc.path("M -16 -16 L 16 16 M 16 -16 L -16 16", R({ stroke: c, strokeWidth: 7 })));
        if (it.text) text(g, it.text, 60, 18, it.size || 52, ok ? "green" : "red");
      },
      bill(g, it) {    // a printed bill with rows; row hlRow gets a highlighter at hlAt
        const w = it.w || 640, rows = it.rows || [], h = it.h || 150 + rows.length * 92;
        add(g, rc.rectangle(0, 0, w, h, R({ fill: "#ffffff", fillStyle: "solid", strokeWidth: 2.6 })));
        add(g, rc.rectangle(0, 0, w, 80, R({ fill: "#1b2a41", fillStyle: "solid", strokeWidth: 2 })));
        text(g, it.title || "CARD BILL", 28, 54, 36, "#fff", { mono: true });
        rows.forEach(([a, b, c], i) => {
          const y = 150 + i * 92;
          if (it.hlRow === i) { const r = el("rect", { x: 14, y: y - 50, width: w - 28, height: 68, fill: C.yel, opacity: 0.75, rx: 6 }, g); r.dataset.hlrow = 1; }
          text(g, a, 28, y, 38, c || "ink");
          text(g, b, w - 28, y, 44, c || "ink", { anchor: "end" });
        });
      },
      coins(g, it) {   // a stack of n coins
        const n = it.n || 10, r = it.r || 70;
        for (let i = 0; i < n; i++) add(g, rc.ellipse(0, -i * 14, r * 2, r * 0.7, R({ fill: it.color ? col(it.color) : "#e8c35a", fillStyle: "solid", strokeWidth: 2.4, seed: 500 + i })));
        if (it.text) text(g, it.text, 0, -n * 14 - r * 0.45 - 18, it.size || 64, it.textColor || it.color || "ink", { anchor: "middle" });
        if (it.label) text(g, it.label, 0, r * 0.35 + (it.labelDy || 56), 34, it.labelColor || (it.color && it.color[0] !== "#" ? it.color : "ink"), { anchor: "middle", mono: true });
      },
      card(g, it) {    // credit card
        const w = 420, h = 264;
        add(g, rc.rectangle(0, 0, w, h, R({ fill: col(it.color || "#3b5bdb"), fillStyle: "hachure", hachureGap: 10, fillWeight: 1.6, strokeWidth: 3 })));
        add(g, rc.rectangle(34, 70, 66, 50, R({ fill: C.yel, fillStyle: "solid", strokeWidth: 2 })));
        text(g, "•••• 4821", 34, 200, 40, "ink", { mono: true });
        if (it.text) text(g, it.text, w / 2, h + 60, 40, it.textColor || "ink", { anchor: "middle", mono: true });
      },
      pos(g, it) {     // card machine
        add(g, rc.rectangle(0, 0, 200, 300, R({ fill: "#cfd6e4", fillStyle: "solid" })));
        add(g, rc.rectangle(24, 24, 152, 90, R({ fill: "#eef6ff", fillStyle: "solid", strokeWidth: 2 })));
        text(g, it.screen || "₹5,000", 100, 82, 34, "ink", { anchor: "middle" });
        for (let i = 0; i < 9; i++) add(g, rc.rectangle(34 + (i % 3) * 46, 136 + Math.floor(i / 3) * 46, 36, 34, R({ strokeWidth: 1.6 })));
      },
      phone(g, it) {
        add(g, rc.rectangle(0, 0, 260, 480, R({ fill: "#2b2f3a", fillStyle: "solid", strokeWidth: 3 })));
        add(g, rc.rectangle(16, 30, 228, 400, R({ fill: "#f7f8fb", fillStyle: "solid", strokeWidth: 1.6 })));
        (it.lines || []).forEach((s, i) => text(g, s, 130, 110 + i * 54, i ? 32 : 40, i ? "dim" : "ink", { anchor: "middle" }));
        (it.apps || []).forEach((a, i) => { const x = 40 + (i % 3) * 66, y = 250 + Math.floor(i / 3) * 70;
          add(g, rc.rectangle(x, y, 52, 52, R({ fill: a.color || "#c9cbd3", fillStyle: "solid", strokeWidth: 1.8 }))); });
      },
      calendar(g, it) {   // month page; marks = [{day, color, text}] ; band = {from, to, color}
        const cw = 92, ch = 70, w = cw * 7, h = 110 + ch * 5;
        add(g, rc.rectangle(0, 0, w, h, R({ fill: "#ffffff", fillStyle: "solid" })));
        add(g, rc.rectangle(0, 0, w, 90, R({ fill: C.red, fillStyle: "solid", strokeWidth: 2 })));
        text(g, it.title || "NOVEMBER", w / 2, 62, 46, "#fff", { anchor: "middle", mono: true });
        const pos = (d) => [((d - 1) % 7) * cw + 10, 110 + Math.floor((d - 1) / 7) * ch + 44];
        if (it.band) { const bg = el("g", { class: "band" }, g);   // one strip per week row, so a long span covers the month
          for (let d = it.band.from; d <= it.band.to; d++) { const [x, y] = pos(d);
            el("rect", { x: x - 8, y: y - 40, width: cw - 2, height: 54, rx: 8, fill: col(it.band.color || "green"), opacity: 0.32 }, bg); } }
        for (let d = 1; d <= (it.days || 30); d++) { const [x, y] = pos(d); text(g, String(d), x, y, 30, C.paperDim || "dim", { mono: true }); }
        (it.marks || []).forEach((m) => { const [x, y] = pos(m.day);
          add(g, rc.circle(x + 20, y - 12, 68, R({ stroke: col(m.color || "red"), strokeWidth: 4 })));
          if (m.text) { text(g, m.text, x + 20, h + 46, 38, m.color || "red", { anchor: "middle", mono: true });
            add(g, rc.line(x + 20, y + 22, x + 20, h + 10, R({ stroke: col(m.color || "red"), strokeWidth: 2 }))); } });
      },
      meter(g, it) {   // gauge with a needle (rotated by the scene's 'needle' keys)
        add(g, rc.arc(0, 0, 360, 360, Math.PI, Math.PI * 2, false, R({ strokeWidth: 4 })));
        add(g, rc.arc(0, 0, 360, 360, Math.PI * 1.6, Math.PI * 2, false, R({ stroke: C.red, strokeWidth: 10 })));
        const nd = el("g", { class: "needle" }, g);
        add(nd, rc.line(0, 0, 0, -150, R({ strokeWidth: 6, stroke: C.red })));
        add(g, rc.circle(0, 0, 30, R({ fill: C.ink, fillStyle: "solid" })));
        if (it.text) text(g, it.text, 0, 80, 40, "red", { anchor: "middle", mono: true });
      },
      toggle(g, it) {  // a big switch; knob slides to ON at onAt
        add(g, rc.rectangle(0, 0, 260, 120, R({ fill: "#e3e5ea", fillStyle: "solid" })));
        const on = el("rect", { x: 4, y: 4, width: 252, height: 112, rx: 54, fill: C.red, opacity: 0, class: "on" }, g);
        const knob = el("g", { class: "knob" }, g); add(knob, rc.circle(60, 60, 92, R({ fill: "#ffffff", fillStyle: "solid" })));
        text(g, "OFF", 20, 170, 34, "dim", { mono: true }); text(g, "ON", 210, 170, 34, "red", { mono: true });
        if (it.text) text(g, it.text, 130, 236, 40, "red", { anchor: "middle" });
      },
      net(g, it) {     // safety net
        add(g, rc.line(0, 0, 0, 200, R())); add(g, rc.line(520, 0, 520, 200, R()));
        add(g, rc.path("M 0 20 C 120 160, 400 160, 520 20", R({ strokeWidth: 3 })));
        for (let i = 1; i < 8; i++) add(g, rc.line(i * 65, 20, i * 65, 120 - Math.abs(4 - i) * 12, R({ strokeWidth: 1.6 })));
        add(g, rc.path("M 0 60 C 120 150, 400 150, 520 60", R({ strokeWidth: 1.6 })));
        if (it.text) text(g, it.text, 260, 250, 44, "ink", { anchor: "middle" });
      },
      scale(g, it) {   // balance: beam rotates by 'tilt' keys (class beam)
        add(g, rc.line(0, -20, 0, 260, R({ strokeWidth: 5 })));
        add(g, rc.path("M -110 300 L 110 300 L 0 250 Z", R({ fill: "#cfd6e4", fillStyle: "solid" })));
        const beam = el("g", { class: "beam" }, g);
        add(beam, rc.line(-330, 0, 330, 0, R({ strokeWidth: 6 })));
        [[-330, it.left], [330, it.right]].forEach(([x, p]) => {
          add(beam, rc.line(x, 0, x - 90, 150, R({ strokeWidth: 2 }))); add(beam, rc.line(x, 0, x + 90, 150, R({ strokeWidth: 2 })));
          add(beam, rc.path(`M ${x - 120} 150 C ${x - 80} 200, ${x + 80} 200, ${x + 120} 150 Z`, R({ fill: "#e9e4d8", fillStyle: "solid" })));
          if (p) { text(beam, p[0], x, 132, 54, p[2] || "ink", { anchor: "middle" }); text(beam, p[1], x, 240, 28, p[2] || "ink", { anchor: "middle", mono: true }); }
        });
      },
      bars(g, it) {    // bars = [{x, h, color, top, label}] from baseline y=0
        (it.bars || []).forEach((b, i) => { const bg = el("g", { class: "bar", "data-i": i }, g);
          add(bg, rc.rectangle(b.x, -b.h, it.w || 200, b.h, R({ fill: col(b.color), fillStyle: "hachure", hachureGap: 9, fillWeight: 2 })));
          if (b.top) text(bg, b.top, b.x + (it.w || 200) / 2, -b.h - 24, 52, b.color, { anchor: "middle" });
          if (b.label) text(g, b.label, b.x + (it.w || 200) / 2, 52, 30, "dim", { anchor: "middle", mono: true }); });
        add(g, rc.line(-40, 0, (it.bars || []).length * 320, 0, R({ strokeWidth: 3 })));
      },
      arrow(g, it) {   // from (0,0) to (dx, dy) with bend
        const [dx, dy] = it.to, b = it.bend || 0, mx = dx / 2 - dy * b, my = dy / 2 + dx * b;
        add(g, rc.path(`M 0 0 Q ${mx} ${my} ${dx} ${dy}`, R({ stroke: col(it.color), strokeWidth: 5 })));
        const a = Math.atan2(dy - my, dx - mx), L = 34;
        add(g, rc.linearPath([[dx - L * Math.cos(a - 0.45), dy - L * Math.sin(a - 0.45)], [dx, dy], [dx - L * Math.cos(a + 0.45), dy - L * Math.sin(a + 0.45)]], R({ stroke: col(it.color), strokeWidth: 5 })));
      },
      loop(g, it) {    // circular arrows (rotation), spun by the scene
        const r = it.r || 230, sp = el("g", { class: "spin" }, g);
        for (let k = 0; k < 3; k++) { const a0 = k * 2.094 + 0.25, a1 = a0 + 1.6;
          add(sp, rc.arc(0, 0, r * 2, r * 2, a0, a1, false, R({ stroke: col(it.color || "red"), strokeWidth: 5 })));
          const ax = r * Math.cos(a1), ay = r * Math.sin(a1), t = a1 + Math.PI / 2;
          add(sp, rc.linearPath([[ax - 30 * Math.cos(t - 0.5), ay - 30 * Math.sin(t - 0.5)], [ax, ay], [ax - 30 * Math.cos(t + 0.5), ay - 30 * Math.sin(t + 0.5)]], R({ stroke: col(it.color || "red"), strokeWidth: 5 }))); }
      },
      box(g, it) {     // a cardboard box with a label (the loan)
        const w = it.w || 300, h = it.h || 220;
        add(g, rc.rectangle(0, 0, w, h, R({ fill: "#d9b382", fillStyle: "hachure", hachureGap: 12, fillWeight: 1.4 })));
        add(g, rc.line(0, 40, w, 40, R({ strokeWidth: 2 })));
        text(g, it.text || "LOAN", w / 2, h / 2 + 40, it.size || 52, it.color || "ink", { anchor: "middle", outline: 0 });
        if (it.sub) text(g, it.sub, w / 2, h + 50, 32, it.subColor || "dim", { anchor: "middle", mono: true });
      },
      stamp(g, it) {   // rubber-stamp text, rotated
        const size = it.size || 64, w = tw(it.text, size, true) + 60;
        add(g, rc.rectangle(-w / 2, -size, w, size * 1.5, R({ stroke: col(it.color || "red"), strokeWidth: 6, roughness: 2 })));
        text(g, it.text, 0, size * 0.18, size, it.color || "red", { anchor: "middle", mono: true });
      },
      contact(g, it) { // generic avatar card (an icon, not a character)
        add(g, rc.rectangle(0, 0, 240, 280, R({ fill: "#ffffff", fillStyle: "solid" })));
        add(g, rc.circle(120, 96, 100, R({ fill: "#cfd6e4", fillStyle: "solid" })));
        add(g, rc.path("M 50 220 C 60 150, 180 150, 190 220 Z", R({ fill: "#cfd6e4", fillStyle: "solid" })));
        text(g, it.text || "FRIEND", 120, 262, 32, it.color || "blue", { anchor: "middle", mono: true });
      },
      house(g, it) {
        add(g, rc.path("M 0 120 L 150 0 L 300 120", R({ strokeWidth: 4 })));
        add(g, rc.rectangle(30, 120, 240, 180, R({ fill: "#f1d9b5", fillStyle: "hachure", hachureGap: 12 })));
        add(g, rc.rectangle(120, 200, 64, 100, R({ fill: "#8a5a3a", fillStyle: "solid" })));
        if (it.text) text(g, it.text, 150, 350, 32, it.color || "ink", { anchor: "middle", mono: true });
      },
      slider(g, it) {  // payment slider: red zone below the minimum, knob moves by 'knob' keys
        const w = it.w || 900;
        add(g, rc.rectangle(0, 0, w, 40, R({ fill: "#e3e5ea", fillStyle: "solid" })));
        add(g, rc.rectangle(0, 0, w * 0.08, 40, R({ fill: C.red, fillStyle: "hachure", hachureGap: 7 })));
        add(g, rc.rectangle(w * 0.08, 0, w * 0.92, 40, R({ fill: C.green, fillStyle: "hachure", hachureGap: 12, fillWeight: 1.2 })));
        text(g, "MIN", w * 0.08, 90, 30, "red", { anchor: "middle", mono: true }); text(g, "FULL BILL", w, 90, 30, "green", { anchor: "end", mono: true });
        const k = el("g", { class: "knob" }, g); add(k, rc.circle(0, 20, 70, R({ fill: "#ffffff", fillStyle: "solid", strokeWidth: 3 })));
      },
      seesaw(g, it) {  // lever (class beam) with two end labels
        add(g, rc.path("M -60 120 L 60 120 L 0 20 Z", R({ fill: "#cfd6e4", fillStyle: "solid" })));
        const beam = el("g", { class: "beam" }, g);
        add(beam, rc.rectangle(-420, 0, 840, 22, R({ fill: "#d9b382", fillStyle: "solid" })));
        text(beam, it.left || "", -330, -30, 46, it.leftColor || "green", { anchor: "middle" });
        text(beam, it.right || "", 330, -30, 46, it.rightColor || "red", { anchor: "middle" });
      },
      pin(g, it) {
        add(g, rc.path("M 0 0 C -40 -40, -40 -100, 0 -100 C 40 -100, 40 -40, 0 0 Z", R({ fill: col(it.color || "red"), fillStyle: "solid" })));
        if (it.text) { const w = it.text.length * 34 * 0.69 + 26;   // label on a paper chip to the right of the head
          el("rect", { x: 40, y: -92, width: w, height: 46, rx: 8, fill: "#fbf8f1", stroke: col(it.color || "red"), "stroke-width": 2 }, g);
          text(g, it.text, 50, -58, 34, it.color || "red", { mono: true }); }
      },
      cross(g, it) { const s = it.size || 120; add(g, rc.path(`M ${-s / 2} ${-s / 2} L ${s / 2} ${s / 2} M ${s / 2} ${-s / 2} L ${-s / 2} ${s / 2}`, R({ stroke: C.red, strokeWidth: 9, roughness: 1.8 }))); },
      ring(g, it) { add(g, rc.ellipse(0, 0, it.w || 400, it.h || 260, R({ stroke: col(it.color || "red"), strokeWidth: 6, roughness: 2.2 }))); },
      strike(g, it) { add(g, rc.line(0, 0, it.w || 500, 0, R({ stroke: C.red, strokeWidth: 8, roughness: 1.6 }))); },
      path(g, it) {    // any SVG path in page px (maps: build/map_aptg.json), drawn on with a light hachure fill
        add(g, rc.path(it.d, R({ stroke: col(it.color || "ink"), strokeWidth: it.sw || 2.6, roughness: it.rough ?? 0.5, bowing: 0.2,
          fill: it.fill ? col(it.fill) : undefined, fillStyle: it.fillStyle || "hachure", hachureGap: it.gap || 14, fillWeight: 1.1 })));
        if (it.label) text(g, it.label, it.lx || 0, it.ly || 0, it.size || 34, it.labelColor || "dim", { mono: true, anchor: "middle" });
      },
      dash(g, it) {    // dashed route from (0,0) to `to`, with an optional mid label
        const [dx, dy] = it.to; const p = el("path", { d: `M 0 0 Q ${dx / 2 - dy * (it.bend || 0)} ${dy / 2 + dx * (it.bend || 0)} ${dx} ${dy}`, fill: "none",
          stroke: col(it.color || "red"), "stroke-width": 5, "stroke-dasharray": "14 12", "stroke-linecap": "round" }, g);
        if (it.text) text(g, it.text, dx / 2 + (it.tx || 0), dy / 2 + (it.ty || -20), it.size || 36, it.color || "red", { anchor: "middle", mono: true });
      },
      split(g, it) {   // one bar split into parts [{f, color, label}], drawn left to right
        const W2 = it.w || 900, h = it.h || 110; let x = 0;
        (it.parts || []).forEach((pt, i) => { const w = W2 * pt.f; const pg = el("g", { class: "part", "data-i": i }, g);
          add(pg, rc.rectangle(x, 0, w, h, R({ fill: col(pt.color), fillStyle: "hachure", hachureGap: 9, fillWeight: 2.2 })));
          if (pt.label) text(pg, pt.label, x + w / 2, h + 50, 34, pt.color, { anchor: "middle", mono: true });
          if (pt.top) text(pg, pt.top, x + w / 2, -26, 56, pt.color, { anchor: "middle" }); x += w; });
      },
      counter(g, it) {  // a number that counts from `from` to `to` between at+0.1 and at+count (₹ and Indian grouping)
        const t = text(g, "", 0, 0, it.size || 96, it.color, { anchor: it.anchor });
        t.classList.add("counter"); t.dataset.fmt = it.fmt || "rs";
        if (it.label) text(g, it.label, it.anchor === "middle" ? 0 : 4, (it.size || 96) * 0.5 + 18, 30, it.labelColor || "dim", { mono: true, anchor: it.anchor });
      },
      photo(g, it) {   // photoreal prop still (video/lib/props, alpha PNG with its own shadow); w,h in page px
        const fl = el("g", { class: "float" }, g);
        el("image", { href: it.src, x: 0, y: 0, width: it.w, height: it.h, preserveAspectRatio: "xMidYMid meet" }, fl);
      },
      calc(g, it) {
        add(g, rc.rectangle(0, 0, 260, 380, R({ fill: "#2b2f3a", fillStyle: "solid" })));
        add(g, rc.rectangle(20, 24, 220, 80, R({ fill: "#dfe8d0", fillStyle: "solid", strokeWidth: 2 })));
        text(g, it.screen || "45%", 220, 84, 46, "ink", { anchor: "end", mono: true });
        for (let i = 0; i < 12; i++) add(g, rc.rectangle(26 + (i % 3) * 72, 130 + Math.floor(i / 3) * 60, 60, 46, R({ fill: "#e3e5ea", fillStyle: "solid", strokeWidth: 1.4 })));
      },
    };
    const DRAWN = new Set(["path", "split", "bill", "coins", "card", "pos", "phone", "calendar", "meter", "toggle", "net", "scale", "bars", "arrow", "loop", "box", "contact", "house", "slider", "seesaw", "calc", "ring", "strike", "cross"]);

    // ---------- animation helpers ----------
    function drawOn(node, t, dur) {
      const ps = [...node.querySelectorAll("path")].filter((p) => (p.getAttribute("stroke") || "none") !== "none");
      const L = ps.map((p) => p.getTotalLength()), tot = L.reduce((a, b) => a + b, 0) || 1; let acc = 0;
      ps.forEach((p, i) => { p.style.strokeDasharray = L[i] + 1; gsap.set(p, { strokeDashoffset: L[i] + 1 });
        tl.to(p, { strokeDashoffset: 0, duration: Math.max(0.02, dur * L[i] / tot), ease: "none" }, t + dur * acc / tot); acc += L[i]; });
      node.querySelectorAll("path[fill]:not([fill=none]), g.band").forEach((p) => { gsap.set(p, { opacity: 0 }); tl.to(p, { opacity: 1, duration: 0.25 }, t + dur * 0.75); });
      node.querySelectorAll("text").forEach((x) => { gsap.set(x, { opacity: 0 }); tl.to(x, { opacity: 1, duration: 0.3 }, t + dur * 0.7); });
    }

    function place(it) {
      const outer = el("g", {}, svg), inner = el("g", {}, outer);
      gsap.set(outer, { x: it.x || 0, y: it.y || 0, rotation: it.rot || 0, scale: it.s || 1, transformOrigin: "0px 0px" });
      K[it.kind](inner, it);
      const t = it.at || 0, how = it.in || (DRAWN.has(it.kind) ? "draw" : "pop");
      if (how === "draw") { gsap.set(inner, { opacity: 1 }); drawOn(inner, t, it.dur || 0.8); }
      else if (how === "pop") { gsap.set(inner, { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }); tl.to(inner, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.2)" }, t); }
      else if (how === "stamp") { gsap.set(inner, { opacity: 0, scale: 1.8, transformOrigin: "50% 50%" }); tl.to(inner, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }, t); }
      else if (how === "drop") { const op = it.opaque ? 1 : 0;   // set down on the page (opaque: already visible on the cut)
        gsap.set(inner, { opacity: op, y: -70, scale: 1.07, rotation: it.dropRot ?? -4, transformOrigin: "50% 50%" });
        if (!op) tl.to(inner, { opacity: 1, duration: 0.25, ease: "none" }, t); tl.to(inner, { y: 0, scale: 1, rotation: 0, duration: 0.75, ease: "power3.out" }, t); }
      else if (how === "fade") { gsap.set(inner, { opacity: 0 }); tl.to(inner, { opacity: 1, duration: it.fade || 0.5, ease: "none" }, t); }
      else if (how === "slide") { gsap.set(inner, { opacity: 0, x: it.from || -160 }); tl.to(inner, { opacity: 1, x: 0, duration: 0.6, ease: "expo.out" }, t); }
      const hl = inner.querySelector("rect.hl"); if (hl) { gsap.set(hl, { scaleX: 0, transformOrigin: "0% 50%" }); tl.to(hl, { scaleX: 1, duration: 0.4, ease: "power2.out" }, t + 0.15); }
      const hr = inner.querySelector("rect[data-hlrow]"); if (hr) { gsap.set(hr, { scaleX: 0, transformOrigin: "0% 50%" }); tl.to(hr, { scaleX: 1, duration: 0.45, ease: "power2.out" }, it.hlAt != null ? it.hlAt : t + 0.6); }
      (it.moves || []).forEach((m) => tl.to(outer, { x: m.x != null ? m.x : undefined, y: m.y != null ? m.y : undefined, scale: m.s != null ? m.s : undefined,
        rotation: m.rot != null ? m.rot : undefined, opacity: m.o != null ? m.o : undefined, duration: m.dur || 0.6, ease: m.ease || "power3.inOut" }, m.at));
      // kind-specific motion keys
      const keys = (sel, prop, list, origin) => { const n = inner.querySelector(sel); if (!n || !list) return; gsap.set(n, { [prop]: list[0][1], transformOrigin: origin || "0px 0px" });
        list.slice(1).forEach(([at, v, d]) => tl.to(n, { [prop]: v, duration: d || 0.8, ease: "power2.inOut" }, at)); };
      keys(".needle", "rotation", it.needle, "50% 100%");
      keys(".beam", "rotation", it.tilt, "50% 0%");
      keys(".spin", "rotation", it.spin, "50% 50%");
      keys(".knob", "x", it.knob);
      if (it.kind === "toggle" && it.onAt != null) { const k = inner.querySelector(".knob"), on = inner.querySelector("rect.on");
        tl.to(k, { x: 140, duration: 0.25, ease: "back.out(2)" }, it.onAt); tl.to(on, { opacity: 0.85, duration: 0.2 }, it.onAt); }
      if (it.kind === "bars") inner.querySelectorAll("g.bar").forEach((b) => { const i = +b.dataset.i, at = (it.grow || [])[i];
        if (at == null) return; gsap.set(b, { scaleY: 0, opacity: 0, transformOrigin: "50% 100%" }); tl.to(b, { scaleY: 1, opacity: 1, duration: 0.7, ease: "back.out(1.4)" }, at); });
      if (it.bandShatterAt != null) { const b = inner.querySelector("g.band"); if (b) tl.to(b, { opacity: 0, scaleX: 0.2, duration: 0.35, ease: "power2.in", transformOrigin: "50% 50%" }, it.bandShatterAt); }
      if (it.bandAt != null) { const b = inner.querySelector("g.band"); if (b) { tl.set(b, { opacity: 0 }, 0); tl.fromTo(b, { opacity: 0, scaleX: 0.3, transformOrigin: "0% 50%" }, { opacity: 1, scaleX: 1, duration: 0.6, immediateRender: false }, it.bandAt); } }
      if (it.kind === "counter") { const t = inner.querySelector("text.counter"), o = { v: it.from || 0 };
        const fmt = (v) => { const n = Math.round(v); const sgn = n < 0 ? "−" : ""; const a = Math.abs(n).toLocaleString("en-IN");
          return it.fmt === "days" ? `${n}` : it.fmt === "pct" ? `${(Math.round(v * 10) / 10).toFixed(it.dp ?? 1)}%` : `${sgn}₹${a}`; };
        t.textContent = (it.prefix || "") + fmt(o.v) + (it.suffix || "");
        (it.steps || [[it.at + 0.1, it.to, it.count || 1.5]]).forEach(([at, to, d]) => tl.to(o, { v: to, duration: d, ease: it.ease || "power1.inOut",
          onUpdate: () => { t.textContent = (it.prefix || "") + fmt(o.v) + (it.suffix || ""); } }, at)); }
      if (it.float) { const f = inner.querySelector("g.float"); if (f) tl.fromTo(f, { rotation: -it.float / 2, y: 0, transformOrigin: "50% 50%" },   // slow living drift, f(t)
        { rotation: it.float / 2, y: -10, duration: Math.max(0.5, (it.until || it.exit || DUR) - t), ease: "sine.inOut" }, t); }
      if (it.exit != null) tl.to(outer, { opacity: 0, y: (it.y || 0) - 40, duration: 0.35, ease: "power2.in" }, it.exit);
      return outer;
    }
    return { place };
  }

  window.Doodle = {
    run(S, id) {
      const svg = document.getElementById("s"), tl = gsap.timeline({ paused: true });
      tl.to({}, { duration: S.duration }, 0);
      DUR = S.duration; if (S.palette) Object.assign(C, S.palette); const kit = Kit(svg, tl);
      seed = 11;
      (S.items || []).forEach((it) => kit.place(it));
      const tag = document.getElementById("tag"); if (S.tag) tag.textContent = S.tag; else tag.remove();
      const kick = document.getElementById("kick"); if (S.kicker) kick.textContent = S.kicker; else kick.remove();
      // camera: per-page keys from the generator (slow push toward each page's content, reset at page turns), else a drift
      if (S.cam && S.cam.length) {
        gsap.set("#cam", { scale: S.cam[0][1], x: S.cam[0][2], y: S.cam[0][3] });
        S.cam.slice(1).forEach(([t, sc, x, y, d]) => tl.to("#cam", { scale: sc, x, y, duration: d || 0.01, ease: d > 0.5 ? "sine.inOut" : "none" }, t));
      } else tl.fromTo("#cam", { scale: 1.0, x: 0 }, { scale: 1.03, x: S.drift || -16, duration: S.duration, ease: "sine.inOut" }, 0);
      tl.fromTo("#paper", { x: 0 }, { x: -12, duration: S.duration, ease: "none" }, 0);
      // calm template (scene_calm.html): soft light blobs drift slowly behind the page, f(t)
      document.querySelectorAll(".glow").forEach((g, i) => tl.fromTo(g, { x: 0, y: 0 },
        { x: (i ? -1 : 1) * 90, y: (i ? 1 : -1) * 50, duration: S.duration, ease: "sine.inOut" }, 0));
      return tl;
    },
  };
})();
