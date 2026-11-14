# Handoff · carrier-catapult

## Session 1 (2026-11-12): started
- Owner: "Start the catapult film" (roadmap #3). Step 1 (`brief.md`) and a first pass of step 2
  (`research/landscape.md`, draft `claims.csv` with 21 rows, all `draft`).
- **The roadmap title needs care:** "can't build" is not a sourced fact. India has a 400 kg demonstrator, no approved
  catapult carrier, and a US offer since 2017. The film tells what is missing.
- **What the research found that changes the film:** the Rafale M (a catapult jet) landed on Vikrant's ramp on
  29 Oct 2026; the US was ordered on 13 Aug 2026 to plan a return to steam; China commissioned Fujian on 5 Nov 2025;
  India ran a steam catapult from 1961 and removed it in 1987-89.
- **Next, in order:** the open research list in `research/landscape.md` §7 (primary documents, the ski-jump penalty
  as a number, comments on the strongest films, search terms, picture sources); then the plan (`plan.md`: angles,
  the locked promise with title and thumbnail concept, the creative spine, the beat sheet), the independent plan
  review, and the owner's approval. Nothing is written for narration yet.

## Session 2 (2026-11-12): research finished, plan v2 written and reviewed; waiting for the owner
- **Research second pass** (`research/landscape.md` §8, `research/search_terms.md`, claims C22 to C34): the 1971
  boiler story holds (Hiranandani via two sources; Cdr Benoy Roy Chowdhury, steel bands, Vir Chakra); the Rafale M
  also took off from Vikrant; no official ski-jump payload number exists; no decision yet on the US steam plan or on
  IAC-2 (searched 12 Nov); comments read on the strongest films; the objection ledger is final.
- **`plan.md` v2** after the independent review (`review_plan_v1.md`, 7.5 → "9 with the changes"; its three
  calculation corrections were right and are in). Proposed lock: title "India Had a Catapult in 1961. Why Not Now?",
  thumbnail "HAD ONE. 1961." (the Rafale at Vikrant's ramp, a glowing band in the deck that stops at the ramp).
- **`footage_requests.md`:** one Cowork request for the primary documents the cloud cannot reach.
- **Waiting for the owner:** approval of the plan with its title and thumbnail concept; the Cowork document request.
- **Next after approval:** step 4, the fact-check at max effort (`plan.md` §9, 15 items; every row in `claims.csv`
  is still `draft`); then the opening and the promise check; footage requests and the Blender heroes (H1, H3, H4)
  start the same day.
- **Owner, 2026-11-12: plan v2 approved**, with the title "India Had a Catapult in 1961. Why Not Now?" and the
  main thumbnail words "HAD ONE. 1961." ("NO CATAPULT" is the challenger). The promise is locked in `plan.md`.
  The owner has the Cowork document request and the first Termux footage line (`footage_requests.md`).
- **Next:** step 4, the fact-check at max effort; then the opening (0:00-0:45) and the promise check.

## Session 3 (2026-11-12): fact-check done
- The owner ran the Termux line (5 of 6 clips in Drive `footage/`; the deck-sound clip failed) and Cowork (DOT&E
  FY2025, the White House memo, the Vikrant history page, Naval News, the NWC paper, DRDO clippings and Technology
  Focus; not reachable: Hiranandani's volumes, TPCR 2025, the 1995 paper, the Vir Chakra citation).
- **Step 4 done:** `claims.csv` rewritten, 39 rows, gate passes (24 confirmed, 13 as reported, 2 our calculation).
  What it changed is in `plan.md` §8a (the energy store, six days not a week, 1989, China's land catapults, DRDO said
  as reported, no Sea Hawk count, no "first" for the Vir Chakra).
- **Next:** step 5: the opening (0:00-0:45) and the promise check, then the full narration with the creative pass,
  `spoken_english_check.py`, the independent narration review, and `narration.md` to the owner. In parallel: the
  Blender heroes H1, H3, H4 and the second footage request (ramp launches, Sea Hawks, the Aero India demonstrator).

## Session 4 (2026-11-13): narration v2 written and reviewed; waiting for the owner
- `vo.txt` (the recording text) and `narration.md` (v2, with the promise check, the creative pass and the review's
  changes); `review_narration_v1.md`; `words.txt` (subject words for the lint); new rows in `claims.csv` and
  `config/pronunciation.csv`. Both gates pass.
- 10,273 characters, so two takes, split at "Has anyone made it work?" (chapter 4).
- **Waiting for the owner:** approval of `narration.md`. No audio before that.
- **Next after approval:** `vo_blocks.py` with the split, `eleven_tts.py` (check the credit balance first),
  `vo_take_check.py`, `vo_rejoin.py`, the joined MP3 to Drive and to the owner. In parallel: the Blender heroes
  (H1, H3, H4) and the second footage request.

## Session 5 (2026-11-13): outside review applied; still waiting for the owner
- The owner attached an outside review "for refinement only". Its physics matches C22 and C23. Taken: the count in
  three blocks of its own (real-time pause, no edit of the take), "Bilu" respelt "Beeloo" in `vo.txt` and
  `config/pronunciation.csv`, TV-first notes for S1, the power spike and S3 in `plan.md`. Not taken, with reasons, in
  `narration.md`. Both gates pass (10,282 characters, still two takes split at chapter 4).
- **Owner, 2026-11-13: narration approved** ("max 10000 characters in one block, split where a natural split happens").
- **Audio:** two takes (Akash, Eleven v4, Creative 0.0, 50%, MP3 192 kbps), split at chapter 4 ("Has anyone made it
  work?"): `vo_blocks.md` built with `--limit 6127` (blocks 6,127 and 4,148 characters). No re-takes. Credit before:
  19,005 left; the API billed 4,521. Joined with `vo_rejoin.py`, gap 1.25 s at the chapter break, room tone −73 dB.
  Then 0.25 s of the take's own pause (−77 dB) added before "Three." so the count runs evenly (onsets 0.95 s and 0.99 s
  apart; PLAYBOOK §6.6 allows lengthening pauses with room tone; no word touched). **642.98 s (10:43)**, review MP3
  −16.7 LUFS, −1.6 dBTP (two-pass linear loudnorm).
- `align/` (script.tsv 212 sentences, align.json, sentences.json): 206 high confidence; the 6 flagged are short punch
  lines ("No.", "So steam is gone.", Nanda's two lines). `vo_take_check.py`: OK.
- Drive `Creator/English/carrier-catapult/vo/`: `cat_vo_full.mp3`, `cat_vo_full.wav`, both takes with their `.txt`.

## Session 5, continued (2026-11-13): audio approved and locked
- **Owner, 2026-11-13: "Audio aproved".** Locked with `vo_lock.py` on `cat_vo_full.mp3` (SHA-256 892915fe…,
  642.98 s, 60 fps, 4 s outro): `vo/timing.json` (212 sentences, 1,877 words, 7 chapters), `vo/captions.en.srt` (real
  forms from `vo/caption_forms.tsv`: Bilu, INS, USS, DRDO, dates, km/h, ₹ with Indian grouping), `vo/lock.json`.
  The two flagged sentences ("One.", "No.") sit where the first alignment put them; nothing set by hand.
  Render copy `vo_full.wav` (48 kHz) in Drive `English/carrier-catapult/vo/`.
- Chapters (description): 00:00 Rafale on INS Vikrant without a catapult · 00:50 Why INS Vikrant has a ski-jump
  ramp · 01:59 India's 1961 steam catapult and the 1971 war · 04:41 How an electric catapult (EMALS) works · 06:25
  China's Fujian vs America's USS Ford · 07:48 DRDO's electric catapult demonstrator · 09:32 What India needs next.
- **Second footage request** (`footage_requests.md` r2): one Termux line, nine clips (Sea Hawks and Alizés on the
  first Vikrant, 1971 east, the Rafale M Goa ski-jump, MiG-29Ks and a trap landing on Vikrant, the first EMALS launch,
  Ford launches, Fujian's KJ-600), and one Cowork request for stills (DRDO's demonstrator, the first Vikrant at
  Belfast, Cdr Roy Chowdhury's photo). The owner ran both (Antigravity in place of Cowork), 2026-11-13.
- **`word_map.md` written** on the locked timing: every sentence group with its base, its word cutaways and its idea
  level; the slot motif's five returns; S1, S2, S3 and a set piece per chapter; labels; the stock list.
- **Next:** the Blender heroes H1, H3, H4 (`scripts/blender/catapult_hero.py`, rendered by `blender-render.yml`);
  stock via the Pixabay API; contact sheets and `media_manifest.csv` once r2 lands; then the Remotion build.

## Session 5, continued (2026-11-13): footage in; the lorry corrected; audio r2
- **In Drive:** all nine r2 clips (`footage/01_…` to `09_…`, `fetched.csv`); stills from Antigravity in
  `footage/cowork/stills/`: Cdr Roy Chowdhury's official portrait and the Vir Chakra handover (PIB, usable with
  credit); two IWM Sea Hawk photos under IWM's non-commercial licence (H4 reference only, never in the film).
  Not found: the Belfast commissioning photo; any DRDO launcher photo.
- **Fact corrected:** Antigravity found DRDO showed a *railgun* trailer at Aero India 2025. Checked: Janes
  (14 Feb 2025) and DRDO's clippings (NPC15to17Feb2025) show only a railgun model; the "EMLS on a trailer" rests on
  one idrw post. C33 rewritten; the four lorry lines now say "a small test model" (C32, as reported).
- **Owner: "Only record what needed, adjust that in audio".** Four paragraphs re-recorded (314 credits billed)
  and placed into the approved audio at their paragraph pauses, levels matched (≤1.1 dB), pauses kept;
  `vo_take_check.py` OK; re-locked: **644.15 s, SHA-256 f416a57d…**, 211 sentences. Drive `vo/r2/`. The old
  lock's audio is still in `vo/`. New lines at 0:29.7, 7:55.5, 9:23.5, 10:18.5.
- `word_map.md` retimed to r2 (old S156 removed; later ids −1) and its rows point at what exists. PLAYBOOK: two
  lessons (paragraph re-records; "shown at" needs the event's own coverage).
- **The owner sent an outside audio audit of r2 (all four edits pass, levels within ~1 dB):** r2 accepted.
- **Footage vetted** (contact sheets in the gitignored `assets/footage/sheets/`), spans and verdicts in
  `media_manifest.csv`. Key finds: the Navy's landing full-frame in India Today's clip at 10.0–14.5 s (crop the logo):
  the first frame; real Indian Sea Hawks on the first Vikrant (roundel, IN157, a launch off the bow at 1.0–2.5 s, the
  nose-wheel match-cut frame at 8–9.5 s); the real EMALS trough at Lakehurst (10–19 s); a clean Ford launch (1–9 s).
  Rejected: the "Goa" compilation (its Rafale shots are animation; S7 is a map pin now), the PM's vertical clip except
  7–9 s, IWM photos (non-commercial).
- **Stock:** Pixabay API: ceiling fan, coil winding, steam, an Indian city road (Drive `footage/stock-pixabay/`).
  Request r3 in `footage_requests.md` (Pexels, for the laptop): flyover end, cooker, family under the fan, meter,
  lattu, kirana balance, Indian engineers. **With the owner.**

## Session 5, continued (2026-11-13): hero shots rendering
- `scripts/blender/catapult_hero.py`: **H3 store** (the motor generator spins up, copper glows, the energy runs out
  at 600), **H4 catapult** (1961 cutaway: the piston fires on steam, the shuttle drags the jet), **H4 drum** (cracks
  glow, three steel bands ratchet tight at 420/560/700), **H4 room** (the gauge needle swings into the red and holds,
  the camera pulls back through the empty boiler room). Test stills checked by eye at each fix.
- **H1 dropped** (tried and judged crude): the deck moments now use the Navy's own footage (TRAP, LAND, LAND-NDTV);
  the flat-to-ramp morph and the hull cutaway become Remotion drawings (R) on the drafting table. `word_map.md` updated.
- **Rendering on GitHub (owner, 2026-11-13: "all 20 runners are free")**: blender-render runs 21 store (6 shards),
  22 drum (6), 23 catapult (4), 24 room (4); 1920x1080, 24 samples, every 2nd frame; about 54 s a frame on a runner,
  so about 75 minutes. A check-in is scheduled to collect, check and upload them to Drive `renders/`.
- **Next:** collect the renders; the Remotion build (word map scenes, R drawings: the deck plan, the balance, the
  radar circles, the side-elevation morph, the hull cutaway, the working of the 19 units, the engine bars, the DOT&E
  bars, the 17 m vs 90 m pull-back, India maps on the official boundary); then music and sound; the 720p review cut.
- **Hero renders done (2026-11-13):** all 20 shards succeeded; frames checked (counts, no dark frames, contact
  sheets); encoded at 60 fps (every 2nd frame held) to Drive `renders/`: `cat_H_store.mp4` (16 s), `cat_H_drum.mp4`
  (16 s), `cat_H_catapult.mp4` (10 s), `cat_H_room.mp4` (10 s). Logged in `media_manifest.csv`. The 16-bit frames
  stay in the gitignored `assets/renders/` (not in Drive: 7.7 GB). A shard takes about 2.3 h on a runner (not 75 min).
- **Next:** the Remotion build (word map scenes and the R drawings), then music and sound, the 720p review cut.

## Session 5, continued (2026-11-13): the Remotion build
- `remotion/` (Remotion 4.0.534, comp `Catapult`, 648.15 s with the 4 s end card), built from Matsya's skeleton:
  `scenes/p1_open_ch2.tsx`, `p2_ch3_ch4.tsx`, `p3_ch5_end.tsx` (every shot and tag on its word from `vo/timing.json`),
  `parts/drawings.tsx` (the deck plan and slot, meter, ramp side, radar circles, cooker, steam split, the 1961
  elevation, the hull cutaway, the fan unrolled, the working, two meters, engine bars, land track, DOT&E bars, the
  document pose, 17 m vs 100 m, China/India, the two ships, the honest sum, three slots, dates, ramp or catapult),
  `parts/SeaMap.tsx` (India's official boundary). Credits and honesty tags are drawn outside the reframing.
  Test stills checked; fixed: SVG glow on horizontal lines (filterUnits userSpaceOnUse), cut-off credits, overlaps.
- `media/clips.tsx` → 41 clips by `tools/prep_clips.py` (Drive `render-media/` before the GitHub render).
- Photos: the "portrait" from Antigravity is a memorial graphic with captions not in claims.csv: only the face and
  the medal are cropped and used (`roy_face.jpg`, `vrc_medal.jpg`).
- Sound: `sound/score.json` (12 library tracks along the feeling curve; no music under the landing and the count),
  `sound/sfx.json` (the three-second motif: whine, thump, wind; steam hiss and clang for 1961; the bands);
  `scripts/score_mix.py` gained whine, thump, wind, steam_hiss, clang, whistle. Mix: −14.0 LUFS, −1.4 dBTP, in Drive
  `mix/`. `vo-render/` holds lock.json and vo_full.wav.
- **Next:** finish the clips, sync `render-media/`, render the 720p review cut on GitHub, our own review
  (`review-cut`), then the independent viewer review.

## Session 5, continued (2026-11-13): the review cuts
- r1 (run 43399044281), r2 (43404314348), r3 (43407401810): measured and read against the words each time; every
  fix in `review/review.md`. r3: no freezes, −14.0 LUFS, −1.4 dBTP. One overlap left in r3 ("FAR SHORT" over the
  181 label, 7:16), fixed in code for the next render.
- **Owner, 2026-11-13: share r3 for the independent viewer review.** r3 shared "anyone with the link" (Drive file
  17N1kR999AlaYPqynqS9aPBANWBG4Rggg). Review session `session_019NnLekPrc9ecvtsWJk5rj8` (no repo); its answer →
  `review/review_viewer_r3.md`, then fixes, `review_ack_r1.md`, the owner's approval of the cut, the 4K master.

## Session 5, end (2026-11-14): viewer review collected → handoff (owner: "after collecting review, prepare handoff
## and merge work; we open a new session later")
- **The independent viewer review of r3 is in:** `review/review_viewer_r3.md` (verdict: not ready; publishable after
  its fixes 1–5; scores 7–9; peak at the boiler/Bilu/1971 stretch; drifts at the repeated flywheel/Ford shots, the
  document cards, and the end).
- **State:** composition on `main` = r3 + one fix ("FAR SHORT" moved clear of the 181 label). Audio locked
  (`vo/lock.json`, f416a57d…), mix in Drive `mix/` (−14 LUFS). Clips in Drive `render-media/` (37) and in the
  gitignored `assets/media/` of this session only. Cuts: Drive `renders/carrier-catapult_review_r{1,2,3}_720p.mp4`;
  **r3 is shared "anyone with the link"** (file 17N1kR999AlaYPqynqS9aPBANWBG4Rggg): unshare it once the review round
  is closed.

### Next session: start here
1. **Pull the media first:** `scripts/gdrive_pull.sh English/carrier-catapult/render-media projects/carrier-catapult/assets/media`
   and `.../vo-render` → `assets/vo`; `cd remotion && npm ci`. Test stills: `npx remotion still` on a bundle (see
   this file's earlier sections); shot list and run-out check: the esbuild snippet in `review/review.md`'s history
   (bundle `src/_shots.ts`, list every shot's start and length; flag clips whose footage is under half the shot).
2. **Check every review point against the composition and a frame before changing anything** (§13.3), then fix and
   write `review/review_ack_r1.md` (FIXED / FIXED NEXT / OPEN / CHECKED with evidence). My first read of its points:
   - **#1 real:** S2's "FIRST VIKRANT · 1961" tag sits on the *new* ship's deck plan (the ramp hatch is drawn).
     Either draw the 1961 ship (flat deck, slot to the bow; `Elevation61` already exists in side view) or change the
     tag (e.g. "INDIA'S FIRST CARRIER HAD ONE · 1961") so it no longer labels this outline.
   - **#2 real:** tags sit at y 760–860 of 1080 (`tag(..., 140, 860, ...)` in the scene files): move every lower-third
     to ≤ 740 and the size up (subtitles take the bottom ~15% for a third of the audience). Also `Label` size.
   - **#3 real (measured):** `sound/score.json` `duck_db` −20 → about −26 and `bed_rms_db` −24 → −28; the stamp at
     S150 and the cue near 6:28 (`w:126:power` impact_low) down 6 dB in `sound/sfx.json`; re-run `score_mix.py`,
     upload `mix/mix.wav`.
   - **#4 real:** `ThreeItems` row runs off the right edge: pull the third item in (x 1560 → 1450) or scale the row.
   - **#5 real:** `Doc` cards: larger (the line in focus big, the rest small), less time each; merge the White House
     and General Atomics cards (S148–150) into one split.
   - **#6:** a Sea Harrier picture needs a licence-clean source (none in hand: search Wikimedia Commons for an
     Indian Navy Sea Harrier, CC BY / PD); animate `Elevation61` (it already seals the slot and lifts the ramp on
     S83: check the frame the reviewer saw).
   - **#7:** the market balance (S24–30): keep the real Indian picture, but cut it to two shorter shots and add the
     ramp drawing's load bar; or replace as suggested.
   - **#8:** repeats: H_store at S120/122/124/135, FORD_launch/FORD_cat ×6, LAND_ramp ×3, H_drum ×4: vary.
   - **#9:** the islands line is a *new fact on screen*: only with a source in `claims.csv`, else skip.
   - **#10:** a 20 s end card means re-locking with `--outro 20` (`vo_lock.py`) and re-mixing (the score's last slot runs
     to `end`); the speed counter from 0 (S106: check, it already counts from 0 on "standing"); blurred fills behind
     the vertical clips (the `Insert` kit already blurs a copy behind: check 1:04 and 4:22).
3. Render r4 (720p, `remotion-render.yml`, 11 runners), our review again, send the owner r4 + `review_ack_r1.md`;
   **the owner approves the cut**, then the 4K master (`scale 2`), then the package when asked.
4. Before upload: the fresh-facts gate (PLAYBOOK §8): the `fresh` rows in `claims.csv` (the next carrier's status,
   the US steam plan, the rupee rate for $1.321 billion).

## Session 6 (2026-11-14): viewer-review fixes → r4
- Every point of `review/review_viewer_r3.md` checked on stills, fixed in code: `review/review_ack_r1.md` (FIXED 1–10,
  islands line not added: no source). New drawings: `RampLoad`, `Cycle45`, `Queue`, `PriceShip`, `DocPair`; `DeckPlan
  oldAt` (the 1961 ship); lower-thirds moved above the subtitle zone in `common.tsx` `tag()`.
- Sea Harrier photo (U.S. Navy, PD) in Drive `render-media/photos/sea_harrier.jpg`, logged.
- End card 20 s: `vo/timing.json` outro 20 (39,849 frames; same as `vo_lock.py --outro 20`). `scripts/score_mix.py`:
  "end" = picture end. New mix in Drive `mix/` (−14.0 LUFS, −1.4 dBTP; voice −15.0 vs bed −35.6 LUFS).
- **r4 dispatched:** run 43578275297 (6 runners) → Drive `renders/carrier-catapult_review_r4_720p.mp4`.
- **Next:** our review of r4 (freeze, loudness, frames at every changed beat), then r4 + `review_ack_r1.md` to the
  owner for approval; unshare r3 (Drive file 17N1kR999AlaYPqynqS9aPBANWBG4Rggg); then the 4K master.
- **r4 (run 43578275297) checked:** −14.0 LUFS, −1.4 dBTP, no black; frames at every changed beat right. Found and
  fixed: the 1961 label touched the old ship's island, the document heads were cut off, the 20 s end card held
  still (freezes from 10:45). **r5** (run 43580873877, Drive `renders/carrier-catapult_review_r5_720p.mp4`, file
  1TceL2huLkdlBnb2eP475N5WbNGitBa4P): −14.0 LUFS, −1.4 dBTP, 11:04, no freezes, no black; the three spots checked.
- **Next:** the owner approves r5 (or asks for changes); then unshare r3 (17N1kR999AlaYPqynqS9aPBANWBG4Rggg), the 4K
  master (`scale 2`, same workflow), the package when asked, the fresh-facts gate within 24 h of upload.
