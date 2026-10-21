// S02 · Which box (0:20.9–0:34.1). Line 4. Under the stairs: the home inverter + tubular battery everyone knows,
// struck out (NOT THIS) and slid aside; then the daylight world: follow the amber cable from the panels down to the
// wall box (ON-GRID INVERTER), which we rename SOLAR BOX as its sun badge pops.
// Cues (local s, from silencedetect on the final VO): "this is not the inverter…" 1.98 · "It's the box…" 5.56 ·
// "Installers call it…" 8.07 · "We'll just call it the solar box" 11.32.
window.SCENE = function (tl, ctx) {
  const { D } = ctx, el = W36.el;
  const svg = document.getElementById("stage");
  W36.lane(svg); W36.xray(svg); document.getElementById("xray").setAttribute("opacity", 0);
  K.hud([{ k: "grid", label: "GRID", v: "230 V · 50.0 Hz", cls: "cyan", hidden: true }, { k: "box", label: "SOLAR BOX", v: "IN STEP ✓", cls: "green", hidden: true }]);
  tl.set("#slowTag", { opacity: 0 }, 0);

  // ---- 0:00 under the stairs: the backup inverter + tall tubular battery (the box people already know) ----
  const inn = el("g", { id: "inside" }, svg);
  const cam = el("g", { id: "inCam" }, inn);
  el("rect", { width: 1920, height: 1080, fill: "#E9D9B8" }, cam);                                         // distemper wall
  el("rect", { y: 840, width: 1920, height: 240, fill: "#B9A585" }, cam);                                   // floor
  for (let i = 0; i < 9; i++) el("line", { x1: i * 240, y1: 840, x2: i * 240 - 120, y2: 1080, stroke: "#A8936F", "stroke-width": 3 }, cam);
  el("rect", { y: 828, width: 1920, height: 14, fill: "#CDBB98" }, cam);                                    // skirting
  el("path", { d: "M 0 0 L 1920 0 L 1920 140 L 0 700 Z", fill: "#8E7A5A" }, cam);                           // underside of the stair waist slab
  for (let i = 0; i < 8; i++) { const x = 240 * i; el("path", { d: `M ${x} ${700 - x * 0.2917} l 240 -70 l 0 -40 l -240 70 Z`, fill: "#7A6748", opacity: 0.5 }, cam); }
  el("path", { d: "M 0 700 L 1920 140", stroke: "#6B5A3E", "stroke-width": 10 }, cam);
  el("rect", { x: 1560, y: 620, width: 26, height: 26, rx: 4, fill: "#F2F2F2", stroke: "#BDBDBD", "stroke-width": 3 }, cam); // wall socket
  el("ellipse", { cx: 940, cy: 836, rx: 520, ry: 26, fill: "rgba(60,40,20,0.28)" }, cam);              // contact shadow
  // the home inverter: dark front, small LCD, three status LEDs, vents
  const inv = el("g", { id: "homeInv" }, cam);
  el("rect", { x: 520, y: 560, width: 400, height: 270, rx: 18, fill: "#2B2F36" }, inv);
  el("rect", { x: 520, y: 560, width: 400, height: 46, rx: 18, fill: "#3A3F48" }, inv);
  el("rect", { x: 580, y: 640, width: 150, height: 70, rx: 6, fill: "#0E3B2E" }, inv);
  el("text", { x: 655, y: 690, "text-anchor": "middle", fill: "#7CF0B5", "font-family": "Inter", "font-weight": 800, "font-size": 40 }, inv).textContent = "230";
  [["#3fb950", 0], ["#d29922", 1], ["#f85149", 2]].forEach(([c, i]) => el("circle", { class: "invLed", cx: 790 + i * 44, cy: 660, r: 11, fill: c, opacity: i ? 0.35 : 1 }, inv));
  for (let i = 0; i < 6; i++) el("rect", { x: 580 + i * 50, y: 760, width: 32, height: 10, rx: 4, fill: "#1B1E23" }, inv);
  // tall tubular battery: off-white case, red lid, six float-indicator caps, two terminals
  const bat = el("g", { id: "homeBat" }, cam);
  el("rect", { x: 1060, y: 400, width: 300, height: 430, rx: 14, fill: "#F1EFEA", stroke: "#CFCAC0", "stroke-width": 4 }, bat);
  el("rect", { x: 1050, y: 380, width: 320, height: 56, rx: 12, fill: "#C0392B" }, bat);
  for (let i = 0; i < 6; i++) el("circle", { cx: 1095 + i * 46, cy: 408, r: 13, fill: i % 2 ? "#F4D03F" : "#ECF0F1", stroke: "#8E2A20", "stroke-width": 3 }, bat);
  el("rect", { x: 1080, y: 352, width: 34, height: 30, rx: 4, fill: "#7F8C8D" }, bat); el("rect", { x: 1306, y: 352, width: 34, height: 30, rx: 4, fill: "#7F8C8D" }, bat);
  el("rect", { x: 1100, y: 520, width: 220, height: 90, rx: 8, fill: "#E0DCD2" }, bat);
  el("path", { d: "M 1097 352 C 1097 300 960 300 900 560", fill: "none", stroke: "#C0392B", "stroke-width": 12, "stroke-linecap": "round" }, cam);
  el("path", { d: "M 1323 352 C 1323 270 980 260 870 560", fill: "none", stroke: "#1B1E23", "stroke-width": 12, "stroke-linecap": "round" }, cam);
  // the strike-out: two slate strokes drawn on
  const x = el("g", { id: "strike", opacity: 0.92 }, inn);
  el("path", { id: "sk1", d: "M 470 330 L 1420 880", stroke: "#2D3B4A", "stroke-width": 34, "stroke-linecap": "round", "stroke-dasharray": 1100, "stroke-dashoffset": 1100 }, x);
  el("path", { id: "sk2", d: "M 1420 330 L 470 880", stroke: "#2D3B4A", "stroke-width": 34, "stroke-linecap": "round", "stroke-dasharray": 1100, "stroke-dashoffset": 1100 }, x);

  // S01 ended dimmed at the door: come up into the room under the stairs, slow drift
  tl.fromTo("#stage", { filter: "brightness(0.55)" }, { filter: "brightness(1)", duration: 0.6, ease: "power1.out" }, 0);
  tl.fromTo("#inCam", { scale: 1.08, svgOrigin: "960 600" }, { scale: 1.0, duration: 5.4, ease: "sine.out" }, 0);
  tl.set("#world", { visibility: "hidden" }, 0);
  // 1.98 "this is not the inverter battery you keep at home": its LEDs blink (the beep), then the strike
  tl.to(".invLed", { opacity: 1, duration: 0.08, repeat: 3, yoyo: true }, 2.1);
  tl.to("#sk1", { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out" }, 3.0)
    .to("#sk2", { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out" }, 3.3);
  K.label(tl, 3.4, 5.0, "NOT THIS", 120, 880).classList.add("red");
  K.tag(tl, 0, 5.3, "ILLUSTRATION");
  // 4.9 the whole corner slides aside; the daylight lane is behind it
  tl.set("#world", { visibility: "visible" }, 4.85);
  tl.to("#inside", { x: -1920, duration: 0.6, ease: "power3.in" }, 4.9).set("#inside", { visibility: "hidden" }, 5.55);

  // ---- 5.56 "It's the box your solar panels connect to": follow the amber cable from the panels down to the box ----
  K.gridLive(tl, 0);
  tl.set("#hud", { opacity: 0 }, 0).set("#hud", { opacity: 1 }, 5.6);   // no empty HUD chip in the room
  K.hudShow(tl, 5.6, "grid");
  K.cam(tl, 0, 720, 300, 2.2, 960, 420);
  const pv = document.getElementById("pvCable");
  const len = pv.getTotalLength();
  const run = el("path", { id: "pvRun", d: pv.getAttribute("d"), fill: "none", stroke: "#FFE08A", "stroke-width": 10, "stroke-linecap": "round",
    "stroke-dasharray": `90 ${len + 200}`, "stroke-dashoffset": 90, opacity: 0 }, document.getElementById("world"));
  tl.set(run, { opacity: 1 }, 5.6).to(run, { attr: { "stroke-dashoffset": -len }, duration: 1.9, ease: "power1.inOut" }, 5.6).set(run, { opacity: 0 }, 7.55);
  K.look(tl, 5.7, 1.9, 900, 640, 2.4, "power2.inOut");
  // 8.07 "Installers call it an on-grid inverter"
  K.label(tl, 8.1, 10.25, "ON-GRID INVERTER", 1110, 250);
  tl.to("#world", { scale: "+=0.08", x: "-=74", y: "-=51", duration: 4.8, ease: "sine.inOut" }, 7.9);  // slow push on the box (centre 924,654)
  // 11.32 "We'll just call it the solar box": the sun badge pops — the box we follow all film
  K.label(tl, 11.35, D, "SOLAR BOX", 1110, 250).classList.add("green");
  tl.fromTo("#badge", { scale: 1 }, { scale: 1.45, duration: 0.22, ease: "back.out(3)", yoyo: true, repeat: 1, immediateRender: false }, 11.35);
  K.hudShow(tl, 11.6, "box");
};
