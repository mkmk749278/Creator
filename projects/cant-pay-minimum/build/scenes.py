#!/usr/bin/env python3
"""Scene designs for Can't Pay Even the Minimum (visual-plan.md). Two kinds:

  desk  (video/lib/plates): photoreal desk plates (props_lib.PLATES) crossfading on a moving camera, for big moments.
  page  (video/lib/doodle): paper pages where photoreal prop cut-outs (props_lib.PROPS) drop in and ink annotations
        (rings, strikes, arrows, short labels) draw on and around them, landing on the prop's anchors.

Every time is film seconds; P(line, "phrase") is when that phrase starts in the VO (build/words.py), so each item appears
on the word that names it. A scene covers a film span [start, end); assemble.py cuts away from it (footage, proofs) and
comes back at the matching time, so the scene keeps time while it is off screen.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import L                     # noqa: E402
from words import P                      # noqa: E402
import props_lib                         # noqa: E402

SCENES = {}


# ---- helpers ----
def photo(name, x, y, w, at, **kw):
    """A prop cut-out placed with its top-left at (x, y), w px wide on the 1920×1080 page."""
    m = props_lib.meta(name)
    it = dict(kind="photo", src=f"img/{name}.png", x=x, y=y, w=w, h=round(w * m["h"] / m["w"]), at=at, in_=kw.pop("in_", "drop"), **kw)
    it["_prop"] = name
    return it


def an(it, key):
    """Page coordinates of anchor `key` of a placed photo item (no rotation on annotated photos)."""
    m = props_lib.meta(it["_prop"]); k = it["w"] / m["w"]; ax, ay = m["anchors"][key]
    return round(it["x"] + ax * k, 1), round(it["y"] + ay * k, 1)


def box(it, key):
    """(x, y, w, h) on the page of a rectangle anchor (key.tl / key.br)."""
    x0, y0 = an(it, key + ".tl"); x1, y1 = an(it, key + ".br")
    return x0, y0, x1 - x0, y1 - y0


def ring(it, key, at, pad=1.25, **kw):
    x, y, w, h = box(it, key)
    return dict(kind="ring", x=round(x + w / 2), y=round(y + h / 2), w=round(w * pad), h=round(h * pad + 30), at=at, dur=kw.pop("dur", 0.5), **kw)


def page(items, out):
    return [dict(it, exit=out) for it in items]


def pa(plate, key):
    """Anchor of a desk plate in 1920×1080 page px (plates are 3840 wide)."""
    x, y = props_lib.meta(plate)["anchors"][key]
    return x / 2, y / 2


def push(t0, t1, s, focus, s0=1.0):
    """Camera key pair: from scale s0 (centred) at t0 to scale s pushed toward focus (x, y page px) by t1."""
    fx, fy = focus
    return [[round(t0, 2), s0, 0, 0, 0.01], [round(t0 + 0.02, 2), s, round(-(fx - 960) * (s - 1), 1), round(-(fy - 540) * (s - 1), 1), round(t1 - t0, 2)]]


# =====================================================================================================================
# ACT 1: hook
# C001 A message comes on your phone. Your credit card payment is overdue.
# C002 Then another message. Then a call from a number you don't know.
# C003 In our last video, ... Today, a harder question.  (assemble.py cuts to part 1 for "In our last video …")
t_sms1 = P("C001", "message") + 0.05
t_over = P("C001", "Your credit")
t_sms2 = P("C002", "another")
t_call = P("C002", "a call")
t_hard = P("C003", "Today")
phoneA = pa("deskA_sms1", "phone:center")
billA = pa("deskA_sms1", "bill:box1")
SCENES["d01_night"] = dict(kind="desk", start=0.0, end=L("C004")[0] - 0.25, tag="SIMULATION", layers=[
    dict(src="deskA_off", at=0),
    dict(src="deskA_sms1", at=t_sms1, fade=0.18),
    dict(src="deskA_sms2", at=t_sms2, fade=0.18),
    dict(src="deskB_call", at=t_call - 0.05),
    dict(src="deskA_sms2", at=t_hard - 0.25),
], cam=[
    [0, 1.0, 0, 0],
    *push(0.0, t_over - 0.1, 1.12, phoneA),
    [round(t_over - 0.05, 2), 1.55, round(-(phoneA[0] - 960) * 0.55, 1), round(-(phoneA[1] - 540) * 0.55, 1), 1.6, "power2.inOut"],
    *push(t_call - 0.05, L("C003")[0] + 2, 1.08, (960, 560)),
    *push(t_hard - 0.25, L("C004")[0], 1.3, billA),
], shake=[[t_sms1, 0.42, 3], [t_sms2, 0.42, 6], *[[t_call + k * 1.0, 0.42, 7] for k in range(5)]],
   sfx=[[t_sms1, "buzz"], [t_sms2, "buzz"], *[[t_call + k * 1.0, "buzz"] for k in range(5)]])

# C004 What if you cannot pay even that minimum?
b = photo("bill_ravi", 560, 70, 720, L("C004")[0] - 0.2, in_="fade", float=0.6)
SCENES["p01_minimum"] = dict(kind="page", start=L("C004")[0] - 0.25, end=L("C005")[0] - 0.2, kicker="OUR EXAMPLE · ₹10,000 BILL", tag="SIMULATION", items=[
    b,
    ring(b, "box1", P("C004", "minimum") - 0.1, color="red"),
    dict(kind="strike", x=box(b, "box1")[0] + 18, y=round(an(b, "box1")[1] + 8), w=round(box(b, "box1")[2] - 36), at=P("C004", "cannot"), dur=0.35),
    dict(kind="label", x=1330, y=round(an(b, "box1")[1] + 20), text="can't pay even this", size=54, color="red", at=P("C004", "even")),
])

# C007 Most people think there is one answer for everyone. There isn't.
# C008 Someone who owes ten thousand rupees and someone who owes ten lakh live two very different stories.
c = photo("card_black", 640, 250, 640, L("C007")[0] - 0.2, float=1.2)
r10k = photo("bill_ravi", 210, 120, 560, P("C008", "ten thousand") - 0.15)
r10l = photo("bill_10l", 1150, 120, 560, P("C008", "ten lakh") - 0.15)
SCENES["p02_two_stories"] = dict(kind="page", start=L("C007")[0] - 0.25, end=L("C009")[0] - 0.2, tag="SIMULATION", items=[
    *page([
        c,
        dict(kind="label", x=960, y=200, text="ONE ANSWER FOR EVERYONE", size=64, anchor="middle", at=P("C007", "one answer")),
        dict(kind="strike", x=455, y=180, w=1010, at=P("C007", "There isn't"), dur=0.35),
    ], L("C008")[0] - 0.35),
    r10k, r10l,
    ring(r10k, "box0", P("C008", "ten thousand") + 0.4, color="blue"),
    ring(r10l, "box0", P("C008", "ten lakh") + 0.4, color="red"),
    dict(kind="label", x=960, y=1010, text="TWO DIFFERENT STORIES", size=60, anchor="middle", hl="yel", at=P("C008", "two very")),
])


# =====================================================================================================================
# ACT 2: the clock, the bank's side, CIBIL
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import cpm_math as M                     # noqa: E402  (tools/cpm_math.py: OUR CALCULATION)

# C011 First, let's understand the clock. The day your last date passes, the bank starts counting.
# C012 Thirty days. Sixty days. Ninety days. The bank's system checks your account every single day.
# C013 If the minimum stays unpaid for ninety days after the due date, the bank must mark your card a bad loan.
#      They call it an NPA. A non performing asset.          (assemble.py: proof RBI NPA rule over "If the minimum ... due date")
b = photo("bill_ravi", 110, 170, 560, L("C011")[0] - 0.1, float=0.5)
X0, X1, YR = 830, 1760, 760
xs = {0: X0, 30: X0 + (X1 - X0) / 3, 60: X0 + 2 * (X1 - X0) / 3, 90: X1}
t30, t60, t90 = P("C012", "Thirty"), P("C012", "Sixty"), P("C012", "Ninety")
t_npa = P("C013", "bad loan")
SCENES["p03_clock"] = dict(kind="page", start=L("C011")[0] - 0.25, end=L("C014")[0] - 0.2, kicker="THE FIRST CLOCK", tag="RBI | IRAC NORMS", items=[
    b,
    ring(b, "box2", P("C011", "last date"), color="red"),
    dict(kind="arrow", x=X0, y=YR, to=[X1 - X0 + 60, 0], at=P("C011", "starts counting") - 0.3, dur=0.7),
    *[dict(kind="label", x=round(xs[d]), y=YR + 70, text=f"DAY {d}", size=34, mono=True, anchor="middle", color="red" if d == 90 else "dim", at=a)
      for d, a in ((0, P("C011", "starts counting")), (30, t30), (60, t60), (90, t90))],
    dict(kind="pin", x=X0, y=YR - 8, color="red", at=P("C011", "starts counting"),
         moves=[dict(at=t30, x=round(xs[30]), dur=0.6), dict(at=t60, x=round(xs[60]), dur=0.6), dict(at=t90, x=round(xs[90]), dur=0.6)]),
    dict(kind="counter", x=1295, y=520, size=190, anchor="middle", fmt="days", from_=0, label="DAYS PAST DUE", at=P("C011", "starts counting"),
         steps=[[P("C011", "starts counting") + 0.2, 3, 1.2], [t30, 30, 0.6], [t60, 60, 0.6], [t90, 90, 0.6], [t_npa - 0.4, 91, 0.2]]),
    dict(kind="stamp", x=round(an(b, "center")[0]), y=round(an(b, "center")[1] + 40), text="NPA · DAY 91", size=78, rot=-12, in_="stamp", at=t_npa),
    dict(kind="label", x=1295, y=960, text="BAD LOAN = NPA", size=64, anchor="middle", hl="yel", at=P("C013", "NPA")),
    dict(kind="label", x=1295, y=1030, text="NON-PERFORMING ASSET", size=30, mono=True, anchor="middle", color="dim", at=P("C013", "non performing")),
], sfx=[[P("C012", "every single") + k * 0.25, "tick"] for k in range(8)])

# C014 Now here is something most people don't know. From that day, your unpaid card is also a loss for the bank.
# C015 The bank must keep aside at least a quarter of what you owe, from its own profit. That is one reason the pressure
#      grows around this time.
b = photo("bill_ravi_overdue", 120, 190, 520, L("C014")[0] - 0.1, float=0.5)
SCENES["p04_provision"] = dict(kind="page", start=L("C014")[0] - 0.25, end=L("C016")[0] - 0.2, kicker="THE BANK'S SIDE", tag="RBI | PROVISIONING RULES", items=[
    b,
    dict(kind="arrow", x=700, y=560, to=[300, 0], bend=-0.15, color="red", at=P("C014", "also a loss")),
    dict(kind="label", x=1010, y=470, text="A LOSS FOR THE BANK", size=58, color="red", at=P("C014", "loss for")),
    dict(kind="box", x=1080, y=600, w=520, h=260, text="BANK'S PROFIT", sub="", at=P("C015", "from its own"), dur=0.6),
    dict(kind="coins", x=1210, y=560, n=4, r=70, color="red", text="25%", textColor="red", in_="pop", at=P("C015", "a quarter"),
         moves=[dict(at=P("C015", "from its own") + 0.4, x=1340, y=780, s=0.9, dur=0.8)]),
    dict(kind="label", x=1010, y=380, text="SET ASIDE ≥ 25% OF WHAT YOU OWE", size=40, mono=True, color="ink", at=P("C015", "keep aside")),
    dict(kind="meter", x=1700, y=330, s=0.55, text="PRESSURE", needle=[[0, -70], [P("C015", "pressure"), 60, 1.2]], at=P("C015", "That is one")),
])

# C016 But listen carefully. Some people say interest stops after ninety days. No rule says that.
# C017 The bank cannot count your unpaid interest as its income. But your bill can keep growing as per your card terms.
b = photo("bill_ravi", 1150, 150, 520, L("C017")[0] - 0.1, float=0.5)
SCENES["p05_myth"] = dict(kind="page", start=L("C016")[0] - 0.25, end=L("C018")[0] - 0.2, kicker="MYTH VS RULE", tag="RBI | IRAC NORMS · CARD TERMS", items=[
    *page([
        dict(kind="sticky", x=700, y=330, w=520, h=300, n="?", lines=["Interest stops", "after 90 days"], color="dim", at=P("C016", "Some people")),
        dict(kind="stamp", x=960, y=520, text="MYTH", size=110, rot=-10, in_="stamp", at=P("C016", "No rule")),
    ], L("C017")[0] - 0.35),
    dict(kind="label", x=140, y=380, text="BANK'S BOOKS", size=34, mono=True, color="dim", at=P("C017", "The bank cannot")),
    dict(kind="label", x=140, y=470, text="unpaid interest", size=64, at=P("C017", "unpaid interest")),
    dict(kind="label", x=140, y=550, text="≠ income", size=64, color="red", at=P("C017", "income")),
    b,
    dict(kind="bars", x=760, y=930, w=70, bars=[dict(x=k * 95, h=h, color="red") for k, h in enumerate((90, 130, 175, 225))],
         grow=[P("C017", "keep growing") + k * 0.18 for k in range(4)], at=P("C017", "keep growing") - 0.1, in_="fade"),
    dict(kind="label", x=760, y=1010, text="YOUR BILL KEEPS GROWING", size=40, color="red", at=P("C017", "card terms")),
])

# C018 There is a second clock too. Your CIBIL. Banks now update the credit bureaus every fifteen days.
# C019 The good part is, the bank must tell you before it reports you as a defaulter. And if you have a genuine dispute, it must wait.
rp = photo("report_ravi", 140, 120, 600, P("C018", "Your CIBIL") - 0.15, float=0.4)
nt = photo("notice_prior", 150, 110, 610, P("C019", "tell you") - 0.15, float=0.4)
SCENES["p06_cibil"] = dict(kind="page", start=L("C018")[0] - 0.25, end=L("C020")[0] - 0.2, kicker="THE SECOND CLOCK", tag="RBI | FROM 1 JAN 2025", items=[
    *page([
        rp,
        ring(rp, "acct0", P("C018", "Your CIBIL") + 0.6, pad=1.05, color="red"),
        dict(kind="calendar", x=930, y=230, s=1.15, title="EVERY MONTH", days=30, at=P("C018", "update"),
             marks=[dict(day=15, color="red", text="UPDATE"), dict(day=30, color="red", text="UPDATE")]),
        dict(kind="label", x=1320, y=180, text="EVERY 15 DAYS", size=64, anchor="middle", hl="yel", at=P("C018", "every fifteen")),
    ], L("C019")[0] - 0.3),
    nt,
    dict(kind="badge", x=920, y=330, text="TELL YOU FIRST", at=P("C019", "before it reports")),
    dict(kind="sticky", x=880, y=560, w=420, h=230, n="!", lines=["Genuine dispute"], color="blue", at=P("C019", "genuine dispute")),
    dict(kind="badge", x=1400, y=680, text="BANK MUST WAIT", at=P("C019", "it must wait")),
])

# C021 And the card itself? At SBI Card, for example, it may be blocked from the very first missed payment.
c = photo("card_navy", 560, 260, 800, L("C021")[0] - 0.1, float=0.8)
SCENES["p07_blocked"] = dict(kind="page", start=L("C021")[0] - 0.25, end=L("C022")[0] - 0.2, kicker="THE CARD ITSELF", tag="SBI CARD | FAQ", items=[
    c,
    dict(kind="stamp", x=960, y=560, text="BLOCKED", size=120, rot=-9, in_="stamp", at=P("C021", "blocked")),
    dict(kind="label", x=960, y=960, text="FROM THE FIRST MISSED PAYMENT", size=52, anchor="middle", hl="yel", at=P("C021", "very first")),
])

# C022–C030 Ravi and Sunita (OUR CALCULATION, tools/cpm_math.py: HDFC late-fee slabs, 3.75% a month, 18% GST)
gr = {p: [round(M.grow(p, m)["total"]) for m in range(7)] for p in (10000, 100000)}
r6, s6 = M.grow(10000, 6), M.grow(100000, 6)
fee_share = (r6["fees"] * 1.18) / r6["extra"]            # late fees + their GST, share of Ravi's 6-month jump (0.68)
br = photo("bill_ravi", 150, 210, 520, P("C023", "Ravi") - 0.15)
bs = photo("bill_sunita", 1250, 210, 520, P("C023", "Sunita") - 0.15)
t_late = P("C025", "seven hundred")
t_1300 = P("C025", "thirteen hundred")
n_r = dict(kind="label", x=round(br["x"] + br["w"] / 2), y=170, text="RAVI · ₹10,000", size=52, anchor="middle", color="blue", at=P("C023", "Ravi"))
n_s = dict(kind="label", x=round(bs["x"] + bs["w"] / 2), y=170, text="SUNITA · ₹1 LAKH", size=52, anchor="middle", color="red", at=P("C023", "Sunita"))
SCENES["p08_ravi_sunita"] = dict(kind="page", start=L("C022")[0] - 0.25, end=L("C031")[0] - 0.2, kicker="SMALL BILL VS BIG BILL", tag="OUR CALCULATION · HDFC BANK MITC | OCT 2026", items=[
    *page([dict(kind="label", x=960, y=560, text="A SMALL BILL GROWS FASTER", size=92, anchor="middle", hl="yel", at=P("C022", "A small bill"))],
          L("C023")[0] - 0.35),
    *page([
        br, bs, n_r, n_s,
        dict(kind="stamp", x=round(an(br, "center")[0]), y=round(an(br, "row1")[1]), text="NOT PAID", size=56, rot=-8, in_="stamp", at=P("C023", "Both stop")),
        dict(kind="stamp", x=round(an(bs, "center")[0]), y=round(an(bs, "row1")[1]), text="NOT PAID", size=56, rot=-8, in_="stamp", at=P("C023", "Both stop") + 0.15),
        dict(kind="label", x=960, y=420, text="SAME", size=60, anchor="middle", at=P("C024", "same interest")),
        dict(kind="label", x=960, y=500, text="3.75% a month", size=46, anchor="middle", color="ink", at=P("C024", "Three point")),
        dict(kind="label", x=960, y=570, text="+ 18% GST", size=46, anchor="middle", color="ink", at=P("C024", "eighteen percent")),
        ring(br, "row2", P("C025", "fixed amount"), pad=1.06, color="red"),
        ring(bs, "row2", P("C025", "fixed amount") + 0.1, pad=1.06, color="red"),
        dict(kind="label", x=960, y=700, text="LATE FEE = FIXED SLAB", size=42, anchor="middle", color="red", at=P("C025", "fixed amount")),
        dict(kind="tag", x=round(an(br, "amt2")[0] - 60), y=round(an(br, "row2")[1] + 70), text="₹750", color="red", at=t_late),
        dict(kind="tag", x=round(an(bs, "amt2")[0] - 120), y=round(an(bs, "row2")[1] + 70), text="₹1,300", color="red", at=t_1300),
        dict(kind="label", x=round(br["x"] + br["w"] / 2), y=1010, text="7.5% A MONTH", size=66, anchor="middle", hl="yel", color="red", at=P("C026", "seven and a half")),
        dict(kind="label", x=round(bs["x"] + bs["w"] / 2), y=1010, text="1.3% A MONTH", size=66, anchor="middle", color="blue", at=P("C026", "one point three")),
    ], L("C027")[0] - 0.45),
    # C027–C030: six months later (1.5 s of silence before C027 in the mix)
    dict(kind="label", x=960, y=150, text="AFTER 6 MONTHS · NOTHING PAID", size=40, mono=True, anchor="middle", color="dim", at=L("C027")[0] - 0.1),
    dict(kind="counter", x=480, y=430, size=130, anchor="middle", from_=10000, label="RAVI", labelColor="blue", at=L("C027")[0],
         steps=[[P("C027", "becomes") - 0.3 + k * 0.45, v, 0.4] for k, v in enumerate(gr[10000][1:])]),
    dict(kind="label", x=480, y=600, text="ALMOST DOUBLE", size=56, anchor="middle", hl="yel", color="red", at=P("C027", "Almost double")),
    dict(kind="counter", x=1440, y=430, size=130, anchor="middle", from_=100000, label="SUNITA", labelColor="red", at=L("C028")[0] - 0.1,
         steps=[[P("C028", "becomes") - 0.2 + k * 0.4, v, 0.36] for k, v in enumerate(gr[100000][1:])]),
    dict(kind="label", x=1440, y=600, text=f"+{round(100 * s6['extra'] / 100000)}%", size=56, anchor="middle", color="blue", at=P("C028", "thirty eight")),
    dict(kind="split", x=510, y=760, w=900, h=100, at=P("C029", "two thirds") - 0.1, dur=0.9,
         parts=[dict(f=round(fee_share, 3), color="red", label="LATE FEES + GST", top="2/3"), dict(f=round(1 - fee_share, 3), color="dim", label="INTEREST + GST")]),
    dict(kind="label", x=960, y=700, text=f"RAVI'S EXTRA {M.inr(r6['extra'])}", size=34, mono=True, anchor="middle", color="dim", at=P("C029", "For Ravi")),
    dict(kind="label", x=960, y=1010, text="SMALLER BILL, HARDER HIT", size=56, anchor="middle", hl="yel", at=P("C029", "the smaller")),
    dict(kind="label", x=60, y=1040, text="OUR CALCULATION · ONE BANK'S FEES · YOUR BILL WILL DIFFER", size=26, mono=True, color="dim", at=P("C030", "our own")),
])
