#!/usr/bin/env python3
"""Join the three VO parts into one programme voiceover with section pauses, and write vo_map.json.

  python3 tools/build_vo.py      -> assets/voiceover.wav (48 kHz mono), vo_map.json (part offsets)

The pauses between parts are section breaks (dip to black, bowl strike, music lifts). The aligned line times in
align/p<N>/align.json are part-relative; programme time = offset[part] + line time.
"""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent.parent
PARTS = ["voice/part1_v4.mp3", "voice/part2_v4.mp3", "voice/part3_v4.mp3"]
GAPS = [1.6, 1.2]  # seconds of silence after part 1 and part 2


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def main():
    offsets, t, ins, chain = [], 0.0, [], []
    for i, p in enumerate(PARTS):
        offsets.append(round(t, 3))
        ins += ["-i", str(HERE / p)]
        chain.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono[a{i}]")
        t += dur(HERE / p)
        if i < len(GAPS):
            chain.append(f"anullsrc=r=48000:cl=mono,atrim=0:{GAPS[i]}[g{i}]")
            t += GAPS[i]
    order = "".join(f"[a{i}]" + (f"[g{i}]" if i < len(GAPS) else "") for i in range(len(PARTS)))
    n = len(PARTS) + len(GAPS)
    out = HERE / "assets" / "voiceover.wav"
    out.parent.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(chain) + f";{order}concat=n={n}:v=0:a=1[o]",
                    "-map", "[o]", "-c:a", "pcm_s16le", str(out)], check=True)
    (HERE / "vo_map.json").write_text(json.dumps({"parts": PARTS, "gaps": GAPS, "offsets": offsets, "duration": round(t, 3)}, indent=1) + "\n")
    print("wrote", out, round(t, 2), "s; offsets", offsets)


if __name__ == "__main__":
    main()
