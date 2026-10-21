# Why Do Most Rooftop Solar Systems Stop Working During a Power Cut?

Roadmap film 36 (`config/roadmap-180s.yaml`), 180-second explainer (PLAYBOOK §4a-9). Phase 1: narration.
VO: `vo.txt` (380 words, about 2:32 at 150 wpm). `scripts/spoken_english_check.py` passes.
Status: draft. Not yet fact-checked (`claims.csv`) or audience-reviewed (§4a-11).

## Viewer's three questions
1. My roof is in full sun. Why does my solar stop when the power goes?
2. Where does all that sunlight go? Is it hurting my panels?
3. What do I buy so the fans stay on?

## Corrections to the brief
| Brief said | What the sources say | What the script does |
|---|---|---|
| The relay trips within 20 ms | IEEE 1547-2018 cl. 8.1.1: detect the island and stop within **2 s** (5 s if the utility agrees). IEC 62116 tests inverters against the same 2 s limit. | VO says "two seconds, at most". 20 ms is **one 50 Hz cycle**, so the HUD shows it as the length of one beat. |
| `[...]` pause tags | §4a-9 rule 7 and §4a-10: no bracket tags in English VO, because Akash may read them aloud | `...` gives a 300–500 ms pause, a spaced ` — ` gives a short stop before a number, and each beat is on its own line |
| The inverter needs the grid reference | True for grid-following inverters (PLL lock), but a balanced island can keep running. That's why active detection exists. | Beat 11 covers this: the inverter pushes its own frequency off a little on purpose, and with no grid it keeps drifting and trips |
| The fix is a hybrid inverter with an ATS | The transfer switch **opens the grid side first**, then the battery-backed inverter forms its own voltage (grid-forming). Anti-islanding still applies on the grid side. | Beat 15: "first cuts your house off from the street. Then the battery becomes the drummer" |

## Claims to source before Phase 2 (fact-check, §12)
- C1 Anti-islanding stops within 2 s at most: IEEE 1547-2018 cl. 8.1.1 (secondary sources so far, ISO-NE and CIGRE). Still needed: the CEA DG connectivity regulations (2013, amended 2019) clause, and IS 16169 (Indian adoption of IEC 62116).
- C2 CEA rules forbid intentional islanding of grid-tied rooftop inverters: Bridge to India, secondary. Need the CEA text.
- C3 A back-fed distribution transformer steps 230 V (phase) / 433 V up to about 11 kV: DISCOM LT/HT network spec.
- C4 "Many" inverters use active frequency-shift detection (Sandia SFS, AFD): Sandia/NREL report.
- C5 Open circuit means I = 0, so P = V × I = 0 W. Panels at Voc are within their rating, and the unextracted energy becomes heat: module datasheet plus an NREL note.
- C6 The hybrid opens its grid relay before forming its own voltage: two hybrid inverter manuals (switchover time goes on the HUD only, labelled from the manual).

## Beat sheet (times from 150 wpm; re-time on the real VO with `align_script.py`)
Colour key, from `blueprint` in brand.yaml: amber = sun and heat, cyan = current, orange = fault, green = verified state.

| # | Time | Phase | VO (first words) | Visual anchor | On-screen text (≤ 3 words) | HUD (top left) | SFX / music |
|---|---|---|---|---|---|---|---|
| 1 | 0:00 | Hook | "Two in the afternoon…" | Real footage: a rooftop array in harsh sun, heat shimmer. Cut to a ceiling fan slowing to a stop | `2:00 PM · 41°C` | `IRRADIANCE 1000 W/m²` (ILLUSTRATIVE), `GRID 230 V · 50.0 Hz` → `0 V` on "goes" | Fan hum dies; a soft relay click on "goes" |
| 2 | 0:05 | Hook | "Your panels are full of power…" | Close-up of the inverter LED going from green to red (real footage) | `FULL SUN. ZERO POWER.` | `PV OUTPUT 0 W` | Room silence |
| 3 | 0:10 | Promise | "Strange, right?…" | Push-in through the inverter case into a blueprint cutaway | – | – | Low pulse starts |
| 4 | 0:17 | Constraint | "Your inverter has one job…" | Cross-section: PV string → DC bus → H-bridge → AC out, with cyan DC dots becoming a sine | `DC → AC` | `DC BUS ~360 V` (ILLUSTRATIVE) · `AC 230 V 50 Hz` | – |
| 5 | 0:26 | Constraint | "But it can't make that beat…" | Grid sine as a drum; inverter sine phase-locked on top of it (two traces, one phase) | `PHASE LOCKED` | `PLL LOCK ✓` (green) | One kick drum per beat, slowed |
| 6 | 0:36 | Rest | "Fifty times a second…" | Magnifier on one cycle with a 20 ms bracket | `ONE BEAT` | `CYCLE 20 ms` | Tick on each cycle |
| 7 | 0:44 | Rest | "Your house takes what it needs…" | Isometric street: house → net meter → service wire → pole transformer, with cyan flow outward | `EXPORT` | `EXPORT +1.8 kW` (ILLUSTRATIVE) | Light hum |
| 8 | 0:54 | Stress | "Now the power company cuts your line." | Substation breaker opens (real footage if found); the street grid goes slate grey | `GRID DOWN` | `GRID 0 V` (orange) | **1.5 s of music silence**, then a low thud |
| 9 | 0:57 | Stress | "Here's the catch…" | Ghost flow: cyan reverses up the service wire, the pole transformer glows, and the HT side counts up to 11 kV. A lineman's gloved hand reaches toward the wire (real footage, ILLUSTRATIVE FOOTAGE) | `BACK-FEED` · `≈ 11 kV` | `HT SIDE 0 → 11,000 V` (orange) | Rising hum to the cut |
| 10 | 1:14 | Stress | "So the inverter is built to notice…" | Inside the inverter: the detector sees the missing beat, the gate pulses stop, the relay contacts spring open | `RELAY OPEN` | `TRIP ≤ 2 s` (IEEE 1547) · `I = 0 A` | Hard relay click on "click" |
| 11 | 1:26 | Edge case | "What if your house uses exactly…" | Balanced island: load = PV. The inverter sine slides off 50 Hz. With grid present it snaps back; with no grid it drifts to the limit | `ACTIVE DETECTION` | `f 50.0 → 50.6 Hz` → `TRIP` (ILLUSTRATIVE) | Detuning tone |
| 12 | 1:41 | Edge case | "So what happens to your panels?…" | Panel I-V curve: the operating dot slides from the MPP to Voc on the voltage axis; the current bar falls to 0 | `P = V × I` (animated, never written as a sum) | `V = Voc` · `I = 0 A` · `P = 0 W` | – |
| 13 | 1:51 | Edge case | "The sunlight still lands…" | Macro of a cell with amber photons turning to heat shimmer | `HEAT, NOT HARM` | `CELL TEMP ↑` (ILLUSTRATIVE) | Soft wind |
| 14 | 1:58 | Fix | "So how do you keep your fans on?…" | Hybrid inverter + LFP battery cutaway (real reference photos first) | `HYBRID + BATTERY` | – | Music lifts |
| 15 | 2:04 | Fix | "When the grid dies, a switch inside…" | Transfer switch: the grid contact opens first (orange X on the street side), then the battery forms the sine and the PV locks to it. Fan restarts (real footage) | `ISLAND, SEALED` | `GRID ✕` · `BATTERY → 230 V 50 Hz` (green) | Two clicks, then fan hum returns |
| 16 | 2:15 | Rule | "Here's the rule…" | Back to the on-grid cutaway with the relay open | `RULE` | – | – |
| 17 | 2:21 | Ruin | "Break it…" | The lineman's hand on the wire, frozen (no shock shown) | `RUIN` | – | Low braam |
| 18 | 2:26 | Reality | "Your solar never failed…" | The drummer/dancer sines, the drum trace flat | `REALITY` | – | Silence, one beat |
| 19 | 2:30 | Bridge | "But when the grid is live…" | End screen: the H-bridge MOSFETs glowing (next film), logo end card under live VO | `NEXT: THE INVERTER` | – | Outro bed |

## Recording blocks (Akash, Eleven v4: stability 0.65, similarity 0.85, style 0.15, speaker boost on)
Block 1 → `voice/vo_01.mp3`: beats 1–10 (1,103 characters). Block 2 → `voice/vo_02.mp3`: beats 11–19 (948 characters).
The text is in `vo.txt`, split at "What if your house uses exactly…".
