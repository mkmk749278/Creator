#!/usr/bin/env python3
"""Assemble Can't Pay Even the Minimum (visual-plan.md) from the shot list below. 720p preview by default.

Scenes (video/cantpay/<id>, rendered by build/render_scenes.sh to assets/scenes/<id>.mp4) carry the picture; real footage
and source proofs cut in at the word they belong to, and the scene keeps time underneath (a shot of scene X at film time t
plays X from t - X.start). Each shot renders once to assets/shots<H>/ (spec hash), then they are joined and mixed:
VO (3 blocks, 0.6 s gaps) + scene SFX + a synthesised tension bed (silent 1.5 s before each reveal, then a low impact)
+ Dreamer (Incompetech, CC BY) under the five steps, two-pass to -14 LUFS.
  python3 projects/cant-pay-minimum/build/assemble.py [--height 720]
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import L, OFF, END, VO_END     # noqa: E402
from words import P                        # noqa: E402

PR_ = Path(__file__).resolve().parents[1]
ROOT = PR_.parents[1]
A = PR_ / "assets"
BR, PF, PH, SC = A / "broll", A / "proof", A / "photos", A / "scenes"
MD = ROOT / "projects/minimum-due/assets"            # our own Part 1 film and its sting/end-card plates
FONTS = MD / "fonts"
LFONT, TFONT = FONTS / "Bricolage-800.ttf", FONTS / "JetBrainsMono-700.ttf"
RENDER_V = 1


def scene_span(sid):
    js = (ROOT / "video/cantpay" / sid / "params.js").read_text()
    a, b = js.split("(")[1].split(" s of")[0].split("–")
    return float(a), float(b)


def S(t, kind, **kw):
    return dict(t=round(t, 2), kind=kind, **kw)


def scene(sid, t=None):
    return S(scene_span(sid)[0] if t is None else t, "scene", id=sid)


def cut(sid, t0, t1, shot):
    """Cut away from scene `sid` at t0 to `shot`, come back to the scene (at the matching time) at t1 (unless the scene
    is over by then)."""
    return [dict(shot, t=round(t0, 2))] + ([scene(sid, t1)] if t1 < scene_span(sid)[1] - 0.3 else [])


TAG_ILL = "ILLUSTRATIVE FOOTAGE"
SHOTS = [
    # ---------------- ACT 1: hook ----------------
    scene("d01_night"),
    *cut("d01_night", P("C003", "In our last") - 0.15, P("C003", "Today") - 0.25,
         S(0, "clip", src=MD / "minimum-due-refined-preview-720p.mp4", ss=130.0, flat=True, label="PART 1 · MINIMUM AMOUNT DUE")),
    scene("p01_minimum"),
    S(L("C005")[0] - 0.2, "clip", src=BR / "pixabay_262440.mp4", ss=3.0, label="MAYBE YOUR SALARY STOPPED"),
    S(P("C005", "Maybe a hospital") - 0.15, "clip", src=BR / "coverr_iv-in-hospital-room-5485.mp4", ss=2.0, label="A HOSPITAL BILL CAME FIRST"),
    S(P("C005", "It happens") - 0.15, "clip", src=BR / "pixabay_154195.mp4", ss=12.0, label="GOOD, HONEST PEOPLE"),
    S(L("C006")[0] - 0.2, "clip", src=BR / "pixabay_230083.mp4", ss=2.0, label="WILL THE POLICE COME?", tag=TAG_ILL),
    S(P("C006", "Will they take") - 0.15, "clip", src=BR / "pixabay_95123.mp4", ss=9.0, label="MY SALARY?"),
    S(P("C006", "Will my family") - 0.15, "clip", src=BR / "pixabay_53958.mp4", ss=6.0, label="MY FAMILY?"),
    scene("p02_two_stories"),
    S(L("C009")[0] - 0.2, "proof", src=PF / "rbi_npa_90.png", label="THE RULES ON PAPER", tag="RBI | MASTER CIRCULAR"),
    S(P("C009", "and the reality") - 0.15, "clip", src=BR / "pixabay_8698.mp4", ss=10.0, label="THE REALITY ON THE GROUND"),
    S(L("C010")[0] - 0.2, "sting"),
    # ---------------- ACT 2: the system ----------------
    scene("p03_clock"),
    *cut("p03_clock", P("C013", "If the minimum") - 0.1, P("C013", "the bank must") - 0.1,
         S(0, "proof", src=PF / "rbi_npa_90.png", tag="RBI | IRAC NORMS")),
    scene("p04_provision"),
    scene("p05_myth"),
    scene("p06_cibil"),
    S(L("C020")[0] - 0.2, "proof", src=PF / "kanoon_sbi_cibil.png", label="SBI CARD HELD AT FAULT", tag="CONSUMER COMMISSION ORDER | VIA INDIAN KANOON"),
    scene("p07_blocked"),
    scene("p08_ravi_sunita"),
    *cut("p08_ravi_sunita", P("C024", "plus eighteen") + 0.9, L("C025")[0] + 0.3,
         S(0, "proof", src=PF / "hdfc_mitc_rate_375.png", tag="HDFC BANK MITC | OCT 2026")),
    *cut("p08_ravi_sunita", P("C025", "It is a fixed") - 0.1, P("C025", "On ten thousand") - 0.1,
         S(0, "proof", src=PF / "hdfc_mitc_late_fee.png", tag="HDFC BANK MITC | OCT 2026")),
    *cut("p08_ravi_sunita", P("C030", "using one") - 0.1, L("C031")[0] - 0.4,
         S(0, "proof", src=PF / "hdfc_mitc_late_fee.png", tag="HDFC BANK MITC | OCT 2026")),
    scene("d02_call"),
    S(L("C032")[0] - 0.2, "clip", src=BR / "pixabay_141672.mp4", ss=1.0, label="1 TO 90 DAYS: MOSTLY CALLS", tag="BANK OF BARODA | COLLECTION TENDER 2022"),
    S(P("C032", "SMS") - 0.2, "clip", src=BR / "pixabay_134872.mp4", ss=6.0, label="SMS, WHATSAPP"),
    S(P("C032", "Many from") - 0.15, "clip", src=BR / "pixabay_262440.mp4", ss=9.0, label="BIG CALL CENTRES IN CITIES"),
    scene("p09_dials"),
    scene("p10_agency"),
    *cut("p10_agency", P("C035", "on accounts") + 0.6, L("C036")[0] - 0.3,
         S(0, "proof", src=PF / "pnb_commission_slabs.png", tag="PNB | RECOVERY AGENT POLICY")),
    scene("p11_map"),
    *cut("p11_map", L("C037")[0] - 0.2, P("C037", "old room") - 0.2,
         S(0, "clip", src=BR / "pixabay_200435.mp4", ss=8.0, label="CARD ADDRESS: THE CITY")),
    *cut("p11_map", P("C037", "village") - 0.1, L("C038")[0] - 0.1,
         S(0, "clip", src=BR / "pixabay_53958.mp4", ss=0.5, label="FAMILY: A FAR VILLAGE")),
    *cut("p11_map", P("C038", "one card company's") - 0.1, P("C038", "six places") + 0.5,
         S(0, "proof", src=PF / "onecard_ap_tg_agencies.png", tag="ONECARD | REPAYMENT AGENCIES LIST")),
    *cut("p11_map", P("C039", "a long trip") - 0.1, P("C039", "So small dues") - 0.15,
         S(0, "clip", src=BR / "pixabay_276582.mp4", ss=1.0, label="A LONG TRIP RARELY PAYS", tag="OUR ESTIMATE")),
    *cut("p11_map", P("C040", "One bank pays") - 0.1, P("C040", "That's worth") - 0.1,
         S(0, "proof", src=PF / "pnb_trace_7500.png", tag="PNB | RECOVERY AGENT POLICY")),
    scene("p12_court"),
    *cut("p12_court", P("C042", "To file a case") - 0.1, P("C042", "On a small") - 0.1,
         S(0, "photo", src=PH / "commons_telangana_high_court_imahesh.jpg", label="COURT FEES + A LAWYER",
           tag="TELANGANA HIGH COURT | PHOTO: IMAHESH, CC BY-SA 4.0")),
    *cut("p12_court", P("C043", "In one real") - 0.1, L("C044")[0] - 0.25,
         S(0, "proof", src=PF / "kanoon_lok_adalat_indore.png", tag="MP STATE COMMISSION | VIA INDIAN KANOON")),
    *cut("p12_court", P("C045", "In the Delhi") - 0.1, P("C045", "void") - 0.5,
         S(0, "proof", src=PF / "bnb_76000_awards.png", tag="BAR AND BENCH | DELHI HIGH COURT")),
    scene("d03_slabs"),
    *cut("d03_slabs", P("C049", "maybe a visit") - 0.1, P("C049", "and settlement") - 0.1,
         S(0, "clip", src=BR / "pixabay_200435.mp4", ss=14.0, label="A VISIT, IF IN A CITY THEY COVER", tag="OUR ESTIMATE")),
    *cut("d03_slabs", P("C050", "people tracing") - 0.1, P("C050", "and legal") - 0.1,
         S(0, "clip", src=BR / "pixabay_111161.mp4", ss=2.0, label="TRACING YOU IF YOU MOVED", tag="OUR ESTIMATE")),
    scene("p13_per_bank"),
    # ---------------- ACT 3: traps, the fear ----------------
    S(L("C053")[0] - 0.25, "clip", src=BR / "pixabay_154195.mp4", ss=0.5, label="TWO TRAPS FOR SALARIED PEOPLE"),
    scene("p14_setoff", L("C054")[0] - 0.25),
    *cut("p14_setoff", L("C056")[0] - 0.15, P("C056", "And in February") - 0.15,
         S(0, "proof", src=PF / "kanoon_ncdrc_setoff_53k.png", label="₹53,000 TAKEN FOR CARD DUES", tag="NCDRC | VIA INDIAN KANOON")),
    *cut("p14_setoff", P("C056", "And in February") - 0.15, L("C057")[0] - 0.3,
         S(0, "proof", src=PF / "kanoon_kerala_hold.png", label="A HOLD IS NOT AN ATTACHMENT", tag="KERALA HIGH COURT | FEB 2026")),
    scene("p15_borrower"),
    scene("p16_chain"),
    S(L("C063")[0] - 0.2, "clip", src=BR / "pixabay_201109.mp4", ss=5.0, label="WILL THE POLICE ARREST YOU?", tag=TAG_ILL),
    scene("d04_truth"),
    S(scene_span("d04_truth")[1], "proof", src=PF / "sc_2019_not_cheating.png", label="NOT REPAYING IS NOT CHEATING", tag="SUPREME COURT | 2019"),
    S(P("C065", "And in twenty") - 0.15, "proof", src=PF / "sc_2025_kukreja.png", label="POLICE ARE NOT RECOVERY AGENTS", tag="SUPREME COURT | 2025"),
    scene("p17_criminal"),
    scene("p18_writeoff"),
    *cut("p18_writeoff", P("C070", "SBI Card") - 0.1, P("C070", "But you still") - 0.1,
         S(0, "proof", src=PF / "sbi_faq_writeoff.png", tag="SBI CARD | FAQ")),
    # ---------------- ACT 4: the defence ----------------
    scene("p19_step1"),
    scene("p20_step2"),
    scene("p21_complain"),
    *cut("p21_complain", P("C074", "since July") - 0.1, P("C074", "The RBI helpline") - 0.1,
         S(0, "proof", src=PF / "rbi_ombudsman_90days.png", tag="RBI | OMBUDSMAN SCHEME 2026")),
    scene("p22_step3"),
    *cut("p22_step3", P("C076", "Type it yourself") - 0.1, P("C076", "Never tap") - 0.15,
         S(0, "proof", src=PF / "ecourts_case_status.png", tag="ECOURTS SERVICES")),
    scene("p23_step4"),
    *cut("p23_step4", P("C078", "won't lend") - 0.1, P("C078", "Later") - 0.2,
         S(0, "clip", src=BR / "pixabay_95123.mp4", ss=10.0, label="NO NEW LOAN FROM THAT BANK FOR A YEAR")),
    scene("p24_step5"),
    *cut("p24_step5", L("C080")[0] - 0.1, P("C080", "Use the") - 0.1,
         S(0, "clip", src=BR / "pixabay_154195.mp4", ss=18.0, label="YOU CHOOSE WHERE YOUR SALARY GOES")),
    scene("d05_recap"),
    *cut("d05_recap", P("C081", "Can they take") - 0.1, P("C081", "Without a court") + 0.6,
         S(0, "clip", src=BR / "pixabay_271463.mp4", ss=2.0, label="CAN THEY TAKE YOUR SALARY?")),
    S(L("C083")[0] - 0.2, "clip", src=BR / "pixabay_134872.mp4", ss=1.0, label="HAS AN AGENT CALLED YOU? COMMENT"),
    S(L("C084")[0] - 0.2, "clip", src=BR / "pixabay_202987.mp4", ss=2.0, label="SHARE IT WITH ONE PERSON"),
    S(P("C084", "And subscribe") - 0.2, "end"),
]


# ---------------------------------------------------------------------------------------------------- render helpers
def run(cmd):
    r = subprocess.run(list(map(str, cmd)), capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-800:]}")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,")


def text_w(txt, font, size):
    from PIL import ImageFont
    return ImageFont.truetype(str(font), size).getlength(txt)


def rate(H, mbps_720, cap=30):
    b = min(cap, mbps_720 * (H / 720) ** 2)
    return ["-b:v", f"{b:.0f}M", "-maxrate", f"{b * 1.2:.0f}M", "-bufsize", f"{b * 2:.0f}M"]


def overlays(W, H, label="", tag=""):
    """Lower-left label (gold bar, dark panel, Bricolage) and lower-right source tag (mono pill)."""
    k = H / 1080; f = []
    if label:
        fs = int(40 * k); pad = int(24 * k); h = int(72 * k); x0, y0 = int(84 * k), int(918 * k)
        w = int(text_w(label, LFONT, fs)) + 2 * pad
        f.append(f"drawbox=x={x0}:y={y0}:w={int(8 * k)}:h={h}:color=0xF6C453@1:t=fill")
        f.append(f"drawbox=x={x0 + int(8 * k)}:y={y0}:w={w}:h={h}:color=0x0B0F17@0.72:t=fill")
        f.append(f"drawtext=fontfile={LFONT}:expansion=none:text='{esc(label)}':x={x0 + int(8 * k) + pad}:y={y0}+({h}-th)/2:fontsize={fs}:fontcolor=white")
    if tag:
        fs = int(19 * k); pad = int(12 * k); h = int(34 * k)
        w = int(text_w(tag, TFONT, fs)) + 2 * pad
        x0, y0 = W - w - int(64 * k), H - h - int(44 * k)
        f.append(f"drawbox=x={x0}:y={y0}:w={w}:h={h}:color=0x0B0F17@0.85:t=fill")
        f.append(f"drawtext=fontfile={TFONT}:expansion=none:text='{esc(tag)}':x={x0 + pad}:y={y0}+({h}-th)/2:fontsize={fs}:fontcolor=white@0.92")
    return f


def kb(W, H, dur, z0=1.0, z1=1.08, fx=0.5, fy=0.5, fx1=None, aspect=None):
    """Ken Burns on a still (ease in-out zoom around a focus, optional horizontal pan), cover-cropped to 16:9 first."""
    n = max(1, int(dur * 30)); fx1 = fx if fx1 is None else fx1
    cfx, cfx1, cfy = fx, fx1, fy
    if aspect and abs(aspect - 16 / 9) > 0.02:
        if aspect > 16 / 9:
            vis = (16 / 9) / aspect; left = max(0, min(1 - vis, fx - vis / 2)); cfx, cfx1 = (fx - left) / vis, (fx1 - left) / vis
        else:
            vis = aspect / (16 / 9); top = max(0, min(1 - vis, fy - vis / 2)); cfy = (fy - top) / vis
    ease = f"(0.5-0.5*cos(PI*on/{n}))"
    o = 4 if H <= 1080 else 2
    pre = (f"scale={W*o}:{H*o}:force_original_aspect_ratio=increase,"
           f"crop={W*o}:{H*o}:'max(0,min(iw-ow,iw*{fx}-ow/2))':'max(0,min(ih-oh,ih*{fy}-oh/2))'")
    return (f"{pre},zoompan=z='{z0}+({z1}-{z0})*{ease}':"
            f"x='iw*({cfx}+({cfx1}-{cfx})*{ease})-iw/zoom/2':y='ih*{cfy}-ih/zoom/2':d={n+2}:s={W}x{H}:fps=30")


def proof_box(png):
    j = Path(png).with_suffix(".json")
    b = json.loads(j.read_text()) if j.exists() else None
    return (b["x0"], b["y0"], b["x1"], b["y1"]) if b else (0.3, 0.45, 0.7, 0.55)


def proof_parts(s, dur):
    """Establish (whose page) -> push in until the highlighted line reads on a phone -> pan along it on long holds."""
    x0, y0, x1, y1 = proof_box(s["src"]); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    zt = max(2.1, min(3.0, 1 / max(0.33, (x1 - x0) * 1.15)))
    if dur < 3.6:
        return [dict(s, kind="still", zoom=(zt * 0.72, zt), focus=(cx, cy + 0.1 / zt))]
    a = min(2.0, max(1.3, dur * 0.28)); rest = dur - a
    parts = [dict(s, kind="still", zoom=(1.0, 1.06), focus=(0.5 + (cx - 0.5) * 0.3, 0.5 + (cy - 0.5) * 0.3)),
             dict(s, t=round(s["t"] + a, 2), kind="still", zoom=(zt * 0.86, zt), focus=(cx, cy + 0.1 / zt))]
    if rest > 4.8:
        half = 0.5 / zt
        p0, p1 = (x0 + half, x1 - half) if x1 - x0 > 2 * half else (cx - 0.1, cx + 0.04)
        parts.append(dict(s, t=round(s["t"] + a + rest / 2, 2), kind="still", zoom=(zt, zt * 1.04), focus=(p0, cy + 0.1 / zt), pan_to=p1))
    return parts


def expand(shots, end):
    shots = [s for i, s in enumerate(shots) if (shots[i + 1]["t"] if i + 1 < len(shots) else end) - s["t"] > 0.1]   # zero-length returns
    out = []
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else end
        dur = nxt - s["t"]
        if s["kind"] == "proof":
            out += proof_parts(s, dur)
        elif s["kind"] == "photo" and dur <= 4.5:
            out.append(dict(s, kind="still", zoom=(1.0, 1.12), focus=(0.5, 0.45)))
        elif s["kind"] == "photo":
            out += [dict(s, kind="still", zoom=(1.0, 1.1), focus=(0.5, 0.45)), dict(s, t=round(s["t"] + dur / 2, 2), kind="still", zoom=(1.15, 1.28), focus=(0.55, 0.4))]
        else:
            out.append(s)
    return out


def render(shot, dur, out, W, H):
    k = shot["kind"]; lab, tag = shot.get("label", ""), shot.get("tag", "")
    enc = ["-frames:v", str(round(dur * 30)), "-an", "-c:v", "libx264", "-preset", "veryfast", *rate(H, 5), "-pix_fmt", "yuv420p", "-r", "30"]
    if k == "clip":
        if shot.get("flat"):
            vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase", f"crop={W}:{H}", "fps=30"]
        else:
            vf = [f"scale={int(W*1.08)}:{int(H*1.08)}:force_original_aspect_ratio=increase", f"crop={int(W*1.08)}:{int(H*1.08)}",
                  f"scale=w='{int(W*1.08)}-{int(W*0.08)}*t/{dur:.2f}':h=-2:eval=frame", f"crop={W}:{H}", "fps=30", "vignette=PI/5"]
        if shot.get("bright"):
            vf.append("eq=brightness=0.06:gamma=1.3")
        run(["ffmpeg", "-v", "error", "-y", "-ss", shot.get("ss", 0), "-stream_loop", "-1", "-i", shot["src"],
             "-vf", ",".join(vf + overlays(W, H, lab, tag)), "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "scene":
        off = shot["t"] - scene_span(shot["id"])[0]
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, off):.3f}", "-i", SC / (shot["id"] + ".mp4"),
             "-vf", ",".join([f"scale={W}:{H}", "fps=30"] + overlays(W, H, lab, tag)), "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "still":
        from PIL import Image
        iw, ih = Image.open(shot["src"]).size
        fx, fy = shot.get("focus", (0.5, 0.5)); z = shot.get("zoom", (1.0, 1.15))
        vf = [kb(W, H, dur, z[0], z[1], fx, fy, shot.get("pan_to"), iw / ih), "vignette=PI/6"] + overlays(W, H, lab, tag)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", shot["src"], "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "sting":
        fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=brightness=-0.15[bg];"
              f"[1:v]scale={int(W*0.62)}:-2,format=rgba,fade=t=in:st=0:d=0.5:alpha=1[l];[bg][l]overlay=(W-w)/2:(H-h)/2")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", MD / "broll/pixabay_200431.mp4", "-loop", "1", "-i", ROOT / "assets/brand/banner.png",
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "end":
        fc = (f"[0:v]scale={int(W*1.12)}:{int(H*1.12)}:force_original_aspect_ratio=increase,crop={int(W*1.12)}:{int(H*1.12)},"
              f"scale=w='{int(W*1.12)}-{int(W*0.12)}*t/{dur:.2f}':h=-2:eval=frame,crop={W}:{H},boxblur=8,eq=brightness=-0.25[bg];"
              f"[1:v]scale={int(W*0.5)}:-2[l];[bg][l]overlay=(W-w)/2:H*0.18-{int(H*0.03)}*t/{dur:.2f},"
              f"drawtext=fontfile={LFONT}:expansion=none:text='SUBSCRIBE · BE PRACTICAL WITH KISHORE':x=(w-tw)/2:y=h*0.72:fontsize={int(H*0.038)}:fontcolor=white,"
              f"drawtext=fontfile={TFONT}:expansion=none:text='EDUCATION ONLY · NOT LEGAL OR FINANCIAL ADVICE':x=(w-tw)/2:y=h*0.80:fontsize={int(H*0.022)}:fontcolor=white@0.8")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-stream_loop", "-1", "-i", BR / "pixabay_200435.mp4", "-loop", "1", "-i", ROOT / "assets/brand/banner.png",
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [out])
    else:
        sys.exit("unknown kind " + k)


def src_mtime(s):
    f = SC / (s["id"] + ".mp4") if s["kind"] == "scene" else s.get("src")
    return Path(f).stat().st_mtime if f and Path(f).exists() else 0


# ---------------------------------------------------------------------------------------------------- audio
def wav(path):
    import numpy as np, wave
    w = wave.open(str(path)); sr = w.getframerate(); ch = w.getnchannels()
    a = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, ch) / 32768
    return (a if ch == 2 else np.repeat(a, 2, 1)), sr


def write_wav(path, a, sr=48000):
    import numpy as np, wave
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype("<i2").tobytes())


def sfx_bus(shots, out):
    """Each scene's sound-effect track under the shots that show it, at the right offset into the scene."""
    import numpy as np
    sr = 48000; bus = np.zeros((int((END + 1) * sr), 2))
    for i, x in enumerate(shots):
        f = SC / f"{x.get('id')}.sfx.wav"
        if x["kind"] != "scene" or not f.exists():
            continue
        a, _ = wav(f)
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else END
        off = int((x["t"] - scene_span(x["id"])[0]) * sr); n = int((nxt - x["t"]) * sr); at = int(x["t"] * sr)
        seg = a[max(0, off): max(0, off) + n]
        bus[at: at + len(seg)] += seg[: len(bus) - at]
    sys.path.insert(0, str(ROOT / "video/lib/doodle"))
    import make_sfx   # the low impact after each reveal's silence (charter: braam/thud at -6 to -8 dB)
    th = make_sfx.thud(); th = th / (np.max(np.abs(th)) + 1e-9) * 10 ** (-7 / 20)
    for r in REVEALS:
        at = int((r - 0.02) * sr); bus[at: at + len(th)] += np.stack([th, th], 1)[: len(bus) - at]
    write_wav(out, bus)


REVEALS = [L("C027")[0], L("C064")[0]]       # 1.5 s of music silence before each, then a low impact (charter)
T_DREAMER = L("C071")[0] - 0.6


def music(out):
    """Tension bed (scripts/make_bed.py, synthesised, ours) to the five steps, then Dreamer under Act 4."""
    bed = A / "bed.wav"; cues = A / "bed_cues.json"
    spec = {"duration": END + 1, "impacts": [r - 0.05 for r in REVEALS] + [L("C013")[0] + 6.0],
            "swells": [{"at": L("C004")[0] - 2.0, "dur": 2.5}, {"at": L("C063")[0] - 1.5, "dur": 3.0}],
            "sections": [{"start": 0, "mood": "tense"}]}
    if not bed.exists() or not cues.exists() or json.loads(cues.read_text()) != spec:
        cues.write_text(json.dumps(spec))
        py = ROOT / ".venv/bin/python"
        run([py if py.exists() else sys.executable, ROOT / "scripts/make_bed.py", cues, bed])
    duck = "+".join(f"between(t,{r - 1.55:.2f},{r - 0.05:.2f})" for r in REVEALS)
    run(["ffmpeg", "-v", "error", "-y", "-i", bed, "-i", A / "music/incompetech_Dreamer.mp3", "-filter_complex",
         f"[0:a]aresample=48000,volume=-25dB,volume='if({duck},0,1)':eval=frame,afade=t=out:st={T_DREAMER - 2.5:.2f}:d=3[b];"
         f"[1:a]aresample=48000,volume=-27dB,afade=t=in:st=0:d=3,afade=t=out:st={END - T_DREAMER - 4:.2f}:d=4,adelay={int(T_DREAMER * 1000)}|{int(T_DREAMER * 1000)}[d];"
         f"[b][d]amix=inputs=2:duration=first:normalize=0", "-t", f"{END:.2f}", out])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--height", type=int, default=720)
    a = ap.parse_args(); H = a.height; W = H * 16 // 9
    global SC
    if H >= 2160:
        SC = A / "scenes4k"
    sd = A / f"shots{H}"; sd.mkdir(parents=True, exist_ok=True)
    shots = expand(sorted(SHOTS, key=lambda s: s["t"]), END)
    lst = []
    for i, s in enumerate(shots):
        end = shots[i + 1]["t"] if i + 1 < len(shots) else END
        dur = (round(end * 30) - round(s["t"] * 30)) / 30
        if dur <= 0:
            sys.exit(f"shot {i} {s.get('id') or s.get('label')} has no time ({s['t']} -> {end})")
        key = hashlib.sha1(json.dumps([s, dur, W, H, src_mtime(s), RENDER_V], default=str, sort_keys=True).encode()).hexdigest()[:8]
        out = sd / f"{i:03d}_{s['kind']}_{key}.mp4"
        if not out.exists():
            render(s, dur, out, W, H)
        print(f"{i:03d} {s['t']:7.2f} {dur:6.2f} {s['kind']:6s} {s.get('id') or s.get('label') or ''}", flush=True)
        lst.append(f"file '{out}'")
    (sd / "list.txt").write_text("\n".join(lst) + "\n")
    video = A / f"video{H}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", sd / "list.txt", "-c", "copy", video])
    sting = next(s for s in shots if s["kind"] == "sting"); nxt = shots[shots.index(sting) + 1]["t"]
    bug_off = f"between(t,{sting['t']},{nxt})+gte(t,{shots[-1]['t']})"
    vo = A / "vo.wav"
    run(["ffmpeg", "-v", "error", "-y", *sum((["-i", PR_ / f"voice/block{b}.mp3"] for b in (1, 2, 3)), []), "-filter_complex",
         "[0:a]apad=pad_dur=0.6[a0];[1:a]apad=pad_dur=0.6[a1];[a0][a1][2:a]concat=n=3:v=0:a=1,aresample=48000", vo])
    mus, sfx, mix = A / "music_bus.wav", A / "sfx_bus.wav", A / "mix_raw.wav"
    music(mus); sfx_bus(shots, sfx)
    run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", mus, "-i", sfx, "-filter_complex",
         "[0:a]aresample=48000[v];[2:a]aresample=48000[s];[v][1:a][s]amix=inputs=3:duration=longest:normalize=0[a]",
         "-map", "[a]", "-t", f"{END:.2f}", mix])

    def integrated(f, af="anull"):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af", f"{af},ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return float(r[r.rindex("I:"):].split()[1])
    gain = -14.0 - integrated(mix)
    ln = f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false"
    for _ in range(2):
        got = integrated(mix, ln)
        if abs(got + 14.0) < 0.25:
            break
        gain += -14.0 - got; ln = f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false"
    logo = A / f"logo_bug_{H}.png"
    run(["ffmpeg", "-v", "error", "-y", "-i", ROOT / "assets/brand/logo_square.png", "-vf", f"scale={int(H*0.09)}:-2,format=rgba,colorchannelmixer=aa=0.85", logo])
    out = A / (f"cant-pay-minimum-preview-{H}p.mp4" if H < 2160 else "cant-pay-minimum-master-4k.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", mix, "-loop", "1", "-framerate", "30", "-t", f"{END:.2f}", "-i", logo,
         "-filter_complex", "[2:v]format=rgba[lg];"
         f"[0:v][lg]overlay=W-w-{int(H*0.04)}:{int(H*0.04)}:enable='not({bug_off})'[v];[1:a]{ln},aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", *rate(H, 4, cap=20),
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{END:.2f}", out])
    print("wrote", out)


if __name__ == "__main__":
    main()
