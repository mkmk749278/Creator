# Visual plan v1: reuse first, build only the gaps (owner, 2026-10-22)

Owner: "use what we have in the repo for the original video, refine it, gather what is missing, use Three.js, cinematic level."
Source of truth for what exists: `video/jet-engine-paradox/` (44 compositions on a shared Three.js stack, `_libA/jepA.js`),
their rendered MP4s on Drive `Creator/English/jet-engine-paradox/scenes/{A,B,C,D}`, the owner-fetched official clips in
`.../sources/` (pulled to `projects/jet-engine-bet/assets/legacy/`, gitignored), and the old 4K film for reference.
Screenplay: `screenplay.md` (v2, "The Walk-Around"), timed to `final/align/align.json`.

## What exists and how it is used in the new film
| Screenplay room / beat | Reuse from the repo | Refine | Gap to build (Three.js) |
|---|---|---|---|
| R1 Hangar walk-around, exhaust push-in (0:00–0:41) | `C1_empty_bay` (Tejas wireframe), `D5_engines_jets` (14 of 99 bar), DD India / PIB Nashik clips for cutaways only (news lower-thirds must be cropped) | New camera, new look | **Hangar + Tejas + nozzle tunnel, procedural, cinematic lighting** (nothing like it exists) |
| Moon / satellites / supercomputer beat (0:42–0:59) | ISRO clips in `sources/` (DLA_64yz8Ss, q2ueCg9bvvQ) | Short match-cuts | Supercomputer rack (3D, small) |
| R2 Engine journey, air-molecule POV (1:19–2:23) | `A2_engine_dive`, `A4_combustor_flow`, the whole `buildEngine`/`buildHotSection`/`gasStream` kit in `jepA.js` | One continuous 64 s camera path instead of 6 s fragments; "squeeze" tightening, fire flash, release stretch | The continuous path and the four SUCK/SQUEEZE/BURN/BLOW beats |
| R3 Blade (2:23–4:15) | `A3_blade_rise`, `A5_thermal_reveal` (gauge exists), `B2_polycrystal`, `B3_creep`, `B4_single_crystal`, `B5_alloy`, `B6_cooling_channels`, `B7_film_cooling` (already macro-skim), `B8_tbc` | Retime to the new voice-over; add inside-the-metal flythrough camera; what-if melt shot | "Blade turns to water" shot; blade-skim extension |
| R4 Spin (4:15–5:27) | `A6_spin_bus` (disc + RPM gauge + bus), `D7_engine_club` (globe), `D13_hours`, `D6_bomb_space` | **Rim-cam** camera; bus at scale | Rim-cam path; rocket-vs-jet split |
| R5 Gallery (5:27–8:31) | `D2_squadrons`, `D3_orders`, `D1_globe_lynn`, `D4_promise`, `C3_sanctions_wireframe`, `C4_kaveri_blueprint`, `C5_thrust_target`, `C7_blueprint_tear`, `C8_dry_kaveri`, `C9_amca_engines`, `D15_china`, proof pages, owner clips (MiG-21, Aero India) | Put each in a "doorway" with a time-corridor dolly; fix numbers to the new script (110 to 120 kN etc. only if the owner's text keeps them) | Corridor/doorway transitions; Delhi decision-room set |

## Build order
1. **R1 hangar** (missing and it opens the film) → snapshots → review.
2. **R2 engine journey** from `jepA.js` (the hero of the film).
3. **R3** retimes and the two new shots (inside-the-metal, melt).
4. **R4** rim-cam. 5. **R5** doorways with existing scenes. 6. Assemble to the voice-over, grade, grain, sound, review (PLAYBOOK §14).
