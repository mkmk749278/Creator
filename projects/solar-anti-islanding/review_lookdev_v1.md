# Independent lookdev review, round 1 (lookdev v1, 2026-10-21)

No-repo session `session_01S2kzs8WHy3xus92kTWRiUM` (archived), per PLAYBOOK §4a-12.
- **Inputs:** four committed preview JPGs (`qa/lookdev_world|push|xray|motion.jpg`) loaded by their raw URLs.
- **Panel:** Priya (21), Ramesh (44), Lakshmi (58), Arjun (30, engineer), Fatima (26, sound off), Meera (35, motion designer) and Suresh (50, DISCOM line engineer, Telangana).

**Verdict: "Change first, then build."** The style is solid and worth keeping. Fixes 1–5 are mandatory.

## What they said, briefly
- **Priya:** the first 3 s barely move, and she'd scroll away. The X-ray looks like a lifeless dashboard. She wants a hard dhol hit, big rings and a fast push.
- **Ramesh:** "D.C. → A.C." and "WATCHING" mean nothing to him. He wants icons (a panel on the left, a socket or bulb on the right) and fewer English labels.
- **Lakshmi:** the image is all beige, like an old photo. The coloured squares read as Tibetan prayer flags, not washing. The sun face is sweet.
- **Arjun:**
  - Nothing feeds the transformer.
  - The LT line is a single wire.
  - The scope shows one teal trace, so "IN STEP" is only a claim.
  - The grid-sensing loop, which is the whole subject, is missing.
  - The relay is a box with a line.
  - The output sine is one static cycle.
- **Fatima:** she can't see a dancer. The drum is small and the rings look like markers. She wants to *see* the beat (a squash, a flash, the badge bobbing).
- **Meera:**
  - There are no depth layers and no foreground.
  - The X-ray is a hard genre switch with no spatial link (a portrait box becomes a landscape rectangle).
  - Two lower-third texts show at once.
  - The logo collides with the sun.
  - The tag collides with the caption.
- **Suresh:** the DP structure is "undressed".
  - Missing: the AB switch (GOS), HG drop-out fuses, lightning arresters, the HT line in, the conservator, the LT distribution box and a danger board.
  - The net meter belongs low, by the door or gate, in a meter box.
  - The DCDB/ACDB are grey windowed enclosures with those labels.

## Top 10 (ranked)
1. **Match-cut transition:**
   - a 0.7 s push until the box fills about 80% of the frame;
   - the casing fades to a wireframe and its outline morphs into the cutaway frame (same centre and aspect);
   - a radial blueprint wipe;
   - the amber cable entry stays in the same screen place.
2. **Two-trace scope:** grid in blue at 4 px, box white or amber dashed at 2 px on top. Start the box trace 30° out of phase, slide it into lock over 0.8 s, then flash "IN STEP ✓" with a click.
3. **Controller "brain" chip and sensing loop:** a chip with an ear icon, a blue sensing line from the grid side of the relay to the chip that pulses on every beat, and the chip driving the relay. Label: "LISTENS TO GRID".
4. **Beat visible with no sound:**
   - the dhol at 1.8× with a clear stick and strap;
   - a squash on each hit (1.0 → 0.85 → 1.05) and a shockwave flash;
   - a 55 px glowing ring emitted at the hit, travelling to the house in about 0.5 s;
   - the sun badge bobs when each ring arrives (the dancer).
5. **Dress the DP structure:**
   - 3 HT conductors coming in;
   - an AB switch with its handle rod;
   - 3 HG fuses and 3 lightning arresters;
   - the conservator, HT bushings and radiator fins;
   - an LT distribution box;
   - a "DANGER 11000 V" board.
   The dhol floats beside the top crossarm, clear of the HT line.
6. **LT line and service routing:**
   - a PSC pole with 4 bare conductors (or an ABC bundle) running off frame right, not under the HUD;
   - a live line with a subtle blue core that goes grey at the cut;
   - the service drop to a wall bracket, then down to a ground-floor meter box by the door, with a red pulse LED and a green EXP.
7. **DCDB/ACDB wired in and labelled** (grey, windowed). Amber runs roof → DCDB → inverter, and blue runs inverter → ACDB → meter. The inverter gets heat-sink fins and cable glands.
8. **Text hierarchy:**
   - captions at 28–30 px (at 720p) on one line;
   - the chip dropped, or moved to a 1.5 s top-centre title;
   - labels at least 18 px (720p) on dark chips;
   - X-ray labels in #C9D1D9;
   - "ILLUSTRATIVE" dropped from the HUD;
   - "ILLUSTRATION · SLOWED DOWN" moved under the logo, shown only when needed;
   - one HUD vocabulary: IN STEP / LISTENING / OFF;
   - the HUD at 70% opacity, flashing only the row that changes.
9. **More Indian, with depth:**
   - clothes on the line (saree, shirt, towel);
   - chajjas and grills on the windows;
   - a stair mumty and a DTH dish;
   - 6–8 panels with a cell texture and a glint;
   - a foreground parallax layer (compound wall and gate, a parked scooter, a blurred neem branch).
10. **Grade and pacing:**
    - a warm blue → peach sky, saturation +15%, a darker street;
    - nothing still for more than 1 s, with the first hit at frame 0;
    - the AC sine travels through the relay to a socket icon;
    - the relay drawn as a lever switch;
    - the logo circle kept in every scene.

## Decisions
- **Take all ten.** One change: the X-ray background stays the brand's `bp_bg` (#0d1117, `config/brand.yaml`, a channel rule) with a slight navy lift in the grid. We don't switch to #0B1B2E.
- **The box trace is white dashed (`bp_readout`), not amber:** amber means DC in our colour code.
- **The "ILLUSTRATIVE" chip leaves the HUD:** illustrative values get the small corner tag only when they're on screen. The HUD rule still applies (every number is in `claims.csv` or tagged).
- **The danger board** uses generic text "DANGER · 11000 V" with a skull icon. No utility name.
