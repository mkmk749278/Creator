# The Insurance Ombudsman (Episode 02, project code BP-HLTH-02-10M; English VO)

English explainer for *Be Practical with Kishore*, **step 4 of Episode 01's plan, opened up** (sequel to
`projects/health-claim-trap`). The same family: cashless denied at 9 PM on a ₹4.5 lakh bill, they paid, filed for
reimbursement, and the claim comes back cut (₹1.2 lakh paid, ₹3.3 lakh cut). Families see two doors, a lawyer and
consumer court or a paid claim-recovery service; the film opens the third: the Insurance Ombudsman. It explains why
Bima Bharosa (Episode 01's step 3) is useful but does not decide, who may file (Rule 14), the two-step clock (write to the insurer, then one month),
the one-year window and the ₹50 lakh limit, the bar on disputes pending or decided elsewhere, filing on cioins.co.in
(18 offices, documents, verification), mediation and the hearing, the award that binds only the insurer, the 30-day
compliance rule and the ₹5,000-a-day penalty, and the Bombay High Court's Dedhia judgment.

**Status (2026-10-15): phase 1, script v1.3, fact-check passed (37/37 confirmed).** Inputs from the owner (Drive `Creator/English/insurance-ombudsman/`):
`Claude.md` (the master directive and VO script, kept verbatim in `handoff/owner-directive.md`), an audit PDF
(`handoff/ombudsman-audit.*`), `BP_HLTH02_Complete_Asset_Pack.zip` (20 Pexels clips, 8 SVG/4K graphics G01–G08, official
source snapshots, and the pack's own `SCRIPT_CORRECTIONS.md`) and `Pexels_India_Footage.zip` (15 India clips). The zips'
notes, registers and contact sheets are in `handoff/asset-pack/`; the media sits in `assets/owner/` (gitignored).
No voiceover was supplied: the owner records `voice/bp-hlth02-ch1.mp3` … `ch4.mp3` from `bunty_blocks.md` after the
fact-check fixes are in.

## Script v1: what changed from the owner's text, and why
The structure, order and voice are the owner's (65 lines, 4 chapters, one ElevenLabs block per chapter, ≈ 11:00 of
speech). Formatting follows the English VO lint (no `!`, quotes, dashes or digits; hyphen-spelled acronyms as the owner
wrote them; the `[sigh]`/`[pause]`/`[slight smile]` cues moved to the pacing column). Every claim the owner's own asset
pack or the CIO pages could not support was rewritten; each change is commented in `tools/make_tsv.py`:

| Owner's line | v1 | Why |
|---|---|---|
| Win in **60 days** (title, O011) | dropped | No end-to-end deadline; Rule 17 gives the Ombudsman three months; no outcome is guaranteed |
| Lawyer fees **₹50,000**, **five years** (O006) | "pay the fees, and wait, often for a long time" | No source for either number |
| Both choices are **a trap** (O008) | "there is a third door" | A court can be the right remedy |
| **1,715** families thrown out (O012, O027) | 1,715 health complaints turned away for not complaining to the insurer first (O027); O012 "one common mistake" | Real: CIO 2024-25 Statement H8 (IO-11); "the one" overstated (jurisdiction was 1,781) |
| ₹4 lakh bill, ₹2.8 lakh cut; 20% + GST = **nearly ₹90,000** | Episode 01's ₹4.5 lakh bill, ₹3.3 lakh cut; 20% = ₹66,000 + 18% GST = ₹77,880, OUR CALCULATION | Same family as Episode 01; arithmetic |
| "What nobody tells you … the Government set up the Ombudsman"; Bima Bharosa "the biggest confusion" | recap of Episode 01's four steps; "step four, opened fully"; Bima Bharosa is useful but not a court | Episode 01 already introduced both and made Bima Bharosa step 3 |
| Recovery firms **not allowed**; contracts **void** under s.23 Contract Act (O021–O023) | Rule 14(1): you, or your legal heir, nominee or assignee, file; the form is free | No decision found for the blanket s.23 claim; not every service is a scam |
| Write to the **GRO**; wait **30 days** | write to the insurer, best of all its GRO; one month | Rule 14(3) wording |
| **17** offices, assigned **automatically** by address proof (O040) | **18** offices; you choose by residence or insurer branch | Thane opened 27 Dec 2024; the portal asks you to choose |
| **One merged PDF**, **Annexure VI-A** emailed back (O042–O047) | five documents, PDF/JPG up to 10 MB each; verified, then registered | The live portal's fields and messages |
| **Over 40%** settled by mediation; insurer pays **before a hearing** | hearing first, mediation within it (about one in three closed health complaints, 9,417 of 29,017), then the award | 40% and "before a hearing" not supported; CIO's centre reviews show every case closed through a hearing |
| **15-minute** video call, **three questions**, any language (O051–O052) | hearing in person or online; explain simply | No fixed duration or questionnaire |
| Award **100%** binding; consumer court **completely open** (O054–O056) | binding on the insurer; other remedies **may** remain | Rules and CIO wording |
| **Bank Rate + 2%**, penalty **paid straight into your account**, 50 days = ₹2.5 lakh (O057–O059) | ₹5,000 a day **unless the insurer challenges the award within 30 days**, on top of any interest due; 10 days = ₹50,000, 30 days = ₹1.5 lakh | Policyholders' Interests master circular 2024 (appeal exception; Bank Rate + 2% is real but lives there, para 25.2); no automatic credit |
| Bombay HC: penalties **from officers' salaries** (O060) | a senior citizen unpaid for over three years after winning an award; award + interest + ₹1 lakh costs, recovered from the officers responsible after an inquiry | Dedhia, 9 Dec 2024, was case-specific |
| Next episode: hospitals **violate** price caps (O063) | "what the government's price rules say about them" | Caps exist only for stents and knee implants; other devices only a 10% yearly rise limit |

## Series continuity (owner, 2026-10-15; PLAYBOOK §4a-4)
**Stands alone:** a viewer who never saw Episode 01 understands everything. The film opens on the situation ("Imagine
you are standing at a hospital billing counter…"), O002 teaches what is needed from Episode 01 (cashless denial is not
the end; pay and claim back; the four steps), and every term is glossed on first use. Episode 01 is a pointer ("we
told this story in our last video"), never required. **Glimpses:** 2–4 s shots from Episode 01's final cut under O001–O002
(counter, the CASHLESS DENIED letter, the staircase), labelled `FROM EPISODE 1`.

Episode 02 continues Episode 01 as one story; checked against Episode 01's recorded script (`../health-claim-trap/script.full.tsv`)
and its published description:
| Episode 01 said | Episode 02 |
|---|---|
| 9 PM billing counter, ₹4,50,000 bill, cashless denied, six-year policy (E001–E007) | O001 recap with the same SIMULATION bill and red stamp; all amounts derive from ₹4.5 lakh |
| Four steps: papers → reimbursement + GRO (14 days) → Bima Bharosa → Ombudsman (E044–E056) | O002 recap on the same staircase motif; O009 "step four of that plan"; O029 "this is step two of our plan" |
| Bima Bharosa = IRDAI's portal, complaints tracked by IRDAI (E050) | O014–O018: useful, on the regulator's record, but not a court; that is why step four exists |
| Ombudsman: free, online, no lawyer, 18 offices, ₹50 lakh, binding; 76%; 8 in 10 within 3 months (E052–E056) | same facts, same sources; O054 reuses "8 in 10 within three months" as the honest answer to "60 days" |
| Rule three: consumables (E060) | O064 teases Episode 03 in its own words (consumables) |
| Title B / thumbnail B: "4 Steps to Get Your Money Back" | working title "… Step 4: The Insurance Ombudsman" |

## Genre and look (PLAYBOOK §5.3, its own art direction)
**Society × business & finance**, a fresh direction from Episode 01's "file at night": **"the third door"**. Daylight
Indian home and desk, the case file and a phone as the protagonists; the law appears as warm paper documents under a
forensic magnifier. Palette taken from the owner's pack graphics (G01–G08 SVGs): night navy `#0B1422` / `#14263B` (base),
signal yellow `#FFDB59` (the clocks, the money, our calculations), teal `#59DCC3` (the Ombudsman route, the rules),
paper white `#F5F7FB` and mist `#B8C7D9` (text), coral `#FF7D80` only for the cut amount and the RETURNED stamp. Fine grain, 30% vignette. Motifs: the **three doors**
(hook, O006–O009; the third door is Episode 01's lit step 4), the **two-step clock** dials (G03, chapter 3), the **document slots** (G05), the **₹5,000 meter**
counting days late (G06; no salary-attachment graphic).
Media stack: the owner's Pexels footage (F01–F20, PX01–PX15; ILLUSTRATIVE FOOTAGE on people and hospitals), the owner's
eight graphics animated in HyperFrames (static PNGs only as layout), credited captures of the Rules PDF, CIO FAQ,
portal and directory, and Bima Bharosa (focused excerpts); SIMULATION emails, letters and agreements (no real insurer,
hospital or agency names; invented numbers). Every computed number carries `OUR CALCULATION`. "Educational only, not
legal advice" on the end card and in the description. YouTube altered content = No.

## Owner decisions (2026-10-15)
1. **Voice: Akash** (ElevenLabs v4, stability 0.65, similarity 0.85, style 0.15, speaker boost), as in Episode 01.
2. **Faceless:** no host clips; desk, phone, document and footage shots carry the film.
3. Still open: the CIO tutorial video (`S09`) is reference only (no reuse licence); a fresh capture of cioins.co.in's
   public pages is used instead.

## Files
| File | What |
|---|---|
| `handoff/` | The owner's directive, audit PDF (+ text), and the asset pack's notes, registers and contact sheets |
| `script.full.tsv` | **Single source**: id, section, te (dub, empty), en (VO), emotion (empty), visual, on-screen, sound, pacing |
| `script.md`, `bunty_blocks.md`, `bunty_blocks_clean.md`, `script.tsv` | Built views (do not edit) |
| `title.txt`, `lang.txt` | Working title; `en` = English VO |
| `tools/build_script.py` | Builds the views and lints the VO (from Episode 01) |
| `tools/make_tsv.py` | One-off generator of v1 with the owner's original lines (record only) |
| `claims.csv`, `fact-check.md` | Fact-check gate (`/fact-check`, `scripts/claims_check.py`) |
| `assets/owner/` | The owner's zips, unpacked (gitignored) |

## Rebuild
```bash
python3 projects/insurance-ombudsman/tools/build_script.py     # after any edit to script.full.tsv
python3 scripts/estimate_vo.py projects/insurance-ombudsman/script.tsv
python3 scripts/claims_check.py projects/insurance-ombudsman/claims.csv
scripts/upload_gdrive.sh --sub English/insurance-ombudsman FILE   # deliveries
```
