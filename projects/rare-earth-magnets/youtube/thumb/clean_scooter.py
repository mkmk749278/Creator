#!/usr/bin/env python3
"""Remove the 'Electron' / 'XO Electron' logos from the stock scooter (Pixabay 1313453) so the thumbnail shows a
generic electric scooter, not a foreign brand (thumbnail panel, 2026-10-22). Bright letter pixels inside each logo
box are filled from the surrounding dark panel (normalised blur), then softened. In: escooter.jpg  Out: escooter_clean.jpg"""
from PIL import Image, ImageFilter
import numpy as np

im = Image.open("escooter.jpg").convert("RGB"); a = np.asarray(im).astype(np.float32)
lum = a.mean(-1)
for (x0, y0, x1, y1, th) in [(436, 418, 522, 486, 40), (915, 500, 1100, 620, 70)]:
    box = a[y0:y1, x0:x1]; L = lum[y0:y1, x0:x1]
    mask = (L > th).astype(np.float32)
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))).astype(np.float32) / 255
    keep = 1 - mask
    fill = np.zeros_like(box)
    w = np.asarray(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float32) / 255 + 1e-4
    for c in range(3):
        ch = np.asarray(Image.fromarray(np.clip(box[..., c] * keep, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
        fill[..., c] = ch / w
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)[..., None] / 255
    a[y0:y1, x0:x1] = box * (1 - m) + fill * m
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save("escooter_clean.jpg", quality=95)
