# Research: what really happens when a credit card bill goes unpaid (India, 2025-2026)

Project: `cant-pay-minimum` · Channel: Be Practical with Kishore · Researcher pass: PRACTICAL REALITY (not rules)
Compiled 2026-10-12. Every SOURCED row was opened in this session (curl + pdftotext or WebFetch). Quotes are exact
from the opened document unless marked "(paraphrase)". RBI/legal rules (SMA/NPA, agent conduct, Sec 420, Lok
Adalat basics, OTS framework, set-off law) are covered by the other researcher and are only touched where needed.

Verdicts: **SOURCED** = opened page says it · **PARTLY** = opened page says part of it, or source is secondary/marketing,
or we did arithmetic on sourced inputs · **UNVERIFIED** = not found on an opened page; our inference or a search-snippet only.

Big caveat for the script: **no Indian card issuer publishes its own internal collection rule like "below ₹X we only
call".** Every "small amounts only get calls" statement is our inference from (a) bucket strategies in bank RFPs and
policies, (b) commission-on-recovery pay models, (c) where agencies sit. Say it as "how the economics push it", not as a
rule.

---

## 1. How recovery is organised in practice (by days past due and by amount)

**1.1 Bank of Baroda: delinquent accounts go to an outsourced tele-calling centre first; field work is added by bucket.**
SOURCED. *RFP for Empanelment of Agency for Collection of Dues*, Bank of Baroda, Receivables Management Dept, RFP ref
BCC:RECMGMNT:115:06, issued 20.08.2022.
https://bankofbaroda.bank.in/-/media/Project/BOB/CountryWebsites/India/tenders/finalrfp-collectionss-18-08-18-21.pdf
(tender page: https://bankofbaroda.bank.in/tenders/corporate-office/request-for-proposal-for-empanelment-of-agency-for--collection-of-dues)
- "The scope of services includes pre-delinquency and 1-90 DPD (or till the account is marked as NPA)/CC/OD and NPAs
  collections management. This will entail a tele-calling led collection, centralized/ regional set up with multi
  lingual workforce."
- "1-90 DPD – tele-calling by centralized cell using auto-dialer outbound tele-calling(standardized scripts for different situations)"
- Table A workflow: Bucket 1 (1 to 30 days): "Tele Calling"; Bucket 2 (31 to 60): "Tele Calling & Field Referrals";
  Bucket 3 (61-90): "Concurrent allocation for calling and field. Tele calling team to extend shadow support."; Bucket 4
  (91+): same concurrent calling and field.
- Pay model: "The commercial bid evaluation will be done on the basis of tele-calling cost. The bidder will have to quote
  for "Per-seat cost" for tele-calling" ... "The minimum number of tele-callers required will be 200." ... "40% of the
  monthly fee amount will be earmarked to be paid to collections partner on adhering to SLA norms."
- City-based call centres: "Tele-calling locations among zones can be selected from below: ... South: Hyderabad,
  Chennai, Bangalore, Mangaluru, Ernakulam".
- Skip tracing: "The agency should help in the process of improving customer's contact-ability/whereabouts. For this,
  the agency should use external databases and other medium through three FTEs using internet (including social
  media), telephone and other means."
- Note: this is a bank's general retail/MSME/agri dues RFP, not card-only.

**1.2 RBL Bank's retail collection policy: amount at risk + bucket decide the strategy; bucket 1 = calls, bucket 2 = 100% field.**
SOURCED. *Retail Collection Policy*, RBL Bank (PDF created 19 Jan 2018).
https://webassets.rbl.bank.in/document/Bank%20Policies/Retail-Collection-Policy.pdf
- "The collection process will be a mix between in-house calling by affiliate officers and field visitations by
  affiliate officers/Managers and external agency employees. ... The stage of delinquency and the amount at risk will
  largely determine the specific collection strategy."
- "Specific account: Assignment logic will be done based on strategy considering area, coverage etc."
- Collection Strategy Matrix: Bucket 1 "Tele Calling and selective field calling"; Bucket 2 "100% to be referred on
  field. Field referral continues, with necessary support of legal action U/s 138"; Bucket >=4 "Field follow-up along
  with necessary legal action ... once the asset is declared NPA".
- Note: retail loans policy (mentions Sec 138 cheques, SARFAESI), not card-specific. Used here for the logic, not for card numbers.

**1.3 Collection-tech vendor: field collection is for larger/complex cases and usually starts at 30-60 DPD.**
PARTLY (vendor marketing). Credgenics, "CG Collect" field collections page (undated, opened 2026-10-12).
https://www.credgenics.com/cg-collect-field-debt-collections
- "Field debt collections are typically employed for larger or more complex debt cases"
- "The field debt collections process is usually initiated between the 30 DPD and 60 DPD buckets"

**1.4 SBI Card: reminders by post/phone/SMS etc., then third-party agents; agent name given to cardholder.**
SOURCED. *Policy for the Issuance and Conduct of Credit Cards*, SBI Card, dated 15-8-2022.
https://www.sbicard.com/sbi-card-en/assets/docs/pdf/who-we-are/notices/policy-for-the-issuance-and-conduct-of-credit-cards-15-8-2022.pdf
- "In the event of default, the Cardholder will be sent reminders from time to time for settlement of any outstanding
  on the card account, either by post, fax, telephone, e-mail, SMS, or any other mode decided by us, and/or we may
  engage third parties to remind, follow up and collect dues. ... The name and contact details of the recovery agent
  shall be provided to the cardholder upon assigning the agent to such cardholder."

**1.5 SBI Card's own timeline of what happens to the card: block, then write-off after more than 6 missed payments.**
SOURCED. SBI Card FAQ "Credit Card Blocking & Unblocking" (opened 2026-10-12).
https://www.sbicard.com/en/faq/card-blocking-unblocking.page
- Headings: "Irregular payments : First payment default" ("your card may be blocked for further usage"); "Up-to 3
  consecutive payments default"; "4-6 consecutive payments default"; "Written-off accounts : More than 6 consecutive
  payments default".
- "In case your SBI Card account has been written-off, credit facility on your card will be permanently withdrawn" and
  it "cannot be re-activated."
- "In case your account is written-off and you pay complete outstanding as per the agreement, we will process your
  request for CIBIL status clean-up ... the process may take 45-60 days post realization of funds."

**1.6 SBI Card says collections are being steered by geography/segment and the environment is "tougher".**
SOURCED. SBI Card Q4 FY25 earnings call transcript (April 2025).
https://www.sbicard.com/sbi-card-en/assets/docs/pdf/who-we-are/notices/SEFilingEarningCallTranscript-apr25.pdf
- "We continue to take various measures to further strengthen our collection capabilities and expand capacity across
  digital and physical channels"
- "this also informs our collection strategy around how to move to different pockets, different segments, different
  geographies."
- Salila Pande: "there is a much more tougher collection environment right now. And we have experienced that there has
  been some stickiness in terms of collections, and there has been a bigger flow from Stage 3 to write-off."

**1.7 PSU bank rule-book: agencies get districts; who allocates depends on the amount.**
SOURCED. PNB SASTRA Division, *Salient features of policy for engagement of Recovery Agencies/Resolution Agents* (PDF
created 14 Jun 2021). https://pnb.bank.in/downloadprocess.aspx?fid=cT0Zz2WiAeLAecOeYnil0A%3D%3D
- "Recovery Agencies/Resolution Agents shall be empanelled for the entire District or Cluster of Districts."
- "Recovery Agencies – Ledger Outstanding Upto Rs. 10 lacs"
- Allocation: "Accounts upto Rs 1.00 lacs — Branch Head"; "Accounts above Rs. 1.00 lacs upto Rs 10.00 lacs — Circle SASTRA Head"
- Scope: "All NPA accounts under Doubtful and Loss category (whether non-suit filed, suit filed or decreed) and also all
  written off accounts". Note: PSU bank NPAs generally (loans), not card-only.

**1.8 Card-issuer agency lists: agencies in Andhra Pradesh/Telangana sit in Hyderabad, Vizag, Vijayawada and cover named cities.**
SOURCED (document undated; titled "Repayment_Agencies_Q3"). OneCard *List of Authorized Collection Agencies* for
"OneCard Credit Card Issuing Banks: SBM Bank (India) Limited, South Indian Bank Limited, Federal Bank Limited, CSB Bank
Limited, BOB Financial Solution Limited". https://www.getonecard.app/legal/Repayment_Agencies_Q3.pdf
- Columns "City_MAT / State_MAT / Address". AP/TS rows name only these coverage cities: Hyderabad, KarimNagar,
  Warangal (Telangana), Vizag, Vijayawada (Andhra Pradesh); e.g. row 14 "Ankuri Associates | Hyderabad, KarimNagar,
  Warangal | Telangana | ... Begumpet, Hyderabad 500016"; row 82 "SriHarshini Associates | Vizag | Andhra Pradesh".
- Several agencies are listed as "All India" (row 1 "FPL Technologies Pvt Ltd All India", row 2 "4Front Solutions All India").
- Our reading (INFERENCE): field coverage is mapped to cities; a village address in a district not on the list would be
  reached by phone/letter or by a city agency travelling, not by a local office. We found no published issuer rule saying this.

**1.9 Industry picture: thousands of small city-based agencies; bots/SMS first, defiant borrowers to local agencies.**
SOURCED (journalism, ~May-June 2023). Anand Adhikari, "Loan-recovery agents or bullies? Inside the dark underbelly of
Indian banking", Business Today. https://www.businesstoday.in/interactive/longread/loan-recovery-agents-or-bullies-inside-the-dark-underbelly-of-indian-banking-262-01-06-2023
- "The industry has a high mortality rate, with most operating regionally or in a city; few national recovery agencies exist."
- "Thousands of such mom-and-pop recovery offices, mostly sole proprietorships, operate from dingy places."
- "The model is to push calls via bots, send SMS and reminders, and manage collection," (Nikhil K. Shetty)
- "So, the job of handling defiant borrowers is gradually shifting to local-level recovery agencies."
- Good Luck Recovery Agency "specialises in the recovery of personal loans and credit cards."
- Banks hand delinquent accounts to agencies by bucket; if one fails, lenders "hand over the loans in the next bucket to another player."

**1.10 Digital legal notices and online arbitration are now bought as a service by a card issuer (BOBCARD).**
PARTLY (search snippets of BOBCARD tender documents; the PDFs could not be opened: TLS chain error on media.bobcard.co.in).
BOBCARD "RFP - Empanelment & Selection of vendor for Legal Support to Collections Unit" (Aug-Sep 2024); pre-bid
responses 17.09.2024: https://media.bobcard.co.in/media/u43ii4id/pre-bid-responses-17092024.pdf ; tender archive
https://www.bobcard.co.in/tender-archive
- Snippet: "The bidder/OEM shall have ability to send digital legal notices to delinquent / NPA/write off Customers via
  whatsapp, email, text messages through the digital platform." Part B: "Online Arbitration". Re-open before quoting on screen.

---

## 2. Recovery agency economics

**2.1 Agencies are paid a cut of what they recover, and the cut is higher for small and old accounts (PNB).**
SOURCED. PNB policy (link in 1.7). "The Agency will be paid commission on the amounts recovered as under:" For NPA
accounts up to Rs 10 lacs:

| Age of NPA | O/s up to Rs 1 lac | O/s above Rs 1 lac | Decreed a/cs |
|---|---|---|---|
| Upto 3 years | 7.5 % | 5.0 % | 5.0% |
| Above 3 up to 5 years | 10.0 % | 7.5 % | 7.5% |
| Beyond 5 years | 15.0 % | 10.0 % | 10.0% |

"(b) For actual written off accounts, the balance as on the date of allotment of the account, be considered for fixation of commission slab."

**2.2 Bank of Maharashtra slab: 12% on NPAs up to ₹2 lakh, falling to 5% above ₹25 lakh; only on cash recovered.**
SOURCED (old: 30/10/2014, Jaipur Zone; NPA loans generally).
https://bankofmaharashtra.bank.in/writereaddata/documentlibrary/8c9f0623-7bfb-41de-b36d-cd3a60f118d5.pdf
- "Recovery effected in NPAs having ledger balance upto INR 2 lakhs ... 12% of Cash Recovery made in each account";
  "above INR 2 lakhs and upto INR 10 lakhs ... 10%"; "above INR 10 lakhs and upto INR 25 lakhs ... 7%"; "above INR 25 lakhs ... 5%"
- Column header: "Outer Limit approved by Head Office inc. Out of Pocket Expenses*" and "* NEGOTIABLE ON CASE-TO-CASE BASIS"
- Practical point (OUR ARITHMETIC): on a ₹10,000 recovery at 7.5% (PNB) the agency earns ₹750; at 12% (BoM) ₹1,200,
  and that has to cover travel ("Inc. Out of Pocket Expenses"). On ₹2 lakh at 10% it is ₹20,000. This is why a long
  trip for a small dues account rarely pays. INFERENCE, not a published rule.

**2.3 Tracing a borrower who moved is a separately paid job (detective agencies).**
SOURCED. PNB policy (link in 1.7), "Policy on engagement of Detective Agencies":
- Task: "Locate the borrower(s)/ co-borrower(s)/ guarantor(s)/ mortgagor(s), (in/outside India) including their legal
  heirs who are either untraceable or not available at the addresses given in Bank's records"
- Fee: "On receipt of information about whereabouts of the missing/absconding borrower ... Rs. 7,500/- per person
  subject to maximum fee of Rs. 45,000/- ... per account." Out of pocket "subject to maximum of Rs. 10,000/- per account."
- INFERENCE: a ₹7,500 tracing fee only makes sense on larger balances; for a ₹10,000 card due it would cost most of the debt.

**2.4 Industry spend and success rate.**
SOURCED (Business Today, link in 1.9).
- "The cumulative spend on collection by banks and NBFCs is a whopping RS 42,000 crore annually." (Rishabh Goel)
- Ketan Purohit (Pioneer Services): "the success rate is 15-16 per cent in recovering bad loans"; "There is an
  accelerated incentive structure, which serves as a carrot to recover a higher percentage."
- "Unlike earlier days, skip tracing is possible today on the strength of tech because of the customer's digital footprint," (Ravinder Beniwal)
- "We have trained 300,000 agents since the beginning. Last year, it was around 30,000-plus," (Biswa Ketan Das; IIBF-type DRA training)

**2.5 Field networks are big but city/pincode-mapped; AI voice is being pitched to replace human callers.**
- SOURCED. The Wire / PTI PR, 19-20 Aug 2025: Arrise has "a presence across 25+ Indian states through a network of over
  5,000 professionals"; combined Credgenics "on-field operations across 18,000+ pin codes".
  https://m.thewire.in/article/ptiprnews/credgenics-acquires-arrise-to-reshape-field-collections-with-tech-enablement
- PARTLY (company claim). CIOL, 01 Oct 2026: Credgenics Prix AI "matched or exceeded human recovery rates" in internal
  tests; supports "more than 12 Indian languages"; trained on "more than 1 billion collections conversations".
  https://www.ciol.com/startup-circle/credgenics-prix-ai-voice-platform-debt-collections-12614807
- INFERENCE: India has roughly 19,000+ pin codes (not checked this session), so "18,000+" is broad but still a
  vendor claim. Do not say "agents cannot reach villages"; say "most agencies sit in cities and work by pincode lists".

**2.6 Address used: residence first, then other addresses, references, and "skip" tracing.**
SOURCED. RBL Retail Collection Policy (link 1.2):
- "The first visit /contact with the customer should be at his place of residence/ mobile. ... When the Collection Unit
  is unable to contact the customer at his residence/ mobile, the customer may be contacted at his/her other address or
  number/through borrower or referee or guarantor."
- "Collections Representative may communicate with third parties to obtain customer's location information ... when the
  customer's present location is either unknown or uncertain or the customer is not contactable or a skip."
- "if the customer is deeply delinquent (more than or equal to 2 months behind ...) or non-contactable or a skip, then
  customer's debt/obligation may be discussed with references provided."
- UNVERIFIED: any published rule that agents use the Aadhaar address vs the card's communication address. Not found.
  Our inference: the file has every address the customer gave (application, KYC, office), and agencies are allocated by
  the address's city/pincode (1.8, 1.2 "considering area, coverage").

---

## 3. Legal route: what it costs and where it happens

**3.1 Court fee for a money suit in Telangana/AP is ad valorem on the amount claimed; heavier, in percent, on small claims.**
PARTLY (Act text from Indian Kanoon, which itself warns it "could not be verified"; our arithmetic).
Telangana Court-fees and Suits Valuation Act, 1956 (adapted from the AP Act). https://indiankanoon.org/doc/19846625/
- Section 20: "In a suit for money (including a suit for damages or compensation, or arrears of maintenance ..." "fee
  shall be computed on the amount claimed."
- Schedule I Art. 1(c) (per AP Second Amendment Act 1958, as reproduced): 60 np per Rs 5 up to Rs 100; Rs 1.10 per Rs 10
  to Rs 1,000; Rs 7.50 per Rs 100 to Rs 10,000; Rs 30 per Rs 500 to Rs 20,000; Rs 40 per Rs 1,000 to Rs 30,000; Rs 60
  per Rs 2,000 to Rs 50,000; Rs 80 per Rs 4,000 to Rs 1 lakh; Rs 100 per Rs 10,000 above Rs 1 lakh.
- OUR CALCULATION (cumulative): ₹10,000 → about ₹786 (7.9%); ₹50,000 → ₹2,386 (4.8%); ₹1 lakh → ₹3,426 (3.4%);
  ₹2 lakh → ₹4,426; ₹5 lakh → ₹7,426; ₹10 lakh → ₹12,426 (1.2%). The ₹1 lakh = ₹3,426 and ₹10 lakh = ₹12,426 figures
  match a third-party calculator seen in a search snippet (defend.ink); the page itself did not render numbers. Have a
  Hyderabad advocate confirm before putting numbers on screen.

**3.2 DRT is not available below ₹20 lakh.** SOURCED. Ministry of Finance notification S.O. 4312(E), F. No. 3/4/2018-DRT,
6 Sept 2018 (reproduced on taxheal): "the provisions of the said Act shall not apply where the amount of debt due to any
bank or financial institution ... is less than twenty lakh rupees." https://www.taxheal.com/?p=68695

**3.3 Card issuers do take card dues to Lok Adalat pre-litigation, in the borrower's city.**
SOURCED. *SBI Cards & Payments vs Sajji Varghese*, M.P. State Consumer Commission, Bhopal, 28 June 2024.
https://indiankanoon.org/doc/68016726/ - dues "Rs.1,82,969/-" pending from November 2017; "In June 2019, the Company
filed a pre-litigation in National Lok Adalat, Indore"; account written off; Rs.2,55,662.89 pending when shown written
off. Commission held SBI Card deficient for reporting to CIBIL without proper prior intimation; Rs 2,000 costs.

**3.4 Telangana runs large Lok Adalats; banks request special sittings.**
PARTLY (search summary of LiveLaw; not opened). TSLSA special Lok Adalat, 18 July 2025: 3,146 cases settled (318
pre-litigation, 2,828 cheque dishonour), ~₹41.29 crore; "on the request of the Union Bank of India, a Special Lok Adalat
was organise[d]". https://www.livelaw.in/news-updates/tslsa-over-3100-cheque-dishonour-pre-litigation-cases-settled-first-special-lok-adalat-542180
No card-specific counts found.

**3.5 Bank-run "arbitration" of retail dues happens at huge scale, and courts are voiding awards by one-sided arbitrators.**
- SOURCED. The Law Advice, 06 Oct 2026, Delhi HC Division Bench (Prathiba M. Singh, Dinesh Bhatt JJ), *Shikha Ghosh v.
  Axis Bank*: "approximately 76,000 arbitral awards had been passed pan-India" by sole arbitrators unilaterally appointed
  by Axis Bank; one arbitrator "handled as many as 4,155 arbitration proceedings involving Axis Bank"; "the High Court
  declared the May 26, 2023 arbitral award unenforceable"; the court "directed the Reserve Bank of India (RBI) ... to
  caution banks and financial institutions". Loan in that case: "approximately ₹16.66 lakh" (type not stated).
  https://www.thelawadvice.com/news/one-arbitrator-4-155-axis-bank-cases-delhi-high-court-raises-serious-concerns-over-unilateral-appointments
- SOURCED (self-reported by platform). Sama: "Sama has resolved over 35 Lakh disputes in India, ranging from E-commerce
  disputes to Credit Card default." https://www.sama.live/rules_and_procedures-2024
- PARTLY (search snippet of offer T&Cs, not the main card agreement): SBI Card offer terms say disputes go to "a sole
  arbitrator appointed by SBICPSL", seat New Delhi. Not confirmed for the cardholder agreement.
- PARTLY (search summary only): a Tis Hazari commercial court (Delhi) judgment of 6 Nov 2025 on a Section 34 petition
  against a 15 Nov 2022 award by a sole arbitrator appointed by SBI Cards; outcome not confirmed (page timed out).
- Practical point (INFERENCE, consistent with 3.5): a person may receive an arbitration notice or award by WhatsApp/email
  from a city they never lived in (Mumbai/Delhi seat). Tell viewers to reply in writing and get a lawyer, not to panic or
  ignore. Legal analysis belongs to the legal researcher.

**3.6 Section 138 NI Act / Section 25 PSS Act for card dues.** UNVERIFIED for card-specific practice. Law-firm explainers
(not opened) say NACH/ECS dishonour is prosecutable like a cheque under PSS Act s.25. RBL's loan policy (1.2) uses Sec 138
in buckets 2-3 for loans with cheques. We found no data on card issuers filing these for card dues. Do not say it happens.

**3.7 Advocate fees, civil suit duration, how often banks sue for small card dues.** UNVERIFIED. Nothing found on an opened page.

---

## 4. Write-off and sale to ARCs

**4.1 Written-off unsecured retail loans sell for roughly 9 to 20 paise per rupee (2023-2025 deals).**
- SOURCED. Bandhan Bank BSE/NSE filing BBL/SEC/178/2025-26, 29 Dec 2025:
  https://bandhan.bank.in/sites/default/files/2025-12/Conclusion-of-sale-of-identified-unsecured-NPA-and-Written-off-Portfolios.pdf
  "Unsecured NPA Portfolio with more than 180 Days Past Due, having principal outstanding of Rs. 3,165.25 Crore ... for
  consideration of Rs. 569.75 Crore, on Security Receipts ('SR') basis" (about 18%, our arithmetic) and "Unsecured
  Written-off Loan Portfolio, having principal outstanding of Rs. 3,707.11 Crore ... to Phoenix ARC Private Limited ... at
  Rs 331.97 Crore" (about 9%). These are microfinance/small-business loans, NOT cards.
- SOURCED. Venture Intelligence, 7 Apr 2023 (citing ET): Phoenix ARC bought unsecured loans "up to INR 8,000 crore" from
  Bandhan, ESAF, Equitas for ~INR 1,500 crore, "a 15-20% recovery for the lenders"; "All deals were done under the 15:85
  structure". https://news.ventureintelligence.com/others/phoenix-arc-buys-loans-of-rs.8,000-cr-from-bandhan,-esaf-sfb,-equitas-for-rs.1,500-cr-
- SOURCED. Angel One, 21 Aug 2024: Phoenix ARC (Kotak-backed) put up NPAs "valued at over ₹3,550 crore" incl.
  "approximately 5.60 lakh unsecured accounts amounting to ₹3,363 crore"; pricing not disclosed. (Our arithmetic: about
  ₹60,000 per unsecured account.) https://uatcdn.angelone.in/news/share-market/phoenix-arc-backed-kotak-mahindra-group-sell-npas

**4.2 Credit-card dues do end up with ARCs and the ARC shows on the credit report / demands money.**
PARTLY. LiveLaw, 31 Jul 2024, Chandigarh District Commission, *Paramjit Kaur Pasricha vs HDFC Bank Ltd and Anr.*, CC
539/2023, order 11.07.2024: HDFC card balance "Rs. 72,927/-" and a Phoenix ARC account "Rs. 1,17,432/-"; Commission
ordered both to withdraw demands, issue NOC, correct CIBIL. The article does not say the ARC account was an assigned card
debt. https://www.livelaw.in/amp/consumer-cases/chandigarh-district-commission-hdfc-bank-phoenix-arc-illegally-demanding-outstanding-balance-unauthorized-credit-cards-265132
- UNVERIFIED: any named 2024-2026 sale of a credit-card portfolio by SBI Card/HDFC/ICICI/Axis, and its price. Not found.
- Business Today 2023 (link 1.9): ARCs buy NPA pools but "banks are generally not willing to sell them"; "A typical
  portfolio coming to market would be somewhere from 700 to 1,000 days past due." (Neeraj Mohan, IARC). SOURCED.
- Safe framing: "Old unsecured dues can be sold to a reconstruction company for a small fraction of their value; the
  calls then come from the new owner, and the debt is not cancelled." The "not cancelled" part: SBI Card FAQ (1.5) shows a
  written-off account still has to be paid "as per the agreement" for CIBIL clean-up.

---

## 5. Settlement reality

**5.1 Published settlement percentages come only from settlement-firm marketing.** PARTLY at best (search summary of
credsettle.com, freed.care etc.; not opened; commercial interest): "banks typically settle for 40-60%", "25% and 70%"
for HDFC by "account vintage, default duration". Do NOT put a percentage on screen as fact. If used: "debt-settlement
companies claim ..." with attribution.

**5.2 'Settled' hurts future borrowing; 'written off' too; 'closed' is the clean status.**
SOURCED. Experian India, Ashish Singhal (MD), "How loan a/c status affects credit scores?", July 2019.
https://experian.in/2019/07/28/how-loan-ac-status-affects-credit-scores
- "the status 'settled' affects your future credit prospects, which in turn will have a negative impact on your credit score."
- "lenders view settled accounts negatively"; "Like Settled, Written Off can dent your chances of a loan or a credit card."
- "Live and closed loans have a positive impact on your credit score, as long as you have made all the payments regularly."

**5.3 Paying the full amount after write-off gets the CIBIL status cleaned (SBI Card).** SOURCED (1.5).

**5.4 Real disputes: banks fail to update CIBIL after settlement / demand more after accepting part.**
PARTLY (casemine commentary via search snippet): Bathinda District Commission, Apr 2024, *Anil Kumar v. Axis Bank*:
bank "accepted a partial settlement of Rs.51,000/- against an alleged outstanding of Rs.51,929.68/- and later demanded an
additional Rs.17,989.26/-". Lesson (SAFE): get the settlement letter in writing before paying.

**5.5 Settlement offers by age of default.** UNVERIFIED in bank documents. Indirect, SOURCED: PNB pays agencies more for
older NPAs (2.1: 7.5% up to 3 yrs, 15% beyond 5 yrs on ≤₹1 lakh), and written-off pools sell for 9-18% (4.1). INFERENCE:
the older the debt, the less the lender expects to get, so offers tend to soften with time. Say it as reasoning.

**5.6 Tax angle.** Not researched further; nothing found.

---

## 6. Charges that pile up (inputs for our 3/6/12-month calculation)

All fees below are "excl. GST"; GST 18% applies on fees and interest.

| Item | HDFC Bank | ICICI Bank (Amazon Pay card MITC) | SBI Card | Axis Bank |
|---|---|---|---|---|
| Interest | 3.75%/month (45% p.a.) "All other variants" | 3.75%/month (45%), w.e.f. Nov 15, 2024; "In case of default, interest charges may increase up to a maximum of 3.8% per month (46% per annum)" | 3.75% p.m. from 1 Nov 2024 (news) | 3.75% per month |
| Late fee ≤₹100 | Nil | Nil | Nil (to ₹100, from 1 May 2026) | Nil below ₹500 |
| ₹101-500 | ₹100 | ₹100 | ₹100 | Nil |
| ₹501-1,000 | ₹500 | ₹500 | ₹500 | ₹500 (₹501-5,000) |
| ₹1,001-5,000 | ₹600 | ₹600 | ₹750 (₹1,001-10,000) | ₹500 |
| ₹5,001-10,000 | ₹750 | ₹750 | ₹750 | ₹750 |
| ₹10,001-25,000 | ₹900 | ₹900 | ₹950 | ₹1,200 (₹10,001-50,000) |
| ₹25,001-50,000 | ₹1,100 | ₹1,100 | ₹1,100 | ₹1,200 |
| Above ₹50,000 | ₹1,300 | ₹1,300 | ₹1,300 | ₹1,300 |
| Extra if MAD missed 2 cycles | not seen | not seen | ₹100 per cycle (news) | "An additional INR 100 charge ... if the 'Minimum Amount Due (MAD)' is not paid for two consecutive cycles and will apply until the MAD is cleared" |
| Over-limit | 2.5% of overlimit, min ₹550 (with consent) | 2.50%, min ₹550 | 2.5%, min ₹500 (older MITC) | 2.5%, min ₹500 |
| Payment return / auto-debit fail | 2% of payment, min ₹450 | 2% of Total Amount Due, min ₹500 | 2% of payment, min ₹350 (older MITC) | 2% of payment, min ₹500 |
| Cash withdrawal fee | 2.5% or ₹500, higher | 2.50%, min ₹500 | 2.5%, min ₹300 (older MITC) | 2.5% (min ₹500) |

Sources (all opened):
- HDFC: *Key Fact Statement cum MITC*, "Version 4.13 Dated – September 2026", "Updated on 08th October'26".
  https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/cards/credit-cards/personal-mitc/mitc-in-english.pdf
  Same slabs in Swiggy HDFC KFS "w.e.f. 1st Oct, 2025": https://media-assets.swiggy.com/portal/static-assets/others/key_fact_statement.pdf
- ICICI: Amazon Pay ICICI MITC "Last updated on July10, 2026": https://www.icici.bank.in/terms-condition/tnc-for-amazon-pay
  Late fee basis: "Outstanding = Total Amount due (as of previous statement) – Payment received before payment due date."
  GST: "Presently the GST rate for banking and financial services is at 18% (applicable on all fees, interest, surcharge
  and other charges)." Compounding: "Effective Oct 26, 2023, any fee/GST transaction on the customer's statement after Oct
  26, 2023 will not be compounded for interest calculation." Cash: "interest will be levied on all cash advances from the
  date of the transaction".
- SBI Card late fees: SBI Card notice "With effect from 1st May 2026" (BPCL SBI Card notice, current and revised tables):
  https://www.sbicard.com/sbi-card-en/assets/docs/pdf/Revisions.pdf ; corroborated by Angel One, 2 Apr 2026: "outstanding
  amounts between ₹1,000 and ₹10,000 will continue to attract a fee of ₹750" and "an additional ₹100 charge may be levied
  if the minimum due is not paid for two consecutive billing cycles".
  https://www.angelone.in/news/personal-finance/sbi-card-revises-late-payment-charges-from-may-1-2026-fees-up-for-small-dues
  NOTE: the notice is addressed to BPCL SBI cardholders; "Rest of the charges remain unchanged" (snippet). PARTLY for
  other SBI cards. SBI interest 3.75%: Goodreturns, 7 Oct 2024: "the rate of Finance Charges will be revised to 3.75%
  p.m." effective 1 Nov 2024. https://www.goodreturns.in/news/sbi-credit-card-sbi-revises-credit-card-charges-declares-2-big-changes-details-inside-1380659.html
  Over-limit/dishonour/cash fees are from the older SBI MITC (service-tax era):
  https://www.sbicard.com/sbi-card-en/assets/docs/pdf/most-important-terms-and-conditions/English%20MITC.pdf . PARTLY.
- Axis: Axis Bank Freecharge Plus card page (opened 2026-10-12), "Finance Charges (Retail purchases and Cash) 3.75% per
  month". https://www.axis.bank.in/cards/credit-card/axis-bank-freecharge-plus-credit-card ; Outlook Money, 19 Aug 2026:
  top slab moves to ₹1,300 "From August 28" 2026.
  https://www.outlookmoney.com/banking/credit-card/axis-bank-credit-card-users-to-face-higher-forex-markup-late-fees-from-august-28

Minimum due (for the calculation): HDFC: "MAD = Total GST + EMI amount + 100% of Fees/Charges + ... 5% of [Retail
Spends ...]" and "where MAD value ... falls below or equal to Rs 200, the MAD value will be charged as Rs 200/-"
(Swiggy HDFC KFS). SBI (older MITC): "5% of Total Outstanding (Min. Rs. 200) + all applicable taxes".

Calculation notes for us (INFERENCE on how to model): interest runs on the whole balance from the transaction dates once
the bill is not paid in full; effective monthly cost on interest = 3.75% × 1.18 = 4.425%; plus one late fee + 18% GST
each missed due date; ICICI does not compound interest on fees/GST since Oct 2023 (others not checked). A ₹10,000
balance attracts a ₹750 late fee (HDFC/ICICI/SBI/Axis), i.e. 7.5% + GST per month on top of interest; a ₹1,00,000
balance attracts ₹1,300, i.e. 1.3%. So small balances grow faster in percent from fees. Card stops being usable (1.5), so
no over-limit on new spends, but fees+interest can push the balance over the limit (SBI: "Over-limit status may also be
applied because of fees and/or interest charges").

---

## 7. Data on delinquency and harassment

**7.1 Bureau data: 91-180 DPD on cards 7.6% (June 2024); small-limit cards riskiest.**
SOURCED. CRIF High Mark news, 13 Dec 2024: 91-180 days "risen by 110 basis points to 7.6 per cent as of June 2024"
(6.5% June 2023); 181-360: 0.7% → 0.9%; above 360: 1.3% → 1.7%; average balance Rs 32,233.
https://www.crifhighmark.com/news-events/news/2024/dec/credit-card-delinquencies-rise-by-110-bps-says-study
SOURCED. CRIF High Mark, 12 Dec 2024: "Cards with limits under Rs 50,000 showed the highest risk, with a 31-90 day DPD
rate of 3.2%, up from 2.5% in Jun 2022."
https://www.crifhighmark.com/news-events/news/2024/dec/credit-cards-seeing-slower-issuance-and-higher-delinquencies-crif-report
SOURCED. Moneylife, 14 Jul 2025 (CRIF report): credit card "PAR of over 90 rising to a staggering 15%".
https://moneylife.in/article/highvalue-loans-rise-in-india-as-delinquencies-surge-in-smallticket-lending-crif-high-mark-report/77671.html
(Different bureaus measure differently; TransUnion CIBIL's balance-level 90+ was ~2.00% in Mar 2025 per search snippet only: UNVERIFIED.)

**7.2 RBI: PSU banks' card NPAs 14.3%, private banks 2.1% (March 2025).**
SOURCED. The Week/PTI, 30 Jun 2025 (RBI FSR June 2025): "Public sector banks' (PSBs) gross non performing assets (NPAs)
from the credit cards portfolio inched up to 14.3 per cent"; private "staying stable at 2.1 per cent".
https://www.theweek.in/wire-updates/business/2025/06/30/dcm98-biz-rbi-report-credit-card.html

**7.3 RBI Ombudsman: card complaints up 20% in FY25, second-biggest category. No recovery-agent count published there.**
SOURCED. RBI *Annual Report of the Ombudsman Scheme 2024-25*. https://rbi.org.in/Scripts/PublicationsView.aspx?id=23441
- "Complaints related to Credit Cards increased by 20.04 per cent and has become the second highest contributor of complaints."
- Appendix 1.6, against banks: Credit Cards 24,549 (2022-23), 33,198 (2023-24), 41,457 (2024-25, 17.16%); against NBFCs 9,063 (2024-25).
- Appendix 1.1 complaints per lakh accounts: Telangana 8.2, Andhra Pradesh 5.0, all-India 7.7.
- No separate recovery-agent harassment number found in the report text. UNVERIFIED for any such figure.

**7.4 AP/Telangana harassment cases are mostly LOAN APPS, not bank cards.** Keep them separate in the script.
- SOURCED. The South First, 18 Oct 2022: AP police "arrested at least 71 persons in the last few months and also brought
  down at least 173 loan apps". https://thesouthfirst.com/andhrapradesh/loan-app-andhra-police-devise-protocol-to-deal-with-the-deadly-menace/
- SOURCED. Siasat, 9 Oct 2026: Kukatpally techie borrowed "over Rs 1.5 crore" from 34 loan apps; cybercrime police
  registered case under BNS 308(5), 351(2)a, 318(4) and IT Act 66-C, 66-D, 67.
  https://siasat.com/hyderabad-techie-loses-rs-22-lakh-to-extortion-by-loan-agents-3554580
- UNVERIFIED: a 2024-2026 Hyderabad police case against a bank credit-card recovery agency. Not found. Do not imply one.

---

## 8. Multiple cards (owner's added scope)

### 8a. Several cards from DIFFERENT banks

**8a.1 Every issuer reports to the bureaus every month, so the other banks see the default.**
SOURCED. ICICI MITC (link §6): "The Bank submits the Card Member's data to CIBIL ... every month in the format prescribed
by CIBIL. This data includes the repayment status of all Cardholders". HDFC Card Member Agreement (footer "As on
September 25, 2026"): "information on usage of credit facilities by customer(s) is/are exchanged across Banks, credit
bureaus and financial institutions."
https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/cards/credit-cards/membership-kit/card-member-agreement-29-10-2019.pdf
RBI IRAC Master Circular 1 Apr 2025, para 4.2.19.3: "Banks shall report a credit card account as 'past due' to credit
information companies (CICs) ... only when a credit card account remains 'past due' for more than three days."
https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=12822

**8a.2 Other issuers may cut your limit using bureau history.**
SOURCED. SBI Card policy 15-8-2022 (link 1.4): "SBI Card may review credit limit for cardholder's account, which include
but not limited to account performance, cardholder's spending, payment and delinquency patterns, credit bureau history,
behavior score and other portfolio triggers." ... "Pro- active limit decrease, which may be permanent or temporary,
initiated by SBI Card, is informed to the customers through SMS / e-mail/letter."
SOURCED. HDFC agreement: "Bank reserves the right to decrease and/or unconditionally cancel the limit assigned on the
Card with due intimation to the card member." ICICI MITC: "ICICI Bank shall at its sole discretion be entitled to review
(including enhancement or reduction), the credit limit ... at any time and only enhancements ... shall be effected ...
along with the consent of the Card Member."
UNVERIFIED: news of a 2024-2026 wave of limit cuts triggered by defaults elsewhere (only blogs found). So: "can", not "will".

**8a.3 The same agencies often work for several lenders.** SOURCED for agencies, INFERENCE for the same person.
OneCard list (1.8) is one agency list for five issuing banks. BOBCARD legal-support RFP asked that "the bidder should be
empaneled with minimum 3 reputed banks/financial institutions for similar work" (search snippet; PARTLY). PNB policy
values "feedback from other Banks". Whether one agent ends up holding one person's accounts from two banks: UNVERIFIED.

**8a.4 Which bank chases first/hardest.** UNVERIFIED. Our inference from §2: balance size and bucket drive the effort
(RBL: "The stage of delinquency and the amount at risk will largely determine the specific collection strategy"), so the
biggest balance at the most aggressive issuer usually gets the most calls; a ₹50k card may stay in tele-calling while a
₹3L card gets field referral. No issuer publishes this.

**8a.5 Settling one bank and the others.** INFERENCE: each issuer's account is reported separately; a 'settled' line on one
does not change the others' status, but it is a negative mark lenders see (5.2). No source says one settlement triggers
action by other banks.

### 8b. Several products at the SAME bank

**8b.1 Shared/combined limit across cards of one issuer.**
SOURCED. ICICI MITC: "In cases where multiple credit cards are mapped to one customer, total spends can be done only up to
the combined aggregate credit limit calculated over all the credit cards cumulatively. It is clarified that the aggregate
credit limit has been defined as the maximum limit across all the credit cards held by the customer."
SOURCED. HDFC MITC (Pixel): "In case of cardholders holding both VISA & RuPay variants of Pixel credit card, a single
statement will be issued ... The Minimum Amount Due (MAD) & Total Amount Due (TAD) will be calculated on the combined
outstanding of both the cards". SBI MITC: "Add-On cardholders share the same limits as that of the Primary Account Holder".

**8b.2 Cross-default: default on one facility lets the bank act under all your agreements with it.**
SOURCED. HDFC Card Member Agreement, heading "CREDIT REFERENCING BUREAU CROSS DEFAULT": "if the Cardmember fails to pay any
monies when due ... or commits any other default under any agreement (including this agreement) with HDFC Bank under
which the Cardmember is enjoying any financial/credit/other facility, then in such event HDFC Bank shall ... be absolutely
entitled to exercise all or any of its rights under any of the Cardmember's agreements (including this agreement) with
HDFC Bank". SBI Card MITC: "SBICPSL can suspend the facility on the Credit Card, if the Cardholder defaults on the payment
due" and the cardholder must "immediately pay SBICPSL the total outstanding Balance on the Account".
https://www.sbicard.com/sbi-card-en/assets/docs/pdf/most-important-terms-and-conditions/english-mitc.pdf

**8b.3 Set-off against your savings/salary account, FDs, even demat holdings at that bank (clause text).**
SOURCED. HDFC Card Member Agreement: "the Bank, at any time and without notice, will have a lien and right of set-off on
all monies belonging to the Cardmember and/or Add-on Cardmember standing to their credit in any account whatsoever with
the Bank ... If upon demand by the Bank, the balance outstanding on the Card Account is not repaid within the prescribed
time, such credit balance in any account including fixed deposit accounts and any properties ... including but not
limited to dematerialised shares or other securities ... held by the Bank as a Depository Participant, may be adjusted
towards dues under the Card Account."
PARTLY (search snippets, not opened): IDFC First, AU SFB, RBL, SBM card agreements carry similar lien/set-off clauses.
SBI Card is a separate company (SBICPSL), not SBI the bank, so an SBI savings account is not the same entity. INFERENCE
from entity names; set-off law itself: legal researcher.

**8b.4 Add-on cards: the primary pays.** SOURCED. HDFC agreement: "The Cardmember will be fully responsible and liable
for all transactions incurred on the Add-on Card(s)"; "The primary applicant will be liable for all charges incurred with
the Add-on card(s)". But note the set-off clause also names "Add-on Cardmember" monies (8b.3). ICICI: "Terms and
Conditions governing Credit Card Facilities shall be applicable to the Supplementary Card Holders as well".

**8b.5 One NPA = all facilities NPA (borrower-wise).** SOURCED for the rule; UNVERIFIED for how banks apply it to retail cards.
RBI IRAC Master Circular, 1 Apr 2025, para 4.2.7.1 "Asset Classification to be borrower-wise and not facility-wise": "all
the facilities granted by a bank to a borrower and investment in all the securities issued by the borrower will have to
be treated as NPA/NPI and not the particular facility/investment or part thereof which has become irregular." Para
4.2.19.2: "A credit card account will be treated as non-performing asset if the minimum amount due ... is not paid fully
within 90 days from the payment due date". The circular has no card exception that we saw. Applies to banks; SBI Card is
an NBFC under separate norms (not checked). Ask the legal researcher to confirm application to retail cards.

**8b.6 UPI-linked RuPay credit cards.** UNVERIFIED for default handling. HDFC MITC lists a "UPI RuPay Mega Saver Card" at
1.99%/month, i.e. it is part of the same card book and same terms. Nothing specific found.

### 8c. Card-to-card rotation, cash, balance transfer, EMI

- SOURCED. Using one card to pay another can get the card cancelled. ICICI MITC: periodic reviews look for "use of the Card
  for repayment of other Credit Cards / loans, fund transfers to Savings Accounts" ... "ICICI Bank may, at its sole
  discretion, cancel the concerned Credit Card(s), including any add-on Cards".
- SOURCED. Cash costs most: fee 2.5% (min ₹500 HDFC/ICICI/Axis) plus interest from day one (ICICI: "interest will be
  levied on all cash advances from the date of the transaction"; HDFC: cash advance fee "2.5% ... or ₹500 whichever is
  higher"). Plus 18% GST on fee and interest.
- SOURCED. HDFC balance transfer: "Balance Transfer Processing Charges: 1% of BT amount or ₹250, whichever is higher."
  HDFC loans on card: "Jumbo Loan Processing Fee ... upto Rs 1,799"; "Insta Loan Processing Fee ... upto Rs 1,499";
  late fee on Insta/Jumbo loan EMIs uses the same banding "w.e.f 20th June, 2026".
- INFERENCE: rotation adds a 2.5%+GST fee per rotation if done via cash/wallet, loses the interest-free period, and each
  card's balance and minimum due rise; when one bank cuts a limit (8a.2) the chain breaks and all cards fall due together.

### 8d. Which card to clear first

- SOURCED (opinion, reputed media). Outlook Money, Meghna Maiti, 15 Aug 2025: avalanche: "Credit card debt and personal
  loan EMIs would be the ones for which you are paying the maximum interest" (clear highest interest first); snowball:
  "Here, you pay the debt with the smallest balance first."
  https://www.outlookmoney.com/personal-finance/independence-day-2025-from-emis-to-freedom-smart-ways-to-slash-your-debt
- INFERENCE (mark as our advice): since all four big issuers charge the same 3.75%/month (§6), "highest interest first"
  does not separate them. Practical tie-breakers: (1) any card at the bank that holds your salary/savings/FD (set-off
  clause 8b.3, cross-default 8b.2); (2) keep at least the minimum due paid on every card to stop late fees, which hit small
  balances hardest in percent (§6); (3) smallest balances can be closed for good, removing a monthly ₹750 + GST fee each.

---

## (a) Amount slab table: what realistically happens

How to read the amount: sources show issuers count **per account per issuer** (late fee slab is on that card's Total
Amount Due; ICICI/HDFC combine cards of the **same** issuer: 8b.1). PNB/BoM agency slabs are per NPA account/borrower at
that bank (2.1, 2.2; 8b.5 borrower-wise). Nothing shows banks adding up dues **across different banks** for collection
decisions; other banks only see it through the bureau (8a). So "₹2 lakh" below means ₹2 lakh owed to one bank.
S = sourced input; I = our inference.

| Owed to one bank | Calls / SMS / bots | Field visit | Legal | Fees & growth | Settlement / end state |
|---|---|---|---|---|---|
| ~₹10,000 | Yes, from first missed date; auto-dialer tele-calling 1-90 DPD (S: BoB RFP, RBL bucket 1) | Unlikely to be worth a long trip: agency earns ~₹750-1,200 on full recovery (S: PNB 7.5%, BoM 12%; I: worth it) | Court fee ~₹786 = 7.9% of claim (PARTLY: our calc); suing rare (I) ; DRT not possible (S) | ₹750 late fee + GST each month = 7.5% of balance on fees alone + 3.75% interest (S inputs, I calc) | Card blocked, written off after >6 missed payments (S: SBI Card); bureau mark (S); may be sold in a pool (I) |
| ~₹50,000 | Yes (S) | Possible from bucket 2/3 if in a covered city (S: BoB/RBL buckets; I: city) | Court fee ~₹2,386 (PARTLY); pre-litigation Lok Adalat notice possible (S: SBI Cards Indore case was ₹1.83L, I for this size) | ₹1,100-1,300 late fee (S); highest-risk card band is limits under ₹50k (S: CRIF) | As above; settlement offers claimed 40-60% only by settlement firms (PARTLY) |
| ~₹1 lakh | Yes (S) | Likely in covered cities from 31-60 DPD (S buckets; I) | Court fee ~₹3,426 = 3.4% (PARTLY); Lok Adalat / online arbitration notices seen in practice (S: 3.3, 3.5) | ₹1,300 late fee = 1.3% (S); interest dominates (I) | Written off after ~6 months, still owed (S: SBI FAQ); ARC sale possible (S for unsecured pools, PARTLY for cards) |
| ~₹2 lakh | Yes (S) | Yes, field referral expected (S: RBL "100% to be referred on field" in bucket 2, loans; I for cards) | Court fee ~₹4,426 (PARTLY); real case: SBI Cards took ₹1.83L dues to Lok Adalat in borrower's city (S) | as above | PSU bank agency commission drops to 5% above ₹1L (S: PNB) |
| ~₹3-5 lakh | Yes (S) | Yes; tracing borrowers who moved is a paid job (S: PNB detective ₹7,500/person) | Court fee ~₹7,426 at ₹5L (PARTLY); civil suit or arbitration more plausible (I) | as above | — |
| ₹10 lakh+ | Yes (S) | Yes (I) | Court fee ~₹12,426 at ₹10L = 1.2% (PARTLY); DRT only from ₹20 lakh (S); Axis case of ₹16.66L went to arbitration (S) | as above | PSU banks move >₹10L to "Resolution Agents"/ARCs (S: PNB, loans) |

## (b) Safe to say / Do not say

**Safe to say (sourced):**
- Unpaid bills first bring calls, SMS and automated calls, usually from big call centres in cities like Hyderabad. (BoB RFP)
- Banks decide how hard to chase by how late you are and how much is at risk. (RBL policy)
- Recovery agencies are often paid only a percentage of what they actually collect; one public bank pays 7.5% on small old accounts. (PNB)
- Agencies are given districts or city lists; in AP and Telangana the card agency lists name Hyderabad, Karimnagar, Warangal, Vizag, Vijayawada. (PNB, OneCard list)
- Late fees go up to ₹1,300 a month plus 18% GST at HDFC, ICICI, SBI Card and Axis; interest is 3.75% a month. (MITCs)
- On a ₹10,000 bill the late fee alone is ₹750 a month; on ₹1 lakh it is ₹1,300. (MITCs)
- SBI Card writes off an account after more than six missed payments, but you still owe it; paying in full later gets CIBIL cleaned. (SBI Card FAQ)
- A 'settled' or 'written off' status hurts future loans; 'closed' is the clean status. (Experian India)
- Card companies do take card dues to Lok Adalat, in the borrower's own city. (SBI Cards Indore case)
- Courts have struck down bank arbitrations where the bank picked the arbitrator alone; one bank had about 76,000 such awards. (Delhi HC, Axis)
- DRT is only for dues of twenty lakh rupees or more. (MoF notification 2018)
- If you also have a savings account or FD at the same bank, the card terms let that bank adjust your money against card dues. (HDFC agreement)
- Default at one bank shows on your credit report and other banks can cut your limits. (bureau reporting + SBI Card policy)
- Card complaints to the RBI Ombudsman rose about 20% in 2024-25. (RBI report)

**Do not say (unsourced or wrong):**
- Do not say "banks never visit for small amounts" or give a rupee cut-off; no bank publishes one. Say "the economics make long trips for small dues rare".
- Do not say agents use your Aadhaar address; not found.
- Do not give settlement percentages (40-60%) as fact; only settlement companies claim them.
- Do not say a named bank sold its credit card dues to an ARC at a named price; not found for 2024-2026.
- Do not say banks file cheque-bounce or NACH-bounce criminal cases for card dues as routine; not found.
- Do not attribute AP/Telangana loan-app suicides or the Hyderabad loan-app cases to bank credit card agents.
- Do not quote advocate fees or how many years a civil suit takes; not found.
- Do not put court-fee rupee figures on screen until a Telangana advocate confirms the schedule (our calculation).
- Do not say "default on one card makes all your cards at that bank NPA" as settled practice; the RBI rule is borrower-wise, but card-level application was not confirmed.
- Do not present AI-voice "matches humans" claims as fact; it is Credgenics' own claim.
