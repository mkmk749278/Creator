#!/usr/bin/env python3
"""Music bed + ambience cuts for Fire and Ice.

  python3 tools/make_bed.py   -> assets/audio/bgm_bed.wav (programme length, fades), assets/audio/amb_monks_cut.wav

Bed: "Cinematic Ambient" by Matio888 (Freesound 795808, CC BY 4.0), one continuous 6:55 track, so the music never
restarts. It is ducked under the VO in assemble.py. Ambience: 10 s of kevp888's Himalaya Buddhist monks recording
(Freesound 440226, CC BY) under the section break into Part 2.
"""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent.parent
A = HERE / "assets" / "audio"


def main():
    import csv
    total = sum(float(r["dur"]) for r in csv.DictReader((HERE / "edl.csv").open()))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(A / "bgm_matio.mp3"), "-af",
                    f"atrim=0:{total:.3f},afade=t=in:d=2.5,afade=t=out:st={total - 5:.3f}:d=5,aresample=48000",
                    "-ac", "2", str(A / "bgm_bed.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "362", "-t", "10", "-i", str(A / "amb_monks.mp3"), "-af",
                    "afade=t=in:d=0.8,afade=t=out:st=8:d=2,aresample=48000", "-ac", "2", str(A / "amb_monks_cut.wav")], check=True)
    print(f"bed {total:.1f} s")


if __name__ == "__main__":
    main()
