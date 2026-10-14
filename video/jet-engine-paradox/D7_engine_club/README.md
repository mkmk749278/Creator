# D7_engine_club: The engine club

Session D scene for *The Jet Engine Paradox* (program 160.15–172.31, 12.16 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1XiVxYA2dtNQ2cL0OyZuElNTwek-LgGYr/view · contact sheet: https://drive.google.com/file/d/1e21WukGAAkapGt91y8_Me4eSEjaCQEMa/view

Title THE ENGINE CLUB (lower left). A polar-tilted view over the North Atlantic holds USA, Russia, Britain and France; each reticle marker and its makers' callout lands as the VO names it. The camera then swings east for CHINA (AECC); India's coast warms faint amber with a hollow, dashed reticle: in view, but empty.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–11.84 J027: “But only a handful can design and build a modern fighter engine on their own. The main ones are America, Russia, Britain and France. And, after decades of struggle, China.” · on-screen `THE ENGINE CLUB`

## Parameters (`params.js`)
`title`, `members` (name, makers, [lat, lon], time, callout side/offset), `india`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `globe.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- Markers sit near each maker's home region (GE/P&W north-east US, UEC Saturn/Klimov west Russia, Rolls-Royce Derby, Safran Paris, AECC Beijing).
- "India outlined" is done with its coastline and a soft tint, never a land-border outline (a land border is a political border).
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D7_engine_club`): 387 s wall.
