---
name: deliver
description: Hand a finished or preview cut to the phone-only owner - upload links, contact sheet, SRT, YouTube description with credits, and a plain-words report. Use when a preview or final video is ready.
---

# Deliver to the owner

1. **Video:** `scripts/upload_gofile.sh <file>` for the master and a 720p copy (needs `gofile.io` and `*.gofile.io`
   allowlisted in the environment's network settings). If upload is blocked, say so plainly and offer the alternatives
   (GitHub Actions artifact from a render workflow, or Google Drive via the connector).
2. **Files with `SendUserFile`** (30 MB cap): contact sheet(s), `review.md`, SRT, `description.md`.
3. **Description:** title options, the summary, chapters, safety lines where relevant, and full credits from the manifest
   (`credits.py`), with disputed figures noted ("as reported; other reports say ...").
4. **Report in plain words:** what changed since the last cut, what is still a stand-in or illustrative, rights or Content
   ID risks (fan reels with music, third-party clips), and what you need from the owner. No jargon.
5. **Commit** sources, EDL, manifests, claims, transcripts, SRT and description to `main`; large media stay out of git.
6. Once the owner approves a cut, stop editing it: deliver exactly that cut (upscale, captions only).
