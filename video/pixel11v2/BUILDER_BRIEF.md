# Builder brief v2: Pixel 11 consensus video (revision)

Other agents are building the other parts in parallel. Stay inside your own folder
`video/pixel11v2/<part>/` and write only your output MP4.

v1 was reviewed. v2 must fix what the review found: evidence over opinion counts, honest framing
of findings, model clarity, and less visual sameness. The rules below are **mandatory**.

## Already scaffolded for you
- `index.html`: 1920×1080 root, voice `<audio>`, background, host bar with Maya/Leo chips and live
  captions synced to `HF_TIMINGS`. Keep all of these.
- `shared/theme.css`: tokens and classes, including the new `.model-badge`, `.tag-claim`,
  `.tag-measured`, `.tag-editorial`, `.sample` and `.sample-label`.
- `media/`: official Google product images. Use these to show the *phone*.
- `samples/`: camera samples Google published, if any exist. Use these to show photos *taken with* the phone.
  Their metadata is in `samples/samples.json`.
- Your beats: `runs/pixel-11/v2/script.json`. Each line has a `beat` describing the visual, and an
  optional `badge` naming the model. Timings: `runs/pixel-11/v2/voice/<part>.timings.json`.
- Facts: only from `script.json` and `runs/pixel-11/research/` (including `v2/`). Never invent numbers, quotes or scores.

## Mandatory rules (from the review)
1. **Model badge.** If a line's `badge` is set, show `<div class="model-badge"><span class="dot"></span>BADGE TEXT</div>`
   for that whole scene. One phone's finding must never sit under another phone's badge.
2. **Label every number by type.** Use `.tag-claim` for "Google claims" (manufacturer figures), `.tag-measured`
   for "Measured by <outlet>", and `.tag-editorial` for "Our editorial rating". Never present a manufacturer
   figure as a measurement, or our rating as a published average.
3. **Denominators.** When the beat gives "N of M outlets", show both numbers ("11 of 15 outlets"). Never show a bare count.
4. **No paused zeros.** No element may ever show 0, 0.0 or $0. Either keep a number invisible
   (`opacity: 0`) until its count-up starts and finish within 0.8 s, or fade the final value in.
   Scores always fade in at their final value; do not count them up from zero.
5. **Different tests never share a scale.** Battery and brightness results from different tests go in
   separate panels, each with its test condition written in plain words (from the beat).
6. **Camera samples** (`samples/`):
   - Show the full image for at least 3 s before any crop or zoom.
   - Always show a `.sample-label` reading exactly `Model | lens/zoom | mode | Source: Google sample`,
     with "not stated" where `samples.json` says so.
   - No filters or colour changes on samples. If you crop, label it "Crop".
7. **Quotes.** Put a quote card on screen only while the host is saying those same words.
   The beat tells you when. The caption and the card must not compete: place quote cards in the upper area.
8. **Vary the layout.** Avoid long runs of identical cards. Use full-bleed samples, side-by-side panels,
   tables, a big single number, and product images at different scales. Change the visual every 4–9 s.
9. Layout from v1 still applies:
   - Nothing over the host bar (the bottom 220 px).
   - No `filter: blur()` and no `backdrop-filter`.
   - Text at least 30 px, ≤ 12 words per text block (quotes excepted), high contrast.
   - One paused `tl`, all times absolute.

## Done means
1. `npx hyperframes check` passes, with 0 errors and no contrast warnings.
2. Snapshot every scene with `npx hyperframes snapshot --at <times> --no-end --describe false -o /tmp/claude-0/-home-user-Creator/5433c6b3-e644-596d-bb26-5a81f8ed6e2c/scratchpad/v2snaps-<part>`.
   Look at every PNG and check rules 1–9: badges correct, no zeros, labels present, nothing over the captions.
   Fix and repeat (up to 3 rounds).
3. Render with `npx hyperframes render --workers 2 --quality standard --output /home/user/Creator/runs/pixel-11/v2/parts/<part>.mp4`.
4. Use `ffprobe` to confirm the duration matches `data-duration` and an audio stream exists.
5. Report in under 120 words.
