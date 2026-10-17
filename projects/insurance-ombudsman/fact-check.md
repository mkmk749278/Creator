# Fact-check: The Insurance Ombudsman (Episode 02)

Independent full pass, 2026-10-15 (there was no draft `claims.csv`). Checked: `script.full.tsv` v1.2 (O001–O065,
regenerated 05:37, md5 `c80e681d`), `title.txt`, and the owner's titles in `handoff/owner-directive.md` PART 4.
Every row in `claims.csv` names its source. 33 of the 37 quotes were machine-checked word for word against copies
fetched this pass. The other 4 come from the scanned CIO annual report tables and the OCR'd 2023 amendment, and were
read from the page images (saved in `sources/`). The owner's copies of the Rules (S01) and the CIO annual report (S02)
are byte-identical to the live cioins.co.in files, and S03–S07 match the live pages.

## Summary

- **Gate:** `37 claims: confirmed 37`, passed. **It passes on the corrected wording.** Eight rows (IO-06, IO-10,
  IO-13, IO-23, IO-27, IO-29, IO-31, IO-36) describe the replacement text below, not what `script.full.tsv` says
  today. Make the eight changes, then re-run the gate and re-check only those lines.
- **What holds (no change needed):**
  - **Rules:** who may file (Rule 14(1)); the two-step clock and its one month (Rule 14(3)); the one-year window; the
    ₹50 lakh limit, raised from ₹30 lakh by G.S.R. 828(E) of 9 Nov 2023; the binding award (Rule 17(8)).
  - **IRDAI circulars:** the 14-day grievance rule (Policyholders' Interests master circular, 2024). The 30-day
    compliance rule, the ₹5,000 a day and "on top of interest" (health master circular para 20 and IRDAI health FAQ 45).
  - **Offices and portal:** 18 offices, Thane the 18th from 27.12.2024; you choose by where you live or the insurer's
    office. The form: Register Complaint, OTP, PDF/JPG up to 10 MB each, "verified, then registered". Filing is free.
  - **Middlemen and the court case:** recovery firms charging 20% plus GST (Insurance Samadhan publishes exactly
    this). The Dedhia judgment as worded.
  - **Our sums:** 4,50,000 − 1,20,000 = 3,30,000; 66,000 + 18% = 77,880; 9,417 / 29,017 = 32.5%;
    22,791 / 29,017 = 78.5%; 10 and 30 days × ₹5,000.
- **What must change (8 items, details below):**
  1. The ₹5,000-a-day penalty has an exception: none if the insurer appeals the award within 30 days (O010, O059).
  2. O014's "Many families stop there … not enough" has no source. IRDAI's own 2025-26 data: 63% of complaints
     closed on Bima Bharosa were settled in the policyholder's favour.
  3. The 18% GST rate must be labelled as assumed (O021 on screen).
  4. The bar on cases pending or decided elsewhere is Rule 14(5), not 14(3) (O037 tag).
  5. Hearing and mediation are in the wrong order, and O051 ("often … pays before any hearing") has no source. The
     CIO's own figures show every complaint it takes up is closed through a hearing. "Last year" is stale: the data is
     2024-25.
  6. "Eight out of ten closed within three months" holds only for complaints that were closed (O054).
  7. See 1 (O059).
  8. There are no "price caps" on gloves, masks or syringes, only a 10%-a-year limit on price rises (O064).
- **Bima Bharosa, exactly** (IRDAI's own pages, IO-12 to IO-14):
  - It is IRDAI's complaint portal: "a gateway to register complaints with insurance companies".
  - A complaint "will flow to the insurance company's system as well as the IRDAI repository".
  - The insurer must "attend to it within two weeks", or 14 days under the 2024 circular.
  - IRDAI monitors, and on escalation "shall facilitate re-examination of the complaint and resolution by the
    insurance company".
  - The insurer closes the complaint if you do not come back within 8 weeks. If you are not satisfied, you "may
    approach the Insurance Ombudsman or the appropriate legal authority".
  - No IRDAI page says IRDAI or Bima Bharosa decides a claim or orders payment. "Useful, on the regulator's record,
    the company must answer, but it does not decide" is right.
- **The owner's 1,715 is real** (IO-11). CIO Annual Report 2024-25, Statement H8: of 32,503 health complaints
  received, 4,928 were not taken up. 1,715 of them were "Customer Not represented to Ins. Co. [14(3)(a)]": the person
  had not complained to the insurer first. In 2023-24 the figure was 3,869 of 6,699. One caution: in 2024-25,
  "Not within Jurisdiction [14(1)]" was slightly larger (1,781).
- **New since June 2026, found this pass:**
  - **Lawyers at the Ombudsman.** The 2026 ruling is the **Karnataka** High Court, not Kerala ("KHC" is Karnataka's
    neutral-citation code; Kerala's is "KER"). Division Bench, 1 July 2026, WA 1534/2026, 2026:KHC:32548-DB, not
    16 July. Once a case reaches the Rule 17 award stage, the complainant may bring an advocate; there are no lawyers
    at the mediation stage. It follows the Telangana High Court (2023). It is not in the script; IO-37 is ready if
    it is added.
  - **IRDAI consultation paper (23 Sep 2026), para 58, figures for 2025-26:** 63% of Bima Bharosa complaints, 75%
    at the Ombudsman and 54% in consumer forums and courts went the policyholder's way.
  - **The Ombudsman Rules are unchanged since 9 Nov 2023.** The draft 2025 amendment (G.S.R. 864(E)) was still not
    notified at the end of September 2026.
  - The CIO FAQ still says "17 offices". It is out of date: the directory and the annual report say 18.
- **The owner's audit PDF, checked** (none of these points is in the script now):
  - Wrong or unsupported:
    - The Section 23 Contract Act "void" claim has no supporting decision.
    - "17 centres" is out of date (18 since 27 Dec 2024).
    - Dedhia was pronounced on **9** December 2024, not 10.
    - The pending-or-decided bar is Rule 14(5); "Rule 14(3)(c)–(d)" does not exist.
  - Right, with a correction: "Bank Rate + 2%" is real, but it comes from the 2024 Policyholders' Interests master
    circular, para 25.2, not from Rule 17(7) itself (IO-33).
  - Right: its 1,715, 27,575 and 26,507 match Statement H8. Its health totals (32,655 received, 29,156 disposed,
    8,429 pending) come from the CIO's centre-wise Statement H2. The film and Episode 01 use the company-wise
    Statement H3 (32,503; 29,017; 8,414). The two CIO tables differ by under 1%, and both give "about one in three"
    and "about eight in ten" (`sources/cio-2024-25-H2-…jpg`).
- **Line ids:** the brief used v1 ids. In v1.2:
  - Bima Bharosa is O014–O017; Rule 14(1) is O022; the clock is O025–O037; GST is O021; consumer court is O007.
  - Offices are O041; filing is O039–O048; mediation and hearing are O050–O052; "eight in ten" is O054.
  - Rule 17 is O056–O057; the penalty is O058–O060; Dedhia is O061; next episode is O064.

## Script changes required (gate-blocking)

1. **O010 VO** (appeal exception):
   - Now: `And if the company pays that award late, it has to pay you a penalty of five thousand rupees for every day of delay.`
   - New: `And if the company does not challenge the award, but pays it late, it has to pay you a penalty of five thousand rupees for every day of delay.`
   - Reason: Policyholders' Interests master circular, 5 Sep 2024, Part B VI.4(iv): "This provision will not be
     applicable in case insurer chooses to appeal against the award of the Insurance Ombudsman within 30days."
     Episode 01 made the same fix (IO-10).
2. **O014 VO:**
   - Now: `Many families stop there, and here is why that is not enough.`
   - New: `It often works. But if it does not work for you, do not stop there.`
   - On screen, add the source for "often works":
     `STEP 3 · bimabharosa.irdai.gov.in · 63% SETTLED FOR THE POLICYHOLDER, 2025–26 [IRDAI CONSULTATION PAPER | 2026]`.
   - Reason: there is no source for "many families stop there". IRDAI says 63% of complaints closed on Bima Bharosa
     in 2025-26 were settled in the policyholder's favour, so "not enough" as a general rule is wrong. O015–O017 still
     work as the "if it doesn't" case (IO-13).
3. **O021 on screen** (GST label):
   - Now: `₹66,000 FEE + 18% GST = ₹77,880 · OUR CALCULATION`
   - New: `₹66,000 FEE + 18% GST (ASSUMED) = ₹77,880 · OUR CALCULATION`
   - Reason: the firms quote only "plus applicable GST". 18% is the standard rate for professional services (CBIC,
     Heading 9983); applying it here is our assumption (IO-06).
4. **O037 on screen** (rule number):
   - Now: `PENDING OR DECIDED ELSEWHERE = NOT ALLOWED [RULE 14(3)]`
   - New: `PENDING OR DECIDED ELSEWHERE = NOT ALLOWED [RULE 14(5)]`
   - Reason: Rule 14(5) holds this bar: "proceedings are pending before or disposed of by any court or consumer forum
     or arbitrator". The VO is right (IO-23).
5. **O050–O052** (hearing first, mediation through it, award if no settlement; correct year; cut the unsourced line):
   - **O050**
     - Now: `Many complaints end in mediation under Rule sixteen. The Ombudsman suggests a fair settlement, and if both sides agree, the case closes. Last year, about one in three health complaints that were closed, ended this way.`
     - New: `The Ombudsman hears both sides, you and the company. The hearing can be in person, or online by video.`
     - Takes O052's picture and `ILLUSTRATIVE HEARING`.
   - **O051**
     - Now: `Often, once the Ombudsman's notice reaches the insurer, the company agrees to pay before any hearing takes place.`
     - New: `Many complaints end in mediation under Rule sixteen. The Ombudsman suggests a fair settlement, and if both sides agree, the case closes. In twenty twenty-four to twenty-five, about one in three health complaints that were closed, ended this way.`
     - Takes O050's picture and `≈ 1 IN 3 · OUR CALCULATION [CIO ANNUAL REPORT | 2024–25]`.
   - **O052**
     - Now: `If there is no settlement, there is a hearing. It can be in person, or online by video.`
     - New: `If there is no settlement, the Ombudsman decides the case, and passes an award.`
     - Picture: the G04 award panel, or the S01 Rules p11 award clause.
   - Reasons:
     - O051 has no source. In the CIO Annual Report 2024-25, every centre's brief review shows 100% of complaints it
       took up closed "through online hearing" or "off line hearing", with mediation as a share of them. Ahmedabad:
       91% online, 9% offline, 35.70% by mediation (`sources/cio-2024-25-brief-review-…jpg`).
     - So the hearing comes first in every case taken up, and settlements are reached through it. Rule 15(4): the
       Ombudsman disposes of a complaint "after giving the parties … a reasonable opportunity of being heard".
     - "Last year" is wrong in a late-2026 film. 2024-25 is the latest CIO report; none newer is on cioins.co.in today.
     - See IO-27 to IO-29. O053 ("You don't need fancy legal words…") reads best right after the new O050 (optional move).
6. **O054 VO and on screen** (what the eight in ten counts):
   - Now: `In twenty twenty-four to twenty-five, about eight out of ten health complaints were closed within three months.`
   - New: `Of the health complaints the Ombudsman closed in twenty twenty-four to twenty-five, about eight out of ten were closed within three months.`
   - On screen, now: `8 IN 10 WITHIN 3 MONTHS [CIO ANNUAL REPORT | 2024–25]`; new: `8 IN 10 CLOSED CASES · UNDER 3 MONTHS [CIO ANNUAL REPORT | 2024–25]`.
   - Reason: health and year are right (Statement H3: 22,791 of 29,017 disposed = 78.5%). But the base is complaints
     closed, as the CIO itself states it. 8,414 were still open at year end, 4,826 of them already past three months.
     Of all 37,431 complaints handled, 61% were closed within three months (IO-31).
7. **O059 VO and on screen** (appeal exception):
   - Now: `If it is late, it must pay you a penalty of five thousand rupees for every day of delay, on top of any interest that is due.`
   - New: `If it is late, and it has not challenged the award within those thirty days, it must pay you a penalty of five thousand rupees for every day of delay, on top of any interest that is due.`
   - On screen, now: `₹5,000 / DAY [IRDAI HEALTH FAQ 45]`; new:
     `₹5,000 / DAY · NOT IF CHALLENGED IN 30 DAYS [IRDAI HEALTH FAQ 45 · POLICYHOLDERS' INTERESTS MASTER CIRCULAR | 2024]`.
   - Reason: as in 1 (IO-10). O060's sums stay right.
8. **O064 VO** (no caps on gloves, masks or syringes):
   - Now: `…look at what we pay for surgical consumables, and the price caps the government has set on some of them.`
   - New: `…look at what we pay for these consumables, and what the government's price rules say about them.`
   - Reason: ceiling prices exist only for a few devices: coronary stents and knee implants (PIB, Rajya Sabha reply,
     17 Mar 2026). All other medical devices, including these consumables, only have the rule that their price may
     not rise more than 10% a year (IO-36).

All new VO sentences pass the English VO lint in `tools/build_script.py`.

## Optional (recommended, not gate-blocking)

- **O012:** `the one mistake that gets complaints turned away` → `one common mistake that gets complaints turned away`.
  In 2024-25, "not within jurisdiction" (1,781) slightly beat "no complaint to the insurer first" (1,715). The year
  before, skipping the insurer was the top reason (IO-11).
- **O027** (use the owner's figure, now sourced):
  - VO: `In twenty twenty-four to twenty-five alone, seventeen hundred and fifteen health complaints were turned away for this one reason. The person had not complained to the insurance company first.`
  - On screen: `1,715 HEALTH COMPLAINTS TURNED AWAY · NO COMPLAINT TO THE INSURER FIRST [CIO ANNUAL REPORT 2024–25 | STATEMENT H8]`.
- **O017:** `it cannot pass an order telling the company to pay you` → `it does not pass an order telling the company to
  pay you`. IRDAI's pages describe what it does (forwards, monitors, facilitates); none says what it cannot do.
- **O018:** `set up under the Insurance Ombudsman Rules, twenty seventeen` → `which works under the Insurance Ombudsman
  Rules, twenty seventeen`. The institution dates from 1998-99; the 2017 Rules replaced the 1998 ones.
- **O019:** `Now, look at the second trap.` → `Now, back to the second door.` Bima Bharosa is now called useful, so the second
  "trap" no longer has a first.
- **O006:** `most middle-class families` → `many families`. There is no survey behind "most".
- **O007:** drop `pay the fees,`. A consumer commission needs no lawyer, and the fee is nil for claims up to ₹5 lakh
  (National Consumer Helpline FAQ 39 and 45). The "long wait" part is sourced (IO-04).
- **O008:** `as much as twenty percent` → `twenty percent or more`. Insurance Samadhan takes 22% for cases resolved
  "at the legal level" (IO-05).
- **O030:** `Every insurer publishes its grievance officer's email on its website.` →
  `Every insurer has to show its grievance officer's details on its website, and the Ombudsman's website lists their
  email addresses too.` (IO-19)
- **O035:** add `If you are late for a good reason, the Ombudsman can still allow it.` (Rule 14(4), condonation).
- **O037:**
  - VO: `already decided` → `already closed`. The Rule says "disposed of", which also covers a case withdrawn or
    dismissed.
  - On screen: `PENDING OR CLOSED ELSEWHERE`.
- **O041:** `or the insurance company's branch that handled your policy` → `or the insurance company's office you are
  complaining against`. Rule 14(1) and the form say the branch or office "complained against".
- **New O050:** add `In twenty twenty-four to twenty-five, three out of four hearings were online.` (CIO 2024-25 preface:
  "Online hearings also increased to 76%", all lines).
- **O053 or O010:** say it outright: `You don't need a lawyer.` The title promises "No Lawyer Fees", but no line says
  it (CIO FAQ Q12; IO-30).
- **O061**, sharper and still exact (IO-35):
  `And in December twenty twenty-four, the Bombay High Court heard the case of a senior citizen who had won an Ombudsman award, but was not paid for more than three years. The court ordered the insurance company to pay the award with interest, plus one lakh rupees in costs, and said the costs and interest should be recovered from the officers responsible, after an inquiry.`
- **O010 on screen:** the one tag `[IRDAI HEALTH MASTER CIRCULAR | 2024]` sits after three items. Split it:
  `FREE TO FILE [CIO FAQ] · AWARD BINDS THE INSURER [RULE 17] · ₹5,000 / DAY LATE [IRDAI HEALTH MASTER CIRCULAR | 2024]`.
- **O005:** "silently cut": insurers must explain a cut. Health master circular para 17(b): "In case, the claim is
  repudiated or disallowed partially, details shall be conveyed to the claimant along with full details giving
  reference to the specific terms and conditions of the policy document." So "silently" should read as "without
  warning", and the picture should not suggest there was no letter at all.

## Title and packaging

- **Current title** (`title.txt`): "Health Insurance Claim Rejected Again? Step 4: The Insurance Ombudsman (Free, No
  Lawyer Fees)". **Accurate.**
  - Filing is free (CIO FAQ Q15).
  - No lawyer is needed (CIO FAQ Q12). The 2026 Karnataka ruling only lets you bring one at the award stage.
- **Owner's PART 4 options:**
  1. "Health Insurance Claim Rejected? How to Win in 60 Days (Zero Lawyer Fees)": **do not use.**
     - No outcome is guaranteed.
     - There is no 60-day figure anywhere. Rule 17(4) gives the Ombudsman three months after all papers arrive. In
       2024-25, 78.5% of closed health complaints took up to three months, so "about three months" is the honest
       promise.
  2. "The ₹5,000/Day Penalty Rule Insurance Companies Hope You Never Discover": **do not use as is.**
     - "Hope you never discover" claims a motive we cannot source.
     - The penalty only starts after an award goes unpaid for 30 days, and not if the insurer appeals.
     - If you want it: "The ₹5,000-a-Day Ombudsman Penalty: How It Works".
  3. "Don't Go to Consumer Court! Use the Insurance Ombudsman Instead (Step-by-Step)": **do not use.** It cuts against
     the film's own balance: O057 keeps the consumer forum open after an award. It is wrong for claims over ₹50 lakh
     and for cases outside the Ombudsman's scope, and a case already in consumer court bars the Ombudsman
     (Rule 14(5)).
  - The directive's working title "Win Your Claim in 60 Days Without a Lawyer" has the same 60-day problem.
- **PART 4 description chapters to change:**
  - "The 20% Private Claim Recovery Racket (Rule 14 & Contract Act)": the Contract Act claim is unsupported; avoid
    "racket".
  - "The 14-Day GRO Rule & The 1,715 Threshold Dismissal Trap": 14 days and 1,715 are both real, but the 14 days does
    not unlock the Ombudsman; the one month does.
  - "What Happens Inside the 15-Minute Video Hearing": there is no fixed length.
  - "The ₹5,000/Day Delay Penalty & Bombay High Court Salary Attachment Rule": there is no general salary rule; it
    was one case, after an inquiry.
- **Thumbnail promise by 0:30** (PLAYBOOK §4a): at the estimated pace, "step four, the Insurance Ombudsman" is heard at
  about 0:40 (end of O002) and "costs zero rupees" at about 1:50 (O010). Put `STEP 4: INSURANCE OMBUDSMAN · FREE`
  on screen during O001–O002.
- **Description:** carry what the VO leaves out:
  - the appeal exception, and penal interest at 2% above the bank rate (IO-33);
  - a consumer commission needs no lawyer and is free up to ₹5 lakh;
  - condonation of delay (Rule 14(4));
  - IRDAI's 2025-26 figures (63% Bima Bharosa, 75% Ombudsman, 54% courts);
  - the 1,715 and 3,869 counts;
  - the Karnataka and Telangana lawyer rulings;
  - "Educational only, not legal advice".

## Answers to the brief, item by item

1. **Bima Bharosa:** see the Summary. The complaint goes to the insurer and onto IRDAI's record. The insurer
   resolves it; IRDAI monitors and facilitates. Nothing shows it adjudicates or orders payment (IO-12 to IO-14).
2. **Rule 14:**
   - 14(1): you, or your legal heir, nominee or assignee (IO-16).
   - 14(3)(a): a written representation, then rejection, no reply in one month, or an unhappy reply (IO-18).
   - 14(3)(b): one year (IO-21).
   - The pending-or-disposed bar is **14(5)** (IO-23, change 4).
3. **Recovery fees:** supported. Insurance Samadhan: 20% + GST, or 22% "at the legal level", plus ₹999 to register.
   GetClaims: 10–20% plus ₹5,000. ClaimSarathee: 10% (IO-05).
4. **14 days:** Policyholders' Interests master circular, IRDAI/PP&GR/CIR/MISC/117/9/2024, 5 Sep 2024, Part B VI.2(i).
   The tag is right (IO-20).
5. **₹50 lakh:**
   - Rule 17(3) proviso (ii): "not award compensation exceeding rupees fifty lakhs (including relevant expenses, if
     any)".
   - G.S.R. 828(E) of 9 Nov 2023 replaced "thirty" with "fifty".
   - The CIO FAQ words it as "compensation sought … should not exceed Rs. 50 Lakhs" (IO-21, IO-22).
6. **Offices:** 18, Thane from 27.12.2024. You choose the centre by your residence or the insurer's branch or office
   (IO-24).
7. **Filing:** all confirmed on the live form (IO-17, IO-25, IO-26).
   - "Register complaint" and a mobile OTP (valid 90 s).
   - PDF/JPG up to 10 MB each; complaint copy and ID/address proof mandatory; photograph listed.
   - Declaration checkbox; "verified … and post successful verification … registered".
8. **Mediation:**
   - 9,417 / 29,017 = 32.5%, about one in three. Recommendations are mediated settlements the complainant accepted
     (Rule 16(2); CIO Statement H5).
   - "Last year" must become 2024-25.
   - "Often … pays before any hearing" has no source and conflicts with the CIO's hearing data (change 5).
9. **Hearings:** in person or by video (CIO FAQ Q16; Rule 15(5); 76% online in 2024-25).
10. **Rule 17:**
    - 17(6): comply "within thirty days of the receipt of the award".
    - 17(7): interest "at a rate per annum as specified in the regulations".
    - 17(8): binding on the insurers.
    - The complainant is not bound and may take "recourse to the normal process of law" (CIO FAQ Q21) (IO-08, IO-32).
11. **Penalty:**
    - Health master circular para 20 and IRDAI health FAQ 45 match. "On top of any interest" is supported.
    - 10 days = ₹50,000 and 30 days = ₹1,50,000 are right.
    - The appeal exception is missing (changes 1 and 7).
    - Bank Rate + 2% is real: Policyholders' Interests master circular para 25.2, "in terms of rule 17 (7)" (IO-33).
12. **Dedhia** (Bombay HC, 9 Dec 2024):
    - The insurer's writ was dismissed with ₹1 lakh exemplary costs, and it was told to pay the ₹27,13,582 award with
      7% interest from 1 July 2021.
    - A Regional Manager inquiry must fix the officials responsible, and the costs and interest are to be recovered
      from them, "if necessary, by making deductions from their salaries", with natural justice.
    - It was a health-claim award left unpaid for over three years, so "made to fight for years" is fair. O061 is
      exact as written; the sharper optional line names the award (IO-35).
13. **Non-entertainable:** 4,928 health complaints in 2024-25, of which 1,715 were under 14(3)(a). The 1,715 is
    real; see optional O027 (IO-11).
14. **Consumer court:** you need no lawyer, and the fee is nil up to ₹5 lakh. "Often for a long time" is fair: India
    Justice Report 2026 says more than a third of filed cases in the 19 State Commissions that shared data had been
    pending for more than three years, against a 3–5 month target in the Act (IO-04).
15. **NPPA:**
    - Ceiling prices exist only for a few devices: coronary stents and knee implants (PIB, 17 Mar 2026). NPPA revises
      the stent prices each April, so quote the current notice if Episode 03 gives a figure.
    - Other devices, consumables included, are limited to a 10% yearly price rise.
    - So O064 must change (change 8).
16. **GST 18%:** the arithmetic is right. The rate is our assumption, so label it (change 3).

## v1.3 re-check (2026-10-15)

Light scope (PLAYBOOK §12): I compared v1.3 (`script.full.tsv`, md5 `50df2912`) with v1.2 (git HEAD) field by field
and re-checked only the 22 lines that changed. All other lines are unchanged.
- **All 8 required changes are in, word for word:** O010, O014 (with the 63% tag), O021, O037, O050–O052, O054, O059,
  O064. Every VO line passes `lint_en`.
- **Optionals applied, all still supported by their sources:**
  - O002 on-screen `STEP 4: INSURANCE OMBUDSMAN · FREE`. This also brings the thumbnail promise forward, to about 0:20–0:40.
  - O005 drops "silently"; O006 says "many families"; O007 drops "pay the fees".
  - O008 "twenty percent or more"; O010 split tags; O012 "one common mistake".
  - O017 "does not pass"; O018 "which works under"; O019 "back to the second door".
  - O027 uses 1,715 with the H8 tag; O030 GRO wording; O061 the sharper Dedhia line.
- **`claims.csv`:** rows updated to quote the v1.3 text and line ids.
  - Mediation now sits at O051 (IO-28, IO-29), the hearing at O050 and the award at O052 (IO-27).
  - The "REQUIRED CHANGE" notes now read "applied in v1.3".
  - Every on-screen tag cited in a claim exists in the file.
- **Gate:** `37 claims: confirmed 37`, passed, and it now describes the script as it stands.
- **Still open (optional, not applied):**
  - O035 condonation line.
  - O037 "already closed".
  - O041 "office you are complaining against".
  - A spoken "You don't need a lawyer".
  - The 76%-online line.
  - Moving O053 after O050.
