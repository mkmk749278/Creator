"""Voice-over and an original music bed -- both free, both licence-clean.

Two deliberate choices:

  * **edge-tts** (Microsoft neural voices) rather than a paid API. It also
    returns per-word timings, which the caption layer needs.
  * **The music is SYNTHESISED here, not sourced.** A "royalty-free" track
    lifted from a library is the fastest way to get a commercial account muted
    or a video taken down, and Instagram's own audio library is not licensed for
    a business account in every region. A bed generated from oscillators is
    unambiguously ours.
"""
from __future__ import annotations

import asyncio
import os
import pathlib
import subprocess
import wave

import numpy as np

from . import brand
from .captions import Word

SR = 48_000

# The proxy in this environment MITMs TLS; edge-tts is aiohttp and needs both
# the bundle and an explicit proxy or it dies on certificate verification.
_CA = "/root/.ccr/ca-bundle.crt"


def _tts_kwargs() -> dict:
    kw: dict = {}
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        kw["proxy"] = proxy
    if os.path.exists(_CA):
        os.environ.setdefault("SSL_CERT_FILE", _CA)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", _CA)
    return kw


async def _speak(text: str, out: pathlib.Path, voice: str, rate: str, pitch: str):
    import edge_tts

    c = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch,
                             boundary="WordBoundary", **_tts_kwargs())
    audio, words = b"", []
    async for ch in c.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            words.append(Word(ch["text"], ch["offset"] / 1e7, ch["duration"] / 1e7))
    out.write_bytes(audio)
    return words


def speak(text: str, out: pathlib.Path, *, voice: str = brand.VOICE,
          rate: str = brand.VOICE_RATE, pitch: str = brand.VOICE_PITCH) -> list[Word]:
    """Render `text` to `out` (mp3) and return word timings."""
    out.parent.mkdir(parents=True, exist_ok=True)
    return asyncio.run(_speak(text, out, voice, rate, pitch))


def duration(path: pathlib.Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


# --- music ----------------------------------------------------------------
def _adsr(n: int, a: float, d: float, s: float, r: float) -> np.ndarray:
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    s_n = max(0, n - a_n - d_n - r_n)
    return np.concatenate([
        np.linspace(0, 1, a_n, endpoint=False) if a_n else np.array([]),
        np.linspace(1, s, d_n, endpoint=False) if d_n else np.array([]),
        np.full(s_n, s),
        np.linspace(s, 0, r_n) if r_n else np.array([]),
    ])[:n]


def _tone(freq: float, n: int, harmonics=(1.0, 0.5, 0.25, 0.12), detune=0.0) -> np.ndarray:
    t = np.arange(n) / SR
    out = np.zeros(n)
    for i, amp in enumerate(harmonics, 1):
        f = freq * i * (1 + detune)
        out += amp * np.sin(2 * np.pi * f * t)
    return out / max(1e-9, sum(harmonics))


def _lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    """One-pole lowpass -- enough to take the fizz off an additive saw."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def music_bed(seconds: float, *, bpm: float = 100.0, seed: int = 7,
              key: float = 220.0) -> np.ndarray:
    """An original, gentle A-minor bed: pad + sub + pluck arp + soft drums.

    Deliberately unobtrusive. A promo reel's bed exists to stop the voice
    sounding like it was recorded in a cupboard, not to be noticed.
    """
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    beat = 60.0 / bpm
    bar = beat * 4

    # i - VI - III - VII in A minor, as semitone offsets from the key root.
    prog = [(0, 3, 7), (-4, 0, 5), (3, 7, 10), (-2, 2, 7)]
    mix = np.zeros(n)

    n_bars = int(np.ceil(seconds / bar))
    for b in range(n_bars):
        chord = prog[b % len(prog)]
        start = int(b * bar * SR)
        length = min(int(bar * SR), n - start)
        if length <= 0:
            break

        # Pad: three detuned voices, filtered, slow attack.
        pad = np.zeros(length)
        for st in chord:
            f = key * 2 ** (st / 12)
            pad += _tone(f, length, (1.0, 0.35, 0.18, 0.08), detune=rng.uniform(-3e-3, 3e-3))
        pad = _lowpass(pad / 3, 1400) * _adsr(length, 0.5, 0.4, 0.75, 0.8) * 0.34
        mix[start:start + length] += pad

        # Sub bass on the root, one note per bar.
        f = key / 2 * 2 ** (chord[0] / 12)
        sub = np.sin(2 * np.pi * f * np.arange(length) / SR)
        mix[start:start + length] += sub * _adsr(length, 0.02, 0.25, 0.6, 0.5) * 0.30

        # Pluck arp on eighths.
        for i in range(8):
            s = start + int(i * beat / 2 * SR)
            ln = int(beat / 2 * SR)
            if s + ln > n:
                break
            st = chord[i % len(chord)] + (12 if i % 4 >= 2 else 0)
            f = key * 2 * 2 ** (st / 12)
            env = np.exp(-np.linspace(0, 7, ln))
            mix[s:s + ln] += _tone(f, ln, (1.0, 0.3, 0.1)) * env * 0.085

        # Kick on 1 and 3, hats on offbeats.
        for i in (0, 2):
            s = start + int(i * beat * SR)
            ln = min(int(0.16 * SR), n - s)
            if ln <= 0:
                continue
            t = np.arange(ln) / SR
            sweep = np.sin(2 * np.pi * (95 * np.exp(-t * 26) + 44) * t)
            mix[s:s + ln] += sweep * np.exp(-t * 17) * 0.42
        for i in range(8):
            s = start + int((i * beat / 2 + beat / 4) * SR)
            ln = min(int(0.05 * SR), n - s)
            if ln <= 0:
                continue
            t = np.arange(ln) / SR
            mix[s:s + ln] += rng.normal(0, 1, ln) * np.exp(-t * 150) * 0.035

    mix = np.tanh(mix * 1.15) * 0.82
    fade = int(min(1.5, seconds / 4) * SR)
    if fade > 0:
        mix[:fade] *= np.linspace(0, 1, fade)
        mix[-fade:] *= np.linspace(1, 0, fade)
    return mix


def write_wav(path: pathlib.Path, mono: np.ndarray, *, width: float = 0.12):
    """Write a lightly-widened stereo wav."""
    path.parent.mkdir(parents=True, exist_ok=True)
    d = int(width * SR / 100)
    left = mono
    right = np.concatenate([np.zeros(d), mono[:-d]]) if d else mono
    st = np.stack([left, right], axis=1)
    st = np.clip(st, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


def mix_track(vo: pathlib.Path | None, music: pathlib.Path, out: pathlib.Path,
              seconds: float, *, music_db: float = -19.0, duck: bool = True):
    """Mix VO over the bed, ducking the bed under the voice.

    Ducking is a real sidechain compressor rather than a fixed level: a static
    mix that sits right under a loud line disappears under a quiet one.
    """
    out.parent.mkdir(parents=True, exist_ok=True)

    # The track must be EXACTLY the video's length. amix with duration=first
    # ends the mix when the voice stops, which silently truncated an 8s bed to
    # the 3.7s of narration and left the tail of the video in dead silence.
    # apad then atrim pins the length from both directions regardless of which
    # input is longer. loudnorm also resamples to its own internal rate
    # (96kHz here) unless something downstream puts it back to 48k.
    tail = f"apad,atrim=0:{seconds},afade=t=out:st={max(0.0, seconds - 0.8):.3f}:d=0.8,"          f"loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000"

    if vo is None:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(music),
               "-af", f"volume={music_db + 8}dB,{tail}",
               "-c:a", "aac", "-b:a", "192k", str(out)]
    else:
        chain = (
            f"[1:a]aresample=48000,volume={music_db}dB[bed];"
            "[0:a]aresample=48000,volume=1.0[voice];"
        )
        if duck:
            chain += ("[voice]asplit=2[v1][vsc];"
                      "[bed][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=12:"
                      "release=340:makeup=1[bedduck];"
                      "[v1][bedduck]amix=inputs=2:duration=longest:"
                      "dropout_transition=0:normalize=0[mixed];")
        else:
            chain += ("[voice][bed]amix=inputs=2:duration=longest:"
                      "normalize=0[mixed];")
        chain += f"[mixed]{tail}[out]"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(vo), "-i", str(music),
               "-filter_complex", chain, "-map", "[out]",
               "-c:a", "aac", "-b:a", "192k", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg mix failed:\n{r.stderr[-2000:]}")
    return out
