# D6_bomb_space: Nine nuclear states, about ten launchers

Session D scene for *The Jet Engine Paradox* (program 154.44–160.15, 5.71 s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: https://drive.google.com/file/d/1mso9yzSlpBsuHDRLTmhjJr7fy6ouEvn2/view · contact sheet: https://drive.google.com/file/d/1YEncSlj6Zyy6RbAKsZ6P_amUkeLyfxn5/view

Land-only globe. Big 9 / NUCLEAR-ARMED STATES with nine red reticle pulses at the nine states (abstract: no labels, no borders); on "About ten" the counter turns to ~10 / OWN ROCKET TO ORBIT and ten orbits draw around the globe, each with its satellite.

Cues (word times inside lines estimated from pauses in the recorded VO):
- +0.15–5.55 J026: “Nine countries have nuclear bombs. About ten have put a satellite in space with their own rocket.”

## Parameters (`params.js`)
`nuclear` (n, label, pulse positions), `orbit` (n, label, count), beat times `t`.

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `globe.js`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
- Pulse positions are the nine nuclear-armed states in SIPRI's count; the orbits are illustrative (no countries named).
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh D6_bomb_space`): 177 s wall.
