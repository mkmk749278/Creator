TITLE = "C5 Wrong form, no caution order, walkie-talkies, training"
HUD = "17.06.2024 · 08:50 · RANGAPANI–CHATTERHAT"
LIBS = ["kanchan.js"]
CSS = """
  .form { position: absolute; top: 250px; width: 420px; height: 300px; background: #EDE6D3; border-radius: 8px;
    box-shadow: 0 22px 50px rgba(0,0,0,0.55); color: #2B2418; box-sizing: border-box; padding: 28px 34px; }
  .form .code { font: 800 92px/1 Inter, Arial, sans-serif; letter-spacing: -0.01em; }
  .form .ln { height: 10px; background: rgba(59,51,38,0.22); border-radius: 5px; margin: 16px 0; }
  .form .use { font: 800 24px/1.3 Inter, Arial, sans-serif; letter-spacing: 0.04em; color: #3B3326; margin-top: 22px; }
  .form .ring { position: absolute; inset: -10px; border-radius: 14px; border: 8px solid #DC2626; opacity: 0; }
  #fa { left: 460px; } #fd { left: 1040px; }
  #neq { position: absolute; left: 925px; top: 330px; font: 800 110px/1 Inter, Arial, sans-serif; color: #F87171; opacity: 0; }
  #stn { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
  .chip { font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #F8FAFC; }
"""
BODY = """  <svg id="schem" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div class="form" id="fa"><div class="code">T/A 912</div><div class="use">For passing a failed automatic signal</div><div class="ln" style="width:72%"></div><div class="ring" id="ra"></div></div>
  <div class="form" id="fd"><div class="code">T/D 912</div><div class="use">For when all signals fail · what the rules required here</div><div class="ln" style="width:70%"></div></div>
  <div id="neq">≠</div>
  <svg id="stn" viewBox="0 0 1920 1080" data-layout-allow-overflow>
    <g id="bldg" opacity="0" transform="translate(960 400)">
      <path d="M -170 90 L -170 -30 L 0 -120 L 170 -30 L 170 90 Z" fill="#0B1220" stroke="#94A3B8" stroke-width="4"/>
      <rect x="-40" y="20" width="80" height="70" fill="#1E293B" stroke="#94A3B8" stroke-width="3"/>
      <text x="0" y="-20" text-anchor="middle" style="font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.16em; fill: #CBD5E1">STATION</text></g>
    <g id="ring" opacity="0"><circle cx="960" cy="400" r="330" fill="none" stroke="#DC2626" stroke-width="4" stroke-dasharray="14 12"/></g>
    <g class="ck" id="ck1" opacity="0" transform="translate(560 640)"><rect x="-230" y="-44" width="460" height="88" rx="14" fill="rgba(15,23,42,0.92)" stroke="#DC2626" stroke-width="3"/>
      <text x="-150" y="12" class="chip">CAUTION ORDER</text><path class="x" d="M -206 -16 L -178 16 M -178 -16 L -206 16" stroke="#F87171" stroke-width="7" stroke-linecap="round"/></g>
    <g class="ck" id="ck2" opacity="0" transform="translate(1360 640)"><rect x="-230" y="-44" width="460" height="88" rx="14" fill="rgba(15,23,42,0.92)" stroke="#DC2626" stroke-width="3"/>
      <text x="-150" y="12" class="chip">WALKIE-TALKIES</text><path class="x" d="M -206 -16 L -178 16 M -178 -16 L -206 16" stroke="#F87171" stroke-width="7" stroke-linecap="round"/></g>
    <g class="ck" id="ck3" opacity="0" transform="translate(960 790)"><rect x="-230" y="-44" width="460" height="88" rx="14" fill="rgba(15,23,42,0.92)" stroke="#DC2626" stroke-width="3"/>
      <text x="-150" y="12" class="chip">TRAINING</text><path class="x" d="M -206 -16 L -178 16 M -178 -16 L -206 16" stroke="#F87171" stroke-width="7" stroke-linecap="round"/></g>
  </svg>
  <div class="kav-label red" id="lab1">T/A 912 ≠ T/D 912<small>THE WRONG FORM</small></div>
  <div class="kav-label red" id="lab2">Failures of the system<small>NOT JUST ONE LOCO PILOT</small></div>"""
JS = """
  const S = buildKanchan();
  tl.set("#pass", { x: 1260 }, 0); tl.set("#goods", { x: 760 }, 0);
  tl.set(".asig .lamp-on", { opacity: 0 }, 0); tl.set(".asig rect", { attr: { stroke: "#7F1D1D" } }, 0); tl.set(".lbl", { opacity: 0 }, 0); tl.set(".asig text", { opacity: 0 }, 0);
  tl.fromTo("#world", { transformOrigin: "50% 50%", scale: 1.3, x: -40, y: 160, opacity: 0.4 }, { scale: 1.36, x: -80, y: 170, opacity: 0.32, duration: D, ease: "sine.inOut" }, 0);
  // the two forms come in; on "wrong form, T-A nine one two" the T/A slip gets the crimson ring and slides to the goods train
  tl.from("#fa", { opacity: 0, y: 50, rotation: -3, duration: 0.7, ease: "power3.out" }, 0.2);
  tl.from("#fd", { opacity: 0, y: 50, rotation: 3, duration: 0.7, ease: "power3.out" }, 0.45);
  tl.to("#fa", { rotation: -2, y: -8, duration: 4, ease: "sine.inOut" }, 1.0);
  tl.to("#fd", { rotation: 2, y: 6, duration: 4, ease: "sine.inOut" }, 1.0);
  const tA = at("V049", "T-A nine one two"), tD = at("V049", "instead of T-D");
  tl.to("#ra", { opacity: 1, duration: 0.3 }, tA);
  tl.to("#fa", { scale: 1.08, duration: 0.4, ease: "back.out(2)" }, tA);
  tl.to("#neq", { opacity: 1, duration: 0.3 }, tD);
  tl.to("#fd", { opacity: 0.55, duration: 0.5 }, tD + 0.2);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tD);
  // forms clear; the station and the three missing pieces tick crimson around it
  const tC = at("V049", "with no caution order");
  tl.to("#fa", { x: -420, y: 260, scale: 0.55, rotation: -12, opacity: 0.0, duration: 0.8, ease: "power2.in" }, tC - 0.6);
  tl.to("#fd, #neq", { opacity: 0, duration: 0.5 }, tC - 0.6);
  tl.to("#bldg", { opacity: 1, duration: 0.5 }, tC - 0.3);
  tl.to("#world", { opacity: 0.18, duration: 0.6 }, tC - 0.3);
  const ticks = [["#ck1", tC], ["#ck2", at("V049", "missing walkie talkies")], ["#ck3", at("V049", "training that")]];
  ticks.forEach(([s, t]) => {
    tl.fromTo(s, { opacity: 0, scale: 0.9, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, t);
    tl.from(s + " .x", { opacity: 0, scale: 2.2, transformOrigin: "50% 50%", duration: 0.3 }, t + 0.25);
  });
  const tS = at("V049", "failures of the system");
  tl.to("#lab1", { opacity: 0, duration: 0.3 }, tS - 0.3);
  tl.fromTo("#ring", { opacity: 0, scale: 0.85, transformOrigin: "960px 400px" }, { opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }, tS);
  tl.to("#ring circle", { attr: { "stroke-dashoffset": -120 }, duration: D - tS, ease: "none" }, tS);
  tl.to("#lab2", { opacity: 1, duration: 0.5 }, tS + 0.2);
  tl.to("#bldg", { scale: 1.05, transformOrigin: "50% 50%", duration: D - tC, ease: "sine.inOut" }, tC);
"""
