TITLE = "E9 Which route do you travel?"
BG = "none"
LIBS = ["map.js", "mapdraw.js"]
CSS = """
  #sweep { display: none; }
  #map { position: absolute; inset: 0; width: 1920px; height: 1080px; opacity: 0.85; }
  #cm { position: absolute; left: 96px; top: 560px; width: 900px; padding: 26px 30px; border-radius: 18px; background: rgba(15,23,42,0.94); border: 2px solid #334155;
    box-shadow: 0 30px 70px rgba(0,0,0,0.55); font-family: Inter, Arial, sans-serif; color: #F8FAFC; opacity: 0; box-sizing: border-box; }
  #cm .pn { font: 600 22px Inter, Arial, sans-serif; color: #94A3B8; margin-bottom: 14px; }
  #cm .row { display: flex; gap: 22px; }
  #cm .av { flex: none; width: 74px; height: 74px; border-radius: 37px; background: #F59E0B; color: #1F1300; font: 800 30px/74px Inter, Arial, sans-serif; text-align: center; }
  #cm .nm { font: 700 24px Inter, Arial, sans-serif; color: #CBD5E1; }
  #cm .tx { font: 800 54px/1.12 Inter, Arial, sans-serif; margin-top: 8px; }
  #cm .sub { font: 500 28px/1.3 Inter, Arial, sans-serif; color: #CBD5E1; margin-top: 10px; }
"""
BODY = """  <svg id="map" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="cm"><div class="pn">Pinned comment</div><div class="row"><div class="av">BP</div><div><div class="nm">Be Practical with Kishore</div>
    <div class="tx">WHICH ROUTE DO YOU TRAVEL?</div><div class="sub">Is Kavach working on it yet? Tell me below.</div></div></div></div>"""
JS = """
  const Mp = buildMap(document.getElementById("map"));
  tl.set("#rails", { opacity: 0.55 }, 0);
  for (const k of ["dm", "dh"]) { tl.set(Mp.C[k].glow, { opacity: 0 }, 0); tl.set(Mp.C[k].core, { opacity: 0.6, attr: { "stroke-dasharray": "7 7", "stroke-width": 3, stroke: "#F59E0B" } }, 0); }
  for (const k of ["w_dm", "va", "w_d1", "w_d2", "w_d3", "w_d4", "w_d5", "w_d6", "w_d7"]) { tl.set(Mp.C[k].glow, { opacity: 0.25 }, 0); tl.set(Mp.C[k].core, { opacity: 0.9 }, 0); }
  for (const k of ["scr1", "scr2", "scr3", "scr4"]) { tl.set(Mp.C[k].glow, { opacity: 0.25, attr: { stroke: "#F59E0B" } }, 0); tl.set(Mp.C[k].core, { opacity: 0.9, attr: { stroke: "#FCD34D" } }, 0); }
  tl.fromTo("#mworld", { transformOrigin: "880px 560px", scale: 1.0, x: 180, y: -40 }, { scale: 1.06, x: 120, y: -60, duration: D, ease: "sine.inOut" }, 0);
  tl.fromTo("#cm", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.2);
"""
