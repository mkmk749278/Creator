#!/usr/bin/env python3
"""Real satellite plates for film maps: a cloud-free Sentinel-2 true-colour crop and a matching Copernicus DEM.

Why: flat vector maps read as a template next to archive photos (outside review of film 1, 2026-10-28). A real place
should look like the real ground: river bends, hills, red earth. Both sources allow commercial use with attribution:
- Sentinel-2 L2A (Copernicus, via the Element84 Earth Search STAC on AWS): "Contains modified Copernicus Sentinel data <year>".
- Copernicus DEM GLO-30 (AWS open data): "Copernicus DEM GLO-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space
  GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA".
(EOX's s2cloudless mosaics are CC BY-NC-SA for commercial channels: never use them.)

Output, in OUT/: <name>.jpg (true colour, graded only lightly), <name>_dem.png (16-bit metres), <name>_depth.png
(8-bit, near = white, for DepthPhoto), <name>_hill.png (hillshade), <name>.json (bounds, metres per pixel, scene ids,
credit line). The plate is a local azimuthal-equidistant grid on the centre, so distances are true near the middle.

Usage:
  .venv-geo/bin/python scripts/sat_crop.py --name sakchi --center 86.185,22.81 --width-km 24 --px 3840 \
      --dates 2024-11-01/2025-03-31 --out films/tata-history/assets/media/sat
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np
import rasterio
from pystac_client import Client
from rasterio.crs import CRS
from rasterio.transform import from_bounds
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling

STAC = 'https://earth-search.aws.element84.com/v1'
DEM_URL = 'https://copernicus-dem-30m.s3.amazonaws.com/{n}/{n}.tif'


LAEA = '+proj=laea +lat_0=22 +lon_0=80 +R=6371000 +units=m +no_defs'
KM_PER_UNIT = 3.0


def laea(lon: float, lat: float) -> tuple[float, float]:
    # same formula as project() in IndiaMap.tsx (sphere R = 6371 km), metres
    r = math.pi / 180
    l, p, p0 = (lon - 80) * r, lat * r, 22 * r
    k = math.sqrt(2 / (1 + math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l)))
    return 6371000 * k * math.cos(p) * math.sin(l), 6371000 * k * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l))


def dem_tile(lat: int, lon: int) -> str:
    ns = 'N' if lat >= 0 else 'S'
    ew = 'E' if lon >= 0 else 'W'
    n = f'Copernicus_DSM_COG_10_{ns}{abs(lat):02d}_00_{ew}{abs(lon):03d}_00_DEM'
    return DEM_URL.format(n=n)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--center', required=True, help='lon,lat')
    ap.add_argument('--width-km', type=float, required=True)
    ap.add_argument('--px', type=int, default=3840, help='output width; height is 9/16 of it')
    ap.add_argument('--aspect', type=float, default=16 / 9)
    ap.add_argument('--dates', default='2024-10-15/2025-03-31', help='dry season: clear skies, no monsoon haze')
    ap.add_argument('--max-cloud', type=float, default=5)
    ap.add_argument('--scenes', type=int, default=6, help='best scenes to stack, clearest first')
    ap.add_argument('--out', required=True)
    ap.add_argument('--local', action='store_true', help='local azimuthal grid instead of the film map projection')
    a = ap.parse_args()

    lon0, lat0 = (float(v) for v in a.center.split(','))
    w_m = a.width_km * 1000
    h_m = w_m / a.aspect
    W, H = a.px, round(a.px / a.aspect)
    if a.local:
        crs = CRS.from_proj4(f'+proj=aeqd +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m +no_defs')
        cx, cy = 0.0, 0.0
    else:
        # The film's map projection (lib/remotion/map/indiaGeo.ts MAP_PROJ, scripts/india_map.py): a plate lands exactly
        # under the official boundary, the pins and the routes.
        crs = CRS.from_proj4(LAEA)
        cx, cy = laea(lon0, lat0)
    bounds = (cx - w_m / 2, cy - h_m / 2, cx + w_m / 2, cy + h_m / 2)
    transform = from_bounds(*bounds, W, H)
    # lon/lat box for the search (generous)
    dlat = (h_m / 2) / 111_000 * 1.2
    dlon = (w_m / 2) / (111_000 * math.cos(math.radians(lat0))) * 1.2
    bbox = [lon0 - dlon, lat0 - dlat, lon0 + dlon, lat0 + dlat]

    items = list(
        Client.open(STAC).search(collections=['sentinel-2-l2a'], bbox=bbox, datetime=a.dates, query={'eo:cloud_cover': {'lt': a.max_cloud}}, max_items=60).items()
    )
    items.sort(key=lambda it: it.properties['eo:cloud_cover'])
    if not items:
        raise SystemExit('no Sentinel-2 scenes: widen --dates or --max-cloud')

    # Stack the clearest scenes and take the per-pixel median of valid samples: haze and small clouds drop out.
    stack: list[np.ndarray] = []
    used: list[str] = []
    for it in items:
        if len(stack) >= a.scenes:
            break
        with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', AWS_NO_SIGN_REQUEST='YES'):
            with rasterio.open(it.assets['visual'].href) as src, WarpedVRT(src, crs=crs, transform=transform, width=W, height=H, resampling=Resampling.lanczos) as vrt:
                rgb = vrt.read(out_dtype='uint8')  # 3, H, W
        valid = (rgb.sum(axis=0) > 0)
        if valid.mean() < 0.15:
            continue
        stack.append(np.where(valid[None], rgb, 0).astype(np.float32))
        used.append(it.id)
        print('scene', it.id, f"cloud {it.properties['eo:cloud_cover']:.2f}%", f'coverage {valid.mean():.0%}')
    arr = np.stack(stack)  # N,3,H,W
    arr[arr == 0] = np.nan
    med = np.nanmedian(arr, axis=0)
    hole = np.isnan(med).any(axis=0)
    if hole.any():
        print(f'warning: {hole.mean():.1%} of the plate has no data; filled by inpainting')
    med = np.nan_to_num(med, nan=0).transpose(1, 2, 0).clip(0, 255).astype(np.uint8)
    # Trim edge rows/columns that are mostly empty (a strip past the last scene): an inpainted edge smears.
    t0, t1, l0, l1 = 0, H, 0, W
    while l1 - l0 > W * 0.8 and hole[:, l1 - 1].mean() > 0.02: l1 -= 1
    while l1 - l0 > W * 0.8 and hole[:, l0].mean() > 0.02: l0 += 1
    while t1 - t0 > H * 0.8 and hole[t1 - 1, l0:l1].mean() > 0.02: t1 -= 1
    while t1 - t0 > H * 0.8 and hole[t0, l0:l1].mean() > 0.02: t0 += 1
    if (t0, t1, l0, l1) != (0, H, 0, W):
        print(f'trimmed empty edges: cols {l0}-{l1} rows {t0}-{t1}')
        med, hole = med[t0:t1, l0:l1], hole[t0:t1, l0:l1]
        x_a, y_a = transform * (l0, t0)
        x_b, y_b = transform * (l1, t1)
        bounds = (x_a, y_b, x_b, y_a)
        W, H = l1 - l0, t1 - t0
        transform = from_bounds(*bounds, W, H)
        w_m = bounds[2] - bounds[0]
    if hole.any():
        med = cv2.inpaint(med, hole.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)

    # TCI is a flat 0-255 stretch of reflectance; give it a gentle film curve (the film's grade comes on top in Remotion).
    f = med.astype(np.float32) / 255
    f = np.clip((f - 0.02) / 0.85, 0, 1) ** 0.92
    f = f * f * (3 - 2 * f) * 0.35 + f * 0.65  # soft S-curve
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out / f'{a.name}.jpg'), cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])

    # DEM on the same grid (tiles are 1°×1°).
    dem = np.full((H, W), np.nan, np.float32)
    for la in range(math.floor(bbox[1]), math.floor(bbox[3]) + 1):
        for lo in range(math.floor(bbox[0]), math.floor(bbox[2]) + 1):
            try:
                with rasterio.Env(AWS_NO_SIGN_REQUEST='YES'):
                    with rasterio.open(dem_tile(la, lo)) as src, WarpedVRT(src, crs=crs, transform=transform, width=W, height=H, resampling=Resampling.bilinear, src_nodata=-32767, nodata=np.nan) as vrt:
                        d = vrt.read(1, out_dtype='float32')
                dem = np.where(np.isnan(dem) & ~np.isnan(d), d, dem)
            except rasterio.errors.RasterioIOError:
                print('no DEM tile (sea?)', la, lo)
    dem = np.nan_to_num(dem, nan=0)
    cv2.imwrite(str(out / f'{a.name}_dem.png'), np.clip(dem, 0, 65535).astype(np.uint16))
    lo_, hi_ = np.percentile(dem, 1), np.percentile(dem, 99.5)
    depth = np.clip((dem - lo_) / max(1, hi_ - lo_), 0, 1)
    cv2.imwrite(str(out / f'{a.name}_depth.png'), (cv2.GaussianBlur(depth, (0, 0), W / 900) * 255).astype(np.uint8))
    mpp = w_m / W
    gy, gx = np.gradient(dem, mpp)
    az, alt = math.radians(315), math.radians(40)
    slope = np.arctan(np.hypot(gx, gy) * 1.6)
    aspect = np.arctan2(-gx, gy)
    shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    cv2.imwrite(str(out / f'{a.name}_hill.png'), (np.clip(shade, 0, 1) * 255).astype(np.uint8))
    # relief plate: the true-colour image lit by the terrain (soft-light of the hillshade), what the film shows
    col = cv2.imread(str(out / f'{a.name}.jpg')).astype(np.float32) / 255
    hs = cv2.GaussianBlur(np.clip(shade, 0, 1).astype(np.float32), (0, 0), 1.2)[..., None]
    flat = np.sin(alt)  # shade of flat ground
    lit = np.clip(col * (0.55 + 0.45 * hs / flat), 0, 1)
    cv2.imwrite(str(out / f'{a.name}_relief.jpg'), (lit * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])

    years = sorted({u.split('_')[2][:4] for u in used})
    meta = {
        'name': a.name, 'center': [lon0, lat0],
        # bounds in film map units (1 unit = 3 km, y down), for SatMap's <image>: [x0, y0, x1, y1]
        'mapBounds': None if a.local else [bounds[0] / 3000, -bounds[3] / 3000, bounds[2] / 3000, -bounds[1] / 3000], 'width_km': a.width_km, 'px': [W, H], 'm_per_px': mpp, 'crs': crs.to_proj4(),
        'scenes': used, 'dem_m': [float(dem.min()), float(dem.max())],
        'credit': f"Contains modified Copernicus Sentinel data {', '.join(years)}; Copernicus DEM GLO-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS by the European Union and ESA",
    }
    (out / f'{a.name}.json').write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == '__main__':
    main()
