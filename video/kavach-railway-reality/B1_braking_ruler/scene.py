TITLE = "B1 Vande Bharat: 654 m from 130 km/h"
LIBS = ["tele.js"]
CSS = """
  #tele { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .ax { font: 600 20px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.06em; font-variant-numeric: tabular-nums; }
  .chip { font: 800 30px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
  .big { font: 800 64px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
"""
BODY = """  <svg id="tele" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div class="kav-label amber" id="lab1">Vande Bharat · 130 km/h<small>EMERGENCY BRAKE · 654 M</small></div>"""
JS = """
  const svg = document.getElementById("tele"), E = KT.el;
  const cam = E("g", { id: "cam" }, svg);
  KT.rail(cam, 330);
  const C = KT.chart(cam, { x0: 300, x1: 1640, y0: 720, y1: 470, maxD: 700, maxV: 140, vTicks: [0, 50, 100, 130], dMinor: 25, dMajor: 100, dLabels: true });
  const curve = E("path", { id: "curve", d: "M 0 0", fill: "none", stroke: "#F59E0B", "stroke-width": 6, "stroke-linecap": "round" }, cam);
  const pt = E("circle", { r: 10, fill: "#F59E0B", opacity: 0 }, cam);
  const stopG = E("g", { id: "stopG", opacity: 0 }, cam);
  E("line", { x1: C.X(654), y1: 360, x2: C.X(654) + 0.3, y2: 736, stroke: "#F59E0B", "stroke-width": 3, "stroke-dasharray": "8 8" }, stopG);
  const big = E("text", { x: C.X(654) - 26, y: 560, "text-anchor": "end", class: "big" }, stopG); big.textContent = "654 m";
  const brk = E("g", { id: "brk", opacity: 0 }, cam);
  E("line", { x1: C.X(0), y1: 360, x2: C.X(0) + 0.3, y2: 736, stroke: "#38BDF8", "stroke-width": 3, "stroke-dasharray": "8 8" }, brk);
  const bt = E("text", { x: C.X(0) + 14, y: 400, class: "ax", fill: "#7DD3FC" }, brk); bt.textContent = "EMERGENCY BRAKE";
  const train = KT.trainset(cam, "train", 330);
  const chipG = E("g", { id: "chipG" }, cam);
  E("rect", { x: -150, y: 230, width: 190, height: 52, rx: 10, fill: "rgba(15,23,42,0.9)", stroke: "#38BDF8", "stroke-width": 2 }, chipG);
  const chip = E("text", { x: -55, y: 267, "text-anchor": "middle", class: "chip" }, chipG); chip.textContent = "130 km/h";
  // camera: gentle push-in, then a drift right to follow the stop
  tl.fromTo("#cam", { transformOrigin: "50% 50%", scale: 1.0, x: 30, y: 40 }, { scale: 1.05, x: -30, y: 30, duration: D, ease: "sine.inOut" }, 0);
  tl.from("#chart", { opacity: 0, y: 30, duration: 0.8, ease: "power3.out" }, 0.2);
  tl.from(".ruler line", { opacity: 0, duration: 0.25, stagger: 0.02 }, 0.4);
  // physics: approach at 130 km/h to scale on the ruler (36.1 m/s), brake on "needs about", constant deceleration to 654 m
  const PXM = (C.X(700) - C.X(0)) / 700, tB = at("V023", "needs about") - 0.2, T = Math.min(5.6, CUES.cues.V023.to + 0.1 - tB);
  const pos = { d: -36.1 * tB }, place = () => {
    const d = pos.d, x = C.X(d);
    train.setAttribute("transform", `translate(${x} 0)`); chipG.setAttribute("transform", `translate(${x} 0)`);
    const v = d <= 0 ? 130 : 130 * Math.sqrt(Math.max(0, 1 - d / 654));
    chip.textContent = `${Math.round(v)} km/h`;
    if (d > 0) { const kk = 1 - Math.sqrt(Math.max(0, 1 - d / 654)); curve.setAttribute("d", KT.stopPath(C, 130, 654, 120).split("L").slice(0, Math.max(1, Math.round(120 * kk) + 1)).join("L")); pt.setAttribute("cx", x); pt.setAttribute("cy", C.Yv(v)); }
    else { curve.setAttribute("d", `M ${C.X(0)} ${C.Yv(130)}`); pt.setAttribute("cx", C.X(0)); pt.setAttribute("cy", C.Yv(130)); }
  };
  place();
  tl.to(pos, { d: 0, duration: tB, ease: "none", onUpdate: place }, 0);
  const u = { k: 0 };
  tl.to(u, { k: 1, duration: T, ease: "none", onUpdate: () => { pos.d = 654 * (1 - Math.pow(1 - u.k, 2)); place(); } }, tB);
  tl.set(pt, { opacity: 1 }, tB);
  tl.to("#brk", { opacity: 1, duration: 0.3 }, tB);
  tl.to("#stopG", { opacity: 1, duration: 0.5 }, tB + T - 0.2);
  tl.to("#lab1", { opacity: 1, duration: 0.6 }, at("V023", "A Vande Bharat"));
"""
