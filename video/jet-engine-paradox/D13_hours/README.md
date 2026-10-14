# D13_hours: Thousands of hours

Session D scene for *The Jet Engine Paradox* (program 309.11–312.62, 3.51 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1rpxBmYKqlw8UeBoGdyxxXWGInvW0zBEQ/view · contact sheet: https://drive.google.com/file/d/1rWMUwOO4I7YmEozzYtxUiEVsO_SXp5Ow/view

Left: a stopwatch (ROCKET: MINUTES) sweeps once and stops with a recoil. Right: a four-drum odometer (JET ENGINE: THOUSANDS OF HOURS) rolls to 4,000 and a + stamps in.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–3.13 J050: “And it must run for thousands of hours between overhauls.” · on-screen `JET ENGINE: THOUSANDS OF HOURS`

## Parameters (`params.js`)
labels, `hours`, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `kit.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- The rocket side shows no number (spec gives none).
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D13_hours`): 119 s wall.
