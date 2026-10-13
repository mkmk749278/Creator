#!/usr/bin/env python3
"""Program timeline: VO line times from align/block{1,2}/align.json plus the picture-only breaks below.

Writes align/program.json: every VO line with its program start/end (seconds of the finished film) and every break
(VO_PAUSE / diegetic / end card). Scene specs (scenes.json), the EDL and the assembler all read program times from
here, so a re-alignment or a changed break moves everything together.

  python3 projects/jet-engine-paradox/tools/timeline.py
"""
import csv
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
BLOCK_GAP = 1.5          # between block 1 (ends 'go inside the engine') and block 2: the dive into the engine
# picture-only breaks inserted AFTER the named line (seconds); the VO is silent, the picture keeps moving
BREAKS = {
    "J019": (1.5, "VO_PAUSE", "1.5 s total music silence, then a low thud on 'India has been here before' (reveal 1)"),
    "J049": (2.0, "DIEGETIC", "afterburner take-off roar at full level, no VO"),
    "J053": (1.5, "VO_PAUSE", "1.5 s total music silence, braam lands on 'melting point' (core reveal)"),
    "J087": (1.5, "VO_PAUSE", "title burn-in breathes; music swell"),
    "J090": (10.0, "END_CARD", "end card with subscribe and YouTube end-screen zones (5-20 s rule)"),
}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def main():
    rows = list(csv.DictReader(open(HERE / "script.full.tsv", encoding="utf-8"), delimiter="\t"))
    a = json.load(open(HERE / "align/block1/align.json")) + json.load(open(HERE / "align/block2/align.json"))
    assert len(a) == len(rows), (len(a), len(rows))
    d1 = dur(HERE / "voice/block1.mp3")
    lines, breaks, shift = [], [], 0.0
    for i, (r, al) in enumerate(zip(rows, a)):
        vo_off = 0.0 if i < 45 else d1 + BLOCK_GAP          # where this line sits in the joined VO track
        if i == 45:
            breaks.append(dict(after="J045", start=round(d1 + shift, 2), len=BLOCK_GAP, kind="VO_PAUSE",
                               note="block gap: camera dives into the engine"))
        s, e = al["start"] + vo_off + shift, al["end"] + vo_off + shift
        lines.append(dict(id=r["id"], section=r["section"], start=round(s, 2), end=round(e, 2),
                          vo_start=round(al["start"] + vo_off, 2), vo_end=round(al["end"] + vo_off, 2), en=r["en"],
                          onscreen=r["onscreen"], cite=r["cite"]))
        if r["id"] in BREAKS:
            ln, kind, note = BREAKS[r["id"]]
            # the break starts at the end of this line's audio chunk (before the next line's speech)
            nxt = (a[i + 1]["start"] + (0.0 if i + 1 < 45 else d1 + BLOCK_GAP)) if i + 1 < len(a) else al["end"] + vo_off
            bstart = (al["end"] + vo_off + nxt) / 2 + shift
            breaks.append(dict(after=r["id"], start=round(bstart, 2), len=ln, kind=kind, note=note,
                               vo_at=round((al["end"] + vo_off + nxt) / 2, 2)))
            shift += ln
    total = lines[-1]["end"] + BREAKS["J090"][0]
    json.dump(dict(block1_dur=d1, block_gap=BLOCK_GAP, total=round(total, 2), lines=lines, breaks=breaks),
              open(HERE / "align/program.json", "w"), indent=1, ensure_ascii=False)
    print(f"program length {total:.2f} s ({int(total // 60)}:{total % 60:04.1f}); {len(breaks)} breaks")


if __name__ == "__main__":
    main()
