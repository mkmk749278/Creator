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
Still to fetch (Commons is rate-limiting this IP; retry slowly): Kaveri at Aero India, GTX-35VS Kaveri, Kaveri prototype,
Tejas / Tejas Mk1A, MiG-21 Bison, INS Arihant, Pokhran-II (Shakti) site, LVM3, Chandrayaan-3, MOM.

## Owner fetch (YouTube official channels): `fetch_list.md`
