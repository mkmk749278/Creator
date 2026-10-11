#!/usr/bin/env python3
"""Every number in the Minimum Amount Due film's worked example (README, research record). Shown on screen as
OUR CALCULATION.

Interest follows ICICI Bank's published method: Interest = Days / 365 x Amount x Rate, per transaction from its date, on
the full statement balance until the payment date, then on the residual (icici.bank.in credit-card interest-rates page).
MAD follows HDFC Bank's formula from the June 2025 statement: GST + EMI + 100% fees + 5% of (finance charge + retail +
cash), or 100% of the finance charge + 5% of (retail + cash) when the finance charge is larger.
Rate 3.75% a month (45% a year), GST 18% on interest.
"""
from datetime import date

RATE, GST = 0.45, 0.18
S1, DUE, S2 = date(2026, 10, 25), date(2026, 11, 14), date(2026, 11, 25)
SPENDS = [(date(2026, 10, 5), 10000), (date(2026, 10, 12), 15000), (date(2026, 10, 20), 5000)]
TOTAL = sum(a for _, a in SPENDS)


def interest(amount, start, end):
    return amount * RATE * (end - start).days / 365


def hdfc_mad(finance, retail, fees=0.0, emi=0.0):
    gst = finance * GST
    five = 0.05 * (finance + retail)
    return gst + emi + fees + (five if five > finance else finance + 0.05 * retail)


def month_one(paid, fresh=0.0):
    """Interest + GST on statement 2 when `paid` is paid on the due date; `fresh` is a spend on 15 Nov."""
    i = sum(interest(a, d, S1) for d, a in SPENDS)
    i += interest(TOTAL, S1, DUE) + interest(TOTAL - paid, DUE, S2)
    i += interest(fresh, date(2026, 11, 15), S2)
    return i, i * GST


def mad_only(balance, months, floor=200.0, monthly=RATE / 12):
    """Pay only the HDFC-formula MAD each month, no new spends. Returns (paid, balance) after `months`, and the months
    needed to clear (capped at 2,000)."""
    paid, m, snap = 0.0, 0, None
    while balance > 0.5 and m < 2000:
        fc = balance * monthly
        due = balance + fc * (1 + GST)
        pay = min(max(hdfc_mad(fc, balance), floor), due)
        balance, paid, m = due - pay, paid + pay, m + 1
        if m == months:
            snap = (paid, balance)
    return snap, m


def main():
    print(f"MAD month 1: 5% of {TOTAL:,} = {0.05 * TOTAL:,.0f}")
    for d, a in SPENDS:
        print(f"  free days for {a:,} spent {d}: {(DUE - d).days}")
    i, g = month_one(1500)
    print(f"Pay MAD 1,500: interest {i:,.2f} + GST {g:,.2f} = {i + g:,.2f}; new balance {TOTAL - 1500 + i + g:,.2f}")
    i2, g2 = month_one(1500, fresh=5000)
    tot = TOTAL - 1500 + 5000 + i2 + g2
    print(f"  + 5,000 petrol on 15 Nov: interest+GST {i2 + g2:,.2f}; total {tot:,.2f}; "
          f"HDFC MAD {hdfc_mad(i2, TOTAL - 1500 + 5000):,.2f}")
    i3, g3 = month_one(29999)
    print(f"Pay 29,999 (one rupee short): interest {i3:,.2f} + GST {g3:,.2f} = {i3 + g3:,.2f}")
    fc = RATE / 12
    share = fc * (1 + GST) / (0.05 * (1 + fc) + fc * GST)
    print(f"Steady state: {share:.1%} of each MAD payment is interest + GST")
    for months in (12, 60):
        (paid, bal), _ = mad_only(30000, months)
        print(f"MAD only from 30,000: after {months} months paid {paid:,.0f}, still owe {bal:,.0f}")
    for floor in (0, 200, 500):
        _, m = mad_only(30000, 1, floor=floor)
        print(f"  months to clear with a {floor} floor: {m} ({m / 12:.1f} years)")


if __name__ == "__main__":
    main()
