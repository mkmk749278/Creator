#!/usr/bin/env python3
"""Build the land-only India rail map data for the Session D map scenes (D4, D5, D6, D1 backdrop).

Inputs (Natural Earth 1:10m, public domain; downloaded from github.com/nvkelso/natural-earth-vector/geojson):
  ne_10m_land.geojson        merged land (no political borders are drawn)
  ne_10m_railroads.geojson   railway lines
  ne_10m_admin_0_countries   used ONLY to keep the rail lines that lie in India; never drawn
Output: map.js (window.KMAP) with SVG path strings in a 1920x1080 frame, Lambert conformal conic projection.

  python3 -I build_map.py <dir-with-geojson> <out map.js>
"""
import json, math, sys, heapq

SRC, OUT = sys.argv[1], sys.argv[2]
W, H = 1920, 1080
# Lambert conformal conic (India's usual parallels 12.47 N / 35.17 N), centre 80.5 E 22.5 N
P1, P2, LAT0, LON0 = map(math.radians, (12.472944, 35.172806, 22.5, 80.5))
N = math.log(math.cos(P1) / math.cos(P2)) / math.log(math.tan(math.pi / 4 + P2 / 2) / math.tan(math.pi / 4 + P1 / 2))
F = math.cos(P1) * math.tan(math.pi / 4 + P1 / 2) ** N / N
R0 = F / math.tan(math.pi / 4 + LAT0 / 2) ** N
SCALE = 1880.0          # px per unit (India's north-south span fits ~1000 px)
CX, CY = 880.0, 560.0   # projected centre point on screen (map sits left of centre: logo bug top-right)


def proj(lon, lat):
    r = F / math.tan(math.pi / 4 + math.radians(lat) / 2) ** N
    th = N * (math.radians(lon) - LON0)
    return CX + SCALE * r * math.sin(th), CY - SCALE * (R0 - r * math.cos(th))


def dp(pts, tol):
    """Douglas-Peucker simplification of a projected polyline."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-9
        best, bi = -1, -1
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / L
            if d > best: best, bi = d, i
        if best > tol:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


def d_of(pts, close=False):
    s = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return s + ("Z" if close else "")


# ---- land: every ring that touches the view box (with margin) ----
land = json.load(open(f"{SRC}/ne_10m_land.geojson"))
land_d = []
for f in land["features"]:
    g = f["geometry"]; polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        for ring in poly:
            xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
            if max(xs) < 55 or min(xs) > 110 or max(ys) < -2 or min(ys) > 45:
                continue
            pp = [proj(max(50, min(115, x)), max(-5, min(48, y))) for x, y in ring]
            pp = dp(pp, 0.6)
            if len(pp) < 4: continue
            bx = [p[0] for p in pp]; by = [p[1] for p in pp]
            if max(bx) < -400 or min(bx) > W + 400 or max(by) < -400 or min(by) > H + 400: continue
            if (max(bx) - min(bx)) * (max(by) - min(by)) < 9: continue   # specks
            land_d.append(d_of(pp, True))

# ---- rails in India ----
adm = json.load(open(f"{SRC}/adm0.geojson"))
ind = [f for f in adm["features"] if f["properties"].get("ADM0_A3") == "IND"][0]
rings = [p[0] for p in ind["geometry"]["coordinates"]]


def in_india(x, y):
    ins = False
    for ring in rings:
        j = len(ring) - 1
        for i in range(len(ring)):
            xi, yi = ring[i]; xj, yj = ring[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: ins = not ins
            j = i
    return ins


def km(c):
    return sum(math.hypot((c[i + 1][0] - c[i][0]) * math.cos(math.radians(c[i][1])) * 111.2, (c[i + 1][1] - c[i][1]) * 111.2) for i in range(len(c) - 1))


rr = json.load(open(f"{SRC}/ne_10m_railroads.geojson"))
lines = []
for f in rr["features"]:
    g = f["geometry"]; cs = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
    for c in cs:
        xs = [p[0] for p in c]; ys = [p[1] for p in c]
        if max(xs) < 67 or min(xs) > 98 or max(ys) < 6 or min(ys) > 37: continue
        if in_india(*c[len(c) // 2]): lines.append(c)

# routing graph over the rail vertices (snap to ~100 m, join near-touching ends)
key = lambda p: (round(p[0], 3), round(p[1], 3))
adj = {}
def edge(a, b):
    w = km([a, b]); adj.setdefault(key(a), []).append((key(b), w)); adj.setdefault(key(b), []).append((key(a), w))
for c in lines:
    for i in range(len(c) - 1): edge(c[i], c[i + 1])
ends = [c[0] for c in lines] + [c[-1] for c in lines]
nodes = list(adj)
for e in ends:
    for n in nodes:
        if n != key(e) and abs(n[0] - e[0]) < 0.05 and abs(n[1] - e[1]) < 0.05 and km([e, n]) < 4: edge(e, list(n))


def nearest(lon, lat):
    return min(nodes, key=lambda n: (n[0] - lon) ** 2 + (n[1] - lat) ** 2)


def route(stops):
    path = []
    for (a, b) in zip(stops, stops[1:]):
        s, t = nearest(*a), nearest(*b)
        dist, prev, q = {s: 0}, {}, [(0, s)]
        while q:
            d, u = heapq.heappop(q)
            if u == t: break
            if d > dist.get(u, 1e18): continue
            for v, w in adj[u]:
                if d + w < dist.get(v, 1e18): dist[v] = d + w; prev[v] = u; heapq.heappush(q, (d + w, v))
        seg = [t]
        while seg[-1] != s: seg.append(prev[seg[-1]])
        seg.reverse(); path += seg if not path else seg[1:]
    return path


C = {  # lon, lat (station areas)
    "delhi": (77.22, 28.64), "mathura": (77.67, 27.49), "kota": (75.85, 25.18), "ratlam": (75.04, 23.33),
    "vadodara": (73.18, 22.31), "surat": (72.84, 21.20), "mumbai": (72.84, 18.97), "ahmedabad": (72.60, 23.03),
    "kanpur": (80.35, 26.45), "prayagraj": (81.85, 25.44), "ddu": (83.12, 25.28), "gaya": (85.00, 24.79),
    "dhanbad": (86.43, 23.80), "howrah": (88.34, 22.58),
    "secunderabad": (78.50, 17.44), "wadi": (76.99, 17.06), "vikarabad": (77.90, 17.34), "bidar": (77.52, 17.91),
    "nanded": (77.32, 19.15), "kazipet": (79.53, 18.00), "dhone": (77.87, 15.40),
}
corr = {
    "dm": route([C[k] for k in ("delhi", "mathura", "kota", "ratlam", "vadodara", "surat", "mumbai")]),
    "va": route([C["vadodara"], C["ahmedabad"]]),
    "dh": route([C[k] for k in ("delhi", "kanpur", "prayagraj", "ddu", "gaya", "dhanbad", "howrah")]),
    "scr1": route([C["wadi"], C["secunderabad"], C["kazipet"]]),
    "scr2": route([C["vikarabad"], C["bidar"]]),
    "scr3": route([C["secunderabad"], C["nanded"]]),
    "scr4": route([C["secunderabad"], C["dhone"]]),
}
corr_out = {}
for k, p in corr.items():
    print(k, round(km([list(n) for n in p])), "km", file=sys.stderr)
    corr_out[k] = d_of(dp([proj(*n) for n in p], 0.5))

# rail lines, ordered by distance from Delhi so the network can "grow" outwards
dx0, dy0 = proj(*C["delhi"])
rails = []
total = 0
for c in lines:
    pp = dp([proj(*p) for p in c], 0.5)
    if len(pp) < 2: continue
    mx, my = pp[len(pp) // 2]
    rails.append((math.hypot(mx - dx0, my - dy0), d_of(pp), round(km(c))))
    total += km(c)
rails.sort()
print(len(rails), "rail lines,", round(total), "km in the Natural Earth set", file=sys.stderr)

pts = {k: [round(v, 1) for v in proj(*ll)] for k, ll in C.items()}
grat = []   # faint graticule every 5 degrees (telemetry texture)
for lon in range(60, 105, 5): grat.append(d_of([proj(lon, la / 2) for la in range(0, 85)]))
for lat in range(5, 45, 5): grat.append(d_of([proj(lo / 2, lat) for lo in range(110, 215)]))
out = {"W": W, "H": H, "land": land_d, "rails": [r[1] for r in rails], "railR": [round(r[0]) for r in rails],
       "corr": corr_out, "pts": pts, "grat": grat}
open(OUT, "w").write("// Generated by video/kavach-railway-reality/_D_tools/build_map.py from Natural Earth 1:10m land and railroads\n"
                     "// (public domain). Land only: no political borders are drawn. Lambert conformal conic, 1920x1080.\n"
                     "window.KMAP = " + json.dumps(out, separators=(",", ":")) + ";\n")
print("wrote", OUT, round(len(open(OUT).read()) / 1024), "KB", file=sys.stderr)
