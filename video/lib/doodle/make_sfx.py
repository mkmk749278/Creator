#!/usr/bin/env python3
"""Synthesise the doodle sound effects (pop, whoosh, scribble, rip, thud, clink, squeak) and mix them on SCENE.sfx cues.

Seeded numpy synthesis, no samples, so no licence questions; swap in recorded CC0 effects (Freesound) later if wanted.
Levels follow PLAYBOOK §11: impacts about -7 dB, small effects about -9 dB (relative to full scale before the master).
Usage: python3 make_sfx.py params.js out.wav
"""
import json, re, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(12)


def env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)


def noise(n):
    return rng.standard_normal(n)


def lp(x, k):           # one-pole low-pass, k in (0, 1): smaller = darker
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc); y[i] = acc
    return y


def bp(x, lo, hi):      # crude band-pass via FFT mask
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 28) + 260
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.03)


def whoosh():
    n = int(0.55 * SR); t = np.arange(n) / SR
    x = noise(n); out = np.zeros(n)
    for i in range(0, n, 2048):   # sweep a band upward
        c = 300 + 2600 * (i / n)
        seg = x[i:i + 2048]; out[i:i + len(seg)] = bp(seg, c * 0.6, c * 1.4)
    return out * np.sin(np.pi * t / t[-1]) ** 2 * 1.6


def scribble():
    n = int(0.9 * SR); t = np.arange(n) / SR
    strokes = (np.sin(2 * np.pi * 7.5 * t) > -0.2).astype(float)
    return bp(noise(n), 1800, 7000) * strokes * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)) * 0.7


def rip():
    n = int(0.35 * SR)
    grains = (rng.random(n) < 0.04).astype(float) * rng.random(n)
    return bp(grains * 6 + noise(n) * 0.25, 900, 6500) * env(n, 0.01, 0.16)


def thud():
    n = int(0.3 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (110 * np.exp(-t * 9) + 45) * t) * env(n, 0.002, 0.08)
    return body + lp(noise(n), 0.08) * env(n, 0.001, 0.02) * 0.8


def clink():
    n = int(0.6 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(2350, 1), (3720, .6), (5110, .4), (6680, .25)])
    s2 = np.roll(s, int(0.07 * SR)) * 0.6   # a second coin
    return (s + s2) * env(n, 0.001, 0.12) * 0.5


def squeak():
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 1500 + 300 * np.sin(2 * np.pi * 4 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * bp(noise(n), 800, 3000) * 0.9 * np.sin(np.pi * t / t[-1])


def buzz():   # phone vibrating on a wooden desk: ~170 Hz motor, rattle harmonics, a little wood knock
    n = int(0.42 * SR); t = np.arange(n) / SR
    motor = np.sign(np.sin(2 * np.pi * 172 * t)) * 0.5 + np.sin(2 * np.pi * 344 * t) * 0.3
    rattle = bp(noise(n), 300, 2400) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 172 * t)))
    shape = np.minimum(1, t / 0.02) * np.minimum(1, (t[-1] - t) / 0.04)
    return lp(motor + rattle * 0.35, 0.35) * shape


def tick():   # soft clock tick for counters
    n = int(0.05 * SR)
    return bp(noise(n), 2000, 6000) * env(n, 0.0005, 0.008)


SOUNDS = {"buzz": (buzz, -11), "tick": (tick, -20), "pop": (pop, -9), "whoosh": (whoosh, -12), "scribble": (scribble, -15), "rip": (rip, -8),
          "thud": (thud, -7), "clink": (clink, -10), "squeak": (squeak, -14)}

if __name__ == "__main__":
    js = open(sys.argv[1]).read()
    m = re.search(r'"duration":\s*([\d.]+)', js)
    if m:   # generated params.js: a JSON object after "window.SCENE ="
        scene = json.loads(js[js.index("=") + 1:].strip().rstrip(";"))
        dur, cues = float(scene["duration"]), scene.get("sfx", [])
    else:   # hand-written params.js (the doodle sample)
        dur = float(re.search(r"duration:\s*([\d.]+)", js).group(1))
        cues = json.loads(re.search(r"sfx:\s*(\[\[.*?\]\])", js, re.S).group(1).replace("'", '"'))
    mix = np.zeros(int(dur * SR) + SR)
    for at, name in cues:
        fn, db = SOUNDS[name]; x = fn(); x = x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
        i = int(at * SR); mix[i:i + len(x)] += x[: len(mix) - i]
    mix = mix[: int(dur * SR)]
    st = np.stack([mix, mix], 1)
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
    print("wrote", sys.argv[2], len(cues), "cues")
