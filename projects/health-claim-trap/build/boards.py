"""Whiteboard scenes (video/lib/whiteboard), timed to the VO. Every number from tools/claim_math.py (OUR CALCULATION)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import L, sents

s24, s25, s55, s59 = sents("E024"), sents("E025"), sents("E055"), sents("E059")
B1 = s24[0]["start"] - 0.25
B2 = s55[1]["start"] - 0.3
B3 = s59[-1]["start"] - 0.2

BOARDS = [
    dict(id="b01_room", start=B1, end=L("E025")[1] + 0.35, tag="OUR CALCULATION · ILLUSTRATIVE EXAMPLE", steps=[
        dict(write="Room limit: ₹5,000 a day", x=200, y=250, size=88, color="black", at=s24[0]["start"] + 0.5, dur=2.4),
        dict(write="Room taken: ₹8,000 a day", x=200, y=410, size=88, color="blue", at=s24[0]["start"] + 3.6, dur=2.2),
        dict(write="Cut only ₹3,000?", x=200, y=600, size=96, color="red", at=s24[1]["start"] + 0.1, dur=1.6),
        dict(cross=[1080, 560, 110], color="red", dur=0.5),
        dict(erase=True, at=s25[0]["start"] - 0.1, dur=1.1),
        dict(write="They pay 5 of every 8 rupees", x=200, y=250, size=84, color="black", at=s25[0]["start"] + 1.1, dur=2.3),
        dict(write="Surgery · doctor · nursing", x=200, y=410, size=76, color="blue", dur=1.9),
        dict(write="Cut = 37.5%", x=200, y=650, size=140, color="red", at=s25[1]["start"] - 0.1, dur=1.4),
        dict(underline="last", color="red", dur=0.35),
        dict(write="Medicines: no cut ✓", x=200, y=870, size=60, color="green", dur=1.0),
    ]),
    dict(id="b02_ombud", start=B2, end=L("E055")[1] + 0.3, tag="OUR CALCULATION · CIO ANNUAL REPORT 2024-25 | STATEMENT H3", steps=[
        dict(write="Settled: 9,417", x=200, y=230, size=86, color="green", at=s55[1]["start"] + 0.4, dur=1.4),
        dict(write="+ Won by award: 6,126", x=200, y=380, size=86, color="green", dur=1.6),
        dict(write="= 15,543 of 20,440", x=200, y=540, size=90, color="black", dur=1.5),
        dict(write="→ 76%", x=200, y=720, size=130, color="blue", dur=0.8),
        dict(underline="last", color="blue", dur=0.35),
        dict(write="Closed in 3 months: 78.5%", x=200, y=930, size=76, color="black", at=s55[2]["start"] + 0.1, dur=1.8),
        dict(underline="last", color="green", dur=0.5),
    ]),
    dict(id="b03_callback", start=B3, end=L("E059")[1] + 0.4, tag="OUR CALCULATION · ILLUSTRATIVE EXAMPLE", steps=[
        dict(write="One bigger room", x=260, y=380, size=110, color="black", at=s59[-1]["start"] + 0.3, dur=1.4),
        dict(write="= ₹59,625 cut", x=260, y=640, size=150, color="red", dur=1.8),
        dict(underline="last", color="red", dur=0.5),
    ]),
]
