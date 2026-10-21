# Independent lookdev review, round 4 (lookdev v4, 2026-10-21)

No-repo session `session_01EXjVbmed6SfvM3zBkwR1kD` (archived), PLAYBOOK §4a-12. Same panel; v4 preview JPGs by raw URL.

**Scores:** premium 6.5 · clarity 7 · Indian authenticity 7 · technical correctness 7.5. Up from 6.5 · 6 · 7 · 6 in round 3.
**Verdict:** "Change first, then build: fix blockers 1–5 … The rest of the look is approved and can be polished during the build."

- **Arjun:** "Mostly correct, and better than most of YouTube."
  - The H-bridge diagonal pairs, the filter inductor, the relay before the point of common coupling, the sensing tap on the grid side, the house junction outside the box, and DC flowing while AC jiggles: all correct.
  - Wrong: the chip lines have no direction, the dhol's zigzag reads as a resistor, and the world beat needs a slowed-down tag.
- **Suresh:** the DP, the 11 kV insulators, the danger plate and the DB placement are "how our installers do it".
  - The transformer still reads as a flat box at phone size.
  - Earthing (green-yellow earth wires, earth pit, lightning arrester) is missing.
  - The danger plate should be bilingual.
- **Lakshmi:** the X-ray is "like a good blackboard drawing … the flow goes from left to right". She also noticed that the HUD ghosted to 25% looks like a bug.

## Blockers → what v5 does
1. **The dhol is redrawn:**
   - a wooden barrel with darker bands;
   - V-shaped rope lacing in triangles between two cream skins;
   - a curved stick;
   - on each beat: the skins flash white for 3 frames, the badge pulses to 108%, and the leader ends with a dot on the 11 kV conductors.
2. **The X-ray grid icon** is the same round GRID dhol badge, pulsing on each beat.
3. **Direction on the chip lines:** the blue sensing line gets an arrowhead *into* the chip with blue pulses flowing in, and the white command lines get arrowheads *out* to the D.C.→A.C. block and the safety switch with pulses flowing out.
4. **Type hierarchy:**
   - X-ray title 52 px, component labels 42 px, note 34 px (1080p).
   - "SAFETY / SWITCH" on two lines, inside the frame.
   - The world's "11 kV / 433 V" label is removed (not in the VO).
   - NET METER at 26 px, GRID at 34 px.
5. **The beat ring** is 2× the size with a glow, the wires flash at ≥ 70%, and a "SLOWED DOWN" tag sits under the dhol badge.

## Polish → scene build (logged, not blocking)
- Transformer tank detail readable at phone size.
- Earthing (green-yellow), an earth pit, and a lightning-arrester spike.
- A bilingual danger plate (needs Devanagari/Telugu fonts).
- Inverter LCD "50.0 Hz".
- Sun-badge eyes only on the dancer lines.
- A full match-cut, with cables straightening into the schematic lines.
- Props out of the caption band.
- The HUD at full strength in the X-ray, not ghosted. v5 already does this.
