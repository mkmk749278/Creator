# pharma-apis: acknowledgement of the 30 Oct 4K audit (round 4)

**For the next reviewer.** This answers `Forensic Audit: India's Medicine Powder (pharma-apis) / 4K master` item by
item. The cut to review is `pharma_apis_720_r4.mp4` (Drive `Creator/English/pharma-apis/`, 11:28, 1280x720, 30 fps,
−14.1 LUFS, peak −1.1 dBFS). The 4K master comes once the owner finalises the cut.

Status key: **FIXED** (in the review cut) · **FIXED NEXT** (done in code after the review cut, in the next one) ·
**OPEN** (waiting on footage now on Drive) · **CHECKED** (measured; nothing to change, with the evidence).

Times are the review cut's own times. Where an item moved, both are given.

## 1. Critical red flags

| Audit item | Status | What we did / found |
|---|---|---|
| 10:30 "It has the factories" over the East Asian worker clip | FIXED | Now a Lyfius worker in a hard hat at the Kakinada plant. The 7:22 clip is tagged `PIXABAY · ILLUSTRATIVE`. |
| Judder: "51 shots, 24/25 fps footage" | FIXED (cause was different) | We measured all 20,640 frames of the 4K master. The footage conform from round 3 worked: no repeated frames on any footage shot. The 406 repeats were **whole frames, grain included, only on our slow animated scenes**: the film grain stepped 24 times a second on a 30 fps timeline. The first fix (`floor(t*30)`) still repeated every 3rd frame; `Math.round` fixed it, tested frame by frame in the browser. **Review cut: 0 repeated frames.** |
| 8 black flash frames (1:18.87 … 10:38.73) | FIXED | We found 13, all on the first frame of a new shot: shot times were rounded **up** to 3 decimals, so on the cut frame the new shot had not started and the old one had ended. Times are now floored onto their frames (`build/frame_floor.py`). **Review cut: 0 flashes.** |
| Flicker chains 1:34.27, 1:35.57, 8:09.13, 9:41.77, 10:08.47 (4:00.33 not found in the review cut) | FIXED NEXT | Confirmed: the others are the Lyfius promo's own 3–4-frame wipes, inside spans we had marked clean (scene detection misses wipes). The clean spans are now split at every frame-difference transition of the source (5 spans split or trimmed). In the next cut. |

## 2. Science, tech and regulation

| Audit item | Status | What we did / found |
|---|---|---|
| 4:30 "Paracetamol is *cooked*" over petri dishes | OPEN | Reactor and Indian bulk-drug plant footage was fetched on 30 Oct (Drive `r4/footage/`); it goes in next round. |
| 5:08–5:21 Pen G → 6-APA → amoxicillin over capsules | FIXED | New animated scene `chain`: one penam core drawn once, penicillin G's side group (green) snipped off on "smaller base powder", H₂N marks 6-A.P.A. on "six A.P.A.", amoxicillin's group (with its NH₂ and the ring's OH) locks on. Skeletal formulae, `ILLUSTRATION`. |
| 6:38 / 7:12 the 1% → 86% numbers too small | FIXED | Hero numbers centre screen with a capsule bar and their bases: "<1%" for 1991 (6:39), the same "<1%" back in the same place on "Remember that one per cent?", then a match cut to "86%" on the word "eighty-six" (7:20), capsule filling, low thud. |
| 9:39 "₹5,000 crore" over one company's plant | FIXED | Now PSU Watch's report "Total investment of Rs 5,210 crore made under PLI scheme for bulk drugs till June 2026: Govt" (the claim's source). |
| Rolling counters show wrong numbers for about a second | FIXED | Every counter lands in 0.45 s or less. |

## 3. Audio, pronunciation, subtitles

| Audit item | Status | What we did / found |
|---|---|---|
| Loudness, captions | CHECKED | Unchanged pass: −14.1 LUFS, −1.1 dBTP, captions in sync. |
| Possible doubled words 0:50.8, 5:22.8, 8:01.3 | CHECKED (round 3) | The same lines were checked in round 3: transcript errors, and one breath 8 dB down. The takes are the owner's originals (re-uploaded 30 Oct, identical to the millisecond). **Owner: one listen at those times.** |
| Pronunciation list (Pimpri, Ranbaxy, Kakinada, Aurobindo, Lyfius, Nakkapalli, "six A.P.A.") | OPEN (owner's ears) | For the owner's audio-only pass before the 4K lock. |

## 4. Visuals, repetition, cartography

**A. Emotional peaks on generic stock**

| Time | Status | Notes |
|---|---|---|
| 3:35 Pimpri 1954 | OPEN | No 1950s HAL photo found that we may use; Nehru Archive and the UN photo library block the cloud. Asked the owner to save one from his phone. |
| 4:05 "Picture your grandparents' India" | OPEN | Films Division / 1950s India films fetched 30 Oct; next round. |
| 4:08 "A young, poor country…" | OPEN | Same footage set. |
| 3:45 "A small cut could kill you" | OPEN | A 1940s wounded-soldier treatment newsreel (CriticalPast) fetched; next round. |
| 6:43–7:04 the STOPPED roll call | OPEN | IDPL Rishikesh's abandoned plant (4 clips) fetched; next round, one real image per name where one exists. |
| 6:10 / 7:28 the chimney (twice) | OPEN | No China drug-park imagery cleared yet. |
| 1:42 2001 H.I.V. human stakes | OPEN | AP Archive and TAC footage of the 2001 protests fetched; next round. |
| 0:58 Hubei, dead repeat of the map | FIXED | China News Service footage of Wuhan, 26 Jan 2020 (CC BY 4.0): the empty aerial, then the empty boulevard on "the whole province was shut down". Logos cropped out. |

**B. Signature moment 1% → 86%:** FIXED (above).

**C. Shot-to-word swaps**

| Time | Status | Notes |
|---|---|---|
| 0:00 generic pills | OPEN | Indian export carton / packing line wanted; plant footage set fetched. |
| 1:19 Western hands | OPEN | Indian medicine box wanted. |
| 1:36, 2:32 foreign capsule lines | OPEN | Indian bulk-drug plant footage fetched; next round. |
| 3:12 pink tablets for paracetamol | FIXED | A fever thermometer on white tablets. |
| 3:24 11 s of grey blisters | FIXED | 0.6 s of black under "It did.", then Hindustan Antibiotics' old signboard behind trees today (ABP Majha, tagged TODAY). The 1954 photo is still open (A). |
| 5:15 opening tablets again | FIXED | The `chain` scene covers the whole line. |
| 5:58 licence era over a capsule machine | OPEN | No licence-era document found yet. |
| 7:35 shaky handheld mill | FIXED | The tanks scene, steady: "Small plant: can't compete", "Big plant: big risk", a PRICE WAR stamp on "wipe it out" (with sound). |
| 7:51 PLI over a Western lab | FIXED | The Department of Pharmaceuticals press note (9 Dec 2021: "41 products … Rs. 6,940 cr."), tagged with its real date. |
| 10:11 lesson over a conveyor | FIXED | New scene `chain_lesson`: India's last link (saffron), China's links before it (amber), the joint cracks on "the step before". |

**D. Repeats:** the fermenter's day clock now only runs forward and the germ beat is labelled "What if"; the
Kakinada tank keeps its own clock (FIXED). Western lab now 1× (was 2), green capsule line 1× (was 2), pale tablets 1×
(was 2). Capsule machine (3×) and chimney (2×) wait for the fetched footage (OPEN).

**E. Quality and safe zones**

| Item | Status | Notes |
|---|---|---|
| Lyfius promo soft at 4K | CHECKED | It is a web promo; shots kept short. Original masters only from Lyfius/Aurobindo. |
| 9:39 / 8:20 murky satellite crossfades | FIXED | 9:39 is now the PSU Watch document; 8:20 is a straight cut. |
| 5:25 POWER/WATER/STEAM over the logo | FIXED | Meters moved left under the cost bars. |
| 6:18–6:23, 9:10–9:16 source tags at the logo | CHECKED | In the 720p cut the tags sit left of the logo bug, not under it. |
| 9:47 "SAME STATE · ANDHRA PRADESH" tiny, on the subtitle | FIXED | 40 px, two lines, beside the pins, well above the captions. |
| 2:17 "THE REST OF THE TABL…" clipped | FIXED | Layers moved 140 px left so the punched-in pieces keep the label. |
| Map's northern boundary | CHECKED (round 3) | Land outline only; no borders drawn. |

## 5. Package

Title, description and chapters unchanged (chapter times re-checked against the final cut). The thumbnail
suggestions ("86% · ONE COUNTRY", the "WHOSE POWDER?" split capsule) and the staged upload plan are taken up at delivery.

## New holds found in the review cut (under the audit's radar)
1:50.7 (2.2 s, the $10,400 card), 1:53.4 (1.7 s), 2:12.6 (1.8 s), 7:33.9 (1.6 s, the tanks building). For the next round.
