# Media sourcing brief: breath-hold documentary v2

Several sessions run in parallel, one per topic. Stay inside your own folder
`video/breathhold/_media/<topic>/` and push only to the branch you were given.

v1 is all motion graphics (`runs/breath-hold/deliver/contact_sheet.jpg`). v2 adds **real photos and video**
over or beside those graphics. Read `runs/breath-hold/deliver/edit_cue_sheet.md` for the scene list
with video times and `runs/breath-hold/research/facts.md` for the facts.

## Licences: hard rules
- Allowed: **Public domain, CC0, CC BY**. Also allowed: **CC BY-SA** (mark `"share_alike": true`).
- **Not allowed:** NC or ND licences, "all rights reserved", stock-site watermarks, news-channel footage,
  film trailers or stills (Street Fighter, Capcom, Paramount, Legendary), Instagram or YouTube downloads,
  and anything whose licence you cannot read on the file page.
- No AI-generated images of real people. No images from other YouTube creators.
- Sources that work from this container: Wikimedia Commons (API: `https://commons.wikimedia.org/w/api.php`,
  read `extmetadata` via `prop=imageinfo&iiprop=url|size|extmetadata`), archive.org (check the item's licence),
  Library of Congress, Wellcome Collection, NIH/NASA (public domain). Pexels and Pixabay are blocked (no API keys).
- Verify each file's licence on its own page. Never infer it from the search result.

## What to deliver
1. Files in `video/breathhold/_media/<topic>/`:
   - Images: JPEG q90, longest side ≤ 2400 px, at least 1200 px wide. Never crop away the subject.
     Keep the original colours: no filters.
   - Video: MP4 H.264, 1920×1080 (pad or scale, never stretch), 30 fps, **no audio track**, trimmed to the
     best 5–20 s, ≤ 15 MB each.
   - Filenames: `<nn>_<short-slug>.jpg|mp4`.
2. `video/breathhold/_media/<topic>/manifest.json`: an array with, for every file:
   `file, kind (photo|video|illustration), title, what_it_shows (one line, honest), source_page, file_url,
   author, licence, licence_url, attribution (ready-to-print credit line), share_alike, width, height,
   duration_s (video), year (if known), suggested_scenes (scene ids from the cue sheet), notes`.
3. `video/breathhold/_media/<topic>/contact.jpg`: one tiled contact sheet of everything, for a phone check.
4. Your total stays under 60 MB. Aim for 8–20 strong items, not 50 weak ones.

## Honesty rules (these go on screen)
- `what_it_shows` must be literally true. A photo of Vidyut at a 2017 film launch is **not** the 2026 event.
  Write "Vidyut Jammwal at the Commando 2 trailer launch, 2017".
- A painting or illustration is an illustration; say so. A different person's freediving is not a record attempt
  unless the source says it is.

## Done
Commit with a clear message and push to your branch. Your final message: what you found, what you could
not find, the total size, and any licence doubts. Under 150 words.
