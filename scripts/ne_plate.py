#!/usr/bin/env python3
"""A satellite-style ground plate for SeaMap from Natural Earth (public domain), for films whose map reaches south of
the equator (the Blue Marble plate stops there, and NASA's image server refuses the cloud).

  python3 scripts/ne_plate.py NE1_HR_LC_SR_W_DR.tif OUT_DIR [--box -1050 -900 1150 1500] [--km-per-px 1.25]

Natural Earth I with shaded relief, land cover, water and drainages (naciscdn.org/naturalearth/10m/raster/
NE1_HR_LC_SR_W_DR.zip, 21600 x 10800, plate carree, -180..180, 90..-90). Reprojected with numpy into the map projection
of lib/remotion/map/indiaGeo.ts (Lambert azimuthal equal-area, lat0 22, lon0 80, R 6371 km; 1 map unit = 3 km, y down).
Writes OUT_DIR/bm_plate.jpg and bm_plate.json ({mapBounds, px, credit}), the files SeaMap reads.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
R = 6371000.0
LAT0, LON0 = np.radians(22.0), np.radians(80.0)


def inverse_laea(x, y):
    """metres (x east, y north) -> lon, lat in degrees"""
    rho = np.hypot(x, y)
    c = 2 * np.arcsin(np.clip(rho / (2 * R), -1, 1))
    with np.errstate(invalid="ignore", divide="ignore"):
        lat = np.arcsin(np.cos(c) * np.sin(LAT0) + np.where(rho > 0, y * np.sin(c) * np.cos(LAT0) / rho, 0))
        lon = LON0 + np.arctan2(x * np.sin(c), rho * np.cos(LAT0) * np.cos(c) - y * np.sin(LAT0) * np.sin(c))
    return np.degrees(lon), np.degrees(lat)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--box", type=float, nargs=4, default=[-1050, -900, 1150, 1500])
    ap.add_argument("--km-per-px", type=float, default=1.25)
    a = ap.parse_args()
    x0, y0, x1, y1 = a.box
    W = round((x1 - x0) * 3 / a.km_per_px)
    H = round((y1 - y0) * 3 / a.km_per_px)
    src = np.asarray(Image.open(a.src).convert("RGB"))
    sh, sw = src.shape[:2]
    out = np.zeros((H, W, 3), np.uint8)
    xs = (x0 + (np.arange(W) + 0.5) * (x1 - x0) / W) * 3000.0
    for r0 in range(0, H, 512):  # rows in bands to keep memory small
        r1 = min(H, r0 + 512)
        ys = -(y0 + (np.arange(r0, r1) + 0.5) * (y1 - y0) / H) * 3000.0  # map y is down; northing is up
        X, Y = np.meshgrid(xs, ys)
        lon, lat = inverse_laea(X, Y)
        px = ((lon + 180.0) / 360.0 * sw).astype(np.int64) % sw
        py = np.clip(((90.0 - lat) / 180.0 * sh).astype(np.int64), 0, sh - 1)
        out[r0:r1] = src[py, px]
    Path(a.out).mkdir(parents=True, exist_ok=True)
    Image.fromarray(out).save(Path(a.out) / "bm_plate.jpg", quality=90)
    (Path(a.out) / "bm_plate.json").write_text(json.dumps({"mapBounds": [x0, y0, x1, y1], "px": [W, H],
                                                           "credit": "Natural Earth (public domain)"}))
    print(W, H)


if __name__ == "__main__":
    main()
