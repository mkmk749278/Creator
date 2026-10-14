# The Health Insurance Claim Rejection Trap (Episode 01, project code BP-HLTH-01-10M; English VO)

English explainer for *Be Practical with Kishore*, built from the owner's master handoff (`handoff/master-handoff.pdf`,
text in `handoff/master-handoff.txt`, 2026-10-14). The film covers a night-time cashless denial at a hospital billing
counter, why a cashless "no" is not a claim rejection, who a TPA really is (a private company the insurer hires, and one
that cannot reject a claim on its own: IRDAI requires the insurer's Claims Review Committee to approve every rejection),
the three most common denial reasons (including the proportionate room-rent deduction, worked out on a whiteboard), the
IRDAI 60-month moratorium and the 1-hour and 3-hour cashless rules, the four-step fight-back plan (papers → reimbursement
and grievance officer → Bima Bharosa → Insurance Ombudsman, with real CIO 2024-25 outcome data), and three rules to apply
before buying or renewing.

**Status (2026-10-14): phase 1, script v2.** The owner sent "Master Handoff & Fixes" (`handoff/master-handoff-fixes.*`):
their own rewrite of the VO in 4 chapter files, hyphen-spelled acronyms (I-R-D-A-I, T-P-A, c-i-o-i-n-s) so Akash does not
say "Ir-dye", and audio cues `[sigh]`, `[pause]`, `[slight smile]`. v2 (`script.full.tsv`, ids E001–E064) keeps their
text word for word except formatting (no `!`, quotes, long dashes) and 19 sentences corrected (16 after the first check, 3 more after the v2 re-check) against `claims.csv`
(list below; each is commented in `tools/make_tsv_v2.py`). 4 chapter blocks, about 8,000 characters and 9:25 of speech plus
the two 3 s pauses and music beats; lint clean. v1.1 is kept in `v1/`. Next: the owner records
`voice/bp-hlth01-ch1.mp3` … `ch4.mp3`, then timing, sourcing and the EDL.

### v2: the owner's sentences changed, and why
| Line | Owner's v2 text | Now | Source |
|---|---|---|---|
| E009 | a rule that makes **most** of these rejections illegal | makes **this exact denial** illegal, once your policy has crossed five years | Moratorium covers non-disclosure after 60 months only (HC-08) |
| E036 | Your normal policy limits still apply | limits **and exclusions** still apply | IRDAI's CIS format: after the moratorium a claim can still fail on proven fraud and permanent exclusions (HC-39) |
| E047 | within fifteen to thirty days | … of discharge. Check your policy for your exact limit. | Limits differ by policy (HC-16) |
| E011 | get your money back **within sixty days** | get your money back | No source; Ombudsman closes 8 in 10 within three months (HC-27) |
| E015 | a **private corporate agency** … let's be honest about corporate incentives | a company hired and paid by the insurance company | One TPA is owned by state insurers (HC-03b) |
| E016 | TPA staff … default reaction … quick cashless denial letter | about seven out of every ten health claims are settled through T-P-As | No source for the old line; IRDAI annual report 2024-25: 69% (HC-35) |
| E021 | But they use it anyway to deny your payout | in the first five years the company can still use it; after five years the rule changes | Non-disclosure is a lawful ground before 60 months (HC-08) |
| E025 | a cut of about 37% **across your entire bill** | on those charges | Only room-linked charges are cut; medicines are exempt in every current wording (HC-09, HC-10) |
| E033 | cannot question … non-disclosure **or pre-existing diseases** | non-disclosure, like an old disease you did not mention | The clause covers non-disclosure and misrepresentation (HC-08) |
| E035 | proven **criminal** fraud … establish **in court** | proven fraud that the company has to establish | "except for established fraud"; no court in the rule (HC-36) |
| E039 | officially uploads the **complete final bill** … within **exactly** three hours | sends the final discharge request … within three hours | Circular para 16: "receipt of discharge authorization request" (HC-15) |
| E040 | any extra **room rent** | any extra amount | "the additional amount if any charged by the hospital" (HC-15) |
| E048 | **Principal Nodal Officer, the P-N-O**; always quote the moratorium | Grievance Redressal Officer; quote it if your policy has crossed five years | PNO is a bank term; insurers name a Grievance Redressal Officer (HC-17) |
| E050 | tracked directly by **government authorities** | tracked directly by the I-R-D-A-I | Bima Bharosa is IRDAI's portal (HC-18) |
| E052 | do NOT go to a consumer court, do NOT hire a lawyer | you do NOT need a consumer court case or an expensive lawyer | Consumer court stays open to the policyholder (HC-30) |
| E055 | the Ombudsman **resolved** over 32,000; over 75% **of decided cases** | offices **received** over 32,000; **of the cases they settled or decided**, over 75% | 32,503 received, 29,017 disposed (HC-25); 76% counts mediated settlements, which the Rules do not call decisions (HC-40) |
| E059 | **saving two thousand rupees** … can cost you sixty thousand | In our example, one bigger room cost almost sixty thousand rupees | No source for the premium saving; ₹59,625 is our worked example (HC-09) |
| E060 | 5–15% … an add-on of **₹500–800 covers them completely** | **Reports say** 5–15% … some insurers sell an add-on; check its price and its limit | Estimates vary (HC-33b); no source for the price; riders have caps, e.g. ₹1,500 a year for up to ₹15,000 |

Still in the owner's packaging, and wrong: title option 1 ("Why 80% … get rejected": IRDAI 2024-25 has about 8%
repudiated, 87% settled), the description's "how TPAs profit from denial letters" and "within 60 days", and the
thumbnail's "OVERTURN IT IN 60 DAYS". Option 2 or 3 is safe. BGM: the handoff repeats −18 to −22 dB; the charter's
−24 to −26 dB is the stricter rule and stays unless the owner says otherwise.

### v1 (for the record)
## What changed from the handoff (and why)
The structure, voice and most lines are the owner's. These changes follow the sources (`claims.csv`):
| Handoff | Script v1 | Why |
|---|---|---|
| Title option "Why 80% of Health Insurance Claims Get Rejected" | not used | False: IRDAI's FY 2023-24 data has about 82% of health claims settled. A title the film contradicts breaks §4a |
| "Over 75% of disputes decided in favour of the consumer" | "Of the cases they settled or decided, about three out of four went in favour of the policyholder" | True for FY 2024-25 health complaints only when you count mediation settlements + awards against all decided cases (15,543 of 20,440 = 76%, `tools/claim_math.py`); it is about 54% of all disposed complaints |
| "Binding award … within 60 days" | "About eight out of ten complaints were closed within three months"; insurer pays within 30 days or ₹5,000 a day | CIO 2024-25: 78.5% within 3 months. 30 days + ₹5,000/day = Master Circular para 20 |
| "Only exception … prove in a court of law that you committed criminal fraud" | "Proven fraud … that the company has to establish" | The clause says "except for established fraud"; no court is mentioned |
| "After five years they cannot reject your claim because of an old medical history" | adds: normal limits and exclusions still apply; port, don't cancel | The moratorium covers non-disclosure and misrepresentation only; ported credits count (para 13 note) |
| TPAs "operate under volume-based metrics … to protect payout ratios" | TPA is a private company hired and paid by the insurer; IRDAI bars TPA pay linked to claims ratio; rejection needs the insurer's committee | The handoff claim had no source; IRDAI's own rule says the opposite about pay. Mechanism, not villain (§4a) |
| Room rent: "they cut forty percent off your entire surgery, doctor fees, and nursing" | 5/8 paid on surgery, doctor and nursing too, about 37% cut; many policies exempt medicines, some also implants and tests: check your wording | The exact maths; IRDAI's 2020 exemptions were repealed in May 2024, so current policy wordings decide |
| Insurer resolves a grievance in "exactly fifteen days" | 14 days | IRDAI Policyholders' Interests master circular, 5 Sep 2024 |
| Consumables rider "₹500–800 a year"; "₹30–40 thousand of the bill" | "Reports say" 5–15% of a bill; some insurers sell an add-on | No source for the handoff numbers; guides give 5–15%; one insurer's rider is ₹1,500 a year |
| "Ombudsman … decides within 60 days", "file online in less than five minutes" | removed | No source |
| BGM −18 to −22 dB | −24 to −26 dB under speech | The charter's sound matrix (stricter) wins (PLAYBOOK Part B intro) |
| 3.0 s VO silences at 04:45 and 08:35 | kept as `VO_PAUSE` 3.0 s after H035 and H058 | The owner asked; music still goes silent for 1.5 s before the core reveal (H036) |
| "I-R-D-A-I", "P-N-O", "I-C-R" | IRDAI; "grievance officer"; papers named in plain words | Dashes are banned in TTS text; simpler words (§4a-2) |

## Genre and look (PLAYBOOK §5.3, its own art direction)
**Society × business & finance.** Art direction **"the file at night"**: a hospital at 9 PM, where the case file is the
protagonist. The owner's palette: carbon slate `#0F172A` (night), analytical cyan `#0284C7` (the law, our proof), amber
caution `#F59E0B` (clocks, TPA, warnings), warning crimson `#DC2626` (only the denial stamp and the myths), crisp white
`#F8FAFC` (text). Fluorescent-corridor light, fine grain, 30% vignette; from chapter 4 ("Before you buy") the film
moves into daylight. Motifs:
- the red **CASHLESS DENIED stamp** that cracks under a cyan **NOT A CLAIM REJECTION** overstamp (hook, H009) and is
  struck through in gold by the moratorium clause (H037);
- the **60-month ring** (96 segments, 36 fall away) that closes around the hook family's six years (H040);
- the amber **discharge clock** (1 hour, then 3 hours);
- the **four-step staircase** in the lower-left corner through chapter 3; the case-file **tabs** for reasons and rules.
Media stack: real Indian hospital b-roll (Pixabay API, Commons), credited screen recordings of the IRDAI circular PDF
(forensic magnifier, gold highlighter on the exact words), cioins.co.in and Bima Bharosa; SIMULATION letters, bills and
forms (no real hospital, insurer or TPA name); BOARD whiteboard (`video/lib/whiteboard`) for the room-rent maths and the
76% calculation; split-screen myth (red) vs rule (cyan) cards limited to 2–4-word tags. Every computed number carries
`OUR CALCULATION · …`. "Educational only, not insurance advice" on the end card and in the description. YouTube altered
content = No (no realistic synthetic real events).

## Open questions for the owner
1. **Voice:** the handoff names ElevenLabs **Akash** (v4, stability 0.65, similarity 0.85, style 0.15, speaker boost).
   CLAUDE.md still says Bunty is the channel voice. Using Akash for this film, as the handoff says, unless the owner
   says otherwise.
2. **Studio presence:** the handoff wants Kishore on camera holding a discharge summary and the circular. Either the
   owner films 3–4 short pieces to camera on the phone (E010–E011, E028, E061–E064), or the film stays faceless with
   desk-and-document shots. AI images of the owner (the handoff's thumbnail prompt) are not allowed (§12); the thumbnail
   should use a real photo.
3. **Headline split-screens** ("CASHLESS DENIED!", "INSURANCE SCAM!"): only real, credited headlines, never mock-ups that
   look like a real outlet.

## Files
| File | What |
|---|---|
| `handoff/` | The owner's master handoff and the fixes version (PDF + text), verbatim |
| `v1/` | Script v1.1 and its claims, before the owner's v2 |
| `script.full.tsv` | **Single source**: id, section, te (dub, empty), en (VO), emotion (empty), visual, on-screen text, sound, pacing |
| `script.md`, `bunty_blocks.md`, `bunty_blocks_clean.md`, `script.tsv` | Built views (do not edit) |
| `tools/build_script.py` | Builds the views and lints the VO (copied from minimum-due) |
| `tools/claim_math.py` | The room-rent maths and the CIO percentages, reproducible |
| `tools/make_tsv.py`, `tools/make_tsv_v2.py`, `tools/draft_claims.py` | One-off generators of v1, v2 and the draft claims (record only) |
| `claims.csv`, `fact-check.md` | Fact-check gate (`/fact-check`, `scripts/claims_check.py`) |
| `sources/` | Renders of the scanned CIO 2024-25 Statement H3 table used for the numbers |

## Rebuild
```bash
python3 projects/health-claim-trap/tools/build_script.py      # after any edit to script.full.tsv
python3 projects/health-claim-trap/tools/claim_math.py
python3 scripts/estimate_vo.py projects/health-claim-trap/script.tsv
python3 scripts/claims_check.py projects/health-claim-trap/claims.csv
```

## Sources used by the writer (the fact-check re-verifies)
- IRDAI Master Circular on Health Insurance Business, IRDAI/HLT/CIR/PRO/84/5/2024, 29 May 2024: para 13 (moratorium),
  15 (1-hour cashless), 16 (3-hour discharge, shareholders' fund), 17 (Claims Review Committee, clause-level reasons,
  insurer/TPA collect documents), 20 (30-day award compliance, ₹5,000/day), Chapter II B (TPA pay not linked to ICR).
- Council for Insurance Ombudsmen Annual Report 2024-25 (`cioins.co.in/annualreports/AnnualReport2024-2025.pdf`),
  Statement H3, health insurance: received 32,503; recommendations 9,417; awards for complainant 6,126; awards for
  insurer 4,897; withdrawn 3,649; non-entertainable 4,928; disposed 29,017; within 3 months 22,791. The 2023-24 report
  gives 31,490 received, 10,140 / 6,235 / 4,125 (80% for the policyholder on the same method).
- cioins.co.in: no fee; compensation up to ₹50 lakh; escalate if unresolved after 30 days; within one year.
- Proportionate deduction method: current Arogya Sanjeevani wordings (Go Digit 2026, IFFCO-Tokio 2024). The IRDAI 2020
  guidelines exempting pharmacy, implants, diagnostics and ICU were repealed by the 29 May 2024 master circular.
- IRDAI annual report FY 2023-24 via Outlook Business, Moneylife and Business Standard: about 82% of health claims settled;
  ₹10,937 crore repudiated (9.34% by value).
