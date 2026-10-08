#!/usr/bin/env python3
"""Join the three VO parts into one programme voiceover (fact-check cuts applied, section pauses), write vo_map.json.

  python3 tools/build_vo.py      -> assets/voiceover.wav (48 kHz mono), vo_map.json
Cuts and gaps live in tools/vomap.py.
"""
import json
import subprocess
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vomap import CUTS, GAPS, HERE, PARTS, offsets, part_dur  # noqa: E402


def main():
    ins, chain, order, n = [], [], "", 0
    for i, p in enumerate(PARTS, 1):
        ins += ["-i", str(HERE / p)]
        t, k = 0.0, 0
        for s, e, add, _ in sorted(CUTS.get(i, [])) + [(part_dur(i), part_dur(i), 0.0, "")]:
            if s > t + 0.01:
                chain.append(f"[{i - 1}:a]atrim={t}:{s},asetpts=N/SR/TB,aresample=48000,aformat=channel_layouts=mono[a{i}_{k}]")
                order += f"[a{i}_{k}]"; n += 1; k += 1
            if add:
                chain.append(f"anullsrc=r=48000:cl=mono,atrim=0:{add}[s{i}_{k}]")
                order += f"[s{i}_{k}]"; n += 1; k += 1
            t = e
        if i <= len(GAPS):
            chain.append(f"anullsrc=r=48000:cl=mono,atrim=0:{GAPS[i - 1]}[g{i}]")
            order += f"[g{i}]"; n += 1
    out = HERE / "assets" / "voiceover.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(chain) + f";{order}concat=n={n}:v=0:a=1[o]",
                    "-map", "[o]", "-c:a", "pcm_s16le", str(out)], check=True)
    off, total = offsets()
    (HERE / "vo_map.json").write_text(json.dumps({"parts": PARTS, "gaps": GAPS, "offsets": off, "duration": total,
                                                  "cuts": {str(k): v for k, v in CUTS.items()}}, indent=1, ensure_ascii=False) + "\n")
    real = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout)
    print(f"wrote {out} {real:.2f} s (map says {total:.2f} s); offsets {off}")


if __name__ == "__main__":
    main()
