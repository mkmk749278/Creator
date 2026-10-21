#!/usr/bin/env python3
"""Burned-in captions (ASS) + an SRT for YouTube, from the final edit's exact line times.

Each VO line is split into short phrases (≤ 42 characters, at punctuation first). Phrase times are shared out by
character count across the line, then each boundary snaps to the middle of the nearest real pause in the VO
(silencedetect, 0.10 s) when one lies within 0.45 s. No Whisper. Spoken forms become readable ones
(D.C. → DC, two hundred and thirty → 230 …).

  python3 projects/solar-anti-islanding/tools/make_captions.py   # writes captions.ass, captions_en.srt
"""
import json
import re
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
LINES = json.loads((PROJ / "align_take2/edit3_lines_exact.json").read_text())
VO = PROJ / "voice/vo_v10_take3_edit.mp3"
MAXC = 34
READ = [(r"\bD\.C\.", "DC"), (r"\bA\.C\.", "AC"), ("two hundred and thirty volts", "230 volts"),
        ("about eleven thousand volts", "about 11,000 volts"), ("fifty full swings", "50 full swings"),
        ("within two seconds", "within 2 seconds"), ("Two in the afternoon", "2 PM")]


def silences():
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(VO), "-af", "silencedetect=n=-32dB:d=0.08", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r)]
    return list(zip(st, en))


def readable(text):
    for a, b in READ: text = re.sub(a, b, text)
    return text


def syl(text):
    n = 0
    for w in re.findall(r"[A-Za-z.']+", text):
        if re.fullmatch(r"(?:[A-Z]\.)+", w): n += 3 * w.count("W") + (len(w) // 2 - w.count("W"))   # spelled letters
        else: n += max(1, len(re.findall(r"[aeiouy]+", w.lower())) - (1 if w.lower().endswith("e") and len(w) > 3 else 0))
    return max(n, 1)


def phrases(text):
    """Punctuation phrases (these end at real pauses), each split into ≤ MAXC display pieces near the middle."""
    groups = []
    for p in re.split(r"(?<=[.?!…])\s+|\s+(?=—)|(?<=\.\.\.)\s+", text):
        p = p.strip()
        if not p: continue
        if groups and (len(p) < 16 or len(" ".join(groups[-1])) < 16) and len(" ".join(groups[-1])) + 1 + len(p) <= 40:
            groups[-1] = [" ".join(groups[-1]) + " " + p]; continue          # fold short bits into a neighbour
        out, stack = [], [p]
        while stack:
            q = stack.pop(0)
            if len(readable(q)) <= MAXC: out.append(q); continue
            mid = len(q) / 2
            commas = [i for i, ch in enumerate(q) if ch == "," and 0.3 * len(q) < i < 0.75 * len(q)]
            cut = min(commas, key=lambda i: abs(i - mid)) + 1 if commas else min((i for i, ch in enumerate(q) if ch == " "), key=lambda i: abs(i - mid))
            stack[:0] = [q[:cut].strip(), q[cut:].strip()]
        groups.append(out)
    return groups


_ENV = None


def envelope():
    """10 ms loudness envelope of the VO (for syllable-peak counting)."""
    global _ENV
    if _ENV is None:
        import numpy as np
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(VO), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
        e = np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, mode="same"))[::160]          # 100 frames a second
        _ENV = np.convolve(e, np.hanning(7) / np.hanning(7).sum(), mode="same")
    return _ENV


def peaks(a, b):
    """Syllable nuclei between a and b: envelope peaks 80 ms apart that rise 3 dB over the dip before them."""
    import numpy as np
    e = envelope()[int(a * 100):int(b * 100)]; db = 20 * np.log10(e + 1e-5); n, last, low = 0, -99, 0
    for i in range(1, len(db) - 1):
        low = min(low, db[i]) if n or i > 1 else db[i]
        if db[i] >= db[i - 1] and db[i] > db[i + 1] and db[i] > -35 and db[i] - low > 3 and i - last >= 8:
            n, last, low = n + 1, i, db[i]
    return n


def align(sy, L0, L1, cand):
    """Boundaries at the pauses where the measured syllable count (envelope peaks) best matches the text (in order)."""
    import numpy as np
    k, m = len(sy), len(cand)
    cum, t, acc = [], L0, 0
    for a, b in cand: acc += peaks(t, a); cum.append(acc); t = b
    total = acc + peaks(t, L1)
    want = np.cumsum(sy)[:-1] / sum(sy) * total
    INF = float("inf"); D = [[INF] * m for _ in range(k - 1)]; B = [[-1] * m for _ in range(k - 1)]
    for j in range(m): D[0][j] = abs(cum[j] - want[0])
    for i in range(1, k - 1):
        for j in range(m):
            for q in range(j):
                v = D[i - 1][q] + abs(cum[j] - want[i])
                if v < D[i][j]: D[i][j], B[i][j] = v, q
    j = min(range(m), key=lambda x: D[k - 2][x]); out = [j]
    for i in range(k - 2, 0, -1): j = B[i][j]; out.append(j)
    return [cand[x] for x in out[::-1]]


def align_rate(sy, L0, L1, cand):
    """Choose one real pause per phrase boundary (in order) so each phrase's speaking time fits its syllables (DP)."""
    k, m = len(sy), len(cand)
    def run(r):
        c = lambda a, b, s: ((b - a) - s * r) ** 2 / (s * r)
        INF = float("inf"); D = [[INF] * m for _ in range(k - 1)]; B = [[-1] * m for _ in range(k - 1)]
        for j in range(m): D[0][j] = c(L0, cand[j][0], sy[0])
        for i in range(1, k - 1):
            for j in range(m):
                for q in range(j):
                    v = D[i - 1][q] + c(cand[q][1], cand[j][0], sy[i])
                    if v < D[i][j]: D[i][j], B[i][j] = v, q
        j = min(range(m), key=lambda x: D[k - 2][x] + c(cand[x][1], L1, sy[-1]))
        out = [j]
        for i in range(k - 2, 0, -1): j = B[i][j]; out.append(j)
        return [cand[x] for x in out[::-1]]
    r = (L1 - L0) * 0.88 / sum(sy)
    ch = run(r)
    r = ((L1 - L0) - sum(b - a for a, b in ch)) / sum(sy)          # refine the speech rate with the chosen pauses
    return run(r)


def ts(t, srt=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",") if srt else f"{h}:{m:02d}:{s:05.2f}"


def main():
    sil = silences()
    cues = []
    for l in LINES:
        gr = phrases(l["en"]); L0, L1 = l["start"], l["end"]
        cand = [(a, b) for a, b in sil if L0 + 0.3 < a and b < L1 - 0.3]
        while len(gr) - 1 > len(cand):                            # fewer pauses than phrases: merge the shortest pair
            i = min(range(len(gr) - 1), key=lambda i: len(" ".join(gr[i] + gr[i + 1]))); gr[i:i + 2] = [gr[i] + gr[i + 1]]
        ch = align([syl(" ".join(g)) for g in gr], L0, L1, cand) if len(gr) > 1 else []
        edges = [L0] + [(a + b) / 2 for a, b in ch] + [L1]
        for i, g in enumerate(gr):                                # pieces inside a phrase share its time by syllables
            sy = [syl(p) for p in g]; t = edges[i]
            for p, y in zip(g, sy):
                u = t + (edges[i + 1] - edges[i]) * y / sum(sy)
                text = readable(p).replace("...", "…")
                if text.endswith(".") and not text.endswith("…"): text = text[:-1]          # no full stop on a caption
                cues.append((t, u, text)); t = u
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,66,&H00FFFFFF,&H00FFFFFF,&H330D1117,&H330D1117,-1,0,0,0,100,100,0,0,3,16,0,2,60,60,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{ts(a)},{ts(b - 0.04)},Cap,,0,0,0,,{t}" for a, b, t in cues]
    (PROJ / "captions.ass").write_text(hdr + "\n".join(ev) + "\n")
    srt = [f"{i + 1}\n{ts(a, True)} --> {ts(b - 0.04, True)}\n{t}\n" for i, (a, b, t) in enumerate(cues)]
    (PROJ / "captions_en.srt").write_text("\n".join(srt))
    print(f"{len(cues)} cues; longest {max(len(t) for *_, t in cues)} chars; shortest {min(b - a for a, b, _ in cues):.2f} s")


if __name__ == "__main__":
    main()
