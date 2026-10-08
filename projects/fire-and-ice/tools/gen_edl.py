#!/usr/bin/env python3
"""Step 2: generate edl.csv from the shot list below + the VO line slots (align/p<N>/slots.csv) + vo_map.json.

Every shot belongs to a VO line (or a run of lines): the line's picture slot (cut in the pause before it) is split
between its shots by weight, so cuts land on the breath and the picture matches the words (semantic lock).
HyperFrames scenes ("hf/<scene>.mp4") are anchored to a line: the scene's t=0 is that line's slot start, so a
scene stays in sync with the VO even when other shots cut away in the middle of it.

  python3 tools/gen_edl.py && python3 tools/edl_md.py
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
VO = json.loads((HERE / "vo_map.json").read_text())
OFF = VO["offsets"]
SLOTS = {}
for p in (1, 2, 3):
    for r in csv.DictReader((HERE / f"align/p{p}/slots.csv").open()):
        SLOTS[(p, int(r["line"]))] = (OFF[p - 1] + float(r["picture_start"]), OFF[p - 1] + float(r["picture_end"]), r["en"])
PART_END = {1: OFF[1], 2: OFF[2]}   # part 1/2 slots run on through the section pause

VICE = "VICE · THE SUPERHUMAN WORLD OF THE ICEMAN (2016)"
DW = "DW EUROMAXX (2021) · FOOTAGE: WIM HOF METHOD"
PIX = ""  # Pixabay B-roll needs no on-screen credit (credited in the description)


def S(a, w=1.0, m="none", o="grain+vignette", tx="", tp="", cr="", si=0.0, sfx="", fx="", blk="", note="", anchor=None, fallback=""):
    return dict(a=a, w=w, m=m, o=o, tx=tx, tp=tp, cr=cr, si=si, sfx=sfx, fx=fx, blk=blk, note=note, anchor=anchor, fallback=fallback)


def HF(scene, anchor, w=1.0, tx="", sfx="", fx="", note=""):
    return S(f"hf/{scene}.mp4", w=w, o="hf", anchor=anchor, sfx=sfx, fx=fx, note=note, tx=tx)


B = "broll/pixabay_{}.mp4".format
V = "raw/dm_x4ly2a2.mp4"   # VICE, 288p
D = "raw/dm_x7zlb64.mp4"   # DW Euromaxx, 288p
PH = "photos/{}.jpg".format

# (part, first_line, last_line): shots.  Block: ICE (cold open), EMBER (Tummo), STEEL (Wim Hof + science)
SHOTS = [
    # ---------------- PART 1: hook ----------------
    ((1, 1, 1), "ICE", [S(B(345020), tx="−20 °C", tp="timer", sfx="audio/sfx_blizzard.mp3@0@-6", fx="fin")]),
    ((1, 2, 2), "ICE", [S(B(63281)), S(B(200327))]),
    ((1, 3, 3), "ICE", [S(V, si=147.0, cr=VICE, note="VICE host, untrained, shirtless in a snowy gorge"),
                         S(V, si=1880.0, cr=VICE, note="the same untrained host, shirtless, wet, in the snow")]),
    ((1, 4, 7), "ICE", [HF("hypothermia", (1, 4), w=3.0, sfx="audio/sfx_heartbeat.mp3@0@-10"),
                         S(B(7105), w=0.55, note="a soap bubble freezing: 'freezes like an ice doll'", sfx="audio/sfx_ice_crack2.mp3@0.3@-8"),
                         S(B(252819), w=0.7, sfx="audio/sfx_ice_crack.mp3@0@-10")]),
    ((1, 8, 8), "EMBER", [S(B(258658), sfx="audio/sfx_howl.mp3@0@-12"), S(B(199956))]),
    ((1, 9, 9), "EMBER", [S(PH("milarepa_kailash"), m="zoom_in", tx="MILAREPA, 'THE COTTON-CLAD' YOGI | TIBETAN PAINTING", cr="ART INSTITUTE OF CHICAGO · PUBLIC DOMAIN"),
                           S(PH("tummo_naropa"), m="pan_lr", cr="PHOTO: TANUMANASI · CC BY-SA 3.0", note="a modern Tummo practitioner meditating on snow")]),
    ((1, 10, 10), "EMBER", [HF("wet_sheet", (1, 10))]),
    ((1, 11, 11), "EMBER", [S(B(2344), m="push", sfx="audio/sfx_steam.mp3@0.2@-12", note="steam rising"),
                             S("hf/wet_sheet.mp4", o="hf", si=9.6)]),
    ((1, 12, 12), "STEEL", [S("hf/logo_sting.mp4", o="hf+nologo", sfx="audio/sfx_whoosh.mp3@0@-6", fx="fin")]),
    ((1, 13, 14), "STEEL", [S(PH("hms_gordon"), m="zoom_in", tx="HARVARD MEDICAL SCHOOL | BOSTON, USA", cr="PHOTO: CC BY-SA 4.0"),
                             S(B(186391), note="Ladakh valley"), S(B(175816), note="monastery in the Indian Himalaya")]),
    ((1, 15, 15), "STEEL", [S(D, si=3.2, tx="WIM HOF | 'THE ICEMAN' · NETHERLANDS", cr=DW)]),
    ((1, 16, 16), "STEEL", [S(D, si=12.0, cr=DW), S(V, si=2175.0, cr=VICE, note="archive: running barefoot in snow")]),
    ((1, 17, 17), "STEEL", [S(PH("wimhof_portrait"), m="zoom_in", cr="PHOTO: AAD VILLERIUS · CC BY-SA 2.0", note="Hof in an ice-cube box"),
                             S(D, si=8.0, cr=DW)]),
    ((1, 18, 18), "STEEL", [S(V, si=531.0, cr=VICE, note="2012 Radboud test: IV line"), S(V, si=557.0, cr=VICE), S(D, si=116.0, cr=DW)]),
    ((1, 19, 19), "STEEL", [S(B(8625), m="push", sfx="audio/sfx_fire.mp3@0@-12"), S(D, si=128.0, cr=DW, note="Hof meditating on an ice floe")]),
    ((1, 20, 20), "STEEL", [S(V, si=2181.0, cr=VICE, note="archive: Hof meditating in the snow"), S(V, si=1812.0, cr=VICE)]),
    ((1, 21, 21), "STEEL", [S(B(6310), m="push"), S(B(45595), m="push", tx="FIRE & ICE | THE SCIENCE OF TUMMO", fx="fout",
                                                     sfx="audio/sfx_bowl_strike.mp3@3.6@-4")]),
    # ---------------- PART 2: Tummo and the Harvard studies ----------------
    ((2, 1, 1), "EMBER", [S(PH("tummo_practice"), m="pan_rl", tx="TUMMO | 'INNER FIRE' MEDITATION", cr="TIBETAN MURAL · PUBLIC DOMAIN", fx="fin",
                             sfx="audio/sfx_bowl.mp3@0@-14;audio/amb_monks_cut.wav@0@-10"), S(B(1429), si=1.0)]),
    ((2, 2, 2), "EMBER", [S(B(58), si=4.0), S(B(1429), si=8.0, tx="ALSO CALLED CHANDALI YOGA")]),
    ((2, 3, 3), "EMBER", [S(B(443), si=9.0, note="monk in a cave shrine, India"), S(B(258657))]),
    ((2, 4, 4), "EMBER", [S(PH("hms_1900s"), m="zoom_in", cr="POSTCARD · PUBLIC DOMAIN"),
                           S(PH("hms_gordon"), m="pan_lr", tx="DR. HERBERT BENSON | HARVARD MEDICAL SCHOOL", cr="PHOTO: CC BY-SA 4.0")]),
    ((2, 5, 5), "EMBER", [HF("benson_map", (2, 5))]),
    ((2, 6, 6), "EMBER", [S(B(175815)), S(B(443), si=2.0)]),
    ((2, 7, 8), "EMBER", [HF("finger_temp", (2, 7))]),
    ((2, 9, 9), "EMBER", [S(PH("tummo_naropa"), m="zoom_in", cr="PHOTO: TANUMANASI · CC BY-SA 3.0"), S(B(290916), o="grain+vignette+illus")]),
    ((2, 10, 11), "EMBER", [HF("finger_temp", (2, 7))]),
    ((2, 12, 12), "EMBER", [S(B(252819), si=20.0, sfx="audio/sfx_ice_crack2.mp3@0@-10")]),
    ((2, 13, 13), "EMBER", [HF("wet_sheet", (2, 13))]),
    ((2, 14, 14), "EMBER", [S(V, si=432.5, cr=VICE, note="an untrained man gasping in an icy canal")]),
    ((2, 15, 15), "EMBER", [HF("wet_sheet", (2, 13), sfx="audio/sfx_steam.mp3@0.5@-14")]),
    ((2, 16, 16), "EMBER", [S(PH("hms_1900s"), m="zoom_in", tx="BENSON ET AL. | NATURE, 1982", cr="POSTCARD · PUBLIC DOMAIN")]),
    ((2, 17, 17), "EMBER", [S(B(85063), m="push"), S(B(260163), o="grain+vignette"), S(PH("tummo_practice"), m="zoom_out", fx="fout")]),
    # ---------------- PART 3: Wim Hof, brown fat ----------------
    ((3, 1, 1), "STEEL", [S(V, si=49.5, cr=VICE, fx="fin"), S(D, si=32.0, tx="WIM HOF | 'THE ICEMAN'", cr=DW)]),
    ((3, 2, 2), "STEEL", [S(PH("wimhof_2eight"), m="zoom_in", cr="PHOTO: STEFAN BRENDING · CC BY-SA 3.0 DE")]),
    ((3, 3, 3), "STEEL", [S(PH("wimhof_portrait"), m="pan_lr", cr="PHOTO: AAD VILLERIUS · CC BY-SA 2.0"), S(D, si=0.0, cr=DW, note="Hof lowers himself into an ice barrel")]),
    ((3, 4, 4), "STEEL", [S(V, si=615.5, tx="RADBOUD UNIVERSITY MEDICAL CENTRE | NIJMEGEN, NETHERLANDS", cr=VICE), S(V, si=610.5, cr=VICE)]),
    ((3, 5, 5), "STEEL", [S(V, si=543.0, cr=VICE), S(V, si=547.0, cr=VICE)]),
    ((3, 6, 8), "STEEL", [HF("lps_chart", (3, 6), w=1.6), S(D, si=66.0, cr=DW, note="Hof doing his breathing exercise"), HF("lps_chart", (3, 6), w=2.2),
                          S(V, si=577.0, cr=VICE, note="Prof. Peter Pickkers, Radboud")]),
    ((3, 9, 9), "STEEL", [S(B(45595), m="push", si=4.0)]),
    ((3, 10, 10), "STEEL", [S(V, si=371.7, cr=VICE, note="Hof steps into an icy Amsterdam canal"), S(V, si=375.0, cr=VICE)]),
    ((3, 11, 11), "STEEL", [S(PH("bat_petct"), m="zoom_in", fallback="hf/fat_cells.mp4", tx="BROWN FAT ON A PET-CT SCAN"), S(PH("bat_histo"), m="pan_lr", fallback="hf/mito.mp4")]),
    ((3, 12, 14), "STEEL", [HF("fat_cells", (3, 12))]),
    ((3, 15, 15), "STEEL", [HF("mito", (3, 15), w=1.2), S(B(6758), w=0.8, sfx="audio/sfx_fire.mp3@0@-12")]),
    ((3, 16, 17), "STEEL", [HF("brain_signal", (3, 16))]),
    ((3, 18, 18), "STEEL", [S("hf/mito.mp4", o="hf", si=5.6)]),
    ((3, 19, 20), "STEEL", [HF("nst", (3, 19))]),
    ((3, 21, 22), "EMBER", [HF("tummo_spine", (3, 21))]),
    ((3, 23, 23), "STEEL", [S(V, si=2223.0, cr=VICE), S(D, si=130.0, cr=DW), S(PH("tummo_practice"), m="zoom_in", cr="TIBETAN MURAL · PUBLIC DOMAIN"), S(V, si=2248.0, cr=VICE)]),
    ((3, 24, 24), "STEEL", [S(D, si=100.0, cr=DW)]),
    ((3, 25, 25), "STEEL", [S(B(258657), si=6.0)]),
    ((3, 26, 27), "STEEL", [S("hf/end_card.mp4", o="hf+nologo", fx="fin")]),
]
END_TAIL = 10.0   # the end card runs on after the last word (YouTube end screen)


def main():
    rows, n = [], 0
    for (p, a, b), blk, shots in SHOTS:
        t0, t1 = SLOTS[(p, a)][0], SLOTS[(p, b)][1]
        if p in PART_END and b == max(l for (pp, l) in SLOTS if pp == p):
            t1 = PART_END[p]
        if (p, b) == (3, 27):
            t1 += END_TAIL
        words = " ".join(SLOTS[(p, l)][2] for l in range(a, b + 1))
        W = sum(s["w"] for s in shots)
        t = t0
        for k, s in enumerate(shots):
            dur = (t1 - t0) * s["w"] / W
            n += 1
            si = s["si"]
            if s["anchor"]:
                si = round(t - SLOTS[s["anchor"]][0], 3)
            rows.append(dict(id=f"S{n:03d}", block=s["blk"] or blk, type="SHOT", vo_at="", dur=f"{dur:.3f}", vo_skip="", vo_in=f"{t:.3f}",
                             vo_out=f"{t + dur:.3f}", src_in=f"{si:.3f}" if si else "", src_out="", asset=s["a"], fallback=s.get("fallback", ""),
                             motion=s["m"], overlay=s["o"], text=s["tx"], text_pos=s["tp"], sfx=s["sfx"], subtitle="", optional="", fx=s["fx"],
                             credit=s["cr"], note=(s["note"] or (words[:90] if k == 0 else "")), line=f"P{p} L{a}" + (f"-{b}" if b != a else "")))
            t += dur
    cols = list(rows[0].keys())
    with (HERE / "edl.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} shots, {t:.1f} s programme")


if __name__ == "__main__":
    main()
