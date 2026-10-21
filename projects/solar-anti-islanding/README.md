# Film 36 · Why Do Most Rooftop Solar Systems Stop Working During a Power Cut?

Roadmap film 36 (`config/roadmap-180s.yaml`), a 180-second explainer (PLAYBOOK §4a-9).
- **Narration:** English. The VO went through 9 text audience reviews and 1 audio review, and v10 is final (`vo.txt`).
- **Recording:** owner's full take 2, edited with 17 pauses, line 3 at ×0.92 and line 15 spliced: `voice/vo_v10_take2_edit.mp3` (3:26.4, about 162 wpm).
- **Timing:** exact line times are in `align_take2/edit_lines_exact.json`. Everything is timed to these.

**Mechanism:** a grid-tied (on-grid) inverter follows the grid's 50 Hz beat. When the grid goes, it must stop within
2 s (anti-islanding), because a back-fed transformer would turn 230 V into about 11 kV on a line the lineman thinks is dead.
- **Passive detection:** the beat is missing, or the voltage or frequency drifts.
- **Active detection:** the inverter deliberately pushes its frequency off a little. The grid pulls it back; with no grid it drifts and trips.
- **Panels:** with the circuit open, I = 0 and P = 0. The light becomes heat, and the DC wires are still live.
- **Fix:** a hybrid inverter isolates the house from the street first, then the battery forms the beat.

## Art direction (owner, 2026-10-21: "Daylight + blueprint X-ray")
Built from the independent visual panel (`review_visual_suggestions_v1.md`).
- **World: warm daylight, one continuous Indian lane.** Flat RCC roofs with elevated GI panel frames, a black water tank, a
  clothes line, tulsi, a concrete LT pole with cable spaghetti, a double-pole 11 kV distribution transformer, a wall net-meter
  box, a modular switchboard, 3-pin sockets, white ceiling fans. No brands. The camera *travels* roof → wall → meter → pole →
  transformer and never cuts between unrelated diagrams. Flat 2D vector with soft grain and warm light (HyperFrames
  SVG/GSAP), with real footage where the real thing exists.
- **X-ray: dark blueprint** (`blueprint` in `config/brand.yaml`) for every look *inside* a machine: the solar box, the
  relay, the oscilloscope, the transformer coils, the hybrid's transfer switch. Enter with a push-in through the casing and a
  scan-line wipe; exit by pulling back out to the daylight world. The Blender hero shots live here.
- **HUD:** top-left, persistent, `hud.md`. It sits over both modes.
- **Colour code (learned once, same in both modes):** amber `bp_pressure` = DC and sunlight; cyan `bp_signal` = AC and the
  beat; slate `bp_passive` = dead wire; red `bp_fail` = danger, used sparingly; green `bp_verified` = safe or locked.
- **Recurring motif:**
  - **The drummer** is a stylised **dhol icon on the transformer**. Each beat sends a cyan ring down the wire, one ring per crest (shown slowed down).
  - **The dancer** is the **solar box with a small sun badge**.
  - **Scope strip:** two traces, grid and box. "In step" means they overlap.
  - **Journey:** the dhol goes silent at the cut, tests the beat at 1:59, flies to the battery at 2:53, and fades at 3:16.
  - No human drummer or dancer characters.
- **"What if" scenes** (1:19–1:36) get a dashed frame border, desaturation and a `WHAT IF` tag. The endangered lineman stays
  stylised and **freezes before contact**: never a shock, sparks on a body or a fall.
- **Honest physics (Arjun's list):**
  - DC is a flat line; AC charges jiggle in place.
  - 50 Hz is always shown slowed, with a `SLOWED DOWN` tag.
  - The step-up goes LT → HT.
  - No current after the box is off.
  - The net meter is a digital bidirectional one.
  - No panel voltage number; the label is "STILL LIVE".
  - No real settings menu or steps for disabling protection.
- **Real footage (stock, licensed, `ILLUSTRATIVE FOOTAGE` where it could pass as an event):** rooftop panels in harsh sun,
  ceiling fan slowing, a lineman in helmet and gloves on a pole (respectful, no harm), a technician with gloves and a
  multimeter, and a fan spinning back up.
- **Captions** in a slim burned-in band for viewers with the sound off.

## Engines
- **HyperFrames (2D world, X-ray diagrams, HUD, captions):** most of the film.
- **Blender Cycles hero cutaways (3–4 shots):**
  - the 11 kV distribution transformer, LT → HT (1:25);
  - the relay contacts opening inside the solar box (1:42);
  - the hybrid's transfer switch opening its grid side (2:49);
  - optionally the home inverter and tubular battery (0:21).
- **Three.js:** only if a 3D move is needed outside those shots.

Files: `vo.txt` · `hud.md` · `screenplay.md` · `claims.csv` / `fact-check.md` (pending) · `review_*` · `edit_fixes.md` ·
`tools/edit_take.py`.
