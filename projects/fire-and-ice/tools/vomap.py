"""Shared VO time map: part-relative line times -> programme time, with the fact-check cuts applied.

CUTS remove a stretch of a VO part (cut in the pauses at line-slot boundaries); `insert` seconds of silence replace it
(a VO_PAUSE beat for picture, music and on-screen text). Lines inside a cut are dropped everywhere (EDL, SRT).
Why each cut exists: fact-check.md (lines that are wrong and can't be fixed on screen without a re-record).
"""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent.parent
PARTS = ["voice/part1_v4.mp3", "voice/part2_v4.mp3", "voice/part3_v4.mp3"]
GAPS = [1.6, 1.2]  # section pauses after part 1 and part 2
CUTS = {  # part: [(start, end, insert_silence, why)]
    1: [(26.738, 29.947, 0.0, "P1 L7 'absolute rule of medical science': no such rule (fact-check C04)")],
    2: [(84.672, 95.164, 0.0, "P2 L16-17 invented 'Harvard papers: undeniable proof' quote (C29)")],
    3: [(102.523, 113.705, 6.5, "P3 L23 'undeniable evidence' overclaim (C48); replaced by a 6.5 s skeptic beat")],
}


def part_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(HERE / PARTS[p - 1])],
                                capture_output=True, text=True, check=True).stdout)


def removed_before(p, t):
    return sum(e - s - ins for s, e, ins, _ in CUTS.get(p, []) if e <= t + 1e-6)


def in_cut(p, t0, t1):
    return any(t0 >= s - 1e-3 and t1 <= e + 1e-3 for s, e, _, _ in CUTS.get(p, []))


def offsets():
    """Programme start of each part, after cuts."""
    off, t = [], 0.0
    for p in (1, 2, 3):
        off.append(round(t, 3))
        t += part_dur(p) - removed_before(p, 1e9)
        if p <= len(GAPS):
            t += GAPS[p - 1]
    return off, round(t, 3)


def prog(p, t, off=None):
    off = off or offsets()[0]
    return off[p - 1] + t - removed_before(p, t)
