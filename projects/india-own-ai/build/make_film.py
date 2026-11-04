#!/usr/bin/env python3
"""India-own-AI film assembly: the shot list, the PIECE METER, overlays and captions -> HyperFrames parts in
video/aig/p1..p5. Adapted from the pharma film (projects/pharma-apis/build/make_film.py): same timing model, dissolves,
clean-span footage placement, frame flooring and part seams; new here are the token tiles and the animated plates.

Times: every shot sits on a VO line (align/align.json, 1-based = vo.txt rows) or sentence (align/sentences.json).
BEATS insert picture-led silences after lines; F() maps raw VO time to film time; voice/vo_film.wav is the VO with
those silences. Media: the owner's footage (assets/footage), Pexels picks (assets/pexels_*), PIB photos (assets/pib),
document captures (assets/docs); animated beats are overlays over a generated plate (assets/plates/plate.png).
Every number on screen has a claims.csv row; token pieces come from research/token_pieces.json (tools/token_pieces.py).
Usage: python3 projects/india-own-ai/build/make_film.py   (then npm run vendor in each part; render: PLAYBOOK §3a)
"""
import html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import frame_floor as FF  # noqa: E402

P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]; A = P / "assets"; OUTV = ROOT / "video/aig"
esc = html.escape
LINES = json.loads((P / "align/align.json").read_text())
SENTS = json.loads((P / "align/sentences.json").read_text())
TOK = json.loads((P / "research/token_pieces.json").read_text())

# ---------- picture-led beats: seconds of silence after these lines (screenplay.md) ----------
BEATS = {4: 1.5,     # the broken letter holds
         16: 1.0,    # the budget bar reaches the loss bar
         53: 1.5,    # music silence before "ten thousand crore... against thirteen lakh crore"
         67: 1.2,    # the music drops before the payoff
         71: 1.0}    # Sarvam's numbers land, a saffron chime
CUTS = sorted((round((LINES[n - 1]["end"] + LINES[n]["start"]) / 2, 3), s) for n, s in BEATS.items())


def F(t):
    return round(t + sum(s for c, s in CUTS if c <= t), 3)


def L(n, k=0.0):
    a, b = LINES[n - 1]["start"], LINES[n - 1]["end"]
    return F(a + (b - a) * k)


def LE(n):
    return F(LINES[n - 1]["end"])


def S(n, k):
    return F([s for s in SENTS if s["line"] == n][k]["start"])


def SE(n, k):
    return F([s for s in SENTS if s["line"] == n][k]["end"])


WORDS = json.loads((P / "align/words.json").read_text())   # build/words.py: word times, raw VO seconds
_norm = lambda w: re.sub(r"[^a-z0-9.']", "", w.lower()).strip(".'")


def W(n, phrase, k=0):
    """film time of the k-th place in line n where `phrase` (one or more words) is said"""
    ws = [w for w in WORDS if w["line"] == n]; want = [_norm(x) for x in phrase.split()]
    hits = [i for i in range(len(ws)) if all(i + j < len(ws) and _norm(ws[i + j]["w"]).startswith(x) for j, x in enumerate(want))]
    if len(hits) <= k:
        raise SystemExit(f"word {phrase!r} not in line {n}: {' '.join(w['w'] for w in ws)}")
    return F(ws[hits[k]]["t"])


PRE = 0.15
VO_END = F(LINES[-1]["end"])
END = round(VO_END + 8.0, 2)
FPS = 30

# ---------- media ----------
PX = {  # Pexels picks (qa/pexels/verdicts.md): key -> (file, folder)
    "MON": "pexels_termux/pexels_01_monsoon_pune_29081675.mp4", "RAIN": "pexels_ag/pexels_01_india_monsoon_city_street_34430107.mp4",
    "TYP": "pexels_ag/pexels_02_female_typing_smartphone_6963836.mp4", "TYP2": "pexels_ag/pexels_02_hands_typing_smartphone_7560581.mp4",
    "LIBW": "pexels_termux/pexels_03_library_walk_17151509.mp4", "LIBA": "pexels_ag/pexels_03_library_bookshelves_aisle_854533.mp4",
    "GIRL": "pexels_ag/pexels_04_indian_girl_reading_book_40526006.mp4", "BOY": "pexels_ag/pexels_04_child_reading_book_warm_light_8343356.mp4",
    "HPAGE": "pexels_ag/pexels_05_hindi_printed_page_close_up_30077914.mp4", "NEWS": "pexels_ag/pexels_05_indian_newspaper_sorting_street_19494262.mp4",
    "BAZ": "pexels_ag/pexels_06_indian_bazaar_shop_signboards_29614744.mp4", "CROWD": "pexels_ag/pexels_07_crowded_indian_market_above_31485217.mp4",
    "KOL": "pexels_ag/pexels_07_kolkata_crowded_market_aerial_39867091.mp4", "LED": "pexels_ag/pexels_08_server_units_blinking_leds_7140928.mp4",
    "RACK": "footage/pexels_server_rack_5028622.mp4", "CHIP": "pexels_ag/pexels_09_electronic_chip_microchip_macro_6755158.mp4",
    "PCB": "pexels_ag/pexels_09_circuit_board_macro_focus_7609195.mp4", "FAB": "pexels_ag/pexels_10_cleanroom_workers_white_suits_32386623.mp4",
    "STK": "pexels_termux/pexels_11_stock_graph_14003933.mp4", "CANDLE": "pexels_ag/pexels_11_candlestick_charts_trading_screen_38892330.mp4",
    "BLR": "pexels_termux/pexels_12_bengaluru_sunrise_30590791.mp4", "BLR2": "pexels_ag/pexels_12_bengaluru_tech_park_wide_17629504.mp4",
    "TAP": "pexels_ag/pexels_13_water_tap_turned_off_hand_4061892.mp4", "CAP": "pexels_ag/pexels_14_us_capitol_building_iconic_wide_29188235.mp4",
    "FARM": "pexels_ag/pexels_15_farmer_using_smartphone_field_32045282.mp4", "RUP": "pexels_ag/pexels_16_counting_rupee_notes_henna_hands_17060680.mp4",
    "VOICE": "pexels_ag/pexels_17_man_recording_voice_message_phone_5321800.mp4", "CITY": "pexels_ag/pexels_18_new_delhi_urban_skyline_dusk_31948241.mp4",
    "SEMI": "footage/pexels_semiconductor_6754830.mp4",
}
FOOT = {  # third-party footage from the owner's Drive (asset-manifest.md): key -> (file, on-screen credit)
    "YOT": ("03_J0Cin9zOSSM.mp4", "FOOTAGE · DIGIT · YOTTA NM1 DATA CENTRE, NAVI MUMBAI"),
    "BHA": ("04_oG_whhbr0sg.mp4", "FOOTAGE · MONEYCONTROL · BHASHINI"),
    "KIS": ("05_u8uJ6tqYt4I.mp4", "FOOTAGE · AGRICULTURE INDIA · KISAN E-MITRA"),
    "BSW": ("01_ytvy1JruLlY.mp4", "FOOTAGE · BUSINESS STANDARD"),
    "TATA": ("01_Ap3ek027Feo.mp4", "FOOTAGE · BRIGHT WAY · TATA FAB SITE, DHOLERA"),
    "NVD": ("02_tiaX1Ja3C5g_h.mp4", "FOOTAGE · NVIDIA · JENSEN HUANG, NVIDIA CEO"),
}
# owner-fetched YouTube clips (Termux, Creator/English/india-own-ai/footage/): used when present, else the fallback shot
YT = {"VAI": "zhtFmBv2hmg", "PMX": "Y1mdgQkUHn0", "IND": "K7PBZSmJrXQ_h", "NAV": "85RfBSq6X04_h",
      "BGN": "YNrzA_wRBW8", "PKN": "Er0FGccFg3Q", "BHD": "6CCU07GFEus"}
YT_TAG = {"VAI": "FOOTAGE · CNBC-TV18 · INDIAAI BRIEFING · 30 JAN 2025", "PMX": "FOOTAGE · NARENDRA MODI · AI IMPACT EXPO, BHARAT MANDAPAM · FEB 2026",
          "IND": "FOOTAGE · SARVAM · INDUS", "NAV": "FOOTAGE · CNBC-TV18 · GSLV-F18 / NVS-03 · 30 OCT 2026",
          "BGN": "FOOTAGE · INDIA TODAY GLOBAL · BHARATGEN", "PKN": "FOOTAGE · NDTV · PRATYUSH KUMAR, SARVAM CO-FOUNDER",
          "BHD": "FOOTAGE · DIGITAL INDIA · BHASHINI BHASHA DAAN"}


def yt_file(key):
    d = A / "footage" / "yt"
    if d.exists():
        for f in d.glob(f"*_{YT[key]}.mp4"):
            return f
    return None


def media(name, raw=False):
    src = None
    if name in PX:
        src = A / PX[name]
    elif name in FOOT:
        src = A / "footage" / FOOT[name][0]
    elif name in YT:
        src = yt_file(name)
    if src is not None:
        conf = A / "conformed" / src.name
        return conf if conf.exists() and not raw else src
    if name.startswith("ST_"):   # word-level stock (round 2): assets/stock, Pixabay videos / Openverse photos
        for ext in (".mp4", ".jpg"):
            f = A / "stock" / f"{name[3:]}{ext}"
            if f.exists():
                conf = A / "conformed" / f.name
                return conf if ext == ".mp4" and conf.exists() and not raw else f
    if name.startswith("PIB_"):
        return A / "pib" / f"{name[4:]}.jpg"
    if name.startswith("D_"):
        for ext in (".png", ".jpg"):
            f = A / "docs" / f"{name[2:]}{ext}"
            if f.exists():
                return f
    if name == "plate":
        return A / "plates" / "plate.png"
    raise SystemExit(f"missing media {name}")


def have(name):
    try:
        return media(name).exists()
    except SystemExit:
        return False


def default_tag(src):
    if src in FOOT:
        return FOOT[src][1]
    if src in YT:
        return YT_TAG[src]
    if src in PX:
        return "PEXELS"
    if src.startswith("ST_"):
        if media(src).suffix == ".mp4":
            return "PIXABAY"
        r = STOCK.get(src[3:], {})
        return f"PHOTO · {r.get('author', '').upper()} · CC {r.get('licence', '').upper()} · OPENVERSE"
    if src.startswith("PIB_"):
        return "PHOTO · PIB · 30 JAN 2025"
    if src.startswith("D_"):
        return "DOCUMENT"
    return ""


STOCK = {Path(r[0]).stem: dict(page=r[1], author=r[2], licence=r[3]) for r in json.loads((A / "stock/picked.json").read_text())} \
    if (A / "stock/picked.json").exists() else {}
SEQ, OV, INS = [], [], []
XF = 0.2


def ins(at, src, dur=1.5, ms=0.0, move="in", tag=None, origin=None, dim=None):
    """a word-level cutaway (owner, r1: "while we are saying names, verbs... show that clip, even one or two seconds"):
    cut to `src` just before the word at `at`, hold `dur`, then the shot underneath resumes where it would have been"""
    INS.append(dict(at=round(at - PRE, 3), src=src, dur=dur, ms=ms, move=move, tag=tag, origin=origin, dim=dim))


def apply_ins():
    for it in sorted(INS, key=lambda x: x["at"]):
        SEQ.sort(key=lambda s: s["t0"])
        t = it["at"]; i = max(k for k, s in enumerate(SEQ) if s["t0"] <= t + 1e-6); par = SEQ[i]
        nxt = SEQ[i + 1]["t0"] if i + 1 < len(SEQ) else END
        if nxt - t < 0.7:          # the word lands just before a cut: the insert opens the next shot instead
            if i + 1 >= len(SEQ) or t - par["t0"] < 0.5:
                print(f"  ~ insert {it['src']} at {t:.1f} skipped (next cut in {nxt - t:.2f}s)"); continue
            i += 1; par = SEQ[i]; SEQ.pop(i)
            nxt = SEQ[i]["t0"] if i < len(SEQ) else END
            end = t + it["dur"]
            dim = it["dim"] if it["dim"] is not None else (0.55 if par["src"] == "plate" else False)
            SEQ.append(dict(t0=round(t, 3), src=it["src"], move=it["move"], tag=default_tag(it["src"]) if it["tag"] is None else it["tag"],
                            ms=it["ms"], origin=it["origin"], dim=dim, hard=False))
            if nxt - end >= 0.7:
                pm = par["ms"][0] if isinstance(par["ms"], list) else par["ms"]
                adv = max(0.0, end - par["t0"]) if media(par["src"]).suffix == ".mp4" else 0.0
                SEQ.append(dict(par, t0=round(end, 3), ms=round(pm + adv, 3)))
            continue
        lead = t - par["t0"]
        if lead < 0.6:             # right at the start of a shot: the insert opens it
            t = par["t0"]; SEQ.pop(i); lead = 0.0
        end = t + it["dur"]
        dim = it["dim"] if it["dim"] is not None else (0.55 if par["src"] == "plate" else False)
        new = dict(t0=round(t, 3), src=it["src"], move=it["move"], tag=default_tag(it["src"]) if it["tag"] is None else it["tag"],
                   ms=it["ms"], origin=it["origin"], dim=dim, hard=False)
        SEQ.append(new)
        if nxt - end >= 0.7:       # the shot underneath carries on, as if it had kept running
            pm = par["ms"][0] if isinstance(par["ms"], list) else par["ms"]
            adv = (end - par["t0"]) if media(par["src"]).suffix == ".mp4" else 0.0
            SEQ.append(dict(par, t0=round(end, 3), ms=round(pm + adv, 3)))
        elif lead == 0.0 and nxt - t < 0.7 + it["dur"]:
            pass                   # the insert simply runs to the next cut
    SEQ.sort(key=lambda s: s["t0"])


def shot(t0, src, move="push", tag=None, ms=0.0, origin=None, dim=False, hard=False):
    SEQ.append(dict(t0=round(t0, 3), src=src, move=move, tag=default_tag(src) if tag is None else tag, ms=ms, origin=origin, dim=dim, hard=hard))


def el(h, at, to):
    if to is not None and to < at + 0.3:   # an end before (or right after) the start never fades out: it stays on screen
        raise SystemExit(f"overlay ends before it starts ({at:.2f} -> {to:.2f}): {h[:90]}")
    OV.append(dict(h=h, at=round(at, 3), to=None if to is None else round(to, 3)))


def attrs(at, to, fx, d=None):
    return f'data-at="{round(at, 3)}" data-fx="{fx}"' + (f' data-to="{round(to, 3)}"' if to is not None else "") + (f' data-d="{d}"' if d else "")


def chip(text, at, to, x, y, col="ink", size="", fx="pop"):
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{esc(text)}</div>', at, to)


def cite(text, at, to):
    el(f'<div class="cite" {attrs(at, to, "fade")}>{esc(text)}</div>', at, to)


def illus(at, to, text="ILLUSTRATION"):
    el(f'<div class="illus" {attrs(at, to, "fade")}>{esc(text)}</div>', at, to)


def datebig(text, small, at, to):
    el(f'<div class="datebig scrim" {attrs(at, to, "left", 0.4)}>{esc(text)}<small>{esc(small)}</small></div>', at, to)


def namelt(name, role, at, to):
    el(f'<div class="namelt" {attrs(at, to, "left", 0.45)}><b>{esc(name)}</b><span>{esc(role)}</span></div>', at, to)


def count(at, to, x, y, a, b, start, dur, pre="", suf="", col="ink", size="", dec=0):
    dur = min(dur, 0.45)
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, "pop")}><span data-count="{a},{b},{round(start, 3)},{dur}" '
       f'data-pre="{esc(pre)}" data-suf="{esc(suf)}" data-dec="{dec}" data-ease="power2.out">{esc(pre)}{a}{esc(suf)}</span></div>', at, to)


def box(cls, at, to, x, y, w=None, h=None, fx="fade", d=None, inner="", style=""):
    st = f"left:{x}px;top:{y}px" + (f";width:{w}px" if w is not None else "") + (f";height:{h}px" if h is not None else "") + (";" + style if style else "")
    allow = " data-layout-allow-overlap" if cls.startswith(("half", "cut", "blackout", "pgi", "stack", "onepage", "brick", "dotf", "vbar")) else ""
    el(f'<div class="{cls}"{allow} style="{st}" {attrs(at, to, fx, d)}>{inner}</div>', at, to)


# ---------- the PIECE METER: tiles for one language on one chopper ----------
LANG = {"en": "ENGLISH", "hi": "हिंदी · HINDI", "mr": "मराठी · MARATHI", "te": "తెలుగు · TELUGU", "zh": "中文 · CHINESE"}
WHO = {"deepseek": "DEEPSEEK CHOPPER", "chatgpt": "CHATGPT'S CHOPPER", "sarvam": "SARVAM'S CHOPPER"}


def tile_w(p):
    if p["bad"]:
        return 112
    return max(64, int(len(p["t"].strip() or " ") * 34 + 40))


def tiles(who, lang, at, to, y, x0=110, x1=1810, cls="", stagger=None, meter_y=None, meter_cls=""):
    """the sentence as its real pieces: one tile each, popping in left to right, wrapping inside x0..x1"""
    ps = TOK[who][lang]; n = len(ps)
    stg = stagger if stagger is not None else min(0.09, 1.6 / max(n, 1))
    x, yy = x0, y
    for i, p in enumerate(ps):
        w = tile_w(p)
        if x + w > x1:
            x, yy = x0, yy + 110
        t = round(at + i * stg, 3)
        txt = "½" if p["bad"] else esc(p["t"].strip() or "␣")
        c = "tok bad" if p["bad"] else f"tok {cls}".strip()
        el(f'<div class="{c}" style="left:{x}px;top:{yy}px" {attrs(t, to, "pop", 0.18)}>{txt}</div>', t, to)
        x += w + 12
    if meter_y is not None:
        el(f'<div class="meter {meter_cls}" style="top:{meter_y}px" {attrs(at, to, "left", 0.3)}><span class="lang">{esc(LANG[lang])}</span>'
           f'<span class="who">{esc(WHO[who])}</span><span class="n"><span data-count="0,{n},{round(at, 3)},{round(min(0.45, n * stg), 3)}" '
           f'data-pre="" data-suf="" data-dec="0">0</span></span></div>', at, to)
    return n


def bubble(text, small, at, to, x, y):
    el(f'<div class="bubble" style="left:{x}px;top:{y}px" {attrs(at, to, "up", 0.35)}><small>{esc(small)}</small>{esc(text)}</div>', at, to)


Q = {"en": "Will it rain in my village tomorrow?", "hi": "क्या कल मेरे गाँव में बारिश होगी?", "mr": "उद्या माझ्या गावात पाऊस पडेल का?",
     "te": "రేపు మా ఊరిలో వర్షం పడుతుందా?", "zh": "明天我们村会下雨吗？"}


def vbars(at, to, items, base_x=760, gap=230, unit=19, y0=720):
    """vertical bars: items = [(label, value, colour, show_from)]; height = value * unit px"""
    for i, (lab, v, col, t) in enumerate(items):
        x = base_x + i * gap; h = int(v * unit)
        box(f"vbar c-{col}", t, to, x, y0 - h, 120, h, "grow", 0.6, style="transform-origin:50% 100%")
        box("vnum", t + 0.3, to, x - 50, y0 - h - 74, fx="up", inner=esc(str(v)))
        box("vlab", t, to, x - 50, y0 + 18, fx="fade", inner=esc(lab))


# =====================================================================================================
# THE CUT (film seconds). VO cue in each comment; L(n) = line n of vo.txt.
# =====================================================================================================
c = lambda n: L(n) - PRE
# ---------------- Ch 1 · Can India build its own ChatGPT? ----------------
shot(0.0, "MON", "slow", ms=0.5)                                       # "Ask an A.I. one simple question."
shot(S(1, 1) - PRE, "TYP", "in", ms=6.0, dim=0.35)                     # "Will it rain in my village tomorrow?"
bubble(Q["en"], "YOU ASK", S(1, 1), L(2, 0.05), 300, 220)
shot(c(2), "plate", "slow")                                            # "Before it reads your question, the machine chops it into pieces."
bubble(Q["en"], "YOU ASK", L(2, 0.05), S(2, 1), 300, 220)
tiles("deepseek", "en", S(2, 1), LE(2), 470, cls="en", meter_y=110)   # "In English... just eight."
bubble(Q["hi"], "हिंदी · HINDI", L(3), S(3, 1) + 1.0, 300, 220)       # "Now ask it in Hindi."
tiles("deepseek", "hi", S(3, 1) + 1.2, LE(3), 470, meter_y=110)       # "On DeepSeek... eighteen. More than double."
cite("[OUR TEST | DEEPSEEK V3 TOKENIZER]", S(3, 1), LE(6))
tiles("deepseek", "mr", L(4), S(4, 1) - 0.05, 300, meter_y=110, stagger=0.045)       # "Marathi, twenty."
tiles("deepseek", "te", S(4, 1), S(4, 2) + 0.2, 300, meter_y=110)     # "Telugu, twenty-five."
# "And in those two, it even cuts some of your letters in half." -> the Telugu letter ఊ cracked, held 1.5 s (BEATS)
box("half l", S(4, 2) + 0.2, LE(4) + 1.5, 520, 170, fx="fade", d=0.3, inner="ఊ")
box("half r", S(4, 2) + 0.2, S(4, 2) + 0.8, 520, 170, fx="fade", d=0.3, inner="ఊ")
box("half r", S(4, 2) + 0.8, LE(4) + 1.5, 610, 200, fx="right", d=0.5, inner="ఊ")
box("cut", S(4, 2) + 0.6, S(4, 2) + 0.95, 860, 190, 10, 600, "grow", 0.25)
chip("1 letter = 2 pieces", S(4, 2) + 1.2, LE(4) + 1.5, 1240, 160, "red", "sm", "up")
shot(c(5), "plate", "slow")                                            # "So can India build an A.I. of its own?"
vbars(L(5), LE(6), [("English", 8, "abroad", L(5)), ("हिंदी", 18, "abroad", L(5) + 0.15), ("मराठी", 20, "abroad", L(5) + 0.3),
                    ("తెలుగు", 25, "red", L(5) + 0.45), ("中文", 7, "abroad", S(6, 2))])
chip("Can India build its own?", L(5, 0.15), LE(5) + 0.3, 110, 130, "saffron", "sm", "up")
chip("Built in China", S(6, 3), LE(6), 110, 250, "abroad", "sm", "pop")   # "Fewer than English."
shot(c(7), "SEMI", "slow", ms=2.0, dim=0.25)                           # "A machine speaks best in the language of the people who built it."
chip("Built in America · built in China", L(7, 0.45), LE(7), 120, 160, "abroad", "sm", "up")
shot(c(8), "ST_r2_phonein_2", "in", ms=4.0)                                       # "Your apps pay these machines by the piece."
chip("Pay by the piece", L(8, 0.3), LE(8), 120, 640, "paper", "sm", "up")
chip("More pieces = bigger bill", L(8, 0.6), LE(8), 120, 760, "red", "sm", "up")
shot(c(9), "D_techcrunch_go_free", "doc", origin="50% 40%", tag="DOCUMENT · TECHCRUNCH · 27 OCT 2025")   # "last November... Go free"
datebig("4 NOV 2025", "CHATGPT GO · FREE FOR A YEAR", L(9, 0.2), LE(9))
cite("[OPENAI | TECHCRUNCH 27 OCT 2025]", L(9, 0.2), LE(9))
shot(c(10), "ST_notify_1", "out", ms=1.0, dim=0.3)                            # "For the first people who signed up, that free year runs out... about now."
datebig("NOV 2026", "THE FREE YEAR ENDS", L(10, 0.5), LE(10))
shot(c(11), "VOICE", "slow", ms=1.0)                                   # "So when yours ends, whose machine...? America? China? Or here?"
chip("America?", S(11, 1), LE(11), 160, 640, "abroad", "sm", "pop")
chip("China?", S(11, 2), LE(11), 560, 640, "abroad", "sm", "pop")
chip("Or here?", S(11, 3), LE(11), 880, 640, "saffron", "sm", "pop")
shot(c(12), "CANDLE", "in", ms=2.0, tag="PEXELS · ILLUSTRATIVE FOOTAGE")   # "go back to one Monday. The twenty-seventh of January"
datebig("27 JAN 2025", "A MONDAY", L(12, 0.55), LE(12))
shot(c(13), "plate", "slow")                                           # "A small Chinese lab called DeepSeek... beaten ChatGPT in downloads"
box("plate", L(13), LE(13), 520, 300, fx="up", inner="App Store · top free apps<small>RANK 1 · DEEPSEEK · RANK 2 · CHATGPT · 27 JAN 2025</small>")
illus(L(13), LE(13), "ILLUSTRATION · RANKS FROM REUTERS")
cite("[REUTERS | 27 JAN 2025]", L(13), LE(13))
shot(c(14), "plate", "slow")                                           # "five and a half million dollars... giants spending billions"
box("brick in", L(14, 0.5), LE(14), 560, 700, fx="pop")
chip("$5.6 M · DeepSeek says", L(14, 0.5), LE(14), 420, 560, "saffron", "sm", "up")
for k in range(14):
    box("brick", S(14, 1) + k * 0.04, LE(14), 1080 + (k % 7) * 92, 700 - (k // 7) * 46, fx="pop", d=0.15)
chip("Billions", S(14, 1) + 0.4, LE(14), 1200, 500, "abroad", "sm", "up")
cite("[DEEPSEEK-V3 PAPER | ARXIV 2412.19437]", L(14), LE(14))
shot(c(15), "STK", "in", ms=1.0, tag="PEXELS · ILLUSTRATIVE FOOTAGE")   # "Nvidia loses around five hundred and ninety billion dollars"
count(L(15, 0.45), LE(15), 120, 600, 0, 593, L(15, 0.5), 0.45, "−$", " BN", "red", "xl")
chip("≈ ₹51 lakh crore", S(15, 1), LE(15), 130, 790, "red", "sm", "up")
cite("[REUTERS / LSEG | 27 JAN 2025]", L(15), LE(15))
shot(c(16), "plate", "slow")                                           # "roughly the size of India's whole Union Budget... in one day"
box("hbar c-red", L(16), LE(16) + 1.0, 260, 380, 1300, 120, "grow", 0.6)
box("hkey", L(16), LE(16) + 1.0, 260, 330, inner="NVIDIA · LOST IN ONE DAY · ≈ ₹51 LAKH CRORE")
box("hbar c-saffron", S(16, 1) + 0.4, LE(16) + 1.0, 260, 640, 1284, 120, "grow", 1.4, style="background:linear-gradient(90deg,#c76a10,#ff9933)")
box("hkey", S(16, 1) + 0.4, LE(16) + 1.0, 260, 590, inner="INDIA'S WHOLE UNION BUDGET 2025-26 · ₹50.65 LAKH CRORE")
cite("[UNION BUDGET 2025-26 | OUR CONVERSION]", S(16, 1), LE(16) + 1.0)
shot(c(17), "VAI" if have("VAI") else "PIB_image001QNTH", "crop2" if have("VAI") else "in", ms=0.2, origin="50% 18%")   # "Three days later... Ashwini Vaishnaw..."
namelt("Ashwini Vaishnaw", "UNION I.T. MINISTER · 30 JAN 2025", W(17, "minister"), SE(17, 0))
shot(S(17, 1) - PRE, "VAI" if have("VAI") else "PIB_image002946I", "crop2" if have("VAI") else "left", ms=37.5, origin="50% 18%")                       # "India will build its own A.I. model... within six months."
chip("Within 6 months", S(17, 1) + 1.5, LE(17), 120, 640, "saffron", "sm", "up")
cite("[PIB | 30 JAN 2025]", L(17), LE(17))
shot(c(18), "PIB_image002946I", "right")                               # "So did India keep that promise? You'll see."
shot(S(18, 2) - PRE, "plate", "slow")                                  # "...around minute ten, the same test again"
tiles("sarvam", "te", S(18, 2), LE(18), 420, cls="saffron")
box("blackout", S(18, 2) + 0.9, LE(18), 0, 0, 1920, 1080, fx="fade", d=0.3, style="background:rgba(10,14,21,.94);z-index:31")
chip("Around minute 10", S(18, 2) + 1.0, LE(18), 700, 480, "saffron", "", "pop")
shot(c(19), "plate", "slow")                                           # "what's actually inside one of these machines... three things"
for k, (lab, colr) in enumerate([("?", "paper"), ("?", "chip"), ("?", "saffron")]):
    box(f"frame3 c-{colr}", L(19, 0.05) + k * 0.35, LE(19), 120 + k * 580, 330, fx="pop", inner=lab)
# ---------------- Ch 2 · How ChatGPT actually works ----------------
shot(c(20), "GIRL", "slow", ms=2.0)                                    # "Picture a child who has read every book in a giant library."
shot(S(20, 1) - PRE, "LIBW", "in", ms=1.0, dim=0.35)                   # "You start a sentence... the child guesses your next word."
bubble("Will it rain in my village …", "YOU START", S(20, 1), LE(20), 300, 240)
for k, w in enumerate(["tomorrow", "?"]):
    el(f'<div class="tok en" style="left:{1180 + k * 280}px;top:420px" {attrs(S(20, 2) + k * 0.6, LE(20), "pop", 0.2)}>{w}</div>', S(20, 2) + k * 0.6, LE(20))
shot(c(21), "plate", "slow")                                           # "It guesses the next piece, again and again..."
for k, (w, p) in enumerate([("tomorrow", "71%"), ("today", "18%"), ("soon", "6%")]):
    box("plate", L(21) + k * 0.2, LE(21), 300 + k * 460, 520, fx="up", inner=f"{w}<small>NEXT-PIECE GUESS · {p}</small>",
        style="border-color:#ff9933" if k == 0 else "")
illus(L(21), LE(21))
shot(c(22), "plate", "slow")                                           # "three things. A library... A reading room... And teachers"
for k, (lab, colr, t) in enumerate([("Library", "paper", L(22, 0.05)), ("Reading room", "chip", S(22, 2)), ("Teachers", "saffron", S(22, 3))]):
    box(f"frame3 c-{colr}", t, LE(22), 120 + k * 580, 330, fx="pop", inner=lab)
shot(c(23), "HPAGE", "in", ms=8.0)                                       # "The library is words — trillions of pieces of text"
chip("Library = words", L(23, 0.1), SE(23, 0), 120, 640, "paper", "sm", "up")
shot(S(23, 1) - PRE, "LED", "slow", ms=0.5)                            # "The reading room is chips..."
chip("Reading room = chips", S(23, 1), SE(23, 1), 120, 640, "chip", "sm", "up")
shot(S(23, 2) - PRE, "ST_r2_itblr_3", "slow", ms=12.0)   # (a third use, on purpose: the only real Indian engineers we have; the laptop clip shows a fake hacker screen)                           # "And the teachers? They're engineers."
chip("Teachers = engineers", S(23, 2), LE(23), 120, 640, "saffron", "sm", "up")
shot(c(24), "BLR", "slow", ms=1.0)                                     # "India has the teachers... software for companies all over the world."
shot(S(24, 2) - PRE, "BLR2", "slow", ms=14.0)   # (the Business Standard clip burns its own captions in: dropped, round 1 review)
chip("India has the teachers", L(24, 0.1), LE(24), 120, 160, "saffron", "sm", "up")
# ---------------- Ch 3 · Why AI is weak in Indian languages ----------------
shot(c(25), "plate", "slow")                                           # "your missing pieces are the library and the reading room"
for k, (lab, colr) in enumerate([("Library", "red"), ("Reading room", "red"), ("Teachers", "saffron")]):
    box(f"frame3 c-{colr}", L(25), LE(25), 120 + k * 580, 330, fx="fade", inner=lab)
chip("Missing", L(25, 0.3), LE(25), 470, 150, "red", "sm", "stamp")
shot(c(26), "D_commoncrawl_stats", "doc", origin="30% 30%", tag="DOCUMENT · COMMON CRAWL")   # "Common Crawl... an early model"
cite("[BROWN ET AL. 2020 | GPT-3 PAPER]", S(26, 2), LE(26))
shot(c(27), "D_commoncrawl_stats", "doc", origin="80% 40%", tag="DOCUMENT · COMMON CRAWL · CC-MAIN-2026-43")   # "latest copy... two billion pages"
count(L(27, 0.3), LE(27), 120, 640, 0, 2.17, L(27, 0.35), 0.45, "", " BN PAGES", "ink", "", 2)
datebig("OCT 2026", "CC-MAIN-2026-43", L(27, 0.2), LE(27))
shot(c(28), "plate", "slow")                                           # "English? Forty-two out of every hundred pages."
for i in range(100):
    x, y = 430 + (i % 20) * 54, 220 + (i // 20) * 72
    box("pgi", L(28) + i * 0.006, LE(28), x, y, fx="pop", d=0.12)
    if i < 42:
        box("pgi en", S(28, 1) + i * 0.012, LE(28), x, y, fx="fade", d=0.12)
chip("English · 42 of 100", S(28, 1) + 0.6, LE(28), 640, 640 + 40, "abroad", "sm", "up")
shot(c(29), "plate", "slow")                                           # "For every one page in Hindi... about two hundred pages in English"
# to scale: one Hindi page against its English pages (2.4 px a page), then the camera "pulls back" on L30 to 0.3 px a page
box("onepage", L(29), LE(29), 300, 780, fx="fade")
box("hkey", L(29), LE(29), 300, 720, inner="1 HINDI PAGE")
box("stack", L(29, 0.4), LE(29), 760, 780 - 484, 260, 484, "grow", 1.0, style="transform-origin:50% 100%")
box("hkey", L(29, 0.5), LE(29), 760, 780 - 484 - 50, inner="≈ 200 ENGLISH PAGES")
cite("[COMMON CRAWL'S OWN COUNT | OCT 2026]", L(29), LE(31))
shot(c(30), "plate", "slow")                                           # "Marathi? About fifteen hundred. Telugu? About two thousand three hundred."
for x, n, lab, t in [(420, 202, "HINDI ≈ 200", L(30)), (900, 1554, "MARATHI ≈ 1,550", S(30, 1)), (1380, 2308, "TELUGU ≈ 2,300", S(30, 3))]:
    h = int(n * 0.3)
    box("stack", t, LE(30), x, 780 - h, 260, h, "grow", 0.6, style="transform-origin:50% 100%")
    box("onepage", t, LE(30), x, 784, fx="fade")
    box("hkey", t + 0.2, LE(30), x - 20, 780 - h - 50, inner=esc(lab))
box("hkey", L(30), LE(30), 120, 120, inner="ENGLISH PAGES FOR EACH ONE PAGE · SAME SCALE")
chip("8 crore speakers each", S(30, 4) + 0.4, LE(30), 120, 200, "saffron", "sm", "up")
shot(c(31), "plate", "slow")                                           # "All of India's languages... less than one page in every hundred."
for i in range(100):
    x, y = 430 + (i % 20) * 54, 220 + (i // 20) * 72
    box("pgi en" if i < 99 else "pgi in", L(31) + i * 0.004, LE(31), x, y, fx="pop", d=0.1)
chip("All Indian languages · < 1%", L(31, 0.5), LE(31), 520, 640 + 40, "saffron", "sm", "up")
shot(c(32), "KOL", "slow", ms=1.0)                                     # "More than one in every six people on Earth lives in your country."
chip("1 in 6 people on Earth", L(32, 0.2), S(32, 2), 120, 160, "saffron", "sm", "up")
shot(S(32, 2) - PRE, "CROWD", "in", ms=6.0)                            # "But in the library these machines read, your language is almost invisible."
chip("< 1% of the library", S(32, 2) + 0.4, LE(32), 120, 160, "red", "sm", "up")
shot(c(33), "plate", "slow")                                           # "China's A.I. mostly needs one written language... twenty-two... a dozen scripts"
box("shelf cn", S(33, 1), LE(33), 160, 260, 1600, None, "grow", 0.6, inner="中文")
SCRIPTS = ["हिंदी", "বাংলা", "తెలుగు", "मराठी", "தமிழ்", "اردو", "ગુજરાતી", "ಕನ್ನಡ", "ଓଡ଼ିଆ", "മലയാളം", "ਪੰਜਾਬੀ", "অসমীয়া",
           "मैथिली", "ᱥᱟᱱᱛᱟᱲᱤ", "कश्मीरी", "नेपाली", "सिन्धी", "डोगरी", "कोंकणी", "মৈতৈলোন্", "बड़ो", "संस्कृतम्"]
for k, s_ in enumerate(SCRIPTS):
    box("shelf", S(33, 2) + k * 0.06, LE(33), 160 + (k % 6) * 270, 400 + (k // 6) * 90, 250, None, "pop", 0.18, inner=esc(s_))
chip("22 languages · ~12 scripts", S(33, 3), LE(33), 160, 140, "paper", "sm", "up")
cite("[CONSTITUTION, 8TH SCHEDULE]", S(33, 2), LE(33))
shot(c(34), "BAZ", "slow", ms=2.0)                                      # "that's why your question cost so much more... the chopper learns from this library"
shot(c(35), "plate", "slow")                                           # "rain or village, one neat piece each... chopped into bits... half a letter"
el(f'<div class="tok en" style="left:300px;top:300px" {attrs(L(35, 0.1), LE(35), "pop")}>rain</div>', L(35, 0.1), LE(35))
el(f'<div class="tok en" style="left:520px;top:300px" {attrs(L(35, 0.2), LE(35), "pop")}>village</div>', L(35, 0.2), LE(35))
tiles("deepseek", "te", S(35, 1), LE(35), 560)
cite("[OUR TEST | DEEPSEEK V3 TOKENIZER]", L(35), LE(35))
shot(c(36), "HPAGE", "in", ms=0.5)                                     # "Here's the rule. A machine learns from what it reads."
chip("Rule: it learns what it reads", L(36, 0.3), LE(36), 120, 640, "paper", "sm", "up")
shot(c(37), "plate", "slow")                                           # "tiny corner of the library... learns it last... charges you more"
for i in range(100):
    x, y = 430 + (i % 20) * 54, 220 + (i // 20) * 72
    box("pgi en" if i < 99 else "pgi in", L(37), LE(37), x, y, fx="fade", d=0.1)
chip("Learned last · costs more", L(37, 0.6), LE(37), 520, 680, "red", "sm", "up")
shot(c(38), "BHD" if have("BHD") else "BHA", "slow" if have("BHD") else "crop", ms=27.7 if have("BHD") else 48.2, origin="50% 40%")                  # "someone has to build the Indian part of the library. Page by page, voice by voice."
shot(S(38, 1) - PRE, "VOICE", "in", ms=3.0)
shot(S(38, 2) - PRE, "BHD" if have("BHD") else "BHA", "slow" if have("BHD") else "crop", ms=63.5 if have("BHD") else 4.2, origin="50% 30%")
chip("Bhasha Daan · speak, write, see", S(38, 1), LE(38), 120, 160, "saffron", "sm", "up")
shot(c(39), "D_aikosh", "doc", origin="25% 85%", tag="DOCUMENT · AI KOSH · NOV 2026")   # "A.I. Kosh, now holds more than sixteen thousand collections."
count(L(39, 0.5), LE(39), 120, 160, 0, 16140, L(39, 0.55), 0.45, "", "+ DATASETS", "saffron", "sm")
cite("[AIKOSH.INDIAAI.GOV.IN | NOV 2026]", L(39), LE(39))
# ---------------- Ch 4 · India's GPU problem ----------------
shot(c(40), "LED", "in", ms=4.0)                                       # "you need a place to read it. And this is where India hits a wall."
shot(c(41), "CHIP", "in", ms=2.0)                                      # "This is the reading room. A chip like this one, made by... Nvidia"
chip("G.P.U. · lakhs of rupees each", S(41, 2), LE(41), 120, 640, "chip", "sm", "up")
shot(c(42), "RACK", "slow", ms=3.0)                                    # "you need thousands of them, wired together, running for months"
shot(c(43), "FAB", "slow", ms=2.0)                                     # "India doesn't make these chips... America... Taiwan"
chip("Designed: U.S.A.", S(43, 2), LE(43), 120, 560, "abroad", "sm", "up")
chip("Made: mostly Taiwan", S(43, 2) + 0.4, LE(43), 120, 680, "abroad", "sm", "up")
shot(S(43, 3) - PRE, "TATA", "crop", ms=74.0, origin="50% 50%")        # "If you watched our chip film, you know why."
shot(c(44), "TAP", "in", ms=40.0)                                      # "India found out how fast that door can close."
datebig("JAN 2025", "", L(44, 0.1), LE(44))
shot(c(45), "D_fr_rule_p1-01", "doc", origin="50% 20%", tag="DOCUMENT · U.S. FEDERAL REGISTER · 15 JAN 2025")   # "America's government put out a new rule"
shot(S(45, 1) - PRE, "plate", "slow")                                  # "three groups... allies freely... China blocked"
for k, (lab, colr, t) in enumerate([("Tier 1 · allies · free", "green", S(45, 2)), ("Tier 2 · capped", "amber", S(45, 1) + 0.3), ("Tier 3 · blocked", "red", S(45, 3))]):
    box("plate", t, LE(46), 200 + k * 560, 420, fx="up", inner=esc(lab), style=f"border-color:var(--{colr})")
el(f'<div class="chip c-amber" style="left:820px;top:200px" {attrs(L(46), LE(46), "stamp")}>India</div>', L(46), LE(46))
box("plate", L(46, 0.5), LE(46), 760, 600, fx="up", inner="Limit on chips<small>AI DIFFUSION RULE · 90 FR 4544</small>")
cite("[BIS | 15 JAN 2025]", S(45, 1), LE(46))
shot(c(47), "CAP", "slow", ms=2.0)                                     # "Four months later... scrapped... The tap is in someone else's hand."
datebig("12 MAY 2025", "RULE RESCINDED", L(47, 0.15), S(47, 1))
shot(S(47, 2) - PRE, "TAP", "in", ms=36.0)
chip("Someone else's tap", S(47, 2) + 0.2, LE(47), 120, 640, "red", "sm", "up")
shot(c(48), "YOT", "slow", ms=60.0)                                    # "India didn't wait... It rented one... and shared it."
shot(c(49), "ST_r2_dcc_3", "slow", ms=4.0)                                    # "Under the IndiaAI Mission... one common pool..."
chip("One common pool", L(49, 0.2), LE(49), 120, 160, "chip", "sm", "up")
chip("Govt pays part", L(49, 0.75), LE(49), 120, 280, "saffron", "sm", "up")
shot(c(50), "plate", "slow")                                           # "eighteen thousand... forty-five thousand"
count(L(50, 0.1), LE(50), 300, 420, 0, 18693, L(50, 0.12), 0.45, "", " CHIPS", "chip", "xl")
chip("JAN 2025", L(50, 0.1), SE(50, 0), 300, 300, "slate", "sm", "fade")
count(S(50, 1), LE(50), 300, 640, 18693, 45000, S(50, 1) + 0.2, 0.45, "", "+ CHIPS", "saffron", "xl")
chip("JUNE 2026", S(50, 1), LE(50), 300, 800, "slate", "sm", "fade")
cite("[PIB | 30 JAN 2025 · JUNE 2026]", L(50), LE(50))
shot(c(51), "plate", "slow")                                           # "Meta... three hundred and fifty thousand... almost eight times"
box("dotf c-saffron", S(51, 1), LE(51), 160, 300, 212, 212, "pop", style="color:var(--saffron)")
box("hkey", S(51, 1), LE(51), 160, 540, inner="INDIA'S POOL · 45,000")
box("dotf c-abroad", S(51, 1) + 1.2, LE(51), 560, 300, 1000, 350, "grow", 1.0, style="color:var(--abroad)")   # 1 px² = 1 chip: 350,000 vs 212² = 44,944
box("hkey", S(51, 1) + 1.6, LE(51), 560, 680, inner="ONE COMPANY · META · ≈ 350,000 (TARGET, END 2024)")
cite("[ZUCKERBERG | JAN 2024]", S(51, 1), LE(51))
shot(c(52), "plate", "slow")                                           # "India's whole A.I. mission is about ten thousand crore rupees"
box("brick in", S(52, 1) + 0.4, LE(54), 200, 690, fx="pop")
box("hkey", S(52, 1) + 0.6, LE(54), 120, 750, inner="INDIA AI MISSION · ₹10,372 CR · 5 YEARS")
cite("[PIB | 7 MAR 2024]", S(52, 1), LE(52))
shot(c(53), "plate", "slow")                                           # "Meta... around thirteen lakh crore rupees... much of it for A.I."
for k in range(126):
    box("brick", L(53, 0.3) + k * 0.025, LE(54), 520 + (k % 14) * 92, 690 - (k // 14) * 46, fx="pop", d=0.12)
box("hkey", L(53, 0.4), LE(54), 520, 230, inner="META · 2026 · ≈ ₹13 LAKH CRORE ($135-145 BN)")
cite("[META Q3 2026 RESULTS]", L(53), LE(54))
shot(c(54), "plate", "slow")                                           # "That's not double. That's more than a hundred times as much."
chip("> 100×", S(54, 3), LE(54), 120, 200, "red", "xl", "stamp")
shot(c(55), "plate", "slow")                                           # "So is it hopeless? No. Because remember DeepSeek."
chip("Hopeless?", L(55), S(55, 1), 700, 440, "slate", "", "pop")
chip("No.", S(55, 1), LE(55), 820, 440, "saffron", "xl", "pop")
shot(c(56), "D_deepseek_p11-11", "doc", origin="50% 90%", tag="DOCUMENT · DEEPSEEK-V3 TECHNICAL REPORT")   # "about two thousand chips... cut-down version"
count(L(56, 0.2), LE(56), 120, 500, 0, 2048, L(56, 0.25), 0.45, "", " H800 CHIPS", "chip", "")
chip("Cut-down, for China", S(56, 2), LE(56), 120, 640, "abroad", "sm", "up")
cite("[DEEPSEEK-V3 PAPER | ARXIV 2412.19437]", L(56), LE(56))
shot(c(57), "BLR", "slow", ms=4.0)                                     # "You need clever engineering... Indian engineers can play."
chip("Clever beats biggest", S(57, 1) + 0.3, LE(57), 120, 640, "saffron", "sm", "up")
# ---------------- Ch 5 · What India built: Sarvam and BharatGen ----------------
shot(c(58), "BLR2", "slow", ms=10.0)                                   # "April twenty twenty-five... A Bengaluru startup called Sarvam."
datebig("APR 2025", "INDIAAI PICKS ITS FIRST MODEL BUILDER", L(58, 0.05), LE(58))
chip("Sarvam · Bengaluru", L(58, 0.7), LE(58), 120, 640, "saffron", "", "up")
shot(c(59), "PKN" if have("PKN") else "D_sarvam_blog", "crop2" if have("PKN") else "doc", ms=5.1, origin="32% 45%")   # "Vivek Raghavan and Pratyush Kumar... four thousand chips"
namelt("Pratyush Kumar", "CO-FOUNDER, SARVAM · WITH VIVEK RAGHAVAN", L(59, 0.2), S(59, 1))
count(S(59, 1), LE(59), 120, 640, 0, 4096, S(59, 1) + 0.6, 0.45, "", " H100 CHIPS", "chip", "")
shot(c(60), "D_sarvam_105b_hf", "doc", origin="50% 30%", tag="DOCUMENT · HUGGING FACE")   # "Sarvam's next model is built on top of a French one"
chip("May 2025 · built on a French base", L(60, 0.35), LE(60), 120, 640, "abroad", "sm", "up")
shot(c(61), "ST_r2_itblr_0", "slow", ms=22.0)   # (the NDTV clip at 15 s is a stage with its own anchor captions: not used)                                    # "Can an Indian team train one from zero, start to finish, at home?"
box("prog", S(61, 2), LE(61), 360, 680, inner='<div class="fill" style="transform:scaleX(0.02)"></div>')
chip("From zero?", S(61, 2) + 0.3, LE(61), 720, 640, "saffron", "sm", "pop")
shot(c(62), "PMX" if have("PMX") else "CITY", "slow", ms=5.3)         # "February twenty twenty-six. Bharat Mandapam, Delhi."
datebig("18 FEB 2026", "BHARAT MANDAPAM · AI IMPACT SUMMIT", L(62, 0.05), LE(62))
shot(c(63), "PMX" if have("PMX") else "D_sarvam_blog", "slow" if have("PMX") else "doc", ms=25.1, origin="50% 35%")   # "two new models... a hundred and five billion parameters"
count(S(63, 1) + 0.4, SE(63, 1) + 3.5, 120, 640, 0, 105, S(63, 1) + 0.5, 0.45, "", " BN DIALS", "saffron", "xl")
shot(c(64), "ST_r2_dc_0", "slow", ms=8.0)                                    # "Trained from scratch. In India... twelve trillion pieces"
el(f'<div class="prog" style="top:680px" {attrs(L(64), LE(64), "fade")}><div class="fill" data-at="{round(L(64) + 0.2, 3)}" data-fx="grow" data-d="3.0"></div></div>', L(64), LE(64))
chip("Trained from scratch · in India", L(64), S(64, 3), 120, 160, "saffron", "sm", "up")
count(S(64, 3) + 0.8, LE(64), 120, 160, 0, 12, S(64, 3) + 1.0, 0.45, "", " TRILLION PIECES", "paper", "sm")
cite("[SARVAM | FEB 2026]", L(64), LE(64))
shot(c(65), "D_sarvam_105b_hf", "doc", origin="70% 30%", tag="DOCUMENT · HUGGING FACE · APACHE 2.0")   # "made the model open... download it... for free"
chip("Open · free to build on", L(65, 0.35), LE(65), 120, 640, "saffron", "sm", "up")
shot(c(66), "plate", "slow")                                           # "six months... ten at the most... about a year... delivered"
box("tline", L(66), LE(66) + 1.2, 140, 560, None, None, "grow", 0.6)
for k, (x, lab, small, t) in enumerate([(140, "30 JAN 2025", "THE PROMISE", L(66)), (560, "+6 MONTHS", "HOPED", S(66, 0) + 0.8),
                                        (980, "+10 MONTHS", "AT THE MOST", S(66, 0) + 2.4), (1400, "18 FEB 2026", "DELIVERED", S(66, 1))]):
    box("tick", t, LE(66) + 1.2, x + 13, 563, fx="pop")
    box("tlab", t, LE(66) + 1.2, x, 600, fx="up", inner=f"<small>{esc(small)}</small>{esc(lab)}")
shot(c(67), "BGN" if have("BGN") else "D_bharatgen_blog", "crop2" if have("BGN") else "doc", ms=111.9, origin="50% 25%")   # "BharatGen... Param Two... twenty-two languages"
chip("BharatGen · IIT Bombay", L(67, 0.2), LE(67), 120, 640, "saffron", "sm", "up")
chip("Param2 · 22 languages", L(67, 0.6), LE(67), 120, 760, "saffron", "sm", "up")
# ---- the payoff: the same test, three choppers
shot(c(68), "TYP", "in", ms=3.0, dim=0.3)                              # "Now remember my promise to you. The chopping test. Same question."
bubble(Q["en"], "SAME QUESTION", S(68, 2), LE(68), 300, 260)
shot(c(69), "plate", "slow")                                           # "DeepSeek's chopper... 18, 20, 25"
ROWS = [("deepseek", "abroad", 69), ("chatgpt", "abroad", 70), ("sarvam", "saffron", 71)]
for r, (who, colr, ln) in enumerate(ROWS):
    y = 220 + r * 230; t0 = L(ln)
    box("hkey", t0, LE(71) + 1.0, 120, y, inner=esc(WHO[who]))
    for k, lang in enumerate(["hi", "mr", "te"]):
        n = len(TOK[who][lang]); tk = S(ln, k + 1) if ln != 70 else S(70, 1) + k * 1.0
        box(f"hbar c-{'saffron' if colr == 'saffron' else 'slate'}", tk, LE(71) + 1.0, 560 + k * 430, y + 50, n * 15, 70, "grow", 0.4)
        box("hval", tk + 0.2, LE(71) + 1.0, 560 + k * 430, y - 10, fx="up", inner=f"{esc(LANG[lang].split(' · ')[0])} {n}")
chip("= English", S(71, 1) + 1.2, LE(71) + 1.0, 700, 720, "saffron", "sm", "pop")
cite("[OUR TEST | 3 TOKENIZERS]", L(69), LE(71) + 1.0)
shot(c(72), "plate", "slow")                                           # "a thousand sentences, each in thirteen languages"
FL = json.loads((P / "research/token_test_flores200.json").read_text())
LG = [("hin_Deva", "हिंदी"), ("ben_Beng", "বাংলা"), ("mar_Deva", "मराठी"), ("tel_Telu", "తెలుగు"), ("tam_Taml", "தமிழ்"), ("guj_Gujr", "ગુજરાતી"),
      ("kan_Knda", "ಕನ್ನಡ"), ("mal_Mlym", "മലയാളം"), ("pan_Guru", "ਪੰਜਾਬੀ"), ("ory_Orya", "ଓଡ଼ିଆ")]
for k, (code, lab) in enumerate(LG):
    y = 150 + k * 82; ds = FL[code]["deepseekV3"] / FL["eng_Latn"]["deepseekV3"]; sv = FL[code]["sarvam"] / FL["eng_Latn"]["sarvam"]
    t = S(72, 1) + k * 0.12
    box("hkey", t, LE(73), 120, y + 18, inner=esc(lab))
    box("hbar c-slate", t, LE(73), 420, y, int(ds * 230), 34, "grow", 0.4)
    box("hbar c-saffron", t + 0.5, LE(73), 420, y + 38, int(sv * 230), 34, "grow", 0.4, style="background:linear-gradient(90deg,#c76a10,#ff9933)")
box("hkey", S(72, 1), LE(73), 1500, 260, inner="GREY · DEEPSEEK<br/>SAFFRON · SARVAM<br/>× ENGLISH")
cite("[OUR TEST | FLORES-200, 1,012 SENTENCES]", S(72, 1), LE(73))
chip("Odia · 5.5× → 1.4×", S(73, 1), LE(73), 1300, 680, "saffron", "sm", "pop")
shot(c(74), "plate", "slow")                                           # "the gap shrinks, a lot... an Indian team put the missing pieces in"
for k, (lab, colr) in enumerate([("Library", "saffron"), ("Reading room", "chip"), ("Teachers", "saffron")]):
    box(f"frame3 c-{colr}", L(74) + k * 0.2, LE(74), 120 + k * 580, 330, fx="pop", inner=lab)
shot(c(75), "KIS", "slow", ms=63.0, tag="FOOTAGE · AGRICULTURE INDIA · KISAN E-MITRA (A GOVERNMENT CHATBOT)")   # "Sarvam says its models help run Aadhaar services... Maharashtra..."
chip("Aadhaar · Sarvam says", S(75, 1), S(75, 2), 120, 160, "saffron", "sm", "up")
datebig("28 OCT 2026", "MAHARASHTRA · 2,500 OFFICIALS", S(75, 2), LE(75))
cite("[FORBES INDIA · AIM NETWORK]", L(75), LE(75))
# ---------------- Ch 6 · Has India caught up? ----------------
shot(c(76), "CITY", "slow", ms=4.0, dim=0.3)                           # "has India built its own ChatGPT? ... Not yet."
chip("Not yet", S(76, 3), LE(76), 120, 640, "red", "", "stamp")
shot(c(77), "plate", "slow")                                           # "DeepSeek's newest big model has one point six trillion..."
box("dotf c-saffron", L(77, 0.2), LE(77), 200, 360, 120, 120, "pop", style="color:var(--saffron)")
box("hkey", L(77, 0.2), LE(77), 160, 500, inner="SARVAM · 105 BN")
box("dotf c-abroad", L(77, 0.45), LE(77), 560, 220, 600, 365, "grow", 1.0, style="color:var(--abroad)")   # 1.6 TN / 105 BN = 15.2 x 120²
box("hkey", L(77, 0.6), LE(77), 560, 620, inner="DEEPSEEK V4 PRO · 1.6 TRILLION · ≈ 15×")
shot(c(78), "D_sarvam_blog", "doc", origin="50% 70%", tag="DOCUMENT · SARVAM BLOG")   # "Sarvam says it plainly... bigger clusters, bigger budgets"
chip("Others: bigger clusters, bigger budgets", L(78, 0.4), LE(78), 120, 640, "abroad", "sm", "up")
shot(c(79), "plate", "slow")                                           # "the real scoreboard..."
for k, (lab, st, colr, t) in enumerate([("Teachers", "HAVE", "saffron", S(79, 1)), ("Library", "STARTED", "paper", S(79, 2)), ("Reading room", "RENTED", "abroad", S(79, 3))]):
    box(f"frame3 c-{'saffron' if colr == 'saffron' else 'paper' if colr == 'paper' else 'chip'}", t, LE(79), 120 + k * 580, 330, fx="pop", inner=f"{lab}<br/>{st}")
shot(c(80), "D_aikosh", "doc", origin="50% 30%", tag="DOCUMENT · AI KOSH")   # "twenty Indian proposals... up to a trillion dials"
chip("20 proposals picked", L(80, 0.25), LE(80), 120, 640, "saffron", "sm", "up")
chip("Goal: 1 trillion dials", L(80, 0.65), LE(80), 120, 760, "paper", "sm", "up")
shot(c(81), "MON", "slow", ms=8.0)                                     # "So here's the lesson. A machine speaks best..."
shot(c(82), "RUP", "in", ms=1.0)                                       # "If India only rents... paying extra to be understood"
chip("Paying extra", L(82, 0.4), LE(82), 120, 640, "red", "sm", "up")
shot(c(83), "plate", "slow")                                           # "an Indian machine that reads your Hindi, Marathi, Telugu, Bengali or Odia..."
for k, lab in enumerate(["हिंदी", "मराठी", "తెలుగు", "বাংলা", "ଓଡ଼ିଆ"]):
    el(f'<div class="tok saffron" style="left:{220 + k * 300}px;top:460px" {attrs(L(83, 0.05) + k * 0.25, LE(83), "pop", 0.2)}>{lab}</div>', L(83, 0.05) + k * 0.25, LE(83))
shot(c(84), "ST_notify_1", "slow", ms=4.0, dim=0.2)                                      # "check your ChatGPT plan before the free year ends..."
chip("Check your plan", L(84, 0.3), LE(84), 120, 640, "saffron", "sm", "up")
shot(c(85), "FARM", "slow", ms=1.0)                                    # "ask the same question in your own language to two or three..."
shot(S(85, 1) - PRE, "IND" if have("IND") else "D_techcrunch_indus", "slow" if have("IND") else "doc", ms=5.0, origin="30% 40%")
shot(S(85, 2) - PRE, "KIS", "slow", ms=1.0)
chip("Pay for the one that understands you", S(85, 2), LE(85), 120, 160, "saffron", "sm", "up")
shot(c(86), "ST_r2_inflag_1", "slow", ms=1.0)
shot(W(86, "Navik") - PRE, "NAV" if have("NAV") else "ST_satellite_0", "slow", ms=10.0)          # "NavIC... why does your phone still lean on America's G.P.S.?"
chip("NavIC · next story", S(86, 1), LE(86), 120, 640, "saffron", "sm", "up")
shot(c(87), "plate", "slow")                                           # "Ask any A.I. one question in your mother tongue... tell me in the comments"
bubble("Which A.I. answered best in your language?", "TELL ME IN THE COMMENTS", L(87, 0.1), VO_END - 1.6, 300, 380)
shot(c(88), "plate", "slow")                                           # "This is Be Practical with Kishore. Stay practical. Jai Hind."


# =====================================================================================================
# WORD-LEVEL CUTAWAYS (owner, after r1): every name, place, number and verb gets its own picture on the word.
# word_map.md is the plan; W(line, "word") is the word's film time. Over an animated plate the cutaway is dimmed
# so the animation stays on top (three layers). No stock clip more than twice (owner's standing note).
# =====================================================================================================
D = dict(move="doc", origin="50% 30%")
# real camera footage only, matched to the situation (owner, round 2: "all should look real and should match situation");
# rejected by eye: CGI flags, satellites, HUDs, green-screen calendars, timers, progress bars, Western classrooms, a posed
# actor, a "Mumbai" skyline that is Taipei, Pakistani rupee notes, CGI yuan, an "Aadhaar centre" photo of an MLA office.
ins(W(1, "rain"), "RAIN", 1.0, ms=2.0)                                  # "Will it rain
ins(W(1, "village"), "ST_r2_village_5", 1.6, ms=1.0)                    #  in my village tomorrow?"
ins(W(3, "DeepSeek"), "D_deepseek_v3_abs", 1.1, **D)                    # "On DeepSeek,
ins(W(3, "Chinese"), "ST_r2_china_3", 1.2, ms=2.0)                      #  the famous Chinese A.I."
ins(W(4, "Marathi"), "ST_pune_1", 1.3, ms=1.0)                          # "Marathi, twenty."
ins(W(4, "Telugu"), "ST_hyderabad_1", 1.3, ms=2.0)                      # "Telugu, twenty-five."
ins(W(5, "India"), "ST_r2_inflag_3", 1.4, ms=1.0)                       # "So can India build...
ins(W(6, "Chinese"), "ST_r2_cnflagr_2", 1.4, ms=1.0)                    # "Ask it in Chinese."
ins(W(7, "people"), "FAB", 2.2, ms=6.0, dim=0.25)               # "the people who built it."
ins(W(8, "pride"), "ST_inflag_1", 1.3, ms=2.0)                          # "not just pride."
ins(W(8, "apps"), "ST_appstore_2", 1.5, ms=1.0)                         # "Your apps pay these machines"
ins(W(9, "signed"), "TYP2", 1.4, ms=1.0)                                # "Maybe you signed up too."
ins(W(9, "biggest"), "CROWD", 1.6, ms=8.0)                              # "one of its biggest markets."
ins(W(11, "America"), "ST_usflag_1", 1.3, ms=1.0)                       # "One built in America?
ins(W(11, "China"), "ST_r2_cnflagr_2", 1.3, ms=6.0)                     #  One built in China?
ins(W(11, "here"), "ST_r2_inflag_3", 1.8, ms=8.0)                       #  Or one built here?"
ins(W(13, "Chinese"), "ST_r2_shanghai_2", 1.3, ms=3.0)                  # "A small Chinese lab
ins(W(13, "DeepSeek"), "D_deepseek_p1-01", 1.3, **D)                    #  called DeepSeek"
ins(W(13, "downloads"), "ST_r2_phonein_2", 1.2, ms=1.0)                 # "in downloads
ins(W(13, "Apple's"), "ST_appstore_2", 1.3, ms=6.0)                     #  on Apple's App Store
ins(W(13, "America"), "ST_usflag_0", 1.4, ms=2.0)                       #  in America."
ins(W(14, "five"), "ST_r2_usd_1", 1.6, ms=1.0)                          # "five and a half million dollars."
ins(W(14, "American"), "ST_wallst_2", 1.6, ms=2.0)                      # "The American giants"
ins(W(15, "Nvidia"), "NVD", 1.8, ms=20.0)
namelt("Jensen Huang", "NVIDIA CEO", W(15, "Nvidia") + 0.1, W(15, "Nvidia") + 1.6)                               # "chip company Nvidia"
ins(W(15, "fifty"), "RUP", 1.5, ms=3.0)                                 # "fifty lakh crore rupees."
ins(W(16, "India's"), "ST_r2_parl_0", 1.5, ms=2.0)                      # "India's whole Union Budget"
ins(W(17, "Delhi"), "ST_delhi_0", 1.2, ms=12.0)                         # "in Delhi,"
ins(W(19, "inside"), "RACK", 1.4, ms=8.0)                               # "what's actually inside"
ins(W(19, "magic"), "PCB", 1.4, ms=2.0)                                 # "it isn't magic."
ins(W(20, "library"), "LIBA", 1.6, ms=5.0)                              # "a giant library."
ins(W(20, "start"), "TYP2", 1.4, ms=5.0)                                # "You start a sentence"
ins(W(21, "chatbot"), "ST_notify_0", 1.6, ms=2.0)                       # "all a chatbot does."
ins(W(22, "library"), "LIBW", 1.3, ms=6.0)                              # "A library to read.
ins(W(22, "reading"), "SEMI", 1.3, ms=2.0)                              #  A reading room
ins(W(22, "teachers"), "ST_r2_itblr_0", 1.8, ms=2.0)                    #  And teachers"
ins(W(23, "chips"), "ST_wafer_1", 1.3, ms=2.0)                          # "The reading room is chips,"
ins(W(24, "teachers"), "ST_r2_itblr_3", 1.6, ms=1.0)                    # "India has the teachers."
ins(W(24, "Indian"), "ST_r2_itblr_0", 1.6, ms=12.0)                     # "Indian engineers write software"
ins(W(29, "fifty"), "ST_varanasi_2", 1.8, ms=3.0)                       # "more than fifty crore people."
ins(W(30, "eight"), "KOL", 1.6, ms=8.0)                                 # "around eight crore people"
ins(W(33, "China's"), "ST_r2_china_4", 1.4, ms=2.0)                     # "China's A.I."
ins(W(33, "scripts"), "BAZ", 1.6, ms=6.0)                               # "a dozen different scripts."
ins(W(34, "library"), "LIBA", 1.6, ms=12.0)                        # "this same library."
ins(W(35, "rain"), "RAIN", 1.1, ms=9.0)                                 # "like rain
ins(W(35, "village"), "ST_r2_village_0", 1.2, ms=1.0)                   #  or village"
ins(W(38, "Page"), "ST_books_0", 1.3, ms=1.0)                           # "Page by page,"
ins(W(39, "government"), "ST_r2_parl_0", 1.5, ms=9.0)                   # "A government data shelf"
ins(W(40, "words"), "NEWS", 1.4, ms=8.0)                               # "words are only half of it."
ins(W(41, "Nvidia"), "NVD", 1.2, ms=85.0, tag="FOOTAGE · NVIDIA")                # "made by... Nvidia."
ins(W(43, "America"), "ST_usflag_1", 1.3, ms=6.0)                       # "designed in America
ins(W(43, "Taiwan"), "ST_taipei_1", 1.6, ms=2.0)                        #  and made mostly in Taiwan."
ins(W(45, "America's"), "ST_whitehouse_0", 1.6, ms=3.0)                 # "America's government"
ins(W(45, "China"), "ST_r2_china_1", 1.4, ms=2.0)                       # "China was blocked."
ins(W(47, "scrapped"), "D_bis_rescission", 1.8, **D)                    # "scrapped that rule."
ins(W(49, "IndiaAI"), "D_indiaai_compute", 1.5, **D)                    # "Under the IndiaAI Mission,"
ins(W(49, "startups"), "ST_r2_itblr_3", 1.5, ms=6.0)                    # "Indian startups and researchers"
ins(W(51, "American"), "ST_usflag_0", 1.3, ms=9.0)                      # "one American company, Meta,"
ins(W(53, "investors"), "ST_nyse_1", 1.5, move="in")                    # "Meta told its investors"
ins(W(53, "buildings"), "ST_dcbuild_1", 1.6, ms=2.0)                    # "on buildings and machines"
ins(W(55, "DeepSeek"), "D_deepseek_v3_abs", 1.3, move="doc", origin="50% 60%")   # "Because remember DeepSeek."
ins(W(56, "China"), "ST_r2_shanghai_0", 1.4, ms=4.0)                    # "sold to China."
ins(W(57, "biggest"), "ST_r2_dc_0", 1.3, ms=2.0)                             # "the biggest room."
ins(W(57, "clever"), "PCB", 1.5, ms=8.0)                                # "clever engineering."
ins(W(58, "government"), "PIB_image002946I", 1.4, move="left")          # "The government picks"
ins(W(58, "Sarvam"), "PMX" if have("PMX") else "D_sarvam_blog", 1.8, ms=5.3)   # "A Bengaluru startup called Sarvam."
ins(W(59, "Nvidia"), "NVD", 1.5, ms=30.0, tag="FOOTAGE · NVIDIA · H100 MODULE")                              # "those Nvidia chips"
ins(W(60, "French"), "ST_paris_1", 1.6, ms=2.0)                         # "on top of a French one."
ins(W(61, "home"), "ST_delhi_1", 1.4, ms=6.0)                           # "at home?"
ins(W(62, "Delhi"), "ST_delhi_0", 1.2, ms=24.0)                         # "Bharat Mandapam, Delhi."
ins(W(64, "India"), "ST_r2_inflag_1", 1.3, ms=6.0)                                # "In India."
ins(W(66, "minister"), "VAI" if have("VAI") else "PIB_image001QNTH", 1.6, ms=62.0, move="crop2", origin="50% 18%")   # "The minister had hoped"
ins(W(67, "Param"), "D_bharatgen_param2_hf", 1.6, **D)                  # "called Param Two"
ins(W(68, "village"), "ST_pune_0", 1.4, ms=3.0)                         # "in my village tomorrow?"
ins(W(73, "Odia"), "ST_konark_1", 1.6, ms=3.0, tag="PIXABAY · ODISHA")  # "Look at Odia."
ins(W(75, "Maharashtra"), "ST_mantralaya_1", 1.6, move="in")            # "Maharashtra gave..."
ins(W(77, "DeepSeek's"), "D_deepseek_p5-05", 1.4, **D)                  # "DeepSeek's newest big model"
ins(W(78, "clusters"), "ST_r2_dcc_3", 1.3, ms=2.0)                             # "far bigger clusters,
ins(W(78, "budgets"), "ST_r2_usd_0", 1.5, ms=2.0)                       #  with far bigger budgets."
ins(W(80, "BharatGen's"), "BGN" if have("BGN") else "D_bharatgen_blog", 1.6, ms=116.0)   # "BharatGen's mandate"
ins(W(82, "languages"), "NEWS", 1.6, ms=4.0)                            # "in our own languages."
for lw, city, m, tg in [("Hindi", "ST_varanasi_0", 3.0, "PIXABAY · VARANASI"), ("Marathi", "ST_pune_0", 6.0, "PIXABAY · PUNE"),
                        ("Telugu", "ST_hyderabad_0", 4.0, "PIXABAY · HYDERABAD"), ("Bengali", "ST_kolkata_0", 4.0, "PIXABAY · KOLKATA"),
                        ("Odia", "ST_konark_1", 14.0, "PIXABAY · ODISHA")]:
    ins(W(83, lw), city, 0.9, ms=m, dim=0.45, tag=tg)                   # "reads your Hindi, Marathi, Telugu, Bengali or Odia"
ins(W(85, "Chat", 0), "D_techcrunch_go_free", 1.0, **D)                 # "Chat G.P.T.,
ins(W(85, "DeepSeek"), "D_deepseek_v3_abs", 1.0, move="doc", origin="50% 50%")   #  DeepSeek,"
ins(W(85, "understands"), "ST_farmerphone_1", 1.8, ms=2.0)              # "the one that really understands you."
ins(W(86, "phone"), "ST_notify_0", 1.4, ms=6.0)                         # "why does your phone
ins(W(86, "America's"), "CAP", 1.6, ms=6.0)                             #  still lean on America's G.P.S.?"
ins(W(87, "mother"), "ST_farmerphone_1", 1.6, ms=9.0)                   # "in your mother tongue"
ins(W(88, "Jai"), "ST_inflag_1", 1.6, ms=6.0, dim=0.2)                  # "Jai Hind."


# ---------------- sound cues (build/make_sound.py reads build/sound.json) ----------------
SFX = []


def sfx(name, at, gain=0.0):
    SFX.append((name, round(at, 3), gain))


sfx("keyboard_type", S(1, 1) - 0.4, -6)
sfx("tile_run", S(2, 1)); sfx("tile_run", S(3, 1) + 1.2); sfx("tile_run", L(4)); sfx("tile_run", S(4, 1))
sfx("glass_crack", S(4, 2) + 0.6, 2); sfx("tile_tick", S(6, 2), 4)
sfx("notify_ping", L(9, 0.2)); sfx("market_bell", L(12, 0.5)); sfx("notify_ping", L(13, 0.1))
sfx("counter_tick", L(15, 0.5)); sfx("low_thud", S(16, 1) + 1.8, -2)
sfx("page_turn", L(20), 6); sfx("paper_riffle", L(29, 0.4), 6); sfx("paper_riffle", S(30, 1), 6); sfx("paper_riffle", S(30, 3), 6)
sfx("tile_run", S(35, 1)); sfx("server_hum", L(40), -4); sfx("server_hum", L(41, 0.5), -6)
sfx("water_stop", L(44), 4); sfx("lock_click", L(46), 2); sfx("water_stop", S(47, 2), 4)
sfx("counter_tick", L(50, 0.55)); sfx("counter_tick", S(50, 1) + 0.2); sfx("brick_thud", S(52, 1) + 0.4, 4)
for k in range(0, 126, 9):
    sfx("brick_thud", L(53, 0.3) + k * 0.025, -4)
sfx("braam", S(54, 3) - 0.1, -1); sfx("low_thud", S(54, 3), -2); sfx("chime_bright", S(55, 1), 2)
sfx("counter_tick", S(64, 3) + 1.0); sfx("tile_run", L(69)); sfx("tile_run", L(70)); sfx("chime_bright", S(71, 1) + 0.3, 4)
sfx("low_thud", S(76, 3), -4); sfx("tile_run", L(83, 0.25))
# music: (cue, film start, source in-point, film end); 1.5 s of silence before the L54 reveal; the score turns at "No."
MUSIC = [("cue1_open", 0.0, 0.0, 90.0), ("cue1_open", 90.0, 22.0, c(20)), ("cue2_library", c(20), 0.0, c(20) + 150.0),
         ("cue2_library", c(20) + 150.0, 40.0, c(40)), ("cue3_wall", c(40), 0.0, LE(53) + 0.05),
         ("cue4_build", S(55, 1), 0.0, S(55, 1) + 170.0), ("cue5_honest", S(55, 1) + 170.0, 0.0, END)]
SILENT = [(LE(53) + 0.05, S(55, 1)), (LE(67) + 0.1, L(68) + 0.4)]   # the reveal and the music drop before the payoff


# =====================================================================================================
# machinery (from the pharma film)
# =====================================================================================================
def captions():
    out = []
    for r in SENTS:
        a, b, text = F(r["start"]), F(r["end"]), r["en"]
        text = text.replace("Navik", "NavIC")   # the VO respelling stays out of the captions
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
        for p in split:
            d = (b - a) * len(p) / tot
            out.append((round(t, 2), round(t + d, 2), esc(p))); t += d
    held = []
    for i, (a, b, p) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else b + 1.0
        held.append((a, round(max(b, min(b + 0.35, nxt - 0.03)), 2), p))
    return held


def film_vo():
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
        cc = min(starts, key=lambda x: abs(x - END * k / n))
        b.append(round((round(cc * FPS) + round(XF * FPS)) / FPS, 4))
    return b + [END]


RESET = 4.6
FRAMES = {"doc": [("doc", "50% 28%"), ("doc", "50% 52%"), ("doc", "50% 76%")],
          "crop": [("crop2", "28%"), ("crop", "50%"), ("crop2", "72%")],
          "foot": [("cutA", "32% 38%"), ("cutB", "68% 58%"), ("cutA", "62% 34%"), ("cutB", "36% 62%")]}


def split_long():
    """every hold over RESET becomes near-equal pieces, each a new framing; plates (animated beats) stay whole"""
    out = []
    for s, nxt in zip(SEQ, SEQ[1:] + [dict(t0=END)]):
        d = nxt["t0"] - s["t0"]; ms = s["ms"]
        if d <= RESET + 0.4 or s["src"] == "plate":
            out.append(dict(s, ms=ms[0] if isinstance(ms, list) else ms)); continue
        n = math.ceil(d / RESET); step = d / n
        kind = "doc" if s["src"].startswith("D_") or s["src"].startswith("PIB_") else "crop" if s["move"] == "crop" else "foot"
        for k in range(n):
            p = dict(s, t0=r3(s["t0"] + k * step))
            p["ms"] = r3((ms[0] if isinstance(ms, list) else ms) + k * step)
            if k:
                p["move"], p["origin"] = FRAMES[kind][(k - 1) % len(FRAMES[kind])]
                if kind == "crop":
                    p["origin"] += " " + (s["origin"] or "50% 50%").split()[1]
            out.append(p)
    SEQ[:] = out


_RATE = {}


def rate(src):
    if src not in _RATE:
        r = 30.0
        m = media(src)
        if m.parent.name == "conformed":
            n, dd = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                                    "-of", "csv=p=0", str(media(src, raw=True))], capture_output=True, text=True).stdout.strip().split("/")
            r = int(n) / int(dd)
        _RATE[src] = r
    return _RATE[src]


CLEAN = {   # clean spans checked by eye on qa/owner_spans.jpg (raw source seconds)
    "BSW": [(68.5, 70.7), (70.9, 74.9)],                       # Wipro only (the rest of the clip is AI-made art and text cards)
    "YOT": [(10.3, 22.0), (24.8, 35.7), (42.5, 59.7), (59.9, 64.5)],
    "BHA": [(4.1, 6.9), (13.9, 15.6), (15.8, 17.1), (48.1, 50.4)],
    "KIS": [(0.3, 3.9), (14.5, 16.8), (62.2, 67.7), (88.7, 89.9)],
    "TATA": [(72.8, 85.7)],
    "NVD": [(0.5, 12.5), (17.0, 42.0), (84.6, 87.6)],   # Jensen Huang to camera; the closing logo card
    # the owner's YouTube clips (qa/yt_spans.jpg): spans between their own cuts, 0.1 s clear
    "VAI": [(0.2, 13.3), (20.5, 30.9), (37.5, 52.8), (60.4, 84.6), (92.3, 118.3)],
    "PMX": [(5.3, 14.8), (25.1, 27.0), (27.2, 28.6), (29.9, 35.1), (51.5, 64.5)],
    "PKN": [(5.1, 24.7)],
    "BGN": [(111.9, 123.9)],
    "BHD": [(27.7, 28.8), (29.9, 31.5), (31.7, 32.7), (32.9, 34.0), (35.3, 37.3), (63.5, 65.7), (65.9, 68.5)],
    "IND": [(0.5, 59.9)],
    "NAV": [(15.3, 54.4)],
}


def clean_ranges(src):
    if src in CLEAN:
        return CLEAN[src]
    return None


def clean_assign():
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
        plan = None
        for n in (1, 2, 3, 4):
            sub = film / n
            if n > 1 and sub < 1.3:
                break
            picks = []
            for k in range(n):
                cnd = best(s["src"], rs, (sub + tail) * sp, s["ms"] + k * 2.0)
                if cnd is None:
                    break
                picks.append(cnd[1]); used.setdefault(s["src"], []).append((cnd[1], cnd[1] + sub * sp))
            rep = sum(overlap(s["src"], x, x + sub * sp) - sub * sp for x in picks) if len(picks) == n else None
            for _ in picks:
                used[s["src"]].pop()
            if rep is not None and (plan is None or rep + 0.4 * (n - 1) < plan[0]):
                plan = (rep + 0.4 * (n - 1), sub, picks)
        if plan is None:
            plan = (0, film, [rs[0][0]])
        _, sub, starts = plan
        for x in starts:
            used.setdefault(s["src"], []).append((x, x + sub * sp))
        for k, x in enumerate(starts):
            out.append(dict(s, t0=r3(s["t0"] + k * sub), ms=r3(x)))
    SEQ[:] = out


def snap_frames():
    for s in SEQ:
        s["t0"] = round(round(s["t0"] * FPS) / FPS, 4)
        if media(s["src"]).suffix == ".mp4":
            s["ms"] = s["ms"] * rate(s["src"]) / 30.0
        s["ms"] = round(round(s["ms"] * FPS) / FPS, 4)


def write_srt(caps):
    def ts(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"
    rows = [f"{i}\n{ts(a)} --> {ts(b)}\n{html.unescape(t)}\n" for i, (a, b, t) in enumerate(caps, 1)]
    (P / "youtube").mkdir(exist_ok=True)
    (P / "youtube/subtitles.en.srt").write_text("\n".join(rows), encoding="utf-8")


def make_plate():
    """the reading-room plate (assets/plates/plate.png): blue-black, faint grid, warm light from the left"""
    out = A / "plates" / "plate.png"
    if out.exists():
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.new("RGB", (1920, 1080), (10, 14, 21)); d = ImageDraw.Draw(im)
    for x in range(0, 1920, 64):
        d.line([(x, 0), (x, 1080)], fill=(18, 23, 31))
    for y in range(0, 1080, 64):
        d.line([(0, y), (1920, y)], fill=(18, 23, 31))
    glow = Image.new("RGB", (1920, 1080), (0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse((-500, -200, 900, 1300), fill=(70, 52, 26)); g.ellipse((1300, 400, 2400, 1500), fill=(26, 34, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(260))
    im = Image.blend(im, Image.eval(Image.merge("RGB", [a.point(lambda v: v) for a in glow.split()]), lambda v: v), 0.0)
    from PIL import ImageChops
    im = ImageChops.add(im, glow)
    im.save(out)


def emit():
    make_plate()
    SEQ.sort(key=lambda s: s["t0"])
    apply_ins()
    split_long()
    clean_assign()
    snap_frames()
    for s, nxt in zip(SEQ, SEQ[1:] + [dict(t0=END)]):
        s["t1"] = nxt["t0"]
        assert s["t1"] - s["t0"] > 0.4, (s["src"], s["t0"], s["t1"])
        m = media(s["src"])
        if m.suffix == ".mp4":
            need = s["ms"] + s["t1"] - s["t0"] + XF
            hv = probe(m)
            if need > hv - 0.05 and s["t1"] - s["t0"] + XF < hv - 0.1:   # a later piece of a split hold: start it earlier, never freeze
                s["ms"] = round(round(max(0.0, hv - (s["t1"] - s["t0"]) - XF - 0.1) * FPS) / FPS, 4)
                need = s["ms"] + s["t1"] - s["t0"] + XF
            if need > hv + 0.05:
                print(f"  ! {s['src']} needs {need:.1f}s, has {hv:.1f}s (t={s['t0']:.1f}): the last frame will hold")
    caps = captions(); PARTS = part_bounds()
    for k in range(len(PARTS) - 1):
        emit_part(f"p{k + 1}", PARTS[k], PARTS[k + 1], caps)
    (P / "build/parts.json").write_text(json.dumps(PARTS))
    (P / "build/timing.json").write_text(json.dumps({"BEATS": BEATS, "CUTS": CUTS, "END": END}))
    (P / "build/sound.json").write_text(json.dumps({"END": END, "SFX": SFX, "MUSIC": MUSIC, "SILENT": SILENT}, indent=1))
    write_srt(caps)
    film_vo()
    print(f"film {END:.1f}s ({int(END // 60)}:{END % 60:04.1f}); payoff (L68) at {L(68):.1f}s ({int(L(68) // 60)}:{L(68) % 60:04.1f}); "
          f"{len(SEQ)} shots, {len(OV)} overlays; YouTube clips present: {[k for k in YT if have(k)]}")


def seam_cut(h, a, b, t0, t1):
    if a < t0 - 1e-6:
        h = re.sub(r'data-fx="[^"]*"', 'data-fx="cut"', h, count=1)
    if b > t1 + 1e-6:
        h = h.replace("<div ", "<div data-cut ", 1)
    return h


def emit_part(pid, t0, t1, caps):
    D = FF.ft(round(t1 * FPS) - round(t0 * FPS)); d = OUTV / pid
    shutil.rmtree(d / "media", ignore_errors=True); (d / "media").mkdir(parents=True, exist_ok=True)
    shutil.copytree(OUTV / "_shared", d / "shared", dirs_exist_ok=True)
    shutil.copy(ROOT / "assets/brand/logo_square.png", d / "media/logo_square.png")
    loc = lambda x: r3(x - t0)
    H = []
    part = [x for x in SEQ if x["t0"] < t1 - 1e-6 and x["t1"] > t0 + 1e-6]
    for i, s in enumerate(part):
        fs, fe = round(s["t0"] * FPS) - round(t0 * FPS), round(s["t1"] * FPS) - round(t0 * FPS)
        ms = s["ms"]
        if fs < 0:
            ms = round(ms + (-fs) / FPS, 4) if media(s["src"]).suffix == ".mp4" else ms
            fs = 0
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
               else f'<div class="dim" style="background:rgba(6,9,13,{s["dim"]})"></div>')
        if src.suffix == ".mp4":
            H.append(f'      <div id="{pid}-s{i}" class="shot"{xf} data-vs="{st}" data-vd="{du}" style="visibility:hidden"><video id="{pid}-v{i}" class="m" src="{fn}" muted playsinline '
                     f'data-move="{s["move"]}"{org} data-start="{st}" data-duration="{du}" data-media-start="{ms}" data-track-index="2" data-volume="0"></video></div>')
            H.append(f'      <div class="vover"{xf} data-vs="{st}" data-vd="{du}" style="visibility:hidden">{dim}{tag}</div>')
        else:
            fit = ' style="object-fit:contain;background:#0a0e15"' if s["src"].startswith("D_") else ""
            H.append(f'      <div id="{pid}-s{i}" class="shot"{xf} data-start="{st}" data-duration="{du}" data-track-index="1">'
                     f'<img class="m a" src="{fn}" alt=""{fit} data-move="{s["move"]}"{org} />{dim}{tag}</div>')
    O = []
    for o in OV:
        a, b = o["at"], o["to"] if o["to"] is not None else END
        if b <= t0 or a >= t1:
            continue
        h = re.sub(r'(data-(?:at|to)=")([\d.]+)"', lambda mm: f'{mm.group(1)}{min(D, max(0.0, loc(float(mm.group(2)))))}"', o["h"])
        h = re.sub(r'(data-count="[\d.]+,[\d.]+,)([\d.]+)', lambda mm: f'{mm.group(1)}{max(0.0, loc(float(mm.group(2))))}', h)
        O.append("      " + seam_cut(h, a, b, t0, t1))
    cap = "\n".join(seam_cut(f'      <div class="cap" data-at="{max(0.0, loc(a))}" data-to="{min(D, loc(b))}" data-fx="fade" data-d="0.12">{cc}</div>', a, b, t0, t1)
                    for a, b, cc in caps if b > t0 and a < t1)
    endcard = ""
    if t1 >= END - 1e-6:   # the channel is named only here (CLAUDE.md): logo, name, the next film
        e0 = loc(VO_END - 1.5)
        endcard = (f'      <div class="endcard" data-at="{e0}" data-fx="fade"><img class="logo" src="media/logo_square.png" alt="" />'
                   f'<div class="ch">Be Practical<br/>with Kishore</div><div class="tile"><div class="nx">NEXT · INDIA\'S MISSING PIECES</div>'
                   f'<div class="tt">India built its own G.P.S. Why doesn\'t your phone use it?</div></div><div class="sub">SUBSCRIBE</div></div>')
    (d / "index.html").write_text(PAGE.format(pid=pid, D=D, shots="\n".join(H), ov="\n".join(O), cap=cap, endcard=endcard))
    print(f"{pid}: {t0:.1f}-{t1:.1f} ({D:.1f}s) {sum(1 for x in SEQ if t0 - 1e-6 <= x['t0'] < t1 - 1e-6)} shots, {len(O)} overlays")


PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>India own AI: {pid}</title>
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/aig.css" />
    <script src="shared/aig.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-ext-800-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2212, U+2013, U+2248, U+00D7, U+2192; }}
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-ext-600-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2212, U+2013, U+2248, U+00D7, U+2192; }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 700; src: url("vendor/fonts/jetbrains-mono-latin-700-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 800; src: url("vendor/fonts/jetbrains-mono-latin-800-normal.woff2") format("woff2"); }}
    </style>
  </head>
  <body>
    <!-- Generated by projects/india-own-ai/build/make_film.py. Edit that, not this file. -->
    <div id="root" data-composition-id="{pid}" data-start="0" data-width="1920" data-height="1080" data-duration="{D}">
{shots}
      <div class="grade" style="z-index:15"></div>
{ov}
{endcard}
{cap}
      <img class="bug" src="media/logo_square.png" alt="Be Practical with Kishore" />
      <canvas id="grain" width="500" height="290"></canvas>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      AIG_animate(tl, {D});
      window.__timelines["{pid}"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    emit()
