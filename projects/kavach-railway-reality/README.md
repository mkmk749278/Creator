# The Kavach Railway Reality (Video 27, English explainer)

Explainer for *Be Practical with Kishore* from the owner's handoff (`brief/owner-handoff.pdf`, received 2026-10-15) and
the owner's two audits (`brief/technical-audit-2026-10-15.md`, `brief/research-dossier.md`). Every train crash restarts
the same online fight: "no Kavach" vs "Kavach makes crashes impossible". The film opens in a night cab (hook), shows what
Kavach physically is (tags, station computer, radio, loco unit; SIL-4 without the myth), works out the stopping physics
on the board (RDSO's 940 m at 130 km/h, fog, 208 SPADs), audits the rollout numbers (commissioned vs fitted vs work
started, money, the slowest step), and then the reveal: Balasore (false green from the signalling itself: nobody can say
for sure) vs Kanchanjunga (failed signals and broken backup rules: where Kavach could really help). Verdict: three
questions to ask of any viral Kavach post.

**Status (2026-10-15): phase 1 in progress.** Script v1.1: 126 lines, 3 voice blocks (4,075–4,177 characters),
≈ 14:50 at the estimator's rate. Fact-check gate passes (82 claims: 76 confirmed, 5 claim, 1 disputed). Every change from the handoff and why: `brief/changes-from-brief.md`. Fact-check:
`claims.csv`, `fact-check.md`. Next: owner approves the script, then records the blocks (`voice/block1.mp3` …).

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
in Act 4 → dissolved in the verdict). Silence: 1.5 s before K103 ("Here is the honest answer").

## Voice
Handoff: **Akash**, ElevenLabs v4, stability 0.65, similarity 0.85, style 0.15, speaker boost on. English rules: numbers as
words, no digits, dashes, brackets, quotes or `!` (lint in `tools/build_script.py`).

## Files and rebuild
| File | What |
|---|---|
| `script.full.tsv` | **Single source**: id, section, te (dub, empty), en VO, emotion (empty), visual, on-screen, sound, pacing, cite |
| `tools/make_tsv.py` | One-time v1 author helper (do not re-run after edits to the TSV) |
| `script.md`, `bunty_blocks.md`, `bunty_blocks_clean.md`, `script.tsv` | Built views (do not edit) |
| `claims.csv`, `fact-check.md` | Fact-check gate |
| `brief/` | Owner's handoff + audits (PDF and text) and `changes-from-brief.md` |

```bash
python3 projects/kavach-railway-reality/tools/build_script.py         # views + lint
python3 scripts/claims_check.py projects/kavach-railway-reality/claims.csv
```
