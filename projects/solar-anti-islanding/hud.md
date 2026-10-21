# Film 36 · Telemetry HUD spec (Block 1)

**Layout and style:**
- Top-left, on a `bp_panel` scrim at 85% opacity, monospace numbers in `bp_readout`, labels ≤ 3 words, at most 4 rows
  visible at once. A row pops in only when the VO first needs it.
- It sits over both the daylight world and the X-ray.
- Logo bug top-right; citation tags bottom-right.

**Change timing:** every value changes on its cue word (`screenplay.md`, times from `align_take2/edit_lines_exact.json`).

| Readout | Unit | Normal | Stressed | Colour | Cue | Source / label |
|---|---|---|---|---|---|---|
| GRID | V · Hz | `230 V · 50.0 Hz` | `0 V · — ` at the cut (0:04.5 "power cut", again 1:16 "switches off the supply") | cyan → slate | L1, L9 | claims: 230 V, 50 Hz |
| SUN | W/m² | `≈ 1000 W/m²` | stays (the paradox) | amber | L1 | ILLUSTRATIVE |
| SOLAR BOX | state | `IN STEP ✓` | `TRIPPED` at each click (0:10, 1:45, 2:19); `WATCHING` in the X-ray | green / red / cyan | L2, L12, L16 | anti-islanding |
| TRIP TIMER | s | — | `0.0 → TRIP` stops before 2.0 with `≤ 2 s LIMIT` | `bp_readout`, limit `bp_fail` | L12 | CEA reg. 11(6)(e) first, then IEEE 1547 / IS 16169 (claims) |
| BOX FREQ | Hz | `50.0` (follows the grid) | balanced case: `50.0 → 50.2 → 50.4` → `TRIP` at the **50.5 Hz** line (CEA 11(6)(b)) | cyan → red | L14–L16 | values ILLUSTRATIVE (method from the claims) |
| EXPORT | kW | `+1.2 kW` (extra to the street) | `0.0` at the transformer, balanced street | amber | L8, L13 | ILLUSTRATIVE |
| PANEL | I · P | `I > 0 · P > 0` | `I = 0 A · P = 0 W` | amber → slate | L17 | claims: open circuit |
| LINE (what-if) | V | — | `230 V → ≈ 11,000 V` (`11 kV LINE`; no exact counter landing) | `bp_fail`, dashed what-if frame | L11 | claims: 11 kV distribution |
| BACKUP | source | — | `GRID ✕ · BATTERY → 230 V 50 Hz` | slate ✕ / green | L20 | hybrid claim |

**Rules:**
- Nothing on the HUD contradicts the VO, and every number is either in `claims.csv` or marked with an `ILLUSTRATIVE` chip under the panel.
- 50 Hz motion on screen always carries a `SLOWED DOWN` tag.
- The HUD fades to a single GRID row during the real-footage hook (0:00–0:15) so the paradox shot stays clean.
