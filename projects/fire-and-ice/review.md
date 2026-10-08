# Fire and Ice: pre-render review (PLAYBOOK §14)

## Cut 1 (2026-10-08, 1080p, 5:33, −14.0 LUFS integrated)
Reviewed from timecoded sheets every 2 s (`runs/fire-and-ice/qa/cut1/`, gitignored) against `edl.md`, plus exact-frame
grabs of every third-party in-point (`qa/raw_check`).

| # | Issue | Where | Fix (cut 2) |
|---|---|---|---|
| 1 | Near-black frames for ~5 s (snowflakes, embers on black) under the "FIRE & ICE" title | 1:31–1:35, P1 L21 | Blizzard plateau → furnace fire with the title |
| 2 | Dark forest shot, Hof tiny in frame, under "how can will control body temperature?" | 1:29, P1 L20 | VICE close-up of Hof's face |
| 3 | Tummo practitioner photo cover-cropped: person cut off at the bottom | 0:39, 2:25 | 1280×720 crop around the person (`tummo_naropa_crop.jpg`) |
| 4 | "ALSO CALLED CHANDALI YOGA" over a city square full of pigeons (wrong in-point) | 1:49, P2 L2 | Himalayan monastery aerial |
| 5 | Reclining Buddha statue under "real biological fact or a trick?" | 2:13, P2 L6 | Real photo: monk walking in Dharamsala |
| 6 | Stock woman meditating (crop top) stands in for the monks starting Tummo | 2:29, P2 L9 | Thermal Tummo breathing scene |
| 7 | Psychedelic CG neuron tunnel: generic filler (§5.1.8) | 3:09, P2 L17 | Dropped; neuron + Tibetan mural share the line |
| 8 | Part 3 opens on a black frame (VICE fade-in) | 3:13 | In-point moved 0.7 s later |
| 9 | Embers on black: near-black | 3:55, P3 L9 | Bright embers (8625) |
| 10 | Missing histology photo fell back to the mitochondria scene, so it appeared twice in 20 s | 4:05, P3 L11 | Brown-fat cell 3D illustration (CC BY-SA, labelled) |
| 11 | Yak in a field under "tell us your opinion in the comments" | 5:11 | Snowy Himalayan valley |
| 12 | P2 L3 second shot was a yak; better: a real Tibetan monk | 1:53 | Photo: monk on the Dharamsala pilgrimage path |
| 13 | Earlier in-point slips caught before render: TV talk-show frame with burned subtitles, a signpost mid-shot, DW's own "WIM HOF" lower-third doubling ours, a kitchen frame before the canal | P1 L3, P3 L1/L3/L10 | In-points corrected from 1 fps sheets |

Checklist status (cut 1): motion ✓ (no still over 1.5 s: every photo has Ken Burns; scenes animate), face + name of Wim Hof
at 1:05 when first named ✓ (the film's subject is a practice, so the monks/Tummo mural appear at 0:34), logo sting on
"welcome to Be Practical" ✓, logo bug ✓, end card ✓ (20 s, end-screen zones, safety line), science animated and
labelled ✓, stock repeats ≤ 2 ✓, credits on all third-party footage ✓, loudness ✓. Open: fact-check (on-screen numbers
in the hypothermia, finger-temperature, endotoxin and map scenes wait for `claims.csv`).

## Cut 2 (2026-10-08): fixes verified
Exact-frame grabs at each fixed timecode (`qa/cut2fix/sheet.jpg`): all 13 fixes in place; no near-black frames left
outside dips; −14.0 LUFS. Still open: on-screen numbers wait for the fact-check (scenes re-render in about a minute each).
