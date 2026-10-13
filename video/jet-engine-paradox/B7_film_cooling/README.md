# B7_film_cooling: Film cooling

Session B scene for *The Jet Engine Paradox* (program 375.01–380.97, 5.96 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

Close-up on the leading edge: hot gas (amber streaks) comes from upstream and splits round the glowing leading edge. From 0.75 s the hole rows (showerhead, pressure-side and suction-side rows) light cyan and air jets out, bending downstream to hug the surface. From 2.5 s a thin cyan blanket spreads over the surface from the hole rows and the heat glow fades under it, while the camera pulls back. FILM COOLING at 3.9 s.

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–5.61 J063: “It comes out through rows of tiny holes, and covers the blade in a thin blanket of cooler air.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B7_film_cooling.mp4` (pinned 0.8.103).
