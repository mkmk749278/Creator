# Can't Pay Even the Minimum: PROOF shots (2026-10-13)

Files: `assets/proof/<id>.png` (3840×2160, a 1920×1080 viewport at 2×) and `<id>.json` (highlight box as fractions of the
frame, for the push-in). Contact sheet with every box outlined in red: `qa/proof_sheet.jpg` (checked: each highlight is on
the quoted words and no pop-up, cookie bar or ad covers it).

- Web pages: `node build/proof_shots.js /opt/node-tools assets/proof [id,id]`. This is a copy of the minimum-due script
  with three changes: the matcher ignores whitespace and quote marks and can span text nodes; collapsed FAQ answers are
  opened; fixed layers on `<html>` (Google's "anno" chip) and late pop-ups are removed in a second sweep.
- PDFs: `python3 -I build/proof_pdf.py <pdf dir> assets/proof [id,id] [--list]` renders the page at about 266 dpi
  (pdftoppm), finds the words with `pdftotext -bbox-layout`, adds a multiply-blend highlighter and places the page on a
  grey PDF-viewer frame. The PDFs were downloaded with `curl -sSL -A '<Chrome UA>'` from the URLs below, saved as
  hdfc_mitc.pdf, pnb.pdf, onecard.pdf, hdfc_cma.pdf, indusind.pdf and sc2019.pdf.
- Text on the RBI, Indian Kanoon and SBI FAQ pages is small at full frame. Use the 2–2.5× push-in on the box
  (PLAYBOOK §14).

| id | line(s) | claim | url | quote highlighted | citation tag | status |
|---|---|---|---|---|---|---|
| rbi_npa_90 | C013 | CP-005 | https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=12822 | A credit card account will be treated as non-performing asset if the minimum amount due, as mentioned in the statement, is not paid fully within 90 days from the payment due date mentioned in the statement. | [RBI \| IRAC NORMS] | ok |
| rbi_provision_25 | C014 / C015 | CP-006 | same as above | The ‘unsecured exposures’ which are identified as ‘substandard’ would attract additional provision of 10 per cent, i.e., a total of 25 per cent on the outstanding balance. | [RBI \| PROVISIONING RULES] | ok |
| rbi_bureau_15days | C018 | CP-010 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12718 | CICs and CIs shall keep the credit information collected/maintained by them updated regularly on a fortnightly basis (i.e., as on 15th and last day of the respective month) | [RBI \| FROM 1 JAN 2025] | ok |
| kanoon_sbi_cibil | C020 | CP-012 | https://indiankanoon.org/doc/68016726/ | On this account we conclude that the District Commission has rightly held the Company deficient in service i.e. by not properly intimating the respondent. | [MP STATE CONSUMER COMMISSION \| 2024] | ok |
| sbi_faq_block | C021 | CP-013 | https://www.sbicard.com/en/faq/card-blocking-unblocking.page | In case you have missed making payment of at least minimum amount due as of latest statement on your SBI Credit Card, your card may be blocked for further usage. (the "2) Irregular payments : First payment default" answer is opened) | [SBI CARD \| FAQ] | ok |
| sbi_faq_writeoff | C068 / C070 | CP-139, CP-141 | same as above | More than 6 consecutive payments default + In case your account is written-off and you pay complete outstanding as per the agreement, we will process your request for CIBIL status clean-up | [SBI CARD \| FAQ] | ok |
| hdfc_mitc_rate_375 | C024 | CP-015 | https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/cards/credit-cards/personal-mitc/mitc-in-english.pdf (p. 10) | All other variants 3.75% 45.0% (finance charges table, excl. GST) | [HDFC · ICICI · SBI CARD · AXIS \| 2026] | ok (note 1) |
| hdfc_mitc_late_fee | C025 (also C022, C026, C079) | CP-016 | same PDF (p. 13) | Charges in case of default (no payment or delayed payment): Basis Credit Card bill amount … ₹5,001 to ₹10,000 ₹750/- … More than ₹50,000 ₹1300/- | [HDFC BANK MITC \| SEP 2026] | ok (note 2) |
| pnb_commission_slabs | C035 | CP-026, CP-027 | https://pnb.bank.in/downloadprocess.aspx?fid=cT0Zz2WiAeLAecOeYnil0A%3D%3D (p. 8) | The Agency will be paid commission on the amounts recovered as under: … upto Rs 1 lac … Upto 3 years 7.5 % … Above 3 years upto 5 10.0 % … Beyond 5 years 15.0 % | [PNB \| AGENCY TENDER] | ok |
| onecard_ap_tg_agencies | C038 | CP-030 | https://www.getonecard.app/legal/Repayment_Agencies_Q3.pdf (p. 3) | Row 28: CollMan Services, Tirupathi, Andhra Pradesh, NO.19-12-356 BAIRAGIPETTADA ,OPP TO PADMAVATHI PARK ,NEAR INDIAN BANK,TIRUPATHI-517501; plus the city cells Hyderabad/KarimNagar/Warangal (row 22), Vizag (24), Hyderabad (25) and Vijaywada (29). All six places are on this one page. | [ONECARD \| AGENCY LIST] | ok (note 3) |
| pnb_trace_7500 | C040 | CP-032 | same PNB PDF (p. 22) | On receipt of information about whereabouts of the missing/absconding … Rs. 7,500/- per person subject to maximum fee of Rs. 45,000/- | [PNB \| TENDER] | ok |
| kanoon_lok_adalat_indore | C043 | CP-104 | https://indiankanoon.org/doc/68016726/ | In June 2019, the Company filed a pre-litigation in National Lok Adalat, Indore + dues of Rs.1,82,969/- | [MP STATE CONSUMER COMMISSION \| 2024] | ok (note 4) |
| livelaw_lok_adalat_decree | C044 | CP-107 | https://www.livelaw.in/amp/high-court/jammu-kashmir/jammu-and-kashmir-high-court-lok-adalat-awards-deemed-decrees-no-further-appeals-under-section-96-of-cpc-allowed-240513 | every award issued by the Lok Adalat is deemed to be a decree of a Civil Court and is final and binding | none in claims.csv; suggest [J&K AND LADAKH HIGH COURT \| VIA LIVELAW] | ok (paywall box hidden) |
| bnb_76000_awards | C045 | CP-108 | https://www.barandbench.com/news/litigation/delhi-high-court-shocked-to-find-one-arbitrator-handled-axis-banks-4155-arbitrations-in-5-years | The bank also disclosed that 76,000 awards had been passed pan-India by sole arbitrators who were unilaterally appointed in disputes involving the bank. | [DELHI HIGH COURT \| ARBITRATION RULING] | ok |
| drt_20_lakh | C046 | CP-111 | https://www.taxheal.com/?p=68695 | the provisions of the said Act shall not apply where the amount of debt due to any bank or financial institution or to a consortium of banks or financial institutions is less than twenty lakh rupees. | [FINANCE MINISTRY \| 2018] | ok |
| hdfc_cma_setoff | C055 | CP-122 | https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/cards/credit-cards/membership-kit/card-member-agreement-29-10-2019.pdf (p. 15) | It is agreed that the Bank, at any time and without notice, will have a lien and right of set-off on all monies belonging to the Cardmember and/or Add-on Cardmember standing to their credit in any account whatsoever with the Bank | [HDFC BANK \| CARDMEMBER AGREEMENT] | ok |
| kanoon_ncdrc_setoff_53k | C056 | CP-123 | https://indiankanoon.org/doc/65053962/ | In view of the aforesaid clause, the petitioner bank was entitled to set off the credit card dues at any point of time, without any notice to the complainant. Therefore, deduction of the amount of Rs.53,043.68 from the saving bank account of the complainant was in consonance with the above referred condition | [NCDRC VIA GOODRETURNS \| 2019] | ok (note 5) |
| kanoon_kerala_hold | C056 | CP-124 | https://indiankanoon.org/doc/98197117/ | the action initiated by the respondents by freezing the account of the 1st petitioner is not an attachment, but according to the bank, it is in exercise of the right of adjustment or the right akin to set off | [KERALA HIGH COURT \| 2026] | ok |
| indusind_bcsbi_3days | C058 | CP-127 | https://bank.indusind.bank.in/content/dam/regulatoryDisclosure/codeOfCommitment/coc_english.pdf (p. 52) | We will send you intimation to this effect by e-mail on your registered e-mail id / registered mobile number or letter within three days from placing lien / hold on your deposit account. | [BCSBI CODE \| 2018] | ok |
| sc_2019_not_cheating | C064 / C065 (also C081) | CP-133, CP-134 | https://api.sci.gov.in/supremecourt/2018/17145/17145_2018_Judgement_03-Jan-2019.pdf (pp. 8–9, stacked) | The mere inability of the appellant to return the loan amount cannot give rise to a criminal prosecution for cheating unless fraudulent or dishonest intention is shown right at the beginning of the transaction, as it is this mens rea which is the crux of the offence. | [SUPREME COURT (2019) \| SATISHCHANDRA SHAH] | ok (the sentence crosses the page break, so both pages are shown) |
| sc_2025_kukreja | C065 | CP-135 | https://www.caseciter.com/shrichand-rajaram-kukreja-vs-state-of-maharashtra-2025-insc-794-quashing-civil-disputes-criminal-cases/ | The allegations, made in the complaint, present a dispute which is purely commercial and civil in nature. It seems that the complainant has contrived to somehow or the other, involve the police machinery to act as recovery agents on his behalf. | [SUPREME COURT (2025) \| KUKREJA] | ok (note 6) |
| rbi_ombudsman_90days | C074 | CP-147 | https://www.rbi.org.in/Scripts/FAQView.aspx?Id=153 | The complaint must be made to the RBI Ombudsman within 90 days from the date on which the above timeline expires or the date of the last communication from the concerned Regulated Entity, whichever is later. | [RBI \| OMBUDSMAN SCHEME 2026] | ok |
| rbi_faq_14448 | C074 | CP-147 | same as above | The IVRS facility on Toll Free No. 14448 is available 24x7. | [RBI \| OMBUDSMAN SCHEME 2026] | ok (same page as the claim, not its quote) |
| rbi_faq_cms_address | C074 | CP-147 | same as above | One centralised complaint lodging portal i.e., https://cms.rbi.org.in | [RBI \| OMBUDSMAN SCHEME 2026] | ok (same page as the claim, not its quote) |
| rbi_cms_portal | C074 | CP-147 | https://cms.rbi.org.in/ | page only | [RBI \| OMBUDSMAN SCHEME 2026] | **failed**: connection reset (Chromium and curl, two tries); use rbi_faq_cms_address instead |
| ecourts_case_status | C076 | CP-149 | https://services.ecourts.gov.in/ecourtindia_v6/ | page only (Search by CNR number box) | [ECOURTS] | ok |

## Notes for the edit and the fact-check
1. **C024**: CP-015's own source and quote are ICICI's Amazon Pay terms. This shot is the HDFC MITC, which shows the
   same 3.75% a month (45% a year) excluding GST. Both support the multi-bank tag.
2. **C025**: the MITC PDF footer reads "Version 4.14 Dated – October 2026", but the tag says `SEP 2026`. Change the tag
   to `OCT 2026`, or check which version the fact-check used.
3. **C038**: the VO and visual plan name six places, Tirupati included, and this page shows all six. The CP-030 claim
   text lists only five; update the wording in claims.csv.
4. **C043**: the brief asked for "the LiveLaw Lok Adalat story (SBI Card, Indore)". In claims.csv the SBI Card / Indore
   Lok Adalat facts come from the consumer-commission order on Indian Kanoon (CP-104), and the LiveLaw link is a J&K High
   Court story that Lok Adalat awards are decrees (C044, CP-107). Both are shot.
5. **C056**: the proof is the NCDRC order on Indian Kanoon, not GoodReturns. Suggest the tag `[NCDRC | 2019]`.
6. **C065**: the 2025 Kukreja source in claims.csv is caseciter.com, a case summary site, not api.sci.gov.in. The
   highlighted words are the judgment's lines as quoted there. For a primary source, find the 2025 INSC 794 PDF on
   sci.gov.in.
