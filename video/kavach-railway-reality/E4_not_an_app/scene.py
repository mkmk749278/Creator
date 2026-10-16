TITLE = "E4 Kavach is not an app"
BG = "none"
LIBS = ["map.js", "mapdraw.js"]
CSS = """
  #sweep { display: none; }
  #map { position: absolute; inset: 0; width: 1920px; height: 1080px; opacity: 0; }
  #parts { position: absolute; inset: 0; width: 1920px; height: 1080px; filter: drop-shadow(0 18px 24px rgba(0,0,0,0.55)); }
  #icon { position: absolute; left: 820px; top: 300px; width: 280px; height: 280px; border-radius: 64px; background: linear-gradient(160deg, #0EA5E9, #0369A1);
    box-shadow: 0 30px 70px rgba(0,0,0,0.55), inset 0 2px 0 rgba(255,255,255,0.35); }
  #icon svg { position: absolute; left: 60px; top: 46px; }
  #icon .nm { position: absolute; left: -60px; right: -60px; top: 300px; text-align: center; font: 600 34px Inter, Arial, sans-serif; color: #E2E8F0; }
  #sw { position: absolute; left: 1220px; top: 250px; width: 420px; height: 588px; opacity: 0; }
  #note { position: absolute; left: 96px; bottom: 120px; }
"""
BODY = """  <svg id="map" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="icon"><svg width="160" height="190" viewBox="0 0 160 190"><path d="M80 8 L148 34 L148 92 C148 140 116 170 80 184 C44 170 12 140 12 92 L12 34 Z" fill="none" stroke="#F0F9FF" stroke-width="12" stroke-linejoin="round"/>
    <path d="M48 96 L72 120 L116 72" fill="none" stroke="#F0F9FF" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="nm" data-layout-allow-overflow>Kavach</div></div>
  <svg id="parts" viewBox="0 0 1920 1080" data-layout-allow-overflow>
    <!-- the real hardware (simplified, after the reference photos): loco computer, cab screen, RFID tag, roof antenna, radio tower -->
    <g id="h0" opacity="0"><rect x="-90" y="-60" width="180" height="120" rx="8" fill="#D7D8D2" stroke="#8B8F93" stroke-width="3"/><rect x="-62" y="-46" width="124" height="22" fill="#C81E1E"/>
      <g fill="#2B2F34">""" + "".join(f'<rect x="{-70 + i * 16}" y="-12" width="10" height="58"/>' for i in range(9)) + """</g><text x="0" y="82" text-anchor="middle" stroke="none" style="font: 800 13px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #CBD5E1">LOCO COMPUTER</text></g>
    <g id="h1" opacity="0"><rect x="-80" y="-66" width="160" height="132" rx="10" fill="#121315" stroke="#3A3D42" stroke-width="4"/><rect x="-62" y="-50" width="124" height="96" fill="#050607"/>
      <path d="M -40 20 A 34 34 0 1 1 20 26" fill="none" stroke="#22C55E" stroke-width="6"/><rect x="34" y="-36" width="10" height="66" fill="#38BDF8"/><text x="0" y="88" text-anchor="middle" stroke="none" style="font: 800 13px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #CBD5E1">CAB SCREEN</text></g>
    <g id="h2" opacity="0"><rect x="-80" y="-18" width="160" height="36" rx="10" fill="#AEB4BA" stroke="#6B7280" stroke-width="3"/><path d="M -10 -8 L 10 -8 L 0 -26 Z" fill="#F2C200" transform="translate(0 20)"/>
      <rect x="-56" y="18" width="10" height="28" fill="#CBD5E1"/><rect x="46" y="18" width="10" height="28" fill="#CBD5E1"/><text x="0" y="66" text-anchor="middle" stroke="none" style="font: 800 13px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #CBD5E1">RFID TAG</text></g>
    <g id="h3" opacity="0"><path d="M -50 20 A 50 46 0 0 1 50 20 Z" fill="#0D0E10" stroke="#3A3D42" stroke-width="3"/><rect x="-14" y="20" width="28" height="22" fill="#0D0E10"/><text x="0" y="62" text-anchor="middle" stroke="none" style="font: 800 13px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #CBD5E1">ROOF ANTENNA</text></g>
    <g id="h4" opacity="0" stroke="#9EA4A8" stroke-width="5" fill="none"><path d="M -40 80 L -8 -80 L 8 -80 L 40 80 M -32 40 L 32 40 M -22 -10 L 22 -10 M -36 60 L 22 -10 M 36 60 L -22 -10"/><rect x="-14" y="-104" width="28" height="22" fill="#E5E5E0" stroke="none"/><text x="0" y="104" text-anchor="middle" stroke="none" style="font: 800 13px Inter, Arial, sans-serif; letter-spacing: 0.12em; fill: #CBD5E1">RADIO TOWER</text></g>
  </svg>
  <svg id="sw" viewBox="0 0 300 420">
    <rect x="40" y="40" width="220" height="340" rx="22" fill="#2A2E34" stroke="#5B6470" stroke-width="5"/>
    <rect x="90" y="80" width="120" height="260" rx="14" fill="#15181C"/>
    <g id="lev"><rect x="134" y="120" width="32" height="150" rx="10" fill="#B91C1C"/><rect x="104" y="100" width="92" height="40" rx="14" fill="#DC2626"/></g>
    <text x="150" y="70" text-anchor="middle" style="font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #CBD5E1">ALL INDIA</text>
    <text x="150" y="372" text-anchor="middle" style="font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.14em; fill: #94A3B8">ON</text>
  </svg>
  <div class="kav-label" id="note">Not an app<small>STEEL, RADIO AND SOFTWARE ON THE GROUND</small></div>"""
JS = """
  const tW = at("V009", "what Kavach actually is"), tA = at("V009", "isn't an app"), tN = at("V009", "nobody can switch"), tO = at("V009", "overnight");
  // 1) a phone-app icon (a tempting idea)  2) it breaks into the real hardware  3) one big switch: flipped, and the map stays dark
  tl.fromTo("#icon", { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.6)" }, 0.1);
  tl.to("#icon", { y: -12, duration: tA - 0.7, ease: "sine.inOut" }, 0.7);
  const spots = [[470, 360], [960, 280], [1450, 380], [700, 720], [1250, 690]];
  spots.forEach(([x, y], i) => { tl.fromTo("#h" + i, { opacity: 0, x: 960, y: 440, scale: 0.3 }, { opacity: 1, x, y, scale: 1.9, duration: 0.7, ease: "power3.out" }, tA + 0.1 + i * 0.06);
    tl.to("#h" + i, { y: y - 14, rotation: (i % 2 ? 4 : -4), svgOrigin: `0 0`, duration: tN - tA - 0.5, ease: "sine.inOut" }, tA + 0.8); });
  tl.to("#icon", { scale: 0.2, opacity: 0, rotation: 30, duration: 0.4, ease: "power2.in" }, tA);
  tl.to("#note", { opacity: 1, duration: 0.5 }, tA + 0.4);
  // the switch over a dim India map: the lever goes down and nothing lights up
  const Mp = buildMap(document.getElementById("map"));
  tl.set("#corr", { opacity: 0 }, 0); tl.set("#rails", { opacity: 0.25 }, 0);
  tl.to(["#h0", "#h1", "#h2", "#h3", "#h4"], { opacity: 0, duration: 0.4 }, tN - 0.3);
  tl.to("#note", { opacity: 0, duration: 0.3 }, tN - 0.3);
  tl.fromTo("#map", { opacity: 0 }, { opacity: 0.55, duration: 0.6 }, tN - 0.3);
  tl.fromTo("#mworld", { transformOrigin: "880px 560px", scale: 0.92, x: -260, y: 0 }, { scale: 0.96, x: -280, y: -10, duration: D - tN + 0.3, ease: "sine.inOut" }, tN - 0.3);
  tl.fromTo("#sw", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45 }, tN);
  tl.to("#lev", { rotation: 180, svgOrigin: "150 230", duration: 0.35, ease: "power3.in" }, tN + 0.9);
  tl.fromTo("#sw", { x: 0 }, { x: 5, duration: 0.05, yoyo: true, repeat: 3 }, tN + 1.25);
  tl.to("#rails", { opacity: 0.4, duration: 0.12, yoyo: true, repeat: 1 }, tN + 1.3);
"""
