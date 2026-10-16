TITLE = "B4 Kavach knows the signal ahead and brakes early"
LIBS = ["fogview.js", "dmi.js"]
BG = "none"
CSS = """
  #fog { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
  #dmi { position: absolute; left: 1210px; top: 300px; width: 640px; height: 590px; filter: drop-shadow(0 18px 30px rgba(0,0,0,0.6)); }
  .dmiT { font: 800 15px Inter, Arial, sans-serif; letter-spacing: 0.16em; fill: #FB7185; }
  .dmiK { font: 800 18px Inter, Arial, sans-serif; fill: #D1D5DB; }
  .dmiS { font: 600 15px Inter, Arial, sans-serif; fill: #E5E7EB; }
  .dmiN { font: 800 14px Inter, Arial, sans-serif; fill: #F3F4F6; }
  .dmiV { font: 800 26px Inter, Arial, sans-serif; fill: #050607; }
  .dmiM { font: 800 21px Inter, Arial, sans-serif; fill: #F8FAFC; }
  .dmiF { font: 700 11px Inter, Arial, sans-serif; fill: #CBD5E1; }
  .dmiB { font: 800 15px Inter, Arial, sans-serif; letter-spacing: 0.06em; fill: #111827; }
  #tl { position: absolute; left: 110px; top: 110px; padding: 10px 20px; border-radius: 10px; background: rgba(15,23,42,0.88); border: 2px solid #38BDF8; font: 800 28px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #7DD3FC; opacity: 0; }
  #lab1 { bottom: 270px; }
  #ring { position: absolute; left: 1196px; top: 286px; width: 668px; height: 618px; border-radius: 26px; border: 5px solid #38BDF8; opacity: 0; }
"""
BODY = """  <canvas id="fog" width="1920" height="1080"></canvas>
  <img id="fogimg" src="fog.png" alt="" style="display:none" />
  <svg id="dmi" viewBox="0 0 760 700" data-layout-allow-overflow></svg>
  <div id="ring" data-layout-allow-occlusion></div>
  <div id="tl">▶▶ TIME-LAPSE</div>
  <div class="kav-label" id="lab1">Kavach screen in the cab<small>KNOWS THE RED SIGNAL 800 M AHEAD</small></div>"""
JS = """
  // ILLUSTRATION after the real Kavach cab screen (design-reference.md). 110 km/h; red signal 800 m ahead when Kavach
  // shows it; the permitted speed (green arc) falls along a braking curve (about 1 m/s^2, stopping about 200 m short);
  // the pilot does not slow, Kavach warns, then brakes; the train stops still out of sight of the signal in the fog.
  const FV = FogView(document.getElementById("fog"), document.getElementById("fogimg"));
  const M = KDMI(document.getElementById("dmi"));
  const V0 = 110 / 3.6, AB = 1.0, MARGIN = 200, $ = (id) => document.getElementById(id);
  const tG = CUES.cues.V029.at, tK = at("V029", "it already knows"), tS = at("V029", "shows it on the screen"), tW = at("V029", "if the loco pilot"), tB = at("V029", "brakes early");
  const T0 = 800 + V0 * tK, TL = 12, tStop = V0 / AB;
  const st = { t: 0, travel: 300, zsig: 400, cab: true }, clock = { t: 0 };
  const frame = () => {
    const t = clock.t, tb = t < tB ? 0 : Math.min(tStop, (t - tB) * TL);
    const v = t < tB ? V0 : Math.max(0, V0 - AB * tb), d = t < tB ? V0 * t : V0 * tB + V0 * tb - 0.5 * AB * tb * tb;
    const left = T0 - d, known = t >= tK - 0.3;
    st.t = t + 17; st.travel = 300 + d; st.zsig = left; FV.draw(st);
    const vp = known ? Math.min(110, Math.sqrt(2 * AB * Math.max(0, left - MARGIN)) * 3.6) : 110;
    const stopped = t >= tB && v <= 0.01;
    let msg = "", warn = 0, brake = 0;
    if (known) msg = `Signal at Danger in ${String(Math.round(left)).padStart(4, "0")}m`;
    if (t >= tW && t < tB) { msg = "Overspeed · Reduce Speed"; warn = 1; }
    if (t >= tB) { msg = stopped ? "Train Stopped by Kavach" : "Brakes Applied by Kavach"; brake = 1; }
    M.set({ v: v * 3.6, vp, td: known ? left - MARGIN : 1500, ma: known ? left : 3000, asp: known ? "R" : "G", sd: known ? left : 0,
      msg, warn, brake, loc: 233.4 + d / 1000, mode: `DC 1.00   TL 650 m   ${known ? "Full Supervision Mode" : "Staff Responsible"}` });
  };
  frame();
  tl.to(clock, { t: D, duration: D, ease: "none", onUpdate: frame }, 0);
  tl.fromTo("#dmi", { opacity: 0.0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 0.1);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tK);
  tl.to("#lab1", { opacity: 0, duration: 0.3 }, tW - 0.3);
  tl.fromTo("#ring", { opacity: 0, scale: 1.05 }, { opacity: 1, scale: 1, duration: 0.3, yoyo: true, repeat: 3 }, tS);
  tl.to("#tl", { opacity: 1, duration: 0.3 }, tB);
  // gentle camera drift towards the screen
  tl.fromTo("#fog, #dmi, #ring", { scale: 1.0, transformOrigin: "1500px 600px" }, { scale: 1.06, duration: D, ease: "sine.inOut" }, 0);
"""
