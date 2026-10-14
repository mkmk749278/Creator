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
