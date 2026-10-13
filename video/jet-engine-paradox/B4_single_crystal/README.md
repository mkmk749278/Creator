# B4_single_crystal: One single crystal

Session B scene for *The Jet Engine Paradox* (program 356.54–361.60, 5.06 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

The B2 grain cube (same seeds) merges: gaps close, every grain's lattice rotates into one orientation, tints and red borders fade, until one unbroken lattice remains (SINGLE CRYSTAL at 2.3 s). A light sweep runs across the lattice with no break ('No borders at all'), then the blade surface closes over the crystal (reverse of B1's burn-through) and the camera pulls back to the whole blade while a light band runs root to tip.

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–4.68 J059: “So the best blades are grown as one single crystal. No borders at all.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B4_single_crystal.mp4` (pinned 0.8.103).
