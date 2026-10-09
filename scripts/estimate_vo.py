#!/usr/bin/env python3
"""Estimate how long Bunty (ElevenLabs Telugu) will take to speak a script, before any TTS is generated (PLAYBOOK §7).

Per-line model fitted on the 65 lines of fire-and-ice (three eleven_v4 Bunty takes, timed by align_script.py):
  seconds = 0.065 x characters + 0.07 x '...' + 0.53 x commas + 0.22 per line
Characters count everything in the line (letters, vowel signs, spaces, punctuation). Held-out accuracy: take totals within
1%, single lines +/-0.5 s, start times drift up to ~3.5 s inside a take. That is good enough to plan the EDL and act
lengths. Exact timings still come from align_script.py on the real VO. The rate is about 14.3 characters/s; a Prahlad
Jani take ran ~13.5, so treat estimates as +/-7% until more takes are measured.

  python3 scripts/estimate_vo.py SCRIPT [--srt out.srt]

SCRIPT: plain text or a te<TAB>en TSV, one spoken line per row. A line holding only `---` (or starting with `## `) starts
a new ElevenLabs block; each block is checked against the 4,000-4,500 character target and the 5,000 cap.
Lines starting with `#` (other than `## `) are ignored. Prints per-block and total durations; --srt writes estimated cues.
"""
import argparse
import re
import sys

PER_CHAR, PER_DOTS, PER_COMMA, PER_LINE = 0.065, 0.07, 0.53, 0.22
TARGET, CAP = (4000, 4500), 5000


def line_seconds(te):
    dots = te.count("...")
    commas = te.count(",")
    return PER_CHAR * len(te) + PER_DOTS * dots + PER_COMMA * commas + PER_LINE


def mmss(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def srt_time(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def read_blocks(path):
    blocks, cur = [], []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.strip() == "---" or line.startswith("## "):
            if cur:
                blocks.append(cur)
            cur = []
            continue
        if not line.strip() or line.startswith("#"):
            continue
        te = re.split(r"\t| \| ", line)[0].strip()
        if te.lower() == "te":  # TSV header
            continue
        te = re.sub(r"\[[^\]]*\]", "", te).strip()  # audio tags are not spoken
        if te:
            cur.append(te)
    if cur:
        blocks.append(cur)
    return blocks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script")
    ap.add_argument("--srt", help="write estimated cues (one per line, programme time, blocks back to back)")
    args = ap.parse_args()

    blocks = read_blocks(args.script)
    if not blocks:
        sys.exit("no spoken lines found")
    t, cues = 0.0, []
    print("block  chars  lines  est. length  check")
    for i, lines in enumerate(blocks, 1):
        chars = sum(len(x) for x in lines) + len(lines) - 1  # lines joined with a space, as sent to ElevenLabs
        secs = sum(line_seconds(x) for x in lines)
        if chars > CAP:
            check = f"OVER the {CAP:,} cap: split it"
        elif chars < TARGET[0] and i < len(blocks):
            check = f"short (target {TARGET[0]:,}-{TARGET[1]:,})"
        elif chars > TARGET[1]:
            check = f"long (target {TARGET[0]:,}-{TARGET[1]:,})"
        else:
            check = "ok"
        print(f"{i:>5}  {chars:>5,}  {len(lines):>5}  {mmss(secs):>11}  {check}")
        for x in lines:
            d = line_seconds(x)
            cues.append((t, t + d, x))
            t += d
    lo, hi = t * 0.93, t * 1.07
    print(f"total  {mmss(t)} spoken (likely {mmss(lo)}-{mmss(hi)}), before edit pauses, diegetic cuts and music-only beats")
    if args.srt:
        with open(args.srt, "w", encoding="utf-8") as f:
            for n, (a, b, x) in enumerate(cues, 1):
                f.write(f"{n}\n{srt_time(a)} --> {srt_time(b)}\n{x}\n\n")
        print(f"wrote {args.srt} ({len(cues)} estimated cues)")


if __name__ == "__main__":
    main()
