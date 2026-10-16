"""Plates for session B's scenes ("the third door" desk world). Deterministic (seeded); run once, output in b_kit/plates/.

desk.jpg   2240x1260  navy linen desk blotter, cool fill, soft edge falloff (the base the camera drifts over)
light.png  2240x1260  warm window light: two blurred panes with a mullion shadow, RGBA, screen-blended and drifted
paper.jpg  640x640    warm paper tile: fibres + mottling (background of every document)
"""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path

OUT = Path(__file__).parent / "plates"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
W, H = 2240, 1260

def blur(a, r):
    im = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255

# desk: navy base, linen weave (horizontal + vertical threads), low-frequency mottling, vignette falloff
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
base = np.array([0x0B, 0x14, 0x22], np.float32) / 255
top = np.array([0x1A, 0x2E, 0x47], np.float32) / 255
g = np.clip(1 - (((x - W * 0.42) / (W * 0.75)) ** 2 + ((y - H * 0.38) / (H * 0.8)) ** 2), 0, 1) ** 1.3
img = base[None, None] * (1 - g[..., None]) + top[None, None] * g[..., None]
wx = blur(rng.random((H, W)).astype(np.float32), 0.6)
thread = (np.sin(x * 2.1) * 0.5 + 0.5) * 0.5 + (np.sin(y * 1.9) * 0.5 + 0.5) * 0.5
mott = blur(rng.random((H // 8, W // 8)).astype(np.float32), 3)
mott = np.asarray(Image.fromarray((mott * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
tex = (thread - 0.5) * 0.035 + (wx - 0.5) * 0.05 + (mott - 0.5) * 0.06
img = np.clip(img * (1 + tex[..., None] * 2.2), 0, 1)
Image.fromarray((img * 255).astype(np.uint8)).save(OUT / "desk.jpg", quality=88)

# window light: two tall panes, skewed (light falls at an angle), mullion gap, heavy blur; warm key colour
m = np.zeros((H, W), np.float32)
sk = (y - H * 0.5) * 0.55          # skew: panes lean to the right as they go down
for x0 in (W * 0.12, W * 0.36):
    m += ((x - sk > x0) & (x - sk < x0 + W * 0.21) & (y > H * 0.02) & (y < H * 0.92)).astype(np.float32)
m = blur(m * 0.9, 38) * 0.75 + blur(m, 120) * 0.35
fall = np.clip(1.15 - x / (W * 1.05), 0, 1)
a = np.clip(m * fall, 0, 1)
warm = np.array([255, 214, 160], np.float32)
rgba = np.dstack([np.broadcast_to(warm[c], (H, W)) for c in range(3)] + [a * 255]).astype(np.uint8)
Image.fromarray(rgba, "RGBA").save(OUT / "light.png", optimize=True)

# paper tile: off-white, fibres (short stretched noise), mottling; tileable enough at 640 px for a document face
P = 640
p = np.ones((P, P, 3), np.float32) * np.array([0.965, 0.955, 0.93], np.float32)
fib = np.asarray(Image.fromarray((rng.random((P, P)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
fib2 = np.asarray(Image.fromarray((rng.random((P // 2, P * 2)) * 255).astype(np.uint8)).resize((P, P), Image.BICUBIC)).astype(np.float32) / 255
mo = np.asarray(Image.fromarray((rng.random((P // 32, P // 32)) * 255).astype(np.uint8)).resize((P, P), Image.BICUBIC)).astype(np.float32) / 255
t = (fib - 0.5) * 0.045 + (fib2 - 0.5) * 0.03 + (mo - 0.5) * 0.04
p = np.clip(p * (1 + t[..., None]), 0, 1)
Image.fromarray((p * 255).astype(np.uint8)).save(OUT / "paper.jpg", quality=90)
print("plates written to", OUT)
