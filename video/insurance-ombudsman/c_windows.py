"""Session C windows: film-time VO windows (scenes.md) -> per-scene section layout (30 fps frames).
Each clip = window + 0.25 s handle each side, rounded up to whole frames; sections laid end to end in one
composition per scene, then split frame-exactly by split_clips.sh. Writes windows.json and windows.js."""
import csv, json, math, pathlib
FPS = 30
HERE = pathlib.Path(__file__).parent
TIMING = HERE / "../../projects/insurance-ombudsman/timing.csv"
SCENES = {  # scene folder -> [(clip name, VO id, film start, film end)]; O047 in C3, O048 in C1 (S0 correction, 2026-10-15)
    "C1_filing_stepper": [("C1_filing_stepper_O039", "O039", 352.01, 356.93), ("C1_filing_stepper_O040", "O040", 357.13, 362.51),
                          ("C1_filing_stepper_O048", "O048", 403.56, 412.80)],
    "C2_offices_board": [("C2_offices_board_O041", "O041", 362.93, 377.97)],
    "C3_document_slots": [("C3_document_slots_O042", "O042", 378.38, 380.80), ("C3_document_slots_O043", "O043", 381.24, 383.62),
                          ("C3_document_slots_O044", "O044", 384.06, 387.80), ("C3_document_slots_O045", "O045", 388.22, 391.22),
                          ("C3_document_slots_O046", "O046", 391.66, 395.09), ("C3_document_slots_O047", "O047", 395.48, 403.15)],
    "C4_binding_award": [("C4_binding_award_O010", "O010", 89.72, 108.88), ("C4_binding_award_O052", "O052", 436.69, 440.90),
                         ("C4_binding_award_O056", "O056", 462.79, 468.85), ("C4_binding_award_O057", "O057", 469.28, 477.22)],
    "C5_proof_magnifier": [("C5_proof_magnifier_O018", "O018", 182.57, 193.38), ("C5_proof_magnifier_O022", "O022", 219.61, 231.38),
                           ("C5_proof_magnifier_O027", "O027", 258.60, 269.40), ("C5_proof_magnifier_O035", "O035", 324.69, 331.49),
                           ("C5_proof_magnifier_O036", "O036", 331.90, 335.69), ("C5_proof_magnifier_O037", "O037", 336.09, 347.88)],
}
sent = {}
for r in csv.DictReader(open(TIMING)):
    sent.setdefault(r["id"], []).append((float(r["film_start"]), float(r["film_end"]), r["sentence"]))
out = {}
for scene, wins in SCENES.items():
    t, secs = 0, []
    for clip, vid, a, b in wins:
        frames = math.ceil(round((b - a + 0.5) * FPS, 3))
        f0 = a - 0.25  # film time of the clip's first frame
        secs.append({"clip": clip, "id": vid, "film_start": a, "film_end": b, "frame0": t, "frames": frames,
                     "start": round(t / FPS, 4), "dur": round(frames / FPS, 4),
                     "sentences": [[round(s - f0, 3), round(e - f0, 3), txt] for s, e, txt in sent[vid]]})
        t += frames
    out[scene] = {"frames": t, "duration": round(t / FPS, 4), "sections": secs}
    (HERE / scene).mkdir(exist_ok=True)
    (HERE / scene / "windows.js").write_text("window.WIN = " + json.dumps(out[scene], indent=1, ensure_ascii=False) + ";\n")
(HERE / "windows.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
for s, v in out.items():
    print(s, v["duration"], [(x["id"], x["start"], x["dur"]) for x in v["sections"]])
