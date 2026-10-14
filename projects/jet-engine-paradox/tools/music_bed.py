#!/usr/bin/env python3
"""Music bed for The Jet Engine Paradox from licensed tracks, with charter levels (owner, 2026-10-14: "you source a soundtrack").

  python3 tools/music_bed.py VO_PROGRAM.wav OUT.wav

Tracks (Kevin MacLeod, incompetech.com, CC BY 4.0; credited in the description) in assets/music/:
  Interloper         0:00 -> crossfade at the science section   (tension: hook, betrayal, the ghost of Kaveri)
  Long Note Four     science section                             (mystery: inside the engine)
  Lasting Hope       J071 "But the Kaveri story did not end" -> end card (hope: the turning point, the verdict)
Each track is normalised to the same loudness. The gain follows the VO program (voice + diegetic clip sound): about
14 dB under the voice while it speaks, rising to about 6 dB under it in pauses, with 0.5 s ramps (charter: BGM -24 to
-26 dB under speech, -12 dB in pauses). Before each core reveal the music cuts to total silence for 1.5 s, then a low
thud lands (charter). Deterministic: same inputs, same output.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 48000
P = Path(__file__).resolve().parent.parent
M = P / "assets" / "music"
PROG = json.loads((P / "align" / "program.json").read_text())
LINE = {x["id"]: x for x in PROG["lines"]}
END = PROG["total"]
SILENCES = [b["start"] for b in PROG["breaks"] if b["kind"] == "VO_PAUSE" and b["after"] in ("J019", "J053")]
X_SCIENCE = 258.0                      # Interloper (263 s) hands over to Long Note Four on "go inside the engine"
X_HOPE = LINE["J071"]["start"] - 0.5   # "But the Kaveri story did not end in two thousand eight."
SECTIONS = [("Interloper.mp3", 0.0, 0.0), ("Long_Note_Four.mp3", X_SCIENCE, 20.0), ("Lasting_Hope.mp3", X_HOPE, 0.0)]
XF = 5.0                               # crossfade seconds
UNDER, PAUSE = -14.0, -6.0             # music loudness relative to the voice, under speech / in pauses (≈ -28 / -20 LUFS after the -14 LUFS master)
RAMP = 0.5


def load(f, ss=0.0):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", str(f), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def lufs(x):
    """integrated loudness via ffmpeg ebur128 (exact, same meter as the master pass)"""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-af", "ebur128", "-f", "null", "-"], input=x.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float(r[r.rindex("I:"):].split()[1])


def main(vo_path, out_path):
    n = int((END + 1) * SR)
    bed = np.zeros((n, 2), np.float32)
    ref = -20.0
    for i, (name, at, ss) in enumerate(SECTIONS):
        x = load(M / name, ss)
        x *= 10 ** ((ref - lufs(x)) / 20)
        stop = SECTIONS[i + 1][1] + XF if i + 1 < len(SECTIONS) else END + 1
        a, b = int(at * SR), min(n, int(stop * SR))
        x = x[: b - a]
        env = np.ones(len(x), np.float32)
        if i > 0:
            k = min(len(x), int(XF * SR)); env[:k] = np.linspace(0, 1, k)
        if i + 1 < len(SECTIONS):
            k = min(len(x), int(XF * SR)); env[-k:] = np.minimum(env[-k:], np.linspace(1, 0, k))
        else:
            k = int(4.0 * SR); env[-k:] = np.minimum(env[-k:], np.linspace(1, 0, k))   # last 4 s fade out
        bed[a:a + len(x)] += x * env[:, None]

    # gain automation from the voice: speech mask on 50 ms RMS, bridged over short gaps, slewed with 0.5 s ramps
    vo = load(vo_path)
    vo_l = lufs(vo)
    hop = int(0.05 * SR)
    m = len(vo) // hop
    rms = np.sqrt(np.mean(vo[: m * hop].reshape(m, hop, 2) ** 2, axis=(1, 2))) + 1e-9
    speech = 20 * np.log10(rms) > -42
    bridge = int(0.9 / 0.05)               # pauses shorter than 0.9 s stay ducked (no pumping between words)
    idx = np.flatnonzero(speech)
    for p, q in zip(idx[:-1], idx[1:]):
        if 1 < q - p <= bridge:
            speech[p:q] = True
    lead = int(RAMP / 0.05)                # start ducking a ramp before speech so the first word is clean
    sp = speech.copy()
    for j in np.flatnonzero(speech):
        sp[max(0, j - lead):j] = True
    target = np.where(sp, vo_l + UNDER - ref, vo_l + PAUSE - ref)   # dB gain applied to the -20 LUFS bed
    g = np.empty_like(target); g[0] = target[0]
    step = (PAUSE - UNDER) / (RAMP / 0.05)
    for j in range(1, len(target)):
        d = target[j] - g[j - 1]
        g[j] = g[j - 1] + np.clip(d, -step, step)
    gain = np.interp(np.arange(n) / SR, np.arange(len(g)) * 0.05, 10 ** (g / 20), right=10 ** (g[-1] / 20)).astype(np.float32)
    for s in SILENCES:                     # 1.5 s of total silence, 40 ms edges
        t = np.arange(n) / SR
        w = np.clip(np.minimum((t - s) / 0.04, (s + 1.5 - t) / 0.04), 0, 1)
        gain *= 1 - w
    bed *= gain[:, None]

    # low thud right after each silence: 42 Hz sine with a pitch drop + soft noise body
    for s in SILENCES:
        t = np.arange(int(2.5 * SR)) / SR
        f = 42 + 30 * np.exp(-t * 9)
        thud = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
        rng = np.random.default_rng(7)
        noise = np.convolve(rng.standard_normal(len(t)), np.ones(240) / 240, "same") * np.exp(-t * 6) * 0.35
        th = (thud + noise) * 10 ** ((vo_l - 4 - lufs(np.stack([thud + noise] * 2, 1))) / 20)
        a = int((s + 1.5) * SR)
        bed[a:a + len(th)] += np.stack([th, th], 1)[: n - a]

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le",
                    str(out_path)], input=np.clip(bed, -1, 1).astype(np.float32).tobytes(), check=True)
    print(f"bed: voice {vo_l:.1f} LUFS; music {UNDER:+.0f} dB under speech, {PAUSE:+.0f} dB in pauses; silences at {SILENCES}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
