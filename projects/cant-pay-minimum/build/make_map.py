#!/usr/bin/env python3
"""Andhra Pradesh + Telangana outlines for the agency-map page (C037-C039), from Natural Earth admin-1 (public domain,
naturalearthdata.com), projected to page px and simplified. State borders only (no national border drawn).
  python3 build/make_map.py /path/to/ne_10m_admin_1_states_provinces.geojson   -> build/map_aptg.json"""
import json, math, sys
from pathlib import Path

BOX = (1010, 110, 1820, 1000)   # x0, y0, x1, y1 on the 1920×1080 page
CITIES = {"Hyderabad": (17.385, 78.4867), "Warangal": (17.9689, 79.5941), "Karimnagar": (18.4386, 79.1288),
          "Vizag": (17.6868, 83.2185), "Vijayawada": (16.5062, 80.648), "Tirupati": (13.6288, 79.4192),
          "village": (14.95, 77.85)}    # an illustrative village far from all six (Anantapur district countryside)


def dp(pts, eps):
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]; dx, dy = x1 - x0, y1 - y0; n = math.hypot(dx, dy) or 1e-9
    d = [abs(dy * (x - x0) - dx * (y - y0)) / n for x, y in pts[1:-1]]
    i = max(range(len(d)), key=d.__getitem__)
    if d[i] > eps:
        return dp(pts[:i + 2], eps)[:-1] + dp(pts[i + 1:], eps)
    return [pts[0], pts[-1]]


feats = {f["properties"]["name"]: f for f in json.load(open(sys.argv[1]))["features"]
         if f["properties"].get("adm0_a3") == "IND" and f["properties"]["name"] in ("Andhra Pradesh", "Telangana")}
rings = {}
for name, f in feats.items():
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rings[name] = max((p[0] for p in polys), key=len)   # mainland outer ring
lon = [x for r in rings.values() for x, _ in r]; lat = [y for r in rings.values() for _, y in r]
k = math.cos(math.radians(sum(lat) / len(lat)))
w, h = (max(lon) - min(lon)) * k, max(lat) - min(lat)
s = min((BOX[2] - BOX[0]) / w, (BOX[3] - BOX[1]) / h)
ox = BOX[0] + ((BOX[2] - BOX[0]) - w * s) / 2; oy = BOX[1] + ((BOX[3] - BOX[1]) - h * s) / 2
proj = lambda la, lo: (round(ox + (lo - min(lon)) * k * s, 1), round(oy + (max(lat) - la) * s, 1))
out = {"source": "Natural Earth 10m admin-1 (public domain)", "states": {}, "cities": {n: proj(*ll) for n, ll in CITIES.items()},
       "km_per_px": round(111.2 / s, 3)}
for name, r in rings.items():
    ring = [proj(la, lo) for lo, la in r]
    far = max(range(len(ring)), key=lambda i: math.hypot(ring[i][0] - ring[0][0], ring[i][1] - ring[0][1]))
    pts = dp(ring[:far + 1], 1.6)[:-1] + dp(ring[far:], 1.6)   # closed ring: simplify the two halves
    out["states"][name] = "M " + " L ".join(f"{x} {y}" for x, y in pts) + " Z"
    print(name, len(r), "->", len(pts), "points")
(Path(__file__).parent / "map_aptg.json").write_text(json.dumps(out, indent=0))
print(out["cities"], out["km_per_px"])
