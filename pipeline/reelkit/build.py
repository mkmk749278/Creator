"""Assemble a reel: script -> voice -> timed scenes -> frames -> MP4.

Scene timing is driven by the VOICE, not by a stopwatch. A scene may declare
`"until": "some phrase"`, and the cut lands on the frame where that phrase is
actually spoken -- taken from edge-tts word boundaries. Authoring durations by
hand drifts the moment a line is reworded, and the drift is invisible until you
watch the whole thing back.

Frames are piped to ffmpeg as raw RGB rather than written out as PNGs: a 30s
reel is 900 frames at 1080x1920, and the disk round trip costs more than the
rendering does.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time

from PIL import Image

from . import audio, brand, captions, scenes


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def phrase_time(words: list[captions.Word], phrase: str) -> float | None:
    """Start time of `phrase` in the narration, or None if it is not spoken."""
    target = _norm(phrase).split()
    if not target:
        return None
    norm = [_norm(w.text) for w in words]
    for i in range(len(norm) - len(target) + 1):
        if norm[i:i + len(target)] == target:
            return words[i].start
    return None


def resolve_timings(specs: list[dict], words: list[captions.Word],
                    total: float) -> list[tuple[float, float]]:
    """Return (start, dur) per scene.

    A scene's start is the moment its `until` phrase is spoken; scenes without
    one are spread evenly across the gap to the next anchored scene, so a script
    can anchor only the cuts that matter.
    """
    n = len(specs)
    anchors: list[float | None] = [None] * n
    anchors[0] = 0.0
    for i, spec in enumerate(specs):
        if i == 0:
            continue
        if spec.get("until"):
            t = phrase_time(words, spec["until"])
            if t is None:
                print(f"  ! scene {i}: phrase {spec['until']!r} is not in the "
                      f"narration; falling back to even spacing")
            else:
                anchors[i] = max(0.0, t - spec.get("lead", 0.18))

    # Fill unanchored scenes evenly between their neighbours.
    known = [i for i, a in enumerate(anchors) if a is not None]
    for a, b in zip(known, known[1:]):
        gap = anchors[b] - anchors[a]
        for k in range(a + 1, b):
            anchors[k] = anchors[a] + gap * (k - a) / (b - a)
    last = known[-1]
    if last < n - 1:
        gap = total - anchors[last]
        for k in range(last + 1, n):
            anchors[k] = anchors[last] + gap * (k - last) / (n - last)

    starts = [float(a) for a in anchors]
    for i in range(1, n):                       # keep strictly increasing
        starts[i] = max(starts[i], starts[i - 1] + 0.5)
    return [(starts[i], (starts[i + 1] if i + 1 < n else total) - starts[i])
            for i in range(n)]


def _srt(chunks: list[captions.Chunk], path: pathlib.Path):
    def ts(s: float) -> str:
        h, r = divmod(s, 3600)
        m, sec = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(sec):02d},{int((sec % 1) * 1000):03d}"

    out = []
    for i, c in enumerate(chunks, 1):
        out.append(f"{i}\n{ts(c.start)} --> {ts(c.end + 0.25)}\n"
                   f"{' '.join(w.text for w in c.words)}\n")
    path.write_text("\n".join(out), encoding="utf-8")


def build(script_path: pathlib.Path, out_dir: pathlib.Path | None = None) -> pathlib.Path:
    script = json.loads(script_path.read_text(encoding="utf-8"))
    out_dir = out_dir or script_path.parent / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "work"
    work.mkdir(exist_ok=True)

    name = script.get("id", script_path.parent.name)
    print(f"\n=== {name} ===")

    # 1. Voice -------------------------------------------------------------
    narration = script.get("voice", "").strip()
    words: list[captions.Word] = []
    vo_path = None
    if narration:
        vo_path = work / "vo.mp3"
        print("  voice: edge-tts")
        words = audio.speak(narration, vo_path,
                            voice=script.get("voice_name", brand.VOICE),
                            rate=script.get("voice_rate", brand.VOICE_RATE))
        # WordBoundary events carry no punctuation; read it back off the script
        # so captions can break where the sentences do.
        captions.mark_punctuation(words, narration)
        vo_len = audio.duration(vo_path)
        print(f"  narration {vo_len:.2f}s, {len(words)} words")
    else:
        vo_len = 0.0

    tail = script.get("tail", 1.6)
    total = round(max(vo_len + tail, script.get("min_duration", 0.0)), 3)

    # 2. Timings -----------------------------------------------------------
    specs = script["scenes"]
    timings = resolve_timings(specs, words, total)
    # A scene shorter than about a second reads as a flash, not a cut. It is
    # always a scripting problem -- two anchors sitting on adjacent phrases --
    # so say so loudly rather than silently shipping a strobe.
    MIN_SCENE = 1.2
    for spec, (s, d) in zip(specs, timings):
        flag = "  <-- TOO SHORT" if d < MIN_SCENE else ""
        print(f"  {spec['type']:<10} {s:6.2f}s +{d:5.2f}s  "
              f"{spec.get('until','(start)')}{flag}")
    short = [(i, d) for i, (_, d) in enumerate(timings) if d < MIN_SCENE]
    if short:
        print(f"  ! {len(short)} scene(s) under {MIN_SCENE}s -- move the `until` "
              f"anchor later or merge the scenes")

    chunks = captions.group(words) if words else []
    if chunks:
        _srt(chunks, out_dir / f"{name}.srt")

    # 3. Audio -------------------------------------------------------------
    bed = work / "bed.wav"
    audio.write_wav(bed, audio.music_bed(total + 1.0,
                                         bpm=script.get("bpm", 100),
                                         seed=script.get("music_seed", 7)))
    track = work / "track.m4a"
    audio.mix_track(vo_path, bed, track, total,
                    music_db=script.get("music_db", -19.0))

    # 4. Frames -> ffmpeg --------------------------------------------------
    mp4 = out_dir / f"{name}.mp4"
    n_frames = int(round(total * brand.FPS))
    xfade = script.get("xfade", 0.28)
    cap_cfg = script.get("captions", {})
    show_caps = cap_cfg.get("enabled", True)

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pixel_format", "rgb24",
        "-video_size", f"{brand.W}x{brand.H}", "-framerate", str(brand.FPS),
        "-i", "pipe:0",
        "-i", str(track),
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.1",
        "-r", str(brand.FPS), "-g", str(brand.FPS * 2),
        "-c:a", "copy", "-shortest", "-movflags", "+faststart",
        str(mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    t0 = time.time()
    poster_at = script.get("poster_at", 0.9)
    try:
        for i in range(n_frames):
            t = i / brand.FPS
            idx = max(0, min(len(specs) - 1,
                             next((k for k, (s, d) in enumerate(timings)
                                   if s <= t < s + d), len(specs) - 1)))
            s, d = timings[idx]
            frame = scenes.render(specs[idx], t - s, d)

            # Cross-dissolve into the next scene.
            if idx + 1 < len(specs) and (s + d - t) < xfade:
                ns, nd = timings[idx + 1]
                nxt = scenes.render(specs[idx + 1], max(0.0, t - ns), nd)
                a = min(1.0, max(0.0, (t - (s + d - xfade)) / xfade))
                frame = Image.blend(frame, nxt, a)

            if show_caps and chunks:
                layer = captions.render(
                    t, chunks,
                    baseline=cap_cfg.get("baseline", 1330),
                    font_size=cap_cfg.get("size", 74))
                if layer is not None:
                    frame = frame.convert("RGBA")
                    frame.alpha_composite(layer)
                    frame = frame.convert("RGB")

            if abs(t - poster_at) < 1.0 / brand.FPS / 2:
                frame.save(out_dir / f"{name}_poster.jpg", quality=92)

            proc.stdin.write(frame.tobytes())
            if i % 90 == 0:
                print(f"    frame {i}/{n_frames}  ({time.time()-t0:.0f}s)")
        proc.stdin.close()
    except BrokenPipeError:
        pass

    err = proc.stderr.read().decode()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed:\n{err[-2500:]}")

    size = mp4.stat().st_size
    print(f"  -> {mp4}  {size/1e6:.1f} MB  {total:.2f}s  "
          f"(rendered in {time.time()-t0:.0f}s)")
    return mp4
