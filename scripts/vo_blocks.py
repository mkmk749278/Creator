#!/usr/bin/env python3
"""Build the owner's recording file for an English VO (owner, 2026-10-28; PLAYBOOK §4a-2).

One Markdown file holds the full narration to read through, then the same text split into click-to-copy recording
blocks (fenced code, under 1,500 characters each, blank line between beats). Send this one file with every VO change,
and paste the blocks in the chat as well.

usage: python3 scripts/vo_blocks.py projects/<slug>/vo.txt --prefix pha --title "pharma APIs"
       (writes projects/<slug>/vo_blocks.md)
"""
import argparse
from pathlib import Path

VOICE = ("Akash, Eleven v4, stability 0.65, similarity 0.85, style 0.15, speaker boost on (PLAYBOOK §4a-10). "
         "Paste each block as is; the blank lines are pauses.")


def split_blocks(lines, limit):
    blocks, cur = [], []
    for line in lines:
        if cur and len("\n\n".join(cur + [line])) > limit:
            blocks.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vo", help="vo.txt, one spoken beat per line")
    ap.add_argument("--prefix", required=True, help="take file prefix, e.g. pha -> voice/pha_b01.mp3")
    ap.add_argument("--title", required=True)
    ap.add_argument("--limit", type=int, default=1450, help="max characters per block (hard cap 1,500)")
    ap.add_argument("--out", help="default: vo_blocks.md next to vo.txt")
    args = ap.parse_args()

    vo = Path(args.vo)
    lines = [l.strip() for l in vo.read_text(encoding="utf-8").splitlines() if l.strip()]
    blocks = split_blocks(lines, args.limit)
    words = sum(len(l.split()) for l in lines)
    n = len(blocks)

    out = [f"# Recording file: {args.title}", "",
           f"{words} words · {n} blocks · about {words / 155:.0f}–{words / 145:.0f} minutes at 145–155 words a minute.", "",
           f"**Voice:** {VOICE} Save each take as `voice/{args.prefix}_bNN.mp3` (NN = block number).", "",
           "## Full narration", ""]
    for line in lines:
        out += [line, ""]
    out += ["## Recording blocks (tap to copy)", ""]
    for i, block in enumerate(blocks, 1):
        text = "\n\n".join(block)
        out += [f"### Block {i} of {n} · {len(text)} characters · save as `voice/{args.prefix}_b{i:02d}.mp3`", "",
                "```", text, "```", ""]

    dest = Path(args.out) if args.out else vo.with_name("vo_blocks.md")
    dest.write_text("\n".join(out), encoding="utf-8")
    print(f"{dest}: {words} words, {n} blocks {[len(chr(10).join(b)) for b in blocks]}")


if __name__ == "__main__":
    main()
