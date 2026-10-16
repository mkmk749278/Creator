// Session A helpers on top of vendor/fin/fin.js (FIN.rng, FIN.keys, FIN.hook, FIN.grain). Everything is f(t).
const IO = {};
// floating dust motes in window light: n seeded particles inside box {x, y, w, h}
IO.motes = (parent, n, seed, box, alpha = 1) => {
  const r = FIN.rng(seed), ps = [];
  for (let i = 0; i < n; i++) {
    const d = document.createElement("div"); d.className = "mote"; parent.appendChild(d);
    const s = 0.5 + r() * 1.6;
    d.style.width = d.style.height = (4 + s * 4).toFixed(1) + "px";
    ps.push({ d, x: box.x + r() * box.w, y: box.y + r() * box.h, ax: 20 + r() * 40, ay: 10 + r() * 30, w: 0.15 + r() * 0.35, ph: r() * 6.28, vy: -4 - r() * 8, o: (0.25 + r() * 0.6) * alpha });
  }
  FIN.hook((t) => { for (const p of ps) {
    const x = p.x + Math.sin(t * p.w + p.ph) * p.ax, y = p.y + p.vy * t + Math.cos(t * p.w * 0.8 + p.ph) * p.ay;
    p.d.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
    p.d.style.opacity = (p.o * (0.6 + 0.4 * Math.sin(t * 1.3 + p.ph))).toFixed(3);
  } });
};
// slow handheld-like camera drift on an element, pure function of t (seeded sines)
IO.drift = (el, amp = 6, seed = 3) => { const r = FIN.rng(seed), a = r() * 6, b = r() * 6;
  FIN.hook((t) => { el.style.translate = `${(Math.sin(t * 0.37 + a) * amp).toFixed(2)}px ${(Math.sin(t * 0.29 + b) * amp * 0.7).toFixed(2)}px`; }); };
// small line icons (stroke = currentColor)
IO.ICONS = {
  check: '<path d="M10 25 L20 35 L38 13" />',
  gavel: '<path d="M14 20 L26 8 L34 16 L22 28 Z" /><path d="M24 22 L40 38" /><path d="M8 42 H30" />',
  clock: '<circle cx="24" cy="24" r="17" /><path d="M24 14 V24 L31 29" />',
  zero: '<rect x="6" y="12" width="36" height="24" rx="4" /><circle cx="24" cy="24" r="6" />',
};
IO.icon = (n) => `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round">${IO.ICONS[n]}</svg>`;
// Four-step staircase (Episode 01 motif rebuilt in this palette) as SVG. Returns handles per step:
// {top, front, glow, pool, num, cx, topY} so a scene can light steps and park the case file on a tread.
IO.stairs = (svg, o = {}) => {
  const NS = "http://www.w3.org/2000/svg", x0 = o.x0 ?? 360, w = o.w ?? 300, rise = o.rise ?? 120, floor = o.floor ?? 880,
    dx = o.dx ?? 110, dy = o.dy ?? -70, pre = o.id ?? "st";
  const mk = (tag, at, parent = svg) => { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); parent.appendChild(e); return e; };
  const defs = mk("defs", {});
  defs.innerHTML = `
    <linearGradient id="${pre}-front" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20374f"/><stop offset="1" stop-color="#0d1828"/></linearGradient>
    <linearGradient id="${pre}-top" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#3a5675"/><stop offset="1" stop-color="#253f5c"/></linearGradient>
    <linearGradient id="${pre}-side" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#16283d"/><stop offset="1" stop-color="#0b1422"/></linearGradient>
    <radialGradient id="${pre}-poolY"><stop offset="0" stop-color="#FFDB59" stop-opacity=".55"/><stop offset="1" stop-color="#FFDB59" stop-opacity="0"/></radialGradient>
    <radialGradient id="${pre}-poolT"><stop offset="0" stop-color="#59DCC3" stop-opacity=".7"/><stop offset="1" stop-color="#59DCC3" stop-opacity="0"/></radialGradient>
    <filter id="${pre}-blur" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="9"/></filter>`;
  const steps = [];
  for (let i = 0; i < 4; i++) {
    const x = x0 + i * w, top = floor - (i + 1) * rise, g = mk("g", { id: `${pre}-s${i + 1}` });
    const col = i === 3 ? "T" : "Y";
    const pool = mk("ellipse", { cx: x + w / 2 + dx / 2, cy: top + dy / 2 - 30, rx: w * 0.75, ry: 120, fill: `url(#${pre}-pool${col})`, opacity: 0 }, g);
    const front = mk("rect", { x, y: top, width: w, height: floor - top, fill: `url(#${pre}-front)` }, g);
    const topF = mk("polygon", { points: `${x},${top} ${x + w},${top} ${x + w + dx},${top + dy} ${x + dx},${top + dy}`, fill: `url(#${pre}-top)` }, g);
    const lit = mk("polygon", { points: `${x},${top} ${x + w},${top} ${x + w + dx},${top + dy} ${x + dx},${top + dy}`, fill: col === "T" ? "#59DCC3" : "#FFDB59", opacity: 0 }, g);
    if (i === 3) mk("polygon", { points: `${x + w},${top} ${x + w + dx},${top + dy} ${x + w + dx},${floor + dy} ${x + w},${floor}`, fill: `url(#${pre}-side)` }, g);
    const glow = mk("rect", { x: x - 6, y: top - 8, width: w + 12, height: 16, rx: 8, fill: col === "T" ? "#59DCC3" : "#FFDB59", filter: `url(#${pre}-blur)`, opacity: 0 }, g);
    const edge = mk("rect", { x, y: top - 2, width: w, height: 4, fill: "#B8C7D9", opacity: 0.35 }, g);
    const num = mk("text", { "data-layout-allow-occlusion": "", "data-layout-allow-overlap": "", x: x + 30, y: top + 104, fill: "#B8C7D9", "font-family": "Inter, Arial, sans-serif", "font-weight": 800, "font-size": 92, opacity: 0.22 }, g);
    num.textContent = String(i + 1);
    steps.push({ g, top: lit, front, glow, edge, pool, num, cx: x + w / 2 + dx / 2, topY: top + dy / 2 });
  }
  return steps;
};
// manila case file as an SVG group, drawn around (0,0) = bottom centre; move it with GSAP x/y
IO.caseFile = (svg, id, s = 1) => {
  const NS = "http://www.w3.org/2000/svg", g = document.createElementNS(NS, "g"); g.setAttribute("id", id);
  g.innerHTML = `<g transform="scale(${s})">
    <ellipse cx="0" cy="2" rx="96" ry="12" fill="#000" opacity=".35"/>
    <path d="M-84 -86 L-36 -86 L-26 -100 L20 -100 L28 -86 L84 -86 L84 0 L-84 0 Z" fill="#c9a86a"/>
    <rect x="-78" y="-80" width="150" height="70" fill="#F5F7FB" opacity=".92" transform="rotate(-3)"/>
    <path d="M-88 -70 L88 -70 L80 0 L-80 0 Z" fill="#d8b97a"/>
    <rect x="-58" y="-50" width="70" height="8" rx="4" fill="#8a6a35" opacity=".55"/>
    <rect x="-58" y="-34" width="44" height="8" rx="4" fill="#8a6a35" opacity=".45"/></g>`;
  svg.appendChild(g); return g;
};
