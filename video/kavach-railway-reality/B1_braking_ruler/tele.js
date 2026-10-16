/* Telemetry world (B scenes): a side-on train over a distance ruler, and a speed-vs-distance chart drawn like a
   precision instrument. Constant-deceleration curves (v = v0 * sqrt(1 - d/D)) are the honest shape for a stop at a
   steady braking rate; the assembler tags curves ILLUSTRATIVE where the spec says so. Builds into <svg id="tele">. */
window.KT = (function () {
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  // chart frame: x0..x1 px <-> 0..maxD m ; y0 (v=0) .. y1 (v=maxV) px
  function chart(svg, o) {
    const g = el("g", { id: o.id || "chart" }, svg);
    const { x0, x1, y0, y1, maxD, maxV } = o;
    const X = (d) => x0 + (x1 - x0) * d / maxD, Yv = (v) => y0 - (y0 - y1) * v / maxV;
    el("rect", { x: x0 - 90, y: y1 - 70, width: x1 - x0 + 150, height: y0 - y1 + 140, rx: 18, fill: "rgba(11,18,32,0.88)", stroke: "#334155", "stroke-width": 2 }, g);
    for (let i = 0; i <= o.vTicks.length - 1; i++) {
      const v = o.vTicks[i];
      el("line", { x1: x0, y1: Yv(v) + 0.3, x2: x1, y2: Yv(v), stroke: "rgba(148,163,184,0.16)", "stroke-width": 1.5 }, g);
      const t = el("text", { x: x0 - 16, y: Yv(v) + 7, "text-anchor": "end", class: "ax" }, g); t.textContent = v;
    }
    el("line", { x1: x0, y1: y0, x2: x1, y2: y0 + 0.3, stroke: "#64748B", "stroke-width": 2.5 }, g);
    const ruler = el("g", { class: "ruler" }, g);
    for (let d = 0; d <= maxD; d += o.dMinor) {
      const major = d % o.dMajor === 0;
      el("line", { x1: X(d), y1: y0, x2: X(d) + 0.2, y2: y0 + (major ? 18 : 9), stroke: major ? "#94A3B8" : "#475569", "stroke-width": major ? 2.5 : 1.5 }, ruler);
      if (major && o.dLabels) { const t = el("text", { x: X(d), y: y0 + 46, "text-anchor": "middle", class: "ax" }, ruler); t.textContent = d === 0 ? "0" : `${d} m`; }
    }
    const yl = el("text", { x: x0 - 16, y: y1 - 26, "text-anchor": "end", class: "ax" }, g); yl.textContent = o.vLabel || "KM/H";
    return { g, X, Yv };
  }
  // constant-deceleration stop curve from speed v0 over distance D, as an SVG path in chart space
  function stopPath(C, v0, D, n = 60) {
    let s = "";
    for (let i = 0; i <= n; i++) { const d = D * (1 - Math.pow(1 - i / n, 2)), v = v0 * Math.sqrt(Math.max(0, 1 - d / D)); s += `${i ? "L" : "M"} ${C.X(d).toFixed(1)} ${C.Yv(v).toFixed(1)} `; }
    return s;
  }
  // side-on train: aerodynamic trainset nose (Vande Bharat-like, generic, no livery text) + cars to the left
  function trainset(svg, id, y, cars = 5, carLen = 150) {
    const g = el("g", { id }, svg);
    for (let i = 0; i < cars; i++) {
      const x = -carLen * (i + 1) - 8 * i - 150;
      el("rect", { x, y: y - 46, width: carLen, height: 46, rx: 8, fill: "#E2E8F0", stroke: "#94A3B8", "stroke-width": 2 }, g);
      el("rect", { x: x + 14, y: y - 36, width: carLen - 28, height: 12, rx: 4, fill: "#1E3A5F" }, g);
      el("rect", { x, y: y - 10, width: carLen, height: 6, fill: "#0284C7" }, g);
    }
    el("path", { d: `M -150 ${y - 46} L -40 ${y - 46} C 10 ${y - 46}, 34 ${y - 18}, 40 ${y} L -150 ${y} Z`, fill: "#F1F5F9", stroke: "#94A3B8", "stroke-width": 2 }, g);
    el("path", { d: `M -60 ${y - 40} C -20 ${y - 40}, 8 ${y - 30}, 18 ${y - 18} L -60 ${y - 18} Z`, fill: "#0F2A4A" }, g);
    el("rect", { x: -150, y: y - 10, width: 186, height: 6, fill: "#0284C7" }, g);
    el("circle", { cx: 30, cy: y - 8, r: 5, fill: "#FDE68A" }, g);
    return g;
  }
  function rail(svg, y, x0 = -200, x1 = 2200) {
    const g = el("g", {}, svg);
    el("line", { x1: x0, y1: y + 4, x2: x1, y2: y + 4.3, stroke: "#94A3B8", "stroke-width": 4 }, g);
    for (let x = x0; x < x1; x += 34) el("rect", { x, y: y + 8, width: 18, height: 6, fill: "#334155" }, g);
    return g;
  }
  return { el, chart, stopPath, trainset, rail };
})();
