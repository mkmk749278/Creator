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


## Round 3 (owner's 720p audit, 2026-10-29) → 4K master

Fixed: judder (30 fps conform), flash frames (clean spans, frame-snapped cuts), the PM/PLI slide and promo titles
(excluded spans), the Tribune ad (headline crop, date tag corrected to 4 Mar), "5 cases" (now "a handful", as the VO),
bases named on the 1991 and today gauges, Hubei only on the March 2020 line (other China lines are sea lanes to
Nhava Sheva and Chennai), Indian ports (JNPT photos), period labels (TODAY on HAL wall and lab), 1954 on an archive
drawing, 1991 on the Budget speech, 2001 on MSF's report, capsule animation only at open and close, real strips,
the gate labels, Lyfius boxes and logo cropped out, captions held to word end and lifted to 79%, source tags 22 px
at the top right, stamps clear of the logo bug, end card 20 s, Cipla scene moving after the collapse, tablet labels
36 px, tanks and tablet scenes split, the germ on a growing culture. SRT rebuilt in this cut's time.
Checked and not changed: the four "doubled words" (three are transcript errors; the fourth is breath, 8 dB down, a
different spectrum); the India outline (land only, no borders drawn); "+ heat removed" (not in our sources).

### 4K master assembled (2026-10-30)
The round-3 session hit its usage limit after the five native 4K parts finished on Actions (Drive `renders/4k/`), so the
mix was rebuilt in a new session. The owner re-uploaded the eight Akash takes to Drive `English/pharma-apis/Vo/`
(p1–p8.mp3 = `voice/pha_b01–08.mp3`): each matches `align/blocks.json` to the millisecond, and `align_blocks.py`
reproduces `align/` byte for byte, so the timing is unchanged. `film_vo()` + `make_sound.py` + `assemble.sh`
(PARTS_DIR = the 4K parts) → `pharma_apis_4k.mp4`: 11:28.0, 3840x2160 at 30 fps, about 19.7 Mb/s, −14.1 LUFS, peak
−1.1 dBFS. Part lengths match `parts.json` within one frame; full decode has no errors; no black frames; captions and
picture line up across all four joins (contact sheet checked). One freeze over 2 s: 1:50.8–1:53.0 (2.2 s), the $10,400
card holding while the VO reads the price, before the notes collapse. Left as is: fixing it needs a part re-render.

### Owner's note on the 4K master (2026-10-30): the Corona-days shot
"While we are talking about Corona we simply showed public on a road; that might not fit." Right: 0:21–0:29 was a
generic Pixabay market street (px_1643, ILLUSTRATIVE FOOTAGE) that could be any day. Pixabay's COVID clips were a cartoon,
promos with their own text, or not India; the Commons COVID-India photos are all after the lockdown (distancing
stickers, PPE, vaccines), which would contradict "not the lockdown yet". Now the line sits on a dated report: The
Tribune, 4 Mar 2020, "Chemist shops run out of hand sanitizers, face masks in several parts of Delhi-NCR" (PTI copy),
first the headline and date, then a push into its photo of masked buyers at a Delhi chemist counter, under "3 MARCH
2020". The photo is shown as part of the page (its file was re-uploaded by the site in 2024, so it is not claimed as a
3 March picture). Part 1 re-rendered in 4K on Actions; the other four parts are unchanged.
Master rebuilt with the new part 1 (Drive `renders/4k_v2/video_pha_p1.mp4`): 11:28.0, −14.1 LUFS, peak −1.1 dBFS; part 1
decodes clean, no black frames; the only freeze is still the known 2.2 s $10,400 card at 1:50.8. Same Drive link.

## Round 4 (independent 4K audit, 30 Oct 2026, `114d468b-4k-2026-10-30.md`) → next 720p review cut

Measured before fixing (all 20,640 frames of the 4K master):
- **"Judder" = the grain, not the footage.** The footage conform worked (no repeated frames on any stock or promo shot).
  Whole-frame repeats (grain included) came only on our slow animated scenes: `pha.js` stepped the grain 24 times a
  second on the 30 fps timeline, so every 5th frame nothing moved. Fixed: one grain step per frame. The 720p cut of
  29 Oct had the same pattern, so it was never a 4K load problem. (HyperFrames' "sparse keyframes" warning was tested
  and is not the cause.)
- **13 one-frame flashes** of the empty background (the audit found 8): shot times were rounded UP to 3 decimals
  (78.867 for the frame at 78.8667), so on the cut frame the new shot had not started and the old one had ended.
  Fixed: `build/frame_floor.py`, shot start/end floored onto their frames (`make_film.py` uses it).
- The session rebuilt `assets/` from the Drive part tars + raw footage + Pixabay originals, so `make_film.py` runs again;
  four in-points moved by fractions of a second on single-shot stock (re-fetched renditions have other frame rates).

Fixed from the audit:
- 10:30 "It has the factories": a Lyfius worker in a hard hat (the 7:22 clip stood for China); 7:22 tagged ILLUSTRATIVE.
- 0:58 Hubei: China News Service footage of Wuhan, 26 Jan 2020 (CC BY 4.0, Commons): the empty aerial, then the empty
  boulevard on "the whole province was shut down" (no more dead repeat of the 0:29 map). Framed 1.6x: logos out.
- 1% → 86%: hero numbers centre screen ("<1%" for 1991, the same "<1%" on "Remember that one per cent?", then a match
  cut to "86%" on "eighty-six" with the capsule filling and a low thud), bases underneath.
- 5:08 penicillin G → 6-A.P.A. → amoxicillin: `chain` scene, one penam core, the side group snipped and replaced
  (skeletal formulae, ILLUSTRATION). 10:11 lesson: `chain_lesson`, India's last link, China's links before it, the
  joint cracks.
- 7:51 PLI: the Department of Pharmaceuticals press note (9 Dec 2021, "41 products … Rs. 6,940 cr.").
- 9:39 "₹5,000 crore": PSU Watch's report (Rs 5,210 crore till June 2026), not one company's plant.
- 3:12 fever tablet: a thermometer on white tablets (paracetamol is white).
- 3:24 "It did.": 0.6 s of black under the words, then Hindustan Antibiotics' old signboard behind trees today.
- 7:35 the trap: the tanks, steady, "Small plant: can't compete" / "Big plant: big risk", a PRICE WAR stamp (+ sound).
- Fermenter: the day clock only moves forward; the germ beat is a "What if" branch; the Kakinada tank keeps its clock.
- Counters land in under 0.45 s. Safe zones: tank meters moved left, "SAME STATE · ANDHRA PRADESH" large and clear of
  the captions, tablet layers 140 px left (the punched-in pieces clipped "THE REST OF THE TABLET").

Waiting on the owner's phone (YouTube search + Pexels, `scripts/termux_search_to_drive.sh`): Pimpri 1950s, the
grandparents' India, "a cut could kill you", the STOPPED roll call (one real image per name), the 2001 H.I.V. human
beat, an Indian export carton / packing line (0:00), an Indian medicine box (1:19), Indian plants (1:36, 2:32), a
chemical reactor for "cooked" (4:30), a licence-era document (5:58), China's drug parks (6:10, 7:28).

### Round 4 review cut (720p, 30 Oct 2026)
`pharma_apis_720_r4.mp4` on Drive: 11:28.0, 1280x720 at 30 fps, −14.1 LUFS, peak −1.1 dBFS, rendered on Actions
(720p option). All 20,640 frames measured: **0 repeated frames, 0 one-frame flashes** (the 4K master had 406 and 13).
The first 720p attempt still repeated every 3rd frame: the grain used `floor(t * 30)`; `Math.round` fixed it, checked
frame by frame in the browser before the re-render. Holds over 1.6 s: 1:50.7 (2.2 s, the $10,400 card), 1:53.4 (1.7 s),
2:12.6 (1.8 s), 7:33.9 (1.6 s, the tanks building). Next: the archive and plant footage from the owner's phone (YouTube
bot check on the mobile IP; script now paces requests and takes a throwaway account's cookies), then the 4K master.

## Round 5 (30 Oct 2026): final 4K master

Answers the r4 720p review and the owner's two extra reviews item by item in `review_ack_r5.md`. Master:
`pharma_apis_4k.mp4` (Drive `Creator/English/pharma-apis/`), 3840×2160, 30 fps, 11:28.3, 20,650 frames.
Measured: 0 repeats between moving frames, 0 flash frames, 0 freezes over 1.6 s, clean part seams, −14.2 LUFS,
−1.7 dBTP. Owner's audio-only pass still asked for: 0:50.8, 8:21.9, 10:38.3 and the name list in the ack.
