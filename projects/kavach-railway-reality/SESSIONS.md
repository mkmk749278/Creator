# Scene sessions brief: The Kavach Railway Reality

You are one of five parallel scene sessions (A, B, C, D, E) for this film. The coordinator session (S0) does the real
footage, documents, music, assembly and review. Read, in order: `CLAUDE.md`, PLAYBOOK §4a-4 (the owner's production
guide: visual pillars), §5 (the look), §9 (realistic animation and the vendored 3D stack), §10 (HyperFrames gotchas),
this file, `projects/kavach-railway-reality/README.md` (art direction "Signal Room"), then your section of
`projects/kavach-railway-reality/scenes.md` (exact durations and word cues, generated from the real VO timing).
The script and facts are locked and fact-checked: **do not change any on-screen number or wording** in your spec. If a
spec line is impossible or looks wrong, write it in your report instead of improvising.

## The bar
A premium, next-generation investigative explainer (Vox, Johnny Harris, Fern, high-end rail-engineering films), not
slides, not clip-art, not a generic dashboard. Every frame should look like one designed world, **"Signal Room"**:
- **A, 3D hardware world:** real-time Three.js (vendored), physically based materials: weathered locomotive steel and
  paint (generic WAP-7-like electric loco, no livery text or logos), concrete PSC sleepers, granite ballast, polished rail
  heads, a yellow-black RFID tag box, a lattice telecom tower. HDRI lighting from the shared library, ACES/AgX tone
  mapping, dusk/night grading with signal colours as the light sources, bloom only on lamps and cyan data, fog/haze
  depth, slow purposeful camera moves (dolly, orbit, push-in; never static). Data and radio are cyan light (pulses, rings,
  flowing particles along wires). X-ray views = cyan edge lines over a ghosted shell.
- **B, telemetry world:** the Kavach cab display's grammar (LP-OCIP: target distance, permitted speed, signal aspect,
  mode) as precision instruments on carbon slate: thin lines, tabular numbers, tick marks, needles with inertia,
  speed-vs-distance curves drawn ahead of a train silhouette, a fog shader for the windscreen. No glass cards, no neon
  dashboard clichés.
- **C, forensics world:** 2.5D signalling schematics as an investigator's light table: track diagrams drawn stroke by
  stroke on dark slate with paper grain, signals as real three-aspect heads, points that physically swing, current
  flowing as light along wires, crimson for the false input, cyan for Kavach. Generic schematics, never a traced copy
  of a real station drawing (label ILLUSTRATION / SIMULATION).
- **D, data world:** land-only India map (no political borders; Natural Earth land as in
  `video/fireice/benson_map/mkmap.mjs`), rail lines as thin luminous strokes, counters as precision instruments, the
  funnel and flowchart drawn as rail lines. Whiteboard maths: copy `video/lib/whiteboard` (README) for every BOARD shot:
  real marker handwriting, stroke by stroke.
- **E, phone and paper world:** a realistic Android phone (generic green chat app, never WhatsApp or YouTube branding,
  generic Indian family names), forwarded-message cards, rubber stamps with ink texture (`.kav-stamp`), a standards page
  under a magnifier; title and chapter cards that look like film titles, not slides.

## Shared rules for every scene
- **Copy `video/kavach-railway-reality/_shared/kav.css`** into each scene folder and use its tokens and `.kav-label`,
  `.kav-num`, `.kav-stamp` classes. Palette: slate `#0F172A`, cyan `#0284C7` / `#38BDF8`, amber `#F59E0B`, crimson
  `#DC2626`, white `#F8FAFC`; signal green `#22C55E` for aspects only. Font: vendored Inter (add
  `vendor/fonts/inter-latin-ext-600-normal.woff2` to `index.html` if you show ₹, ≈, → or ≠).
- **Keep corners clear:** the assembler adds the citation tag and the ILLUSTRATION/SIMULATION tag bottom-right
  (520×170 px) and the logo bug top-right (260×160 px). Do **not** draw citation tags, ILLUSTRATION tags or logos
  yourself even though the spec mentions them; put in-scene labels lower-left (`.kav-label`) or inside the graphic.
  Text ≤ 15% of the frame, 2–4-word labels, numbers and counters.
- **Timing:** each scene is one HyperFrames composition at 1920×1080, 30 fps, whose `data-duration` equals the scene's
  duration in `scenes.md` exactly. Key every beat to the word cues (seconds inside the scene). Cues are per line; for a
  word inside a line, place it by its share of the line's characters (the voice is even-paced: about 14 characters/s).
  Visual reset every 3.5–5 s (owner, 2026-10-15): a camera move, a new element, a push-in; something moves in every
  frame; no hold over 1.5 s.
- **Determinism:** everything a pure function of time (seeded RNG, no `Date.now`, no `repeat: -1`, no stepped state).
- **Folders:** `video/kavach-railway-reality/<scene_id>/` (e.g. `video/kavach-railway-reality/A3_rfid_tags/`). Reuse
  your own models across your scenes (a shared `_<letter>_lib.js` copied into each folder is fine). Procedural geometry
  is expected; a CC0/CC BY model from a source in PLAYBOOK §9 is fine if logged with its licence in your scene README.
  Run `npm run vendor` (or `node scripts/vendor-assets.mjs`) after creating folders so `vendor/` is populated.
- **Loop:** `npx hyperframes lint` → `check` → `snapshot` → look at every PNG at full size → fix → repeat until it
  looks premium; then render: `npx hyperframes render --workers 3 --output <id>.mp4` for 3D (`--workers 4` for 2D).
  Start renders detached: `setsid nohup … < /dev/null > render.log 2>&1 & disown` and watch with Monitor (CLAUDE.md
  cloud traps). One render at a time.
- **Check each render:** `ffprobe` duration = spec duration (±1 frame), 1920×1080, 30 fps; contact sheet
  (`python3 scripts/contact_sheet.py <mp4> --out <dir> --every 1`) and look at it; fix and re-render anything that looks
  cheap, flat, aliased, too dark (no near-black frames: keep mid-tones lifted), or unreadable on a phone.
- **Deliver:** upload every final MP4 and its contact sheet with
  `scripts/upload_gdrive.sh --sub kavach-railway-reality/scenes/<session letter> <files…>`. Commit only code, READMEs
  and small previews (`preview.jpg` ≤ 500 KB) to your branch `kavach-scenes-<letter>`; never commit MP4s. Push; open no
  PR (the coordinator merges).
- **Report** (your final message): per scene: id, final duration, Drive link, render time, anything you could not do as
  specified and why. Same effort and quality as a single dedicated session: never lower it to finish sooner.
