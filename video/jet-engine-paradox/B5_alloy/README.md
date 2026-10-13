# B5_alloy: Nickel superalloy + rhenium

Session B scene for *The Jet Engine Paradox* (program 361.60–366.52, 4.92 s, 1920×1080, 30 fps). Spec and cues: `projects/jet-engine-paradox/scenes.md`.

Hero blade turning slowly; element tiles (Ni, Co, Cr, Al, Ta, W, Re, with names) fly in and orbit like a recipe, Ni the largest. Ni glows on 'nickel'; label NICKEL SUPERALLOY at 1.1 s. Re pulses amber and grows on 'rhenium' (3.45 s) as '· + RHENIUM' appears in the label. On 'mixed in' the tiles spiral into the blade and an amber light band runs up the metal.

Cues (VO line timing; word cues inside a line are estimated by character position, no word-level alignment exists):
- +0.15–4.52 J060: “The metal is a nickel super alloy, with rare elements like rhenium mixed in.”

- Tag: ILLUSTRATION (added by the assembler, bottom-right; this scene leaves both right corners clear).
- Code: `index.html` + `lib.js` (copy of `../_b_lib/lib.js`; edit there and run `../_b_lib/sync.sh`) + `jep.css` (copy of `../_shared/jep.css`).
- Assets: `vendor/library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0). Everything else is procedural (no third-party models or textures).
- Render: `npx hyperframes render --workers 3 --video-bitrate 24M --output B5_alloy.mp4` (pinned 0.8.103).
