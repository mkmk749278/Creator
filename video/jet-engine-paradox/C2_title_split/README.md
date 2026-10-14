# C2_title_split: Moon vs empty engine bay

Session C scene for *The Jet Engine Paradox* (program 35.99–42.32, 6.33 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1Qc958vrT0KxkYFATmaiCHgm2u-ed3baT/view

Split frame on a glowing amber seam at x = 960. Left: the photo slot (Chandrayaan-3) under a slow push and drift.
Right: the generic delta fighter draws itself in a rear three-quarter view (0.15–2.6 s) and its empty engine bay glows
from 2.2 s. At 3.2 s ("Why can it not build…") the line `INDIA LANDED ON THE MOON. WHY NOT A JET ENGINE?` burns in
letter by letter across the seam (hot amber glow cooling to white).

Cue (word times estimated by character position):
- +0.15–5.98 J008: “So here is the question. India landed on the Moon. Why can it not build its own fighter jet engine?”

## Parameters (`params.js`)
| key | meaning |
|---|---|
| `photo` | path of the real Chandrayaan-3 image for the left half; `""` renders the PHOTO SLOT plate |
| `photoPos` | CSS `object-position` inside the left half (960×1080, pushed 10 %) |
| `line` | the burned-in line |
| `burnAt` | start of the burn-in (s) |

## Notes
- Tag and logo bug are added by the assembler; both right corners are clear.
- Code: `index.html` + `_bp.js`/`_c.css` (copies of `../_c_lib/`) + `jep.css`. Generic procedural airframe.
- Render (pinned 0.8.103, 4 workers): 19 s wall for 6.33 s.
