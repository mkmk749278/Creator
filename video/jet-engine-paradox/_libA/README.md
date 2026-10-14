# Session A: thermal-world 3D scenes (The Jet Engine Paradox)

Eight HyperFrames compositions (`../A1_title_blade` … `../A8_verdict_blade`), all built on one procedural model set and
render stack in `jepA.js`, so the science sequence reads as one world ("The Hot Section", thermal world).
All models are procedural and generic (illustrations, not any manufacturer's part): no external models, no textures
beyond the shared library HDRI `library/hdri/studio_small_09_1k.hdr` (Poly Haven, CC0).

## The model set (`jepA.js`)
- **HP turbine blade** `makeBlade()`: twisted, cambered airfoil loft (NACA-style thickness on a Bezier camber line,
  chord taper and twist with span), squealer tip (rim + recessed floor), platform that follows the hub camber line,
  shank with seal lips, fir-tree root with three rounded serrations. Film-cooling hole decals: 5 showerhead rows on the
  leading edge, 2 shaped pressure-side rows, 1 suction-side row, trailing-edge slots. `airfoilAt(u, v)` samples the
  surface (used for holes and the cooling-film particles).
- **Material** `hotMetal()`: physically based nickel-superalloy grey with a procedural roughness map, heat tint, an
  emissive glow that follows a normalised temperature field (hot leading edge and tip, cooled streaks behind the holes)
  and a thermal-camera mode (ironbow ramp, `U.uThermal`). Temperature scale: 1.0 = alloy melting point; the metal stays
  near 0.72, the gas reaches 1.15 (fact-check JE-063 proportions). Also the blueprint→metal sweep used by A2.
- **Hot section** `buildHotSection()`: disc (lathe), 48-blade ring (coarse LOD; hero blade and holes full detail),
  32 nozzle guide vanes, cutaway annular combustor (louvred liners, dilution holes, 20 swirler cups and fuel stems,
  flame jets + volumetric fire), shroud and outer case.
- **Turbofan** `buildEngine()` (A2): spinner, 3-stage fan, 7-stage compressor with stators, the hot section, 2-stage LP
  turbine, afterburner duct with flame holders, nozzle; amber blueprint lines for everything.
- **Effects:** seeded embers, hot-gas particle stream with trails, cooling-film particles, rotor motion-blur ghosts,
  backdrop with haze / drafting grid / hot-gas thermal field, heat shimmer pass, bloom, vignette, ACES, FXAA, film grain
  with lifted slate blacks. Everything is a pure function of time.
- **Bus** `makeBus()`: stylised low-poly red double-decker, no branding or text.

## Workflow
- Edit `_libA/jepA.js`, then `./_libA/sync.sh` copies it (and `_shared/jep.css`) into every scene folder.
- `node scripts/vendor-assets.mjs` (or `npm ci`) vendors three, postprocessing, GSAP, Inter and the HDRI per scene.
- Render detached: `setsid nohup bash _libA/render.sh A6_spin_bus A5_thermal_reveal … < /dev/null > /dev/null 2>&1 & disown`
  (sets `HYPERFRAMES_RENDER_DETACHED=1`, see PLAYBOOK §15). `_libA/finish.sh <id>` probes, makes contact sheets and
  `preview.jpg`, uploads to Drive `Creator/jet-engine-paradox/scenes/A`.
- A7 uses cuts of the A5, A6 and A8 renders as its panels: run `A7_recap/make_media.sh` after those renders.
- `window.BENCH` flags for cost tests: `msaa`, `bloom: 0`, `noShimmer`, `noBlur`, `noFxaa`.

## Measured cost (1080p, 3 workers, pinned hyperframes 0.8.103, 4 vCPU software GL)
A6 one-second slice: 4× MSAA + 7 blur ghosts 398 s per output second; MSAA off 164; LOD ring 127; no clearcoat 107;
no ghosts 42; no bloom/shimmer 35. Shipped stack: FXAA, 4 ghosts only while spinning, LOD ring, no clearcoat.
Per-scene render times are in the session report.

## Notes for the assembler
- No citation tags, ILLUSTRATION tags or logos are drawn in-scene (corners kept clear). All of A1–A8 need the
  ILLUSTRATION tag; A5/A6 need `[ROLLS-ROYCE | 2012]`, A4 `[NASA | ROLLS-ROYCE]`.
- A1 leaves 0–2.5 s clean for the logo sting.
- A5 carries 2.35:1 bars from ~2.4 s (the core reveal); its label sits above the bottom bar.
- `≈` in A6 is an inline SVG (Inter has no U+2248).

## Renders (2026-10-13, 1080p30, 3 workers; Drive `Creator/jet-engine-paradox/scenes/A`)
| Scene | Frames / duration | Render wall time |
|---|---|---|
| A1_title_blade | 413 / 13.77 s | 536 s |
| A2_engine_dive | 188 / 6.27 s | 1314 s |
| A3_blade_rise | 151 / 5.03 s | 217 s |
| A4_combustor_flow | 169 / 5.63 s | 856 s |
| A5_thermal_reveal | 543 / 18.10 s | 2066 s (restart overlap included) |
| A6_spin_bus | 372 / 12.40 s | 697 s |
| A7_recap | 200 / 6.67 s | 482 s |
| A8_verdict_blade | 220 / 7.33 s | 752 s |
Delivery files are re-encoded with `-crf 17 -maxrate 30M` (`finish.sh`); the raw renders are ~120 Mbps.
