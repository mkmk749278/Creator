# Handoff · matsya-6000 (2026-11-09)

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
- **Waiting for the owner to approve the audio** (listen for Isro, Matsya, Noh-teel, Raju Ramesh, Jatinder Pal Singh).

## Next session, in order
1. If the owner flags a line: change the text if needed, regenerate only that block (`eleven_tts.py --only N`),
   re-join, re-check, resend. Once approved: `vo_lock.py`, `vo_timing.py` → `vo/timing.json`, captions with
   "Nautile" and "1,00,000 tonnes".
2. Footage: the owner runs the Termux line and the Cowork request (`footage_requests.md`).
3. Blender hero shots H1–H4 (plan §7, §8a), then Remotion.
