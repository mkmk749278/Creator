# C6_split_blueprint: New jet and new engine at once

Session C scene for *The Jet Engine Paradox* (program 208.44–215.23, 6.79 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1VxE34K5Xl0g_atBWSnmiAMCKjkrH_y1d/view

Split blueprint on a dashed divider. Left: the generic delta fighter airframe; right: the Kaveri half-section. Both draw
in a shuffled stroke order, in fits and starts (seeded noise), and never get past about two thirds: lines flicker,
pen tips are everywhere and construction lines race across both sheets. At 5.38 s ("That doubled the risk") both
drawings turn red and pulse twice with a red glow; the divider turns red.

Cue (word times estimated by character position):
- +0.15–6.49 J034: “And India was building a brand new jet, the Tejas, at the same time. Both almost from scratch. That doubled the risk.”

## Parameters (`params.js`): `tRisk` (s), `drawn` (how far the drawings get, 0–1). No on-screen words.

## Notes
- The first ~1.3 s is mostly construction marks and pen tips (the drawings start from nothing).
- ILLUSTRATION tag and logo bug come from the assembler.
- Render (pinned 0.8.103, 4 workers): 19 s wall for 6.79 s.
