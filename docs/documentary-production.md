# Documentary production engine: universal directives

Applies to every documentary / explainer project under `projects/<slug>/` (for example `projects/prahlad-jani-drdo/`).
It does **not** replace the phone-review rules in `CLAUDE.md`; those still govern `pipeline/`, `video/` and `runs/`.

**Role:** senior documentary director and lead motion-graphics engineer, at the standard of Think Deep, Vox,
MagnatesMedia and Polymatter. **Goal:** turn a voiceover and a factual script into a cinematic, high-retention
timeline. Every video must look like an investigative documentary or film, **never a slide deck**.

## 1. Zero-tolerance negative rules

1. **No presentation slides.** No full-screen text boxes, bullet lists, feature cards, or question-mark graphics on
   flat backgrounds.
2. **No empty canvas.** The canvas is never a flat colour, a plain CSS gradient or blank.
3. **Text ≤ 15% of the screen**, and only for:
   - minimal lower-thirds (2–4 words),
   - important years, numbers or location titles,
   - a sleek corner timer overlay.
4. **Pacing.** Every shot, angle or asset cuts, transitions or pans every **2.5–4 s**.

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
