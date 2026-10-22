#!/usr/bin/env python3
"""Rare earth film sound (adapted from the UPI film): a synthesised music bed and a sound-effects track, 48 kHz,
deterministic and licence-free.

Bed: minor pad + soft sub pulse by section; total silence 1.5 s before each core reveal (CLAUDE.md audio rule: the
chain breaks, thorium, the April 2025 licence shock, "it never went away"), a low hit on each, a hopeful lift for
India's answer and a full swell over the end screen.
SFX: one cue per on-screen event (counters, chain links, stamps, map arcs).
Usage: python3 projects/rare-earth-magnets/build/make_sound.py  -> assets/audio/{bed,sfx}.wav
"""
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000; DUR = 636.0; N = int(DUR * SR)
rng = np.random.default_rng(21)
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
    i = int(at * SR); j = min(N, i + len(x)); track[i:j] += gain * x[: j - i]


def tone(f, d, a=0.005, r=0.2, harm=(1.0,), detune=0.0):
    t = np.arange(int(d * SR)) / SR; y = sum(h * np.sin(2 * np.pi * f * (k + 1) * t * (1 + detune * k)) for k, h in enumerate(harm))
    return y * env(len(t), a, r)


def noise(d):
    return rng.standard_normal(int(d * SR))


# ---------------- bed ----------------
CHORDS = {"tense": [(110.0, 130.8, 164.8), (98.0, 116.5, 146.8)], "calm": [(130.8, 164.8, 196.0), (110.0, 138.6, 164.8)],
          "drive": [(146.8, 174.6, 220.0), (130.8, 155.6, 196.0)], "hope": [(130.8, 164.8, 196.0), (146.8, 185.0, 220.0)]}
SECTIONS = [(0, "tense"), (53.6, "drive"), (112.7, "calm"), (173.2, "drive"), (219.7, "tense"), (283.8, "calm"),
            (305.0, "tense"), (386.2, "tense"), (449.9, "hope"), (531.65, "calm"), (574.05, "drive"), (618.0, "hope")]
REVEALS = [214.07, 305.0, 386.24, 448.14]   # bed silent for 1.5 s before each, low hit on it
bed = np.zeros(N)
for si, (s0, mood) in enumerate(SECTIONS):
    s1 = SECTIONS[si + 1][0] if si + 1 < len(SECTIONS) else DUR
    bar = 4.0; k = 0; t = s0
    while t < s1:
        d = min(bar, s1 - t); ch = CHORDS[mood][k % 2]; n = int(d * SR); tt = np.arange(n) / SR
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.003 * tt) + 0.25 * np.sin(2 * np.pi * f * 0.5 * tt) for f in ch)
        put(bed, t, lp(pad, 900) * env(n, 0.8, 0.8) * 0.05)
        t += bar; k += 1
    bpm = {"tense": 72, "drive": 90, "calm": 0, "hope": 0}[mood]
    if bpm:
        p = 60 / bpm; t = s0
        while t < s1 - 0.2:
            thump = tone(52, 0.35, 0.002, 0.3, (1.0, 0.3)) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9)
            put(bed, t, thump, 0.16); t += p
bed += lp(hp(rng.standard_normal(N), 4000), 9000) * (0.004 + 0.003 * np.sin(2 * np.pi * t_all / 11))
for at in REVEALS:
    i, j = int((at - 1.5) * SR), int(at * SR); ramp = int(0.25 * SR)
    bed[i - ramp:i] *= np.linspace(1, 0, ramp); bed[i:j] = 0; bed[j:j + ramp] *= np.linspace(0, 1, ramp)
    hit = (tone(41, 2.4, 0.003, 2.0, (1.0, 0.5, 0.25)) + lp(noise(2.4), 200) * 0.6) * np.exp(-np.arange(int(2.4 * SR)) / SR * 1.6)
    put(bed, at, hit, 0.5)
end = int(618.0 * SR); bed[end:] *= np.linspace(1.0, 2.2, N - end)   # end screen: music carries it
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


def clink():   # chain link: two short metallic partials
    return sum(tone(f, 0.5, 0.001, 0.45) * np.exp(-np.arange(int(0.5 * SR)) / SR * 9) for f in (1860, 2790, 3720)) * 0.12


def snap():    # magnet snap / chain break
    y = thud(90) * 0.5; c = click(1200, 0.05); y[:len(c)] += c; return y


def chime():
    return sum(tone(f, 1.4, 0.003, 1.2, (1.0, 0.25)) * np.exp(-np.arange(int(1.4 * SR)) / SR * 3) * g for f, g in ((1046.5, 0.5), (1568.0, 0.35)))


def err():
    return tone(180, 0.45, 0.003, 0.08, (1.0, 0.6, 0.4)) * 0.4


CUES = [(0.15, whoosh(0.5), 0.25), (9.85, err(), 0.35), (10.85, err(), 0.35), (12.2, snap(), 0.6), (14.0, thud(55), 0.6),
        (16.7, whoosh(0.6), 0.2), (19.95, thud(50), 0.6), (21.0, err(), 0.4), (26.3, whoosh(0.5), 0.2), (32.7, whoosh(0.6), 0.25),
        (38.0, thud(48), 0.8), (38.5, thud(48), 0.8), (51.0, click(1500, 0.05), 0.5), (60.5, snap(), 0.5),
        (69.2, whoosh(0.4), 0.2), (72.9, chime(), 0.3), (74.7, chime(), 0.3), (94.5, whoosh(0.7), 0.25), (104.3, thud(55), 0.7),
        (121.5, whoosh(0.5), 0.2), (138.9, snap(), 0.6), (148.6, click(1800, 0.04), 0.5), (165.4, click(900, 0.04), 0.4),
        (170.0, whoosh(0.5), 0.25), (197.1, snap(), 0.8), (200.8, chime(), 0.4)] + \
       [(t, clink(), 0.9) for t in (207.5, 208.4, 209.6, 211.1, 212.2, 213.0)] + [(214.4, snap(), 1.0),
        (224.6, whoosh(0.8), 0.25), (248.8, err(), 0.3), (261.8, whoosh(0.6), 0.2), (266.3, whoosh(0.6), 0.2), (269.3, whoosh(0.6), 0.2),
        (276.3, chime(), 0.25), (278.3, thud(55), 0.6), (295.4, click(1500, 0.05), 0.4), (317.9, thud(60), 0.6),
        (339.7, whoosh(0.6), 0.2), (346.3, whoosh(0.8), 0.25), (352.6, whoosh(0.8, False), 0.25), (366.8, err(), 0.35),
        (390.0, thud(55), 0.7), (392.6, thud(55), 0.6), (400.6, whoosh(0.5), 0.2), (407.4, whoosh(0.4), 0.2), (422.0, err(), 0.5),
        (425.4, thud(55), 0.6), (430.4, click(1500, 0.05), 0.5), (433.9, thud(50), 0.6), (437.3, chime(), 0.3), (452.4, chime(), 0.4),
        (463.4, whoosh(0.5), 0.2), (475.3, whoosh(0.7), 0.25), (481.0, chime(), 0.35)] + \
       [(t, clink(), 0.7) for t in (486.0, 487.4, 488.2, 488.9)] + [(493.9, click(1800, 0.04), 0.5), (499.7, thud(55), 0.5),
        (521.3, chime(), 0.35), (528.4, thud(55), 0.5), (551.9, thud(48), 0.6), (557.7, err(), 0.5), (564.8, chime(), 0.5),
        (586.9, click(1500, 0.05), 0.5), (590.8, click(1500, 0.05), 0.5), (610.8, whoosh(0.8), 0.3), (618.1, chime(), 0.5)]
for at, x, g in CUES:
    put(fx, at, x, g)
sf.write(OUT / "sfx.wav", (fx / max(1e-9, np.max(np.abs(fx))) * 0.7).astype(np.float32), SR)
print("bed + sfx ->", OUT)
