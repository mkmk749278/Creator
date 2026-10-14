# C9_amca_engines: AMCA, F414 now, 120 kN later

Session C scene for *The Jet Engine Paradox* (program 461.63–473.87, 12.24 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/19v1festa7_f99l7tVoRORpNBxXgGaIrZ/view

J078: a generic twin-engine stealth fighter (AMCA-like planform: chined faceted body, caret intakes, trapezoid wing,
canted twin fins) draws itself in a near plan view (0.1–2.3 s); two engines draw into the bays in white (1.4–2.7 s)
with a two-line leader `GE F414`; label `AMCA MK1 · GE F414` at 0.8 s. J079: at 4.4 s ("For later jets") the white
engines dissolve into embers; the camera swings and pushes in while a clean-sheet engine draws itself into both bays
in hot amber (5.6–8.0 s) and starts to glow. Label `AMCA MK2 · 120 kN CLASS` at 7.3 s, with the line
`INDIAN DESIGN, INDIAN RIGHTS` unfolding under it at 10.85 s ("own the design").

Cues (word times estimated by character position):
- +0.15–3.95 J078: “The first AMCA jets will use GE's F four one four engine.”
- +4.34–12.02 J079: “For later jets, India wants a new engine of about one hundred and twenty kilonewtons. And this time, it wants to own the design.”

## Parameters (`params.js`): all on-screen words and the beat times.

## Notes
- ILLUSTRATION tag and logo bug come from the assembler; both right corners are clear.
- The airframe is procedural and generic (`BP.stealth()`), not a copy of an ADA drawing; the "clean-sheet engine" is a
  generic engine block (no real design is implied).
- Rendered length 368 frames (12.267 s; spec 12.24 s = 367.2 frames, within one frame).
- Render (pinned 0.8.103, 4 workers): 38 s wall for 12.24 s.
