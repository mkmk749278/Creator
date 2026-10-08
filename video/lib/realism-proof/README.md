# realism-proof

Reference scene for the vendored 3D stack (PLAYBOOK §9): a translucent cell with organelles, lit by a library HDRI,
N8AO ambient occlusion, mipmap bloom, vignette and AgX tone mapping, organic motion from seeded 4D simplex noise.
It is the template new 3D library scenes start from, and the baseline for `scripts/bench_render.py`.

- Not a parameterised library scene (no `params.js`): copy it, don't drop it into a film.
- `window.BENCH = {ao: 0, bloom: 0, hdri: 0}` turns passes off for cost measurement.
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0).

## Render cost (1080p, 2 s, `--workers 3`, cloud VM 4 vCPU, software GL, pinned hyperframes 0.8.103)

| Variant | Wall time (2 s) | s per output s | vs full |
|---|---|---|---|
| full (HDRI + N8AO half-res + bloom + vignette + AgX) | 103.6 s | 51.8 | 1.00× |
| no N8AO | 53.3 s | 26.6 | 0.51× |
| no bloom | 93.1 s | 46.5 | 0.90× |
| bare (no HDRI, AO, bloom) | 17.0 s | 8.5 | 0.16× |

N8AO alone doubles the cost; bloom adds ~11%. Use N8AO for hero close-ups only (or bake contact shadows).
