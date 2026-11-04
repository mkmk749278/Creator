#!/usr/bin/env python3
"""Synthesise the film's 16 sound effects in code into assets/audio/sfx/<name>.mp3 (48 kHz mono).

Why (owner, 2026-11-04): the r1 ElevenLabs SFX were never saved to Drive; the "our country" re-cut moved the VO, so
the mix had to be rebuilt; the environment's ElevenLabs key lacks sound_generation, the connector account had no
credits, and Openverse's Freesound/Wikimedia downloads return 403/429 from the container. The owner chose effects
made in code: no licence, no third party, fully reproducible (seeded noise, pure functions).
usage: python3 projects/india-own-ai/tools/synth_sfx.py      (needs numpy, scipy, soundfile, ffmpeg)
"""
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
OUT = Path(__file__).resolve().parents[1] / "assets/audio/sfx"
RNG = np.random.default_rng(20261104)


def t(d):
    return np.arange(int(d * SR)) / SR


def noise(d):
    return RNG.standard_normal(int(d * SR))


def bp(x, lo, hi, order=4):
    return signal.sosfilt(signal.butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def lp(x, f, order=4):
    return signal.sosfilt(signal.butter(order, f, "lowpass", fs=SR, output="sos"), x)


def hp(x, f, order=4):
    return signal.sosfilt(signal.butter(order, f, "highpass", fs=SR, output="sos"), x)


def env(n, a, dec):
    """attack a seconds (linear), then exponential decay with time constant dec seconds"""
    tt = np.arange(n) / SR
    e = np.exp(-np.maximum(tt - a, 0) / dec)
    if a > 0:
        e *= np.minimum(tt / a, 1)
    return e


def place(buf, x, at):
    i = int(at * SR); j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i]


def tick(f=2600, d=0.04, bright=1.0):
    x = np.sin(2 * np.pi * f * t(d)) * 0.6 + bp(noise(d), 2000, 9000) * 0.25 * bright
    return x * env(len(x), 0.0006, 0.008)


def bell(f, d, partials=((1, 1), (2.76, 0.45), (5.4, 0.25), (8.93, 0.12)), dec=0.5):
    tt = t(d)
    return sum(a * np.sin(2 * np.pi * f * r * tt) * np.exp(-tt / (dec / r ** 0.5)) for r, a in partials) * env(len(tt), 0.002, 10)


def fade(x, fi=0.005, fo=0.05):
    n = len(x); a, b = int(fi * SR), int(fo * SR)
    x[:a] *= np.linspace(0, 1, a); x[n - b:] *= np.linspace(1, 0, b)
    return x


def make():
    S = {}
    S["tile_tick"] = np.concatenate([tick(2400), np.zeros(int(0.2 * SR))])
    run = np.zeros(int(1.5 * SR)); at = 0.0
    for k in range(9):
        place(run, tick(2200 + 140 * k + RNG.uniform(-60, 60), bright=0.8) * (0.7 + 0.3 * k / 8), at)
        at += 0.13 - 0.008 * k
    S["tile_run"] = run
    cnt = np.zeros(int(2.0 * SR)); at = 0.0; gap = 0.11
    while at < 1.6:
        c = bp(noise(0.012), 2500, 6000) * env(int(0.012 * SR), 0.0003, 0.003) + tick(1800, 0.012, 0.3) * 0.4
        place(cnt, c, at); at += gap; gap = max(0.035, gap * 0.9)
    place(cnt, bp(noise(0.03), 1500, 5000) * env(int(0.03 * SR), 0.0005, 0.008) * 1.4, at + 0.02)   # the stop
    S["counter_tick"] = cnt
    kb = np.zeros(int(2.5 * SR)); at = 0.05
    while at < 2.3:
        tap = lp(noise(0.03), 2500) * env(int(0.03 * SR), 0.001, 0.006) + np.sin(2 * np.pi * 180 * t(0.03)) * env(int(0.03 * SR), 0.001, 0.008) * 0.5
        place(kb, tap * RNG.uniform(0.6, 1.0), at); at += RNG.uniform(0.09, 0.2)
    S["keyboard_type"] = kb
    lk = np.zeros(int(1.0 * SR))
    for at, g in ((0.05, 0.7), (0.11, 1.0)):
        c = hp(noise(0.004), 3000) * env(int(0.004 * SR), 0, 0.001) * 2
        ring = sum(np.sin(2 * np.pi * f * t(0.25)) * a for f, a in ((3150, 0.5), (5120, 0.3), (7300, 0.15))) * env(int(0.25 * SR), 0, 0.03)
        place(lk, c * g, at); place(lk, ring * g * 0.5, at)
    S["lock_click"] = lk
    p = np.zeros(int(1.0 * SR))
    place(p, bell(1320, 0.8, ((1, 1), (2, 0.25)), dec=0.25), 0.0); place(p, bell(1760, 0.8, ((1, 1), (2, 0.2)), dec=0.3) * 0.8, 0.09)
    S["notify_ping"] = p
    ch = np.zeros(int(1.6 * SR))
    place(ch, bell(1046.5, 1.4, dec=0.7), 0.0); place(ch, bell(1568, 1.3, dec=0.8) * 0.9, 0.14)
    S["chime_bright"] = ch
    tt = t(1.5); fr = 45 + 40 * np.exp(-tt / 0.06)
    th = np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(len(tt), 0.004, 0.35) + lp(noise(1.5), 400) * env(len(tt), 0.001, 0.03) * 0.6
    S["low_thud"] = th
    tt = t(1.2); fr = 70 + 60 * np.exp(-tt / 0.03)
    S["brick_thud"] = (np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(len(tt), 0.002, 0.12)
                       + bp(noise(1.2), 150, 1800) * env(len(tt), 0.001, 0.05) * 0.9
                       + bp(noise(1.2), 1500, 5000) * env(len(tt), 0.0005, 0.01) * 0.3)
    tt = t(4.0)
    saw = sum(signal.sawtooth(2 * np.pi * f * tt) for f in (54.7, 55.3, 109.4, 110.8, 82.0)) / 5
    sweep = np.zeros_like(saw); blk = 2400
    for i in range(0, len(saw), blk):   # a filter that opens then closes, block-wise
        fc = 200 + 1400 * np.exp(-((i / SR - 0.35) ** 2) / 0.25)
        sweep[i:i + blk] = lp(saw[max(0, i - 4800):i + blk], fc, 2)[-len(saw[i:i + blk]):]
    S["braam"] = (sweep * 1.2 + np.sin(2 * np.pi * 41 * tt) * 0.8) * env(len(tt), 0.08, 1.4)
    gc = np.zeros(int(1.5 * SR)); at = 0.0
    for k in range(7):
        b = hp(noise(0.006), 2500) * env(int(0.006 * SR), 0, 0.0015) * (1.6 if k == 0 else RNG.uniform(0.4, 0.9))
        place(gc, b, at); at += RNG.uniform(0.008, 0.03)
    place(gc, sum(np.sin(2 * np.pi * f * t(0.6)) * a for f, a in ((3700, 0.25), (5900, 0.18), (8200, 0.1))) * env(int(0.6 * SR), 0, 0.09), 0.0)
    S["glass_crack"] = gc
    tt = t(1.2); sw = np.sin(np.pi * np.clip(tt / 0.45, 0, 1)) ** 2
    pt = bp(noise(1.2), 1500, 7000) * sw * 0.5 + bp(noise(1.2), 400, 2000) * sw * 0.3
    place(pt, bp(noise(0.03), 800, 4000) * env(int(0.03 * SR), 0.001, 0.008) * 1.2, 0.45)   # the page lands
    S["page_turn"] = pt
    rf = np.zeros(int(1.5 * SR)); at = 0.05
    for k in range(26):
        fl = bp(noise(0.02), 1800, 6500) * env(int(0.02 * SR), 0.001, 0.005)
        place(rf, fl * RNG.uniform(0.5, 1.0), at); at += 0.045 + 0.02 * np.sin(k)
    S["paper_riffle"] = rf
    tt = t(5.0)
    hum = sum(np.sin(2 * np.pi * 50 * h * tt) * a for h, a in ((1, 0.5), (2, 0.3), (3, 0.15), (6, 0.06)))
    fan = lp(noise(5.0), 900) * 0.6 + bp(noise(5.0), 2000, 5000) * 0.05
    S["server_hum"] = fade(hum * 0.5 + fan, 0.6, 0.8)
    tt = t(2.0); flow = bp(noise(2.0), 600, 5000) * (0.6 + 0.4 * np.abs(lp(noise(2.0), 30) * 3))
    flow *= np.clip(1 - (tt - 0.9) / 0.35, 0, 1)
    tt2 = t(0.12); drip = np.sin(2 * np.pi * np.cumsum(900 + 1400 * tt2 / 0.12) / SR) * env(len(tt2), 0.001, 0.02)
    place(flow, drip * 0.8, 1.55)
    S["water_stop"] = flow
    mb = bp(noise(3.0), 200, 2500) * 0.12 * np.clip(t(3.0) / 0.3, 0, 1)   # floor murmur
    for k in range(18):   # an electric bell: fast strikes on one bell
        place(mb, bell(880, 0.25, dec=0.15) * 0.5, 0.1 + k / 9)
    S["market_bell"] = fade(mb, 0.01, 0.4)
    return S


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, x in make().items():
        x = np.asarray(x, np.float32); x = x / (np.max(np.abs(x)) or 1) * 0.89   # -1 dBFS; make_sound.py renormalises
        wav = OUT / f"{name}.wav"; sf.write(wav, x, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "192k", str(OUT / f"{name}.mp3")], check=True)
        wav.unlink()
        print(f"{name}.mp3  {len(x) / SR:.2f} s")
