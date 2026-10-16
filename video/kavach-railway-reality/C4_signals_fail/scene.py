TITLE = "C4 Rangapani: automatic signals failed"
HUD = "17.06.2024 · 08:50 · RANGAPANI–CHATTERHAT"
LIBS = ["kanchan.js"]
CSS = """
  #slip { position: absolute; left: 960px; top: 640px; width: 430px; height: 270px; transform: rotate(-4deg);
    background: #EDE6D3; border-radius: 6px; box-shadow: 0 18px 40px rgba(0,0,0,0.5); color: #3B3326; padding: 26px 30px; box-sizing: border-box; }
  #slip h4 { margin: 0 0 16px; font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.12em; color: #2B2418; }
  #slip .ln { height: 10px; background: rgba(59,51,38,0.25); border-radius: 5px; margin: 13px 0; }
  #rule { position: absolute; left: 1180px; top: 190px; width: 600px; padding: 20px 26px; background: rgba(15,23,42,0.92); border: 2px solid #F59E0B; border-radius: 12px; opacity: 0;
    font: 800 40px/1.2 Inter, Arial, sans-serif; color: #F8FAFC; }
  #rule small { display: block; font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.12em; color: #FCD34D; margin-bottom: 8px; }
  #slip .stamp { position: absolute; right: 28px; bottom: 22px; width: 96px; height: 96px; border-radius: 50%;
    border: 5px double rgba(185,28,28,0.75); transform: rotate(12deg); }
"""
BODY = """  <svg id="schem" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="slip" data-layout-allow-occlusion><h4>PAPER AUTHORITY</h4><div class="ln" style="width:92%"></div><div class="ln" style="width:78%"></div>
    <div class="ln" style="width:85%"></div><div class="ln" style="width:60%"></div><div class="stamp"></div></div>
  <div id="rule"><small>THE RULE · GR 9.02</small>At each failed signal: stop 1 min, then max 15 km/h</div>
  <div class="kav-label" id="lab1">Rangapani · 17 Jun 2024<small>NEAR NEW JALPAIGURI, NORTH BENGAL</small></div>
  <div class="kav-label red" id="lab2">Signals failed<small>AUTOMATIC BLOCK SIGNALLING</small></div>"""
JS = """
  const S = buildKanchan();
  tl.set("#pass", { x: 1150 }, 0);
  tl.set("#goods", { x: -200 }, 0);
  tl.fromTo("#world", { transformOrigin: "50% 50%", scale: 1.16, x: 60, y: 70 }, { scale: 1.24, x: -40, y: 60, duration: D, ease: "sine.inOut" }, 0);
  tl.from("#t-up, #t-dn", { opacity: 0, duration: 1.0, stagger: 0.3 }, 0.1);
  tl.from(".asig", { opacity: 0, y: 24, duration: 0.5, stagger: 0.15 }, 0.6);
  tl.from("#pass", { opacity: 0, duration: 0.8 }, 1.2);
  tl.to("#lab1", { opacity: 1, duration: 0.6 }, at("V048", "Rangapani"));
  const tF = at("V048", "The automatic signals had failed");
  tl.to("#lab1", { opacity: 0, duration: 0.3 }, tF);
  // each automatic signal flickers and goes dark, one after another
  document.querySelectorAll(".asig .lamp-on").forEach((el, i) => {
    const t = tF + 0.2 + i * 0.28;
    tl.to(el, { opacity: 0.2, duration: 0.06 }, t).to(el, { opacity: 0.9, duration: 0.06 }, t + 0.08).to(el, { opacity: 0, duration: 0.12 }, t + 0.18);
  });
  tl.to(".asig rect", { attr: { stroke: "#7F1D1D" }, duration: 0.6 }, tF + 1.6);
  tl.to("#lab2", { opacity: 1, duration: 0.6 }, tF + 0.6);
  const tP = at("V048", "on a paper authority");
  tl.to("#lbl-up, #lbl-dn", { opacity: 0, duration: 0.3 }, tP - 0.6);
  tl.from("#slip", { opacity: 0, y: 60, rotation: 4, duration: 0.8, ease: "power3.out" }, tP - 0.3);
  // both trains creep forward slowly from "paper authority" to the end
  tl.to("#pass", { x: 1260, duration: D - tP, ease: "none" }, tP);
  tl.to("#goods", { x: 760, duration: D - tP + 0.6, ease: "power1.out" }, tP - 0.6);
  tl.fromTo("#rule", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, at("V048", "at a slow"));
  tl.to("#slip", { y: -10, rotation: -2.5, duration: D - tP, ease: "sine.inOut" }, tP + 0.5);
"""
