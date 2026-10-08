"""Time hand-corrected phrases against Whisper word timestamps.

Input (phrases file): one line per ASR segment window: `start<TAB>end<TAB>phrase | phrase | ...`
(times from the ASR; phrases are the corrected text, split where you want subtitle cuts).
Each window's ASR words are mapped by cumulative character share onto its phrases, so every cut
lands on a real word boundary. Output: transcript.te.tsv (start, end, text).
Usage: python tools/align_phrases.py phrases.tsv asr.json transcript.te.tsv
"""
import json
import sys


def main(phr_path, asr_path, out_path):
    words = [w for seg in json.load(open(asr_path, encoding="utf-8")) for w in seg["words"]]
    out = ["# start\tend\ttext   (seconds in assets/voiceover.mp3; Whisper large-v3 word timings, hand-corrected text;"
           " [?] = verify by ear)"]
    for line in open(phr_path, encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        s, e, text = line.rstrip("\n").split("\t")
        s, e = float(s), float(e)
        phrases = [p.strip() for p in text.split("|") if p.strip()]
        ws = [w for w in words if s - 0.05 <= (w["s"] + w["e"]) / 2 <= e + 0.05]
        if len(phrases) == 1 or len(ws) < 2:
            bounds = [s] + [s + (e - s) * sum(map(len, phrases[:i + 1])) / sum(map(len, phrases))
                            for i in range(len(phrases))]
        else:
            lens = [len(w["w"].strip()) + 1 for w in ws]
            total, cum = sum(lens), []
            for n in lens:
                cum.append((cum[-1] if cum else 0) + n)
            share, bounds, acc = sum(map(len, phrases)), [s], 0
            for p in phrases[:-1]:
                acc += len(p)
                j = min(range(len(ws)), key=lambda k: abs(cum[k] / total - acc / share))
                bounds.append(ws[j]["e"])
            bounds.append(e)
        for p, a, b in zip(phrases, bounds, bounds[1:]):
            out.append(f"{a:.2f}\t{b:.2f}\t{p}")
    open(out_path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote {out_path}: {len(out) - 1} lines")


if __name__ == "__main__":
    main(*sys.argv[1:4])
