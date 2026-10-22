#!/usr/bin/env python3
"""Rare earth film assembly: the shot list, overlays, chain bar and captions -> HyperFrames parts in video/rem/p1..p5.

Times are seconds on the joined VO (assets/vo/vo_full.wav; sentence cues in align/sentences.json). Every shot shows
what the VO says at that second (screenplay.md). Base media: real footage the owner fetched (assets/yt, fetched.csv),
Pixabay B-roll (assets/broll), document plates (assets/plates), 3D/2D scene renders (assets/renders). Everything drawn
on top is HTML animated by video/rem/_shared/rem.js (engine copied from the UPI film). Numbers on screen come from
claims.csv; the exact labels follow fact-check.md §3.
Usage: python3 projects/rare-earth-magnets/build/make_film.py   (then npm run vendor; render each part)
"""
import html, json, re, shutil
from pathlib import Path

P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]; A = P / "assets"
OUTV = ROOT / "video/rem"
# ---------- v5 retime (owner's notes 2026-10-22: new opening, stairs, simpler lines) ----------
# Most shots below were cut on the v4 takes. R(t) maps a v4 film time onto the v5 voice track, sentence by sentence
# (align/sentences_v4.json -> align/sentences.json; unchanged sentences map exactly, changed ones linearly between
# their neighbours). Shots and overlays written inside `with v5():` are already in v5 time and are not mapped.
import difflib
OLD_S = json.loads((P / "align/sentences_v4.json").read_text())
NEW_S = json.loads((P / "align/sentences.json").read_text())
V4_VO_END, V4_END = 621.6, 636.0
VO_END = round(NEW_S[-1]["end"], 2)
END = round(VO_END + (V4_END - V4_VO_END), 2)   # VO + end screen (YouTube end-screen elements need 5-20 s)


def _anchors():
    a, b = [s["en"] for s in OLD_S], [s["en"] for s in NEW_S]
    pts = [(0.0, 0.0)]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                pts += [(OLD_S[i]["start"], NEW_S[j]["start"]), (OLD_S[i]["end"], NEW_S[j]["end"])]
    pts += [(V4_VO_END, VO_END), (V4_END, END)]
    return sorted(set(pts))


ANCH = _anchors()


def R(t):
    """v4 film time -> v5 film time (piecewise linear through the anchors)."""
    for (x0, y0), (x1, y1) in zip(ANCH, ANCH[1:]):
        if x0 <= t <= x1:
            return round(y0 + (t - x0) * (y1 - y0) / (x1 - x0), 3) if x1 > x0 else y0
    return round(t - ANCH[-1][0] + ANCH[-1][1], 3)


V5 = False


class v5:
    def __enter__(self):
        global V5
        V5 = True

    def __exit__(self, *a):
        global V5
        V5 = False
esc = html.escape

YT = {  # owner-fetched footage (assets/yt/fetched.csv): short, credited excerpts
    "Y01": ("01_xv0orNEbLG0.mp4", "FOOTAGE · CHETAK / BAJAJ AUTO"), "Y02": ("02_-E8U3-4liOI.mp4", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY"),
    "Y03": ("03_U8WZWhNwej8.mp4", "FOOTAGE · REUTERS"), "Y04": ("04_bLFYChw5c0Y.mp4", "FOOTAGE · SKY NEWS"),
    "Y05": ("05_2EiOSbusqLY.mp4", "FOOTAGE · MANORAMA NEWS"), "Y06": ("06_nXCKJFgsisQ.mp4", "FOOTAGE · THE NEWS MINUTE"),
    "Y07": ("07_7pcfpgTYsPM.mp4", "FOOTAGE · BMAG (NINGBO BESTWAY)"), "Y08": ("08_JNCKRKOmKXg.mp4", "FOOTAGE · JDA MAGNET"),
    "Y11": ("11_1oEOJO-xD_0.mp4", "FOOTAGE · IDAHO NATIONAL LABORATORY"),
}


def media(name):
    if name in YT:
        return A / "yt" / YT[name][0]
    if name.startswith("px_"):
        f = A / "broll" / f"pixabay_{name[3:]}.mp4"
        return f if f.exists() else A / "photos" / f"pixabay_{name[3:]}.jpg"
    if name.startswith("R_"):
        return A / "renders" / f"{name[2:]}.mp4"
    for d in ("plates", "photos"):
        for ext in (".png", ".jpg"):
            f = A / d / f"{name}{ext}"
            if f.exists():
                return f
    raise SystemExit(f"missing media {name}")


SHOTS, OV = [], []


def shot(t0, t1, src, move="push", tag=None, ms=0.0, origin=None, dim=False):
    if tag is None:
        tag = YT[src][1] if src in YT else ("PIXABAY" if src.startswith("px_") else "ILLUSTRATION" if src.startswith("R_") else "")
    if move == "crop" and origin is None:
        origin = "50% 6%"
    if not V5:
        t0, t1 = R(t0), R(t1)
    SHOTS.append(dict(t0=t0, t1=t1, src=src, move=move, tag=tag, ms=ms, origin=origin, dim=dim))


def el(h, at, to=None):
    if not V5:   # the html carries F-marked v4 times; emit() maps those through R
        at, to = R(at), (R(to) if to is not None else None)
    OV.append(dict(h=h, at=at, to=to))


def attrs(at, to, fx, d=None, extra=""):
    m = "N" if V5 else "F"   # N: already v5 time; F: v4 time, mapped in emit()
    s = f'data-at="{m}{at}" data-fx="{fx}"' + (f' data-to="{m}{to}"' if to is not None else "") + (f' data-d="{d}"' if d else "")
    return s + extra


def chip(text, at, to, x, y, col="amber", size="", fx="pop", icon=""):
    ic = f'<span class="ico">{icon}</span>' if icon else ""
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{ic}{esc(text)}</div>', at, to)


def lbl(text, at, to, x, y, col="ink", fx="left"):
    el(f'<div class="lbl c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{esc(text)}</div>', at, to)


def cite(text, at, to):
    el(f'<div class="cite" {attrs(at, to, "fade")}>{esc(text)}</div>', at, to)


def count(at, to, x, y, a, b, start, dur, pre="", suf="", col="ink", size="", fx="pop", dec=0):
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}><span data-count="{a},{b},{"N" if V5 else "F"}{start},{dur}" data-pre="{esc(pre)}" '
       f'data-suf="{esc(suf)}" data-dec="{dec}" data-ease="power2.out">{esc(pre)}{a}{esc(suf)}</span></div>', at, to)


def hl(at, to, x, y, w, h, d=0.6):
    el(f'<div class="hl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" {attrs(at, to, "grow", d)}></div>', at, to)


def big(text, at, to, x, y, col="ink", fx="pop"):
    el(f'<div class="big c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{esc(text)}</div>', at, to)


def quote(text, small, at, to, top=None):
    st = f' style="top:{top}px;bottom:auto"' if top is not None else ""
    el(f'<div class="quote"{st} {attrs(at, to, "up", 0.5)}>{esc(text)}<small>{esc(small)}</small></div>', at, to)


def namelt(name, role, at, to):
    el(f'<div class="namelt" {attrs(at, to, "left", 0.45)}><b>{esc(name)}</b><span>{esc(role)}</span></div>', at, to)


def rrr(head, text, col, at, to):
    el(f'<div class="rrr" {attrs(at, to, "up", 0.45)}><small class="c-{col}">{esc(head)}</small>{esc(text)}</div>', at, to)


def datebig(text, small, at, to):
    el(f'<div class="datebig" {attrs(at, to, "left", 0.4)}>{esc(text)}<small>{esc(small)}</small></div>', at, to)


def hbar(at, to, x, y, w, col, key, val_html, vx=None, d=0.9):
    el(f'<div class="hkey" style="left:{x}px;top:{y - 46}px" {attrs(at, to, "fade")}>{esc(key)}</div>', at, to)
    el(f'<div class="hbar c-{col}" style="left:{x}px;top:{y}px;width:{w}px" {attrs(at, to, "grow", d)}></div>', at, to)
    el(f'<div class="hval" style="left:{(vx or x + w + 30)}px;top:{y + 10}px" {attrs(at + d * 0.5, to, "fade")}>{val_html}</div>', at + d * 0.5, to)


LINKS = ["SAND", "MIXED", "CLEAN<br/>POWDER", "METAL", "ALLOY", "MAGNET"]


def chain(at, to, show=(), states=(), y=640):
    """The six-link chain. show: [(i, t)] when link i appears (default: all at `at`). states: [(i, t, colour)]."""
    show = dict(show) or {i: at for i in range(6)}
    parts = []
    for i, name in enumerate(LINKS):
        x = i * 292
        if i:
            parts.append(f'<div class="jn" style="left:{x - 44}px" {attrs(show.get(i, at), to, "fade")}></div>')
        parts.append(f'<div class="lk" style="left:{x}px" {attrs(show.get(i, at), to, "pop", 0.3)}>{name}</div>')
        for (j, t, col) in states:
            if j == i:
                parts.append(f'<div class="lk c-{col}" style="left:{x}px" {attrs(t, to, "fade", 0.35)}>{name}</div>')
    el(f'<div class="chain" style="top:{y}px">' + "".join(parts) + "</div>", at, to)


RE17 = ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Sc", "Y"]


def tiles(at, to, on=(), heavy=(), on_t=None, y=430, stagger=0.06):
    for i, s in enumerate(RE17):
        x = 130 + i * 98; t = at + i * stagger
        el(f'<div class="tile" style="left:{x}px;top:{y}px" {attrs(t, to, "pop", 0.25)}>{s}</div>', t, to)
        if s in on:
            el(f'<div class="tile on" style="left:{x}px;top:{y}px" {attrs(on_t, to, "fade")}>{s}</div>', on_t, to)
        if s in heavy:
            el(f'<div class="tile heavy" style="left:{x}px;top:{y}px" {attrs(on_t, to, "fade")}>{s}</div>', on_t, to)


def boxes(at, to, n_amber, half=False, x0=520, y0=380, t_amber=None):
    for i in range(10):
        x, y = x0 + (i % 5) * 150, y0 + (i // 5) * 120; t = at + i * 0.06
        el(f'<div class="box" style="left:{x}px;top:{y}px" {attrs(t, to, "pop", 0.25)}></div>', t, to)
        cls = "box c-amber" if i < n_amber else ("box half" if half and i == n_amber else "")
        if cls:
            ta = (t_amber or at + 0.8) + i * 0.08
            el(f'<div class="{cls}" style="left:{x}px;top:{y}px" {attrs(ta, to, "fade")}></div>', ta, to)


def tick(at, to, x, label, small, col="amber", y=560, ly=600):
    el(f'<div class="tick" style="left:{x}px;top:{y}px;background:var(--{col})" {attrs(at, to, "pop")}></div>', at, to)
    el(f'<div class="tlab" style="left:{x - 30}px;top:{ly}px" {attrs(at + 0.1, to, "up")}><small class="c-{col}">{esc(small)}</small>{esc(label)}</div>', at + 0.1, to)


def tline(at, to):
    el(f'<div class="tline" {attrs(at, to, "grow", 0.8)}></div>', at, to)


# =====================================================================================================
# THE CUT (film seconds = VO seconds). VO cue in each comment.
# =====================================================================================================
# ---- HOOK (0:00-0:53): Pune, half the scooters, one magnet, our sand
with v5():   # v5 opening (owner 2026-10-22): the magnet you already carry, the spec sheet, then Pune
    EA = R(22.65)
    shot(0.0, 2.44, "T_sandmagnet", "in", "")                                          # "There's a magnet in your pocket right now."
    chip("In your pocket", 0.4, 2.44, 120, 760, "cyan", "", "up")
    shot(2.44, 5.6, "commons_Nokia_motor", "in", "PHOTO · RAIMOND SPEKKING · CC BY-SA 4.0")  # "When your phone buzzes, that's a tiny motor spinning..."
    lbl("Phone vibration motor", 3.0, 5.6, 120, 160, "cyan")
    shot(5.6, 9.77, "R_buzz", "none", ms=3.0)                                          # "...and inside it sits a tiny, very strong magnet."
    chip("Tiny, very strong magnet", 7.4, 9.77, 120, 760, "cyan", "", "up")
    shot(9.77, 13.07, "P_ather", "in", "DOCUMENT · SHRIRAM FINANCE · ATHER 450X")       # "Now check the spec sheet of an electric scooter or car."
    chip("Scooter", 10.2, 13.07, 120, 160, "slate", "sm", "pop")
    shot(13.07, 15.3, "P_nexon", "in", "DOCUMENT · AUTOCAR INDIA · TATA NEXON EV")      # "Look at the motor line,"
    chip("Car", 13.3, 15.3, 120, 160, "slate", "sm", "pop")
    shot(15.3, 18.07, "P_nexon_row", "in", "DOCUMENT · AUTOCAR INDIA · TATA NEXON EV")  # "...and you'll often see two words... permanent magnet."
    chip("Permanent magnet", 15.6, 18.07, 1180, 760, "cyan", "", "pop")
    cite("[AUTOCAR INDIA | NEXON EV SPECS]", 13.3, 18.07)
    shot(18.07, 20.7, "R_motor", "none", ms=4.5)                                       # "Same family of magnet, just bigger."
    chip("Same magnet · bigger", 18.3, 20.7, 120, 760, "cyan", "", "up")
    shot(20.7, 22.7, "Y01", "in", ms=52.0)                                             # "No magnet, no motor."
    lbl("No magnet, no motor", 20.85, 22.7, 120, 160, "red")
    shot(22.7, 24.99, "Y01", "slow", ms=31.5)                                          # "No motor... no E.V."
    shot(24.99, 30.38, "Y01", "slow", ms=57.0)                                         # "And in 2025, that one magnet hit India's E.V. makers hard."
    shot(30.38, 37.77, "Y01", "slow", ms=37.0)                                         # "July, Pune. Bajaj's electric Chetak factory was making barely half..."
    datebig("JULY 2025", "PUNE · BAJAJ CHETAK PLANT", 30.45, 37.77)
    chip("Output ≈ half", 33.6, 37.77, 1260, 760, "red", "sm", "pop")
    shot(37.77, 40.84, "R_bp_bg", "slow", ms=0.0)                                      # "The reason? Not a strike. Not batteries."
    chip("Strike", 38.67, 40.84, 560, 420, "slate", "", "pop", "✕")
    chip("Batteries", 39.61, 40.84, 980, 420, "slate", "", "pop", "✕")
    shot(40.84, 44.76, "R_map_asia", "none", "MAP · LAND ONLY", ms=9.0)                 # "That small magnet... and most of them come from China."
    chip("Most from China", 42.3, 44.76, 120, 760, "amber", "", "up")
    shot(44.76, EA, "R_bp_bg", "push", ms=4.0)                                         # "In July 2024, about 20,000 Chetaks a month. In July 2025... less than 11,000."
    el(f'<div class="hkey" style="left:220px;top:300px" {attrs(44.85, EA, "fade")}>CHETAK OUTPUT · ONE MONTH</div>', 44.85, EA)
    hbar(44.9, EA, 220, 400, 1180, "slate", "JULY 2024", '<span data-count="0,20384,N45.0,1.6">0</span>')
    hbar(49.1, EA, 220, 620, 626, "red", "JULY 2025", '<span data-count="0,10824,N49.2,1.4">0</span>')
    chip("−47%", 50.6, EA, 1160, 610, "red", "", "pop")
    cite("[AUTOCAR INDIA | AUG 2025]", 44.9, EA)
shot(22.65, 26.3, "Y05", "crop", ms=63.5)                                              # "And the crazy part? The raw material ... in the sand on our own beaches"
chip("Our own sand", 23.9, 26.3, 120, 300, "amber", "", "pop")
shot(26.3, 32.2, "R_map_india", "none", "MAP · LAND ONLY", ms=0.2)                     # "— in Andhra Pradesh, Kerala, Tamil Nadu and Odisha."
shot(32.2, 37.85, "px_180875", "slow", ms=2.0)                                          # "By our own government's count... about seven million tonnes"
count(32.6, 37.85, 120, 300, 0, 7.23, 32.7, 1.6, "", "", "amber", "xl", dec=2)
el(f'<div class="hkey" style="left:130px;top:470px;color:var(--ink)" {attrs(33.2, 37.85, "fade")}>MILLION TONNES · RARE EARTH OXIDE · IN THE GROUND</div>', 33.2, 37.85)
cite("[DAE / AMD | RAJYA SABHA 2026]", 32.6, 37.85)
shot(37.85, 40.45, "T_sandmagnet", "in", "")                                           # "So why can't India make the magnet?"
big("OUR SAND.", 38.0, 40.45, 110, 200, "ink", "left")
big("THEIR MAGNET.", 38.5, 40.45, 110, 370, "amber", "left")
shot(40.45, 42.8, "px_180875", "slow", ms=9.0)                                            # "Stay with me, and you'll see three things."
big("3 THINGS", 40.6, 42.8, 620, 420, "cyan")
shot(42.8, 45.45, "Y11", "in", ms=36.0)                                                # "The hard step nobody else wanted to do."
lbl("1 · The hard step", 43.0, 45.45, 120, 760, "cyan")
shot(45.45, 50.6, "R_grain", "in", ms=4.5)                                              # "Then, about five minutes in, the secret inside our sand..."
lbl("2 · The secret in our sand", 45.6, 50.6, 120, 760, "amber")
chip("~5 min in", 46.5, 50.6, 1380, 160, "slate", "sm", "pop")
shot(50.6, 53.6, "R_bp_bg", "push", ms=10.0)                                            # "And at the end, the date you should watch."
lbl("3 · The date to watch", 50.75, 53.6, 120, 760, "red")
el(f'<div class="cal" style="left:820px;top:330px" {attrs(51.0, 53.6, "pop")}><div class="d"><div class="w">NOV</div><div class="n">10</div></div></div>', 51.0, 53.6)

# ---- THE MAGNET (0:53-1:53)
shot(53.6, 58.1, "Y07", "in", ms=103.5)                                                # "First, what is this magnet? It's called a rare earth magnet."
chip("Rare earth magnet", 56.1, 58.1, 120, 760, "cyan", "", "up")
shot(58.1, 62.7, "Y07", "crop", ms=87.5, origin="100% 0%")                                              # "Mostly iron, a pinch of boron, and a metal called neodymium."
with v5():   # "It's mostly iron. Add a little boron... and one special metal, called neodymium."
    chip("Iron", 88.0, R(62.7), 120, 560, "slate", "sm", "pop"); chip("Boron", 90.0, R(62.7), 120, 660, "slate", "sm", "pop")
    chip("Neodymium", 92.3, R(62.7), 120, 760, "cyan", "sm", "pop")
shot(62.7, 68.1, "Y02", "crop", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY", ms=66.0)        # "It's small, but it's very strong. And in a motor, strength is everything."
chip("Small · very strong", 63.0, 68.1, 120, 760, "cyan", "sm", "up")
shot(68.1, 78.6, "R_bp_bg", "slow", "ILLUSTRATIVE", ms=12.0)                            # "Here's why... same push from a smaller motor... lighter... more kilometres... Makes sense?"
el(f'<div class="ringm" style="left:300px;top:300px;width:460px;height:460px" {attrs(69.2, 78.6, "pop")}></div>', 69.2, 78.6)
el(f'<div class="ringm strong" style="left:1180px;top:390px;width:280px;height:280px" {attrs(70.0, 78.6, "pop")}></div>', 70.0, 78.6)
lbl("Weaker magnet", 69.3, 78.6, 300, 230, "slate", "fade"); lbl("Strong magnet", 70.1, 78.6, 1110, 230, "cyan", "fade")
chip("Same push", 71.0, 78.6, 760, 120, "ink", "sm", "pop")
chip("Lighter", 72.9, 78.6, 1560, 400, "green", "sm", "pop")
chip("More km per charge", 74.7, 78.6, 1100, 720, "green", "sm", "pop")
with v5():   # callbacks to the opening: the spec sheet, the phone's buzz
    shot(R(78.6), 113.1, "P_nexon_row", "slow", "DOCUMENT · AUTOCAR INDIA · TATA NEXON EV")  # "That's why the spec sheet says permanent magnet."
    chip("Permanent magnet", 110.4, 113.1, 1180, 760, "cyan", "", "pop")
    shot(113.1, 117.56, "Y01", "in", ms=77.0)                                          # "Most electric scooters and cars on the road use these magnets..."
    chip("Most EVs", 114.0, 117.56, 120, 760, "cyan", "", "up")
    shot(117.56, 120.94, "px_202987", "in", ms=2.0)                                     # "And it's not just vehicles. Remember the buzz in your phone?"
    lbl("Your phone's buzz", 119.3, 120.94, 120, 760, "cyan")
    shot(120.94, 123.2, "R_buzz", "none", ms=7.0)                                      # "Same kind of magnet."
    chip("Same kind of magnet", 121.0, 123.2, 120, 760, "cyan", "", "up")
    shot(123.2, 124.8, "px_209180", "slow", ms=3.0)                                    # "You'll also find it in many wind turbines,"
    lbl("Wind turbines", 123.3, 124.8, 120, 760, "cyan")
    shot(124.8, R(92.7), "pixabay_7278481", "in", "PHOTO · PIXABAY")                   # "and in defence systems."
    lbl("Defence", 125.0, R(92.7), 120, 760, "cyan")
shot(92.7, 100.85, "px_23215", "slow", ms=1.0)                                          # "India needs about four thousand tonnes... we buy almost all of them from abroad."
count(94.4, 100.85, 120, 300, 0, 4000, 94.5, 1.4, "~", " T / YEAR", "amber", "xl")
chip("Almost all imported", 98.0, 100.85, 120, 520, "ink", "sm", "up")
cite("[DAE | LOK SABHA 2026]", 94.4, 100.85)
shot(100.85, 105.7, "R_bp_bg", "slow", ms=14.0)                                         # "And more than eight out of every ten come from one country. China."
boxes(101.0, 105.7, 8, True, t_amber=102.0)
chip("85–90% from China", 104.3, 105.7, 620, 680, "amber", "", "pop")
cite("[GOVT OF INDIA | PIB 2026 · BY WEIGHT]", 101.0, 105.7)
shot(105.7, 112.7, "px_73847", "in", ms=3.0)                                            # "So you're probably thinking... dig it up and make them? Let's open that box."
chip("Dig it up?", 107.6, 112.7, 120, 300, "amber", "", "pop")

# ---- SEPARATION (1:53-3:23)
shot(112.7, 121.35, "Y03", "in", ms=22.0)                                              # "Here's the catch... Rare earths are not actually rare. The rare part is getting them out clean."
chip("Not actually rare", 115.8, 121.35, 120, 760, "green", "", "up")
chip("Getting them out clean", 118.7, 121.35, 120, 620, "amber", "sm", "up")
shot(121.35, 126.0, "R_bp_bg", "slow", ms=16.0)                                         # "There are seventeen of them... mixed together."
tiles(121.4, 126.0)
big("17", 121.5, 126.0, 860, 640, "cyan")
shot(126.0, 143.6, "R_siblings", "none", ms=0.0)                                        # "Think of them as seventeen brothers and sisters ... pull one of them out of the crowd? ...no single magic step."
lbl("Look alike", 130.9, 136.0, 120, 760, "slate")
chip("Pull one out?", 138.9, 143.6, 1200, 200, "cyan", "", "pop")
shot(143.6, 151.75, "Y11", "in", ms=73.5)                                              # "You dissolve the mix in acid, and the liquid flows through a long row of tanks..."
lbl("Acid + tanks", 144.6, 151.75, 120, 760, "cyan")
chip("A tiny bit each tank", 148.6, 151.75, 1080, 160, "amber", "sm", "pop")
with v5():
    shot(R(151.75), 194.9, "R_tanks", "none", ms=4.0)                                  # "So you repeat it. Again and again. A big plant can run hundreds of these tanks..."
count(154.6, 160.0, 120, 300, 1, 300, 154.7, 4.5, "TANK ", "", "cyan", "")
el(f'<div class="hkey" style="left:130px;top:410px" {attrs(155.0, 160.0, "fade")}>ILLUSTRATIVE COUNT · "HUNDREDS"</div>', 155.0, 160.0)
with v5():   # the staircase replaces "washing rice" (owner 2026-10-22: rice is washed once or twice, not hundreds of times)
    shot(194.9, R(168.0), "R_stairs", "none", ms=0.0)                                  # "Think of it like climbing stairs. Each tank is one step... You climb hundreds of steps."
    chip("Each tank = one step", 196.6, 202.3, 120, 160, "ink", "", "pop")
    chip("Hundreds of steps", 202.8, R(168.0), 120, 280, "cyan", "", "pop")
with v5():   # the second half, one real step per VO clause (v5 wording)
    EE = R(203.7)
    shot(R(168.0), 209.9, "Y08", "crop", ms=7.0)                                      # "And that's only the first half. The second half is faster. Let me run you through it."
    chip("Second half", 206.8, 209.9, 120, 300, "cyan", "", "pop")
    shot(209.9, 212.95, "Y08", "crop", ms=0.0)                                         # "Next, the clean rare earth becomes a metal."
    lbl("Metal", 210.2, 212.95, 120, 300, "cyan")
    shot(212.95, 217.69, "Y08", "crop", ms=11.0)                                       # "You melt it with iron and boron... and that mix is called an alloy."
    lbl("+ Iron + Boron", 213.4, 217.69, 120, 300, "amber")
    chip("Alloy", 215.6, 217.69, 120, 400, "cyan", "sm", "pop")
    shot(217.69, 220.29, "Y08", "crop", ms=28.5)                                       # "Then you cool it into thin pieces."
    lbl("Thin pieces", 217.85, 220.29, 120, 300, "cyan")
    shot(220.29, 222.4, "R_magline", "none", ms=10.8)                                  # "Hydrogen gas cracks those pieces,"
    shot(222.4, 225.72, "Y07", "crop", ms=13.0, origin="100% 0%")                      # "and you grind them into a powder finer than flour."
    lbl("Finer than flour", 222.6, 225.72, 120, 160, "cyan")
    shot(225.72, 229.2, "R_magline", "none", ms=16.5)                                  # "You line that powder up inside a strong magnetic field,"
    shot(229.2, 230.7, "Y07", "crop", ms=28.0, origin="100% 0%")                       # "press it into a block,"
    shot(230.7, 233.66, "Y07", "crop", ms=37.5, origin="100% 0%")                      # "and bake it at about a thousand degrees Celsius."
    lbl("~1,000–1,100 °C", 230.9, 233.66, 120, 160, "orange")
    shot(233.66, 237.22, "Y07", "crop", ms=70.0, origin="100% 0%")                     # "Only at the very end do you switch on its magnetism."
    shot(237.22, EE, "Y02", "crop", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY", ms=67.5)   # "That's when you finally have a magnet."
    chip("Magnet", 237.5, EE, 120, 760, "cyan", "", "up")
shot(203.7, 219.7, "R_bp_bg", "slow", ms=20.0)                                          # "So a magnet isn't one factory. It's a chain. Sand, to mixed ... to magnet. Miss one link... stuck."
big("A CHAIN", 206.3, 213.4, 700, 330, "ink")
with v5():
    chip("Not one factory", 240.5, R(206.3), 760, 420, "slate", "", "pop")   # "So a magnet isn't one factory."
chain(207.5, 219.7, show=[(0, 207.5), (1, 208.4), (2, 209.6), (3, 211.1), (4, 212.2), (5, 213.0)], states=[(3, 214.4, "red")])
chip("Stuck", 215.3, 219.7, 860, 420, "red", "", "pop")

# ---- HOW CHINA WON (3:40-4:43)
shot(219.7, 222.85, "R_map_asia", "none", "MAP · LAND ONLY", ms=8.0)                    # "So how did China end up leading every link?"
shot(222.85, 231.3, "R_map_asia", "none", "MAP · LAND ONLY", ms=10.5)                   # Deng Xiaoping is reported to have said ...
quote("The Middle East has oil. China has rare earths.", "DENG XIAOPING · AS REPORTED · 1992", 224.6, 231.3, top=110)
shot(231.3, 236.4, "Y03", "in", ms=64.5)                                                # "And China treated it like a national mission. Long-term, and patient."
chip("National mission", 231.6, 236.4, 120, 760, "amber", "", "up")
shot(236.4, 240.8, "R_bp_bg", "slow", ms=24.0)                                          # "Until about forty years ago, America made most of the world's rare earths."
tline(236.5, 240.8)
tick(236.8, 240.8, 300, "America leads", "UNTIL THE 1980s", "cyan")
shot(240.8, 245.95, "Y03", "in", ms=13.5)                                               # "Then the work moved to China, where labour was cheaper and pollution rules were weaker."
chip("Cheaper labour", 241.6, 245.95, 120, 300, "amber", "sm", "pop")
chip("Weaker pollution rules", 243.6, 245.95, 120, 420, "amber", "sm", "pop")
shot(245.95, 254.3, "Y04", "crop", ms=38.5)                                            # "Because separating rare earths is dirty work. Strong acids. Lots of waste..."
chip("Strong acids", 248.8, 254.3, 120, 160, "red", "sm", "pop")
chip("Lots of waste", 250.0, 254.3, 120, 280, "red", "sm", "pop")
shot(254.3, 259.2, "Y07", "crop", ms=10.0, origin="100% 0%")                                               # "So China did it for thirty years... and got very, very good at it."
chip("30 years", 254.5, 259.2, 120, 760, "amber", "", "up")
shot(259.2, 274.9, "R_bp_bg", "slow", ms=26.0)                                          # IEA: six of ten, eight and a half of ten, more than nine of ten
el(f'<div class="hkey" style="left:220px;top:250px;color:var(--ink)" {attrs(259.4, 274.9, "fade")}>CHINA\'S SHARE OF THE WORLD</div>', 259.4, 274.9)
hbar(261.8, 274.9, 220, 380, 720, "amber", "DIGGING · 2025", "~60%")
hbar(266.3, 274.9, 220, 560, 1020, "amber", "CLEANING / SEPARATING · 2025", "~85%")
hbar(269.3, 274.9, 220, 740, 1128, "amber", "MAKING THE MAGNETS · 2024", "94%")
cite("[IEA | 2026]", 272.3, 274.9)
shot(274.9, 283.8, "R_bp_bg", "slow", ms=30.0)                                          # "Digging is the easy part. The tanks and the furnaces are the hard part... China runs most of them."
chain(274.95, 283.8, states=[(0, 276.3, "green"), (1, 278.3, "amber"), (2, 278.3, "amber"), (3, 278.8, "amber"), (4, 278.8, "amber"), (5, 279.3, "amber")])
chip("Easy", 276.3, 283.8, 160, 480, "green", "sm", "pop")
chip("Hard", 278.3, 283.8, 1000, 480, "amber", "sm", "pop")

# ---- WHAT STOPPED INDIA (4:43-6:26)
shot(283.8, 294.0, "px_334883", "slow", ms=1.0)                                         # "So what about India? ... What stopped us? ... two things"
chip("What stopped us?", 287.6, 294.0, 120, 160, "ink", "", "pop")
lbl("1 · What's inside", 290.3, 294.0, 120, 660, "amber"); lbl("2 · What we did", 292.1, 294.0, 120, 750, "amber")
shot(294.0, 298.2, "Y05", "crop", ms=19.5)                                             # "In India, rare earths mostly come in a mineral called monazite."
chip("Monazite", 295.4, 298.2, 120, 160, "amber", "", "pop")
shot(298.2, 302.3, "Y05", "crop", ms=83.6)                                             # "You'll find it in the dark sand on some beaches in the south and east."
lbl("Dark mineral sand", 298.5, 302.3, 120, 760, "slate")
shot(302.3, 314.2, "R_grain", "none", ms=0.0)                                           # "And monazite has a surprise inside it. Thorium. It's radioactive..."
lbl("Thorium", 305.0, 314.2, 1180, 300, "orange", "fade")
chip("Radioactive", 306.1, 314.2, 1180, 380, "orange", "sm", "pop")
chip("Nuclear fuel", 307.7, 314.2, 1180, 480, "orange", "sm", "pop")
shot(314.2, 322.5, "P_ibm_act", "in", "DOCUMENT · INDIAN BUREAU OF MINES")             # "So by law, monazite is treated as an atomic material. Under the Atomic Energy Act..."
chip("Atomic Energy Act", 317.9, 322.5, 120, 160, "amber", "sm", "pop")
cite("[INDIAN BUREAU OF MINES | YEARBOOK 2022]", 314.4, 322.5)
shot(322.5, 326.9, "Y06", "crop", ms=105.5)                                            # "Indian Rare Earths Limited — today it's simply called I.R.E.L."
namelt("I.R.E.L.", "INDIAN RARE EARTHS LIMITED · GOVT OF INDIA", 322.7, 326.9)
shot(326.9, 337.8, "P_ibm_demand", "in", "DOCUMENT · INDIAN BUREAU OF MINES")          # "...kept things safe. But ... kept the business small. ... demand ... limited."
chip("Kept small", 329.7, 337.8, 120, 160, "slate", "sm", "pop")
cite("[INDIAN BUREAU OF MINES | 2022]", 332.8, 337.8)
shot(337.8, 344.9, "Y06", "crop", ms=203.0)                                            # "And here's the painful part. In 2024, I.R.E.L. produced about 2,900 tonnes."
count(339.6, 344.9, 120, 160, 0, 2900, 339.7, 1.4, "", " T · 2024", "amber", "")
cite("[REUTERS | JUN 2025]", 339.6, 344.9)
shot(344.9, 350.0, "R_map_asia", "none", "MAP · LAND ONLY", ms=0.6)                     # "And more than a thousand tonnes went to Japan, under a deal signed back in 2012."
chip("> 1,000 T to Japan", 346.3, 350.0, 1140, 550, "ink", "sm", "pop")
chip("Deal · 2012", 347.9, 350.0, 1140, 660, "slate", "sm", "pop")
shot(350.0, 358.8, "R_map_asia", "none", "MAP · LAND ONLY", ms=8.6)                     # "You send the raw material out... buy the finished magnets in..."
chip("Raw material out", 351.0, 358.8, 120, 650, "ink", "sm", "up")
chip("Magnets in", 352.6, 358.8, 120, 760, "amber", "sm", "up")
shot(358.8, 364.9, "R_bp_bg", "slow", ms=32.0)                                          # "Our sand is rich in the lighter rare earths, like neodymium."
tiles(358.9, 371.9, on=("La", "Ce", "Pr", "Nd", "Sm"), on_t=361.0, stagger=0.02)
chip("Rich in light ones", 361.2, 364.9, 620, 640, "cyan", "sm", "pop")
shot(364.9, 371.9, "R_bp_bg", "slow", ms=2.0)                                           # "But a magnet inside a hot motor also needs a little of two heavier ones..."
tiles(364.9, 371.9, heavy=("Tb", "Dy"), on_t=366.8, stagger=0.0)
chip("Keep strength in heat", 368.3, 371.9, 620, 640, "red", "sm", "pop")
shot(371.9, 379.2, "P_pib_reserves", "in", "DOCUMENT · PIB / DAE")                      # "Our own atomic energy department says India has very little of those..."
chip("Very little in India", 372.4, 379.2, 120, 160, "red", "sm", "pop")
cite("[DAE | RAJYA SABHA 2026]", 372.4, 379.2)
shot(379.2, 386.2, "R_bp_bg", "slow", ms=8.0)                                           # "So the sand alone was never going to be enough. You need the whole chain. ...wake-up call."
chain(379.3, 386.2, states=[(0, 379.6, "green")])
chip("Whole chain", 382.2, 386.2, 760, 420, "cyan", "sm", "pop")

# ---- THE SHOCK (6:26-7:30)
shot(386.2, 395.35, "R_bp_bg", "slow", ms=18.0)                                         # "April 2025. China said companies now need special permission..."
datebig("4 APRIL 2025", "CHINA · NEW EXPORT LICENCES", 386.3, 395.35)
tiles(388.4, 395.35, heavy=("Sm", "Gd", "Tb", "Dy", "Lu", "Sc", "Y"), on_t=390.0, stagger=0.02)
chip("+ magnets with them", 392.6, 395.35, 620, 640, "red", "sm", "pop")
cite("[MOFCOM ANNOUNCEMENT No. 18 | 2025]", 388.4, 395.35)
shot(395.35, 399.8, "px_24255", "slow", ms=2.0)                                          # "Permission takes time. And while you wait, your supply dries up."
chip("Waiting", 395.6, 399.8, 120, 760, "amber", "", "up")
shot(399.8, 407.2, "P_autocar", "in", "DOCUMENT · AUTOCAR INDIA")                       # "By July, Bajaj was making about half the Chetaks... Ather and T.V.S. felt the pressure too."
lbl("Ather · T.V.S.", 404.7, 407.2, 120, 760, "amber")
cite("[AUTOCAR INDIA | AUG 2025]", 400.0, 407.2)
shot(407.2, 416.1, "P_cnbc", "in", "DOCUMENT · CNBC-TV18")                              # "Back in April, Rajiv Bajaj had warned — ... could halt within weeks."
namelt("Rajiv Bajaj", "MANAGING DIRECTOR · BAJAJ AUTO · APRIL 2025", 407.4, 416.1)
cite("[MONEYCONTROL / CNBC-TV18 | APR 2025]", 407.4, 416.1)
shot(416.1, 424.7, "P_ians", "in", "DOCUMENT · IANS")                                   # "Later, China started giving permission ... But there was a condition. ... not for defence."
chip("Some licences", 416.4, 424.7, 120, 760, "green", "sm", "up")
chip("Not for defence", 422.0, 424.7, 1180, 160, "red", "", "pop")
cite("[IANS | OCT 2025]", 416.4, 424.7)
shot(424.7, 433.7, "R_bp_bg", "slow", ms=22.0)                                          # "Then in October 2025, China announced even wider rules... on hold for one year."
tline(424.8, 433.7)
tick(424.9, 433.7, 300, "Licence rule", "APR 2025", "red")
tick(425.4, 433.7, 760, "Wider rules", "OCT 2025", "red")
tick(430.4, 433.7, 1220, "Paused · 1 year", "NOV 2025", "amber")
shot(433.7, 446.3, "P_technology", "in", "DOCUMENT · TECHNOLOGY.ORG")                   # "...set to end on November tenth. ... trade deal till January. ... Will China stretch this hold too...?"
chip("On paper: 10 Nov 2026", 433.9, 446.3, 120, 560, "amber", "sm", "pop")
chip("US–China truce: 10 Jan 2027", 437.3, 446.3, 120, 660, "cyan", "sm", "pop")
chip("Stretch?", 443.1, 446.3, 1300, 760, "ink", "", "pop")
cite("[MOFCOM | 2025–26 · AS OF 21 OCT 2026]", 434.0, 446.3)
shot(446.3, 449.9, "R_bp_bg", "slow", ms=34.0)                                          # "And the April permission rule? It never went away."
tline(446.3, 449.9)
tick(446.4, 449.9, 300, "Licence rule", "APR 2025", "red")
chip("Still on", 448.2, 449.9, 300, 760, "red", "", "pop")

# ---- INDIA'S ANSWER (7:30-8:51)
shot(449.9, 455.65, "px_334883", "slow", ms=6.0)                                        # "So is India just waiting? Not at all — and this part might surprise you."
chip("Not at all", 452.4, 455.65, 120, 760, "green", "", "up")
shot(455.65, 463.1, "Y02", "slow", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY", ms=147.5)  # "In Visakhapatnam, on a campus of the Bhabha Atomic Research Centre, India already runs a rare earth magnet plant."
lbl("Visakhapatnam", 455.9, 463.1, 120, 160, "cyan")
cite("[DAE | PIB 2026]", 456.0, 463.1)
shot(463.1, 467.55, "Y02", "crop", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY", ms=12.0)     # "It's built with our own technology, from Bhabha and a D.R.D.O. lab."
chip("BARC + DRDO tech", 463.4, 467.55, 120, 760, "cyan", "sm", "up")
shot(467.55, 473.5, "Y02", "crop", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY", ms=56.0)     # "And it makes a special magnet that can take high heat..."
chip("Samarium-cobalt", 467.8, 473.5, 120, 160, "cyan", "sm", "pop")
chip("Defence · space", 469.6, 473.5, 120, 270, "slate", "sm", "pop")
shot(473.5, 480.2, "P_pmindia", "in", "DOCUMENT · PMINDIA")                             # "In November 2025, the government approved a scheme worth about 7,300 crore rupees."
count(475.2, 480.2, 120, 760, 0, 7280, 475.3, 1.4, "₹", " CRORE", "green", "")
cite("[UNION CABINET | 26 NOV 2025]", 473.7, 480.2)
shot(480.2, 490.2, "R_bp_bg", "slow", ms=4.0)                                           # "The goal? Six thousand tonnes ... And the full chain — from rare earth powder, to metal, to alloy, to finished magnet."
count(480.9, 490.2, 600, 230, 0, 6000, 481.0, 1.4, "", " T / YEAR", "green", "xl")
chain(484.9, 490.2, states=[(2, 486.0, "cyan"), (3, 487.4, "cyan"), (4, 488.2, "cyan"), (5, 488.9, "cyan")])
shot(490.2, 499.45, "P_ddindia", "in", "DOCUMENT · DD INDIA")                          # "Five companies can win up to 1,200 tonnes each. This August, twenty bids came in. ... L and T, Coal India and ReNew."
chip("5 × 1,200 T", 490.5, 499.45, 120, 560, "green", "sm", "pop")
chip("20 bids · Aug 2026", 493.9, 499.45, 120, 660, "cyan", "sm", "pop")
chip("L&T · Coal India · ReNew", 496.2, 499.45, 120, 760, "ink", "sm", "up")
cite("[MHI / DD INDIA | AUG 2026]", 490.5, 499.45)
shot(499.45, 503.0, "px_40054", "slow", ms=4.0, dim=True)                                         # "The winners are still to be announced, so keep your eyes on this."
chip("Winners: not yet", 499.7, 503.0, 120, 160, "amber", "", "pop")
el(f'<div class="hkey" style="left:140px;top:290px" {attrs(500.0, 503.0, "fade")}>AS OF 21 OCT 2026</div>', 500.0, 503.0)
shot(503.0, 510.3, "R_map_india", "none", "MAP · LAND ONLY · ILLUSTRATIVE ZONES", ms=15.6)  # "The 2026 budget also announced special rare earth zones in Odisha, Kerala, Andhra Pradesh and Tamil Nadu."
cite("[UNION BUDGET 2026–27]", 503.2, 510.3)
shot(510.3, 514.75, "P_budget", "in", "DOCUMENT · PIB")                                 # "Mining, processing, research and factories, all linked up."
shot(514.75, 524.2, "R_map_asia", "none", "MAP · LAND ONLY", ms=1.0)                    # "And remember the Japan deal? In June 2025, Reuters reported that India asked I.R.E.L. to stop those exports..."
chip("Reported · Reuters · Jun 2025", 516.5, 524.2, 1040, 650, "ink", "sm", "pop")
chip("Keep it home", 521.3, 524.2, 1040, 760, "green", "sm", "pop")
shot(524.2, 531.65, "R_bp_bg", "slow", ms=16.0)                                         # "So the plan is to keep the sand here. The money is here. Now comes the hard middle..."
chain(524.3, 531.65, states=[(0, 524.5, "green"), (1, 528.4, "amber"), (2, 528.4, "amber"), (3, 528.4, "amber"), (4, 528.4, "amber")])
chip("Sand: here", 524.6, 531.65, 120, 420, "green", "sm", "pop")
chip("Money: here", 526.8, 531.65, 560, 420, "green", "sm", "pop")
chip("The hard middle", 528.4, 531.65, 1080, 420, "amber", "sm", "pop")

# ---- HONEST TIMELINE + RULE / RUIN / REALITY (8:51-9:34)
shot(531.65, 539.65, "R_bp_bg", "slow", ms=24.0)                                        # "Let me be honest... two years to be built. Then five years of support."
lbl("The honest timeline", 531.8, 539.65, 220, 220, "cyan")
hbar(533.4, 539.65, 220, 400, 300, "cyan", "BUILD", "2 YEARS", vx=560)
hbar(537.4, 539.65, 540, 600, 750, "green", "SUPPORT", "5 YEARS", vx=1320)
cite("[SCHEME GUIDELINES | MHI 2025]", 534.3, 539.65)
shot(539.65, 549.6, "Y07", "slow", ms=0.0)                                           # "And China has a head start of more than thirty years. Running hundreds of tanks well... practice."
chip("30+ years ahead", 539.9, 549.6, 120, 160, "amber", "", "pop")
chip("Practice", 543.6, 549.6, 120, 760, "cyan", "sm", "up")
shot(549.6, 556.4, "Y05", "crop", ms=21.0)                                             # RULE: "If you only sell the sand, you sell cheap and you buy expensive."
rrr("RULE", "Sell sand cheap. Buy magnets costly.", "amber", 551.9, 556.4)
shot(556.4, 562.55, "Y01", "slow", ms=41.0)                                            # RUIN: "When the one seller says stop, your factories stop. You saw it in Pune."
rrr("RUIN", "One seller says stop. Factories stop.", "red", 557.7, 562.55)
shot(562.55, 569.65, "Y02", "crop", "FOOTAGE · PMO · DEPT OF ATOMIC ENERGY", ms=42.0)  # REALITY: "India has the sand. It has the scientists. And now it has the money."
rrr("REALITY", "The sand. The scientists. The money.", "green", 564.8, 569.65)
shot(569.65, 574.05, "R_bp_bg", "slow", ms=28.0)                                        # "What's left is the hard middle — more tanks, and the furnaces."
chain(569.7, 574.05, states=[(0, 569.9, "green"), (1, 571.4, "amber"), (2, 571.4, "amber"), (3, 572.6, "amber"), (4, 572.6, "amber"), (5, 569.9, "green")])

# ---- WHAT IT MEANS FOR YOU + BRIDGE (9:34-10:21)
with v5():
    shot(R(574.05), 611.07, "px_202987", "slow", ms=7.0)                               # "So what does this mean for you? If you're planning to buy an electric scooter or a new phone, remember this."
    shot(611.07, R(585.6), "Y01", "in", ms=142.0)                                      # "A small magnet inside it depends on this chain — and that can change its price, and even when it reaches your showroom."
    chip("Price", 615.0, R(585.6), 120, 160, "amber", "sm", "pop")
    chip("Delivery date", 617.0, R(585.6), 120, 270, "amber", "sm", "pop")
shot(585.6, 595.95, "R_bp_bg", "slow", ms=10.0)                                          # "Watch two things. November tenth ... And the scheme winners..."
el(f'<div class="cal" style="left:300px;top:330px" {attrs(586.9, 595.95, "pop")}><div class="d"><div class="w">NOV</div><div class="n">10</div></div></div>', 586.9, 595.95)
lbl("Pause ends, or stretched?", 586.9, 595.95, 300, 600, "amber", "fade")
el(f'<div class="cal" style="left:1150px;top:330px" {attrs(590.8, 595.95, "pop")}><div class="d"><div class="w">MHI</div><div class="n">5</div></div></div>', 590.8, 595.95)
lbl("Scheme winners", 590.8, 595.95, 1150, 600, "green", "fade")
shot(595.95, 601.55, "R_tanks", "none", ms=9.5)                                         # "India won't fix this in one jump. It'll be tank by tank... furnace by furnace."
chip("Tank by tank", 598.4, 601.55, 120, 760, "cyan", "", "up")
shot(601.55, 610.6, "px_40948", "slow", ms=0.0)                                         # "And magnets aren't the only missing piece. India is called the pharmacy of the world..."
chip("Pharmacy of the world", 604.2, 610.6, 120, 160, "green", "sm", "pop")
chip("Ingredients from China?", 607.0, 610.6, 120, 270, "amber", "sm", "pop")
shot(610.6, 618.0, "endtile", "in", "PIXABAY", dim=True)                                          # "Why? That's our next story. Which missing piece should we open after that? Tell me in the comments."
big("NEXT: MEDICINES", 610.8, 613.0, 380, 420, "green")
chip("Which piece next?", 613.2, 618.0, 620, 420, "cyan", "", "pop", "💬")
shot(618.0, V4_END, "R_bp_bg", "slow", "", ms=14.0)                                         # "This is Be Practical with Kishore. Stay practical. Jai Hind." + end screen
el('<div class="endcard" ' + attrs(618.1, None, "fade", 0.8) + '><img class="logo" src="media/logo_square.png" alt=""/><div class="ch">Be Practical<br/>with Kishore</div>'
   '<div class="sub">SUBSCRIBE</div><div class="tile"><img src="media/endtile.jpg" alt=""/><div class="nx">INDIA\'S MISSING PIECES · NEXT</div>'
   '<div class="tt">The pharmacy of the world\'s missing ingredient</div></div></div>', 618.1)

# ---------- captions from the sentence cues ----------
NUMS = [("twenty twenty-five", "2025"), ("twenty twenty-six", "2026"), ("twenty twenty-four", "2024"), ("twenty twelve", "2012"),
        ("nineteen ninety-two", "1992"), ("about twenty thousand", "about 20,000"), ("less than eleven thousand", "less than 11,000"),
        ("about seven million tonnes", "about 7 million tonnes"), ("about four thousand tonnes", "about 4,000 tonnes"),
        ("about two thousand nine hundred tonnes", "about 2,900 tonnes"), ("more than a thousand tonnes", "more than 1,000 tonnes"),
        ("about seven thousand three hundred crore rupees", "about ₹7,300 crore"), ("Six thousand tonnes", "6,000 tonnes"),
        ("twelve hundred tonnes", "1,200 tonnes"), ("twenty bids", "20 bids"), ("November tenth", "November 10"),
        ("about forty years ago", "about 40 years ago"), ("thirty years", "30 years"), ("about a thousand degrees", "about 1,000 degrees"),
        ("seventeen", "17"), ("I.R.E.L.", "IREL"), ("D.R.D.O.", "DRDO"), ("T.V.S.", "TVS"), ("L and T", "L&T")]


def capify(s):
    for a, b in NUMS:
        s = s.replace(a, b)
    s = esc(s)
    return re.sub(r"(₹[\d,]+(?: crore)?|\b\d[\d,.]*\b(?: (?:million )?tonnes| years| degrees)?)", r"<b>\1</b>", s)


def captions():
    out = []
    for r in json.loads((P / "align/sentences.json").read_text()):
        a, b, text = r["start"], r["end"], r["en"]
        parts, cur = [], ""
        for w in re.split(r"(?<=[,—?])\s+|\s+(?=—)", text):
            if cur and len(cur) + len(w) > 46:
                parts.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        parts.append(cur)
        tot = sum(len(p) for p in parts); t = a
        for n, p in enumerate(parts):
            d = (b - a) * len(p) / tot
            out.append((round(t, 2), round(t + d + (0.12 if n == len(parts) - 1 else 0.0), 2), capify(p))); t += d
    return out


# ---------- emit parts (cut at shot boundaries nearest to equal splits) ----------
def r3(x):
    return round(x, 3)


def part_bounds(n=5):
    starts = sorted({s["t0"] for s in SHOTS})
    b = [0.0]
    for k in range(1, n):
        b.append(min(starts, key=lambda x: abs(x - END * k / n)))
    return b + [END]


def emit():
    SHOTS.sort(key=lambda s: s["t0"])
    for a, b2 in zip(SHOTS, SHOTS[1:]):   # the cut must be gapless and non-overlapping
        assert abs(a["t1"] - b2["t0"]) < 1e-6, (a["src"], a["t1"], b2["t0"])
    caps = captions(); PARTS = part_bounds()
    for k in range(len(PARTS) - 1):
        t0, t1 = PARTS[k], PARTS[k + 1]; D = r3(t1 - t0); pid = f"p{k + 1}"; d = OUTV / pid
        shutil.rmtree(d / "media", ignore_errors=True); (d / "media").mkdir(parents=True, exist_ok=True)
        shutil.copytree(OUTV / "_shared", d / "shared", dirs_exist_ok=True)
        shutil.copy(ROOT / "assets/brand/logo_square.png", d / "media/logo_square.png")
        if (A / "plates/endtile.jpg").exists():
            shutil.copy(A / "plates/endtile.jpg", d / "media/endtile.jpg")
        (d / "vendor/fonts").mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "node_modules/gsap/dist/gsap.min.js", d / "vendor/gsap.min.js")
        for f in ["inter/files/inter-latin-600-normal.woff2", "inter/files/inter-latin-800-normal.woff2", "inter/files/inter-latin-ext-600-normal.woff2",
                  "inter/files/inter-latin-ext-800-normal.woff2", "jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2",
                  "jetbrains-mono/files/jetbrains-mono-latin-800-normal.woff2"]:
            shutil.copy(ROOT / "node_modules/@fontsource" / f, d / "vendor/fonts" / Path(f).name)
        loc = lambda x: r3(x - t0)
        H = []
        for i, s in enumerate(x for x in SHOTS if t0 - 1e-6 <= x["t0"] < t1 - 1e-6):
            st, du = loc(s["t0"]), r3(s["t1"] - s["t0"]); src = media(s["src"])
            fn = f"media/{src.name}"
            if not (d / fn).exists():
                shutil.copy(src, d / fn)
            tag = f'<div class="tag">{esc(s["tag"])}</div>' if s["tag"] else ""
            org = f' data-origin="{s["origin"]}"' if s["origin"] else ""
            if src.suffix == ".mp4":
                H.append(f'      <div id="{pid}-s{i}" class="shot" data-vs="{st}" data-vd="{du}" style="visibility:hidden"><video id="{pid}-v{i}" class="m" src="{fn}" muted playsinline '
                         f'data-move="{s["move"]}"{org} data-start="{st}" data-duration="{du}" data-media-start="{s["ms"]}" data-track-index="2" data-volume="0"></video></div>')
                H.append(f'      <div class="vover" data-vs="{st}" data-vd="{du}" style="visibility:hidden">{tag}</div>')
            else:
                H.append(f'      <div id="{pid}-s{i}" class="shot" data-start="{st}" data-duration="{du}" data-track-index="1">'
                         f'<img class="m a" src="{fn}" alt="" data-move="{s["move"]}"{org} />{"<div class=dim></div>" if s["dim"] else ""}{tag}</div>')
        O = []
        for o in OV:
            a, b = o["at"], o["to"] if o["to"] is not None else END
            if b <= t0 or a >= t1:
                continue
            ft = lambda mk, x: float(x) if mk == "N" else R(float(x))
            h = re.sub(r'(data-(?:at|to)=")([FN])([\d.]+)"', lambda mm: f'{mm.group(1)}{min(D, max(0.0, loc(ft(mm.group(2), mm.group(3)))))}"', o["h"])
            h = re.sub(r'(data-count="[\d.]+,[\d.]+,)([FN])([\d.]+)', lambda mm: f'{mm.group(1)}{max(0.0, loc(ft(mm.group(2), mm.group(3))))}', h)
            O.append("      " + h)
        cap = "\n".join(f'      <div class="cap" data-at="{max(0.0, loc(a))}" data-to="{min(D, loc(b))}" data-fx="fade" data-d="0.12">{c}</div>'
                        for a, b, c in caps if b > t0 and a < t1)
        (d / "index.html").write_text(PAGE.format(pid=pid, D=D, shots="\n".join(H), ov="\n".join(O), cap=cap))
        print(f"{pid}: {t0:.1f}-{t1:.1f} ({D:.1f}s) {sum(1 for x in SHOTS if t0 - 1e-6 <= x['t0'] < t1 - 1e-6)} shots, {len(O)} overlays")
    (P / "build/parts.json").write_text(json.dumps(PARTS))


PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Rare earth magnets: {pid}</title>
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/rem.css" />
    <script src="shared/rem.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-ext-800-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2212; }}
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-ext-600-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2212; }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 700; src: url("vendor/fonts/jetbrains-mono-latin-700-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 800; src: url("vendor/fonts/jetbrains-mono-latin-800-normal.woff2") format("woff2"); }}
    </style>
  </head>
  <body>
    <!-- Generated by projects/rare-earth-magnets/build/make_film.py. Edit that, not this file. -->
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
      REM_animate(tl, {D});
      window.__timelines["{pid}"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    emit()
