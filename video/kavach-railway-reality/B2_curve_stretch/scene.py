TITLE = "B2 130 to 160 km/h: about half again"
LIBS = ["tele.js"]
CSS = """
  #tele { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .ax { font: 600 20px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.06em; font-variant-numeric: tabular-nums; }
  .tag { font: 800 28px Inter, Arial, sans-serif; letter-spacing: 0.06em; font-variant-numeric: tabular-nums; }
  .big { font: 800 96px Inter, Arial, sans-serif; fill: #F59E0B; font-variant-numeric: tabular-nums; }
"""
BODY = """  <svg id="tele" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div class="kav-label amber" id="lab1">+50%<small>130 → 160 KM/H · SAME BRAKES</small></div>"""
JS = """
  const svg = document.getElementById("tele"), E = KT.el;
  const cam = E("g", { id: "cam" }, svg);
  const C = KT.chart(cam, { x0: 260, x1: 1680, y0: 760, y1: 300, maxD: 1100, maxV: 170, vTicks: [0, 130, 160], dMinor: 50, dMajor: 250, dLabels: false });
  const D130 = 654, D160 = 654 * Math.pow(160 / 130, 2);   // same deceleration: distance scales with speed squared
  const c130 = E("path", { d: KT.stopPath(C, 130, D130, 120), fill: "none", stroke: "#38BDF8", "stroke-width": 6, "stroke-linecap": "round" }, cam);
  const c160 = E("path", { d: KT.stopPath(C, 160, D160, 120), fill: "none", stroke: "#F59E0B", "stroke-width": 7, "stroke-linecap": "round" }, cam);
  const t130 = E("text", { x: C.X(0) + 20, y: C.Yv(130) + 44, class: "tag", fill: "#7DD3FC" }, cam); t130.textContent = "130 KM/H";
  const t160 = E("text", { x: C.X(0) + 20, y: C.Yv(160) - 18, class: "tag", fill: "#FCD34D" }, cam); t160.textContent = "160 KM/H";
  const br = E("g", { id: "br", opacity: 0 }, cam);
  E("path", { d: `M ${C.X(D130)} ${C.Yv(0) + 26} L ${C.X(D130)} ${C.Yv(0) + 50} L ${C.X(D160)} ${C.Yv(0) + 50.5} L ${C.X(D160)} ${C.Yv(0) + 26}`, fill: "none", stroke: "#F59E0B", "stroke-width": 4 }, br);
  E("path", { d: `M ${(C.X(D130) + C.X(D160)) / 2} ${C.Yv(0) + 50} L ${(C.X(D130) + C.X(D160)) / 2 + 60} ${C.Yv(130) + 40}`, fill: "none", stroke: "#F59E0B", "stroke-width": 2, "stroke-dasharray": "6 6" }, br);
  const bt = E("text", { x: (C.X(D130) + C.X(D160)) / 2 + 60, y: C.Yv(130) + 20, "text-anchor": "middle", class: "big" }, br); bt.textContent = "+50%";
  const dash = (p) => { const L = p.getTotalLength(); p.setAttribute("stroke-dasharray", L); p.setAttribute("stroke-dashoffset", L); return L; };
  dash(c130); dash(c160);
  tl.fromTo("#cam", { transformOrigin: "50% 50%", scale: 1.0, x: 20 }, { scale: 1.06, x: -30, duration: D, ease: "sine.inOut" }, 0);
  tl.from("#chart", { opacity: 0, duration: 0.6 }, 0);
  tl.to(c130, { attr: { "stroke-dashoffset": 0 }, duration: 1.4, ease: "power2.out" }, Math.max(0.2, at("V026", "from one hundred and thirty") - 0.2));
  tl.from(t130, { opacity: 0, duration: 0.4 }, at("V026", "from one hundred and thirty"));
  tl.to(c130, { opacity: 0.45, duration: 0.6 }, at("V026", "to one hundred and sixty"));
  tl.to(c160, { attr: { "stroke-dashoffset": 0 }, duration: 2.0, ease: "power2.out" }, at("V026", "to one hundred and sixty"));
  tl.from(t160, { opacity: 0, duration: 0.4 }, at("V026", "to one hundred and sixty"));
  const tH = at("V026", "it grows by about half");
  tl.fromTo("#br", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(2)" }, tH);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tH + 0.2);
"""
