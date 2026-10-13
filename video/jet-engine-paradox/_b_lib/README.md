# Session B shared library

`lib.js` is the source of truth for Session B's eight scenes (B1–B8); `sync.sh` copies it (and `../_shared/jep.css`) into every
`B*_*/` folder and re-vendors three.js, postprocessing and the HDRI. The folder name starts with `_` so the vendoring walk skips it.

What it provides (all a pure function of time):
- `createStage`: renderer, HDRI (studio_small_09, CC0), MSAA composer, bloom, vignette, ACES, and a lens pass (heat shimmer band,
  slight chromatic aberration, seeded grain); a slate backdrop with slow amber haze anchored to the view; the HyperFrames ready handshake.
- `buildBlade`: procedural HP turbine blade: cambered, twisted airfoil loft (about 110° of flow turning), squealer tip, platform,
  shank, fir-tree root; shader film-cooling holes (3 showerhead rows, pressure and suction rows, trailing-edge slots) from surface
  coordinates; `surfAt(arc, y)` returns a surface point and normal for emitting air.
- `metalMaterial(features)`: MeshPhysicalMaterial + feature flags: HOLES, LATTICE (FCC atoms with sphere shading), BLOCK (Voronoi
  grain borders from neighbour seeds, red boundary glow), SWEEP, SCAN, HEAT (red→amber→pale ironbow), DISSOLVE / REVEAL (screen-space
  burn-through), WORLEY. Has a NaN guard (a NaN pixel would otherwise blank the whole frame through the bloom blur).
- `voronoiCells` / `grainMeshes`: true 3D Voronoi grains (convex polyhedra clipped from a box) with per-grain tint and lattice.
- `buildChannels`, `ghostMaterial`, `channelMaterial`: internal cooling passages and the x-ray look; `Streaks`, `Path`, `makeEmbers`, `elementTile`.

HyperFrames notes learned here (also worth adding to PLAYBOOK §10):
- The three adapter waits on `window.THREE.DefaultLoadingManager`, which an ES-module scene never sets. Scenes therefore create a
  `window.__hf.buildReady` promise in a classic `<head>` script; `lib.js` resolves it after the HDRI and fonts load and frame 0 is drawn.
  Without it, early snapshot/render frames can be captured black.
- A geometry without `uv` under `anisotropy` gives NaN normals; with bloom on, the NaN spreads and the whole frame renders black.
