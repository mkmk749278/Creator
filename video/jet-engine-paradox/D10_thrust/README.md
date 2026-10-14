# D10_thrust: 81 kN target, about 70 reported

Session D scene for *The Jet Engine Paradox* (program 225.91–231.63, 5.72 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/13u1anhMr1HT7HjuQCvFmUvBbD3yOE6B3/view · contact sheet: https://drive.google.com/file/d/1QaQe3rzg_48qiDapdaj5w4Z2VOgXZUPU/view

Thrust bar 0–90 kN. The dashed 81 kN line rises on "eighty one" (81 kN TARGET); on "it reached only about seventy" the fill climbs, stalls at ~70 with a dying shudder, and the gap to 81 hatches red (~70 kN REPORTED).

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–5.51 J037: “It was meant to push eighty one kilonewtons. As reported, it reached only about seventy.” · on-screen `81 kN TARGET · ~70 kN REPORTED`

## Parameters (`params.js`)
`max`, `target`, `reported`, labels, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `kit.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- Same thrust-bar motif as the film's other target/achieved scenes (target line vs fill).
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D10_thrust`): 181 s wall.
