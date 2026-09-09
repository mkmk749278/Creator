#!/usr/bin/env python3
"""Fail if any rendered caption straddles a full stop.

A caption line carrying the end of one sentence and the start of the next reads
as two half-thoughts, and it is the single most common way an auto-captioned
reel looks machine-made. `captions.mark_punctuation` exists to prevent it.

It stopped preventing it on 2026-09-09 and nothing noticed, because the failure
is silent by construction: the captions still render, still sit in time with the
voice, and simply stop breaking where the sentences do. The cause was one
hyphenated compound desyncing the token cursor -- which cost the marks for the
whole rest of that reel, not for one word.

So the property is checked against the ARTIFACT rather than trusted from the
code that writes it: read each reel's .srt back, and for every adjacent pair of
words on one caption line, ask whether the script puts a sentence end between
them. That question is answerable from files already on disk and needs no
re-render, which is what makes it cheap enough to run every time.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def straddles(srt: pathlib.Path, narration: str) -> list[str]:
    bad = []
    for block in srt.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        words = lines[2].split()
        for a, b in zip(words, words[1:]):
            if re.search(re.escape(a) + r"[.!?]+[\"')\]]*\s+" + re.escape(b), narration):
                bad.append(lines[2])
                break
    return bad


def main() -> int:
    failed = 0
    for d in sorted((ROOT / "reels").iterdir()):
        script = d / "script.json"
        if not script.exists():
            continue
        doc = json.loads(script.read_text(encoding="utf-8"))
        srt = d / "out" / f"{doc['id']}.srt"
        if not srt.exists():
            print(f"  {doc['id']:<26} not rendered")
            continue
        bad = straddles(srt, doc.get("voice", ""))
        mark = "OK " if not bad else "BAD"
        print(f"  {mark} {doc['id']:<26} {len(bad)} straddling caption(s)"
              + (f"  e.g. {bad[0]!r}" if bad else ""))
        failed += len(bad)
    if failed:
        print(f"\n  {failed} caption(s) run across a full stop. The usual cause is "
              f"a character edge-tts and captions.mark_punctuation tokenise "
              f"differently -- it now WARNS at render time, so re-render and read "
              f"the log.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
