/* Land-only India rail map for D4-D6 (Natural Earth 1:10m land + railroads, public domain; no political borders are
   drawn). Rail lines are ordered by distance from Delhi so the network can grow outwards; corridor paths follow the
   Natural Earth lines between station areas (generic routing, labelled ILLUSTRATIVE by the assembler). */
window.buildMap = function (svg) {
  const M = window.KMAP, NS = "http://www.w3.org/2000/svg";
  const g = (id, parent = svg) => { const e = document.createElementNS(NS, "g"); if (id) e.setAttribute("id", id); parent.appendChild(e); return e; };
  const path = (d, attrs, parent) => { const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); for (const k in attrs) p.setAttribute(k, attrs[k]); parent.appendChild(p); return p; };
  const world = g("mworld");
  const grat = g("grat", world); M.grat.forEach((d) => path(d, { fill: "none", stroke: "rgba(148,163,184,0.08)", "stroke-width": 1 }, grat));
  const land = g("land", world); M.land.forEach((d) => path(d, { fill: "#18253F", stroke: "rgba(56,189,248,0.34)", "stroke-width": 1.4, "stroke-linejoin": "round" }, land));
  const rails = g("rails", world);
  const rl = M.rails.map((d) => path(d, { fill: "none", stroke: "rgba(203,213,225,0.62)", "stroke-width": 2, "stroke-linecap": "round" }, rails));
  const corr = g("corr", world), C = {};
  for (const k in M.corr) {
    const glow = path(M.corr[k], { fill: "none", stroke: "#38BDF8", "stroke-width": 12, "stroke-linecap": "round", opacity: 0.25 }, corr);
    const core = path(M.corr[k], { fill: "none", stroke: "#7DD3FC", "stroke-width": 4.5, "stroke-linecap": "round" }, corr);
    C[k] = { glow, core };
  }
  const dots = g("dots", world), P = {};
  for (const k in M.pts) { const [x, y] = M.pts[k]; const c = document.createElementNS(NS, "circle"); c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", 5); c.setAttribute("fill", "#F8FAFC"); c.setAttribute("opacity", 0); dots.appendChild(c); P[k] = c; }
  // prepare a path for a stroke-draw tween
  const prep = (p) => { const L = p.getTotalLength(); p.setAttribute("stroke-dasharray", L); p.setAttribute("stroke-dashoffset", L); return L; };
  return { M, rl, C, P, prep, world };
};
