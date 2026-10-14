"""Film timeline from the recorded VO (voice/bp-hlth01-ch1..4.mp3, align/chN/align.json + align/chN.ids).

Chapters play back to back with CH_GAP s between files. The owner's two 3.0 s VO silences (handoff: "zero-voiceover
pauses") are cut into the audio after the last sentence of E032 ("So, what does it mean for you?") and of E053 (the
cioins.co.in line). Everything else reads film seconds from here:
  L("E033") -> (start, end) of a script line; SENT -> sentence cues for subtitles; SEGMENTS -> how to build vo.wav.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CH_GAP = 0.6
PAUSES = {"E032": 3.0, "E053": 3.0}
TAIL = 6.0   # end card runs on after the last word


def _dur(p):
    import subprocess
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


SENT, SEGMENTS, _L = [], [], {}
_t = 0.0
for ch in (1, 2, 3, 4):
    lines = json.load(open(HERE / f"align/ch{ch}/align.json"))
    ids = (HERE / f"align/ch{ch}.ids").read_text().split()
    assert len(lines) == len(ids), (ch, len(lines), len(ids))
    src = HERE / f"voice/bp-hlth01-ch{ch}.mp3"
    total = _dur(src)
    seg_start, shift = 0.0, _t          # film time = source time + shift (shift grows at each inserted pause)
    for k, (l, eid) in enumerate(zip(lines, ids)):
        s, e = l["start"] + shift, l["end"] + shift
        SENT.append(dict(id=eid, ch=ch, start=round(s, 3), end=round(e, 3), text=l["en"]))
        a, b = _L.get(eid, (s, e))
        _L[eid] = (min(a, s), max(b, e))
        last_of_line = k + 1 == len(ids) or ids[k + 1] != eid
        if last_of_line and eid in PAUSES and k + 1 < len(lines):
            cut = (l["end"] + lines[k + 1]["start"]) / 2      # middle of the natural gap: no clipped breath
            SEGMENTS.append(dict(src=str(src), ss=seg_start, to=cut, at=round(seg_start + shift, 3)))
            seg_start = cut
            shift += PAUSES[eid]
    SEGMENTS.append(dict(src=str(src), ss=seg_start, to=total, at=round(seg_start + shift, 3)))
    _t = total + shift + CH_GAP
END = round(_L["E064"][1] + TAIL, 2)
CHAPTER_START = {ch: min(x["start"] for x in SENT if x["ch"] == ch) for ch in (1, 2, 3, 4)}


def L(eid):
    """(start, end) in film seconds of a script line, e.g. L("E033")."""
    a, b = _L[eid]
    return round(a, 2), round(b, 2)


def sents(eid):
    return [x for x in SENT if x["id"] == eid]


if __name__ == "__main__":
    for x in SENT:
        print(f"{x['id']} {x['start']:7.2f} {x['end']:7.2f}  {x['text'][:70]}")
    print("pauses:", {k: L(k)[1] for k in PAUSES}, "END", END)
