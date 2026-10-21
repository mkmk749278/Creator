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
blocks, cur = [], []
for l in lines:
    size = sum(len(x) + 2 for x in cur) + len(l)
    if cur and (size > CAP or (l.startswith(CHAPTERS) and sum(len(x) + 2 for x in cur) > 700)):
        blocks.append(cur); cur = []
    cur.append(l)
blocks.append(cur)
out = ["# Recording blocks: Akash (ElevenLabs), rare earth magnets\n",
       "Voice: Akash, the channel's English voice and settings. Paste each block as is; the blank lines are pauses. "
       "Save each take as `voice/rem_bNN.mp3` (NN = block number).\n"]
for i, b in enumerate(blocks, 1):
    text = "\n\n".join(b)
    assert len(text) < CAP, (i, len(text))
    out.append(f"## Block {i} of {len(blocks)} · {len(text)} characters · save as `voice/rem_b{i:02d}.mp3`\n\n```\n{text}\n```\n")
(HERE / "vo_blocks.md").write_text("\n".join(out))
print(len(blocks), "blocks:", [len("\n\n".join(b)) for b in blocks])
