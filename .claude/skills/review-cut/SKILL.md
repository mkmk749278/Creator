---
name: review-cut
description: Review a rendered documentary cut frame by frame against the pre-render checklist (PLAYBOOK §14) using timecoded contact sheets, and write review.md. Use after every render and before showing a cut to the owner.
---

# Review a cut

1. Sheets: `python3 scripts/contact_sheet.py <cut.mp4> --out runs/<slug>/qa --every 2` (use `--every 1` for fast-cut
   sections). For a single scene, also `npx hyperframes snapshot` at its key times.
2. Review at `high` effort or above, against PLAYBOOK §14, with the EDL (`projects/<slug>/edl.md`) open beside the sheets:
   - **In a session:** open every `sheet-NN.jpg` with Read and go tile by tile; check each tile's picture against the VO
     words at that timecode (semantic lock), on-screen numbers vs the VO, labels, logo, stills over 1.5 s, slide-like
     frames, stock repeats, crops, black frames.
   - **In GitHub Actions / with an API key:** `.venv/bin/python -m pipeline.review_cut --sheets runs/<slug>/qa
     --edl projects/<slug>/edl.md --out runs/<slug>/qa` (Opus at `max`, from `config/models.yaml` `cut_review`).
3. Audio can't be judged from stills: check loudness (`ffmpeg -af ebur128`), VO silence under LIVE/diegetic rows, and
   music restarts separately.
4. Write `runs/<slug>/qa/review.md` (issue → timecode/shot ID → fix). Fix every blocker and major issue, re-render the
   affected shots, re-run the review. Nothing goes to the owner with an open blocker.
5. Send the owner the contact sheet(s) and `review.md` with the preview link.
