"""Subtitles from a corrected transcript.

Step 1 (auto): split ASR word timings into caption-sized cues.
  python scripts/make_srt.py split asr_raw.json cues.json
Step 2 (human/Claude): fix the text of each cue in cues.json (times stay).
Or: python scripts/make_srt.py tsv cues.json sentences_a.tsv [sentences_b.tsv ...]
Step 3: write SRT in video time (shifted by the live pauses).
  python scripts/make_srt.py srt cues.json pause_map.json out.srt
"""

import json
import sys

MAX_CHARS = 46
MAX_DUR = 5.5


def split(asr_path, out_path):
    segs = json.load(open(asr_path, encoding="utf-8"))
    words = [w for s in segs for w in s["words"]]
    cues, cur = [], []

    def flush():
        if cur:
            cues.append({"start": round(cur[0]["s"], 2), "end": round(cur[-1]["e"], 2),
                         "text": "".join(w["w"] for w in cur).strip()})
            cur.clear()

    for i, w in enumerate(words):
        text = "".join(x["w"] for x in cur) + w["w"]
        gap = w["s"] - cur[-1]["e"] if cur else 0
        if cur and (len(text.strip()) > MAX_CHARS or w["e"] - cur[0]["s"] > MAX_DUR or gap > 0.45):
            flush()
        cur.append(w)
        if w["w"].strip().endswith(("?", ".", "!")):
            flush()
    flush()
    json.dump(cues, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(cues)} cues")


def from_tsv(out_path, *tsv_paths):
    """Corrected sentences (start<TAB>end<TAB>text) -> caption cues. Long sentences are split at
    punctuation (or spaces) into cues of <= MAX_CHARS, timed in proportion to their length."""
    import re
    cues = []
    for p in tsv_paths:
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            a, b, text = line.rstrip("\n").split("\t")
            a, b = float(a), float(b)
            parts = [x.strip() for x in re.split(r"(?<=[,.?!])\s+", text) if x.strip()]
            chunks = []
            for x in parts:  # merge short clauses, break long ones at spaces
                if chunks and len(chunks[-1]) + len(x) + 1 <= MAX_CHARS:
                    chunks[-1] += " " + x
                    continue
                while len(x) > MAX_CHARS:
                    k = x.rfind(" ", 0, MAX_CHARS)
                    k = k if k > 10 else MAX_CHARS
                    chunks.append(x[:k].strip()); x = x[k:].strip()
                chunks.append(x)
            # never leave a tiny orphan cue: fold it into its neighbour
            merged = []
            for c in chunks:
                if merged and (len(c) < 14 or len(merged[-1]) < 14) and len(merged[-1]) + len(c) < MAX_CHARS + 14:
                    merged[-1] += " " + c
                else:
                    merged.append(c)
            chunks = merged
            total = sum(len(c) for c in chunks)
            t = a
            for c in chunks:
                d = (b - a) * len(c) / total
                cues.append({"start": round(t, 2), "end": round(t + d, 2), "text": c})
                t += d
    json.dump(cues, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(cues)} cues")


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def srt(cues_path, pmap_path, out_path):
    cues = json.load(open(cues_path, encoding="utf-8"))
    pauses = json.load(open(pmap_path))["pauses"]
    sh = lambda t: t + sum(p["len"] for p in pauses if p["at"] <= t)
    lines = []
    for i, c in enumerate(cues, 1):
        s, e = sh(c["start"]), sh(c["end"])
        if i < len(cues):
            e = min(e + 0.25, sh(cues[i]["start"]) - 0.04)  # linger a little, never overlap
        lines += [str(i), f"{ts(s)} --> {ts(e)}", c["text"], ""]
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {out_path}: {len(cues)} cues")


if __name__ == "__main__":
    {"split": split, "srt": srt, "tsv": from_tsv}[sys.argv[1]](*sys.argv[2:])
