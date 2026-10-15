# The Kavach Railway Reality (Video 27, English explainer)

Explainer for *Be Practical with Kishore* from the owner's handoff (`brief/owner-handoff.pdf`, received 2026-10-15) and
the owner's two audits (`brief/technical-audit-2026-10-15.md`, `brief/research-dossier.md`). Every train crash restarts
the same online fight: "no Kavach" vs "Kavach makes crashes impossible". The film opens in a night cab (hook), shows what
Kavach physically is (tags, station computer, radio, loco unit; SIL-4 without the myth), works out the stopping physics
on the board (Vande Bharat's 654 m from 130 km/h, freight maths, fog, 208 SPADs), audits the rollout numbers (commissioned vs fitted vs work
started, money, the slowest step), and then the reveal: Balasore (false green from the signalling itself: nobody can say
for sure) vs Kanchanjunga (failed signals and broken backup rules: where Kavach could really help). Verdict: three
questions to ask of any viral Kavach post.

**Status (2026-10-15): phase 1, script v2.** Rewritten in the owner's new English style (PLAYBOOK §4a-4, guide in
Part F): elder-brother voice, phonetic acronyms for Akash (R-D-S-O, R-F-I-D, U-H-F, S-I-L, H-B-L, P-I-B), hook with an
open loop ("around the eight minute mark"), forensic dissection, a three-step citizen's action plan (check forwards, read
PIB/CRS, Rail Madad 139), outro with "Jai Hind". 61 lines, 3 voice blocks, 10,402 characters: ≈ 12:26 by the estimator,
≈ 11:10 at the measured English Akash rate (×0.9). Views: `screenplay.md` (TIME | AUDIO | VISUAL + SFX), `script.md`,
`bunty_blocks.md` (paste-ready). v1.1 history: `brief/changes-from-brief.md`. Fact-check gate passes (81 claims: 75 confirmed, 6 claim): `claims.csv`,
`fact-check.md`.

**VO recorded (2026-10-15):** Akash "Confident and Natural", eleven_v4: `voice/block1.mp3` 3:24, `block2.mp3` 3:38,
`block3.mp3` 3:47 = **10:49**. Timed with `align_script.py` (`align/block1-3/`): speech-to-text ratio 0.85–1.18 on every
line (nothing skipped or doubled); 20 of 61 boundaries flagged as one-pause-ambiguous for a listen. Raw-VO times: open
loop 0:47, payoff starts 7:02 ("the question I promised"), Balasore answer 7:35, Kanchanjunga 8:08, action plan 9:27.
The line promises "around the eight minute mark": the edit's pauses (logo sting, 1.5 s silences, diegetic breaks) must
land the payoff at ~7:30–8:15, or re-record that one sentence. Next: beats, sourcing, EDL.

## Genre and look (PLAYBOOK §5.3, own art direction)
**Tech × society investigation.** Art direction **"Signal Room"**: the film moves between three worlds.
1. **Real world** (night cabs, fog, tracks, sheds, archive of the two crash sites, credited and short).
2. **Telemetry world** (the machine's view): Kavach cab-display grammar: target distance, permitted speed, braking curve
   drawn ahead of the train, signal aspects on carbon slate; the 3D hardware X-ray of the loco and track.
3. **Board and proof world**: maths worked live on `video/lib/whiteboard`; RDSO, CRS and PIB pages under the forensic magnifier.

Palette (owner's handoff): Carbon Slate `#0F172A` (base), Signal Cyan `#0284C7` (Kavach, data, radio), Amber Caution
`#F59E0B` (warnings, our calculations), Danger Crimson `#DC2626` (failure, collision), Crisp White `#F8FAFC` (text).
Engines from the handoff: H1 hardware X-ray, H2 braking curve, H3 fog split, H4 rollout funnel, H5 Balasore logic gate,
H6 Kanchanjunga simulation. All animation labelled ILLUSTRATION / SIMULATION; our maths labelled ILLUSTRATIVE.
Recurring motifs: the four-link chain; the braking curve drawn ahead of the train; the two viral myths (hook → stamped
in the crash section → dissolved in the outro). Silence: 1.5 s before V057 ("Here's the honest answer").

## Voice
Handoff: **Akash**, ElevenLabs v4, stability 0.65, similarity 0.85, style 0.15, speaker boost on. English rules: numbers as
words, no digits, brackets, quotes or `!`; `—` allowed; letter acronyms hyphenated; never 3+ very short sentences in a
row (lint in `tools/build_script.py`).

## Files and rebuild
| File | What |
|---|---|
| `script.full.tsv` | **Single source**: id, section, te (dub, empty), en VO, emotion (empty), visual, on-screen, sound, pacing, cite |
| `tools/make_tsv.py`, `tools/make_tsv_v2.py` | One-time v1 / v2 author helpers (do not re-run after edits to the TSV) |
| `screenplay.md`, `script.md`, `bunty_blocks.md`, `bunty_blocks_clean.md`, `script.tsv` | Built views (do not edit) |
| `claims.csv`, `fact-check.md` | Fact-check gate |
| `brief/` | Owner's handoff + audits (PDF and text) and `changes-from-brief.md` |

```bash
python3 projects/kavach-railway-reality/tools/build_script.py         # views + lint
python3 scripts/claims_check.py projects/kavach-railway-reality/claims.csv
```
