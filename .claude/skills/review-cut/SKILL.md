---
name: review-cut
description: Review a rendered documentary cut before anyone sees it - measured checks (flash, freeze, judder, shot lengths, seams, loudness), the shot-word audit, frames against the audio, legibility at 480p and a creative pass - and write review.md. Use after every render.
---

# Review a cut

Checklist and reasons: PLAYBOOK §13. Review at `high` effort or above.

1. **Measure every frame:** flash frames (darker than 45% of both neighbours; 1–9-frame shots at cuts), frozen holds
   (`freezedetect=n=0.002:d=1.5` at 480p), judder (repeated frames with `tblend` difference), shot lengths (none over
   5 s), part seams, loudness (`ebur128`: −14 LUFS ±1, −1 dBTP), picture and audio lengths.
2. **Shot-word audit:** every shot with its words and one frame, graded WRONG / WEAK / OK. Names, places, years and
   verbs need their own picture.
3. **Frames against the audio:** `python3 scripts/contact_sheet.py <cut.mp4> --out <qa> --every 1` (or one frame per
   second with the words heard); read every sheet at 480p size for legibility, empty or covered frames, labels, the
   void, stock repeats, foreign stand-ins and on-screen numbers against the voice.
4. **A creative pass** over the whole film: what would make each weak moment unforgettable?
5. Write `projects/<slug>/review/review.md` (issue → time/shot → fix). Fix, re-render, review again. Nothing goes to
   the owner with an open blocker. After an owner or outside review, answer it item by item in `review_ack_rN.md`,
   checking each note against the composition, timings and a frame before changing anything.
