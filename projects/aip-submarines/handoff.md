# Handoff · aip-submarines (2026-11-06, end of session; weekly limit)

Branch `ccr-cc92ffe7-fv5thg`, PR #76 (open; nothing on it is red). Everything below is committed and pushed.

## Where the film stands (PLAYBOOK §3 steps)
- Steps 1–6 done: topic, research, plan, facts (43 claims, gate passes), narration and audio **approved by the owner**.
  The audio is locked: `vo/lock.json` (SHA-256), `vo/timing.json` (184 sentences, 4.5 s outro).
- Step 7 footage: done from the Termux fetches (`footage_log.md`, `media/clips.tsv`). The **Cowork request B is still
  unanswered** (PIB/DRDO prototype photos, thyssenkrupp footage, Pexels list, ISPR Hangor clip). The film works
  without them; they would upgrade the drawn beats.
- Steps 8–10 done: the picture is built in Remotion (`remotion/`), and the four Blender hero shots (H1a/b/c, H3, H4)
  are rendered. The mix is in Drive `mix/mix.wav` (bed 23 dB under the voice).
- Step 11: three own-review rounds (`review.md`). Step 12: one independent review (`review_viewer_r1.md`); its
  fixes are applied (`review_ack_r1.md`).
- **In flight:** round-4 720p render `aip_review_r4_720p.mp4` (remotion-render run dispatched about 18:15 UTC on
  the branch). It lands in Drive `Built-on-Bharat/aip-submarines/renders/`.

## Next session, in order
1. Check the round-4 run (GitHub MCP `actions_list` on `remotion-render.yml`). If a shard hung on apt, cancel and
   `rerun_failed_jobs`. Pull the cut: `/tmp`-style rclone (see `scripts/upload_gdrive.sh` for the config) or
   `scripts/gdrive_pull.sh Built-on-Bharat/aip-submarines/renders <dir>`.
2. Measure it (ebur128, blackdetect) and check frames at 0:12, 2:58, 4:38, 6:45, 7:08, 7:30–7:50, 8:12.
3. Send the owner the r4 Drive link (it is private) and a summary of `review_ack_r1.md`. **Trash
   `renders/aip_review_r3_720p.mp4`**: it is shared "anyone with the link" for the independent reviewer, and
   trashing it kills the link (the Drive connector cannot remove a permission; tell the owner first).
4. Run the independent review again on r4 with the **new real-audience panel** (`prompts/audience_review_v1.md`).
   The r4 file must be link-shared for it (ask the owner, as for r3). Then `review_ack_r2.md`.
5. **The owner approves the cut** → render the 4K master once (`scale` 2, name `aip_master_4k.mp4`).
6. Step 14 (title, thumbnail, description) only when the owner asks.

## Open items needing the owner
- Extra pauses after "twenty twenty-one" and "turned down" (independent review #8): these change the approved audio.
- A horizontal P-8I clip would replace the vertical Navy short (review #4); a Termux fetch, if they want it.
- The Cowork request B (above).

## Local-only things that a new container will not have
- `assets/` (footage, clips, maps, hero clips, renders) and the `.venv-blender` / `.venv-geo` virtual environments.
  The clips, maps and hero clips are all in Drive `render-media/`; the raw footage is in Drive `footage/`. Blender
  hero frames are in workflow artifacts (90 days) if a hero shot must be re-encoded.
