#!/usr/bin/env python3
"""Build media_manifest.csv (every asset in the EDL with its licence) from the download logs.

Sources: assets/broll/fetch.log (stock_fetch.py rows), assets/photos/commons.csv (Commons API metadata),
plus the hand-entered rows below (Dailymotion broadcasts, Freesound audio, map data, our own animation).
  python3 tools/manifest.py   -> media_manifest.csv (and warns about EDL assets with no licence row)
"""
import csv
import io
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
A = HERE / "assets"
FIELDS = ["file", "kind", "what_it_shows", "source_page", "file_url", "author", "licence", "licence_url", "attribution", "edl_slots", "notes"]

MANUAL = [
    ["raw/dm_x4ly2a2.mp4", "video", "VICE documentary 'The Superhuman World of the Iceman' (2016): Wim Hof under ice, in an icy canal, the 2012 Radboud endotoxin test (IV, EEG, hospital ward), Prof. Peter Pickkers, archive of Hof running barefoot in snow and meditating; host Matt Shea shirtless in snow",
     "https://www.dailymotion.com/video/x4ly2a2", "", "VICE", "Uploader's copyright (VICE official Dailymotion channel): short credited excerpts for commentary; owner to confirm", "", "VICE · The Superhuman World of the Iceman (2016)", "", "288p; contains archive footage credited by VICE to Dutch Institute for Sound and Vision, EenVandaag, Henny Bodgert"],
    ["raw/dm_x7zlb64.mp4", "video", "DW Euromaxx 'Eiskaltes Vergnügen: Winterbaden mit Wim Hof' (2021): Hof in an ice barrel, running in snow, ice-cube column, lying breathing exercise, hospital endotoxin test, meditating on an ice floe, walking into an icy lagoon",
     "https://www.dailymotion.com/video/x7zlb64", "", "Deutsche Welle (DW); clips watermarked wimhofmethod.com", "Uploader's copyright (DW official channel): short credited excerpts for commentary; owner to confirm", "", "DW Euromaxx (2021); footage: Wim Hof Method", "", "288p"],
    ["audio/bgm_matio.mp3", "audio", "'Cinematic Ambient' music bed (6:55)", "https://freesound.org/people/Matio888/sounds/795808/", "", "Matio888", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/", "'Cinematic Ambient' by Matio888 (Freesound), CC BY 4.0", "whole film", "bed via tools/make_bed.py"],
    ["audio/amb_monks.mp3", "audio", "Field recording: Himalaya, Buddhist monks", "https://freesound.org/people/kevp888/sounds/440226/", "", "kevp888", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/", "'BR_078v2_Himalaya_BuddhistMonks' by kevp888 (Freesound), CC BY 4.0", "P2 L1", "10 s cut amb_monks_cut.wav"],
    ["audio/sfx_blizzard.mp3", "audio", "Blizzard wind", "https://freesound.org/people/craigsmith/sounds/675701/", "", "craigsmith", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "craigsmith (Freesound), CC0", "P1 L1", ""],
    ["audio/sfx_howl.mp3", "audio", "Howling wind", "https://freesound.org/people/JSilverSound/sounds/528328/", "", "JSilverSound", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "JSilverSound (Freesound), CC0", "P1 L8", ""],
    ["audio/sfx_ice_crack.mp3", "audio", "Ice cracking sequence", "https://freesound.org/people/GregorQuendel/sounds/424993/", "", "GregorQuendel", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/", "'Ice Cracking Sequence' by GregorQuendel (Freesound), CC BY 4.0", "P1 L7", ""],
    ["audio/sfx_ice_crack2.mp3", "audio", "Ice crack", "https://freesound.org/people/ecfike/sounds/177217/", "", "ecfike", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "ecfike (Freesound), CC0", "P1 L6, P2 L12", ""],
    ["audio/sfx_fire.mp3", "audio", "Fire crackling", "https://freesound.org/people/kingsrow/sounds/181563/", "", "kingsrow", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "kingsrow (Freesound), CC0", "P1 L19, P3 L15", ""],
    ["audio/sfx_steam.mp3", "audio", "Steam hiss", "https://freesound.org/people/jaimage/sounds/269667/", "", "jaimage", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "jaimage (Freesound), CC0", "P1 L11, P2 L15", ""],
    ["audio/sfx_bowl.mp3", "audio", "Tibetan singing bowl", "https://freesound.org/people/enhuber/sounds/400819/", "", "enhuber", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "enhuber (Freesound), CC0", "P2 L1", ""],
    ["audio/sfx_bowl_strike.mp3", "audio", "Singing bowl strike", "https://freesound.org/people/inoshirodesign/sounds/271370/", "", "inoshirodesign", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "inoshirodesign (Freesound), CC0", "P1 L21", ""],
    ["audio/sfx_whoosh.mp3", "audio", "Deep whoosh", "https://freesound.org/people/Kinoton/sounds/351256/", "", "Kinoton", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "Kinoton (Freesound), CC0", "P1 L12", ""],
    ["audio/sfx_heartbeat.mp3", "audio", "Heartbeat 60 bpm", "https://freesound.org/people/loudernoises/sounds/332821/", "", "loudernoises", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "loudernoises (Freesound), CC0", "P1 L4", ""],
    ["video/fireice/benson_map/map.js", "data", "World land outlines (no political borders)", "https://github.com/topojson/world-atlas", "", "Natural Earth / Mike Bostock (world-atlas 2.0.2)", "Public domain (Natural Earth); package ISC", "https://www.naturalearthdata.com/about/terms-of-use/", "Made with Natural Earth", "P2 L5", ""],
    ["hf/*.mp4", "animation", "Original HyperFrames animation (video/fireice/): thermal figures, cells, mitochondria, map, charts, logo sting, end card", "", "", "Be Practical with Kishore", "Own work", "", "", "", "no AI generation used"],
]


def main():
    rows = {}
    log = (A / "broll" / "fetch.log").read_text()
    for line in log.splitlines():
        if line.startswith("pixabay_"):
            r = next(csv.reader(io.StringIO(line)))
            rows["broll/" + r[0]] = dict(zip(FIELDS, ["broll/" + r[0], r[1], "", r[3], r[4], r[5], r[6], r[7], r[8], "", f"{r[9]}x{r[10]}"]))
    for r in csv.DictReader((A / "photos" / "commons.csv").open()):
        rows["photos/" + r["file"]] = dict(file="photos/" + r["file"], kind="image", what_it_shows=" ".join(r["desc"].split())[:160], source_page=r["page"], file_url="",
                                           author=r["author"], licence=r["licence"], licence_url=r["licence_url"],
                                           attribution=f"{r['author']} / Wikimedia Commons, {r['licence']}", edl_slots="", notes=f"{r['w']}x{r['h']}")
    if "photos/tummo_naropa.jpg" in rows:   # derived crops keep the source's licence row
        rows["photos/tummo_naropa_crop.jpg"] = dict(rows["photos/tummo_naropa.jpg"], file="photos/tummo_naropa_crop.jpg", notes="1280x720 crop of tummo_naropa.jpg")
    for m in MANUAL:
        rows[m[0]] = dict(zip(FIELDS, m))
    used = {}
    for e in csv.DictReader((HERE / "edl.csv").open()):
        used.setdefault(e["asset"], []).append(e["line"])
    for k, r in rows.items():
        if k in used:
            r["edl_slots"] = " ".join(sorted(set(used[k]), key=used[k].index))
    with (HERE / "media_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for k in sorted(rows):
            if k in used or not k.startswith(("broll/", "photos/")):
                w.writerow(rows[k])
    missing = [a for a in used if a not in rows and not a.startswith("hf/")]
    print(f"{sum(1 for k in rows if k in used)} used assets logged; no licence row for: {missing or 'none'}")


if __name__ == "__main__":
    main()
