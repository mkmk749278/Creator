# Episode 02 scenes, session C (filing and proof)

Five HyperFrames compositions for *The Insurance Ombudsman* (`projects/insurance-ombudsman/`, brief in `SESSIONS.md`,
specs in `scenes.md`). Art direction "the third door": warm paper, window light, pre-blurred real footage plates, the
owner's palette (navy, signal yellow, teal, paper, mist, coral only for cuts). 1920×1080, 30 fps.

| Scene | Clips (VO window + 0.25 s handle each side) | What it shows |
|---|---|---|
| `C1_filing_stepper` | `C1_filing_stepper_O039` 5.43 s, `_O040` 5.90 s, `_O048` 9.77 s | Browser schematic: `cioins.co.in` typed letter by letter on the spelled VO; stepper Register → Details → Upload → Review; Register Complaint click, masked mobile number, OTP to the phone (dots only), Verified on "O-T-P" (ILLUSTRATION). O048: step 4 review, rows checked, declaration ticked, Submit, Verified → Registered, acknowledgement (complaint no. HYD-H-2026-0471, same invented number as C4's award) saved to the phone (SIMULATION) |
| `C2_offices_board` | `C2_offices_board_O041` 15.57 s | Split-flap board of the 18 offices (G08 order); lamps light on the spoken names (Hyderabad, Bengaluru, Mumbai, Delhi, Kolkata), then all 18; home and branch routes to the chosen office |
| `C3_document_slots` | `C3_document_slots_O042` 2.93, `_O043` 2.90, `_O044` 4.27, `_O045` 3.50, `_O046` 3.93 s, `_O047` 8.20 s | Upload step (3) of the same stepper: five SIMULATION papers fly into their slots on "One … Four … And five"; PDF/JPG chips + `PDF / JPG · MAX 10 MB EACH [CIOINS.CO.IN]` |
| `C4_binding_award` | `C4_binding_award_O010` 19.67, `_O052` 4.73, `_O056` 6.57, `_O057` 8.47 s | O010: the third door opens → FREE TO FILE (fee ₹0) → award, seal, teal lock (AWARD BINDS THE INSURER) → days-late calendar with +₹5,000 per day. O052: complaint and reply stay apart, award drops, signed, sealed. O056/O057: G04 as two case folders: INSURER (Rule 17(8) crop highlighted, lock closes on "binding") / COMPLAINANT (copy unlocked, route to a forum) |
| `C5_proof_magnifier` | `C5_proof_magnifier_O018` 11.33, `_O022` 12.30, `_O027` 11.30, `_O035` 7.30, `_O036` 4.30, `_O037` 12.30 s | Forensic magnifier + gold highlighter on the real pages: Rules p1 title and short title; Rule 14(1) "himself or through his legal heirs, nominee or assignee"; CIO 2024–25 Statement H8 column 14(3(a)) Total 1,715 + its legend; 14(3)(b) "within one year" → 17(3) "[fifty] lakhs"; footnote 3 G.S.R. 828(E) 9.11.2023; 14(5) word by word |

Coordinator correction (S0, 2026-10-15): O047 belongs to C3 (`C3_document_slots_O047`) and C1 renders O048
(film 403.56–412.80, on screen SIMULATION) instead.

## Timing
`c_windows.py` turns the film-time windows into one layout per scene (sections end to end, whole frames) and writes
`windows.json` + each scene's `windows.js`. Beats inside a window come from `timing.csv` sentences plus silencedetect
pauses on the real Akash VO (`voice/bp-hlth02-ch2-4.mp3` sits at film +132.35 s). One render per scene, then
`split_clips.py` cuts the master frame-exactly into the clips (CRF 17, 18 Mb/s cap) and a 4-frame contact sheet each.

## Sources and rights
- `img/rules_p*.jpg`: S01 *Insurance Ombudsman Rules, 2017 (updated as on 9.11.2023)*, PDF pages 1, 9, 11 at 300 dpi
  (owner's asset pack `official_sources/S01_Ombudsman_Rules_2023.pdf`); highlight boxes from `pdftotext -bbox`.
- `img/cio_h8.jpg`: CIO Annual Report 2024–25, Statement H8 (`projects/insurance-ombudsman/sources/`).
- Plates (`media/plate.mp4`, gitignored, rebuilt by `make_plates.py`): owner's Pexels clips F10 (C1), F14 (C2), F07 (C3),
  F08 + F09 (C4), F09 + F07 (C5), heavily blurred and graded as out-of-focus background only (Pexels licence,
  `handoff/asset-pack/FOOTAGE_REGISTER.csv`).
- All letters, forms, IDs, numbers are SIMULATION (invented complaint/policy numbers, masked phone and OTP, silhouettes).

## Rebuild
```bash
python3 c_windows.py                       # windows.json + <scene>/windows.js
python3 make_plates.py <BP_HLTH02_Asset_Pack dir>
./sync_shared.sh && (cd ../.. && node scripts/vendor-assets.mjs)
(cd C5_proof_magnifier && npx hyperframes check)
setsid nohup ./render_all.sh > renders/render.log 2>&1 < /dev/null & disown   # SCENES="C2_offices_board" to pick
```
