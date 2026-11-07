# Handoff · aip-submarines (2026-11-06, evening)

Branch `ccr-235edd1d-ezbsf6` (PR #76 merged earlier today). Everything below is committed and pushed.

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
- Round 4 (`aip_review_r4_720p.mp4`, in Drive) measured and checked: `review.md` § Round 4. Three holds (5:46, 7:46),
  the Defence Secretary quote layout (4:37) and the clipped map credit are fixed in the source.
- Round 5 (`aip_review_r5_720p.mp4`, Drive id `1HdilW6WE8ZxPn0esWTVM4z9-vezR1AhP`) measured and checked
  (`review.md` § Round 5) and sent to the owner. Asked: trash r3 (kills its public link) and link-share r5 for the
  independent reviewer.

## Next session, in order
1. Read the owner's answers on trashing r3 and sharing r5. Trash r1–r4 once they agree (the Drive connector can trash
   but cannot remove a permission).
2. Pull r5 if needed: `scripts/gdrive_pull.sh Built-on-Bharat/aip-submarines/renders <dir>`.
3. Run the independent review again on r5 with the **new real-audience panel** (`prompts/audience_review_v1.md`).
   The r5 file must be link-shared for it (ask the owner, as for r3). Then `review_ack_r2.md`.
4. **The owner approves the cut** → render the 4K master once (`scale` 2, name `aip_master_4k.mp4`).
5. Step 14 (title, thumbnail, description) only when the owner asks.

## Open items needing the owner
- Extra pauses after "twenty twenty-one" and "turned down" (independent review #8): these change the approved audio.
- A horizontal P-8I clip would replace the vertical Navy short (review #4); a Termux fetch, if they want it.
- The Cowork request B (above).

## Local-only things that a new container will not have
- `assets/` (footage, clips, maps, hero clips, renders) and the `.venv-blender` / `.venv-geo` virtual environments.
  The clips, maps and hero clips are all in Drive `render-media/`; the raw footage is in Drive `footage/`. Blender
  hero frames are in workflow artifacts (90 days) if a hero shot must be re-encoded.
