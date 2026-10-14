# C4_kaveri_blueprint: 1986, planning an engine

Session C scene for *The Jet Engine Paradox* (program 178.54–183.25, 4.71 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1TTA3Pw_02QDvX8kswoaCp37Vb0CSIDvA/view

A drafting-table blueprint: a generic twin-spool afterburning turbofan half-section (GTX-35VS-style layout: 3-stage
fan, 6-stage HP compressor, annular combustor, one HP and one LP turbine stage, afterburner with V-gutters, con-di
nozzle) draws itself stroke by stroke (0.1–3.5 s): centreline, casing, revolved station rings, fan, compressor,
combustor, turbines, shafts, section hatching, afterburner. Dimension lines follow (3.1–4.2 s); the combustor warms
from 2.4 s. The camera dollies and swings from a 34° three-quarter view toward side-on. Amber stamp
`1986 · GTRE, BENGALURU · PROPOSAL` slams on at 1.1 s (after "nineteen eighty six").

Cue (word times estimated by character position):
- +0.15–4.41 J029: “In nineteen eighty six, Indian engineers began planning their own fighter engine.”

## Parameters (`params.js`): `stamp` (text), `stampAt` (s).

## Notes
- ILLUSTRATION tag and logo bug come from the assembler; both right corners are clear.
- The drawing is generic and procedural (`BP.engineSection()` in `../_c_lib/_bp.js`), not a copy of a GTRE drawing.
- Rendered length 142 frames (4.733 s; spec 4.71 s = 141.3 frames, within one frame).
- Render (pinned 0.8.103, 4 workers): 16 s wall for 4.71 s.
