TITLE = "E13_ch_crashes Chapter card: TWO CRASHES"
BG = "none"
CSS = """
  #sweep { display: none; }
  #slate { position: absolute; inset: -80px; background:
      radial-gradient(ellipse at 30% 40%, rgba(56,189,248,0.07), rgba(0,0,0,0) 60%),
      repeating-linear-gradient(115deg, rgba(255,255,255,0.018) 0 2px, rgba(0,0,0,0) 2px 9px),
      linear-gradient(160deg, #111a2e, #0b1220 60%, #070b14); }
  #rail { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
  #num { position: absolute; left: 110px; top: 596px; font: 800 34px Inter, Arial, sans-serif; letter-spacing: 0.3em; color: #EF4444; opacity: 0; }
  #word { position: absolute; left: 104px; top: 640px; font: 800 150px/1 Inter, Arial, sans-serif; letter-spacing: -0.01em; color: #F8FAFC; white-space: nowrap;
    clip-path: inset(0 100% 0 0); text-shadow: 0 8px 40px rgba(0,0,0,0.6); }
"""
BODY = """  <div id="slate"></div>
  <svg id="rail" viewBox="0 0 1920 1080" data-layout-allow-overflow>
    <g id="trk"><path id="r1" d="M -40 840 L 1960 840.4" stroke="#EF4444" stroke-width="5" fill="none"/><path id="r2" d="M -40 872 L 1960 872.4" stroke="#EF4444" stroke-width="5" fill="none"/>
      <g id="sl" stroke="#EF4444" stroke-width="4" opacity="0.55"></g></g>
    <circle id="dot" r="9" cy="856" cx="-40" fill="#EF4444"/>
  </svg>
  <div id="num">CHAPTER 3</div>
  <div id="word">TWO CRASHES</div>"""
JS = """
  const NS = "http://www.w3.org/2000/svg", sl = document.getElementById("sl");
  for (let x = -20; x < 1960; x += 34) { const l = document.createElementNS(NS, "line"); l.setAttribute("x1", x); l.setAttribute("x2", x + 0.3); l.setAttribute("y1", 832); l.setAttribute("y2", 880); sl.appendChild(l); }
  for (const id of ["r1", "r2"]) { const p = document.getElementById(id), L = p.getTotalLength(); p.setAttribute("stroke-dasharray", L); p.setAttribute("stroke-dashoffset", L);
    tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 0.8, ease: "power2.out" }, 0.05); }
  tl.fromTo("#sl", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power2.out" }, 0.05);
  tl.fromTo("#dot", { attr: { cx: -40 } }, { attr: { cx: 1960 }, duration: 0.8, ease: "power2.out" }, 0.05);
  tl.to("#num", { opacity: 1, duration: 0.3 }, 0.25);
  tl.to("#word", { clipPath: "inset(0 0% 0 0)", duration: 0.55, ease: "power3.out" }, 0.3);
  tl.fromTo("#word", { x: -30 }, { x: 10, duration: D, ease: "power1.out" }, 0.3);
  tl.fromTo("#slate", { x: 0, y: 0 }, { x: -60, y: -20, duration: D, ease: "none" }, 0);
  tl.fromTo("#trk", { x: 0 }, { x: -40, duration: D, ease: "none" }, 0);
  tl.to(["#word", "#num", "#rail"], { opacity: 0, duration: 0.25 }, D - 0.25);
"""
