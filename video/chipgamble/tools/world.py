import json, math, sys
d = json.load(open(sys.argv[1])); out = sys.argv[2]
W = 8000.0
def pt(lon, lat):
    lat = max(-80, min(84, lat))
    x = (lon + 180) / 360 * W
    y = (1 - math.log(math.tan(math.pi/4 + math.radians(lat)/2)) / math.pi) / 2 * W
    return x, y
paths = {}; centers = {}
for f in d["features"]:
    p = f["properties"]; iso = p.get("ADM0_A3")
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    parts = []
    for poly in polys:
        ring = poly[0]; pts = []; last = None
        for c in ring:
            x, y = pt(*c[:2])
            if last is None or abs(x-last[0]) + abs(y-last[1]) > 1.2:
                pts.append((x, y)); last = (x, y)
        if len(pts) < 4: continue
        parts.append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + "Z")
    if parts:
        paths[iso] = "".join(parts)
        centers[iso] = [round(v) for v in pt(p["LABEL_X"], p["LABEL_Y"])]
js = "window.WORLD=" + json.dumps({"W": W, "paths": paths, "centers": centers}, separators=(",", ":")) + ";\n"
open(out, "w").write(js)
print(len(js), len(paths))
