# Minimum Amount Due: self-review log

Method (PLAYBOOK §14): after each assembly, `build/review_shots.py` draws 3 frames per shot next to the VO spoken over
it (`qa/review/shots_NN.jpg`). Every shot is judged against §14. Each finding gets a fix and the lesson behind it, then
the film is re-assembled and reviewed again until a round finds nothing worth fixing. A whole-film pass comes last.

## Round 1: v1 (first full 720p cut, 61 shots)

| Shots | Finding | Fix | Lesson |
|---|---|---|---|
| ICICI and RBI proofs, news | Highlighted line about 10 px tall on a phone: unreadable | Re-shot pages at 2×; wide establish, then push to 1.6–2.5× on the saved highlight box, then pan | A proof the viewer can't read proves nothing |
| RBI rules page | "Get notified" pop-up over the page | Remove every fixed or sticky element before the screenshot | Check pages for overlays, not only cookie bars |
| Business Standard | Ad banners in frame | Hide ad slots; frame the headline tight | |
| 1.08 hook, 1.17 groceries | TABAK supermarket (foreign) | Groceries: Kartik General Store (Commons, India). Hook: flash-forwards of the maths boards | Indian places in every stand-in |
| 2.24 EMI | European teen on a phone | HDFC branch in Hyderabad with Telugu signage (Commons) | Search Commons by brand plus city |
| 2.16 cash from card | Guard asleep in front of a shop shutter (ATM photo) | HDFC ATM with an auto outside | Look at the whole photo, not just the subject |
| b02, b03, b04, b06, b11, b12 | Boards held 15–42 s without a cut; blank board after each duster | Cut away at duster moments to a relevant clip or proof (ICICI 3.75% page, calendar flip, payment clips) | No board over ~16 s; never show an empty board |
| b02 | "Minimum ≠ safety net" was struck through, reversing the meaning | Write the myth "Minimum = safety net", strike it, then write "Minimum = interest switch ON" | Strike only the myth |
| b03, b08 | Text overlap and text off the board | `cx()` shrinks to fit; positions re-measured | Measure every line with the pen-font metrics |
| Supreme Court, petrol pump | 4:3 and portrait photos squashed into 16:9 | Cover-crop to 16:9 around the focus before zooming | zoompan stretches the whole input to the output size |
| Mix | −14.8 LUFS | Exact gain, then a −1.5 dBFS limiter | `loudnorm` linear mode undershoots when the true peak limits it |
| Final mux | Encoded at 0.3× real time | Pre-scale the 4096 px logo once | Never rescale a big overlay on every frame |

## Round 2: v2 (84 shots)

| Shots | Finding | Fix | Lesson |
|---|---|---|---|
| Whole film | Shot lengths rounded per shot: picture up to ~0.2 s off the VO mid-film | Frame-exact lengths from absolute frame numbers, `-frames:v` per shot | Cumulative rounding is real drift over 80+ cuts |
| Hook | Four boards in a row (13 s) before the sting | Third flash-forward replaced by real footage | Keep the real/board mix even inside a montage |
| 1.31 sample | Falling ₹500 notes under "NO NEW SPENDING" read as money pouring in | Real hands-on-phone clip for that beat | A picture can contradict its label |
| ICICI 3.75% cutaway | 1.4 s wide establish too small to read | Short proofs go straight into the push | Below ~3.6 s, skip the establish |
| b03 | "Groceries: 25 days" touched the board's bottom edge | Layout moved up 60–70 px | Keep text above y ≈ 940 |
| b07 | Blank board for 2 s at the start | First line starts with the VO | Write from the first word |
| HDFC branch, Supreme Court | Cover-crop cut the sign or roof | Focus raised to 0.4 | Buildings: keep the roofline and signage in frame |
| Loudness | −14.2 LUFS, peak −0.8 dBFS | Within target | |

## Round 3: v3 (91 shots)

| Shots | Finding | Fix | Lesson |
|---|---|---|---|
| 1.31 board (from the style sample) | "Bank added ₹1,981" ran off the board; the sample was built before the text-fit fix | Rebuilt as boards b15/b16 on the measured layout; the sample keeps only its real clips | Re-render old scenes when the engine improves |
| b15 | Circle still being drawn at the cut | Shorter write `dur` so the circle ends 0.4 s before the cut | A shape must finish before the cut |
| Whole film | 87 frame-exact shots, 14,544 frames = VO end; −14.2 LUFS, peak −0.8 dBFS | No change needed | |

## Whole-film pass (v3)

- **Mix:** boards were 50% of the runtime against about 50% real footage, proofs and sims. Two more real cut-ins went
  where the VO describes something real (the bill's minimum; a card swipe for "interest from the day you spent"). Boards
  stay where the maths is worked out. Now 49% board, 51% real/proof/sim.
- **Rhythm:** 91 shots, average 5.3 s. The longest holds are boards with continuous writing (about 15–17 s: b02 and b06),
  each broken by a duster or a cutaway.
- **Remaining choices for the owner:**
  - The 12.6 s end card.
  - b06 and b13 stay on the board for the key maths and the recap.
  - Stand-ins are labelled "ILLUSTRATION".
