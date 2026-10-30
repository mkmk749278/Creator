#!/usr/bin/env python3
"""Pharma film assembly: the shot list, overlays, gauge and captions -> HyperFrames parts in video/pha/p1..p5.

Times: every shot is placed on a VO line (align/align.json, 1-based line numbers = vo.txt rows) or sentence
(align/sentences.json). The film adds picture-led beats where the voice stops (BEATS: seconds of silence after a line,
screenplay.md); F() maps a raw VO time to film time and voice/vo_film.wav is the VO with those silences inserted.
Base media: owner-fetched footage (assets/footage), Pixabay (assets/stock), Wellcome (assets/wellcome), documents
(assets/docs) and the animated scenes (assets/renders, from video/pha/gen_scenes.py, rendered on GitHub Actions).
Numbers on screen come from claims.csv. Overlays are animated by video/pha/_shared/pha.js (the rare earth engine).
Usage: python3 projects/pharma-apis/build/make_film.py   (then npm run vendor; render the parts: PLAYBOOK §3a)
"""
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import frame_floor as FF  # noqa: E402

P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]; A = P / "assets"; OUTV = ROOT / "video/pha"
esc = html.escape
LINES = json.loads((P / "align/align.json").read_text())
SENTS = json.loads((P / "align/sentences.json").read_text())

# ---------- picture-led beats: seconds of silence inserted after these lines (screenplay.md) ----------
BEATS = {6: 1.5, 16: 1.0, 24: 1.0, 28: 1.5, 30: 2.0, 37: 2.5, 42: 2.0, 51: 1.5, 52: 0.6, 53: 0.6, 54: 0.6, 55: 1.5,
         60: 1.0, 63: 1.5, 3: 0.6, 11: 0.4,
         7: 0.4}   # 7: a held breath before "Yes." (second review, 30 Oct: the question ran straight into the answer)
CUTS = sorted((round((LINES[n - 1]["end"] + LINES[n]["start"]) / 2, 3), s) for n, s in BEATS.items())


def F(t):
    """raw VO seconds -> film seconds"""
    return round(t + sum(s for c, s in CUTS if c <= t), 3)


def L(n, k=0.0):
    """film time at fraction k through line n (k=0: its first word)"""
    a, b = LINES[n - 1]["start"], LINES[n - 1]["end"]
    return F(a + (b - a) * k)


def LE(n):
    return F(LINES[n - 1]["end"])


def S(n, k):
    """film start of the k-th sentence (0-based) of line n"""
    return F([s for s in SENTS if s["line"] == n][k]["start"])


PRE = 0.15                       # the picture cuts this long before the line's first word ("cut on the breath")
VO_END = F(LINES[-1]["end"])
END = round(VO_END + 8.0, 2)    # end screen (YouTube end-screen elements need 5-20 s; review: 24 s was too long)

FOOT = {  # owner-fetched footage (assets/footage/fetched.csv; Pexels downloaded by the owner)
    "Y02": ("02_1ddBzBUaa8k.mp4", "FOOTAGE · LYFIUS PHARMA"), "Y04": ("04_3aclBlRaYNQ.mp4", "FOOTAGE · ABP MAJHA"),
    "Y05": ("05_keUkhEBY_fs_stab.mp4", "FOOTAGE · AMAR AGRO INDUSTRY"), "Y06": ("06_ZT2VuADHAFo_stab.mp4", "FOOTAGE · ADINATH STONES"),
    "APc": ("ap_pretoria_court_20010418.mp4", "AP ARCHIVE · PRETORIA HIGH COURT · 18 APR 2001"),
    "CNa": ("cns_wuhan_aerial_20200126.mp4", "CHINA NEWS SERVICE · WUHAN · 26 JAN 2020 · CC BY 4.0"),
    "CNs": ("cns_wuhan_streets_20200126.mp4", "CHINA NEWS SERVICE · WUHAN · 26 JAN 2020 · CC BY 4.0"),
    # round 5 (owner-fetched 30 Oct): the roll call's real places, Hindustan Antibiotics' signboard, a 1944 penicillin ward
    "MPC": ("r5_09_OZTjlmB7Llk.mp4", "FOOTAGE · MPC NEWS · HINDUSTAN ANTIBIOTICS, PIMPRI · 2015"),
    "ETV": ("r5_05_L3VNPM_fBAA.mp4", "FOOTAGE · ETV TELANGANA · I.D.P.L. HYDERABAD · 2026"),
    "HSN": ("r5_08_-KiqNoJvtbo.mp4", "FOOTAGE · NEXT GENERATION NEWS · PIMPRI · 2015"),
    "ICI": ("r5_04_-7HmDfgaakg.mp4", "ARCHIVE FILM · PENICILLIN · I.C.I. 1944 · BRUNNER MOND FILM ARCHIVE"),
    "CIP": ("r5_02_xziIt2SJp34.mp4", "FOOTAGE · CIPLA · MAKE IN INDIA"),
    # round 6 (owner-fetched 30 Oct): Chinese drug plants today, for "China went all in… huge plants" (the chimney was a stand-in)
    "CGT": ("r6_01_9c-PcIWGwQY.mp4", "FOOTAGE · CGTN · CSPC PLANT, SHIJIAZHUANG · 2022"),
    "CCV": ("r6_02_mXsHcF87-Is.mp4", "FOOTAGE · CCTV+ · CHINA · 2026"),
    "PXa": ("3922881-uhd_4096_2160_25fps.mp4", "PEXELS"), "PXb": ("13048933-uhd_3840_2160_30fps.mp4", "PEXELS"),
}


def media(name, raw=False):
    src = None
    if name in FOOT:
        src = A / "footage" / FOOT[name][0]
    elif name.startswith("px_"):
        src = A / "stock" / f"pixabay_{name[3:]}.mp4"
    if src is not None:   # the 30 fps conform (build/conform.sh) when it exists: no judder (owner's review, 2026-10-29)
        conf = A / "conformed" / src.name
        return conf if conf.exists() and not raw else src
    if name.startswith("PH_"):
        return A / "photos" / f"pixabay_{name[3:]}.jpg"
    if name.startswith("J_"):
        return A / "photos" / f"jnpt_{name[2:]}.jpg"
    if name.startswith("R_"):   # PHA_RENDERS=4k: the native 3840x2160 scene renders for the master (render_scenes_4k.sh)
        sub = "renders4k" if os.environ.get("PHA_RENDERS") == "4k" else "renders"
        return A / sub / f"video_pha_{name[2:]}.mp4"
    if name.startswith("W_"):
        return A / "wellcome" / f"{name[2:]}.jpg"
    if name.startswith("D_"):
        for ext in (".jpg", ".png"):
            f = A / "docs" / f"{name[2:]}{ext}"
            if f.exists():
                return f
    if name == "endcard":
        return ROOT / "assets/brand/banner.png"
    raise SystemExit(f"missing media {name}")


def default_tag(src):
    if src in FOOT:
        return FOOT[src][1]
    if src.startswith("px_"):
        return "PIXABAY"
    if src.startswith("R_"):
        return ""          # the scenes carry their own ILLUSTRATION tag
    if src.startswith("W_"):
        return "WELLCOME COLLECTION · CC BY 4.0"
    if src.startswith("PH_"):
        return "PIXABAY"
    if src.startswith("J_"):   # CC BY-SA asks for the photographer's name with the licence
        who = {"J_aerial": "EVENT HORIZON 299792", "J_seaside": "KUWARONLINE"}[src]
        return f"J.N. PORT, NAVI MUMBAI · {who} · WIKIMEDIA COMMONS · CC BY-SA 4.0"
    if src.startswith("D_"):
        return "DOCUMENT"
    return ""


SEQ, OV = [], []


XF = 0.2   # every cut is a 6-frame dissolve (owner, 2026-10-30: "should not look like stitches, all should feel smooth")


def shot(t0, src, move="push", tag=None, ms=0.0, origin=None, dim=False, hard=False):
    """a base shot from t0 until the next shot starts (the cut is gapless by construction). hard=True: the cuts into and
    out of this shot stay hard (a deliberate rhythm: the verb cuts, the Cipla montage); every other cut dissolves over XF,
    the outgoing shot running XF longer under the incoming one"""
    SEQ.append(dict(t0=round(t0, 3), src=src, move=move, tag=default_tag(src) if tag is None else tag, ms=ms, origin=origin, dim=dim, hard=hard))


# Cipla's film cuts every 1-2 s and burns captions into most shots: its caption-free spans (frame-checked), raw seconds
CIP_SPANS = [(3.47, 4.92), (13.1, 14.05), (37.25, 38.21), (46.1, 47.33),   # the four verbs, each sized to its one word
             (38.3, 40.0), (14.2, 15.33), (44.5, 45.49), (15.45, 16.33), (11.22, 12.04), (0.05, 0.75), (16.44, 17.1), (1.7, 2.45),
             (27.4, 29.75), (12.15, 13.0), (51.6, 53.8), (2.6, 3.32)]   # the last four: no lower third
SRC_FPS = {"CIP": 299 / 12}


def montage(t0, t1, src, starts, move="crop2", origin="50% 50%", tag=None):
    """back-to-back pieces from one source, each as long as its own clean span (CLEAN) allows, until t1; one shot per piece
    so clean_assign keeps each inside its span (owner's review, 30 Oct: picture to word, shot by shot)"""
    t = t0
    for a in starts:
        span = next(b - a for x, b in CIP_SPANS if abs(x - a) < 1e-6)
        shot(round(t, 3), src, move, ms=a, origin=origin, tag=tag, hard=True)
        t += span * SRC_FPS[src] / 30 - 0.04
        if t >= t1 - 0.3:
            return
    raise SystemExit(f"montage {src} at {t0}: spans end at {t:.2f}, need {t1}")


def el(h, at, to):
    OV.append(dict(h=h, at=at, to=to))


def attrs(at, to, fx, d=None):
    return f'data-at="{at}" data-fx="{fx}"' + (f' data-to="{to}"' if to is not None else "") + (f' data-d="{d}"' if d else "")


def chip(text, at, to, x, y, col="ink", size="", fx="pop"):
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{esc(text)}</div>', at, to)


def cite(text, at, to):
    el(f'<div class="cite" {attrs(at, to, "fade")}>{esc(text)}</div>', at, to)


def datebig(text, small, at, to, scrim=True):   # dark backing: dates sit on bright footage too
    el(f'<div class="datebig{" scrim" if scrim else ""}" {attrs(at, to, "left", 0.4)}>{esc(text)}<small>{esc(small)}</small></div>', at, to)


def namelt(name, role, at, to):
    el(f'<div class="namelt" {attrs(at, to, "left", 0.45)}><b>{esc(name)}</b><span>{esc(role)}</span></div>', at, to)


def count(at, to, x, y, a, b, start, dur, pre="", suf="", col="ink", size="", dec=0):
    dur = min(dur, 0.45)   # lands in under half a second: a slow roll showed wrong numbers long enough to read (audit 2026-10-30)
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, "pop")}><span data-count="{a},{b},{start},{dur}" '
       f'data-pre="{esc(pre)}" data-suf="{esc(suf)}" data-dec="{dec}" data-ease="power2.out">{esc(pre)}{a}{esc(suf)}</span></div>', at, to)


def stamp(text, at, to, x, y):
    el(f'<div class="stamp" style="left:{x}px;top:{y}px" {attrs(at, to, "stamp", 0.28)}>{esc(text)}</div>', at, to)


def plate(text, small, at, to, x, y):
    el(f'<div class="plate" style="left:{x}px;top:{y}px" {attrs(at, to, "up", 0.4)}>{esc(text)}<small>{esc(small)}</small></div>', at, to)


def gauge(at, to, pct, key, src):
    """the CAPSULE GAUGE, bottom right: fills amber to `pct` (China's share), labelled with its base and source"""
    w = max(0.01, pct / 100)
    el(f'<div class="gauge" {attrs(at, to, "up", 0.4)}><div class="cap2"><div class="fill" style="width:100%" '
       f'data-at="{at + 0.2}" data-fx="grow" data-d="1.0"></div><div class="seam"></div><div class="val">{esc(pct_txt(pct))}</div></div>'
       f'<div class="key">{esc(key)}<br/>{esc(src)}</div></div>'.replace('style="width:100%"', f'style="width:{w * 100:.1f}%"'), at, to)


def hero(num, key, at, to, pct, col="steel", cut_in=False, cut_out=False):
    """the film's two numbers as heroes (audit 2026-10-30: they lived only in a small corner gauge): one big number centre
    screen over a capsule bar that fills to China's share, its base underneath; the same place and size every time, so
    "<1%" can match-cut to "86%"."""
    w = max(0.6, pct)
    # the match cut is a hard cut both ways (second review, 30 Oct: a 0.25 s cross-fade read as the "86%" box jittering)
    el(f'<div class="hero c-{col}"{" data-cut" if cut_out else ""} {attrs(at, to, "cut" if cut_in else "fade", 0.25)}><div class="num">{esc(num)}</div>'
       f'<div class="bar"><div class="fill" style="width:{w:.1f}%" data-at="{round(at + 0.15, 3)}" data-fx="grow" data-d="0.8"></div></div>'
       f'<div class="key">{esc(key)}</div></div>', at, to)


def pct_txt(p):
    return "<1%" if p < 1 else f"{p:g}%"


def coins(at, to, n_amber=86, x0=430, y0=250):
    """100 coins, n_amber of them turn amber (86 of every 100 rupees of imported antibiotic powder)"""
    for i in range(100):
        x, y = x0 + (i % 20) * 54, y0 + (i // 20) * 64; t = round(at + i * 0.012, 3)
        el(f'<div class="box" style="left:{x}px;top:{y}px;width:42px;height:42px;border-radius:50%" {attrs(t, to, "pop", 0.2)}></div>', t, to)
        if i < n_amber:
            ta = round(at + 1.2 + i * 0.014, 3)
            el(f'<div class="box c-amber" style="left:{x}px;top:{y}px;width:42px;height:42px;border-radius:50%" {attrs(ta, to, "fade", 0.2)}></div>', ta, to)


# =====================================================================================================
# THE CUT (film seconds). VO cue in each comment; L(n) = line n of vo.txt.
# =====================================================================================================
c = lambda n: L(n) - PRE           # cut time for line n
HERO86 = round(S(57, 3) + 1.15, 3)   # "China's share is around eighty-six per cent": the word "eighty-six"
# ---- HOOK: pharmacy of the world, the capsule, the locked doors (0:00-1:35)
shot(0.0, "PXb", "slow", ms=1.0)                                   # "India sells medicines to around two hundred countries..."
chip("Pharmacy of the world", 1.2, LE(1), 120, 640, "steel", "", "up")
shot(c(2), "R_capsule_open", "none", ms=0.6)                       # "But open one antibiotic capsule..."
shot(S(2, 1) - PRE, "R_map_stream", "none", ms=0.4)                # "That's the actual medicine... began in China."
shot(c(3), "px_40948", "in", ms=1.0)                               # "The rest of the capsule is just there to carry it to you."
# the Corona days as a dated report, not a generic street (owner, 2026-10-30): the Tribune page of 4 Mar 2020, headline
# and date first, then down into its photo of masked buyers at a Delhi chemist counter
TRIB = "DOCUMENT · THE TRIBUNE · 4 MAR 2020"
shot(c(4), "D_tribune_2020_masks", "in", origin="50% 22%", tag=TRIB)   # "Now think back to the Corona days... Not the lockdown yet"
shot(round(c(4) + (c(5) - c(4)) / 2, 3), "D_tribune_2020_masks", "doc", origin="50% 74%", tag=TRIB)   # "three weeks before it. The third of March"
datebig("3 MARCH 2020", "LOCKDOWN 24 MARCH · 3 WEEKS AWAY", L(4, 0.55), LE(4))
shot(c(5), "R_map_hubei", "none", ms=0.0)                          # "In China, the city of Wuhan has been locked down..."
shot(c(6), "D_dgft_2020_noti50-1", "in", tag="DOCUMENT · DGFT")   # "Delhi. A two-page government order goes out..."
chip("13 ingredients", S(6, 2), LE(6) + 1.5, 120, 640, "red", "sm", "pop")
chip("Paracetamol", S(6, 3), LE(6) + 1.5, 640, 640, "red", "sm", "pop")
cite("[DGFT NOTIFICATION 50/2015-20 | 3 MAR 2020]", L(6, 0.1), LE(6) + 1.5)
shot(c(7), "J_aerial", "in", dim=0.3)   # an Indian port (JNPT), not a foreign one                           # "Wait. India? The pharmacy of the world... locking its own doors?"
chip("Exports: by licence", L(7, 0.4), LE(7), 120, 640, "red", "", "pop")
# the second time in Hubei shows the place (audit 2026-10-30: the map again was a dead repeat): Wuhan three days into
# its lockdown, framed 1.6x from the centre so the agency logos in the corners stay out
shot(c(8), "CNa", "y02", ms=6.0, origin="50% 50%")                  # "Yes. And the reason was Corona. Wuhan sits in a Chinese province called Hubei..."
shot(L(8, 0.62) - PRE, "CNs", "y02", ms=9.2, origin="50% 50%")      # "...and the whole province was shut down."
shot(c(9), "D_tribune_2020_head", "in", tag="DOCUMENT · THE TRIBUNE")   # headline only: no ad banner  # "Reports at the time said..."
cite("[THE TRIBUNE | 4 MAR 2020]", L(9), LE(9))
shot(c(10), "PH_257336", "in")   # real strips (the capsule animation is kept for the open and the close)                      # "So here's the question... who makes the powder?"
shot(c(11), "PXa", "slow", ms=0.5)                                 # "And before you worry — this isn't about the quality..."
chip("Quality: not the issue", L(11, 0.2), LE(11), 120, 160, "green", "sm", "up")
chip("Supply: the issue", L(11, 0.6), LE(11), 120, 260, "amber", "sm", "up")
shot(c(12), "Y02", "y02", ms=[49.78, 42.0, 86.26], origin="35% 30%")              # "Stay with me. Around minute eight... Andhra Pradesh"
chip("Minute 8 · Andhra Pradesh", L(12, 0.15), LE(12), 120, 160, "saffron", "sm", "up")
# ---- INDIA EARNED IT (1:31-2:50)
# "First, let's give India its due... India earned it." on an Indian plant (owner's review, 30 Oct: it was a Chinese
# softgel line): Cipla's own film, caption-free spans only
montage(c(13), c(14), "CIP", [38.3, 14.2, 44.5, 15.45, 11.22, 0.05, 16.44, 1.7])
shot(c(14), "D_msf2001-01", "in", tag="DOCUMENT · MSF · 2001")   # the 2001 ARV price report, not a microscope                         # "Think back to two thousand one."
# the people first (audit 2026-10-30): H.I.V.-positive activists in court for the medicine-price case, Pretoria, 18 Apr 2001
# (AP; the 4:3 picture filled at 1.42x)
shot(S(14, 1) - PRE, "APc", "crop2", ms=24.78, origin="50% 50%")   # "H.I.V. is killing millions in Africa."
# the price drop to scale: the pile of $100 notes collapses (scene 10.0 s) exactly as the $350 card lands
shot(S(14, 2) - PRE, "R_cipla", "slow", ms=round(max(0.0, 10.0 - (L(15, 0.55) - (S(14, 2) - PRE))), 3))   # "The medicines exist... a dollar a day... One dollar."
datebig("2001", "H.I.V. MEDICINES", L(14, 0.05), c(17))
# same unit on both cards (owner's review, 2026-10-29): MSF 7 Feb 2001, "about $10,400" in the US vs Cipla's "$350 per year" (P14, P15)
count(L(14, 0.6), c(17), 230, 250, 0, 10400, L(14, 0.62), 1.3, "$", " / YEAR", "red", "xl")
chip("Western price", L(14, 0.75), c(17), 236, 382, "red", "sm", "up")
count(L(15, 0.55), c(17), 230, 470, 350, 350, L(15, 0.55), 0.9, "$", " / YEAR", "green", "xl")   # lands at its value (r4 review: a ghost "$0" faded in first)
chip("Cipla · under $1 a day", L(15, 0.7), c(17), 236, 602, "green", "sm", "up")
cite("[MSF | 2001]", L(14, 0.6), c(17))
shot(c(17), "J_seaside", "left")   # JNPT from the sea                            # "And today... more than two and a half lakh crore rupees a year."
count(L(17, 0.4), LE(17), 120, 640, 0, 2.5, L(17, 0.45), 1.2, "₹", " LAKH CRORE+", "ink", "", 1)
cite("[PIB | EXPORTS 2024-25]", L(17, 0.4), LE(17))
shot(c(18), "R_tablet", "slow", ms=1.0)   # skip the empty first second                            # "Every tablet has two parts." ... coating, strip, box
# "And you should be proud of this. Indian companies are world class at that last part." Cipla's chief in his plant
# (no lower third in these spans), not a foreign capsule line
montage(c(21), S(21, 2) - PRE, "CIP", [27.4, 12.15, 51.6, 2.6])
# one cut per verb, on the word (second review, 30 Oct: one machine held under four actions): Cipla's own line, the
# letterbox and captions framed out (crop2); the cut points sit in the voice's own gaps between the words
shot(S(21, 2) - PRE, "CIP", "crop2", ms=13.15, origin="50% 50%", hard=True)     # "Mixing," (the coating drum)
shot(round(S(21, 2) + 0.626, 3), "CIP", "crop2", ms=3.5, origin="50% 50%", hard=True)    # "pressing," (tablets off the press)
shot(round(S(21, 2) + 1.476, 3), "CIP", "crop2", ms=37.26, origin="50% 50%", hard=True)  # "packing," (blister line)
shot(round(S(21, 2) + 2.256, 3), "CIP", "crop2", ms=46.12, origin="50% 50%", hard=True)  # "and passing the toughest inspections" (clean room)
# "...on the planet.": Lyfius's quality lab, two microscope shots (the lab's first shot is the teaser's at 1:33)
shot(round(S(21, 2) + 3.236, 3), "Y02", "y02", ms=96.02, origin="35% 30%", tag="FOOTAGE · LYFIUS PHARMA · QUALITY LAB")
shot(round(S(21, 2) + 3.236 + (c(22) - S(21, 2) - 3.236) / 2, 3), "Y02", "y02", ms=97.74, origin="35% 30%", tag="FOOTAGE · LYFIUS PHARMA · QUALITY LAB")
shot(c(22), "PH_1851178", "in")                         # "But the powder you swallow?"
shot(c(23), "D_niti_cover-01", "in", tag="DOCUMENT · NITI AAYOG")  # "In 2025, India bought these powders... sixty-five thousand crore"
count(L(23, 0.5), LE(23), 120, 640, 0, 65000, L(23, 0.55), 1.4, "₹", " CRORE · 2025", "amber", "sm")
cite("[NITI AAYOG $7.4 BN | OUR CONVERSION]", L(23, 0.5), LE(23))
shot(c(24), "R_map_trade", "none", ms=3.0)   # no Hubei here: the route lands at Indian ports                        # "And the biggest seller, by far... China."
shot(c(25), "D_niti_p-40", "in", dim=0.55, tag="DOCUMENT · NITI AAYOG")   # "And if you look at antibiotics... about eighty-six went to China."
coins(L(25, 0.45), LE(25))
gauge(L(25, 0.75), LE(25), 86.1, "TODAY · ANTIBIOTIC POWDER IMPORTS · CHINA'S SHARE", "NITI AAYOG · 2025")
cite("[NITI AAYOG | TRADE WATCH Q4 FY26]", L(25, 0.4), LE(25))
shot(c(26), "PH_1539191", "in", dim=0.15)   # a fever thermometer on white tablets (audit 2026-10-30: paracetamol is white, not pink)   # "Even your fever tablet has a China link..."
chip("Raw chemical: para-aminophenol", L(26, 0.6), LE(26), 120, 640, "amber", "sm", "up")   # P25: PAP, a big share from China
cite("[INDUSTRY REPORTS]", L(26, 0.6), LE(26))
# ---- INDIA MADE ITS OWN PENICILLIN (3:16-4:19)
shot(c(27), "PH_1851178", "out")                                    # "So you might be thinking — has it always been like this?"
# "It did.": 0.6 s of black under the words (audit 2026-10-30), then Hindustan Antibiotics' old signboard behind the trees
# today: "this part of the story, most people have never heard"
# the black runs to the signboard's cut (r4 review 3:29: the blisters showed again for 7 frames between them)
el(f'<div class="blackout" {attrs(S(28, 0) - 0.12, S(28, 1) - PRE, "fade", 0.08)}></div>', S(28, 0) - 0.12, S(28, 1) - PRE)
shot(S(28, 1) - PRE, "Y04", "crop", ms=[10.45, 14.25], origin="50% 50%", tag="FOOTAGE · ABP MAJHA · TODAY")
shot(c(29), "R_pimpri", "none", ms=0.0)   # map -> Pimpri, 15 Aug 1947 -> 1954 (< 7 years), the factory rises (owner's review: a lab drawing was here)              # "Pimpri, near Pune. Nineteen fifty-four..."
datebig("1954", "PIMPRI · NEAR PUNE", L(29, 0.05), LE(29))
shot(c(30), "ICI", "slow", ms=531.2)                                # "Penicillin was the miracle drug of that time..." (the 1944 film's own penicillin vials)
# a wounded man on a drip, masked doctors at the bed; then the same men well again (I.C.I.'s 1944 penicillin film)
shot(S(30, 1) - PRE, "ICI", "slow", ms=581.5)                       # "Back then, a small cut on your hand could kill you."
shot(S(30, 2) - PRE, "ICI", "slow", ms=[572.6, 559.3])              # "With penicillin, it became a few days of medicine for you."
chip("Miracle drug", L(30, 0.1), S(30, 1) - PRE, 120, 640, "green", "", "up")   # off before "a small cut could kill you"
shot(c(31), "HSN", "crop", ms=[27.1, 34.3], origin="50% 60%")   # the board, then the works (r4 review 3:32: the ABP clip crossed its own cut)             # "The government sets up... Hindustan Antibiotics. By 1956..."
namelt("Hindustan Antibiotics", "PIMPRI · SET UP 1954 · PENICILLIN BY 1956", L(31, 0.15), LE(31))
cite("[DEPT OF PHARMACEUTICALS | HAL]", L(31, 0.15), LE(31))
# "Picture your grandparents' India. A young, poor country, growing... in its own factory": the Pimpri plant at work, a
# cyclist on the road, a fermenter turning gold, vials out of the door (owner's review: a potency chart was here)
shot(c(32), "R_pimpri_grow", "none", ms=0.0)
# "Soon, others join in — Alembic, Sarabhai and Ranbaxy": each plant rises on its own name beside Pimpri
shot(c(33), "R_skyline_rise", "none", ms=0.0)
shot(c(34), "R_fermenter", "push", ms=0.0)                         # "How do you actually make penicillin?"
# ---- WHY PENICILLIN IS A SCALE GAME (4:19-5:43)
shot(c(35), "R_cooked", "none", ms=0.0)   # a batch reactor, step by step (audit 2026-10-30: petri dishes said biology)   # "Many medicines, like paracetamol, are cooked from chemicals..."
chip("Cooked", L(35, 0.2), S(35, 1), 120, 640, "steel", "", "pop")
shot(S(35, 1) - PRE, "W_B0004595", "in")                           # "Penicillin is different. Penicillin is grown."
chip("Grown", S(35, 2), LE(35), 120, 640, "green", "", "pop")
shot(c(36), "W_B0004843", "in")                                    # "You take a special mould... a cousin of the green patches..."
shot(S(36, 1) - PRE, "R_fermenter", "none", ms=0.5)                # "You put it in a giant steel tank... sugar and air."
# the day clock only runs forward (audit 2026-10-30): this piece flows into the germ beat at day 3 (9.8 s), the what-if
# batch runs on to day 7 under the murk, and "take the penicillin out" carries on from there
shot(c(37), "R_fermenter", "none", ms=round(9.8 - (S(37, 2) - PRE - c(37)), 3))   # "For about a week, the tank runs day and night..."
shot(S(37, 2) - PRE, "R_fermenter", "none", ms=9.8)   # the stray germ hits a growing culture (day 2-3), not the finished gold
chip("What if · one germ = lost batch", S(37, 2), LE(37) + 2.0, 120, 160, "red", "sm", "up")
el(f'<div class="contam" {attrs(S(37, 2) + 0.15, LE(37) + 2.0, "fade", 0.9)}></div>', S(37, 2) + 0.15, LE(37) + 2.0)   # the broth turns murky (ILLUSTRATION)
shot(c(38), "R_fermenter", "none", ms=round(9.8 + c(38) - (S(37, 2) - PRE), 3))                      # "Then you take the penicillin out... penicillin G."
chip("Penicillin G", L(38, 0.6), LE(38), 1320, 160, "green", "sm", "pop")
# the chemistry itself (audit 2026-10-30: capsules under the chips skipped it): one core, the side group snipped off and a new
# one locked on (gen_scenes.chain: snip ~1.2 s, "six A.P.A." 3.3 s, amoxicillin 7.5 s from the cut)
shot(c(39), "R_chain", "none", ms=0.0)                             # "Next, it's turned into a smaller base powder... amoxicillin"
shot(c(40), "R_tanks", "none", ms=0.5)                             # "A bigger tank makes the powder cheaper. Much cheaper."
shot(c(42), "Y06", "slow", ms=4.0)                                 # "Think of a flour mill. A big chakki grinds each kilo cheaper..."
chip("Small chakki", L(42, 0.1), S(42, 2), 120, 640, "steel", "sm", "up")
shot(S(42, 2) - PRE, "Y05", "crop", ms=1.0, origin="50% 10%")     # "Double your tank, and your costs don't double... but your output does."
chip("Bigger mill · cheaper kilo", S(42, 2) + 0.3, LE(42) + 2.0, 120, 640, "green", "sm", "up")
shot(c(43), "R_tanks", "none", ms=9.4)                             # "So you can guess who wins..."
shot(c(44), "PH_257336", "out", dim=0.2)                        # "And that's exactly where India's story turns."
# ---- HOW CHINA TOOK THE POWDER (5:43-7:23)
shot(c(45), "MPC", "slow", ms=19.8, dim=0.4)                       # "Now, here's what we got wrong." (H.A.'s workers at their own wall)
shot(S(45, 1) - PRE, "ETV", "crop2", ms=25.8, origin="45% 55%", dim=0.4)   # "...allowed only a few companies to make penicillin" (I.D.P.L.)
shot(S(45, 1) - PRE + 4.3, "Y04", "crop", ms=7.35, origin="50% 50%", dim=0.4, tag="FOOTAGE · ABP MAJHA · HINDUSTAN ANTIBIOTICS · TODAY")   # "...and only in small amounts" (H.A.)
shot(S(45, 2) - PRE, "HSN", "crop", ms=34.3, origin="50% 60%", dim=0.4)   # "So our plants stayed too small to be cheap."
chip("Few licences", L(45, 0.35), LE(45), 120, 300, "red", "sm", "up")
chip("Small plants", L(45, 0.6), LE(45), 120, 420, "red", "sm", "up")
cite("[MDPI ECONOMIES 2021]", L(45, 0.35), LE(45))
# China, owner-fetched news footage of its drug plants (round 6): mass lines on "went all in", CSPC's plant and a robot
# warehouse on "huge plants, in huge drug parks", the chimney kept only for "looser pollution rules". Tagged with their year
shot(c(46), "CCV", "crop", ms=43.1, origin="35% 70%")                # "Meanwhile, in the nineteen nineties, China went all in on medicine ingredients."
shot(c(47), "CGT", "y02", ms=39.4, origin="40% 45%")   # 1.6x keeps 13-77% of the height: the place caption (top) and subtitles (bottom) stay out               # "It built huge plants, in huge drug parks,"
shot(round(c(47) + 3.0, 3), "CCV", "crop", ms=22.4, origin="35% 70%")   # "...with cheap power and cheap water."
shot(S(47, 1) - PRE, "px_199788", "slow", ms=6.0)                    # "Its factories also faced looser pollution rules."
chip("Cheap power · cheap water", L(47, 0.3), LE(47), 120, 640, "amber", "sm", "up")
cite("[CFR | THE PHARMA CHOKE POINT]", L(47, 0.3), LE(47))
shot(c(48), "R_map_trade", "none", ms=9.0)                        # "And then cheap Chinese penicillin flooded the world market..."
shot(c(49), "D_budget1991-01", "in", dim=0.35, tag="DOCUMENT · BUDGET SPEECH 1991-92")                 # "Nineteen ninety-one — the year India opened up its economy..."
datebig("1991", "INDIA OPENS ITS ECONOMY", L(49, 0.05), LE(50))
# "Now remember this one number": the number becomes the hero (audit 2026-10-30), and comes back at 7:11
hero("<1%", "1991 · ALL MEDICINE POWDER IMPORTS · CHINA'S SHARE · RIS DP 268", S(49, 2) + 3.2, LE(50) + 1.0, 0.5)
# the roll call (r4 review: St Isaac's Cathedral, St Petersburg, was under "Hindustan Antibiotics"; out): the gears go
# quiet, then H.A.'s own wall with its workers protesting to save it (2015), I.D.P.L. Hyderabad's gate, the gears again
# the roll call (owner's review, 30 Oct: the names sat on stock gears): the skyline from 4:15, now six plants, goes quiet;
# H.A. and I.D.P.L. on their real places, each named and stamped there; then back to the skyline, where Torrent,
# Ranbaxy and Sarabhai go dark on their own names and Alembic last (scene clock = film time from line 51's cut)
shot(c(51), "R_skyline_dark", "none", ms=0.0)                        # "Then, one by one, the Indian penicillin plants went quiet."
shot(round(LE(51) + 0.3, 3), "MPC", "slow", ms=12.45, dim=0.4)     # "Hindustan Antibiotics. Stopped."
shot(c(53), "ETV", "crop2", ms=4.45, origin="45% 55%", dim=0.4)     # "I.D.P.L. Stopped."
shot(c(54), "R_skyline_dark", "none", ms=round(c(54) - c(51), 3))    # "Torrent. Ranbaxy. Sarabhai. Stopped." ... "Alembic. Stopped."
for name, ln, a, b in [("Hindustan Antibiotics", 52, round(LE(51) + 0.35, 3), c(53)), ("I.D.P.L.", 53, L(53), c(54))]:
    plate(name, "", a, b, 160, 230)
    stamp("STOPPED", round(LE(ln) - 0.35, 3), b, 1100, 235)
cite("[RIS DP 268 · ISID WP239]", L(52), LE(55) + 1.4)
shot(c(56), "px_23215", "slow", ms=[0.0, 11.0])   # two clean stretches of the port (r6 audit: a hazard-marked deck sat mid-clip)                            # "By about twenty twenty, India was importing all of that base powder"
chip("Base powder: 100% imported", L(56, 0.3), LE(56), 120, 640, "amber", "sm", "up")
cite("[ISID WP239]", L(56, 0.3), LE(56))
shot(c(57), "D_niti_p-40", "in", dim=0.6, tag="DOCUMENT · NITI AAYOG")   # "Remember that one per cent?... around eighty-six per cent."
# "Remember that one per cent?": the same "<1%" in the same place, then a match cut to "86%" on "eighty-six" (the low thud
# in make_sound.py sits on HERO86) and the capsule fills
hero("<1%", "1991 · ALL MEDICINE POWDER IMPORTS · CHINA'S SHARE · RIS DP 268", S(57, 0), HERO86, 0.5, cut_out=True)
hero("86%", "TODAY · ANTIBIOTIC POWDER IMPORTS · CHINA'S SHARE · NITI AAYOG 2025", HERO86, LE(57) + 0.8, 86.1, "amber", cut_in=True)
shot(c(58), "CCV", "crop", ms=18.8, origin="35% 70%", dim=0.3)      # "Niti Aayog estimates Chinese powder costs 35-40% less..." (Chinese packers)
# "So tell me — if you ran a company, would you build a plant here?": India's plants dark, then the empty Kakinada plot
shot(S(58, 1) - PRE, "R_skyline_dark", "push", ms=19.2)
shot(round(S(58, 1) - PRE + 1.8, 3), "Y02", "y02", ms=8.25, origin="35% 30%", tag="FOOTAGE · LYFIUS PHARMA · THE COAST SITE", hard=True)   # the span holds the shot, not a dissolve tail
chip("China's powder: 35–40% cheaper", L(58, 0.2), LE(58), 120, 160, "amber", "sm", "up")
cite("[NITI AAYOG ESTIMATE]", L(58, 0.2), LE(58))
# the trap on the tanks, steady (audit 2026-10-30: the handheld mill shook): small can't compete, big is a risk, and a
# price war stamps the big tank
shot(c(59), "R_tanks", "slow", ms=0.8)                              # "That's the trap. You can't compete without a big plant..."
chip("Small plant: can't compete", S(59, 1), LE(59) + 0.5, 120, 160, "red", "sm", "up")
chip("Big plant: big risk", S(59, 2), LE(59) + 0.5, 120, 260, "amber", "sm", "up")
stamp("PRICE WAR", round(LE(59) - 0.9, 3), LE(59) + 0.5, 1010, 470)
shot(c(60), "D_dgft_2020_noti50-1", "out", tag="DOCUMENT · DGFT")  # "Then Corona came — and India had to lock its own doors."
shot(c(61), "D_dop_pli_pressnote_2021-1", "in", origin="50% 72%", dim=0.35, tag="DOCUMENT · DEPT OF PHARMACEUTICALS · PRESS NOTE · DEC 2021")   # the scheme on its own paper, not a Western lab (audit 2026-10-30)   # "It launched a scheme..."
count(L(62, 0.5), LE(62), 120, 300, 0, 6940, L(62, 0.55), 1.2, "₹", " CRORE", "saffron", "")
chip("41 ingredients", L(62, 0.25), LE(62), 120, 460, "saffron", "sm", "up")
cite("[DEPT OF PHARMACEUTICALS | PLI 2020]", L(62, 0.25), LE(62))
shot(c(63), "R_map_india", "none", ms=3.6)                         # "And one company took the biggest bet of all."
# ---- KAKINADA SWITCHES IT BACK ON (the promised minute eight)
shot(c(64) - BEATS[63] + 0.2, "Y02", "y02", ms=[11.0, 42.0, 49.78], origin="35% 30%")   # the satellite zoom onto the coast              # (silence, then) "Kakinada, Andhra Pradesh. On the coast, a new plant..."
namelt("Kakinada, Andhra Pradesh", "LYFIUS PHARMA · AUROBINDO PHARMA", L(64, 0.1), L(64, 0.55))
shot(L(64, 0.58) - PRE, "D_aurobindo_lyfius_2024-1", "doc", origin="50% 32%", tag="DOCUMENT · AUROBINDO PHARMA · 29 OCT 2024")   # "built by Aurobindo Pharma, through its unit called Lyfius"
shot(c(65), "Y02", "y02", ms=[62.38, 67.74, 86.26], origin="35% 30%")             # "Inside are the giant tanks... the company says ₹2,500 crore... 15,000 tonnes"
chip("₹2,500 cr · company figure", L(65, 0.35), LE(65), 120, 160, "saffron", "sm", "up")
chip("15,000 tonnes a year", L(65, 0.7), LE(65), 120, 280, "saffron", "sm", "up")
shot(c(66), "Y02", "y02", ms=[52.66, 59.58, 80.98, 91.66, 33.0, 74.98], origin="35% 30%")             # "In twenty twenty-four, the tanks start running..."
datebig("2024", "PENICILLIN G · MADE IN INDIA AGAIN", L(66, 0.05), LE(66))
shot(c(67), "J_aerial", "out")   # cheap imports at an Indian port                           # "But you know the trap... cheap imports were still waiting at the port."
shot(c(68), "D_dgft_2026_mip-1", "in", tag="DOCUMENT · DGFT")      # "So on the twenty-ninth of January, 2026, the government stepped in."
datebig("29 JAN 2026", "MINIMUM IMPORT PRICE", L(68, 0.1), LE(69))
# the floor as a border gate; the amoxicillin and 6-APA lanes (scene 9.6 s) open on "The same rule covers..."
shot(c(69), "R_mipgate", "none", ms=round(max(0.0, 9.6 - (S(69, 2) - c(69))), 3))   # "It set a minimum price at the border..."
cite("[DGFT | 29 JAN 2026]", L(68, 0.1), LE(69))
shot(c(70), "R_fermenter_lit", "none", ms=4.0)                     # "Think of it as a shield..."
shot(c(71), "R_mipgate", "none", ms=10.4, dim=0.25)   # "below a fair price": the gate
shot(L(71, 0.5) - PRE, "R_map_trade", "none", ms=13.0, dim=0.2)   # "...whether China is selling penicillin here": the route in                 # "And in September 2026... below a fair price."
chip("Anti-dumping check · Sep 2026", L(71, 0.3), LE(71), 120, 540, "steel", "sm", "up")
chip("On Lyfius Pharma's application", L(71, 0.45), LE(71), 120, 640, "steel", "sm", "up")   # DGTR initiation 28 Sep 2026 (P63 note)
cite("[DGTR | 28 SEP 2026]", L(71, 0.3), LE(71))
shot(c(72), "R_fermenter_lit", "none", ms=round(4.0 + c(71) - c(70), 3))   # the Kakinada tank keeps its own clock running                  # "But that shield has an end date... January 2027."
datebig("JAN 2027", "THE SHIELD ENDS", L(72, 0.5), LE(73))
shot(c(73), "D_dgft_2026_mip-2", "doc", origin="50% 58%", tag="DOCUMENT · DGFT")   # "the date to watch": "a period of one year"                                # "That's the date to watch..."
shot(c(74), "Y02", "y02", ms=[86.26, 93.42], origin="35% 30%")            # "And here's the balance the government has to strike..."
chip("Protect the plant", L(74, 0.4), LE(74), 120, 160, "saffron", "sm", "up")
chip("Keep medicines affordable", L(74, 0.7), LE(74), 120, 280, "green", "sm", "up")
# a scheme-wide figure on the scheme's own report, not over one company's plant (audit 2026-10-30); the headline carries the number
shot(c(75), "D_psuwatch_pli_2026_169", "in", tag="DOCUMENT · PSU WATCH · JUNE 2026")   # "And it's not just penicillin... five thousand crore"
cite("[DEPT OF PHARMACEUTICALS | JUNE 2026]", L(75, 0.45), LE(75))
shot(c(76), "R_map_india", "none", ms=6.5)                         # "Three giant bulk drug parks... Nakkapalli... same state"
shot(c(77), "R_map_india", "none", ms=9.0)   # "none of those parks": the park pins                       # "None of those parks is up and running yet..."
chip("None running yet", L(77, 0.25), LE(77), 120, 640, "red", "sm", "up")
shot(c(78), "Y02", "y02", ms=[97.74, 65.62], origin="35% 30%")            # "So has India won? Not yet. But it's back in the fight."
# ---- RULE, RUIN, REALITY + WHAT IT MEANS FOR YOU
shot(c(79), "R_chain_lesson", "none", ms=0.0)   # the lesson as the chain: India's last link, China's before it, the joint cracks (audit 2026-10-30)   # "So here's the lesson..."
shot(c(80), "D_dgft_2020_noti50-1", "in", tag="DOCUMENT · DGFT")  # "And the cost? You saw it in the Corona days..."
shot(c(81), "px_262464", "slow", ms=9.0, dim=0.2, tag="PIXABAY · ILLUSTRATIVE")   # "the reality today. India has the scientists."
shot(S(81, 2) - PRE, "Y02", "y02", ms=76.86, origin="35% 30%")   # "It has the factories.": a Lyfius worker in a hard hat (the 7:22 clip stood for China; audit 2026-10-30)
shot(S(81, 3) - PRE, "Y02", "y02", ms=[86.26, 59.58], origin="35% 30%")   # "And now, it's growing its own penicillin again."             # "But here's the reality today..."
shot(c(82), "PH_1540220", "in")                                 # "So what does this mean for you? Keep taking your medicines..."
shot(c(84), "R_capsule_open", "push", ms=3.6)                      # "But the next time you take an antibiotic... began in China."
shot(c(85), "R_map_home", "none", ms=0.8)                          # "And if the plant in Kakinada wins... right here in India."
shot(c(86), "R_map_home", "out", ms=6.0, dim=0.5)                  # "Medicines aren't the only missing piece... India's own A.I.?"
chip("Next: India's own A.I.", L(86, 0.5), END, 120, 160, "steel", "", "up")
shot(c(87), "endcard", "push", tag="")                             # pinned question, channel line, end screen
chip("Which medicine should India make fully?", L(87, 0.2), END, 120, 290, "saffron", "sm", "up")


# ---------- captions from the sentence timings (film time) ----------
def captions():
    out = []
    for r in SENTS:
        a, b, text = F(r["start"]), F(r["end"]), r["en"]
        parts, cur = [], ""
        for w in re.split(r"(?<=[,—?])\s+|\s+(?=—)", text):
            if cur and len(cur) + len(w) > 46:
                parts.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        parts.append(cur)
        split = []
        for q in parts:
            while len(q) > 96:
                mid = q.rfind(" ", 0, len(q) // 2 + 8); split.append(q[:mid]); q = q[mid + 1:]
            split.append(q)
        tot = sum(len(p) for p in split); t = a
        for n, p in enumerate(split):
            d = (b - a) * len(p) / tot
            out.append((round(t, 2), round(t + d, 2), esc(p))); t += d
    # hold each caption until its words are over, then fade (review: captions faded out mid-word): run on 0.35 s,
    # but never into the next caption
    held = []
    for i, (a, b, p) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else b + 1.0
        held.append((a, round(max(b, min(b + 0.35, nxt - 0.03)), 2), p))
    return held


def film_vo():
    """voice/vo_film.wav: the joined VO with the BEATS silences inserted"""
    src = P / "voice/vo_full.wav"; out = P / "voice/vo_film.wav"
    pts = [0.0] + [cut for cut, _ in CUTS]
    filt, labels = [], []
    for i, a in enumerate(pts):
        b = pts[i + 1] if i + 1 < len(pts) else None
        trim = f"atrim=start={a}" + (f":end={b}" if b is not None else "")
        pad = f",apad=pad_dur={CUTS[i][1]}" if b is not None else ""
        filt.append(f"[0:a]{trim},asetpts=PTS-STARTPTS{pad}[s{i}]"); labels.append(f"[s{i}]")
    # two short voiced bursts 8-10 dB under the word just before them, heard by the r4 reviewer's transcriber as "them.
    # them." (0:50.8) and "and and" (8:21.5): a breath or a soft repeat either way, so the edit lowers them 24 dB
    duck = ",".join(f"volume=enable='between(t,{x:.3f},{y:.3f})':volume=0.063" for x, y in
                    [(LE(6) - 0.16, LE(6) + 0.1), (L(65) + 6.56, L(65) + 6.92)])
    filt.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1,{duck},apad=whole_dur={END}[o]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter_complex", ";".join(filt), "-map", "[o]",
                    "-ar", "48000", "-ac", "1", str(out)], check=True)
    return out


def r3(x):
    return round(x, 3)


def probe(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True, check=True).stdout)


def part_bounds(n=5):
    starts = [s["t0"] for s in SEQ[1:]]
    b = [0.0]
    for k in range(1, n):
        b.append(min(starts, key=lambda x: abs(x - END * k / n)))
    return b + [END]


RESET = 4.6   # longest hold before a visual reset (CLAUDE.md: every 3.5-5.0 s)
# framings a split piece cuts to: (move, origin); documents read down the page, footage alternates punch-ins
FRAMES = {"doc": [("doc", "50% 28%"), ("doc", "50% 52%"), ("doc", "50% 76%")],
        "crop": [("crop2", "28%"), ("crop", "50%"), ("crop2", "72%")],   # x only: each shot keeps its own height
        "y02": [("y02", "25% 30%"), ("y02", "60% 30%"), ("y02", "42% 30%")],
        "anim": [("cutB", "50% 50%"), ("push", "50% 50%")],
        "foot": [("cutA", "32% 38%"), ("cutB", "68% 58%"), ("cutA", "62% 34%"), ("cutB", "36% 62%")]}


SPLIT_R = {"R_tablet", "R_tanks"}   # renders whose long holds sit still (freezedetect), centred so a punch-in keeps the labels


def split_long():
    """Cut every hold over RESET into near-equal pieces, each with a new framing (one change per cut). Video keeps
    running (or jumps to the next in-point when a shot lists several); animated renders and the end card move on their
    own and are left whole."""
    out = []
    for s, nxt in zip(SEQ, SEQ[1:] + [dict(t0=END)]):
        d = nxt["t0"] - s["t0"]; ms = s["ms"]
        if d <= RESET + 0.4 or (s["src"].startswith("R_") and s["src"] not in SPLIT_R) or s["src"] == "endcard":
            out.append(dict(s, ms=ms[0] if isinstance(ms, list) else ms)); continue
        n = math.ceil(d / RESET); step = d / n
        kind = "y02" if s["src"] == "Y02" else "anim" if s["src"] in SPLIT_R or s["src"].endswith("_169") else "doc" if s["src"].startswith("D_") else "crop" if s["move"] == "crop" else "foot"
        for k in range(n):
            p = dict(s, t0=r3(s["t0"] + k * step))
            p["ms"] = ms[k] if isinstance(ms, list) and k < len(ms) else (
                (ms[-1] if isinstance(ms, list) else ms) + (k - (len(ms) - 1 if isinstance(ms, list) else 0)) * step)
            p["ms"] = r3(p["ms"])
            if k:
                p["move"], p["origin"] = FRAMES[kind][(k - 1) % len(FRAMES[kind])]
                if kind == "crop" and s["src"] != "Y02":
                    p["origin"] += " " + (s["origin"] or "50% 50%").split()[1]
            out.append(p)
    SEQ[:] = out


# Clean source ranges, checked frame by frame (owner's review, 2026-10-29): a piece of third-party footage may only play
# inside one of these, so it never shows a few frames of the promo's own next shot (the "flash frames"), the Prime
# Minister and PLI slides (Y02 17-32 s), title cards, lower-third boxes or the press meet (Y04 from 19 s).
CLEAN = {
    # Y02 is always framed with "y02" below (1.45x from 35% 35%): the bottom 20% (lower-third boxes) and top 11% (the
    # Lyfius logo) stay out of frame, so only titles, the PM/PLI slides (17-32 s), the white fade (79-80 s) and the
    # collage and group shots (103-108 s) need excluding; spans run 0.1 s clear of the promo's own cuts
    # 30 Oct audit: the promo also cross-wipes inside these (3-4 frame wipes scdet missed); spans split at every
    # frame-difference transition of the conformed source (peak > 25), mapped to raw time (x1.2)
    "Y02": [(8.2, 10.95), (11.0, 13.9), (33.0, 34.9), (42.32, 49.58), (49.78, 52.46), (52.66, 55.7), (57.18, 59.38), (59.58, 62.18), (62.38, 65.42), (65.62, 67.54), (67.74, 71.42), (71.62, 72.86), (73.06, 74.78), (74.98, 76.66), (77.48, 78.8), (80.98, 82.14), (82.34, 83.42), (83.62, 84.96), (86.26, 87.68), (88.12, 90.02), (90.22, 91.46), (91.66, 93.22), (93.42, 95.82), (96.02, 97.54), (97.74, 99.48), (99.92, 101.38), (101.58, 102.8)],
    "Y04": [(6.05, 7.25), (7.35, 10.3), (10.45, 14.1), (14.25, 19.05)],
    # round 5 sources: spans between their own cuts (scdet 12), 0.1 s clear; Cipla's only where no caption is burned in
    "MPC": [(12.37, 18.7), (20.3, 25.95)],   # the source dissolves 18.9-20.2 "ETV": [(4.34, 9.5), (25.7, 30.94)],
    "HSN": [(26.98, 34.1), (34.3, 39.58), (39.78, 45.82)],
    "CIP": CIP_SPANS,
    "CCV": [(10.9, 14.78), (14.98, 18.58), (18.78, 22.18), (22.38, 25.63), (25.83, 28.98), (32.78, 34.23), (43.07, 46.38), (46.58, 49.87), (50.07, 52.18)],
    "CGT": [(39.38, 43.02), (43.22, 46.46)],
    "ICI": [(559.1, 564.5), (572.56, 577.54), (581.42, 587.58), (531.0, 537.9)],   # the vials (526.7-531 is the lab notebook)
}
FPS = 30


_RATE = {}


def rate(src):
    """source frames per second when its conform exists, else 30: the conform plays each source frame once at 30 fps, so
    1 film second uses 30/rate source seconds, and source time t sits at t * rate/30 in the conformed file"""
    if src not in _RATE:
        r = 30.0
        if media(src).parent.name == "conformed":
            n, d = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                                   "-of", "csv=p=0", str(media(src, raw=True))], capture_output=True, text=True).stdout.strip().split("/")
            r = int(n) / int(d)
        _RATE[src] = r
    return _RATE[src]


def clean_ranges(src):
    """CLEAN, else the spans between the source's own cuts (assets/cuts/<name>.txt from scdet), 0.1 s clear of each cut."""
    if src in CLEAN:
        return CLEAN[src]
    m = media(src, raw=True)
    cf = A / "cuts" / (m.stem + ".txt")
    if m.suffix != ".mp4" or not cf.exists():
        return None
    cuts = [float(x) for x in cf.read_text().split()]
    if not cuts:
        return None
    edges = [0.0] + cuts + [probe(m)]
    return [(a + (0.1 if a else 0), b - 0.1) for a, b in zip(edges, edges[1:]) if b - a > 0.6]


def clean_assign():
    """Place every footage piece inside clean spans, using footage not yet used where possible (no repeats).
    A piece takes the unused window nearest its requested in-point; when no unused window holds it whole, it becomes
    2 or 3 cuts of at least 1.5 s, each in its own unused window (the promo cuts every 1-3 s, so its spans are short)."""
    used, out = {}, []

    def overlap(src, a, b):
        return sum(max(0.0, min(b, y) - max(a, x)) for x, y in used.get(src, []))

    def best(src, rs, need, want):
        cands = []
        for a, b in rs:
            if b - a < need:
                continue
            x = a
            while x + need <= b + 1e-6:
                cands.append((overlap(src, x, x + need) * 10 + abs(x - want) * 0.02, x)); x += 0.25
        return min(cands) if cands else None

    for i, s in enumerate(SEQ):
        rs = clean_ranges(s["src"])
        end = SEQ[i + 1]["t0"] if i + 1 < len(SEQ) else END
        if not rs:
            out.append(s); continue
        sp = 30.0 / rate(s["src"])
        nxt = SEQ[i + 1] if i + 1 < len(SEQ) else None
        tail = XF if nxt is not None and not (s.get("hard") or nxt.get("hard")) else 0.0
        film = end - s["t0"]
        plan = None                                           # (repeat seconds + a small price per extra cut, sub, starts)
        for n in (1, 2, 3, 4):
            sub = film / n
            if n > 1 and sub < 1.3:
                break
            picks = []
            for k in range(n):
                c = best(s["src"], rs, (sub + tail) * sp, s["ms"] + k * 2.0)
                if c is None:
                    break
                picks.append(c[1]); used.setdefault(s["src"], []).append((c[1], c[1] + sub * sp))
            rep = sum(overlap(s["src"], x, x + sub * sp) - sub * sp for x in picks) if len(picks) == n else None
            for _ in picks:                                   # undo; the chosen plan is re-added below
                used[s["src"]].pop()
            if rep is not None and (plan is None or rep + 0.4 * (n - 1) < plan[0]):
                plan = (rep + 0.4 * (n - 1), sub, picks)
        if plan is None:
            plan = (0, film, [rs[0][0]])
        _, sub, starts = plan
        for x in starts:
            used.setdefault(s["src"], []).append((x, x + sub * sp))
        for k, x in enumerate(starts):
            p = dict(s, t0=r3(s["t0"] + k * sub), ms=r3(x))
            if k and s["src"] == "Y02":
                p["move"], p["origin"] = FRAMES["y02"][k % 3]
            out.append(p)
    SEQ[:] = out


def snap_frames():
    """Every cut and in-point on a whole 1/30 s frame (the half-frame offsets showed as one-frame slivers)."""
    for s in SEQ:
        s["t0"] = round(round(s["t0"] * FPS) / FPS, 4)
        if media(s["src"]).suffix == ".mp4":
            s["ms"] = s["ms"] * rate(s["src"]) / 30.0     # source time -> conformed time
        s["ms"] = round(round(s["ms"] * FPS) / FPS, 4)


def write_srt(caps):
    """YouTube captions in this cut's own time (review: the align SRT was in raw-VO time, up to 14 s off the film)."""
    def ts(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"
    rows = [f"{i}\n{ts(a)} --> {ts(b)}\n{html.unescape(t)}\n" for i, (a, b, t) in enumerate(caps, 1)]
    (P / "youtube").mkdir(exist_ok=True)
    (P / "youtube/subtitles.en.srt").write_text("\n".join(rows), encoding="utf-8")


def emit():
    SEQ.sort(key=lambda s: s["t0"])
    split_long()
    clean_assign()
    snap_frames()
    for s, nxt in zip(SEQ, SEQ[1:] + [dict(t0=END)]):
        s["t1"] = nxt["t0"]
        assert s["t1"] - s["t0"] > 0.4, (s["src"], s["t0"], s["t1"])
        m = media(s["src"])
        if m.suffix == ".mp4":
            need = s["ms"] + s["t1"] - s["t0"]
            have = probe(m)
            if need > have + 0.05:
                print(f"  ! {s['src']} needs {need:.1f}s, has {have:.1f}s (t={s['t0']:.1f}): the last frame will hold")
    caps = captions(); PARTS = part_bounds()
    for k in range(len(PARTS) - 1):
        emit_part(f"p{k + 1}", PARTS[k], PARTS[k + 1], caps)
    (P / "build/parts.json").write_text(json.dumps(PARTS))
    write_srt(caps)
    film_vo()
    print(f"film {END:.1f}s ({int(END // 60)}:{END % 60:04.1f}); Kakinada at {L(64):.1f}s ({int(L(64) // 60)}:{L(64) % 60:04.1f}); "
          f"{len(SEQ)} shots, {len(OV)} overlays")


def seam_sliver(a, b, t0, t1):
    """Kept for reference: items crossing a seam are no longer dropped, they cut in and out at the seam instead
    (round 5: a dropped caption sliver and fades on both sides of a seam read as a 2-3 frame dip)."""
    return False


def seam_cut(h, a, b, t0, t1):
    """an overlay that continues from the previous part appears at once; one that continues into the next leaves at once"""
    if a < t0 - 1e-6:
        h = re.sub(r'data-fx="[^"]*"', 'data-fx="cut"', h, count=1)
    if b > t1 + 1e-6:
        h = h.replace("<div ", "<div data-cut ", 1)
    return h


def emit_part(pid, t0, t1, caps):
    # the part's length floored onto its last frame: r3() rounded p1 up to 136.667 s and the renderer made a 4101st,
    # empty frame (a one-frame blank at the seam, and every later part 1 frame late against the voice; round 5)
    D = FF.ft(round(t1 * FPS) - round(t0 * FPS)); d = OUTV / pid
    shutil.rmtree(d / "media", ignore_errors=True); (d / "media").mkdir(parents=True, exist_ok=True)
    shutil.copytree(OUTV / "_shared", d / "shared", dirs_exist_ok=True)
    shutil.copy(ROOT / "assets/brand/logo_square.png", d / "media/logo_square.png")
    loc = lambda x: r3(x - t0)
    H = []
    part = [x for x in SEQ if t0 - 1e-6 <= x["t0"] < t1 - 1e-6]
    for i, s in enumerate(part):
        # start and end floored onto their frames (frame_floor.py): rounded up, the cut frame showed the empty background
        fs, fe = round(s["t0"] * FPS) - round(t0 * FPS), round(s["t1"] * FPS) - round(t0 * FPS)
        # the dissolve: the incoming shot fades in over XF while the outgoing one runs XF longer beneath it; none at a
        # part's first frame (nothing of this part lies under it) and none into or out of a hard shot
        prev, nxt = (part[i - 1] if i else None), (part[i + 1] if i + 1 < len(part) else None)
        soft_in = fs > 0 and prev is not None and not (prev.get("hard") or s.get("hard"))
        soft_out = nxt is not None and not (s.get("hard") or nxt.get("hard"))
        fe += round(XF * FPS) if soft_out else 0
        st, du = FF.ft(fs), round(FF.ft(fe) - FF.ft(fs), 4); src = media(s["src"])
        xf = f' data-xf="{XF}"' if soft_in else ""
        fn = f"media/{src.name}"
        if not (d / fn).exists():
            shutil.copy(src, d / fn)
        tag = f'<div class="tag">{esc(s["tag"])}</div>' if s["tag"] else ""
        org = f' data-origin="{s["origin"]}"' if s["origin"] else ""
        dim = ("" if not s["dim"] else '<div class="dim"></div>' if s["dim"] is True
               else f'<div class="dim" style="background:rgba(4,18,21,{s["dim"]})"></div>')
        if src.suffix == ".mp4":
            H.append(f'      <div id="{pid}-s{i}" class="shot"{xf} data-vs="{st}" data-vd="{du}" style="visibility:hidden"><video id="{pid}-v{i}" class="m" src="{fn}" muted playsinline '
                     f'data-move="{s["move"]}"{org} data-start="{st}" data-duration="{du}" data-media-start="{s["ms"]}" data-track-index="2" data-volume="0"></video></div>')
            H.append(f'      <div class="vover"{xf} data-vs="{st}" data-vd="{du}" style="visibility:hidden">{dim}{tag}</div>')
        else:
            fit = ' style="object-fit:contain;background:#071a1e"' if s["src"].startswith("D_") or s["src"] == "endcard" else ""
            H.append(f'      <div id="{pid}-s{i}" class="shot"{xf} data-start="{st}" data-duration="{du}" data-track-index="1">'
                     f'<img class="m a" src="{fn}" alt=""{fit} data-move="{s["move"]}"{org} />{dim}{tag}</div>')
    O = []
    for o in OV:
        a, b = o["at"], o["to"] if o["to"] is not None else END
        if b <= t0 or a >= t1 or seam_sliver(a, b, t0, t1):
            continue
        h = re.sub(r'(data-(?:at|to)=")([\d.]+)"', lambda mm: f'{mm.group(1)}{min(D, max(0.0, loc(float(mm.group(2)))))}"', o["h"])
        h = re.sub(r'(data-count="[\d.]+,[\d.]+,)([\d.]+)', lambda mm: f'{mm.group(1)}{max(0.0, loc(float(mm.group(2))))}', h)
        O.append("      " + seam_cut(h, a, b, t0, t1))
    cap = "\n".join(seam_cut(f'      <div class="cap" data-at="{max(0.0, loc(a))}" data-to="{min(D, loc(b))}" data-fx="fade" data-d="0.12">{c}</div>', a, b, t0, t1)
                    for a, b, c in caps if b > t0 and a < t1)
    (d / "index.html").write_text(PAGE.format(pid=pid, D=D, shots="\n".join(H), ov="\n".join(O), cap=cap))
    print(f"{pid}: {t0:.1f}-{t1:.1f} ({D:.1f}s) {sum(1 for x in SEQ if t0 - 1e-6 <= x['t0'] < t1 - 1e-6)} shots, {len(O)} overlays")


PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Pharma film: {pid}</title>
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/pha.css" />
    <script src="shared/pha.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-ext-800-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2212, U+2013; }}
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-ext-600-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2212, U+2013; }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 700; src: url("vendor/fonts/jetbrains-mono-latin-700-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 800; src: url("vendor/fonts/jetbrains-mono-latin-800-normal.woff2") format("woff2"); }}
    </style>
  </head>
  <body>
    <!-- Generated by projects/pharma-apis/build/make_film.py. Edit that, not this file. -->
    <div id="root" data-composition-id="{pid}" data-start="0" data-width="1920" data-height="1080" data-duration="{D}">
{shots}
      <div class="grade" style="z-index:15"></div>
{ov}
{cap}
      <img class="bug" src="media/logo_square.png" alt="Be Practical with Kishore" />
      <canvas id="grain" width="500" height="290"></canvas>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      PHA_animate(tl, {D});
      window.__timelines["{pid}"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    emit()
