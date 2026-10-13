# Scene sessions brief: The Jet Engine Paradox

You are one of four parallel scene sessions (A, B, C, D) for this film. The coordinator session (S0) does the real
footage, documents, music, assembly and review. Read, in order: `CLAUDE.md`, PLAYBOOK §5 (the look), §9 (realistic
animation and the vendored 3D stack), §10 (HyperFrames gotchas), this file, then your section of `scenes.md`
(exact durations and word cues; generated from the real VO timing). The script and facts are locked and fact-checked:
**do not change any on-screen number or wording** in your spec. If a spec line is impossible or looks wrong, write it
in your report instead of improvising.

## The owner's ask for these scenes
"While explaining the science, build crystal clear 3D and animated clips. We need to meet next gen of tech."
That is the bar: a premium, next-generation science documentary (think high-end engine-maker films and top explainer
channels), not slides, not clip-art, not a generic dashboard. Every frame should look like it came from one designed
world, "The Hot Section" (README of the project):
- **Thermal world (A, B):** real-time Three.js, physically based metal (nickel superalloy: warm grey, anisotropic-ish
  brushed highlights, roughness 0.35–0.5), HDRI lighting (`vendor/library/hdri/studio_small_09` from the shared library),
  ACES/AgX tone mapping, bloom on hot parts only, heat shimmer, embers/particles by seeded noise, slow purposeful camera
  moves (dolly, orbit, push-ins; never static). Heat is shown as heat: an ironbow thermal palette or emissive amber, never
  as a bare number. Cool air is the only cyan. Depth of field via pre-blurred plates or subtle focus pulls.
- **Blueprint world (C):** 1980s drafting-table precision on titanium slate: thin amber line work drawn stroke by stroke
  (SVG stroke-dashoffset or canvas), construction lines, dimension arrows, a faint grid, paper grain, slight parallax
  between layers, a slow camera drift. Generic engineering drawings (labelled ILLUSTRATION by the assembler), never a
  traced copy of a real manufacturer's drawing.
- **Globe and data (D):** a land-only 3D globe (no political borders, Natural Earth land as in
  `video/fireice/benson_map/mkmap.mjs`), lit like a night-side planet with an amber atmosphere rim; arcs as glowing
  great circles; counters and gauges as precision instruments (tabular numbers, tick marks, needles with inertia). No
  floating glass cards, no neon-on-black dashboards, no centred title + subtitle, no icon grids, no emoji (PLAYBOOK §5.1).

## Shared rules for every scene
- **Copy `video/jet-engine-paradox/_shared/jep.css`** into each scene folder and use its tokens and `.jep-label` /
  `.jep-num` classes. Palette: slate `#0B0E14`, amber `#F97316`, red `#EF4444`, ceramic white `#F8FAFC`, cyan
  `#38BDF8` (cooling air only). Font: vendored Inter (add `vendor/fonts/inter-latin-ext-600-normal.woff2` to
  `index.html` if you show ₹ or ≈).
- **Keep corners clear:** the assembler adds the citation tag and the ILLUSTRATION tag in the bottom-right
  (520×170 px) and the logo bug in the top-right (260×160 px). Do **not** draw citation tags, ILLUSTRATION tags or logos
  yourself even though the spec text mentions them; put in-scene labels lower-left (`.jep-label`) or inside the
  graphic. Text ≤ 15% of the frame, 2–4-word labels, numbers and counters.
- **Timing:** each scene is one HyperFrames composition at 1920×1080, 30 fps, whose `data-duration` equals the
  scene's duration in `scenes.md` exactly. Key every beat to the word cues listed under your scene (seconds inside the
  scene); land labels and counters on the words. Something moves in every frame; no hold over 1.5 s.
- **Determinism:** everything a pure function of time (seeded RNG, no `Date.now`, no `repeat: -1`, no stepped state).
- **Folders:** `video/jet-engine-paradox/<scene_id>/` (e.g. `video/jet-engine-paradox/A3_blade_rise/`). Reuse your own
  models across your scenes (a shared `_lib.js` inside your session's scenes is fine; copy it into each folder).
  Procedural geometry is expected (turbine blade = twisted airfoil loft + platform + fir-tree root + cooling-hole rows;
  disc = instanced blades). A CC0/CC BY model from a source in PLAYBOOK §9 is fine if logged with its licence in your
  scene README.
- **Loop:** `npx hyperframes lint` → `check` → `snapshot` → look at every PNG at full size → fix → repeat until it
  looks premium; then render with the repo's pinned CLI: `npx hyperframes render --workers 3 --output <id>.mp4` for 3D
  (`--workers 4` for 2D). Start renders detached: `setsid nohup … < /dev/null > render.log 2>&1 & disown` and watch with
  Monitor (CLAUDE.md cloud traps). One render at a time.
- **Check each render:** `ffprobe` duration = spec duration (±1 frame), 1920×1080, 30 fps; make a contact sheet
  (`python3 scripts/contact_sheet.py <mp4> --out <dir> --every 1`) and look at it; fix and re-render anything that
  looks cheap, flat, aliased, too dark (no near-black frames: keep mid-tones lifted), or unreadable on a phone.
- **Deliver:** upload every final MP4 and its contact sheet with
  `scripts/upload_gdrive.sh --sub jet-engine-paradox/scenes/<session letter> <files…>` (Drive works in new sessions).
  Commit only code, READMEs and small previews (`preview.jpg` ≤ 500 KB) to your branch `jep-scenes-<letter>`; never
  commit MP4s. Push, then open no PR (the coordinator merges).
- **Report** (your final message): per scene: id, final duration, Drive link, render time, anything you could not do
  as specified and why. Same effort and quality as a single dedicated session: never lower it to finish sooner.
