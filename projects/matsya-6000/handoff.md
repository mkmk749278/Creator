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

## Next session, in order
1. Contact sheets and clean spans for the ten clips and the PIB photos; `media_manifest.csv` rows.
2. The owner runs the Cowork r2 request on the laptop (real files only).
3. Blender hero shots H1–H4 (plan §7, §8a), then Remotion.
