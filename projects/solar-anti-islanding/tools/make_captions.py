#!/usr/bin/env python3
"""Burned-in captions (ASS) + an SRT for YouTube, from the final edit's exact line times.

Each VO line is split into short phrases (≤ 42 characters, at punctuation first). Phrase times are shared out by
character count across the line, then each boundary snaps to the middle of the nearest real pause in the VO
(silencedetect, 0.10 s) when one lies within 0.45 s. No Whisper. Spoken forms become readable ones
(D.C. → DC, two hundred and thirty → 230 …).

  python3 projects/solar-anti-islanding/tools/make_captions.py   # writes captions.ass, captions_en.srt
"""
import json
import re
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
LINES = json.loads((PROJ / "align_take2/edit3_lines_exact.json").read_text())
VO = PROJ / "voice/vo_v10_take3_edit.mp3"
MAXC = 46
READ = [(r"\bD\.C\.", "DC"), (r"\bA\.C\.", "AC"), ("two hundred and thirty volts", "230 volts"),
        ("about eleven thousand volts", "about 11,000 volts"), ("fifty full swings", "50 full swings"),
        ("within two seconds", "within 2 seconds"), ("Two in the afternoon", "2 PM")]


def silences():
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(VO), "-af", "silencedetect=n=-35dB:d=0.10", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r)]
    return [(a + b) / 2 for a, b in zip(st, en)]


def phrases(text):
    for a, b in READ: text = re.sub(a, b, text)
    parts = re.split(r"(?<=[.?!…])\s+|\s+(?=—)|(?<=\.\.\.)\s+", text)
    out = []
    for p in parts:
        p = p.strip()
        stack = [p]
        while stack:                                           # split long phrases near the middle (a comma first)
            q = stack.pop(0)
            if len(q) <= MAXC: out.append(q); continue
            mid = len(q) / 2
            commas = [i for i, ch in enumerate(q) if ch == "," and 0.3 * len(q) < i < 0.75 * len(q)]
            cut = min(commas, key=lambda i: abs(i - mid)) + 1 if commas else min((i for i, ch in enumerate(q) if ch == " "), key=lambda i: abs(i - mid))
            stack[:0] = [q[:cut].strip(), q[cut:].strip()]
        p = ""
        if p: out.append(p)
    out = [p for p in out if p]
    merged = []                                                 # fold short tails ("reverse", "off") into a neighbour
    for p in out:
        if merged and (len(p) < 16 or len(merged[-1]) < 16) and len(merged[-1]) + 1 + len(p) <= 52: merged[-1] += " " + p
        else: merged.append(p)
    return merged


def ts(t, srt=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",") if srt else f"{h}:{m:02d}:{s:05.2f}"


def main():
    sil = silences()
    cues = []
    for l in LINES:
        ph = phrases(l["en"]); n = sum(len(p) for p in ph)
        t, a = l["start"], l["start"]
        for i, p in enumerate(ph):
            b = l["end"] if i == len(ph) - 1 else a + (l["end"] - l["start"]) * len(p) / n
            if i < len(ph) - 1:
                near = [s for s in sil if abs(s - b) < 0.45 and a + 0.6 < s < l["end"] - 0.6]
                if near: b = min(near, key=lambda s: abs(s - b))
            text = p.replace("...", "…")
            if text.endswith(".") and not text.endswith("…"): text = text[:-1]          # no full stop on a caption
            cues.append((a, b, text)); a = b
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,50,&H00FFFFFF,&H00FFFFFF,&H5A0D1117,&H5A0D1117,-1,0,0,0,100,100,0,0,3,14,0,2,80,80,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{ts(a)},{ts(b - 0.04)},Cap,,0,0,0,,{t}" for a, b, t in cues]
    (PROJ / "captions.ass").write_text(hdr + "\n".join(ev) + "\n")
    srt = [f"{i + 1}\n{ts(a, True)} --> {ts(b - 0.04, True)}\n{t}\n" for i, (a, b, t) in enumerate(cues)]
    (PROJ / "captions_en.srt").write_text("\n".join(srt))
    print(f"{len(cues)} cues; longest {max(len(t) for *_, t in cues)} chars; shortest {min(b - a for a, b, _ in cues):.2f} s")


if __name__ == "__main__":
    main()
