#!/usr/bin/env python3
"""Check recorded VO takes before they go into a film, without any speech recognition (no Whisper; PLAYBOOK §7, §15).

Two failures this catches, both shipped once:
  1. A take that says a phrase twice. ElevenLabs sometimes repeats a phrase; the jet engine film went out with
     "past the speed of sound past the speed of sound" and "and survive for twenty-five years" twice (spliced re-takes).
     Sign: a sentence that takes far longer than its words, or a re-take longer than the line it replaces when the edit
     removed words.
  2. Speech cut off the end of a take. A trim that cut at the take's last *pause* dropped the last sentence of four
     pharma blocks, "Jai Hind" included. Sign: speech after the trim point, and the block's last sentences squeezed
     into too little time.

usage:
  python3 scripts/vo_take_check.py --sentences projects/<slug>/align/sentences.json
        [--takes 'projects/<slug>/voice/<prefix>_b*.mp3' --trimmed 'projects/<slug>/voice/t*.wav']
  sentences.json: a list of {line, en, start, end} (tools/align_blocks.py writes it). Exit 1 when anything is flagged:
  listen to every flagged line (the owner re-records the block; never splice a phrase in, PLAYBOOK §4a-2).
"""
import argparse
import glob
import json
import re
import statistics
import subprocess
import sys

SQUEEZED, STRETCHED, MIN_WORDS = 0.6, 1.6, 5     # pace vs the film's median seconds per word


def duration(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def loud_after(path, t):
    """seconds of speech-level audio after t (silencedetect at -38 dB)"""
    log = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{t:.3f}", "-i", path, "-af", "silencedetect=n=-38dB:d=0.15",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    rest = duration(path) - t
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    silent = sum((ends[i] if i < len(ends) else rest) - s for i, s in enumerate(starts))
    return max(0.0, rest - silent)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sentences", required=True)
    ap.add_argument("--takes", help="glob of the raw takes, in block order")
    ap.add_argument("--trimmed", help="glob of the trimmed takes the film uses, same order")
    a = ap.parse_args()
    flags = []

    rows = []
    for s in json.load(open(a.sentences)):
        w = len(re.findall(r"[A-Za-z0-9']+", s["en"]))
        if w:
            rows.append((s, w, (s["end"] - s["start"]) / w))
    med = statistics.median(p for _, _, p in rows)
    print(f"{len(rows)} sentences, median {med:.3f} s a word")
    for s, w, p in rows:
        if w >= MIN_WORDS and (p < med * SQUEEZED or p > med * STRETCHED):
            kind = "squeezed: audio missing?" if p < med * SQUEEZED else "stretched: a repeated phrase or a long pause?"
            flags.append(f"L{s['line']} at {s['start']:.1f}s, {p / med:.2f}x the median pace ({kind}): {s['en'][:80]}")

    if a.takes and a.trimmed:
        for raw, cut in zip(sorted(glob.glob(a.takes)), sorted(glob.glob(a.trimmed))):
            lost = loud_after(raw, duration(cut))
            if lost > 0.3:
                flags.append(f"{raw}: {lost:.1f}s of speech after the trim point (cut at {duration(cut):.2f}s)")

    for f in flags:
        print("FLAG", f)
    print("OK" if not flags else f"{len(flags)} flag(s): listen before the film uses these takes")
    sys.exit(1 if flags else 0)


if __name__ == "__main__":
    main()
