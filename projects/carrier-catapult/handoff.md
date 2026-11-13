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
- **Waiting for the owner:** a listen to the four new paragraphs. **Next:** contact sheets and
  `media_manifest.csv` for r1 and r2; the Blender heroes H1, H3, H4; stock via the Pixabay API; the Remotion build.
