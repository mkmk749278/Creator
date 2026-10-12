"""Line timings for the recorded VO (align/block*/align.json). Block 2 starts 0.6 s after block 1 ends (253.5 s)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
GAP_B2 = 253.5
_T = {}
for b, off in ((1, 0.0), (2, GAP_B2)):
    for i, l in enumerate(json.load(open(HERE / f"align/block{b}/align.json")), 1):
        _T[f"{b}.{i:02d}"] = (round(off + l["start"], 2), round(off + l["end"], 2))
END = _T["2.32"][1] + 6.0   # end card runs on after the last line


def L(key):
    """(start, end) of a VO line in film seconds, e.g. L("1.07")."""
    return _T[key]
