# B3_creep: Creep

Session B scene for *The Jet Engine Paradox* (program 349.73–356.54, 6.81 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

A bar of grains held in two grips. Heat (amber glow, embers, heat shimmer, light from below) from 'heat' (0.45 s); white pull arrows from 'huge force' (1.05 s). From 1.9 s the bar stretches slowly: grains move apart, slide and tilt at the boundaries, and the red boundaries open into glowing gaps (brightest on 'borders', 3.4-4.4 s). A small blade beside it lengthens past a dashed line at its original tip height, a red bar marking the extra length. CREEP at 5.4 s. Strain is exaggerated for the eye (illustration).

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–6.42 J058: “Under heat and huge force, the metal slowly stretches along those borders. Engineers call it creep.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B3_creep.mp4` (pinned 0.8.103).
