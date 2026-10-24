# Independent cut review: film_v1_720p.mp4 (session session_01HjxSYAGNMmoBcHo2fQ2RC4, 2026-10-23)

Method: frames every 0.5 s (459 frames) on 12 timecoded contact sheets, full-res checks of suspect frames, scene-cut
detection, stream probe. Voice timings from `final/align/align.json`.

## 0. Blocker: the picture stops at 3:49
The 720p file has a **229.3 s video stream and a 510.6 s audio stream**: from 3:49.3 to 8:30.6 there is no picture
(confirmed here with ffprobe). The B6 slot at 3:36.7 also shows B3 (creep bar) again; B6 arrives 10.8 s late.
Gate added for every future cut: video and audio durations must match within 0.1 s, and the contact sheet must run to the last second.

## 1. Scores
Story clarity 3/10 as delivered (≈6.5 for the first 3:49). Visual realism 5/10. Cinematic quality 4/10.

## 2. Findings in the first 3:49 (v0 status)
| Time | Problem | v0? | Fix |
|---|---|---|---|
| 0:00–0:07 | Near-black first frame, peach band across the bottom 20%, "OCTOBER 2026" illegible until 0:04, no HAL/Bengaluru/Nashik text | not fixed | Lit first frame, band gone, date sharp at 0:00.2, "HAL · BENGALURU · NASHIK" at 0:03 |
| 0:07.8–0:20.2 | Hangar jets are toy-like tall-tailed straight-wing trainers, not a tailless delta Tejas; ~20 visible vs "about thirty"; no radome/cockpit on "radars fitted, cockpits wired" | not fixed | Real DD India HAL Nashik line footage; keep the label |
| 0:20.8–0:25.2 | "DELIVERED TO THE AIR FORCE: 0" works | kept | Hold 1 s past "Not one." |
| 0:28–0:33.1 | Floating nozzle petal ring, white pole, cables, dotted ring, bar, red block inside the "empty" tunnel | not fixed | Truly empty tunnel, hold 1.5 s on "Nothing." |
| 0:33.7–0:41.3 | 14 OF 99 bar works | kept | 2–3 s of the real GE F404 under the bar |
| 0:41.8–0:53.4 | Moon only | not fixed | LVM3 lift-off on "commercial satellites"; soft dissolve at 0:54 |
| 0:59.4–1:11.6 | No smartphone, no inferno, 3.5 s spoiler montage, blade-rise used twice in 13 s | not fixed | Phone beside the blade; flame on the blade; cut the montage |
| 1:12–1:19 | Empty Engine Club globe, "USA" 1 s only | not fixed | Five markers on "four or five countries", 1986→2026 line on "forty years" |
| 1:19.5–2:10 | **New R2 engine journey with SUCK/SQUEEZE/BURN/BLOW chips: works, best upgrade** | fixed | Add "hundreds of kg / second", 30× dial, 1,700 °C readout |
| 2:10.5–2:18.3 | 8 s of near-black arcs on "shoots out the exhaust… past the speed of sound" | not fixed | Nozzle plume 2 s, then real Tejas afterburner take-off 5 s |
| 2:18.5–2:22.8 | Cutaway works | improved | Flame→blade arrow, hold 1 s |
| 2:23.2–2:54.5 | 31 s single heat-map hold; 1,400 / 930 / 470 never on screen; no melt | not fixed | Three tags + 470° bracket, melt 2:47–2:54, second angle at 2:40 |
| 2:54.8–3:05 | Red "WEAK BORDERS" joints on "zero joints" (shows the problem, not the fix) | not fixed | 1-2-3 trick row, then the seamless single-crystal blade |
| 3:05.3–3:20.6 | No spoon / brick wall; cube reused; "CREEP" 5 s early | not fixed | Spoon → brick wall macro; "CREEP" at 3:19.5 |
| 3:21–3:36.3 | No vacuum furnace | not fixed | 5 s furnace withdrawal / grain selector |
| 3:36.7–3:47.5 | Wrong clip (creep bar) on "the blade is hollow" | regression | B6 cooling channels from 3:36.7 |
| 3:49–8:30 | No picture | — | Re-assemble |
| letterbox | Bars on at 0:59–1:03 and 2:23–2:54 only | not fixed | Remove or apply everywhere |

**Voice fact flag (2:16, line 17):** "throwing a **forty-ton** fighter past the speed of sound". A Tejas Mk1A is about
13.5 t at maximum take-off weight; no `claims.csv` row backs it. Remove "forty-ton" or re-record the line.

## 4. 15 highest-value fixes (ranked)
1. Re-assemble the whole film; duration gate before upload.
2. Hangar opener 0:07.8–0:20.2 on real HAL Nashik footage (DD India); R1 only for the walk to the exhaust, and only with a real Tejas shape.
3. Truly empty exhaust tunnel 0:28–0:33.1.
4. Blow 2:10.5–2:18.3: nozzle plume, then the PIB Tejas afterburner; settle "forty-ton".
5. Opening frame 0:00–0:07 (lit, no band, date and place sharp).
6. Thermometer numbers 2:39–2:54 and the melt.
7. Engine readouts 1:37–2:06.
8. Real GE F404 at 0:36–0:41 and 5:49–5:57.
9. "Zero joints" and vacuum-furnace shots.
10. Smartphone and inferno 0:59–1:11.
11. Engine Club markers; China centred before the word (1:12, 5:05, 8:03).
12. "Back to those thirty silent jets" 5:26.7 on the real Nashik line.
13. MiG-21 retiring ~5:38–5:43: IAF final-flight footage.
14. Ghatak ~7:20: DRDO flying-wing footage.
15. Ending 8:14.7–8:30.6: Tejas in flight, blade push, on-screen question, 3–4 s end card with channel name and logo, fade.

## 5. Pacing
Drags: 0:08–0:25, 2:10.5–2:18.3, 2:23.5–2:54.5, 3:37–3:47.5. Rushes: 1:03.5–1:07.5. Holds needed: "Not one.", "Nothing.",
"Directly behind the fire.", the 470° gap. Real footage was only ~5% of the first 3:49 (target 25–30%).
Keep: Chandrayaan-3 footage, DELIVERED 0 and 14 OF 99 labels, dusk apron, **R2 engine journey and chips**, hero blade,
element tiles, cooling x-ray, thermometer layout, the blueprint-orange wireframe look.

## 6. A real walk-around
Shoot the walk-around from real HAL Nashik footage with CG only where no camera can go: open on the real Mk1A line, cut
two or three real line shots under the labels, a real low tracking shot to the back, then match-cut into a clean CG
tunnel that is truly empty. Every exit from CG lands on something real (F404 at 14 of 99, Tejas afterburner on "speed of
sound", MiG-21's last flight on "retiring", DRDO flying wing on "Ghatak"). One lens language: low, slow, 35 mm-feel
tracking, shallow depth, warm practical lights, no letterbox switching. Return to the hangar in the middle and at the end.
