# C3_sanctions_wireframe: 1998, engines and flight-control help cut off

Session C scene for *The Jet Engine Paradox* (program 136.24–144.07, 7.83 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1BndNOhwjnRryEOqBsWBFhQDbVDkJFlhq/view

A plan-view blueprint of the generic delta fighter (prototype era: slightly warmer, older paper) draws itself in 2 s
under a slow orbit. 1.0–2.3 s a white engine block draws into the bay, leader `GE F404`. On "stopped" (3.5 s) it turns
red, a red `STOPPED` stamp slams on, and the engine breaks up and fades (3.95–5.0 s). 4.3–5.8 s a white FLIGHT
CONTROLS box draws in the centre fuselage with dashed wiring to the elevons and rudder (leader `FLIGHT CONTROLS`). On
"ended" (6.9 s) it turns red, gets its own `STOPPED` stamp and fades. Label: `F404 SALES STOPPED` at 3.55 s, extended
to `F404 SALES STOPPED · FLIGHT-CONTROL HELP ENDED` at 6.95 s.

Cue (word times estimated by character position):
- +0.15–7.54 J023: “Sales of the same GE F four zero four engines to India were stopped. American help on the Tejas flight controls also ended.”

## Parameters (`params.js`)
All on-screen words (`engineLead`, `boxLead`, `stamp`, `label1`, `label2`) and the two beat times (`tEngineStop`,
`tBoxStop`).

## Notes
- The citation tag [AEROSPACEWEB | BUSINESS STANDARD], ILLUSTRATION tag and logo bug are added by the assembler; both
  right corners are clear. The leader `GE F404` is the only word not in the spec line (it names the engine block the VO
  names).
- Code: `index.html` + `_bp.js`/`_c.css` (copies of `../_c_lib/`) + `jep.css`. Generic procedural airframe and engine.
- Render (pinned 0.8.103, 4 workers): 25 s wall for 7.83 s.
