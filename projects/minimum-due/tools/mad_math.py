#!/usr/bin/env python3
"""Every number in the Minimum Amount Due film's worked example (README, research record). Shown on screen as
OUR CALCULATION.

Interest follows ICICI Bank's published method (icici.bank.in credit-card interest-rates page):
Interest = Days / 365 x Amount x Rate, each transaction from its own date (the transaction day counts), the full balance
until the payment day, then the reduced balance from the payment day to the next statement date (both days count).
MAD follows HDFC Bank's formula from the June 2025 statement: GST + EMI + 100% fees + 5% of (finance charge + retail +
cash), or 100% of the finance charge + 5% of (retail + cash) when the finance charge is larger; the 5% part is rounded
up to the next ₹10, as in all three of HDFC's illustrations. Payments go to GST, then interest, then principal. GST is
not charged interest (RBI Directions 2025, para 23(2)); unpaid interest is. Rate 3.75% a month (45% a year), GST 18%.
"""
import math
from datetime import date

RATE, GST, FLOOR = 0.45, 0.18, 200.0
S1, DUE, S2 = date(2026, 10, 25), date(2026, 11, 14), date(2026, 11, 25)
SPENDS = [(date(2026, 10, 5), 10000), (date(2026, 10, 12), 15000), (date(2026, 10, 20), 5000)]
TOTAL = sum(a for _, a in SPENDS)


def interest(amount, days):
    return amount * RATE * days / 365


def up10(x):
    return math.ceil(x / 10) * 10


def hdfc_mad(finance, retail):
    five = up10(0.05 * (finance + retail))
    return finance * GST + (five if five > finance else finance + up10(0.05 * retail))


def month_one(paid, fresh=0.0):
    """Interest on statement 2 when `paid` is paid on the due date; `fresh` is a spend on 15 Nov."""
    i = sum(interest(a, (DUE - d).days) for d, a in SPENDS)
    i += interest(TOTAL - paid, (S2 - DUE).days + 1)
    i += interest(fresh, (S2 - date(2026, 11, 15)).days + 1)
    return i


def next_month(d, day=None):
    return date(d.year + (d.month == 12), d.month % 12 + 1, day or d.day)


def mad_only(snapshots=(12, 60)):
    """Continue the film's example with no new spends, paying only the MAD on each due date (the ₹1,500 is payment 1).
    Returns {payments: (paid so far, still owed)}, the months to clear, and the interest + GST share of the payments."""
    i = month_one(1500)
    prin, intr, gst, paid, n, st = TOTAL - 1500.0, i, i * GST, 1500.0, 1, S2
    out, charged, payments = {}, 0.0, 0.0
    while prin + intr + gst > 0.5 and n < 2000:
        due, nst = next_month(st, 14), next_month(st)
        pay = min(max(hdfc_mad(intr, prin), FLOOR), prin + intr + gst)
        base = prin + intr
        p = pay
        for part in ("gst", "intr", "prin"):
            v = {"gst": gst, "intr": intr, "prin": prin}[part]
            take = min(p, v)
            p -= take
            if part == "gst":
                gst -= take
            elif part == "intr":
                intr -= take
            else:
                prin -= take
        paid, n = paid + pay, n + 1
        new = interest(base, (due - st).days) + interest(prin + intr, (nst - due).days)
        intr, gst, st = intr + new, gst + new * GST, nst
        if n <= 13:
            charged, payments = charged + new * (1 + GST), payments + pay
        if n in snapshots:
            out[n] = (paid, prin + intr + gst)
    return out, n, charged / payments


def main():
    print(f"MAD month 1: 5% of {TOTAL:,} = {0.05 * TOTAL:,.0f}")
    for d, a in SPENDS:
        print(f"  free days for {a:,} spent {d}: {(DUE - d).days}")
    i = month_one(1500)
    print(f"Pay MAD 1,500: interest {i:,.2f} + GST {i * GST:,.2f} = {i * (1 + GST):,.2f}; "
          f"new balance {TOTAL - 1500 + i * (1 + GST):,.2f}")
    i2 = month_one(1500, fresh=5000)
    print(f"  + 5,000 petrol on 15 Nov: interest+GST {i2 * (1 + GST):,.2f}; "
          f"total {TOTAL - 1500 + 5000 + i2 * (1 + GST):,.2f}; HDFC MAD {hdfc_mad(i2, TOTAL - 1500 + 5000):,.2f}")
    i0 = month_one(0)
    print(f"Pay nothing: interest {i0:,.2f}; paying the MAD saves {i0 - i:,.2f} of interest")
    i3 = month_one(29999)
    print(f"Pay 29,999 (one rupee short): interest {i3:,.2f} + GST {i3 * GST:,.2f} = {i3 * (1 + GST):,.2f}")
    snaps, months, share = mad_only()
    for k, (paid, owed) in snaps.items():
        print(f"MAD only: after {k} payments paid {paid:,.0f}, still owe {owed:,.0f}")
    print(f"  interest + GST charged / payments made, first year: {share:.1%}")
    print(f"  months to clear (₹{FLOOR:.0f} floor): {months} ({months / 12:.1f} years)")


if __name__ == "__main__":
    main()
