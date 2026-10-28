#!/usr/bin/env python3
"""Time every vo.txt line (and sentence) on the eight Akash takes (voice/pha_bNN.mp3) without Whisper.

Same method as the rare-earth film: each take's trailing silence is trimmed to 0.25 s, each take is aligned on its own
sentences with scripts/align_script.py, then the takes are joined into voice/vo_full.wav with GAP seconds between them
and every time is shifted onto that timeline. Blocks come from scripts/vo_blocks.py (the split the owner recorded from).
Writes align/align.json (line, en, start, end, confidence, block), align/sentences.json, align/blocks.json and
align/subtitles.en.srt (one cue per sentence).
usage: python3 projects/pharma-apis/tools/align_blocks.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent.parent
GAP = 0.7
sys.path.insert(0, str(ROOT / "scripts"))
from vo_blocks import split_blocks  # noqa: E402

def run(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)

def duration(p):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)).stdout)

def trimmed(mp3, wav):
    """Cut the take 0.25 s after its last pause starts, so every block join gets the same GAP."""
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp3), "-af", "silencedetect=n=-45dB:d=0.2", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    d = duration(mp3)
    cut = starts[-1] + 0.25 if starts and d - starts[-1] > 0.45 else d
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-t", f"{cut:.3f}",
        "-af", f"afade=t=out:st={max(0, cut - 0.08):.3f}:d=0.08", "-ar", "48000", "-ac", "1", str(wav))
    return cut

def srt_time(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

vo_lines = [l.strip() for l in (HERE / "vo.txt").read_text().splitlines() if l.strip()]
blocks = split_blocks(vo_lines, 1490)
out = HERE / "align"; out.mkdir(exist_ok=True)
voice = HERE / "voice"
lines, sentences, offsets, wavs, t = [], [], [], [], 0.0
for i, b in enumerate(blocks, 1):
    mp3 = voice / f"pha_b{i:02d}.mp3"
    wav = voice / f"t{i:02d}.wav"
    dur = trimmed(mp3, wav)
    sents, owner = [], []
    for li, l in enumerate(b):
        for x in re.split(r"(?<=[.?])\s+(?=[A-Z])", l):
            if x.strip():
                sents.append(x.strip()); owner.append(li)
    tsv = out / f"s{i:02d}.tsv"
    tsv.write_text("".join(f"{x}\n" for x in sents))
    run(sys.executable, str(ROOT / "scripts/align_script.py"), str(wav), str(tsv), "--out", str(out / f"s{i:02d}"))
    rows = json.loads((out / f"s{i:02d}/align.json").read_text())
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
    wavs.append(wav)
    t += dur + GAP
(out / "align.json").write_text(json.dumps(lines, indent=1))
(out / "sentences.json").write_text(json.dumps(sentences, indent=1))
(out / "blocks.json").write_text(json.dumps(offsets, indent=1))
with open(out / "subtitles.en.srt", "w") as f:
    for n, s in enumerate(sentences, 1):
        nxt = sentences[n]["start"] if n < len(sentences) else s["end"] + 0.3
        end = nxt if nxt - s["end"] <= 1.0 else s["end"] + 0.3
        f.write(f"{n}\n{srt_time(s['start'])} --> {srt_time(end)}\n{s['en']}\n\n")
inputs = sum([["-i", str(w)] for w in wavs], [])
filt = "".join(f"[{k}:a]apad=pad_dur={GAP}[a{k}];" for k in range(len(wavs) - 1)) + f"[{len(wavs)-1}:a]anull[a{len(wavs)-1}];"
filt += "".join(f"[a{k}]" for k in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1[o]"
run("ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", filt, "-map", "[o]", "-ac", "1", str(voice / "vo_full.wav"))
low = [l["line"] for l in lines if l["confidence"] != "high"]
print(f"{len(lines)} lines, {t - GAP:.1f} s; low-confidence lines: {low}")
