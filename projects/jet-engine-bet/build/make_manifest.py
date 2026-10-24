#!/usr/bin/env python3
"""Write projects/jet-engine-bet/media_manifest.csv: one row per third-party file the 4K edit actually uses (CLAUDE.md rights rule).

Sources: the Commons/Openverse manifest in assets/real/manifest.json, the owner-fetched official clips (fetch_list.md of the
old film), the TurboSquid airframe, Poly Haven CC0 textures. Scenes we rendered ourselves are not listed.
  python3 projects/jet-engine-bet/build/make_manifest.py
"""
import csv, importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]; P = ROOT / "projects/jet-engine-bet"
spec = importlib.util.spec_from_file_location("a4k", ROOT / "video/jet-engine-bet/assemble/assemble_4k.py")
A = importlib.util.module_from_spec(spec); sys.argv = sys.argv[:1]; spec.loader.exec_module(A)
used = {}
for s in A.SHOTS:
    if s["kind"] == "card": continue
    used.setdefault(s["src"].name, []).append(f"{int(s['t0'] // 60)}:{s['t0'] % 60:04.1f}")
real = {m["file"]: m for m in json.loads((P / "assets/real/manifest.json").read_text())}
OFFICIAL = {  # owner-fetched official channels (projects/jet-engine-paradox/fetch_list.md); short credited excerpts, owner-cleared
    "YfQNVWn8aIc.mp4": ("DD India: Rajnath Singh inaugurates 3rd LCA Mk1A line, HAL Nashik (hangar, Mk1A on the jig, Mk1A taxiing)", "https://www.youtube.com/watch?v=YfQNVWn8aIc", "DD India (Prasar Bharati)", "VIDEO: DD INDIA"),
    "ryolgbuDNSg.mp4": ("PIB India: Tejas at Aero India 2019 (taxi, display flying)", "https://www.youtube.com/watch?v=ryolgbuDNSg", "Press Information Bureau", "VIDEO: PIB INDIA"),
    "DLA_64yz8Ss.mp4": ("ISRO: Chandrayaan-3 landing broadcast, mission control", "https://www.youtube.com/watch?v=DLA_64yz8Ss", "ISRO", "VIDEO: ISRO"),
    "q2ueCg9bvvQ.mp4": ("ISRO: LVM3 launch broadcast", "https://www.youtube.com/watch?v=q2ueCg9bvvQ", "ISRO", "VIDEO: ISRO"),
    "52f1mQqaii8.mp4": ("Indian Air Force: MiG-21 final flight tribute", "https://www.youtube.com/watch?v=52f1mQqaii8", "Indian Air Force", "VIDEO: INDIAN AIR FORCE"),
    "zCYBJtBaUXw.mp4": ("Indian Air Force: MiG-21 farewell, flight line", "https://www.youtube.com/watch?v=zCYBJtBaUXw", "Indian Air Force", "VIDEO: INDIAN AIR FORCE"),
}
rows = []
for name, at in sorted(used.items()):
    if name in OFFICIAL:
        w, url, auth, tag = OFFICIAL[name]
        rows.append([f"assets/legacy/sources/{name}", "footage (excerpt)", w, url, "fetched by the owner (Fetch media workflow)", auth,
                     "third-party; short credited excerpt (PLAYBOOK §8.6), owner-cleared", "", f"{tag} (on-screen tag) · used at {', '.join(at)}"])
    elif name in real:
        m = real[name]
        rows.append([f"assets/real/{name}", m["kind"], m["what_it_shows"][:160], m["source_page"], m.get("file_url", ""), m["author"][:80],
                     m["licence"], m.get("licence_url", ""), f"{m['credit']} · used at {', '.join(at)}"])
rows.append(["video/jet-engine-bet/R1v3_walk/models/tejas_lite.fbx", "3D model", "HAL Tejas Fighter Navy (twin-seat airframe, repainted Air Force grey, decals removed)",
             "https://www.turbosquid.com/3d-models/hal-tejas-fighter-navy-3d-model-1458138", "downloaded free by the owner, 2026-10-23", "TurboSquid artist (product 1458138)",
             "TurboSquid Royalty Free License (free product); treated as editorial: documentary only, never in the thumbnail; file not redistributed",
             "https://blog.turbosquid.com/royalty-free-license/", "CG walk-around 0:07.8-0:15.1 and 0:20.7-0:33.7 (ILLUSTRATION tag)"])
for f in ("hangar_interior_2k.hdr", "hangar_concrete_floor (diff, rough, nor_gl 2k)"):
    rows.append([f"video/jet-engine-bet/_lib/ph/{f}", "HDRI/texture", "hangar lighting and floor for the CG walk-around", "https://polyhaven.com", "https://dl.polyhaven.org",
                 "Poly Haven", "CC0", "https://polyhaven.com/license", "no credit required"])
with open(P / "media_manifest.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["file", "kind", "what_it_shows", "source_page", "file_url", "author", "licence", "licence_url", "attribution"]); w.writerows(rows)
print(len(rows), "rows ->", P / "media_manifest.csv")
