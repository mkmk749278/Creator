# C1_empty_bay: The empty engine bay

Session C scene for *The Jet Engine Paradox* (program 15.18–20.88, 5.70 s, 1920×1080, 30 fps). Spec and cues:
`projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1PUG-zl6Bm7jF3S71mAZ1C8yWPeDxeTNP/view

0–1.55 s: the photo slot under a slow push (1.00 → 1.10 over the scene). 1.55–2.45 s: a scan line wipes the blueprint
paper in over the photo (paper at 84 % so the photo still shows through). 1.75–4.45 s: the generic single-engine delta
fighter draws itself stroke by stroke (hot pen tips, construction lines, a length dimension) under a slow 3D camera
drift; 3.55–4.45 s the engine bay draws in hot amber and from 3.9 s glows as an empty cavity. Label `TEJAS MK1A · HAL`
at 3.45 s ("fighter jets").

Cue (word times inside the line are estimated by character position; no word-level alignment exists):
- +0.15–5.30 J004: “And yet... in hangars in Bengaluru and Nashik, brand new fighter jets are waiting.”

## Parameters (`params.js`)
| key | meaning |
|---|---|
| `photo` | path of the real hangar photo (relative to this folder). `""` renders the neutral PHOTO SLOT plate. |
| `photoPos` | CSS `object-position` for the photo (it is cropped to fill 1920×1080 and pushed in 10 %) |
| `label` | lower-left label text |
Re-render after setting the photo: `npx hyperframes render --workers 4 --video-bitrate 16M --output C1_empty_bay.mp4`.

## Notes
- Tag ILLUSTRATION (and the logo bug) are added by the assembler; both right corners are left clear.
- Code: `index.html` + `_bp.js`, `_c.css` (copies of `../_c_lib/`; edit there and run `../_c_lib/sync.sh`) + `jep.css`.
  The airframe is procedural and generic (a tailless compound delta with side intakes), not traced from any HAL drawing.
- Render (pinned 0.8.103, 4 workers, canvas 2D): 17 s wall for 5.7 s.
