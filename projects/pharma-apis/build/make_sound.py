#!/usr/bin/env python3
"""Pharma film sound (adapted from the rare earth film): a synthesised music bed and a sound-effects track, 48 kHz,
deterministic and licence-free. Times come from make_film.py (film time, beats included).

Bed: cold piano-like pad and a slow pulse by chapter; total silence 1.5 s before each core reveal (CLAUDE.md audio rule:
Pimpri 1954, the roll call, Kakinada, the January 2027 end date), a low hit on each, a warmer lift from Kakinada on,
and a swell over the end screen.
SFX: one cue per on-screen event (the order's phone ring, counters, the STOPPED stamps, map arcs, the shield).
Usage: python3 projects/pharma-apis/build/make_sound.py  -> assets/audio/{bed,sfx}.wav
"""
import importlib.util
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

_spec = importlib.util.spec_from_file_location("make_film", Path(__file__).with_name("make_film.py"))
MF = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(MF)
L, LE, S = MF.L, MF.LE, MF.S
SR = 48000; DUR = MF.END; N = int(DUR * SR)
rng = np.random.default_rng(28)
P = Path(__file__).resolve().parents[1]; OUT = P / "assets/audio"; OUT.mkdir(parents=True, exist_ok=True)
t_all = np.arange(N) / SR


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def lp(x, f):
    return sosfilt(butter(2, f, "lowpass", fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, "highpass", fs=SR, output="sos"), x)


def env(n, a, r, shape=1.0):
    e = np.ones(n); na, nr = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    e[:na] = np.linspace(0, 1, na) ** shape; e[-nr:] *= np.linspace(1, 0, nr) ** shape; return e


def put(track, at, x, gain=1.0):
    i = max(0, int(at * SR)); j = min(N, i + len(x)); track[i:j] += gain * x[: j - i]


def tone(f, d, a=0.005, r=0.2, harm=(1.0,)):
    t = np.arange(int(d * SR)) / SR; y = sum(h * np.sin(2 * np.pi * f * (k + 1) * t) for k, h in enumerate(harm))
    return y * env(len(t), a, r)


def noise(d):
    return rng.standard_normal(int(d * SR))


# ---------------- bed ----------------
CHORDS = {"cold": [(110.0, 130.8, 164.8), (103.8, 123.5, 155.6)], "pride": [(130.8, 164.8, 196.0), (146.8, 174.6, 220.0)],
          "lab": [(98.0, 123.5, 146.8), (110.0, 138.6, 164.8)], "dark": [(87.3, 103.8, 130.8), (82.4, 98.0, 123.5)],
          "hope": [(130.8, 164.8, 196.0), (146.8, 185.0, 220.0)]}
SECTIONS = [(0, "cold"), (L(13), "pride"), (L(18), "lab"), (L(25), "cold"), (L(29), "pride"), (L(34), "lab"),
            (L(45), "dark"), (L(61), "cold"), (L(64), "hope"), (L(77), "cold"), (L(81), "hope")]
REVEALS = [L(29), L(52), L(64), L(72, 0.5)]   # bed silent for 1.5 s before each, low hit on it
bed = np.zeros(N)
for si, (s0, mood) in enumerate(SECTIONS):
    s1 = SECTIONS[si + 1][0] if si + 1 < len(SECTIONS) else DUR
    bar = 4.0; k = 0; t = s0
    while t < s1:
        d = min(bar, s1 - t); ch = CHORDS[mood][k % 2]; n = int(d * SR); tt = np.arange(n) / SR
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.45 * np.sin(2 * np.pi * f * 2.003 * tt) + 0.2 * np.sin(2 * np.pi * f * 0.5 * tt) for f in ch)
        put(bed, t, lp(pad, 950) * env(n, 0.8, 0.8) * 0.05)
        # a soft "piano" pluck on each bar (clean-room coldness), louder in pride and hope
        pl = tone(ch[2] * 2, 1.8, 0.003, 1.6, (1.0, 0.3, 0.12)) * np.exp(-np.arange(int(1.8 * SR)) / SR * 2.4)
        put(bed, t, pl, {"pride": 0.05, "hope": 0.06}.get(mood, 0.03))
        t += bar; k += 1
    bpm = {"cold": 68, "dark": 76, "lab": 84}.get(mood, 0)
    if bpm:
        p = 60 / bpm; t = s0
        while t < s1 - 0.2:
            thump = tone(50, 0.35, 0.002, 0.3, (1.0, 0.3)) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9)
            put(bed, t, thump, 0.13); t += p
bed += lp(hp(rng.standard_normal(N), 4000), 9000) * (0.004 + 0.003 * np.sin(2 * np.pi * t_all / 11))   # air-handler hiss
for at in REVEALS:
    i, j = int((at - 1.5) * SR), int(at * SR); ramp = int(0.25 * SR)
    bed[i - ramp:i] *= np.linspace(1, 0, ramp); bed[i:j] = 0; bed[j:j + ramp] *= np.linspace(0, 1, ramp)
    hit = (tone(41, 2.4, 0.003, 2.0, (1.0, 0.5, 0.25)) + lp(noise(2.4), 200) * 0.6) * np.exp(-np.arange(int(2.4 * SR)) / SR * 1.6)
    put(bed, at, hit, 0.5)
# the roll call runs under silence after its reveal (screenplay): bed stays out until Alembic's stamp
i, j = int(L(52) * SR), int((LE(55) + 1.4) * SR); bed[i:j] *= 0.0
end = int(MF.VO_END * SR); bed[end:] *= np.linspace(1.0, 2.2, N - end)   # end screen: music carries it
bed *= env(N, 1.5, 4.0)
sf.write(OUT / "bed.wav", (bed / np.max(np.abs(bed)) * 0.6).astype(np.float32), SR)

# ---------------- sfx ----------------
fx = np.zeros(N)


def whoosh(d=0.6, up=True):
    n = int(d * SR); x = noise(d); c = np.linspace(400, 3000, n) if up else np.linspace(3000, 400, n)
    y = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        f = c[i]; y[i:i + seg] = bp(x[i:i + seg + 512], max(100, f * 0.5), min(20000, f * 1.6))[: len(y[i:i + seg])]
    return y * env(n, d * 0.5, d * 0.5, 2) * 0.6


def click(f=2500, d=0.03):
    return bp(noise(d), f * 0.7, f * 1.4) * env(int(d * SR), 0.001, 0.02) * 0.8


def thud(f=60):
    return (tone(f, 0.5, 0.002, 0.4, (1.0, 0.4)) + lp(noise(0.5), 300) * 0.5) * np.exp(-np.arange(int(0.5 * SR)) / SR * 10)


def stampfx():   # rubber stamp: a dull thud with a paper slap
    y = thud(70) * 0.8; s = bp(noise(0.08), 600, 2500) * env(int(0.08 * SR), 0.001, 0.06); y[:len(s)] += s * 0.6; return y


def ring():      # a phone ringing twice (the 3 March order)
    out = np.zeros(int(2.4 * SR))
    for k in (0.0, 1.2):
        r = tone(1350, 0.8, 0.005, 0.05, (1.0, 0.5)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * np.arange(int(0.8 * SR)) / SR)))
        i = int(k * SR); out[i:i + len(r)] += r * 0.35
    return out


def chime():
    return sum(tone(f, 1.4, 0.003, 1.2, (1.0, 0.25)) * np.exp(-np.arange(int(1.4 * SR)) / SR * 3) * g for f, g in ((1046.5, 0.5), (1568.0, 0.35)))


def pop():     # the capsule pulling apart
    return bp(noise(0.06), 300, 1800) * env(int(0.06 * SR), 0.001, 0.05) * 0.9


def bubbles(d=2.5):
    y = np.zeros(int(d * SR))
    for k in range(18):
        b = tone(500 + (k * 137) % 700, 0.06, 0.002, 0.05) * np.linspace(1, 0, int(0.06 * SR))
        put_at = int(((k * 0.37) % d) * SR); y[put_at:put_at + len(b)] += b[: len(y) - put_at] * 0.25
    return y


CUES = [(L(2, 0.15), pop(), 0.6), (MF.S(2, 1) - 0.2, whoosh(0.7), 0.25), (L(6, 0.25), ring(), 0.6), (L(7), thud(55), 0.6),
        (L(14, 0.62), click(1500, 0.05), 0.4), (L(15, 0.55), chime(), 0.35), (L(24), thud(48), 0.7), (L(25, 0.45), click(1800, 0.04), 0.4),
        (L(25, 1.2 / 1e9 + 0.75), chime(), 0.3), (L(35, 0.95), chime(), 0.25), (L(36, 0.6), bubbles(), 0.6), (L(37), bubbles(), 0.5),
        (L(38, 0.6), chime(), 0.3), (L(44), whoosh(0.8), 0.3), (L(48), whoosh(0.8, False), 0.3), (L(49, 0.65), click(1500, 0.05), 0.4),
        (L(57, 0.6), thud(50), 0.6), (L(62, 0.55), click(1500, 0.05), 0.4), (L(68, 0.1), thud(55), 0.6), (L(70), chime(), 0.4),
        (L(76, 0.7), chime(), 0.35), (L(85), chime(), 0.5)]
CUES += [(round(LE(n) - 0.35, 3), stampfx(), 1.0) for n in (52, 53, 54, 55)]
# the notes fly away as the $350 card lands; the border gate: a thud for each container stopped, a click for each let through
CUES += [(MF.L(15, 0.55), whoosh(1.0), 0.4)]
_g0 = MF.c(69) - max(0.0, 9.6 - (MF.S(69, 2) - MF.c(69)))
CUES += [(_g0 + t, thud(70), 0.5) for t in (1.4, 5.6, 11.2, 11.8)] + [(_g0 + t, click(1800, 0.05), 0.35) for t in (3.6, 7.4, 13.2, 13.8)]
# one stray germ: a low, dissonant warning sting as the broth turns murky
CUES += [(MF.S(37, 2) + 0.15, (tone(98, 1.6, 0.01, 1.2, (1.0, 0.4)) + tone(104, 1.6, 0.01, 1.2, (0.7,))) * np.exp(-np.arange(int(1.6 * SR)) / SR * 1.5), 0.55)]
for at, x, g in CUES:
    put(fx, at, x, g)
sf.write(OUT / "sfx.wav", (fx / max(1e-9, np.max(np.abs(fx))) * 0.7).astype(np.float32), SR)
print("bed + sfx ->", OUT, f"({DUR:.1f}s)")
