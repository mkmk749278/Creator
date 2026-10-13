# B1_metal_zoom: Into the metal

Session B scene for *The Jet Engine Paradox* (program 341.36–344.05, 2.69 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

Continuous log-space push from a 3/4 view of the blade into a point on the pressure side. From 1.45 s the surface burns away from the centre of frame (glowing amber edge) and reveals the grain structure underneath: a slab of 3D Voronoi grains with an FCC atom lattice per grain, the same shader as B2, so the cut into B2 is continuous. Etched borders are dark (not red yet).

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–2.23 J056: “The first secret is in the metal itself.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B1_metal_zoom.mp4` (pinned 0.8.103).
- Measured render (1080p, 3 workers, cloud VM 4 vCPU, software GL): 218 s wall for 2.69 s (81 s per output second).
