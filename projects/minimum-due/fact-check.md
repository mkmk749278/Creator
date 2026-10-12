# Fact-check: Minimum Amount Due (script v1.1, 2026-10-11)

`claims.csv`: **93 claims, all confirmed**; `python3 scripts/claims_check.py projects/minimum-due/claims.csv` → gate passed.

## What the independent pass found and how v1.1 fixed it
The independent fact-check (95 claims) confirmed every rule and source and flagged 18 rows wrong and 1 unverified.
All were fixed in `script.full.tsv`:

| Line | Problem | Fix |
|---|---|---|
| M004 (en) | "most people" unsupported | "many people" (TransUnion CIBIL survey, 2017) |
| M013, M014, M023, M091 | wrong RBI paragraph in tags | para 5 (definitions), para 29 (billing cycle) |
| M016, M037 | example numbers without OUR CALCULATION / tagged as ICICI's | relabelled OUR CALCULATION |
| M020 | "minimum saves not one rupee of interest" overstated (it saves ≈ ₹22) | "doesn't stop interest, doesn't save the free period" |
| M040–M042 | our math skipped the transaction day (banks count it) | ₹1,679 + ₹302 = **₹1,981**; balance **₹30,481** |
| M046 | "most people don't know this" unverified | "this one is very important" |
| M050 | MAD rounding + day count | total ₹35,561, MAD ₹2,084, interest + GST ₹2,061 |
| M053 | "interest only on principal" wrong (unpaid interest is charged interest) | sentence dropped; the fees/taxes rule stays |
| M056–M059 | long-run model charged interest only after payment | re-modelled: year 1 paid ₹19,987, owe ₹24,771 (74% went to interest + GST); year 5 paid ₹69,896, owe ₹12,956 |
| M065 | "of this" mixed a CRIF Mar 2025 figure into an RBI 2026 total; "over 90 days" | names the 91–360-day bucket, separate stack |
| M083 | "up to forty days" is only our example | "depending on the card, up to fifty days" |
| M090 | HDFC EMI range out of date | ≈ 11–25% (Apr–Jun 2026); recheck before publishing |

## Method for every OUR CALCULATION figure
`python3 projects/minimum-due/tools/mad_math.py`: ICICI's published method (each transaction from its own date, the
transaction day counted; full balance until the payment day, then the residual), HDFC's June 2025 MAD formula (5% part
rounded up to ₹10), 45% a year, 18% GST, no interest on GST, payments applied to GST, then interest, then principal.
The fact-checker's month-1 recomputation matches the tool exactly. Its long-run run used slightly different, unrecorded
assumptions (year 5: ₹69,769 / ₹12,348 vs ours ₹69,896 / ₹12,956); the film uses the reproducible tool output, says
"about", and labels it OUR CALCULATION.

## For the YouTube description
- Rates, MAD formulas and free days differ by card: 3.75%/month is ICICI's published rate; HDFC MITC 20–50 days,
  ICICI 18–48 days. "Check your own card's KFS and MITC."
- RBI Directions 2025 = RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025,
  RBI/DOR/2025-26/155 (28 Nov 2025); the official PDF is captcha-gated from our servers, text verified via TaxGuru's
  reproduction and the 2022 Master Direction on rbi.org.in.
- Timestamped source list: build from `claims.csv` `source_url` per line id once the VO is timed.
