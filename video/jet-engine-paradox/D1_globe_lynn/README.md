# D1_globe_lynn: Lynn to Bengaluru

Session D scene for *The Jet Engine Paradox* (program 27.77–35.99, 8.22 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1AOFPQYIuWc8KTNiy41JnPYTE9kgkP1dD/view · contact sheet: https://drive.google.com/file/d/1LF_4sWBHdeeTihx2flKDQKDYTC961Jom/view

Land-only globe turns from the Atlantic to New England; a reticle marker and callout land on LYNN, USA at "Lynn". At "about thirteen thousand kilometres" an amber great-circle arc (with a dashed ground track) draws to BENGALURU while the camera travels with it and the distance counter rides the arc to ~13,000 KM (OUR CALCULATION). India's coast warms amber when the arc lands.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–7.82 J007: “The biggest reason? They are waiting for an engine. An engine made in Lynn, Massachusetts, about thirteen thousand kilometres away.” · on-screen `LYNN, USA → BENGALURU · ~13,000 KM (OUR CALCULATION)`

## Parameters (`params.js`)
`from`, `to` (names, [lat, lon]), `route`, `km`, `note`, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `globe.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- Distance check: Lynn (42.47 N, 70.95 W) to Bengaluru (12.97 N, 77.59 E) great circle = 13,065 km, shown as ~13,000.
- The spec's corner tag (OUR CALCULATION) is also kept small under the counter because it is part of the on-screen line.
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D1_globe_lynn`): 260 s wall.
