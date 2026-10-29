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
import re
import shutil
import subprocess
from pathlib import Path

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
END = round(VO_END + 12.0, 2)   # end screen (YouTube end-screen elements need 5-20 s)

FOOT = {  # owner-fetched footage (assets/footage/fetched.csv; Pexels downloaded by the owner)
    "Y02": ("02_1ddBzBUaa8k.mp4", "FOOTAGE · LYFIUS PHARMA"), "Y04": ("04_3aclBlRaYNQ.mp4", "FOOTAGE · ABP MAJHA"),
    "Y05": ("05_keUkhEBY_fs_stab.mp4", "FOOTAGE · AMAR AGRO INDUSTRY"), "Y06": ("06_ZT2VuADHAFo_stab.mp4", "FOOTAGE · ADINATH STONES"),
    "PXa": ("3922881-uhd_4096_2160_25fps.mp4", "PEXELS"), "PXb": ("13048933-uhd_3840_2160_30fps.mp4", "PEXELS"),
}


def media(name):
    if name in FOOT:
        return A / "footage" / FOOT[name][0]
    if name.startswith("px_"):
        return A / "stock" / f"pixabay_{name[3:]}.mp4"
    if name.startswith("R_"):
        return A / "renders" / f"video_pha_{name[2:]}.mp4"
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
# ---- HOOK: pharmacy of the world, the capsule, the locked doors (0:00-1:35)
shot(0.0, "PXb", "slow", ms=1.0)                                   # "India sells medicines to around two hundred countries..."
chip("Pharmacy of the world", 1.2, LE(1), 120, 760, "steel", "", "up")
shot(c(2), "R_capsule_open", "none", ms=0.6)                       # "But open one antibiotic capsule..."
shot(S(2, 1) - PRE, "R_map_stream", "none", ms=0.4)                # "That's the actual medicine... began in China."
shot(c(3), "px_40948", "in", ms=1.0)                               # "The rest of the capsule is just there to carry it to you."
shot(c(4), "px_1643", "slow", tag="ILLUSTRATIVE FOOTAGE", ms=2.0, dim=0.45)   # "Now think back to the Corona days..."
datebig("3 MARCH 2020", "LOCKDOWN 24 MARCH · 3 WEEKS AWAY", L(4, 0.55), LE(4))
shot(c(5), "R_map_hubei", "none", ms=0.0)                          # "In China, the city of Wuhan has been locked down..."
shot(c(6), "D_dgft_2020_noti50-1", "in", tag="DOCUMENT · DGFT")   # "Delhi. A two-page government order goes out..."
chip("13 ingredients", S(6, 2), LE(6) + 1.5, 120, 760, "red", "sm", "pop")
chip("Paracetamol", S(6, 3), LE(6) + 1.5, 640, 760, "red", "sm", "pop")
cite("[DGFT NOTIFICATION 50/2015-20 | 3 MAR 2020]", L(6, 0.1), LE(6) + 1.5)
shot(c(7), "px_23008", "slow", dim=0.35)                           # "Wait. India? The pharmacy of the world... locking its own doors?"
chip("Exports: by licence", L(7, 0.4), LE(7), 120, 760, "red", "", "pop")
shot(c(8), "R_map_hubei", "none", ms=5.5)                          # "Yes. And the reason was Corona..."
shot(c(9), "D_tribune_2020", "in", tag="DOCUMENT · THE TRIBUNE")  # "Reports at the time said..."
cite("[THE TRIBUNE | 3 MAR 2020]", L(9), LE(9))
shot(c(10), "R_capsule_open", "push", ms=4.2)                      # "So here's the question... who makes the powder?"
shot(c(11), "PXa", "slow", ms=0.5)                                 # "And before you worry — this isn't about the quality..."
chip("Quality: not the issue", L(11, 0.2), LE(11), 120, 160, "green", "sm", "up")
chip("Supply: the issue", L(11, 0.6), LE(11), 120, 260, "amber", "sm", "up")
shot(c(12), "Y02", "crop", ms=[32.0, 50.0, 65.3], origin="50% 8%")              # "Stay with me. Around minute eight... Andhra Pradesh"
chip("Minute 8 · Andhra Pradesh", L(12, 0.15), LE(12), 120, 160, "saffron", "sm", "up")
# ---- INDIA EARNED IT (1:31-2:50)
shot(c(13), "px_45675", "slow", ms=1.0)                            # "First, let's give India its due..."
shot(c(14), "px_262189", "slow", dim=0.72)                         # "Think back to two thousand one. H.I.V. ... ten thousand dollars"
datebig("2001", "H.I.V. MEDICINES", L(14, 0.05), LE(16))
# same unit on both cards (owner's review, 2026-10-29): MSF 7 Feb 2001, "about $10,400" in the US vs Cipla's "$350 per year" (P14, P15)
count(L(14, 0.6), LE(16), 600, 330, 0, 10400, L(14, 0.62), 1.3, "$", " / YEAR", "red", "xl")
chip("Western price", L(14, 0.75), LE(16), 606, 462, "red", "sm", "up")
count(L(15, 0.5), LE(16), 600, 566, 0, 350, L(15, 0.55), 0.9, "$", " / YEAR", "green", "xl")
chip("Cipla · under $1 a day", L(15, 0.7), LE(16), 606, 698, "green", "sm", "up")
cite("[MSF | 2001]", L(14, 0.6), LE(16))
shot(c(17), "px_29021", "slow", ms=2.0)                            # "And today... more than two and a half lakh crore rupees a year."
count(L(17, 0.4), LE(17), 120, 760, 0, 2.5, L(17, 0.45), 1.2, "₹", " LAKH CRORE+", "ink", "", 1)
cite("[PIB | EXPORTS 2024-25]", L(17, 0.4), LE(17))
shot(c(18), "R_tablet", "none", ms=0.0)                            # "Every tablet has two parts." ... coating, strip, box
shot(c(21), "px_45682", "slow", ms=1.0)                            # "Indian companies are world class at that last part."
shot(c(22), "R_capsule_open", "in", ms=6.0)                         # "But the powder you swallow?"
shot(c(23), "D_niti_cover-01", "in", tag="DOCUMENT · NITI AAYOG")  # "In 2025, India bought these powders... sixty-five thousand crore"
count(L(23, 0.5), LE(23), 120, 760, 0, 65000, L(23, 0.55), 1.4, "₹", " CRORE · 2025", "amber", "sm")
cite("[NITI AAYOG $7.4 BN | OUR CONVERSION]", L(23, 0.5), LE(23))
shot(c(24), "R_map_stream", "none", ms=3.0)                        # "And the biggest seller, by far... China."
shot(c(25), "D_niti_p-40", "in", dim=0.78, tag="DOCUMENT · NITI AAYOG")   # "And if you look at antibiotics... about eighty-six went to China."
coins(L(25, 0.45), LE(25))
gauge(L(25, 0.75), LE(25), 86.1, "ANTIBIOTIC POWDER IMPORTS · CHINA'S SHARE", "NITI AAYOG · 2025")
cite("[NITI AAYOG | TRADE WATCH Q4 FY26]", L(25, 0.4), LE(25))
shot(c(26), "px_76395", "slow", dim=0.3)                           # "Even your fever tablet has a China link..."
chip("Raw chemical: para-aminophenol", L(26, 0.6), LE(26), 120, 760, "amber", "sm", "up")   # P25: PAP, a big share from China
cite("[INDUSTRY REPORTS]", L(26, 0.6), LE(26))
# ---- INDIA MADE ITS OWN PENICILLIN (3:16-4:19)
shot(c(27), "W_L0012314", "in")                                    # "So you might be thinking — has it always been like this?"
shot(c(29), "Y04", "crop", ms=8.0, origin="50% 50%")              # "Pimpri, near Pune. Nineteen fifty-four..."
datebig("1954", "PIMPRI · NEAR PUNE", L(29, 0.05), LE(29))
shot(c(30), "W_L0012314", "out")                                   # "Penicillin was the miracle drug of that time..."
chip("Miracle drug", L(30, 0.1), LE(30) + 2.0, 120, 760, "green", "", "up")
shot(c(31), "Y04", "crop", ms=[14.5, 6.0], origin="50% 50%")             # "The government sets up... Hindustan Antibiotics. By 1956..."
namelt("Hindustan Antibiotics", "PIMPRI · SET UP 1954 · PENICILLIN BY 1956", L(31, 0.15), LE(31))
cite("[DEPT OF PHARMACEUTICALS | HAL]", L(31, 0.15), LE(31))
shot(c(32), "R_map_india", "none", ms=0.0)                         # "Just think about it. Picture your grandparents' India..."
shot(S(32, 2) - PRE, "W_L0032175", "in")   # "A young, poor country, growing... in its own factory" (penicillin production apparatus, archival)
shot(c(33), "px_262464", "slow", ms=1.0, dim=0.2)                  # "Soon, others join in — Alembic, Sarabhai and Ranbaxy..."
plate("Alembic", "", L(33, 0.35), LE(33), 160, 300); plate("Sarabhai", "", L(33, 0.45), LE(33), 560, 300); plate("Ranbaxy", "", L(33, 0.55), LE(33), 1000, 300)
shot(c(34), "R_fermenter", "push", ms=0.0)                         # "How do you actually make penicillin?"
# ---- WHY PENICILLIN IS A SCALE GAME (4:19-5:43)
shot(c(35), "px_197486", "slow", ms=4.0)                           # "Many medicines, like paracetamol, are cooked from chemicals..."
chip("Cooked", L(35, 0.2), S(35, 1), 120, 760, "steel", "", "pop")
shot(S(35, 1) - PRE, "W_B0004595", "in")                           # "Penicillin is different. Penicillin is grown."
chip("Grown", S(35, 2), LE(35), 120, 760, "green", "", "pop")
shot(c(36), "W_B0004843", "in")                                    # "You take a special mould... a cousin of the green patches..."
shot(S(36, 1) - PRE, "R_fermenter", "none", ms=0.5)                # "You put it in a giant steel tank... sugar and air."
shot(c(37), "R_fermenter", "none", ms=6.8)                         # "For about a week, the tank runs day and night..."
chip("One germ = lost batch", S(37, 2), LE(37) + 2.0, 120, 160, "red", "sm", "up")
el(f'<div class="contam" {attrs(S(37, 2) + 0.15, LE(37) + 2.0, "fade", 0.9)}></div>', S(37, 2) + 0.15, LE(37) + 2.0)   # the broth turns murky (ILLUSTRATION)
shot(c(38), "R_fermenter", "none", ms=15.0)                        # "Then you take the penicillin out... penicillin G."
chip("Penicillin G", L(38, 0.6), LE(38), 1320, 160, "green", "sm", "pop")
shot(c(39), "px_40948", "slow", ms=0.5, dim=0.4)                   # "Next, it's turned into a smaller base powder..."
shot(S(39, 2) - PRE, "PXb", "slow", ms=10.0, dim=0.3)              # "From that base, factories make amoxicillin..."
chip("Penicillin G", L(39, 0.05), LE(39), 120, 300, "green", "sm", "left")
chip("→ The base (6-A.P.A.)", L(39, 0.3), LE(39), 120, 420, "steel", "sm", "left")
chip("→ Amoxicillin", L(39, 0.75), LE(39), 120, 540, "ink", "sm", "left")
shot(c(40), "R_tanks", "none", ms=0.0)                             # "A bigger tank makes the powder cheaper. Much cheaper."
shot(c(42), "Y06", "slow", ms=4.0)                                 # "Think of a flour mill. A big chakki grinds each kilo cheaper..."
chip("Small chakki", L(42, 0.1), S(42, 2), 120, 760, "steel", "sm", "up")
shot(S(42, 2) - PRE, "Y05", "crop", ms=1.0, origin="50% 10%")     # "Double your tank, and your costs don't double... but your output does."
chip("Bigger mill · cheaper kilo", S(42, 2) + 0.3, LE(42) + 2.0, 120, 760, "green", "sm", "up")
shot(c(43), "R_tanks", "none", ms=9.4)                             # "So you can guess who wins..."
shot(c(44), "R_map_stream", "none", ms=6.0)                        # "And that's exactly where India's story turns."
# ---- HOW CHINA TOOK THE POWDER (5:43-7:23)
shot(c(45), "Y04", "crop", ms=[10.0, 14.5], origin="50% 50%", dim=0.35)    # "Now, here's what we got wrong... only a few companies"
chip("Few licences", L(45, 0.35), LE(45), 120, 300, "red", "sm", "up")
chip("Small plants", L(45, 0.6), LE(45), 120, 420, "red", "sm", "up")
cite("[MDPI ECONOMIES 2021]", L(45, 0.35), LE(45))
shot(c(46), "px_199788", "slow", ms=0.0)                            # "Meanwhile, in the nineteen nineties, China went all in..."
chip("Cheap power · cheap water", L(47, 0.3), LE(47), 120, 760, "amber", "sm", "up")
cite("[CFR | THE PHARMA CHOKE POINT]", L(47, 0.3), LE(47))
shot(c(48), "R_map_stream", "none", ms=8.0)                        # "And then cheap Chinese penicillin flooded the world market..."
shot(c(49), "px_262189", "slow", ms=2.0, dim=0.78)                 # "Nineteen ninety-one — the year India opened up its economy..."
datebig("1991", "INDIA OPENS ITS ECONOMY", L(49, 0.05), LE(50))
gauge(L(49, 0.65), LE(50) + 1.0, 0.5, "ALL MEDICINE POWDER IMPORTS · CHINA'S SHARE", "RIS DP 268")
shot(c(51), "px_212001", "slow", ms=[0.0, 3.6, 7.2], dim=0.55)
shot(c(54), "px_212000", "slow", ms=[0.0, 3.8, 7.6], dim=0.55)   # the roll call over still gears (no people under the stamps)    # "Then, one by one, the Indian penicillin plants went quiet."
for i, (name, ln) in enumerate([("Hindustan Antibiotics", 52), ("I.D.P.L.", 53), ("Torrent · Ranbaxy · Sarabhai", 54), ("Alembic", 55)]):
    plate(name, "", L(ln), LE(55) + 1.4, 160, 170 + i * 170)
    stamp("STOPPED", round(LE(ln) - 0.35, 3), LE(55) + 1.4, 1180, 175 + i * 170)
cite("[RIS DP 268 · ISID WP239]", L(52), LE(55) + 1.4)
shot(c(56), "px_23215", "slow", ms=4.0)                            # "By about twenty twenty, India was importing all of that base powder"
chip("Base powder: 100% imported", L(56, 0.3), LE(56), 120, 760, "amber", "sm", "up")
cite("[ISID WP239]", L(56, 0.3), LE(56))
shot(c(57), "D_niti_p-40", "in", dim=0.6, tag="DOCUMENT · NITI AAYOG")   # "Remember that one per cent?... around eighty-six per cent."
gauge(L(57, 0.6), LE(57), 86.1, "ANTIBIOTIC POWDER IMPORTS · CHINA'S SHARE", "NITI AAYOG · 2025")
shot(c(58), "px_45680", "slow", ms=[0.0, 2.9], dim=0.45)                  # "Niti Aayog estimates Chinese powder costs 35-40% less..."
shot(S(58, 1) - PRE, "px_199788", "in", ms=6.0, dim=0.45)           # "So tell me — if you ran a company, would you build a plant here?"
chip("China's powder: 35–40% cheaper", L(58, 0.2), LE(58), 120, 160, "amber", "sm", "up")
cite("[NITI AAYOG ESTIMATE]", L(58, 0.2), LE(58))
shot(c(59), "R_tanks", "none", ms=12.0)                            # "That's the trap..."
shot(c(60), "D_dgft_2020_noti50-1", "out", tag="DOCUMENT · DGFT")  # "Then Corona came — and India had to lock its own doors."
shot(c(61), "px_45682", "slow", ms=6.0, dim=0.6)                   # "And this time, the central government decided to break the trap."
shot(c(62), "px_197486", "slow", ms=1.0, dim=0.65)                 # "It launched a scheme..."
count(L(62, 0.5), LE(62), 120, 300, 0, 6940, L(62, 0.55), 1.2, "₹", " CRORE", "saffron", "")
chip("41 ingredients", L(62, 0.25), LE(62), 120, 460, "saffron", "sm", "up")
cite("[DEPT OF PHARMACEUTICALS | PLI 2020]", L(62, 0.25), LE(62))
shot(c(63), "R_map_india", "none", ms=3.6)                         # "And one company took the biggest bet of all."
# ---- KAKINADA SWITCHES IT BACK ON (the promised minute eight)
shot(c(64) - BEATS[63] + 0.2, "Y02", "slow", ms=[32.0, 50.0, 81.0])              # (silence, then) "Kakinada, Andhra Pradesh. On the coast, a new plant..."
namelt("Kakinada, Andhra Pradesh", "LYFIUS PHARMA · AUROBINDO PHARMA", L(64, 0.1), LE(64))
shot(c(65), "Y02", "crop", ms=62.0, origin="50% 8%")             # "Inside are the giant tanks... the company says ₹2,500 crore... 15,000 tonnes"
chip("₹2,500 cr · company figure", L(65, 0.35), LE(65), 120, 160, "saffron", "sm", "up")
chip("15,000 tonnes a year", L(65, 0.7), LE(65), 120, 280, "saffron", "sm", "up")
shot(c(66), "Y02", "crop", ms=[74.0, 81.0], origin="50% 8%")             # "In twenty twenty-four, the tanks start running..."
datebig("2024", "PENICILLIN G · MADE IN INDIA AGAIN", L(66, 0.05), LE(66))
shot(c(67), "px_216619", "slow", ms=4.0)                           # "But you know the trap... cheap imports were still waiting at the port."
shot(c(68), "D_dgft_2026_mip-1", "in", tag="DOCUMENT · DGFT")      # "So on the twenty-ninth of January, 2026, the government stepped in."
datebig("29 JAN 2026", "MINIMUM IMPORT PRICE", L(68, 0.1), LE(69))
chip("₹2,216 / kg · penicillin G", L(69, 0.4), LE(69), 120, 760, "saffron", "sm", "up")
cite("[DGFT | 29 JAN 2026]", L(68, 0.1), LE(69))
shot(c(70), "R_fermenter_lit", "none", ms=4.0)                     # "Think of it as a shield..."
shot(c(71), "px_23759", "slow", ms=2.0, dim=0.5)                 # "And in September 2026... below a fair price."
chip("Anti-dumping check · Sep 2026", L(71, 0.3), LE(71), 120, 760, "steel", "sm", "up")
chip("On Lyfius Pharma's application", L(71, 0.45), LE(71), 120, 830, "steel", "sm", "up")   # DGTR initiation 28 Sep 2026 (P63 note)
cite("[DGTR | 28 SEP 2026]", L(71, 0.3), LE(71))
shot(c(72), "R_fermenter_lit", "none", ms=10.0)                    # "But that shield has an end date... January 2027."
datebig("JAN 2027", "THE SHIELD ENDS", L(72, 0.5), LE(73))
shot(c(73), "Y02", "crop", ms=50.0, origin="50% 8%")                                # "That's the date to watch..."
shot(c(74), "Y02", "crop", ms=86.0, origin="50% 8%")            # "And here's the balance the government has to strike..."
chip("Protect the plant", L(74, 0.4), LE(74), 120, 160, "saffron", "sm", "up")
chip("Keep medicines affordable", L(74, 0.7), LE(74), 120, 280, "green", "sm", "up")
shot(c(75), "Y02", "crop", ms=[49.0, 64.0], origin="50% 8%")            # "And it's not just penicillin... five thousand crore"
count(L(75, 0.45), LE(75), 120, 160, 0, 5000, L(75, 0.5), 1.0, "₹", " CRORE+ INVESTED", "saffron", "sm")
cite("[DEPT OF PHARMACEUTICALS | JUNE 2026]", L(75, 0.45), LE(75))
shot(c(76), "R_map_india", "none", ms=6.5)                         # "Three giant bulk drug parks... Nakkapalli... same state"
shot(c(77), "R_map_stream", "none", ms=10.0)                       # "None of those parks is up and running yet..."
chip("None running yet", L(77, 0.25), LE(77), 120, 760, "red", "sm", "up")
shot(c(78), "Y02", "crop", ms=110.0, origin="50% 8%")            # "So has India won? Not yet. But it's back in the fight."
# ---- RULE, RUIN, REALITY + WHAT IT MEANS FOR YOU
shot(c(79), "px_45675", "in", ms=8.0, dim=0.3)                     # "So here's the lesson..."
shot(c(80), "D_dgft_2020_noti50-1", "in", tag="DOCUMENT · DGFT")  # "And the cost? You saw it in the Corona days..."
shot(c(81), "Y02", "crop", ms=96.0, origin="50% 8%")             # "But here's the reality today..."
shot(c(82), "PXa", "slow", ms=0.3)                                 # "So what does this mean for you? Keep taking your medicines..."
shot(c(84), "R_capsule_open", "push", ms=3.6)                      # "But the next time you take an antibiotic... began in China."
shot(c(85), "R_map_home", "none", ms=0.8)                          # "And if the plant in Kakinada wins... right here in India."
shot(c(86), "R_map_home", "out", ms=6.0, dim=0.5)                  # "Medicines aren't the only missing piece... India's own A.I.?"
chip("Next: India's own A.I.", L(86, 0.5), END, 120, 160, "steel", "", "up")
shot(c(87), "endcard", "push", tag="")                             # pinned question, channel line, end screen
chip("Which medicine should India make fully?", L(87, 0.2), END, 120, 760, "saffron", "sm", "up")


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
            out.append((round(t, 2), round(t + d + (0.12 if n == len(split) - 1 else 0.0), 2), esc(p))); t += d
    return out


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
        "anim": [("cutB", "50% 50%"), ("push", "50% 50%")],
        "foot": [("cutA", "32% 38%"), ("cutB", "68% 58%"), ("cutA", "62% 34%"), ("cutB", "36% 62%")]}


SPLIT_R = {"R_tablet"}   # renders whose long holds sit still (freezedetect), centred so a punch-in keeps the labels


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
        kind = "anim" if s["src"] in SPLIT_R else "doc" if s["src"].startswith("D_") else "crop" if s["move"] == "crop" else "foot"
        for k in range(n):
            p = dict(s, t0=r3(s["t0"] + k * step))
            p["ms"] = ms[k] if isinstance(ms, list) and k < len(ms) else (
                (ms[-1] if isinstance(ms, list) else ms) + (k - (len(ms) - 1 if isinstance(ms, list) else 0)) * step)
            p["ms"] = r3(p["ms"])
            if k:
                p["move"], p["origin"] = FRAMES[kind][(k - 1) % len(FRAMES[kind])]
                if kind == "crop":
                    p["origin"] += " " + (s["origin"] or "50% 50%").split()[1]
            out.append(p)
    SEQ[:] = out


def emit():
    SEQ.sort(key=lambda s: s["t0"])
    split_long()
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
        st, du = loc(s["t0"]), r3(s["t1"] - s["t0"]); src = media(s["src"])
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
