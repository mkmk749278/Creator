# Rare earth magnets: cut review (PLAYBOOK §14)

## Cut 1 (2026-10-22): 1080p preview, 636 s
Method: a contact sheet of every 5 s (`qa/cut1/sheet-01..15.jpg`, 127 frames) plus full-size frames wherever something looked wrong.

| # | Time | Problem | Fix in cut 2 |
|---|------|---------|--------------|
| 1 | 0:05.6–0:08.4 | Chetak shot fades to black (source cross-fade at 138 s): the VO says "half the scooters" over a dark screen | In-point moved to 132 s (headlamp fitting, assembly line) |
| 2 | 0:21 | "−47%" chip covers the last digit of 10,824 | Chip moved right |
| 3 | 0:40.5 | "3 THINGS" sits alone on the blueprint grid (looks like a slide) | Beach aerial behind it (our sand) |
| 4 | 0:51 | Calendar with "?", which breaks the rule against question-mark graphics | Shows the real date, NOV 10 |
| 5 | 0:58–1:02 | IRON / BORON / NEODYMIUM in grey text on a white background, hard to read; faint burned-in source title | Chips with a backing; crop from the bottom |
| 6 | 3:06–3:20, 4:14 | BMAG clips have burned-in captions (JET MILLING, PRESSING, MAGNETIZATION) under ours, plus the BMAG logo | Crop from the top-right corner (origin 100% 0%) hides both |
| 7 | 2:48–3:03 | JDA clip has a logo at the top and subtitles at the bottom. Cropping the top shows the subtitles, so the crop stays at the top | Our labels moved below the logo; the logo stays as the credit (tag FOOTAGE · JDA MAGNET) |
| 8 | 3:44 | Deng quote overlaps the map's INDIA pin and the caption | Quote moved to the top |
| 9 | 7:14–7:26, 8:10–8:19 | Chips cover the document headlines | Chips moved down over the document body |
| 10 | 8:19.5 | "WINNERS: NOT YET" on an empty grid | Over factory footage (Pixabay 40054) |
| 11 | 8:51 | Empty frame for 2.7 s ("Let me be honest…") | "THE HONEST TIMELINE" label; the BUILD bar starts 0.9 s earlier |
| 12 | 10:10–10:18 | "NEXT: MEDICINES" and "WHICH PIECE NEXT?" on an empty grid | Over the pills still (the end-card image) |
| 13 | Mix | −15.9 LUFS: loudnorm's linear mode backed off because of the true-peak ceiling | Static gain to −14 LUFS + limiter at −1.5 dBTP, measured twice (`build/assemble.sh`) |

Checked and fine:
- The 0:00 frame shows the thumbnail subject (magnet on black sand).
- Lede within 25 s: Pune output halved, one magnet.
- Open loop names "about five minutes in", and the thorium reveal lands at 5:02. True.
- No logo or welcome inside the film; the channel is named only at the end.
- Every number on screen matches the VO and claims.csv.
- Maps are land only.
- Every stand-in is tagged "ILLUSTRATION", "ILLUSTRATIVE" or "PIXABAY".

Left as is:
- The A CHAIN, chain, tiles and bar scenes are on the moving blueprint grid. They are animation, not still text.
- The JDA logo stays as the credit.

## Facts re-checked before delivery (2026-10-22)
- China's hold on the October 2025 rules still ends **10 Nov 2026** on paper. The US–China arrangements are extended to 10 Jan 2027, and there is no rare-earth-specific extension yet. The VO ("set to end on November tenth… trade deal till January") still holds.
- REPM scheme: 20 bids (Aug 2026), no winners announced. "Still to be announced" holds.

## Cut 3 (2026-10-22): v5 voice (owner's notes), 11:09
How it was built:
- New takes for blocks 1–4 and 6–8; block 5 kept.
- Sentence alignment: 208 sentences, 5 short ones flagged. Each flagged boundary checked against the silences.
- Shots retimed through `R()` (v4→v5 sentence map). The opening, the magnet recipe, the callbacks, the stairs, the factory steps and the takeaway were re-authored in v5 time.
- Every remaining shot boundary is within 0.35 s of a sentence start, or on a clause by design.
- Siblings sync re-checked: the sphere leaves 0.15 s after "pull one of them out".

Seen on the 5 s sheets (`qa/cut3`), all fine:
- The new opening (Nokia teardown photo, vibration-motor cutaway, Ather and Nexon spec sheets, hub motor, Chetak line).
- The stairs replacing the rice.
- The factory steps under their clauses.

Fixed after the sheets (in the next render):
- An empty grid for 2.5 s at 4:00 → "Not one factory" chip.
- "Hold" → "Pause" on the timeline tick and the closing calendar label, to match the v5 VO.

Open:
- **Open loop:** "about five minutes in", but thorium is now at **5:41** (the section starts at 5:19). The fix is a one-sentence pickup from the owner: "Then, about six minutes in, the secret inside our sand that kept it locked away."
- **Lede:** the Pune event is at 0:30, later than the 25 s guide. This is the owner's call: they asked for the familiar opening first. The magnet is on screen from 0:00, and India is named at 0:25.

Mix: −14.2 LUFS, sample peak −0.9 dBFS.

## Cut 4 (2026-10-22): final candidate, 11:09
- **Open loop closed.** The owner recorded the pickup "Then, about six minutes in…". It is spliced into block 1 over the old sentence, at the same length:
  - pickup 4% faster (inaudible), its mid pause shortened;
  - lead-in pause 0.37 s, as in the original take;
  - every later timing unchanged (silences checked against the original take).
  - Thorium is at 5:41; the chip reads "~6 MIN IN".
- **Fixes from cut 3, verified on frames:**
  - "Not one factory" chip over the empty grid at 4:00;
  - "Paused · 1 year" on the timeline;
  - "Pause ends, or stretched?" on the closing calendar.
- **Mix:** −14.1 LUFS, sample peak −0.5 dBFS (YouTube turns it down, not up).
- **Lede:** still at 0:30 by the owner's choice (see cut 3).

## Cut 5 (2026-10-22): independent review (separate cloud session, read-only) and fixes, native 4K
Verdict was "not ready". Fixed:

**Broken or mismatched frames**
- **5:38 blue channel wipe (Manorama):** replaced by TNM dark beach plus Manorama sand, both before the wipe.
- **4:42 auto-show car (Reuters cut inside the shot):** replaced by two smokestack pieces (13.0 s and 37.0 s).
- **End card:** the baked-in tile for the unreleased next film is removed. The YouTube end-screen area is left free.
- **0:38 empty grid:** dimmed welding sparks on the Chetak line now sit behind Strike/Batteries.
- **Pixabay jetty (twice):** replaced.
  - 5:22: the Kerala coast, then the TNM reporter holding black sand ("What's inside our sand").
  - 8:06: the Vizag plant aerial ("Not at all").

**Maps**
- India map lifted above the caption band, so Kerala and Tamil Nadu are no longer hidden.
- Pins appear in the VO's order; the corridor zones follow the VO's order.
- `map_china` (no Japan pin or arc) is used at 0:42 and 4:16–4:30. Japan appears only with the Japan deal.

**Numbers and wording on screen**
- The counter reads "~₹7,300 crore", matching the VO (the exact ₹7,280 crore stays in claims.csv).
- "Samarium-cobalt" → "Heat-proof magnet", matching the VO.

**Captions**
- At most two lines. The caption box was capped at half the frame by `left:50%`, so it now uses `width:max-content` (≤1500 px).
- Parts over 96 characters are split into two events.

**Documents**
- Ather spec: tight crop on the PMSM sentence.
- Technology.org: headline, then the key-takeaway bullets. The coin-cell photo is gone.
- Chips moved off the headlines.

**Labels**
- JDA labels moved below the source logo.
- 2:34 chips in reading order.

**Grid stretches → dimmed real footage** (`dim=` on video shots):
- the chain intro over the BMAG line (dim 0.78);
- the IEA bars over the Baotou mine;
- the light/heavy tiles over Kerala beach mining (TNM);
- April 2025 over the Baotou chimney skyline (Sky);
- 6,000 t/year over the Vizag aerial.

**Not changed**
- **Narration (locked):** the review's pacing notes (process recital, numbers barrage) are kept for the next script.
- **MEA spokesperson name tag:** not added, because the identity is unverified.
- **Package:** the review's title, chapters 7:01 and 10:05, and thumbnail E2 (E rebuilt with its notes).

**Master:** native 4K via `build/render_parts_4k.sh` (`make_native_4k.mjs`, never `--resolution 4k`).
