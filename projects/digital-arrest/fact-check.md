# Fact-check: Digital Arrest (v1 script)

Checked on 2026-10-09 by an independent fact-check pass at max effort. Script checked: `script.full.tsv` (v1) as of
commit `001017d` (06:35 UTC): 93 lines, including the new L94b. Every claim is in `claims.csv`: 84 atomic claims, each
with a source link and a word-for-word quote. Memory was not used as a source.

**Gate: FAILS until 10 rows are fixed.** That is expected: all 10 are small script or on-screen edits, listed below with
ready-to-paste Telugu lines. After the edits, those rows can be set to `confirmed` with the sources named in each row's
`note`, and `python3 scripts/claims_check.py projects/digital-arrest/claims.csv` will pass.

| Status | Count |
|---|---|
| confirmed | 70 |
| claim (said by someone, and the VO says so) | 3 |
| disputed | 1 |
| unverified | 4 |
| wrong | 6 |

## What passed

- **The numbers.** 1,23,672 complaints in 2024, a fall of more than half in 2025 and 16,377 to 30 June 2026 come from the
  signed Supreme Court record of 4 Aug 2026 (I4C Fourth Status Report). "More than 300 a day" is correct (338). "Over
  ₹1,900 crore" lost in 2024 holds under both published figures.
- **The judge case.** 23 Feb first call, Neredmet, "Deepak Kumar", the fake circle inspector, the woman who used a real
  retired IPS officer's name, the Indiranagar FIR story, the "Supreme Court warrant", the letter, "don't tell your family",
  house confinement on video, the refund promise, 25 Feb to 2 Mar, ₹1.66 crore and the Malkajgiri cyber crime police.
  Each detail has two or more independent reports (TNM, Namasthe Telangana, ETV Bharat Telugu, Newsmeter, Sakshi Post,
  NTV Telugu, The420.in).
- **Oswal and Haryana.** The fake Skype hearing, the then-CJI's name, "couldn't see his face, heard him banging a hammer"
  (his own words), the stamped order on WhatsApp, Skype on while sleeping, ₹7 crore and the "secret supervision
  account" are confirmed. So is the Haryana (Ambala) couple whose case started the Supreme Court suo motu case
  (SC order, 17 Oct 2025).
- **The playbook.** Courier, TRAI and police pretexts; parcel, SIM and money-laundering stories; studios and uniforms
  (MHA alert, 14 May 2024); "RBI account" and FD-breaking (police-sourced cases); mule-account layers; the doctor who
  died after about 70 hours (Sept 2025).
- **The law.** BNSS ss.43, 36, 48 and 58 were checked against the Gazette text and say what the script says. BNSS has no
  "digital arrest" provision (the Rajasthan High Court said so too). The Mann Ki Baat quote (27 Oct 2024) and the I4C
  advisory (Oct 2024) are correct. RBI holds no accounts for individuals.
- **The advice.** 1930, cybercrime.gov.in, Chakshu (only for suspected fraud calls, which is how the script uses it),
  keep evidence, don't install remote-access apps (RBI and NPCI warnings), and "a real case comes with a written notice".
  The Supreme Court ruled in July 2025 that police notices can't be served on WhatsApp. Court summons can legally arrive
  electronically, but only with the court seal or a digital signature, so the line still holds.

## Required edits (the gate fails until these are made)

Each new Telugu line passes the project's Bunty lint: Telugu only, no `!`, quotes or dashes, no banned words.

**1. L07: "a few days at most" is wrong.** Cases ran 14 days (Haryana couple, SC order), 18 days, 40 days and over six
months.
- te: జీవితమంతా కష్టపడి దాచుకున్న డబ్బు, కొన్ని రోజుల్లో, కొన్నిసార్లు కొన్ని గంటల్లోనే, మాయం.
- en: Money saved over a whole lifetime, gone in a few days, sometimes in just a few hours.
- Source for "hours": Mangaluru police case, money sent within 5 hours of the call (Deccan Herald, 31 Oct 2025).

**2. L17, on-screen only: 58,249 is a typo.** The signed SC order says 58,239. ThePrint misprinted it, and the script
copied ThePrint.
- On-screen: `58,239 · 2025 [I4C STATUS REPORT | SUPREME COURT, AUG 2026]`. The VO is unchanged.

**3. L33: "career" has only one source** (Newsmeter). Every other report says reputation.
- te: అరెస్ట్ అయితే మీ పరువు, ప్రతిష్ఠ, అంతా పోతుంది అని భయపెడతారు.
- en: They threaten that if he's arrested, his reputation and good name will all be gone.

**4. L35: "four transfers" has only one source** (The420.in). The dates are confirmed by The420.in and ETV Bharat. TNM,
which the tag cites, gives neither the dates nor the count.
- te: ఫిబ్రవరి ట్వెంటీ ఫిఫ్త్ నుంచి మార్చ్ సెకండ్ వరకు, కొన్ని ట్రాన్స్ఫర్స్ లో, వన్ క్రోర్ సిక్స్టీ సిక్స్ లాక్స్ పంపేశారు.
- en: From February twenty-fifth to March second, in several transfers, he sent one crore sixty-six lakh.
- On-screen: `TRANSFERS · 25 FEB–2 MAR · ₹1.66 CR [THE420.IN · ETV BHARAT | MAR 2026]`

**5. L36: "they went silent" has no source.** No report says it.
- te: రిఫండ్ రాలేదు. అప్పుడు అర్థమైంది, ఇది స్కామ్ అని.
- en: The refund never came. That's when it sank in: it was a scam.

**6. L37, on-screen only: the PTI tag is wrong.** PTI's report names no police unit; it also says age 69 and "more than
Rs one crore".
- On-screen: `CCS MALKAJGIRI [THE NEWS MINUTE · NAMASTHE TELANGANA | MAR 2026]`. The VO is unchanged.

**7. L47, on-screen only: "SEPT 2024" is wrong.** The fraud happened on 28–30 Aug 2024, and the cited articles are
from 1 Oct 2024.
- On-screen: `₹7 CRORE · AUG 2024 [BAR & BENCH · BUSINESS STANDARD | OCT 2024]`. The VO is unchanged.

**8. L49: "one judge's signature" is wrong.** The SC order says "forged signatures of Judges". The amount was
₹1,05,50,000, so "over" is added.
- te: హర్యానా లో ఒక వృద్ధ దంపతులకి, సుప్రీం కోర్ట్ పేరుతో, జడ్జి ల సంతకాలు ఫోర్జ్ చేసిన ఆర్డర్స్ చూపించి, వన్ క్రోర్ ఫైవ్ లాక్స్ కి పైగా కొట్టేశారు. ఆ కేస్ తోనే సుప్రీం కోర్ట్ ఈ స్కామ్ ని సుమోటో గా తీసుకుంది.
- en: In Haryana, an elderly couple was shown orders in the Supreme Court's name with judges' forged signatures, and
  robbed of over one crore five lakh. That case is what made the Supreme Court take up this scam on its own.

**9. L72: D.K. Basu is not the source of all five rules.**
- D.K. Basu (18 Dec 1996) gave rules 2–4: name badge, attested arrest memo, and telling a relative.
- Rule 1 (touch or confine) is the old CrPC s.46.
- Rule 5 (24 hours) is CrPC s.57 and Article 22(2) of the Constitution (PIB's CrPC-to-BNSS comparison).

The new line:
- te: నేమ్ బ్యాడ్జ్, అరెస్ట్ మెమో, ఫ్యామిలీ కి చెప్పడం, ఈ రూల్స్ సుప్రీం కోర్ట్ ఇచ్చిన డి కె బసు జడ్జిమెంట్ నుంచి వచ్చాయి. ఇప్పుడు అవి చట్టంలోనే ఉన్నాయి.
- en: The name badge, the arrest memo, telling your family: these rules came from the Supreme Court's D K Basu judgment.
  Today they are written into the law itself.

Optional extra sentence:
- te: ట్వెంటీ ఫోర్ అవర్స్ రూల్ అయితే మన రాజ్యాంగంలోనే ఉంది.
- en: And the twenty-four-hour rule is in our Constitution itself.

**10. L74, on-screen only: the I4C part of the tag is unsupported.** The I4C advisory only says "no arrest on video
call". The money point comes from the RBI and police.
- On-screen: `MONEY DEMAND = SCAM [RBI · POLICE ADVISORIES]`. The VO is unchanged.

## Disputed and conflicting figures (put these in the YouTube description)

- **2024 loss.** ThePrint (Feb 2026) gives ₹1,918 crore. The Government's own Rajya Sabha reply (12 Mar 2025) gives
  ₹1,935.51 crore. The VO's "over ₹1,900 crore" is right either way. **Recommended:** change the L15 on-screen text to
  `₹1,935 CRORE · 2024 [MHA REPLY, RAJYA SABHA | MAR 2025]` (the official figure).
- **2025 complaints.** ThePrint (Feb 2026) printed 17,264. That can't be a full-year count: the Government told
  Parliament that 17,718 cases were reported in Jan–Feb 2025 alone. The signed SC record (58,239) is used.
- **Judge's age and amount.** PTI's first report said 69 and "more than Rs one crore". Later reports say 73 and ₹1.66
  crore. The VO avoids the age; keep it that way.
- **Haryana amount.** The Week and ETV Bharat misprinted ₹1.5 crore. The SC order says ₹1,05,50,000.

## Recommended (optional) edits

- **L59: "చాలావరకు" means "mostly".** The MHA official's words were "Many of these scam calls...", which is also what the
  English column says. Suggested te: ఈ కాల్స్ లో చాలా, కంబోడియా, మయన్మార్, థాయ్లాండ్ లాంటి దేశాల్లోని స్కామ్ సెంటర్స్ నుంచి వస్తున్నాయని అధికారులు చెప్తున్నారు.
  (The I4C CEO's own list was Cambodia, Myanmar and Laos.)
- **L62 tag.** No MHA or I4C source says "not in law". Use `[BNSS 2023 | RAJASTHAN HIGH COURT, JAN 2025]`.
- **L17 VO attribution**, given the conflicting ThePrint figure. Suggested te: ఇక్కడ ఒక గుడ్ న్యూస్ కూడా ఉందండి. సుప్రీం కోర్ట్ కి ఇచ్చిన ఐ ఫోర్ సి రిపోర్ట్ ప్రకారం, ట్వెంటీ ట్వెంటీ ఫైవ్ లో కంప్లైంట్స్ సగానికి పైగా తగ్గి, ఫిఫ్టీ ఎయిట్ థౌసండ్ కి వచ్చాయి.
- **L52: "within minutes" is rhetoric, not a measured figure.** In the Mangaluru case the scam fell apart about an hour
  after the victim told a neighbour. Softer te if wanted: ఫ్యామిలీ కి ఎందుకు చెప్పొద్దంటారో తెలుసా. మీరు మీ అబ్బాయికో, ఒక ఫ్రెండ్ కో ఒక్క కాల్ చేస్తే చాలు, చాలాసార్లు ఈ స్కామ్ అక్కడే బయటపడుతుంది.
- **Missing citation tags (charter rule).** Add tags to these factual lines:
  - L24–L34: `[TNM · NAMASTHE TELANGANA | MAR 2026]`
  - L41–L43: `[MHA ALERT | MAY 2024]`
  - L51: `[TNM · MONEYLIFE | 2024]`
  - L56–L58: e.g. `[DECCAN HERALD | OCT 2025]`
  - L85: `[DoT · SANCHAR SAATHI]`
- **L72 tag.** The 1996 date is correct (judgment 18 Dec 1996, reported (1997) 1 SCC 416).

## Notes for picture and description

- **L49:** the Ambala stock is right (PTI: "a senior citizen couple in Haryana's Ambala").
- **L29 and L47:** never show the real officer's or the CJI's face.
- **L51:** the REC timer at 47 hours fits "digital arrest for two days" (Business Standard).
- **Oswal recovery:** police recovered ₹5.25 crore of his ₹7 crore. Not in the VO, but worth a description line next
  to L60 ("getting it back is very hard").
- **L54:** reports say "heart attack" or "cardiac arrest". The link to the scam rests on the family's complaint and the
  police's culpable-homicide charge. The VO doesn't overclaim.
- **Block length:** the required edits add 36 characters net (L72 +53, L49 +9, L07 +5, L35 +2, L33 −7, L36 −26).
  Re-run `tools/build_script.py`; the README says block 2 is already over the 5,000 cap.

## v2 (`v2/script.full.tsv`): same problems, not yet checked

v2 repeats several v1 issues. Apply the same fixes there:
- V007: four transfers
- V018: the VO says "nineteen hundred and eighteen crore". This is disputed: say "over nineteen hundred crore" or use
  the ₹1,935 crore official figure.
- V020: 58,249 should be 58,239
- V032: SEPT 2024 should be AUG 2024
- V044: four transfers, "went silent", and a tag that cites TNM for the dates
- V052: one judge's signature, and ₹1.05 crore should be "over"
- V057: "career"
- V061: tag
- V069: D.K. Basu covering all five rules
- V071: I4C tag

v2's new claims have **not** been fact-checked: the ED money trail and crypto, the I4C CEO's 45%, OHCHR, UNODC, MEA
repatriations, CBI Chakra-V, CFCFRMS ₹11,158 crore, Arnsten 2009, Goleman 1995. v2 needs its own fact-check pass before
recording.
