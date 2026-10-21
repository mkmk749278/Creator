# Independent lookdev review, round 2 (lookdev v2, 2026-10-21)

No-repo session `session_019jAWgph89xvNxxjG8v12Ph` (archived), PLAYBOOK §4a-12. Same seven-person panel as round 1.
It got the four v2 preview JPGs (`qa/lookdev2_*.jpg`) by raw URL and was not told about round 1.

**Scores:** premium 6 · clarity 6 · Indian authenticity 7.5 · technical correctness 6.5.
**Verdict:** "Change first, then build. The style and colour code are right. Fix text size, the inverter shape, the
beat's visibility, and the wiggling-wire and missing control-line errors, then lock the look."

- **Suresh (DISCOM):** the DP structure is "surprisingly right" (AB switch and handle, HG fuses, porcelain bushings, conservator, LT box, the service-cable mess).
  - The danger plate should be enamel with a skull and crossbones and the voltage.
  - The panels float.
  - The inverter reads as a chip.
  - The drum on the transformer implies the transformer makes the 50 Hz. The grid does.
- **Arjun:** the output wire drawn as a sine is the "electricity is a wiggly rope" misconception. The chip must also drive the bridge.
- **Fatima:** the ring is lost on a phone. Flash the whole wire, and let the badge jump.
- **Meera:**
  - "Good bones."
  - Flat lighting, with no contact shadows or depth layers.
  - Four text blocks plus five labels in the world shot.
  - The sun sits behind the title chip.
- **Ramesh, Lakshmi:** DCDB/ACDB/EXP and the small text are unreadable. The X-ray socket looks like a surprised face.

## Top 10 (ranked) → what v3 does
1. **Bigger text everywhere:** captions 52 px, HUD 34 px, X-ray labels 34 px, corner tag 24 px (all at 1080p).
2. **The solar box redrawn as a real inverter:** no side pins; ribbed fin blocks on both sides, an LCD, and glands with cables at the bottom. The sun badge stays.
3. **A visible beat:**
   - each hit gives a 15% squash and a white flash;
   - the LT and service cores flash bright blue;
   - the ring is 2× bigger;
   - the badge bounces 12 px.
4. **X-ray AC on a straight wire with travelling blue pulses.** The sine stays only in the scope.
5. **Control line chip → D.C.→A.C. block.** The label is "WATCHES THE GRID" (an eye, so the label matches the icon). The sensing dashes flow into the chip.
6. **The push matches the X-ray:** a dashed outline draws on over the casing before the wipe (the casing and frame have the same aspect, 0.857), and a beat pulse runs up the sensing line just after the cut.
7. **Declutter:** the DRUMMER · DANCER chip is dropped (the caption says it), and the HUD dims during the X-ray.
8. **Hardware:**
   - an enamel skull-and-crossbones DANGER · 11000 V plate;
   - a GI elevated frame under the panels;
   - an Indian 3-pin socket (big earth hole on top) with a switch;
   - the H-bridge drawn as four switch symbols;
   - a 3×2 panel icon.
9. **The dhol moves to the 11 kV line coming from the horizon, tagged GRID.** The beat travels HT → DP → LT → service → meter. This matches the VO ("Think of the grid as a drummer").
10. **Polish:** contact shadows under every box, and a skyline parallax layer.

The X-ray diagram stays at its scale. Its frame has to match the pushed-in box exactly, so the scope stays where it is.

**Not taken:** hiding the HUD in the X-ray. The persistent HUD is a format rule (§4a-9), so it only dims.
