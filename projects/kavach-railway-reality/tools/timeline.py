#!/usr/bin/env python3
"""Program timeline: VO line times from align/block{1,2,3}/align.json plus the picture-only breaks below.

Writes align/program.json: every VO line with its program start/end (seconds of the finished film), where it sits in
the joined VO track, and every break (TITLE / CHAPTER / DIEGETIC / VO_PAUSE / END_CARD). Scene specs (scenes.json), the
EDL and the assembler read program times from here, so a re-alignment or a changed break moves everything together.

  python3 projects/kavach-railway-reality/tools/timeline.py
"""
import csv
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
# picture-only breaks inserted AFTER the named line (seconds); the VO is silent, the picture keeps moving
BREAKS = {
    "V008": (2.5, "TITLE", "title THE KAVACH RAILWAY REALITY rises out of the night track bed"),
    "V011": (2.5, "DIEGETIC", "the March 2022 trial clip plays with its own sound: engines brake and stop"),
    "V020": (1.5, "CHAPTER", "chapter card THE PHYSICS (end of block 1)"),
    "V031": (1.5, "CHAPTER", "chapter card THE ROLLOUT"),
    "V038": (1.5, "CHAPTER", "chapter card TWO CRASHES (end of block 2)"),
    "V042": (2.0, "VO_PAUSE", "memorial silence, music out"),
    "V043": (1.5, "VO_PAUSE", "1.5 s total music silence, then a low braam on 'the honest answer' (core reveal)"),
    "V053": (1.5, "CHAPTER", "chapter card WHAT YOU CAN DO, warm music returns"),
    "V061": (10.0, "END_CARD", "end card with subscribe and YouTube end-screen zones"),
}
BLOCKS = 3


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def main():
    rows = list(csv.DictReader(open(HERE / "script.full.tsv", encoding="utf-8"), delimiter="\t"))
    al, offs, off = [], [], 0.0
    for b in range(1, BLOCKS + 1):
        a = json.load(open(HERE / f"align/block{b}/align.json"))
        al += [dict(x, block=b, off=off) for x in a]
        offs.append(off)
        off += dur(HERE / f"voice/block{b}.mp3")
    vo_total = off
    assert len(al) == len(rows), (len(al), len(rows))
    lines, breaks, shift = [], [], 0.0
    for i, (r, a) in enumerate(zip(rows, al)):
        vs, ve = a["start"] + a["off"], a["end"] + a["off"]
        lines.append(dict(id=r["id"], section=r["section"], block=a["block"], start=round(vs + shift, 2),
                          end=round(ve + shift, 2), vo_start=round(vs, 2), vo_end=round(ve, 2), en=r["en"],
                          onscreen=r["onscreen"], cite=r["cite"], confidence=a["confidence"]))
        if r["id"] in BREAKS:
            ln, kind, note = BREAKS[r["id"]]
            nxt = al[i + 1]["start"] + al[i + 1]["off"] if i + 1 < len(al) else ve
            cut = (ve + nxt) / 2          # the break opens in the pause after this line, cut on the breath
            breaks.append(dict(after=r["id"], start=round(cut + shift, 2), len=ln, kind=kind, note=note,
                               vo_at=round(cut, 2)))
            shift += ln
    total = lines[-1]["end"] + BREAKS["V061"][0]
    json.dump(dict(block_offsets=[round(o, 3) for o in offs], vo_total=round(vo_total, 3), total=round(total, 2),
                   lines=lines, breaks=breaks), open(HERE / "align/program.json", "w"), indent=1, ensure_ascii=False)
    L = {l["id"]: l for l in lines}
    mm = lambda s: f"{int(s // 60)}:{s % 60:04.1f}"
    print(f"program {mm(total)}; payoff V039 {mm(L['V039']['start'])}; honest answer V044 {mm(L['V044']['start'])}; "
          f"Kanchanjunga V048 {mm(L['V048']['start'])}; action plan V054 {mm(L['V054']['start'])}")


if __name__ == "__main__":
    main()
