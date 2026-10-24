#!/usr/bin/env python3
"""Jet engine film v2 sound: synthesised music bed + SFX (deterministic, licence-free), then the master mix with the VO.

Adapted from projects/rare-earth-magnets/build/make_sound.py. Cues come from the 4K edit itself
(video/jet-engine-bet/assemble/assemble_4k.py SHOTS), so they move with the picture:
- a soft click on every on-screen label, a low whoosh into every real-footage shot that follows a CG/scene shot,
  a jet rumble under shots of a Tejas in flight;
- the bed goes silent for 1.5 s before each core reveal and lands a low hit on it (CLAUDE.md audio rule);
- mix: VO leads, bed -11 dB ducked by a sidechain compressor, SFX -9 dB; two-pass linear gain to -14 LUFS, TP limiter.
Usage: python3 projects/jet-engine-bet/build/make_sound.py   -> projects/jet-engine-bet/assets/audio/{bed,sfx,master}.wav
"""
import importlib.util, subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("a4k", ROOT / "video/jet-engine-bet/assemble/assemble_4k.py")
A = importlib.util.module_from_spec(spec); sys.argv = sys.argv[:1]; spec.loader.exec_module(A)
SHOTS = sorted(A.SHOTS, key=lambda s: s["t0"])
SR = 48000; DUR = A.END; N = int(DUR * SR)
OUT = ROOT / "projects/jet-engine-bet/assets/audio"; OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(31); t_all = np.arange(N) / SR

def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "highpass", fs=SR, output="sos"), x)
def env(n, a, r, shape=1.0):
    e = np.ones(n); na, nr = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    e[:na] = np.linspace(0, 1, na) ** shape; e[-nr:] *= np.linspace(1, 0, nr) ** shape; return e
def put(track, at, x, gain=1.0):
    i = int(at * SR); j = min(N, i + len(x));
    if i < N: track[i:j] += gain * x[: j - i]
def tone(f, d, a=0.005, r=0.2, harm=(1.0,)):
    t = np.arange(int(d * SR)) / SR; return sum(h * np.sin(2 * np.pi * f * (k + 1) * t) for k, h in enumerate(harm)) * env(len(t), a, r)
def noise(d): return rng.standard_normal(int(d * SR))

# ---------------- bed: sections follow the film's chapters ----------------
CHORDS = {"tense": [(110.0, 130.8, 164.8), (98.0, 116.5, 146.8)], "calm": [(130.8, 164.8, 196.0), (110.0, 138.6, 164.8)],
          "drive": [(146.8, 174.6, 220.0), (130.8, 155.6, 196.0)], "hope": [(130.8, 164.8, 196.0), (146.8, 185.0, 220.0)]}
SECTIONS = [(0, "tense"), (41.8, "drive"), (79.5, "drive"), (143.2, "tense"), (174.8, "calm"), (255.5, "tense"), (285.1, "drive"),
            (326.7, "tense"), (392.6, "calm"), (436.0, "hope"), (456.3, "drive"), (494.7, "hope"), (507.1, "hope")]
SECTIONS = [(A.M(t), m) for t, m in SECTIONS]   # old voice-over times -> the re-take timeline (splices.json)
REVEALS = [A.M(t) for t in (30.5, 141.4, 164.2, 367.0, 479.5)]   # "Nothing." / "Directly behind the fire." / the 470° gap / May 1998 / the decision
bed = np.zeros(N)
for si, (s0, mood) in enumerate(SECTIONS):
    s1 = SECTIONS[si + 1][0] if si + 1 < len(SECTIONS) else DUR
    bar = 4.0; k = 0; t = s0
    while t < s1:
        d = min(bar, s1 - t); ch = CHORDS[mood][k % 2]; n = int(d * SR); tt = np.arange(n) / SR
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.003 * tt) + 0.25 * np.sin(2 * np.pi * f * 0.5 * tt) for f in ch)
        put(bed, t, lp(pad, 900) * env(n, 0.8, 0.8) * 0.05); t += bar; k += 1
    bpm = {"tense": 70, "drive": 92, "calm": 0, "hope": 0}[mood]
    if bpm:
        p = 60 / bpm; t = s0
        while t < s1 - 0.2:
            put(bed, t, tone(52, 0.35, 0.002, 0.3, (1.0, 0.3)) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9), 0.16); t += p
bed += lp(hp(rng.standard_normal(N), 4000), 9000) * (0.004 + 0.003 * np.sin(2 * np.pi * t_all / 11))
for at in REVEALS:
    i, j = int((at - 1.5) * SR), int(at * SR); ramp = int(0.25 * SR)
    bed[i - ramp:i] *= np.linspace(1, 0, ramp); bed[i:j] = 0; bed[j:j + ramp] *= np.linspace(0, 1, ramp)
    hit = (tone(41, 2.4, 0.003, 2.0, (1.0, 0.5, 0.25)) + lp(noise(2.4), 200) * 0.6) * np.exp(-np.arange(int(2.4 * SR)) / SR * 1.6)
    put(bed, at, hit, 0.5)
e0 = int(A.M(507.1) * SR); bed[e0:] *= np.linspace(1.0, 2.2, N - e0)   # end card: the music carries it
bed *= env(N, 1.5, 3.0)
sf.write(OUT / "bed.wav", (bed / np.max(np.abs(bed)) * 0.6).astype(np.float32), SR)

# ---------------- sfx from the edit ----------------
def whoosh(d=0.6, up=True):
    n = int(d * SR); x = noise(d + 0.02); c = np.linspace(400, 3000, n) if up else np.linspace(3000, 400, n); y = np.zeros(n); sg = 2048
    for i in range(0, n, sg): y[i:i + sg] = bp(x[i:i + sg + 512], max(100, c[i] * 0.5), min(20000, c[i] * 1.6))[: len(y[i:i + sg])]
    return y * env(n, d * 0.5, d * 0.5, 2) * 0.6
def click(f=2200, d=0.03): return bp(noise(d), f * 0.7, f * 1.4) * env(int(d * SR), 0.001, 0.02) * 0.8
def rumble(d):   # distant jet: low filtered noise swell
    return lp(hp(noise(d), 40), 380) * env(int(d * SR), d * 0.35, d * 0.45, 1.5) * 1.4
fx = np.zeros(N)
REALJET = ("ryolgbuDNSg", "tvid_36", "52f1mQqaii8", "tejas_28", "tejas_23", "tejas_24", "mk1a_37")
for k, s in enumerate(SHOTS):
    t1 = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else DUR
    real = s["kind"] in ("p",) or s["credit"]
    prev_cg = k and (SHOTS[k - 1]["ill"] or SHOTS[k - 1]["kind"] == "cg")
    if real and prev_cg: put(fx, max(0, s["t0"] - 0.35), whoosh(0.5), 0.22)
    if any(r in s["src"].name for r in REALJET): put(fx, s["t0"], rumble(t1 - s["t0"]), 0.5)
    for (a, b, _) in s["labels"]: put(fx, a, click(), 0.35)
put(fx, A.M(33.6), whoosh(0.8, False), 0.3)   # whip out of the tunnel
sf.write(OUT / "sfx.wav", (fx / max(1e-9, np.max(np.abs(fx))) * 0.7).astype(np.float32), SR)

# ---------------- master ----------------
def ff(*a): r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], capture_output=True, text=True); r.returncode and sys.exit(r.stderr[-1500:])
def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    v = [l.split()[1] for l in r.stderr.splitlines() if l.strip().startswith("I:")]; return float(v[-1])
mix = (f"[0:a]aresample=48000,aformat=channel_layouts=mono,apad=whole_dur={DUR},asplit=2[v][vsc];"
       f"[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-11dB,atrim=0:{DUR}[bedraw];"
       "[bedraw][vsc]sidechaincompress=threshold=0.015:ratio=7:attack=40:release=650:makeup=1[bed];"
       f"[2:a]aresample=48000,aformat=channel_layouts=mono,volume=-9dB,atrim=0:{DUR}[fx];"
       "[v][bed][fx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95,pan=stereo|c0=c0|c1=c0[m]")
ff("-i", str(A.VO), "-i", str(OUT / "bed.wav"), "-i", str(OUT / "sfx.wav"), "-filter_complex", mix, "-map", "[m]", "-ar", "48000", str(OUT / "mix.wav"))
src = OUT / "mix.wav"
for k in (1, 2):
    g = -14 - lufs(src); dst = OUT / ("m1.wav" if k == 1 else "master.wav")
    ff("-i", str(src), "-af", f"volume={g}dB,alimiter=limit=0.84:level=false:attack=2:release=60", "-ar", "48000", str(dst)); src = dst
print(f"master -> {OUT / 'master.wav'}  ({lufs(OUT / 'master.wav'):.1f} LUFS)")
