#!/usr/bin/env python3
"""Doodle scenes that replace the whiteboard boards in the refined cut (owner, 2026-10-12: "white board and writing looks
out dated"; decision: desk for big moments, doodle for explaining; PLAYBOOK §5.6).

Same ids, start/end and erase moments as build/boards.py, so assemble.py's cut-ins and cutaways still land on the page
turns. Objects and metaphors instead of sentences; labels of a few words; every number from claims.csv / mad_math.py
(same values the boards showed). Times below are film seconds via T(line, offset); make_doodles.py makes them relative.
Each item: kind, x, y (top-left of the object), s (scale), at, plus kind props (video/lib/doodle/doodle.js).
"""
from timing import L
from boards import BOARDS

B = {b["id"]: b for b in BOARDS}


def T(line, off=0.0):
    return L(line)[0] + off


def page(items, out):
    """Exit every item of a page at `out` (film s)."""
    return [dict(it, exit=out) for it in items]


CALC = "OUR CALCULATION · ICICI METHOD, 45% A YEAR"
DOODLES = {}

# 1.07 Only 4,688 was not paid. But the interest was almost the same. How?
s = B["b01_how"]["start"]
DOODLES["b01_how"] = dict(kicker="ICICI BANK'S OWN EXAMPLE", tag="ICICI BANK · INTEREST RATES PAGE | 2025", items=[
    dict(kind="scale", x=960, y=330, s=1.35, at=T("1.07", 0.0), dur=1.0, tilt=[[0, 0], [T("1.07", 1.5), -5, 0.6], [T("1.07", 3.8), -0.8, 0.9]]),
    dict(kind="coins", x=514, y=520, n=3, r=90, color="red", text="₹4,688", label="NOT PAID", labelDy=120, at=T("1.07", 1.3),
         moves=[dict(at=T("1.07", 1.5), y=560, dur=0.6), dict(at=T("1.07", 3.8), y=525, dur=0.9)]),
    dict(kind="coins", x=1406, y=440, n=3, r=90, color="amber", text="₹4,317", label="INTEREST + GST", labelDy=120, at=T("1.07", 3.5),
         moves=[dict(at=T("1.07", 3.8), y=515, dur=0.9)]),
    dict(kind="label", x=960, y=960, text="ALMOST THE SAME", size=70, anchor="middle", hl="yel", at=T("1.07", 4.6)),
])

# 1.10-1.15 the two numbers; what the minimum does and does not do; not a safety net but a switch
s = B["b02_numbers"]["start"]
e = [s + 13.66, s + 17.67, s + 29.14]
DOODLES["b02_numbers"] = dict(kicker="OUR EXAMPLE · ₹30,000 BILL", tag="RBI CARD DIRECTIONS 2025 · PARA 5 | HDFC MAD FORMULA", items=[
    *page([
        dict(kind="bill", x=200, y=220, s=1.25, w=820, title="CARD BILL · SIMULATION", rows=[["Total amount due", "₹30,000"], ["Minimum amount due", "₹1,500", "red"]],
             hlRow=0, hlAt=T("1.10", 1.4), at=T("1.10", 0.2), dur=1.2),
        dict(kind="label", x=1260, y=420, text="= the full bill", size=62, color="blue", at=T("1.10", 2.8)),
        dict(kind="ring", x=712, y=533, w=1100, h=160, at=T("1.11", 2.8), dur=0.5),
        dict(kind="label", x=1260, y=560, text="≈ 5% + fees + GST", size=62, color="red", at=T("1.11", 4.2)),
        dict(kind="label", x=1260, y=640, text="MOST BANKS", size=28, color="dim", mono=True, at=T("1.11", 4.4)),
    ], e[0] - 0.25),
    *page([
        dict(kind="coins", x=760, y=820, n=20, r=95, color="#e8c35a", label="BILL ₹30,000", labelColor="ink", at=T("1.12", 0.1), dur=0.9),
        dict(kind="coins", x=760, y=554, n=1, r=95, color="red", in_="pop", at=T("1.12", 1.0), moves=[dict(at=T("1.12", 1.6), x=1300, y=520, s=1.5, dur=0.8)]),
        dict(kind="label", x=1300, y=700, text="₹1,500", size=96, color="red", anchor="middle", at=T("1.12", 2.2)),
        dict(kind="label", x=1300, y=770, text="THE MINIMUM · ABOUT 5%", size=30, color="dim", mono=True, anchor="middle", at=T("1.12", 2.4)),
    ], e[1] - 0.25),
    *page([
        dict(kind="label", x=160, y=200, text="WHAT THE MINIMUM DOES", size=30, color="green", mono=True, at=e[1] + 2.75),
        dict(kind="tag", x=160, y=260, text="₹0 late fee", color="green", size=56, at=T("1.13", 2.5)),
        dict(kind="bill", x=160, y=470, w=520, h=220, title="CIBIL", rows=[["Payment", "ON TIME", "green"]], at=T("1.13", 4.0), dur=0.8),
        dict(kind="badge", x=740, y=580, ok=True, at=T("1.13", 4.6)),
        dict(kind="label", x=1060, y=200, text="WHAT IT DOESN'T DO", size=30, color="red", mono=True, at=T("1.14", 0.0)),
        dict(kind="meter", x=1300, y=470, s=0.85, text="INTEREST KEEPS RUNNING", at=T("1.14", 0.2), dur=0.7,
             needle=[[0, -80], [T("1.14", 0.9), -40, 1.2], [e[2] - 0.4, 50, 3.5]]),
        dict(kind="calendar", x=1150, y=600, s=0.5, title="NOVEMBER", band=dict(**{"from": 1, "to": 28, "color": "green"}), at=T("1.14", 2.4), dur=0.7,
             bandShatterAt=T("1.14", 3.4)),
        dict(kind="label", x=1500, y=660, text="INTEREST-FREE", size=30, color="red", mono=True, at=T("1.14", 3.5)),
        dict(kind="label", x=1500, y=730, text="period LOST", size=56, color="red", at=T("1.14", 3.6)),
    ], e[2] - 0.25),
    dict(kind="net", x=160, y=330, text="a safety net?", at=T("1.15", 0.4), dur=1.0, exit=s + 35.9),
    dict(kind="cross", x=420, y=420, size=260, at=T("1.15", 3.2), dur=0.4),
    dict(kind="toggle", x=880, y=360, s=1.3, text="", at=T("1.15", 3.6), dur=0.6, onAt=T("1.15", 4.4)),
    dict(kind="meter", x=1560, y=560, s=0.9, text="INTEREST", at=T("1.15", 4.4), dur=0.5, needle=[[0, -80], [T("1.15", 4.6), 60, 1.8]]),
    dict(kind="label", x=1050, y=860, text="minimum = interest switch ON", size=64, color="red", anchor="middle", hl="yel", at=T("1.15", 4.8)),
])

# 1.36-1.37 a new swipe gets interest from the same day; the card has become a 45% loan
s = B["b05_newswipe"]["start"]
e0 = s + 6.15
DOODLES["b05_newswipe"] = dict(kicker="TILL THE OLD BILL IS FULLY PAID", tag="HDFC BANK MITC · ICICI BANK", items=[
    *page([
        dict(kind="pos", x=760, y=260, at=T("1.36", 0.2)),
        dict(kind="card", x=200, y=330, s=0.9, at=T("1.36", 0.3), moves=[dict(at=T("1.36", 1.2), x=620, y=400, rot=-12, dur=0.5),
                                                                          dict(at=T("1.36", 1.8), x=200, y=330, rot=0, dur=0.5)]),
        dict(kind="calendar", x=1180, y=200, s=0.62, title="NOVEMBER", marks=[dict(day=15, color="red", text="NEW SWIPE")], at=T("1.36", 2.3), dur=0.8),
        dict(kind="label", x=1380, y=650, text="interest from the same day", size=44, color="red", anchor="middle", at=T("1.36", 3.0)),
        dict(kind="stamp", x=1380, y=860, text="0 FREE DAYS", size=64, rot=-6, in_="stamp", at=T("1.36", 4.2)),
    ], e0 - 0.25),
    dict(kind="label", x=960, y=230, text="your card is not free any more", size=60, anchor="middle", hl="yel", at=e0 + 2.3),
    dict(kind="card", x=380, y=400, s=1.25, at=e0 + 2.3, in_="pop"),
    dict(kind="arrow", x=950, y=560, to=[230, 0], color="red", at=T("1.37", 3.8), dur=0.4),
    dict(kind="tag", x=1200, y=490, text="a 45% loan", color="red", size=72, at=T("1.37", 4.3)),
])

# 2.09 CRIF: card bills unpaid 3 months to 1 year, ₹33,886 crore in March 2025, +44% in a year
s = B["b07_crif"]["start"]
DOODLES["b07_crif"] = dict(kicker="ALL OF INDIA", tag="CRIF HIGH MARK | MAR 2025", items=[
    dict(kind="label", x=960, y=180, text="card bills unpaid 3 months to 1 year", size=54, anchor="middle", at=T("2.09", 0.5)),
    dict(kind="bars", x=620, y=880, w=260, bars=[dict(x=0, h=330, color="#8a8f99", label="A YEAR BEFORE"),
                                                 dict(x=420, h=475, color="red", top="₹33,886 cr", label="MAR 2025")],
         grow=[T("2.09", 5.2), T("2.09", 7.4)], at=T("2.09", 4.8), dur=0.4, in_="pop"),
    dict(kind="arrow", x=770, y=520, to=[230, -40], bend=-0.2, color="red", at=T("2.09", 11.6), dur=0.5),
    dict(kind="tag", x=1340, y=420, text="+44%", color="red", size=84, at=T("2.09", 12.6)),
])

# 2.11-2.12 knowing the maths saves you; card rotation
s = B["b08_maths"]["start"]
e0 = s + 4.85
DOODLES["b08_maths"] = dict(tag="", items=[
    *page([
        dict(kind="bill", x=200, y=300, w=600, h=230, title="CARD BILL", rows=[["Minimum due", "₹1,500", "red"]], at=T("2.11", 0.2), dur=0.8),
        dict(kind="cross", x=500, y=420, size=300, at=T("2.11", 1.4), dur=0.4),
        dict(kind="calc", x=1100, y=250, screen="45%", at=T("2.11", 2.1), dur=0.7),
        dict(kind="label", x=1230, y=760, text="knowing the maths", size=64, color="green", anchor="middle", hl="yel", at=T("2.11", 2.6)),
    ], e0 - 0.2),
    dict(kind="loop", x=960, y=560, r=300, at=T("2.12", 0.9), dur=0.7, spin=[[0, 0], [T("2.12", 1.6), 0], [s + 8.66, 140, 2.8]]),
    dict(kind="card", x=845, y=228, s=0.55, in_="pop", at=T("2.12", 0.2), color="#3b5bdb"),
    dict(kind="card", x=1070, y=618, s=0.55, in_="pop", at=T("2.12", 0.4), color="#2a9d8f"),
    dict(kind="card", x=620, y=618, s=0.55, in_="pop", at=T("2.12", 0.6), color="#e76f51"),
    dict(kind="label", x=960, y=990, text="CARD ROTATION", size=64, color="red", anchor="middle", at=T("2.12", 1.5)),
])

# 2.14 the loan does not come down; only the last date moves; plus a fee
s = B["b09_loop"]["start"]
DOODLES["b09_loop"] = dict(tag="ILLUSTRATION", items=[
    dict(kind="box", x=160, y=420, w=380, h=260, text="₹30,000", sub="LOAN · NOT ONE RUPEE LESS", subColor="red", at=T("2.14", 0.2), dur=0.9),
    dict(kind="calendar", x=700, y=230, s=0.55, title="NOVEMBER", marks=[dict(day=14, text="LAST DATE")], at=T("2.14", 2.4), dur=0.7),
    dict(kind="arrow", x=1080, y=380, to=[200, 0], color="ink", at=T("2.14", 3.4), dur=0.3),
    dict(kind="calendar", x=1300, y=230, s=0.55, title="DECEMBER", marks=[dict(day=14, text="LAST DATE")], in_="pop", at=T("2.14", 3.7)),
    dict(kind="tag", x=1320, y=760, text="+ fee", color="red", size=64, at=T("2.14", 5.4)),
])

# 2.17-2.18 rotation only pushes the loan; five simple steps
s = B["b10_postpone"]["start"]
e0 = s + 4.77
DOODLES["b10_postpone"] = dict(tag="", items=[
    *page([
        dict(kind="box", x=200, y=470, w=360, h=250, text="LOAN", at=T("2.17", 0.2), dur=0.8, moves=[dict(at=T("2.17", 1.4), x=1300, dur=2.0, ease="power1.inOut")]),
        dict(kind="arrow", x=300, y=820, to=[1000, 0], color="dim", at=T("2.17", 1.4), dur=2.0),
        dict(kind="label", x=960, y=260, text="pushed, not paid", size=72, color="red", anchor="middle", hl="yel", at=T("2.17", 2.6)),
    ], e0 - 0.2),
    dict(kind="label", x=960, y=300, text="5 simple steps", size=80, color="green", anchor="middle", at=T("2.18", 1.2)),
    *[dict(kind="sticky", x=170 + i * 330, y=440, w=280, h=200, n=i + 1, in_="pop", at=T("2.18", 1.6 + 0.22 * i)) for i in range(5)],
])

# 2.20-2.22 step 1 pay the full bill; step 2 pay as much as you can; why: more paid = less interest; full bill clears it
s = B["b11_steps12"]["start"]
e0 = s + 11.32
DOODLES["b11_steps12"] = dict(tag="HDFC BANK MITC · ICICI BANK", items=[
    *page([dict(kind="sticky", x=140, y=240, n=1, lines=["Pay the", "FULL bill"], at=T("2.20", 0.1)),
           dict(kind="calendar", x=620, y=230, s=0.62, title="NEXT MONTH", band=dict(**{"from": 1, "to": 30, "color": "green"}), bandAt=T("2.20", 1.6), at=T("2.20", 0.6), dur=0.8),
           dict(kind="tag", x=1180, y=330, text="up to 50 days free", color="green", size=56, sub="DEPENDS ON YOUR CARD", at=T("2.20", 2.2))],
         T("2.21", 0.05)),
    *page([dict(kind="sticky", x=140, y=240, n=2, color="blue", lines=["Pay as much", "as you can"], at=T("2.21", 0.3)),
           dict(kind="slider", x=620, y=520, w=1080, at=T("2.21", 0.8), dur=0.7, knob=[[0, 86], [T("2.21", 1.6), 700, 1.4]]),
           dict(kind="label", x=1160, y=720, text="never below the minimum", size=52, color="red", anchor="middle", at=T("2.21", 3.4))],
         e0 - 0.2),
    dict(kind="tag", x=160, y=280, text="pay more", color="green", size=72, at=e0 + 2.7),
    dict(kind="arrow", x=330, y=440, to=[0, 90], color="ink", at=e0 + 3.0, dur=0.3),
    dict(kind="tag", x=160, y=560, text="less interest", color="red", size=72, at=e0 + 3.2),
    dict(kind="calendar", x=1000, y=200, s=0.62, title="AFTER YOU CLEAR IT", band=dict(**{"from": 1, "to": 30, "color": "green"}), bandAt=T("2.22", 5.8), at=T("2.22", 5.0), dur=0.8),
    dict(kind="badge", x=1050, y=820, ok=True, text="interest-free period back", size=46, at=T("2.22", 6.4)),
])

# 2.24-2.25 step 4 EMI instead of 45%; no unknown loan apps; step 5 last date after salary
s = B["b12_emi"]["start"]
e0 = s + 9.84
DOODLES["b12_emi"] = dict(shift=130, tag="HDFC BANK SMARTEMI PAGE | 2026 · RBI CARD DIRECTIONS", items=[
    *page([dict(kind="sticky", x=120, y=230, n=4, lines=["Ask for", "EMI"], at=T("2.24", 4.8)),
           dict(kind="tag", x=520, y=250, text="45%", color="red", size=80, sub="CARD INTEREST", at=T("2.24", 5.6)),
           dict(kind="tag", x=520, y=520, text="11–25%", color="green", size=80, sub="BANK EMI, E.G. HDFC", at=T("2.24", 7.0)),
           dict(kind="tag", x=1000, y=560, s=0.8, text="+ fee + GST", color="amber", size=56, at=T("2.24", 9.2)),
           dict(kind="phone", x=1430, y=200, s=0.9, lines=["LOAN IN", "5 MINUTES"], apps=[{}, {"color": "#f4a261"}, {}, {}, {"color": "#e76f51"}, {}], at=T("2.24", 11.2), dur=0.6),
           dict(kind="cross", x=1547, y=420, size=300, at=T("2.24", 11.8), dur=0.3),
           dict(kind="label", x=1547, y=760, text="no unknown loan apps", size=40, color="red", anchor="middle", at=T("2.24", 12.0))],
         e0 - 0.25),
    dict(kind="sticky", x=120, y=230, n=5, color="blue", lines=["Last date", "after salary"], at=e0 + 2.25),
    dict(kind="calendar", x=700, y=200, s=0.72, title="EVERY MONTH", marks=[dict(day=5, color="green", text="SALARY")], at=e0 + 2.4, dur=0.8),
    dict(kind="pin", x=788, y=290, color="red", text="LAST DATE", in_="pop", at=e0 + 3.0, moves=[dict(at=T("2.25", 2.6), x=861, y=340, dur=1.0)]),
    dict(kind="label", x=1480, y=520, text="change your bill date", size=52, color="blue", anchor="middle", at=T("2.25", 3.0)),
    dict(kind="label", x=1480, y=600, text="RBI: THE BANK MUST OFFER IT", size=30, color="dim", mono=True, anchor="middle", at=T("2.25", 4.8)),
])

# 2.27-2.28 recap: the minimum saves you from late fee and bad CIBIL, not interest; three numbers
s = B["b13_recap"]["start"]
DOODLES["b13_recap"] = dict(kicker="REMEMBER", tag="", items=[
    *page([dict(kind="label", x=960, y=200, text="the minimum saves you from…", size=56, anchor="middle", at=T("2.27", 0.3)),
           dict(kind="tag", x=170, y=330, text="late fee", color="#8a8f99", size=60, at=T("2.27", 1.8)),
           dict(kind="badge", x=330, y=560, ok=True, at=T("2.27", 2.2)),
           dict(kind="bill", x=720, y=300, w=440, h=220, title="CIBIL", rows=[["Payment", "OK", "green"]], at=T("2.27", 2.8), dur=0.6),
           dict(kind="badge", x=940, y=600, ok=True, at=T("2.27", 3.3)),
           dict(kind="meter", x=1500, y=470, s=0.8, text="INTEREST", at=T("2.27", 4.2), dur=0.5, needle=[[0, -80], [T("2.27", 4.6), 40, 1.5]]),
           dict(kind="badge", x=1500, y=600, ok=False, text="not this", size=44, at=T("2.27", 4.8))],
         T("2.28", 0.0)),
    dict(kind="label", x=960, y=250, text="3 numbers to remember", size=60, anchor="middle", hl="yel", at=T("2.28", 0.4)),
    dict(kind="tag", x=180, y=420, s=1.25, text="45%", color="red", size=84, sub="INTEREST A YEAR", at=T("2.28", 1.8)),
    dict(kind="tag", x=760, y=420, s=1.1, text="18% GST", color="amber", size=72, sub="ON TOP", at=T("2.28", 4.0)),
    dict(kind="tag", x=1320, y=420, s=1.1, text="0 days", color="red", size=72, sub="FREE ON NEW SPENDS", at=T("2.28", 6.6)),
])

# 2.31 next video: can't pay even the minimum
s = B["b14_next"]["start"]
DOODLES["b14_next"] = dict(tag="", items=[
    dict(kind="label", x=960, y=200, text="NEXT VIDEO", size=34, color="dim", mono=True, anchor="middle", at=T("2.31", 0.2)),
    dict(kind="bill", x=620, y=260, w=680, h=240, title="CARD BILL", rows=[["Minimum amount due", "₹1,500", "red"]], at=T("2.31", 0.3), dur=0.8),
    dict(kind="stamp", x=960, y=640, text="UNPAID", size=96, rot=-8, in_="stamp", at=T("2.31", 2.6)),
])
