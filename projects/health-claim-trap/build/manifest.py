#!/usr/bin/env python3
"""Write media_manifest.csv (every asset in the cut, with licence and EDL slots) from the download logs and edl.csv."""
import csv, json, collections
from pathlib import Path
P = Path(__file__).resolve().parents[1]; A = P / "assets"
WHAT = {
 "49815": "Doctor measuring a patient's blood pressure with a cuff", "49814": "Doctor holding up a leg X-ray", "49813": "Gloved hand writing on a medical chart",
 "49809": "Doctor reviewing brain scans on a monitor, writing notes", "229071": "Patient in a wheelchair, doctor examining the leg", "142528": "Clinic staff working at a computer",
 "349087": "Hands flipping through paper files in an archive", "87146": "Hands taking colourful office binders from a shelf", "34258": "Hand writing with a pen on paper",
 "3145": "Hands typing on a laptop, top view", "202987": "Hands using a phone in a dark room", "204421": "Worried man talking on a phone in the dark",
 "212508": "Man sitting on the floor reading a document", "200431": "Hyderabad skyline and lake at dusk, aerial", "134434": "Indian city rooftops at dusk with the national flag",
 "19627": "Indian city highway at night, traffic", "1643": "Busy Indian market street", "326937": "Close-up of an old clock face", "65551": "Syringe on a table, low light",
 "143379": "Gloved hands handling sample tubes", "199442": "Man reading a letter at night by lamplight", "10874": "Silhouettes of people waiting in a dark hall",
 "1383": "Silhouettes waiting by a window", "5457": "IV drip bags in a hospital", "40353": "Nurse working at monitors in a hospital ward", "144015": "Clinic: blood sample being taken",
 "143988": "Patient consulting a doctor in a clinic", "26732": "Pharmacist working at a counter computer", "3175": "Indian street with cycle rickshaws, daytime",
 "143376": "Nurse with a tablet",
}
COVERR = {"coverr-iv-in-hospital-room-5485": "IV stand in a dim hospital room", "coverr-putting-medical-gloves-on-5311": "Hands putting on medical gloves",
          "coverr-a-printer-at-work-in-the-office-5252": "Office printer printing pages", "coverr-giving-cashier-a-credit-card-9719": "Customer handing a card to a cashier",
          "coverr-hands-turning-pages-in-a-notebook-8881": "Hands turning notebook pages", "coverr-transferring-card-details-5376": "Person entering card details on a phone"}
slots = collections.defaultdict(list)
for r in csv.DictReader(open(P / "edl.csv")):
    slots[r["asset"]].append(r["start"])
rows = []
for line in (A / "pixabay_get.log").read_text().splitlines():
    if line.startswith("pixabay_"):
        f = line.split(",")
        pid = f[0][8:-4]
        f[2] = WHAT.get(pid, "Pixabay clip")
        rows.append(f + [" ".join(slots.get(f[0], []))])
for k, v in COVERR.items():
    rows.append([k + ".mp4", "video", v, "https://coverr.co/videos/" + k, f"https://cdn.coverr.co/videos/{k}/1080p.mp4", "Coverr", "Coverr License",
                 "https://coverr.co/license", "Coverr", "1920", "1080", " ".join(slots.get(k + ".mp4", []))])
for png in sorted((A / "proof").glob("*.png")):
    n = png.stem
    src = ("IRDAI Master Circular on Health Insurance Business, IRDAI/HLT/CIR/PRO/84/5/2024 (29 May 2024)", "https://irdai.gov.in/document-detail?documentId=4942918", "IRDAI") if n.startswith("mc_") else \
          ("cioins.co.in home page (screenshot, 14 Oct 2026)", "https://cioins.co.in/", "Council for Insurance Ombudsmen") if n.startswith("cio_") and n != "cio_h3" else \
          ("CIO Annual Report 2024-25, Statement H3 (health)", "https://cioins.co.in/annualreports/AnnualReport2024-2025.pdf", "Council for Insurance Ombudsmen") if n == "cio_h3" else \
          ("Bima Bharosa portal home page (screenshot, 14 Oct 2026)", "https://bimabharosa.irdai.gov.in/", "IRDAI")
    rows.append([png.name, "proof", src[0] + "; highlight added", src[1], src[1], src[2], "Government/statutory document: credited short excerpt", "", src[2], "3840", "2160", " ".join(slots.get(png.name, []))])
for png in sorted((A / "sim").glob("*.png")):
    rows.append([png.name, "simulation", f"SIMULATION document ({png.stem}); no real hospital, insurer or TPA", "", "", "Be Practical with Kishore", "Own work", "", "", "3840", "2160", " ".join(slots.get(png.name, []))])
for mp4 in sorted((A / "scenes").glob("*.mp4")):
    rows.append([mp4.name, "animation", f"HyperFrames scene video/healthclaim/{mp4.stem}", "", "", "Be Practical with Kishore", "Own work", "", "", "1920", "1080", " ".join(slots.get(mp4.stem, []))])
SFX = [("whoosh_deep", "https://freesound.org/s/351256/"), ("whoosh_swish", "https://freesound.org/s/60026/"), ("whoosh_swipe", "https://freesound.org/s/60007/"),
       ("hosp_amb", "https://freesound.org/s/614805/"), ("room_tone", "https://freesound.org/s/129443/"), ("riser", "https://freesound.org/s/244249/"),
       ("impact_soft", "https://freesound.org/s/560156/"), ("typing", "https://freesound.org/s/379418/"), ("click", "https://freesound.org/s/208204/"),
       ("heartbeat", "https://freesound.org/s/332821/"), ("clock", "https://freesound.org/s/459998/"), ("stamp", "https://freesound.org/s/683031/")]
for n, u in SFX:
    rows.append([f"sfx/{n}.mp3", "sfx", n.replace("_", " "), u, u, "Freesound user (via Openverse)", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/", "", "", "", "sound design"])
rows.append(["owner/hospital_cutaway.jpg", "illustration", "AI-generated isometric hospital cutaway supplied by the owner (no real place or person)", "", "", "Owner (AI-generated)", "Owner-supplied; labelled ILLUSTRATION · AI-GENERATED IMAGE", "", "", "1376", "768", "0:03-0:06"])
rows.append(["geo/india-composite.geojson", "map data", "India boundary (Survey of India-based composite)", "https://github.com/datameet/maps/blob/master/Country/india-composite.geojson", "", "DataMeet India community", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/", "India boundaries by DataMeet India community (CC BY 4.0)", "", "", "e21_india"])
for n, u in [("bima_full.png", "https://bimabharosa.irdai.gov.in/"), ("cio_full.png", "https://cioins.co.in/")]:
    rows.append([f"web/{n}", "screen capture", f"Full-page capture of {u} (14 Oct 2026), replayed in a browser frame", u, u, "IRDAI" if "bima" in n else "Council for Insurance Ombudsmen",
                 "Government/statutory site: credited short excerpt", "", "", "2880", "", "e22_bima / e23_cio"])
rows.append(["banner.png / logo_square.png", "brand", "Channel logo sting, bug and end card", "", "", "Be Practical with Kishore", "Own work", "", "", "", "", ""])
rows.append(["bed.wav", "music", "Synthesised music bed (scripts/make_bed.py, seeded, no samples)", "", "", "Be Practical with Kishore", "Own work", "", "", "", "", "whole film"])
with open(P / "media_manifest.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow("file,kind,what_it_shows,source_page,file_url,author,licence,licence_url,attribution,width,height,edl_slots".split(","))
    w.writerows(rows)
print(len(rows), "rows")
