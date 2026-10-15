#!/usr/bin/env python3
"""Assemble The Insurance Ombudsman (Episode 02) from the shot list below (the shot list IS the EDL; edl.md is generated).

Every sentence of the Akash VO (timing.csv, film seconds) has a picture that shows what it says; a change every 2.5-4 s
(split_long cuts long holds into new framings); labels are 2-4-word lower thirds; corner tags carry the citation or
SIMULATION / ILLUSTRATIVE FOOTAGE / OUR CALCULATION / FROM EPISODE 1. Animated scenes come from the parallel sessions
(Drive English/insurance-ombudsman/scenes/<A|B|C>/ -> assets/scenes/<scene>_<Oid>.mp4, each = its VO window + 0.25 s
handles); a missing scene renders as a labelled placeholder so timing can be reviewed early.
Render functions adapted from projects/health-claim-trap/build/assemble.py.
Usage: python3 build/assemble.py [--height 1080] [--edl]
"""
import argparse, csv, hashlib, json, subprocess, sys
from pathlib import Path

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
A = P / "assets"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ILL, SIM, CALC, EP1 = "ILLUSTRATIVE FOOTAGE", "SIMULATION", "OUR CALCULATION", "FROM EPISODE 1"
GAP = 1.5                      # music beat between the two VO takes (timing.csv uses the same)
VO = [(P / "voice/bp-hlth02-ch1.mp3", 0.0), (P / "voice/bp-hlth02-ch2-4.mp3", 130.85 + GAP)]

# ---------- timing ----------
SN = [dict(id=r["id"], start=float(r["film_start"]), end=float(r["film_end"]), text=r["sentence"])
      for r in csv.DictReader(open(P / "timing.csv"))]
END = SN[-1]["end"] + 4.5      # end card after the last line


def at(i, frac=0.0):
    """Cut point for sentence i (1-based, as in timing.csv order): a beat before it starts, or a fraction into it."""
    s = SN[i - 1]
    return round(s["start"] + (s["end"] - s["start"]) * frac - (0.15 if frac == 0 else 0), 2)


def win(oid):
    ss = [s for s in SN if s["id"] == oid]
    return ss[0]["start"], ss[-1]["end"]


# ---------- sources ----------
OWN = A / "owner"
FREG = {r["id"]: OWN / "BP_HLTH02_Asset_Pack" / r["local_file"] for r in csv.DictReader(open(P / "handoff/asset-pack/FOOTAGE_REGISTER.csv"))}
PREG = {r["id"]: OWN / "Pexels_India_Only" / r["local_file"] for r in csv.DictReader(open(P / "handoff/asset-pack/PEXELS_INDIA_SOURCE_REGISTER.csv"))}
B = lambda n: A / "broll" / f"pixabay_{n}.mp4"
G = lambda n: A / "episode1" / "glimpses" / f"{n}.mp4"
WEB = lambda n: A / "web" / f"{n}_full.png"
CM = lambda n: next((A / "commons").glob(f"{n}_*"))
THUMB1 = ROOT / "projects/health-claim-trap/youtube/thumbnail_B.jpg"


def S(t, kind, **kw):
    return dict(t=round(t, 2), kind=kind, **kw)


def F(n, t, ss=1.0, label="", tag=ILL, **kw):
    return S(t, "clip", src=FREG[n], ss=ss, label=label, tag=tag, **kw)


def PX(n, t, ss=1.0, label="", tag=ILL, **kw):
    return S(t, "clip", src=PREG[n], ss=ss, label=label, tag=tag, **kw)


def SC(name, oid, t=None, **kw):
    """An animated scene clip for one VO window; it starts 0.25 s before the window (its handle)."""
    w0 = win(oid)[0]
    return S(w0 - 0.15 if t is None else t, "scene", src=A / "scenes" / f"{name}_{oid}.mp4", base=w0 - 0.25, name=f"{name} · {oid}", **kw)


def GL(n, t, label):
    return S(t, "glimpse", src=G(n), label=label, tag=EP1)


def WP(n, t, label, tag, focus=(0.5, 0.3), zoom=(1.0, 1.35)):
    return S(t, "still", src=WEB(n), label=label, tag=tag, focus=focus, zoom=zoom, top=True)


SHOTS = [
    # ---- 1 The rejection email and the two doors ----
    GL("g1_counter", 0.0, "9 PM · BILLING COUNTER"),
    GL("g2_bill", at(2), "BILL: ₹4,50,000"),
    GL("g3_denied", at(2, 0.5), "CASHLESS DENIED"),
    S(at(3), "still", src=THUMB1, zoom=(1.0, 1.25), focus=(0.5, 0.5), label="EPISODE 1 · THE FOUR STEPS", tag=EP1),
    F("F05", at(5), 2.0, "NOT THE END OF YOUR CLAIM"),
    PX("PX07", at(6), 2.0, "PAY NOW · CLAIM IT BACK"),
    SC("A1_staircase", "O002", t=at(7)),
    GL("g4_step1", at(8), "1 · COLLECT YOUR PAPERS"),
    GL("g5_step2", at(9), "2 · REIMBURSEMENT + GRIEVANCE OFFICER"),
    GL("g6_step3_bima", at(10), "3 · BIMA BHAROSA"),
    GL("g7_step4_cio", at(11), "4 · INSURANCE OMBUDSMAN"),
    F("F01", at(12), 1.0, "PAID FROM YOUR POCKET"),
    F("F09", at(12, 0.55), 2.0, "FILED FOR REIMBURSEMENT"),
    SC("A4_email_stamp", "O004"),
    SC("A3_claim_cut", "O005"),
    SC("A2_three_doors", "O006"),
    SC("A2_three_doors", "O007"),
    PX("PX09", at(17), 2.0, "1 · A LAWYER AND CONSUMER COURT"),
    SC("A2_three_doors", "O008"),
    PX("PX08", at(19), 1.0, "2 · A CLAIM RECOVERY SERVICE"),
    F("F08", at(19, 0.55), 1.0, "20% OR MORE OF YOUR MONEY"),
    SC("A2_three_doors", "O009"),
    SC("A2_three_doors", "O010"),
    WP("cio", at(24), "FILING IS FREE", "CIO FAQ"),
    SC("C4_binding_award", "O010", t=at(25)),
    PX("PX15", at(26), 1.0, "₹5,000 A DAY IF PAID LATE", tag="IRDAI HEALTH MASTER CIRCULAR | 2024"),
    F("F17", at(26, 0.55), 1.0, "UNLESS THE AWARD IS CHALLENGED", tag="IRDAI POLICYHOLDERS' INTERESTS MASTER CIRCULAR | 2024"),
    S(at(27), "sting"),
    PX("PX05", at(28), 2.0, "ONE COMMON MISTAKE"),
    S(at(28, 0.33), "clip", src=B(169446), ss=2.0, label="FILING, STEP BY STEP", tag=ILL),
    PX("PX13", at(28, 0.58), 1.0, "THE HEARING", tag="ILLUSTRATIVE HEARING"),
    PX("PX15", at(28, 0.8), 4.0, "AFTER THE COMPANY LOSES"),
    F("F08", at(29), 4.0, "₹0 TO MIDDLEMEN"),
    F("F15", at(30), 2.0, "LET'S BREAK IT DOWN", tag=""),
    # ---- 2 Bima Bharosa, the Ombudsman and the middleman ----
    WP("bima", at(31), "STEP 3 · BIMA BHAROSA", "63% SETTLED FOR THE POLICYHOLDER, 2025–26 [IRDAI CONSULTATION PAPER | 2026]", focus=(0.3, 0.3)),
    F("F01", at(33), 4.0, "IF IT DOES NOT WORK, DON'T STOP"),
    S(at(34), "clip", src=B(3176), ss=1.0, label="UPLOAD YOUR PAPERS · WAIT", tag=ILL),
    PX("PX08", at(35), 5.0, "THE SAME REPLY AGAIN"),
    PX("PX05", at(36), 8.0, "EVEN THE GOVERNMENT PORTAL?"),
    SC("A5_bima_tracker", "O017"),
    S(at(40), "clip", src=B(17257), ss=5.0, label="BIMA BHAROSA IS NOT A COURT", tag=ILL),
    SC("A5_bima_tracker", "O017", t=at(41)),
    SC("C5_proof_magnifier", "O018"),
    F("F08", at(45), 2.0, "BACK TO THE SECOND DOOR"),
    SC("B1_fee_split", "O020"),
    SC("B1_fee_split", "O021"),
    PX("PX09", at(51), 6.0, "WHAT THEY MAY NOT TELL YOU"),
    SC("C5_proof_magnifier", "O022"),
    WP("cio_complaint", at(53), "THE SAME FREE FORM", "CIOINS.CO.IN"),
    S(at(54), "clip", src=B(169446), ss=8.0, label="NEVER SHARE PASSWORDS OR OTPs", tag=ILL),
    SC("B1_fee_split", "O024"),
    # ---- 3 The two-step clock ----
    SC("A4_email_stamp", "O025"),
    SC("A4_email_stamp", "O026"),
    SC("C5_proof_magnifier", "O027"),
    SC("B2_two_step_clock", "O028"),
    F("F09", at(63), 6.0, "CLOCK STEP 1 · PLAN STEP 2"),
    F("F10", at(65), 1.0, "COMPLAIN IN WRITING TO THE GRO"),
    WP("cio", at(66), "GRO DETAILS: INSURER + CIOINS.CO.IN", "CIOINS.CO.IN", focus=(0.5, 0.05), zoom=(1.2, 1.6)),
    PX("PX14", at(67), 1.0, "ONE CALM, FORMAL EMAIL"),
    F("F09", at(67, 0.5), 10.0, "POLICY NO · CLAIM NO · WHY IT IS WRONG"),
    F("F07", at(68), 2.0, "KEEP EVERY COPY"),
    SC("B2_two_step_clock", "O032"),
    SC("B2_two_step_clock", "O033"),
    SC("B2_two_step_clock", "O034"),
    SC("B2_two_step_clock", "O035"),
    WP("cio_complaint", at(75), "RAISED TO ₹50 LAKH · NOV 2023", "GAZETTE G.S.R. 828(E) | 2023", focus=(0.5, 0.75), zoom=(1.3, 1.7)),
    SC("C5_proof_magnifier", "O037"),
    # ---- 4 Filing, the hearing and the award ----
    PX("PX14", at(78), 4.0, "HOW DO YOU FILE?"),
    SC("C1_filing_stepper", "O039"),
    SC("C1_filing_stepper", "O040"),
    SC("C2_offices_board", "O041"),
    WP("cio_offices", at(83), "THE OFFICE FOR YOUR AREA", "CIO OFFICE DIRECTORY", focus=(0.5, 0.25)),
    SC("C3_document_slots", "O042"),
    SC("C3_document_slots", "O043"),
    SC("C3_document_slots", "O044"),
    SC("C3_document_slots", "O045"),
    SC("C3_document_slots", "O046"),
    SC("C3_document_slots", "O047"),
    SC("C1_filing_stepper", "O048"),
    PX("PX10", at(99), 1.0, "WHAT HAPPENS NEXT?"),
    F("F12", at(100), 1.0, "BOTH SIDES ARE HEARD", tag="ILLUSTRATIVE HEARING"),
    PX("PX11", at(101), 1.0, "IN PERSON OR BY VIDEO", tag="ILLUSTRATIVE HEARING"),
    SC("B4_time_stats", "O051"),
    SC("C4_binding_award", "O052"),
    PX("PX14", at(106), 6.0, "NO LEGAL WORDS NEEDED", tag="ILLUSTRATIVE HEARING"),
    PX("PX12", at(108), 2.0, "WHEN DID YOU BUY THE POLICY?", tag="ILLUSTRATIVE HEARING"),
    PX("PX01", at(109), 2.0, "WHY WERE YOU IN HOSPITAL?"),
    F("F17", at(110), 4.0, "HOW MUCH DID THEY CUT?"),
    SC("B4_time_stats", "O054"),
    F("F14", at(113), 1.0, "BUILT FOR YOU", tag=""),
    SC("C4_binding_award", "O056"),
    SC("C4_binding_award", "O057"),
    SC("B3_penalty_meter", "O058"),
    SC("B3_penalty_meter", "O059"),
    SC("B3_penalty_meter", "O060"),
    S(at(124), "still", src=CM("bhc_03"), zoom=(1.0, 1.2), focus=(0.4, 0.75), label="BOMBAY HIGH COURT · DEC 2024",
      tag="BHARAT HIRJI DEDHIA v. UNION OF INDIA | BOMBAY HC | 2024"),
    S(at(124, 0.45), "still", src=CM("bhc_02"), zoom=(1.05, 1.25), focus=(0.5, 0.4), label="UNPAID FOR OVER 3 YEARS",
      tag="BHARAT HIRJI DEDHIA v. UNION OF INDIA | BOMBAY HC | 2024"),
    S(at(125), "clip", src=B(17257), ss=3.0, label="AWARD + INTEREST + ₹1 LAKH COSTS", tag="BOMBAY HC | 9 DEC 2024"),
    S(at(125, 0.5), "still", src=CM("bhc_01"), zoom=(1.0, 1.3), focus=(0.6, 0.45), label="RECOVERED FROM THE OFFICERS, AFTER AN INQUIRY",
      tag="BHARAT HIRJI DEDHIA v. UNION OF INDIA | BOMBAY HC | 2024"),
    PX("PX10", at(126), 4.0, "THE POWER OF KNOWING YOUR RIGHTS", tag=""),
    F("F14", at(127), 4.0, "NO CONNECTIONS · NO 20% FEES", tag=""),
    S(at(128), "sting"),
    S(at(131), "clip", src=B(63241), ss=2.0, label="NEXT · CONSUMABLES", tag=ILL),
    S(at(131, 0.6), "clip", src=B(151857), ss=1.0, label="GLOVES · MASKS · SYRINGES", tag=ILL),
    S(at(132), "clip", src=B(67764), ss=4.0, label="A ₹5 LAKH BILL, LINE BY LINE", tag=ILL),
    F("F07", at(132, 0.55), 12.0, "WHAT THE PRICE RULES SAY", tag=ILL),
    S(at(133), "end"),
]


# ---------- rendering (from projects/health-claim-trap/build/assemble.py) ----------
def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {' '.join(map(str, cmd))[:400]}\n{r.stderr[-800:]}")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%")


def rate(H, mbps_720, cap=30):
    b = min(cap, mbps_720 * (H / 720) ** 2)
    return ["-b:v", f"{b:.0f}M", "-maxrate", f"{b * 1.2:.0f}M", "-bufsize", f"{b * 2:.0f}M"]


def overlays(W, H, label="", tag=""):
    """Lower-third label (teal bar, the Ombudsman colour) and the corner citation/tag; palette from the owner's G01-G08."""
    k = H / 1080; f = []
    if label:
        f.append(f"drawbox=x={int(70*k)}:y={int(938*k)}:w={int(8*k)}:h={int(64*k)}:color=0x59dcc3@1:t=fill")
        f.append(f"drawtext=fontfile={FONT}:text='{esc(label)}':x={int(96*k)}:y={int(950*k)}:fontsize={int(40*k)}:fontcolor=0xf5f7fb:"
                 f"box=1:boxcolor=0x0b1422@0.72:boxborderw={int(16*k)}")
    if tag:
        f.append(f"drawtext=fontfile={FONT}:text='{esc(tag)}':x=w-tw-{int(70*k)}:y=h-{int(64*k)}:fontsize={int(20*k)}:fontcolor=white@0.9:"
                 f"box=1:boxcolor=0x0b1422@0.6:boxborderw={int(8*k)}")
    return f


def kb(W, H, dur, z0=1.0, z1=1.08, fx=0.5, fy=0.5, fx1=None, top=False):
    n = max(1, int(dur * 30)); fx1 = fx if fx1 is None else fx1
    ease = f"(0.5-0.5*cos(PI*on/{n}))"
    o = 4 if H <= 1080 else 2
    # web captures are tall pages: fit the width, keep the top, so the page reads like a screen
    pre = (f"scale={W*o}:-2,crop={W*o}:{H*o}:0:'min(ih-{H*o},max(0,ih*{fy}-{H*o}/2))'" if top else
           f"scale={W*o}:{H*o}:force_original_aspect_ratio=increase,crop={W*o}:{H*o}")
    fy_ = 0.5 if top else fy
    return (f"{pre},zoompan=z='{z0}+({z1}-{z0})*{ease}':x='iw*({fx}+({fx1}-{fx})*{ease})-iw/zoom/2':y='ih*{fy_}-ih/zoom/2':"
            f"d={n+2}:s={W}x{H}:fps=30")


def placeholder(shot, dur, out, W, H, enc):
    txt = esc("ANIMATED SCENE PENDING · " + shot["name"])
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x14263b:s={W}x{H}:r=30", "-vf",
         f"drawtext=fontfile={FONT}:text='{txt}':x=(w-tw)/2:y=(h-th)/2:fontsize={int(H*0.035)}:fontcolor=0xffdb59",
         "-t", f"{dur:.3f}"] + enc + [out])


def render(shot, dur, out, W, H):
    k = shot["kind"]; ov = overlays(W, H, shot.get("label", ""), shot.get("tag", ""))
    enc = ["-frames:v", str(round(dur * 30)), "-an", "-c:v", "libx264", "-preset", "veryfast", *rate(H, 5), "-pix_fmt", "yuv420p", "-r", "30"]
    if k == "clip":
        pz = 1.3 if shot.get("punch") else 1.08
        px, py = shot.get("punch", (0.5, 0.5))
        vf = [f"scale={int(W*pz)}:{int(H*pz)}:force_original_aspect_ratio=increase",
              f"crop={int(W*1.08)}:{int(H*1.08)}:'(iw-ow)*{px}':'(ih-oh)*{py}'",
              f"scale=w='{int(W*1.08)}-{int(W*0.08)}*t/{dur:.2f}':h=-2:eval=frame", f"crop={W}:{H}", "fps=30",
              "eq=saturation=0.9:contrast=1.04", "vignette=PI/5"] + ov
        run(["ffmpeg", "-v", "error", "-y", "-ss", shot.get("ss", 0), "-stream_loop", "-1", "-i", shot["src"], "-vf", ",".join(vf),
             "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "glimpse":   # Episode 01 shots: played as cut, last frame held if the slot is longer
        run(["ffmpeg", "-v", "error", "-y", "-i", shot["src"], "-vf",
             ",".join([f"scale={W}:{H}", "fps=30", "tpad=stop_mode=clone:stop_duration=5"] + ov), "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "scene":
        if not Path(shot["src"]).exists():
            return placeholder(shot, dur, out, W, H, enc)
        off = shot.get("frm", shot["t"]) - shot["base"]
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, off):.3f}", "-i", shot["src"],
             "-vf", ",".join([f"scale={W}:{H}", "fps=30", "tpad=stop_mode=clone:stop_duration=5"] + ov), "-t", f"{dur:.3f}"] + enc + [out])
    elif k == "still":
        fx, fy = shot.get("focus", (0.5, 0.5))
        z = shot.get("zoom") or (1.0, 1.06)
        vf = [kb(W, H, dur, z[0], z[1], fx, fy, shot.get("pan_to"), shot.get("top", False)), "vignette=PI/6"] + ov
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", shot["src"], "-vf", ",".join(vf), "-t", f"{dur:.3f}"] + enc + [out])
    elif k in ("sting", "end"):
        bg = FREG["F14"]
        if k == "sting":
            fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=brightness=-0.15[bg];"
                  f"[1:v]scale={int(W*0.62)}:-2,format=rgba,fade=t=in:st=0:d=0.5:alpha=1[l];[bg][l]overlay=(W-w)/2:(H-h)/2")
        else:
            fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=8,eq=brightness=-0.25[bg];"
                  f"[1:v]scale={int(W*0.5)}:-2[l];[bg][l]overlay=(W-w)/2:H*0.18,"
                  f"drawtext=fontfile={FONT}:text='SUBSCRIBE · SHARE WITH YOUR FAMILY':x=(w-tw)/2:y=h*0.70:fontsize={int(H*0.035)}:fontcolor=white,"
                  f"drawtext=fontfile={FONT}:text='Educational only · not legal advice · read your policy wording':x=(w-tw)/2:y=h*0.78:fontsize={int(H*0.024)}:fontcolor=white@0.85")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-stream_loop", "-1", "-i", bg, "-loop", "1", "-i", ROOT / "assets/brand/banner.png",
             "-filter_complex", fc, "-t", f"{dur:.3f}"] + enc + [out])
    else:
        sys.exit("unknown kind " + k)


def split_long(shots, end):
    """Cadence (charter: a change every 2.5-4 s): any still or clip longer than ~5 s is cut into ~3.5 s framings."""
    out = []
    for i, s in enumerate(shots):
        nxt = shots[i + 1]["t"] if i + 1 < len(shots) else end
        dur = nxt - s["t"]
        if s["kind"] not in ("still", "clip") or dur <= 5.0:
            out.append(s); continue
        n = max(2, round(dur / 3.6))
        for m in range(n):
            q = dict(s, t=round(s["t"] + dur * m / n, 2))
            if s["kind"] == "clip":
                q["ss"] = s.get("ss", 0) + m * (dur / n + 1.2)
                if m % 2: q["punch"] = (0.35 + 0.3 * (m % 3 == 1), 0.42)
            else:
                z0, z1 = s.get("zoom") or (1.0, 1.1)
                a, b = z0 + (z1 - z0) * m / n, z0 + (z1 - z0) * (m + 1) / n
                q["zoom"] = (a * (1.04 if m % 2 else 1.0), b * (1.04 if m % 2 else 1.0))
            out.append(q)
    return out


def shot_list():
    lst = sorted(SHOTS, key=lambda s: s["t"])
    clean = []
    for i, s in enumerate(lst):   # a shot under 0.4 s gives its time to the next one
        nxt = lst[i + 1]["t"] if i + 1 < len(lst) else END
        if nxt - s["t"] < 0.4 and i + 1 < len(lst):
            lst[i + 1] = dict(lst[i + 1], t=s["t"]); continue
        clean.append(s)
    clean[0] = dict(clean[0], t=0.0)
    return split_long(clean, END)


def write_edl(shots):
    def mmss(t): return f"{int(t // 60)}:{t % 60:05.2f}"
    with open(P / "edl.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "start", "dur", "kind", "source", "label", "tag"])
        for i, s in enumerate(shots):
            nxt = shots[i + 1]["t"] if i + 1 < len(shots) else END
            w.writerow([i + 1, s["t"], round(nxt - s["t"], 2), s["kind"], Path(str(s.get("src", s["kind"]))).name, s.get("label", ""), s.get("tag", "")])
    rows = list(csv.reader(open(P / "edl.csv")))
    with open(P / "edl.md", "w") as f:
        f.write("# EDL: The Insurance Ombudsman (generated by build/assemble.py --edl; edit the shot list, not this file)\n\n"
                f"{len(rows) - 1} shots, {mmss(END)}.\n\n| # | start | dur | kind | source | label | tag |\n|---|---|---|---|---|---|---|\n")
        for r in rows[1:]:
            f.write(f"| {r[0]} | {mmss(float(r[1]))} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |\n")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--height", type=int, default=1080); ap.add_argument("--edl", action="store_true")
    a = ap.parse_args()
    shots = shot_list(); write_edl(shots)
    durs = [(shots[i + 1]["t"] if i + 1 < len(shots) else END) - s["t"] for i, s in enumerate(shots)]
    print(f"{len(shots)} shots, {END:.1f} s, mean {sum(durs)/len(durs):.2f} s, longest {max(durs):.2f} s")
    if a.edl:
        return
    H = a.height; W = H * 16 // 9
    out = A / f"shots{H}"; out.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, (s, d) in enumerate(zip(shots, durs)):
        spec = json.dumps({k: str(v) for k, v in s.items()}, sort_keys=True) + f"{d:.3f}{H}"
        if s["kind"] == "scene" and Path(s["src"]).exists():
            spec += str(Path(s["src"]).stat().st_mtime)
        f = out / f"{i:03d}_{hashlib.md5(spec.encode()).hexdigest()[:10]}.mp4"
        if not f.exists():
            render(s, d, f, W, H)
        parts.append(f)
    lst = out / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    silent = A / f"picture_{H}.mp4"
    # one pass over the joined picture: logo bug (top right), fine film grain
    logo = ROOT / "assets/brand/logo_square.png"
    fc = (f"[0:v]noise=alls=5:allf=t[v];[1:v]scale={int(H*0.075)}:-2,format=rgba,colorchannelmixer=aa=0.8[l];"
          f"[v][l]overlay=W-w-{int(H*0.045)}:{int(H*0.045)}")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-loop", "1", "-i", logo, "-filter_complex", fc,
         "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "medium", *rate(H, 5), "-pix_fmt", "yuv420p", "-r", "30", silent])
    print("picture:", silent)


if __name__ == "__main__":
    main()
