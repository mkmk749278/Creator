---
name: parallel-render
description: Split a documentary's animated scenes and render shards across parallel cloud sessions (each its own 4 vCPU / 16 GB VM) and assemble the result. Use for films over ~5 minutes or with more than ~3 animated scenes, when the owner wants it done faster without lowering quality.
---

# Parallel render

Plan and facts: PLAYBOOK §3. This session is the coordinator (S0).

1. **Lock inputs on `main`** first: script, VO, `claims.csv`, `edl.csv`, `media_manifest.csv`, encode settings in
   `projects/<slug>/parts.json` (`{"width":1920,"height":1080,"fps":30,"codec":"libx264","crf":18,"maxrate":"12M",
   "gop":60,"audio":"aac 48k"}`, or 3840×2160 for the 4K pass). Every shard must use exactly these.
2. **Split** the EDL into blocks of ~2.5 min at dip-to-black points, and list the animated scenes. Assign one folder per
   session: `projects/<slug>/parts/N/`, `video/<slug>/<scene>/`. Sourcing stays in one session (shared IP).
3. **Start sessions** with `create_session` (load the claude-code-remote tools with ToolSearch). Each prompt names: its
   folder and branch (`<slug>-part-N`), the exact EDL rows or scene spec, `parts.json`, "same effort and quality as a
   single session: never lower it", "commit only text outputs; large media go to the URL list / Drive", and the report
   format (what was rendered, duration, any issue). 6–8 sessions maximum: each uses the owner's usage limit.
4. **Watch** with `get_session` / `list_events`; answer their questions; never let your own session idle during long work.
5. **Assemble:** merge each branch into `main` the same day (tell the owner which branches to delete), pull the part
   files, `ffmpeg -f concat -safe 0 -i list.txt -c copy`, then the music bed and ducking over the full length (never per
   part), then `/review-cut`. Archive finished sessions with `archive_session`.
6. Log wall-clock per session and total in PLAYBOOK §15 so the plan's estimates get real numbers.
