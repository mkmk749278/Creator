# B6_cooling_channels: Air: the cooling channels

Session B scene for *The Jet Engine Paradox* (program 366.52–375.01, 8.49 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

J061: the solid blade; an x-ray scan line (amber edge) runs root to tip, turning the blade into a translucent ghost and revealing the hollow inside: a leading-edge passage and a three-pass serpentine with trailing-edge exit ducts. COOLING CHANNELS at 3.95 s. From 4.4 s cool compressor air (cyan particles; the passages fill cyan as the front advances) enters at the bottom of the root and snakes through, leaving through the trailing-edge slots and the leading-edge showerhead.

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–1.81 J061: “The second secret is air.”
- +2.34–8.17 J062: “Each blade is hollow, with tiny channels inside. Cooler air from the compressor is pushed through them.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B6_cooling_channels.mp4` (pinned 0.8.103).
