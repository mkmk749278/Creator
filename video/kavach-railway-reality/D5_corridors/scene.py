TITLE = "D5 Kavach 4.0 corridors"
LIBS = ["map.js", "mapdraw.js"]
CSS = """
  #map { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  #panel { position: absolute; left: 1290px; top: 300px; width: 560px; }
  #scrim { position: absolute; left: 1150px; top: 170px; width: 820px; height: 480px; background: radial-gradient(closest-side, rgba(11,18,32,0.9) 35%, rgba(11,18,32,0) 100%); }
  .tag { font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.2em; color: #38BDF8; margin-bottom: 14px; }
  .k { font: 800 120px Inter, Arial, sans-serif; color: #F8FAFC; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; line-height: 1; }
  .u { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #94A3B8; margin-top: 12px; }
  .blk { opacity: 0; }
  .unused { position: absolute; font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.12em; color: #E0F2FE; padding: 8px 14px;
    background: rgba(8,20,38,0.86); border: 2px solid #38BDF8; border-radius: 8px; opacity: 0; white-space: nowrap; }
  .unused b { color: #7DD3FC; }
"""
BODY = """  <svg id="map" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="scrim" data-layout-allow-occlusion></div>
  <div id="panel">
    <div class="blk" id="b1"><div class="tag">KAVACH 4.0 · WORKING</div><div class="k" id="n1">0</div><div class="u">ROUTE KM · 31 JUL 2026</div></div>
  </div>"""
JS = """
  const Mp = buildMap(document.getElementById("map"));
  // continue D4's framing, then drift towards the corridors
  tl.fromTo("#mworld", { transformOrigin: "880px 560px", scale: 1.02, x: -150, y: 0 }, { scale: 1.05, x: -150, y: -30, duration: D, ease: "sine.inOut" }, 0);
  tl.set("#rails", { opacity: 0.45 }, 0);
  for (const k of ["scr1", "scr2", "scr3", "scr4"]) tl.set([Mp.C[k].glow, Mp.C[k].core], { opacity: 0 }, 0);
  const tStart = at("V033", "newest Kavach"), tN = at("V033", "two thousand six hundred"), tDM = at("V033", "Delhi Mumbai"), tDH = at("V033", "Delhi Howrah"), tBusy = at("V033", "two of the busiest");
  const draw = (k, t, dur) => { for (const p of [Mp.C[k].glow, Mp.C[k].core]) { Mp.prep(p); tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: dur, ease: "power1.inOut" }, t); } };
  ["delhi"].forEach((k) => tl.to(Mp.P[k], { opacity: 1, duration: 0.3 }, tStart - 0.5));
  draw("dm", Math.min(tDM - 1.2, tN - 0.3), 2.4); draw("va", Math.min(tDM - 1.2, tN - 0.3) + 1.8, 0.8);
  draw("dh", tDH - 1.0, 2.2);
  ["mumbai", "ahmedabad"].forEach((k) => tl.to(Mp.P[k], { opacity: 1, duration: 0.3 }, Math.min(tDM - 1.2, tN - 0.3) + 2.2));
  tl.to(Mp.P.howrah, { opacity: 1, duration: 0.3 }, tDH + 1.1);
  // labels live inside the map group so they ride the camera move
  const NS = "http://www.w3.org/2000/svg";
  const label = (id, k, dx, dy, anchor, t1, t2) => {
    const [x, y] = Mp.M.pts[k], g = document.createElementNS(NS, "g"); g.setAttribute("id", id); g.setAttribute("opacity", 0);
    const w = 330, h = 66, rx = anchor === "end" ? x + dx - w : x + dx;
    g.innerHTML = `<line x1="${x}" y1="${y}" x2="${anchor === "end" ? rx + w : rx}" y2="${y + dy + h / 2 + 0.4}" stroke="#38BDF8" stroke-width="2"/>
      <rect x="${rx}" y="${y + dy}" width="${w}" height="${h}" rx="8" fill="rgba(8,20,38,0.9)" stroke="#38BDF8" stroke-width="2"/>
      <text x="${rx + 16}" y="${y + dy + 28}" style="font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #7DD3FC">${t1}</text>
      <text x="${rx + 16}" y="${y + dy + 54}" style="font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #E0F2FE">${t2}</text>`;
    document.getElementById("mworld").appendChild(g); return g;
  };
  label("lab-dm", "ahmedabad", -60, -110, "end", "DELHI → MUMBAI", "1,423 KM GROUP");
  label("lab-dh", "howrah", 30, 110, "start", "DELHI → HOWRAH", "1,210 KM GROUP");
  tl.fromTo("#lab-dm", { opacity: 0 }, { opacity: 1, duration: 0.5 }, tDM);
  tl.fromTo("#lab-dh", { opacity: 0 }, { opacity: 1, duration: 0.5 }, tDH + 0.3);
  // busiest: a pulse travels both corridors
  for (const k of ["dm", "dh"]) tl.fromTo(Mp.C[k].glow, { attr: { "stroke-width": 12 }, opacity: 0.25 }, { attr: { "stroke-width": 22 }, opacity: 0.5, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }, tBusy);
  const a = { v: 0 };
  tl.to("#b1", { opacity: 1, duration: 0.4 }, tN - 0.3);
  tl.to(a, { v: 2633, duration: 1.8, ease: "power2.out", onUpdate: () => document.getElementById("n1").textContent = Math.round(a.v).toLocaleString("en-IN") }, tN - 0.3);
"""
