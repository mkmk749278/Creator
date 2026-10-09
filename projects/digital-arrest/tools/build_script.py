#!/usr/bin/env python3
"""Build every script view from script.full.tsv (the single source; edit only that file).

Writes, in projects/digital-arrest/:
  script.md         phone-readable shooting script: section, Telugu VO, English, visual, on-screen text, sound
  bunty_blocks.md   paste-ready ElevenLabs blocks (Telugu only), 4,000-4,500 characters, split at section ends
  script.tsv        te<TAB>en, one spoken line per row, `---` between blocks (align_script.py / estimate_vo.py)
and lints the Telugu text for the Bunty format (CLAUDE.md, PLAYBOOK §4, §4b): Telugu script only, no ! quotes dashes
brackets or stage directions, at most one `...` per sentence, no banned newspaper connectors or ban-list words.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TARGET, CAP = (4000, 4500), 5000
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from estimate_vo import line_seconds  # noqa: E402  (one timing model for every tool)
BANNED = ["ఈ నేపథ్యంలో", "ఈ క్రమంలో", "అనంతరం", "తద్వారా", "కావున", "సదరు", "పేర్కొన్నారు", "వెల్లడించారు",
          "చండాల", "కటిక చీకటి", "నువ్వు"]


def lint(row):
    te, errs = row["te"], []
    bad = re.findall(r"[^ఀ-౿\s,.‌‍]", te)
    if bad:
        errs.append(f"non-Telugu characters {sorted(set(bad))}")
    for s in re.split(r"(?<=\.)\s", te):
        if s.count("...") > 1:
            errs.append("more than one ... in a sentence")
    errs += [f"banned word {w}" for w in BANNED if w in te]
    return errs


def blocks_of(rows):
    """Fewest blocks that respect the 5,000 cap, sized near 4,250; cut at section ends near the ideal points."""
    import math
    total = sum(len(r["te"]) + 1 for r in rows)
    k = max(math.ceil(total / CAP), round(total / 4250), 1)
    ideal = [total * j / k for j in range(1, k)]
    pos, cuts = 0, []  # cumulative size after each line
    ends = []
    for i, r in enumerate(rows):
        pos += len(r["te"]) + 1
        ends.append((i, pos, i + 1 < len(rows) and rows[i + 1]["section"] != r["section"]))
    for t in ideal:
        # prefer a section end within 450 chars of the ideal point, else the nearest line end
        sec = [e for e in ends if e[2] and abs(e[1] - t) <= 450]
        best = min(sec or ends, key=lambda e: abs(e[1] - t))
        cuts.append(best[0])
    out, start = [], 0
    for c in cuts:
        out.append(rows[start:c + 1]); start = c + 1
    out.append(rows[start:])
    return out


def block_text(block):
    """Lines joined with spaces; a blank line between sections gives Bunty a natural paragraph pause."""
    paras, cur, sec = [], [], None
    for r in block:
        if sec is not None and r["section"] != sec:
            paras.append(" ".join(cur)); cur = []
        cur.append(r["te"]); sec = r["section"]
    paras.append(" ".join(cur))
    return "\n\n".join(paras)


def chars(block):
    return len(block_text(block))


def secs(block):
    return sum(line_seconds(r["te"]) for r in block)


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    rows = list(csv.DictReader(open(HERE / "script.full.tsv", encoding="utf-8"), delimiter="\t"))
    problems = [(r["id"], e) for r in rows for e in lint(r)]
    for pid, e in problems:
        print(f"LINT {pid}: {e}")
    blocks = blocks_of(rows)
    for r_i, b in enumerate(blocks, 1):
        for r in b:
            r["block"] = r_i

    with open(HERE / "script.tsv", "w", encoding="utf-8") as f:
        f.write("te\ten\n")
        for i, b in enumerate(blocks):
            if i:
                f.write("---\n")
            for r in b:
                f.write(f"{r['te']}\t{r['en']}\n")

    total = sum(chars(b) for b in blocks)
    tsecs = sum(secs(b) for b in blocks)
    with open(HERE / "bunty_blocks.md", "w", encoding="utf-8") as f:
        f.write("# Bunty blocks: Digital Arrest\n\nPaste each block as one ElevenLabs generation (voice Bunty, `eleven_v3`/"
                "`eleven_v4`, `language_code: te`). Listen to every take; if a block skips, repeats or drifts, regenerate "
                "it, and send the files as `voice/block1.mp3`, `voice/block2.mp3`, ….\n\n")
        for i, b in enumerate(blocks, 1):
            c = chars(b)
            f.write(f"## Block {i} · {c:,} characters · ~{mmss(secs(b))} · lines {b[0]['id']}–{b[-1]['id']}\n\n")
            f.write(block_text(b) + "\n\n")
        f.write(f"Total {total:,} characters, about {mmss(tsecs)} of speech.\n")

    with open(HERE / "script.md", "w", encoding="utf-8") as f:
        f.write("# Digital Arrest: shooting script (Be Practical with Kishore)\n\n"
                "Built from `script.full.tsv` by `tools/build_script.py`; edit the TSV, not this file. "
                "Each line: **Telugu VO** (what Bunty says), English meaning, then 🎬 picture, 🔤 on-screen text, "
                "🔊 sound. Tags: SIMULATION / RECONSTRUCTION / ILLUSTRATION mark anything that is not real footage.\n\n"
                f"Estimated length: **{mmss(tsecs)}** of speech ({total:,} characters, {len(blocks)} Bunty blocks), "
                "plus pauses and music beats.\n")
        sec = None
        for r in rows:
            if r["section"] != sec:
                sec = r["section"]
                f.write(f"\n## {sec}\n")
            f.write(f"\n**{r['id']}** · block {r['block']}  \n**{r['te']}**  \n_{r['en']}_  \n🎬 {r['visual']}")
            if r["onscreen"]:
                f.write(f"  \n🔤 {r['onscreen']}")
            if r["sound"]:
                f.write(f"  \n🔊 {r['sound']}")
            f.write("\n")

    for i, b in enumerate(blocks, 1):
        c = chars(b)
        flag = "ok" if TARGET[0] <= c <= TARGET[1] else ("OVER CAP" if c > CAP else "outside target")
        print(f"block {i}: {c:,} chars ~{mmss(secs(b))} {b[0]['id']}-{b[-1]['id']} {flag}")
    print(f"total {total:,} chars ~{mmss(tsecs)}; {len(problems)} lint problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
