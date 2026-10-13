# The Jet Engine Paradox: India landed on the Moon. Why can't it build a fighter jet engine? (English explainer)

Explainer for *Be Practical with Kishore* from the owner's master brief (`brief/owner-brief.pdf`, received 2026-10-13;
text copy `brief/owner-brief.txt`). India can land near the Moon's south pole and build nuclear submarines, yet its
newest Tejas Mk1A fighters wait for engines from GE's plant in Lynn, Massachusetts. The film follows the squadron gap and
the F404 delays (Act 1), the 1998 Pokhran sanctions that cut the same engines and flight-control help, the small club of
countries that can build fighter engines, the Kaveri programme from 1986/1989 to its 2008 delinking and the Il-76 flight
tests in Russia (Act 2), the physics of the high-pressure turbine blade (single crystals, film cooling, ceramic coating,
Rolls-Royce's "200 degrees above melting point" and "a London bus on every blade") (Act 3), and the turn: the Dry Kaveri
for combat drones, DMRL's single-crystal blades, the AMCA's 120 kN engine with Safran still awaiting approval, and China's
long road (Act 4 + verdict).

**Status (2026-10-13): phase 1.** Script v1 written from the brief in the channel's simple Indian English (PLAYBOOK
§4a-2): 90 lines, 2 voice blocks (4,264 / 4,076 characters), ≈ 9:50 of speech at the Bunty rate. The owner said runtime
can vary from the brief's 10:30, so the length follows the story. Writer's `claims.csv` (47 rows) logged; independent
fact-check running. Every change from the brief, with its reason: `brief/changes-from-brief.md`. Next: fact-check fixes,
then the owner records or approves TTS of the two blocks (`voice/block1.mp3`, `voice/block2.mp3`).

## Genre and look (PLAYBOOK §5.3, own art direction)
**Tech × geopolitics** (the "tech" row, re-coloured with the owner's palette). Art direction **"The Hot Section"**: a
next-generation documentary look built from three worlds that cross-fade into each other.
1. **Blueprint world** (the plans and the politics): 1980s drafting-table line work on deep titanium slate, drawn stroke
   by stroke; maps are land-only globes (no political borders) with afterburner-amber arcs.
2. **Thermal world** (the physics): an ironbow thermal-camera palette over real-time Three.js renders of the turbine
   stage, the blade, its cooling channels and the crystal lattice. Heat is always shown as heat (colour + shimmer), never
   as a number alone. Labelled ILLUSTRATION.
3. **Real world** (the evidence): ISRO, HAL, DRDO/PIB, IAF, GE, Rolls-Royce and Safran media, archive news and credited
   headlines under a forensic magnifier.

Palette from the brief: Titanium Slate `#0B0E14` (base), Afterburner Amber `#F97316` (India, progress, heat), Warning Red
`#EF4444` (gaps, delays, failure), Ceramic White `#F8FAFC` (text, coating). Cooling air is the one cool accent (cyan
`#38BDF8`), used only for air and cooling.

Recurring motifs:
- **The empty engine bay**: a Tejas wireframe with a glowing amber cavity (hook, Act 1, verdict).
- **The thrust bar** (target line vs achieved fill) for Kaveri, Dry Kaveri and the 120 kN engine.
- **The engine-club globe**: countries light up as makers; India outlined, filling in amber only in Act 4.
- **A corner turbine-temperature gauge (HUD)** that wakes at J051 and stays on through Act 3.
- 35 mm grain, ~30% vignette, anamorphic light streaks on hot metal, 2.35:1 bars only in Act 3's reveal.

Media stack: ISRO Chandrayaan-3 footage; HAL/MoD/PIB Tejas photos and video; GE F404/F414 and Rolls-Royce/Safran press
media; Commons (Il-76 test bed, Kaveri at Aero India, J-20, MiG-21); credited news headlines and the PIB/CAG documents;
Pixabay B-roll for weather, dust and industrial casting (Indian locations where people show). Citation tag on every
claim (`cite` column).

## Voice
Brief: **Akash**, Eleven Multilingual v2, stability 0.60, similarity 0.85, style 0.15, speaker boost on. Several library
voices are named Akash/Aakash; the owner confirms which (see the phase report). English rules: numbers as words, no
digits, dashes, brackets, quotes or `!` in VO text (`tools/build_script.py` lints them).

## Files
| File | What |
|---|---|
| `script.full.tsv` | **Single source**: id, section, (te dub, empty), en VO, emotion (empty), visual, on-screen, sound, pacing, cite |
| `tools/make_tsv.py` | One-time v1 author helper (do not re-run after edits to the TSV) |
| `title.txt`, `lang.txt` (`en`) | Title; VO language |
| `script.md`, `bunty_blocks.md`, `bunty_blocks_clean.md`, `script.tsv` | Built views (do not edit); blocks are voice-agnostic |
| `claims.csv`, `fact-check.md` | Fact-check gate |
| `brief/` | Owner's brief (PDF + text) and `changes-from-brief.md` |

## Rebuild
```bash
python3 projects/jet-engine-paradox/tools/build_script.py
python3 scripts/estimate_vo.py projects/jet-engine-paradox/script.tsv
python3 scripts/claims_check.py projects/jet-engine-paradox/claims.csv
```
