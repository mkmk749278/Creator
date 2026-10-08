# Documentary production engine: universal directives

Applies to every documentary / explainer project under `projects/<slug>/` (for example `projects/prahlad-jani-drdo/`).
It does **not** replace the phone-review rules in `CLAUDE.md`; those still govern `pipeline/`, `video/` and `runs/`.

**Role:** executive documentary director and motion-graphics engineer for "Be Practical with Kishore", at the
standard of Vox, MagnatesMedia, Polymatter, ColdFusion and Think Deep. **Goal:** turn a voiceover and a factual script
into a cinematic, motion-heavy timeline. Every video must look like a broadcast documentary or investigative film,
**never a slide deck, corporate presentation or photo slideshow**.

## 1. Zero-tolerance rules

1. **No presentation cards.** No full-screen text boxes, bullet lists, icon cards, summary slides, or question-mark
   graphics on flat backgrounds.
2. **No static canvas.** A motionless photo or a flat colour never stays on screen for more than **1.5 s**. The canvas
   always has camera motion, particle atmosphere or live video. A plain CSS gradient never counts as a background.
3. **85% real motion.** At least 85% of every timeline is moving video, screen recordings, kinetic data animation or
   high-frame-rate B-roll. Stills are allowed only as authentic archival evidence, and always animated (§3).
4. **Text ≤ 15% of the screen**, and only for:
   - minimal lower-thirds (2–4 words),
   - locations, dates and technical telemetry,
   - numeric counters, timers and data meters.
5. **Pacing.** Every shot, angle or asset cuts, transitions or pans every **2.5–4 s**.
6. **No re-transcription.** When a script exists, never run Whisper or any speech-to-text. Align scenes to the script's
   paragraphs and to `silencedetect` timestamps. Transcribe (see `CLAUDE.md` › Telugu ASR) only when no script exists.

## 1a. Visual language by genre

Pick the genre before sourcing; it decides palette, media stack and accents.

| Genre | Palette | Media stack | Graphic accents |
|---|---|---|---|
| **Science & medical** | Deep navy, surgical teal, graphite | Electron-microscope loops, 3D anatomy, MRI/sonography, macro lab work, cell division | Focus callouts, animated yellow circles on the abnormality, telemetry grids |
| **Biography & martial arts** | Warm amber, chiaroscuro, 35 mm grain | Raw training footage, press conferences, archival newsreels, slow-motion performance, cultural demonstrations | Split-screen comparisons, timecode counters, year stamps |
| **Business & finance** | Terminal charcoal, holographic chart sweeps | Trading floors, HQ aerials, currency printing, shipping lanes, factory automation | Isometric data graphs, metric tickers, animated balance-sheet highlights (no full-screen text) |
| **Tech, AI & digital mysteries** | Matte black, electric cyan, neon phosphor | Data centres, circuit-board macros, browser UI mock-ups, terminal sessions, wafer fabs | Terminal type, syntax-highlight overlays, network-node links |
| **Philosophy, society & lifestyle** | Desaturated monochrome with a saturated hero subject | Fast-motion crowds, commuter platforms, pupil macros, solitary landscapes | Pacing contrast: extreme speed, then sudden stillness |

## 1b. Making stills move

When an authentic photo or document is irreplaceable, it never sits still:
1. **2.5D parallax:** cut the subject from the background; foreground scales toward 1.15x while the background drifts
   to 0.95x.
2. **Atmosphere:** smoke, dust motes, light leaks or rain at ~15% opacity over the still.
3. **Forensic magnifier:** on documents, scans or clippings, slide a magnifier or high-contrast zoom circle over the
   exact line or date the VO is reading.
4. **Moving contact sheet:** 3–4 archival angles slide into a collage one by one, every ~1.5 s, instead of one still.

## 2. Three-layer visual stack (every frame)

| Layer | Content | Rules |
|---|---|---|
| **1: Base** (100% full screen) | Real video footage or ultra-high-res photos | Stills always carry continuous Ken Burns motion (zoom 1.00→1.15, or a slow pan). No motionless photos |
| **2: Atmosphere** | 2.35:1 letterbox bars (when used), subtle 35 mm grain, ~30% edge vignette, light leaks, low-opacity medical/tech HUD wireframes | Never hides the base layer |
| **3: Kinetic accents** | Minimal kinetic type, lower-thirds, data counters | Lower corners, on a dark gradient scrim for readability |

## 3. Asset sourcing playbook

**A. Real-world news, people, history**
- **YouTube** (yt-dlp): press conferences, event footage, debates. Query: exact event + city/year + "raw footage" /
  "press conference" / "full video".
- **Internet Archive** (archive.org): public-domain newsreels, government and military trials.
- **Wikimedia Commons**: public-domain or CC archival photos, paintings, museum collections.

**B. Free cinematic B-roll**
- **Pexels Video**: human emotion, macro (eyes, sweat), cities, ICU monitors, labs, water.
- **Pixabay**: microscopic cells, space, DNA, medical equipment, extreme nature.
- **Coverr / Mixkit**: drone shots, technology, dark moody interiors, screens.

**C. Scientific and specialised**
- **Nature / ScienceDirect / PubMed Central**: published charts, sonography figures, ECGs, electron micrographs.
- **NASA / ESA** (images.nasa.gov): 4K space and astronaut-training footage (public domain).
- **Wellcome Collection**: historical medical illustrations and anatomical drawings.
- **SEC EDGAR / company filings**: balance sheets, IPO filings, regulatory notices (business stories).

What actually downloads from the cloud container differs from this list (YouTube, Pexels, Pixabay and Mixkit are
blocked there): check `CLAUDE.md` › Lessons before sourcing, and use the VPS for YouTube.

**D. AI-generated media (only when no real asset exists)**
- For internal biology, legends or unfilmed experiments, write exact prompts for Midjourney / Sora / Runway.
- Style: 8K, cinematic lighting, "shot on 35 mm Arri Alexa", photorealistic, Octane-style for cells and organs.

### Rights and honesty guardrails (always on)
- Log every asset in `projects/<slug>/media_manifest.csv` (ID, URL, owner, licence, date, EDL slots).
- Third-party news/YouTube footage: short excerpts that you comment on and transform, credited on screen. Prefer
  licensed archive clips (AP Archive, Reuters) for anything long. Never re-upload a whole clip.
- AI shots never depict a real, identifiable person or pose as archival evidence. Label them "illustration" when
  a viewer could mistake them for real data, and log them in `credits.md`.
- Never synthesise a real person's voice or quote. Live-audio pauses use the real recording or nothing.
- Present claims as claims. When a topic touches health, include the mainstream scientific view.

## 4. Standard workflow for every video

### Step 1: asset manifest and download checklist (before any code)
| Asset ID | File Name | Description | Source Platform | Exact Search Query |
| :--- | :--- | :--- | :--- | :--- |
| ASSET_01 | `event_real.mp4` | Main subject live action | YouTube | "[exact search phrase]" |

### Step 2: scene and timeline mapping (EDL)
For every section of the audio: **timecode (start–end)**, **primary full-screen asset**, **motion** (zoom 1.0→1.15x /
L→R pan), **overlay layer**, **kinetic text**, **sound design / ducking cues** (the moments the VO pauses for real audio).

### Step 3: code generation
- Assembly code binds strictly to `projects/<slug>/assets/`.
- Every scene's root background is a video or an animated image.
- Engine: an FFmpeg/Python assembler driven by the EDL CSV (`projects/<slug>/assemble.py`) for footage-led cuts.
  For HyperFrames motion-graphics inserts, follow the HyperFrames rules in `CLAUDE.md`. Remotion is not installed
  in this repo; ask before adding it.
- Zero cards. Zero bullet points. Pure visual storytelling.

## Audio defaults
- **The video is not locked to the VO length.** Programme = VO + every break. Two break types in the EDL:
  - `LIVE`: the VO stops, the **original clip plays with its own audio** (press conference, news report, real
    event sound) for `src_in`–`src_out`, then the VO resumes exactly where it stopped. Any length; keep the
    picture untouched (`motion=none`/`push`) and credit the source in a lower-third. A Telugu translation goes in
    the row's `subtitle` column and lands in the SRT.
  - `VO_PAUSE`: 2–4 s of picture with ambience/SFX only.
  `vo_skip` drops a stretch of VO after the break (e.g. a duplicated take). The pacing rule (cut every 2.5–4 s)
  does not apply inside a LIVE clip; it applies again as soon as the VO resumes.
- **Diegetic cuts.** Whenever authentic footage appears, the narration stops completely and the asset's own sound
  plays for 2–6 s (a conch, a press statement, a monitor alarm, a gavel, machinery). The VO resumes after the sound
  peaks. Never talk over genuine live dialogue; real speech runs as a `LIVE` row for as long as it needs.
- **1-to-1 semantic lock.** The picture shows exactly what the VO says at that second: kidneys or dehydration → renal
  animation; CCTV isolation → a high-angle surveillance view; world records → the actual record attempt.
- The voiceover leads. BGM sits at **−18 to −22 dB** under the VO, sidechain-ducked, and comes up only in VO pauses.
- Live-audio pauses: 2–4 s of real ambience or archival speech.
- Loudness target for YouTube: −14 LUFS integrated, −1 dBTP.

## Deliverables per video (all viewable on a phone)
`asset-manifest.md` · `edl.csv` + `edl.md` · `subtitles.<lang>.srt` · `3d-prompts.md` · `assemble.py` ·
preview MP4 (Actions artifact) · contact sheet PNG.

## Lessons log
### 2026-10 · Prahlad Jani & DRDO (Telugu, 6:30)
- **Source reachability (cloud container):** see `CLAUDE.md` › Lessons. `tools/fetch_assets.py` encodes what works and logs
  licences automatically; `tools/credits.py` turns the manifest into YouTube-description credits.
- **What filled the gaps:** NASA lab B-roll (KSC CRS-21 payload prep) stood in for "scientists/lab"; NASA ISS tour/Earth views for
  "astronauts/space"; Wellcome engravings for anatomy (blurred-fill, tagged "ENGRAVING · WELLCOME COLLECTION"); Wellcome photos of
  Henry Tanner's 1880 fast as historical context; Coverr hospital footage with the CCTV look for the sealed room.
- **What could not be sourced here:** the 2010 news footage and press conference (Reuters/AP archive, paid), DRDO imagery,
  free photos of the subject. These need the VPS (yt-dlp with cookies) or a paid licence.
- **Balance:** a real 16 s CC BY clip of James Randi (archive.org, May 2010) as the `LIVE` skeptic beat, with a Telugu caption.
- **Process:** VO first (transcribe → phrases → align) → EDL from beats → fetch → contact sheet → map EDL to real files
  (`assemble.py --check` must say 0 missing) → section renders of risky shots → full render → SRT rebuild → deliver.

## Pre-render review (every cut, before the final render)
Contact-sheet the cut (`assemble.py` writes one) and go through it shot by shot. Write `review.md` with issue, shot IDs and fix.
- [ ] At least 85% of the runtime is moving footage or animation; no unmoving still or flat frame lasts over 1.5 s.
- [ ] Every shot matches the exact words spoken over it; the VO is silent under every diegetic or LIVE moment.
- [ ] Subject's face and name on screen within 20 s; the name lower-third reappears when the VO says the name.
- [ ] Every frame's on-screen data agrees with the VO at that moment (numbers, monitors, headlines, dates).
- [ ] Stand-in or stock footage near the real story is labelled "ILLUSTRATIVE FOOTAGE"; authentic footage carries its source credit.
- [ ] No stock clip more than twice; no shot over 4 s except HyperFrames scenes and LIVE clips.
- [ ] Science and data beats use animated scenes, labelled honestly (ILLUSTRATION, ILLUSTRATIVE CURVE, HYPOTHESIS).
- [ ] Channel name in the VO means the logo is on screen; the film ends on the end card; the logo bug is present elsewhere.
- [ ] No near-black or dead frames; section changes breathe (dip to black); the music bed never restarts audibly.
- [ ] Claims stay claims; at least one real skeptic or mainstream-science beat on health topics.
- [ ] Loudness about −14 LUFS; VO silent during LIVE clips; subtitles rebuilt after any timing change.

### 2026-10 · v5 changes after owner review
Logo sting and end card from the owner's banner; HyperFrames timeline, vitals, dehydration chart and metabolism dial; Three.js
kidney, bladder (labelled hypothesis) and autophagy scenes; ILLUSTRATIVE FOOTAGE labels; 168/90 monitor photo removed; stock repeats
capped; face and name at 0:18; native 4K master.
