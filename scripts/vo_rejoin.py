#!/usr/bin/env python3
"""Join ElevenLabs block takes into one narration without seams (PLAYBOOK §6.6).

  python3 scripts/vo_rejoin.py OUT.wav take1.mp3 take2.mp3 ... [--gaps 1.1 0.8 0.8 1.25] [--mp3 OUT.mp3]

What a plain concatenation got wrong (matsya-6000, found by an outside listen on 2026-11-10 and measured):
- the takes are generated with the next block's text as context, so a take can end with the first 50-70 ms of the
  next block's first word, cut off by the file end (heard as a clipped "You" or a hiccup before the next block);
- the gaps were exact digital zero, while pauses inside a take sit at about -70 dB: the joins "drop into a vacuum";
- a take can start at full level on its first sample (a click on the attack).
So: each take's tail is cut where such a late burst starts (a 10 ms fade), each take starts with a 5 ms fade-in, and
the gaps are filled with room tone taken from the takes' own typical pause, crossfaded in and out. No word is
touched. --gaps are seconds from the end of each take's file to the start of the next (0.8 was the old join, so
0.8 keeps every later word where it was). Writes a 44.1 kHz 16-bit mono WAV and, with --mp3, a 192 kbps MP3
loudness-normalised to -16 LUFS (true peak -1.5 dB), as the review copy.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 44100


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def db(a):
    return 20 * np.log10(max(1e-12, float(np.sqrt(np.mean(a * a)))))


def tail_cut(x, w_ms=5, quiet_db=-62.0, min_quiet_ms=120):
    """index where a late burst at the very end of a take starts, or len(x) when the take ends in a clean decay"""
    w = int(SR * w_ms / 1000)
    lv = [db(x[i:i + w]) for i in range(0, len(x) - w + 1, w)]
    # walk back over the loud end windows
    i = len(lv) - 1
    if lv[i] < quiet_db:
        return len(x), 0.0
    while i > 0 and lv[i] >= quiet_db:
        i -= 1
    burst_start = i + 1
    # it is a late burst only if quiet comes before it for a while (the last word had already decayed)
    q = 0
    while i > 0 and lv[i] < quiet_db:
        q += 1
        i -= 1
    if q * w_ms < min_quiet_ms:
        return len(x), 0.0
    return burst_start * w, (len(x) - burst_start * w) / SR


def room_tone(takes, n):
    """room tone with the spectrum and level of the takes' typical pause: noise shaped to the average spectrum of
    the pauses near the median level (a looped clip repeats, and one carried a tick; shaped noise does not)"""
    w = int(0.3 * SR)
    cands = []
    for x in takes:
        for i in range(int(2 * SR), len(x) - w - int(2 * SR), int(0.05 * SR)):
            seg = x[i:i + w]
            l = db(seg)
            if -85 < l < -60 and np.abs(seg).max() < 0.004:
                cands.append((l, seg))
    if not cands:
        sys.exit("no room tone found")
    med = float(np.median([c[0] for c in cands]))
    near = [seg for l, seg in cands if abs(l - med) < 2.0]
    nf = 4096
    spec = np.mean([np.abs(np.fft.rfft(seg[k:k + nf] * np.hanning(nf))) ** 2
                    for seg in near for k in range(0, w - nf, nf // 2)], axis=0)
    rng = np.random.default_rng(7)
    white = rng.standard_normal(n)
    W = np.fft.rfft(white)
    f_in = np.linspace(0, 1, len(spec))
    f_out = np.linspace(0, 1, len(W))
    W *= np.sqrt(np.interp(f_out, f_in, spec))
    tone = np.fft.irfft(W, n)
    tone *= 10 ** (med / 20) / np.sqrt(np.mean(tone ** 2))
    return tone, med


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("takes", type=Path, nargs="+")
    ap.add_argument("--gaps", type=float, nargs="*", default=None)
    ap.add_argument("--mp3", type=Path)
    a = ap.parse_args()
    takes = [load(p) for p in a.takes]
    gaps = a.gaps or [0.8] * (len(takes) - 1)
    if len(gaps) != len(takes) - 1:
        sys.exit("one gap per join")
    total = sum(len(x) for x in takes) + sum(int(round(g * SR)) for g in gaps)
    tone, tone_db = room_tone(takes, total)
    out = tone.copy()   # the bed under everything; speech replaces it where a take plays
    pos = 0
    fi, fo, xf = int(0.005 * SR), int(0.010 * SR), int(0.020 * SR)
    for k, x in enumerate(takes):
        x = x.copy()
        cut, burst = tail_cut(x) if k < len(takes) - 1 else (len(x), 0.0)
        if cut < len(x):
            x[cut - fo:cut] *= np.linspace(1, 0, fo)
            x[cut:] = 0.0
        if k > 0:
            x[:fi] *= np.linspace(0, 1, fi)
        # mix: inside the take the take plays; the bed fades out over 20 ms at its start and back in after its cut
        env = np.ones(len(x))
        env[:xf] = np.linspace(0, 1, xf) if k > 0 else 1.0
        env[cut:] = 0.0
        env[max(0, cut - xf):cut] = np.minimum(env[max(0, cut - xf):cut], np.linspace(1, 0, cut - max(0, cut - xf)))
        seg = slice(pos, pos + len(x))
        out[seg] = x * env + out[seg] * (1 - env) if k > 0 else np.where(np.arange(len(x)) < cut, x, out[seg])
        print(f"take {k + 1}: {a.takes[k].name} at {pos / SR:.3f} s, {len(x) / SR:.3f} s"
              + (f", late burst of {burst * 1000:.0f} ms cut at {cut / SR:.3f} s" if burst else ""))
        pos += len(x) + (int(round(gaps[k] * SR)) if k < len(gaps) else 0)
    print(f"room tone {tone_db:.1f} dB; total {total / SR:.3f} s")
    pcm = np.clip(out, -1, 1)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s16le", str(a.out)], input=pcm.tobytes(), check=True)
    if a.mp3:
        # two-pass linear loudnorm to -16 LUFS
        meas = subprocess.run(["ffmpeg", "-v", "info", "-i", str(a.out), "-af",
                               "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                              capture_output=True, text=True).stderr
        import json
        js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
        af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
              f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(a.out), "-af", af, "-ar", str(SR), "-c:a",
                        "libmp3lame", "-b:a", "192k", str(a.mp3)], check=True)


if __name__ == "__main__":
    main()
