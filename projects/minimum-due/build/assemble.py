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
ERASE = {b["id"]: [st["at"] for st in b["steps"] if st.get("erase")] for b in BOARDS}   # board erase times (film s)
CN = A / "commons_new"; BN = A / "broll_new"
RENDER_V = 3   # bump when render() changes, so cached shots re-render


def cutin(board, t, dur, shot):
    """A real cutaway inside a long board at film time t (the board keeps writing underneath; we return `dur` s later)."""
    return [dict(shot, t=round(t, 2)), S(t + dur, "board", id=board)]


def cutaway(board, n, shot, back=2.6):
    """Cut away from a board just before its n-th erase (the board is blank there anyway) and come back `back` s
    later, when the next line is being written. Keeps boards from holding 15-40 s without a cut."""
    t = ERASE[board][n] - 0.2
    return [dict(shot, t=round(t, 2)), S(t + back, "board", id=board)]

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
    # 1.08 "the full maths behind that small number": flash-forwards of the maths itself
    S(L("1.08")[0] - 0.2, "board", id="b04_rules", frm=L("1.26")[0] + 5.0, label="COMING UP: THE FULL MATHS"),
    S(L("1.08")[0] + 2.0, "board", id="b06_slow", frm=L("2.03")[0] + 2.7, label="COMING UP: THE FULL MATHS"),
    S(L("1.08")[0] + 4.2, "clip", src=BR / "coverr-close-up-of-man-using-iphone-15.mp4", ss=8.0, label="IN VERY SIMPLE WORDS"),
    S(L("1.09")[0] - 0.2, "sting"),
    S(BOARD_AT["b02_numbers"], "board", id="b02_numbers"),
    *cutin("b02_numbers", L("1.11")[0] - 0.1, 2.6, S(0, "still", src=SM / "sim_bill.png", zoom=(1.45, 1.65), focus=(0.5, 0.5), label="MINIMUM AMOUNT DUE", tag="SIMULATION")),
    *cutaway("b02_numbers", 1, S(0, "clip", src=BR / "coverr-secure-online-payment-process.mp4", ss=2.0, label="PAID THE MINIMUM ON TIME"), back=2.9),
    S(L("1.16")[0] - 0.2, "clip", src=BR / "pixabay_209456.mp4", ss=1.0, label="SWIPE TODAY"),
    S(L("1.16")[0] + 4.6, "clip", src=BR / "coverr-close-up-of-man-using-iphone-15.mp4", ss=3.0, label="INTEREST FREE PERIOD = ZERO INTEREST", tag="RBI CARD DIRECTIONS 2025 · PARA 5"),
    S(L("1.17")[0] - 0.2, "clip", src=BR / "coverr-online-shopping-with-credit-card.mp4", ss=2.0, label="OCT 5 · PHONE · ₹10,000", tag="ILLUSTRATION · OUR EXAMPLE"),
    S(L("1.17")[0] + 3.6, "clip", src=BR / "pixabay_269529.mp4", ss=3.0, label="OCT 12 · FUNCTION · ₹15,000", tag="ILLUSTRATION · OUR EXAMPLE"),
    S(L("1.17")[0] + 6.6, "photo", src=CN / "provision_13_provisions-shop-simsa-manali-himachal-ma.jpg", label="OCT 20 · GROCERIES · ₹5,000", tag="ILLUSTRATION · PHOTO: TIMOTHY A. GONSALVES, CC BY-SA 4.0"),
    S(BOARD_AT["b03_calendar"], "board", id="b03_calendar"),
    *cutaway("b03_calendar", 0, S(0, "still", src=SM / "sim_bill.png", zoom=(1.5, 1.7), focus=(0.5, 0.66), label="ONE CONDITION", tag="SIMULATION"), back=1.9),
    S(L("1.22")[0] - 0.2, "proof", src=PR / "rbi_lost.png", label="IN THE RBI RULES", tag="RBI CARD DIRECTIONS 2025 · PARA 23(6)"),
    S(L("1.23")[0] - 0.2, "clip", src=BR / "pixabay_3176.mp4", ss=1.0, label="NOV 14 · PAID ONLY ₹1,500"),
    S(BOARD_AT["b04_rules"], "board", id="b04_rules"),
    *cutin("b04_rules", L("1.25")[0] - 0.1, 2.6, S(0, "clip", src=BR / "pixabay_269529.mp4", ss=4.0, label="INTEREST FROM THE DAY OF THE SWIPE")),
    *cutaway("b04_rules", 0, S(0, "proof", src=PR / "icici_rate.png", label="ICICI: 3.75% A MONTH", tag="ICICI BANK · INTEREST RATES PAGE | 2025"), back=2.8),
    *cutaway("b04_rules", 1, S(0, "clip", src=BR / "pixabay_3176.mp4", ss=2.0, label="RULE 2: INTEREST EVEN ON WHAT YOU PAID"), back=2.2),
    # 1.30-1.32: the style sample's real clips, with its two board beats re-rendered as b15/b16
    S(L("1.30")[0] - 0.3, "sample", src=A / "sample/minimum-due-style-sample-v2.mp4", ss=0.0),   # its own label is baked in
    S(BOARD_AT["b15_paid"], "board", id="b15_paid"),
    # the sample's falling-notes beat (9.6-12 s) read as "money pouring in" under "no new spending": real hands instead
    S(L("1.30")[0] - 0.3 + 9.6, "clip", src=BR / "pixabay_142641.mp4", ss=1.0, label="NOT ONE NEW RUPEE SPENT"),
    S(BOARD_AT["b16_wentup"], "board", id="b16_wentup"),
    S(L("1.30")[0] - 0.3 + 17.0, "sample", src=A / "sample/minimum-due-style-sample-v2.mp4", ss=17.0),
    S(L("1.33")[0] - 0.2, "proof", src=PR / "icici_table.png", label="SAME METHOD AS ICICI'S TABLE", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(L("1.34")[0] + 0.2, "proof", src=PR / "icici_interest.png", label="₹4,317 EXPLAINED", tag="ICICI BANK · INTEREST RATES PAGE | 2025"),
    S(L("1.35")[0] - 0.2, "photo", src=CI / "petrol_pump_03_indian-oil-petrol-pump-at-chanchalguda-j.jpg", label="NOV 15 · PETROL ON THE SAME CARD", tag="PHOTO: WIKIMEDIA COMMONS, CC BY-SA 4.0"),
    S(L("1.35")[0] + 3.6, "clip", src=BR / "pixabay_84222.mp4", ss=1.0, label="NEW SPEND"),
    S(BOARD_AT["b05_newswipe"], "board", id="b05_newswipe"),
    *cutaway("b05_newswipe", 0, S(0, "clip", src=BR / "coverr-online-shopping-with-credit-card.mp4", ss=8.0, label="YOUR CARD IS NOT FREE ANY MORE"), back=2.4),
    S(L("2.01")[0] - 0.3, "clip", src=BR / "pixabay_61621.mp4", ss=2.0, label="MONTH AFTER MONTH"),
    S(BOARD_AT["b06_slow"], "board", id="b06_slow"),
    *cutaway("b06_slow", 1, S(0, "keyed", src=BR / "pixabay_370535.mp4", ss=0.5, label="AFTER ONE YEAR", tag="ILLUSTRATION"), back=2.9),
    S(L("2.06")[0] - 0.2, "clip", src=BR / "pixabay_34499.mp4", ss=2.0, label="10+ YEARS TO CLEAR ₹30,000", tag="OUR CALCULATION"),
    S(L("2.07")[0] - 0.2, "still", src=SM / "sim_warning.png", zoom=(1.2, 1.7), focus=(0.5, 0.32), label="THE WARNING ON EVERY BILL", tag="RBI CARD DIRECTIONS 2025 · PARA 23(3)"),
    S(L("2.08")[0] - 0.2, "clip", src=BR / "pixabay_8698.mp4", ss=4.0, label="11.86 CRORE CREDIT CARDS", tag="RBI DATA | MAR 2026"),
    S(BOARD_AT["b07_crif"], "board", id="b07_crif"),
    S(L("2.10")[0] - 0.2, "photo", src=CM / "supreme_court_03_inside-the-supreme-court-of-india-11-jpg.jpg", alt=CM / "supreme_court_04_inside-the-supreme-court-of-india-12-jpg.jpg", label="SUPREME COURT · 20 DEC 2024", tag="30% CAP SET ASIDE · HSBC v. AWAZ | PHOTO: PINAKPANI, CC BY-SA 4.0"),
    S(BOARD_AT["b08_maths"], "board", id="b08_maths"),
    S(L("2.13")[0] - 0.2, "clip", src=BR / "coverr-friends-laughing-in-india-7824.mp4", ss=2.0, label="BORROW FROM A FRIEND"),
    S(BOARD_AT["b09_loop"], "board", id="b09_loop"),
    S(L("2.15")[0] - 0.2, "proof", src=PR / "news_rent.png", label="RENT BY CARD STOPPED", tag="BUSINESS STANDARD | 18 SEP 2025"),
    S(L("2.16")[0] - 0.2, "photo", src=CN / "bank_05_hdfc-bank-atm-jpg.jpg", label="CASH FROM CARD: FEE + INTEREST FROM DAY 1", tag="ICICI BANK | PHOTO: JANE MEJDAHL, CC BY-SA 2.0"),
    S(BOARD_AT["b10_postpone"], "board", id="b10_postpone"),
    S(L("2.19")[0] - 0.2, "switch", a=SM / "sim_autopay_min.png", b=SM / "sim_autopay_full.png", at=2.8, label="1 · AUTO PAY THE FULL BILL", tag="SIMULATION"),
    S(BOARD_AT["b11_steps12"], "board", id="b11_steps12"),
    *cutaway("b11_steps12", 0, S(0, "clip", src=BN / "pixabay_38084.mp4", ss=1.0, label="PAY MORE = LESS INTEREST"), back=2.8),
    S(L("2.23")[0] - 0.2, "still", src=CN / "bhim_14_bhim-upi-id-to-accept-entrance-fee-at-sh.jpg", zoom=(1.0, 1.15), focus=(0.5, 0.3), label="3 · USE UPI / DEBIT CARD", tag="PHOTO: SUYASH DWIVEDI, CC BY-SA 4.0"),
    S(L("2.24")[0] - 0.2, "photo", src=CN / "bank_01_an-hdfc-bank-branch-jpg.jpg", focus=(0.5, 0.42), label="4 · ASK YOUR BANK FOR EMI", tag="PHOTO: JAYANTA, CC BY-SA 3.0"),
    S(BOARD_AT["b12_emi"], "board", id="b12_emi"),
    *cutaway("b12_emi", 0, S(0, "keyed", src=BR / "pixabay_370535.mp4", ss=4.0, label="5 · LAST DATE AFTER SALARY", tag="ILLUSTRATION"), back=2.4),
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


def kb(W, H, dur, z0=1.0, z1=1.08, fx=0.5, fy=0.5, fx1=None, aspect=None):
    """Ken Burns on a big still: zoom z0->z1 around focus (fx, fy), optionally panning the focus x from fx to fx1.
    zoompan clamps x/y inside the picture, so a focus near an edge just stops at the edge."""
    n = max(1, int(dur * 30)); fx1 = fx if fx1 is None else fx1
    cfx, cfx1, cfy = fx, fx1, fy   # 16:9 sources (screenshots, sims): crop is a no-op, focus unchanged
    if aspect and abs(aspect - 16 / 9) > 0.02:   # re-express the focus inside the cropped 16:9 window
        if aspect > 16 / 9:   # wider: crop sides
            vis = (16 / 9) / aspect; left = max(0, min(1 - vis, fx - vis / 2))
            cfx, cfx1 = (fx - left) / vis, (fx1 - left) / vis; cfy = fy
        else:                 # taller: crop top/bottom
            vis = aspect / (16 / 9); top = max(0, min(1 - vis, fy - vis / 2))
            cfy = (fy - top) / vis
    ease = f"(0.5-0.5*cos(PI*on/{n}))"   # ease in-out: no jolt at the cut
    # cover-crop to 16:9 first (around the focus), else zoompan squashes 4:3 and portrait photos into the frame
    pre = (f"scale={W*4}:{H*4}:force_original_aspect_ratio=increase,"
           f"crop={W*4}:{H*4}:'max(0,min(iw-ow,iw*{fx}-ow/2))':'max(0,min(ih-oh,ih*{fy}-oh/2))'")
    return (f"{pre},zoompan=z='{z0}+({z1}-{z0})*{ease}':"
            f"x='iw*({cfx}+({cfx1}-{cfx})*{ease})-iw/zoom/2':y='ih*{cfy}-ih/zoom/2':d={n+2}:s={W}x{H}:fps=30")


def proof_box(png):
    """Highlight box (x0, y0, x1, y1 as fractions) saved by proof_shots.js; falls back to the yellow pixels."""
    j = Path(png).with_suffix(".json")
    if j.exists():
        b = json.loads(j.read_text())
        if b:
            return b["x0"], b["y0"], b["x1"], b["y1"]
    fx, fy = yellow_focus(png)
    return fx - 0.05, fy - 0.02, fx + 0.05, fy + 0.02


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
    enc = ["-frames:v", str(round(dur * 30)), "-an", "-c:v", "libx264", "-preset", "veryfast", "-b:v", "5M", "-maxrate", "6M", "-bufsize", "10M", "-pix_fmt", "yuv420p", "-r", "30"]
    if k in ("clip", "sample"):
        vf = [f"scale={int(W*1.08)}:{int(H*1.08)}:force_original_aspect_ratio=increase", f"crop={int(W*1.08)}:{int(H*1.08)}",
              f"scale=w='{int(W*1.08)}-{int(W*0.08)}*t/{dur:.2f}':h=-2:eval=frame", f"crop={W}:{H}", "fps=30"]
        if k == "sample" or shot.get("flat"):
            vf = [f"scale={W}:{H}", "fps=30"]
        if shot.get("bright"):
            vf.append("eq=brightness=0.08:gamma=1.35")
        if k == "clip" and not shot.get("flat"):
            vf.append("vignette=PI/5")
        vf += overlays(W, H, lab, tag)
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(shot.get("ss", 0)), "-t", f"{dur:.3f}", "-stream_loop", "-1", "-i", str(shot["src"]),
             "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "board":
        off = shot.get("frm", shot["t"]) - BOARD_AT[shot["id"]]
        vf = [f"scale={W}:{H}", "fps=30"] + overlays(W, H, lab, tag)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, off):.3f}", "-i", str(BD / (shot["id"] + ".mp4")), "-vf", ",".join(vf),
             "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k in ("still", "photo", "proof"):
        if k == "proof":
            fx, fy = yellow_focus(shot["src"]); z = (1.25, 1.7)
        elif k == "photo":
            fx, fy = shot.get("focus", (0.5, 0.5)); z = (1.0, 1.12)
        else:
            fx, fy = shot.get("focus", (0.5, 0.5)); z = shot.get("zoom", (1.0, 1.2))
        from PIL import Image
        iw, ih = Image.open(shot["src"]).size
        vf = [kb(W, H, dur, z[0], z[1], fx, fy, shot.get("pan_to"), iw / ih), "vignette=PI/6"] + overlays(W, H, lab, tag)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(shot["src"]), "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [str(out)])
    elif k == "keyed":
        # green-screen graphic (calendar) keyed over a soft, blurred desk so it never sits on flat colour
        fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=12,eq=brightness=-0.12[bg];"
              f"[1:v]scale={W}:{H},chromakey=0x00ff00:0.22:0.08,scale=w='{W}*(1+0.06*t/{dur:.2f})':h=-2:eval=frame[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,fps=30," + ",".join(overlays(W, H, lab, tag) + ["vignette=PI/6"]))
        run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-stream_loop", "-1", "-i", str(BR / "pixabay_202987.mp4"),
             "-ss", str(shot.get("ss", 0)), "-i", str(shot["src"]), "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [str(out)])
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


def proof_parts(s, dur):
    """A proof never sits as a small page: 1) wide establish (whose page is this), 2) push in until the highlighted line
    is readable on a phone (text >= ~20 px at 720p), 3) for long holds, a slow pan along the highlighted row."""
    x0, y0, x1, y1 = proof_box(s["src"])
    cx, cy = s.get("fx", (x0 + x1) / 2), (y0 + y1) / 2
    zt = max(1.6, min(2.5, 1 / max(0.40, (x1 - x0) * 1.4)))
    if dur < 3.6:   # a short cutaway has no time to establish: push straight into the highlight
        return [dict(s, kind="still", zoom=(zt * 0.72, zt), focus=(cx, cy))]
    a = min(2.2, max(1.4, dur * 0.3)); rest = dur - a
    parts = [dict(s, t=s["t"], kind="still", zoom=(1.0, 1.06), focus=(0.5 + (cx - 0.5) * 0.3, 0.5 + (cy - 0.5) * 0.3))]
    if rest <= 4.8:
        parts.append(dict(s, t=round(s["t"] + a, 2), kind="still", zoom=(zt * 0.86, zt), focus=(cx, cy)))
    else:
        parts.append(dict(s, t=round(s["t"] + a, 2), kind="still", zoom=(zt * 0.86, zt), focus=(cx, cy)))
        half = 0.5 / zt   # half the visible width at zoom zt
        p0, p1 = (x0 + half, x1 - half) if x1 - x0 > 2 * half else (cx - 0.12, cx + 0.04)
        parts.append(dict(s, t=round(s["t"] + a + rest / 2, 2), kind="still", zoom=(zt, zt * 1.04), focus=(p0, cy), pan_to=p1))
    return parts


def split_long(shots, end):
    """A still never holds longer than ~4.5 s (charter: a cut every 2.5-4 s). Proofs get establish -> push -> pan
    (proof_parts); other long stills/photos become wide -> mid -> tight framings (or the next photo in `alt`)."""
    out = []
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else end
        dur = nxt - s["t"]
        if s["kind"] == "proof":
            out += proof_parts(s, dur); continue
        if s["kind"] not in ("still", "photo") or dur <= 5.0:
            out.append(s); continue
        n = min(3, int(dur // 3.5) or 1)
        fx, fy = s.get("focus", (0.5, 0.5))
        zooms = {"still": [(1.0, 1.15), (1.2, 1.4), (1.45, 1.7)], "photo": [(1.0, 1.1), (1.12, 1.25), (1.0, 1.1)]}[s["kind"]]
        for j in range(n):
            part = dict(s, t=round(s["t"] + dur * j / n, 2), kind="still", zoom=zooms[j],
                        focus=(0.5 + (fx - 0.5) * (0.4 if j == 0 else 1.0), 0.5 + (fy - 0.5) * (0.4 if j == 0 else 1.0)))
            if s["kind"] == "photo":
                part["focus"] = (fx, fy) if j == 0 else (0.42 + 0.16 * (j % 2), min(fy, 0.4))
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
        dur = (round(end * 30) - round(s["t"] * 30)) / 30   # frame-exact: no drift against the VO over 80+ cuts
        key = hashlib.sha1(json.dumps([s, dur, W, H, src_mtime(s), RENDER_V], default=str, sort_keys=True).encode()).hexdigest()[:8]
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
    # loudness: measure, apply the exact gain to -14 LUFS, then a brick-wall limiter at -1.5 dBFS for the few VO peaks.
    # (loudnorm linear=true silently undershoots, -14.8 LUFS on v1, when the gain would push true peak over the ceiling.)
    def integrated(f, af="anull"):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af", f"{af},ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return float(r[r.rindex("I:"):].split()[1])
    gain = -14.0 - integrated(mix)
    ln = f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false"
    for _ in range(2):   # the limiter shaves a little loudness: top up once or twice
        got = integrated(mix, ln)
        if abs(got + 14.0) < 0.25:
            break
        gain += -14.0 - got; ln = f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false"
    # video: logo bug (30 fps still, bounded) over the joined shots
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(mix), "-loop", "1", "-framerate", "30", "-t", f"{END:.2f}", "-i", str(logo),
         "-filter_complex", "[2:v]format=rgba[lg];"
         f"[0:v][lg]overlay=W-w-{int(H*0.04)}:{int(H*0.04)}:enable='not({bug_off})'[v];[1:a]{ln},aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-b:v", "4M", "-maxrate", "5M", "-bufsize", "8M",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{END:.2f}", str(out)])
    print("wrote", out)


if __name__ == "__main__":
    main()
