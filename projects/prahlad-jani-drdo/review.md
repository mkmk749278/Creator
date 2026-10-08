# Self-review of cut v4 (7:26, 2026-10-07) and the fix plan

Owner notes are marked **(K)**; the rest are mine. "Fix" is what v5 does.

| # | Issue | Where | Fix |
|---|---|---|---|
| 1 **(K)** | Jani's face and name first appear at ~1:35; the hook talks about "a man" for 90 s without showing him | S001–S013 | At "కానీ ఒక వ్యక్తి ఏకంగా 70 years" (0:18) cut to ITN close-up + lower-third "PRAHLAD JANI · 1929–2020"; second face shot by 0:24 |
| 2 **(K)** | Coverr stock (hallway/IV/door) styled as CCTV can be mistaken for trial footage | S023 (1:07), S054, S055 (3:10), S005 | Every stand-in in the trial story carries a permanent "ILLUSTRATIVE FOOTAGE" label; CCTV look only on authentic AJ/ITN CCTV |
| 3 **(K)** | Flickr ECG photo shows **168/90 and sensor warnings**, used 6×, including under "VITALS REPORTED NORMAL" (contradicts the VO) | ecg_photo.jpg ×6 | Removed. Replaced by an animated HyperFrames vitals monitor (HR 72, BP 118/76, SpO₂ 98) labelled "ILLUSTRATIVE" |
| 4 **(K)** | Repeats: lab_microscope ×4, lab_cellplate/hood/pipette ×3, earth ×6, blood_sample ×5, water_drop ×4 | many | Cap any stock clip at 2 uses; replace the lab/space repeats with a **study timeline** (2003 → 22 Apr 2010 → Day 3 → Day 10 → 6 May 2010 → press meet) |
| 5 **(K)** | Channel name spoken (0:34, 6:04) with Earth footage, no logo | S013, S125 | Logo sting built from the channel banner at 0:34; end card with logo + subscribe at the outro; small logo bug through the film |
| 6 **(K)** | Science explained with static engravings | kidney (0:07), bladder (3:46–4:28), autophagy (5:08), hypometabolism (4:58) | Animated HyperFrames scenes: kidney filtration failing, dehydration-vs-flat-vitals chart, bladder reabsorption (labelled "DOCTORS' HYPOTHESIS"), autophagy cell, metabolic dial |
| 7 | "22 APRIL 2010" sits on astronaut footage | S050 | Timeline scene (#4) |
| 8 | Near-black shots (night doorway, rain window) read as dead frames | S021, S062–S066 | Swap or lift exposure |
| 9 | BGM is one 4:48 file looping in a 7:26 film: audible restart at 4:48 | audio | Build a long bed with a 6 s crossfade loop |
| 10 | Only hard cuts; section changes don't breathe | block boundaries | 0.3 s dip-to-black at block changes |
| 11 | Archive footage (288p) is soft when upscaled | AJ/ITN | Lanczos plus mild unsharp; 4:3 shown whole over a blurred fill (kept) |
| 12 | 4K requested | whole film | Native 3840×2160 render: HyperFrames scenes via `make_native_4k.mjs`, FFmpeg at 4K with a lighter oversample |
