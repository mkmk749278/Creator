#!/usr/bin/env python3
"""Insert silent beats into a recorded voiceover at its own pauses (edit-room pacing fix, PLAYBOOK §7).

  python3 scripts/insert_pauses.py VOICE.mp3 CUTS.json OUT.wav [--slots align/slots.csv --slots-out align/slots_edit.csv]

CUTS.json: [{"at": 44.484, "add": 0.6, "why": "..."}, ...] with `at` in the ORIGINAL file's seconds, inside a pause
(silencedetect). Each cut splits the audio there and inserts `add` seconds of silence, so no word is touched.
With --slots, every time column of an align_script.py slots.csv is shifted onto the edited timeline.
"""
import argparse, csv, json, subprocess


def shift(t, cuts):
    return t + sum(c["add"] for c in cuts if c["at"] <= t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice"); ap.add_argument("cuts"); ap.add_argument("out")
    ap.add_argument("--slots"); ap.add_argument("--slots-out")
    a = ap.parse_args()
    cuts = sorted(json.load(open(a.cuts)), key=lambda c: c["at"])
    edges = [0.0] + [c["at"] for c in cuts]
    parts, labels = [], []
    for i, start in enumerate(edges):
        end = edges[i + 1] if i + 1 < len(edges) else None
        trim = f"atrim=start={start}" + (f":end={end}" if end is not None else "")
        parts.append(f"[0:a]{trim},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=mono[s{i}]")
        labels.append(f"[s{i}]")
        if end is not None:
            parts.append(f"anullsrc=r=48000:cl=mono,atrim=duration={cuts[i]['add']}[z{i}]"); labels.append(f"[z{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", a.voice, "-filter_complex", fc,
                    "-map", "[o]", "-ar", "48000", "-ac", "1", a.out], check=True)
    print(f"{len(cuts)} beats, +{sum(c['add'] for c in cuts):.2f} s -> {a.out}")
    if a.slots:
        rows = list(csv.DictReader(open(a.slots)))
        tcols = [k for k in ("picture_start", "picture_end", "speech_start", "speech_end") if k in rows[0]]
        for r in rows:
            for k in tcols:
                r[k] = f"{shift(float(r[k]), cuts):.3f}"
        with open(a.slots_out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        print(f"shifted {len(rows)} rows -> {a.slots_out}")


if __name__ == "__main__":
    main()
