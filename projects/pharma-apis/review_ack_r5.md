# pharma-apis: acknowledgement of the r4 review and the owner's two extra reviews (round 5, final)

**For the next reviewer.** This answers three documents item by item:
- **R4**: `Forensic Audit … / 720p review cut r4` (30 Oct)
- **V**: the owner's review "Look at pharma video, deeply review" (verb-to-cut, loop glitch, repeats)
- **F**: the owner's review "Independent forensic review … audio … YouTube Studio API"

The cut to check is the final 4K master `pharma_apis_4k.mp4` (Drive `Creator/English/pharma-apis/`). It runs
**11:28.3**, 0.4 s longer than r4 because of the new pause before "Yes." So **every time after 0:55 is 0.4 s later than
in the r4 cut.** Below, the review's own time comes first and the final cut's time follows (→).

Status key: **FIXED** (in the final master) · **CHECKED** (measured, nothing to change; the evidence is given) ·
**OPEN** (not done; the reason is given).

## 1. Must-fix before 4K (R4 checklist)

| # | Item | Status | What we did / evidence |
|---|---|---|---|
| 1 | 6:51 St Isaac's Cathedral under the roll call | FIXED | Out of the film. The roll call now plays over the real places. The gears go quiet on "went quiet" (6:43 → 6:43.4). Then H.A.'s own wall with its workers protesting "SAVE H.A." (MPC News, 2015) under **Hindustan Antibiotics**. The label now lands on that cut, so there are no unlabelled seconds (also R4 6:48). Then I.D.P.L. Hyderabad's gate (ETV Telangana 2026, logo and ticker framed out) under **I.D.P.L.**, and the gears again for Torrent, Ranbaxy, Sarabhai and Alembic. The manifest row for Pixabay 212000 is corrected: it was logged as "gears". |
| 2 | Flicker chains 1:34, 1:35, 8:09, 10:09 | FIXED | The Lyfius clean spans are split at every one of the promo's own wipes (round-4 code, now rendered). See §6 for the measured result. |
| 2 | Flicker chain 3:29 | FIXED | The black under "It did." now holds right up to the signboard cut. The blister shot no longer shows again for 7 frames between them. |
| 2 | Flicker chain 3:32 (a car through the source's cut) | FIXED | The signboard shot plays two clean ABP spans (10.45 s and 14.25 s). Line 31 (3:36 → 3:36.3) is now Next Generation News's 2015 footage of H.A.'s board and works. |
| 3 | 0:16.8 capsule clip judder | FIXED | It was telecined (24 frames in 30). Conformed with `decimate=cycle=4`: each frame is shown once. |
| 4 | 1:56 ghost "$0" | FIXED | The $350 card appears at its value, on the word. |
| 4 | 2:16 ghost "THE STRIP" | FIXED | The cause was each tablet layer sliding up 300–470 px through the other labels. Each layer now settles 36 px in place. Checked frame by frame: no doubled labels. |
| 4 | 9:40 PSU Watch headline cut off | FIXED | The 2.8:1 headline is padded to 16:9. The whole headline, "Total investment of Rs 5,210 crore … till June 2026: Govt", is in frame for the full shot, push-in included. |
| 5 | Doubled words 0:50.8 "them. them." | FIXED (owner to confirm) | Measured: after "them" (−18 dB) comes a 0.15 s voiced burst at −26 dB. Either a breath or a soft repeat, so the edit lowers it 24 dB. |
| 5 | 8:21.5 "and and" → 8:21.9 | FIXED (owner to confirm) | "and" at −19 dB, then a second 0.3 s burst at −29 to −39 dB, lowered 24 dB the same way. |
| 5 | 10:37.9 "medicines medicines" → 10:38.3 | CHECKED (owner to confirm) | No extra burst: "Keep taking your medicines exactly as your doctor says" runs at normal pace with no gap or repeat in the level profile. Most likely transcript noise. |
| 5 | Pronunciations: Pimpri 3:35, Ranbaxy 4:18, Kakinada 8:06, Aurobindo 8:11, Lyfius 8:12, Nakkapalli 9:49, "six A.P.A." 5:11 | OPEN (owner's ears) | These are the owner's own takes. A bad one is fixed by re-recording that block, never by splicing. Times in this cut are +0.4 s. |

## 2. Clean-ups (R4 table)

| Time | Status | What we did |
|---|---|---|
| 10:14 China amber vs India saffron | FIXED | China's links are now red (#e5484d), India stays saffron, and the crack is white. Easy to tell apart on a phone. |
| 6:48–6:50 gear with no label | FIXED | "Hindustan Antibiotics" lands on the cut to H.A.'s wall. |
| Holds 1:50.7, 1:53.4, 2:12.6, 7:33.9 | FIXED | The Cipla price scene, the tablet scene and the tanks scene now drift slowly (1.02→1.06 scale) instead of holding still. |

## 3. Should (R4)

| Item | Status | What we did |
|---|---|---|
| 4:30 reactor | FIXED | A new animated batch reactor (`cooked`), drawn from real Indian plant footage, under "cooked from chemicals". |
| 6:43 roll call real footage | FIXED | See §1, item 1. |
| 1:42 TAC 2001 | FIXED | AP Archive, Pretoria High Court, 18 Apr 2001: H.I.V.-positive activists at the medicine-price case. |
| 3:45 newsreel | FIXED | I.C.I.'s 1944 film *Penicillin*. "A small cut on your hand could kill you" plays over a wounded man on a drip with masked doctors at his bed. "With penicillin, it became a few days of medicine" plays over the same men well again. The "Miracle drug" chip now leaves before "a small cut". |
| 4:05 / 4:08 Films Division | OPEN | The 1950s clips fetched were news packages with burned-in graphics (Raj News IDPL story) or not 1950s India. The map and the archive drawing stay. |

## 4. The owner's extra reviews (V and F)

| Item | Status | What we did |
|---|---|---|
| V1: 2:37 "Mixing, pressing, packing, inspections" over one machine | FIXED | One cut per word, cut in the voice's own gaps: Cipla's coating drum on "mixing", tablets off the press on "pressing", the blister line on "packing", the clean room on "inspections", then a Q.C. flask check (Pixabay, tagged ILLUSTRATIVE) on "on the planet". Cipla's letterbox and captions are framed out. |
| V2: the loop glitch | CHECKED | Our engine never loops a clip: every piece plays from its own in-point, and `clean_assign` keeps it inside one clean span of the source. The stutters at 1:36, 10:11 and 5:58 were the promo's own wipes and the repeated softgel line (both fixed here). See §6 for the measured repeats. |
| V3 / F-C: the green capsule machine three times (2:32, 5:58, 7:47) | FIXED | Kept once, at 2:32. 5:58 ("the government allowed only a few companies… our plants stayed too small") is now H.A.'s workers, I.D.P.L.'s works and H.A.'s board. 7:47 ("the central government decided to break the trap") is the Department of Pharmaceuticals press note. |
| F-A: 6:51 cathedral | FIXED | See §1. |
| F-B: 5:16 amoxicillin's side group appears abruptly | FIXED | It now glides in over 1.6 s and locks on, with a click. 6-A.P.A.'s H₂N gives way as it arrives, so the two never overlap. |
| F-D: 7:12–7:20 the "86%" box jitters | FIXED | The cause was a 0.25 s cross-fade between the "<1%" and "86%" heroes. It is now a hard match cut both ways. |
| F-2A: tonal flatness before "Yes." | FIXED (in the edit) | A 0.4 s held breath before "Yes." The voice itself is the owner's own take: a slower take of the collapse lines would mean re-recording blocks 5 and 6, so it's offered, not forced. |
| F-2B: foley gaps | FIXED | A soft tally as the 86 coins turn amber (3:04). The STOPPED stamps get a 60 Hz sub drop under the thud. A glass "snap" as penicillin G's side group comes off and a click as amoxicillin's locks on (5:08–5:16). A rejection buzz with each container the border gate stops (8:47). |
| F-2C: one synth loop 0:00–11:28 | FIXED | Music now changes by act. Act 1 has a driving low bassline under the investigation. Act 2 keeps the lab and pride pads. Act 3 (the plants shut, 5:58–7:47) drops to a sparse sub drone, with silence under the roll call. Act 4 (Kakinada) has rising percussion, kick and hat, growing to the end. Licensed tracks from Studio's Audio Library can replace the bed at mix time, with no new video render. |
| F-3: YouTube Studio API automation | CHECKED | Description: the owner's rule wins (2–4 plain lines and chapters; no sources, hashtags or links), so the suggested sources block is not added. Upload, captions, pinned comment and thumbnail swaps via the API change the public channel, so they wait for the owner's yes. Studio's own Test & Compare runs the three thumbnails. |

## 5. Package

- Title (main): `India Is the Pharmacy of the World. So Who Makes Its Medicine? | Be Practical With Kishore`.
  Test & Compare titles: the Conflict and Explainer titles from R4, in `youtube/description.md`.
- Thumbnails: A "86% FROM ONE COUNTRY" (main), B "MADE IN INDIA?" (challenger), D "WHOSE POWDER?" (the split capsule, new).
  C "INDIA'S ₹2,500 CR BET" stays as a spare.
- Chapters re-checked against this cut. Three moved by a second because of the 0.4 s pause: 5:58, 7:47, 8:06.
- `subtitles.en.srt` was regenerated from this cut's timing.
- Staged upload as R4 advised: Unlisted first, wait for the 4K (VP9) processing, check Content ID (Lyfius, ABP Majha,
  MPC News, ETV Telangana, Next Generation News, I.C.I./Brunner Mond, Cipla, Tribune, CNS, AP, PSU Watch), add the SRT,
  then Public on a weekday at 5:00–5:30 PM IST.

## 6. Measured on the final 4K master

Measured on all 20,650 frames of `pharma_apis_4k.mp4` (3840×2160, 30 fps, 11:28.3), the same checks as R4:

| Check | r4 review cut | Final master |
|---|---|---|
| Frames whose motion repeats on a beat (a near-zero difference between two moving neighbours) | 1 shot, 3.9 s | **0** |
| Black flash frames (one-frame luma dips) | 0 | **0** |
| Fully repeated frames | 5 | 12 (all inside still holds of the source, none between moving frames) |
| Frozen holds over 1.6 s (`freezedetect` n=0.002) | 0 | **0** |
| Cuts closer than 5 frames | the 6 chains above | 3, all checked by eye: the "pressing" tablets' own fast motion before the packing cut (2:38.6), the 0.08 s fade into the black under "It did." (3:29.3), and the cut to the H.A. workers (5:58.0) |
| Part seams (2:16.7, 4:36.0, 6:53.0, 9:11.6) | a framing jump and a label ghost at 2:16 | one clean change at each, overlays and captions continuous across all four |
| Loudness | −14.1 LUFS, −1.1 dBTP | **−14.2 LUFS, −1.7 dBTP**, 3.5 LU range |
| Part frame counts | p1 had one extra empty frame | 4100 + 4179 + 4110 + 4160 + 4101 = 20,650, exactly the film's length |

Found and fixed while measuring the first 4K master (not in any review): every part's first frame dropped its dim,
tags and overlays (a GSAP hide and show both at time 0); seam-crossing labels faded out and in; part 1's length
rounded up gave it a 4101st empty frame, so everything after 2:16 sat one frame behind the voice; the 5:58 protest
shot began inside the source's own dissolve; the AAC encode pushed the true peak to −0.7 dBTP. All five parts were
re-rendered; the numbers above are from that second master.

**Chapters** checked against this master: 0:00, 1:36, 2:12, 2:57, 3:35, 4:30, 5:21, 5:58, 7:47, 8:06, 8:42, 9:16,
10:11 (the open loop's "around minute eight" lands at 8:06.4).
