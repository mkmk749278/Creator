"""Line timings for the recorded VO (align/block*/align.json), keyed by script row id C001..C085.
Block 1 = C001-C035, block 2 = C036-C062, block 3 = C063-C085; each block starts GAP s after the previous file ends."""
import json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
GAP = 0.6
BLOCKS = (1, 2, 3)


def _dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


OFF = {}     # block -> film offset (s)
_T = {}      # "C001" -> (start, end) in film seconds
TEXT = {}    # "C001" -> spoken text
BLOCK = {}   # "C001" -> block number
_off, _n = 0.0, 0
for b in BLOCKS:
    OFF[b] = round(_off, 3)
    for l in json.load(open(HERE / f"align/block{b}/align.json")):
        _n += 1; k = f"C{_n:03d}"
        _T[k] = (round(_off + l["start"], 2), round(_off + l["end"], 2)); TEXT[k] = l["te"]; BLOCK[k] = b
    _off += _dur(HERE / f"voice/block{b}.mp3") + GAP
VO_END = round(_off - GAP, 2)
END = round(_T[f"C{_n:03d}"][1] + 6.0, 2)   # end card runs on after the last line


def L(key):
    return _T[key]


if __name__ == "__main__":
    print(OFF, VO_END, END, len(_T))
