# Handoff · aip-submarines (2026-11-09)

## Public, 2026-11-10 (checked 11:07 IST)
- Live and public at 11:00 IST: 9:15, processed, maxres thumbnail (`thumb_a`), our English SRT and the auto track both
  serving, first in "Practical India" (8 films), not in Built on Bharat. Correct.
- **Source comment posted by the API at 11:07 IST** (thread `UgwcbigjM-HqunELm9F4AaABAg`), 7 min after going public
  (the rule is 60 s: next film, post it the minute it goes public). It stays **unpinned**.
- **Owner, 2026-11-10: the pin is a chat comment, not information.** Posted 11:15 IST (`UgwfNWg5RvqFfsSyi6F4AaABAg`,
  text in `metadata.json` `pinned_comment`): the film's question, wait for India's AIP or take the proven German one.
  **Pinning it is a tap for the owner** (no API). Rule in PLAYBOOK §15.1.
- **End screen (Studio only, no API), decided from frames of the cut:** 9:01 → end (13 s). The last 20 s cannot be
  used whole: the film's own subscribe pill sits mid-frame at 8:59–9:00. From 9:01 the frame is dark water,
  "6,000 M DOWN" left of centre, the sphere in the middle, then the logo card at 9:10; the top-left, top-right and
  bottom-left corners stay empty. Elements: **Video "Best for viewer" top-left, Playlist "Practical India" top-right,
  Subscribe bottom-left.** When the Matsya film is public, change the Video element to it: the tease
  ("Next, we go even deeper… a titanium sphere") promises exactly that film.
- Still on the owner: pin, end screen, Test & Compare (`thumb_c`). 24 h Studio read on 11 Nov at 11:00 IST.

## Owner decisions, 2026-11-09 (standing)
- **Claude acts as channel owner and creative director; Kishore gives every approval.**
- **Six-month goal:** subscribers and monetisation. **Viewer:** all curious Indians, equally.
- **After release Claude may:** pin the source comment, swap the thumbnail on low CTR (PLAYBOOK §15.2 rule), reply to
  comments with facts from sources (`claims.csv` only), and edit the title and description from data.
- **Next film:** roadmap order (Matsya 6000, PLAYBOOK §1.1 #2); data may move a topic up.
- **This film:** title "Why India's Submarines Must Surface"; main thumbnail **CUT IN HALF** (`thumb_a.jpg`),
  Test & Compare challenger **CAN'T STAY HIDDEN** (`thumb_c.jpg`) (owner swapped Claude's proposed order).
  Public **Tuesday 10 November 2026, 11:00 AM IST** (owner chose it over the Thursday/Sunday slots).
- The YouTube token now carries `yt-analytics.readonly`, `yt-analytics-monetary.readonly` and `youtube.force-ssl`
  (checked 2026-11-09).

## Release state (2026-11-09)
- Fresh-facts gate done and logged (`review.md` § Fresh-facts gate): every changeable line holds.
- **Uploaded** by `scripts/yt_upload.py`: video **`ZnrLVpCbBqQ`** (4K60 master from Drive), private, `publishAt`
  2026-11-10T05:30:00Z, category Science & Technology, English, **AI use = No** (owner set it in the app, 2026-11-09),
  main thumbnail `thumb_a.jpg`, our SRT as English captions, description with chapters (`youtube/metadata.json`).
- **Still open:**
  1. Analytics API enabled by the owner (2026-11-09); `scripts/yt_audience.py` works. Last 90 days: 130.7k views,
     avg view 3:07 (about 30% of a film), +462/−46 subs. Viewers: India 51% of views, then US, Malaysia, Singapore,
     Canada, UK, Australia (about 38% together, and they watch longer). 78% are 35+ and about 94% men. TV is 37% of views
     and **47% of watch time**; mobile 51% of views. Traffic is almost all browse features (home feed, 90%); search is
     under 1%. Subscribers are under 1% of views. What follows: the home-feed package (title + thumbnail) decides
     everything; TV viewers mean big-screen picture quality pays; the 30% average view is the number to grow.
  2. **Playlists created by the API** (owner asked, 2026-11-09; ids in `config/youtube_playlists.json`). Owner's scope
     the same day: "Built on Bharat | The Industrial Backbone" (`PLbTelSN7Jsrg`) holds only company histories (the
     Tata film; Amul and others later); "Practical India | Hard Truths, Simply Explained" (`PLYqsLgsTPCfg`) holds the
     weekly films, newest first: AIP, AI, medicines, Tejas, rare earths, Kavach, jet engine, chips.
  3. **Test & Compare** (thumb_c as challenger) is Studio-only (no API): the owner sets it in Studio on the desktop site.
  4. **Source comment** at 11:00 IST: post `pinned_comment` from `metadata.json` (the API can post; pinning is a tap in
     the Studio app).
  5. Studio at 24 h (11 Nov, 11:00 IST): impressions > 1,500 and CTR < 2.5% → swap thumbnail (unless Test & Compare
     is running).
  6. Close-out (§15.3): merge this branch to `main`.

## Earlier (2026-11-07)

Branch `ccr-9fa27be6-01wq25` (holds rounds 4–6; not yet merged to `main`). Everything below is committed and pushed.

## Today (2026-11-07)
- An outside review of r5 (owner's PDF) was checked: audio clean, one reviewer error (`review_ack_r2.md`).
- **Subscribe line added** (owner chose option A): "This story isn't over. When Khanderi goes back to sea with its
  new engine, we'll be there. Subscribe, so you're there too." One new ElevenLabs block (`vo/aip_b07.mp3` in Drive),
  levelled −1.8 dB and inserted after "…any headline you'll read." The joined voice is `aip_vo_full_v2.mp3/.wav`
  (549.91 s); The owner approved the r6 cut and this audio on 2026-11-07 (`vo/lock.json`). Earlier sentences moved at most one frame.
- On screen: Khanderi at sea, "INS KHANDERI · BACK TO SEA · WITH AIP", then a subscribe pill (logo, channel name,
  button turns red on "there") over a calm aerial. New mix in Drive `mix/mix.wav` (old one kept as `mix_r5.wav`).
- **P-8I (review r1 #4) fixed**: the owner's Termux fetch brought Boeing's P-8I first-flight film and ANI's INS
  Rajali clip; the vertical Navy short is gone. Sea-from-above now lands on "hours out over the sea".
- Round 6 720p (`aip_review_r6_720p.mp4`) rendered from commit 3a762cf.

## Next session, in order
1. **Done 2026-11-07:** the owner approved r6 and the audio; the 4K master `aip_master_4k.mp4` is in Drive
   `English/aip-submarines/renders/` and checked. The folder moved from `Built-on-Bharat/` (owner); r1–r5 trashed.
2. Step 14 (title, thumbnail, description, `youtube/metadata.json`) only when the owner asks. Leads from the outside
   review: "Cut in two", the hull plug sliding into the gap. Then the fresh-facts gate within 24 h of upload.
   This film predates the promise-first order (owner, 2026-11-08; PLAYBOOK §3), so here it runs backwards: the
   picture is locked, so the title and thumbnail must confirm sentence 1 ("Night. The Arabian Sea. Somewhere under
   these waves, an Indian submarine is running out of battery.") and pass the promise check (§5.1).

## Older notes (2026-11-06)

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
2. Pull r5 if needed: `scripts/gdrive_pull.sh English/aip-submarines/renders <dir>`.
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
