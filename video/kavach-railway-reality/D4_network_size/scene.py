TITLE = "D4 The size of the job"
LIBS = ["map.js", "mapdraw.js"]
CSS = """
  #map { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  #panel { position: absolute; left: 1290px; top: 300px; width: 540px; }
  .k { font: 800 104px Inter, Arial, sans-serif; color: #F8FAFC; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; line-height: 1; }
  .u { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #94A3B8; margin: 10px 0 46px; }
  .blk { opacity: 0; }
"""
BODY = """  <svg id="map" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="panel">
    <div class="blk" id="b1"><div class="k" id="n1">0</div><div class="u">ROUTE KM · MAR 2025</div></div>
    <div class="blk" id="b2"><div class="k" id="n2">0</div><div class="u">DIESEL + ELECTRIC LOCOS · MAR 2025</div></div>
  </div>"""
JS = """
  const Mp = buildMap(document.getElementById("map"));
  tl.fromTo("#mworld", { transformOrigin: "880px 560px", scale: 0.96, x: -120 }, { scale: 1.02, x: -150, duration: D, ease: "sine.inOut" }, 0);
  tl.set("#corr", { opacity: 0 }, 0);
  tl.from("#land", { opacity: 0, duration: 1.0 }, 0.1);
  // the network grows outwards from Delhi over the first half of the line
  const tJ = at("V032", "Look at the size"), t69 = at("V032", "sixty nine thousand"), t16 = at("V032", "sixteen thousand");
  const n = Mp.rl.length, span = Math.max(2.5, t69 - tJ + 1.5);
  Mp.rl.forEach((p, i) => { Mp.prep(p); tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 0.9, ease: "power1.out" }, tJ - 0.6 + span * i / n); });
  const fmt = (v) => Math.round(v).toLocaleString("en-IN");
  const a = { v: 0 }, b = { v: 0 };
  tl.to("#b1", { opacity: 1, duration: 0.4 }, t69 - 0.2);
  tl.to(a, { v: 69439, duration: 1.6, ease: "power2.out", onUpdate: () => document.getElementById("n1").textContent = fmt(a.v) }, t69 - 0.2);
  tl.to("#b2", { opacity: 1, duration: 0.4 }, t16 - 0.2);
  tl.to(b, { v: 16000, duration: 1.4, ease: "power2.out", onUpdate: () => document.getElementById("n2").textContent = "≈ " + fmt(b.v) }, t16 - 0.2);
"""
