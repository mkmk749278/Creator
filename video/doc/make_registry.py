"""Build video/doc/registry.json: logical asset name -> candidate files (owner ./assets first).

Owner files (the directive's ./assets/ layout) always win when present. Otherwise the
licensed media fetched into video/breathhold/_media/*/manifest.json fill in, with an honest
corner tag ("ARCHIVE PHOTO · 2013", "ILLUSTRATIVE", "B-ROLL") so a stand-in never passes
as event footage. Run: python video/doc/make_registry.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEDIA = ROOT / "video/breathhold/_media"

OWNER = {
    "vidyut_stage_trance": "assets/video/vidyut_stage_trance.mp4",
    "vidyut_tears_macro": "assets/video/vidyut_tears_macro.mp4",
    "vidyut_shivering": "assets/video/vidyut_shivering.mp4",
    "vidyut_shankha": "assets/video/vidyut_shankha.mp4",
    "vidyut_kalari": "assets/video/vidyut_kalari.mp4",
    "vidyut_workouts": "assets/video/vidyut_workouts.mp4",
    "freediver_pool": "assets/video/freediver_pool.mp4",
    "o2_mask_breathing": "assets/video/o2_mask_breathing.mp4",
    "city_rush_timelapse": "assets/video/city_rush_timelapse.mp4",
    "sadhu_haridas_1837": "assets/images/sadhu_haridas_1837.jpg",
    "patanjali_manuscript": "assets/images/patanjali_manuscript.jpg",
}
# Stand-ins when the owner file is missing (all names are merged, in order).
FALLBACK = {
    "vidyut_stage_trance": ["vidyut_portrait", "press_crowd"],
    "vidyut_tears_macro": ["vidyut_portrait", "eyes"],
    "vidyut_shivering": ["vidyut_portrait", "eyes", "press_crowd"],
    "vidyut_shankha": ["conch_video"],
    "vidyut_kalari": ["kalari"],
    "vidyut_workouts": ["kalari"],
    "freediver_pool": ["mifsud", "freediver"],
    "o2_mask_breathing": ["o2", "freediver"],
    "city_rush_timelapse": ["city_rush", "mumbai"],
    "sadhu_haridas_1837": ["court_painting", "haridas_plate"],
    "patanjali_manuscript": ["yogasutra_ms"],
    "haridas_book": ["haridas_plate"],
    "anatomy_carotid": ["anatomy_lungs"],
    "anatomy_brain": ["anatomy_carotid"],
    "anatomy_heart": ["anatomy_lungs"],
    "anatomy_diaphragm": ["anatomy_lungs"],
    "press_crowd": ["mumbai"],
}
# Session manifests: file prefix -> (name, tag, extra)
SESSION = {
    "people": [(r"^0[12]_vidyut", "vidyut_portrait", None)],
    "history": [(r"^01_", "haridas_plate", "ARCHIVE · 1852"), (r"^0[234]_", "haridas_book", "ARCHIVE · 1850s"),
                (r"^0[56]_", "ranjit_court", "ARCHIVE · 1852"), (r"^07_", "court_painting", "PAINTING · 19TH C."),
                (r"^08_", "yogasutra_ms", "MANUSCRIPT"), (r"^(09|10|11|12)_", "yogi_painting", "PAINTING"),
                (r"^1[34]_", "candle", None), (r"^1[56]_", "yogi_photo", None), (r"^1[78]_", "conch", "B-ROLL")],
    "science": [(r"^0[123]_mifsud", "mifsud", "STÉPHANE MIFSUD"), (r"^0[4-7]_", "freediver", None), (r"^09_", "stopwatch", None)],
}
FACE = {"vidyut_portrait": "50% 30%"}


def main():
    assets = {}

    def add(name, entry):
        assets.setdefault(name, {"files": [], "fallback": FALLBACK.get(name, [])})["files"].append(entry)

    for name, f in OWNER.items():
        add(name, {"file": f, "credit": ""})
    for topic, rules in SESSION.items():
        mf = MEDIA / topic / "manifest.json"
        if not mf.exists():
            continue
        for m in json.loads(mf.read_text()):
            for rx, name, tag in rules:
                if re.search(rx, m["file"]):
                    year = re.search(r"(19|20)\d\d", m.get("what_it_shows", "") + m.get("date", "") + m["file"])
                    t = tag if tag else ("ARCHIVE PHOTO" + (f" · {year.group(0)}" if year else "")) if name == "vidyut_portrait" else None
                    credit = m.get("attribution") or m.get("credit") or f"{m.get('author', 'Unknown')} · {m.get('licence')}"
                    add(name, {"file": f"video/breathhold/_media/{topic}/{m['file']}", "credit": credit[:140], "archive": t,
                               "what": m.get("what_it_shows", "")[:120], **({"origin": FACE[name]} if name in FACE else {})})
                    break
    ov = MEDIA / "ov" / "manifest.json"
    if ov.exists():
        for m in json.loads(ov.read_text()):
            name = m["name"]
            tag = {"vidyut_portrait": "ARCHIVE PHOTO", "eyes": "ILLUSTRATIVE", "o2": "ILLUSTRATIVE"}.get(name)
            if name.startswith("anatomy") or name in ("micro_blood", "eeg"):
                tag = "ILLUSTRATION" if "illustr" in m["title"].lower() or "gray" in m["title"].lower() else None
            add(name, {"file": f"video/breathhold/_media/ov/{m['file']}", "credit": m["credit"][:140], "archive": tag, "what": m["title"][:120]})
    for v in sorted((MEDIA / "ov").glob("conch_*.mp4")):
        add("conch_video", {"file": str(v.relative_to(ROOT)), "move": "none", "liveAudio": True,
                            "credit": "Nani Ma B-roll: Sankha-blowing · Subhashish Panigrahi · CC BY-SA 4.0 · archive.org", "burned": True})
    for name in {n for fb in FALLBACK.values() for n in fb} | set(FALLBACK):
        assets.setdefault(name, {"files": [], "fallback": FALLBACK.get(name, [])})
    (Path(__file__).parent / "registry.json").write_text(json.dumps({"assets": assets}, indent=1, ensure_ascii=False) + "\n")
    for n, e in sorted(assets.items()):
        print(f"{n:22s} {len(e['files'])} files  fallback={e['fallback']}")


if __name__ == "__main__":
    main()
