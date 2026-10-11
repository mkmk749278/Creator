#!/usr/bin/env python3
"""Assemble the Minimum Amount Due preview (720p by default) from the shot list below.

Every VO line has a picture (visual-plan.md); shots are rendered one by one to assets/shots/NNN.mp4 at the output size,
joined, then mixed with the VO and a synthesised bed (scripts/make_bed.py). Re-running re-renders only shots whose spec or
source changed. Usage: python3 projects/minimum-due/build/assemble.py [--height 720]
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import L, END
from boards import BOARDS

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
A = P / "assets"
BR, CM, PR, SM, BD = A / "broll", A / "commons", A / "proof", A / "sim", A / "boards"
CI = A / "commons_in"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BOARD_AT = {b["id"]: b["start"] for b in BOARDS}

# ---- shot list: (start, kind, spec). A shot runs until the next shot starts. ----
def S(t, kind, **kw):
    return dict(t=round(t, 2), kind=kind, **kw)

SHOTS = [
    S(0.0, "clip", src=BR / "pixabay_202987.mp4", ss=2.0, label="YOUR CARD BILL IS READY"),
    S(L("1.02")[0] - 0.3, "still", src=SM / "sim_bill.png", zoom=(1.0, 1.35), focus=(0.67, 0.42), label="TOTAL vs MINIMUM", tag="SIMULATION"),
    S(L("1.03")[0] - 0.2, "clip", src=BR / "pixabay_107264.mp4", ss=0.2, label="SALARY NOT IN YET", bright=True),
    S(L("1.03")[0] + 5.6, "clip", src=BR / "pixabay_1643.mp4", ss=2.0, label="MANY PEOPLE THINK THIS"),
    S(L("1.04")[0] - 0.2, "proof", src=PR / "icici_page.png", label="ICICI BANK'S OWN EXAMPLE", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(L("1.05")[0] - 0.2, "proof", src=PR / "icici_bill.png", label="BILL ₹69,688 · PAID ₹65,000", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(L("1.06")[0] - 0.2, "proof", src=PR / "icici_interest.png", label="INTEREST + GST = ₹4,317", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(BOARD_AT["b01_how"], "board", id="b01_how"),
    S(L("1.08")[0] - 0.2, "clip", src=BR / "pixabay_269529.mp4", ss=1.0, label=""),
    S(L("1.08")[0] + 2.0, "clip", src=BR / "pixabay_21117.mp4", ss=1.0, label=""),
    S(L("1.08")[0] + 4.2, "clip", src=BR / "pixabay_220283.mp4", ss=6.0, label=""),
    S(L("1.09")[0] - 0.2, "sting"),
    S(BOARD_AT["b02_numbers"], "board", id="b02_numbers"),
    S(L("1.16")[0] - 0.2, "clip", src=BR / "pixabay_209456.mp4", ss=1.0, label="SWIPE TODAY"),
    S(L("1.16")[0] + 4.6, "clip", src=BR / "coverr-close-up-of-man-using-iphone-15.mp4", ss=3.0, label="INTEREST FREE PERIOD = ZERO INTEREST", tag="RBI CARD DIRECTIONS 2025 · PARA 5"),
    S(L("1.17")[0] - 0.2, "clip", src=BR / "coverr-online-shopping-with-credit-card.mp4", ss=2.0, label="OCT 5 · PHONE · ₹10,000", tag="ILLUSTRATION · OUR EXAMPLE"),
    S(L("1.17")[0] + 3.6, "clip", src=BR / "pixabay_269529.mp4", ss=3.0, label="OCT 12 · FUNCTION · ₹15,000", tag="ILLUSTRATION · OUR EXAMPLE"),
    S(L("1.17")[0] + 6.6, "clip", src=BR / "pixabay_21117.mp4", ss=4.0, label="OCT 20 · GROCERIES · ₹5,000", tag="ILLUSTRATION · OUR EXAMPLE"),
    S(BOARD_AT["b03_calendar"], "board", id="b03_calendar"),
    S(L("1.22")[0] - 0.2, "proof", src=PR / "rbi_lost.png", label="IN THE RBI RULES", tag="RBI CARD DIRECTIONS 2025 · PARA 23(6)"),
    S(L("1.23")[0] - 0.2, "clip", src=BR / "pixabay_3176.mp4", ss=1.0, label="NOV 14 · PAID ONLY ₹1,500"),
    S(BOARD_AT["b04_rules"], "board", id="b04_rules"),
    S(L("1.30")[0] - 0.3, "sample", src=A / "sample/minimum-due-style-sample-v2.mp4", ss=0.0),   # 192.6–212.6
    S(L("1.33")[0] - 0.2, "proof", src=PR / "icici_table.png", label="SAME METHOD AS ICICI'S TABLE", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(L("1.34")[0] + 0.2, "proof", src=PR / "icici_interest.png", label="₹4,317 EXPLAINED", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(L("1.35")[0] - 0.2, "photo", src=CI / "petrol_pump_03_indian-oil-petrol-pump-at-chanchalguda-j.jpg", label="NOV 15 · PETROL ON THE SAME CARD", tag="PHOTO: WIKIMEDIA COMMONS, CC BY-SA 4.0"),
    S(L("1.35")[0] + 3.6, "clip", src=BR / "pixabay_84222.mp4", ss=1.0, label="NEW SPEND"),
    S(BOARD_AT["b05_newswipe"], "board", id="b05_newswipe"),
    S(L("2.01")[0] - 0.3, "clip", src=BR / "pixabay_61621.mp4", ss=2.0, label="MONTH AFTER MONTH"),
    S(BOARD_AT["b06_slow"], "board", id="b06_slow"),
    S(L("2.06")[0] - 0.2, "clip", src=BR / "pixabay_34499.mp4", ss=2.0, label="10+ YEARS TO CLEAR ₹30,000", tag="OUR CALCULATION"),
    S(L("2.07")[0] - 0.2, "still", src=SM / "sim_warning.png", zoom=(1.2, 1.7), focus=(0.5, 0.32), label="THE WARNING ON EVERY BILL", tag="RBI CARD DIRECTIONS 2025 · PARA 23(3)"),
    S(L("2.08")[0] - 0.2, "clip", src=BR / "pixabay_8698.mp4", ss=4.0, label="11.86 CRORE CREDIT CARDS", tag="RBI DATA | MAR 2026"),
    S(BOARD_AT["b07_crif"], "board", id="b07_crif"),
    S(L("2.10")[0] - 0.2, "photo", src=CM / "supreme_court_03_inside-the-supreme-court-of-india-11-jpg.jpg", alt=CM / "supreme_court_04_inside-the-supreme-court-of-india-12-jpg.jpg", label="SUPREME COURT · 20 DEC 2024", tag="30% CAP SET ASIDE · HSBC v. AWAZ | PHOTO: PINAKPANI, CC BY-SA 4.0"),
    S(BOARD_AT["b08_maths"], "board", id="b08_maths"),
    S(L("2.13")[0] - 0.2, "clip", src=BR / "coverr-friends-laughing-in-india-7824.mp4", ss=2.0, label="BORROW FROM A FRIEND"),
    S(BOARD_AT["b09_loop"], "board", id="b09_loop"),
    S(L("2.15")[0] - 0.2, "proof", src=PR / "news_rent.png", label="RENT BY CARD STOPPED", tag="BUSINESS STANDARD | 18 SEP 2025"),
    S(L("2.16")[0] - 0.2, "photo", src=CI / "atm_05_sbi-atm-andheri-west-jpg.jpg", label="CASH FROM CARD: FEE + INTEREST FROM DAY 1", tag="ICICI BANK | PHOTO: WIKIMEDIA COMMONS, CC BY-SA 2.0"),
    S(BOARD_AT["b10_postpone"], "board", id="b10_postpone"),
    S(L("2.19")[0] - 0.2, "switch", a=SM / "sim_autopay_min.png", b=SM / "sim_autopay_full.png", at=2.8, label="1 · AUTO PAY THE FULL BILL", tag="SIMULATION"),
    S(BOARD_AT["b11_steps12"], "board", id="b11_steps12"),
    S(L("2.23")[0] - 0.2, "clip", src=BR / "pixabay_3176.mp4", ss=4.0, label="3 · USE UPI / DEBIT CARD"),
    S(L("2.24")[0] - 0.2, "clip", src=BR / "coverr-a-man-takes-the-phone-out-of-pocket-and-answers-the-call.mp4", ss=1.0, label="4 · ASK YOUR BANK FOR EMI"),
    S(BOARD_AT["b12_emi"], "board", id="b12_emi"),
    S(L("2.26")[0] - 0.2, "still", src=SM / "sim_finance.png", zoom=(1.2, 1.7), focus=(0.5, 0.36), label="CHECK 'FINANCE CHARGES'", tag="SIMULATION · OUR EXAMPLE"),
    S(BOARD_AT["b13_recap"], "board", id="b13_recap"),
    S(L("2.29")[0] - 0.2, "clip", src=BR / "coverr-inside-of-a-car-driving-in-india-1526.mp4", ss=3.0, label="MINIMUM = EMERGENCY BRAKE ONLY"),
    S(L("2.30")[0] - 0.2, "clip", src=BR / "pixabay_9490.mp4", ss=1.0, label="FULL BILL OR MINIMUM? COMMENT"),
    S(BOARD_AT["b14_next"], "board", id="b14_next"),
    S(L("2.32")[0] - 0.2, "end"),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-800:]}")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%")


def overlays(W, H, label="", tag=""):
    k = H / 1080
    f = []
    if label:
        fs = int(40 * k)
        f.append(f"drawtext=fontfile={FONT}:text='{esc(label)}':x={int(84*k)}:y={int(950*k)}:fontsize={fs}:fontcolor=white:"
                 f"box=1:boxcolor=black@0.55:boxborderw={int(18*k)}")
    if tag:
        f.append(f"drawtext=fontfile={FONT}:text='{esc(tag)}':x=w-tw-{int(70*k)}:y=h-{int(64*k)}:fontsize={int(20*k)}:fontcolor=white@0.9:"
                 f"box=1:boxcolor=black@0.45:boxborderw={int(8*k)}")
    return f


def kb(W, H, dur, z0=1.0, z1=1.08, fx=0.5, fy=0.5):
    """Ken Burns on a big still: zoom z0->z1 around focus (fx, fy)."""
    return (f"scale={W*4}:-2,zoompan=z='{z0}+({z1}-{z0})*on/{max(1,int(dur*30))}':"
            f"x='iw*{fx}-iw/zoom/2':y='ih*{fy}-ih/zoom/2':d={max(1,int(dur*30))+2}:s={W}x{H}:fps=30")


def yellow_focus(png):
    """Centre of the highlighted (yellow) text in a proof screenshot, as fractions."""
    from PIL import Image
    im = Image.open(png).convert("RGB"); w, h = im.size; px = im.load()
    xs, ys = [], []
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            if r > 230 and g > 205 and b < 120:
                xs.append(x); ys.append(y)
    if not xs:
        return 0.5, 0.5
    return (sum(xs) / len(xs)) / w, (sum(ys) / len(ys)) / h


def render(shot, dur, out, W, H):
    k = shot["kind"]; lab, tag = shot.get("label", ""), shot.get("tag", "")
    enc = ["-an", "-c:v", "libx264", "-preset", "veryfast", "-b:v", "5M", "-maxrate", "6M", "-bufsize", "10M", "-pix_fmt", "yuv420p", "-r", "30"]
    if k in ("clip", "sample"):
        vf = [f"scale={int(W*1.08)}:{int(H*1.08)}:force_original_aspect_ratio=increase", f"crop={int(W*1.08)}:{int(H*1.08)}",
              f"scale=w='{int(W*1.08)}-{int(W*0.08)}*t/{dur:.2f}':h=-2:eval=frame", f"crop={W}:{H}", "fps=30"]
        if k == "sample":
            vf = [f"scale={W}:{H}", "fps=30"]
        if shot.get("bright"):
            vf.append("eq=brightness=0.08:gamma=1.35")
        if k == "clip":
            vf.append("vignette=PI/5")
        vf += overlays(W, H, lab, tag)
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(shot.get("ss", 0)), "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", str(shot["src"]),
             "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "board":
        off = shot["t"] - BOARD_AT[shot["id"]]
        vf = [f"scale={W}:{H}", "fps=30"]
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, off):.3f}", "-i", str(BD / (shot["id"] + ".mp4")), "-vf", ",".join(vf),
             "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k in ("still", "photo", "proof"):
        if k == "proof":
            fx, fy = yellow_focus(shot["src"]); z = (1.25, 1.7)
        elif k == "photo":
            fx, fy = 0.5, 0.5; z = (1.0, 1.12)
        else:
            fx, fy = shot.get("focus", (0.5, 0.5)); z = shot.get("zoom", (1.0, 1.2))
        vf = [kb(W, H, dur, z[0], z[1], fx, fy), "vignette=PI/6"] + overlays(W, H, lab, tag)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(shot["src"]), "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "switch":
        a, b = shot["a"], shot["b"]
        fc = (f"[0:v]{kb(W, H, dur, 1.3, 1.5, 0.5, 0.25)}[x];[1:v]{kb(W, H, dur, 1.3, 1.5, 0.5, 0.25)}[y];"
              f"[x][y]overlay=enable='gte(t,{shot['at']})'," + ",".join(overlays(W, H, lab, tag)))
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(a), "-loop", "1", "-i", str(b), "-filter_complex", fc,
             "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "sting":
        fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=brightness=-0.15[bg];"
              f"[1:v]scale={int(W*0.62)}:-2,format=rgba,fade=t=in:st=0:d=0.5:alpha=1[l];[bg][l]overlay=(W-w)/2:(H-h)/2")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", str(BR / "pixabay_200431.mp4"), "-loop", "1", "-i", str(ROOT / "assets/brand/banner.png"),
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "end":
        fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=8,eq=brightness=-0.25[bg];"
              f"[1:v]scale={int(W*0.5)}:-2[l];[bg][l]overlay=(W-w)/2:H*0.18,"
              f"drawtext=fontfile={FONT}:text='SUBSCRIBE · NEXT\\: CANT PAY EVEN THE MINIMUM?':x=(w-tw)/2:y=h*0.72:fontsize={int(H*0.035)}:fontcolor=white,"
              f"drawtext=fontfile={FONT}:text='Educational only · not financial advice':x=(w-tw)/2:y=h*0.80:fontsize={int(H*0.024)}:fontcolor=white@0.8")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-stream_loop", "-1", "-i", str(BR / "pixabay_200435.mp4"), "-loop", "1", "-i", str(ROOT / "assets/brand/banner.png"),
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [str(out)])
    else:
        sys.exit("unknown kind " + k)


def src_mtime(s):
    f = BD / (s["id"] + ".mp4") if s["kind"] == "board" else s.get("src")
    return f.stat().st_mtime if f and Path(f).exists() else 0


def split_long(shots, end):
    """A still never holds longer than ~4.5 s (charter: a cut every 2.5-4 s). Long proof/still/photo shots become
    wide -> mid -> tight framings of the same page (or the next photo in `alt`)."""
    out = []
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else end
        dur = nxt - s["t"]
        if s["kind"] not in ("proof", "still", "photo") or dur <= 5.0:
            out.append(s); continue
        n = min(3, int(dur // 3.5) or 1)
        if s["kind"] == "proof":
            fx, fy = yellow_focus(s["src"])
        else:
            fx, fy = s.get("focus", (0.5, 0.5))
        zooms = {"proof": [(1.0, 1.12), (1.25, 1.45), (1.6, 1.8)], "still": [(1.0, 1.15), (1.2, 1.4), (1.45, 1.7)],
                 "photo": [(1.0, 1.1), (1.12, 1.25), (1.0, 1.1)]}[s["kind"]]
        for j in range(n):
            part = dict(s, t=round(s["t"] + dur * j / n, 2), kind="still", zoom=zooms[j],
                        focus=(0.5 + (fx - 0.5) * (0.4 if j == 0 else 1.0), 0.5 + (fy - 0.5) * (0.4 if j == 0 else 1.0)))
            if s["kind"] == "photo":
                part["focus"] = (0.5, 0.5) if j == 0 else (0.42 + 0.16 * (j % 2), 0.5)
                if j == 1 and s.get("alt"):
                    part["src"] = s["alt"]
            out.append(part)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--skip-boards", action="store_true", help="render other shots while board renders are still running")
    a = ap.parse_args(); H = a.height; W = H * 16 // 9
    sd = A / f"shots{H}"; sd.mkdir(parents=True, exist_ok=True)
    shots = split_long(sorted(SHOTS, key=lambda s: s["t"]), END)
    lst = []
    for i, s in enumerate(shots):
        end = shots[i + 1]["t"] if i + 1 < len(shots) else END
        dur = round(end - s["t"], 3)
        key = hashlib.sha1(json.dumps([s, dur, W, H, src_mtime(s)], default=str, sort_keys=True).encode()).hexdigest()[:8]
        out = sd / f"{i:03d}_{s['kind']}_{key}.mp4"   # spec hash: an edited shot re-renders, the rest are reused
        if not out.exists():
            if a.skip_boards and s["kind"] == "board" and not (BD / (s["id"] + ".mp4")).exists():
                print(f"{i:03d} skip board {s['id']}"); continue
            render(s, dur, out, W, H)
        print(f"{i:03d} {s['t']:7.2f} {dur:6.2f} {s['kind']:6s} {s.get('label') or s.get('id') or ''}", flush=True)
        lst.append(f"file '{out}'")
    if a.skip_boards:
        return
    (sd / "list.txt").write_text("\n".join(lst) + "\n")
    video = A / f"video{H}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(sd / "list.txt"), "-c", "copy", str(video)])
    # logo bug top-right on every shot except sting and end card
    sting = next(s for s in shots if s["kind"] == "sting"); endc = shots[-1]
    i_s = shots.index(sting)
    bug_off = f"between(t,{sting['t']},{shots[i_s+1]['t']})+gte(t,{endc['t']})"
    # audio: VO (block1, 0.6 s gap, block2) + bed; bed ducks to silence 1.5 s before the core reveal (line 1.31)
    vo = A / "vo.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "voice/block1.mp3"), "-i", str(P / "voice/block2.mp3"), "-filter_complex",
         "[0:a]apad=pad_dur=0.6[a0];[a0][1:a]concat=n=2:v=0:a=1,aresample=48000", str(vo)])
    bed = A / "bed.wav"
    if not bed.exists():
        cues = {"duration": END + 1, "impacts": [L("1.31")[0] - 0.1, L("1.32")[0] + 9.5], "swells": [{"at": L("1.04")[0] - 2, "dur": 3}],
                "sections": [{"start": 0, "mood": "tense"}, {"start": L("2.18")[0], "mood": "calm"}]}
        (A / "bed_cues.json").write_text(json.dumps(cues))
        run([str(ROOT / ".venv/bin/python") if (ROOT / ".venv/bin/python").exists() else sys.executable, str(ROOT / "scripts/make_bed.py"), str(A / "bed_cues.json"), str(bed)])
    rv = L("1.31")[0]
    duck = f"volume='if(between(t,{rv-1.6},{rv-0.1}),0,1)':eval=frame"
    out = A / f"minimum-due-preview-{H}p.mp4"
    logo = A / f"logo_bug_{H}.png"   # pre-scaled once: the brand PNG is large, and rescaling it per frame made the encode crawl
    run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "assets/brand/logo_square.png"), "-vf",
         f"scale={int(H*0.09)}:-2,format=rgba,colorchannelmixer=aa=0.85", str(logo)])
    # audio: VO + ducked bed, then two-pass linear loudnorm to -14 LUFS (fast on its own; slow inside the video graph)
    mix = A / "mix_raw.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(vo), "-i", str(bed), "-filter_complex",
         f"[1:a]volume=-25dB,{duck}[b];[0:a][b]amix=inputs=2:duration=longest:normalize=0[a]", "-map", "[a]", "-t", f"{END:.2f}", str(mix)])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mix), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1:LRA=11:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
    # video: logo bug (30 fps still, bounded) over the joined shots
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(mix), "-loop", "1", "-framerate", "30", "-t", f"{END:.2f}", "-i", str(logo),
         "-filter_complex", "[2:v]format=rgba[lg];"
         f"[0:v][lg]overlay=W-w-{int(H*0.04)}:{int(H*0.04)}:enable='not({bug_off})'[v];[1:a]{ln},aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-b:v", "4M", "-maxrate", "5M", "-bufsize", "8M",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{END:.2f}", str(out)])
    print("wrote", out)


if __name__ == "__main__":
    main()
