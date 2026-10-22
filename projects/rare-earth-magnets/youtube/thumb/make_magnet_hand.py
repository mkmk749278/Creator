#!/usr/bin/env python3
"""Thumbnail plate: re-skin the coin in Pixabay 2643160 (fingers holding a coin up to the camera) as a plain
nickel-plated disc magnet. Keeps the photo's real lighting, edge and finger overlap; no AI.
In: fingers.jpg  Out: fingers_magnet.jpg   (python3 make_magnet_hand.py)"""
from PIL import Image, ImageFilter
import numpy as np

a = np.asarray(Image.open("fingers.jpg").convert("RGB")).astype(np.float32) / 255
H, W = a.shape[:2]; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy, rx, ry = 641.0, 267.0, 136.0, 129.0
d = np.hypot((xx - cx) / rx, (yy - cy) / ry); rad = np.clip(d, 0, 1); ang = np.arctan2(yy - cy, xx - cx)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
blur = lambda m, k: np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(k))).astype(np.float32) / 255
# skin = the thumb above and the finger below, only near the rim, by colour balance (gold coin has little blue)
skin = (r > g + 0.05) & (r > b + 0.08) & (b > 0.56 * r) & (d > 0.92) & ((yy < cy - 85) | (yy > cy + 85))
skin = np.asarray(Image.fromarray((skin * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.MaxFilter(3))).astype(np.float32) / 255
skin = blur(skin, 1.2)
# new face: satin nickel lit from upper left, faint machining rings, two soft highlights, a bright chamfer ring
lum = 0.60 + 0.20 * (-(xx - cx) / rx * 0.45 - (yy - cy) / ry * 0.65)
sweep = 0.30 * np.exp(-((ang + 0.9) % (2 * np.pi) - np.pi) ** 2 / 0.35) * rad + 0.22 * np.exp(-((ang - 2.2) % (2 * np.pi) - np.pi) ** 2 / 0.25) * rad
face = blur(np.clip(lum + 0.012 * np.sin(rad * 420) + sweep, 0, 1), 0.6)
new = np.stack([face * 0.94, face * 0.97, face * 1.02], -1)
new = np.clip(new + np.exp(-((rad - 0.955) / 0.012) ** 2)[..., None] * 0.55 - np.clip((rad - 0.97) / 0.03, 0, 1)[..., None] * 0.35, 0, 1)
m = (np.clip((1.0 - d) / 0.012, 0, 1) * (1 - skin))[..., None]
out = a * (1 - m) + new * m
# side wall just outside the face: gold -> silver, but never on skin (incl. the shadowed thumb pad)
skin_any = (r > g + 0.04) & (b > 0.50 * r) & (r > 0.35)
wall = (d > 0.97) & (d < 1.12) & (b < 0.56 * r) & ~skin_any & ~((np.abs(yy - cy) > 100) & (d > 1.02))
wm = blur(wall.astype(np.float32), 1.0)[..., None]
lumw = (0.3 * out[..., 0] + 0.59 * out[..., 1] + 0.11 * out[..., 2])[..., None]
out = out * (1 - wm) + np.clip(lumw * 1.12, 0, 1) * np.array([0.93, 0.96, 1.0]) * wm
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save("fingers_magnet.jpg", quality=95)
