#!/usr/bin/env python3
"""Time every vo.txt line (and sentence) on the eight Akash takes (assets/vo/rem_bNN.mp3) without Whisper.

Each take is aligned on its own sentences (every sentence ends in a pause, so this is more robust than whole lines:
13 of 81 line boundaries were uncertain at line level, 2 of 196 at sentence level) with scripts/align_script.py (more robust than one long file), then the takes are
joined into assets/vo/vo_full.wav with GAP seconds between them and every line time is shifted onto that timeline.
Writes align/align.json (line, en, start, end, confidence, block) and align/blocks.json (block offsets).
usage: python3 projects/rare-earth-magnets/tools/align_blocks.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent.parent
GAP = 0.6
sys.path.insert(0, str(HERE / "tools"))
from vo_blocks import blocks  # noqa: E402  (same split the owner recorded from)

out = HERE / "align"
out.mkdir(exist_ok=True)
lines, offsets, t, parts = [], [], 0.0, []
sentences = []
for i, b in enumerate(blocks, 1):
    mp3 = HERE / f"assets/vo/rem_b{i:02d}.mp3"
    sents, owner = [], []
    for li, l in enumerate(b):
        for x in re.split(r"(?<=[.?])\s+(?=[A-Z])", l):
            if x.strip():
                sents.append(x.strip()); owner.append(li)
    tsv = out / f"s{i:02d}.tsv"
    tsv.write_text("".join(f"{x}\n" for x in sents))  # English-only film: text in the first column
    subprocess.run([sys.executable, str(ROOT / "scripts/align_script.py"), str(mp3), str(tsv), "--out", str(out / f"s{i:02d}")],
                   check=True, capture_output=True)
    rows = json.loads((out / f"s{i:02d}/align.json").read_text())
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                               capture_output=True, text=True, check=True).stdout)
    first = len(lines)
    for li, l in enumerate(b):
        idx = [k for k, o in enumerate(owner) if o == li]
        lines.append({"line": len(lines) + 1, "en": l, "start": round(rows[idx[0]]["start"] + t, 3),
                      "end": round(rows[idx[-1]]["end"] + t, 3), "block": i,
                      "confidence": "high" if all(rows[k]["confidence"] == "high" for k in idx) else "check"})
    for k, r in enumerate(rows):
        sentences.append({"line": first + owner[k] + 1, "en": r["te"], "start": round(r["start"] + t, 3),
                          "end": round(r["end"] + t, 3), "confidence": r["confidence"]})
    offsets.append({"block": i, "start": round(t, 3), "duration": round(dur, 3)})
    parts.append(str(mp3))
    t += dur + GAP
(out / "sentences.json").write_text(json.dumps(sentences, indent=1))
(out / "align.json").write_text(json.dumps(lines, indent=1))
(out / "blocks.json").write_text(json.dumps(offsets, indent=1))
# joined master VO: each take, then GAP s of silence
inputs = sum([["-i", p] for p in parts], [])
filt = "".join(f"[{k}:a]aresample=48000,apad=pad_dur={GAP}[a{k}];" for k in range(len(parts)))
filt += "".join(f"[a{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", filt, "-map", "[o]", "-ac", "1",
                str(HERE / "assets/vo/vo_full.wav")], check=True)
low = [l for l in lines if l["confidence"] != "high"]
print(f"{len(lines)} lines, {t - GAP:.1f} s; low confidence: {[l['line'] for l in low]}")
