"""Generate edl.csv from the beat sheet below (v5: review fixes, HyperFrames inserts, 4K).

Each SHOT beat starts where the previous beat or break ended and runs to the next anchor. Its shots are listed
explicitly: (asset, seconds_or_None, src_in). Fixed-length shots keep their seconds; the rest share what is left.
Break rows: ("PAUSE", vo_at, dur, asset, sfx, note) and ("LIVE", vo_at, src_in, src_out, asset, lower_third, subtitle).
Run: python tools/gen_edl.py  (then build_srt.py --offset-map, edl_md.py, credits.py)
"""
import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
VO_END = 368.56
MOT = ["zoom_in", "pan_lr", "zoom_out", "pan_rl"]

# stock or stand-in footage that could be mistaken for the 2010 study: always labelled on screen
ILLUS = {"doctor_scrub.mp4", "drdo_lab.mp4", "iv_room.mp4", "hospital_corridor.mp4", "isolation_door.mp4", "blood_sample.mp4",
         "pulse_oximeter.mp4", "hospital_entrance.mp4", "lab_hood.mp4", "lab_tubes.mp4", "lab_scientist.mp4", "lab_microscope.mp4",
         "lab_cellplate.mp4", "lab_pipette.mp4", "icu_room.jpg"}
CREDIT = {"jani_portrait_red.jpg": "PHOTO: VIA RATIONALIST INTERNATIONAL", "headline_edamaruku.jpg": "SANALEDAMARUKU.COM · 2020",
          "headline_wikipedia.jpg": "WIKIPEDIA", "abstinence_1669.jpg": "LONDON 1669 · WELLCOME COLLECTION",
          "tanner_fast_end.jpg": "DR. HENRY TANNER'S 40-DAY FAST · 1880", "kidney_anatomy.jpg": "ENGRAVING · WELLCOME COLLECTION",
          "bladder_anatomy.jpg": "ENGRAVING · WELLCOME COLLECTION", "yogi_gouache.jpg": "GOUACHE · WELLCOME COLLECTION",
          "sonogram_scan.jpg": "ILLUSTRATIVE SCAN", "ultrasound_screen.jpg": "NASA", "ultrasound_scan2.jpg": "NASA",
          "astronaut_iss.mp4": "NASA", "earth_window.mp4": "NASA", "earth_sunrise.mp4": "NASA",
          "ambaji_gabbar.jpg": "GABBAR HILL, AMBAJI", "jani_ashram_ambaji.jpg": "AMBAJI, GUJARAT",
          **{f: "AL JAZEERA ENGLISH · 2010" for f in ("aj_room.mp4", "aj_press_wide.mp4", "aj_cctv.mp4", "aj_cctv2.mp4", "aj_room_wide.mp4",
                                                   "aj_jani_close.mp4", "aj_ilavazhagan.mp4", "aj_shah.mp4")},
          **{f: "ITN · 2010" for f in ("itn_devotees.mp4", "itn_jani_close.mp4", "itn_jani_close2.mp4", "itn_hospital_bed.mp4", "itn_cctv.mp4")}}
SUB = {("itn_full.mp4", 12.4): "ప్రహ్లాద్ జానీని కలవండి. ఆయన్ని మాతాజీ అని కూడా పిలుస్తారు, అంటే మాతృ దేవత. | ఆయన వయసు 82. | గత 70 ఏళ్లుగా తాను ఏమీ తినలేదు, తాగలేదు అని ఆయన చెప్తారు. | అది నిజమైతే, ఆయన జీవశాస్త్రాన్నే ధిక్కరిస్తున్నారు.",
       ("aj_full.mp4", 88.7): "మనుషులు ఆహారం, నీరు లేకుండా ఎలా బ్రతుకుతున్నారో అర్థం చేసుకుంటే, | ఎక్కువ కాలం ఆహారం, నీరు లేకుండా జీవించేలా వ్యూహాలు రూపొందించడానికి అది మాకు సహాయపడొచ్చు.",
       ("aj_full.mp4", 27.7): "మనమంతా సైన్స్‌లో, బయాలజీలో ఒక అద్భుతాన్ని చూస్తున్నాం. | మాతాజీ ఈ హాస్పిటల్‌లో చేరి ఇప్పటికే 108 గంటలైంది. | ఆయన ఏమీ తినలేదు, ఒక్క చుక్క ద్రవం కూడా తాగలేదు. | అంతకంటే ముఖ్యంగా, ఒక్క చుక్క మూత్రం గానీ, మలం గానీ విసర్జించలేదు.",
       ("skeptic_view.mp4", 7.0): "కొన్ని నిజాలు ఎలాంటి సందేహం లేకుండా నిరూపితమయ్యాయి. | మనతో సహా ప్రతి జీవికి బ్రతకడానికి క్రమం తప్పకుండా ఆహారం, నీరు అవసరం. | దీనికి మినహాయింపులు లేవు. ఒక్కటి కూడా లేదు."}
LIFT = {"doctor_scrub.mp4", "iv_room.mp4", "astronaut_iss.mp4"}  # under-exposed stock: lift shadows
CCTV = {"aj_cctv.mp4", "aj_cctv2.mp4", "itn_cctv.mp4"}  # authentic monitor footage: no extra look needed

# (block, listed_start, [(asset, secs|None, src_in)], [(rel_t, text, pos)], "sfx@rel;...", note)
B = [
    ("B1", 0.00, [("dried_leaf.mp4", None, 0), ("cracked_earth.jpg", None, 0)], [(0, "DAY 1 → 3 → 4", "timer")], "sfx_clock.wav@0", "Hook"),
    ("B1", 6.58, [("hf_kidney3d.mp4", None, 0)], [], "sfx_bass_hit.wav@8.2", "3D: kidneys fail without water"),
    ("B1", 14.99, [("iv_room.mp4", None, 0)], [], "sfx_flatline.wav@2.9", "Flatline lands on 'కానీ'"),
    ("B1", 17.99, [("itn_jani_close.mp4", None, 3.0), ("jani_portrait_red.jpg", None, 0)], [(0.3, "PRAHLAD JANI · 1929–2020", "lower")], "sfx_whoosh.wav@0", "Face + name by 0:18"),
    ("B1", 23.92, [("headline_wikipedia.jpg", None, 0), ("abstinence_1669.jpg", None, 0), ("headline_edamaruku.jpg", None, 0)], [(7.7, "IMPOSSIBLE CLAIM", "lower")], "sfx_whoosh.wav@0", ""),
    ("B1", 33.97, [("hf_logo_sting.mp4", None, 0.15)], [], "", "Channel logo sting"),
    ("B1", 37.91, [("india_drive.mp4", None, 2), ("aj_press_wide.mp4", None, 0), ("aj_ilavazhagan.mp4", None, 0), ("doctor_scrub.mp4", None, 4), ("lab_hood.mp4", None, 0)],
     [(8.6, "DRDO", "lower"), (14.7, "40 DOCTORS", "lower")], "sfx_bass_hit.wav@8.6", ""),
    ("B1", 55.08, [("sterling_hospital_ext.jpg", None, 0), ("aj_room.mp4", None, 0)], [(0.2, "AHMEDABAD · 2010", "lower")], "", ""),
    ("PAUSE", 61.45, 2.5, "aj_room_wide.mp4", "sfx_door_latch.wav@0.3;sfx_heartbeat_monitor.wav@0", "VO pause: door + monitor"),
    ("B1", 61.55, [("aj_cctv.mp4", None, 0), ("itn_cctv.mp4", None, 0), ("aj_cctv2.mp4", None, 0), ("aj_room_wide.mp4", None, 0)],
     [(0, "CCTV 24/7", "lower"), (8.1, "15 DAYS", "timer")], "", "Real 2010 CCTV only"),
    ("B1", 74.93, [("itn_hospital_bed.mp4", None, 0), ("aj_press_wide.mp4", None, 0), ("aj_jani_close.mp4", None, 0), ("aj_cctv2.mp4", None, 6), ("lab_cellplate.mp4", None, 10)], [], "sfx_bass_hit.wav@8.7", ""),
    ("B1", 91.30, [("itn_jani_close2.mp4", None, 1.0), ("aj_jani_close.mp4", None, 1)], [(3.9, "PRAHLAD JANI", "lower")], "sfx_bass_hit.wav@3.9", "Name said in VO"),
    ("B2", 97.21, [("itn_devotees.mp4", None, 0), ("ambaji_gabbar.jpg", None, 0), ("yogi_gouache.jpg", None, 0), ("jani_portrait_red.jpg", None, 0), ("jani_ashram_ambaji.jpg", None, 0)],
     [(0.3, "CHUNRIWALA MATAJI", "lower"), (9, "70+ YEARS", "lower")], "", ""),
    ("LIVE", 112.10, 12.4, 27.7, "itn_full.mp4", "NEWS REPORT · ITN · 2010", ""),
    ("B2", 112.28, [("aj_ilavazhagan.mp4", None, 3), ("lab_scientist.mp4", None, 0), ("sterling_hospital_ext.jpg", None, 0), ("aj_shah.mp4", None, 0)],
     [(0.5, "DIPAS · DRDO", "lower"), (11, "DR. SUDHIR SHAH", "lower")], "", ""),
    ("B2", 125.48, [("lab_pipette.mp4", None, 0), ("lab_tubes.mp4", None, 0)], [], "", ""),
    ("B2", 130.82, [("siachen_soldiers.jpg", None, 0), ("desert_soldiers.mp4", None, 0), ("indian_army.jpg", None, 0), ("astronaut_iss.mp4", None, 0)], [], "sfx_whoosh.wav@0", "Soldiers / extremes / space"),
    ("LIVE", 144.50, 88.7, 102.7, "aj_full.mp4", "G. ILAVAZHAGAN · DIPAS · 2010", ""),
    ("B2", 144.30, [("hf_timeline_a.mp4", None, 1.0)], [], "sfx_bass_hit.wav@0.2", "Study timeline"),
    ("B2", 148.42, [("water_tap_close.mp4", None, 14), ("water_drop_macro.mp4", None, 0)], [(3.4, "ZERO WATER", "lower")], "", "Rule 1"),
    ("B2", 155.42, [("aj_cctv.mp4", None, 1), ("itn_cctv.mp4", None, 3)], [(1.3, "2 CAMERAS · 24/7", "lower")], "", "Rule 2: real CCTV"),
    ("B2", 161.72, [("aj_room_wide.mp4", None, 0), ("doctor_scrub.mp4", None, 8)], [(1.2, "OBSERVER IN ROOM", "lower")], "", "Rule 3"),
    ("B2", 169.84, [("lab_tubes.mp4", None, 6), ("lab_pipette.mp4", None, 8), ("water_drop_macro.mp4", None, 4), ("water_tap_close.mp4", None, 18), ("lab_cellplate.mp4", None, 0)],
     [(8.2, "MEASURED TO THE ML", "lower")], "", "Rule 4"),
    ("B2", 185.41, [("hf_timeline_b.mp4", None, 0.0)], [], "", "Day tracker: days 1–5"),
    ("B2", 190.50, [("hf_dehydration_chart.mp4", None, 0.3)], [], "sfx_clock.wav@0", "Expected collapse vs reported flat line"),
    ("B2", 199.87, [("aj_jani_close.mp4", None, 4), ("hf_vitals.mp4", 9.5, 0)], [(0.5, "NO FATIGUE · NO WEAKNESS", "lower")], "", "Vitals: normal ranges, illustrative"),
    ("B2", 212.71, [("hf_timeline_b.mp4", 5.0, 6.0), ("itn_jani_close2.mp4", None, 2), ("aj_cctv2.mp4", None, 2)], [], "sfx_bass_hit.wav@7.9", ""),
    ("PAUSE", 223.70, 3.0, "ultrasound_screen.jpg", "sfx_heartbeat_monitor.wav@0", "VO pause after 'biggest shock'"),
    ("B3", 223.70, [("bladder_anatomy.jpg", None, 0)], [(0.1, "THE BLADDER MYSTERY", "lower")], "sfx_bass_hit.wav@0", ""),
    ("B3", 226.45, [("kidney_anatomy.jpg", None, 0), ("itn_hospital_bed.mp4", None, 3), ("aj_room.mp4", None, 4), ("ultrasound_screen.jpg", None, 0),
                    ("ultrasound_scan2.jpg", None, 0)], [(0.3, "15 DAYS · NO URINE", "lower")], "", ""),
    ("B3", 246.64, [("hf_bladder3d.mp4", 12.0, 0), ("sonogram_scan.jpg", None, 0), ("lab_microscope.mp4", None, 10), ("blood_sample.mp4", None, 0)], [], "sfx_bass_hit.wav@9.0", "3D: the bladder hypothesis"),
    ("B3", 268.20, [("headline_wikipedia.jpg", None, 0), ("aj_press_wide.mp4", None, 2)], [], "", ""),
    ("B3", 275.50, [("hf_timeline_b.mp4", 3.5, 12.5), ("scale_weight.jpg", None, 0), ("hf_vitals.mp4", 4.0, 3), ("itn_hospital_bed.mp4", None, 6)], [], "", "Day 15"),
    ("B4", 290.74, [("aj_press_wide.mp4", None, 0), ("aj_shah.mp4", None, 4)], [(0.3, "PRESS MEET · MAY 2010", "lower")], "", ""),
    ("LIVE", 298.05, 27.7, 54.7, "aj_full.mp4", "DR. SUDHIR SHAH · STERLING HOSPITAL · 2010", ""),
    ("B4", 298.20, [("hf_metabolism.mp4", 8.0, 0), ("incense.mp4", None, 0)], [], "sfx_bass_hit.wav@0", "Hypothesis: hypometabolism"),
    ("B4", 308.10, [("hf_autophagy3d.mp4", 12.0, 0), ("lab_microscope.mp4", None, 18)], [], "", "3D: autophagy"),
    ("B4", 322.89, [("yogi_gouache.jpg", None, 0), ("incense.mp4", None, 5), ("ambaji_gabbar.jpg", None, 0), ("himalaya_leh.jpg", None, 0)], [], "", ""),
    ("LIVE", 335.60, 7.0, 23.3, "skeptic_view.mp4", "JAMES RANDI · SKEPTIC · MAY 2010", ""),
    ("B4", 335.60, [("earth_window.mp4", None, 0), ("itn_jani_close2.mp4", None, 1), ("itn_jani_close.mp4", None, 5), ("himalaya_leh.jpg", None, 0)], [], "", ""),
    ("B5", 346.68, [("itn_devotees.mp4", None, 4), ("jani_ashram_ambaji.jpg", None, 0), ("aj_jani_close.mp4", None, 8), ("earth_sunrise.mp4", None, 0)], [], "", "Your opinion?"),
    ("B5", 358.97, [("hf_end_card.mp4", None, 0.2)], [], "", "End card: logo + subscribe; YouTube end screen sits here"),
]


def main():
    F = "id,block,type,vo_at,dur,vo_skip,vo_in,vo_out,src_in,src_out,asset,fallback,motion,overlay,text,text_pos,sfx,subtitle,optional,fx,note".split(",")
    rows, n, cursor, prev_block = [], 0, 0.0, None
    for idx, b in enumerate(B):
        kind = b[0]
        if kind == "PAUSE":
            _, at, dur, a, sfx, note = b
            n += 1
            rows.append(dict(id=f"S{n:03d}", block="PAUSE", type="VO_PAUSE", vo_at=at, dur=dur, vo_skip=0, asset=a, motion="zoom_in",
                             overlay="grain+vignette", text=CREDIT.get(a, ""), text_pos="tag" if a in CREDIT else "", sfx=sfx, note=note))
            cursor = at
            continue
        if kind == "LIVE":
            _, at, si, so, a, lt, _sub = b
            n += 1
            rows.append(dict(id=f"S{n:03d}", block="LIVE", type="LIVE", vo_at=at, dur=round(so - si, 2), vo_skip=0, src_in=si, src_out=so,
                             asset=a, motion="none", overlay="grain+vignette", text=lt, text_pos="lower", optional="no",
                             subtitle=SUB.get((a, si), ""), note="Original clip with its own audio"))
            cursor = at
            continue
        blk, listed, shots, texts, sfx, note = b
        a = cursor
        e = B[idx + 1][1] if idx + 1 < len(B) else VO_END
        d = e - a
        fixed = sum(s for _, s, _ in shots if s)
        free = [x for x in shots if not x[1]]
        each = (d - fixed) / len(free) if free else 0
        t = a
        for i, (asset, secs, src) in enumerate(shots):
            length = secs if secs else each
            if i == len(shots) - 1:
                length = e - t  # absorb rounding
            n += 1
            rel0, rel1 = t - listed, t + length - listed
            tx = [x for x in texts if rel0 <= x[0] + 1e-6 < rel1]
            fx = [f"{x.split('@')[0]}@{round(max(0.0, float(x.split('@')[1]) - rel0), 2)}" for x in sfx.split(";")
                  if x and (rel0 <= float(x.split("@")[1]) < rel1 or (i == 0 and float(x.split("@")[1]) < rel0))]
            hf = asset.startswith("hf_")
            overlay = "hf" if hf else "grain+vignette"
            if asset in ILLUS:
                overlay += "+illus"
            if asset in LIFT:
                overlay += "+lift"
            if hf and asset in ("hf_logo_sting.mp4", "hf_end_card.mp4"):
                overlay += "+nologo"
            txt, pos = (tx[0][1], tx[0][2]) if tx else ((CREDIT[asset], "tag") if asset in CREDIT and asset not in ILLUS else ("", ""))
            trans = []
            if i == 0 and blk != prev_block:
                trans.append("fin")
            if i == len(shots) - 1 and (idx + 1 >= len(B) or (B[idx + 1][0] not in ("PAUSE", "LIVE") and B[idx + 1][0] != blk)):
                trans.append("fout")
            rows.append(dict(id=f"S{n:03d}", block=blk, type="SHOT", dur=round(length, 2), vo_in=round(t, 2), vo_out=round(t + length, 2),
                             src_in=src or "", asset=asset, motion="none" if hf else MOT[n % 4], overlay=overlay,
                             text=txt, text_pos=pos, sfx=";".join(fx), fx="+".join(trans), note=note if i == 0 else ""))
            t += length
        cursor = e
        prev_block = blk
    with (HERE / "edl.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=F, restval="")
        w.writeheader()
        w.writerows(rows)
    sh = [r for r in rows if r["type"] == "SHOT"]
    gaps = [(x["id"], x["vo_out"], y["vo_in"]) for x, y in zip(sh, sh[1:]) if abs(x["vo_out"] - y["vo_in"]) > 0.02]
    long_ = [(r["id"], r["asset"], r["dur"]) for r in sh if r["dur"] > 4.2 and not r["asset"].startswith("hf_")]
    from collections import Counter
    reps = {k: v for k, v in Counter(r["asset"] for r in sh).items() if v > 2 and not k.startswith(("hf_", "aj_", "itn_"))}
    print(f"{len(rows)} rows, {len(sh)} shots; VO gaps: {gaps}; long stock shots: {long_}; stock repeats >2: {reps}")


if __name__ == "__main__":
    main()
