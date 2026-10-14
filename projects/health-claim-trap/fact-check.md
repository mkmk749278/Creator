# Fact-check: The Health Insurance Claim Rejection Trap

Independent pass, 2026-10-14, light scope (PLAYBOOK §12). Sources opened this pass are logged row by row in `claims.csv`.
Every quote except four was machine-checked word for word against a local copy of its source. The four exceptions
(HC-21, HC-25, HC-26, HC-27) come from the scanned CIO annual report and were read from the page images.

## Summary

- **Gate:** `48 claims: confirmed 34, disputed 1, unverified 5, wrong 8`. It fails on 13 rows. Each one clears once the
  matching script change below is made and the row is flipped to `confirmed`, with the source already in its note.
- **Strong rows hold.** The master circular quotes (paras 13, 15, 16, 17, 20 and the TPA pay rule) match the irdai.gov.in
  original word for word: `https://irdai.gov.in/document-detail?documentId=4942918`. That URL now replaces the blog copy
  as `source_url`.
- **Nothing changed after May 2024** on the 60-month moratorium, the one-hour and three-hour rules, the 14-day complaint
  rule or the ₹5,000-a-day penalty. I checked IRDAI's circular list (to 22 Sep 2026), its regulations list (to 31 Jul 2026),
  its health FAQ page (dated 09 Oct 2026) and the Policyholders' Interests master circular (5 Sep 2024). Two cautions:
  - The 5 Sep 2024 circular adds an exception: there is no penalty if the insurer appeals the award within 30 days (H064).
  - The Ombudsman Rules have not been amended since 9 Nov 2023. The 2025 insurance-laws amendment Act does not touch
    these points.
- **Our calculations:**
  - The room-rent maths (62.5% paid, 37.5% cut, about ₹60,000 against ₹9,000) is right, and the method matches current
    policy wording.
  - But the 2020 IRDAI proportionate-deduction circular the film cites was **repealed by the 29 May 2024 master
    circular** (Annexure-6, item 19). Nothing in the 2024 rules replaces it, and current policies differ: some exempt only
    medicines, and some apply the cut to ICU charges above the ICU cap. So H027's tag and H028 must change. Some media
    (Outlook Money, Sep 2026) say the 2024 circular carries these exemptions; its text does not.
  - The Ombudsman figures (32,503 complaints, 76%, 78.5%) match Statement H3. Counting mediated settlements as wins is
    fair: the CIO's own Statement H5 is headed "Recommendations and Awards in favour of complainants", with the same total
    of 15,543. Under Rule 16, a recommendation is a settlement the complainant accepts as full and final.
- **Weak rows resolved:**
  - HC-01 (cashless denial vs reimbursement): policy wording.
  - HC-03: IRDAI FAQ.
  - HC-11: IRDAI 2020 guidelines, eight years.
  - HC-17 (14 days): 2024 Policyholders' Interests master circular.
  - HC-18: Bima Bharosa FAQ.
  - HC-21, HC-23, HC-30: CIO report and CIO FAQ ("no provision to engage a lawyer"; "recourse to the normal process
    of law").
  - HC-32 (1% room cap): New India and SBI General.
  - HC-33: non-payable lists confirmed; the share-of-bill figure is disputed.
- **New rows:**
  - HC-34, H001: IRDAI 2024-25 annual report, about 8% of health claims repudiated.
  - HC-35, H014: 69% of claims settled through TPAs.
  - HC-36, H038: fraud definition.
  - HC-37, H044: no data.
- Scenario numbers (₹35,000 × 6 years, ₹4,50,000 bill, 9:00 PM) are labelled SIMULATION and need no source.

## Required script changes (gate-blocking)

1. **H009** on-screen: `NOT A CLAIM REJECTION [IRDAI MASTER CIRCULAR | 29 MAY 2024]` → `NOT A CLAIM REJECTION [AROGYA SANJEEVANI POLICY WORDING]`, reason: the master circular never says this; the right to claim reimbursement after a cashless denial is in the policy wording (HC-01, HC-01b).
2. **H015** VO: `A TPA is a private company.` → `A TPA is a company licensed by IRDAI.`, reason: IRDAI defines a TPA only as a company registered with it, and one TPA (Health Insurance TPA of India) is owned by state-run insurers (HC-03b).
3. **H019** VO: `Now, the three reasons you will see most often on these letters.` → `Now, three reasons you will often see on these letters.`, reason: no source ranks these three as the most frequent; they are common, but so are waiting periods and missing documents (HC-07b).
4. **H027** on-screen: `OUR CALCULATION · 37.5% CUT [IRDAI PRODUCT FILING GUIDELINES | 2020]` → `OUR CALCULATION · 37.5% CUT [AROGYA SANJEEVANI POLICY WORDING]`, reason: the 2020 guidelines were repealed on 29 May 2024; the same method is in current policy wording (HC-09, HC-09b).
5. **H028** VO: `One good thing. IRDAI does not allow this cut on medicines, implants, tests and ICU charges. Check your bill for that.` → `One good thing. Many policies do not apply this cut to medicines, and some also leave out implants and tests. Check what your policy wording says, and check your bill.`; on-screen `NO CUT · MEDICINES · IMPLANTS · TESTS · ICU` → `NO CUT ON MEDICINES · IMPLANTS, TESTS: CHECK YOUR POLICY [POLICY WORDING]`; picture: tick only on medicines, implants and tests in amber, drop ICU. Reason: the IRDAI rule was repealed in 2024; current wordings exempt medicines, only some exempt implants and tests, and the standard wording applies the cut to ICU charges above the ICU cap (HC-10).
6. **H033** VO: `In May twenty twenty four, IRDAI brought it down from eight years to five years.` → `In twenty twenty four, IRDAI brought it down from eight years to five years.`; on-screen `8 YEARS → 5 YEARS [IRDAI MASTER CIRCULAR | 29 MAY 2024]` → `8 YEARS → 5 YEARS [IRDAI INSURANCE PRODUCTS REGULATIONS | 2024]`. Reason: the five-year rule came in the Insurance Products Regulations, notified 20 March 2024 and in force from 1 April 2024; the May circular only repeated it (HC-11b).
7. **H044** VO: `Most people never use this rule, because nobody told them it exists.` → `So remember this rule, and ask for it at the discharge counter.`, reason: there is no data on how many people know or use the rule (HC-37).
8. **H051** VO: `Step two. File a reimbursement claim, within the time your policy gives. Usually about thirty days from discharge.` → `Step two. File a reimbursement claim quickly, within the time your policy gives. Some policies give only fifteen days from discharge, some give thirty.`; on-screen `USUALLY 30 DAYS` → `15–30 DAYS [CHECK YOUR POLICY WORDING]`; picture: calendar strip with day 15 and day 30 marked. Reason: current standard-product wordings give 15 days (Go Digit) or 30 days (IFFCO-Tokio), so "usually thirty" could make a viewer miss a 15-day limit (HC-16).
9. **H059** VO: `The Ombudsman system was set up by the government, only to settle complaints between policyholders and insurance companies.` → `The Ombudsman system was set up by the government, to settle complaints of policyholders against insurance companies.`, reason: it also hears complaints against agents, intermediaries and brokers, so "only" is wrong (HC-21b).
10. **H064** VO: `It must pay within thirty days, or pay a penalty of five thousand rupees for every day of delay, to you.` → `Unless the company challenges the award, it must pay within thirty days, or pay you a penalty of five thousand rupees for every day of delay.`; on-screen `₹50 LAKH · 30 DAYS · ₹5,000/DAY [IRDAI MASTER CIRCULAR | PARA 20]` → `₹50 LAKH [OMBUDSMAN RULES | RULE 17] · 30 DAYS · ₹5,000/DAY [IRDAI POLICYHOLDERS' INTERESTS MASTER CIRCULAR | 2024]`. Reason: the 2024 circular says there is no penalty if the insurer appeals within 30 days, and the ₹50 lakh cap is in the Ombudsman Rules, not para 20 (HC-28b, HC-29b).
11. **H071** VO: `Yes, the company may charge a little extra, or add a waiting period.` → `Yes, the company may charge extra, or add a waiting period.`, reason: no source says the loading is small; insurers set it product by product (HC-31b).
12. **H075** VO: `They can be five to fifteen percent of a hospital bill. Many insurers sell an add on cover for this.` → `Reports say they can be five to fifteen percent of a hospital bill. Some insurers sell an add on cover for this.`; on-screen `5–15% OF A BILL [INSURER AND BROKER GUIDES]` → `5–15% OF A BILL · AS REPORTED [OUTLOOK MONEY | BUSINESS STANDARD]`. Reason: estimates disagree (2–8%, 5–10% and 8–10% before Covid; 10–15% in 2026), so the figure must be attributed, with the other figures in the description; sources say "some" insurers, not "many" (HC-33b, HC-33c).

## Recommended (not gate-blocking)

- **H040** VO: `A rejection letter that says non disclosure.` → `A denial letter that says non disclosure.`, reason: the film's own point is that the H005 letter is a cashless denial, not a rejection.
- **H039** VO: `Two honest points.` → `Three honest points.`, and add after the porting sentence: `And if you increase your cover, the extra amount gets its own five year count.` Reason: IRDAI Insurance Products Regulations 2024 Schedule cl. 8 and IRDAI FAQ Q39: on an enhanced sum insured, the 60 months run from the date of enhancement. Add a claims row when this goes in.
- **H038** VO, optional tightening: `Fraud that the company has to establish.` → `A deliberate lie, and it has to be proved.`, reason: matches "established fraud" plus the policy definition of fraud as an act "with intent to deceive" (HC-36).
- `tools/claim_math.py` docstring: credit the policy wording instead of the repealed 2020 guidelines.
- Description and title: do not use the handoff's "Why 80% of Health Insurance Claims Get Rejected" title idea; IRDAI's 2024-25 report says about 8% of health claims were repudiated. Put the consumables estimates (HC-33b) and the 53.6% all-disposed Ombudsman figure (HC-26 note) in the description, with the line "Educational only, not insurance advice".

## Applied (writer, 2026-10-14)
All 12 required changes and the H040 recommendation ("A denial letter") are in `script.full.tsv`; the matching rows are
now `confirmed` with the sources named above. Three claims were removed from the script rather than sourced, so their rows
were dropped from `claims.csv`: HC-07b (H019 now says "three reasons you will often see"), HC-31b (H071 "may charge
extra") and HC-37 (H044 now "So remember this rule, and ask for it at the discharge counter."). Not applied, to keep the
blocks under 4,500 characters: the optional H038 wording and the H039 "increased cover gets its own five year count"
line (worth a description note). `tools/claim_math.py` docstring now credits the policy wording.

## v2 re-check (2026-10-14)

Light scope (PLAYBOOK §12). I compared every v2 line (E001–E064) with the v1 row named in its visual (`[v1 Hxxx]`) and
with `claims.csv`, and re-verified only the lines whose facts are new or changed, plus the on-screen tags. Sources
re-opened this pass, each quote machine-checked against a local copy (except HC-42):
- the irdai.gov.in master circular (29 May 2024, English PDF and annexure);
- the Policyholders' Interests master circular (5 Sep 2024);
- the IRDAI Annual Report 2024-25 and the Insurance Products Regulations 2024;
- the Insurance Ombudsman Rules 2017 (as amended to 9 Nov 2023);
- cioins.co.in (home page and FAQ), Bima Bharosa (About Us and FAQ) and IRDAI's health FAQ;
- Outlook Money (22 Jan 2026), Bajaj General's no-room-rent-capping page, and New India's Non-Medical Expenses Rider
  page (read through WebFetch: newindia.co.in resets direct downloads).

### Gate
`50 claims: confirmed 46, disputed 1, wrong 3`. It fails on HC-01b, HC-39 and HC-40. Each one clears when the matching
change below is made and the row is set to `confirmed`, as its note says.

### Required script changes (gate-blocking)
1. **E009** on-screen: `NOT A CLAIM REJECTION [AROGYA SANJEEVANI POLICY WORDING]` → `NOT ALLOWED AFTER 5 YEARS [IRDAI INSURANCE PRODUCTS REGULATIONS | 2024]`
   (the cyan overstamp in the picture says the same), and **E027** on-screen: `CASHLESS NO ≠ CLAIM NO` → `CASHLESS NO ≠ CLAIM NO [AROGYA SANJEEVANI POLICY WORDING]`.
   Reason: E009 now says "a legal rule that makes this exact rejection illegal, once your policy has crossed five years".
   That rule is IRDAI's moratorium (Insurance Products Regulations 2024, Schedule cl. 8), not the policy wording. An
   overstamp saying NOT A CLAIM REJECTION over a VO that says "this exact rejection" also contradicts the VO. The "not a
   claim rejection" point is now first made at E027, so its tag moves there (HC-01b, HC-38).
2. **E036** VO: `Your normal policy limits still apply, and if you port your policy to another insurer, your years move with you.` →
   `Your normal policy limits and exclusions still apply, and if you port your policy to another insurer, your years move with you.`;
   card in the picture: `LIMITS STILL APPLY` → `LIMITS, EXCLUSIONS STILL APPLY`.
   Reason: IRDAI's own customer information sheet format (Annexure-1 of the master circular) says that after the
   moratorium a policy stays contestable for "proven fraud and permanent exclusions specified in the policy contract".
   Without "exclusions", E034 ("an old health history cannot be used as an excuse") and E035 ("only one single
   exception") mislead a viewer whose policy permanently excludes a declared condition: they tell that viewer the
   condition cannot be used after five years. v1.1 had these words; the owner's text dropped them (HC-39).
3. **E055** VO: `Over seventy-five percent of decided cases went in favor of the policyholder.` →
   `Of the cases they settled or decided, over seventy-five percent went in favor of the policyholder.`;
   BOARD label (the H062 board in the pacing note): `15,543 of 20,440 decided` → `15,543 of 20,440 settled or decided`.
   Reason: the 76% counts 9,417 settlements by mediation plus 6,126 awards for the policyholder, out of 20,440. The
   Ombudsman Rules (16, 17) and the CIO call mediation outcomes settlements, not decisions. Of the cases actually decided
   by award, 6,126 of 11,023 (56%) went for the policyholder, so "decided cases" points to the wrong number. v1.1 said
   "settled or decided" (HC-40, HC-26).

### Changed lines that check out
- **E001** "thousands … every single day": IRDAI's 2024-25 report counts 29.51 lakh repudiated health claims in the
  year, about 8,100 a day (HC-34). The count includes government schemes and group cover, with no income split, so
  "middle-class" stays the owner's framing.
- **E005** "rejected by the T-P-A": a labelled SIMULATION. Policy wordings let "The Company / TPA" deny
  pre-authorisation, and the film then explains the committee rule (E017) and the denial-versus-rejection difference (E027) (HC-41).
- **E009** VO: a non-disclosure denial after sixty months breaks a binding IRDAI regulation, so "illegal" is fair (HC-38).
  Only its on-screen tag must change (required 1).
- **E015**: "a company hired and paid by the insurance company" matches IRDAI's TPA definition (HC-03).
- **E016**: "seven out of every ten" and its on-screen tag `69% … [IRDAI ANNUAL REPORT | 2024-25]` match I.6.5.5
  (224.08 of 326.01 lakh claims settled through TPAs, Table I.28) (HC-35).
- **E021**: before sixty months, non-disclosure of a material fact voids the policy (standard wording), so "the company
  can still use it" holds (HC-08).
- **E025, E059**: `tools/claim_math.py` re-run gives 62.5% paid, 37.5% cut and a total cut of 59,625 ("almost sixty
  thousand", "In our example") (HC-09).
- **E033, E035**: para 13 matches word for word. Naming only non-disclosure is narrower than the rule, not wrong.
  "Deliberate" fraud matches "with intent to deceive" (HC-08, HC-36).
- **E039–E040**: para 16(a)–(b): "discharge authorization request", three hours, the extra amount paid from the
  shareholders' fund. The tag `[PARA 16]` is right (HC-15).
- **E048**: "Grievance Redressal Officer" and 14 days are both in the 2024 Policyholders' Interests master circular
  (health CIS, Schedule-D item 11; Part B grievance procedure 2(i)), so the E048 tag covers both. "Principal Nodal
  Officer" does not appear in it (HC-17).
- **E050**: Bima Bharosa, About Us: "through which IRDAI monitors disposal of Policyholder Grievances across the industry" (HC-18).
- **E052**: you can go to the Ombudsman after a month with no reply (Rule 14(3)), and no court case is needed. Rule 14(5)
  in fact bars an Ombudsman complaint on a matter already in court (HC-19, HC-23).
- **E054**: the government set it up, it is free, you can file online and no lawyer is needed (Rules 2 and 14; CIO FAQ)
  (HC-20 to HC-23). "Government body" is acceptable plain words (see the recommendation).
- **E055**: 32,503 received ("over thirty-two thousand") and 78.5% closed within three months ("eight out of ten") are
  right (HC-25, HC-27). Only the "decided cases" wording must change (required 3).
- **E056**: ₹50 lakh (Rule 17(3)(ii)) and "binding on the insurers" (Rule 17(8)). The tag `[OMBUDSMAN RULES | RULE 17]`
  is right (HC-28, HC-28b, HC-29).
- **E058**: a declared condition cannot be non-disclosure (IRDAI CIS "Please disclose all pre-existing disease/s …") (HC-31).
- **E060**: "Reports say" 5–15% stays `disputed` with attribution (HC-33b). "Check its price and its limit" fits New
  India's rider: ₹1,500, cover up to ₹15,000 (HC-42).

### Recommended (not gate-blocking)
- **E009** VO: `makes this exact rejection illegal` → `makes this exact denial illegal`. Reason: E027 says a cashless
  denial is not a claim rejection, so the film should use one word for it.
- **E014** VO: `But in reality, it's a middleman called a T-P-A...` → `But in reality, it's usually a middleman called a T-P-A...`.
  Reason: 31% of claims are settled in-house with no TPA. E016 gives the share seconds later, so this is not blocking (HC-35).
- **After E015** (optional, for balance): add `And I-R-D-A-I says a T-P-A's pay cannot depend on how much claim money is paid out.`
  Reason: "hired and paid by the insurance company" invites the unsourced reading that TPAs are paid to deny, and
  IRDAI's rule says the opposite (HC-04, cut in v2).
- **E017** picture: highlight only para 17(a), or add back `And if they reject it, fully or partly, they must tell you the exact policy clause.`
  Reason: the VO no longer covers 17(b) (HC-06).
- **E025** picture: keep the board's no-cut column, with no VO: medicines ticked, implants and tests marked "check your
  policy" [POLICY WORDING]. Reason: the ~₹60,000 bill assumes medicines and tests are not cut, and some wordings exempt
  only medicines (HC-09, HC-10).
- **E039** picture: drop the 1-HOUR ring, or add back `When you ask for cashless, the company must decide within one hour.`
  Reason: the VO and the tag now cover only the three-hour rule (HC-14).
- **E047** VO: `Step Two. File for reimbursement within fifteen to thirty days.` → `Step Two. File for reimbursement within fifteen to thirty days of discharge. Check your policy for your exact limit.`
  Reason: some wordings give only fifteen days. The on-screen tag already says CHECK YOUR POLICY WORDING (HC-16).
- **E054** VO (optional): `The Insurance Ombudsman is a government body set up specifically to resolve insurance disputes.` →
  `The Insurance Ombudsman is a body set up by the government, specifically to resolve insurance disputes.`
  Reason: the government created it, but it is run by a council of insurers' nominees with one IRDAI and one Finance
  Ministry member, and the insurance councils pay for it (Rules 5, 7, 12) (HC-21).
- **E058** VO: `Once it's on paper, they can never call it non-disclosure.` → `The company may charge extra or add a waiting period, but once it's on paper, they can never call it non-disclosure.`
  Reason: v2 dropped the honest cost of disclosing: a pre-existing disease waiting period of up to thirty-six months, or
  a loading (HC-31).
- **E059** on-screen: `OUR CALCULATION · ~₹60,000 CUT (CALLBACK)` → `OUR CALCULATION · ~₹60,000 CUT`. Reason:
  "(CALLBACK)" is a production note.
- **E060** VO: `Reports say gloves, masks, and syringes can be five to fifteen percent of a hospital bill.` →
  `Normal policies often do not pay for these. Reports say gloves, masks, syringes and similar items can be five to fifteen percent of a hospital bill.`
  Reason: the reports' range covers all consumables (Outlook Money lists gloves, syringes, masks, dressings and PPE
  kits), and v2 dropped the reason to buy the cover (HC-33, HC-33b).
- **E002** VO: `five or six straight years` → `six straight years`. Reason: E037 and the on-screen `₹35,000 × 6 YEARS` say six.
- **Chapter lower thirds:** E012 shows CHAPTER 1, E042 shows CHAPTER 3 and E057 shows CHAPTER 4. There is no CHAPTER 2,
  because v1 H030 went with its line. Add `CHAPTER 2 · THE FIVE YEAR RULE` at E028, or renumber.
- **Description:** carry the facts v2 dropped from the VO:
  - the insurer must pay an award within 30 days unless it appeals, or pay a ₹5,000-a-day penalty to you (HC-29, HC-29b);
  - if you are not happy with the award, you can still go to a consumer court (HC-30);
  - file with the Ombudsman within one year; you can go as soon as the insurer rejects your complaint (HC-24, Rule 14(3));
  - an increased sum insured gets its own five-year count;
  - the range of consumables estimates (HC-33b);
  - other ways to count the Ombudsman result: 53.6% of all disposed complaints went for the policyholder, and 55.6% of awards;
  - master circular para 17(c) makes the insurer or TPA collect claim documents from the hospital, but keeping your own
    copies (E045) is still wise;
  - "Educational only, not insurance advice".

### claims.csv changes
- Timecodes now use E ids, and claim wording matches v2.
- Cut in v2 (rows kept, status unchanged, note "cut in v2"): HC-03b, HC-04, HC-06, HC-10, HC-14, HC-24 (still a tag in
  the E054 picture), HC-29b, HC-30 and HC-33. HC-28b now holds the new E056 on-screen line.
- Re-sourced to match v2:
  - HC-17 adds the Grievance Redressal Officer;
  - HC-18 now cites Bima Bharosa's About Us page;
  - HC-28b and HC-29 cite Ombudsman Rule 17;
  - HC-31 cites the IRDAI CIS;
  - HC-32 cites Bajaj General's no-room-rent-capping page.
- New rows:
  - HC-38: E009 VO;
  - HC-39: E034–E036, wrong;
  - HC-40: E055 VO, wrong;
  - HC-41: E005, a TPA can deny cashless;
  - HC-42: E060, add-on price and limit.
- HC-37 stays unused, because v1 dropped it.

### v2 re-check applied (writer, 2026-10-14)
Required: E009 overstamp and tag (NOT ALLOWED AFTER 5 YEARS [IRDAI INSURANCE PRODUCTS REGULATIONS | 2024]) and E027 tag;
E036 "limits and exclusions"; E055 "Of the cases they settled or decided, over seventy-five percent". HC-01b, HC-39,
HC-40 now confirmed. Also applied: E009 "this exact denial", E047 "of discharge. Check your policy for your exact limit.",
E017 and E039 pictures match the VO, E025 keeps a MEDICINES no-cut column, E059 "(CALLBACK)" dropped, chapter lower
thirds renumbered 2-3-4. Left for the owner (their wording): E002 "five or six", E014 "usually", E054 "a body", E058
loading line, E060 "and similar items"; the dropped details go in the description.
