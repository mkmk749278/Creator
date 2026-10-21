#!/usr/bin/env python3
"""Edit one full VO take: add the review's pauses and slow the lines that still read too fast (film 36).

Generic version of assemble_vo.py for a single full take (owner re-recorded the whole VO, 2026-10-21).
Line times come from `align_script.py`; a pause inside a line is placed at the measured silence nearest to where the
phrase should end (its share of the line's characters), and every choice is printed so it can be checked.
Cuts sit at silence midpoints; inserted room tone is digital silence (ElevenLabs pauses measure about -80 dB RMS). Inner pauses use d=0.10: some phrase-end pauses are only 0.10-0.14 s.

  python3 tools/edit_take.py voice/vo_v10_full_take2.mp3 align_take2/align.json voice/vo_v10_take2_edit
"""
import json
import re
import subprocess
import sys
import wave

import numpy as np

SR = 44100
SLOW = {3: 0.92, 15: 0.9}  # lines that read over ~215 wpm in both takes: pitch-safe atempo
# Line 15 reads at ~260 wpm in both full takes; the separately generated clip (speed 0.85) reads it at 220, x0.9 = 198.
REPLACE = {15: ("voice/fix_15.mp3", 0.0, 3.27)}
PAD = 0.22  # half a typical pause around a spliced clip that starts and ends on speech
# (line, phrase the pause follows or None for the end of the line, seconds) — edit_fixes.md
PAUSES = [
    (3, None, 1.0), (4, "keep at home...", 0.5), (4, "on-grid inverter...", 0.6), (6, None, 1.0),
    (7, "as a drummer...", 0.5), (8, None, 1.0), (11, "thirty volts...", 0.5), (11, "thousand volts...", 0.8),
    (11, None, 1.0), (12, None, 1.0), (14, None, 0.6), (15, None, 0.5), (16, None, 1.0), (18, None, 1.0),
    (21, None, 0.7), (22, "just say no...", 0.6), (22, None, 0.6),
]


def pcm(path):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.int16)


def stretch(x, tempo):
    if tempo == 1.0:
        return x
    cmd = ["ffmpeg", "-v", "error", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", "-af", f"atempo={tempo}",
           "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, input=x.tobytes(), capture_output=True, check=True).stdout, dtype=np.int16)


def silences(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                          "silencedetect=noise=-30dB:d=0.10", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(s, e))


def main(take, align_json, out):
    rows = json.load(open(align_json))
    rows = rows if isinstance(rows, list) else rows["lines"]
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", take],
                                 capture_output=True, text=True).stdout)
    sil = silences(take)
    src = pcm(take)
    # Cut points: every line boundary (midpoint of the pause between lines) plus inner pauses.
    cuts = {}  # time -> (seconds to insert, label)
    bounds = [0.0] + [(rows[i]["end"] + rows[i + 1]["start"]) / 2 for i in range(len(rows) - 1)] + [total]
    for line, phrase, sec in PAUSES:
        r = rows[line - 1]
        text = r.get("en") or r.get("te")
        if phrase is None:
            t, label = bounds[line], f"end of line {line}"
        else:
            i = text.index(phrase) + len(phrase)
            est = r["start"] + (r["end"] - r["start"]) * i / len(text)
            inner = [(a, b) for a, b in sil if r["start"] < a and b < r["end"]]
            a, b = min(inner, key=lambda g: abs((g[0] + g[1]) / 2 - est))
            t, label = (a + b) / 2, f'line {line} after "{phrase}" (est {est:.2f}, pause {a:.2f}-{b:.2f})'
        cuts[round(t, 3)] = (cuts.get(round(t, 3), (0, ""))[0] + sec, label)
        print(f"+{sec:.1f}s at {t:7.2f}  {label}")
    # Pieces between consecutive cut points / line bounds; slowed lines are re-read through atempo.
    points = sorted(set([round(b, 3) for b in bounds] + list(cuts)))
    parts, lines_out, t_out = [], {}, 0.0
    for a, b in zip(points, points[1:]):
        line = next(i + 1 for i in range(len(rows)) if bounds[i] - 1e-3 <= a < bounds[i + 1] - 1e-3)
        tempo = SLOW.get(line, 1.0)
        lo = lines_out.setdefault(line, [None, None])
        r = rows[line - 1]
        if line in REPLACE:
            if lo[0] is None:
                path, c0, c1 = REPLACE[line]
                clip = stretch(pcm(path)[int(round(c0 * SR)):int(round(c1 * SR))], tempo)
                seg = np.concatenate([np.zeros(int(PAD * SR), np.int16), clip, np.zeros(int(PAD * SR), np.int16)])
                lo[0], lo[1] = t_out + PAD, t_out + PAD + len(clip) / SR
            else:
                seg = np.zeros(0, np.int16)
        else:
            seg = stretch(src[int(round(a * SR)):int(round(b * SR))], tempo)
            if lo[0] is None and a <= r["start"] <= b:
                lo[0] = t_out + (r["start"] - a) / tempo
            if a <= r["end"] <= b:
                lo[1] = t_out + (r["end"] - a) / tempo
        parts.append(seg)
        t_out += len(seg) / SR
        if b in cuts:
            parts.append(np.zeros(int(round(cuts[b][0] * SR)), dtype=np.int16))
            t_out += cuts[b][0]
    audio = np.concatenate(parts)
    with wave.open(out + ".wav", "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(audio.tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-b:a", "192k", out + ".mp3"], check=True)
    lines = [{"line": n, "start": round(lines_out[n][0], 3), "end": round(lines_out[n][1], 3),
              "en": rows[n - 1].get("en") or rows[n - 1].get("te"), "tempo": SLOW.get(n, 1.0)} for n in sorted(lines_out)]
    json.dump(lines, open(out + ".lines.json", "w"), indent=1)
    print(f"{out}: {len(audio) / SR:.2f} s (take {total:.2f} s)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
