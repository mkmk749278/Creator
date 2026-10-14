# Asset manifest: The Jet Engine Paradox (working, coordinator)

Vetted on contact sheets (`assets/qa_broll/`, `assets/commons/`). Files live in `assets/` (gitignored); licences in
`media_manifest.csv` (built at assembly from `assets/*/manifest*`).

## B-roll (Pixabay, Pixabay Content License)
| File | Shows (literally) | Use | Verdict |
|---|---|---|---|
| pixabay_146606 | Aerial of green mountain ridges with clouds rolling over | J048 "freezing mountain air" | keep |
| pixabay_16160 | Dark stormy sea under heavy cloud, dusk | J048 "humid sea air" | keep (lift mid-tones) |
| pixabay_7686 | Desert dunes; later a man and a dust devil | J048 "desert dust": first 40 % only (no person) | keep, trimmed |
| pixabay_135849 | Welder in a dark workshop, sparks | J069 "made" | keep |
| pixabay_18533, 34717 | Industrial laser cutting metal sheet | J069 "drilled" | keep |
| pixabay_80355 | Hands checking a machined part on a gauge, Indian factory | J069 "tested" | keep |
| pixabay_244334 | A fighter (F-16 type) in clouds, aerial | fallback only for J049 if no IAF clip | fallback, ILLUSTRATIVE FOOTAGE |
| pixabay_52536 | Airliner (civil) fan close-up | — | drop: civil engine, wrong for a fighter beat |
| pixabay_14096 | Green-screen F-16 render | — | drop: CGI, foreign jet |

## Commons (licence per file in `assets/commons/manifest*.json*`)
GE F404 photos ×6 (US Navy PD; FA-50PH CC BY-SA 4.0), J-20 ×4, AMCA model at Aero India, Il-76 with a Kaveri engine.
`assets/commons2/`: GTX-35VS Kaveri on display (Jagan Pillariseti, CC BY 3.0, credited on screen) → J030.

## Proof pages (`assets/proof/`, `tools/proof_shots.js`)
PIB 2012 (J031, J043), SPS Aviation 2008 (C7), Bloomberg 29 Oct 2024 supply-chain quote and headline (J016), US CRS RS20995 2002 (J022), PIB 26 Apr 2021 DMRL release (J075) and its blade photo (GoI press photo, credited PIB).
Still to fetch (Commons is rate-limiting this IP; retry slowly): Kaveri at Aero India, GTX-35VS Kaveri, Kaveri prototype,
Tejas / Tejas Mk1A, MiG-21 Bison, INS Arihant, Pokhran-II (Shakti) site, LVM3, Chandrayaan-3, MOM.

## Owner fetch (YouTube official channels): `fetch_list.md`

## Owner-fetched official clips (2026-10-14, phone yt-dlp → Drive Creator/; local assets/yt/)
Short credited excerpts, credit burned top-left in the cut.
| File | Channel | Shows | Used at |
|---|---|---|---|
| YfQNVWn8aIc | DD India | Tejas Mk1A taxi/flight, airframes on jigs at HAL Nashik (Oct 2025); DD lower third cropped off | J005, J006, J018 |
| ryolgbuDNSg | PIB India | Tejas at Aero India 2019: take-off roll, smoke aerobatics; PIB logo cropped, "Aero India 2019" banner avoided | J024, J049, J089 |
| 52f1mQqaii8 | Indian Air Force | MiG-21 final flight 2025: afterburner close-up, in flight | J012, J025 |
| zCYBJtBaUXw | Indian Air Force | MiG-21 culmination ceremony: flight line at sunset, take-off | J010, J049 |
| q2ueCg9bvvQ (25:00–50:00) | ISRO Official | LVM3-M4/Chandrayaan-3 lift-off; stage-separation animation (labelled) | J046, J047, J085 |
| bYhSZ9uHO0U | DRDO INDIA | Flying-wing demonstrator take-off roll (2022) | J074 |
| KmbdhhXTq7Y | DRDO INDIA | Same flight, DRDO logo | spare |
| _io4f2I5-sY | ISRO | Mars orbit insertion simulation (400×308, labelled ILLUSTRATION) | J003 |
| HcskFT8ngSQ | GE Aerospace | Interview film, engines only as small insets | not used |
| DLA_64yz8Ss (33:00–46:00) | ISRO Official | Landing telecast: mission control, live descent simulation (labelled), touchdown celebration | J001, J002, C2 |
