TITLE = "D6 Under a tenth"
LIBS = ["map.js", "mapdraw.js", "vendor/wb/wb-fonts.js", "vendor/wb/wb.js"]
CSS = """
  #map { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  #panel { position: absolute; left: 1150px; top: 196px; width: 700px; opacity: 0; }
  .tag { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.14em; color: #F59E0B; white-space: nowrap; margin-bottom: 10px; }
  .k { font: 800 96px Inter, Arial, sans-serif; color: #F8FAFC; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; line-height: 1; }
  .k small { font-size: 34px; letter-spacing: 0.14em; color: #94A3B8; margin-left: 14px; }
  #scrim { position: absolute; left: 1020px; top: 100px; width: 950px; height: 420px; background: radial-gradient(closest-side, rgba(11,18,32,0.9) 35%, rgba(11,18,32,0) 100%); }
  #inset { position: absolute; left: 1090px; top: 436px; width: 1920px; height: 1080px; transform-origin: 0 0; opacity: 0; }
  #inset .wb-stage { background: transparent; }
"""
BODY = """  <link rel="stylesheet" href="vendor/wb/wb.css" />
  <svg id="map" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="scrim" data-layout-allow-occlusion></div>
  <div id="panel"><div class="tag">VERSION 3.2 · SOUTH CENTRAL RLY</div><div class="k"><span id="n1">0</span><small>ROUTE KM</small></div></div>
  <div id="inset" data-layout-allow-occlusion data-layout-allow-overflow><div id="stage"></div></div>"""
JS = """
  const Mp = buildMap(document.getElementById("map"));
  tl.fromTo("#mworld", { transformOrigin: "880px 560px", scale: 1.14, x: -150, y: -70 }, { scale: 1.2, x: -330, y: -150, duration: D, ease: "sine.inOut" }, 0);
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
  // whiteboard inset: our calculation, written as the line lands
  tl.fromTo("#inset", { opacity: 0, scale: 0.39, y: 30 }, { opacity: 1, scale: 0.41, y: 0, duration: 0.5, ease: "power2.out" }, tS - 0.5);
  const b = WB.board(document.getElementById("stage"), { seed: 34, tray: false });
  b.write("2,633 + 1,465 = 4,098", { x: 190, y: 290, size: 104, color: "blue", at: tS, dur: 1.2 });
  b.write("4,098 ÷ 69,439 ≈ 5.9%", { x: 190, y: 520, size: 104, color: "black", dur: 1.3 });
  b.write("UNDER 10%", { x: 230, y: 790, size: 128, color: "red", at: tU, dur: 0.9 });
  b.circleLast({ color: "red", dur: 0.5 });
  b.attach(tl);
"""
