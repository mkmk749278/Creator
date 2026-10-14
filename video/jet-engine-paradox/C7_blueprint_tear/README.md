# C7_blueprint_tear: Delinked, September 2008

Session C scene for *The Jet Engine Paradox* (program 244.11–254.04, 9.93 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1gV9WqPwr_HCVtb_MPjvfFX9kpzZdy4nP/view

0–3.55 s: the photo slot (credited headline image) under a slow push, label `SEP 2008 · KAVERI DELINKED FROM TEJAS`
from 0.4 s (stays to the end). 3.55–4.35 s a scan line wipes in the blueprint; the generic delta fighter re-inks with
its Kaveri (amber engine block) in the bay. 4.9 s ("separated from the Tejas programme"): the paper tears along a
jagged line around the engine bay; the torn piece carrying the Kaveri lifts, turns and drifts out of frame
(4.9–6.5 s), leaving a dark hole with a red edge. 6.6 s ("The Tejas would fly with the American engine"): a new paper
patch slides in and seats in the hole, carrying the airframe lines and a different engine drawn in white; leader
`US ENGINE` at 8.3 s ("American").

Cue (word times estimated by character position):
- +0.15–9.64 J041: “In September two thousand eight, the Kaveri was officially separated from the Tejas programme. The Tejas would fly with the American engine.”

## Parameters (`params.js`)
| key | meaning |
|---|---|
| `photo` | path of the credited headline image (first ~4 s); `""` renders the PHOTO SLOT plate |
| `photoPos` | CSS `object-position` for it |
| `label`, `usLead` | on-screen words |
| `wipeAt`, `tearAt`, `patchAt`, `usLeadAt` | beat times (s) |

## Notes
- The headline's credit, the ILLUSTRATION tag and the logo bug are added by the assembler; both right corners are
  clear. `US ENGINE` is the spec's own label for the replacement engine block.
- Code: `index.html` + `_bp.js`/`_c.css` (copies of `../_c_lib/`) + `jep.css`. Generic procedural airframe/engines.
- Render (pinned 0.8.103, 4 workers): 34 s wall for 9.93 s.
