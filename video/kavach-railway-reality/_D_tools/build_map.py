#!/usr/bin/env python3
"""Build the India rail map data for the Session D map scenes (D4, D5, D6).

Inputs (downloaded to a scratch folder, never committed):
  Natural Earth 1:10m, public domain (github.com/nvkelso/natural-earth-vector/geojson):
    ne_10m_admin_0_countries_ind.geojson        countries as India officially shows them (India point of view:
                                                full Jammu & Kashmir and Ladakh, Arunachal Pradesh)
    ne_10m_admin_1_states_provinces_lines.geojson  state lines (only India's are drawn, faintly)
  DataMeet Indian Railways, CC0 (github.com/datameet/railways):
    trains.json   every train's stop sequence; consecutive stops under 35 km apart become the network edges
                  (station-to-station hops, about 71,700 km in all against 69,439 route km: a close stand-in for
                  the track layout; corridors are routed over it)
Output: map.js (window.KMAP) with SVG path strings in a 1920x1080 frame, Lambert conformal conic.

  python3 -I build_map.py <ne-dir> <datameet-dir> <out map.js>
"""
import json, math, sys, heapq

NE, DM, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1920, 1080
P1, P2, LAT0, LON0 = map(math.radians, (12.472944, 35.172806, 22.5, 80.5))
N = math.log(math.cos(P1) / math.cos(P2)) / math.log(math.tan(math.pi / 4 + P2 / 2) / math.tan(math.pi / 4 + P1 / 2))
F = math.cos(P1) * math.tan(math.pi / 4 + P1 / 2) ** N / N
R0 = F / math.tan(math.pi / 4 + LAT0 / 2) ** N
SCALE, CX, CY = 1880.0, 880.0, 560.0


def proj(lon, lat):
    lat = max(-30, min(62, lat)); lon = max(25, min(150, lon))
    r = F / math.tan(math.pi / 4 + math.radians(lat) / 2) ** N
    th = N * (math.radians(lon) - LON0)
    return CX + SCALE * r * math.sin(th), CY - SCALE * (R0 - r * math.cos(th))


def dp(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True; st = [(0, len(pts) - 1)]
    while st:
        a, b = st.pop(); (x1, y1), (x2, y2) = pts[a], pts[b]; dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-9
        best, bi = -1, -1
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / L
            if d > best: best, bi = d, i
        if best > tol: keep[bi] = True; st += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


def ring_d(ring, tol=0.5, keep_small=False):
    pp = [proj(x, y) for x, y in ring]
    k = max(range(len(pp)), key=lambda i: (pp[i][0] - pp[0][0]) ** 2 + (pp[i][1] - pp[0][1]) ** 2)
    pp = dp(pp[:k + 1], tol) + dp(pp[k:], tol)[1:]
    if len(pp) < 4 and not keep_small: return None
    if len(pp) < 3: pp = [(x + dx, y + dy) for x, y in pp[:1] for dx, dy in ((-1.2, 0), (0, -1.2), (1.2, 0), (0, 1.2))]
    bx = [p[0] for p in pp]; by = [p[1] for p in pp]
    if max(bx) < -300 or min(bx) > W + 300 or max(by) < -300 or min(by) > H + 300: return None
    if not keep_small and (max(bx) - min(bx)) * (max(by) - min(by)) < 6: return None
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pp) + "Z"


def line_d(pts, tol=0.5):
    pp = dp([proj(x, y) for x, y in pts], tol)
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pp) if len(pp) > 1 else None


# ---- countries (India point of view) ----
cs = json.load(open(f"{NE}/ne_10m_admin_0_countries_ind.geojson"))["features"]
india, neigh = [], []
for f in cs:
    g = f["geometry"]; polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    out = india if f["properties"]["ADM0_A3"] == "IND" else neigh
    for poly in polys:
        for ring in poly[:1]:
            xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
            if max(xs) < 40 or min(xs) > 125 or max(ys) < -12 or min(ys) > 55: continue
            d = ring_d(ring, 0.35 if out is india else 0.6, keep_small=out is india)
            if d: out.append(d)
# ---- India's state lines (faint) ----
sl = json.load(open(f"{NE}/ne_10m_admin_1_states_provinces_lines.geojson"))["features"]
states = []
for f in sl:
    if f["properties"].get("ADM0_A3") != "IND": continue
    g = f["geometry"]; ls = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
    for l in ls:
        d = line_d(l, 0.6)
        if d: states.append(d)

# ---- rail network from DataMeet stop sequences ----
km = lambda a, b: math.hypot((b[0] - a[0]) * math.cos(math.radians(a[1])) * 111.2, (b[1] - a[1]) * 111.2)
E = {}
for f in json.load(open(f"{DM}/trains.json"))["features"]:
    c = f["geometry"]["coordinates"] if f["geometry"] else []
    for a, b in zip(c, c[1:]):
        k = tuple(sorted([tuple(a), tuple(b)]))
        if k[0] != k[1] and km(a, b) < 35: E[k] = km(a, b)
adj = {}
for (a, b), w in E.items(): adj.setdefault(a, []).append((b, w)); adj.setdefault(b, []).append((a, w))
nodes = list(adj)


def nearest(lon, lat):
    return min(nodes, key=lambda n: (n[0] - lon) ** 2 + (n[1] - lat) ** 2)


def route(stops):
    path = []
    for a, b in zip(stops, stops[1:]):
        s, t = nearest(*a), nearest(*b); dist, prev, q = {s: 0}, {}, [(0, s)]
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
    print(k, round(sum(km(a, b) for a, b in zip(p, p[1:]))), "km", file=sys.stderr)
    corr_out[k] = line_d(p, 0.4)

# network edges bucketed by distance from Delhi (the network "grows" outwards bucket by bucket)
dx0, dy0 = proj(*C["delhi"]); NB = 48; buckets = [[] for _ in range(NB)]
far = 0; segs = []
for (a, b) in E:
    (x1, y1), (x2, y2) = proj(*a), proj(*b); r = math.hypot((x1 + x2) / 2 - dx0, (y1 + y2) / 2 - dy0)
    segs.append((r, f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")); far = max(far, r)
for r, s in segs: buckets[min(NB - 1, int(NB * r / (far + 1)))].append(s)
rails = ["".join(b) for b in buckets]
print(len(E), "edges,", round(sum(E.values())), "km", file=sys.stderr)

pts = {k: [round(v, 1) for v in proj(*ll)] for k, ll in C.items()}
grat = []
for lon in range(60, 105, 5): grat.append(line_d([(lon, la / 2) for la in range(0, 85)], 0.3))
for lat in range(5, 45, 5): grat.append(line_d([(lo / 2, lat) for lo in range(110, 215)], 0.3))
out = {"W": W, "H": H, "india": india, "neigh": neigh, "states": states, "rails": rails, "corr": corr_out, "pts": pts, "grat": grat}
open(OUT, "w").write("// Generated by video/kavach-railway-reality/_D_tools/build_map.py. Boundaries: Natural Earth 1:10m, India point of\n"
                     "// view (public domain). Rail network: DataMeet Indian Railways stop sequences (CC0). Lambert conformal conic, 1920x1080.\n"
                     "window.KMAP = " + json.dumps(out, separators=(",", ":")) + ";\n")
print("wrote", OUT, round(len(open(OUT).read()) / 1024), "KB", file=sys.stderr)
