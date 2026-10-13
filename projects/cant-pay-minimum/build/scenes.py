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
    dict(kind="stamp", x=round(an(b, "center")[0] + 10), y=round(an(b, "center")[1] + 40), text="NPA · DAY 91", size=58, rot=-12, in_="stamp", at=t_npa),
    dict(kind="loop", x=1295, y=470, r=200, color="blue", at=P("C012", "checks"), spin=[[0, 0], [P("C012", "checks"), 0, 0.01], [P("C012", "checks") + 0.05, 360, 3.0]], exit=P("C013", "If the") - 0.1),
    dict(kind="label", x=1295, y=300, text="CHECKED EVERY DAY", size=40, mono=True, anchor="middle", color="blue", at=P("C012", "every single"), exit=P("C013", "If the") - 0.1),
    dict(kind="label", x=1295, y=960, text="BAD LOAN = NPA", size=64, anchor="middle", hl="yel", at=P("C013", "NPA")),
    dict(kind="label", x=1295, y=1030, text="NON-PERFORMING ASSET", size=30, mono=True, anchor="middle", color="dim", at=P("C013", "non performing")),
], sfx=[[P("C012", "every single") + k * 0.25, "tick"] for k in range(8)])

# C014 Now here is something most people don't know. From that day, your unpaid card is also a loss for the bank.
# C015 The bank must keep aside at least a quarter of what you owe, from its own profit. That is one reason the pressure
#      grows around this time.
b = photo("bill_ravi_overdue", 120, 190, 520, L("C014")[0] - 0.1, float=0.5)
stacks = [dict(kind="coins", x=x, y=700, n=6, r=70, color="amber", in_="pop", at=L("C015")[0] + 0.1 * k) for k, x in enumerate((330, 520, 710, 900))]
SCENES["p04_provision"] = dict(kind="page", start=L("C014")[0] - 0.25, end=L("C016")[0] - 0.2, kicker="THE BANK'S SIDE", tag="RBI | PROVISIONING RULES", items=[
    *page([
        b,
        dict(kind="house", x=1290, y=250, s=1.15, text="YOUR BANK", at=P("C014", "something most")),
        dict(kind="arrow", x=700, y=520, to=[540, 0], bend=-0.12, color="red", at=P("C014", "also a loss") - 0.2),
        dict(kind="label", x=1460, y=780, text="A LOSS FOR THE BANK", size=60, anchor="middle", color="red", at=P("C014", "loss for")),
    ], L("C015")[0] - 0.35),
    *stacks,
    dict(kind="label", x=615, y=820, text="WHAT YOU OWE", size=34, mono=True, anchor="middle", color="dim", at=L("C015")[0] + 0.2),
    dict(kind="label", x=1400, y=420, text="SET ASIDE FROM PROFIT", size=40, mono=True, anchor="middle", at=P("C015", "keep aside")),
    dict(kind="box", x=1220, y=470, w=360, h=250, text=" ", at=P("C015", "keep aside"), dur=0.6),
    dict(kind="coins", x=900, y=700, n=6, r=70, color="red", text="25%", textColor="red", in_="pop", at=P("C015", "a quarter"),
         moves=[dict(at=P("C015", "from its own"), x=1400, y=690, dur=0.8)]),
    dict(kind="label", x=1400, y=820, text="AT LEAST A QUARTER", size=46, anchor="middle", hl="yel", at=P("C015", "a quarter") + 0.3),
    dict(kind="meter", x=1720, y=1000, s=0.42, text="PRESSURE", needle=[[0, -70], [P("C015", "pressure"), 60, 1.2]], at=P("C015", "That is one")),
])

# C016 But listen carefully. Some people say interest stops after ninety days. No rule says that.
# C017 The bank cannot count your unpaid interest as its income. But your bill can keep growing as per your card terms.
b = photo("bill_ravi", 1150, 150, 520, L("C017")[0] - 0.1, float=0.5)
SCENES["p05_myth"] = dict(kind="page", start=L("C016")[0] - 0.25, end=L("C018")[0] - 0.2, kicker="MYTH VS RULE", tag="RBI | IRAC NORMS · CARD TERMS", items=[
    *page([
        dict(kind="label", x=960, y=290, text="SOME PEOPLE SAY", size=40, mono=True, anchor="middle", color="dim", at=P("C016", "listen") - 0.2),
        dict(kind="sticky", x=700, y=330, w=520, h=300, n="", lines=["Interest stops", "after 90 days"], color="dim", at=P("C016", "Some people")),
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
rp = photo("report_ravi", 140, 120, 600, L("C018")[0] - 0.2, float=0.4)
nt = photo("notice_prior", 150, 110, 610, L("C019")[0] - 0.2, float=0.4)
SCENES["p06_cibil"] = dict(kind="page", start=L("C018")[0] - 0.25, end=L("C020")[0] - 0.2, kicker="THE SECOND CLOCK", tag="RBI | FROM 1 JAN 2025", items=[
    *page([
        rp,
        ring(rp, "acct0", P("C018", "Your CIBIL") + 0.6, pad=1.05, color="red"),
        dict(kind="calendar", x=930, y=230, s=1.15, title="EVERY MONTH", days=30, at=P("C018", "update"),
             marks=[dict(day=15, color="red"), dict(day=30, color="red")]),
        dict(kind="label", x=1320, y=180, text="EVERY 15 DAYS", size=64, anchor="middle", hl="yel", at=P("C018", "every fifteen")),
    ], L("C019")[0] - 0.3),
    nt,
    dict(kind="badge", x=920, y=330, text="TELL YOU FIRST", at=P("C019", "before it reports")),
    dict(kind="sticky", x=880, y=560, w=420, h=230, n="!", lines=["Genuine dispute"], color="blue", at=P("C019", "genuine dispute")),
    dict(kind="badge", x=920, y=880, text="BANK MUST WAIT", at=P("C019", "it must wait")),
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
br = photo("bill_ravi", 150, 210, 520, L("C022")[0] - 0.2)
bs = photo("bill_sunita", 1250, 210, 520, L("C022")[0] - 0.05)
t_late = P("C025", "seven hundred")
t_1300 = P("C025", "thirteen hundred")
n_r = dict(kind="label", x=round(br["x"] + br["w"] / 2), y=180, text="RAVI · ₹10,000", size=52, anchor="middle", color="blue", at=P("C023", "Ravi"))
n_s = dict(kind="label", x=round(bs["x"] + bs["w"] / 2), y=180, text="SUNITA · ₹1 LAKH", size=52, anchor="middle", color="red", at=P("C023", "Sunita"))
SCENES["p08_ravi_sunita"] = dict(kind="page", start=L("C022")[0] - 0.25, end=L("C031")[0] - 0.2, kicker="SMALL BILL VS BIG BILL", tag="OUR CALCULATION · HDFC BANK MITC | OCT 2026", items=[
        dict(kind="label", x=960, y=120, text="A SMALL BILL GROWS FASTER", size=64, anchor="middle", hl="yel", at=P("C022", "A small bill"), exit=P("C023", "Ravi") - 0.2),
    *page([
        br, bs, n_r, n_s,
        dict(kind="stamp", x=round(an(br, "center")[0]), y=round(an(br, "row4")[1] + 130), text="NOT PAID", size=56, rot=-8, in_="stamp", at=P("C023", "Both stop")),
        dict(kind="stamp", x=round(an(bs, "center")[0]), y=round(an(bs, "row4")[1] + 130), text="NOT PAID", size=56, rot=-8, in_="stamp", at=P("C023", "Both stop") + 0.15),
        dict(kind="label", x=960, y=330, text="SAME", size=60, anchor="middle", at=P("C024", "same interest")),
        dict(kind="label", x=960, y=405, text="3.75% a month", size=46, anchor="middle", color="ink", at=P("C024", "Three point")),
        dict(kind="label", x=960, y=470, text="+ 18% GST", size=46, anchor="middle", color="ink", at=P("C024", "eighteen percent")),
        ring(br, "row2", P("C025", "fixed amount"), pad=1.06, color="red"),
        ring(bs, "row2", P("C025", "fixed amount") + 0.1, pad=1.06, color="red"),
        dict(kind="label", x=960, y=840, text="LATE FEE = FIXED SLAB", size=42, anchor="middle", color="red", at=P("C025", "fixed amount")),
        dict(kind="tag", x=round(br["x"] + br["w"] - 40), y=round(an(br, "row2")[1] - 48), text="₹750", color="red", at=t_late),
        dict(kind="tag", x=round(bs["x"] - 360), y=round(an(bs, "row2")[1] - 48), text="₹1,300", color="red", at=t_1300),
        dict(kind="label", x=round(br["x"] + br["w"] / 2), y=950, text="7.5% A MONTH", size=62, anchor="middle", hl="yel", color="red", at=P("C026", "seven and a half")),
        dict(kind="label", x=round(bs["x"] + bs["w"] / 2), y=950, text="1.3% A MONTH", size=62, anchor="middle", color="blue", at=P("C026", "one point three")),
    ], L("C027")[0] - 0.45),
    # C027–C030: six months later (1.5 s of silence before C027 in the mix)
    dict(kind="label", x=960, y=150, text="AFTER 6 MONTHS · NOTHING PAID", size=40, mono=True, anchor="middle", color="dim", at=L("C027")[0] - 0.1),
    dict(kind="counter", x=480, y=430, size=130, anchor="middle", from_=10000, label="RAVI", labelColor="blue", at=L("C027")[0],
         steps=[[P("C027", "becomes") - 0.3 + k * 0.45, v, 0.4] for k, v in enumerate(gr[10000][1:])]),
    dict(kind="label", x=480, y=600, text="ALMOST DOUBLE", size=56, anchor="middle", hl="yel", color="red", at=P("C027", "Almost double")),
    dict(kind="counter", x=1440, y=430, size=130, anchor="middle", from_=100000, label="SUNITA", labelColor="red", at=L("C028")[0] - 0.1,
         steps=[[P("C028", "becomes") - 0.2 + k * 0.4, v, 0.36] for k, v in enumerate(gr[100000][1:])]),
    dict(kind="label", x=1440, y=600, text=f"+{round(100 * s6['extra'] / 100000)}%", size=56, anchor="middle", color="blue", at=P("C028", "thirty eight")),
    dict(kind="split", x=510, y=700, w=900, h=100, at=P("C029", "two thirds") - 0.1, dur=0.9,
         parts=[dict(f=round(fee_share, 3), color="red", label="2/3 · LATE FEES + GST"), dict(f=round(1 - fee_share, 3), color="dim", label="INTEREST + GST")]),
    dict(kind="label", x=960, y=665, text=f"RAVI'S EXTRA {M.inr(r6['extra'])}", size=34, mono=True, anchor="middle", color="dim", at=P("C029", "For Ravi")),
    dict(kind="label", x=960, y=960, text="SMALLER BILL, HARDER HIT", size=56, anchor="middle", hl="yel", at=P("C029", "the smaller")),
    dict(kind="label", x=60, y=1040, text="OUR CALCULATION · ONE BANK'S FEES · YOUR BILL WILL DIFFER", size=26, mono=True, color="dim", at=P("C030", "our own")),
])


# =====================================================================================================================
# ACT 2b: who comes after you, the agency business, distance, court, the slab walk
import json as _json                     # noqa: E402
MAP = _json.loads((Path(__file__).parent / "map_aptg.json").read_text())
CITY = MAP["cities"]

# C031 Now the real question. Who actually comes after you? And will anyone come to your house?
t_who = P("C031", "Who actually")
SCENES["d02_call"] = dict(kind="desk", start=L("C031")[0] - 0.25, end=L("C032")[0] - 0.2, tag="SIMULATION", layers=[dict(src="deskB_call", at=0)],
    cam=[[0, 1.0, 0, 0], *push(L("C031")[0], L("C032")[0], 1.18, pa("deskB_call", "phone:center"))],
    shake=[[L("C031")[0] + k * 1.1, 0.42, 6] for k in range(5)], sfx=[[L("C031")[0] + k * 1.1, "buzz"] for k in range(5)],
    lower=[dict(at=P("C031", "will anyone"), k="THE REAL QUESTION", t="Will anyone come home?")])

# C033 Banks decide how hard to chase by two things. The days you are late, and the money at risk.
SCENES["p09_dials"] = dict(kind="page", start=L("C033")[0] - 0.25, end=L("C034")[0] - 0.2, kicker="HOW HARD THEY CHASE", tag="RBL BANK | COLLECTION POLICY", items=[
    dict(kind="label", x=960, y=200, text="HOW HARD THEY CHASE", size=56, anchor="middle", at=L("C033")[0] - 0.2),
    dict(kind="meter", x=600, y=640, s=1.15, text="DAYS LATE", needle=[[0, -80], [P("C033", "days you are") + 0.2, 55, 1.2]], at=L("C033")[0] - 0.2),
    dict(kind="meter", x=1320, y=640, s=1.15, text="MONEY AT RISK", needle=[[0, -80], [P("C033", "money at risk") + 0.2, 55, 1.2]], at=L("C033")[0] - 0.1),
    dict(kind="label", x=960, y=640, text="+", size=110, anchor="middle", at=P("C033", "and the")),
])

# C034 After that, many banks hand your account to a recovery agency. And here is the business behind it.
# C035 Many agencies earn only when they collect. A percentage of what you pay. One public sector bank pays its agencies
#      between seven and a half and fifteen percent on accounts up to one lakh.        (assemble.py: PNB proof over the slab line)
# C036 Now see it from their side. If you owe ten thousand, the agency may earn about a thousand rupees. And only if you pay in full.
bl = photo("bill_ravi_overdue", 120, 200, 470, L("C034")[0] - 0.2, float=0.4)
af = photo("agency_file", 1270, 170, 520, P("C034", "recovery agency") - 0.2, float=0.4)
SCENES["p10_agency"] = dict(kind="page", start=L("C034")[0] - 0.25, end=L("C037")[0] - 0.2, kicker="THE BUSINESS BEHIND IT", tag="PNB | RECOVERY AGENT POLICY", items=[
    *page([
        bl, af,
        dict(kind="arrow", x=640, y=540, to=[580, 0], bend=-0.1, color="red", at=P("C034", "hand your account")),
        dict(kind="label", x=930, y=470, text="HANDED OVER", size=44, anchor="middle", color="red", at=P("C034", "hand your account") + 0.2),
        dict(kind="label", x=930, y=700, text="PAID ONLY WHEN THEY COLLECT", size=38, mono=True, anchor="middle", at=P("C035", "earn only")),
        dict(kind="label", x=930, y=820, text="7.5% – 15%", size=110, anchor="middle", hl="yel", color="red", at=P("C035", "seven and a half")),
        dict(kind="label", x=930, y=890, text="ONE PUBLIC SECTOR BANK · UP TO ₹1 LAKH", size=28, mono=True, anchor="middle", color="dim", at=P("C035", "on accounts")),
    ], L("C036")[0] - 0.35),
    dict(kind="label", x=960, y=170, text="SEE IT FROM THEIR SIDE", size=44, mono=True, anchor="middle", color="dim", at=L("C036")[0] - 0.2),
    dict(kind="coins", x=560, y=720, n=10, r=95, color="amber", label="YOU OWE ₹10,000", labelColor="ink", at=P("C036", "If you owe"), dur=0.8),
    dict(kind="coins", x=560, y=720 - 9 * 14, n=1, r=95, color="red", in_="pop", at=P("C036", "the agency may"),
         moves=[dict(at=P("C036", "earn about") , x=1300, y=640, s=1.3, dur=0.8)]),
    dict(kind="label", x=1300, y=500, text="≈ ₹1,000", size=96, anchor="middle", color="red", at=P("C036", "a thousand rupees")),
    dict(kind="label", x=1300, y=820, text="FOR THE AGENCY", size=40, mono=True, anchor="middle", at=P("C036", "a thousand rupees") + 0.2),
    dict(kind="badge", x=1150, y=930, ok=False, text="ONLY IF PAID IN FULL", size=44, at=P("C036", "only if you pay")),
    dict(kind="label", x=60, y=1040, text="OUR ESTIMATE", size=26, mono=True, color="dim", at=P("C036", "may earn")),
])

# C037 Now think about where you live. Say your card has your old room address in the city. But your family lives in a village, far away.
# C038 Agencies usually work city by city, or district by district. In Andhra and Telangana, one card company's agency list
#      names just six places. Hyderabad, Warangal, Karimnagar, Vizag, Vijayawada and Tirupati.
# C039 For a small amount, a long trip to a far village rarely pays for itself. So small dues mostly stay as calls and
#      messages. That's not a rule. It's simple business.
# C040 For bigger amounts, it changes. Finding a person who moved is a paid job. One bank pays seven thousand five hundred
#      rupees for each person traced. That's worth it only when the amount is big.
hx, hy = CITY["Hyderabad"]; vx, vy = CITY["village"]
six = [("Hyderabad", "Hyderabad"), ("Warangal", "Warangal"), ("Karimnagar", "Karimnagar"), ("Vizag", "Vizag"), ("Vijayawada", "Vijayawada"), ("Tirupati", "Tirupati")]
SCENES["p11_map"] = dict(kind="page", start=L("C037")[0] - 0.25, end=L("C041")[0] - 0.2, kicker="WHERE YOU LIVE", tag="ONECARD | REPAYMENT AGENCIES LIST", items=[
    dict(kind="path", d=MAP["states"]["Telangana"], fill="#cfd6e4", label="TELANGANA", lx=1270, ly=240, at=L("C037")[0] - 0.2, dur=1.2),
    dict(kind="path", d=MAP["states"]["Andhra Pradesh"], fill="#e9dcc3", label="ANDHRA PRADESH", lx=1530, ly=660, at=L("C037")[0] + 0.3, dur=1.4),
    dict(kind="pin", x=round(hx), y=round(hy), color="blue", at=P("C037", "old room")),
    dict(kind="label", x=round(hx - 40), y=round(hy - 30), text="CARD ADDRESS", size=30, mono=True, anchor="end", color="blue", at=P("C037", "old room") + 0.1),
    dict(kind="house", x=round(vx - 75), y=round(vy - 150), s=0.5, text="FAMILY · VILLAGE", at=P("C037", "village")),
    dict(kind="dash", x=round(hx), y=round(hy + 10), to=[round(vx - hx), round(vy - hy - 160)], bend=0.12, color="red", text="FAR AWAY", tx=-110, at=P("C037", "far away")),
    dict(kind="label", x=120, y=330, text="AGENCIES WORK", size=44, mono=True, at=P("C038", "Agencies usually")),
    dict(kind="label", x=120, y=410, text="CITY BY CITY", size=64, at=P("C038", "city by city")),
    dict(kind="label", x=120, y=560, text="ONE CARD COMPANY'S LIST:", size=32, mono=True, color="dim", at=P("C038", "agency list")),
    dict(kind="label", x=120, y=650, text="6 PLACES", size=110, color="red", at=P("C038", "six places")),
    *[dict(kind="pin", x=round(CITY[c][0]), y=round(CITY[c][1]), color="red", text=c.upper(), at=P("C038", w)) for c, w in six if c != "Hyderabad"],
    dict(kind="ring", x=round(hx), y=round(hy - 40), w=150, h=150, color="red", at=P("C038", "Hyderabad")),
    dict(kind="label", x=120, y=830, text="SMALL DUES:", size=34, mono=True, color="dim", at=P("C039", "For a small")),
    dict(kind="label", x=120, y=910, text="CALLS AND MESSAGES", size=56, color="blue", at=P("C039", "calls and messages")),
    dict(kind="label", x=120, y=980, text="OUR ESTIMATE · NOT A RULE", size=28, mono=True, color="dim", at=P("C039", "not a rule")),
    dict(kind="tag", x=round(vx + 40), y=round(vy + 40), text="₹7,500", sub="PER PERSON TRACED", color="red", at=P("C040", "seven thousand")),
    dict(kind="ring", x=round(vx), y=round(vy - 60), w=230, h=230, color="red", at=P("C040", "Finding a person")),
])

# C041 What about court? Here again, the amount decides.
# C042 To file a case, the bank pays court fees and a lawyer. On a small amount, that eats a big part of what it can recover.
#      So a court case for ten thousand rarely makes sense for the bank.
# C043 For bigger dues, card companies do use Lok Adalat. You get a notice for a settlement meeting, usually in your own city.
#      In one real case, SBI Card took about one point eight lakh of card dues to a Lok Adalat in the customer's city, Indore.
# C044 If you get such a notice, go. It is a chance to settle with a written record.
# C045 Some banks use arbitration. Be careful here. In the Delhi High Court, one bank admitted about seventy six thousand awards
#      where the bank alone picked the arbitrator. The court said such an award is void and cannot be enforced. The bank can
#      still try to recover in the proper way.
# C046 And the special bank tribunal, the DRT, is only for dues of twenty lakh rupees or more. For most card dues, it is not even possible.
ln = photo("notice_lokadalat", 160, 120, 600, L("C043")[0] - 0.2, float=0.4)
aw = photo("award", 160, 120, 600, L("C045")[0] - 0.2, float=0.4)
cd = photo("card_navy", 1180, 380, 560, L("C046")[0] - 0.1, float=0.6)
SCENES["p12_court"] = dict(kind="page", start=L("C041")[0] - 0.25, end=L("C047")[0] - 0.2, kicker="WHAT ABOUT COURT?", tag="", items=[
    *page([
        dict(kind="label", x=960, y=180, text="THE AMOUNT DECIDES", size=60, anchor="middle", hl="yel", at=P("C041", "the amount")),
        dict(kind="scale", x=960, y=430, s=1.1, at=L("C041")[0] - 0.2, dur=0.9,
             left=["COURT FEE + LAWYER", "WHAT IT COSTS", "red"], right=["₹10,000", "WHAT IT CAN RECOVER", "blue"],
             tilt=[[0, 0], [P("C042", "court fees") + 0.3, -9, 0.8], [P("C042", "eats a big"), -13, 0.6]]),
        dict(kind="label", x=960, y=980, text="A COURT CASE FOR ₹10,000 RARELY MAKES SENSE", size=44, anchor="middle", color="red", at=P("C042", "rarely makes")),
    ], L("C043")[0] - 0.35),
    *page([
        ln,
        dict(kind="label", x=900, y=360, text="BIGGER DUES:", size=34, mono=True, color="dim", at=L("C043")[0]),
        dict(kind="label", x=900, y=450, text="LOK ADALAT", size=84, at=P("C043", "Lok Adalat")),
        dict(kind="pin", x=1000, y=640, color="blue", text="YOUR OWN CITY", at=P("C043", "your own city")),
        dict(kind="label", x=900, y=780, text="SBI CARD · ₹1.8 LAKH · INDORE", size=40, mono=True, at=P("C043", "In one real case")),
        dict(kind="badge", x=950, y=930, text="GO. SETTLE ON RECORD", size=48, at=P("C044", "go")),
    ], L("C045")[0] - 0.35),
    *page([
        aw,
        dict(kind="label", x=900, y=330, text="ARBITRATION", size=72, at=L("C045")[0] - 0.1),
        dict(kind="label", x=900, y=430, text="ABOUT 76,000 AWARDS", size=56, color="red", at=P("C045", "seventy six")),
        dict(kind="label", x=900, y=490, text="ARBITRATOR PICKED BY THE BANK ALONE", size=30, mono=True, color="dim", at=P("C045", "picked the")),
        dict(kind="stamp", x=round(an(aw, "center")[0]), y=round(an(aw, "center")[1] + 60), text="VOID", size=150, rot=-12, in_="stamp", at=P("C045", "void")),
        dict(kind="label", x=900, y=640, text="CANNOT BE ENFORCED", size=52, at=P("C045", "cannot be")),
        dict(kind="label", x=900, y=760, text="IT CAN STILL RECOVER THE PROPER WAY", size=30, mono=True, color="dim", at=P("C045", "still try")),
    ], L("C046")[0] - 0.35),
    dict(kind="label", x=140, y=300, text="DEBT RECOVERY TRIBUNAL", size=40, mono=True, color="dim", at=L("C046")[0] - 0.1),
    dict(kind="label", x=140, y=420, text="DRT", size=150, at=P("C046", "DRT")),
    dict(kind="label", x=140, y=560, text="₹20 LAKH OR MORE", size=72, hl="yel", color="red", at=P("C046", "twenty lakh")),
    cd,
    dict(kind="cross", x=1460, y=560, size=360, at=P("C046", "not even possible")),
    dict(kind="label", x=1460, y=900, text="MOST CARD DUES", size=44, anchor="middle", at=P("C046", "For most")),
])

# C047 So here is my practical reading, slab by slab. No bank publishes this.
# C048 Around ten thousand. Calls and messages, a blocked card and a bad mark on your CIBIL. A court case is unlikely, but the mark stays with you for years.
# C049 Fifty thousand to one lakh. Calls, then an agency, maybe a visit if you live in a city they cover, and settlement or Lok Adalat notices.
# C050 Two to five lakh. Expect field visits, people tracing you if you moved, and legal notices.
# C051 Ten lakh and above. A court case becomes worth the bank's money. Take it seriously from day one.
def chips(line, items, x=1180, y0=250, dy=118, out=None):
    return [dict(at=P(line, w), out=out, x=x, y=y0 + k * dy, text=t, color=c) for k, (w, t, c) in enumerate(items)]


s0, s1, s2, s3 = (L(c)[0] for c in ("C048", "C049", "C050", "C051"))
SCENES["d03_slabs"] = dict(kind="desk", start=L("C047")[0] - 0.25, end=L("C052")[0] - 0.2, tag="OUR ESTIMATE · NO BANK PUBLISHES THIS", layers=[
    dict(src="slab_all", at=0), dict(src="slab0", at=s0 - 0.3, fade=0.5), dict(src="slab1", at=s1 - 0.3, fade=0.5),
    dict(src="slab2", at=s2 - 0.3, fade=0.5), dict(src="slab3", at=s3 - 0.3, fade=0.5),
], cam=[[0, 1.0, 0, 0], *push(0.0, s0 - 0.3, 1.06, (960, 540)),
        *push(s0 - 0.3, s1 - 0.3, 1.08, (760, 560)), *push(s1 - 0.3, s2 - 0.3, 1.08, (760, 560)),
        *push(s2 - 0.3, s3 - 0.3, 1.08, (760, 560)), *push(s3 - 0.3, L("C052")[0], 1.1, (760, 560))],
   lower=[dict(at=L("C047")[0], out=s0 - 0.3, k="MY PRACTICAL READING", t="Slab by slab"),
          dict(at=s0, out=s1 - 0.3, k="SLAB 1", t="Around ₹10,000"), dict(at=s1, out=s2 - 0.3, k="SLAB 2", t="₹50,000 to ₹1 lakh"),
          dict(at=s2, out=s3 - 0.3, k="SLAB 3", t="₹2 to ₹5 lakh"), dict(at=s3, k="SLAB 4", t="₹10 lakh and above")],
   chips=[*chips("C048", [("Calls and", "CALLS AND SMS", "#2563eb"), ("a blocked", "CARD BLOCKED", "#d62839"), ("bad mark", "CIBIL MARK FOR YEARS", "#d62839"),
                          ("court case is unlikely", "COURT: UNLIKELY", "#1f9d6b")], out=s1 - 0.3),
          *chips("C049", [("then an agency", "CALLS, THEN AN AGENCY", "#2563eb"), ("maybe a visit", "VISIT IF IN THEIR CITY", "#e09f1f"),
                          ("settlement", "LOK ADALAT NOTICES", "#d62839")], out=s2 - 0.3),
          *chips("C050", [("field visits", "FIELD VISITS", "#e09f1f"), ("tracing", "TRACING IF YOU MOVED", "#d62839"), ("legal notices", "LEGAL NOTICES", "#d62839")], out=s3 - 0.3),
          *chips("C051", [("court case", "COURT CASE: WORTH IT", "#d62839"), ("Take it seriously", "ACT FROM DAY ONE", "#1f9d6b")])],
   sfx=[[t, "whoosh"] for t in (s0 - 0.3, s1 - 0.3, s2 - 0.3, s3 - 0.3)])

# C052 Remember, these slabs are about what you owe to one bank. Other banks don't add it up. They only see it on your CIBIL.
cs = [photo(n, x, 190, 400, L("C052")[0] - 0.2 + k * 0.12, float=0.8) for k, (n, x) in enumerate((("card_black", 120), ("card_navy", 760), ("card_maroon", 1400)))]
rp2 = photo("report_ravi", 800, 560, 320, P("C052", "They only see") - 0.35)
SCENES["p13_per_bank"] = dict(kind="page", start=L("C052")[0] - 0.25, end=L("C053")[0] - 0.2, kicker="ONE BANK AT A TIME", tag="", items=[
    dict(kind="label", x=960, y=130, text="SLABS ARE PER BANK", size=60, anchor="middle", hl="yel", at=L("C052")[0] - 0.2),
    *cs,
    *[dict(kind="label", x=c["x"] + 200, y=500, text=t, size=34, mono=True, anchor="middle", at=c["at"] + 0.2) for c, t in zip(cs, ("BANK A", "BANK B", "BANK C"))],
    *[dict(kind="label", x=x, y=360, text="+", size=110, anchor="middle", color="dim", at=P("C052", "Other banks")) for x in (640, 1280)],
    *[dict(kind="cross", x=x, y=325, size=110, at=P("C052", "don't add") + k * 0.15) for k, x in enumerate((640, 1280))],
    rp2,
    *[dict(kind="arrow", x=x0, y=560, to=[dx, 170], bend=0.1 * (1 if dx < 0 else -1), color="red", at=P("C052", "They only see") + k * 0.12)
      for k, (x0, dx) in enumerate(((320, 470), (960, 0.1), (1600, -470)))],
    dict(kind="label", x=960, y=1040, text="THEY ALL SEE YOUR CIBIL", size=48, anchor="middle", color="red", at=P("C052", "They only see")),
])
