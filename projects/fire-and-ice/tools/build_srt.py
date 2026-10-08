#!/usr/bin/env python3
"""Programme-timed subtitles: shift each part's SRT (align/p<N>/subtitles.<lang>.srt) by its offset in vo_map.json.

  python3 tools/build_srt.py   -> subtitles.te.srt, subtitles.en.srt (upload subtitles.te.srt to YouTube)
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent.parent
TS = re.compile(r"(\d+):(\d+):(\d+),(\d+)")


def secs(m):
    h, mi, s, ms = map(int, m.groups())
    return h * 3600 + mi * 60 + s + ms / 1000


def fmt(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    off = json.loads((HERE / "vo_map.json").read_text())["offsets"]
    for lang in ("te", "en"):
        out, n = [], 0
        for p, o in enumerate(off, 1):
            for block in (HERE / f"align/p{p}/subtitles.{lang}.srt").read_text(encoding="utf-8").strip().split("\n\n"):
                lines = block.strip().split("\n")
                a, b = TS.findall(lines[1])[0], TS.findall(lines[1])[1]
                t0 = secs(re.match(TS, ":".join(a[:3]) + "," + a[3])) + o
                t1 = secs(re.match(TS, ":".join(b[:3]) + "," + b[3])) + o
                n += 1
                out.append(f"{n}\n{fmt(t0)} --> {fmt(t1)}\n" + "\n".join(lines[2:]))
        (HERE / f"subtitles.{lang}.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
        print(f"subtitles.{lang}.srt: {n} cues")


if __name__ == "__main__":
    main()
