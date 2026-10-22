#!/usr/bin/env python3
"""Split vo.txt into Akash recording blocks (< 1,500 characters each, CLAUDE.md), breaking at chapter starts first.

Writes vo_blocks.md: one fenced block per recording, beats separated by a blank line (TTS pause), with the file name
to save each take as. usage: python3 projects/rare-earth-magnets/tools/vo_blocks.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CAP = 1500
# lines (1-based) that open a chapter: a block should start here when it can
CHAPTERS = ("First, what is this magnet?", "Here's the catch", "So how did China end up", "So what about India?",
            "So the sand alone", "So is India just waiting?", "Let me be honest with you", "So what does this mean")

lines = [l.strip() for l in (HERE / "vo.txt").read_text().splitlines() if l.strip()]
# Block starts are pinned to the v4 takes (2026-10-22), so a change inside one block never moves the others and the
# owner re-records only the blocks whose text changed.
STARTS = ('First, what is this magnet?', "Here's the catch, and it may surprise yo", "So a magnet isn't one factory. It's a ch", 'So what about India? We had the sand all', 'But a magnet inside a hot motor also nee', 'So is India just waiting? Not at all — a', 'Let me be honest with you about the time')
blocks, cur = [], []
for l in lines:
    if cur and l.startswith(STARTS):
        blocks.append(cur); cur = []
    cur.append(l)
blocks.append(cur)
assert len(blocks) == len(STARTS) + 1, "a pinned block start is missing from vo.txt"
if __name__ == "__main__":
    out = ["# Recording blocks: Akash (ElevenLabs), rare earth magnets\n",
           "Voice: Akash, Eleven v4, stability 0.65, similarity 0.85, style 0.15, speaker boost on (PLAYBOOK §4a-10). Paste each block as is; the blank lines are pauses. "
           "Save each take as `voice/rem_bNN.mp3` (NN = block number).\n"]
    for i, b in enumerate(blocks, 1):
        text = "\n\n".join(b)
        assert len(text) < CAP, (i, len(text))
        out.append(f"## Block {i} of {len(blocks)} · {len(text)} characters · save as `voice/rem_b{i:02d}.mp3`\n\n```\n{text}\n```\n")
    (HERE / "vo_blocks.md").write_text("\n".join(out))
    print(len(blocks), "blocks:", [len("\n\n".join(b)) for b in blocks])
