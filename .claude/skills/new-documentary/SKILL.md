---
name: new-documentary
description: Make a weekly documentary for Be Practical with Kishore from a roadmap topic or the owner's idea - topic, deep research (what everyone says vs what it is, our edge), the plan (owner approves), facts, narration (owner approves), ElevenLabs audio (owner approves), footage via Termux and Cowork, word-by-word sync, GitHub renders, sound, the 720p cut, independent viewer review, the 4K master. Stops for the owner at each approval.
---

# New documentary

Rules: `CLAUDE.md`. Each step in full: `docs/PLAYBOOK.md` §3. Work at `high`/`xhigh` effort (`max` for facts and
reviews). Every step has a creative question; never stop at the obvious answer. Send the owner only finished work.

1. **Topic** → `brief.md`: the machine, the paradox, who it's for.
2. **Deep research** → `research/landscape.md`: what everyone says (news, the 3–5 strongest films and their comments,
   officials), what it actually is (primary documents, draft `claims.csv`), **our edge in one sentence**, what real
   pictures exist. No edge: change the angle.
3. **The plan** → `plan.md`: 3+ angles / cold opens / endings, the viewers' real questions, the beat sheet (time,
   question, turn, picture, sound, music), 2–3 signature moments, the hero 3D shots, what was cut (zero sodhi).
   Independent plan review (a new session, no repo; PLAYBOOK §13.3) → fixes. **[owner approves the plan]**
4. **Facts:** `/fact-check` on everything the plan claims; `scripts/claims_check.py` passes.
5. **Narration** → `vo.txt`: creative pass, lean-in test, `spoken_english_check.py`, new terms in
   `config/pronunciation.csv`, independent narration review → `narration.md` sent with SendUserFile.
   **[owner approves the narration]** In parallel from plan approval: footage requests (step 7) and Blender hero
   shots on GitHub.
6. **Audio:** `vo_blocks.py` → `eleven_tts.py` (config/voice.yaml), one take per block, `vo_take_check.py`, join,
   upload to Drive and send. **[owner approves the audio]** Then `align_script.py` → `vo/timing.json`.
7. **Footage** (`/source-media`): Termux line for YouTube, Cowork request for anything blocked (PLAYBOOK §11.3), all
   into the film's Drive folder; contact sheets; `media_manifest.csv`.
8. **Word-by-word sync** (PLAYBOOK §9.5): `word_map.md` (sentence → base shot → word cutaways), scene docs, Remotion
   compositions, Blender shots; stills at every cut and word; shot-word and sentence audits.
9. **Render** (`/parallel-render`): GitHub Actions, at most 6 runners at once.
10. **Music and sound** (PLAYBOOK §12), mix to −14 LUFS.
11. **720p cut:** `/review-cut` until a round finds nothing; upload to Drive.
12. **Independent viewer review** (PLAYBOOK §13.3) → fixes → `review_ack_rN.md`. **[owner approves the cut]**
13. **4K master** once → Drive.
14. **Title, thumbnail, description when the owner asks** (`/deliver`).
After each film: change the playbook rule each lesson belongs to, with its reason.
