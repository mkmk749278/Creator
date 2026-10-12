# Visual refinement changelog: Minimum Amount Due

Brief: the owner's handoff "Minimum Due Visual Refinement" (2026-10-12). Plan: `refine-plan.md`.

The voice-over, script, facts, audio mix and length are unchanged: 8:04.8, 14,544 frames at 30 fps, −14.2 LUFS. The v3
preview (`assets/minimum-due-preview-720p.mp4`, `assemble.py`) is kept intact. The refined cut builds with
`assemble.py --refined` into `assets/minimum-due-refined-preview-720p.mp4`.

## Phase 1 (2026-10-12): the three highest-value scenes

| Replaced (v3) | New scene | What the viewer now sees |
|---|---|---|
| 0:03.6–0:19.5: bill screenshot zooms, dark "salary" clip | `video/minimumdue/s01_pay` (16.0 s) | A phone bill: ₹30,000 total, ₹1,500 minimum highlighted. The finger taps "Pay minimum" and the screen shows "₹1,500 paid". "Still pending ₹28,500" stays on screen. "No late fee" and "CIBIL score safe" appear as they are said. Labelled SIMULATION · OUR EXAMPLE |
| 1:47–3:33: three spend clips, boards b03/b04/b15/b16, sample clips, two cut-ins | `video/minimumdue/s02_timeline` (105.3 s) | One continuous Oct–Nov timeline: the three purchases drop onto their dates (real thumbnails); the bill on 25 Oct and the last date 14 Nov; 40-day and 25-day interest-free spans; the condition; "Paid ₹1,500 (minimum)" on 14 Nov; rule 1 turns the spans into interest from each spend date; the rate chip "3.75% a month = 45% a year, rate in this example (ICICI)"; rule 2 as a step area of the money charged interest (₹10,000 → ₹25,000 → the full ₹30,000 till 14 Nov → ₹28,500 after); rule 3 GST; the 25 Nov bill as a ledger (₹30,000 − ₹1,500 + ₹1,679.18 interest + ₹302.25 GST = ₹30,481.43). A card-balance counter tracks every step. The RBI rules page (1.22) and ICICI's 3.75% page (1.26) stay as cutaways |
| 4:16–4:52: board b06, calendar cutaway, clock clip | `video/minimumdue/s03_allocation` (35.8 s) | The balance line month by month from the checked series. One ₹100 payment splits ₹74 interest + GST / ₹26 to the loan. A marker with linked "Paid so far" and "Still pending" counters lands on year 1 (₹19,987 / ₹24,771) and year 5 (₹69,896 / ₹12,956). The line runs on to year 10, still above zero: "More than 10 years" |

The runtime mix went from 49% whiteboard / 51% real, proof and sim (v3) to **30% whiteboard / 32% money animation /
38% real, proof and sim**.

**Reusable kit:** `video/lib/fin/`:
- Colour meaning: blue principal, green payments, red interest/fees, yellow focus.
- A blurred real backdrop with grade, grain and vignette.
- Phone UI, chips, callouts and a ledger.
- Indian-format ₹ and counters as pure functions of time.

`scripts/vendor-assets.mjs` copies the kit and Inter latin-ext (the ₹ glyph) into pages that use them.

## Validation done

- Every on-screen number comes from `tools/mad_math.py` through `build/scene_data.py`; nothing was typed by hand.
  Year 1 and year 5 match claim MD-049 and the earlier boards. The ledger adds up to ₹30,481.43, as in the tool's output.
- The bank's published example (ICICI ₹69,688 / ₹65,000 / ₹4,317) and our ₹30,000 illustration stay separate. Each
  scene carries an "OUR EXAMPLE" case label and an "OUR CALCULATION" or "SIMULATION" tag. The 3.75% rate is labelled
  "rate in this example (ICICI)".
- Interest is never shown as a running counter. It shows as the money charged interest over time (accrual) and posts
  only on the 25 Nov bill.
- Cue times come from the VO alignment (phrase position within each line, about ±0.3 s).
- `hyperframes lint` and `check`: 0 errors on all three scenes (layout, contrast WCAG AA, motion).
- Snapshots at every cue, plus frames sampled from the actual renders (the counters update during render seeks).
- Per-shot review sheets of the assembled cut: `qa/review_refined/`. Frame count and loudness verified.

## Not done yet (Phase 2, after the owner's review)

- ICICI statement callouts (0:22–0:49).
- The two-choice phone (1:00–1:35).
- Petrol on the timeline (3:51–4:13).
- CRIF bars (5:05–5:19).
- The money flow for card rotation (5:32–6:16).
- Advice as phone actions (6:16–7:20).
- The recap and a designed end screen.

Phase 2 takes the whiteboard under 25%. After that come the 1080p master and the final full-film review.

## Limitations

- This is a visual change, not a new fact-check. It uses the numbers and claims already checked in `claims.csv` and
  `fact-check.md`.
- Cue sync is by phrase position, not word-level timing. It was checked visually, not by ear.

## Master (2026-10-12, after the owner approved the refined cut)

`assets/minimum-due-refined-master.mp4`: 3840×2160, 30 fps, 14,544 frames (identical to the approved cut), 8:04.8,
19.9 Mbps, −14.2 LUFS, peak −0.8 dBFS. https://gofile.io/d/uube0Nlr

- **Native 4K:** all 13 boards and the 3 money scenes, re-rendered by `build/render_4k.sh` with
  `make_native_4k.mjs`, plus the source-page proofs (shot at 2×).
- **Upscaled from 1080p:** the stock clips and the phone simulation stills. Pixabay and Coverr give 1080p (some
  1440p); Commons photos are scaled from their originals.
- **Cut unchanged:** no visual edits after the owner's approval.

YouTube package: `youtube/`.
- `description.md`: titles, description, chapters, sources, credits, tags, pinned comment.
- `subtitles.en.srt`.
- `UPLOAD.md`: the upload checklist.
- `thumbnail_A.jpg` and `thumbnail_B.jpg`, in the channel's navy and gold theme.

Phase 2 of the brief was not started; the owner approved the cut as it is.
