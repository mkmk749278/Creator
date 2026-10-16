TITLE = "B5 Danger inside the stopping distance"
LIBS = ["tele.js"]
CSS = """
  #full { position: absolute; inset: 0; width: 1920px; height: 1080px; }
  .fl { font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.14em; }
"""
BODY = """  <svg id="full" viewBox="300 150 1480 832" data-layout-allow-overflow></svg>
  <div class="kav-label red" id="lab1">Inside the stopping distance<small>PHYSICS STILL WINS</small></div>"""
JS = """
  const full = document.getElementById("full"), E = KT.el;
  KT.rail(full, 640);
  const zone = E("rect", { x: 1150, y: 300, width: 280, height: 360, fill: "rgba(220,38,38,0.22)", opacity: 0 }, full);
  const curve = E("path", { d: "M 400 430 L 760 430 C 1000 430, 1260 480, 1430 600", fill: "none", stroke: "#38BDF8", "stroke-width": 6, "stroke-linecap": "round" }, full);
  E("circle", { cx: 760, cy: 430, r: 12, fill: "#38BDF8" }, full);
  const bt = E("text", { x: 760, y: 400, "text-anchor": "middle", class: "fl", fill: "#7DD3FC" }, full); bt.textContent = "KAVACH BRAKES";
  E("line", { x1: 1430, y1: 620, x2: 1430.3, y2: 700, stroke: "#38BDF8", "stroke-width": 4 }, full);
  const st = E("text", { x: 1440, y: 735, class: "fl", fill: "#7DD3FC" }, full); st.textContent = "STOP POINT";
  const obs = E("g", { opacity: 0 }, full);
  E("rect", { x: 1130, y: 560, width: 40, height: 80, rx: 6, fill: "#DC2626", stroke: "#FCA5A5", "stroke-width": 3 }, obs);
  const ot = E("text", { x: 1150, y: 530, "text-anchor": "middle", class: "fl", fill: "#FCA5A5" }, obs); ot.textContent = "DANGER";
  const train = KT.trainset(full, "tr", 640);
  tl.fromTo("#full", { transformOrigin: "50% 50%", scale: 1.0 }, { scale: 1.06, duration: D, ease: "sine.inOut" }, 0);
  // the train runs in again under its braking curve; danger appears inside the stopping distance
  const tD = at("V030", "If danger appears"), tC = at("V030", "even Kavach");
  tl.fromTo(train, { x: 300 }, { x: 760, duration: tD + 0.3, ease: "none" }, 0);
  tl.fromTo(obs, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, tD + 0.2);
  tl.to(zone, { opacity: 1, duration: 0.5 }, tD + 0.7);
  tl.to(zone, { opacity: 0.5, duration: 0.5, yoyo: true, repeat: 4, ease: "sine.inOut" }, tD + 1.2);
  tl.to(train, { x: 1080, duration: D - tD - 0.3, ease: "power2.out" }, tD + 0.3);
  tl.to(curve, { attr: { stroke: "#F87171" }, duration: 0.4 }, tC);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tD + 0.7);
"""
