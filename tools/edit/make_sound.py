#!/usr/bin/env python3
# Reusable tool kept from an earlier film (repo slimmed 2026-11-05): adapt the paths at the top to the new film.
"""India-own-AI film sound: the ElevenLabs score laid by chapter (assets/audio/music) and the ElevenLabs SFX on their
events (assets/audio/sfx), from build/sound.json (written by make_film.py). Music cues cross-fade over 2 s; the bed is
silent in SILENT windows (CLAUDE.md: 1.5 s of silence before each core reveal). assemble.sh ducks the bed under the VO.
Usage: python3 projects/india-own-ai/build/make_sound.py  -> assets/audio/{bed,sfx}.wav (48 kHz mono)"""
import json, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
P = Path(__file__).resolve().parents[1]; A = P / "assets/audio"; SR = 48000
cfg = json.loads((P / "build/sound.json").read_text()); N = int(cfg["END"] * SR)


def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def norm(x, peak_db):
    p = np.max(np.abs(x)) or 1.0
    return x / p * 10 ** (peak_db / 20)


bed = np.zeros(N, np.float32); XF = 2.0
for name, t0, src, t1 in cfg["MUSIC"]:
    x = norm(load(A / "music" / f"{name}.mp3"), -3.0)
    seg = x[int(src * SR): int(src * SR) + int((t1 - t0 + XF) * SR)]
    n = len(seg); e = np.ones(n, np.float32); f = min(int(XF * SR), n // 2)
    e[:f] = np.linspace(0, 1, f); e[-f:] *= np.linspace(1, 0, f)
    i = int(t0 * SR); j = min(N, i + n); bed[i:j] += (seg * e)[: j - i]
for a, b in cfg["SILENT"]:      # silence windows with 0.25 s ramps
    i, j = int(a * SR), int(b * SR); r = int(0.25 * SR)
    bed[max(0, i - r): i] *= np.linspace(1, 0, min(r, i))
    bed[i:j] = 0; bed[j: j + r] *= np.linspace(0, 1, len(bed[j: j + r]))
fx = np.zeros(N, np.float32); cache = {}
for name, at, gain in cfg["SFX"]:
    if name not in cache:
        cache[name] = norm(load(A / "sfx" / f"{name}.mp3"), -6.0)
    x = cache[name] * 10 ** (gain / 20); i = int(at * SR); j = min(N, i + len(x)); fx[i:j] += x[: j - i]
sf.write(A / "bed.wav", bed, SR); sf.write(A / "sfx.wav", np.clip(fx, -1, 1), SR)
print("bed", round(len(bed) / SR, 1), "s; sfx events", len(cfg["SFX"]))
