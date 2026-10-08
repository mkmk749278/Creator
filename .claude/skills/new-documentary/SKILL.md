---
name: new-documentary
description: Start a new narrated documentary or explainer for Be Practical with Kishore from a script, topic or voiceover. Use when the owner sends a script, VO file or topic for a new video. Runs the whole pipeline in order (project setup, genre, fact-check, sourcing, EDL, scenes, render, review, delivery) and decides what to split across parallel sessions.
---

# New documentary

Rules live in `CLAUDE.md` and `docs/PLAYBOOK.md` Part B; this is the order of work. Work at `high`/`xhigh` effort; never
skip a step to save time (PLAYBOOK §4). Stop and report to the owner at each **[report]**.

1. **Project.** `projects/<slug>/` with `script.md` (owner's text verbatim), `voice/` (VO files), `README.md`
   (one paragraph + rebuild commands). Work on `main`.
2. **Genre and look.** Pick the genre row in PLAYBOOK §5.3; write palette, media stack and accents into the README.
3. **Timing.** `projects/<slug>/script.tsv` (one spoken line per row, `te<TAB>en`) →
   `python3 scripts/align_script.py voice/<vo>.mp3 script.tsv --out align`; listen to the lines `align.md` flags. Never
   Whisper (PLAYBOOK §7). No script → ask the owner for it.
4. **Fact-check.** Run `/fact-check` in a fresh subagent at `max` effort → `claims.csv`; `python3 scripts/claims_check.py`
   must pass before anything goes on screen. **[report]** disputed/claim rows and any script fix needed.
5. **Beats.** Split the script into beats of 2.5–4 s of picture each; for each beat write the literal visual (semantic lock),
   the kind (real footage / animated scene / moving still), and LIVE / diegetic / VO_PAUSE breaks.
6. **Sourcing.** `/source-media` (one session only) → `asset-manifest.md`, `media_manifest.csv`, contact sheets.
   Prefer the shared library (`python3 scripts/library.py list`) and `video/lib/` scenes before new work.
   **[report]** contact sheet + what is still a stand-in + what the owner must fetch (YouTube clips → Fetch media workflow).
7. **EDL.** `edl.csv` + `edl.md`: timecode → asset → motion → overlay → text → sound cues; every stand-in `+illus`.
8. **Animated scenes.** One folder per scene under `video/<slug>/<scene>/` (copy from `video/lib/` when one fits), realism
   recipe PLAYBOOK §9, lint → check → snapshot → look → fix. Over ~3 scenes or a film over 5 min → `/parallel-render`.
9. **Assemble + review.** Render the 1080p cut; `/review-cut` (sheets + Opus, PLAYBOOK §14) until it passes; fix; repeat.
   **[report]** preview link + contact sheet + `review.md`.
10. **Final.** After the owner approves: native 4K for animated scenes, final mix (−14 LUFS), SRT, description with
    credits (`credits.py`), then `/deliver`. Never edit an approved cut.
11. **Lessons.** Add what went wrong or right to PLAYBOOK §15, with the reason, in the same commit.
