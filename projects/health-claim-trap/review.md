# Review: health-claim-trap preview v2 (720p, 8:45) — visual-engine upgrade

Built to the owner's "Visual Engine Upgrade" spec (2026-10-14): every stock clip is replaced by programmatic HyperFrames
scenes (`build/make_engines.py`, 23 compositions); the real IRDAI / CIO / Bima Bharosa pages run on a 3D document rig
with a scan line. Method: `scripts/contact_sheet.py --every 2` (263 frames), each tile checked against the VO line at its
timecode, PLAYBOOK §14. Loudness −14.2 LUFS integrated.

## Engine map
| Time | Engine | Scenes |
|---|---|---|
| 0:00–1:17 | 1 isometric hospital cutaway + hook | e1_hospital (dive, ICU pulse, billing floor, ₹4,50,000 counter), e0_ledger (6 policy years, ₹2,10,000, 0 lapses), s01_letter (stamp), e2_shock (₹62,000 vs ₹3,88,000 short), e2_drain (FD · relative · card), e3_scale (6 years vs one letter), e1b_overstamp (laser slices stamp → 60-month moratorium) |
| 1:19–3:46 | 2 x-ray rig + 3 bill slicer | e4_pillars (3 files), e5_funnel (69 of 100 claims via TPAs; "govt doctor" badge peels off), e6_lock + d_para17, e7_dossier (case sheet → laser thread → 2020 proposal form → denial; BP ≠ fracture; years 1–5 vs 6), e8_opd, e9_slicer (₹9,000 expected → ₹59,625 cut; medicines protected), e10_wall (wall → two lanes → circular as key) |
| 3:46–5:28 | 4 moratorium shield + 5 stopwatch | e11_shield (96 months, 36 shatter, shield at month 60), d_para13 (core reveal), e12_history, e13_burden, e14_port, e15_impact (denial shatters on the shield), e16_stopwatch + d_para16 / d_para16b (3:00:00 → overtime; ₹4,000 delay charge moves to the insurer's fund) |
| 5:28–7:37 | 6 war-room | e17_warroom (one 129 s panned board: 4 nodes, evidence pack, GRO email + 14-day ring, Bima Bharosa radar, 18 Ombudsman offices, CIO data 32,503 → 76%, award shield, ₹5,000/day meter), d_bima, d_cio, d_h3, d_50l |
| 7:37–8:31 | checklist + cheat-sheet | e18_checklist (declare · no room cap · consumables), e19_cheatsheet ("screenshot this" card) |

## Spec items changed for accuracy (claims.csv)
₹59,625 total cut (VO says almost sixty thousand; spec's ₹90,000 would contradict it) · "company hired & paid by the
insurer" (one TPA is state-owned) · no "algorithm" wording (no source) · "fraud the company must prove" (not "criminal")
· "No lawyer needed" (not "lawyers banned, Rule 15") · "76% of settled or decided" · 18 offices, not 17 (CIO 2024-25) ·
city constellation without an India outline · ₹62,000 / ₹3,88,000 / ₹4,000 labelled ILLUSTRATIVE · penalty "unless the
insurer appeals".

## Fixed after the first v2 pass (re-rendered)
Blank first second and blank starts of the drain and checklist scenes; overstamp text clipped ("CASHLESS" only);
7 s near-empty frame under "no shouting, no selling" (now two ✕ cards); leftover ghost folders in the dive; a red fragment
visible before the shield impact; 26 s static framing on war-room node 4 and "0%" shown early (data panel now appears on
cue, cities light one by one, camera drifts); war-room node views zoomed closer; cheat-sheet first block earlier.

## Checked and passing
Numbers match VO and claims.csv (fact-check gate passes, 54 rows); SIMULATION / ILLUSTRATIVE / OUR CALCULATION labels on
every made-up document and number; citation tags on every rule; logo sting at the channel name, bug elsewhere, end card
with "Educational only"; music silent 1.5 s before the moratorium clause; the two 3 s VO pauses carry moving pictures
(the para-13 document rig and the cioins.co.in rig).

## Owner's call
The film is now almost entirely animated (no real-world footage except the official pages). The channel rules prefer
real footage; the owner's spec asked for this. A few real shots (a hospital lobby at night, a billing counter) filmed on a
phone could still open the film if wanted.
