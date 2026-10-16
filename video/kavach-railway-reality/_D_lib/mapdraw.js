/* India rail map for D4-D6. Boundaries: Natural Earth 1:10m, India point of view (India as officially shown: full
   Jammu & Kashmir and Ladakh, Arunachal Pradesh); neighbours dimmed. Rail network: DataMeet Indian Railways
   station-to-station hops (CC0), in 48 buckets ordered by distance from Delhi so the network can grow outwards.
   Corridors are routed over that network between station areas. */
window.buildMap = function (svg) {
  const M = window.KMAP, NS = "http://www.w3.org/2000/svg";
  const g = (id, parent = svg) => { const e = document.createElementNS(NS, "g"); if (id) e.setAttribute("id", id); parent.appendChild(e); return e; };
  const path = (d, attrs, parent) => { const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); for (const k in attrs) p.setAttribute(k, attrs[k]); parent.appendChild(p); return p; };
  if (!svg.querySelector("#mapglow")) svg.insertAdjacentHTML("afterbegin", `<defs><filter id="mapglow" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2800" height="1900">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="indfill" x1="0" x2="0.3" y1="0" y2="1"><stop offset="0" stop-color="#1D3157"/><stop offset="1" stop-color="#15233F"/></linearGradient></defs>`);
  const world = g("mworld");
  const grat = g("grat", world); M.grat.forEach((d) => path(d, { fill: "none", stroke: "rgba(148,163,184,0.07)", "stroke-width": 1 }, grat));
  const land = g("land", world);
  M.neigh.forEach((d) => path(d, { fill: "#111C30", stroke: "rgba(148,163,184,0.22)", "stroke-width": 1, "stroke-linejoin": "round" }, land));
  const ind = g("india", land);
  M.india.forEach((d) => path(d, { fill: "url(#indfill)", stroke: "none" }, ind));
  const st = g("states", ind); M.states.forEach((d) => path(d, { fill: "none", stroke: "rgba(148,163,184,0.16)", "stroke-width": 1, "stroke-dasharray": "4 4" }, st));
  const edge = g("indedge", land);
  M.india.forEach((d) => path(d, { fill: "none", stroke: "rgba(125,211,252,0.75)", "stroke-width": 2, "stroke-linejoin": "round", filter: "url(#mapglow)" }, edge));
  const rails = g("rails", world);
  const rl = M.rails.map((d) => path(d, { fill: "none", stroke: "rgba(226,232,240,0.62)", "stroke-width": 1.4, "stroke-linecap": "round" }, rails));
  const corr = g("corr", world), C = {};
  for (const k in M.corr) {
    const glow = path(M.corr[k], { fill: "none", stroke: "#38BDF8", "stroke-width": 12, "stroke-linecap": "round", "stroke-linejoin": "round", opacity: 0.25 }, corr);
    const core = path(M.corr[k], { fill: "none", stroke: "#7DD3FC", "stroke-width": 4.5, "stroke-linecap": "round", "stroke-linejoin": "round" }, corr);
    if (k.startsWith("w_")) { glow.setAttribute("opacity", 0); core.setAttribute("opacity", 0); }   // working sections: scenes turn them on
    C[k] = { glow, core };
  }
  const dots = g("dots", world), P = {};
  for (const k in M.pts) { const [x, y] = M.pts[k]; const c = document.createElementNS(NS, "circle"); c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", 5); c.setAttribute("fill", "#F8FAFC"); c.setAttribute("opacity", 0); dots.appendChild(c); P[k] = c; }
  const prep = (p) => { const L = p.getTotalLength(); p.setAttribute("stroke-dasharray", L); p.setAttribute("stroke-dashoffset", L); return L; };
  return { M, rl, C, P, prep, world };
};
