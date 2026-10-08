#!/usr/bin/env python3
"""Deterministic silence-to-script alignment: time every script line on the voiceover without Whisper (PLAYBOOK §7).

The script is the source of truth and is already in spoken order, so there is nothing to transcribe or translate:
we only need where each line starts and ends. FFmpeg `silencedetect` finds the pauses; each script line is then
mapped to a run of consecutive speech chunks. Pauses inside a sentence and sentences with no pause between them
mean chunk count != line count (breath-hold: 116 chunks at d=0.35 for 80 lines), so a 1:1 mapping drifts. Instead a
dynamic programme picks which pauses are line boundaries: each line's speech time should match its share of the
script's characters, and longer pauses are preferred as boundaries. Every line gets a confidence; low ones are listed
for a quick listen.

  python3 scripts/align_script.py VOICE.mp3 SCRIPT.tsv --out projects/<slug>/align

SCRIPT.tsv: one spoken line per row, tab-separated `te<TAB>en` (header optional; `en` optional, plain text works too).
Lines starting with `#` are ignored. Split long sentences into separate rows where you want subtitle cuts.
Writes align.json (line, te, en, start, end, confidence), subtitles.te.srt, subtitles.en.srt (English text timed to
the Telugu audio, one cue per line: no SOV/SVO drift) and align.md (lines to check by ear).
"""
import argparse
import csv
import json
import math
import re
import subprocess
import sys
from pathlib import Path


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True, check=True).stdout)


def silences(path, noise, d):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
                          f"silencedetect=noise={noise}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def read_script(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.reader(f, delimiter="\t"):
            if not r or not r[0].strip() or r[0].lstrip().startswith("#"):
                continue
            if not rows and [c.strip().lower() for c in r[:2]] in (["te", "en"], ["te"]):
                continue
            rows.append({"te": r[0].strip(), "en": r[1].strip() if len(r) > 1 else ""})
    return rows


def weight(text):
    # Spoken-length proxy: letters and digits (Telugu combining marks count; punctuation and spaces don't).
    return max(1, sum(ch.isalnum() or 0x0C00 <= ord(ch) <= 0x0C7F for ch in text))


def align(total, gaps, lines, gap_bonus):
    """gaps: [(start, end)] pauses inside (0, total). Returns [(start, end, cost)] per line."""
    gaps = [(max(0.0, s), min(total, e if e is not None else total)) for s, e in gaps]
    lead = gaps[0][1] if gaps and gaps[0][0] <= 0.05 else 0.0           # silence before the first word
    trail = gaps[-1][0] if gaps and gaps[-1][1] >= total - 0.05 else total
    inner = [g for g in gaps if g[0] > lead + 0.05 and g[1] < trail - 0.05]
    # Candidate boundaries: every inner pause. Node 0 = speech start, node k = pause k, last = speech end.
    nodes = [(lead, lead, 0.0)] + [(s, e, e - s) for s, e in inner] + [(trail, trail, 0.0)]
    n, L = len(nodes), len(lines)
    if L > n - 1:
        sys.exit(f"{L} script lines but only {n - 1} speech chunks: lower --min-pause or merge script rows")
    speech_at = [0.0] * n  # cumulative speech time (pauses excluded) at each node's start
    for k in range(1, n):
        speech_at[k] = speech_at[k - 1] + (nodes[k][0] - nodes[k - 1][1])
    w = [weight(l["te"]) for l in lines]
    # Punctuation inside a line (not its last mark) is where the speaker usually pauses.
    punct = [len(re.findall(r"[,.;:?!।—–]+(?=\s+\S)", l["te"])) for l in lines]
    rate = speech_at[-1] / sum(w)
    cum_w = [0]
    for x in w:
        cum_w.append(cum_w[-1] + x)
    INF = float("inf")
    # cost[i][k]: best cost with line i ending at node k. Lines map to consecutive node spans (k_prev, k].
    cost = [[INF] * n for _ in range(L + 1)]
    back = [[-1] * n for _ in range(L + 1)]
    cost[0][0] = 0.0
    for i in range(1, L + 1):
        exp = w[i - 1] * rate
        drift_ok = 0.25 * speech_at[-1]  # prune: a line can't sit far from its expected place in the script
        for k in range(i, n - (L - i)):
            if abs(speech_at[k] - cum_w[i] * rate) > drift_ok:
                continue
            best, arg = INF, -1
            for j in range(i - 1, k):
                if cost[i - 1][j] == INF:
                    continue
                dur = speech_at[k] - speech_at[j]
                inner_pauses = k - j - 1
                c = (cost[i - 1][j] + COST(dur, exp)
                     + PUNCT_MISS * max(0, punct[i - 1] - inner_pauses)
                     + PUNCT_EXTRA * max(0, inner_pauses - punct[i - 1]))
                if c < best:
                    best, arg = c, j
            if arg >= 0:
                bonus = 0.0 if k == n - 1 else gap_bonus * math.log1p(nodes[k][2] / 0.25)
                cost[i][k], back[i][k] = best - bonus, arg
    if cost[L][n - 1] == INF:
        sys.exit("no alignment found: check the script matches the audio")
    spans, k = [], n - 1
    for i in range(L, 0, -1):
        j = back[i][k]
        spans.append((j, k))
        k = j
    spans.reverse()

    def line_cost(i, j, k):
        dur = speech_at[k] - speech_at[j]
        inner = k - j - 1
        return (COST(dur, w[i] * rate) + PUNCT_MISS * max(0, punct[i] - inner)
                + PUNCT_EXTRA * max(0, inner - punct[i]) - (0.0 if k == n - 1 else gap_bonus * math.log1p(nodes[k][2] / 0.25)))

    # How sure is each boundary? Compare with moving it one pause earlier/later (both neighbours re-costed).
    margin = [9.9] * L
    for i in range(L - 1):
        (j, k), (_, k2) = spans[i], spans[i + 1]
        here = line_cost(i, j, k) + line_cost(i + 1, k, k2)
        for alt in (k - 1, k + 1):
            if j < alt < k2:
                d = line_cost(i, j, alt) + line_cost(i + 1, alt, k2) - here
                margin[i] = min(margin[i], d)
                margin[i + 1] = min(margin[i + 1], d)
    out = []
    for i, (j, k) in enumerate(spans):
        start = nodes[j][1] if j else lead
        end = nodes[k][0]
        dur = speech_at[k] - speech_at[j]
        ratio = dur / (w[i] * rate)
        out.append((round(start, 3), round(end, 3), round(ratio, 2), round(margin[i], 3)))
    return out


def _log_cost(dur, exp):
    return math.log((dur + 0.3) / (exp + 0.3)) ** 2


COST = _log_cost
# Tuned on the breath-hold VO (80 lines vs hand-checked onsets): 75/80 starts within 0.15 s, max error 0.94 s.
PUNCT_MISS, PUNCT_EXTRA = 0.1, 0.02


def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(path, cues):
    with open(path, "w") as f:
        for n, (s, e, text) in enumerate(cues, 1):
            f.write(f"{n}\n{srt_time(s)} --> {srt_time(e)}\n{text}\n\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("voice", type=Path)
    ap.add_argument("script", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--noise", type=float, default=-30.0, help="silencedetect threshold in dB")
    ap.add_argument("--min-pause", type=float, default=0.15, help="shortest pause that can be a line boundary (s)")
    ap.add_argument("--gap-bonus", type=float, default=0.35, help="preference for longer pauses as boundaries")
    ap.add_argument("--margin", type=float, default=0.05, help="flag lines whose boundary could move one pause")
    ap.add_argument("--hold", type=float, default=0.25, help="keep each cue on screen this long into the next pause")
    a = ap.parse_args()
    lines = read_script(a.script)
    if not lines:
        sys.exit("empty script")
    total = duration(a.voice)
    timed = align(total, silences(a.voice, a.noise, a.min_pause), lines, a.gap_bonus)
    a.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, (l, (s, e, ratio, margin)) in enumerate(zip(lines, timed), 1):
        conf = "high" if 0.7 <= ratio <= 1.4 and margin >= a.margin else "check"
        rows.append({"line": i, "start": s, "end": e, "te": l["te"], "en": l["en"], "speech_vs_text": ratio,
                     "boundary_margin": margin, "confidence": conf})
    (a.out / "align.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    # Cues hold a little into the following pause (never past the next line's start) so they don't flash off.
    def cues(key):
        res = []
        for i, r in enumerate(rows):
            nxt = rows[i + 1]["start"] if i + 1 < len(rows) else total
            res.append((r["start"], min(r["end"] + a.hold, nxt), r[key]))
        return res
    write_srt(a.out / "subtitles.te.srt", cues("te"))
    if any(r["en"] for r in rows):
        write_srt(a.out / "subtitles.en.srt", cues("en"))
    check = [r for r in rows if r["confidence"] != "high"]
    md = [f"# Script alignment: {len(rows)} lines, {total:.1f} s audio", "",
          f"{len(rows) - len(check)} lines high confidence; {len(check)} to check by ear "
          "(speech time far from the line's text length, or a boundary that could sit one pause earlier/later).", ""]
    if check:
        md += ["| Line | Start | End | Speech/text | Margin | Text |", "|---|---|---|---|---|---|"]
        md += [f"| {r['line']} | {r['start']:.2f} | {r['end']:.2f} | {r['speech_vs_text']} | {r['boundary_margin']} | {r['te'][:60]} |"
               for r in check]
    (a.out / "align.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:3]))


if __name__ == "__main__":
    main()
