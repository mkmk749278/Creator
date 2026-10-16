# Session B scenes (Insurance Ombudsman, Episode 02): money and clocks

Scenes `B1_fee_split`, `B2_two_step_clock`, `B3_penalty_meter`, `B4_time_stats` (specs: `projects/insurance-ombudsman/scenes.md`).
Look: "the third door" desk world. A navy linen desk blotter under warm window light (a drifting light plate and dust motes in the
light), real-paper documents (grain tile, contact and drop shadow, curl highlight), a slow camera drift in every shot, 30% vignette,
grain. Text sits in lower-corner scrims or on the paper objects. Colours follow the owner's G01–G08 palette: yellow for money,
clocks and our calculations; teal for the Ombudsman route and rules; coral is not used.

## How the clips are made
Each scene is one composition that holds its VO windows back to back. Each window is the window length + 0.5 s (0.25 s handle
on both sides), rounded to whole frames at 30 fps (an exact .5 frame rounds down). `K.layout([...])` in `index.html` is the
window table, and `v(film_second)` puts a beat on the VO word. Word times come from silencedetect pauses inside the
sentence timings (`timing.csv`).
```bash
b_kit/sync.sh                                  # copy kit.css, kit.js and the plates into each scene's kit/ (after editing b_kit/)
node scripts/vendor-assets.mjs                 # vendor GSAP and fonts (npm ci does this)
cd B1_fee_split && npx hyperframes lint && npx hyperframes check
npx hyperframes render --workers 4 --crf 18 --output B1.full.mp4
python3 ../b_kit/split.py . B1.full.mp4 clips/  # <scene>_<Oxxx>.mp4 per window + a 4-frame contact sheet each
```
`make_plates.py` regenerates `plates/` (seeded, so the output is the same each time). No footage and no third-party media: every
pixel is generated here (CC0 / own work).

## Notes for the coordinator
- B3/O057 has no on-screen text besides its documents, because the spec gives none. (In v1, B1/O020 had a handwritten
  "20% + GST"; v2 highlights the agreement's own fee line instead.)
- B3/O057 is also listed under C4_binding_award: use one of the two.
- The odometer in B3 counts each new day in the last 15% of that day, so every frame you hold on shows an exact multiple of ₹5,000.

## Revision v2 (owner's notes, 2026-10-15; `projects/insurance-ombudsman/revision-v2.md`)
No blank paper: every document shows real, readable SIMULATION text from one invented family and claim. The texts live in
`kit.js` `K.DOCS` (D2 agreement, D5 complaint, D6 insurer reply, D7 award, D8 recommendation, plus two grievance replies),
and any element with `data-doc="<key>"` is filled at load. B1 highlights the D2 fee line on "twenty percent plus GST".
B3 stamps D7 with RECEIVED 15 SEP 2026 on "receiving it". B4 ticks both "agreed" lines on D8, then "Case closed".
The B2 O034 reply letters and B4's month pages ("MONTH 1–3") also lost their grey bars.
