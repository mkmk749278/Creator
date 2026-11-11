# Handoff · matsya-6000 (2026-11-10)

Film 2 of the roadmap (owner, 2026-11-09: roadmap order, data may move a topic up). Steps 2 and 3 done 2026-11-09: research, plan v2 after the independent review (`plan.md`, `review_plan_v1.md`). **The owner approved plan v2 with the title "ISRO's Hardest Weld Isn't for a Rocket" and the thumbnail "6 KM DOWN" (challengers ISRO'S WELD, WHY A BALL?) on 2026-11-09.**

## Done
- `brief.md` (machine, working paradox, viewer), `research/landscape.md` first pass (news to 6 Nov 2026, YouTube
  landscape and comments, draft edge), draft `claims.csv` (M01–M08 + two OUR CALCULATION rows).
- YouTube search sheets and `landscape.json` in `assets/ytsearch/` (gitignored).

## Step 4 and the opening (2026-11-09)
- Fact-check done for the plan's open items: `plan.md` §8a, claims M18–M27. The big change: ISRO's own video shows
  **five titanium pieces joined by seven welds**, not two halves. The 2021 test sphere was mild steel tested to 600 m.
  No public proof test of the titanium ball (the landing says so honestly).
- **The opening (0:00–0:45) is written and passes the promise check and `spoken_english_check.py`**:
  `narration.md`, `vo_opening.txt`, `words.txt`. Owner: English only, no Hindi, as simple as possible.
- ISRO's video (`assets/ref/isro_samudrayaan_230725.webm`, 3:30) is reusable with credit (ISRO copyright policy);
  upload it to Drive `English/matsya-6000/footage/` with the first footage batch.

## Narration (2026-11-09)
- Full narration v2 in `vo.txt` / `narration.md`, after the independent review (`review_narration_v1.md`). Both gates
  pass: `claims_check.py` (39 claims) and `spoken_english_check.py`. **Sent to the owner for approval.**
- Footage requests ready in `footage_requests.md` (Termux line, Cowork list incl. the blocked MoES PDFs).

## Audio (2026-11-09)
- The owner approved narration v2.2 and said proceed. Five ElevenLabs takes (Akash, Eleven v4, Creative 0.0, 50%,
  MP3 192 kbps), one per block, no re-takes: 6,900 characters. Trimmed, joined with 0.8 s gaps:
  `mat_vo_full.wav` (451.1 s, 7:31), review MP3 loudness-normalised to −16 LUFS. All in Drive `English/matsya-6000/vo/`.
- `align_script.py`: 144 lines, 140 high confidence (the 4 flagged are short punch lines). `vo_take_check.py`: OK.
- **The owner approved the audio on 2026-11-10** ("Continue audio approve"). Locked with `vo_lock.py` on
  `mat_vo_full.mp3` (SHA-256 d3dab31f…, 451.16 s): `vo/timing.json` (144 sentences, 1,241 words, 9 chapters, 60 fps,
  4 s outro), `vo/captions.en.srt` (real forms via `vo/caption_forms.tsv`: ISRO, Nautile, 6 km, 1,00,000 tonnes),
  `vo/lock.json`. Seven sentences at 2:53–3:06 (the five pieces) were misplaced by the aligner by one sentence; set by
  hand from the silences in `vo/sentence_fix.tsv`. `vo_full.wav` (48 kHz) in Drive `vo/`.

## Footage (2026-11-10)
- **Termux done:** all ten clips in Drive `footage/` (`fetched.csv`). Two are vertical (02, 10), 03 is 480p and 05 is
  360p: use as small framed inserts only. Contact sheets and clean spans still to do.
- **Cowork not done.** Drive `footage/cowork/` holds only Word files and a list.xlsx written by an AI app
  (Antigravity/Gemini): text summaries, not the PDFs or photos. Its list names ~25 files that do not exist, and some
  details differ from the real sources (e.g. the wet-test dates). **Nothing in `cowork/` is a source; do not cite it.**
  The Gemini Termux script only saved files on the phone (its rclone line was commented out).
- **Fetched from the cloud instead** (PIB static works): PIB's Deep Ocean Mission feature (17 Aug 2025, 9 pages) and
  its photos, plus the three-crew-inside photo, in Drive `footage/pib/`. Its progress card corroborates M-claims: wet
  trials 22 Jan–14 Feb 2025, "first high-penetration weld of 80mm thickness over 7100mm length in just 32 minutes".
- **Still needed (Cowork on the laptop):** the four MoES PDFs (404 from the cloud), NIOT photos (unreachable), PIB
  release pages 2104039 / 2156508 / Nov 2026 trials as PDFs with their photos, IFREMER Nautile photos (check licence:
  NC is not allowed), the USCG Titan report PDF. Re-sent as `footage_requests.md` §B r2.

## Hero renders (2026-11-10)
- **All ten in Drive `renders/`** (1080p, 30 fps clips from step-2 frames; frame count, flash check and contact
  sheet each): H1_dive, H1_cutaway, H1_dark, H2_pieces, H2_seam, H4_squeeze, H3_weights, H3_assemble, H3_seabed,
  H3_descent. Seabed's frames 380-718 were re-rendered (the camera had clipped through the frame at "Outside your
  window") and spliced in; the joins measure 0.57 and 0.47 of brightness.
- `word_map.md` places every sentence's picture on audio r2; its "Still to get" list is open.
- Music: Cowork made 18 Lyria 3.5 takes in Google Flow Music (Drive `music/`, `list.csv`); picks in
  `media_manifest.csv` (M01-M10; grave = library fx09). The reel `music/matsya_music_reel.mp3` waits for the owner's
  listen for voices before the mix.
- Edit notes: dive 7.3–7.8 s, the camera clips through the window (black shards, a red flange slice): cover it with
  a quick dip or blur through the glass in Remotion. Seam's last 6 s and squeeze's last 3 s are slow: add a Remotion
  push. Squeeze crops the top of the ball at the end (a close-up; fine).

## Audio r2: the joins re-cut (2026-11-10, owner asked for refinement from two outside audio reviews)
- The four glitches the review heard were the four take joins, all measured: takes 2-4 ended with a 46-65 ms
  clipped start of the next block's first word; the gaps were exact digital zero; takes 3-5 started at full level.
- Rebuilt from the same five takes with `scripts/vo_rejoin.py` (no new credits, no word changed): bursts cut,
  5 ms fade-ins, room tone at -72 dB in the gaps; gaps 0.923 / 0.8 / 0.8 / 1.25 s (+0.3 s after "Five people
  died", +0.45 s before "Six thousand metres down"; the "Seven welds" and "You and two others" joins sit inside
  rendered hero shots and keep their timing). 452.13 s, -16.6 LUFS. Drive `vo/r2/`; the first join kept in
  `vo/r1_original_join/`.
- Re-locked (`lock.json` 8deb177e…); **the owner approved r2 on 2026-11-10**; six sentences pinned in `sentence_fix.tsv`
  to the old times + 0.3 s. Everything after 95.2 s moved +0.3 s, after 362.6 s +0.75 s: the hero shots keep their
  internal word timing and are placed at their first sentence's new start.
- The owner tested a single take of the whole narration on a free account (2026-11-10): measured clean and even
  (PLAYBOOK §6.6). Matsya keeps r2 (owner's choice, no credits spent); single takes start with film 3. The free take
  is in the container only, not for the film.
- The second review (EQ) is for the mix (step 10): a -1.5 dB dip at 250 Hz (Q 2), a gentle de-esser at about 7 kHz,
  and +1 dB above 12 kHz only if the music is dense. Check each against the music before applying.

## Cowork r2 and footage vetting (2026-11-10)
- **Cowork r2 done with real files** (saved to the laptop's synced `pexels/cowork_dl/` and to Drive
  `footage/cowork/`, with a proper `list.csv`). Vetted: genuine JPG/PNG/PDF, licences as shown.
  - USCG Titan Marine Board report (4 Aug 2025, 335 pages, US government work). Claims M12, M-CALC3, M27, M30 now cite
    it verbatim (executive summary). `claims_check.py` passes (40 claims).
  - IFREMER Nautile photos, **CC BY 4.0** (surface, recovery, inside with three viewports): usable with credit.
  - PIB 2104039 wet-test photos (609 px, Kattupalli jetty, 7 Feb 2025); PIB 2156508 is only press-conference photos.
  - NIOT: small images, no reuse licence shown: design renders of Matsya (Blender reference) and seabed mining
    references only, never on screen. No NIOT photo of the titanium ball, the 2021 steel ball or OMe 6000 exists.
  - Not obtainable: the four MoES PDFs (404 for everyone now; M19, M20 rest on the quoted text; sansad.in has the
    same answers if a re-check is needed), PIB pages as PDF, and a Nov 2026 PIB release (none published).
  - The old `download_cowork_assets.sh.docx` (AI-written) is still in `footage/cowork/`; ignore it.
- **The ten clips vetted** on contact sheets (Drive `footage/sheets/`): keep F01 (DD India, best: hall, ball,
  inspection), F06 (Nautile, square), F08 (Times Now: ball 2023, a black test sphere over the sea, likely 2021: confirm
  before naming it), F03 as a 480p insert. Reject F02, F04, F05, F07, F09 (foreign subs shown as Indian), F10 (AI-looking).
  Clean spans and verdicts in `media_manifest.csv`.
- **Picture gaps** (our animation, labelled): the titanium ball's forging and the seven welds beyond ISRO's video, the
  Nov 2026 unmanned trials (no real footage yet), Matsya at depth, the Titan comparison.

## The edit and the mix (2026-11-11)
- `remotion/` (Remotion 4.0.534, comp `Matsya`, 456.13 s with the 4 s end card): scenes `a1_open_ch1`, `a2_ball_weld`,
  `a3_inside_sea` from `word_map.md`. `Film.tsx` passes each shot its lead (the dissolve frames before its word), so
  word cues and hero clip times are exact. Clips from `media/clips.tsv` via `tools/prep_clips.py` (37); photos and
  the Natural Earth map plate (`scripts/ne_plate.py`, box to about 25 S) in `assets/media/`, synced to Drive
  `render-media/`; `vo-render/` holds `lock.json`.
- Word-map gaps settled: S118 NEAR FREEZING (claim M36, NOAA); S47-49 Alvin drawn (no clean photo licence); S51 the
  2021 sphere drawn (F08 unidentified); S96-98 names as labels over Nautile, no faces.
- Mix: `sound/score.json`, `sfx.json`, `music_manifest.csv`; `scripts/score_mix.py` → `assets/mix/mix.wav`
  (-14.0 LUFS, -1.4 dBTP; music a median 27 dB under the voice), in Drive `mix/`. The music picks still wait for the
  owner's listen; a swapped cue means re-running the mix only.
- 720p review cut r1 dispatched on `remotion-render.yml` (6 runners) → Drive `renders/matsya_review_r1_720p.mp4`.

## Real clips for every idea (owner note on r3, 2026-11-11), in progress
The owner, on r3: "At least you need to show one real clip of everything to feel realistic. Nail, buffalo on it,
titanium etc." And on the fingernail drawing: the buffalo was drawn the same size as the finger. "Even if you draw in
3D that should feel near to reality."
- **Placed on their words (merged; not rendered yet):**
  - real sea under the depth counter (S14–18);
  - a real buffalo, "ABOUT 600 KG" (S21);
  - INS Vagir's hull (S43);
  - Alvin photo (S47);
  - a ship for 2021 (S50–51);
  - TIG welding in air (S67);
  - a gas flame (S69);
  - GEOMAR nodule photos (S119, S123);
  - a phone (S124).
  Shot list in `remotion/src/scenes/*`; clips in `media/clips.tsv` (PX_*, VAG_surf); credits in
  `media_manifest.csv`. All in Drive `render-media/`.
- **Fetched and waiting in Drive `footage/`** (pull with `scripts/gdrive_pull.sh`, vet on contact sheets, cut with
  `tools/prep_clips.py`, add to `clip_durations.json`, upload the clips to `render-media/clips`):
  - `01_z1f9XfdthU0.mp4`, `02_SCHgaumVHis.mp4`: ISRO's PSLV-C49 / C51 liftoff and onboard camera. Use for S6
    "Isro is known for rockets" in place of the rocket outline.
  - `03_5LJtUk8OQ2o.mp4`: NOAA Ocean Exploration deep-sea dive (public domain). Use for S116–117 "no sunlight …
    your lights".
  - `cowork_r2/` (Pexels; `list.csv` has authors and licences):
    - fingers: 9465178, 5870550 ("Finger in a Yellow Background"), 7299380, 7298020;
    - a hand holding a ball: 11923146, 4753306, 11075640;
    - deep dark: 14597114 (underwater cave), 3695383 (dust in the air: not usable).
- **Not usable from Cowork:**
  - The "carbon fiber" results (12911761, 12911888, 12911784, 11965533) are ordinary blue fabric, not carbon fibre.
    Do not use them as carbon fibre; find a real carbon-fibre weave (Pixabay search, or another request), or keep the
    drawing.
  - No real green-screen finger exists on Pexels.
- **The buffalo forced-perspective shot (the owner chose a composite over filming it himself):**
  - a real finger near the lens with a real buffalo far away (Pixabay 34719, a buffalo grazing at a distance), lined
    up so the hoof sits on the nail, at true scale;
  - the finger comes from Pexels 5870550 (plain yellow background: colour-key it in Remotion, or with ffmpeg
    `colorkey`/`chromakey`), or 7299380 / 9465178 if they key better;
  - it replaces the flat cartoon finger (S19–21);
  - "ABOUT 600 KG" lands on "six hundred kilos" (claim M24 / M-CALC1).
- **Other places to bring nearer reality:**
  - S44 "squeeze a ball in your hand" → Pexels 11923146 or 4753306;
  - S19 "hold out your finger" → a real finger clip.
- **Music:**
  - The owner's cue-sheet note (`Claude.md` upload) matches our map of cues to chapters.
  - Added: silence under "Five people died" (new `music_mute` in `score.json` and `scripts/score_mix.py`). The new
    `mix/mix.wav` is in Drive.
  - Level kept at about 25–27 dB under the voice (PLAYBOOK §12, older TV audience).

## r4: the real clips built (2026-11-11, second session)
- **Owner, 2026-11-11: the finger-and-buffalo shot is not that important; make it in code, but near to reality.** So no
  composite. S21 is now `BuffaloTrueScale` (`remotion/src/parts/drawings.tsx`): world units are centimetres (finger
  1.6 cm thick, buffalo about 1.45 m at the shoulder); the camera starts on the fingertip under a front hoof and pulls
  back to the whole animal, a ring on ONE FINGERNAIL, the label DRAWN TO SCALE, the tag OUR CALCULATION.
- Placed on their words: ISRO's PSLV-C51 lift-off as a framed insert (S5–6, replaces the rocket outline); a real hand
  holding out a finger (S19); a real fingernail in macro at half speed with the arrow tracking the nail and the 600 KG
  count (S20); a real hand squeezing a ball (S44, then H4_squeeze from S45); NOAA's dark midwater and lights on marine
  snow (S116–117, ILLUSTRATIVE FOOTAGE; H3_seabed now enters at S118 at its own 7.5 s).
- Six new clips in Drive `render-media/clips`; rows in `clips.tsv`, `clip_durations.json`, `media_manifest.csv`,
  `word_map.md`. `prep_clips.py` at 3 jobs on 4K sources was killed (memory): use `--jobs 2`.
- Not used: the Pexels finger on yellow (painted nail), the tennis-ball and massage clips, the underwater cave, the
  "carbon fibre" fabric clips (not carbon fibre: the drawing stays).
- 720p review cut r4 dispatched on `remotion-render.yml` from branch `ccr-6eb07f72-kfzr83` →
  Drive `renders/matsya_review_r4_720p.mp4`.
- AIP film at 24 h (11 Nov, 11:15 IST): public, 1,012 views, 7 likes, 1 comment (ours). This session's YouTube token
  has no Analytics scope (403), so impressions and CTR must be read in Studio.

## Next session, in order
1. Our full review of r4 (`review/review.md` § r4): measured checks and the changed shots against the audio.
2. Independent viewer review (§13.3): the reviewer needs r4 shared by "anyone with the link". Ask the owner first;
   it was asked for r3 and not yet answered. Then write `review_ack_r1.md` and get the owner's approval of the cut.
3. The owner's listen to the music reel; swap any flagged cue and re-run the mix.
4. Fresh-facts gate before upload: ISRO's July 2025 wording on "successful testing" vs S136 / M26; M05, M33.
5. Ask before trashing r1–r3 in Drive. Keep r3 until r4 is approved.

## Narration v3 (2026-11-11)
- The owner asked for a rewrite after the audience read (PLAYBOOK §1.2, §1.3). `vo_v3.txt` / `narration_v3.md`:
  1,549 words, 8,566 characters, both gates pass (46 claims). **v2 (`vo.txt`, the lock, r1–r3) is untouched.**
- The owner is generating v3 on a free ElevenLabs account to listen (not licensed for the channel).
- If the owner chooses v3: the independent narration review, a paid one-take recording (about 8,600 credits), a new
  lock, and `word_map.md` re-timed; most r3 pictures carry over, the new lines need pictures (Kishore moments, the
  Titan pressure comparison, 15 → 40 kW, Samudra Manthan, the monsoon, the closing line).

## The film rebuilt on narration v3 (2026-11-11, third session)
- **Owner, 2026-11-11:** agreed to all the audience findings, generated v3 himself as one take (uploaded
  `Matsya.mp3`, 543.7 s, mono 128 kbps) and said "Build the full film". **v3 is now `vo.txt`**; v2's text, lock and
  timing are in `vo/v2/`. The take is in Drive `vo/v3/mat_v3_vo_full.mp3`.
- **Open question on the voice file:** the owner said he would generate on a free account. Free-plan audio is not
  licensed for the channel (PLAYBOOK §6.6). Before any upload to YouTube, ask which account made this take; if free,
  a paid take is needed (about 8,600 credits), then a new lock, and the word cues re-checked (pace will differ).
- Lock: `vo_lock.py`, 183 sentences, 1,549 words, 9:04 + 4 s outro; every sentence ratio 0.63–1.37 except the short
  "One pass." (1.6); no repeat or skip signs. Not listened to by a person other than the owner.
- **Shot list re-cut for v3** in `remotion/src/scenes/*` (`word_map.md` is still the v2 map: the scene files are the
  truth until it is rewritten). New: `Ask` speech bubbles for the two Kishore questions, `PressureCompare` (Titan about
  340 bar against 600 bar, OUR CALCULATION, M-CALC6), 15 → 40 kW, the monsoon (PX_storm), Samudra Manthan over a real
  sea (PX_churn), ₹4,077 crore with its source, the saying over H2_seam, the closing name and line on the end card.
  F01_foam is no longer used (a minister stands in frame).
- Sound: `score.json` and `sfx.json` re-mapped to the v3 sentence ids; mix −14.4 LUFS, about −1.2 dBTP, in Drive
  `mix/mix.wav` (the v2 mix kept as `mix/mix_v2_r4.wav`).
- **720p cut dispatched:** run 42975445665 on `remotion-render.yml` from `ccr-52953fd3-sfo7sb` →
  Drive `renders/matsya_review_r5_v3_720p.mp4`.
- **Known weak points to fix after the first look:** the cricket ball is small in frame (S48) and the hand squeezes a
  blue ball (S49); the carbon-fibre drawing is faint (S33–34); the China depth ladder runs 16 s (S155–158); the
  opening still starts on our 3D ball for 4 s before the real one; paradox lands at 0:25–0:30 and the loop ends at
  0:53 (the rule says 0:45).
- **Still to do:** our full review of r5 (measured checks, shot-word audit), the independent narration review of v3
  and the independent viewer review, then the owner's approval of the cut.

## Audio locked (owner, 2026-11-11)
- **"Lock that audio don't make any changes."** The v3 take (`mat_v3_vo_full.mp3`, SHA in `vo/lock.json`) is the
  film's audio. No re-take, no text change, no re-timing. Every fix from here is picture, sound design or mix.
- **No independent narration review for v3** (owner, same message: "No need of independent review at this stage in
  narration"). The independent viewer review of the cut (step 12) still stands unless the owner says otherwise.
- So the opening's timing (paradox at 0:25–0:32, loop to 0:53) stays as it is.
- Still unanswered: which ElevenLabs account made the take. Ask once more before the upload (licence, PLAYBOOK §6.6).

## r6 sent to the owner (2026-11-11)
- `renders/matsya_review_r6_v3_720p.mp4` (9:08, −14.4 LUFS, no freezes) and `renders/matsya_r6_contact_sheet.jpg`.
  Our review: `review/review.md` § r5 and § r6. r5 was not sent (two wrong pictures, fixed in r6).
- **Next:** the owner's notes on r6; the WEAK rows (one Cowork request: a hand gripping a cricket ball, a real
  carbon-fibre weave, an Indian hand holding a phone); the independent viewer review (needs the owner's yes to share
  the cut by link); then the owner's approval, the 4K master, the package. Audio is locked: picture and mix only.

## Session closed by the owner mid-build (2026-11-11, about 09:00 UTC): where things stand
The owner's last notes on r6: "Fix all of them" (the weak shots), "somewhere we are saying sea but the visuals look
like a dark universe with stars", "the audio was generated from a free account: generate it from the API", "should be
like an outstanding film". Then: "Close the session, merge work."

**Done and in the repo / Drive**
- **Paid audio.** One API take of the same v3 text (Akash, Eleven v4, Creative, 50%, MP3 192 kbps; 3,768 credits
  billed; 20,197 left on 2026-11-11). `vo_take_check`-style signs clean: every sentence ratio 0.6–1.45 except the
  short "One pass." (1.58); pace 169–177 words a minute by quarter. A 0.7 s room-tone breath was added at each of the
  8 chapter turns (PLAYBOOK §6.6). **The film's audio is now `mat_v3_api_vo_full.mp3`** (543.32 s; Drive `vo/v3/`,
  with the raw take `mat_v3_api_take1.mp3`); `vo/lock.json`, `vo/timing.json` and the captions are from it.
  **The owner has not heard this take yet: send it for approval before anything else.** The free take stays in Drive
  `vo/v3/mat_v3_vo_full.mp3`; r6 was built on it.
- **Mix for the API voice:** −14.1 LUFS, −1.2 dBTP, Drive `mix/mix.wav` (the r6 mix kept as
  `mix/mix_v3_freetake_r6.wav`).
- **Real water over every 3D deep-sea shot** (`kit.tsx` `SeaOver`, used by `hero()` for H1_dive, H3_descent,
  H3_seabed, H3_weights, H1_dark, H4_squeeze, and by `Deep`): a blue body of water in screen blend, light shafts near
  the surface only, real bubbles (PX_bubbles, Pixabay 31611). The film now opens on the real sea surface
  (PX_surface) with a counter to 6,000 M, then the ball.
- **Weak shots re-cut in code:** the carbon-fibre wall redrawn large and in contrast; the cricket clip pushed in on
  the ball; a warmer phone shot (PX_phone2); "Stay with me" on the real ball; the Titan date over the real sea;
  the China bars cut to 8 s, then the real jetty photo and real nodules for India's answer.

**NOT done: nothing below has been rendered or looked at**
- `tsc` passed before the last edits were finished being checked; **run `npx tsc --noEmit` first**, then one still to
  confirm every word cue resolves on the new timing.
- **The new sea look has not been seen on a single frame.** Render stills of H1_dive, H3_descent, H4_squeeze and
  `Deep` and judge them against the owner's note before any full render. Tune `SeaOver` (tint strength, bubbles
  opacity) or re-render the heroes in Blender with volumetric water if the composite does not read as sea.
- Check the cricket push-in framing (`from={[1.7, 660, -180]}` was computed, not seen) and the new carbon drawing.
- `PX_surface.mp4` was still encoding when the session closed; if it is not in Drive `render-media/clips`, run
  `tools/prep_clips.py projects/matsya-6000 --only PX_surface --jobs 1` and upload it. `clip_durations.json` holds
  10.0 for it as a placeholder: replace with the measured length.
- No render on the API audio yet. After the checks: `remotion-render.yml` → `matsya_review_r7_v3_720p.mp4`
  (if "Film to Drive" sits over 5 minutes, dispatch `join_from`), our review, then the owner.
- Add `media_manifest.csv` rows for the six new Pixabay clips (138694, 205011, 244491, 31611, 304019, 202987).

**Still needs real pictures (Wikimedia Commons rate-limited this session; Pixabay had none)**: one Cowork request for
a hand gripping a cricket ball, a real carbon-fibre weave, an Indian hand holding a phone, a licence-clean photo of
Titan (US Coast Guard) and of China's Fendouzhe.

**Open with the owner:** approval of the API audio; a yes or skip for the independent viewer review; whether the
opening may start on the real sea rather than the thumbnail's ball (the two rules pull apart; write the choice in
`treatment.md`).

## Session 4 (2026-11-11, from the close above)
- `tsc` clean; every word cue resolves on the API timing (stills render). PX_surface is in Drive (9.93 s, now measured).
- **The sea look, judged on stills:** with `SeaOver` the 3D deep-sea shots read as blue water with bubbles and
  shafts near the surface; no frame reads as space any more. Kept as coded.
- **Opening decided (the two rules no longer pull apart):** r6's black water was why the real surface was put first.
  Now that the ball sits in real-looking water, the film opens on the ball sinking (H1_dive from 0 s) with the depth
  counter 0 → 6,000 M, then the real ball on "this titanium ball". First frame = the thumbnail's subject; the
  surface-plus-"6,000 M DOWN" contradiction is gone. PX_surface stays at S30 (the Titan date). The plan's cold open
  (H1, ball in water) is what plays.
- Re-checked on stills: the carbon-fibre drawing reads (large, red split lines); the cricket ball is now big in frame;
  the China bars are short. Still weak: the blue stress ball at S49 and the non-Indian hands on the phone
  (S16, S135): **Cowork r3** in `footage_requests.md` (also Titan and Fendouzhe photos; Commons still 429).
- `media_manifest.csv`: rows for the six Pixabay clips.
- **r7 dispatched:** run 42994622252 → Drive `renders/matsya_review_r7_v3_720p.mp4`.
- **Owner, 2026-11-11: the API audio approved** (`vo/lock.json` approved); Cowork r3 delivered; "All together with
  fixes render directly in 4k", all 20 runners free. So no 720p of these swaps and no independent viewer review
  before the master (the owner's call). r7 (720p, before the Cowork swaps) is in Drive `renders/` for reference.
- **Cowork r3 into the film:** S14 Coast Guard engineers at Titan's recovered end cap; S31 Titan's wreck on the
  seabed (both US Coast Guard, public domain); S16 and S135 real hands on phones (Pexels); S48 a real hand closing
  round a cricket ball, S49 the ball unchanged ("NOTHING HAPPENS"); S155 Fendouzhe, a full-size exhibit model
  (CC BY-SA, labelled), then the depth bars from S156. The blue textile clips are not carbon fibre: not used. The real
  Fendouzhe photo on Commons is portrait only; not used.
- From the r7 check (−14.1 LUFS, −1.2 dBTP, no freezes): ISRO_ti re-cropped to remove ISRO's burned-in "Ti6Al4V" caption and logo; H3_assemble (the rig in a black starry void) now under `SeaOver` too.
- **4K master dispatched** on 20 runners → Drive `renders/matsya_master_4k.mp4`.
- **4K master done:** Drive `renders/matsya_master_4k.mp4` (3840×2160, 60 fps, 9:07, 1.70 GB, md5
  9b8cecf96968cad78aa5bc667ec1015e), from run 43000831768's shards. Its "Film to Drive" hit Drive's shared rclone
  quota (403 rateLimitExceeded, queries per minute) and retried for an hour; the copy did land (same md5 as a join
  made in the session). Checked: −14.1 LUFS, −1.2 dBTP, no freezes, no black, every 6 s frame looked at.
- **Next:** the owner watches the master; then the package (thumbnails from the locked concept, title, description,
  chapters, SRT, metadata.json) when the owner asks; the fresh-facts gate within 24 h of upload.
