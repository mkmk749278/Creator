TITLE = "D6 Under a tenth"
LIBS = ["map.js", "mapdraw.js"]
CSS = """
  #map { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  #panel { position: absolute; left: 1150px; top: 196px; width: 700px; opacity: 0; }
  .tag { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.14em; color: #F59E0B; white-space: nowrap; margin-bottom: 10px; }
  .k { font: 800 96px Inter, Arial, sans-serif; color: #F8FAFC; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; line-height: 1; }
  .k small { font-size: 34px; letter-spacing: 0.14em; color: #94A3B8; margin-left: 14px; }
  #scrim { position: absolute; left: 1000px; top: 100px; width: 950px; height: 420px; background: radial-gradient(closest-side, rgba(11,18,32,0.9) 35%, rgba(11,18,32,0) 100%); }
  #waf { position: absolute; left: 1120px; top: 362px; width: 640px; height: 540px; opacity: 0; background: rgba(11,18,32,0.86); border: 2px solid #1E293B; border-radius: 16px; }
  .wl { font: 800 21px Inter, Arial, sans-serif; letter-spacing: 0.1em; fill: #94A3B8; }
  .wb { font: 800 44px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
"""
BODY = """  <svg id="map" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="scrim" data-layout-allow-occlusion></div>
  <div id="panel"><div class="tag">VERSION 3.2 · SOUTH CENTRAL RLY</div><div class="k"><span id="n1">0</span><small>ROUTE KM</small></div></div>
  <svg id="waf" viewBox="0 0 640 540" data-layout-allow-overflow><g id="wg"></g></svg>"""
JS = """
  const Mp = buildMap(document.getElementById("map"));
  tl.fromTo("#mworld", { transformOrigin: "880px 560px", scale: 1.05, x: -150, y: -30 }, { scale: 1.06, x: -250, y: -30, duration: D, ease: "sine.inOut" }, 0);
  tl.set("#rails", { opacity: 0.45 }, 0);
  for (const k of ["delhi", "mumbai", "ahmedabad", "howrah"]) tl.set(Mp.P[k], { opacity: 1 }, 0);
  for (const k of ["dm", "va", "dh"]) tl.set([Mp.C[k].glow, Mp.C[k].core], { opacity: 0.75 }, 0);
  const tO = at("V034", "older version"), tN = at("V034", "one thousand four hundred"), tS = at("V034", "South Central"), tK = at("V034", "and Kavach"), tU = at("V034", "well under");
  ["scr1", "scr2", "scr3", "scr4"].forEach((k, i) => {
    const { glow, core } = Mp.C[k];
    glow.setAttribute("stroke", "#F59E0B"); core.setAttribute("stroke", "#FCD34D");
    for (const p of [glow, core]) { Mp.prep(p); tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 1.1, ease: "power1.inOut" }, tO + 0.2 + i * 0.35); }
  });
  for (const k of ["secunderabad", "wadi", "kazipet", "bidar", "nanded", "dhone", "vikarabad"]) { Mp.P[k].setAttribute("fill", "#FDE68A"); tl.to(Mp.P[k], { opacity: 1, duration: 0.3 }, tS); }
  tl.fromTo("#panel", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.45 }, tN - 0.3);
  const a = { v: 0 };
  tl.to(a, { v: 1465, duration: 1.5, ease: "power2.out", onUpdate: () => document.getElementById("n1").textContent = Math.round(a.v).toLocaleString("en-IN") }, tN - 0.3);
  // share of the network: 100 squares = 69,439 route km; Kavach 4.0 (2,633) + version 3.2 (1,465) = 5.9% (our calculation)
  const NS2 = "http://www.w3.org/2000/svg", wg = document.getElementById("wg"), SQ = 32, GP = 6, OX = 34, OY = 66;
  const mk2 = (tag, a, p) => { const e = document.createElementNS(NS2, tag); for (const k in a) e.setAttribute(k, a[k]); p.appendChild(e); return e; };
  mk2("text", { x: OX, y: 30, class: "wl" }, wg).textContent = "THE WHOLE NETWORK · 1 SQUARE = 1%";
  const cells = [];
  for (let i = 0; i < 100; i++) { const cx = OX + (i % 10) * (SQ + GP), cy = OY + Math.floor(i / 10) * (SQ + GP);
    mk2("rect", { x: cx, y: cy, width: SQ, height: SQ, rx: 4, fill: "#1E293B", stroke: "#334155", "stroke-width": 1.5 }, wg);
    cells.push([mk2("rect", { x: cx, y: cy, width: 0, height: SQ, rx: 4, fill: "#38BDF8" }, wg), mk2("rect", { x: cx, y: cy, width: 0, height: SQ, rx: 4, fill: "#F59E0B" }, wg)]); }
  const tenth = mk2("rect", { x: OX - 8, y: OY - 8, width: 10 * (SQ + GP) + 10, height: SQ + 16, rx: 8, fill: "none", stroke: "#F8FAFC", "stroke-width": 3, "stroke-dasharray": "10 7", opacity: 0 }, wg);
  const tenthT = mk2("text", { x: OX + 10 * (SQ + GP) + 22, y: OY + 27, class: "wl", fill: "#F8FAFC", opacity: 0 }, wg); tenthT.textContent = "ONE TENTH";
  tenthT.style.fill = "#F8FAFC";
  const res = mk2("g", { opacity: 0 }, wg);
  mk2("text", { x: OX, y: OY + 10 * (SQ + GP) + 50, class: "wb" }, res).textContent = "≈ 5.9% WORKING";
  const pc = { c: 0, a: 0 }, C4 = 2633 / 69439 * 100, C3 = 1465 / 69439 * 100;
  const fill = () => { for (let i = 0; i < 100; i++) { const c = Math.min(1, Math.max(0, pc.c - i)), a = Math.min(1, Math.max(0, pc.c + pc.a - i)) - c;
    const [rc, ra] = cells[i], x = +rc.getAttribute("x"); rc.setAttribute("width", SQ * c); ra.setAttribute("x", x + SQ * c); ra.setAttribute("width", SQ * Math.max(0, a)); } };
  fill();
  tl.fromTo("#waf", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, tS - 0.6);
  tl.to(pc, { c: C4, duration: 1.0, ease: "power2.out", onUpdate: fill }, tS - 0.1);
  tl.to(pc, { a: C3, duration: 0.8, ease: "power2.out", onUpdate: fill }, tS + 0.9);
  tl.to([tenth, tenthT], { opacity: 1, duration: 0.4 }, tU - 0.2);
  tl.fromTo(tenth, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -68 }, duration: D - tU, ease: "none" }, tU);
  tl.to(res, { opacity: 1, duration: 0.4 }, tU + 0.5);
  tl.to("#waf", { x: -620, y: -222, scale: 1.45, transformOrigin: "0px 0px", duration: 0.8, ease: "power3.inOut" }, tU - 0.2);
  tl.to("#map", { opacity: 0.25, duration: 0.6 }, tU - 0.2);
  tl.to(["#panel", "#scrim"], { opacity: 0, duration: 0.4 }, tU - 0.3);

"""
