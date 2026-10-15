# The Insurance Ombudsman (Episode 02, project code BP-HLTH-02-10M; English VO)

English explainer for *Be Practical with Kishore*, the sequel to `projects/health-claim-trap` (Episode 01). A
reimbursement claim comes back rejected or cut (₹4 lakh bill, ₹1.2 lakh paid). Families see two doors, a lawyer and
consumer court or a paid claim-recovery service; the film opens a third: the Insurance Ombudsman. It explains why Bima
Bharosa tracks but does not decide, who may file (Rule 14), the two-step clock (write to the insurer, then one month),
the one-year window and the ₹50 lakh limit, the bar on disputes pending or decided elsewhere, filing on cioins.co.in
(18 offices, documents, verification), mediation and the hearing, the award that binds only the insurer, the 30-day
compliance rule and the ₹5,000-a-day penalty, and the Bombay High Court's Dedhia judgment.

**Status (2026-10-15): phase 1, script v1 + fact-check.** Inputs from the owner (Drive `Creator/English/insurance-ombudsman/`):
`Claude.md` (the master directive and VO script, kept verbatim in `handoff/owner-directive.md`), an audit PDF
(`handoff/ombudsman-audit.*`), `BP_HLTH02_Complete_Asset_Pack.zip` (20 Pexels clips, 8 SVG/4K graphics G01–G08, official
source snapshots, and the pack's own `SCRIPT_CORRECTIONS.md`) and `Pexels_India_Footage.zip` (15 India clips). The zips'
notes, registers and contact sheets are in `handoff/asset-pack/`; the media sits in `assets/owner/` (gitignored).
No voiceover was supplied: the owner records `voice/bp-hlth02-ch1.mp3` … `ch4.mp3` from `bunty_blocks.md` after the
fact-check fixes are in.

## Script v1: what changed from the owner's text, and why
The structure, order and voice are the owner's (64 lines, 4 chapters, one ElevenLabs block per chapter, ≈ 9:30 of
speech). Formatting follows the English VO lint (no `!`, quotes, dashes or digits; hyphen-spelled acronyms as the owner
wrote them; the `[sigh]`/`[pause]`/`[slight smile]` cues moved to the pacing column). Every claim the owner's own asset
pack or the CIO pages could not support was rewritten; each change is commented in `tools/make_tsv.py`:

| Owner's line | v1 | Why |
|---|---|---|
| Win in **60 days** (title, O011) | dropped | No end-to-end deadline; Rule 17 gives the Ombudsman three months; no outcome is guaranteed |
| Lawyer fees **₹50,000**, **five years** (O006) | "pay the fees, and wait, often for a long time" | No source for either number |
| Both choices are **a trap** (O008) | "there is a third door" | A court can be the right remedy |
| **1,715** families thrown out (O011, O027) | "the one mistake that gets complaints thrown out" | Count and cause not verified at table level (fact-check may restore it) |
| 20% + GST = **nearly ₹90,000** (O020) | ₹80,000 + 18% GST = ₹94,400, labelled OUR CALCULATION | Arithmetic |
| Recovery firms **not allowed**; contracts **void** under s.23 Contract Act (O021–O023) | Rule 14(1): you, or your legal heir, nominee or assignee, file; the form is free | No decision found for the blanket s.23 claim; not every service is a scam |
| Write to the **GRO**; wait **30 days** | write to the insurer, best of all its GRO; one month | Rule 14(3) wording |
| **17** offices, assigned **automatically** by address proof (O040) | **18** offices; you choose by residence or insurer branch | Thane opened 27 Dec 2024; the portal asks you to choose |
| **One merged PDF**, **Annexure VI-A** emailed back (O042–O047) | five documents, PDF/JPG up to 10 MB each; verified, then registered | The live portal's fields and messages |
| **Over 40%** settled by mediation (O049) | "about one in three" (CIO 2024-25, 9,417 of 29,017; to be confirmed) | 40% not verified |
| **15-minute** video call, **three questions**, any language (O051–O052) | hearing in person or online; explain simply | No fixed duration or questionnaire |
| Award **100%** binding; consumer court **completely open** (O054–O056) | binding on the insurer; other remedies **may** remain | Rules and CIO wording |
| **Bank Rate + 2%**, penalty **paid straight into your account**, 50 days = ₹2.5 lakh (O057–O059) | ₹5,000 a day on top of any interest due; 10 days = ₹50,000, 30 days = ₹1.5 lakh | Interest formula not in Rule 17; no automatic credit |
| Bombay HC: penalties **from officers' salaries** (O060) | one case; costs recovered from the officers responsible, after an inquiry | Dedhia, 9 Dec 2024, was case-specific |
| Next episode: hospitals **violate** price caps (O063) | "the price caps the government has set on some of them" | No allegation in a teaser |

## Genre and look (PLAYBOOK §5.3, its own art direction)
**Society × business & finance**, a fresh direction from Episode 01's "file at night": **"the third door"**. Daylight
Indian home and desk, the case file and a phone as the protagonists; the law appears as warm paper documents under a
forensic magnifier. Palette taken from the owner's pack graphics (G01–G08 SVGs): night navy `#0B1422` / `#14263B` (base),
signal yellow `#FFDB59` (the clocks, the money, our calculations), teal `#59DCC3` (the Ombudsman route, the rules),
paper white `#F5F7FB` and mist `#B8C7D9` (text), coral `#FF7D80` only for the cut amount and the RETURNED stamp. Fine grain, 30% vignette. Motifs: the **three doors**
(hook, O005–O008), the **two-step clock** dials (G03, chapter 3), the **document slots** (G05), the **₹5,000 meter**
counting days late (G06; no salary-attachment graphic).
Media stack: the owner's Pexels footage (F01–F20, PX01–PX15; ILLUSTRATIVE FOOTAGE on people and hospitals), the owner's
eight graphics animated in HyperFrames (static PNGs only as layout), credited captures of the Rules PDF, CIO FAQ,
portal and directory, and Bima Bharosa (focused excerpts); SIMULATION emails, letters and agreements (no real insurer,
hospital or agency names; invented numbers). Every computed number carries `OUR CALCULATION`. "Educational only, not
legal advice" on the end card and in the description. YouTube altered content = No.

## Open questions for the owner
1. **Voice:** the directive names ElevenLabs **Akash** (v4, stability 0.65, similarity 0.85, style 0.15, speaker
   boost), as in Episode 01. Using Akash unless the owner says otherwise.
2. **Host clips:** the pack has no Kishore footage. 3–4 short phone clips to camera (O010–O011, O061–O064) would help;
   otherwise the film stays faceless.
3. **CIO tutorial video** (`S09`): reference only, no reuse licence. A fresh screen capture of cioins.co.in's public
   pages is safer.

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
