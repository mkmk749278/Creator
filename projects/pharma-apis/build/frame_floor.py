#!/usr/bin/env python3
"""Write every shot's start and end a hair BEFORE its frame (floor to 0.0001 s), never after.

A cut at frame 2366 is 78.866666... s; written as 78.867 (rounded up) the new shot had not started on that frame and
the old one had ended, so the empty background flashed for one frame (13 flashes found in the 30 Oct audit).
make_film.py writes shot times through ft(); this script applies the same rule to already generated parts.
usage: python3 projects/pharma-apis/build/frame_floor.py video/pha/p1/index.html [...]
"""
import math
import re
import sys

FPS = 30


def ft(frame):
    """frame index -> seconds, floored to 4 decimals so it never lands after the frame"""
    return math.floor(frame / FPS * 1e4) / 1e4


def fix(html):
    def pair(m):
        a, sk, dk = m.group(0), m.group("sk"), m.group("dk")
        s, d = float(m.group("s")), float(m.group("d"))
        fs, fe = round(s * FPS), round((s + d) * FPS)
        return a.replace(f'{sk}="{m.group("s")}"', f'{sk}="{ft(fs)}"').replace(f'{dk}="{m.group("d")}"', f'{dk}="{round(ft(fe) - ft(fs), 4)}"')
    pat = r'(?P<sk>data-(?:start|vs))="(?P<s>[\d.]+)"\s+(?P<dk>data-(?:duration|vd))="(?P<d>[\d.]+)"'
    return re.subn(pat, pair, html)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        h, n = fix(open(f).read())
        open(f, "w").write(h)
        print(f, n, "timings floored")
