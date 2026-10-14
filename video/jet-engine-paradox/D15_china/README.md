# D15_china: China's road

Session D scene for *The Jet Engine Paradox* (program 493.43–503.92, 10.49 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/19BZXqTGDMCkHVzQN6zFWHyFEhftTETNI/view · contact sheet: https://drive.google.com/file/d/1D3wc_-OV7e1C7XEcVFXVDyRVhiwJh5f_/view

A J-20 photo slot with a slow push-in; years axis without dates whose ticks stream past during "decades, and many failures"; chips light in turn RUSSIAN AL-31F → CHINESE WS-10C → WS-15 (earlier ones dim), with J-20: top left.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–10.25 J083: “China walked this same road. Its J twenty stealth fighter used Russian engines at first. It took China decades, and many failures, to switch to engines of its own.” · on-screen `J-20: RUSSIAN AL-31F → CHINESE WS-10C → WS-15`

## Parameters (`params.js`)
`photo` (path of the J-20 photo; empty renders the neutral slate PHOTO SLOT plate), `focus` (push-in target, 0..1), `lead`, `chips`, beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `kit.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- **Photo slot:** put the licensed J-20 photo in this folder (for example `assets/j20.jpg`), set `photo: "assets/j20.jpg"` in `params.js`, log it in the media manifest, re-render. It loads through Three's loading manager, so HyperFrames waits for it; it is cover-fitted with a dark lower scrim for the chips.
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D15_china`): 349 s wall.
