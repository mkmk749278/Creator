# B2_polycrystal: Many crystals, weak borders

Session B scene for *The Jet Engine Paradox* (program 344.05–349.73, 5.68 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

Opens tight on a cube face (atoms large), pulls back and orbits to a 3/4 view of a cube of 27 Voronoi grains, each a different metallic tint with its own lattice orientation. MANY CRYSTALS lands on 'many' (1.55 s). On 'The borders' (2.85 s) the grain boundaries glow Warning Red; WEAK BORDERS at 3.08 s; on 'weak spots' the grains part slightly, exposing glowing boundary planes.

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–5.36 J057: “Normal metal is made of many tiny crystals. The borders between them are weak spots.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B2_polycrystal.mp4` (pinned 0.8.103).
- Measured render (1080p, 3 workers, cloud VM 4 vCPU, software GL): 325 s wall for 5.68 s (57 s per output second).
