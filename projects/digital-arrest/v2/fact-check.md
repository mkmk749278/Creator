# Fact-check: Digital Arrest v2 ("The Digital Arrest Scam Syndicate")

Checked on 2026-10-09 by an independent fact-check pass at max effort, in a fresh context. Script checked:
`v2/script.full.tsv` at commit `ec833da`, which already includes the v1 fixes (58,239; ₹1,935 crore; AUG 2024; judges'
signatures; D.K. Basu scope; tags). Every claim is in `v2/claims.csv`: **112 atomic claims**, each with a source link and a
word-for-word quote. 111 of the 112 quotes were machine-checked against the pages fetched today. The other one comes from
ThePrint, which blocks downloads, so it was read through a web extract. Memory was not used as a source.

**Gate: FAILS until 2 lines change** (V035 and V048). Both fixes are small, and the new Telugu lines are below.

| Status | Count |
|---|---|
| confirmed | 105 |
| claim (someone's claim, and the VO says so) | 5 |
| unverified | 2 |
| disputed / wrong | 0 |

## The short version

- **The new v2 material holds up.** The yearly numbers come from the Government's Rajya Sabha reply (12 Mar 2025) and the
  signed Supreme Court record (4 Aug 2026). The I4C CEO's 45% (May 2024), the UN's 1,20,000 + 1,00,000 and "victims, not
  criminals" (Aug 2023) and UNODC's "just under $40 billion" profits (Apr 2025) all check out. So do the MEA's 2,411
  repatriated and 150+ trapped (1 Jun 2026), CBI Chakra-V's 8.5 lakh mule accounts (Jun 2025), the ED money trail in
  the Oswal case and CFCFRMS's ₹11,158 crore held (to 30 Jun 2026). Arnsten (2009) and Goleman (1995) are quoted
  correctly.
- **The v1 fixes are in and correct**, including the four-year total. "Over ₹3,000 crore" for 2022–25 holds under every
  published 2025 estimate (details below).
- **Two lines say more than the sources do.**
  1. V035: money leaving the country "in minutes".
  2. V048: "nearly a week of fear without a break".
- **The ED material is presented as allegations** ("ED says", "ED alleges"). That is right: none of it has been tested in
  court yet.

## Required edits (the gate fails until these are made)

Both new lines pass the project's Bunty lint: Telugu only, no `!`, quotes or dashes, no banned words.

**1. V035: "the money crosses the border in minutes" has no source.** What the sources show is two steps:
- The money is pulled out of the mule accounts within minutes. Mumbai police (FPJ, 1 Aug 2026) say "within 15 minutes of
  the transactions". The ED says "immediate cash withdrawals".
- Then it is moved abroad through crypto or trade-based laundering (ED chargesheet, Tribune, 21 Feb 2026).

The new line:
- te: సో, ఒక్క కాల్ వెనకాల ఎంత పెద్ద నెట్వర్క్ ఉందో అర్థమైంది కదా. కాల్ చేసేవాడు ఒక దేశంలో. అకౌంట్స్ ఇంకో రాష్ట్రంలో. డబ్బు నిమిషాల్లో మాయమై, తర్వాత దేశం దాటిపోతుంది.
- en: So you can see how big a network sits behind one call. The caller in one country. The accounts in another state.
  The money vanishes within minutes, and then leaves the country.
- Sources: [FPJ, Mumbai police, 1 Aug 2026](https://www.freepressjournal.in/mumbai/mumbai-police-bust-mule-account-racket-7-arrested-10-lakh-cash-seized);
  [Tribune, ED chargesheet, 21 Feb 2026](https://www.tribuneindia.com/news/punjab/ed-files-chargesheet-against-five-in-oswal-digital-arrest-case/).
- Length: +7 characters. Block 1 goes from 4,499 to 4,506. That is just over the 4,500 target and far under the 5,000 cap.

**2. V048: "without a break" isn't in any report.** The ordeal ran from the first call on 23 Feb to the last transfer on 2 Mar.
Reports say he was under pressure "for several days" (The420.in) and kept on video calls (Newsmeter, ETV Bharat). None
says the fear or the surveillance was continuous.

The new line:
- te: ఇప్పుడు ఆలోచించండి. ఒక గంట కాదు, ఒక రోజు కాదు. రోజుల తరబడి, బెదిరింపులు, నిఘా, భయం. ఆ స్థితిలో చదువు, హోదా, అనుభవం, ఏదీ పనిచేయదు. అది వాళ్ళ బలహీనత కాదు. అది మెదడు బయాలజీ.
- en: Now think. Not one hour, not one day. Days on end of threats, surveillance and fear. In that state, education, status,
  experience, none of it works. That isn't their weakness. That's the biology of the brain.
- Sources: [The420.in, 9 Mar 2026](https://the420.in/hyderabad-retired-judge-duped-digital-arrest-cyber-fraud/);
  [Newsmeter, 9 Mar 2026](https://newsmeter.in/crime/retired-judge-in-hyderabad-duped-of-rs-166-crore-by-fake-cbi-officials-in-digital-arrest-scam-764289).
- Picture: don't run the REC counter "DAY 1 → DAY 8" as if he was recorded non-stop for 8 days. Show the calendar
  23 FEB → 2 MAR instead, or keep RECONSTRUCTION on the counter.
- Length: +8 characters (block 2 goes to 4,099).

After both edits, set rows `V2-048` and `V2-061` in `claims.csv` to `confirmed`, using the sources in their notes. Then
re-run `python3 projects/digital-arrest/tools/build_script.py projects/digital-arrest/v2` and
`python3 scripts/claims_check.py projects/digital-arrest/v2/claims.csv`.

## Figures that disagree between sources (put these in the YouTube description)

- **Total lost, 2022–25 (V019).** The official yearly figures are ₹91.14 crore (2022), ₹339.03 crore (2023) and
  ₹1,935.51 crore (2024), from the MHA reply of 12 Mar 2025. That makes ₹2,365.68 crore for 2022–24. No official full-year
  figure exists for 2025. Published estimates for 2025:
  - ₹644 crore (ThePrint, 18 Feb 2026)
  - about ₹1,585 crore (The420.in, 3 Jan 2026: 8% of ₹19,812.96 crore)
  - about ₹2,025 crore (ThePrint, 21 Feb 2026: 9% of ₹22,495 crore)

  So the four-year total is about ₹3,010–4,390 crore. **"Over three thousand crore" is safe.** Don't show an exact sum.
  "Billions" works in rupees (₹30+ billion), so keep that label in rupees, never dollars.
- **2024 loss (V018).** ₹1,935.51 crore in the Rajya Sabha reply against ₹1,918 crore in ThePrint (Feb 2026). The VO's
  "over nineteen hundred crore" and the on-screen ₹1,935 crore are fine.
- **2025 complaints (V020).** The SC record says 58,239. ThePrint misprinted 58,249 (fixed). ThePrint's earlier 17,264
  "cases" can't be a full year: the Government counted 17,718 in Jan–Feb 2025 alone.
- **UNODC $40 billion (V025).** This is UNODC's own press-release figure for the yearly *profits* of hundreds of
  industrial-scale scam centres in East and Southeast Asia. The report text says "tens of billions of dollars". It is
  not a loss figure and not India-only. UNODC's separate *loss* figure (US$18–37 billion in East and Southeast Asia,
  2023) must not be mixed in. At ₹95.92 per dollar (27 Jul 2026), just under $40 billion is about ₹3.7–3.8 lakh crore,
  so "over three lakh crore" is right.
- **Golden hour (V078).** Maharashtra's CM and an MHA official say the first hour (60 minutes). MP police say the first
  two hours. "First hour" is the common usage. The West Bengal advisory site was down today.
- **Judge case.** PTI's first report: age 69, "more than Rs one crore". Later reports: 73, ₹1.66 crore. The VO avoids the
  age; keep it that way. Only The420.in gives four transfers; v2 no longer states a count.
- **Oswal.** The fraud was 28–30 Aug 2024. ED-based reports from Oct 2026 misprint "August 2023". Police recovered
  ₹5.25 crore of the ₹7 crore, which is worth a description line.
- **Haryana.** The SC order says ₹1,05,50,000; some outlets misprinted ₹1.5 crore.

## Science and health context (description, and optional on screen)

- **Mainstream view:** acute stress impairs working memory and flexible thinking. Feeling in control protects (Arnsten,
  *Nat Rev Neurosci* 2009). A 2016 meta-analysis found impaired working memory and cognitive flexibility, with mixed
  effects on self-control (Shields et al.). The film's simplified version is fair.
- **Skeptic:** neuroscientist Joseph LeDoux (NYU) says there is no "fear centre": the amygdala detects and responds to
  threats, but the feeling of fear is assembled elsewhere. "Amygdala hijack" (Goleman, 1995) is a popular metaphor, not a
  clinical term. Add one line on this to the description. An optional SIMPLIFIED tag on the V012 brain shot would also
  help.

## Optional edits (recommended, not required)

- **V012:** "the part that controls fear" is the popular "fear centre" idea.
  - te: సైకాలజిస్ట్ డేనియల్ గోల్మన్ దీనికి ఒక పేరు పెట్టారు. అమిగ్డలా హైజాక్. భయం వచ్చినప్పుడు, మెదడులో ప్రమాదాన్ని పసిగట్టే అలారం లాంటి భాగం, ఆలోచించే భాగాన్ని పక్కకి నెట్టేస్తుంది.
  - en: … When fear strikes, the brain's alarm, the part that senses danger, pushes the thinking part aside.
- **V016 on-screen:** `39,925 COMPLAINTS · ₹91 CR · 2022 [MHA REPLY, RAJYA SABHA | MAR 2025]`. This uses the primary
  source and the same word ("complaints") as the later lines.
- **V020 on-screen:** `AWARENESS HELPED, SAYS MHA OFFICIAL [THEPRINT | FEB 2026]`. The current "AWARENESS WORKS" states
  one anonymous official's view as fact.
- **V034:** the first sentence (crypto commissions) reads as fact. To attribute all of it:
  - te: ఈ డి ఆరోపణ ప్రకారం, మ్యూల్ అకౌంట్స్ సప్లై చేసిన వాళ్ళకి కమీషన్ కూడా క్రిప్టో లోనే వచ్చింది. ఆ అకౌంట్స్ కంబోడియా, వియత్నాం లో ఉన్న వాళ్ళకి సప్లై చేశారని, నేపాల్ నుంచి ఓ టి పి లు చదివే యాప్ వాడారని కూడా ఈ డి చెప్తోంది.
  - en: According to the ED's allegations, even the commission for supplying mule accounts came in crypto. The ED also says
    the accounts were supplied to people in Cambodia and Vietnam, and that an app was used to read OTPs from Nepal.
  - This adds 31 characters to block 1, so only take it if you also trim block 1.
- **V038:** "a person tells no one" is absolute.
  - te: సిగ్గు, పరువు భయం ఉన్న చోట, మనిషి ఎవరికీ చెప్పడానికి వెనకాడతాడు.
  - en: Where there is shame and fear for one's reputation, a person hesitates to tell anyone.
  - Telangana Cyber Security Bureau SP (ETV Bharat, 21 Mar 2026) says scammers exploit the fear of losing reputation.
- **V048:** "none of it works" is stronger than the lab evidence.
  - te: ఆ స్థితిలో చదువు, హోదా, అనుభవం కూడా మనల్ని కాపాడలేకపోవచ్చు.
  - en: In that state, even education, status and experience may not protect us.
- **V053:** the order's own word is "aghast". నివ్వెరపోయింది is closer than ఆశ్చర్యపోయింది.
- **V072 on-screen:** add the two left-out sections: `BNS 316(2) · 318(4) · 319(2) · 338 · 308(2) · IT ACT 66C, 66D [TNM | MAR 2026]`.
- **V077 tag:** RBI and NPCI name AnyDesk only. TeamViewer and APK files come from police advisories (Gurugram;
  Hyderabad). Use `[RBI ALERT 1/2019 · NPCI · POLICE ADVISORIES]`.
- **V079:** under MHA's Jan 2026 SOP, banks hold the disputed amount, and freezing the whole account is the exception.
  - te: మీ కంప్లైంట్ బ్యాంకులకు వెళ్తుంది, డబ్బు చేరిన అకౌంట్స్ లో ఆ డబ్బుని హోల్డ్ చేయమని.
  - en: Your complaint goes to the banks, asking them to put that money on hold in the accounts it reached.
- **V080 tag:** `[MHA REPLY, LOK SABHA | AUG 2026]` (written reply, 11 Aug 2026). Keep "HELD (NOT ALL REFUNDED)": the SC
  record shows only ₹18.05 crore actually restored through the restoration portal.
- **Missing citation tags (charter rule):**
  - V001–V006 and V037–V043 (judge case): `[TNM · ETV BHARAT | MAR 2026]`
  - V055: `[TNM | OCT 2024]`
  - V058–V059: `[TNM · ETV BHARAT]`
  - V083: `[DoT · SANCHAR SAATHI]`

## Notes for picture and compliance

- Never show the real officer whose name was used (V040) or the then-CJI (V054). Keep the simulated search page blurred.
- V027: if Air Force repatriation footage is used, caption its real date and place.
- V056: respectful visuals only. The death is reported as a heart attack or cardiac arrest, not suicide, so the Press
  Council suicide norms don't apply. The VO doesn't claim proven causation.
- Crypto appears only as a crime route, so the SEBI finance rules don't apply. Keep "Altered content = Yes" for the
  SIMULATION scenes.

## Sources that blocked automated access (and what was used instead)

| Blocked source | Used instead |
|---|---|
| ohchr.org (403) | UN News and OCCRP |
| ThePrint (browser check) | WebFetch extracts |
| mea.gov.in (403) | ANI's direct quote of the Foreign Secretary, plus The Indian Express via a summary |
| NPCI PDF (403) | Outlook Business's reproduction of the release |
| West Bengal CSCoE (down today) | Maharashtra CM, MHA official, MP police |

Shared claims reuse the v1 check's extra sources where noted ("v1 row Cxx" in `claims.csv`): Namasthe Telangana, Sakshi
Post, NTV Telugu and Deccan Herald.
