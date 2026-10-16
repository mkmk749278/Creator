TITLE = "B5 Danger inside the stopping distance"
LIBS = ["tele.js"]
CSS = """
  #full { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .fl { font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.1em; }
  .big { font: 800 56px Inter, Arial, sans-serif; font-variant-numeric: tabular-nums; }
  .chip { font: 800 34px Inter, Arial, sans-serif; fill: #F8FAFC; font-variant-numeric: tabular-nums; }
  #flash { position: absolute; inset: 0; background: radial-gradient(circle at 1050px 600px, rgba(254,202,202,0.95), rgba(220,38,38,0.35) 30%, rgba(0,0,0,0) 60%); opacity: 0; }
"""
BODY = """  <svg id="full" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>
  <div id="flash" data-layout-allow-occlusion></div>
  <div class="kav-label red" id="lab1">Danger too close<small>ILLUSTRATION · 110 KM/H</small></div>"""
JS = """
  // ILLUSTRATION: 110 km/h (30.6 m/s), braking about 1 m/s^2 -> needs about 470 m; danger appears 250 m ahead,
  // so the train still reaches it at sqrt(30.6^2 - 2 x 250) = 20.9 m/s = about 75 km/h.
  const full = document.getElementById("full"), E = KT.el, K = 3.0, NX = 300, RY = 560;
  const V0 = 110 / 3.6, A = 1.0, DS = V0 * V0 / (2 * A), DD = 250, VI = Math.sqrt(V0 * V0 - 2 * A * DD), TI = (V0 - VI) / A;
  const X = (m) => NX + m * K;          // metres from the braking point
  const cam = E("g", { id: "cam" }, full);
  KT.rail(cam, RY);
  for (let m = -100; m <= 520; m += 50) { E("line", { x1: X(m), y1: RY + 26, x2: X(m) + 0.3, y2: RY + (m % 100 ? 38 : 50), stroke: m % 100 ? "#475569" : "#94A3B8", "stroke-width": m % 100 ? 2 : 3 }, cam);
    if (m >= 0 && m % 100 === 0) E("text", { x: X(m), y: RY + 84, "text-anchor": "middle", class: "fl", fill: "#94A3B8", style: "font-size:24px" }, cam).textContent = m + " m"; }
  // stopping distance (cyan) and danger distance (red) brackets
  const need = E("g", { opacity: 0 }, cam), by = RY - 200;
  E("path", { d: `M ${X(0)} ${by + 16} L ${X(0)} ${by} L ${X(DS)} ${by + 0.4} L ${X(DS)} ${by + 16}`, fill: "none", stroke: "#38BDF8", "stroke-width": 4 }, need);
  E("text", { x: X(DS / 2), y: by - 22, "text-anchor": "middle", class: "fl", fill: "#7DD3FC" }, need).textContent = "NEEDS ≈ 470 M TO STOP";
  E("line", { x1: X(DS), y1: by, x2: X(DS) + 0.3, y2: RY, stroke: "#38BDF8", "stroke-width": 2, "stroke-dasharray": "8 8" }, need);
  const dang = E("g", { opacity: 0 }, cam), dy = RY + 140;
  E("path", { d: `M ${X(0)} ${dy - 16} L ${X(0)} ${dy} L ${X(DD)} ${dy + 0.4} L ${X(DD)} ${dy - 16}`, fill: "none", stroke: "#F87171", "stroke-width": 4 }, dang);
  E("text", { x: X(DD / 2), y: dy + 50, "text-anchor": "middle", class: "fl", fill: "#FCA5A5" }, dang).textContent = "DANGER ONLY 250 M AWAY";
  const obs = E("g", { opacity: 0 }, cam);
  E("rect", { x: X(DD) + 2, y: RY - 90, width: 46, height: 88, rx: 6, fill: "#DC2626", stroke: "#FCA5A5", "stroke-width": 3 }, obs);
  E("text", { x: X(DD) + 64, y: RY - 36, class: "fl", fill: "#FCA5A5" }, obs).textContent = "DANGER";
  const train = KT.trainset(cam, "tr", RY);
  const chipG = E("g", {}, cam);
  E("rect", { x: -190, y: RY - 150, width: 210, height: 60, rx: 12, fill: "rgba(15,23,42,0.92)", stroke: "#38BDF8", "stroke-width": 2 }, chipG);
  const chip = E("text", { x: -85, y: RY - 108, "text-anchor": "middle", class: "chip" }, chipG); chip.textContent = "110 km/h";
  const hit = E("g", { opacity: 0 }, cam);
  E("rect", { x: X(DD / 2) - 300, y: RY + 230, width: 600, height: 96, rx: 14, fill: "rgba(15,23,42,0.92)", stroke: "#F87171", "stroke-width": 3 }, hit);
  E("text", { x: X(DD / 2), y: RY + 297, "text-anchor": "middle", class: "big", fill: "#F87171" }, hit).textContent = "HITS AT ≈ 75 KM/H";
  const tD = at("V030", "If danger appears"), tC = at("V030", "even Kavach");
  const tB = tD + 0.25, TP = Math.max(1.6, tC + 0.9 - tB);          // presentation time from braking to impact
  const st = { t: 0 }, place = () => {
    const t = st.t; let d, v;
    if (t < tB) { d = -V0 * (tB - t); v = V0; }
    else { const s = Math.min(TI, (t - tB) * TI / TP); d = V0 * s - 0.5 * A * s * s; v = V0 - A * s; }
    const x = X(Math.min(d, DD));
    train.setAttribute("transform", `translate(${x} 0)`); chipG.setAttribute("transform", `translate(${x} 0)`);
    chip.textContent = `${Math.round(v * 3.6)} km/h`;
    chip.setAttribute("fill", t >= tB ? "#FCA5A5" : "#F8FAFC");
  };
  place();
  tl.to(st, { t: D, duration: D, ease: "none", onUpdate: place }, 0);
  tl.fromTo(obs, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, tD);
  tl.to(need, { opacity: 1, duration: 0.4 }, tB);
  tl.to(dang, { opacity: 1, duration: 0.4 }, tB + 0.6);
  const tI = tB + TP;
  tl.to("#flash", { opacity: 1, duration: 0.08 }, tI).to("#flash", { opacity: 0, duration: 0.6 }, tI + 0.08);
  tl.fromTo("#cam", { x: 0 }, { x: 10, duration: 0.05, yoyo: true, repeat: 5 }, tI);
  tl.to(hit, { opacity: 1, duration: 0.3 }, tI + 0.1);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tB + 0.3);
  tl.fromTo("#cam", { scale: 1.08, transformOrigin: "960px 600px" }, { scale: 1.14, duration: D, ease: "sine.inOut" }, 0);
"""
