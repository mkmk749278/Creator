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

## Next session, in order
1. The owner's listen to the music reel (`music/matsya_music_reel.mp3`): swap any cue with a voice; then add the
   kept takes to `config/music_library.csv`.
2. Close `word_map.md`'s "Still to get" (Alvin photo, water temperature at 6,000 m, F08's sphere, PIB's caption).
3. Remotion: copy `projects/aip-submarines/remotion` (4.0.534) as the start, scenes from `word_map.md`, hero clips
   placed at their sentence starts, the dive window dip, pushes on the slow holds; then step 8 onward.
