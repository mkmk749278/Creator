#!/usr/bin/env python3
"""Word timings for the VO, without Whisper (CLAUDE.md): inside each aligned line (timing.py), FFmpeg silencedetect finds
the short pauses; each pause is pinned to the nearest punctuation break (. , ? ...) by the text's character position;
words between two anchors share the time by their length (letters + a small constant). Typical error a few tenths of
a second, enough to land a doodle item on the word that names it and to review every frame against what is heard.

  python3 build/words.py            # writes build/words.json and prints a check
  from words import P               # P("C011", "ten thousand") -> film seconds of that phrase's first word
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P_ = HERE.parent
sys.path.insert(0, str(HERE))
from timing import _T, TEXT, BLOCK, OFF   # noqa: E402

OUT = HERE / "words.json"


def line_texts():
    """VO text per row id (C001..): align.json keeps the spoken English in its 'te' field."""
    return dict(TEXT)


def pauses(block, a, b):
    """Internal pauses (start, end) in block-file seconds between a and b."""
    f = P_ / f"voice/block{block}.mp3"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(f), "-af",
                        "silencedetect=noise=-34dB:d=0.11", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return [(a + x, a + y) for x, y in zip(s, e) if a + y < b - 0.05 and a + x > a + 0.05]


def weight(w):
    return len(re.sub(r"[^A-Za-z0-9]", "", w)) + 1.5


def build():
    texts, out = line_texts(), []
    for key, (s, e) in sorted(_T.items(), key=lambda kv: kv[1][0]):
        block = BLOCK[key]; off = OFF[block]
        words = texts[key].split()
        cum, tot = [0.0], 0.0
        for w in words:
            tot += weight(w); cum.append(tot)
        # punctuation breaks: index i = break after word i
        breaks = [i + 1 for i, w in enumerate(words[:-1]) if re.search(r"[.,?;:]$|\.\.\.$", w)]
        ps = pauses(block, s - off, e - off)
        # anchors: (word index, time) ; start and end of the line, plus each pause pinned to the nearest unused break
        speech = (e - s) - sum(b - a for a, b in ps)
        anchors = [(0, s)]
        used = set()
        for a, b in ps:
            # expected text fraction at this pause = speech time before it / total speech
            before = (a - (s - off)) + 0 - sum(min(pb, a) - pa for pa, pb in ps if pa < a and pb <= a)
            frac = max(0.0, min(1.0, before / max(speech, 0.1)))
            cand = [i for i in breaks if i not in used]
            if not cand:
                continue
            i = min(cand, key=lambda i: abs(cum[i] / tot - frac))
            if abs(cum[i] / tot - frac) > 0.18:
                continue
            used.add(i); anchors.append((i, (a + off, b + off)))
        anchors.append((len(words), e))
        anchors.sort(key=lambda x: x[0])
        # walk segments between anchors
        seg_starts = []
        prev_i, prev_t = 0, s
        times = [None] * len(words)
        for i, t in anchors[1:]:
            t0 = prev_t
            t1 = t[0] if isinstance(t, tuple) else t
            span = cum[i] - cum[prev_i] or 1
            for k in range(prev_i, i):
                times[k] = (t0 + (t1 - t0) * (cum[k] - cum[prev_i]) / span, t0 + (t1 - t0) * (cum[k + 1] - cum[prev_i]) / span)
            prev_i, prev_t = i, (t[1] if isinstance(t, tuple) else t)
        for k, w in enumerate(words):
            out.append(dict(line=key, i=k, word=w, start=round(times[k][0], 2), end=round(times[k][1], 2)))
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=0))
    return out


_W = None


def W():
    global _W
    if _W is None:
        _W = json.loads(OUT.read_text()) if OUT.exists() else build()
    return _W


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).split()


def P(line, phrase, n=1):
    """Film time of the n-th occurrence of `phrase` (its first word) in VO line `line`."""
    ws = [w for w in W() if w["line"] == line]
    target = norm(phrase)
    toks = [norm(w["word"])[0] if norm(w["word"]) else "" for w in ws]
    hits = [k for k in range(len(toks)) if toks[k:k + len(target)] == target]
    if len(hits) < n:
        raise KeyError(f"'{phrase}' not in line {line}: {' '.join(w['word'] for w in ws)}")
    return ws[hits[n - 1]]["start"]


def said(t0, t1):
    """Words heard between film times t0 and t1."""
    return " ".join(w["word"] for w in W() if w["end"] > t0 and w["start"] < t1)


if __name__ == "__main__":
    ws = build()
    print(len(ws), "words")
    for k in ("C001", "C040", "C080"):
        print(k, " ".join(f"{w['word']}@{w['start']:.1f}" for w in ws if w["line"] == k))
