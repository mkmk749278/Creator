# Research A: RBI rules on SMA/NPA, provisioning, credit bureau, settlement (India, checked 2026-10-12)

Scope: complements research_practical.md (no repeat of agency economics, fees, DRT, ARC sales). Every finding:
plain-words statement, verdict, URL + access date + short exact quote. All pages opened 2026-10-12.

## A1. When a card account becomes SMA-0/1/2 and NPA

**A1.1 NPA rule for cards.** If the minimum amount due on a statement is not paid in full within 90 days of that statement's
due date, the bank treats the card account as an NPA (bad loan). **TRUE.**
- RBI Master Circular, Income Recognition, Asset Classification, Provisioning (UCBs), RBI/2025-26/14,
  DOR.STR.REC.10/21.04.048/2025-26, 1 Apr 2025, para 2.1.2(B):
  https://www.rbi.org.in/Scripts/BS_ViewMasterCirculars.aspx?id=12821 (opened 2026-10-12):
  "A credit card account will be treated as non-performing asset if the minimum amount due, as mentioned in the statement,
  is not paid fully within 90 days from the payment due date mentioned in the statement."
- Same wording in the 1 Apr 2022 edition (RBI/2022-23/17), which also carries the three-day CIC rule: "Banks shall report a
  credit card account as 'past due' to credit information companies (CICs) ... only when a credit card account remains
  'past due' for more than three days." https://rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=12283
- Caveat: the pages I could open are the *UCB* (co-operative bank) master circulars. The commercial-bank version is now the
  RBI (Commercial Banks – Income Recognition, Asset Classification and Provisioning) Directions, 2025, "Updated as on
  October 01, 2026" (https://rbi.org.in/SCRIPTS/BS_ViewMasDirections.aspx?id=13146); its PDF (164MD.PDF) sat behind a
  captcha, so I could not quote its card paragraph. The same 90-day minimum-due rule has long applied to commercial banks
  and the search-engine extracts of RBI pages carry the identical sentence, but treat "the commercial-bank paragraph
  number" as UNVERIFIED. Safe wording: "RBI rules say a card becomes a bad loan, an NPA, when the minimum due stays unpaid
  for ninety days after the due date."

**A1.2 SMA stages and day-end process (Nov 2021 clarification).** Overdue from the due date itself; SMA-0 up to 30 days,
SMA-1 31-60, SMA-2 61-90; tagging happens in the bank's daily day-end run, so the NPA date is the exact calendar day the
90 days are completed. **TRUE** (applies to all commercial banks, co-op banks and NBFCs).
- RBI circular RBI/2021-2022/125, DOR.STR.REC.68/21.04.048/2021-22, 12 Nov 2021, "Prudential norms on IRACP pertaining to
  Advances - Clarifications", addressed to "All Commercial Banks (including Small Finance Banks, Local Area Banks and
  Regional Rural Banks) excluding Payments Banks" plus co-op banks, AIFIs and NBFCs. Reproduced at
  https://taxguru.in/?p=794197 (opened 2026-10-12). Quotes: illustration "the date of overdue shall be March 31, 2021"
  (loan due 31 Mar), tagged SMA-1 on 30 Apr "upon completion of 30 days of being continuously overdue";
  "classification of borrower accounts as SMA as well as NPA shall be done as part of day-end process for the relevant
  date"; "the date of SMA/NPA shall reflect the asset classification status of an account at the day-end of that calendar
  date."
- SMA bands also in the 2025 UCB master circular para 2.1.6 (id=12821): SMA-0 "Up to 30 days", SMA-1 "More than 30 days and
  up to 60 days", SMA-2 "More than 60 days and up to 90 days".

**A1.3 Getting out of NPA needs ALL arrears paid.** Paying only part (or only interest) does not make the account
"standard" again. **TRUE.**
- Same 12 Nov 2021 circular, para 10 (taxguru copy): accounts classified as NPA "may be upgraded as 'standard' asset only
  if entire arrears of interest and principal are paid by the borrower."
- 2025 UCB master circular para 2.2.1(ii): upgrade where "entire overdues pertaining to all the credit facilities availed
  by a borrower from a given bank have been regularised by repayment through genuine sources".
- Nuance (inference from the "all the credit facilities ... from a given bank" wording): NPA is borrower-level at a bank,
  so a card NPA can drag the same customer's other loans at that bank into NPA. research_practical.md 8b already covers
  cross-default; this is the regulatory reason.

**A1.4 Days past due counted from the statement due date.** **TRUE.** RBI card directions para 23(5) (Part 1, README) and
the master circular text above: "The number of 'days past due' and late payment charges shall, however, be computed from
the payment due date mentioned in the credit card statement."

**A1.5 Coming change (2027).** RBI press release, 27 Apr 2026, "RBI issues Directions on Asset Classification,
Provisioning, and Income Recognition for Commercial Banks": new final Directions plus 13 amendment directions (one on
"Credit Cards and Debit Cards: Issuance and Conduct"); "These Directions shall come into effect from April 01, 2027."
https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62628 (opened 2026-10-12). Contents (whether the
90-day card rule or provisioning changes) **UNVERIFIED**; the current rules stay in force until 31 Mar 2027, so the film
can describe today's rules without a caveat, but do not claim "this will never change".

## A2. NPA provisioning and income recognition

**A2.1 Provisioning.** For commercial banks, a sub-standard (first-year NPA) loan needs a 15% provision, and an *unsecured*
one (a credit card is unsecured) needs 25%. **TRUE as the long-standing rule; current paragraph UNVERIFIED** (2025
Directions PDF behind captcha).
- RBI circular RBI 2010-11/529, DBOD.No.BP.BC.94/21.04.048/2011-12, 18 May 2011, to all scheduled commercial banks:
  https://rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx?Id=6415 (opened 2026-10-12): "Advances classified as
  "sub-standard" will attract a provision of 15 per cent"; "unsecured exposures" classified as sub-standard "will attract
  an additional provision of 10 per cent, i.e., a total of 25 per cent".
- Co-op banks (UCB master circular 2025 para 5.1.2(iii)) use a flat "general provision of 10 per cent on total
  outstanding". Not needed for the film.
- Plain words for VO: once your card turns NPA, the bank must set aside about a quarter of what you owe from its own profit.
  That is why banks push hard around day 60-90. (The "why they push" part is our inference; say "one reason".)

**A2.2 Income recognition.** The bank may not count unpaid interest on an NPA as income; it is booked only when actually
received, and interest already booked but unpaid is reversed. **TRUE.**
- UCB master circular 2025 (id=12821) para 4.1.1: "Income from non-performing assets (NPA) is not recognised on accrual
  basis" but is "booked as income only when it is actually received"; para 4.2.1: interest accrued and credited "should be
  reversed or provided for, if the same is not realised". Same principle applies to commercial banks (IRACP framework).

**A2.3 Does the customer's interest stop?** **FALSE as a general claim.** No RBI text found that stops a bank charging
contractual interest/fees on an NPA card; the IRACP rule is about the bank's *accounts*, not the customer's statement.
INFERENCE (mark as such): the bank can keep levying contractual charges (subject to the card directions' limits, e.g. no
capitalisation of unpaid charges / no negative amortisation, see Part 1 README), but cannot show them as income until
paid. Many banks do stop sending statements or block the card after write-off; that is practice, not a rule
(see research_practical.md sec 4). Do not say "interest stops after 90 days".

## A3. Credit bureau reporting, record life, free report, complaints

**A3.1 Reporting every 15 days.** Since 1 Jan 2025 lenders update bureaus fortnightly (as on the 15th and the last day of
each month), submitting within 7 days. So a missed payment can show on your report within about three weeks, not
"next month or later". **TRUE.**
- RBI/2024-25/60, DoR.FIN.REC.No.32/20.16.056/2024-25, 8 Aug 2024, "Frequency of reporting of credit information by
  Credit Institutions to Credit Information Companies": https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12718
  (opened 2026-10-12): "updated regularly on a fortnightly basis (i.e., as on 15th and last day of the respective month)";
  "shall be ensured within seven (7) calendar days of the relevant reporting fortnight"; "These instructions shall be
  effective from January 1, 2025."
- "About three weeks" is our arithmetic (up to 15 days to the next cut-off + 7 days to submit); say "within a few weeks".

**A3.2 Three-day grace before "past due" is reported.** **TRUE** (card directions para 23(5), Part 1 README; same text in
the master circular, see A1.1). DPD itself still counts from the due date, so day 4 shows as DPD 4, not DPD 1.

**A3.3 You get an SMS/email when the bank reports your default.** **TRUE** (where your number/email is on file). Note: the
rule says *while* reporting, not *before*; do not say "the bank must warn you before".
- RBI/2023-24/73, DoR.FIN.REC.49/20.16.003/2023-24, 26 Oct 2023, "Strengthening of customer service rendered by Credit
  Information Companies and Credit Institutions", para 2.1.2:
  https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12553 (opened 2026-10-12): "CIs shall send alerts through SMS/
  email to customers while submitting information to CICs" (regarding default / Days Past Due).
- Same circular, para 2.1.1: CICs alert you "when their Credit Information Report (CIR) is accessed".

**A3.4 One free full credit report (with score) a year from each bureau.** **TRUE.** Same circular para 2.8: "CICs shall
provide easy access to Free Full Credit Report", link "displaying the link prominently on their website (on the Home page
itself)". (One per calendar year per CIC is the long-standing 2016 rule; the "with score" detail is in the 2023 circular
as summarised by the fetch; quote only the line above.) Four CICs exist (CIBIL, Experian, Equifax, CRIF High Mark) per
common knowledge; UNVERIFIED in this session, so do not list them on screen without a source.

**A3.5 Complaint fixing deadline and ₹100 a day.** If a wrong entry is not fixed within 30 days of your complaint, you get
₹100 for each day of delay; the bank gets 21 days, the bureau the remaining 9. **TRUE.**
- RBI/2023-24/72, DoR.FIN.REC.48/20.16.003/2023-24, 26 Oct 2023, "Framework for compensation to customers for delayed
  updation/ rectification of credit information": https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12554
  (opened 2026-10-12): "Complainants shall be entitled to a compensation of ₹100 per calendar day" if the complaint is
  "not resolved within a period of thirty (30) calendar days"; "a CI would get twenty-one (21) days and CICs would
  effectively get the remainder of nine (9) days". Note: this is for *wrong or not-updated* data, not for removing a true
  default.

**A3.6 How long a record stays: "seven years" is a MINIMUM, not an expiry.** **PARTLY.** The law tells bureaus and
lenders to keep data for at least seven years; it does not say it is deleted after seven years.
- Credit Information Companies Regulations, 2006, via https://www.legitquest.com/act/the-credit-information-companies-regulations-2006/8409
  (opened 2026-10-12): Reg 10(d)(a) credit information kept for "a minimum period of seven years"; Reg 11(4)(i) personal
  data, same "a minimum period of seven years"; preservation and destruction rules are set by the CIC/CI with RBI approval
  (Reg 10(d)(b)).
- Older industry note (CRIF High Mark news, Aug 2015, search result only, not opened) said the 7-year floor with no
  maximum led some CICs to report data up to 25 years old. UNVERIFIED (not opened).
- Safe wording: "The law makes bureaus keep this record for at least seven years." Do not say "it vanishes after seven
  years".

**A3.7 What "settled" and "written off" mean on the report.** **TRUE (lender explainer, not regulator).**
- Moneyview explainer (no page date, footer 2026): https://moneyview.in/cibil-score/how-to-remove-write-off-from-cibil
  (opened 2026-10-12). Written off: "the lender could not retrieve the loan amount from the borrower, despite multiple
  tries"; Settled: borrower pays "only a part of the loan" and the lender forgives the rest; a settled status stays "for
  as long as 7 years"; to change it: "The only way to remove a settled status from your CIBIL report is by paying off the
  remaining loan amount" then a No Dues certificate and lender update.
- No RBI text found defining these labels (RBI/2023-24/73 does not mention them). CIBIL's own FAQ returned 403.
- Plain words: "Settled" tells every future lender you did not pay in full. Paying the balance later can change it to
  closed, but the late-payment history before that stays (inference from how DPD history works; mark as inference).

## A4. RBI 2023 compromise settlement and technical write-off framework

## Safe to say / Do not say
