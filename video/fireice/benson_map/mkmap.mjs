import { geoNaturalEarth1, geoPath, geoInterpolate } from "d3-geo";
import { feature, mesh } from "topojson-client";
import { readFileSync, writeFileSync } from "node:fs";
const topo = JSON.parse(readFileSync("node_modules/world-atlas/countries-110m.json", "utf8"));
const countries = feature(topo, topo.objects.countries);
const W = 1920, H = 1080;
// frame: North Atlantic to the Himalaya
const proj = geoNaturalEarth1().fitExtent([[60, 60], [W - 60, H - 60]], { type: "MultiPoint", coordinates: [[-80, 50], [100, 20], [-60, 25], [95, 45]] });
const path = geoPath(proj).digits(1);
const ltopo = JSON.parse(readFileSync("node_modules/world-atlas/land-110m.json", "utf8"));
const land = path(feature(ltopo, ltopo.objects.land));  // merged landmasses: no political borders
const P = {
  boston: [-71.06, 42.36], dharamsala: [76.32, 32.22], leh: [77.58, 34.15], gangtok: [88.61, 27.33],
};
const pts = Object.fromEntries(Object.entries(P).map(([k, v]) => [k, proj(v).map(x => +x.toFixed(1))]));
const arc = (a, b) => { const ip = geoInterpolate(P[a], P[b]); return "M" + Array.from({ length: 81 }, (_, i) => proj(ip(i / 80)).map(x => x.toFixed(1)).join(" ")).join(" L"); };
const out = { W, H, land, pts, arcDharamsala: arc("boston", "dharamsala"), arcLeh: arc("boston", "leh"), arcGangtok: arc("boston", "gangtok") };
writeFileSync("/home/user/Creator/video/fireice/benson_map/map.js", "// Generated from world-atlas 2.0.2 (Natural Earth 1:110m land, public domain; package ISC; no political borders) by a d3-geo NaturalEarth1 projection.\nwindow.MAP = " + JSON.stringify(out) + ";\n");
console.log(pts, (JSON.stringify(out).length / 1024).toFixed(0) + " KB");
