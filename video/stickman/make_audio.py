#!/usr/bin/env python3
"""Score and sound effects for the stick-man demo (stick.js), all synthesised with seeded numpy: no samples, no licences.

Music: a plucked ukulele-like instrument (additive harmonics with per-harmonic decay) that follows the story beats and
drops out for the panic and right before the bonk. SFX: footsteps on the walk's own plant times, paper flutter, catch,
folds, ding, whooshes, bonk, twinkles. Usage: python3 make_audio.py out.wav   (then loudnorm to -14 LUFS in the mux)
"""
import sys, wave
import numpy as np

SR, DUR = 48000, 18.6
N = int(SR * DUR)
rng = np.random.default_rng(7)
mus, sfx = np.zeros(N), np.zeros(N)


def put(buf, at, x, db):
    i = int(at * SR)
    if i >= N: return
    x = x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
    buf[i:i + len(x)] += x[: N - i]


def tt(d): return np.arange(int(d * SR)) / SR
def noise(n): return rng.standard_normal(n)


def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def env(t, a, r): return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
def hz(n): return 440 * 2 ** ((n - 69) / 12)   # MIDI note -> Hz


# ---------------- instruments ----------------
def pluck(note, d=1.2, bright=1.0):
    t = tt(d); f = hz(note); x = np.zeros_like(t)
    for k in range(1, 11):
        x += np.sin(2 * np.pi * f * k * (1 + 0.0007 * k * k) * t) / k ** (1.3 / bright) * np.exp(-t * (2.2 + 1.6 * k))
    return x * np.minimum(1, t / 0.002)


def strum(at, notes, db=-20, d=1.0, down=True, gap=0.014):
    for i, n in enumerate(notes if down else notes[::-1]): put(mus, at + i * gap, pluck(n, d), db - i * 0.8)


def bell(f, d=1.4):
    t = tt(d)
    return sum(np.sin(2 * np.pi * f * m * t) * a * np.exp(-t * (2.5 + m)) for m, a in [(1, 1), (2.76, .5), (5.4, .25), (8.9, .12)]) * np.minimum(1, t / 0.001)


def whistle(notes):   # [(start, dur, midi)] with glides
    for s, d, n in notes:
        t = tt(d); f = hz(n) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t)) * (1 - 0.03 * np.exp(-t * 30))
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) + bp(noise(len(t)), hz(n) * 0.9, hz(n) * 1.3) * 0.08
        put(mus, s, x * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05), -22)


def whoosh(d=0.6, lo=300, hi=3000, rise=True):
    t = tt(d); x = noise(len(t)); out = np.zeros_like(x); step = 1024
    for i in range(0, len(x), step):
        p = i / len(x); c = lo + (hi - lo) * (p if rise else 1 - p)
        out[i:i + step] = bp(x[i:i + step], c * 0.6, c * 1.5)
    return out * np.sin(np.pi * t / t[-1]) ** 2


def thud(f0=110, d=0.25):
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 9) + 40) / SR) * env(t, 0.002, 0.07) + bp(noise(len(t)), 80, 900) * env(t, 0.001, 0.015) * 0.6


def crinkle(d=0.18):
    t = tt(d); g = (rng.random(len(t)) < 0.03) * rng.random(len(t))
    return bp(g * 5 + noise(len(t)) * 0.2, 1500, 9000) * env(t, 0.004, d / 2.5)


def boing(f0=180, d=0.6):
    t = tt(d); f = f0 * (1 + 0.6 * np.exp(-t * 6) * np.sin(2 * np.pi * 14 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, 0.003, 0.22)


# ---------------- music ----------------
C, F, G, Am, Em = [60, 64, 67, 72], [60, 65, 69, 72], [59, 62, 67, 71], [57, 60, 64, 69], [59, 64, 67, 71]
b = 0.5   # 120 bpm
for i, ch in enumerate([C, C, G, G, Am, Am]):            # walk: bouncy down-up strums
    strum(i * b, ch, -21); strum(i * b + b * 0.5, ch[1:], -26, 0.5, down=False)
whistle([(0.25, 0.3, 79), (0.67, 0.3, 76), (1.09, 0.25, 79), (1.51, 0.35, 81), (1.93, 0.3, 79), (2.35, 0.45, 76)])
for k, n in enumerate([69, 72, 76, 74, 72, 71]):         # curious: sparse plucks while the paper falls and puzzles him
    put(mus, 3.0 + k * 0.42, pluck(n, 1.3, 0.8), -24)
for i, ch in enumerate([C, F, G, C, F]):                   # idea + folding: bright strums
    strum(5.6 + i * b, ch, -19); strum(5.6 + i * b + b * 0.5, ch[1:], -25, 0.5, down=False)
for k in range(6): put(mus, 8.3 + k * 0.075, pluck(72 + k, 0.3), -26)     # wind-up ratchet
fl = [72, 76, 79, 84, 79, 76]                                              # flight: rolling arpeggio, lifts in the loop
for k in range(int((12.3 - 8.9) / 0.125)):
    n = fl[k % 6] + (2 if 9.9 < 8.9 + k * 0.125 < 11.0 else 0)
    put(mus, 8.9 + k * 0.125, pluck(n, 0.5, 1.2), -24 + (2 if k % 6 == 0 else 0))
for k, n in enumerate([60, 64, 67]): put(mus, 13.5 + k * 0.12, pluck(n, 1.0), -24)  # relief
strum(15.42, [60, 64, 67, 72, 76], -16, 1.6); strum(15.92, [62, 67, 71, 74], -19, 0.8)  # laugh: fanfare
for k, n in enumerate([79, 76, 72, 67]): put(mus, 16.3 + k * 0.07, pluck(n, 0.4), -22)   # the plane pops off: falling run
for k, n in enumerate([67, 72]): put(mus, 16.88 + k * 0.08, pluck(n, 0.6), -21)            # caught it
strum(17.3, [60, 64, 67, 72, 76, 79], -15, 2.2, gap=0.022)                                # wink: final chord

# ---------------- sfx ----------------
X0, V, TD, TS, S = -80, 300, 2.6, 3.0, 210                                  # walk, as in stick.js
ts = np.arange(0, TS, 1 / SR / 10)
d = np.where(ts < TD, V * ts, V * TD + V * (ts - TD) - V * (ts - TD) ** 2 / (2 * (TS - TD)))
for k in range(1, int(d[-1] / (S / 2)) + 1):
    at = ts[np.searchsorted(d, k * S / 2)]
    put(sfx, at, thud(150, 0.12), -24)
for at in [3.3, 3.42, 5.95, 8.9, 9.9, 15.92, 16.26, 16.96]: put(sfx, at, thud(140, 0.14), -21)
t = tt(2.2); put(sfx, 1.9, bp(noise(len(t)), 600, 4000) * (0.3 + 0.7 * np.abs(np.sin(2 * np.pi * 0.72 * t))) * np.minimum(1, t / 0.4), -30)  # flutter
put(sfx, 4.1, crinkle(0.14), -13)                                                                        # catch
t = tt(0.55); put(sfx, 4.85, bp(noise(len(t)), 2000, 7000) * (np.sin(2 * np.pi * 9 * t) > 0.3), -27)      # scratch
put(sfx, 4.75, boing(330, 0.35), -22)                                                                    # "?"
put(sfx, 5.58, bell(1568) + 0.6 * bell(2093), -12)                                                       # ding
for at in [6.45, 6.8, 7.15, 7.5]: put(sfx, at, crinkle(0.2), -14)                                       # folds
for k, f in enumerate([2637, 3136, 3951]): put(sfx, 7.94 + k * 0.06, bell(f, 0.6), -22)                  # sparkle
put(sfx, 8.66, whoosh(0.4, 400, 3500), -9)                                                               # throw
put(sfx, 9.95, whoosh(0.9, 500, 2200), -18)                                                              # loop
put(sfx, 12.36, bell(880, 0.5) * np.sign(np.sin(np.linspace(0, 300, int(0.5 * SR)))) * 0.5, -20)        # "!" sting
put(sfx, 12.5, whoosh(0.7, 300, 2800), -8)                                                               # fly-over
put(sfx, 13.9, boing(900, 0.15), -20)                                                                    # sweat drop plip
put(sfx, 14.3, whoosh(0.35, 500, 3000), -16)                                                             # it comes back...
put(sfx, 14.6, thud(240, 0.2), -6); put(sfx, 14.6, boing(150, 0.7), -12)                                 # bonk
for k in range(5): put(sfx, 14.7 + k * 0.16, bell(3000 + 400 * (k % 3), 0.4), -25)                       # stars
for k, n in enumerate([74, 71]): put(sfx, 11.5 + k * 0.32, pluck(n, 0.5, 0.7), -23)                   # "hmm, where did it go?"
put(sfx, 16.28, boing(420, 0.4), -15)                                                                     # pop off the head
put(sfx, 16.86, crinkle(0.12), -13)                                                                      # catch
put(sfx, 17.3, bell(2637, 1.0) + 0.5 * bell(3520, 1.0), -15)                                             # wink ting

mix = mus * 0.9 + sfx
mix[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))
st = np.stack([mix, mix], 1)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st / max(1e-9, np.max(np.abs(st))) * 0.89, -1, 1) * 32767).astype("<i2").tobytes())
print("wrote", sys.argv[1])
