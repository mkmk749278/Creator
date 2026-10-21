#!/usr/bin/env python3
"""Film 01 sound: a synthesised music bed and a sound-effects track, both 48 kHz, deterministic and licence-free.

Bed: dark minor pad + soft sub pulse that changes by section; total silence 1.5 s before the core reveal
("So where is your money right now?", CLAUDE.md audio rule), a low hit on it, and a lift for the bridge.
SFX: one cue per on-screen event (state sound logos: success chime, failed buzz, processing tick).
Usage: python3 projects/upi-money-deducted/build/make_sound.py  -> assets/audio/{bed,sfx}.wav
"""
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000; DUR = 258.0; N = int(DUR * SR)
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
          "drive": [(146.8, 174.6, 220.0), (130.8, 155.6, 196.0)]}
SECTIONS = [(0, "tense"), (22.0, "drive"), (73.5, "tense"), (116.7, "tense"), (147.0, "drive"), (183.2, "calm"), (242.7, "calm")]
bed = np.zeros(N)
for si, (s0, mood) in enumerate(SECTIONS):
    s1 = SECTIONS[si + 1][0] if si + 1 < len(SECTIONS) else DUR
    bar = 4.0; k = 0; t = s0
    while t < s1:
        d = min(bar, s1 - t); ch = CHORDS[mood][k % 2]; n = int(d * SR); tt = np.arange(n) / SR
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.003 * tt) + 0.25 * np.sin(2 * np.pi * f * 0.5 * tt) for f in ch)
        put(bed, t, lp(pad, 900) * env(n, 0.8, 0.8) * 0.05)
        t += bar; k += 1
    # sub pulse (heartbeat-like) quicker in drive/tense sections
    bpm = {"tense": 72, "drive": 92, "calm": 0}[mood]
    if bpm:
        p = 60 / bpm; t = s0
        while t < s1 - 0.2:
            thump = tone(52, 0.35, 0.002, 0.3, (1.0, 0.3)) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9)
            put(bed, t, thump, 0.16); t += p
# shimmer: filtered noise breathing slowly
bed += lp(hp(rng.standard_normal(N), 4000), 9000) * (0.004 + 0.003 * np.sin(2 * np.pi * t_all / 11))
# silence 1.5 s before the reveal (116.7), a low hit on it; also a short dip before "Call dropped"
for a, b in ((115.2, 116.7), (80.9, 81.6)):
    i, j = int(a * SR), int(b * SR); ramp = int(0.25 * SR)
    bed[i - ramp:i] *= np.linspace(1, 0, ramp); bed[i:j] = 0; bed[j:j + ramp] *= np.linspace(0, 1, ramp)
for at in (116.7, 81.6):
    hit = (tone(41, 2.4, 0.003, 2.0, (1.0, 0.5, 0.25)) + lp(noise(2.4), 200) * 0.6) * np.exp(-np.arange(int(2.4 * SR)) / SR * 1.6)
    put(bed, at, hit, 0.5)
bed *= env(N, 1.5, 4.0)
sf.write(OUT / "bed.wav", (bed / np.max(np.abs(bed)) * 0.6).astype(np.float32), SR)

# ---------------- sfx ----------------
fx = np.zeros(N)


def buzz(d=0.18):   # phone vibration
    t = np.arange(int(d * SR)) / SR; return lp(np.sign(np.sin(2 * np.pi * 170 * t)) * 0.4, 600) * env(len(t), 0.005, 0.03)


def whoosh(d=0.6, up=True):
    n = int(d * SR); x = noise(d); c = np.linspace(400, 3000, n) if up else np.linspace(3000, 400, n)
    y = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        f = c[i]; y[i:i + seg] = bp(x[i:i + seg + 512], max(100, f * 0.5), min(20000, f * 1.6))[: len(y[i:i + seg])]
    return y * env(n, d * 0.5, d * 0.5, 2) * 0.6


def ring(d=1.6):    # old telephone bell: two fast-alternating bells
    t = np.arange(int(d * SR)) / SR; am = (np.sin(2 * np.pi * 20 * t) > 0).astype(float)
    y = (np.sin(2 * np.pi * 1400 * t) + 0.6 * np.sin(2 * np.pi * 2100 * t)) * am
    return lp(y, 5000) * env(len(t), 0.01, 0.1) * 0.25


def chime():
    return sum(tone(f, 1.4, 0.003, 1.2, (1.0, 0.25)) * np.exp(-np.arange(int(1.4 * SR)) / SR * 3) * g for f, g in ((1046.5, 0.5), (1568.0, 0.35)))


def err():
    return tone(180, 0.45, 0.003, 0.08, (1.0, 0.6, 0.4)) * 0.4


def click(f=2500, d=0.03):
    return bp(noise(d), f * 0.7, f * 1.4) * env(int(d * SR), 0.001, 0.02) * 0.8


def tick():
    return click(4200, 0.025) * 0.7


def static(d):
    return hp(noise(d), 1500) * 0.09 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * np.arange(int(d * SR)) / SR))


def deadtone(d=1.2):
    t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * 425 * t) * (np.sin(2 * np.pi * 1.6 * t) > -0.2) * 0.12 * env(len(t), 0.01, 0.1)


def thud(f=60):
    return (tone(f, 0.5, 0.002, 0.4, (1.0, 0.4)) + lp(noise(0.5), 300) * 0.5) * np.exp(-np.arange(int(0.5 * SR)) / SR * 10)


def coin():
    return sum(tone(f, 0.7, 0.001, 0.6) * np.exp(-np.arange(int(0.7 * SR)) / SR * 6) for f in (2637, 3520, 4186)) * 0.15


def shutter():
    return np.concatenate([click(3000, 0.04), np.zeros(int(0.05 * SR)), click(2200, 0.05)])


def rise(f0):
    return tone(f0, 0.5, 0.01, 0.3, (1.0, 0.3)) * 0.18


CUES = [  # (time, sound, gain)
    (0.35, buzz(), 0.8), (0.6, buzz(), 0.8), (4.45, click(1800), 0.5), (7.0, whoosh(0.5, False), 0.25),
    (11.85, whoosh(0.4), 0.2), (22.0, whoosh(0.5), 0.25)] + [(22.45 + 0.24 * k, click(2200, 0.02), 0.5) for k in range(6)] + [
    (24.55, whoosh(0.7), 0.35), (26.0, click(900, 0.05), 0.5), (29.55, whoosh(0.5, False), 0.25),
    (31.8 + 0.12 * 0, click(3000), 0.3), (32.9, whoosh(0.6), 0.25), (36.0, ring(1.5), 0.7), (37.8, ring(1.0), 0.6),
    (44.0, tone(880, 0.25, 0.005, 0.2) * 0.2, 1.0), (44.8, tone(988, 0.25, 0.005, 0.2) * 0.2, 1.0), (45.6, tone(1174, 0.25, 0.005, 0.2) * 0.2, 1.0),
    (47.3, ring(1.0), 0.5), (48.1, click(700, 0.06), 0.8), (50.4, chime(), 0.6),
    (53.1, ring(1.0), 0.5), (54.2, err(), 0.7), (59.0, err(), 0.5), (62.0, whoosh(1.2, False), 0.35), (67.1, chime(), 0.35),
    (70.6, click(2200, 0.02), 0.6), (69.2, chime(), 0.3),
    (73.8, ring(1.4), 0.6), (75.6, ring(1.4), 0.55), (77.6, static(4.0), 1.0), (81.6, deadtone(1.2), 1.0),
    (98.4, shutter(), 0.7), (101.2, buzz(), 0.6), (102.4, chime(), 0.35),
    (123.2, tone(220, 0.8, 0.02, 0.5, (1.0, 0.5)) * 0.15, 1.0),
    (131.4, whoosh(0.6), 0.2), (139.16, thud(70), 0.9), (140.8, chime(), 0.4), (143.47, thud(55), 0.9), (145.0, whoosh(1.0, False), 0.3),
    (147.0, whoosh(0.5), 0.2), (157.8, click(1500, 0.05), 0.5), (163.4, click(1500, 0.05), 0.5),
    (174.6, coin(), 0.9), (177.4, coin(), 0.9), (185.8, chime(), 0.35), (188.1, err(), 0.45), (193.0, tick(), 0.6),
    (201.2, thud(48), 0.5), (206.0, buzz(), 0.6), (207.4, buzz(), 0.6), (212.4, thud(65), 0.8), (212.7, thud(65), 0.8),
    (217.3, click(2200, 0.02), 0.6), (220.0, click(2200, 0.02), 0.6), (226.0, rise(330), 1.0), (227.2, rise(392), 1.0), (230.0, rise(494), 1.0),
    (238.5, whoosh(0.4), 0.2), (243.4, ring(1.0), 0.4), (245.6, chime(), 0.45), (251.9, chime(), 0.3)]
# processing tick: the "ticking clock" state logo while it says processing on screen
CUES += [(82.6 + 0.5 * k, tick(), 0.35) for k in range(16)] + [(87.3 + 0.5 * k, tick(), 0.25) for k in range(7)]
for at, x, g in CUES:
    put(fx, at, x, g)
sf.write(OUT / "sfx.wav", (fx / max(1e-9, np.max(np.abs(fx))) * 0.7).astype(np.float32), SR)
print("bed + sfx ->", OUT)
