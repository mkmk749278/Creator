# Viewer review 3: triage (2026-10-16)

An independent session with no repo access watched the voiced reel v1 (8:34) as frames at 2 fps and read the narration
text. This file records what we did with each finding. Reel times are v1 times.

## Content

| Finding | Verdict | Action |
|---|---|---|
| C7 shows "RULE: MAX 15 KM/H" as what Kavach enforces; E7 then debunks "Kavach always locks 15" | **Accepted** | C7 now reads "HELD SLOW · TO A SET LIMIT". "STOPS SHORT" became "ROOM TO STOP": the narration only claims a slow speed and the allowed movement. |
| "Several sources give 10 km/h under GR 9.02" | Checked, kept | KV-082 and KV-092: the CCRS preliminary report (via Indian Express, 16 Jul 2024) gives 15 km/h at failed automatic signals under GR 9.02. The C4 rule card and the E7 line stay. |
| D4 J&K outline looks de facto | Rejected (again) | The map is built from the official India-POV boundary data (`_D_tools/build_map.py`, review 2). |
| C3 "ITS OWN CHECKS" needs an apostrophe | Changed | "ITS" was correct as a possessive. Reworded to "KAVACH'S OWN CHECKS" so it reads clearly. |
| C3: train positions jump from C1 | Deferred | The schematics are separate views; to be matched in the EDL pass with real footage. |
| A9 labels differ from A2 | Partly | A9 lists the narration's four conditions (engine, track section, signalling data, room to stop), not the four hardware links. Labels are now "SIGNAL DATA" and "ROOM TO STOP", wider and bigger. |

## Clipping and bugs

| Finding | Action |
|---|---|
| D9 "WORKIN" badge clipped | The camera now ends at scale 1.15 and x −40, so the badge sits inside the frame. |
| C4 "KANCHANJUNGA EXP" cut off | The label is anchored at the rear of the rake. |
| E7 "DEPENDS ON SET-UP" stamp clipped and covering the dial | The stamp is moved under the forward card. The dial is now 0–40 km/h, so 15 reads clearly. |
| D2 metres counter out of sync | Checked: no change. The counter is the nose position (36.1 m/s × t). A frame at 3.0 s shows 103 m with the nose about 5 m short of the 3 s post. The reviewer's 60/96 readings do not reproduce. |
| E4 "RADIO TOWER" blob | Fixed earlier (`stroke="none"`); the reviewer saw the old cut. |
| E1 lock-screen date | Already "Monday"; the reviewer saw the old cut. |

## Pacing and holds

| Finding | Action |
|---|---|
| E2: 8 s still of two cards | The camera leans into each forward as it is read, then pulls back. A marker sweeps under "never bothered with safety" and "Crashes are impossible now". The MYTH labels are bigger. |
| E8: phone still for 6 s | Push-in on the forward while it is introduced. On "ask three questions", three numbered slots slide in and fill on each question. The "?" glyphs are now 1/2/3 (channel rule: no question-mark graphics). |
| B6: 208 still for 6 s | On "in five years… April 2019 to March 2024", a bar sweeps the five years and each year lights as it passes. "12" stays on its own word (semantic lock). |
| A9: 7.5 s with little change | One callout per phrase: ~~MAGIC~~ → ~~USELESS~~ → INDIAN-BUILT SAFETY LAYER → BRAKES EARLY. Then the four conditions light up. |
| A8: brake-pipe wave reads as all at once | Frames show the 3D wave does travel (5.7 s → 11.3 s), but the rear is foreshortened. Added a large strip: "BRAKES APPLIED · COACH n OF 8", with the engine and eight coach cells filling in turn. No timing number, because we have no sourced figure for it. |
| C6: "→ ≈ 40" shown before the impact | The label first reads "78 km/h · TOP SPEED"; "→ ≈ 40 km/h · AT IMPACT" appears at the impact. |
| C4: signals look working before "had failed" | Kept. They fail on the words "The automatic signals had failed"; the narration does not say it earlier. |

## Not done in this pass (logged for the EDL and assembly)
- **Phone text size across about 30 scenes.** This is the review's top item. Primary labels are mostly 26–34 px, and secondary lines are 18–22 px. Each scene needs a separate pass to make them bigger or remove them.
- **Look of the 3D world.** A WAP-7-style engine, a flat RFID tag, a two-pane cab window, the A3 transparent engine body, and one time of day across A1–A7. These are model rebuilds.
- **Shorter holds still open:** E4 icon, A5 black climb, D3/D8/B2 empty axes at the start, D5, D7 clippings, B1, B3 timer freeze, A1 cut count.
- **A shared 2D four-link chain graphic** for A2, E5 and A9.
