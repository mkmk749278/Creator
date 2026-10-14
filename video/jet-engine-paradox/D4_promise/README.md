# D4_promise: Promised 2023, first engine March 2025

Session D scene for *The Jet Engine Paradox* (program 91.08–97.31, 6.23 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1pUO7gN3tC-IOevLCkNZ4nZVFLSJxyr2g/view · contact sheet: https://drive.google.com/file/d/1lPNpYEwO9gU3GUL45HIVbgt8j7LaiR6z/view

Engraved timeline 2021–2026 (month ticks). The amber PROMISED 2023 pin drops on "twenty twenty three"; the delivery pin then slides month by month (its chip reads the month as it moves) to MAR 2025 while the gap fills red, ending on FIRST ENGINE MAR 2025.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–5.94 J015: “The engines were due from twenty twenty three. The first one came only in March twenty twenty five.” · on-screen `PROMISED 2023 · FIRST ENGINE MAR 2025`

## Parameters (`params.js`)
`years`, `promised`, `first`, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `kit.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- The spec's one-line text is split onto the two pins (PROMISED 2023 · FIRST ENGINE MAR 2025).
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D4_promise`): 193 s wall.
