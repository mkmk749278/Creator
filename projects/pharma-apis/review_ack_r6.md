# pharma-apis: acknowledgement of the owner's review (round 6)

**For the next reviewer.** This answers the owner's notes of 30 Oct:
1. "Look at 3:36 to 3:40 and 4:10 to 4:15 while saying Pimpri, independence etc. What are the visuals actually showing,
   and while showing industries' names what are we showing? Most of the time the verbs, names and narration don't suit
   the scenes. Narration to scene, every second, word by word, scene by scene."
2. "Directly render the full film in 4K, and it should not look like stitches; all should feel smooth on screen."

The cut is the 4K master `pharma_apis_4k.mp4` (Drive `Creator/English/pharma-apis/`, replacing the round-5 master),
11:28.3, the same timing as round 5, so all times below hold for both.

Status key: **FIXED** · **CHECKED** (measured, the evidence given) · **OPEN** (not done, the reason given).

## 1. Narration to scene, word by word

Every one of the 181 round-5 shots was listed against the words spoken over it, with one frame each
(`build/shot_word_audit.py`; the full table and grades are in `review_picture_audit_r6.md`). 11 were WRONG, 8 WEAK.

| Time | Words | Was | Status / now |
|---|---|---|---|
| 3:35.6–3:44.9 | "Pimpri, near Pune. 1954. India has been free for less than seven years, and it's building a factory to make its own penicillin." | A British lab drawing | FIXED: the scene `pimpri`. India map → the Pimpri pin; a line fills from 15 AUG 1947 to 1954, "< 7 YEARS FREE"; the factory rises out of the ground with a crane, its lights come on, the tricolour flies, "PENICILLIN FACTORY" |
| 3:44.9 | "Penicillin was the miracle drug of that time." | A potency chart | FIXED: the 1944 I.C.I. film's own penicillin vials |
| 4:05.1–4:15.0 | "Picture your grandparents' India. A young, poor country, growing one of the most important medicines on earth… in its own factory." | Map, then the potency chart | FIXED: `pimpri_grow`. The plant at dusk, a cyclist on the road; the wall opens on a fermenter turning gold; vials roll out of its door |
| 4:15.0–4:24.2 | "Soon, others join in — Alembic, Sarabhai and Ranbaxy. India is making its own antibiotics." | A modern stock lab with name boxes | FIXED: `skyline_rise`. Each company's plant rises beside Pimpri on its own name; all light up on "making its own antibiotics" |
| 6:43.8–7:04.8 | "The Indian penicillin plants went quiet. H.A. Stopped. I.D.P.L. Stopped. Torrent. Ranbaxy. Sarabhai. Stopped. … Alembic. Stopped." | Stock gears | FIXED: the same skyline, six plants, goes quiet, then dark one by one on each name with a STOPPED stamp; H.A. and I.D.P.L. on their real footage |
| 1:36.6–1:42.8 | "First, let's give India its due… India earned it." | A Chinese softgel line | FIXED: Cipla's own plant (8 caption-free shots) |
| 2:32.4–2:37.2 | "Indian companies are world class at that last part." | The same Chinese line | FIXED: Cipla's chief in his plant, Cipla's line |
| 2:40.6 | "…the toughest inspections on the planet." | A Western stock model | FIXED: Lyfius's quality lab, Kakinada (microscope, bench) |
| 6:10.2–6:19.4 | "China went all in… It built huge plants, in huge drug parks, with cheap power and cheap water." | A smoking chimney | FIXED: real Chinese plants: CCTV+ mass vial lines and CGTN's CSPC plant, Shijiazhuang (the owner's Termux fetch); the chimney stays only on "looser pollution rules" |
| 7:22.1 | "Niti Aayog estimates Chinese powder costs 35–40% less…" | Pixabay worker | FIXED: Chinese packers (CCTV+) |
| 7:28.7 | "So tell me — if you ran a company, would you build a plant here?" | The chimney again | FIXED: India's plants, dark; then the empty Kakinada coast site |
| 7:04.8 | "India was importing all of that base powder…" | A port aerial with a hazard-marked deck | FIXED: the clean stretches of the same aerial |
| 8:26.7 | "…the tanks start running." | Bare land | FIXED: the fermenter hall |
| 2:37.2–2:40.6 | "Mixing, pressing, packing, and passing…" | — | CHECKED: each cut sits in the voice's own gap before its word (measured 157.32 / 158.13 / 158.85 / 159.48 s) |
| 0:00, 1:11, 1:19, 2:42, 3:24, 5:55 | Question and turn lines ("who makes the powder?", "has it always been like this?") | Medicine close-ups | CHECKED, kept: these lines name no object; the medicine is the subject |

No film of 1950s Pimpri, Alembic, Sarabhai or Ranbaxy exists that we could find or clear (YouTube API search,
`research/yt_search_r6.json`), so those beats are drawn from the words, labelled ILLUSTRATION, with no facts beyond the
narration's own.

## 2. "Should not look like stitches, all should feel smooth"

| Item | Status | What we did |
|---|---|---|
| Hard cuts between shots | FIXED | Every cut is now a 6-frame (0.2 s) dissolve: the incoming shot fades in while the outgoing one runs on beneath it. Each footage piece reserves those 6 frames inside its own clean span, so a dissolve never shows the source's next shot |
| Deliberate fast cuts | CHECKED, kept hard | The four verb cuts at 2:37 and the Cipla montage at 1:36 / 2:32 (0.7–1.4 s shots): dissolves there would smear the rhythm |
| Part seams | CHECKED | The five parts join with no blink (round 5's seam fix); see §3 |
| Direct 4K | DONE | No 720p round this time, per the owner |

## 3. Measured on the 4K master

MEASUREMENTS

## 4. Package

Title, description and chapters unchanged (the timing did not move): `youtube/description.md`. Thumbnails A (main), B, D
(challengers). The SRT is regenerated from this cut.
