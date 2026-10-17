---
name: deliver
description: Hand a finished or preview cut to the phone-only owner - upload links, contact sheet, SRT, thumbnail, click-to-copy title and description with chapters and credits, and a plain-words report. Use when a preview or final video is ready.
---

# Deliver to the owner

1. **Video:** `scripts/upload_gdrive.sh --sub <English|Telugu>/<slug> <file>…` for the master and a 720p copy: they land in the owner's
   Google Drive `Creator/<English|Telugu>/<slug>/` folder (owner, 2026-10-13: Drive replaces Gofile). Needs `GDRIVE_RCLONE_TOKEN`
   (one-time phone setup, PLAYBOOK §1). If it is missing, say so plainly, give the setup steps, and fall back to
   `scripts/upload_gofile.sh` for this delivery. Small text files (description, SRT, review) can also go to the
   `Creator/<slug>/` folder with the Google Drive connector.
2. **Files with `SendUserFile`** (30 MB cap): contact sheet(s), `review.md`, SRT, `description.md`.
3. **YouTube package (every final video, PLAYBOOK §13a):** a thumbnail in the channel theme (A and B, 1280×720 JPG,
   `projects/<slug>/youtube/thumb/`); the title in a click-to-copy code block ending `| Be Practical With Kishore`;
   a simple description in a click-to-copy code block with chapter timestamps from `0:00`, safety lines where
   relevant, and full credits from the manifest (`credits.py`), with disputed figures noted ("as reported; other
   reports say ..."). Paste the title and description blocks in the chat reply too.
4. **Report in plain words:** what changed since the last cut, what is still a stand-in or illustrative, rights or Content
   ID risks (fan reels with music, third-party clips), and what you need from the owner. No jargon.
5. **Commit** sources, EDL, manifests, claims, transcripts, SRT, thumbnails and description; large media stay out of git.
   For a final video: push the branch, open a PR to `main`, merge it, tell the owner which branch to delete, and
   archive the session.
6. Once the owner approves a cut, stop editing it: deliver exactly that cut (upscale, captions only).
