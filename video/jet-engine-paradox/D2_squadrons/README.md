# D2_squadrons: 42 vs 29 squadrons

Session D scene for *The Jet Engine Paradox* (program 60.87–66.69, 5.82 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1UOYMZLoHTaxxmq_gfeK1BQClbYrsrjIs/view · contact sheet: https://drive.google.com/file/d/1uklDlVbi7Ibgk4zUWdxdIe-Cz8Pf6r0Q/view

42 delta-fighter slots (7 × 6) draw in on a drafting grid while SANCTIONED counts to 42 on "forty two". On "twenty nine" 29 slots fill amber one by one (the ACTUAL counter follows the fills to ~29); the 13 empty slots turn red and pulse.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–5.54 J011: “The Air Force is supposed to have forty two fighter squadrons. Today it has about twenty nine.” · on-screen `SANCTIONED 42 · ACTUAL ~29`

## Parameters (`params.js`)
`sanctioned`, `actual`, labels, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `kit.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- Generic delta silhouette (not a manufacturer drawing).
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D2_squadrons`): 186 s wall.
