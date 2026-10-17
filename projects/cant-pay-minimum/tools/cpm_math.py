#!/usr/bin/env python3
"""How an unpaid card bill grows when nothing is paid at all, by amount owed (OUR CALCULATION in the film).

Inputs (research_practical.md section 6, sources opened 2026-10-12):
- Interest 3.75% a month (45% a year) at HDFC, ICICI, SBI Card and Axis.
- Late fee per missed due date on the outstanding, HDFC Bank KFS/MITC v4.13 (Sep 2026) slabs:
  up to ₹100 nil; ₹101-500 ₹100; ₹501-1,000 ₹500; ₹1,001-5,000 ₹600; ₹5,001-10,000 ₹750; ₹10,001-25,000 ₹900;
  ₹25,001-50,000 ₹1,100; above ₹50,000 ₹1,300.
- GST 18% on interest and on fees.
- RBI card directions 2025 para 23(2): unpaid charges, levies and taxes are not capitalised for interest, so fees and GST
  never earn interest; unpaid interest does (as in part 1's method, projects/minimum-due/tools/mad_math.py).
Model (simplified, stated on screen as OUR CALCULATION): the bill is unpaid from the first due date; each month adds
interest on (principal + unpaid interest) at 3.75%, GST on that interest, one late fee on the previous month's total and
GST on the fee. No new spends, no over-limit fee, no two-cycle ₹100 extra (SBI/Axis), no recovery or legal costs.
Real bills differ by bank, dates and day counts; this shows the shape, not anyone's exact bill.
"""
RATE_M, GST = 0.0375, 0.18
SLABS = [(100, 0), (500, 100), (1000, 500), (5000, 600), (10000, 750), (25000, 900), (50000, 1100)]


def late_fee(outstanding):
    for cap, fee in SLABS:
        if outstanding <= cap:
            return fee
    return 1300


def grow(principal, months):
    """Returns total owed and the parts after `months` missed due dates."""
    interest_unpaid = fees = gst = 0.0
    total = principal
    for _ in range(months):
        i = (principal + interest_unpaid) * RATE_M
        f = late_fee(total)
        interest_unpaid += i
        fees += f
        gst += GST * (i + f)
        total = principal + interest_unpaid + fees + gst
    return dict(total=total, interest=interest_unpaid, fees=fees, gst=gst, extra=total - principal)


def inr(x):
    s = f"{round(x):,}"
    a, *b = s.split(",")
    digits = s.replace(",", "")
    if len(digits) <= 3:
        return "₹" + digits
    head, tail = digits[:-3], digits[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts + [tail])


if __name__ == "__main__":
    print("OUR CALCULATION · nothing paid · 3.75%/month interest + HDFC late-fee slabs + 18% GST")
    print(f"{'owed':>10} | {'after 3 months':>16} | {'after 6 months':>16} | {'after 12 months':>17} | fee share of the 6-month extra")
    for p in (10000, 50000, 100000, 200000, 500000, 1000000):
        r3, r6, r12 = grow(p, 3), grow(p, 6), grow(p, 12)
        print(f"{inr(p):>10} | {inr(r3['total']):>9} (+{r3['extra'] / p:4.0%}) | {inr(r6['total']):>9} (+{r6['extra'] / p:4.0%}) | "
              f"{inr(r12['total']):>10} (+{r12['extra'] / p:4.0%}) | late fees {r6['fees'] * 1.18 / r6['extra']:.0%}")
    print("\nDetail, 6 months:")
    for p in (10000, 100000):
        r = grow(p, 6)
        print(f"  {inr(p)}: interest {inr(r['interest'])}, late fees {inr(r['fees'])}, GST {inr(r['gst'])} -> total {inr(r['total'])}")
