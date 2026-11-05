#!/usr/bin/env python3
"""Depth maps for archive photos, for DepthPhoto's 2.5D camera dolly (PLAYBOOK §8.2).

  .venv/bin/python scripts/depth_map.py films/tata-history/assets/media/A001a.jpg [more.jpg ...]
writes <name>_depth.png next to each image (8-bit grey, white = near, same aspect, max 1024 px wide: the depth is
smooth, the photo carries the detail).

Model: Depth Anything V2 Small (Apache-2.0), ONNX export `onnx-community/depth-anything-v2-small` (model.onnx), run
on CPU with onnxruntime 1.31.1 (the review venv: PLAYBOOK §7.9). Pinned by the Hub revision below.
The raw output is relative inverse depth; we normalise each photo to its 2nd–98th percentile, then soften edges a
little (a median filter) so the displaced mesh tears less at silhouettes.
"""
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from PIL import Image, ImageFilter

REPO, FILE, REV = "onnx-community/depth-anything-v2-small", "onnx/model.onnx", "main"
SIZE = 518  # the model's native input (multiple of 14)


def load() -> ort.InferenceSession:
    path = hf_hub_download(REPO, FILE, revision=REV)
    return ort.InferenceSession(path, providers=["CPUExecutionProvider"])


def depth(sess: ort.InferenceSession, img: Image.Image) -> np.ndarray:
    w, h = img.size
    s = SIZE / min(w, h)
    nw, nh = (round(w * s / 14) * 14, round(h * s / 14) * 14)
    x = np.asarray(img.convert("RGB").resize((nw, nh), Image.BICUBIC), dtype=np.float32) / 255.0
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    out = sess.run(None, {sess.get_inputs()[0].name: x})[0]
    return np.squeeze(out)


def main() -> None:
    sess = load()
    for f in sys.argv[1:]:
        p = Path(f)
        img = Image.open(p)
        d = depth(sess, img)
        lo, hi = np.percentile(d, 2), np.percentile(d, 98)
        d = np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)
        g = Image.fromarray((d * 255).astype(np.uint8))
        w = min(1024, img.size[0])
        g = g.resize((w, round(w * img.size[1] / img.size[0])), Image.BICUBIC).filter(ImageFilter.MedianFilter(5))
        out = p.with_name(p.stem + "_depth.png")
        g.save(out)
        print(f"{out} {g.size[0]}x{g.size[1]}")


if __name__ == "__main__":
    main()
