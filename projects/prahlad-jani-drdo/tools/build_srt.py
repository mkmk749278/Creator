"""Build subtitles.te.srt from transcript.te.tsv.

With --offset-map, VO times are shifted to programme time using the break rows (LIVE / VO_PAUSE) in
edl.csv, and a LIVE row's `subtitle` text (e.g. a Telugu translation of the archival speech) is added as its
own cue. Cues longer than MAX_CHARS are split at word boundaries into consecutive cues, with time shared by
character count. Each cue is wrapped to at most two lines of LINE_CHARS. [?] markers are dropped.
Usage: python tools/build_srt.py [--offset-map [--edl path/to/edl.csv]]
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from assemble import BREAKS, load_edl  # noqa: E402
LINE_CHARS, MAX_CHARS, MIN_DUR = 40, 80, 0.8


def load(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        s, e, t = line.split("\t")
        rows.append((float(s), float(e), t.replace("[?]", "").strip()))
    return rows


def breaks(use_edl):
    """[(vo_at, dur, vo_skip, programme_start, subtitle)] for every row that stops the VO."""
    if not use_edl:
        return []
    rows, _ = load_edl(sys.argv[sys.argv.index("--edl") + 1] if "--edl" in sys.argv else None)
    return [(float(r["vo_at"]), r["dur"], float(r["vo_skip"] or 0), r["start"], (r.get("subtitle") or "").strip())
            for r in rows if r["type"] in BREAKS]


def shift(t, ps):
    """VO time -> programme time. A pause inserts dur seconds at vo_at and drops vo_skip seconds of VO."""
    return t + sum(d - k for at, d, k, *_ in ps if t >= at + k)


def skipped(t, ps):
    return any(at <= t < at + k for at, _, k, *_ in ps)


def split(s, e, text):
    words, chunks, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > MAX_CHARS:
            chunks.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    chunks.append(cur)
    total, t, out = sum(len(c) for c in chunks), s, []
    for c in chunks:
        d = (e - s) * len(c) / total
        out.append((t, t + d, c))
        t += d
    return out


def wrap(text):
    if len(text) <= LINE_CHARS:
        return text
    words = text.split()
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return " ".join(words[:best]) + "\n" + " ".join(words[best:])


def ts(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    use_edl = "--offset-map" in sys.argv
    ps = breaks(use_edl)
    cues = [(shift(s, ps), shift(e, ps), t) for r in load(HERE / "transcript.te.tsv") for s, e, t in split(*r)
            if not skipped(s, ps)]
    for _, dur, _, start, sub in ps:  # captions for the live archival clips
        if sub:
            cues += split(start + 0.2, start + dur - 0.2, sub)
    cues.sort()
    lines = []
    for i, (s, e, t) in enumerate(cues, 1):
        e = max(e, s + MIN_DUR)
        if i < len(cues):
            e = min(e, cues[i][0] - 0.04)
        lines += [str(i), f"{ts(s)} --> {ts(e)}", wrap(t), ""]
    name = "subtitles.te.programme.srt" if use_edl else "subtitles.te.srt"
    (HERE / name).write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {name}: {len(cues)} cues")


if __name__ == "__main__":
    main()
