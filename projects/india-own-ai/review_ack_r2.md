# Review acknowledgement, round 2 → 4K master r3 (2026-11-04)

Review answered: `Review/reviews/bepracticalwithkishore/india-own-ai/720-r2-2026-11-04.md` (on `india_own_ai_r2_720.mp4`).
The VO, its timing and the approved r2 audio mix are unchanged, so **every time below is the same in r2 and r3**.
The owner asked for the final 4K now (2026-11-04: "continue fixes and render in 4k final refined film"), so this round
goes straight to the native 4K master instead of a 720p review cut.

How it was checked: every note against the composition, the word timings (`align/words.json`) and a frame of r2
(`hyperframes snapshot` sheets before and after); `npx hyperframes check` on every part: 0 errors.

## 1. Critical red flags

| # | Time | Note | Status | What changed, with evidence |
|---|---|---|---|---|
| 1 | 8:24–8:30 | "Pratyush Kumar" strap on NDTV's Shiv Aroor | **FIXED** | Confirmed from the clip's own title ("NDTV Ind.AI Summit: Sarvam AI CEO Pratyush Kumar On AI-Powered Smart Glasses", `footage/fetched.csv`): the guest in the purple kurta is Pratyush Kumar. New `pk` crop (2.0×, origin 78% 55%) shows him alone; the NDTV header, "SHIV AROOR"/"MANAGING EDITOR" straps, the "LIVE" bar and the NDTV bug are all outside the frame. The span stops at 19.6 s, before the audience cutaway. Our strap now sits beside him (x = 1100 of 1920) and lands on the word "Pratyush". The source is re-conformed from the 1080p original (was 720p). The crop holds through split holds too (`KEEP` in `split_long`). |
| 2 | 8:33–8:43 | 105B card under "built on top of a French one" | **FIXED** | Now the `sarvamai/sarvam-m` Hugging Face card, pushed in on "sarvam-m is a multilingual, hybrid-reasoning, text-only language model built on Mistral-Small" (captured 4 Nov 2026, `tools/capture_docs_r3.cjs`). The 105B card plays only at 9:18–9:26. |
| 3 | 5:28–5:36 | AI Kosh banner gives away the 9:00 reveal | **FIXED** | Only the stats strip ("16140+ Datasets · 379 Models · 22 Sectors · 689 Organizations") is on screen (`docs/aikosh_stats.png`, cropped from the same capture). No Sarvam text, no QR code. |
| 4 | 2:19–2:26 | Main open loop over a near-black plate | **FIXED** | The film's own progress bar: red fill to "YOU ARE HERE · 2:19", a saffron pin drops at minute 10 on the word "minute" with a 44 px "MINUTE 10" label, DeepSeek's 25 Telugu pieces (red half-letters) run above it, and on "an Indian machine" they fade and Sarvam's 11 saffron pieces land over the pin. Full contrast, nothing faded; the blackout plate is gone. |
| 5 | 11:01–11:02 | V3 paper under "one point six trillion" | **FIXED** | The `deepseek-ai/DeepSeek-V4-Pro` card, pushed in on "DeepSeek-V4-Pro with 1.6T parameters (49B activated)", undimmed. |
| 6 | 5:45–5:54 | Phone-size BGA chip under "a chip like this one… Nvidia" | **FIXED** | The real NVIDIA H100 modules from the Nvidia clip (span 27.6–30.6 s), tagged "FOOTAGE · NVIDIA · H100 MODULES", from "A chip like this one". "This is the reading room" opens on the wafer clip. At 8:31 "those Nvidia chips" now shows the IndiaAI compute portal. |
| 7 | 10:40–10:52, 12:25 | KISAN farmer under Aadhaar and Maharashtra | **FIXED** | 10:38 "already at work" → Sarvam's own Indus film. 10:40 Aadhaar → Sarvam's customer story "Aadhaar activates voice agents for 4 crore Indians" (the PIB release and the UIDAI PDF are blocked from this container: 403/503), with "AADHAAR · SARVAM SAYS". 10:47 Mantralaya photo stays on "Maharashtra", then AIM's report "Sarvam AI Rolls Out Indus Cowork to 2,500 Maharashtra Govt Officials" (the film's own source, claims.csv A75). 12:13–12:26: three chat apps on cards with the same Hindi question (labelled ILLUSTRATION). The farmer clip is no longer in the film. |

## 2. Scientific, technical and regulatory

| Time | Note | Status | Evidence |
|---|---|---|---|
| 2:12 | "WITHIN 6 MONTHS" harsher than the record | **FIXED** | Label reads "HOPED 6 · AT MOST 10 MONTHS". |
| 6:35–6:37 | Date card covers the BIS release headline | **FIXED** | The "12 MAY 2025" card moved to the lower left (top 560 px), clear of the document and the caption. |
| 7:32 | Rupee rate not in the tag | **FIXED** | "[META Q3 2026 \| ₹94.91/$ ON 2 NOV 2026]" (the rate claims.csv A52 used). |
| 7:10–7:21 | 2024 target vs 2026 count | **FIXED** | Meta's label adds "AND MORE SINCE"; India's reads "45,000 · JUNE 2026". |
| 1:21–1:24 | Shanghai under "a small Chinese lab" | **FIXED** | Hangzhou's West Lake (Pixabay 322063, tagged "PIXABAY · HANGZHOU, WEST LAKE"). Shanghai stays at 8:05 on "sold to China". |
| other rows | token counts, $590 bn, 45,000 GPUs, 105B/12T/18 Feb, 15× | **CHECKED** | The reviewer confirmed them; no VO change. |

## 3. Audio, pronunciation and subtitles

| Note | Status | Evidence |
|---|---|---|
| Master loudness | **CHECKED** | The 4K master carries the r2 mix unchanged (−14.2 LUFS, peak −1.8 dBFS), re-measured after the remux. The two lift points (1:43, 7:43) are left for the owner's listen. |
| "Navik" in the SRT | **CHECKED** | `youtube/subtitles.en.srt` (the upload file) already says "It's called NavIC." The aligned working SRT is not for upload. |
| SRT splits at "A.I. / Kosh", "India A.I. / Impact Summit", "I.I.T. / Bombay" | **FIXED** | `caption_rows()` joins those rows; each name is now on one card in the burned-in captions and in the upload SRT. |
| Pronunciations (Pratyush, Vaishnaw, Mandapam, Param Two, Kosh, Odia, Indus) | **OPEN (owner)** | VO is locked; for the owner's listening pass. |
| 0:51 caption on TechCrunch's headline | **OPEN** | The headline is the document being shown; the caption sits under it briefly. Left as is. |
| 9:39 BharatGen reel caption under ours | **FIXED** | BharatGen span ends at 115.6 s, before the reel's "DEVELOPERS GAIN ACCESS…" band appears. |
| 11:12 our text over "Sovereign Models" art | **FIXED** | Blog pushed in at its top (title), chip raised to 560 px. |
| 12:38 CNBC-TV18 headline and logo | **FIXED** | New `bot` crop (1.6×, anchored at the bottom) shows only the rocket; the headline box and logo are out of frame (checked at 12:37). |

## 4. Visual assets, repetition, cartography

| Time | Note | Status | Now |
|---|---|---|---|
| 0:42–0:50 | Low-cut-top crop on "your apps pay by the piece" | **FIXED** | The Hindi question being chopped into its 18 real DeepSeek pieces, with the PIECE METER counting up and "PAY BY THE PIECE / MORE PIECES = BIGGER BILL". (No Indian-hands typing clip exists in our pool or on Pixabay; the two Drive typing clips are the same foreign stock look.) |
| 1:08–1:11 | Foreign model on a phone | **FIXED** | Three chat-app cards with the same Hindi question (ILLUSTRATION), then the America / China / here flags. |
| 5:25 | Same model under "voice by voice" | **FIXED** | Bhasha Daan's own contributors reel. |
| 1:16–1:22 | Generic stock ticker | **OPEN** | Nasdaq and Reuters pages are blocked from this container; the clip stays labelled "PEXELS · ILLUSTRATIVE FOOTAGE". |
| 4:47–4:55 | ZARA street on "the chopper learns from this library" | **FIXED** | The library shelf (English 42 of 100 pages, then Hindi / Marathi / Telugu shelves) and DeepSeek's Telugu pieces dropping out of it. |
| 5:55–6:00 | Lab rack on "thousands, wired together" | **FIXED** | Data-hall cabling. (A first swap to a "data centre" stock clip turned out to be a quarry in the snapshot and was rejected.) |
| 9:02–9:05 | PM at "India Energy Stack" on "105 billion" | **FIXED** | Only the span at Sarvam's own "Sovereign Models · Sarvam 30B / 105B" screens. |
| 12:03–12:12 | Stock hands on "check your ChatGPT plan" | **FIXED (partly)** | The ChatGPT Go free-for-a-year page with "NOV 2026 · THE FREE YEAR ENDS". chatgpt.com's plan screen is behind Cloudflare from here, so no real subscription screenshot. |
| 12:29–12:37 | A flag on a pole for 8 s | **FIXED** | Flag only on "built for itself", then the NVS-03 rocket on the pad and lift-off on "satellite navigation, up in space", ISRO's IRNSS/NavIC page on "NavIC". |
| Rule of 2 | Cable clip ×5, farmer ×3, India Gate ×3 | **FIXED** | Counted in the build: no stock clip or still more than twice (real event footage and documents excepted). The two cable clips now play once each. |
| Empty three-box plate | Boxes stay empty | **FIXED** | Each box fills with its picture when named (Hindi page, the H100 modules, an engineer at work) at 2:52, 3:22, 10:32 and the 11:19 scoreboard. 2:27 keeps question marks on purpose: nothing is named yet. |
| 1:26–1:37 | Near-empty plates | **FIXED** | DeepSeek-V3's first page dimmed under the App Store card; at 1:34 the V3 report's Table 1 ("$5.576M") under "the final training run". |
| 7:10–7:48 | Holds with no visible motion | **FIXED** | Counters run with the words: Meta's 0 → 3,50,000 chips, "≈ 1× → 8×", and "1× → 2×" on "not double" before the "> 100×" stamp. |
| Creative 1 | Three-tier world map | **OPEN** | Not built: it needs India's border exactly as the Survey of India map; a wrong border is worse than chips. Next film or a Short. |
| Creative 2 | 11:40 thesis callback with Telugu chips | **OPEN** | Not built this round. |
| Creative 3 | 8:44 training-loss curve | **FIXED** | An orange loss curve draws from zero across the line, labelled "ILLUSTRATIVE CURVE", with "TRAINING FROM ZERO". |

### Typography (measured at 1920×1080 in snapshots)
| Time | Note | Status |
|---|---|---|
| 1:54–2:03 | Bar labels 33 px | **FIXED**: all `.hkey` labels 44 px, brighter (#c9d4de) with a shadow. |
| 4:07–4:15 | Hindi bar under the caption, Telugu label at the edge | **FIXED**: stacks at 0.24 px a page, base at y = 700, tallest label at y ≈ 91, inside the frame; title shortened. |
| 4:39–4:46 | Shelf names 33 px | **FIXED**: 44 px, Telugu 53 px. |
| 7:10–7:21 | Labels crossed by the Meta box | **FIXED**: India and Meta labels in their own zones (hyperframes check: no overlap). |
| 7:49 | "> 100×" over "META · 2026" | **FIXED**: badge moved to the left column (y = 400). |
| 9:29–9:35 | Timeline 36 / 21 px | **FIXED**: 44 / 30 px. |
| 10:16–10:31 | FLORES legend in the corner, no "× English" line, no BharatGen | **FIXED**: legend inside the chart ("BAR = PIECES PER ENGLISH PIECE"), and a green BharatGen bar for Odia on the word "BharatGen's" (from our FLORES run, 1.3×). |
| 9:36–9:46 | BharatGen logo clipped | **FIXED (mostly)**: gentle push only; the card's own framing still runs close to the right edge in the source. |
| 8:24 | Name strap role 24 px | **FIXED**: 30 px. |

## 5. Packaging
- **Thumbnail:** B is the main (as recommended), upgraded with the "INDIA'S FIX?" chip and a drop shadow on the dark words (`youtube/thumbnail_b.jpg`). A stays the A/B challenger.
- **Titles and the schedule** (Unlisted ≥ 3 h, Fri 6 Nov 5:00–5:30 PM IST, before mid-November): for the owner's `/deliver` step.

## Also found in this round
- The 4K master renders as 10 parts (~80 s each, `NPARTS=10`) so no job carries the 600 MB media of the old p1/p4.
- Seven sources that were shrunk to 720p for the review render are back at full resolution (the NDTV, PM, BharatGen and Bhasha Daan clips at 1080p; Bengaluru sunrise at 2160p; library walk at 1440p), mapped frame-exact to the r2 timing.
