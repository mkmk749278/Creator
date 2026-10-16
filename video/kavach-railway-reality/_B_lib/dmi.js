/* Kavach cab screen (DMI, "KAVACH LP-OCIP"), drawn after the real unit (projects/kavach-railway-reality/design-reference.md:
   TCAS_Retrofitted_DMI_P7.jpg, TCAS_DMI_Screenshot.jpg). Generic numbers; no maker names. Builds into an <svg> of
   viewBox 0 0 760 700 and returns set(state) to redraw it from a pure state object:
   { v (km/h), vp (permitted km/h), td (target distance m), ma (movement authority m), asp ("R"|"Y"|"YY"|"G"),
     sd (signal distance m), msg, mode, loc (km), warn (0..1), brake (0..1) } */
window.KDMI = function (svg) {
  const NS = "http://www.w3.org/2000/svg";
  const el = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); (p || svg).appendChild(e); return e; };
  const tx = (x, y, s, cls, p, anchor) => { const e = el("text", { x, y, class: cls, "text-anchor": anchor || "start" }, p); e.textContent = s; return e; };
  // bezel and buttons
  el("rect", { x: 0, y: 0, width: 760, height: 560, rx: 18, fill: "#121315", stroke: "#2A2C30", "stroke-width": 4 });
  el("rect", { x: 8, y: 8, width: 744, height: 544, rx: 14, fill: "none", stroke: "#1C1E21", "stroke-width": 3 });
  tx(380, 34, "KAVACH LP-OCIP", "dmiT", null, "middle");
  const sideL = ["⏻", "◐", "⚙", "☼", "F", "M"], sideR = ["C", "◄", "►", "▲", "▼", "E"];
  sideL.forEach((s, i) => { el("rect", { x: 22, y: 70 + i * 66, width: 44, height: 44, rx: 6, fill: "#18191B", stroke: "#4A4D52", "stroke-width": 2 }); tx(44, 99 + i * 66, s, "dmiK", null, "middle"); });
  sideR.forEach((s, i) => { el("rect", { x: 694, y: 70 + i * 66, width: 44, height: 44, rx: 6, fill: "#18191B", stroke: "#4A4D52", "stroke-width": 2 }); tx(716, 99 + i * 66, s, "dmiK", null, "middle"); });
  for (let i = 0; i < 10; i++) { el("rect", { x: 128 + i * 52, y: 506, width: 36, height: 34, rx: 4, fill: "#18191B", stroke: "#4A4D52", "stroke-width": 2 }); tx(146 + i * 52, 530, String((i + 1) % 10), "dmiK", null, "middle"); }
  // screen
  const scr = el("g", { transform: "translate(90 54)" });
  el("rect", { x: 0, y: 0, width: 580, height: 438, fill: "#050607", stroke: "#3A3D42", "stroke-width": 2 }, scr);
  tx(14, 22, "30356", "dmiS", scr); const clock = tx(566, 22, "31-Jan-2026  02:14:07", "dmiS", scr, "end");
  // speedometer 0..200 (left), arc spans 240 degrees
  const cx = 168, cy = 182, R = 120, a0 = -120, span = 240, ang = (v) => (a0 + span * v / 200) * Math.PI / 180;
  const P = (v, r) => [cx + r * Math.sin(ang(v)), cy - r * Math.cos(ang(v))];
  const arc = (v1, v2, r) => { const [x1, y1] = P(v1, r), [x2, y2] = P(v2, r); return `M ${x1} ${y1} A ${r} ${r} 0 ${(v2 - v1) / 200 * span > 180 ? 1 : 0} 1 ${x2} ${y2}`; };
  for (let v = 0; v <= 200; v += 10) { const [x1, y1] = P(v, R), [x2, y2] = P(v, v % 20 ? R - 9 : R - 16); el("line", { x1, y1, x2, y2, stroke: "#E5E7EB", "stroke-width": v % 20 ? 1.5 : 2.5 }, scr);
    if (v % 20 === 0) { const [lx, ly] = P(v, R - 38); tx(lx, ly + 6, String(v), "dmiN", scr, "middle"); } }
  const perm = el("path", { fill: "none", stroke: "#22C55E", "stroke-width": 10, "stroke-linecap": "butt" }, scr);
  const needle = el("line", { x1: cx, y1: cy, x2: cx, y2: cy - 100, stroke: "#F8FAFC", "stroke-width": 5, "stroke-linecap": "round" }, scr);
  const hub = el("circle", { cx, cy, r: 26, fill: "#F8FAFC" }, scr); const vtxt = tx(cx, cy + 9, "0", "dmiV", scr, "middle");
  const loc = tx(cx, 326, "LOC : 1446.36 Km", "dmiS", scr, "middle");
  // target distance bar (yellow, left)
  el("rect", { x: 18, y: 60, width: 16, height: 220, fill: "#111" , stroke: "#333", "stroke-width": 1 }, scr);
  const tbar = el("rect", { x: 18, y: 60, width: 16, height: 0, fill: "#EAB308" }, scr);
  const ttxt = tx(26, 300, "", "dmiS", scr, "middle");
  // movement authority (blue bar) and signal icon
  tx(326, 44, "Move Authority", "dmiS", scr);
  for (const [lab, f] of [["3000", 0], ["1000", 0.33], ["500", 0.55], ["250", 0.75], ["0", 1]]) { el("line", { x1: 330, y1: 60 + 220 * f, x2: 344, y2: 60 + 220 * f + 0.3, stroke: "#9CA3AF", "stroke-width": 1.5 }, scr); tx(326, 64 + 220 * f, lab, "dmiS", scr, "end"); }
  el("rect", { x: 350, y: 60, width: 18, height: 220, fill: "#111", stroke: "#333", "stroke-width": 1 }, scr);
  const mabar = el("rect", { x: 350, y: 60, width: 18, height: 0, fill: "#38BDF8" }, scr);
  const matxt = tx(359, 300, "", "dmiS", scr, "middle");
  el("rect", { x: 440, y: 56, width: 70, height: 206, rx: 34, fill: "#0A0A0A", stroke: "#E5E7EB", "stroke-width": 3 }, scr);
  const lamps = [0, 1, 2, 3].map((i) => el("circle", { cx: 475, cy: 88 + i * 48, r: 19, fill: "#0A0A0A", stroke: "#E5E7EB", "stroke-width": 3 }, scr));
  el("circle", { cx: 475, cy: 286, r: 13, fill: "#0A0A0A", stroke: "#E5E7EB", "stroke-width": 2.5 }, scr); tx(475, 291, "A", "dmiS", scr, "middle");
  const sdt = tx(475, 322, "", "dmiS", scr, "middle");
  // status and message lines
  el("rect", { x: 0, y: 338, width: 580, height: 28, fill: "#0B0C0E", stroke: "#3A3D42", "stroke-width": 1 }, scr);
  const mode = tx(14, 358, "DC 0.47   TL 25 m   Full Supervision Mode", "dmiS", scr);
  el("rect", { x: 0, y: 366, width: 440, height: 40, fill: "#0B0C0E", stroke: "#3A3D42", "stroke-width": 1 }, scr);
  const msgBg = el("rect", { x: 1, y: 367, width: 438, height: 38, fill: "#0B0C0E" }, scr);
  const msg = tx(12, 393, "", "dmiM", scr);
  tx(452, 386, "RF ▂▄▆█", "dmiS", scr);
  const keys = ["P_TRP", "REV", "OVRD", "SHNT", "MBT", "SR", "CONFIG", "", "CNFM", "INFO"];
  keys.forEach((k, i) => { el("rect", { x: 4 + i * 57.6, y: 410, width: 54, height: 24, fill: "#1F2A44", stroke: "#3B4A6B", "stroke-width": 1 }, scr); tx(31 + i * 57.6, 427, k, "dmiF", scr, "middle"); });
  // button panel below the bezel
  el("rect", { x: 40, y: 572, width: 680, height: 124, rx: 10, fill: "#9CA3AF", stroke: "#6B7280", "stroke-width": 3 });
  [["COMMON", "#2B2D31"], ["ACK/CANCEL", "#2563EB"], ["SOS", "#DC2626"]].forEach(([l, c], i) => { const x = 160 + i * 220;
    el("circle", { cx: x, cy: 622, r: 30, fill: c, stroke: "#E5E7EB", "stroke-width": 4 }); tx(x, 682, l, "dmiB", null, "middle"); });
  const ASP = { R: ["#EF4444", 3], Y: ["#FACC15", 2], YY: ["#FACC15", 2], G: ["#22C55E", 1] };   // lamps top to bottom: Y, G, Y, R (Indian 4-aspect)
  function set(s) {
    perm.setAttribute("d", arc(0, Math.max(1, s.vp), R + 6));
    const a = ang(s.v); needle.setAttribute("x2", cx + 100 * Math.sin(a)); needle.setAttribute("y2", cy - 100 * Math.cos(a));
    vtxt.textContent = Math.round(s.v);
    hub.setAttribute("fill", s.v > s.vp + 2 ? "#F59E0B" : "#F8FAFC");
    const tf = Math.max(0, Math.min(1, s.td / 1500)); tbar.setAttribute("height", 220 * tf); tbar.setAttribute("y", 60 + 220 * (1 - tf)); ttxt.textContent = Math.max(0, Math.round(s.td)) + " m";
    const mf = Math.max(0, Math.min(1, Math.log10(1 + s.ma) / Math.log10(3001))); mabar.setAttribute("height", 220 * mf); mabar.setAttribute("y", 60 + 220 * (1 - mf)); matxt.textContent = String(Math.max(0, Math.round(s.ma))).padStart(5, "0") + " m";
    lamps.forEach((l, i) => l.setAttribute("fill", "#0A0A0A"));
    const [c, i] = ASP[s.asp] || ASP.R; lamps[i].setAttribute("fill", c); if (s.asp === "YY") lamps[0].setAttribute("fill", c);
    sdt.textContent = String(Math.max(0, Math.round(s.sd))).padStart(4, "0") + " m";
    if (s.loc != null) loc.textContent = `LOC : ${s.loc.toFixed(2)} Km`;
    msg.textContent = s.msg || "";
    msgBg.setAttribute("fill", s.brake > 0 ? "#7F1D1D" : s.warn > 0 ? "#713F12" : "#0B0C0E");
    if (s.mode) mode.textContent = s.mode;
  }
  return { set };
};
