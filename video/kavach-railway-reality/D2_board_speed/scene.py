TITLE = "D2 36 metres every second"
LIBS = ["tele.js"]
CSS = """
  #tele { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .ax { font: 800 22px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.12em; }
  .sec { font: 800 34px Inter, Arial, sans-serif; fill: #F8FAFC; letter-spacing: 0.06em; font-variant-numeric: tabular-nums; }
  .m36 { font: 800 54px Inter, Arial, sans-serif; fill: #38BDF8; font-variant-numeric: tabular-nums; }
  .clk { font: 800 92px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
  #lab { top: 80px; bottom: auto; }
  .clu { font: 800 24px Inter, Arial, sans-serif; fill: #94A3B8; letter-spacing: 0.16em; }
"""
BODY = """  <svg id="tele" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div class="kav-label" id="lab">130 km/h<small>OUR CALCULATION · 130 ÷ 3.6 ≈ 36 M/S</small></div>"""
JS = """
  // real time, real scale: 8.5 px per metre, 130 km/h = 36.1 m/s = 307 px every second
  const svg = document.getElementById("tele"), E = KT.el, PXM = 8.5, V = 130 / 3.6, RY = 600, X0 = 210;
  const cam = E("g", { id: "cam" }, svg);
  // overhead-line masts every 45 m and the ground
  E("rect", { x: -200, y: RY + 20, width: 2400, height: 500, fill: "rgba(15,23,42,0.6)" }, cam);
  for (let m = -30; m < 200; m += 45) { const x = X0 + m * PXM; E("line", { x1: x, y1: RY + 4, x2: x + 0.3, y2: RY - 230, stroke: "#334155", "stroke-width": 7 }, cam);
    E("line", { x1: x, y1: RY - 214, x2: x + 60, y2: RY - 214.3, stroke: "#334155", "stroke-width": 4 }, cam); }
  E("line", { x1: -200, y1: RY - 186, x2: 2200, y2: RY - 185.6, stroke: "rgba(148,163,184,0.45)", "stroke-width": 2 }, cam);
  KT.rail(cam, RY);
  // a post every 36.1 m: one second of travel each
  const posts = [], brs = [];
  for (let k = 0; k <= 4; k++) { const x = X0 + k * V * PXM, g = E("g", { opacity: k ? 0.25 : 1 }, cam);
    E("line", { x1: x, y1: RY + 24, x2: x + 0.3, y2: RY + 120, stroke: "#38BDF8", "stroke-width": 4 }, g);
    E("rect", { x: x - 52, y: RY + 128, width: 104, height: 50, rx: 8, fill: "rgba(11,37,64,0.95)", stroke: "#38BDF8", "stroke-width": 2 }, g);
    E("text", { x, y: RY + 164, "text-anchor": "middle", class: "sec" }, g).textContent = k + " S"; posts.push(g);
    if (k) { const b = E("g", { opacity: 0 }, cam), xa = X0 + (k - 1) * V * PXM + 8, xb = x - 8, yb = RY + 236;
      E("path", { d: `M ${xa} ${yb - 14} L ${xa} ${yb} L ${xb} ${yb + 0.3} L ${xb} ${yb - 14}`, fill: "none", stroke: "#38BDF8", "stroke-width": 3 }, b);
      E("text", { x: (xa + xb) / 2, y: yb + 66, "text-anchor": "middle", class: "m36" }, b).textContent = "36 m"; brs.push(b); } }
  const train = KT.trainset(cam, "train", RY);
  train.setAttribute("transform", `translate(${X0} 0) scale(1.3 1.3)`);
  // stopwatch
  const clk = E("g", { id: "clkg" }, svg);
  E("circle", { cx: 1560, cy: 180, r: 96, fill: "rgba(11,18,32,0.9)", stroke: "#334155", "stroke-width": 6 }, clk);
  const arc = E("path", { fill: "none", stroke: "#38BDF8", "stroke-width": 10, "stroke-linecap": "round" }, clk);
  const hand = E("line", { x1: 1560, y1: 180, x2: 1560, y2: 100, stroke: "#F8FAFC", "stroke-width": 5, "stroke-linecap": "round" }, clk);
  E("circle", { cx: 1560, cy: 180, r: 9, fill: "#F8FAFC" }, clk);
  const ct = E("text", { x: 1380, y: 212, "text-anchor": "end", class: "clk" }, clk), cu = E("text", { x: 1380, y: 250, "text-anchor": "end", class: "clu" }, clk);
  cu.textContent = "METRES TRAVELLED";
  const t0 = at("V024", "At that speed");
  const st = { t: 0 }, place = () => {
    const s = st.t - t0, x = X0 + s * V * PXM;                 // nose position (s < 0 before the start post)
    train.setAttribute("transform", `translate(${x} ${RY - RY * 1.3}) scale(1.3)`);
    const sec = Math.max(0, s), ph = sec % 1, a = ph * Math.PI * 2;
    hand.setAttribute("x2", 1560 + 80 * Math.sin(a)); hand.setAttribute("y2", 180 - 80 * Math.cos(a));
    arc.setAttribute("d", ph < 0.002 ? "M 1560 90" : `M 1560 90 A 90 90 0 ${ph > 0.5 ? 1 : 0} 1 ${1560 + 90 * Math.sin(a)} ${180 - 90 * Math.cos(a)}`);
    ct.textContent = Math.round(sec * V);
    posts.forEach((g, k) => g.setAttribute("opacity", k === 0 || sec >= k ? 1 : 0.25));
    brs.forEach((b, k) => b.setAttribute("opacity", Math.min(1, Math.max(0, (sec - (k + 1)) * 5 + 1))));
  };
  place();
  tl.to(st, { t: D, duration: D, ease: "none", onUpdate: place }, 0);
  tl.fromTo("#cam", { transformOrigin: "960px 640px", scale: 1.1 }, { scale: 1.16, duration: D, ease: "sine.inOut" }, 0);
  tl.to("#lab", { opacity: 1, duration: 0.5 }, at("V024", "thirty six") - 0.3);
"""
