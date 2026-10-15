# Scene sessions brief: The Insurance Ombudsman (Episode 02)

You are one of three parallel scene sessions (A, B, C). The coordinator (S0) does the real footage, web captures,
Episode 01 glimpses, music, assembly and review. Read, in order: `CLAUDE.md`, PLAYBOOK §5 (the look), §9 (realism),
§10 (HyperFrames gotchas), this file, the README of this project (genre, palette, series continuity), then your scenes in
`scenes.md` (exact VO windows from the real Akash VO, film seconds). Load the `/hyperframes` skills before writing any
composition. The script and facts are locked and fact-checked (`claims.csv`, 37/37): **do not change any on-screen
number or wording.** If a spec line looks wrong or impossible, write it in your report instead of improvising.

## The world: "the third door"
Daylight Indian home and desk; the case file and a phone are the protagonists; the law appears as warm paper documents
under a forensic magnifier. Premium explainer quality (Vox, Polymatter, Johnny Harris), never slides, clip-art, glass
cards, neon dashboards, icon grids or a centred title + subtitle (PLAYBOOK §5.1).
- **Palette** (from the owner's G01–G08 SVGs in `assets/owner/BP_HLTH02_Asset_Pack/graphics/`, gitignored: copy them from
  Drive `Creator/English/insurance-ombudsman/BP_HLTH02_Complete_Asset_Pack.zip` with `rclone` as in
  `scripts/upload_gdrive.sh`, or rebuild from the SVG descriptions in `handoff/asset-pack/CLAUDE_VISUAL_HANDOFF.md`):
  night navy `#0B1422` / `#14263B`, signal yellow `#FFDB59` (money, clocks, our calculations), teal `#59DCC3` (the
  Ombudsman route, the rules), paper white `#F5F7FB`, mist `#B8C7D9`, coral `#FF7D80` only for cuts and the RETURNED stamp.
- **Materials:** real paper (grain, soft shadow, slight curl), light from a window (warm key, cool fill), shallow depth
  of field via pre-blurred layers, 30% vignette, fine film grain, a slow camera drift or push-in in every shot.
- Use the owner's graphics as **layouts and named SVG groups to animate**, never as a static PNG on screen.
- Text ≤ 15% of the frame; tags as given in `scenes.md` (`[SOURCE | DATE]`, OUR CALCULATION, EXAMPLE, SIMULATION,
  ILLUSTRATION) in a small lower-corner label. Numbers in Indian format (₹4,50,000; ₹1,50,000). Tabular figures.
- No real insurer, hospital, agency or person names; invented policy/claim numbers; no real OTP, phone or Aadhaar.

## Technical rules (CLAUDE.md, HyperFrames 0.8.103)
- One folder per scene: `video/insurance-ombudsman/<scene>/` (e.g. `A2_three_doors/`), 1920×1080, 30 fps, one paused GSAP
  timeline at `window.__timelines["<scene>"]`, pure function of time, vendored GSAP/fonts only (`npm ci` vendors them).
- **Durations:** for each VO window listed under your scene, render one clip `<scene>_<id>.mp4` lasting the window
  length + 0.5 s (0.25 s handle each side); several windows may share one composition with a `data-start` offset.
  Key beats land on the word the window's VO says (time them from the window start in `scenes.md`).
- Loop: `npx hyperframes lint` → `check` → `snapshot` → look at the PNGs → fix; then render `--workers 4`, `-crf`-capped.
  Start renders with `setsid nohup … < /dev/null & disown` and watch with Monitor (CLAUDE.md cloud traps).
- Make a 4-frame contact sheet per clip and look at it before delivering.

## Deliver
1. Upload clips + contact sheets: `scripts/upload_gdrive.sh --sub English/insurance-ombudsman/scenes/<session> FILES…`.
2. Commit only source (compositions, no MP4) on your own branch `scenes-io-<session>` and push; open no PR (S0 merges).
3. Report: clip list with durations, anything you could not do, anything that looked wrong in a spec.

| Session | Scenes |
|---|---|
| A (story) | A1_staircase, A2_three_doors, A3_claim_cut, A4_email_stamp, A5_bima_tracker |
| B (money and clocks) | B1_fee_split, B2_two_step_clock, B3_penalty_meter, B4_time_stats |
| C (filing and proof) | C1_filing_stepper, C2_offices_board, C3_document_slots, C4_binding_award, C5_proof_magnifier |
| S0 (coordinator) | footage edit, cioins.co.in / Bima Bharosa / Rules PDF captures, Episode 01 glimpses, music, assembly, review |
