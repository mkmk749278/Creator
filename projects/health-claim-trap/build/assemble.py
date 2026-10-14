#!/usr/bin/env python3
"""Assemble The Health Insurance Claim Rejection Trap (720p preview by default) from the shot list below.

The shot list IS the EDL (edl.md is generated from it): every VO line has a picture, cut on the breath, a change every
2.5-4 s; stills move (Ken Burns, proof push-ins); labels are 2-4-word lower thirds; tags carry the citation
([SOURCE | DATE]) or SIMULATION / ILLUSTRATIVE FOOTAGE / OUR CALCULATION. Shots render one by one to
assets/shots<H>/ (spec-hashed, so only changed shots re-render), are joined, then mixed with the VO (with the owner's
two 3 s silences), a synthesised bed (scripts/make_bed.py) and a logo bug.
Usage: python3 projects/health-claim-trap/build/assemble.py [--height 720] [--edl]
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from timing import L, sents, END, SEGMENTS, PAUSES
from boards import BOARDS

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
A = P / "assets"
BR, PR, SM, SC, CM = A / "broll", A / "proof", A / "sim", A / "scenes", A / "commons"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BOARD_AT = {b["id"]: b["start"] for b in BOARDS}
RENDER_V = 1
ILL = "ILLUSTRATIVE FOOTAGE"


def S(t, kind, **kw):
    return dict(t=round(t, 2), kind=kind, **kw)


def at(eid, word=None, k=0, frac=None):
    s = sents(eid)[k]
    if word is None and frac is None:
        return s["start"] - 0.2
    if frac is None:
        i = s["text"].lower().find(word.lower()); assert i >= 0, (eid, word)
        frac = i / max(1, len(s["text"]))
    return s["start"] + (s["end"] - s["start"]) * frac - 0.15


def scene_meta(sid):
    js = (ROOT / "video/healthclaim" / sid / "data.js").read_text()
    d = json.loads(js[js.index("=") + 1:].strip().rstrip(";"))
    return d["start"], d["start"] + d["duration"]


def clip(n, **kw):
    return dict(kind="clip", src=BR / n, **kw)


B = lambda n: BR / f"pixabay_{n}.mp4"
C = lambda n: BR / f"coverr-{n}.mp4"
SCN = lambda sid: S(scene_meta(sid)[0], "scene", id=sid)

SHOTS = [
    # ---- 1 The midnight bill ----
    S(0.0, "clip", src=B(74585), ss=1.0, label="IMAGINE THIS", tag=ILL),
    S(at("E001", "thousands"), "clip", src=B(3175), ss=5.0, label="29.5 LAKH CLAIMS REJECTED IN A YEAR", tag="IRDAI ANNUAL REPORT | 2024-25"),
    SCN("s00_receipts"),
    S(at("E003"), "clip", src=C("iv-in-hospital-room-5485"), ss=1.0, label="AN EMERGENCY", tag=ILL),
    S(at("E003", "admitted", k=1), "clip", src=B(229071), ss=2.0, label="ADMITTED", tag=ILL),
    S(at("E004"), "clip", src=B(26732), ss=2.0, label="9:00 PM · BILLING COUNTER", tag=ILL),
    S(at("E004", k=1), "clip", src=C("a-printer-at-work-in-the-office-5252"), ss=1.0, label="DISCHARGE PAPERS READY", tag=ILL),
    S(at("E004", k=2), "still", src=SM / "bill.png", zoom=(1.0, 1.9), label="BILL: ₹4,50,000", tag="SIMULATION"),
    SCN("s01_letter"),
    S(at("E007", "banks"), "clip", src=B(134434), ss=9.0, label="NIGHT · BANKS CLOSED"),
    S(at("E007", "break your"), "clip", src=B(202987), ss=2.0, label="BREAK THE FIXED DEPOSIT", tag=ILL),
    S(at("E007", "borrow"), "clip", src=B(204421), ss=3.0, label="BORROW FROM RELATIVES", tag=ILL),
    S(at("E007", "swipe"), "clip", src=C("transferring-card-details-5376"), ss=1.0, label="SWIPE A CREDIT CARD", tag=ILL),
    S(at("E008"), "clip", src=B(199442), ss=1.0, label="WHY DID I PAY ALL THESE YEARS?", tag=ILL),
    SCN("s01b_overstamp"),
    S(L("E010")[0] - 0.25, "sting"),
    S(at("E011"), "clip", src=B(134434), ss=4.0, label="NO SHOUTING · NO SELLING"),
    S(at("E011", "real", k=1), "proof", src=PR / "mc_cover.png", label="THE REAL IRDAI RULES", tag="IRDAI MASTER CIRCULAR | 29 MAY 2024"),
    S(at("E011", "who really", k=1), "clip", src=B(142528), ss=1.0, label="WHO REALLY SAYS NO", tag=ILL),
    S(at("E011", "step-by-step", k=1), "still", src=SM / "claim_form.png", zoom=(1.0, 1.3), label="HOW TO GET YOUR MONEY BACK", tag="SIMULATION"),
    S(at("E012"), "clip", src=B(34258), ss=2.0, label="CHAPTER 2 · WHO SAYS NO"),
    # ---- 2 Who really says no ----
    S(at("E013"), "clip", src=B(40353), ss=2.0, label="WHO SAYS NO AT THE DESK?", tag=ILL),
    SCN("s02_flow"),
    S(at("E014", "evaluating"), "clip", src=B(49809), ss=2.0, label="EVALUATING YOUR REPORTS?", tag=ILL),
    S(at("E014", k=1), "scene", id="s02_flow"),
    S(at("E017"), "proof", src=PR / "mc_para17.png", label="NO REJECTION WITHOUT COMMITTEE APPROVAL", tag="IRDAI MASTER CIRCULAR | PARA 17"),
    S(at("E017", "three excuses", k=1), "clip", src=B(87146), ss=2.0, label="3 EXCUSES YOU WILL OFTEN SEE"),
    S(at("E018"), "clip", src=B(349087), ss=2.0, label="1 · NON-DISCLOSURE"),
    S(at("E019"), "clip", src=B(49814), ss=1.0, label="A BROKEN LEG, OR DENGUE", tag=ILL),
    S(at("E019", "junior doctor", k=1), "clip", src=B(49813), ss=1.0, label="ONE LINE IN YOUR NOTES", tag=ILL),
    S(at("E019", k=2), "still", src=SM / "notes.png", zoom=(1.2, 2.2), label="PATIENT HAS MILD BLOOD PRESSURE", tag="SIMULATION"),
    S(at("E020"), "clip", src=B(142528), ss=4.0, label="THE REVIEWER", tag=ILL),
    S(at("E020", "opens", k=1), "still", src=SM / "proposal.png", zoom=(1.1, 2.0), label="YOUR PROPOSAL FORM · 2020", tag="SIMULATION"),
    S(at("E021"), "clip", src=B(49815), ss=2.0, label="BLOOD PRESSURE ≠ BROKEN LEG", tag=ILL),
    S(at("E021", k=2), "proof", src=PR / "mc_para13.png", label="AFTER 5 YEARS, THE RULE CHANGES", tag="IRDAI MASTER CIRCULAR | PARA 13"),
    S(at("E022"), "clip", src=B(5457), ss=1.0, label="2 · NOT MEDICALLY NECESSARY"),
    S(at("E022", k=2), "clip", src=B(143988), ss=0.5, label="COULD IT BE AN OPD VISIT?", tag=ILL),
    S(at("E023"), "clip", src=C("iv-in-hospital-room-5485"), ss=6.0, label="3 · ROOM RENT LIMIT"),
    S(BOARD_AT["b01_room"], "board", id="b01_room"),
    S(at("E025") + 2.6, "still", src=SM / "bill.png", zoom=(1.6, 1.9), focus=(0.5, 0.25), label="SURGERY · DOCTOR · NURSING", tag="SIMULATION"),
    S(at("E025") + 5.0, "board", id="b01_room"),
    S(at("E026"), "clip", src=B(212508), ss=2.0, label="FEELING HELPLESS", tag=ILL),
    S(at("E026", k=1), "clip", src=B(74585), ss=7.0, label="THE DOOR IS CLOSED?", tag=ILL),
    S(at("E027"), "still", src=SM / "letter_note.png", zoom=(1.2, 2.1), label="CASHLESS NO ≠ CLAIM NO", tag="AROGYA SANJEEVANI POLICY WORDING"),
    # ---- 3 The five year rule and the clock ----
    S(at("E028"), "proof", src=PR / "mc_ref.png", label="CHAPTER 3 · THE FIVE YEAR RULE", tag="IRDAI MASTER CIRCULAR | 29 MAY 2024"),
    S(at("E029"), "clip", src=C("hands-turning-pages-in-a-notebook-8881"), ss=8.0, label="THE MORATORIUM PERIOD"),
    SCN("s03_ring"),
    S(at("E032"), "proof", src=PR / "mc_para13.png", label="WHAT IT MEANS FOR YOU", tag="IRDAI MASTER CIRCULAR | PARA 13"),
    S(at("E034"), "clip", src=B(199442), ss=6.0, label="OLD HISTORY ≠ EXCUSE AFTER 5 YEARS", tag=ILL),
    S(at("E035"), "proof", src=PR / "mc_fraud.png", label="ONLY EXCEPTION: PROVEN FRAUD", tag="IRDAI MASTER CIRCULAR | PARA 13"),
    S(at("E035", k=2), "clip", src=B(144015), ss=1.0, label="NOT A FORGOTTEN FEVER", tag=ILL),
    S(at("E036"), "clip", src=C("hands-turning-pages-in-a-notebook-8881"), ss=1.0, label="LIMITS, EXCLUSIONS STILL APPLY"),
    S(at("E036", "port"), "proof", src=PR / "mc_port.png", label="PORT: YOUR YEARS MOVE WITH YOU", tag="IRDAI MASTER CIRCULAR | PARA 13 NOTE"),
    S(at("E036", "cancel", k=1), "clip", src=B(349087), ss=6.0, label="CANCEL = COUNT RESETS TO ZERO"),
    SCN("s03b_family"),
    SCN("s04_clock"),
    S(at("E040"), "proof", src=PR / "mc_wait.png", label="NO WAITING FOR DISCHARGE", tag="IRDAI MASTER CIRCULAR | PARA 16"),
    S(at("E040") + 3.6, "scene", id="s04_clock"),
    S(at("E040", "paid by", k=1) - 0.4, "proof", src=PR / "mc_para16b.png", label="INSURER PAYS FOR THE DELAY", tag="IRDAI MASTER CIRCULAR | PARA 16(b)"),
    S(at("E041"), "clip", src=B(26732), ss=6.0, label="ASK FOR THE 3-HOUR RULE"),
    # ---- 4 The four step plan and buyer rules ----
    S(at("E042"), "clip", src=B(40353), ss=8.0, label="CHAPTER 4 · THE FOUR STEP PLAN", tag=ILL),
    S(at("E043"), "clip", src=B(204421), ss=8.0, label="DON'T SHOUT · DON'T PANIC", tag=ILL, step=0),
    S(at("E044"), "clip", src=B(87146), ss=10.0, label="1 · COLLECT YOUR PAPERS", step=1),
    S(at("E045"), "clip", src=C("giving-cashier-a-credit-card-9719"), ss=1.0, label="PAY THE BILL IF YOU MUST", tag=ILL, step=1),
    S(at("E045", "copies", k=1), "still", src=SM / "claim_form.png", zoom=(1.3, 1.8), focus=(0.5, 0.55), label="SUMMARY · BILL · REPORTS · DENIAL LETTER", tag="SIMULATION", step=1),
    S(at("E046"), "clip", src=B(34258), ss=7.0, label="DOCTOR'S LETTER: WHY IT WAS NEEDED", tag=ILL, step=1),
    S(at("E047"), "still", src=SM / "claim_form.png", zoom=(1.6, 2.1), label="2 · CLAIM REIMBURSEMENT · 15–30 DAYS", tag="CHECK YOUR POLICY WORDING", step=2),
    S(at("E048"), "still", src=SM / "email.png", zoom=(1.0, 1.25), label="WRITE TO THE GRIEVANCE OFFICER", tag="SIMULATION", step=2),
    S(at("E048", k=1), "still", src=SM / "email.png", zoom=(1.5, 1.9), label="QUOTE THE 5-YEAR RULE (AFTER 5 YEARS)", tag="SIMULATION", step=2),
    S(at("E048", "fourteen", k=1) if "fourteen" in sents("E048")[1]["text"] else at("E048", k=2), "proof", src=PR / "bima_14days.png",
      label="REPLY WITHIN 14 DAYS", tag="IRDAI POLICYHOLDERS' INTERESTS MASTER CIRCULAR | 2024", step=2),
    S(at("E049"), "proof", src=PR / "bima_register.png", label="3 · BIMA BHAROSA", tag="BIMABHAROSA.IRDAI.GOV.IN", step=3),
    S(at("E050", "regulator", k=1), "clip", src=B(3145), ss=2.0, label="TRACKED BY IRDAI", step=3),
    S(at("E051"), "proof", src=PR / "cio_oneyear.png", label="4 · INSURANCE OMBUDSMAN", tag="CIOINS.CO.IN", step=4),
    S(at("E052"), "clip", src=B(212508), ss=6.0, label="NO COURT CASE · NO LAWYER NEEDED", step=4),
    S(at("E053"), "proof", src=PR / "cio_online.png", label="CIOINS.CO.IN", tag="COUNCIL FOR INSURANCE OMBUDSMEN", step=4),
    S(at("E054"), "clip", src=B(3145), ss=8.0, label="FREE · ONLINE · NO LAWYER NEEDED", tag="CIOINS.CO.IN", step=4),
    S(at("E055"), "proof", src=PR / "cio_h3.png", label="32,503 HEALTH COMPLAINTS · 2024-25", tag="CIO ANNUAL REPORT 2024-25 | STATEMENT H3", step=4),
    S(BOARD_AT["b02_ombud"], "board", id="b02_ombud", step=4),
    S(at("E056"), "proof", src=PR / "cio_50lakh.png", label="AWARD UP TO ₹50 LAKH · BINDING", tag="INSURANCE OMBUDSMAN RULES | RULE 17", step=4),
    S(at("E057"), "clip", src=B(1643), ss=8.0, label="BEFORE YOU BUY"),
    S(at("E058"), "still", src=SM / "proposal_declared.png", zoom=(1.0, 1.7), label="1 · DISCLOSE IN WRITING", tag="SIMULATION"),
    S(at("E059"), "clip", src=B(5457), ss=4.0, label="2 · NO ROOM RENT CAPPING"),
    S(BOARD_AT["b03_callback"], "board", id="b03_callback"),
    S(at("E060"), "clip", src=C("putting-medical-gloves-on-5311"), ss=1.0, label="3 · CONSUMABLES COVER"),
    S(at("E060", k=1, frac=0.35), "clip", src=B(65551), ss=2.0, label="5–15% OF A BILL · AS REPORTED", tag="OUTLOOK MONEY | BUSINESS STANDARD"),
    S(at("E060", k=2), "clip", src=B(143379), ss=2.0, label="CHECK THE PRICE AND THE LIMIT"),
    S(at("E061"), "clip", src=B(200431), ss=3.0, label="PEACE OF MIND"),
    S(at("E061", k=1), "scene", id="s03_ring", frm=scene_meta("s03_ring")[1] - 2.0, label="KNOW THE 5-YEAR RULE"),
    S(at("E061", k=2), "proof", src=PR / "cio_online.png", label="USE THE OMBUDSMAN"),
    S(at("E062"), "clip", src=B(1643), ss=3.0),
    S(at("E063"), "end"),
]


# ---- v2 (owner's visual-engine upgrade, 2026-10-14): programmatic scenes (build/make_engines.py) replace stock b-roll;
# real source pages run on the 3D document rig (d_*). Scenes carry their own labels and citation tags. ----
SC2 = lambda sid, t=None: S(scene_meta(sid)[0] if t is None else t, "scene", id=sid)
SHOTS_V2 = [
    SC2("e1_hospital"), SC2("e0_ledger"), SC2("e1_hospital", scene_meta("e0_ledger")[1]),
    SC2("s01_letter"), SC2("e2_shock"), SC2("e2_drain"), SC2("e3_scale"), SC2("e1b_overstamp"),
    S(L("E010")[0] - 0.25, "sting"),
    SC2("e4_pillars"), SC2("e5_funnel"), SC2("e6_lock"), SC2("d_para17"), SC2("e7_dossier"), SC2("e8_opd"), SC2("e9_slicer"), SC2("e10_wall"),
    SC2("e11_shield"), SC2("d_para13"), SC2("e12_history"), SC2("e13_burden"), SC2("e14_port"), SC2("e15_impact"),
    SC2("e16_stopwatch"), SC2("d_para16"), SC2("e16_stopwatch", scene_meta("d_para16")[1]), SC2("d_para16b"), SC2("e16_stopwatch", scene_meta("d_para16b")[1]),
    SC2("e17_warroom"), SC2("d_bima"), SC2("e17_warroom", scene_meta("d_bima")[1]), SC2("d_cio"), SC2("e17_warroom", scene_meta("d_cio")[1]),
    SC2("d_h3"), SC2("e17_warroom", scene_meta("d_h3")[1]), SC2("d_50l"), SC2("e17_warroom", scene_meta("d_50l")[1]),
    SC2("e18_checklist"), SC2("e19_cheatsheet"),
    S(at("E063"), "end"),
]
VERSION = "v2"


# ---------- rendering (adapted from projects/minimum-due/build/assemble.py) ----------
def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-800:]}")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%")


def rate(H, mbps_720, cap=30):
    b = min(cap, mbps_720 * (H / 720) ** 2)
    return ["-b:v", f"{b:.0f}M", "-maxrate", f"{b * 1.2:.0f}M", "-bufsize", f"{b * 2:.0f}M"]


def overlays(W, H, label="", tag="", step=None):
    k = H / 1080; f = []
    if label:
        f.append(f"drawbox=x={int(70*k)}:y={int(938*k)}:w={int(8*k)}:h={int(64*k)}:color=0x0284c7@1:t=fill")
        f.append(f"drawtext=fontfile={FONT}:text='{esc(label)}':x={int(96*k)}:y={int(950*k)}:fontsize={int(40*k)}:fontcolor=white:"
                 f"box=1:boxcolor=0x0f172a@0.72:boxborderw={int(16*k)}")
    if tag:
        f.append(f"drawtext=fontfile={FONT}:text='{esc(tag)}':x=w-tw-{int(70*k)}:y=h-{int(64*k)}:fontsize={int(20*k)}:fontcolor=white@0.9:"
                 f"box=1:boxcolor=0x0f172a@0.6:boxborderw={int(8*k)}")
    if step is not None:   # the four-step plan: a corner tracker, current step lit (amber), done steps cyan
        for i in range(4):
            col = "0xf59e0b@0.95" if i + 1 == step else ("0x0284c7@0.9" if i + 1 < step else "0x0f172a@0.7")
            x, y, s = int((70 + i * 78) * k), int(60 * k), int(64 * k)
            f.append(f"drawbox=x={x}:y={y}:w={s}:h={s}:color={col}:t=fill")
            f.append(f"drawtext=fontfile={FONT}:text='{i + 1}':x={x}+({s}-tw)/2:y={y}+({s}-th)/2:fontsize={int(36*k)}:fontcolor=white")
        f.append(f"drawtext=fontfile={FONT}:text='STEPS':x={int(388*k)}:y={int(80*k)}:fontsize={int(24*k)}:fontcolor=white@0.85")
    return f


def kb(W, H, dur, z0=1.0, z1=1.08, fx=0.5, fy=0.5, fx1=None):
    n = max(1, int(dur * 30)); fx1 = fx if fx1 is None else fx1
    ease = f"(0.5-0.5*cos(PI*on/{n}))"
    o = 4 if H <= 1080 else 2
    pre = f"scale={W*o}:{H*o}:force_original_aspect_ratio=increase,crop={W*o}:{H*o}"
    return (f"{pre},zoompan=z='{z0}+({z1}-{z0})*{ease}':x='iw*({fx}+({fx1}-{fx})*{ease})-iw/zoom/2':y='ih*{fy}-ih/zoom/2':"
            f"d={n+2}:s={W}x{H}:fps=30")


def focus_of(png):
    j = Path(png).with_suffix(".json")
    if j.exists():
        b = json.loads(j.read_text())
        if b:
            return (b["x0"] + b["x1"]) / 2, (b["y0"] + b["y1"]) / 2, b["x1"] - b["x0"]
    return 0.5, 0.5, 0.3


def render(shot, dur, out, W, H):
    k = shot["kind"]; ov = overlays(W, H, shot.get("label", ""), shot.get("tag", ""), shot.get("step"))
    enc = ["-frames:v", str(round(dur * 30)), "-an", "-c:v", "libx264", "-preset", "veryfast", *rate(H, 5), "-pix_fmt", "yuv420p", "-r", "30"]
    if k == "clip":
        pz = 1.3 if shot.get("punch") else 1.08
        px, py = shot.get("punch", (0.5, 0.5))
        vf = [f"scale={int(W*pz)}:{int(H*pz)}:force_original_aspect_ratio=increase",
              f"crop={int(W*1.08)}:{int(H*1.08)}:'(iw-ow)*{px}':'(ih-oh)*{py}'",
              f"scale=w='{int(W*1.08)}-{int(W*0.08)}*t/{dur:.2f}':h=-2:eval=frame", f"crop={W}:{H}", "fps=30",
              "eq=saturation=0.85:contrast=1.04", "vignette=PI/5"] + ov
        run(["ffmpeg", "-v", "error", "-y", "-ss", shot.get("ss", 0), "-stream_loop", "-1", "-i", shot["src"], "-vf", ",".join(vf),
             "-t", f"{dur:.3f}"] + enc + [out])
    elif k in ("board", "scene"):
        base = BOARD_AT[shot["id"]] if k == "board" else scene_meta(shot["id"])[0]
        off = shot.get("frm", shot["t"]) - base
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, off):.3f}", "-i", SC / (shot["id"] + ".mp4"),
             "-vf", ",".join([f"scale={W}:{H}", "fps=30", "tpad=stop_mode=clone:stop_duration=5"] + ov), "-t", f"{dur:.3f}"] + enc + [out])
    elif k in ("still", "proof"):
        fx, fy, fw = focus_of(shot["src"])
        fx, fy = shot.get("focus", (fx, fy))
        z = shot.get("zoom") or (1.0, 1.06)
        vf = [kb(W, H, dur, z[0], z[1], fx, fy, shot.get("pan_to")), "vignette=PI/6"] + ov
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", shot["src"], "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "sting":
        fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=brightness=-0.15[bg];"
              f"[1:v]scale={int(W*0.62)}:-2,format=rgba,fade=t=in:st=0:d=0.5:alpha=1[l];[bg][l]overlay=(W-w)/2:(H-h)/2")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", B(200431), "-loop", "1", "-i", ROOT / "assets/brand/banner.png",
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "end":
        fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=8,eq=brightness=-0.25[bg];"
              f"[1:v]scale={int(W*0.5)}:-2[l];[bg][l]overlay=(W-w)/2:H*0.18,"
              f"drawtext=fontfile={FONT}:text='SUBSCRIBE · SHARE WITH ONE FAMILY MEMBER':x=(w-tw)/2:y=h*0.70:fontsize={int(H*0.035)}:fontcolor=white,"
              f"drawtext=fontfile={FONT}:text='Educational only · not insurance advice · read your policy wording':x=(w-tw)/2:y=h*0.78:fontsize={int(H*0.024)}:fontcolor=white@0.85")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-stream_loop", "-1", "-i", B(200431), "-loop", "1", "-i", ROOT / "assets/brand/banner.png",
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [out])
    else:
        sys.exit("unknown kind " + k)


def proof_parts(s, dur):
    """A proof never sits as a small page: wide establish (whose page), then push in until the highlight reads on a
    phone, then (long holds) a slow pan along it."""
    fx, fy, fw = focus_of(s["src"])
    zt = max(1.8, min(3.2, 0.9 / max(0.18, fw)))
    if dur < 3.4:
        return [dict(s, kind="still", zoom=(zt * 0.75, zt), focus=(fx, fy))]
    a = min(2.0, max(1.3, dur * 0.28)); parts = [dict(s, kind="still", zoom=(1.0, 1.08), focus=(0.5 + (fx - 0.5) * 0.3, 0.5 + (fy - 0.5) * 0.3))]
    parts.append(dict(s, t=round(s["t"] + a, 2), kind="still", zoom=(zt * 0.8, zt), focus=(fx, fy)))
    if dur - a > 5.0:
        half = 0.5 / zt
        parts.append(dict(s, t=round(s["t"] + a + (dur - a) / 2, 2), kind="still", zoom=(zt, zt * 1.05),
                          focus=(max(half, fx - fw / 2 + half), fy), pan_to=min(1 - half, fx + fw / 2 - half)))
    return parts


def split_long(shots, end):
    """Cadence (charter: a change every 2.5-4 s, nothing static over ~4.5 s): proofs get establish -> push -> pan;
    any still or clip longer than ~5 s is cut into ~3.5 s framings (a camera punch to a different crop counts as a cut)."""
    out = []
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else end
        parts = proof_parts(s, nxt - s["t"]) if s["kind"] == "proof" else [s]
        for j, p in enumerate(parts):
            pend = parts[j + 1]["t"] if j + 1 < len(parts) else nxt
            dur = pend - p["t"]
            if p["kind"] not in ("still", "clip") or dur <= 5.0:
                out.append(p); continue
            n = max(2, round(dur / 3.6))
            for m in range(n):
                q = dict(p, t=round(p["t"] + dur * m / n, 2))
                if p["kind"] == "clip":
                    q["ss"] = p.get("ss", 0) + m * (dur / n + 1.2)
                    if m % 2: q["punch"] = (0.35 + 0.3 * (m % 3 == 1), 0.42)
                else:
                    z0, z1 = p.get("zoom") or (1.0, 1.1)
                    a, b = z0 + (z1 - z0) * m / n, z0 + (z1 - z0) * (m + 1) / n
                    q["zoom"] = (a * (1.04 if m % 2 else 1.0), b * (1.04 if m % 2 else 1.0))
                out.append(q)
    return out


def src_mtime(s):
    f = SC / (s["id"] + ".mp4") if s["kind"] in ("board", "scene") else s.get("src")
    return f.stat().st_mtime if f and Path(f).exists() else 0


def shot_list():
    return split_long(sorted(SHOTS_V2 if VERSION == "v2" else SHOTS, key=lambda s: s["t"]), END)


def write_edl(shots):
    """edl.csv + edl.md from the shot list (phone-readable)."""
    import csv
    rows = []
    for i, s in enumerate(shots):
        end = shots[i + 1]["t"] if i + 1 < len(shots) else END
        src = s.get("id") or (Path(s["src"]).name if s.get("src") else s["kind"])
        rows.append(dict(n=i, start=f"{s['t']:.2f}", end=f"{end:.2f}", dur=f"{end - s['t']:.2f}", kind=s["kind"], asset=src,
                         motion={"clip": "slow push 1.08", "still": f"Ken Burns {s.get('zoom')}", "board": "marker writes", "scene": "animated",
                                 "sting": "logo sting", "end": "end card"}.get(s["kind"], ""),
                         label=s.get("label", ""), tag=s.get("tag", ""), step=s.get("step", "")))
    with open(P / "edl.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    md = ["# EDL: The Health Insurance Claim Rejection Trap", "", "Generated from `build/assemble.py` (the shot list is the EDL). Times are film seconds; "
          "sound cues are in `build/assemble.py` (bed, impacts, the 1.5 s music silence before E033, the two 3 s VO pauses).", "",
          "| # | Start | Dur | Kind | Asset | Lower third | Tag |", "|---|---|---|---|---|---|---|"]
    md += [f"| {r['n']} | {r['start']} | {r['dur']} | {r['kind']} | {r['asset']} | {r['label']} | {r['tag']} |" for r in rows]
    durs = [float(r["dur"]) for r in rows]
    md += ["", f"{len(rows)} shots, median {sorted(durs)[len(durs)//2]:.2f} s, longest {max(durs):.2f} s."]
    (P / "edl.md").write_text("\n".join(md) + "\n")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--height", type=int, default=720); ap.add_argument("--edl", action="store_true")
    a = ap.parse_args(); H = a.height; W = H * 16 // 9
    shots = shot_list()
    write_edl(shots)
    if a.edl:
        return
    sd = A / f"shots{H}"; sd.mkdir(parents=True, exist_ok=True)
    lst = []
    for i, s in enumerate(shots):
        end = shots[i + 1]["t"] if i + 1 < len(shots) else END
        dur = (round(end * 30) - round(s["t"] * 30)) / 30
        key = hashlib.sha1(json.dumps([s, dur, W, H, src_mtime(s), RENDER_V], default=str, sort_keys=True).encode()).hexdigest()[:8]
        out = sd / f"{i:03d}_{s['kind']}_{key}.mp4"
        if not out.exists():
            render(s, dur, out, W, H)
        print(f"{i:03d} {s['t']:7.2f} {dur:6.2f} {s['kind']:6s} {s.get('label') or s.get('id') or ''}", flush=True)
        lst.append(f"file '{out}'")
    (sd / "list.txt").write_text("\n".join(lst) + "\n")
    video = A / f"video{H}_{VERSION}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", sd / "list.txt", "-c", "copy", video])
    # ---- audio: VO segments at their film times (the owner's two 3 s silences are the gaps) ----
    vo = A / "vo.wav"
    inputs, fl = [], []
    for j, g in enumerate(SEGMENTS):
        inputs += ["-ss", f"{g['ss']:.3f}", "-to", f"{g['to']:.3f}", "-i", g["src"]]
        fl.append(f"[{j}:a]aresample=48000,adelay={int(g['at'] * 1000)}:all=1[a{j}]")
    fl.append("".join(f"[a{j}]" for j in range(len(SEGMENTS))) + f"amix=inputs={len(SEGMENTS)}:normalize=0:duration=longest[o]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", "[o]", "-t", f"{END:.2f}", vo])
    bed = A / "bed.wav"
    reveal = L("E033")[0]
    cues = {"duration": END + 1,
            "impacts": [round(scene_meta("s01_letter")[0] + 6.6, 2), round(scene_meta("e1b_overstamp")[0] + 8.7, 2), round(reveal, 2)],
            "swells": [{"at": L("E009")[0] - 2, "dur": 3}],
            "sections": [{"start": 0, "mood": "tense"}, {"start": L("E042")[0], "mood": "neutral"}, {"start": L("E057")[0], "mood": "calm"}]}
    cj = A / "bed_cues.json"
    if not bed.exists() or not cj.exists() or json.loads(cj.read_text()) != cues:
        cj.write_text(json.dumps(cues))
        py = ROOT / ".venv/bin/python"
        run([py if py.exists() else sys.executable, ROOT / "scripts/make_bed.py", cj, bed])
    # music: -25 dB under speech; 0 for 1.5 s before the core reveal (E033, the moratorium clause)
    duck = f"volume='if(between(t,{reveal - 1.6},{reveal - 0.05}),0,1)':eval=frame"
    mix = A / "mix_raw.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", bed, "-filter_complex",
         f"[1:a]volume=-25dB,{duck}[b];[0:a][b]amix=inputs=2:duration=longest:normalize=0[a]", "-map", "[a]", "-t", f"{END:.2f}", mix])

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
    sting = next(s for s in shots if s["kind"] == "sting"); i_s = shots.index(sting); endc = shots[-1]
    bug_off = f"between(t,{sting['t']},{shots[i_s+1]['t']})+gte(t,{endc['t']})"
    logo = A / f"logo_bug_{H}.png"
    run(["ffmpeg", "-v", "error", "-y", "-i", ROOT / "assets/brand/logo_square.png", "-vf", f"scale={int(H*0.09)}:-2,format=rgba,colorchannelmixer=aa=0.85", logo])
    out = A / f"health-claim-trap-preview-{VERSION}-{H}p.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", mix, "-loop", "1", "-framerate", "30", "-t", f"{END:.2f}", "-i", logo,
         "-filter_complex", "[2:v]format=rgba[lg];"
         f"[0:v][lg]overlay=W-w-{int(H*0.04)}:{int(H*0.04)}:enable='not({bug_off})'[v];[1:a]{ln},aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", *rate(H, 4, cap=20),
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{END:.2f}", out])
    print("wrote", out)


if __name__ == "__main__":
    main()
