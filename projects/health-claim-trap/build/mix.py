#!/usr/bin/env python3
"""Sound design for the film (owner, 2026-10-14: "some audio gap is totally silent; know the audio techniques").

Mixed in numpy at 48 kHz stereo, all gains as dB (charter sound matrix, CLAUDE.md):
  - VO leads; music bed rides -25 dB under speech and lifts to -13 dB in pauses (0.5 s ramps, sidechain-style);
    before the core reveal (E033) the music drops out for 1.5 s, but room tone and a soft riser stay: never digital silence.
  - room tone under the whole film (-40 dB) so no frame is ever silent;
  - hospital ambience under the real hospital clips, leading each clip by 0.4 s (J-cut) and tailing 0.3 s (L-cut);
  - whoosh on cuts between real footage and animation, impact on stamps/reveals, typing and clicks on the browser
    clips, a clock tick under the discharge stopwatch, a heartbeat under "your heart drops".
SFX: Freesound CC0 via Openverse (assets/sfx, logged in media_manifest.csv).
"""
import json, subprocess
import numpy as np
from pathlib import Path

SR = 48000
P = Path(__file__).resolve().parents[1]
A = P / "assets"; SFX = A / "sfx"


def load(path, ss=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{dur:.3f}"] if dur else []) + \
          ["-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def norm(c, target=-20.0):
    """Scale a clip to a target RMS (dBFS) so the gains below mean the same for every source file."""
    r = float(np.sqrt(np.mean(c ** 2)) + 1e-9)
    return c * (10 ** (target / 20) / r)


def db(x):
    return 10 ** (x / 20)


def place(buf, clip, t, gain_db=0.0, fade=0.01):
    i = int(t * SR)
    if i >= len(buf) or len(clip) == 0:
        return
    c = clip[: len(buf) - max(i, 0)].copy()
    if i < 0:
        c = c[-i:]; i = 0
    n = min(int(fade * SR), len(c) // 2)
    if n > 0:
        r = np.linspace(0, 1, n)[:, None]; c[:n] *= r; c[-n:] *= r[::-1]
    buf[i:i + len(c)] += c * db(gain_db)


def bed_loop(path, total):
    b = norm(load(path))
    reps = int(np.ceil(total * SR / len(b)))
    return np.tile(b, (reps, 1))[: int(total * SR)]




def build(shots, sent, end, reveal, inserts, browser_cues, stopwatch, out_path, vo_path, bed_path):
    total = end + 0.5
    N = int(total * SR)
    mix = np.zeros((N, 2), np.float32)
    vo = load(vo_path)[:N]
    mix[: len(vo)] += vo

    # ---- music bed with sidechain-style ducking ----
    fs = 100
    g = np.full(int(total * fs), -13.0)                      # pauses: -13 dB
    for s in sent:
        a, b = int((s["start"] - 0.15) * fs), int((s["end"] + 0.1) * fs)
        g[max(0, a):b] = -25.0                                # under speech: -25 dB
    a, b = int((reveal - 1.6) * fs), int((reveal - 0.05) * fs)
    g[a:b] = -80.0                                            # music out 1.5 s before the reveal (charter)
    k = int(0.5 * fs)
    g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]   # 0.5 s ramps
    gl = db(np.interp(np.arange(N) / SR, np.arange(len(g)) / fs, g)).astype(np.float32)[:, None]
    bed = load(bed_path)
    if len(bed) < N:
        bed = np.vstack([bed, np.zeros((N - len(bed), 2), np.float32)])
    mix += bed[:N] * gl

    # ---- room tone: never digital silence ----
    mix += bed_loop(SFX / "room_tone.mp3", total) * db(-24)   # normalised to -20 dBFS first: about -44 dBFS

    # ---- hospital ambience under real hospital clips (J/L cuts) ----
    amb = bed_loop(SFX / "hosp_amb.mp3", total)
    ag = np.zeros(int(total * fs))
    for t0, t1, hospital in inserts:
        if hospital:
            ag[max(0, int((t0 - 0.4) * fs)):int((t1 + 0.3) * fs)] = 1.0
    k = int(0.35 * fs)
    ag = np.convolve(np.pad(ag, (k, k)), np.ones(k) / k, mode="same")[k:-k]
    mix += amb * (np.interp(np.arange(N) / SR, np.arange(len(ag)) / fs, ag).astype(np.float32)[:, None] * db(-10))

    # ---- whooshes on footage <-> animation cuts, at least 2.5 s apart ----
    swish, swipe, deep = (norm(load(SFX / f)) for f in ("whoosh_swish.mp3", "whoosh_swipe.mp3", "whoosh_deep.mp3"))
    last = -9
    for i in range(1, len(shots)):
        a_, b_ = shots[i - 1]["kind"], shots[i]["kind"]
        t = shots[i]["t"]
        if (a_ == "clip") != (b_ == "clip") or (a_ == b_ == "scene" and shots[i - 1].get("id") != shots[i].get("id")):
            if t - last >= 2.5 and abs(t - reveal) > 3:
                place(mix, swish if i % 2 else swipe, t - 0.18, -16)
                last = t
    # ---- reveal: riser into a soft cinematic impact; stamps ----
    riser = norm(load(SFX / "riser.mp3"))
    e = np.convolve((riser ** 2).mean(1), np.ones(SR // 10) / (SR // 10), mode="same")
    pk = int(np.argmax(e))                                    # the riser's loudest point lands on the reveal
    rs = riser[max(0, pk - int(4.0 * SR)):pk]
    place(mix, rs, reveal - len(rs) / SR, -14, fade=0.6)
    place(mix, norm(load(SFX / "impact_soft.mp3")), reveal - 0.05, -6)
    place(mix, deep, reveal - 2.6, -22, fade=0.5)
    stamp = norm(load(SFX / "stamp.mp3"))
    for t in browser_cues.get("stamps", []):
        place(mix, stamp, t, -10)
    # ---- browser clips: typing and clicks ----
    typing, click = norm(load(SFX / "typing.mp3")), norm(load(SFX / "click.mp3"))
    for t0, t1 in browser_cues.get("typing", []):
        place(mix, typing[: int((t1 - t0) * SR)], t0, -20, fade=0.05)
    for t in browser_cues.get("clicks", []):
        place(mix, click[: int(0.35 * SR)], t, -14)
    # ---- clock under the discharge stopwatch; heartbeat under "your heart drops" ----
    clock = norm(load(SFX / "clock.mp3"))
    t = stopwatch[0]
    while t < stopwatch[1]:
        place(mix, clock, t, -27, fade=0.2); t += len(clock) / SR
    for t0, t1 in browser_cues.get("heart", []):
        place(mix, norm(load(SFX / "heartbeat.mp3"))[: int((t1 - t0) * SR)], t0, -16, fade=0.3)

    mix = np.clip(mix, -1, 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", str(out_path)],
                   input=mix.astype(np.float32).tobytes(), check=True)
    return out_path
