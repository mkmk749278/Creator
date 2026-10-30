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
         60: 1.0, 63: 1.5, 3: 0.6, 11: 0.4}
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
    "CNa": ("cns_wuhan_aerial_20200126.mp4", "CHINA NEWS SERVICE · WUHAN · 26 JAN 2020 · CC BY 4.0"),
    "CNs": ("cns_wuhan_streets_20200126.mp4", "CHINA NEWS SERVICE · WUHAN · 26 JAN 2020 · CC BY 4.0"),
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


def shot(t0, src, move="push", tag=None, ms=0.0, origin=None, dim=False):
    """a base shot from t0 until the next shot starts (the cut is gapless by construction)"""
    SEQ.append(dict(t0=round(t0, 3), src=src, move=move, tag=default_tag(src) if tag is None else tag, ms=ms, origin=origin, dim=dim))


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


def hero(num, key, at, to, pct, col="steel"):
    """the film's two numbers as heroes (audit 2026-10-30: they lived only in a small corner gauge): one big number centre
    screen over a capsule bar that fills to China's share, its base underneath; the same place and size every time, so
    "<1%" can match-cut to "86%"."""
    w = max(0.6, pct)
    el(f'<div class="hero c-{col}" {attrs(at, to, "fade", 0.25)}><div class="num">{esc(num)}</div>'
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
shot(c(13), "px_45675", "slow", ms=1.0)                            # "First, let's give India its due..."
shot(c(14), "D_msf2001-01", "in", tag="DOCUMENT · MSF · 2001")   # the 2001 ARV price report, not a microscope                         # "Think back to two thousand one. H.I.V. ... ten thousand dollars"
# the price drop to scale: the pile of $100 notes collapses (scene 10.0 s) exactly as the $350 card lands
shot(S(14, 2) - PRE, "R_cipla", "none", ms=round(max(0.0, 10.0 - (L(15, 0.55) - (S(14, 2) - PRE))), 3))   # "The medicines exist... a dollar a day... One dollar."
datebig("2001", "H.I.V. MEDICINES", L(14, 0.05), c(17))
# same unit on both cards (owner's review, 2026-10-29): MSF 7 Feb 2001, "about $10,400" in the US vs Cipla's "$350 per year" (P14, P15)
count(L(14, 0.6), c(17), 230, 250, 0, 10400, L(14, 0.62), 1.3, "$", " / YEAR", "red", "xl")
chip("Western price", L(14, 0.75), c(17), 236, 382, "red", "sm", "up")
count(L(15, 0.5), c(17), 230, 470, 0, 350, L(15, 0.55), 0.9, "$", " / YEAR", "green", "xl")
chip("Cipla · under $1 a day", L(15, 0.7), c(17), 236, 602, "green", "sm", "up")
cite("[MSF | 2001]", L(14, 0.6), c(17))
shot(c(17), "J_seaside", "left")   # JNPT from the sea                            # "And today... more than two and a half lakh crore rupees a year."
count(L(17, 0.4), LE(17), 120, 640, 0, 2.5, L(17, 0.45), 1.2, "₹", " LAKH CRORE+", "ink", "", 1)
cite("[PIB | EXPORTS 2024-25]", L(17, 0.4), LE(17))
shot(c(18), "R_tablet", "none", ms=1.0)   # skip the empty first second                            # "Every tablet has two parts." ... coating, strip, box
shot(c(21), "px_45682", "slow", ms=1.0)                            # "Indian companies are world class at that last part."
shot(c(22), "PH_1851178", "in")                         # "But the powder you swallow?"
shot(c(23), "D_niti_cover-01", "in", tag="DOCUMENT · NITI AAYOG")  # "In 2025, India bought these powders... sixty-five thousand crore"
count(L(23, 0.5), LE(23), 120, 640, 0, 65000, L(23, 0.55), 1.4, "₹", " CRORE · 2025", "amber", "sm")
cite("[NITI AAYOG $7.4 BN | OUR CONVERSION]", L(23, 0.5), LE(23))
shot(c(24), "R_map_trade", "none", ms=3.0)   # no Hubei here: the route lands at Indian ports                        # "And the biggest seller, by far... China."
shot(c(25), "D_niti_p-40", "in", dim=0.55, tag="DOCUMENT · NITI AAYOG")   # "And if you look at antibiotics... about eighty-six went to China."
coins(L(25, 0.45), LE(25))
gauge(L(25, 0.75), LE(25), 86.1, "TODAY · ANTIBIOTIC POWDER IMPORTS · CHINA'S SHARE", "NITI AAYOG · 2025")
cite("[NITI AAYOG | TRADE WATCH Q4 FY26]", L(25, 0.4), LE(25))
shot(c(26), "PH_1853400", "in", dim=0.15)   # tablets, not a pipette robot                           # "Even your fever tablet has a China link..."
chip("Raw chemical: para-aminophenol", L(26, 0.6), LE(26), 120, 640, "amber", "sm", "up")   # P25: PAP, a big share from China
cite("[INDUSTRY REPORTS]", L(26, 0.6), LE(26))
# ---- INDIA MADE ITS OWN PENICILLIN (3:16-4:19)
shot(c(27), "PH_1851178", "out")                                    # "So you might be thinking — has it always been like this?"
shot(c(29), "W_L0032175", "in")   # an archive drawing carries 1954 (the HAL wall footage is today)              # "Pimpri, near Pune. Nineteen fifty-four..."
datebig("1954", "PIMPRI · NEAR PUNE", L(29, 0.05), LE(29))
shot(c(30), "W_L0012314", "out")                                   # "Penicillin was the miracle drug of that time..."
chip("Miracle drug", L(30, 0.1), LE(30) + 2.0, 120, 640, "green", "", "up")
shot(c(31), "Y04", "crop", ms=[14.25, 7.35], origin="50% 50%", tag="FOOTAGE · ABP MAJHA · TODAY")             # "The government sets up... Hindustan Antibiotics. By 1956..."
namelt("Hindustan Antibiotics", "PIMPRI · SET UP 1954 · PENICILLIN BY 1956", L(31, 0.15), LE(31))
cite("[DEPT OF PHARMACEUTICALS | HAL]", L(31, 0.15), LE(31))
shot(c(32), "R_map_india", "none", ms=0.0)                         # "Just think about it. Picture your grandparents' India..."
shot(S(32, 2) - PRE, "W_L0012314", "out")   # "A young, poor country, growing... in its own factory" (penicillin production apparatus, archival)
shot(c(33), "px_262464", "slow", ms=1.0, dim=0.2, tag="PIXABAY · ILLUSTRATIVE · TODAY")                  # "Soon, others join in — Alembic, Sarabhai and Ranbaxy..."
plate("Alembic", "", L(33, 0.35), LE(33), 160, 300); plate("Sarabhai", "", L(33, 0.45), LE(33), 560, 300); plate("Ranbaxy", "", L(33, 0.55), LE(33), 1000, 300)
shot(c(34), "R_fermenter", "push", ms=0.0)                         # "How do you actually make penicillin?"
# ---- WHY PENICILLIN IS A SCALE GAME (4:19-5:43)
shot(c(35), "px_197486", "slow", ms=4.0)                           # "Many medicines, like paracetamol, are cooked from chemicals..."
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
shot(c(39), "px_40948", "slow", ms=0.5, dim=0.4)                   # "Next, it's turned into a smaller base powder..."
shot(S(39, 2) - PRE, "PXb", "slow", ms=10.0, dim=0.3)              # "From that base, factories make amoxicillin..."
chip("Penicillin G", L(39, 0.05), LE(39), 120, 300, "green", "sm", "left")
chip("→ The base (6-A.P.A.)", L(39, 0.3), LE(39), 120, 420, "steel", "sm", "left")
chip("→ Amoxicillin", L(39, 0.75), LE(39), 120, 540, "ink", "sm", "left")
shot(c(40), "R_tanks", "none", ms=0.5)                             # "A bigger tank makes the powder cheaper. Much cheaper."
shot(c(42), "Y06", "slow", ms=4.0)                                 # "Think of a flour mill. A big chakki grinds each kilo cheaper..."
chip("Small chakki", L(42, 0.1), S(42, 2), 120, 640, "steel", "sm", "up")
shot(S(42, 2) - PRE, "Y05", "crop", ms=1.0, origin="50% 10%")     # "Double your tank, and your costs don't double... but your output does."
chip("Bigger mill · cheaper kilo", S(42, 2) + 0.3, LE(42) + 2.0, 120, 640, "green", "sm", "up")
shot(c(43), "R_tanks", "none", ms=9.4)                             # "So you can guess who wins..."
shot(c(44), "PH_257336", "out", dim=0.2)                        # "And that's exactly where India's story turns."
# ---- HOW CHINA TOOK THE POWDER (5:43-7:23)
shot(c(45), "px_45677", "slow", ms=[0.2, 4.6, 1.2], dim=0.4)    # "Now, here's what we got wrong... only a few companies"
chip("Few licences", L(45, 0.35), LE(45), 120, 300, "red", "sm", "up")
chip("Small plants", L(45, 0.6), LE(45), 120, 420, "red", "sm", "up")
cite("[MDPI ECONOMIES 2021]", L(45, 0.35), LE(45))
shot(c(46), "px_199788", "slow", ms=0.0)                            # "Meanwhile, in the nineteen nineties, China went all in..."
chip("Cheap power · cheap water", L(47, 0.3), LE(47), 120, 640, "amber", "sm", "up")
cite("[CFR | THE PHARMA CHOKE POINT]", L(47, 0.3), LE(47))
shot(c(48), "R_map_trade", "none", ms=9.0)                        # "And then cheap Chinese penicillin flooded the world market..."
shot(c(49), "D_budget1991-01", "in", dim=0.35, tag="DOCUMENT · BUDGET SPEECH 1991-92")                 # "Nineteen ninety-one — the year India opened up its economy..."
datebig("1991", "INDIA OPENS ITS ECONOMY", L(49, 0.05), LE(50))
# "Now remember this one number": the number becomes the hero (audit 2026-10-30), and comes back at 7:11
hero("<1%", "1991 · ALL MEDICINE POWDER IMPORTS · CHINA'S SHARE · RIS DP 268", S(49, 2) + 3.2, LE(50) + 1.0, 0.5)
shot(c(51), "px_212001", "slow", ms=[0.0, 3.6, 7.2], dim=0.55)
shot(c(54), "px_212000", "slow", ms=[0.0, 3.8, 7.6], dim=0.55)   # the roll call over still gears (no people under the stamps)    # "Then, one by one, the Indian penicillin plants went quiet."
for i, (name, ln) in enumerate([("Hindustan Antibiotics", 52), ("I.D.P.L.", 53), ("Torrent · Ranbaxy · Sarabhai", 54), ("Alembic", 55)]):
    plate(name, "", L(ln), LE(55) + 1.4, 160, 230 + i * 160)   # clear of the logo bug (top right)
    stamp("STOPPED", round(LE(ln) - 0.35, 3), LE(55) + 1.4, 1100, 235 + i * 160)
cite("[RIS DP 268 · ISID WP239]", L(52), LE(55) + 1.4)
shot(c(56), "px_23215", "slow", ms=4.0)                            # "By about twenty twenty, India was importing all of that base powder"
chip("Base powder: 100% imported", L(56, 0.3), LE(56), 120, 640, "amber", "sm", "up")
cite("[ISID WP239]", L(56, 0.3), LE(56))
shot(c(57), "D_niti_p-40", "in", dim=0.6, tag="DOCUMENT · NITI AAYOG")   # "Remember that one per cent?... around eighty-six per cent."
# "Remember that one per cent?": the same "<1%" in the same place, then a match cut to "86%" on "eighty-six" (the low thud
# in make_sound.py sits on HERO86) and the capsule fills
hero("<1%", "1991 · ALL MEDICINE POWDER IMPORTS · CHINA'S SHARE · RIS DP 268", S(57, 0), HERO86, 0.5)
hero("86%", "TODAY · ANTIBIOTIC POWDER IMPORTS · CHINA'S SHARE · NITI AAYOG 2025", HERO86, LE(57) + 0.8, 86.1, "amber")
shot(c(58), "px_45680", "slow", ms=[0.0, 2.9], dim=0.45, tag="PIXABAY · ILLUSTRATIVE")                # "Niti Aayog estimates Chinese powder costs 35-40% less..."
shot(S(58, 1) - PRE, "px_199788", "in", ms=6.0, dim=0.45)           # "So tell me — if you ran a company, would you build a plant here?"
chip("China's powder: 35–40% cheaper", L(58, 0.2), LE(58), 120, 160, "amber", "sm", "up")
cite("[NITI AAYOG ESTIMATE]", L(58, 0.2), LE(58))
shot(c(59), "Y05", "crop", ms=8.0, origin="50% 10%")   # the big mill again, not the same COST OF EACH KILO frame                            # "That's the trap..."
shot(c(60), "D_dgft_2020_noti50-1", "out", tag="DOCUMENT · DGFT")  # "Then Corona came — and India had to lock its own doors."
shot(c(61), "px_45682", "slow", ms=6.0, dim=0.6)                   # "And this time, the central government decided to break the trap."
shot(c(62), "px_197486", "slow", ms=1.0, dim=0.65)                 # "It launched a scheme..."
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
shot(c(66), "Y02", "y02", ms=[97.74, 59.58], origin="35% 30%")             # "In twenty twenty-four, the tanks start running..."
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
shot(c(75), "D_psuwatch_pli_2026", "in", tag="DOCUMENT · PSU WATCH · JUNE 2026")   # "And it's not just penicillin... five thousand crore"
cite("[DEPT OF PHARMACEUTICALS | JUNE 2026]", L(75, 0.45), LE(75))
shot(c(76), "R_map_india", "none", ms=6.5)                         # "Three giant bulk drug parks... Nakkapalli... same state"
shot(c(77), "R_map_india", "none", ms=9.0)   # "none of those parks": the park pins                       # "None of those parks is up and running yet..."
chip("None running yet", L(77, 0.25), LE(77), 120, 640, "red", "sm", "up")
shot(c(78), "Y02", "y02", ms=[97.74, 65.62], origin="35% 30%")            # "So has India won? Not yet. But it's back in the fight."
# ---- RULE, RUIN, REALITY + WHAT IT MEANS FOR YOU
shot(c(79), "px_45675", "in", ms=8.0, dim=0.3)                     # "So here's the lesson..."
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
    filt.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1,apad=whole_dur={END}[o]")
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
        kind = "y02" if s["src"] == "Y02" else "anim" if s["src"] in SPLIT_R else "doc" if s["src"].startswith("D_") else "crop" if s["move"] == "crop" else "foot"
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
    "Y02": [(11.0, 13.9), (33.0, 34.9), (42.0, 49.58), (49.78, 52.46), (52.66, 55.7), (57.18, 59.38), (59.58, 62.18),
            (62.38, 65.42), (65.62, 67.54), (67.74, 71.42), (71.62, 72.86), (73.06, 74.78), (74.98, 76.66), (76.86, 78.8),
            (80.98, 82.14), (82.34, 83.42), (83.62, 86.06), (86.26, 90.02), (90.22, 91.46), (91.66, 93.22), (93.42, 95.82),
            (96.02, 97.54), (97.74, 101.38), (101.58, 102.8)],
    "Y04": [(6.05, 7.25), (7.35, 10.3), (10.45, 14.1), (14.25, 19.05)],
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
        film = end - s["t0"]
        plan = None                                           # (repeat seconds + a small price per extra cut, sub, starts)
        for n in (1, 2, 3, 4):
            sub = film / n
            if n > 1 and sub < 1.3:
                break
            picks = []
            for k in range(n):
                c = best(s["src"], rs, sub * sp, s["ms"] + k * 2.0)
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
    """An item crossing a part seam with under 0.6 s on this side: drop that sliver (it reads as a flash)."""
    return (a < t0 or b > t1) and min(b, t1) - max(a, t0) < 0.6


def emit_part(pid, t0, t1, caps):
    D = r3(t1 - t0); d = OUTV / pid
    shutil.rmtree(d / "media", ignore_errors=True); (d / "media").mkdir(parents=True, exist_ok=True)
    shutil.copytree(OUTV / "_shared", d / "shared", dirs_exist_ok=True)
    shutil.copy(ROOT / "assets/brand/logo_square.png", d / "media/logo_square.png")
    loc = lambda x: r3(x - t0)
    H = []
    for i, s in enumerate(x for x in SEQ if t0 - 1e-6 <= x["t0"] < t1 - 1e-6):
        # start and end floored onto their frames (frame_floor.py): rounded up, the cut frame showed the empty background
        fs, fe = round(s["t0"] * FPS) - round(t0 * FPS), round(s["t1"] * FPS) - round(t0 * FPS)
        st, du = FF.ft(fs), round(FF.ft(fe) - FF.ft(fs), 4); src = media(s["src"])
        fn = f"media/{src.name}"
        if not (d / fn).exists():
            shutil.copy(src, d / fn)
        tag = f'<div class="tag">{esc(s["tag"])}</div>' if s["tag"] else ""
        org = f' data-origin="{s["origin"]}"' if s["origin"] else ""
        dim = ("" if not s["dim"] else '<div class="dim"></div>' if s["dim"] is True
               else f'<div class="dim" style="background:rgba(4,18,21,{s["dim"]})"></div>')
        if src.suffix == ".mp4":
            H.append(f'      <div id="{pid}-s{i}" class="shot" data-vs="{st}" data-vd="{du}" style="visibility:hidden"><video id="{pid}-v{i}" class="m" src="{fn}" muted playsinline '
                     f'data-move="{s["move"]}"{org} data-start="{st}" data-duration="{du}" data-media-start="{s["ms"]}" data-track-index="2" data-volume="0"></video></div>')
            H.append(f'      <div class="vover" data-vs="{st}" data-vd="{du}" style="visibility:hidden">{dim}{tag}</div>')
        else:
            fit = ' style="object-fit:contain;background:#071a1e"' if s["src"].startswith("D_") or s["src"] == "endcard" else ""
            H.append(f'      <div id="{pid}-s{i}" class="shot" data-start="{st}" data-duration="{du}" data-track-index="1">'
                     f'<img class="m a" src="{fn}" alt=""{fit} data-move="{s["move"]}"{org} />{dim}{tag}</div>')
    O = []
    for o in OV:
        a, b = o["at"], o["to"] if o["to"] is not None else END
        if b <= t0 or a >= t1 or seam_sliver(a, b, t0, t1):
            continue
        h = re.sub(r'(data-(?:at|to)=")([\d.]+)"', lambda mm: f'{mm.group(1)}{min(D, max(0.0, loc(float(mm.group(2)))))}"', o["h"])
        h = re.sub(r'(data-count="[\d.]+,[\d.]+,)([\d.]+)', lambda mm: f'{mm.group(1)}{max(0.0, loc(float(mm.group(2))))}', h)
        O.append("      " + h)
    cap = "\n".join(f'      <div class="cap" data-at="{max(0.0, loc(a))}" data-to="{min(D, loc(b))}" data-fx="fade" data-d="0.12">{c}</div>'
                    for a, b, c in caps if b > t0 and a < t1 and not seam_sliver(a, b, t0, t1))
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
