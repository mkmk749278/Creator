# Minimum Amount Due: visual refinement plan

Source brief: owner's handoff "Minimum Due Visual Refinement" (2026-10-12). Narration, script, facts and audio stay
unchanged; v3 (`assets/minimum-due-preview-720p.mp4`, built by `build/assemble.py`) is kept intact. The refined cut is
assembled separately (`build/assemble.py --refined` → `assets/minimum-due-refined-preview.mp4`). The target is the
whiteboard at ≤ 20–25 % of the runtime.

All on-screen numbers come from `tools/mad_math.py` through `build/scene_data.py` (claims MD-049 and related). Cue times
come from the VO alignment. The bank's published example (ICICI, ₹69,688 / ₹65,000 / ₹4,317) and our illustration
(₹30,000 card bill) keep separate, labelled visual cases.

## Phase 1: the three highest-value scenes (this phase)

| Film time | Lines | Was (v3) | Now |
|---|---|---|---|
| 0:03.6–0:19.5 | 1.02–1.03 | bill screenshot zooms, dark "salary" clip | **s01_pay**: phone bill (₹30,000 total, ₹1,500 minimum highlighted) → tap "Pay minimum" → "₹1,500 paid" → "Still pending ₹28,500" stays on screen; "No late fee ✓" and "CIBIL safe ✓" appear when said. SIMULATION label |
| 1:47–3:33 | 1.17–1.32 | spend clips, boards b03/b04/b15/b16, cut-ins | **s02_timeline**: one continuous Oct–Nov timeline. Purchases drop onto their dates (real thumbnails); statement 25 Oct and last date 14 Nov; 40-day and 25-day interest-free spans; ₹1,500 payment; rule 1 turns the spans into interest from each spend date; the balance-charged area shows rule 2 (₹30,000 till 14 Nov, ₹28,500 after); rate chip "3.75 %/month · 45 %/yr, ICICI rate in this example"; GST; statement 25 Nov ledger: −₹1,500 paid, +₹1,679.18 interest, +₹302.25 GST = ₹30,481.43. The RBI-rules page (1.22) and the ICICI 3.75 % page (1.26) stay as cutaways |
| 4:16–4:52 | 2.02–2.06 | board b06 + calendar cutaway | **s03_allocation**: a ₹100 payment splits ₹74 interest + GST / ₹26 loan; the balance line runs month by month from the checked series with linked "Paid so far" and "Still pending" counters (year 1: ₹19,987 / ₹24,771; year 5: ₹69,896 / ₹12,956); year 10 still pending → "more than ten years" |

## Later phases (after the owner reviews Phase 1)

| Film time | Lines | Planned treatment |
|---|---|---|
| 0:22–0:49 | 1.04–1.07 | ICICI statement: dim other rows, lift each amount into a large callout, case label "ICICI'S OWN EXAMPLE" |
| 1:00–1:35 | 1.10–1.15 | One phone with two choices (full bill / minimum); consequences appear beside each as named |
| 3:51–4:13 | 1.35–1.37 | Petrol purchase on the same timeline (15 Nov) with zero interest-free days |
| 5:05–5:19 | 2.09 | CRIF comparison as an animated bar pair with date and source |
| 5:32–6:16 | 2.11–2.17 | Card rotation as money moving friend → card → rent app → friend with the total pending visible |
| 6:16–7:20 | 2.18–2.26 | Advice as actions: autopay switch, statement finance-charges row, EMI rate comparison, bill-date move on a calendar |
| 7:20–8:05 | 2.27–2.32 | One clean recap composition; designed end screen |
