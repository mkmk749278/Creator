#!/usr/bin/env python3
"""Film 36 master audio: final VO + synthesised music bed + synthesised SFX, mixed and normalised.

Everything is generated (no samples, no licences): the bed comes from scripts/make_bed.py, the SFX
(dhol beats, relay clicks, breaker clunks, whooshes, test pings, ticks) are synthesised here with a fixed seed.
Cue times are film seconds, taken from the scene JS (scene start + local cue; see video/solar36/scenes.json).

Rules applied (CLAUDE.md audio): VO leads (peaks about -2 to -3 dB), bed ducked under speech by a sidechain,
1.5 s of total music silence before each core reveal and a low thud on it, small SFX -8 to -10 dB under the VO,
impacts -6 to -8 dB, master -14 LUFS by two-pass LINEAR gain + limiter.

  python3 projects/solar-anti-islanding/tools/build_audio.py      # writes assets/audio/{bed,sfx,master}.wav
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects/solar-anti-islanding"
OUT = PROJ / "assets/audio"
SR = 48000
DUR = 213.67                      # VO 207.67 s + 6 s end-screen tail (S10)
BEAT = 0.6
rng = np.random.default_rng(36)
S = {s["id"]: s["start"] for s in json.load(open(ROOT / "video/solar36/scenes.json"))}


def beats(sc, t0, t1):
    out, t = [], t0
    while t < t1 - 0.05:
        out.append(S[sc] + t); t += BEAT
    return out


DHOL = beats("S04", 6.0, 16.2) + beats("S04", 16.2, 22.555) + beats("S05", 0.1, 2.5) + beats("S07", 0.2, 7.0) \
    + [S["S07"] + t for t in np.arange(19.2, 24.3, BEAT)] + beats("S09", 15.7, 18.796)
REVEALS = [S["S05"] + 16.8, S["S06"] + 8.4, S["S07"] + 29.9]          # ≈ 11,000 V · the click · the 50.5 Hz trip
CLICKS = [9.6, S["S06"] + 8.4, S["S07"] + 29.9]
CLUNKS = [S["S05"] + 2.7, S["S07"] + 7.1, S["S09"] + 11.6]
THUNKS = [4.4]                                                          # the power cut in the hook
WHOOSH = [S["S03"] + 0.05, S["S06"] + 0.8, S["S07"] + 8.0, S["S10"] + 21.6, S["S04"] + 5.0, S["S07"] + 16.6,
          S["S05"] + 11.65, S["S05"] + 19.85, S["S07"] + 18.95, S["S09"] + 10.3, S["S10"] + 23.0, S["S02"] + 4.9]
PINGS = [S["S07"] + 17.3]
TICKS = [S["S07"] + t for t in (12.8, 14.0, 15.2, 16.4, 24.9, 26.2, 27.5, 28.65)] + [S["S02"] + 11.35]
BOWLS = [S["S10"] + 17.84, S["S10"] + 28.05]


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def add(buf, at, x, gain_db):
    i = int(at * SR); m = min(len(x), len(buf) - i)
    if m > 0: buf[i:i + m] += x[:m] * 10 ** (gain_db / 20)


def dhol(n=int(0.5 * SR)):
    t = np.arange(n) / SR
    f = 70 + 60 * np.exp(-t * 18)                                      # pitch drops like a struck bass head
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.16)
    slap = rng.standard_normal(n) * env(n, 0.0005, 0.012)
    return body + 0.25 * slap


def click(n=int(0.08 * SR)):
    t = np.arange(n) / SR
    return (rng.standard_normal(n) * env(n, 0.0002, 0.006) + 0.6 * np.sin(2 * np.pi * 2400 * t) * env(n, 0.0002, 0.01))


def clunk(n=int(0.6 * SR)):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 25)) * t) * env(n, 0.001, 0.12) + 0.4 * rng.standard_normal(n) * env(n, 0.0005, 0.02)


def whoosh(n=int(0.7 * SR)):
    x = rng.standard_normal(n); t = np.arange(n) / SR
    k = np.convolve(x, np.ones(40) / 40, mode="same")
    return k * np.sin(np.pi * t / t[-1]) ** 2 * 2.5


def ping(n=int(0.9 * SR)):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1320 * t) * env(n, 0.002, 0.25) + 0.3 * np.sin(2 * np.pi * 2640 * t) * env(n, 0.002, 0.12)


def tick(n=int(0.05 * SR)):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1800 * t) * env(n, 0.0003, 0.008)


def norm(x): return x / (np.max(np.abs(x)) + 1e-9)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # 1) music bed from make_bed.py (sections follow the film's mood), impacts on the reveals
    cues = {"duration": DUR, "impacts": REVEALS + THUNKS, "bowls": BOWLS,
            "sections": [{"start": 0, "mood": "tense"}, {"start": 51.3, "mood": "other"}, {"start": 73.9, "mood": "tense"},
                         {"start": 110.1, "mood": "other"}, {"start": 160.7, "mood": "calm"}]}
    (OUT / "bed_cues.json").write_text(json.dumps(cues))
    subprocess.run([sys.executable, str(ROOT / "scripts/make_bed.py"), str(OUT / "bed_cues.json"), str(OUT / "bed_raw.wav")], check=True)
    bed, _ = sf.read(OUT / "bed_raw.wav", dtype="float32")
    if bed.ndim == 1: bed = np.stack([bed, bed], 1)
    # 1.5 s of total music silence before each core reveal (0.15 s ramps); the impact lands on the reveal
    g = np.ones(len(bed))
    for r in REVEALS:
        a, b = int((r - 1.5) * SR), int(r * SR); ramp = int(0.15 * SR)
        g[a:b] = 0; g[a - ramp:a] = np.linspace(1, 0, ramp); g[b - int(0.02 * SR):b] = 0
    bed = bed * g[:, None]
    # 2) SFX track (mono → stereo), levels relative to a 0 dBFS-peak voice
    sfx = np.zeros(int(DUR * SR))
    d0, c0, k0, w0, p0, t0 = norm(dhol()), norm(click()), norm(clunk()), norm(whoosh()), norm(ping()), norm(tick())
    for t in DHOL: add(sfx, t, d0, -16)
    for t in CLICKS: add(sfx, t, c0, -8)
    for t in CLUNKS: add(sfx, t, k0, -9)
    for t in WHOOSH: add(sfx, t - 0.25, w0, -18)
    for t in PINGS: add(sfx, t, p0, -14)
    for t in TICKS: add(sfx, t, t0, -16)
    for t in REVEALS: add(sfx, t, k0, -7)                                # the low thud on each reveal
    sf.write(OUT / "bed.wav", bed.astype(np.float32), SR)
    sf.write(OUT / "sfx.wav", np.stack([sfx, sfx], 1).astype(np.float32), SR)
    # 3) mix: voice (leveled, padded), bed ducked by the voice, SFX on top; then one linear gain to -14 LUFS
    vo = PROJ / "voice/vo_v10_take3_edit.mp3"
    fc = (f"[0:a]aresample=48000,apad=whole_dur={DUR},highpass=f=70,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=150,"
          "aformat=channel_layouts=stereo,asplit=2[v][sc];"
          "[1:a]aresample=48000,volume=-17dB[b];[b][sc]sidechaincompress=threshold=0.015:ratio=10:attack=30:release=600[bd];"
          "[2:a]aresample=48000[fx];[v][bd][fx]amix=inputs=3:duration=first:normalize=0[a]")
    mix = OUT / "mix.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vo), "-i", str(OUT / "bed.wav"), "-i", str(OUT / "sfx.wav"),
                    "-filter_complex", fc, "-map", "[a]", "-t", str(DUR), "-c:a", "pcm_f32le", str(mix)], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mix), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float([l for l in r.split("Integrated loudness")[1].splitlines() if "I:" in l][0].split()[1])
    gain = -14 - I
    master = OUT / "master.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mix), "-af",
                    f"volume={gain:.2f}dB,alimiter=limit=0.76:attack=5:release=50:level=false,afade=t=out:st={DUR - 1.5}:d=1.5",
                    "-ar", "48000", "-c:a", "pcm_s16le", str(master)], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(master), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    summ = r.split("Summary:")[1]
    print(f"mix {I:.1f} LUFS -> gain {gain:+.2f} dB"); print(" ".join(summ.split()))


if __name__ == "__main__":
    main()
