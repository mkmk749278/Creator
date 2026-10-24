# Independent cut review: film_v2_4k (session session_012YydojFB1avnX5NudJNBP8, 2026-10-23)

# Independent review: cut v2 of `film_v2_4k_review.mp4` (3840×2160, 8:34.2)

The file does not pass §14 yet. Most of v1's big problems are fixed: the film runs to the end, the R2 readouts are there, the thermometer numbers land, and the walk-around opens on real HAL footage. But I found a visible **"PHOTO SLOT" placeholder**, a burned-in label that contradicts the voice, a wrong-subject photo under "China", and about nine places where old burned-in captions show through or collide with the new labels. Those must be fixed before upload.

**How I checked it**
- **Streams:** video and audio are both 514.200 s, so the duration gate passes. The voice ends at 8:30.2 and the end card runs to 8:34.2.
- **Loudness:** −14.0 LUFS integrated, true peak −1.4 dBFS, loudness range 3.1 LU. All on spec.
- **Frames:** 1,028 frames at 0.5 s steps (which covers every cut), on 29 timecoded sheets with the voice line marked. I looked at every frame, then pulled 27 full-4K frames and 0.1 s bursts at the suspect moments.
- **Real footage share:** 134.9 s of 514.2 s (26%), inside the 25–30% target. Note that 69.5 s of it is stills with a slow pan and zoom.

## 1. Scores for 0:00–0:42

| | /10 | Why |
|---|---|---|
| Story clarity | **8** | The date and "HAL HANGARS · BENGALURU · NASHIK" are sharp by 0:03. "DELIVERED TO THE AIR FORCE: 0", the empty tunnel and "ENGINES SENT 14 OF 99" all land on their words. |
| Visual realism | **6** | The real DD/PIB/MoD shots help a lot. The CG hangar (0:07.8–0:15.1) is near-black and reads as game-engine. The exhaust petals (0:30.5–0:33.6) are flat white with no shading. The PIB taxi at 0:37.6–0:41.8 is soft upscaled SD at 4K. |
| Cinematic quality | **6** | It cuts real → CG → real → CG (0:07.8, 0:15.1, 0:20.7) with a different exposure each time, and there is no single lens language. |
| Feels like a real walk-around | **5** | The CG walk is broken up by four 1–1.6 s real inserts. "Cockpits wired" (0:17.5) is the Army chief **flying** in a Tejas trainer, which contradicts "standing in dead silence, not delivered". You never feel you are walking: you are shown a slideshow, then a dark CG hangar. |

## 2. Blockers (must fix before upload)

1. **7:06.5–7:08.6: "PHOTO SLOT" placeholder text**, centred on an empty slate under "2008 DELINKED FROM TEJAS" (scene C1_empty_bay). This is the worst defect in the cut.
2. **7:54.9–7:55.8: the burned-in "SAFRAN + GTRE · SELECTED AUG 2025" shows bare for about 0.4 s and ghosts for about 1 s.** It sits between the "offer: joint development" and "Rolls-Royce + Reliance" labels. It contradicts the voice ("has offered…", "The decision sits in New Delhi") and the "DECISION PENDING" label. Deeper problem: `claims.csv` JB-089 says the government **picked Safran in August 2025**, so lines 57–58 and the "Decision pending" label may themselves be stale. **The owner needs to decide which is true**, then make the voice and the screen agree.
3. **8:03.6–8:09.2: "CHINA · 30 years to its own fighter engines" is laid over a MoD photo of IAF Su-30MKIs and French Rafales (Exercise Garuda).** It presents Indian and French jets as Chinese. Replace it.
4. **Burned-in labels showing through or colliding with the new overlays.** These are sharp at 4K and look like errors:
   - **1:16.5–1:19.3:** "THE ENGINE CLUB" runs through "40 YEARS / 1986 → 2026".
   - **3:02.5–3:05.3:** "SINGLE CRYSTAL" under "1 · ZERO JOINTS"; it is left alone on screen at 3:05.0.
   - **3:07–3:12:** "MANY CRYSTALS" under "BILLIONS OF CRYSTALS".
   - **3:21.5–3:26:** "SINGLE CRYSTAL" under "IN A VACUUM FURNACE".
   - **4:05.5–4:09.5:** "FILM COOLING" under "1,700 °C FIRE".
   - **5:06–5:10:** the "1986 · GTRE, BENGALURU · PROPOSAL" stamp is half-hidden behind "NOT IN THE DRAWING".
   - **5:10–5:13.6:** "SINGLE CRYSTAL" under "VACUUM METALLURGY".
   - **6:11–6:13:** "F404 SALES STOPPED" under "POKHRAN TESTS → U.S. SANCTIONS".
   - **7:30.0:** "…NE BLADE" pokes out to the right of the D.M.R.L. label.
   - **Fix:** re-render the HyperFrames scenes with their captions switched off. Opaque cover boxes don't work: these scenes fade their captions on their own timing.
5. **7:15.4–7:16.0: the cost headline jumps ₹382 CR → ₹385 CR → ₹411 CR** in the last half second. The D12 counter keeps running past the cut. Trim or freeze it at 7:15.3.
6. **Voice facts.** All of these need one re-record session:
   - **2:16:** "forty-ton fighter" (known).
   - **7:11:** "twenty-one-hundred-crore" against "₹1,996 CR SPENT BY 2012" on screen (known; JB-078 says "about Rs 2,000 crore", so say "two thousand crore").
   - **New, 4:56–5:05:** "jump from idle to supersonic in two seconds" is physically wrong (an engine spools to full power in seconds; the aircraft does not go supersonic). The screen label already says "idle to full power in seconds", so the voice and screen disagree.
   - **New, 5:38:** "The old MiG-twenty-ones are retiring" against "MIG-21 · RETIRED SEP 2025" on screen (JB-057). In an October 2026 film that should be past tense.
7. **3:01.9–3:02.3: a red London-style double-decker bus** appears in the A7 "3 TRICKS" recap. It is a foreign vehicle, it breaks the Indian-places rule, and it spoils the 4:26 bus reveal. Re-render A7 without it.

## 3. On-screen text vs voice: contradictions, timing, clipping, placeholders, leftovers

| Time | Problem |
|---|---|
| 7:06.5–7:08.6 | "PHOTO SLOT" placeholder |
| 7:54.9–7:55.8 | burned-in "SELECTED AUG 2025" against the voice's "decision sits in New Delhi" |
| 8:03.6–8:09.2 | "CHINA" over IAF and French jets |
| 7:14.5 | "₹1,996 CR SPENT BY…" clipped while it types on; then the 382→411 jump (7:15.4–7:16) |
| 7:11.4 on | screen ₹1,996 crore against voice "twenty-one hundred" (known) |
| 4:56–5:02 | label "idle to full power in seconds" against voice "idle to supersonic in two seconds" |
| 5:38–5:43 | "RETIRED SEP 2025" against voice "are retiring" |
| 6:04–6:07 | burned-in "26 September 2025" date on MiG-21 retirement footage under "India has seen this exact movie before" (wrong footage for the line; should be 1998) |
| 1:16.5–1:19.3, 3:02.5–3:05.3, 3:07–3:12, 3:21.5–3:26, 4:05.5–4:09.5, 5:06–5:10, 5:10–5:13.6, 6:11–6:13, 7:30 | double text and leftover captions (see blocker 4) |
| 0:54–0:59, 1:10–1:12, 3:33–3:36.5, 8:19–8:22.5 | burned-in "HIGH-PRESSURE TURBINE BLADE" every time the A3 clip is reused, including over the closing line "forged inside the blade" |
| 8:20.5 | a dark rectangle in the lower left of the blade shot (looks like an empty label box) |
| 7:10.5–7:11.3 | burned-in "TEJAS MK1A · HAL" on a 2008 delinking beat (Mk1A did not exist then) |
| 7:41–7:48 | burned-in "AMCA MK1 · GE F414" shown while the voice talks about the 110 kN engine; the "AMCA MK2 · 110 kN" label arrives at 7:48.3, at the end of the sentence, for 1.8 s (late and short) |
| 5:17.4–5:26 | markers come up USA, Russia, Britain, France; the voice says America, Britain, France, Russia |
| 1:19.0 | China marker arrives only as the line ends |
| 6:01–6:03.5 | four timeline tags (APR 2023 → NOV 2024 → MAR 2025 → FIRST ENGINE MAR 2025) in 2.5 s: unreadable |
| 7:20.6–7:24.7 | the photo is the SWiFT flying-wing demonstrator labelled "Ghatak … (demonstrator)"; say "SWiFT, Ghatak's testbed" |
| 7:24.7–7:36 | "60 single-crystal blades to HAL" over a fighter high-pressure blade; JB-083 says they were for a **helicopter** engine |
| 2:24–2:47, 4:10–4:15 | burned-in heat-map and coating labels (GAS ▸, ALLOY MELTING POINT, +200 °C, METAL; HOT GAS, CERAMIC COATING) are about 30 px tall at 4K: unreadable on a phone |
| 5:46–5:51 | a tiny "83" caption at the bottom left; reads as debris |
| 2:12–2:16 | a faint ghost of the source's own burned-in text along the bottom left of the PIB climb |

Text sharpness: the PIL overlay labels are crisp at native 4K (checked at full resolution). The burned-in HyperFrames captions are visibly softer, being upscaled.

## 4. Status of v1's top 15

| # | v1 fix | v2 status |
|---|---|---|
| 1 | Re-assemble whole film; duration gate | **Fixed.** 514.2 s video and audio; the gate is in `assemble_4k.py` |
| 2 | Hangar opener on real HAL Nashik footage | **Partly.** Real DD India/MoD shots at 0:00–0:07.8 and 0:15.1–0:20.7, but 0:07.8–0:15.1 and 0:20.7–0:33.7 are still dark CG; "Cockpits wired" is the wrong photo |
| 3 | Truly empty exhaust tunnel | **Fixed.** 0:30.5–0:33.6 has an empty black core and holds about 3 s; the petals are crude |
| 4 | Blow: plume, then PIB afterburner; settle "forty-ton" | **Mostly.** Real PIB climb 2:10.5–2:16.5 plus nozzle-glow photo; no CG plume; "forty-ton" still waits on the re-record |
| 5 | Opening frame lit, date and place sharp | **Fixed** |
| 6 | Thermometer numbers and the melt | **Numbers fixed** (1,400 at 2:39.5, 930 at 2:41.5, 470 at 2:44.5). **Melt not fixed:** 2:47–2:54 is a flame surge with no melting blade; a burn hole appears at 2:57.5 under the wrong line |
| 7 | Engine readouts 1:37–2:06 | **Fixed.** Hundreds of kg/s, 30×, 1,700 °C, all on cue |
| 8 | Real GE F404 at 0:36 and 5:49 | **Fixed.** Test-cell photo at 0:33.7, DoD photo at 5:56.5 |
| 9 | "Zero joints" and vacuum-furnace shots | **Not fixed.** 3:02 is a lattice with leftover text; 3:21 says "vacuum furnace" over a lattice; no furnace anywhere |
| 10 | Smartphone and inferno, 0:59–1:11 | **Not fixed.** "Smaller than your smartphone" sits over a wireframe engine; no phone; no flame on the blade (it only reddens at 1:07.5) |
| 11 | Engine Club markers; China centred before the word | **Partly.** Markers now appear, but China arrives late at 1:19, the order is wrong at 5:17, and the China beat at 8:03 is wrong |
| 12 | "Thirty silent jets" on the real Nashik line | **Fixed** (5:26.7), but it is the same clip and in-point as 0:02.4 |
| 13 | MiG-21 retiring on IAF footage | **Fixed** (5:38.2); the voice tense is now the problem |
| 14 | Ghatak on DRDO flying-wing footage | **Mostly.** A MoD photo of SWiFT, a 4 s still; fix the label |
| 15 | Ending | **Mostly.** Tejas in flight, blade, the question card at 8:22.8 and the end card with logo all work. But the blade carries a burned-in label, the PIB climb at 8:14.7 repeats the clip from 2:10.5, and the end card is 7 s with no motion at all |
| — | Letterbox switching | **Not fixed.** Bars appear only on the heat map, 2:23–2:47 |

## 5. The 10 highest-value remaining fixes (ranked)

1. **7:06.5–7:08.6:** replace the PHOTO SLOT with a real 2008-era Kaveri-on-test-bed or LCA-prototype photo. Re-render C1 with the photo, or cut straight from the 7:00 thrust bar to the 7:09 wireframe.
2. **Safran fact (7:50–8:03, voice lines 57–58):** the owner decides "selected August 2025" (JB-089) or "pending". Then re-render D14 with captions off and set one label that matches the voice.
3. **Strip the burned-in captions** from A3, B4, B2, B7, B8, C3/C6, C4, D7, D14 and C9 by re-rendering with captions off. That clears every timecode in blocker 4, plus the "HIGH-PRESSURE TURBINE BLADE" text at 0:54, 3:33 and 8:19.
4. **8:03.6–8:09.2:** replace the Garuda photo with licensed Chinese J-20 footage, or reuse D7 with China centred and "WS-10 · 30 YEARS" on it. Never IAF or French jets under "China".
5. **One voice re-record session:** 2:16 "forty-ton" (remove it); 4:56 "idle to full power in seconds"; 5:38 "have retired"; 7:11 "two thousand crore". Rebuild alignment and subtitles afterwards.
6. **7:15.4:** freeze or trim the D12 counter. **3:01.9:** re-render A7 without the double-decker.
7. **Walk-around 0:07.8–0:33.7:** lift CG exposure by about 1 stop to match the DD footage. Replace 0:17.5 with a cockpit-on-the-line shot (the DD clip around the LA-5046 radome has workers in the cockpit). Shade the exhaust petals. Use one CG camera move with no more than two real inserts, so it plays as one walk.
8. **0:59.5–1:08:** a real phone beside the blade on "smartphone"; a flame washing the blade on "inferno". **2:47–2:54:** a visible blade melt on "turns to water", and move the 2:57.5 burn hole there.
9. **3:21–3:26:** add a vacuum-furnace or grain-selector withdrawal shot (5 s). Cut A3 blade-rise uses from 5 to 2: give 7:24.7 the DMRL photo or a casting shot, and 8:18.4 a fresh hero angle.
10. **Data timing:**
    - 5:17 markers in voice order: America, Britain, France, Russia.
    - 6:01–6:03.5: hold two tags, not four.
    - 7:41: "AMCA MK2 · 110 kN" on the word "one-hundred-and-ten", held 3 s.
    - 7:24.7: "60 blades · helicopter engine · 2021" to match JB-083.

## 6. Pacing

- **Drags:**
  - 2:23–2:47: 24 s of the same yellow and red heat map behind letterbox bars, with tiny unreadable text. Cut a second angle in at 2:33.
  - 4:26–4:33.5: 7.5 s bus still.
  - 6:20–6:32.6: 12.5 s of two stills on "built in-house / own the jet". Cut in real flight footage at 6:26.
  - 4:15.5–4:26: 10.5 s on the RPM disc (the counter helps).
  - 4:45–4:51.5: an ISRO flight-parameters monitor on "we build cryogenic rocket engines". Use the LVM3 lift-off; the 4:51.5 shot is a rocket sitting on the pad on "fires for three minutes".
- **Stills over 4 s:** 4:26 (7.5 s), 6:20 (6.1), 6:26 (6.4), 6:32.6 (4.5), 7:20.6 (4.1), 7:36.3 (4.6), 8:03.6 (5.6), 8:09.2 (5.5).
- **Dead frames:** about 0.5–2.5 s near-black or empty openings at 5:32.0, 5:38.0, 5:43.5, 6:07.0, 6:37.0, 6:41.5, 7:00.0–7:02.5 (an empty axis for 2.5 s) and 7:41.0. Trim the scene heads.
- **Rushes:** 6:01–6:03.5 (timeline tags) and the 1:16.5–1:19.3 globe labels.
- **Works:** 0:20.7–0:25.2 "Not one"; 1:19.5–2:10.5 the R2 engine journey (51 s, but it keeps moving and the chips land); 3:12.5–3:20.6 the creep bar, with "CREEP" now on the word; 3:36.7–4:15 the cooling, air-shield and coating sequence; 5:32–5:52 squadrons and orders; 6:53–7:06 the weight dial and thrust bar; the question card and end card.
- **Repeats** (all real or own footage, so not a stock-rule breach, but noticeable):
  - A3 blade rise: 5 uses.
  - B4 single crystal: 4 uses.
  - PIB Tejas: 4 uses; 2:10.5 and 8:14.7 look identical.
  - DD Nashik clip: 4 uses.
  - LVM3 pad: 2 uses.

Nothing was edited, committed or pushed. Working files are in `/tmp/claude-0/-home-user-Creator/9fca1d80-6a56-5f86-8d7a-a6c3547aa634/scratchpad/` (the contact sheets are in its `sheets` folder).
