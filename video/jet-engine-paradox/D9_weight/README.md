# D9_weight: 1,100 kg target, 1,235 kg actual

Session D scene for *The Jet Engine Paradox* (program 221.21–225.91, 4.7 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1rr2-r7piwEzONZ6vt0ASHxK8lYEgrhGu/view · contact sheet: https://drive.google.com/file/d/1jG6UAkTPKoSFBshTa5LY4LzShFPBjEt8/view

Precision dial 900–1,400 kg (10 kg ticks). The needle swings with inertia to 1,100 on "eleven hundred kilos" (amber target mark, 1,100 KG TARGET), then on "twelve hundred and thirty five" overshoots and settles on 1,235 while the overweight band glows red (1,235 KG ACTUAL). Live readout under the hub.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–4.43 J036: “It was meant to weigh eleven hundred kilos. It weighed twelve hundred and thirty five.” · on-screen `1,100 KG TARGET · 1,235 KG ACTUAL`

## Parameters (`params.js`)
`range`, `target`, `actual`, labels, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `kit.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.

- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D9_weight`): 173 s wall.
