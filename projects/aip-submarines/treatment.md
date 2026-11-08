# Treatment notes · Why India's Submarines Must Surface

Decisions made while building the picture (2026-11-06), with the reason for each.

- **The patrol strip is the film's motif.** A strip of time with red marks (the hours a boat must snorkel) appears
  at S50 and comes back at S54–55 (fewer, shorter), S62 (four days becomes fourteen), S72 (what AIP buys) and S177,
  where its last red mark goes out ("the mast stays down"). One picture carries the whole argument about exposure, so
  the viewer never needs a number to follow it.
- **No fake headlines.** The plan had a "headline wall" for "ghost maker" and "invisible". We have no licensed
  screenshots of real headlines, and drawing made-up ones would fabricate a record. Instead, the boat itself fades to
  a ghost and vanishes while the words appear as quotations ("ONLINE", "HEADLINES").
- **H2 (the battery cutaway) is a Remotion drawing on the steel plate, not a Blender render.** The real internal
  layout is not public, so the shot is labelled SIMPLIFIED. A flat, labelled drawing is more honest than a
  photoreal render of a layout we invented, and every system lights on its own word. The Blender budget went to the
  three shots that carry the story: H1 (the mast at night, and its reprise where the mast stays down), H3 (the powder
  and water) and H4 (the hull cut open and the new section rolling in).
- **H1's mast breaks the surface on "a thin steel mast"** rather than on "rises". The render's rise starts 1.2 s
  earlier than planned; the edit starts it on "Raise" and lets the mast appear while its own words are spoken.
- **The P-8I footage is vertical** (the Navy's own short). It sits in a frame on its own blurred fill rather than being
  stretched or cropped to a sliver.
- **Pakistan and China get two factual labels on a map.** No threat music, no red, no warship graphics (plan §8).
- **The end card holds 4.5 s after the last word** (`vo_lock.py --outro 4.5`): the voice ends on "bottom of the
  ocean", and the logo is the only branding in the film.
- **Long holds are reframed automatically.** Any shot over 4.5 s is split into framings about 4 s long, with an eased
  18-frame camera move between them (`Film.tsx` `Reframe`), so no framing is held for more than 5 s.

## Lessons for the playbook
- esbuild resolves `../brand` to `Brand.tsx` on a case-insensitive match; film code imports the map projection from
  `indiaGeo.ts` directly rather than through `IndiaMap.tsx`.
- NASA's `eoimages.gsfc.nasa.gov` resets connections from the cloud; the same Blue Marble tiles download from
  `assets.science.nasa.gov/content/dam/science/esd/eo/images/bmng/...`.

## The package (2026-11-08)
- **Title:** "Why India Has to Cut Its Own Submarine in Two" (the film's own words at 0:52, the chapter at 5:02). The
  film predates the promise-first rule: its sentence 1 is the battery running out, so the package confirms 0:52, not
  sentence 1. "Why India's Submarines Must Surface" (which sentence 1 confirms) is kept as the title test.
- **Thumbnail, round 3** after the owner's review: our dry-dock boat cut in half with the new AIP section in the gap,
  cut away and glowing; words CUT IN HALF (the film's chapter name). Challengers: WHAT'S INSIDE? (same scene, tighter)
  and CAN'T STAY HIDDEN (the night snorkel with radar rings). "THE 10M SECRET" was dropped: the plug is public.
