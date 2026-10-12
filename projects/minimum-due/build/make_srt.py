#!/usr/bin/env python3
"""English subtitles for the whole film from the VO alignment (no Whisper; PLAYBOOK §7).

Each aligned line is cut into cues of at most two 42-character rows, split at sentence ends, then commas, then words;
a cue's time is its share of the line by character position (the same method as the scene cues).
Usage: python3 projects/minimum-due/build/make_srt.py [out.srt]
"""
import re, sys, textwrap
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from review_shots import vo_lines

MAX = 84   # two rows of 42


def pieces(text):
    out = []
    for sent in re.split(r"(?<=[.?])\s+", text.strip()):
        while len(sent) > MAX:
            cut = sent.rfind(", ", 0, MAX)
            cut = cut + 1 if cut > 30 else sent.rfind(" ", 0, MAX)
            out.append(sent[:cut].strip()); sent = sent[cut:].strip()
        if sent:
            out.append(sent)
    # merge very short neighbours so cues are not flashes
    merged = []
    for p in out:
        if merged and len(merged[-1]) + 1 + len(p) <= MAX and (len(p) < 22 or len(merged[-1]) < 22):
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged


def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "youtube/subtitles.en.srt"
    out.parent.mkdir(parents=True, exist_ok=True)
    cues = []
    for _, s, e, text in vo_lines():
        ps = pieces(text); total = sum(len(p) for p in ps); acc = 0
        for p in ps:
            a = s + (e - s) * acc / total; acc += len(p); b = s + (e - s) * acc / total
            cues.append((a, b, "\n".join(textwrap.wrap(p, 42))))
    out.write_text("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues, 1)), encoding="utf-8")
    print(out, len(cues), "cues")


if __name__ == "__main__":
    main()
