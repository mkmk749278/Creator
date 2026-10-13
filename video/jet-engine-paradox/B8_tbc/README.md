# B8_tbc: Ceramic heat shield

Session B scene for *The Jet Engine Paradox* (program 380.97–384.63, 3.66 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

Curved section of the blade wall: hot gas (amber streaks) above, metal, bond coat, cooling air (cyan) below. From 0.75 s the ceramic top coat seals over the metal from left to right (glowing front, columnar texture). The section face shows the temperature as an ironbow gradient, dropping steeply through the ceramic and gently through the metal (no numbers). Layer labels HOT GAS / CERAMIC COATING / METAL / COOLING AIR track the section on the right; THERMAL BARRIER COATING at 1.25 s.

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–3.24 J064: “And on top, a ceramic coating acts like a heat shield.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B8_tbc.mp4` (pinned 0.8.103).
- Measured render (1080p, 3 workers, cloud VM 4 vCPU, software GL): 151 s wall for 3.66 s (41 s per output second).
