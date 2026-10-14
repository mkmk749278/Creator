# Session C shared code: the blueprint world

- `_bp.js`: Canvas 2D renderer with a real perspective camera (`BP.camera`), stroke-by-stroke drawing with hot pen tips
  (`BP.draw`, `BP.seq`), drafting paper + parallax grid + lamp light + two-level bloom + dust + animated grain
  (`BP.Stage`), dimension lines and construction lines, and four generic, procedural drawings reused across scenes:
  `BP.fighter()` (single-engine tailless delta light fighter, empty engine bay), `BP.stealth()` (twin-engine stealth
  fighter, AMCA-like planform), `BP.engineBlock(bay)` (3D engine to drop into a bay) and `BP.engineSection()`
  (twin-spool afterburning turbofan half-section, GTX-35VS-style layout, with revolved station rings for depth).
  Everything is a pure function of time (seeded hashes only). None of it is traced from a maker's drawing.
- `_c.css`: shared layout (photo slot, vignette, leader labels, stamps). Tokens from `../_shared/jep.css`.
- `sync.sh`: copies `_bp.js`, `_c.css` and `jep.css` into every `C*_*` scene folder. Run it after editing here.
