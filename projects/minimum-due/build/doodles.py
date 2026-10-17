#!/usr/bin/env python3
"""Doodle scenes that replace the whiteboard boards in the refined cut (owner, 2026-10-12: "white board and writing looks
out dated"; decision: desk for big moments, doodle for explaining; PLAYBOOK §5.6).

Same ids, start/end and page-turn moments as build/boards.py, so assemble.py's cut-ins and cutaways still land.
Every item appears on the word that names it: P(line, "phrase") is that phrase's time in the VO (build/words.py).
Objects and metaphors instead of sentences; labels of a few words; every number from claims.csv / mad_math.py.
Each item: kind, x, y (top-left of the object), s (scale), at, plus kind props (video/lib/doodle/doodle.js).
Back-from-cutaway times (RET) come from assemble.py's cutaway lengths, so nothing pops while a clip covers the board.
"""
from timing import L
from boards import BOARDS
from words import P

B = {b["id"]: b for b in BOARDS}
ER = {b["id"]: [st["at"] for st in b["steps"] if st.get("erase")] for b in BOARDS}


def page(items, out):
    """Exit every item of a page at `out` (film s)."""
    return [dict(it, exit=out) for it in items]


def ret(bid, n, back):
    """Film time the board is back on screen after assemble.py's cutaway at erase n (cutaway starts 0.2 s before it)."""
    return ER[bid][n] - 0.2 + back


DOODLES = {}

# 1.07 Only four thousand, six hundred and eighty eight was not paid. But the interest was almost the same. How?
DOODLES["b01_how"] = dict(kicker="ICICI BANK'S OWN EXAMPLE", tag="ICICI BANK · INTEREST RATES PAGE | 2025", items=[
    dict(kind="scale", x=960, y=330, s=1.35, at=L("1.07")[0] - 0.1, dur=0.8,
         tilt=[[0, 0], [P("1.07", "four") + 0.25, -5, 0.6], [P("1.07", "interest") + 0.35, -0.8, 0.9]]),
    dict(kind="coins", x=514, y=520, n=3, r=90, color="red", text="₹4,688", label="NOT PAID", labelDy=120, at=P("1.07", "four"),
         moves=[dict(at=P("1.07", "four") + 0.25, y=560, dur=0.6), dict(at=P("1.07", "interest") + 0.35, y=525, dur=0.9)]),
    dict(kind="coins", x=1406, y=440, n=3, r=90, color="amber", text="₹4,317", label="INTEREST + GST", labelDy=120, at=P("1.07", "interest"),
         moves=[dict(at=P("1.07", "interest") + 0.35, y=515, dur=0.9)]),
    dict(kind="label", x=960, y=960, text="ALMOST THE SAME", size=70, anchor="middle", hl="yel", at=P("1.07", "almost")),
])

# 1.10-1.15 the two numbers; what the minimum does and does not do; not a safety net but a switch
bid = "b02_numbers"; e = ER[bid]
cutin_back = L("1.11")[0] - 0.1 + 2.6          # assemble.py cut-in (sim bill) at 1.11, 2.6 s
back1 = ret(bid, 1, 2.9)
DOODLES[bid] = dict(kicker="OUR EXAMPLE · ₹30,000 BILL", tag="RBI CARD DIRECTIONS 2025 · PARA 5 | HDFC MAD FORMULA", items=[
    *page([
        dict(kind="bill", x=200, y=220, s=1.25, w=820, title="CARD BILL · SIMULATION", rows=[["Total amount due", "₹30,000"], ["Minimum amount due", "₹1,500", "red"]],
             hlRow=0, hlAt=P("1.10", "Total"), at=P("1.10", "the two numbers") - 0.2, dur=1.0),
        dict(kind="label", x=1260, y=420, text="= the full bill", size=62, color="blue", at=P("1.10", "full money")),
        dict(kind="ring", x=712, y=533, w=1100, h=160, at=cutin_back + 0.05, dur=0.5),
        dict(kind="label", x=1260, y=560, text="≈ 5% of the bill", size=58, color="red", at=P("1.11", "five")),
        dict(kind="label", x=1260, y=640, text="+ fees", size=58, color="red", at=P("1.11", "fees")),
        dict(kind="label", x=1470, y=640, text="+ GST", size=58, color="red", at=P("1.11", "GST")),
        dict(kind="label", x=1260, y=716, text="MOST BANKS", size=28, color="dim", mono=True, at=P("1.11", "Most banks")),
    ], e[0] - 0.25),
    *page([
        dict(kind="coins", x=760, y=820, n=20, r=95, color="#e8c35a", label="BILL ₹30,000", labelColor="ink", at=P("1.12", "thirty"), dur=0.8),
        dict(kind="coins", x=760, y=554, n=1, r=95, color="red", in_="pop", at=P("1.12", "the minimum"),
             moves=[dict(at=P("1.12", "the minimum") + 0.3, x=1300, y=520, s=1.5, dur=0.7)]),
        dict(kind="label", x=1300, y=700, text="₹1,500", size=96, color="red", anchor="middle", at=P("1.12", "fifteen")),
        dict(kind="label", x=1300, y=770, text="THE MINIMUM · ABOUT 5%", size=30, color="dim", mono=True, anchor="middle", at=P("1.12", "fifteen") + 0.3),
    ], e[1] - 0.25),
    *page([
        dict(kind="label", x=160, y=200, text="WHAT THE MINIMUM DOES", size=30, color="green", mono=True, at=back1 + 0.05),
        dict(kind="tag", x=160, y=260, text="₹0 late fee", color="green", size=56, at=back1 + 0.15),
        dict(kind="bill", x=160, y=470, w=520, h=220, title="CIBIL", rows=[["Payment", "ON TIME", "green"]], at=P("1.13", "report"), dur=0.7),
        dict(kind="badge", x=740, y=580, ok=True, at=P("1.13", "CIBIL")),
        dict(kind="label", x=1060, y=200, text="WHAT IT DOESN'T DO", size=30, color="red", mono=True, at=P("1.14", "But")),
        dict(kind="meter", x=1300, y=470, s=0.85, text="INTEREST KEEPS RUNNING", at=P("1.14", "does not stop"), dur=0.6,
             needle=[[0, -80], [P("1.14", "interest"), -40, 1.0], [e[2] - 0.4, 50, 3.0]]),
        dict(kind="calendar", x=1150, y=600, s=0.5, title="NOVEMBER", band={"from": 1, "to": 28, "color": "green"}, at=P("1.14", "And you lose") - 0.2, dur=0.6,
             bandShatterAt=P("1.14", "lose") + 0.25),
        dict(kind="label", x=1500, y=660, text="INTEREST-FREE", size=30, color="red", mono=True, at=P("1.14", "interest free period")),
        dict(kind="label", x=1500, y=730, text="period LOST", size=56, color="red", at=P("1.14", "period")),
    ], e[2] - 0.25),
    dict(kind="net", x=160, y=330, text="a safety net?", at=e[2] + 0.15, dur=1.2),
    dict(kind="cross", x=420, y=420, size=260, at=P("1.15", "not a safety"), dur=0.35),
    dict(kind="toggle", x=880, y=360, s=1.3, text="", at=P("1.15", "it is a switch") - 0.1, dur=0.5, onAt=P("1.15", "starts")),
    dict(kind="meter", x=1560, y=560, s=0.9, text="INTEREST", at=P("1.15", "starts"), dur=0.4, needle=[[0, -80], [P("1.15", "interest meter"), 60, 1.6]]),
    dict(kind="label", x=1050, y=860, text="minimum = interest switch ON", size=64, color="red", anchor="middle", hl="yel", at=P("1.15", "meter")),
])

# 1.36-1.37 a new swipe gets interest from the same day; the card has become a 45% loan
bid = "b05_newswipe"; e0 = ER[bid][0]; back = ret(bid, 0, 2.4)
DOODLES[bid] = dict(kicker="TILL THE OLD BILL IS FULLY PAID", tag="HDFC BANK MITC · ICICI BANK", items=[
    *page([
        dict(kind="pos", x=760, y=260, at=B[bid]["start"] + 0.05),
        dict(kind="card", x=200, y=330, s=0.9, at=B[bid]["start"] + 0.15,
             moves=[dict(at=P("1.36", "every new swipe"), x=620, y=400, rot=-12, dur=0.45), dict(at=P("1.36", "swipe") + 0.4, x=200, y=330, rot=0, dur=0.5)]),
        dict(kind="calendar", x=1180, y=200, s=0.62, title="NOVEMBER", marks=[dict(day=15, color="red", text="NEW SWIPE")], at=P("1.36", "swipe"), dur=0.7),
        dict(kind="label", x=1380, y=650, text="interest from the same day", size=44, color="red", anchor="middle", at=P("1.36", "gets interest")),
        dict(kind="stamp", x=1380, y=860, text="0 FREE DAYS", size=64, rot=-6, in_="stamp", at=P("1.36", "same day") + 0.3),
    ], e0 - 0.25),
    dict(kind="label", x=960, y=230, text="your card is not free any more", size=60, anchor="middle", hl="yel", at=max(back + 0.05, P("1.37", "your card"))),
    dict(kind="card", x=380, y=400, s=1.25, at=back + 0.05, in_="pop"),
    dict(kind="arrow", x=950, y=560, to=[230, 0], color="red", at=P("1.37", "It has become"), dur=0.4),
    dict(kind="tag", x=1200, y=490, text="a 45% loan", color="red", size=72, at=P("1.37", "forty five")),
])

# 2.09 CRIF: card bills unpaid 3 months to 1 year, ₹33,886 crore in March 2025, +44% in a year
DOODLES["b07_crif"] = dict(kicker="ALL OF INDIA", tag="CRIF HIGH MARK | MAR 2025", items=[
    dict(kind="tag", x=700, y=430, text="CRIF High Mark", color="#1b2a41", size=60, sub="CREDIT BUREAU · INDIA", at=B["b07_crif"]["start"] + 0.1, exit=P("2.09", "credit card bills") - 0.1),
    dict(kind="label", x=960, y=180, text="card bills unpaid 3 months to 1 year", size=54, anchor="middle", at=P("2.09", "credit card bills")),
    dict(kind="bars", x=620, y=880, w=260, bars=[dict(x=0, h=330, color="#8a8f99", label="A YEAR BEFORE"),
                                                 dict(x=420, h=475, color="red", top="₹33,886 cr", label="MAR 2025")],
         grow=[P("2.09", "forty four"), P("2.09", "thirty three")], at=P("2.09", "thirty three") - 0.3, dur=0.4, in_="pop"),
    dict(kind="tag", x=1340, y=420, text="+44%", color="red", size=84, at=P("2.09", "more than")),
    dict(kind="arrow", x=770, y=520, to=[230, -40], bend=-0.2, color="red", at=P("2.09", "percent more"), dur=0.5),
])

# 2.11-2.12 knowing the maths saves you; card rotation
bid = "b08_maths"; e0 = ER[bid][0]
DOODLES[bid] = dict(tag="", items=[
    *page([
        dict(kind="bill", x=200, y=300, w=600, h=230, title="CARD BILL", rows=[["Minimum due", "₹1,500", "red"]], at=P("2.11", "So what saves"), dur=0.7),
        dict(kind="cross", x=500, y=420, size=300, at=P("2.11", "small number"), dur=0.35),
        dict(kind="calc", x=1100, y=250, screen="45%", at=P("2.11", "It is knowing") - 0.1, dur=0.6),
        dict(kind="label", x=1230, y=760, text="knowing the maths", size=64, color="green", anchor="middle", hl="yel", at=P("2.11", "knowing")),
    ], e0 - 0.2),
    dict(kind="card", x=845, y=228, s=0.55, in_="pop", at=P("2.12", "Some people"), color="#3b5bdb"),
    dict(kind="card", x=1070, y=618, s=0.55, in_="pop", at=P("2.12", "use a"), color="#2a9d8f"),
    dict(kind="card", x=620, y=618, s=0.55, in_="pop", at=P("2.12", "shortcut"), color="#e76f51"),
    dict(kind="loop", x=960, y=560, r=300, at=P("2.12", "They call"), dur=0.6, spin=[[0, 0], [P("2.12", "rotation"), 0], [B[bid]["end"], 140, 2.6]]),
    dict(kind="label", x=960, y=990, text="CARD ROTATION", size=64, color="red", anchor="middle", at=P("2.12", "card rotation")),
])

# 2.14 the loan does not come down; only the last date moves; plus a fee
DOODLES["b09_loop"] = dict(tag="ILLUSTRATION", items=[
    dict(kind="box", x=160, y=420, w=380, h=260, text="₹30,000", sub="LOAN · NOT ONE RUPEE LESS", subColor="red", at=P("2.14", "your loan"), dur=0.8),
    dict(kind="calendar", x=700, y=230, s=0.55, title="NOVEMBER", marks=[dict(day=14, text="LAST DATE")], at=P("2.14", "Only the last date") - 0.1, dur=0.6),
    dict(kind="arrow", x=1080, y=380, to=[200, 0], color="ink", at=P("2.14", "moves"), dur=0.3),
    dict(kind="calendar", x=1300, y=230, s=0.55, title="DECEMBER", marks=[dict(day=14, text="LAST DATE")], in_="pop", at=P("2.14", "next month")),
    dict(kind="tag", x=1320, y=760, text="+ fee", color="red", size=64, at=P("2.14", "fee")),
])

# 2.17-2.18 rotation only pushes the loan; five simple steps
bid = "b10_postpone"; e0 = ER[bid][0]
DOODLES[bid] = dict(tag="", items=[
    *page([
        dict(kind="box", x=200, y=470, w=360, h=250, text="LOAN", at=P("2.17", "rotation"), dur=0.7, moves=[dict(at=P("2.17", "pushes"), x=1300, dur=1.6, ease="power1.inOut")]),
        dict(kind="arrow", x=300, y=820, to=[1000, 0], color="dim", at=P("2.17", "pushes"), dur=1.6),
        dict(kind="label", x=960, y=260, text="pushed, not paid", size=72, color="red", anchor="middle", hl="yel", at=P("2.17", "pushes") + 0.4),
    ], e0 - 0.2),
    dict(kind="label", x=960, y=300, text="what should we do", size=80, color="green", anchor="middle", at=ER[bid][0] + 0.2),
    *[dict(kind="sticky", x=170 + i * 330, y=440, w=280, h=200, n=i + 1, in_="pop", at=P("2.18", "Five") + 0.15 + 0.2 * i) for i in range(5)],
])

# 2.20-2.22 step 1 pay the full bill; step 2 pay as much as you can; why: more paid = less interest; full bill clears it
bid = "b11_steps12"; e0 = ER[bid][0]; back = ret(bid, 0, 2.8)
DOODLES[bid] = dict(tag="HDFC BANK MITC · ICICI BANK", items=[
    *page([dict(kind="sticky", x=140, y=240, n=1, lines=["Pay the", "FULL bill"], at=B[bid]["start"] + 0.1),
           dict(kind="calendar", x=620, y=230, s=0.62, title="NEXT MONTH", band={"from": 1, "to": 30, "color": "green"}, bandAt=P("2.20", "Up to fifty"),
                at=P("2.20", "really free") - 0.3, dur=0.7),
           dict(kind="tag", x=1180, y=330, text="up to 50 days free", color="green", size=56, sub="DEPENDS ON YOUR CARD", at=P("2.20", "fifty days"))],
         P("2.21", "Two") - 0.1),
    *page([dict(kind="sticky", x=140, y=240, n=2, color="blue", lines=["Pay as much", "as you can"], at=P("2.21", "Two") + 0.2),
           dict(kind="slider", x=620, y=520, w=1080, at=P("2.21", "If you cannot"), dur=0.6, knob=[[0, 86], [P("2.21", "as much as"), 700, 1.2]]),
           dict(kind="label", x=1160, y=720, text="never below the minimum", size=52, color="red", anchor="middle", at=P("2.21", "never less"))],
         e0 - 0.2),
    dict(kind="tag", x=160, y=280, text="pay more", color="green", size=72, at=max(back + 0.05, P("2.22", "Pay more"))),
    dict(kind="arrow", x=330, y=440, to=[0, 90], color="ink", at=P("2.22", "less interest") - 0.3, dur=0.3),
    dict(kind="tag", x=160, y=560, text="less interest", color="red", size=72, at=P("2.22", "less interest")),
    dict(kind="calendar", x=1000, y=200, s=0.62, title="AFTER YOU CLEAR IT", band={"from": 1, "to": 30, "color": "green"}, bandAt=P("2.22", "comes back") - 0.2,
         at=P("2.22", "once you clear"), dur=0.7),
    dict(kind="badge", x=1050, y=820, ok=True, text="interest-free period back", size=46, at=P("2.22", "comes back")),
])

# 2.24-2.25 step 4 EMI instead of 45%; no unknown loan apps; step 5 last date after salary
bid = "b12_emi"; e0 = ER[bid][0]; back = ret(bid, 0, 2.4)
DOODLES[bid] = dict(shift=130, tag="HDFC BANK SMARTEMI PAGE | 2026 · RBI CARD DIRECTIONS", items=[
    *page([dict(kind="sticky", x=120, y=230, n=4, lines=["Ask for", "EMI"], at=B[bid]["start"] + 0.1),
           dict(kind="tag", x=520, y=250, text="45%", color="red", size=80, sub="CARD INTEREST", at=P("2.24", "For example")),
           dict(kind="tag", x=520, y=520, text="11–25%", color="green", size=80, sub="BANK EMI, E.G. HDFC", at=P("2.24", "eleven")),
           dict(kind="tag", x=1000, y=560, s=0.8, text="+ fee + GST", color="amber", size=56, at=P("2.24", "check the fee")),
           dict(kind="phone", x=1430, y=200, s=0.9, lines=["LOAN IN", "5 MINUTES"], apps=[{}, {"color": "#f4a261"}, {}, {}, {"color": "#e76f51"}, {}],
                at=P("2.24", "never take"), dur=0.5),
           dict(kind="cross", x=1547, y=420, size=300, at=P("2.24", "unknown apps"), dur=0.3),
           dict(kind="label", x=1547, y=760, text="no unknown loan apps", size=40, color="red", anchor="middle", at=P("2.24", "unknown apps") + 0.15)],
         e0 - 0.25),
    dict(kind="sticky", x=120, y=230, n=5, color="blue", lines=["Last date", "after salary"], at=back + 0.05),
    dict(kind="calendar", x=700, y=200, s=0.72, title="EVERY MONTH", marks=[dict(day=5, color="green", text="SALARY")], at=back + 0.15, dur=0.7),
    dict(kind="pin", x=788, y=290, color="red", text="LAST DATE", in_="pop", at=back + 0.5, moves=[dict(at=P("2.25", "change your bill date"), x=861, y=340, dur=0.9)]),
    dict(kind="label", x=1480, y=520, text="change your bill date", size=52, color="blue", anchor="middle", at=P("2.25", "change your bill date")),
    dict(kind="label", x=1480, y=600, text="RBI: THE BANK MUST OFFER IT", size=30, color="dim", mono=True, anchor="middle", at=P("2.25", "RBI rules")),
])

# 2.27-2.28 recap: the minimum saves you from late fee and bad CIBIL, not interest; three numbers
DOODLES["b13_recap"] = dict(kicker="REMEMBER", tag="", items=[
    *page([dict(kind="label", x=960, y=200, text="the minimum saves you from…", size=56, anchor="middle", at=B["b13_recap"]["start"] + 0.15),
           dict(kind="tag", x=170, y=330, text="late fee", color="#8a8f99", size=60, at=P("2.27", "late fees")),
           dict(kind="badge", x=330, y=560, ok=True, at=P("2.27", "late fees") + 0.3),
           dict(kind="bill", x=720, y=300, w=440, h=220, title="CIBIL", rows=[["Payment", "OK", "green"]], at=P("2.27", "bad CIBIL"), dur=0.5),
           dict(kind="badge", x=940, y=600, ok=True, at=P("2.27", "CIBIL") + 0.35),
           dict(kind="meter", x=1500, y=470, s=0.8, text="INTEREST", at=P("2.27", "Not from interest"), dur=0.4, needle=[[0, -80], [P("2.27", "interest") + 0.2, 40, 1.2]]),
           dict(kind="badge", x=1500, y=600, ok=False, text="not this", size=44, at=P("2.27", "interest"))],
         L("2.28")[0]),
    dict(kind="label", x=960, y=250, text="3 numbers to remember", size=60, anchor="middle", hl="yel", at=P("2.28", "three numbers")),
    dict(kind="tag", x=180, y=420, s=1.25, text="45%", color="red", size=84, sub="INTEREST A YEAR", at=P("2.28", "Forty five")),
    dict(kind="tag", x=760, y=420, s=1.1, text="18% GST", color="amber", size=72, sub="ON TOP", at=P("2.28", "Eighteen")),
    dict(kind="tag", x=1320, y=420, s=1.1, text="0 days", color="red", size=72, sub="FREE ON NEW SPENDS", at=P("2.28", "zero")),
])

# 2.31 next video: can't pay even the minimum
DOODLES["b14_next"] = dict(tag="", items=[
    dict(kind="label", x=960, y=200, text="NEXT VIDEO", size=34, color="dim", mono=True, anchor="middle", at=B["b14_next"]["start"] + 0.1),
    dict(kind="bill", x=620, y=260, w=680, h=240, title="CARD BILL", rows=[["Minimum amount due", "₹1,500", "red"]], at=P("2.31", "next video") + 0.2, dur=0.7),
    dict(kind="stamp", x=960, y=640, text="UNPAID", size=96, rot=-8, in_="stamp", at=P("2.31", "cannot pay")),
])
