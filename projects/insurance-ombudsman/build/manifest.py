#!/usr/bin/env python3
"""Write media_manifest.csv: every asset the film may use, with its licence (CLAUDE.md rights rule).
Sources: the owner's Pexels pack registers (handoff/asset-pack), Pixabay API (authors looked up), Commons manifest,
web captures, Episode 01 glimpses. Usage: python3 build/manifest.py"""
import csv, json, os, urllib.request
from pathlib import Path
P = Path(__file__).resolve().parents[1]
H = P / "handoff" / "asset-pack"
COLS = "file,kind,what_it_shows,source_page,file_url,author,licence,licence_url,attribution,width,height,edl_slots".split(",")
rows = []
for r in csv.DictReader(open(H / "FOOTAGE_REGISTER.csv")):
    rows.append(dict(file="owner/BP_HLTH02_Asset_Pack/" + r["local_file"], kind="video", what_it_shows=r["title"] + "; " + r["usage"],
                     source_page=r["source_url"], file_url="", author="Pexels contributor (see page)", licence="Pexels License",
                     licence_url=r["license_url"], attribution="Pexels", width=r["width"], height=r["height"], edl_slots=r["id"]))
for r in csv.DictReader(open(H / "PEXELS_INDIA_SOURCE_REGISTER.csv")):
    rows.append(dict(file="owner/Pexels_India_Only/" + r["local_file"], kind="video", what_it_shows=r["title"] + "; " + r["role"],
                     source_page=r["source_url"], file_url="", author=r["author"], licence="Pexels License",
                     licence_url=r["license_url"], attribution=f"Pexels / {r['author']}", width=r["width"], height=r["height"], edl_slots=r["id"]))
PIX = {"151857": "Syringe needle close-up on black", "67764": "Syringe on a turntable, blue light",
       "169446": "Typing on a phone keyboard at night (OTP stand-in)", "3176": "Finger tapping a smartphone on a desk",
       }   # 17257 (court columns) and 63241 (woman in a mask) dropped in revisions v2 / v3
key = os.environ.get("PIXABAY_API_KEY")
for vid, what in PIX.items():
    author = "Pixabay contributor"
    if key:
        try:
            req = urllib.request.Request(f"https://pixabay.com/api/videos/?key={key}&id={vid}", headers={"User-Agent": "Mozilla/5.0 Creator"})
            author = json.load(urllib.request.urlopen(req, timeout=30))["hits"][0]["user"] or author
        except Exception:
            pass
    rows.append(dict(file=f"broll/pixabay_{vid}.mp4", kind="video", what_it_shows=what, source_page=f"https://pixabay.com/videos/id-{vid}/",
                     file_url="", author=author, licence="Pixabay Content License", licence_url="https://pixabay.com/service/license-summary/",
                     attribution=f"Pixabay / {author}", width="", height="", edl_slots=""))
# Commons rows: from commons_fetch.py's manifest when present; the 2026-10-16 4K rebuild fetched the same three files
# directly (Special:FilePath), so otherwise the rows already in media_manifest.csv are kept
cmf = P / "assets" / "commons" / "manifest.json"
old = [r for r in csv.DictReader(open(P / "media_manifest.csv"))] if (P / "media_manifest.csv").exists() else []
cm = json.load(open(cmf)) if cmf.exists() else []
if not cm:
    rows += [r for r in old if r["file"].startswith("commons/bhc_")]
for it in (cm if isinstance(cm, list) else cm.get("items", cm.values())):
    f = it.get("file") or it.get("local") or ""
    if not any(k in f for k in ("bhc_01", "bhc_02", "bhc_03")):
        continue
    rows.append(dict(file="commons/" + Path(f).name, kind="photo", what_it_shows="Bombay High Court building, Mumbai",
                     source_page=it.get("page", it.get("source_page", "")), file_url=it.get("url", ""), author=it.get("author", it.get("artist", "")),
                     licence=it.get("licence", it.get("license", "")), licence_url=it.get("licence_url", it.get("license_url", "")),
                     attribution=it.get("credit", ""), width="", height="", edl_slots="O061"))
for f, url, what in (("web/bima_full.png", "https://bimabharosa.irdai.gov.in/", "Bima Bharosa home page (IRDAI), captured 15 Oct 2026"),
                     ("web/cio_full.png", "https://cioins.co.in/", "Council for Insurance Ombudsmen home page, captured 15 Oct 2026"),
                     ("web/cio_complaint_full.png", "https://cioins.co.in/Complaint", "CIO grievance portal, eligibility check, captured 15 Oct 2026"),
                     ("web/cio_offices_hyd_full.png", "https://cioins.co.in/Ombudsman", "CIO office directory, Hyderabad centre selected, captured 16 Oct 2026"),
                     ("web/cio_gro_blur.png", "https://cioins.co.in/GRONonLife", "CIO list of insurers' Grievance Redressal Officers; officers' names and personal emails blurred, captured 16 Oct 2026")):
    rows.append(dict(file=f, kind="screen capture", what_it_shows=what, source_page=url, file_url=url, author="IRDAI / CIO",
                     licence="Government website, short credited excerpt", licence_url="", attribution=url, width="", height="", edl_slots=""))
for g in sorted((P / "assets" / "episode1" / "glimpses").glob("g*.mp4")):
    rows.append(dict(file="episode1/glimpses/" + g.name, kind="video", what_it_shows="Glimpse from Episode 01 (our own film)",
                     source_page="projects/health-claim-trap", file_url="", author="Be Practical with Kishore",
                     licence="Own work (third-party layers credited in Episode 01 media_manifest.csv)", licence_url="",
                     attribution="Episode 01", width="3840", height="2160", edl_slots="O001-O002"))
rows.append(dict(file="episode1/bill_consumables.png", kind="still", what_it_shows="Episode 01's SIMULATION hospital bill, Medicines and consumables line (O064)",
                 source_page="projects/health-claim-trap", file_url="", author="Be Practical with Kishore", licence="Own work", licence_url="",
                 attribution="Episode 01", width="2480", height="1395", edl_slots="O064"))
for name, raw, what in (("IO-1", "hospital_corporate", "Clinic helpdesk worker with a headset (Canva video template)"),
                        ("IO-2", "office_computer", "Hands typing on a laptop; the cioins.co.in grievance page composited on the screen (Canva template + our capture)"),
                        ("IO-3", "office_computer", "Laptop loading spinner while typing (Canva video template)"),
                        ("IO-5", "medical_white_blue", "Doctor explaining papers to a patient, cropped from a Canva video template")):
    rows.append(dict(file=f"canva/{name}.mp4", kind="video", what_it_shows=what, source_page=f"Canva template in the owner's account ({raw}; 4K MP4 export via the Canva connector, tools/make_canva.py)",
                     file_url="", author="Canva Pro (owner's account)", licence="Canva Content License (Pro)",
                     licence_url="https://www.canva.com/policies/content-license-agreement/", attribution="Canva",
                     width="3840", height="2160", edl_slots=name))
with open(P / "media_manifest.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
