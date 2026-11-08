---
name: deliver
description: Hand a finished cut to the phone-only owner - Drive links, contact sheet, SRT, thumbnails, click-to-copy title and description with chapters, metadata.json, the release schedule and a plain-words report. Use when a review cut or the final master is ready.
---

# Deliver to the owner

Rules: `CLAUDE.md` and PLAYBOOK §4 (package), §14 (render and deliver), §15 (release).

1. **Video to Drive:** `scripts/upload_gdrive.sh --sub <folder> <file>…`, where `<folder>` is `English/<slug>`
   (inside `Creator/`; playlist films too). The master and a 720p copy. Needs `GDRIVE_RCLONE_TOKEN`;
   if it is missing, say so plainly and stop.
2. **Files with `SendUserFile`:** contact sheet(s), `review.md` or `review_ack_rN.md`, the SRT.
3. **The YouTube package (final films):** in `projects/<slug>/youtube/`:
   - thumbnails: a main and two challengers, 1280×720 JPG, built from the concept locked in `plan.md` (PLAYBOOK §4.5);
     challengers vary the picture and words, never the promise; re-run the promise check (§5.1) on all three;
   - `metadata.json`: the locked title + 2 alternatives, description, chapters, playlist, schedule slot, spelling tags, the pinned
     source comment;
   - the title (under 45 characters, no suffix) and the description (2–4 lines, chapters from `00:00`, no links) also
     pasted in the chat as click-to-copy code blocks. Chapter times come from the exact file uploaded.
4. **Release plan in the reply:** the slot (Sunday 11:30 AM IST, or Thursday 6:30 PM IST), "upload now and schedule",
   "Altered or synthetic content = Yes", add to the "Built on Bharat | The Industrial Backbone" playlist, pin the source
   comment within 60 s, no self-views, read Studio at 24 h.
5. **Report in plain words:** what changed since the last cut, what is illustrative, any rights or Content ID risk, and
   what you need from the owner.
6. **Close-out:** commit (no large media), push, PR to `main`, merge, name the branch to delete, archive the session.
   Once the owner approves a cut, stop editing it.
