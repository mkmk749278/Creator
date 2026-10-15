#!/usr/bin/env python3
"""Write align/<take>.tsv (one sentence per row, for subtitle-sized cues) and align/<take>.ids (the script id of each row)
from script.full.tsv, for the script lines a voice take covers. Usage: make_align_tsv.py TAKE FIRST_ID LAST_ID"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
take, first, last = sys.argv[1:4]
rows = [r for r in csv.DictReader(open(HERE / "script.full.tsv", encoding="utf-8"), delimiter="\t")
        if first <= r["id"] <= last]
(HERE / "align").mkdir(exist_ok=True)
with open(HERE / "align" / f"{take}.tsv", "w", encoding="utf-8") as t, open(HERE / "align" / f"{take}.ids", "w") as i:
    t.write("te\ten\n")
    for r in rows:
        for s in re.split(r"(?<=[.?])\s+(?=[A-Z])", r["en"].strip()):
            t.write(f"{s}\t{s}\n")
            i.write(r["id"] + "\n")
print(take, len(rows), "lines")
