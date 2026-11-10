#!/usr/bin/env python3
"""Lock the owner-approved joined VO and time every sentence and word on it (PLAYBOOK §6.6, §6.7).

Unlike vo_timing.py this never re-joins or re-trims the takes: the file the owner approved is the film's audio, byte
for byte (its SHA-256 goes into the lock). No transcription: the locked script is the truth, only timings are needed.
1. Sentences of vo.txt are placed with the silence-to-script aligner (align_script.align).
2. Inside a sentence, clause boundaries snap to nearby pauses and words spread by spoken length (vo_timing helpers).
3. Chapters start at the sentence whose text begins with each prefix in chapters.tsv (`prefix<TAB>title`).

Usage: scripts/vo_lock.py projects/<slug> --audio projects/<slug>/assets/vo/<prefix>_vo_full.mp3 [--fps 60] [--outro 4]
Optional vo/sentence_fix.tsv (`sentence prefix<TAB>start<TAB>end`, seconds): sentences the aligner misplaced,
set by hand from the silences around them (never from speech recognition); listed in timing.md.
Optional vo/caption_forms.tsv (`spoken<TAB>written`, applied in order to the SRT only): the real forms for captions
(digits, ₹, ISRO, true spellings of respelt names), PLAYBOOK §6; a row that matches nothing stops the run.
Writes projects/<slug>/vo/: timing.json (sentences, words, chapters; seconds and frames), captions.en.srt,
timing.md (sentences to check), lock.json (audio name, SHA-256, duration, approval). Also writes
assets/vo/vo_full.wav (48 kHz mono, same audio, for Remotion).
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from align_script import align, silences  # noqa: E402
from vo_timing import dur, time_sentence  # noqa: E402


def split_sentences(vo: str) -> list[str]:
    out = []
    for para in vo.split("\n"):
        para = para.strip()
        if para and not para.startswith("#"):
            out += [s.strip() for s in re.split(r"(?<=[.?])\s+(?=[A-Z0-9])", para) if s.strip()]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("film", type=Path)
    ap.add_argument("--audio", type=Path, required=True)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--approved", default="", help="who approved and when, e.g. 'owner, 2026-11-06'")
    ap.add_argument("--outro", type=float, default=0.0, help="seconds of picture after the voice (end card); the mix pads to match")
    a = ap.parse_args()
    film, fps = a.film, a.fps
    out = film / "vo"
    out.mkdir(exist_ok=True)
    sents = split_sentences((film / "vo.txt").read_text(encoding="utf-8"))
    chap_rows = [l.split("\t", 1) for l in (out / "chapters.tsv").read_text().splitlines() if "\t" in l]

    total = dur(a.audio)
    gaps = [(x, y if y is not None else total) for x, y in silences(a.audio, -35, 0.08)]
    spans = align(total, [g for g in gaps if g[1] - g[0] >= 0.15], [{"te": s, "en": ""} for s in sents], 0.35)

    fix_path = out / "sentence_fix.tsv"
    fixes = [l.split("\t") for l in fix_path.read_text().splitlines() if l.count("\t") == 2] if fix_path.exists() else []
    for pre, fs, fe in fixes:
        hits = [i for i, x in enumerate(sents) if x.startswith(pre)]
        if len(hits) != 1:
            sys.exit(f"sentence_fix prefix must match one sentence: {pre}")
        ss, se, ratio, margin = spans[hits[0]]
        spans[hits[0]] = (float(fs), float(fe), ratio, 9.9)
    timing = {"fps": fps, "audio": a.audio.name, "sentences": [], "words": [], "chapters": []}
    ci = 0
    for sid, (sent, (ss, se, ratio, margin)) in enumerate(zip(sents, spans)):
        if ci < len(chap_rows) and sent.startswith(chap_rows[ci][0]):
            timing["chapters"].append({"title": chap_rows[ci][1].strip(), "start": round(ss, 3)})
            ci += 1
        chapter = timing["chapters"][-1]["title"] if timing["chapters"] else ""
        timing["sentences"].append({"id": sid, "chapter": chapter, "text": sent, "start": round(ss, 3),
                                    "end": round(se, 3), "ratio": ratio, "margin": margin})
        for w in time_sentence(sent, ss, se, gaps):
            timing["words"].append({"s": sid, "w": w["w"], "start": w["start"], "end": w["end"]})
    if ci != len(chap_rows):
        sys.exit(f"chapter prefix not found in order: {chap_rows[ci][0]}")
    timing["duration"] = round(total, 3)
    timing["voDurationInFrames"] = round(total * fps)
    timing["outro"] = a.outro
    timing["durationInFrames"] = round((total + a.outro) * fps)  # the film: voice plus the end card
    for key in ("sentences", "words", "chapters"):
        for x in timing[key]:
            for k in ("start", "end"):
                if k in x:
                    x[k + "Frame"] = round(x[k] * fps)
    (out / "timing.json").write_text(json.dumps(timing, indent=0, ensure_ascii=False))

    def srt(t: float) -> str:
        ms = round(t * 1000)
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    S = timing["sentences"]
    forms_path = out / "caption_forms.tsv"
    forms = [l.split("\t") for l in forms_path.read_text(encoding="utf-8").splitlines() if l.count("\t") == 1] \
        if forms_path.exists() else []
    shown = [x["text"] for x in S]
    for spoken, written in forms:
        if not any(spoken in t for t in shown):
            sys.exit(f"caption_forms row matches no sentence: {spoken}")
        shown = [t.replace(spoken, written) for t in shown]
    cues = [f"{i}\n{srt(x['start'])} --> {srt(min(x['end'] + 0.2, S[i]['start'] if i < len(S) else total))}\n"
            f"{shown[i - 1]}\n" for i, x in enumerate(S, 1)]
    (out / "captions.en.srt").write_text("\n".join(cues), encoding="utf-8")
    fixed = {f[0] for f in fixes}
    weak = [x for x in S if not any(x["text"].startswith(f) for f in fixed)
            and (x["margin"] < 0.05 or not 0.6 < x["ratio"] < 1.6)]
    rep = [f"# VO timing: {film.name}", "", f"{total:.2f} s · {len(S)} sentences · {len(timing['words'])} words · "
           f"{len(timing['chapters'])} chapters", "", "## Chapters"]
    rep += [f"- {int(c['start'] // 60):02d}:{int(c['start'] % 60):02d} {c['title']}" for c in timing["chapters"]]
    rep += ["", f"## Set by hand (vo/sentence_fix.tsv): {len(fixes)}"] + [f"- {f[1]}–{f[2]} s: {f[0]}" for f in fixes]
    rep += ["", "## Sentences to check (low margin or odd length)"]
    rep += [f"- {x['start']:.2f}s ratio {x['ratio']} margin {x['margin']}: {x['text'][:70]}" for x in weak] or ["- none"]
    (out / "timing.md").write_text("\n".join(rep) + "\n")

    wav = a.audio.parent / "vo_full.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(a.audio), "-ac", "1", "-ar", "48000", str(wav)], check=True)
    lock = {"audio": a.audio.name, "sha256": hashlib.sha256(a.audio.read_bytes()).hexdigest(),
            "duration": round(total, 3), "approved": a.approved, "wav": wav.name,
            "wav_duration": round(dur(wav), 3)}
    (out / "lock.json").write_text(json.dumps(lock, indent=1) + "\n")
    print("\n".join(rep[:3 + len(timing["chapters"]) + 3 + len(fixes)]))
    print(f"{len(weak)} sentences to check; lock: {lock['sha256'][:12]}")


if __name__ == "__main__":
    main()
