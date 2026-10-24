# India's Jet Engine Bet (rebuild of "India Landed on the Moon. Why Can't It Build a Jet Engine?")

Rebuild of `projects/jet-engine-paradox/` (owner, 2026-10-22: "we need to rebuild everything", after Studio showed 1.2K views,
average view duration 1:57 = 20.9% of 9:22, and retention falling from 100% to about 33% in the first minute). The old
project stays untouched as the source of facts (`../jet-engine-paradox/claims.csv`, 66 rows).

**What changed, and why (the magnet film's method, `../rare-earth-magnets/`):**
| Old film (v2) | New film |
|---|---|
| Moon, submarine, Mars glory for 36 s; question at 0:39 | Cold open on the thing in the hangar: ~30 jets, none delivered, 14 of 99 engines (0:00–0:30); Moon/submarines only as the twist |
| "Welcome to Be Practical with Kishore", sting and title card at 0:42 | No welcome. Channel named only in the sign-off |
| Squadrons, orders, sanctions, history for 2 minutes before the mechanism | Short "why one engine matters" (about 1:10), then control (1998) as the Rule, then the mechanism |
| No open loop | Open loop at 0:35: three promised things, the blade, Kaveri, the decision awaiting in Delhi |
| Verdict frame ("why can't it?") | Live bet frame: Dry Kaveri, D.M.R.L. blades, Safran 120 kN deal awaiting approval, dates to watch |
| Lecture-style narration | Spoken English: you/I, questions, check-ins, Rule, Ruin, Reality, bridge to the next film |

Files: `vo.txt` (recording text, one beat per line, ~1,640 words, ~10:50 at Akash's pace) · `script.tsv` · `vo_blocks.md`
(8 Akash blocks, each under 1,500 characters; build with `tools/vo_blocks.py`).
Check: `python3 scripts/spoken_english_check.py projects/jet-engine-bet/vo.txt --min-words 1300 --max-words 1900` (passes).

**Facts:** every line maps to a row of the old `claims.csv` that was already checked (JE-001 to JE-066); no new facts were added.
New or re-ordered lines that need a fresh `/fact-check` round before recording:
- "India was the first country ever to land near the Moon's south pole" (JE-002, fine).
- "with your money" (public order, unsourced framing: remove if the checker objects).
- "about four minutes in" open-loop minute: re-time after the VO is recorded.
- Time-sensitive: 14 of 99 engines, ~30 jets built, none delivered, Safran deal awaiting approval (as of 13 Oct 2026): re-check the day before upload.
- "Moon was the easier problem" verdict is dropped; the hook now carries the paradox.

**Next phases (not started):** (1) `/fact-check` the changed lines; (2) audience review (`prompts/audience_review_v1.md`, new
session, no repo); (3) screenplay in the magnet film's format (chain-bar equivalent: a THREE-LINK "HOT SECTION" bar: metal,
air, coating; HUD: engines sent 14/99, jets waiting ~30), with hero 3D shots (turbine blade cutaway with film cooling, grain
vs single crystal, Kaveri thrust bar); (4) record, align, source, build, review, render, YouTube package with a new
thumbnail (one object, one number, 2–4 words, clear of the bottom-right timestamp).
