#!/usr/bin/env python3
"""YouTube package for The Jet Engine Paradox (owner, 2026-10-14): title with the channel name, a plain-English description
with chapters and credits, and English subtitles from the fact-checked script on the real VO timing (no Whisper).

  python3 tools/youtube_pack.py            -> youtube/title.txt, youtube/description.txt, youtube/subtitles.en.srt

Chapter times come from align/program.json, so they match the cut exactly.
"""
import csv
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parent.parent
OUT = P / "youtube"
PROG = json.loads((P / "align" / "program.json").read_text())
L = {x["id"]: x for x in PROG["lines"]}
ROWS = {r["id"]: r for r in csv.DictReader(open(P / "script.full.tsv", encoding="utf-8"), delimiter="\t")}

TITLE = "India Landed on the Moon. Why Can't It Build a Jet Engine? | Be Practical With Kishore"
CHAPTERS = [  # (first line, chapter title) - first must start at 0:00; each 2-4 min (PLAYBOOK §4a)
    ("J001", "India reached the Moon, so why no jet engine?"),
    ("J010", "The Air Force is short of fighter jets"),
    ("J020", "1998: sanctions and a hard lesson"),
    ("J029", "The Kaveri engine story"),
    ("J046", "Why a jet engine is harder than a rocket"),
    ("J051", "The blade that lives hotter than its melting point"),
    ("J071", "The turning point"),
    ("J084", "The verdict"),
]


def ts(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def description():
    ch = "\n".join(f"{ts(0 if i == 0 else L[a]['start'])} {name}" for i, (a, name) in enumerate(CHAPTERS))
    return f"""India landed on the Moon in 2023. It builds nuclear submarines. It reached Mars on its first try.
So why are India's new Tejas fighter jets still waiting for an engine made in America?

In this video we look at why a fighter jet engine is one of the hardest machines on Earth to build, what happened to India's own Kaveri engine, and what India is doing now to finally make one of its own.

Chapters
{ch}

Every fact in this video comes from a public source: PIB and the Ministry of Defence, the CAG audit report of 2010, Rolls-Royce, the University of Cambridge, Bloomberg, The New Indian Express, The Wire, Janes, The Defense Post and the US Congressional Research Service. The source is shown on screen as each fact is said.

Animated scenes are illustrations made for this video. Clips marked ILLUSTRATIVE FOOTAGE are stand-in shots, not the real event.

Credits
Footage: ISRO, DD India, Indian Air Force, PIB India, DRDO (official channels), used for news commentary and education.
Photos: Prime Minister's Office (INS Arihant, GODL-India), Ministry of Defence (Il-76 with Kaveri, GODL-India), PIB (DMRL blades, 2021), Jagan Pillariseti (Kaveri engine, CC BY 3.0), FlyingDaggers45SQUADRON (AMCA model, CC BY-SA 4.0), N509FZ (Chengdu J-20, CC BY-SA 4.0), US Navy (GE F404, public domain), all via Wikimedia Commons; Moon photo and industrial B-roll from Pixabay.
Music: "Interloper", "Long Note Four" and "Lasting Hope" by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 (creativecommons.org/licenses/by/4.0/).

What do you think: will India have its own fighter jet engine in the next ten years? Tell me in the comments.

#India #JetEngine #Kaveri #Tejas #DRDO #BePracticalWithKishore
"""


def cues():
    """2-line cues (42 chars a line, at most 5.5 s) per script line, timed by characters inside the line's VO span."""
    out = []
    for i in sorted(L, key=lambda k: L[k]["start"]):
        if i not in ROWS:
            continue
        text = re.sub(r"\s+", " ", ROWS[i]["en"]).strip()
        s0, s1 = L[i]["start"], L[i]["end"]
        words, chunks, cur = text.split(" "), [], ""
        for w in words:   # break at sentence ends first, then at 84 chars
            if cur and (len(cur) + 1 + len(w) > 84 or re.search(r"[.?]$", cur) and len(cur) > 30):
                chunks.append(cur); cur = w
            else:
                cur = f"{cur} {w}".strip()
        chunks.append(cur)
        total = sum(len(c) for c in chunks)
        t = s0
        for c in chunks:
            d = (s1 - s0) * len(c) / total
            if len(c) > 42:   # two balanced lines
                cut = min((abs(len(c[:k]) - len(c) / 2), k) for k in [m.start() for m in re.finditer(" ", c)])[1]
                c = c[:cut] + "\n" + c[cut + 1:]
            out.append((t, min(t + d, t + 5.5), c)); t += d
    return out


def srt(cs):
    f = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"
    return "\n".join(f"{n}\n{f(a)} --> {f(b)}\n{c}\n" for n, (a, b, c) in enumerate(cs, 1))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "title.txt").write_text(TITLE + "\n")
    (OUT / "description.txt").write_text(description())
    cs = cues()
    (OUT / "subtitles.en.srt").write_text(srt(cs))
    print(f"title {len(TITLE)} chars; description {len(description())} chars; {len(cs)} subtitle cues")
