"""Whiteboard segments for Minimum Amount Due (video/lib/whiteboard). Times are absolute film seconds; build.py turns
each segment into video/minimumdue/<id>/params.js with times relative to the segment start.

Every step's text is spoken in the same VO line (semantic lock); numbers come from tools/mad_math.py and claims.csv.
"""
from timing import L
from wbmeasure import width

G, R, K, B = "green", "red", "black", "blue"
CALC = "OUR CALCULATION · ICICI METHOD, 45% P.A."


MAXW = 1540   # usable line width: x 220 → 1760


def w(text, x, y, at, dur=None, size=100, color=K, maxw=None, **kw):
    """One line of writing; the size shrinks so the line fits the board (measured with the engine's own font data)."""
    room = maxw or (1760 - x)
    size = min(size, int(size * room / max(1, width(text, size))))
    d = dict(write=text, x=x, y=y, at=at, size=size, color=color, **kw)
    if dur:
        d["dur"] = dur
    return d


def flow(x, y, size, parts, gap=0.45, maxw=None):
    """Several pieces written one after another on the same line: parts = [(text, at, dur, color), ...]."""
    room = maxw or (1760 - x)
    total = sum(width(p[0], size) for p in parts) + gap * size * (len(parts) - 1)
    if total > room:
        size = int(size * room / total)
    out, cx = [], x
    for text, at, dur, color in parts:
        out.append(dict(write=text, x=round(cx), y=y, at=at, dur=dur, size=size, color=color))
        cx += width(text, size) + gap * size
    return out


def cx(text, centre, y, at, dur, size, color):
    return dict(write=text, x=round(centre - width(text, size) / 2), y=y, at=at, dur=dur, size=size, color=color)


BOARDS = [
    dict(id="b01_how", start=L("1.07")[0] - 0.2, end=L("1.07")[1] + 0.4, tag="ICICI BANK · INTEREST RATES PAGE | 2025", steps=[
        *flow(220, 340, 100, [("Not paid:", L("1.07")[0] + 0.2, 1.0, K), ("₹4,688", L("1.07")[0] + 1.3, 1.1, K)]),
        *flow(220, 570, 100, [("Interest + GST:", L("1.07")[0] + 2.4, 1.2, R), ("₹4,317", L("1.07")[0] + 3.7, 1.0, R)]),
        cx("How?", 960, 840, L("1.07")[1] - 0.9, 0.7, 140, B),
    ]),
    dict(id="b02_numbers", start=L("1.10")[0] - 0.2, end=L("1.15")[1] + 0.4, tag="RBI CARD DIRECTIONS 2025 · PARA 5 | HDFC MAD FORMULA", steps=[
        w("Total amount due", 220, 300, L("1.10")[0] + 1.0, 1.6, 80, B),
        w("= the full bill", 300, 430, L("1.10")[0] + 2.8, 1.3, 80, B),
        w("Minimum amount due", 220, 610, L("1.11")[0] + 0.3, 1.8, 80, R),
        w("≈ 5% + fees + GST", 300, 740, L("1.11")[0] + 4.2, 2.2, 80, R),
        dict(erase=True, at=L("1.11")[1] + 0.1, dur=0.7),
        w("₹30,000 × 5% = ₹1,500", 220, 560, L("1.12")[0] + 0.3, 2.6, 100, K),
        dict(underline="last", color=R, dur=0.4),
        dict(erase=True, at=L("1.12")[1] + 0.1, dur=0.8),
        dict(tick=[220, 290, 64], at=L("1.13")[0] + 2.2, color=G),
        w("No late fee", 330, 320, L("1.13")[0] + 2.5, 1.2, 80, G),
        dict(tick=[220, 460, 64], at=L("1.13")[0] + 4.0, color=G),
        w("No late report to CIBIL", 330, 490, L("1.13")[0] + 4.3, 1.5, 80, G),
        dict(cross=[220, 600, 64], at=L("1.14")[0] + 0.2, color=R),
        w("Interest does not stop", 330, 660, L("1.14")[0] + 0.5, 1.6, 80, R),
        dict(cross=[220, 770, 64], at=L("1.14")[0] + 2.4, color=R),
        w("Interest free period lost", 330, 830, L("1.14")[0] + 2.7, 1.6, 80, R),
        dict(erase=True, at=L("1.15")[0] + 0.1, dur=0.9),
        w("Minimum ≠ safety net", 260, 420, L("1.15")[0] + 1.2, 1.8, 100, K),
        dict(strike="last", at=L("1.15")[0] + 3.2, dur=0.5),
        w("= interest switch ON", 260, 700, L("1.15")[0] + 4.0, 1.9, 100, R),
        dict(box="last", color=R, dur=0.6),
    ]),
    dict(id="b03_calendar", start=L("1.18")[0] - 0.2, end=L("1.21")[1] + 0.4, tag="ILLUSTRATION · OUR EXAMPLE", steps=[
        dict(line=[220, 560, 1720, 560], at=L("1.18")[0] + 0.1, dur=0.6, color=K),
        cx("Oct 5", 300, 650, L("1.18")[0] + 0.5, 0.5, 56, K), cx("Oct 25", 960, 650, L("1.18")[0] + 1.3, 0.6, 56, K),
        cx("BILL ₹30,000", 940, 470, L("1.18")[0] + 2.0, 1.4, 54, B),
        cx("Nov 14", 1600, 650, L("1.18")[0] + 3.6, 0.6, 56, R), cx("LAST DATE", 1540, 470, L("1.18")[0] + 4.4, 1.0, 52, R),
        dict(line=[300, 760, 1600, 760], at=L("1.19")[0] + 0.3, dur=1.0, color=G, width=14),
        w("Phone: 40 days interest free", 260, 870, L("1.19")[0] + 1.3, 1.6, 60, G),
        w("Groceries: 25 days", 260, 970, L("1.19")[0] + 3.4, 1.2, 60, G),
        dict(erase=True, at=L("1.20")[0] - 0.2, dur=0.6),
        w("ONE CONDITION:", 260, 380, L("1.20")[0] + 0.4, 0.9, 110, R),
        w("pay the FULL bill by the last date", 260, 600, L("1.21")[0] + 0.3, 2.6, 80, K),
        dict(underline="last", color=R, dur=0.4),
        w("₹1 less → no interest free period", 260, 820, L("1.21")[0] + 3.6, 2.2, 80, R),
    ]),
    dict(id="b04_rules", start=L("1.24")[0] - 0.2, end=L("1.29")[1] + 0.4, tag=CALC, steps=[
        w("RULE 1", 220, 300, L("1.24")[0] + 0.1, 0.6, 80, R),
        w("Interest from the day you SPENT", 220, 440, L("1.24")[0] + 2.5, 2.6, 80, K),
        w("₹10,000 from Oct 5", 300, 600, L("1.25")[0] + 0.5, 1.6, 74, R),
        w("₹15,000 from Oct 12", 300, 730, L("1.25")[0] + 3.4, 1.6, 74, R),
        w("₹5,000 from Oct 20", 300, 860, L("1.25")[0] + 6.3, 1.6, 74, R),
        dict(erase=True, at=L("1.26")[0] - 0.1, dur=0.8),
        w("3.75% a month", 260, 420, L("1.26")[0] + 2.6, 1.7, 110, K),
        w("× 12 = 45% a year", 260, 660, L("1.26")[0] + 5.2, 2.0, 110, R),
        dict(underline="last", color=R, dur=0.4),
        dict(erase=True, at=L("1.27")[0] - 0.1, dur=0.8),
        w("RULE 2", 220, 300, L("1.27")[0] + 0.2, 0.6, 80, R),
        w("Interest even on what you paid", 220, 440, L("1.27")[0] + 1.4, 2.4, 80, K),
        w("Till Nov 14: on ₹30,000", 300, 600, L("1.28")[0] + 0.3, 2.4, 74, R),
        w("After: on ₹28,500", 300, 730, L("1.28")[0] + 4.3, 2.2, 74, R),
        *flow(220, 900, 74, [("RULE 3", L("1.29")[0] + 0.2, 0.6, R), ("+ 18% GST on interest", L("1.29")[0] + 1.6, 1.9, K)]),
    ]),
    dict(id="b05_newswipe", start=L("1.36")[0] - 0.2, end=L("1.37")[1] + 0.4, tag="HDFC BANK MITC · ICICI BANK", steps=[
        w("New swipe, Nov 15: ₹5,000", 220, 360, L("1.36")[0] + 0.3, 2.0, 90, K),
        w("Interest free days = 0", 220, 600, L("1.36")[0] + 2.6, 2.0, 100, R),
        dict(box="last", color=R, dur=0.5),
        dict(erase=True, at=L("1.37")[0] + 0.1, dur=0.7),
        w("Your card", 300, 440, L("1.37")[0] + 2.2, 1.2, 120, K),
        w("= a 45% LOAN", 300, 700, L("1.37")[0] + 4.3, 1.9, 130, R),
        dict(underline="last", color=R, dur=0.4),
    ]),
    dict(id="b06_slow", start=L("2.02")[0] - 0.2, end=L("2.05")[1] + 0.4, tag="OUR CALCULATION · HDFC MAD FORMULA, 45% P.A.", steps=[
        w("RBI: loan must not grow", 220, 360, L("2.02")[0] + 0.4, 2.2, 90, B),
        w("…but how slowly?", 220, 600, L("2.02")[0] + 5.6, 1.6, 100, R),
        dict(erase=True, at=L("2.03")[0] - 0.1, dur=0.7),
        w("Every ₹100 you pay:", 220, 300, L("2.03")[0] + 0.6, 1.8, 80, K),
        dict(bar=[300, 900, 200, 444], at=L("2.03")[0] + 2.8, dur=1.2, color=R),
        dict(bar=[620, 900, 200, 156], at=L("2.03")[0] + 5.9, dur=0.8, color=G),
        w("₹74 interest + GST", 900, 560, L("2.03")[0] + 4.0, 1.8, 70, R),
        w("₹26 cuts your loan", 900, 780, L("2.03")[0] + 6.8, 1.7, 70, G),
        dict(erase=True, at=L("2.04")[0] - 0.1, dur=0.7),
        *flow(220, 340, 80, [("Year 1:", L("2.04")[0] + 1.0, 0.8, K), ("paid ₹19,987", L("2.04")[0] + 3.0, 1.5, G)]),
        w("pending ₹24,771", 560, 490, L("2.04")[0] + 5.5, 1.8, 80, R),
        *flow(220, 720, 80, [("Year 5:", L("2.05")[0] + 0.3, 0.8, K), ("paid ₹69,896", L("2.05")[0] + 1.6, 1.5, G)]),
        w("pending ₹12,956", 560, 870, L("2.05")[0] + 3.6, 1.6, 80, R),
        dict(underline="last", color=R, dur=0.4),
    ]),
    dict(id="b07_crif", start=L("2.09")[0] - 0.2, end=L("2.09")[1] + 0.4, tag="CRIF HIGH MARK | MAR 2025", steps=[
        w("Card bills unpaid 3 months to 1 year", 220, 300, L("2.09")[0] + 2.0, 3.0, 64, K),
        dict(bar=[340, 900, 240, 320], at=L("2.09")[0] + 5.2, dur=1.0, color=K),
        cx("a year before", 460, 980, L("2.09")[0] + 6.3, 1.0, 40, K),
        dict(bar=[900, 900, 240, 460], at=L("2.09")[0] + 7.4, dur=1.2, color=R),
        cx("₹33,886 cr", 1020, 410, L("2.09")[0] + 8.7, 1.5, 70, R),
        cx("Mar 2025", 1020, 980, L("2.09")[0] + 10.3, 0.8, 40, R),
        dict(arrow=[1220, 780, 1400, 560], color=R, dur=0.5),
        w("+44%", 1420, 560, L("2.09")[1] - 1.2, 0.7, 110, R),
    ]),
    dict(id="b08_maths", start=L("2.11")[0] - 0.2, end=L("2.12")[1] + 0.4, tag="", steps=[
        w("What saves you?", 300, 420, L("2.11")[0] + 0.3, 1.4, 100, K),
        w("Knowing the maths", 300, 680, L("2.11")[0] + 2.3, 1.7, 110, G),
        dict(circle="last", color=G, dur=0.5),
        dict(erase=True, at=L("2.12")[0], dur=0.6),
        cx("CARD ROTATION", 960, 600, L("2.12")[0] + 1.6, 1.6, 130, R),
    ]),
    dict(id="b09_loop", start=L("2.14")[0] - 0.2, end=L("2.14")[1] + 0.4, tag="ILLUSTRATION", steps=[
        w("Friend", 220, 330, L("2.14")[0] + 0.2, 0.6, 76, B), dict(arrow=[740, 300, 880, 300], dur=0.3, bend=0),
        w("Bill", 920, 330, L("2.14")[0] + 1.3, 0.4, 76, K), dict(arrow=[1230, 300, 1330, 300], dur=0.3, bend=0),
        w("Rent", 1370, 330, L("2.14")[0] + 2.2, 0.5, 76, K),
        dict(arrow=[1500, 400, 420, 400], dur=0.5, bend=-0.22),
        w("Loan: SAME", 260, 680, L("2.14")[0] + 3.2, 1.0, 100, R),
        w("Last date +1 month, + fee", 260, 880, L("2.14")[0] + 4.5, 1.8, 80, R),
    ]),
    dict(id="b10_postpone", start=L("2.17")[0] - 0.2, end=L("2.18")[1] + 0.4, tag="", steps=[
        w("Rotation = postpone", 260, 480, L("2.17")[0] + 0.5, 1.8, 110, R),
        dict(underline="last", at=L("2.17")[0] + 2.6, dur=0.4, color=K),
        dict(erase=True, at=L("2.18")[0] - 0.1, dur=0.5),
        cx("5 simple steps", 960, 600, L("2.18")[0] + 1.2, 1.4, 130, G),
    ]),
    dict(id="b11_steps12", start=L("2.20")[0] - 0.2, end=L("2.22")[1] + 0.4, tag="HDFC BANK MITC · ICICI BANK", steps=[
        w("1. Pay the FULL bill", 220, 300, L("2.20")[0] + 0.1, 1.4, 90, G),
        w("→ up to 50 days interest free", 300, 450, L("2.20")[0] + 1.8, 2.2, 74, G),
        w("2. Pay as much as you can", 220, 640, L("2.21")[0] + 0.3, 2.0, 90, B),
        w("never less than the minimum", 300, 790, L("2.21")[0] + 3.3, 1.8, 74, R),
        dict(erase=True, at=L("2.22")[0] - 0.1, dur=0.7),
        w("More paid = less interest", 240, 440, L("2.22")[0] + 2.3, 2.2, 100, G),
        w("Clear all → interest free period back", 240, 720, L("2.22")[0] + 5.3, 2.4, 80, G),
    ]),
    dict(id="b12_emi", start=L("2.24")[0] + 4.6, end=L("2.25")[1] + 0.4, tag="HDFC BANK SMARTEMI PAGE | APR–JUN 2026", steps=[
        w("4. EMI", 220, 280, L("2.24")[0] + 4.8, 0.6, 90, B),
        dict(bar=[300, 860, 200, 450], at=L("2.24")[0] + 5.6, dur=0.8, color=R),
        cx("45%", 400, 380, L("2.24")[0] + 6.5, 0.4, 64, R),
        dict(bar=[620, 860, 200, 250], at=L("2.24")[0] + 7.0, dur=0.6, color=G),
        cx("11–25%", 720, 580, L("2.24")[0] + 7.7, 0.7, 56, G),
        w("+ fee + GST", 980, 560, L("2.24")[0] + 9.2, 1.2, 70, K),
        w("✗ unknown loan apps", 980, 740, L("2.24")[0] + 11.6, 1.6, 70, R),
        dict(erase=True, at=L("2.25")[0] - 0.2, dur=0.6),
        w("5. Last date AFTER salary", 220, 440, L("2.25")[0] + 1.4, 2.4, 100, B),
        w("change your bill date (RBI)", 300, 680, L("2.25")[0] + 4.6, 2.2, 80, K),
    ]),
    dict(id="b13_recap", start=L("2.27")[0] - 0.2, end=L("2.28")[1] + 0.4, tag="", steps=[
        w("Minimum saves you from:", 220, 280, L("2.27")[0] + 0.3, 1.4, 76, K),
        dict(tick=[230, 360, 56], at=L("2.27")[0] + 2.0), w("late fee", 320, 400, L("2.27")[0] + 2.2, 0.7, 72, G),
        dict(tick=[1000, 360, 56], at=L("2.27")[0] + 3.0), w("bad CIBIL", 1090, 400, L("2.27")[0] + 3.2, 0.8, 72, G),
        dict(cross=[230, 470, 56], at=L("2.27")[0] + 4.4), w("NOT interest", 320, 530, L("2.27")[0] + 4.6, 1.0, 72, R),
        *flow(220, 840, 120, [("45%", L("2.28")[0] + 1.8, 0.7, R), ("18% GST", L("2.28")[0] + 4.0, 1.0, K), ("0 days", L("2.28")[0] + 6.6, 0.9, R)], gap=0.8),
    ]),
    dict(id="b14_next", start=L("2.31")[0] - 0.2, end=L("2.31")[1] + 0.4, tag="", steps=[
        w("Next video:", 300, 420, L("2.31")[0] + 0.2, 1.0, 100, B),
        w("can't pay even the minimum?", 300, 660, L("2.31")[0] + 1.4, 2.4, 90, R),
    ]),
]
