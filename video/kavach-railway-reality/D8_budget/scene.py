TITLE = "D8 Kavach budget"
CSS = """
  #bg { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .ax { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #94A3B8; }
  .yr { font: 800 34px Inter, Arial, sans-serif; letter-spacing: 0.1em; fill: #CBD5E1; }
  .amt { font: 800 76px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; letter-spacing: -0.01em; }
  .cr { font: 800 28px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #94A3B8; }
  .ttl { font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.2em; fill: #38BDF8; }
  .dl { font: 800 44px Inter, Arial, sans-serif; fill: #F59E0B; letter-spacing: 0.02em; }
"""
BODY = """  <svg id="bg" viewBox="0 0 1920 1080" data-layout-allow-overflow>
    <defs>
      <linearGradient id="b1" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#64748B"/><stop offset="1" stop-color="#1E293B"/></linearGradient>
      <linearGradient id="b2" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7DD3FC"/><stop offset="1" stop-color="#075985"/></linearGradient>
      <linearGradient id="scan" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="rgba(255,255,255,0)"/><stop offset="0.5" stop-color="rgba(255,255,255,0.35)"/><stop offset="1" stop-color="rgba(255,255,255,0)"/></linearGradient>
      <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><feGaussianBlur stdDeviation="12" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <clipPath id="c1"><rect id="r1c" x="0" y="0" width="0" height="0"/></clipPath><clipPath id="c2"><rect id="r2c" x="0" y="0" width="0" height="0"/></clipPath>
    </defs>
    <g id="world">
      <g id="grid"></g>
      <text x="300" y="180" class="ttl">KAVACH · YEARLY ALLOCATION</text>
      <g id="bar1"><rect id="r1" fill="url(#b1)" stroke="#94A3B8" stroke-width="2"/></g>
      <g id="bar2"><rect id="r2" fill="url(#b2)" stroke="#7DD3FC" stroke-width="2" filter="url(#glow)"/></g>
      <line id="cap1" stroke="#CBD5E1" stroke-width="3" stroke-dasharray="10 8" opacity="0"/>
      <g id="v1" opacity="0"><text id="a1" class="amt">₹0</text><text id="k1" class="cr">CRORE</text></g>
      <g id="v2" opacity="0"><text id="a2" class="amt">₹0</text><text id="k2" class="cr">CRORE</text></g>
      <text id="y1" class="yr" text-anchor="middle">2024–25</text><text id="y2" class="yr" text-anchor="middle">2025–26</text>
      <g id="delta" opacity="0"><path id="darr" fill="none" stroke="#F59E0B" stroke-width="4"/><path id="dhead" fill="#F59E0B"/><text id="dtx" class="dl">≈ +50%</text></g>
    </g>
  </svg>"""
JS = """
  const $ = (id) => document.getElementById(id), set = (id, a) => { for (const k in a) $(id).setAttribute(k, a[k]); }, NS = "http://www.w3.org/2000/svg";
  const BASE = 900, K = 560 / 1673.19, X1 = 520, X2 = 1000, BW = 260;    // bars to scale: 560 px = Rs 1,673.19 cr
  const h1 = 1112.57 * K, h2 = 1673.19 * K;
  // instrument grid: a line every Rs 250 crore
  const grid = $("grid");
  for (let v = 0; v <= 1750; v += 250) { const y = BASE - v * K; const l = document.createElementNS(NS, "line"); l.setAttribute("x1", 300); l.setAttribute("x2", 1500); l.setAttribute("y1", y + 0.4); l.setAttribute("y2", y);
    l.setAttribute("stroke", v ? "rgba(148,163,184,0.12)" : "#64748B"); l.setAttribute("stroke-width", v ? 1.5 : 3); grid.appendChild(l);
    if (v) { const t = document.createElementNS(NS, "text"); t.setAttribute("x", 290); t.setAttribute("y", y + 7); t.setAttribute("text-anchor", "end"); t.setAttribute("class", "ax"); t.textContent = v.toLocaleString("en-IN"); grid.appendChild(t); } }
  const yl = document.createElementNS(NS, "text"); yl.setAttribute("x", 290); yl.setAttribute("y", BASE - 1750 * K - 34); yl.setAttribute("text-anchor", "end"); yl.setAttribute("class", "ax"); yl.textContent = "₹ CRORE"; grid.appendChild(yl);
  set("r1", { x: X1, width: BW, y: BASE, height: 0 }); set("r2", { x: X2, width: BW, y: BASE, height: 0 });
  set("r1c", { x: X1, width: BW, y: BASE - h1, height: h1 }); set("r2c", { x: X2, width: BW, y: BASE - h2, height: h2 });
  
  set("y1", { x: X1 + BW / 2, y: BASE + 54 }); set("y2", { x: X2 + BW / 2, y: BASE + 54 });
  set("a1", { x: X1 - 10, y: BASE - h1 - 70 }); set("k1", { x: X1 - 6, y: BASE - h1 - 28 });
  set("a2", { x: X2 - 10, y: BASE - h2 - 70 }); set("k2", { x: X2 - 6, y: BASE - h2 - 28 });
  set("cap1", { x1: X1 + BW, x2: X2 + BW + 40, y1: BASE - h1, y2: BASE - h1 + 0.4 });
  const ax = X2 + BW + 70, ya = BASE - h1, yb = BASE - h2 + 8;
  set("darr", { d: `M ${ax} ${ya} L ${ax + 0.4} ${yb + 24}` }); set("dhead", { d: `M ${ax - 14} ${yb + 26} L ${ax} ${yb} L ${ax + 14} ${yb + 26} Z` });
  set("dtx", { x: ax + 28, y: (ya + yb) / 2 + 16 });
  const fmt = (v) => "≈ ₹" + (Math.round(v / 10) * 10).toLocaleString("en-IN") + " CR";
  const tM = at("V036", "The money"), t1 = at("V036", "one thousand one hundred"), t2 = at("V036", "one thousand six hundred"), tY = at("V036", "in twenty twenty five");
  tl.from(["#grid", ".ttl", "#y1", "#y2"], { opacity: 0, duration: 0.8, stagger: 0.1 }, 0.1);
  // bars rise while the sentence builds to each number; the big figure is the rounded one the narration says, the exact
  // allocation sits under it (PIB Mar 2025: Rs 1,112.57 cr for 2024-25; Rajya Sabha Aug 2025: Rs 1,673.19 cr for 2025-26)
  const grow = (r, h, a, k, v, t, d, exact) => { tl.to(r, { attr: { y: BASE - h, height: h }, duration: d, ease: "power2.out" }, t);
    // the label shows only the final rounded figure and rides up with the bar top (no count through wrong values)
    a.textContent = fmt(v).replace(" CR", ""); k.textContent = "CRORE";
    tl.to(a.parentNode, { opacity: 1, duration: 0.3 }, t + d * 0.5);
    tl.fromTo(a.parentNode, { y: h }, { y: 0, duration: d, ease: "power2.out" }, t); };
  grow("#r1", h1, $("a1"), $("k1"), 1100, at("V036", "the yearly"), t1 + 0.4 - at("V036", "the yearly"), "EXACT ₹1,112.57 CR");
  grow("#r2", h2, $("a2"), $("k2"), 1670, t2 - 1.4, 2.0, "EXACT ₹1,673.19 CR");
  tl.to("#cap1", { opacity: 1, duration: 0.4 }, t2 + 1.0);
  tl.fromTo("#delta", { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: 0.5 }, Math.min(tY, D - 2.6));
  tl.fromTo("#world", { transformOrigin: "900px 600px", scale: 1.0, x: 0 }, { scale: 1.06, x: -30, duration: D, ease: "sine.inOut" }, 0);
"""
