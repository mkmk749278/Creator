---
name: source-media
description: Find, download, vet and log real footage, photos, music and sound effects for a documentary, working down the tested fallback chains. Use when a video needs media for its beats, or a source is blocked. Produces asset-manifest.md, media_manifest.csv rows and labelled contact sheets.
---

# Source media

Read PLAYBOOK §8 first (tested sources, keys, fallback chains, rules). One sourcing session per video: every cloud session
shares one IP, so parallel sessions only multiply 429s. Subagents may search in parallel on hosts that don't rate-limit.

For each beat in the EDL draft:
1. **Library first:** `python3 scripts/library.py list` and `video/lib/` (HDRIs, models, beds, verified B-roll).
2. **Real event footage next**, down the chain for its need (§8.4). Search several candidates; keep the highest
   resolution; note exact in/out points from 1 fps timecoded sheets.
3. **Download** with the matching tool: `scripts/openverse_fetch.py`, `scripts/commons_fetch.py` (User-Agent, standard
   thumb widths), `projects/prahlad-jani-drdo/tools/fetch_assets.py` (Coverr, NASA, Wellcome), `scripts/fetch_media.py`
   (yt-dlp: Dailymotion, archive.org, Instagram, Facebook; YouTube works only some of the time from the cloud).
   YouTube blocked → list exact URLs and `@START-END` ranges for the owner to run in the **Fetch media for a video**
   workflow (VPS runner or YT_COOKIES), and ask him to put the artifact in Google Drive. Never use VPNs, proxies or
   alternative clients.
4. **Licence in code:** commercial-use licences only (CC0, PD, CC BY, CC BY-SA, Pexels/Pixabay/Coverr/Unsplash licences);
   check each file's own page; NC/ND never. Third-party news/event clips: short, credited excerpts, owner-cleared.
5. **Vet:** `python3 scripts/contact_sheet.py <folder> --out <qa>`; look at every tile; drop mismatches (about a third
   of search results are wrong). `what_it_shows` must be literally true.
6. **Log:** a `media_manifest.csv` row per file (ID, file, what_it_shows, source page, file URL, author, licence,
   licence URL, attribution, EDL slots). Reusable, licence-clean items → `python3 scripts/library.py add ...`.
7. **Report:** contact sheet, what is real vs stand-in (stand-ins get "ILLUSTRATIVE FOOTAGE"), what failed and why, and
   the exact asks for the owner. Update PLAYBOOK §8.1 if a source's status changed.
