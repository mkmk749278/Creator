---
name: new-documentary
description: Start and run a new weekly documentary for Be Practical with Kishore from a roadmap topic, an owner's idea or a script. Runs the whole pipeline in order (brief and package, research, treatment, script, fact-check, audience review, recording, timing, media, scenes, review cut, master, release) and stops to report after each stage.
---

# New documentary

Rules: `CLAUDE.md`. How each stage works: `docs/PLAYBOOK.md` §3 (the pipeline table). Work at `high`/`xhigh` effort;
never skip a check to save time. Stop and report to the owner at each **[report]**; send only finished work.

1. **Brief and package** (§1.1, §4): `projects/<slug>/brief.md` starting from the roadmap's research flags; search words
   in `research/search_terms.md`; title, thumbnail idea and the paradox chosen first. **[report]**
2. **Research** (§8): sources logged as you go in a draft `claims.csv` (URL + verbatim quote). Primary documents for the
   mechanism, one layer deeper than common knowledge.
3. **Treatment** (§5.2): `treatment.md`: 3+ angles, 3+ cold opens, 3+ thumbnail concepts, 2–3 signature moments, the
   art direction, the sound palette. **[report]**
4. **Script** (§5, §6, §7): `vo.txt` + `screenplay.md` with the Q column; new terms added to `config/pronunciation.csv`;
   `scripts/spoken_english_check.py` passes.
5. **Fact-check:** `/fact-check` in a fresh subagent at `max`; `scripts/claims_check.py` passes.
6. **Audience review** (§13.3): a new session with no repo, `prompts/audience_review_v1.md`, lean-in map; fact-safe
   fixes; checks re-run. **[report]** recording blocks in the chat + `vo_blocks.md` + the review summary.
7. **Recording and timing** (§6.6, §6.7): each take passes `scripts/vo_take_check.py`; `align_script.py` →
   `vo/timing.json`; the owner's audio-only pass.
8. **Media** (§11): `/source-media` → `asset-manifest.md`, `media_manifest.csv`, contact sheets; YouTube picks through
   `yt_search.py` and one Termux line for the owner. **[report]** what the owner must fetch.
9. **Scenes** (§9, §10): design references first; a scene handoff doc per scene; Blender hero shots, Three.js and
   Remotion scenes; stills at every cut and word cue, looked at.
10. **Review cut, 720p** (§13, §14): render on GitHub Actions; `/review-cut` until a round finds nothing.
    **[report]** the cut + contact sheet + `review.md`.
11. **Owner review rounds:** collect all notes, one 720p cut per round, `review_ack_rN.md` each round.
12. **Master and release:** after approval, the 4K master once; then `/deliver`.
13. **Lessons:** change the playbook rule the lesson belongs to (with the reason), in the same commit.
