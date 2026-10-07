"""Step 3: assemble the documentary from edl.csv + ./assets/ with FFmpeg.

Three layers on every shot (docs/documentary-production.md):
  1. full-screen base: video or photo, always moving (Ken Burns zoom 1.00->1.15 or a pan)
  2. atmosphere: film grain, edge vignette, optional HUD overlay (assets/hud_overlay.mp4), optional 2.35:1 bars
  3. kinetic accents: lower-third / corner timer / "ILLUSTRATION" tag over a dark gradient scrim

Audio: VO leads. The programme is NOT locked to the VO length: at each break row the VO stops and resumes
afterwards, exactly where it stopped (minus any `vo_skip`):
  LIVE      the original clip plays with its OWN audio (asset from src_in to src_out; length = src_out - src_in)
  VO_PAUSE  2-4 s of picture + ambience/SFX only
BGM sits ~-20 dB, side-chain ducked under all speech (VO + live clips); SFX come from the `sfx` column; final
loudness -14 LUFS / -1 dBTP. `src_in` on a SHOT row picks where in the source clip the shot starts.

A missing asset falls back to the EDL `fallback`, then to a moving placeholder labelled MISSING (preview only).

  python assemble.py                    # 1080p30 preview  -> out/preview.mp4 + out/contact_sheet.jpg
  python assemble.py --4k               # 3840x2160 master -> out/master_4k.mp4
  python assemble.py --letterbox --burn-subs
  python assemble.py --check            # list missing assets and exit
"""
import argparse
import csv
import math
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "out"
VO_FILE = "voiceover.mp3"
EDL = HERE / "edl.csv"
FPS = 30
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
BREAKS = {"LIVE", "VO_PAUSE"}  # rows that stop the VO
GRADE = {  # colour grade per block (teal investigation / saffron subject / clinical)
    "B1": "colorbalance=rs=-0.04:bs=0.06:rm=-0.02:bm=0.04,eq=contrast=1.06:saturation=0.9",
    "B2": "colorbalance=rs=-0.03:bs=0.05:rm=-0.02:bm=0.03,eq=contrast=1.05:saturation=0.92",
    "B3": "colorbalance=rs=-0.02:gs=0.02:bs=0.05,eq=contrast=1.07:saturation=0.9",
    "B4": "colorbalance=rs=0.03:gs=0.01:bs=-0.02:rm=0.02,eq=contrast=1.05:saturation=0.95",  # saffron: the science / yogic
    "B5": "colorbalance=rs=0.02:bs=0.02,eq=contrast=1.04:saturation=0.95",
    "PAUSE": "eq=contrast=1.08:saturation=0.85",
    "LIVE": "eq=contrast=1.04:saturation=0.95",  # archival: light touch only
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed:\n{' '.join(map(str, cmd))}\n{r.stderr[-3000:]}")
    return r


def font():
    for q in ("Inter:bold", "DejaVu Sans:bold"):
        r = subprocess.run(["fc-match", "-f", "%{file}", q], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
    sys.exit("no font found (install fonts-dejavu)")


def load_edl(path=None, keep_optional=False):
    rows = list(csv.DictReader(pathlib.Path(path or EDL).open(encoding="utf-8")))
    # an optional LIVE clip that is not downloaded yet is left out (no dead air); rebuild SRTs after downloading
    if not keep_optional:
        rows = [r for r in rows if not (r.get("optional") == "yes" and resolve(r)[0] is None)]
    t = 0.0
    for r in rows:
        src_in, src_out = num(r.get("src_in")), num(r.get("src_out"))
        r["src_in"] = src_in or 0.0
        r["dur"] = src_out - r["src_in"] if src_out else float(r["dur"])
        r["start"] = t  # programme time
        t += r["dur"]
    return rows, t


def num(v):
    return float(v) if v not in (None, "") else None


def aspect(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    w, h = map(int, r.stdout.strip().split(",")[:2])
    return w / h


def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def resolve(r):
    for name in (r["asset"], r["fallback"]):
        if name and (ASSETS / name).exists():
            return ASSETS / name, name != r["asset"]
    return None, True


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def motion(kind, W, H, n):
    """zoompan expression for frame `on` in [0, n): zoom 1.00->1.15 or a pan at 1.12 zoom."""
    p = f"(on/{max(n - 1, 1)})"
    ease = f"(0.5-0.5*cos(PI*{p}))"
    if kind == "push":  # barely-there drift for live archival clips
        z, x, y = f"1+0.04*{ease}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif kind == "zoom_in":
        z, x, y = f"1+0.15*{ease}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif kind == "zoom_out":
        z, x, y = f"1.15-0.15*{ease}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif kind == "pan_rl":
        z, x, y = "1.12", f"(iw-iw/zoom)*(1-{ease})", "ih/2-(ih/zoom/2)"
    else:  # pan_lr
        z, x, y = "1.12", f"(iw-iw/zoom)*{ease}", "ih/2-(ih/zoom/2)"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS}"


def render_shot(i, r, W, H, args, fontfile, tmp):
    n = max(1, round(r["dur"] * FPS))
    src, fell_back = resolve(r)
    u = H / 1080  # UI scale
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    # Layer 1: full-screen base, always moving
    if src is None:
        cmd += ["-f", "lavfi", "-i", f"gradients=s={W}x{H}:c0=0x0b1f2a:c1=0x1d3b4a:c2=0x3a1420:speed=0.02:r={FPS}"]
        base = (f"drawtext=fontfile='{fontfile}':text='MISSING  {esc(r['asset'])}':fontcolor=white@0.5:"
                f"fontsize={int(34 * u)}:x=(w-tw)/2:y=(h-th)/2")
    else:
        is_img = src.suffix.lower() in IMG_EXT
        cmd += ["-loop", "1", "-framerate", str(FPS)] if is_img else ["-ss", str(r["src_in"]), "-stream_loop", "-1"]
        cmd += ["-i", str(src)]
        if r["motion"] == "none" and not is_img:  # play the real footage untouched (cover-fit only)
            base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}"
        elif is_img and aspect(src) < 1.3:  # tall/square still: fit it over a blurred, darkened copy of itself
            base = (f"split[bgi][fgi];[bgi]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                    f"boxblur=40:2,eq=brightness=-0.18:saturation=0.7[bgo];[fgi]scale=-2:{int(H * 2 * 0.92)}:flags=lanczos[fgo];"
                    f"[bgo][fgo]overlay=(W-w)/2:(H-h)/2,setsar=1,{motion(r['motion'], W, H, n)}")
        else:
            base = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase:flags=lanczos,crop={W * 2}:{H * 2},"
                    f"setsar=1,{motion(r['motion'], W, H, n)}")
    graph = [f"[0:v]{base},{GRADE.get(r['block'], GRADE['B1'])},format=yuv420p[l1]"]
    cur, k = "[l1]", 1
    # Layer 2: atmosphere (HUD at low opacity, vignette, grain, optional 2.35:1 bars)
    hud = ASSETS / "hud_overlay.mp4"
    if "hud" in r["overlay"] and hud.exists():
        cmd += ["-stream_loop", "-1", "-i", str(hud)]
        graph.append(f"[{k}:v]scale={W}:{H},format=rgba,colorchannelmixer=aa=0.22[hud]")
        graph.append(f"{cur}[hud]overlay=shortest=1[l1h]")
        cur, k = "[l1h]", k + 1
    atmos = ["vignette=angle=PI/4.5", "noise=alls=4:allf=t"]
    if "cctv" in r["overlay"]:
        u2 = H / 1080
        atmos = ["hue=s=0", "colorchannelmixer=rr=0.55:gg=0.95:bb=0.6", "noise=alls=14:allf=t",
                 f"drawgrid=w=iw:h={max(2, int(3 * u2))}:t=1:c=black@0.25", "vignette=angle=PI/3.5",
                 f"drawtext=fontfile='{fontfile}':text='● REC':fontcolor=red:fontsize={int(34 * u2)}:x={int(60 * u2)}:y={int(50 * u2)}"
                 f":alpha='if(lt(mod(t,1),0.6),1,0)'",
                 f"drawtext=fontfile='{fontfile}':text='CAM 0{1 + int(r['start']) % 2}   %{{pts\\:hms}}':fontcolor=white@0.85:"
                 f"fontsize={int(30 * u2)}:x=w-tw-{int(60 * u2)}:y={int(50 * u2)}"]
    if args.letterbox:
        bar = int((H - W / 2.35) / 2)
        atmos.append(f"drawbox=y=0:w=iw:h={bar}:color=black:t=fill,drawbox=y=ih-{bar}:w=iw:h={bar}:color=black:t=fill")
    graph.append(f"{cur}{','.join(atmos)}[l2]")
    cur = "[l2]"
    # Layer 3: kinetic accents (fade/slide in over 0.35 s)
    text, pos = r["text"].strip(), r["text_pos"].strip()
    if text:
        alpha, pad = "alpha='min(1,t/0.35)'", int(64 * u)
        draws = []
        if pos == "timer":
            draws.append(f"drawbox=x=iw-{int(470 * u)}:y={int(50 * u)}:w={int(420 * u)}:h={int(78 * u)}:color=black@0.45:t=fill")
            draws.append(f"drawtext=fontfile='{fontfile}':text='{esc(text)}':fontcolor=0xFFB020:fontsize={int(40 * u)}:"
                         f"x=w-{int(450 * u)}:y={int(70 * u)}:{alpha}")
        elif pos == "tag":
            draws.append(f"drawtext=fontfile='{fontfile}':text='{esc(text)}':fontcolor=white@0.85:fontsize={int(27 * u)}:"
                         f"box=1:boxcolor=black@0.45:boxborderw={int(10 * u)}:x={pad}:y={int(56 * u)}")
        else:  # lower-third over a dark gradient scrim: amber rule + text sliding up
            cmd += ["-i", str(tmp / "scrim.png")]
            graph.append(f"{cur}[{k}:v]overlay=0:0[l2s]")
            cur, k = "[l2s]", k + 1
            y = f"h-{int(190 * u)}+{int(20 * u)}*(1-min(1,t/0.35))"
            draws.append(f"drawbox=x={pad}:y=ih-{int(206 * u)}:w={int(90 * u)}:h={max(2, int(5 * u))}:color=0xFFB020:t=fill")
            draws.append(f"drawtext=fontfile='{fontfile}':text='{esc(text)}':fontcolor=white:fontsize={int(52 * u)}:"
                         f"x={pad}:y='{y}':{alpha}:shadowcolor=black@0.6:shadowx=0:shadowy={int(3 * u)}")
        graph.append(f"{cur}{','.join(draws)}[l3]")
        cur = "[l3]"
    out = tmp / f"{i:03d}.mp4"
    cmd += ["-filter_complex", ";".join(graph), "-map", cur, "-frames:v", str(n), "-r", str(FPS),
            "-c:v", "libx264", "-preset", args.preset, "-crf", "18" if args.uhd else "20",
            "-maxrate", "45M" if args.uhd else "12M", "-bufsize", "90M" if args.uhd else "24M",
            "-pix_fmt", "yuv420p", "-an", str(out)]
    run(cmd)
    return out, src is None or fell_back


def make_scrim(W, H, tmp):
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=black:s={W}x{H}", "-vf",
         f"format=rgba,geq=r=0:g=0:b=0:a='if(gt(Y,H*0.62),200*pow((Y-H*0.62)/(H*0.38),1.4),0)'",
         "-frames:v", "1", str(tmp / "scrim.png")])


def build_audio(rows, total, tmp):
    vo = ASSETS / VO_FILE
    if not vo.exists():
        sys.exit(f"missing {vo} (copy the combined voiceover there)")
    inputs = ["-i", str(vo)]
    bgm = ASSETS / "bgm_dark.mp3"
    if bgm.exists():
        inputs += ["-stream_loop", "-1", "-i", str(bgm)]
    fmt = "aresample=48000,aformat=channel_layouts=stereo"
    # 1. VO with a gap at every break row (VO resumes where it stopped, minus vo_skip)
    graph, pieces, cur = [], [], 0.0
    for k, r in enumerate(r for r in rows if r["type"] in BREAKS):
        at, skip = float(r["vo_at"]), float(r["vo_skip"] or 0)
        graph.append(f"[0:a]atrim={cur}:{at},asetpts=N/SR/TB[p{k}]")
        graph.append(f"anullsrc=r=44100:cl=mono,atrim=0:{r['dur']}[s{k}]")
        pieces += [f"[p{k}]", f"[s{k}]"]
        cur = at + skip
    graph.append(f"[0:a]atrim=start={cur},asetpts=N/SR/TB[pend]")
    pieces.append("[pend]")
    graph.append(f"{''.join(pieces)}concat=n={len(pieces)}:v=0:a=1,{fmt}[vo]")
    speech, fx = ["[vo]"], []
    # 2. LIVE rows: the original clip's own audio, levelled to sit with the VO
    for r in rows:
        if r["type"] != "LIVE":
            continue
        src, _ = resolve(r)
        if src is None or src.suffix.lower() in IMG_EXT or not has_audio(src):
            print(f"  warning: {r['id']} LIVE clip {r['asset']} has no audio; leaving silence")
            continue
        idx = inputs.count("-i")
        inputs += ["-i", str(src)]
        d = r["dur"]
        graph.append(f"[{idx}:a]atrim={r['src_in']}:{r['src_in'] + d},asetpts=N/SR/TB,loudnorm=I=-18:TP=-2,"
                     f"afade=t=in:d=0.15,afade=t=out:st={max(0.0, d - 0.25)}:d=0.25,{fmt},"
                     f"adelay={int(r['start'] * 1000)}:all=1[l{idx}]")
        speech.append(f"[l{idx}]")
    graph.append(f"{''.join(speech)}amix=inputs={len(speech)}:normalize=0:duration=longest,asplit=2[sp][spsc]")
    layers = ["[sp]"]
    # 3. BGM at -20 dB, side-chain ducked under all speech (comes up in VO_PAUSE breaks)
    if bgm.exists():
        graph.append(f"[1:a]atrim=0:{total},volume=-20dB,{fmt}[bg]")
        graph.append("[bg][spsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[bgd]")
        layers.append("[bgd]")
    else:
        graph.append("[spsc]anullsink")
    # 4. SFX / ambience at programme time
    for r in rows:
        for item in filter(None, (r["sfx"] or "").split(";")):
            name, _, rel = item.partition("@")
            f = ASSETS / name.split(" (")[0].strip()
            if not f.exists():
                continue
            idx = inputs.count("-i")
            inputs += ["-i", str(f)]
            at = r["start"] + (float(rel) if rel else 0)
            pause = r["type"] == "VO_PAUSE"
            dur = r["dur"] if pause else 3.0
            graph.append(f"[{idx}:a]atrim=0:{dur},afade=t=out:st={max(0.0, dur - 0.3)}:d=0.3,"
                         f"volume={'0dB' if pause else '-8dB'},{fmt},adelay={int(at * 1000)}:all=1[x{idx}]")
            fx.append(f"[x{idx}]")
    layers += fx
    graph.append(f"{''.join(layers)}amix=inputs={len(layers)}:normalize=0:duration=longest,"
                 f"apad,atrim=0:{total},loudnorm=I=-14:TP=-1:LRA=11[a]")
    out = tmp / "mix.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(graph),
         "-map", "[a]", "-ar", "48000", str(out)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--4k", dest="uhd", action="store_true")
    ap.add_argument("--letterbox", action="store_true")
    ap.add_argument("--burn-subs", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", help="render shots a-b (1-based, preview a section)")
    ap.add_argument("--preset", default="veryfast")
    ap.add_argument("--edl", default=str(EDL))
    args = ap.parse_args()
    rows, total = load_edl(args.edl)
    missing = sorted({r["asset"] for r in rows if resolve(r)[0] is None or resolve(r)[1]})
    live = sum(r["dur"] for r in rows if r["type"] in BREAKS)
    print(f"{len(rows)} rows, {total:.1f} s programme ({live:.1f} s of it VO breaks / live clips); "
          f"{len(missing)} assets missing or on fallback")
    for m in missing:
        print("  missing:", m)
    if args.check:
        return
    W, H = (3840, 2160) if args.uhd else (1920, 1080)
    OUT.mkdir(exist_ok=True)
    tmp = OUT / ("tmp_4k" if args.uhd else "tmp")
    tmp.mkdir(exist_ok=True)
    make_scrim(W, H, tmp)
    fontfile = font()
    lo, hi = (1, len(rows))
    if args.only:
        lo, hi = map(int, args.only.split("-"))
    clips = []
    for i, r in enumerate(rows, 1):
        if lo <= i <= hi:
            clip, _ = render_shot(i, r, W, H, args, fontfile, tmp)
            clips.append(clip)
            print(f"  [{i}/{len(rows)}] {r['id']} {r['asset']} {r['dur']:.2f}s", flush=True)
    (tmp / "list.txt").write_text("".join(f"file '{c.name}'\n" for c in clips))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
         "-c", "copy", str(tmp / "video.mp4")])
    name = "master_4k.mp4" if args.uhd else "preview.mp4"
    vcodec = ["-c:v", "copy"]
    if args.burn_subs:
        vcodec = ["-vf", f"subtitles={HERE / 'subtitles.te.programme.srt'}:force_style='FontName=Noto Sans Telugu,"
                  f"FontSize=20,Outline=1,MarginV=60'", "-c:v", "libx264", "-crf", "18", "-preset", args.preset,
                  "-maxrate", "45M" if args.uhd else "12M", "-bufsize", "90M" if args.uhd else "24M"]
    if args.only:
        shutil.copy(tmp / "video.mp4", OUT / f"section_{lo}-{hi}.mp4")
        print("wrote", OUT / f"section_{lo}-{hi}.mp4")
        return
    audio = build_audio(rows, total, tmp)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "video.mp4"), "-i", str(audio), *vcodec,
         "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", str(OUT / name)])
    # contact sheet: one frame from the middle of every shot
    sel = "+".join(f"eq(n\\,{round((r['start'] + r['dur'] / 2) * FPS)})" for r in rows)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / name), "-vf",
         f"select='{sel}',scale=384:-2,tile=8x{math.ceil(len(rows) / 8)}:padding=4", "-frames:v", "1",
         "-vsync", "vfr", str(OUT / "contact_sheet.jpg")])
    print("wrote", OUT / name, "and", OUT / "contact_sheet.jpg")


if __name__ == "__main__":
    main()
