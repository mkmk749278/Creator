#!/usr/bin/env python3
"""Programme-timed subtitles: map each part's SRT (align/p<N>/subtitles.<lang>.srt) to programme time (tools/vomap.py),
dropping lines removed by the fact-check cuts.

  python3 tools/build_srt.py   -> subtitles.te.srt, subtitles.en.srt (upload subtitles.te.srt to YouTube)
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
from vomap import in_cut, offsets, prog  # noqa: E402
TS = re.compile(r"(\d+):(\d+):(\d+),(\d+)")


def secs(m):
    h, mi, s, ms = map(int, m.groups())
    return h * 3600 + mi * 60 + s + ms / 1000


def fmt(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    off, _ = offsets()
    for lang in ("te", "en"):
        out, n = [], 0
        for p in (1, 2, 3):
            for block in (HERE / f"align/p{p}/subtitles.{lang}.srt").read_text(encoding="utf-8").strip().split("\n\n"):
                lines = block.strip().split("\n")
                a, b = TS.findall(lines[1])[0], TS.findall(lines[1])[1]
                a0 = secs(re.match(TS, ":".join(a[:3]) + "," + a[3]))
                b0 = secs(re.match(TS, ":".join(b[:3]) + "," + b[3]))
                if in_cut(p, (a0 + b0) / 2, (a0 + b0) / 2):   # line removed by a fact-check cut
                    continue
                t0, t1 = prog(p, a0, off), prog(p, b0, off)
                n += 1
                out.append(f"{n}\n{fmt(t0)} --> {fmt(t1)}\n" + "\n".join(lines[2:]))
        (HERE / f"subtitles.{lang}.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
        print(f"subtitles.{lang}.srt: {n} cues")


if __name__ == "__main__":
    main()
