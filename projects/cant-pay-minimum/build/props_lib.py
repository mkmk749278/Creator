#!/usr/bin/env python3
"""Photoreal props and desk plates for this film (owner, 2026-10-13: "use ultra realistic photos for card, bill, etc.").

PROPS: alpha cut-outs (video/lib/props, one prop each) for the paper pages. PLATES: full desk frames (props studio desk
mode) for the big moments. Each spec renders once into assets/props/<name>.png + <name>.json (size and anchors, the
pixel position of named spots such as box1 = the minimum-due box), and re-renders only when its spec changes.
Every bill, card and screen is ours: fictional names, no bank logos, SIMULATION on screen.

  python3 build/props_lib.py [name ...]     # shoot missing or changed ones
"""
import hashlib, json, subprocess, sys
from pathlib import Path

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
OUT = P / "assets/props"

RAVI_ROWS = [["Previous balance", "₹10,000"], ["Payments received", "₹0"], ["Late payment fee", "₹750"],
             ["Interest (3.75% a month)", "₹375"], ["GST 18% on fee + interest", "₹203"]]
SMS1 = {"app": "Messages", "when": "now", "title": "AX-CARDSV", "body": "Your credit card payment is overdue. Please pay immediately to avoid further charges."}
SMS2 = {"app": "Messages", "when": "now", "title": "AX-CARDSV", "body": "Reminder: your card account is past due. Pay the minimum amount due today."}

# ---- cut-outs for pages (top-down-ish so annotations read straight) ----
PROPS = {
    "bill_ravi": dict(type="bill", yaw=0, elev=84, aspect=0.8, hiBox=1, name="RAVI KUMAR", rows=RAVI_ROWS),
    "bill_ravi_overdue": dict(type="bill", yaw=0, elev=84, aspect=0.8, hiBox=1, name="RAVI KUMAR", rows=RAVI_ROWS, stamp="OVERDUE"),
    "bill_10l": dict(type="bill", yaw=0, elev=84, aspect=0.8, name="ARJUN RAO", cardno="CARD  5190 •••• •••• 2286",
                     address="H.NO 4-12, KUKATPALLY, HYDERABAD 500072",
                     boxes=[["TOTAL AMOUNT DUE", "₹10,00,000"], ["MINIMUM AMOUNT DUE", "₹50,000"], ["PAYMENT DUE DATE", "05 NOV 2026"]],
                     rows=[["Previous balance", "₹10,00,000"], ["Payments received", "₹0"], ["Late payment fee", "₹1,300"]]),
    "bill_sunita": dict(type="bill", yaw=0, elev=84, aspect=0.8, hiBox=-1, name="SUNITA REDDY", cardno="CARD  6011 •••• •••• 5402",
                        address="PLOT 33, MADHAPUR, HYDERABAD 500081", accent="#4a1d3a",
                        boxes=[["TOTAL AMOUNT DUE", "₹1,00,000"], ["MINIMUM AMOUNT DUE", "₹5,000"], ["PAYMENT DUE DATE", "05 NOV 2026"]],
                        rows=[["Previous balance", "₹1,00,000"], ["Payments received", "₹0"], ["Late payment fee", "₹1,300"],
                              ["Interest (3.75% a month)", "₹3,750"], ["GST 18% on fee + interest", "₹909"]]),
    "report_ravi": dict(type="report", yaw=0, elev=84, aspect=0.8, score=642, name="RAVI KUMAR",
                        accounts=[{"lender": "BANK A", "type": "CREDIT CARD", "dpd": ["000", "000", "000", "030", "060", "090"]},
                                  {"lender": "BANK B", "type": "PERSONAL LOAN", "dpd": ["000", "000", "000", "000", "000", "000"]}]),
    "notice_prior": dict(type="notice", yaw=0, elev=84, aspect=0.8, **{"from": "CARD SERVICES", "fromLine": "CUSTOMER NOTICE · SIMULATION"}, head="PRIOR NOTICE", ref="REF: CARD 4821 •••• 7730",
                         lines=["To: Mr. Ravi Kumar", "Subject: Reporting to credit bureaus", "", "Your card account is overdue. If it is not paid,",
                                "it will be reported as a default after 7 days."], bodyLines=8),
    "agency_file": dict(type="notice", yaw=0, elev=84, aspect=0.8, **{"from": "RECOVERY AGENCY", "fromLine": "COLLECTIONS · HYDERABAD · SIMULATION"},
                        head="ACCOUNT ALLOCATION", ref="BATCH: OCT-2026 / 118", date="DATE: 02 DEC 2026",
                        lines=["Customer: Ravi Kumar", "Card: 4821 •••• 7730", "Outstanding: ₹10,000", "Days past due: 95",
                               "Agency fee: a share of what is collected"], bodyLines=5),
    "notice_lokadalat": dict(type="notice", yaw=0, elev=84, aspect=0.8, **{"from": "LOK ADALAT", "fromLine": "PRE-LITIGATION SITTING · SIMULATION"},
                             head="NOTICE TO APPEAR", ref="MATTER: CARD DUES", date="DATE: 14 DEC 2026",
                             lines=["To: Mr. Ravi Kumar", "Venue: court complex, your city", "Time: 10:30 AM",
                                    "Purpose: settlement of card dues"], bodyLines=6),
    "award": dict(type="notice", yaw=0, elev=84, aspect=0.8, **{"from": "SOLE ARBITRATOR", "fromLine": "APPOINTED BY THE BANK · SIMULATION"},
                  head="ARBITRAL AWARD", ref="CASE: CC/ARB/2026/0912", date="DATE: 20 NOV 2026",
                  lines=["Claimant: the card company", "Respondent: Mr. Ravi Kumar", "", "The respondent shall pay the amount claimed."], bodyLines=7),
    "card_maroon": dict(type="card", color="maroon", yaw=6, elev=62, aspect=1.5, number="5190 •••• •••• 2286", name="RAVI KUMAR"),
    "card_teal": dict(type="card", color="teal", yaw=-4, elev=62, aspect=1.5, number="6011 •••• •••• 9054", name="RAVI KUMAR"),
    "card_black": dict(type="card", color="black", yaw=-8, elev=62, aspect=1.5),
    "card_navy": dict(type="card", color="navy", yaw=-8, elev=62, aspect=1.5),
    "phone_sms1": dict(type="phone", yaw=-4, elev=80, aspect=0.75, clock="11:48", date="Tuesday, 14 October", notes=[SMS1]),
}

# ---- desk plates (same camera within a scene, so plates crossfade cleanly) ----
DESK_A = dict(type="desk", px=3840, aspect=1.7778, mug={"at": [20, -21]}, pen={"at": [-4, -16], "yaw": 30},
              cam={"elev": 50, "az": 8, "dist": 56, "look": [0, 0, 2], "fov": 34, "range": 30, "bokeh": 2.5})
DESK_B = dict(DESK_A, cam={"elev": 72, "az": 4, "dist": 34, "look": [4, 0, 3], "fov": 34, "range": 14, "bokeh": 3})


def desk(base, phone, **kw):
    props = [dict(type="phone", id="phone", at=[4, 3], yaw=-12, clock="11:48", date="Tuesday, 14 October", **phone),
             dict(type="bill", id="bill", at=[-22, -4], yaw=14, hiBox=1, rows=RAVI_ROWS),
             dict(type="card", id="card", at=[21, 12], yaw=18, color="black", matte=True)]
    return dict(base, props=props, **kw)


PLATES = {
    "deskA_off": desk(DESK_A, dict(screen="off")),
    "deskA_sms1": desk(DESK_A, dict(notes=[SMS1])),
    "deskA_sms2": desk(DESK_A, dict(notes=[SMS2, SMS1])),
    "deskB_sms2": desk(DESK_B, dict(notes=[SMS2, SMS1])),
    "deskB_call": desk(DESK_B, dict(screen="call", caller="Unknown number", number="+91 9•••• •••21")),
}
# slab walk (C047-C051): four bills in a row on one desk; one overview camera and one camera per bill
SLABS = [("₹10,000", "₹500"), ("₹75,000", "₹3,750"), ("₹3,50,000", "₹17,500"), ("₹12,00,000", "₹60,000")]
SLAB_X = [-36, -12, 12, 36]


def slab_desk(cam):
    props = [dict(type="bill", id=f"bill{i}", at=[x, 0], yaw=[4, -3, 3, -4][i], flat=True, name="CARDHOLDER", cardno="CARD  •••• •••• •••• ••••",
                  address="SIMULATION", boxes=[["TOTAL AMOUNT DUE", tot], ["MINIMUM AMOUNT DUE", mn], ["PAYMENT DUE DATE", "05 NOV 2026"]], hiBox=0,
                  rows=[["Previous balance", tot], ["Payments received", "₹0"]]) for i, ((tot, mn), x) in enumerate(zip(SLABS, SLAB_X))]
    return dict(type="desk", px=3840, aspect=1.7778, props=props, lamp={"pos": [-30, 95, -40], "target": [0, 0, 4], "power": 3.6, "angle": 0.8},
                pen={"at": [-50, 22], "yaw": 20}, cam=cam)


PLATES["slab_all"] = slab_desk({"elev": 62, "az": 0, "dist": 128, "look": [0, 0, 2], "fov": 34, "range": 70, "bokeh": 1.5})
for i, x in enumerate(SLAB_X):
    PLATES[f"slab{i}"] = slab_desk({"elev": 60, "az": 6, "dist": 52, "look": [x, 0, -3], "fov": 34, "range": 20, "bokeh": 2.5})
ALL = {**PROPS, **PLATES}


PROPS_V = 1   # bump when video/lib/props changes how existing props look (new prop types don't need a bump)


def _hash(spec):
    return hashlib.sha1((json.dumps(spec, sort_keys=True, ensure_ascii=False) + str(PROPS_V)).encode()).hexdigest()[:12]


def shoot(names=None):
    OUT.mkdir(parents=True, exist_ok=True)
    hf = OUT / "hashes.json"; done = json.loads(hf.read_text()) if hf.exists() else {}
    todo = {n: s for n, s in ALL.items() if (not names or n in names) and (done.get(n) != _hash(s) or not (OUT / f"{n}.png").exists())}
    if not todo:
        return
    spec = OUT / "_specs.json"; spec.write_text(json.dumps(todo, ensure_ascii=False))
    subprocess.run(["node", str(ROOT / "video/lib/props/shoot.mjs"), str(spec), str(OUT)], check=True)
    for n, s in todo.items():
        done[n] = _hash(s)
    hf.write_text(json.dumps(done, indent=0, sort_keys=True))


def meta(name):
    return json.loads((OUT / f"{name}.json").read_text())


if __name__ == "__main__":
    shoot(sys.argv[1:] or None)
