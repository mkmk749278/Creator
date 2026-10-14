# C8_dry_kaveri: The Dry Kaveri

Session C scene for *The Jet Engine Paradox* (program 427.07–437.66, 10.59 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1lrn39m92Zn_b4yK6f4DDebVQc2OCowDn/view

J072: the Kaveri half-section (same drawing as C4) re-inks; at 0.7 s ("took out the afterburner") the afterburner
section flashes red, a red cut line marks the turbine exit, and the whole afterburner and con-di nozzle slide off aft
and fade (0.85–2.4 s). A short fixed nozzle draws in (2.1–2.9 s) and the camera re-centres on the shorter engine.
Label `DRY KAVERI · NO AFTERBURNER` at 3.6 s. J073: the engine rises, a precision thrust bar (0–60 kN, ticks every
2 kN, numbers every 10) draws in at 5.2 s with a dashed white target line at 46 kN (`TARGET`); 6.8–8.3 s the amber
fill grows past the target line to 48.5 kN with a counting readout ending `~48.5 kN`; label switches to
`~48.5 kN · TARGET 46 kN` at 8.4 s.

Cues (word times estimated by character position):
- +0.15–4.56 J072: “GTRE took out the afterburner and made a simpler version. The Dry Kaveri.”
- +5.13–10.29 J073: “In tests in Russia, it gave about forty eight kilonewtons of push, a little more than its target.”

## Parameters (`params.js`)
`label1`, `label2`, `targetWord`, `target` (46), `value` (48.5), `scaleMax` (60) and the beat times.

## Notes
- Citation tag [ORF | THE WEEK | 2026], ILLUSTRATION tag and logo bug come from the assembler; both right corners
  are clear. The readout counts up while the bar fills (intermediate values are the animation, the final value is
  the spec's ~48.5 kN). `TARGET` marks the dashed line (spec wording).
- Labels with units use `.keepcase` so `kN` is not upper-cased.
- Render (pinned 0.8.103, 4 workers): 31 s wall for 10.59 s.
