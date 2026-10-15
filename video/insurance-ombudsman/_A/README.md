# Session A scenes: The Insurance Ombudsman (Episode 02)

Five scenes from `projects/insurance-ombudsman/scenes.md`, built in this film's palette ("the third door").
Each composition is generated: edit `_A/<scene>.src.html` (+ shared `kit.css` / `kit.js`), then `python3 _A/build.py`.

| Clip | VO window (film s) | Length | Composition range |
|---|---|---|---|
| `A1_staircase_O002.mp4` | 15.69–36.89 | 21.70 s | A1_staircase 0–21.70 |
| `A1_staircase_O009.mp4` | 83.17–89.29 | 6.62 s | A1_staircase 21.70–28.32 (alternative to A2's O009) |
| `A1_staircase_corner.mov` | chapter 2–3 callbacks | 6.00 s | ProRes 4444 with alpha, lower-left corner |
| `A2_three_doors_O006…O010.mp4` | 60.10–108.88 | 4.42 / 6.86 / 12.19 / 6.62 / 19.66 s | one continuous scene, local = film − 59.85 |
| `A3_claim_cut_O005.mp4` | 46.92–59.63 | 13.21 s | whole |
| `A4_email_stamp_O004.mp4` | 43.73–46.50 | 3.27 s | 0–3.27 |
| `A4_email_stamp_O025.mp4`, `_O026.mp4` | 248.85–258.08 | 6.11 / 3.66 s | 3.27–9.38, 9.34–13.00 |
| `A5_bima_tracker_O017.mp4` | 158.97–182.01 | 23.54 s | whole |
| `A6_gro_email_O029/O030/O031.mp4` (v2) | 277.15–303.14 | 7.19 / 14.96 / 4.42 s | one scene, local = film − 276.90 |

Every clip = window + 0.25 s handle each side, 1920×1080, 30 fps. Beats are timed from the sentence timings in
`timing.csv` plus silencedetect pauses inside the long sentences (O005, O008, O010); each source file lists its beats.

## Rebuild
```bash
_A/make_plates.sh                 # blurred backplates from the owner's asset pack -> <scene>/media/ (gitignored)
python3 _A/build.py && (cd ../.. && node scripts/vendor-assets.mjs)
_A/render_queue.sh A1_staircase A1_staircase_corner A2_three_doors A3_claim_cut A4_email_stamp A5_bima_tracker
_A/cut_clips.sh                   # per-window clips + 4-frame contact sheets -> _A/out/
```

## Media and labels (for media_manifest.csv)
- Backplates (pre-blurred, graded): owner's Pexels clips F07 (A3, A2 O010), F02 (A4 O004), F09 (A4 O025-26), F10 (A5, A6 at a different section);
  Pexels licence, source URLs in `projects/insurance-ombudsman/handoff/asset-pack/FOOTAGE_REGISTER.csv`. Blurred to
  depth-of-field plates; no person is identifiable as part of any real event.
- Everything else is drawn in HTML/SVG: no AI images. Labels: `EXAMPLE` (A3), `SIMULATION` (A2 O008 agreement, A4 email,
  A3 letter watermark). Invented: "Sample Health Insurance" (as Episode 01), claim no. CLM-2408-55217.

## Revision v2 (owner's preview notes, `projects/insurance-ombudsman/revision-v2.md`)
Every paper now carries real, readable SIMULATION text from the revision's documents (no grey bars):
D1 settlement advice (A3 letter, A4 O004 opened email), D2 recovery agreement with the fee line highlighted (A2 O008),
D3 Bima Bharosa ticket + the insurer's reply (A5), D4 GRO email typed in VO order (new A6), D5 complaint under the
RETURNED stamp with "Representation to insurer: NOT ATTACHED" (A4 O026), D7 award text on the A2 O010 desk.
Re-rendered: A2 O008 (and O010, whose desk papers were grey bars too), A3 O005, A4 O004 + O026, A5 O017, new A6.
Not re-rendered (unchanged; small case-file icons only): A1 O002/O009, A1 corner, A2 O006/O007/O009, A4 O025.
Plates fixed: the slowed backplates were capped at their source length (`-t` after `-i`); now full length.
