# Review: health-claim-trap preview v5 (native 4K, 8:45) — owner's review of v3

Method: 32-frame contact sheet at the owner's timestamps plus the new scenes, from the 2160p cut; every frame checked
against the VO line at that second (PLAYBOOK §14); scene snapshots checked before the render.

## Owner's points → what changed
| Owner's point | v5 |
|---|---|
| 0:00 European street | Night waiting hall (pixabay 10874) → owner's AI cutaway (labelled) |
| 0:13 stretcher rush | Ambulance (Coverr) → IV room at night. No Indian stretcher clip on reachable free sources: owner to supply |
| 0:35 billing counter + printed bill | 9:00 PM counter clip → printer, hand lifts pages → SIMULATION bill (reframed on the total) → man reading a stamped letter (0:31) → letter scene |
| 0:44 mother's panic | "Your heart drops" face close-up → worried woman on the phone ("your family panics"). Indian clip: owner to supply |
| 0:48 corridor call to borrow | Man on the phone in the dark (204421), as v3 |
| Void 0:45 | Covered by the two clips above (e2_shock no longer in the cut; its panels now show from frame 1 anyway) |
| Void 1:08 | Stamp now on a SIMULATED paper denial letter; laser split; 60-month bar fills; camera push |
| Void 3:02 | Real clinic clips across the whole "outpatient visit" line (143988 → 49815); Excuse 3 = two rooms ₹5,000 vs ₹8,000/day with the limit line |
| Bill Guillotine −37.5% | e9 rebuilt: four towers (room, surgeon and doctor, nursing, medicines); three blades take 37.5% (OUR CALCULATION, VO "about thirty-seven percent"); medicines PROTECTED; total cut ₹59,625 |
| Void 3:48 / 4:56 · Titanium Shield vs TPA arrow | Metal "60 MONTHS" shield emblem on a taller month bar; red "TPA DENIAL · NON-DISCLOSURE" arrow shatters on it |
| Void 4:33 | Proven fraud: two full cards with icons, PROOF NEEDED seal |
| 3-Hour Stopwatch | e16 now an analog dial: amber ring to 3:00:00, red overtime ring, ₹4,000 moves to the insurer's fund |
| Void 6:04 | Reimbursement checklist card (within 15–30 days) before the grievance email |
| 7:13 table scan | e24: tilted India map (DataMeet, CC BY 4.0) with **18** beacons, 32,503 counter, radial gauge to 76% "of the health cases settled or decided", 78.5% in 3 months, ₹50 lakh binding, ₹5,000/day meter to ₹1,30,000 "unless the insurer appeals" |
| Keep 3:25 / 5:42 | Unchanged (272617; transferring-card-details) |

Every engine scene now sits on a blurred, drifting hospital backdrop (owner's cutaway image, blurred) instead of a flat blue gradient.

## Accuracy calls (claims.csv)
17 beacons → 18: the CIO Annual Report 2024-25 lists 18 offices. "Consumer win rate" → "of the health cases settled or
decided": the 76% is 15,543 of 20,440 settled-or-decided cases, not all complaints. −37.5% is our exact 3/8 calculation.

## Fixed after the first v5 pass
Printer shot was near-black (in-point moved to the hand lifting the pages); bill still cropped its labels (reframed);
guillotine frame on the tall tower overlapped the header; citation tag overlapped tower values.

## Still owed by the owner
Five Indian clips swap in 1:1 at the same timecodes (INSERTS_V5 in build/assemble.py): night waiting room with son and
medical file, stretcher rush, billing counter handing a printed bill, mother's panic close-up, corridor phone call.

---

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
