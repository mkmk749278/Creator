# Review: pharma-apis preview 1 (11:19, 2026-10-28)

Cut: `projects/pharma-apis/assets/out/pharma_apis_preview.mp4` (1080p, 12 Mb/s, −14.1 LUFS, peak −1.1 dBFS).
Method: 340 frames every 2 s on 38 timecoded sheets, read tile by tile against the VO (`vo_times.txt`), plus
`freezedetect` (n=0.002, 1.5 s) and a shot-length listing from the EDL engine. Checklist: PLAYBOOK §14.

## Blockers (fixed, re-render pending)

| # | Issue | Where | Fix |
|---|---|---|---|
| B1 | Overlays and captions crossing a part seam stayed on screen for the whole next part ("Cooked" chip over part 3, gauge over part 4, a caption over part 5) | p3, p4, p5 | Caught by `hyperframes check` before the render: seam slivers dropped, short windows squeeze both fades (`pha.js`) |
| B2 | Identifiable real people under the roll call: the ABP Majha clip turns into a workers' press meet (a named man at microphones) from 0:20 of the source; STOPPED stamps landed on their faces | 3:59–4:01, 6:41–6:59 | Every Y04 shot now stays inside 0:06–0:19 of the source (the HAL building and its sign) |
| B3 | Third-party burned-in text over our captions and reveal: Lyfius "PENICILLIN G PROJECT" title card, "SPRAWLING 135-ACRE SITE" and "+60 MW POWER PLANT" boxes | 1:25–1:33, 7:57–8:05, 9:13–9:17, 9:29–9:31 | In-points moved to clean stretches (0:32, 0:48, 0:64, 0:80); remaining Lyfius shots use the high crop (origin 50% 8%) that hides the lower boxes |

## Major (fixed)

| # | Issue | Where | Fix |
|---|---|---|---|
| M1 | Long holds: 79 shots, 8.6 s on average, up to 23.6 s on one stock clip (microscope, 1:40–2:03), 21 s on one news clip, 15–17 s on gazette pages. Rule: a visual reset every 3.5–5 s | whole film | `split_long()` in `make_film.py`: any hold over 4.6 s becomes near-equal pieces, each cutting to a new framing (punch-ins for footage, reading down the page for documents, x-shifts for cropped news). 153 shots, 4.4 s on average; animated scenes stay whole |
| M2 | Still frames: the exploded tablet sat still for 2.1–3.4 s at a time; the end card for 11.7 s | 2:15–2:29, 10:58–11:19 | Tablet split with centred punch-ins; end card gets a slow push |
| M3 | Semantic: the India map showed today's plants (Kakinada, Nakkapalli) over "picture your grandparents' India… a young, poor country" | 4:06–4:12 | The map cuts away before the Kakinada pin; the HAL building (Pimpri) carries the line |
| M4 | The map's "SAME STATE · ANDHRA PRADESH" label sat under the captions | 9:37–9:46 | Label moved up (y 980 → 860), scene re-rendered |
| M5 | Top ticker of the Marathi news clip (पिंपरी-चिंचवड) visible | Y04 shots | Crop centred (origin 50% 50%) hides both the top ticker and the bottom banner |

## Minor (logged, not changed)

- Generic stock carries a few abstract lines: the microscope for H.I.V. prices and 1991, the port for China's drug parks,
  lab vials for paracetamol. All are moving, labelled PIXABAY, within the two-use limit, and the on-screen numbers carry
  the meaning; better real footage for Cipla 2001 would raise these beats (owner Termux fetch, next film or a v2).
- The import map at 2:51 already shows Kakinada while the VO talks about imports (a deliberate foreshadow of minute eight).
- The tanks scene opens on an almost empty frame for about a second (5:19).

## Checks that passed

- Lede: the export ban (the thumbnail's 86% world) is on screen by 0:37; the minute-eight promise lands at 7:56.8.
- Numbers on screen match the VO and claims.csv: 86 of 100 rupees, ₹65,000 crore, ₹2.5 lakh crore+, $10,000 → $1 a day,
  41 ingredients, ₹6,940 crore, ₹2,500 crore (company figure), 15,000 tonnes, ₹2,216/kg, Jan 2027, ₹5,000 crore+.
- Honesty labels: ILLUSTRATION on every animated scene, ILLUSTRATIVE FOOTAGE on the 2020 street, ILLUSTRATIVE on the cost
  bars; every third-party shot tagged with its source.
- Channel named only at the end; logo bug throughout; no slide-like frames; captions readable on every sheet.
- Audio: −14.1 LUFS integrated, peak −1.1 dBFS; bed silent before the four reveals (by construction, `make_sound.py`).

## Next

Re-render all five parts (every part changed with the splits), re-run sheets and freezedetect, then deliver.

## Pending for the next review round (batched; owner, 2026-10-29: one 720p cut per round, 4K after finalising)

1. **Restore the narration the take trim cut off** (about 13 s; PLAYBOOK §15): the last sentence of blocks 1, 4, 5, 6 and 8,
   "Jai Hind" included. Fixed trim in `tools/align_blocks.py`; re-run it, then `make_film.py` and `make_sound.py`
   (film 11:32, Kakinada at about 8:06), check with `scripts/vo_take_check.py`, render at 720p.
2. Weak stock beats, if better footage arrives: the microscope under the 2001 H.I.V. prices and 1991, the port under
   China's drug parks.
3. Then the owner's review notes on preview 3.

## Round 2 (owner's review of preview 3, 2026-10-29) → v4, 720p

Done:
- Narration restored: the trim had cut the last sentence off blocks 1, 4, 5, 6 and 8 ("Jai Hind" included). Film 11:32,
  Kakinada at 8:06 (still "around minute eight"). `vo_take_check.py` passes.
- Maps: the import route lands on India as a whole (no city); Kakinada appears first at the reveal (8:06) and after.
- Cipla cards in one unit: $10,400 / year (Western price) and $350 / year (Cipla · under $1 a day) [MSF, 7 Feb 2001; P14, P15].
- Raw chemical named: para-aminophenol (P25). Anti-dumping line adds "On Lyfius Pharma's application" (DGTR, 28 Sep 2026).
- "One germ = lost batch": the broth turns murky with a low warning sting (ILLUSTRATION).
- De-duplication: exports on a different port clip (29021); China's plants and "would you build a plant here?" on factory
  chimneys (199788); "others join in" on an Indian QC lab (262464); anti-dumping on a night terminal (23759); roll call on
  still gears (212000/212001); "young, poor country" on the Wellcome penicillin production drawing (L0032175). HAL wall
  now 3 uses (3:33, 3:54 where the VO names it, 5:55); blister machine 3 uses; port aerials 4 (two clips, twice each).
- Chakki clips stabilised (vidstab); the burned phone number on Y05 stays cropped out.

Not done, and why:
- "Medecines" typo at 10:44: not in our captions (the text reads "Medicines"); the review misread it.
- MIP math ($13.50 China price, $25 Indian break-even): no source found; facts only from sources. ₹2,216/kg stays.
- "Qule Pharma (Aurobindo unit)": the Aurobindo link is not sourced; only the Lyfius application is shown.
- Airport freighter at 8:27: the VO there says "waiting at the port", so it stays a port shot (semantic lock).
- 1080p60 / 4K export: review cuts are 720p; 4K once the owner finalises (owner, 2026-10-29).

Round 2 creative pass (owner, 2026-10-29: "use your creativity everywhere"):
- The fermenter is now a living week: sugar streams in and is eaten, spores sprout glowing tips and branch, colonies
  spread and the broth clouds, the mould releases golden penicillin until the broth is gold, a 6x magnifier on one hyphal
  tip, MOULD / PENICILLIN meters (ILLUSTRATIVE), day and night on the steel, a slow push in. Same scene, saffron, for the
  Kakinada twin.
- 2001 price drop: 104 notes of $100 collapse to 3½, timed to the $350 card (replaces 15 s of microscope stock).
- Minimum import price: a border gate; containers under ₹2,216/kg stopped ("LICENCE NEEDED"), dearer ones pass; the
  amoxicillin (₹2,733) and 6-APA (₹3,405) lanes open on "the same rule covers…" (container prices ILLUSTRATIVE; floors
  from DGFT Notification 56/2025-26). Thuds and clicks on the gate, a whoosh as the notes fly.

### v4 720p review (2026-10-29)
11:32, 1280x720, −14.1 LUFS, peak −1.1 dBFS; 346 frames on 39 sheets (`runs/pharma-apis/qa4`). Freezes: 4, all ≤ 3.3 s.
Minor, for the next round: the Cipla scene holds ~3 s after the notes fly (2:01); the tanks scene opens on a near-still
1.6 s (5:23); the "one germ" murk lands on the Day 7 gold broth (4:57), not on a growing culture.
