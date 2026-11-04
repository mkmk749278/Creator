# Review acknowledgement, round 3: "our country, our language" (owner, 2026-11-04)

**The note (owner):** "While we are saying 'your country, your language', we have to say 'our country, our language'.
That hits the emotion right." Times below are the r4 cut's own (13:06.5), from `align/` and `build/make_film.py`.

## The owner's note, item by item
| # | Line (r4 time) | Was | Now | Status |
|---|---|---|---|---|
| 1 | L4, 0:22 | cuts some of **your** letters in half | **our** letters | FIXED (block 1 re-take) |
| 2 | L5, 0:30 | speaks **your** language best? | **our** language | FIXED (block 1) |
| 3 | L25, 3:22 | So **your** missing pieces | **our** missing pieces | FIXED (block 3) |
| 4 | L32, 4:21 | lives in **your** country … **your** language is almost invisible | **our** country … **our** language | FIXED (block 3) |
| 5 | L33, 4:37 | **Your** country's Constitution | **Our** country's | FIXED (block 4) |
| 6 | L37, 5:12 | If **your** language … charges **you** more | **our** language … charges **us** more | FIXED (block 4) |
| 7 | L51, 7:17 | eight times **your** country's shared pool | **our** country's | FIXED (block 5) |
| 8 | L74, 10:28 | So for **your** language | **our** language | FIXED (block 7) |
| 9 | L83, 11:49 | reads **your** Hindi, Marathi, Telugu… | **our** Hindi… | FIXED (block 8) |
| 10 | YouTube description line 1 | chops **your** Hindi | **our** Hindi | FIXED (`youtube/package.md`) |

CHECKED, kept as "you/your" on purpose: what the viewer does or owns: "ask in your own language" (L85), "your
mother tongue" (L87), "your apps", "your Chat G.P.T. plan", "your phone", "Check your plan" chip, "Which A.I. answered
best in your language?" comment bubble. The rule is in CLAUDE.md and PLAYBOOK §4a-10 rule 13.

## How it was made
- Six whole-block Akash re-takes (no splicing), owner's settings; `vo_take_check.py`: one flag, L70, the same slow
  list read ("Hindi eight, Marathi fourteen, Telugu fifteen") as the approved take. Blocks 2, 6 and 9 are the approved takes.
- Every line re-aligned (`tools/align_blocks.py`); line starts move between −2.6 s and +1.5 s; film 13:06.5 (was 13:06.9).
- Picture: the r3 build reproduced byte-for-byte from the old timing first (proving the rebuild), then rebuilt on the
  new timing. Chapters: 2:35, 3:22, 5:36, 8:14, 10:52 (were 2:33, 3:21, 5:36, 8:15, 10:52). The minute-ten promise
  pays off at 9:46 (was 9:47).
- Audio: the sound effects from r1 were never saved, so the 16 effects are now made in code
  (`tools/synth_sfx.py`, the owner's choice). Mix rebuilt from stems, −14.4 LUFS on the test bounce.

## Also found and fixed in this round
- **11:16 "far bigger budgets":** the faster read dropped the dollar-notes cutaway (next cut 0.59 s away); it now
  starts on "far bigger budgets".
- **2:25 Sarvam tiles over the caption:** on the new timing the third row of tiles sat on "I'll run that same
  chopping test…" for 1.5 s (`hyperframes check` failed); the tiles sit 70 px higher, check passes.

## OPEN
- The 4K parts render on GitHub Actions (run 78); then assembly, a full-film freeze/black scan, join checks and the
  loudness of the final MP4.
- The owner's audio-only pass of the new voice (`india_own_ai_vo_r4.mp3`) and the soundtrack with the code-made effects.
