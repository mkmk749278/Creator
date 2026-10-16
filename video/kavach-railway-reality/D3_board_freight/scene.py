TITLE = "D3 A goods train needs about 930 m"
LIBS = ["tele.js"]
CSS = """
  #tele { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .ax { font: 800 22px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.1em; font-variant-numeric: tabular-nums; }
  .zl { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.1em; }
  .zn { font: 800 46px Inter, Arial, sans-serif; font-variant-numeric: tabular-nums; }
  .tot { font: 800 72px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
  .rd { font: 800 54px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
  .ru { font: 800 20px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.16em; }
  .chipt { font: 800 34px Inter, Arial, sans-serif; fill: #F8FAFC; letter-spacing: 0.04em; }
"""
BODY = """  <svg id="tele" viewBox="0 0 1920 1080" data-layout-allow-overflow>
    <defs>
      <filter id="hot" filterUnits="userSpaceOnUse" x="-20000" y="-2000" width="40000" height="4000"><feGaussianBlur stdDeviation="0.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <linearGradient id="gnd" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="rgba(30,41,59,0.6)"/><stop offset="1" stop-color="rgba(30,41,59,0)"/></linearGradient>
      <linearGradient id="amb" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="rgba(245,158,11,0.45)"/><stop offset="1" stop-color="rgba(245,158,11,0.04)"/></linearGradient>
      <linearGradient id="crm" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="rgba(220,38,38,0.45)"/><stop offset="1" stop-color="rgba(220,38,38,0.04)"/></linearGradient>
    </defs>
    <g id="world"></g>
    <g id="wide"></g>
    <g id="read"></g>
  </svg>"""
JS = """
  // Our calculation, illustrative model (claims.csv): 5,000 t at 75 km/h (20.8 m/s); brakes take about 10 s to build up
  // (208 m at speed), then a steady 0.30 m/s^2 stop (v^2/2a = 723 m); about 930 m in all. Distances are to scale; time is
  // shown as a time-lapse with the real seconds on the readout.
  const E = KT.el, W = document.getElementById("world"), G = document.getElementById("wide"), R = document.getElementById("read");
  const V0 = 75 / 3.6, A = 0.30, TD = 10, D1 = V0 * TD, D2 = V0 * V0 / (2 * A), DT = D1 + D2, T2 = V0 / A;   // 208.3, 723.4, 931.7 m, 69.4 s
  const RY = 430, PX = 1.5, CXW = 470;   // (intro: the camera sits 120 px lower so the train is mid-frame)                              // rail line on screen; wide view 1.5 px/m centred on 470 m
  // ---- world (metres; drawn through one transform): track, masts, loco + 58 wagons ----
  const trk = E("g", {}, W);
  E("line", { x1: -3000, y1: 0.6, x2: 1400, y2: 0.62, stroke: "#94A3B8", "stroke-width": 0.18 }, trk);
  E("line", { x1: -3000, y1: 1.0, x2: 1400, y2: 1.02, stroke: "#334155", "stroke-width": 0.5, "stroke-dasharray": "0.25 0.35" }, trk);
  for (let m = -3000; m < 1400; m += 60) { E("line", { x1: m, y1: 0.4, x2: m + 0.01, y2: -7.5, stroke: "#334155", "stroke-width": 0.3 }, trk); E("line", { x1: m, y1: -7.2, x2: m + 2.2, y2: -7.21, stroke: "#334155", "stroke-width": 0.18 }, trk); }
  E("line", { x1: -3000, y1: -6.4, x2: 1400, y2: -6.41, stroke: "rgba(148,163,184,0.4)", "stroke-width": 0.06 }, trk);
  const train = E("g", {}, W), blocks = [];
  // loco (WAG-9-like freight electric, generic): nose at x = 0 of the train group
  E("path", { d: "M -20 -3.9 L -1.2 -3.9 L 0 -2.8 L 0 -0.6 L -20 -0.6 Z", fill: "#7F1D1D", stroke: "#FCA5A5", "stroke-width": 0.08 }, train);
  E("rect", { x: -20, y: -2.0, width: 20, height: 0.35, fill: "#FDE68A" }, train);
  E("rect", { x: -2.6, y: -3.4, width: 1.6, height: 1.0, rx: 0.1, fill: "#0F2A4A" }, train);
  E("path", { d: "M -14 -3.9 L -12.5 -4.9 L -11 -3.9", fill: "none", stroke: "#94A3B8", "stroke-width": 0.1 }, train);
  for (const x of [-17.5, -16, -14.5, -5.5, -4, -2.5]) { E("circle", { cx: x, cy: -0.1, r: 0.55, fill: "#1E293B", stroke: "#64748B", "stroke-width": 0.08 }, train); blocks.push([E("rect", { x: x - 0.75, y: -0.45, width: 0.22, height: 0.7, fill: "#F97316", opacity: 0 }, train), -x]); }
  E("circle", { cx: -0.15, cy: -2.2, r: 0.2, fill: "#FEF3C7" }, train);
  const wag = 10.7, gap = 0.4;
  for (let i = 0; i < 58; i++) { const x1 = -20 - gap - i * (wag + gap), x0 = x1 - wag;
    E("rect", { x: x0, y: -3.2, width: wag, height: 2.6, rx: 0.12, fill: "#5B3A2A", stroke: "#A16207", "stroke-width": 0.06 }, train);
    for (let r = 0; r < 4; r++) E("line", { x1: x0 + 1.2 + r * 2.8, y1: -3.1, x2: x0 + 1.21 + r * 2.8, y2: -0.7, stroke: "#3F2A1F", "stroke-width": 0.12 }, train);
    for (const x of [x0 + 1.6, x0 + 3.1, x1 - 3.1, x1 - 1.6]) { E("circle", { cx: x, cy: -0.1, r: 0.45, fill: "#1E293B", stroke: "#64748B", "stroke-width": 0.06 }, train);
      blocks.push([E("rect", { x: x - 0.65, y: -0.4, width: 0.2, height: 0.6, fill: "#F97316", opacity: 0 }, train), -x]); } }
  const glow = E("rect", { x: 0, y: -0.75, width: 0, height: 0.6, fill: "#FB923C", opacity: 0 }, train);   // brake heat along the train (reads in the wide view)
  const TL = 20 + 58 * (wag + gap);
  // spokes on the loco and the first wagons (turn with distance while the camera is close)
  const spokes = [];
  train.querySelectorAll("circle").forEach((c, i) => { if (i > 40) return; const x = +c.getAttribute("cx"), r = +c.getAttribute("r");
    if (r < 0.3) return; spokes.push([E("line", { x1: x, y1: -0.1, x2: x, y2: -0.1, stroke: "#94A3B8", "stroke-width": 0.08 }, train), x, r * 0.85]); });
  const ground = E("rect", { x: -4000, y: 1.3, width: 8000, height: 24, fill: "url(#gnd)" }, W); W.insertBefore(ground, W.firstChild);
  // ---- wide-view instruments (screen space, wide mapping) ----
  const XW = (m) => 960 + (m - CXW) * PX;
  const rul = E("g", { opacity: 0 }, G);
  for (let m = 0; m <= 1000; m += 50) { const maj = m % 100 === 0; E("line", { x1: XW(m), y1: RY + 26, x2: XW(m) + 0.3, y2: RY + (maj ? 50 : 38), stroke: maj ? "#94A3B8" : "#475569", "stroke-width": maj ? 3 : 2 }, rul);
    if (maj) E("text", { x: XW(m), y: RY + 80, "text-anchor": "middle", class: "ax" }, rul).textContent = m ? m + " m" : "0"; }
  E("line", { x1: XW(0), y1: RY + 26, x2: XW(1000), y2: RY + 26.3, stroke: "#475569", "stroke-width": 2 }, rul);
  // speed chart under the ruler: 0..80 km/h
  const cy0 = 900, cy1 = 640, YV = (v) => cy0 - (cy0 - cy1) * v / 80;
  const ch = E("g", { opacity: 0 }, G);
  for (const v of [0, 25, 50, 75]) { E("line", { x1: XW(0), y1: YV(v) + 0.3, x2: XW(1000), y2: YV(v), stroke: v ? "rgba(148,163,184,0.14)" : "#64748B", "stroke-width": v ? 1.5 : 2.5 }, ch);
    E("text", { x: XW(0) - 14, y: YV(v) + 8, "text-anchor": "end", class: "ax" }, ch).textContent = v; }
  E("text", { x: XW(0) - 14, y: cy1 - 30, "text-anchor": "end", class: "ax" }, ch).textContent = "KM/H";
  const z1 = E("path", { fill: "url(#amb)" }, ch), z2 = E("path", { fill: "url(#crm)" }, ch);
  const c1 = E("path", { fill: "none", stroke: "#F59E0B", "stroke-width": 6, "stroke-linecap": "round" }, ch), c2 = E("path", { fill: "none", stroke: "#EF4444", "stroke-width": 6, "stroke-linecap": "round" }, ch);
  const lab1 = E("g", { opacity: 0 }, ch), lab2 = E("g", { opacity: 0 }, ch);
  E("text", { x: XW(D1 / 2), y: YV(75) + 70, "text-anchor": "middle", class: "zl", fill: "#FCD34D" }, lab1).textContent = "BRAKES BUILD UP";
  E("text", { x: XW(D1 / 2), y: YV(75) + 122, "text-anchor": "middle", class: "zn", fill: "#FCD34D" }, lab1).textContent = "≈ 208 m";
  E("text", { x: XW(D1 + 300), y: YV(40) + 6, "text-anchor": "middle", class: "zl", fill: "#FCA5A5" }, lab2).textContent = "BRAKING";
  E("text", { x: XW(D1 + 300), y: YV(40) + 58, "text-anchor": "middle", class: "zn", fill: "#FCA5A5" }, lab2).textContent = "≈ 723 m";
  // total bracket above the train
  const tot = E("g", { opacity: 0 }, G), by = RY - 120;
  E("path", { d: `M ${XW(0)} ${by + 16} L ${XW(0)} ${by} L ${XW(DT)} ${by + 0.3} L ${XW(DT)} ${by + 16}`, fill: "none", stroke: "#F8FAFC", "stroke-width": 3 }, tot);
  E("text", { x: XW(DT / 2), y: by - 22, "text-anchor": "middle", class: "tot" }, tot).textContent = "≈ 930 m";
  E("line", { x1: XW(DT), y1: by, x2: XW(DT) + 0.3, y2: cy0, stroke: "rgba(248,250,252,0.5)", "stroke-width": 2, "stroke-dasharray": "8 8" }, tot);
  const brk = E("g", { opacity: 0 }, G);
  E("line", { x1: XW(0), y1: RY - 60, x2: XW(0) + 0.3, y2: cy0, stroke: "#F59E0B", "stroke-width": 2.5, "stroke-dasharray": "8 8" }, brk);
  // ---- readouts and intro chips ----
  const rdg = E("g", { opacity: 0 }, R);
  [["sp", 96, "KM/H"], ["dm", 330, "METRES"], ["ts", 564, "SECONDS"]].forEach(([id, x, u]) => { E("text", { id, x, y: 150, class: "rd" }, rdg).textContent = "0"; E("text", { x, y: 182, class: "ru" }, rdg).textContent = u; });
  const tlp = E("text", { x: 800, y: 150, class: "ru", fill: "#7DD3FC", opacity: 0 }, rdg); tlp.textContent = "▶▶ TIME-LAPSE";
  const chips = E("g", { opacity: 0 }, R);
  E("rect", { x: 96, y: 160, width: 420, height: 74, rx: 12, fill: "rgba(15,23,42,0.88)", stroke: "#F59E0B", "stroke-width": 2 }, chips);
  E("text", { x: 306, y: 210, "text-anchor": "middle", class: "chipt" }, chips).textContent = "5,000 T · 75 KM/H";
  // ---- time map: presentation t -> real seconds tau (brake at tau = 0); rate ramps 1 -> K while the camera pulls out (zoom = Z0 / rate) ----
  const K = 13, Z0 = 13, tA = 3.9, tB = 5.9, rate = (t) => t < tA ? 1 : t > tB ? K : 1 + (K - 1) * (0.5 - 0.5 * Math.cos(Math.PI * (t - tA) / (tB - tA)));
  const N = 400, cum = [0]; for (let i = 1; i <= N; i++) { const a = (i - 1) * D / N, b = i * D / N; cum.push(cum[i - 1] + (b - a) * (rate(a) + rate(b)) / 2); }
  const tauB = (() => { const i = Math.round(tB / D * N); return cum[i]; })();          // real time elapsed when the brakes go on
  const tau = (t) => { const f = Math.min(N, t / D * N), i = Math.floor(f); return (cum[i] + (cum[Math.min(N, i + 1)] - cum[i]) * (f - i)) - tauB; };
  const dist = (s) => s <= TD ? V0 * s : s <= TD + T2 ? D1 + V0 * (s - TD) - 0.5 * A * (s - TD) ** 2 : DT;   // s = seconds since brake application
  const speed = (s) => s <= TD ? V0 : s <= TD + T2 ? V0 - A * (s - TD) : 0;
  const curve = (d0, d1) => { let p = ""; for (let i = 0; i <= 80; i++) { const d = d0 + (d1 - d0) * i / 80, v = d <= D1 ? 75 : 75 * Math.sqrt(Math.max(0, 1 - (d - D1) / D2)); p += `${i ? "L" : "M"} ${XW(d).toFixed(1)} ${YV(v).toFixed(1)} `; } return p; };
  const st = { t: 0 }, $ = (id) => document.getElementById(id);
  const place = () => {
    const t = st.t, s = tau(t), d = s < 0 ? V0 * s : dist(s), v = s < 0 ? V0 : speed(s);
    const z = Z0 / rate(t), k = PX * z, e = t <= tA ? 0 : t >= tB ? 1 : 0.5 - 0.5 * Math.cos(Math.PI * (t - tA) / (tB - tA));
    const nx = 1240 + (XW(0) - 1240) * e, cx = t < tB ? d - (nx - 960) / k : CXW, oy = 120 * (1 - e);   // nose glides from 1240 px to the 0 m mark
    W.setAttribute("transform", `translate(${960 - cx * k} ${RY + oy}) scale(${k} ${Math.max(9, k)})`);   // heights stay >= 9 px/m (vertical exaggeration in the wide view)
    if (k > 3) for (const [l, x, r] of spokes) { const a = d / (r / 0.85); l.setAttribute("x1", x - r * Math.cos(a)); l.setAttribute("y1", -0.1 - r * Math.sin(a)); l.setAttribute("x2", x + r * Math.cos(a)); l.setAttribute("y2", -0.1 + r * Math.sin(a)); }
    train.setAttribute("transform", `translate(${d} 0)`);
    // the brake application travels back along the train at ~250 m/s (air-brake signal), blocks glow while braking
    const front = s < 0 ? -1 : s * 250;
    for (const [b, back] of blocks) b.setAttribute("opacity", s >= 0 && back <= front && v > 0.05 ? Math.min(1, 0.35 + Math.min(1, s / TD) * 0.65) : 0);
    { const f = Math.min(TL, Math.max(0, front)); glow.setAttribute("x", -f); glow.setAttribute("width", f); glow.setAttribute("opacity", s >= 0 && v > 0.05 ? 0.35 + 0.6 * Math.min(1, s / TD) : 0); }
    if (s > 0) { const a1 = Math.min(d, D1); c1.setAttribute("d", curve(0, Math.max(0.1, a1))); z1.setAttribute("d", curve(0, Math.max(0.1, a1)) + ` L ${XW(a1)} ${cy0} L ${XW(0)} ${cy0} Z`);
      if (d > D1) { c2.setAttribute("d", curve(D1, d)); z2.setAttribute("d", curve(D1, d) + ` L ${XW(d)} ${cy0} L ${XW(D1)} ${cy0} Z`); } else { c2.setAttribute("d", "M 0 0"); z2.setAttribute("d", "M 0 0"); } }
    else { c1.setAttribute("d", "M 0 0"); z1.setAttribute("d", "M 0 0"); c2.setAttribute("d", "M 0 0"); z2.setAttribute("d", "M 0 0"); }
    $("sp").textContent = Math.round(v * 3.6); $("dm").textContent = Math.max(0, Math.round(d)); $("ts").textContent = Math.max(0, Math.round(s));
  };
  place();
  tl.to(st, { t: D, duration: D, ease: "none", onUpdate: place }, 0);
  const t5 = at("V025", "five thousand"), t9 = at("V025", "more than nine");
  tl.fromTo(chips, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5 }, t5 - 0.2);
  tl.to(chips, { opacity: 0, duration: 0.4 }, tB - 1.4);
  tl.to([rul, ch], { opacity: 1, duration: 0.35 }, tB - 0.2);
  tl.to(rdg, { opacity: 1, duration: 0.5 }, tB - 0.8);
  tl.to(tlp, { opacity: 1, duration: 0.3 }, tA + 0.6);
  tl.to(brk, { opacity: 1, duration: 0.3 }, tB);
  tl.to(lab1, { opacity: 1, duration: 0.4 }, tB + 0.5);
  tl.to(lab2, { opacity: 1, duration: 0.4 }, tB + 2.2);
  tl.to(tot, { opacity: 1, duration: 0.6 }, Math.min(t9, D - 1.6));
"""
