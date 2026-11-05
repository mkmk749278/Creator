"""Synthesise a calm music bed + sound design for a narrated documentary (no samples, no licences).

Everything is generated from sine/noise primitives with a fixed seed, so the bed
is deterministic and royalty-free:
  - tanpura-style drone (Sa-Pa plucks with rich harmonics, slow decay)
  - soft pad chords that change every few bars
  - optional heartbeat that speeds up across a window (hypercapnic stress)
  - optional singing-bowl strikes
  - optional low "impact" swells

Usage: python scripts/make_bed.py cues.json out.wav
cues.json: {"duration": 430.0,
            "heartbeat": [{"start": 170, "end": 290, "bpm_from": 62, "bpm_to": 118}],
            "bowls": [300.0, 340.0],
            "impacts": [2.0, 145.0],
            "swells": [{"at": 140.0, "dur": 4.0}],
            "sections": [{"start": 0, "mood": "tense"}, {"start": 300, "mood": "calm"}]}
"""

import json
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(16)


def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = min(int(a * SR), n // 2), min(int(r * SR), n // 2)  # short segments: fades fit inside
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def tanpura_pluck(f, dur=3.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(1, 14):
        # jawari buzz: upper partials decay slower and beat slightly
        amp = 1 / k ** 0.9
        det = 1 + 0.0007 * k
        s += amp * np.sin(2 * np.pi * f * k * det * t) * np.exp(-t * (1.2 / (1 + 0.15 * k)))
    s *= np.minimum(1, t / 0.02)
    return s / 6


def lowpass(x, fc):
    return sosfilt(butter(2, fc / (SR / 2), "low", output="sos"), x)


def bandpass(x, lo, hi):
    return sosfilt(butter(2, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x)


def moving_average(x, k):
    c = np.cumsum(np.concatenate([np.full(k // 2, x[0]), x, np.full(k - k // 2, x[-1])]))
    return (c[k:] - c[:-k])[: len(x)] / k


def heartbeat(n, t0, t1, bpm0, bpm1, out):
    t = t0
    while t < t1:
        p = (t - t0) / (t1 - t0)
        bpm = bpm0 + (bpm1 - bpm0) * p
        gain = 0.35 + 0.45 * p
        for off, g in ((0.0, 1.0), (0.24, 0.7)):  # lub-dub
            i = int((t + off) * SR)
            m = int(0.18 * SR)
            if i + m >= n:
                continue
            tt = np.arange(m) / SR
            thump = np.sin(2 * np.pi * (55 - 60 * tt) * tt) * np.exp(-tt * 28)
            out[i:i + m] += gain * g * thump * 0.9
        t += 60 / bpm


def bowl(at, n, out, f=233.0):
    m = min(int(9 * SR), n - int(at * SR))
    if m <= 0:
        return
    tt = np.arange(m) / SR
    s = (np.sin(2 * np.pi * f * tt) + 0.6 * np.sin(2 * np.pi * f * 2.71 * tt) * np.exp(-tt * 0.5)
         + 0.35 * np.sin(2 * np.pi * f * 5.18 * tt) * np.exp(-tt * 0.9))
    s *= np.exp(-tt * 0.32) * (1 + 0.25 * np.sin(2 * np.pi * 3.1 * tt)) * np.minimum(1, tt / 0.005)
    i = int(at * SR)
    out[i:i + m] += 0.22 * s


def impact(at, n, out):
    m = min(int(4 * SR), n - int(at * SR))
    if m <= 0:
        return
    tt = np.arange(m) / SR
    s = np.sin(2 * np.pi * (48 * np.exp(-tt * 0.6)) * tt) * np.exp(-tt * 1.4)
    s += lowpass(rng.standard_normal(m), 400) * np.exp(-tt * 3) * 0.3
    i = int(at * SR)
    out[i:i + m] += 0.55 * s


def swell(at, dur, n, out):
    m = int(dur * SR)
    i = int(max(0, at - dur) * SR)
    m = min(m, n - i)
    tt = np.arange(m) / SR
    s = bandpass(rng.standard_normal(m), 150, 2400) * (tt / dur) ** 2.2
    out[i:i + m] += 0.18 * s


def main():
    cues = json.loads(open(sys.argv[1]).read())
    dur = cues["duration"]
    n = int(dur * SR)
    t = np.arange(n) / SR
    drone = np.zeros(n)
    pad = np.zeros(n)
    fx = np.zeros(n)

    sa = 130.81  # C3 tonic
    # Tanpura cycle: Pa Sa Sa Sa(low), ~4.4 s per cycle
    cycle = [(sa * 1.5 / 2, 0.0), (sa, 1.1), (sa, 2.2), (sa / 2, 3.3)]
    c = 0.0
    while c < dur:
        for f, off in cycle:
            i = int((c + off) * SR)
            p = tanpura_pluck(f)
            m = min(len(p), n - i)
            if m > 0:
                drone[i:i + m] += p[:m]
        c += 4.4
    drone = lowpass(drone, 2600)

    # Pad: slow chords (i - VI - III - VII in C minor), 17.6 s each = 4 tanpura cycles
    chords = [[1, 1.189, 1.498], [0.794, 1, 1.189], [1.189, 1.498, 1.782], [0.891, 1.122, 1.335]]
    seg = 17.6
    k = 0
    while k * seg < dur:
        i0 = int(k * seg * SR)
        m = min(int((seg + 3) * SR), n - i0)
        tt = np.arange(m) / SR
        s = np.zeros(m)
        for r in chords[k % 4]:
            for det in (0.998, 1.002):
                s += np.sin(2 * np.pi * sa * 2 * r * det * tt + rng.uniform(0, 6.28))
        s *= env_adsr(m, 3.0, 3.0)
        pad[i0:i0 + m] += s / 6
        k += 1
    pad = lowpass(pad, 1400)
    # Breath-like air: very slow filtered noise swells
    air = bandpass(rng.standard_normal(n), 300, 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 11.0)) ** 2

    # Mood: tense sections lean on drone + air, calm sections on pad + bowls
    mood_pad = np.full(n, 0.7)
    mood_drone = np.full(n, 0.8)
    for s in cues.get("sections", []):
        i = int(s["start"] * SR)
        if s["mood"] == "tense":
            mood_pad[i:], mood_drone[i:] = 0.45, 1.0
        elif s["mood"] == "calm":
            mood_pad[i:], mood_drone[i:] = 0.9, 0.7
        else:
            mood_pad[i:], mood_drone[i:] = 0.7, 0.8
    mood_pad = moving_average(mood_pad, int(2.5 * SR))
    mood_drone = moving_average(mood_drone, int(2.5 * SR))

    for h in cues.get("heartbeat", []):
        heartbeat(n, h["start"], h["end"], h["bpm_from"], h["bpm_to"], fx)
    for b in cues.get("bowls", []):
        bowl(b, n, fx)
    for a in cues.get("impacts", []):
        impact(a, n, fx)
    for s in cues.get("swells", []):
        swell(s["at"], s["dur"], n, fx)

    music = drone * mood_drone * 0.55 + pad * mood_pad * 0.5 + air * 0.035
    mix = music + fx
    fade = env_adsr(n, 2.0, 4.0)
    mix *= fade
    mix /= np.max(np.abs(mix)) + 1e-9
    mix *= 0.9
    # Gentle stereo: tiny delay on the right channel
    d = int(0.011 * SR)
    right = np.concatenate([np.zeros(d), mix[:-d]])
    sf.write(sys.argv[2], np.stack([mix, right], 1).astype(np.float32), SR)
    print(f"wrote {sys.argv[2]} ({dur:.1f}s)")


if __name__ == "__main__":
    main()
