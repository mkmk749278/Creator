# D14_paris_derby: Safran picked; deal awaits approval

Session D scene for *The Jet Engine Paradox* (program 473.87–493.43, 19.56 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1cbHNoOMs4rXTN1fku7PypskVVvmvuzBW/view · contact sheet: https://drive.google.com/file/d/1tJMA7RyxVJ1g6EAOdLhQQJ34cy083wt3/view

J080: SAFRAN marker in Paris, amber arc to Bengaluru (GTRE), lower-left SAFRAN + GTRE · SELECTED AUG 2025. J081: camera pushes in on India, its coast warms and FULL INDIAN IP stamps down. J082: chip AWAITING FINAL APPROVAL · OCT 2026 (pulsing pending dot) while the Safran arc turns dashed; then a second, ceramic-amber arc from Derby (ROLLS-ROYCE + RELIANCE, AUG 2026) to a hollow India marker.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–5.10 J080: “In twenty twenty five, the government picked France's Safran to build it together with GTRE.” · on-screen `SAFRAN + GTRE · SELECTED AUG 2025`
- +5.45–10.06 J081: “India's condition is clear. The design and the rights must belong to India.” · on-screen `FULL INDIAN IP`
- +10.40–19.30 J082: “As of now, that deal is still waiting for final approval. And in August twenty twenty six, Rolls-Royce and Reliance also offered to build an engine in India.” · on-screen `AWAITING FINAL APPROVAL · OCT 2026`

## Parameters (`params.js`)
`safran`, `gtre`, `selected`, `stamp`, `status`, `rr` (name, sub, from, to), beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `globe.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- The Derby arc ends at central India (no city named, since the spec says only "India").
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D14_paris_derby`): 576 s wall.
