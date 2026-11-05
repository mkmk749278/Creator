#!/usr/bin/env python3
"""The all-India satellite plate for SatMap: NASA Blue Marble Next Generation (topography and bathymetry, December
2004; public domain, credit "NASA Earth Observatory") reprojected into the film's map projection.

Blue Marble tiles are plate carrée, 21600 px per 90°: C1 = 0–90°E, D1 = 90–180°E, both 90°N–0°. Download once:
  https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x21600x21600.{C1,D1}.jpg

Usage: .venv-geo/bin/python scripts/bluemarble_india.py BM_DIR OUT_DIR [--km-per-px 1.25]
Writes OUT_DIR/india_bm.jpg and india_bm.json ({mapBounds: [x0, y0, x1, y1]} in map units, 1 unit = 3 km, y down).
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import rasterio
from affine import Affine
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.vrt import WarpedVRT

LAEA = '+proj=laea +lat_0=22 +lon_0=80 +R=6371000 +units=m +no_defs'
# map units (3 km): wide enough for Karachi, Burma, Tibet and the sea down to the equator
BOX = (-1050, -900, 1150, 720)
DEG = 90 / 21600


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('bm')
    ap.add_argument('out')
    ap.add_argument('--km-per-px', type=float, default=1.25)
    a = ap.parse_args()
    x0, y0, x1, y1 = BOX
    W = round((x1 - x0) * 3 / a.km_per_px)
    H = round((y1 - y0) * 3 / a.km_per_px)
    dst_t = from_bounds(x0 * 3000, -y1 * 3000, x1 * 3000, -y0 * 3000, W, H)
    out = np.zeros((3, H, W), np.uint8)
    for tile, lon0 in (('C1', 0), ('D1', 90)):
        src_t = Affine(DEG, 0, lon0, 0, -DEG, 90)
        with rasterio.open(Path(a.bm) / f'bm_{tile}.jpg') as src, WarpedVRT(
            src, src_crs=CRS.from_epsg(4326), src_transform=src_t, crs=CRS.from_proj4(LAEA), transform=dst_t, width=W, height=H, resampling=Resampling.lanczos
        ) as vrt:
            d = vrt.read()
        m = d.sum(axis=0) > 0
        out[:, m] = d[:, m]
        print(tile, f'{m.mean():.0%} of the plate')
    img = out.transpose(1, 2, 0)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(Path(a.out) / 'india_bm.jpg'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    (Path(a.out) / 'india_bm.json').write_text(json.dumps({'mapBounds': list(BOX), 'px': [W, H], 'credit': 'NASA Earth Observatory, Blue Marble Next Generation (Dec 2004)'}))
    print(W, H)


if __name__ == '__main__':
    main()
