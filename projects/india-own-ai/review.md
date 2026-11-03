# Review: cut r1 (720p, 2026-11-03)

`assets/out/india_own_ai_r1_720.mp4` (Drive `English/india-own-ai/review/r1/`), 13:06.9, 1280×720 30 fps,
−14.2 LUFS, peak −1.8 dBFS. Parts rendered on GitHub (Render film, commit d79b276). Sheets: `qa/r1_sheet/`.

## Checked (PLAYBOOK §14)
- **Lede in 25 s:** "So can India build an A.I. of its own?" at 0:24.6 (VO) with the on-screen question. ✓
- **Open loop:** "around minute ten" (2:17) → the chopping test returns at 9:47. ✓
- **Numbers on screen** come from claims.csv rows; token tiles are the real pieces (research/token_pieces.json). ✓
- **Hindi first** (owner, 2026-11-03): Hindi → Marathi → Telugu in the open, the library and the payoff. ✓
- **Silence before the reveal:** 1.5 s music silence before "ten thousand crore... thirteen lakh crore"; music drop before the payoff. ✓
- **Channel named only at the end;** logo bug throughout; end card with the NavIC bridge. ✓
- **Fixed in this round before sending:** Indic labels rendered as boxes on GitHub (fonts), a news clip's own burned-in
  caption, two empty plates (2:28, 2:52), clipped date labels, label overlaps (hyperframes check: 0 errors on all parts).

## Known, for round 2
1. **Four script names in the 13-language chart (10:18) and some of the 22 shelves (4:36) are boxes:** Gujarati, Kannada,
   Malayalam, Gurmukhi, Urdu/Arabic, Ol Chiki and Meitei fonts are not bundled yet.
2. **Stand-ins until the owner's YouTube/photos arrive:** the minister's promise (PIB photo, not video), the summit stage
   (city aerial), Sarvam's founders (Sarvam blog page), BharatGen (blog page), NavIC lift-off (city aerial).
3. Some animated plates are sparse for 1-2 s while elements build (e.g. 1:56, 7:24).
4. The 5:40 server-LED shot is very dark.
5. Shot-by-word audit (`shot_word_audit.py`) not yet run on this cut.
