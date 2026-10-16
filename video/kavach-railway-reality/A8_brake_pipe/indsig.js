/* Indian colour-light signal, drawn after Commons photos (design-reference.md): black backplate, four hooded lamps
   top to bottom YELLOW, GREEN, YELLOW, RED (double yellow = lamps 1 and 3 lit; red = bottom), white post with ladder,
   number plate under the head, and for automatic signals a white disc with a black "A".
   indianSignal(x, y, { id, plate, auto, scale }) returns SVG markup with the foot of the post at (x, y).
   Lit lamps are separate circles: #<id>-y1, #<id>-g, #<id>-y2, #<id>-r (opacity 0 = dark). */
window.indianSignal = function (x, y, o = {}) {
  const id = o.id || "sig", k = o.scale || 1, post = 150 * k, hw = 26 * k, hh = 150 * k, top = y - post - hh, r = 11 * k;
  const ly = (i) => top + (22 + i * 35) * k, col = ["#FACC15", "#4ADE80", "#FACC15", "#F87171"], dim = ["#3A3010", "#10331D", "#3A3010", "#3A1414"];
  const ids = ["y1", "g", "y2", "r"];
  let s = `<g id="${id}">
    <line x1="${x}" y1="${y}" x2="${x + 0.3}" y2="${top + hh}" stroke="#D9DEE4" stroke-width="${7 * k}"/>
    ${Array.from({ length: 6 }, (_, i) => `<line x1="${x + 9 * k}" y1="${y - 14 * k - i * 22 * k}" x2="${x + 19 * k}" y2="${y - 14 * k - i * 22 * k + 0.3}" stroke="#9AA3AE" stroke-width="${2 * k}"/>`).join("")}
    <line x1="${x + 9 * k}" y1="${y}" x2="${x + 9.3 * k}" y2="${top + hh}" stroke="#9AA3AE" stroke-width="${1.6 * k}"/><line x1="${x + 19 * k}" y1="${y}" x2="${x + 19.3 * k}" y2="${top + hh}" stroke="#9AA3AE" stroke-width="${1.6 * k}"/>
    <rect x="${x - hw}" y="${top}" width="${2 * hw}" height="${hh}" rx="${7 * k}" fill="#111316" stroke="#2C3036" stroke-width="${2 * k}"/>`;
  for (let i = 0; i < 4; i++) s += `<circle cx="${x}" cy="${ly(i)}" r="${r}" fill="${dim[i]}"/>
    <circle id="${id}-${ids[i]}" class="lit" cx="${x}" cy="${ly(i)}" r="${r}" fill="${col[i]}" opacity="0" filter="url(#glow)"/>
    <path d="M ${x - r * 1.45} ${ly(i) - r * 0.2} A ${r * 1.45} ${r * 1.45} 0 0 1 ${x + r * 1.45} ${ly(i) - r * 0.2} L ${x + r * 1.6} ${ly(i) - r * 1.6} L ${x - r * 1.6} ${ly(i) - r * 1.6} Z" fill="#050607"/>`;
  s += `<rect x="${x - 17 * k}" y="${top + hh + 8 * k}" width="${34 * k}" height="${18 * k}" rx="${2 * k}" fill="#F3F4F6"/>
    <text x="${x}" y="${top + hh + 22 * k}" text-anchor="middle" style="font: 800 ${13 * k}px Inter, Arial, sans-serif; fill: #111827">${o.plate || "S1"}</text>`;
  if (o.auto) s += `<circle cx="${x}" cy="${top + hh + 44 * k}" r="${13 * k}" fill="#F8FAFC" stroke="#111827" stroke-width="${1.5 * k}"/>
    <text x="${x}" y="${top + hh + 50 * k}" text-anchor="middle" style="font: 800 ${16 * k}px Inter, Arial, sans-serif; fill: #111827">A</text>`;
  return s + "</g>";
};
