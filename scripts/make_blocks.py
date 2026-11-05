#!/usr/bin/env python3
"""Split a VO script into ElevenLabs recording blocks (PLAYBOOK §7.5, §7.7).

Akash takes stay under 1,500 characters (Creator's measured limit for English Akash takes). Blocks break only between
beats (blank lines), and prefer a chapter break: a line `## ` in the VO file marks one and is not spoken.
Writes a Markdown file with one fenced block per take, headed with its number, length, voice settings and the file
name to save, ready to paste into the chat (one-tap copy on the phone).

Usage: scripts/make_blocks.py films/<slug>/script/vo.txt SLUG OUT.md [--max 1500]
"""
import argparse
from pathlib import Path

VOICE = "Akash · Eleven v4 · stability 0.65 · similarity 0.85 · style 0.15 · speaker boost on"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("vo")
    ap.add_argument("slug")
    ap.add_argument("out")
    ap.add_argument("--max", type=int, default=1500)
    ap.add_argument("--voice", default=VOICE, help="voice and settings line for the block headings")
    ap.add_argument("--suffix", default="", help="file-name suffix, e.g. -perf for the tagged performance take")
    a = ap.parse_args()
    beats: list[tuple[bool, str]] = []  # (chapter break before this beat, text)
    brk = True
    for para in Path(a.vo).read_text().split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.startswith("## "):
            brk = True
            continue
        beats.append((brk, para))
        brk = False
    blocks: list[list[str]] = []
    cur: list[str] = []
    size = 0
    for i, (chap, text) in enumerate(beats):
        add = len(text) + (2 if cur else 0)
        # Close the block at a chapter break once it is reasonably full, or when the next beat would overflow it.
        if cur and (size + add > a.max or (chap and size > 0.55 * a.max)):
            blocks.append(cur)
            cur, size = [], 0
            add = len(text)
        cur.append(text)
        size += add
    if cur:
        blocks.append(cur)
    out = [f"# Recording blocks: {a.slug}{a.suffix}\n", f"{len(blocks)} blocks · voice: {a.voice}\n"]
    for n, b in enumerate(blocks, 1):
        body = "\n\n".join(b)
        assert len(body) <= a.max, f"block {n} is {len(body)} characters"
        out.append(f"**Block {n} of {len(blocks)}** · {len(body)} characters · save as `vo/{a.slug}{a.suffix}-b{n:02d}.mp3`\n")
        out.append("```\n" + body + "\n```\n")
    Path(a.out).write_text("\n".join(out))
    print(f"{len(blocks)} blocks, sizes: {[len(chr(10).join(b)) for b in blocks]}")


if __name__ == "__main__":
    main()
