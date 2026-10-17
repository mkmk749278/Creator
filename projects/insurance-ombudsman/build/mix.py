#!/usr/bin/env python3
"""Soundtrack for The Insurance Ombudsman (charter sound matrix, CLAUDE.md "Audio"), mixed in numpy at 48 kHz stereo:
  - the two Akash takes at their film times (VO leads);
  - a synthesised bed (scripts/make_bed.py: no samples, no licences) at -25 dB under speech, lifting to -13 dB in
    pauses with 0.5 s ramps; silent for 1.5 s before each core reveal, then a low impact (-7 dB);
  - pink room tone at about -44 dBFS so no frame is digitally silent;
  - master to -14 LUFS with two-pass linear loudnorm, then muxed with the picture.
Usage: .venv/bin/python build/mix.py [--height 1080]
"""
import argparse, csv, json, subprocess, sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assemble import P, ROOT, A, VO, END, SN, at   # noqa: E402

SR = 48000
REVEALS = [at(20), at(60), at(124)]      # "Stop right there" (third door), the 1,715, the Bombay High Court


def movavg(x, k):
    """Centred moving average via cumulative sums (np.convolve with a long kernel is far too slow on 27 M samples)."""
    c = np.cumsum(np.concatenate([np.zeros(1), x]))
    y = (c[k:] - c[:-k]) / k
    pad = len(x) - len(y)
    return np.concatenate([np.full(pad // 2, y[0]), y, np.full(pad - pad // 2, y[-1])])


def db(x):
    return 10 ** (x / 20)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--height", type=int, default=1080); a = ap.parse_args()
    out = A / "audio"; out.mkdir(exist_ok=True)
    N = int(END * SR)
    cues = {"duration": END, "impacts": [r + 1.5 for r in REVEALS],
            "sections": [{"start": 0, "mood": "tense"}, {"start": 345, "mood": "calm"}, {"start": 527, "mood": "calm"}]}
    cj = out / "cues.json"
    if not cj.exists() or cj.read_text() != json.dumps(cues):
        cj.write_text(json.dumps(cues))
    bed_wav = out / "bed.wav"
    if not bed_wav.exists() or bed_wav.stat().st_mtime < (out / "cues.json").stat().st_mtime - 1:
        subprocess.run([ROOT / ".venv/bin/python", ROOT / "scripts/make_bed.py", out / "cues.json", bed_wav], check=True)
    vo = np.zeros((N, 2), np.float32)
    for path, t in VO:
        c = load(path); i = int(t * SR); vo[i:i + len(c)] += c[:N - i]
    # bed gain curve: -25 dB in speech, -13 dB in pauses longer than 0.6 s, 0.5 s ramps; 1.5 s silence before reveals
    g = np.full(N, -13.0)
    for s in SN:
        g[int((s["start"] - 0.25) * SR):int((s["end"] + 0.25) * SR)] = -25.0
    for r in REVEALS:
        g[int(r * SR):int((r + 1.5) * SR)] = -90.0
    gl = db(movavg(g, int(0.5 * SR)))[:, None].astype(np.float32)
    bed = load(bed_wav)
    bed = np.vstack([bed, np.zeros((max(0, N - len(bed)), 2), np.float32)])[:N]
    rms = np.sqrt(np.mean(bed ** 2)) + 1e-9
    bed = bed * (db(-20) / rms)                      # normalise the bed to -20 dBFS RMS so the gains mean the same
    rng = np.random.default_rng(2)                   # pink-ish room tone
    w = rng.standard_normal((N, 2)).astype(np.float32)
    room = np.stack([movavg(w[:, c], 48) for c in (0, 1)], axis=1).astype(np.float32)   # gentle low-pass: soft hiss
    room = room / (np.sqrt(np.mean(room ** 2)) + 1e-9) * db(-44)
    vpk = np.max(np.abs(vo)) + 1e-9
    mix = vo * (db(-2.5) / vpk) + bed * gl + room
    raw = out / "mix_raw.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", raw],
                   input=mix.astype(np.float32).tobytes(), check=True)
    # two-pass linear loudnorm to -14 LUFS
    st = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = json.loads(st[st.rindex("{"):st.rindex("}") + 1])
    master = out / "master.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
                    f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
                    f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", str(SR), master], check=True)
    pic = A / f"picture_{a.height}.mp4"
    final = P / "assets" / f"insurance-ombudsman-preview-{a.height}p.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", master, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    print("final:", final)


if __name__ == "__main__":
    main()
