#!/usr/bin/env python3
"""Assemble The Jet Engine Paradox from the program timeline (align/program.json), the animated scenes (scenes.json,
renders in assets/scenes/<session>/<id>.mp4) and the coordinator's shots (SHOTS below).

  python3 projects/jet-engine-paradox/tools/assemble.py [--height 720|1080|2160] [--check]

Picture: every VO line has a shot; animated scenes cover their own windows; everything else is real footage, stills
with motion (Ken Burns), PIB proofs under a push-in, or, while an asset is still missing, a clearly marked PENDING
plate (so the cut can be reviewed for timing before every asset exists; `--check` lists what is pending).
Shots render one by one to assets/shots<H>/ (cached by a spec hash) and are joined with concat -c copy.
Final pass: citation tag + ILLUSTRATION tag (bottom right) and the on-screen line (lower left) for non-scene lines,
logo bug (top right), logo sting on the channel name, end card; VO with its picture-only breaks, music bed ducked under
speech (silent 1.5 s before the two reveals), two-pass loudness to -14 LUFS.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
A = P / "assets"
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_M = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
RENDER_V = 1
PROG = json.loads((P / "align/program.json").read_text())
SCENES = json.loads((P / "scenes.json").read_text())
LINES = {l["id"]: l for l in PROG["lines"]}
END = PROG["total"]
BR, CM, PF, YT = A / "broll", A / "commons", A / "proof", A / "yt"


def L(i):
    return LINES[i]["start"]


def S(t, kind, **kw):
    return dict(t=round(t - 0.15, 2), kind=kind, **kw)   # cut 0.15 s before the line speaks (cut on the breath)


# ---- coordinator shots for lines no animated scene covers (visual column of script.full.tsv) ----
# kind: clip(src, ss) | still(src, zoom, focus) | proof(src) | pending(desc) | scene(id, frm=program time to start from)
#       | dissolve(a, b, xd, zoom, focus): push into scene a's last frame, then cross-dissolve into scene b's held first frame
F404 = CM / "General_Electric_F404_05_ge-f404-engine-jpg.jpg"
F404B = CM / "General_Electric_F404_01_f404-turbojet-engine-on-uss-abraham-linc.jpg"
IL76 = CM / "Il-76_with_a_Kaveri_engine.jpg"
KAV = A / "commons2" / "GTX-35VS_Kaveri.jpg"
AMCA = CM / "AMCA_model_Aero_India_07_amca-model-displayed-during-aero-india-2.jpg"
SHOTS = [
    S(0.15, "clip", src=YT / "DLA_64yz8Ss.mp4", ss=28, credit="ISRO · MISSION CONTROL · 23 AUG 2023"),
    S(3.2, "clip", src=YT / "DLA_64yz8Ss.mp4", ss=486, crop=(0.0, 0.08, 1.0, 1.0), credit="ISRO · LIVE DESCENT SIMULATION", illus=True),
    S(L("J002"), "clip", src=YT / "DLA_64yz8Ss.mp4", ss=763, credit="ISRO · TOUCHDOWN · 23 AUG 2023"),
    S(L("J003"), "still", src=A / "commons2" / "INS_Arihant_at_sea_(cropped).jpg", zoom=(1.0, 1.15), focus=(0.4, 0.5), dark=True, illus=False, credit="PMO · INS ARIHANT · 2018"),
    S(L("J003") + 2.6, "clip", src=YT / "_io4f2I5-sY.mp4", ss=19, credit="ISRO · MOM SIMULATION", illus=True),
    S(L("J005"), "clip", src=YT / "YfQNVWn8aIc.mp4", ss=135.5, crop=(0.08, 0.0, 0.92, 0.74), credit="DD INDIA · HAL NASHIK 2025"),
    S(L("J006"), "clip", src=YT / "YfQNVWn8aIc.mp4", ss=43, crop=(0.08, 0.0, 0.92, 0.74), credit="DD INDIA · TEJAS MK1A"),
    S(L("J010"), "clip", src=YT / "zCYBJtBaUXw.mp4", ss=9, credit="INDIAN AIR FORCE"),
    S(L("J012"), "clip", src=YT / "52f1mQqaii8.mp4", ss=21, credit="INDIAN AIR FORCE · MIG-21 FINAL FLIGHT"),
    S(L("J014"), "still", src=F404, zoom=(1.05, 1.25), focus=(0.5, 0.5), illus=False),
    S(L("J014") + 4.0, "still", src=F404B, zoom=(1.1, 1.3), focus=(0.5, 0.55), illus=False),
    S(L("J016"), "proof", src=PF / "bloomberg_supply.png", label="BLOOMBERG · 29 OCT 2024"),
    S(L("J016") + 2.6, "proof", src=PF / "bloomberg_penalty.png", label="BLOOMBERG · 29 OCT 2024"),
    S(L("J018"), "clip", src=YT / "YfQNVWn8aIc.mp4", ss=146, crop=(0.08, 0.0, 0.92, 0.74), credit="DD INDIA · TEJAS MK1A FLIGHT"),
    S(L("J019"), "still", src=F404, zoom=(1.35, 1.7), focus=(0.55, 0.5), dark=True, illus=False),
    S(L("J020") - 1.5, "black"),
    S(L("J020"), "proof", src=PF / "goi_1998_pokhran.png", label="GOVT OF INDIA · PAPER LAID IN PARLIAMENT · MAY 1998"),
    S(L("J022"), "proof", src=PF / "crs_sanctions.png", label="US CONGRESSIONAL RESEARCH SERVICE · 2002"),
    S(L("J024"), "clip", src=YT / "ryolgbuDNSg.mp4", ss=25, crop=(0.06, 0.12, 1.0, 1.0), credit="PIB · TEJAS · AERO INDIA 2019"),
    S(L("J025"), "clip", src=YT / "52f1mQqaii8.mp4", ss=8.6, credit="INDIAN AIR FORCE"),
    S(L("J028"), "dissolve", a="D7_engine_club", b="C4_kaveri_blueprint", xd=2.4, zoom=(1.0, 1.9), focus=(0.575, 0.72), illus=True),  # globe tail → C4's first frame; J029 runs C4 on
    S(L("J030"), "still", src=KAV, zoom=(1.0, 1.12), focus=(0.5, 0.5), illus=False, credit="KAVERI ENGINE · J. PILLARISETI · CC BY 3.0"),
    S(L("J030") + 2.8, "still", src=KAV, zoom=(1.5, 1.7), focus=(0.22, 0.52), illus=False, credit="KAVERI ENGINE · J. PILLARISETI · CC BY 3.0"),
    S(L("J030") + 5.6, "still", src=KAV, zoom=(1.6, 1.4), focus=(0.62, 0.42), illus=False, credit="KAVERI ENGINE · J. PILLARISETI · CC BY 3.0"),
    S(L("J031"), "proof", src=PF / "pib_2012.png", label="PIB · DEFENCE MINISTRY · 2012"),
    S(L("J035"), "still", src=KAV, zoom=(1.7, 1.45), focus=(0.6, 0.55), dark=True, illus=False, credit="KAVERI PROTOTYPE · J. PILLARISETI · CC BY 3.0"),  # upgrade: GTRE test-cell footage (Feb 2026 afterburner run) if a telecast turns up
    S(L("J042"), "still", src=IL76, zoom=(1.0, 1.18), focus=(0.5, 0.5), illus=False),
    S(L("J043"), "proof", src=PF / "pib_2012_ftb.png"),
    S(L("J046"), "clip", src=YT / "q2ueCg9bvvQ.mp4", ss=636, credit="ISRO · LVM3-M4 LIFT-OFF 2023"),
    S(L("J047"), "clip", src=YT / "q2ueCg9bvvQ.mp4", ss=663, credit="ISRO · LVM3-M4"),
    S(L("J047") + 4.0, "clip", src=YT / "q2ueCg9bvvQ.mp4", ss=805, credit="ISRO · ANIMATION · STAGE SEPARATION", illus=True),
    S(L("J048"), "clip", src=BR / "pixabay_16160.mp4", ss=4, bright=True),
    S(L("J048") + 2.3, "clip", src=BR / "pixabay_146606.mp4", ss=6),
    S(L("J048") + 4.6, "clip", src=BR / "pixabay_7686.mp4", ss=2),
    S(L("J049"), "clip", src=YT / "ryolgbuDNSg.mp4", ss=9.4, crop=(0.06, 0.12, 1.0, 1.0), credit="PIB · TEJAS TAKE-OFF"),
    S(L("J049") + 3.2, "clip", src=YT / "zCYBJtBaUXw.mp4", ss=138, credit="INDIAN AIR FORCE"),
    S(L("J068"), "clip", src=BR / "pixabay_135849.mp4", ss=1),
    S(L("J069"), "clip", src=BR / "pixabay_135849.mp4", ss=5),
    S(L("J069") + 3.0, "clip", src=BR / "pixabay_34717.mp4", ss=6),
    S(L("J069") + 6.0, "clip", src=BR / "pixabay_80355.mp4", ss=1),
    S(L("J070"), "still", src=F404B, zoom=(1.4, 1.6), focus=(0.5, 0.45), dark=True, illus=False),
    S(L("J071"), "scene", id="C4_kaveri_blueprint", frm=None),
    S(L("J074"), "clip", src=YT / "bYhSZ9uHO0U.mp4", ss=1.5, credit="DRDO · FLYING-WING DEMONSTRATOR 2022"),
    S(L("J075"), "proof", src=PF / "pib_2021_dmrl.png", label="PIB · DEFENCE MINISTRY · 26 APR 2021"),
    S(L("J075") + 4.4, "still", src=PF / "pib_2021_blades.jpg", zoom=(1.0, 1.25), focus=(0.5, 0.45), illus=False),
    S(L("J076"), "still", src=IL76, zoom=(1.1, 1.3), focus=(0.45, 0.5), illus=False),
    S(L("J076") + 3.0, "scene", id="B4_single_crystal", frm=None),
    S(L("J077"), "still", src=AMCA, zoom=(1.0, 1.2), focus=(0.5, 0.5), illus=False),
    S(L("J084"), "scene", id="C2_title_split", frm=None),
    S(L("J085"), "clip", src=YT / "q2ueCg9bvvQ.mp4", ss=660, credit="ISRO · LVM3-M4 / CHANDRAYAAN-3"),
    S(L("J087"), "scene", id="A1_title_blade", frm=None, off=6.0),
    S(L("J088"), "scene", id="C8_dry_kaveri", frm=None),
    S(L("J088") + 3.6, "scene", id="B4_single_crystal", frm=None),
    S(L("J088") + 7.2, "still", src=AMCA, zoom=(1.2, 1.4), focus=(0.5, 0.5), illus=False),
    S(L("J089"), "clip", src=YT / "ryolgbuDNSg.mp4", ss=29.5, crop=(0.06, 0.12, 1.0, 1.0), credit="PIB · TEJAS"),
    S(L("J090"), "end"),
]


SCENE_CREDITS = {"D15_china": "J-20 · N509FZ · CC BY-SA 4.0"}   # real photos placed inside animated scenes


def scene_shots():
    out = []
    for sid, s in SCENES.items():
        out.append(dict(t=s["start"], kind="scene", id=sid, frm=s["start"], illus=True, **({"credit": SCENE_CREDITS[sid]} if sid in SCENE_CREDITS else {})))
    return out


def scene_file(sid):
    return A / "scenes" / sid[0] / f"{sid}.mp4"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"FAILED: {' '.join(map(str, cmd))[:400]}\n{r.stderr[-1500:]}")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")


def rate(H, mbps_1080, cap=30):
    b = min(cap, mbps_1080 * (H / 1080) ** 2)
    return ["-b:v", f"{b:.0f}M", "-maxrate", f"{b * 1.2:.0f}M", "-bufsize", f"{b * 2:.0f}M"]


def kb(W, H, dur, z0, z1, fx, fy, ar):
    """Ken Burns on a still: eased zoom z0->z1 around (fx, fy), oversampled 2x, no jitter."""
    n = max(1, round(dur * 30))
    ow = W * 2
    oh = int(ow / ar) if ar > W / H else H * 2
    if ar <= W / H:
        ow = int(oh * ar)
    e = f"(1-cos(PI*on/{n}))/2"
    return (f"scale={ow}:{oh},crop='min(iw,ih*{W}/{H})':'min(ih,iw*{H}/{W})',scale={W*2}:{H*2},"
            f"zoompan=z='{z0}+({z1}-{z0})*{e}':x='iw*{fx}-iw/zoom/2':y='ih*{fy}-ih/zoom/2':d={n + 2}:s={W}x{H}:fps=30")


def render(s, dur, out, W, H):
    enc = ["-frames:v", str(round(dur * 30)), "-an", "-c:v", "libx264", "-preset", "veryfast", *rate(H, 8, cap=50),
           "-pix_fmt", "yuv420p", "-r", "30"]
    k = s["kind"]
    if k == "scene" and not scene_file(s["id"]).exists():
        k, s = "pending", dict(s, desc=f"SCENE {s['id']} · session {s['id'][0]} rendering")
    if k == "scene":
        f = scene_file(s["id"])
        off = s.get("off", 0.0) if s.get("frm") is None else max(0.0, s["t"] - s["frm"])
        vf = f"scale={W}:{H}:flags=lanczos,fps=30,tpad=stop_mode=clone:stop_duration=30"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-i", str(f), "-vf", vf, "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "dissolve":   # push into scene a's last frame, then cross-dissolve into scene b's first frame (held) so b starts cleanly next
        fa, fb = scene_file(s["a"]), scene_file(s["b"])
        if not (fa.exists() and fb.exists()):
            return render(dict(kind="pending", desc=f"dissolve {s['a']} → {s['b']}"), dur, out, W, H)
        last = out.with_suffix(".last.png")
        run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", str(fa), "-frames:v", "1", "-update", "1", str(last)])
        xd = s.get("xd", 2.0)
        fx, fy = s.get("focus", (0.5, 0.5))
        z0, z1 = s.get("zoom", (1.0, 1.5))
        fc = (f"[0:v]{kb(W, H, dur, z0, z1, fx, fy, W / H)},trim=duration={dur:.3f},setpts=PTS-STARTPTS[a];"
              f"[1:v]scale={W}:{H}:flags=lanczos,fps=30,trim=end_frame=1,tpad=stop_mode=clone:stop_duration={dur:.3f},setpts=PTS-STARTPTS[b];"
              f"[a][b]xfade=transition=fade:duration={xd}:offset={dur - xd:.3f}")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(last), "-i", str(fb),
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "clip":
        z = 1.08
        pre = []
        if s.get("crop"):   # (x0, y0, x1, y1) fractions: drop burned-in tickers and channel logos before scaling
            x0, y0, x1, y1 = s["crop"]
            pre = [f"crop=iw*{x1 - x0}:ih*{y1 - y0}:iw*{x0}:ih*{y0}"]
        vf = pre + [f"scale={int(W*z)}:{int(H*z)}:force_original_aspect_ratio=increase", f"crop={int(W*z)}:{int(H*z)}",
              f"scale=w='{int(W*z)}-{int(W*(z-1))}*t/{dur:.2f}':h=-2:eval=frame", f"crop={W}:{H}", "fps=30"]
        if s.get("bright"):
            vf.append("eq=brightness=0.06:gamma=1.3")
        vf.append("vignette=PI/5")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(s.get("ss", 0)), "-stream_loop", "-1", "-i", str(s["src"]),
             "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k in ("still", "proof"):
        from PIL import Image
        iw, ih = Image.open(s["src"]).size
        z = s.get("zoom", (1.0, 1.15))
        fx, fy = s.get("focus", (0.5, 0.5))
        if k == "proof":   # push from the whole page into the highlighted words (box saved by proof_shots.js)
            bx = json.loads(Path(s["src"]).with_suffix(".json").read_text())
            fx, fy = (bx["x0"] + bx["x1"]) / 2, (bx["y0"] + bx["y1"]) / 2
            z = (1.15, max(1.8, min(2.6, 0.8 / (bx["x1"] - bx["x0"]))))
        vf = [kb(W, H, dur, z[0], z[1], fx, fy, iw / ih), "vignette=PI/6"]
        if s.get("dark"):
            vf.append("eq=brightness=-0.08:contrast=1.15:saturation=0.8")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(s["src"]), "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "black":
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x05070a:s={W}x{H}:r=30,noise=alls=6:allf=t",
             "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "pending":
        fs = int(H * 0.034)
        vf = (f"noise=alls=10:allf=t,drawtext=fontfile={FONT}:text='FOOTAGE PENDING':x=(w-tw)/2:y=h*0.40:fontsize={int(fs*1.2)}"
              f":fontcolor=0xF97316,drawtext=fontfile={FONT_M}:text='{esc(s['desc'])}':x=(w-tw)/2:y=h*0.50:fontsize={fs}"
              f":fontcolor=0xF8FAFC@0.9")
        if s.get("fetch"):
            vf += (f",drawtext=fontfile={FONT_M}:text='owner fetch list #{s['fetch']}':x=(w-tw)/2:y=h*0.57:"
                   f"fontsize={int(fs*0.7)}:fontcolor=0x94A3B8")
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x121826:s={W}x{H}:r=30", "-vf", vf,
             "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "end":
        fs = int(H * 0.034)
        fc = (f"color=c=0x0B0E14:s={W}x{H}:r=30,noise=alls=7:allf=t[bg];[1:v]scale={int(W*0.42)}:-2[l];"
              f"[bg][l]overlay=(W-w)/2:H*0.16,drawtext=fontfile={FONT}:text='SUBSCRIBE FOR THE NEXT DEEP DIVE':"
              f"x=(w-tw)/2:y=h*0.70:fontsize={fs}:fontcolor=0xF8FAFC,drawbox=x=iw*0.06:y=ih*0.62:w=iw*0.26:h=ih*0.30:"
              f"color=0xF97316@0.5:t=3,drawbox=x=iw*0.68:y=ih*0.62:w=iw*0.26:h=ih*0.30:color=0xF97316@0.5:t=3")
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc", "-loop", "1", "-i", str(ROOT / "assets/brand/banner.png"),
             "-filter_complex", fc.replace("color=c=", "color=c=", 1), "-t", f"{dur:.3f}"] + enc + [str(out)])
    else:
        sys.exit(f"unknown kind {k}")


def build_shots():
    shots = sorted(SHOTS + scene_shots(), key=lambda s: s["t"])
    # a coordinator shot that falls inside a scene's window is a deliberate cutaway only if listed; scenes win otherwise
    wins = [(s["start"], s["end"]) for s in SCENES.values()]
    keep = []
    for s in shots:
        inside = s["kind"] != "scene" and any(a - 0.01 <= s["t"] < b - 0.2 for a, b in wins)
        if not inside:
            keep.append(s)
    return keep


def build_vo(out):
    """Joined VO in program time: block 1, 1.5 s gap, block 2, with silences at every picture-only break."""
    d1 = PROG["block1_dur"]
    segs, cur = [], 0.0
    cuts = sorted((b["vo_at"], b["len"]) for b in PROG["breaks"] if "vo_at" in b and b["kind"] != "END_CARD")
    for at, ln in cuts:
        segs.append((cur, at, ln)); cur = at
    segs.append((cur, None, 0.0))
    joined = A / "vo_joined.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "voice/block1.mp3"), "-i", str(P / "voice/block2.mp3"), "-filter_complex",
         f"[0:a]aresample=48000,apad=pad_dur={PROG['block_gap']}[a0];[1:a]aresample=48000[a1];[a0][a1]concat=n=2:v=0:a=1",
         str(joined)])
    parts, fc = [], []
    for i, (a, b, pad) in enumerate(segs):
        trim = f"atrim=start={a}" + (f":end={b}" if b is not None else "")
        fc.append(f"[0:a]{trim},asetpts=PTS-STARTPTS" + (f",apad=pad_dur={pad}" if pad else "") + f"[s{i}]")
        parts.append(f"[s{i}]")
    fc.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,apad=whole_dur={END:.2f}")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(joined), "-filter_complex", ";".join(fc), "-t", f"{END:.2f}", str(out)])


def overlays(W, H, shots):
    """drawtext windows: citation tag per line (bottom right), ILLUSTRATION over scenes and illustrative stills,
    the on-screen line (lower left) where no animated scene covers the line."""
    f = []
    fs = int(H * 0.025)
    scene_win = [(s["start"], s["end"]) for s in SCENES.values()]
    for l in PROG["lines"]:
        a, b = l["start"] - 0.1, l["end"] + 0.4
        if l["cite"]:
            f.append(f"drawtext=fontfile={FONT_M}:text='{esc(l['cite'])}':x=w-tw-{int(W*0.035)}:y=h-{int(H*0.075)}:"
                     f"fontsize={fs}:fontcolor=0xF8FAFC@0.85:box=1:boxcolor=0x0B0E14@0.55:boxborderw={int(fs*0.5)}:"
                     f"enable='between(t,{a:.2f},{b:.2f})'")
        covered = any(x <= l["start"] < y for x, y in scene_win)
        if l["onscreen"] and not covered:
            f.append(f"drawtext=fontfile={FONT}:text='{esc(l['onscreen'])}':x={int(W*0.05)}:y=h-{int(H*0.16)}:"
                     f"fontsize={int(H*0.034)}:fontcolor=0xF8FAFC:box=1:boxcolor=0x0B0E14@0.7:boxborderw={int(H*0.014)}:"
                     f"enable='between(t,{a + 0.3:.2f},{b:.2f})'")
    for i, s in enumerate(shots):
        end = shots[i + 1]["t"] if i + 1 < len(shots) else END
        if s.get("credit"):
            f.append(f"drawtext=fontfile={FONT_M}:text='{esc(s['credit'])}':x={int(W*0.035)}:y={int(H*0.045)}:"
                     f"fontsize={int(fs*0.8)}:fontcolor=0xF8FAFC@0.8:box=1:boxcolor=0x0B0E14@0.45:boxborderw={int(fs*0.35)}:"
                     f"enable='between(t,{s['t']:.2f},{end:.2f})'")
        if s["kind"] == "scene" or s.get("illus"):
            f.append(f"drawtext=fontfile={FONT_M}:text='ILLUSTRATION':x=w-tw-{int(W*0.035)}:y=h-{int(H*0.115)}:"
                     f"fontsize={int(fs*0.85)}:fontcolor=0xF97316@0.9:enable='between(t,{s['t']:.2f},{end:.2f})'")
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--check", action="store_true", help="list pending shots and missing scenes, render nothing")
    a = ap.parse_args()
    H = a.height; W = H * 16 // 9
    shots = build_shots()
    if a.check:
        pend = [s for s in shots if s["kind"] == "pending"]
        miss = sorted({s["id"] for s in shots if s["kind"] == "scene" and not scene_file(s["id"]).exists()})
        print(f"{len(shots)} shots; {len(pend)} pending footage; {len(miss)} scenes not rendered yet")
        for s in pend:
            print(f"  PENDING {s['t']:7.2f} {s['desc']}")
        print("  scenes missing:", ", ".join(miss))
        return
    sd = A / f"shots{H}"; sd.mkdir(parents=True, exist_ok=True)
    lst = []
    for i, s in enumerate(shots):
        end = shots[i + 1]["t"] if i + 1 < len(shots) else END
        dur = (round(end * 30) - round(s["t"] * 30)) / 30
        if dur <= 0:
            continue
        src = scene_file(s["id"]) if s["kind"] == "scene" else s.get("src")
        mt = Path(src).stat().st_mtime if src and Path(src).exists() else 0
        key = hashlib.sha1(json.dumps([s, dur, W, H, mt, RENDER_V], default=str, sort_keys=True).encode()).hexdigest()[:8]
        out = sd / f"{i:03d}_{s['kind']}_{key}.mp4"
        if not out.exists():
            render(s, dur, out, W, H)
        print(f"{i:03d} {s['t']:7.2f} {dur:6.2f} {s['kind']:7s} {s.get('id') or s.get('desc') or Path(str(s.get('src',''))).name}", flush=True)
        lst.append(f"file '{out}'")
    (sd / "list.txt").write_text("\n".join(lst) + "\n")
    video = A / f"video{H}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(sd / "list.txt"), "-c", "copy", str(video)])

    vo = A / "vo_program.wav"
    build_vo(vo)
    bed = A / "bed.wav"
    reveals = [b["start"] for b in PROG["breaks"] if b["kind"] == "VO_PAUSE" and b["after"] in ("J019", "J053")]
    if not bed.exists():
        cues = {"duration": END + 1, "impacts": [r + 1.5 for r in reveals], "swells": [{"at": L("J009") - 1, "dur": 3}],
                "sections": [{"start": 0, "mood": "tense"}, {"start": L("J071"), "mood": "calm"}]}
        (A / "bed_cues.json").write_text(json.dumps(cues))
        py = ROOT / ".venv/bin/python"
        run([str(py) if py.exists() else sys.executable, str(ROOT / "scripts/make_bed.py"), str(A / "bed_cues.json"), str(bed)])
    silence = "+".join(f"between(t,{r:.2f},{r + 1.5:.2f})" for r in reveals)
    mix = A / "mix_raw.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(vo), "-i", str(bed), "-filter_complex",
         f"[1:a]volume=-25dB,volume='if({silence},0,1)':eval=frame[b];"
         f"[b][0:a]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=500[bd];"
         f"[0:a][bd]amix=inputs=2:duration=first:normalize=0[a]", "-map", "[a]", "-t", f"{END:.2f}", str(mix)])

    def integrated(f, af="anull"):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af", f"{af},ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return float(r[r.rindex("I:"):].split()[1])
    gain = -14.0 - integrated(mix)
    ln = lambda g: f"volume={g:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false"
    for _ in range(2):
        got = integrated(mix, ln(gain))
        if abs(got + 14.0) < 0.25:
            break
        gain += -14.0 - got

    logo = A / f"logo_bug_{H}.png"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "assets/brand/logo_square.png"), "-vf",
         f"scale={int(H*0.085)}:-2,format=rgba,colorchannelmixer=aa=0.85", str(logo)])
    sting = A / f"sting_{H}.png"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "assets/brand/banner.png"), "-vf", f"scale={int(W*0.5)}:-2", str(sting)])
    t_sting = L("J009")
    t_end = SHOTS[-1]["t"]
    ov = ",".join(overlays(W, H, shots))
    out = A / f"jet-engine-paradox-cut-{H}p.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(mix),
         "-loop", "1", "-framerate", "30", "-t", f"{END:.2f}", "-i", str(logo),
         "-loop", "1", "-framerate", "30", "-t", f"{END:.2f}", "-i", str(sting), "-filter_complex",
         f"[3:v]format=rgba,fade=t=in:st={t_sting:.2f}:d=0.4:alpha=1,fade=t=out:st={t_sting + 2.2:.2f}:d=0.4:alpha=1[sg];"
         f"[0:v][sg]overlay=(W-w)/2:(H-h)/2:enable='between(t,{t_sting:.2f},{t_sting + 2.7:.2f})'[v1];"
         f"[v1][2:v]overlay=W-w-{int(H*0.04)}:{int(H*0.04)}:enable='not(between(t,{t_sting:.2f},{t_sting + 2.7:.2f})+gte(t,{t_end:.2f}))'[v2];"
         f"[v2]{ov}[v];[1:a]{ln(gain)},aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium" if H >= 2160 else "veryfast", *rate(H, 8, cap=40 if H >= 2160 else 20),
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{END:.2f}", str(out)])
    print("wrote", out)


if __name__ == "__main__":
    main()
