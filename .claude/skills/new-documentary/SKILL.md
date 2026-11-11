---
name: new-documentary
description: Make a weekly documentary for Be Practical with Kishore from a roadmap topic or the owner's idea - topic, deep research (what everyone says vs what it is, our edge), the plan (owner approves), facts, narration (owner approves), ElevenLabs audio (owner approves), footage via Termux and Cowork, word-by-word sync, GitHub renders, sound, the 720p cut, independent viewer review, the 4K master. Stops for the owner at each approval.
---

# New documentary

Rules: `CLAUDE.md`. Each step in full: `docs/PLAYBOOK.md` §3. Work at `high`/`xhigh` effort (`max` for facts and
reviews). Every step has a creative question and a creative output; never stop at the obvious answer (the method:
PLAYBOOK §5.2: name the obvious, diverge by kind, the swap test, choose for the viewer). Send the owner only finished
work.

1. **Topic** → `brief.md`: the machine, the paradox, who it's for.
2. **Deep research** → `research/landscape.md`: what everyone says (news, the 3–5 strongest films and their comments,
   officials), what it actually is (primary documents, draft `claims.csv`), **our edge in one sentence**, what real
   pictures exist, and **the story bank** (15+ sourced moments, people, objects and senses, numbers that can become
   things, ironies, failures). No edge: change the angle. Thin bank: research more.
3. **The plan** → `plan.md`: 3+ angles; **the promise locked at the top** (one sentence, title + 2 alternatives,
   thumbnail concept; PLAYBOOK §3 step 3, §4); 3+ cold opens / endings that differ in kind and deliver it; **the
   creative spine** (the one image, the motif and its returns, the feeling curve, a device per chapter, the retell
   line; PLAYBOOK §5.2); the viewers' real questions; the beat sheet (time, question, turn, picture idea, sound,
   music); 2–3 signature moments and a set piece per chapter; the hero 3D shots; what was cut (zero sodhi).
   Independent plan review (a new session, no repo; PLAYBOOK §13.3) → fixes. **[owner approves the plan]**
4. **Facts:** `/fact-check` on everything the plan claims; `scripts/claims_check.py` passes.
5. **Narration** → `vo.txt`: **the opening (0:00–0:45) first, through the promise check** (PLAYBOOK §5.1: sentence 1
   confirms the thumbnail), then the rest; the creative pass (PLAYBOOK §6.5, its table in `narration.md`), lean-in test, `spoken_english_check.py`, new terms in
   `config/pronunciation.csv`, independent narration review → `narration.md` sent with SendUserFile.
   **[owner approves the narration]** In parallel from plan approval: footage requests (step 7) and Blender hero
   shots on GitHub.
6. **Audio** (never before the opening is verified and the narration approved): `vo_blocks.py` → `eleven_tts.py`
   (config/voice.yaml), as few takes as possible (one under 10,000 characters; PLAYBOOK §6.6), `vo_take_check.py`, join,
   upload to Drive and send. **[owner approves the audio]** Then `align_script.py` → `vo/timing.json`.
7. **Footage** (`/source-media`): Termux line for YouTube, Cowork request for anything blocked (PLAYBOOK §11.3), all
   into the film's Drive folder; contact sheets; `media_manifest.csv`.
8. **Word-by-word sync** (PLAYBOOK §9.5, §9.10): `word_map.md` (sentence → base shot and its idea level → word
   cutaways; every chapter's turn and payoff at level 2 or 3 before building), scene docs, Remotion
   compositions, Blender shots; stills at every cut and word; shot-word and sentence audits.
9. **Render** (`/parallel-render`): GitHub Actions, at most 6 runners at once.
10. **Music and sound** (PLAYBOOK §12), mix to −14 LUFS.
11. **720p cut:** `/review-cut` until a round finds nothing; upload to Drive.
12. **Independent viewer review** (PLAYBOOK §13.3) → fixes → `review_ack_rN.md`. **[owner approves the cut]**
13. **4K master** once → Drive.
14. **Finished package when the owner asks** (`/deliver`): thumbnails from the locked concept, the locked title,
    description.
After each film: change the playbook rule each lesson belongs to, with its reason.
