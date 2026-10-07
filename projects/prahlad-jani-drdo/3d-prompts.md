# 3D / AI animation prompts: Prahlad Jani & DRDO

These prompts produce **abstract anatomy, schematics and sci-art only**. Never use them to generate an
image of Prahlad Jani, the doctors, the hospital or "archival" footage. Viewers must never mistake an AI shot
for real evidence. Log every generated clip in `credits.md` (tool, prompt ID, date).

Global look (append to every prompt):
> cinematic documentary, 16:9, 4K, shallow depth of field, volumetric light, film grain 3%, color grade deep
> teal / slate / navy shadows, accent color per scene, no text, no logos, no watermark, no human faces

Negative prompt (for tools that support it):
> text, letters, watermark, logo, face, realistic person, cartoon, low poly, oversaturated, flicker, morphing anatomy

Target clip length: 4–6 s each (the EDL cuts every 2.5–3.5 s). Generate 2–3 variations per ID.

---

## P1: Kidney failure vs. normal filtration ("the 3-day rule")
**EDL slots:** B1-03, B1-04 · **Accent:** toxic amber vs. clean cyan

- **P1a (healthy):** Photorealistic macro cross-section of a human kidney, glowing cyan blood flowing through
  branching arterioles into nephron glomeruli, clear filtrate droplets forming, slow dolly forward through the
  renal cortex, Octane render, subsurface scattering, wet organic textures.
- **P1b (shutting down):** Same kidney cross-section under severe dehydration: capillaries visibly constricting,
  blood thickening and darkening to deep maroon-amber, crystalline urea needles accumulating in the tubules,
  flow slowing to a stall, light dimming, slow push-in, ominous, Unreal Engine 5 cinematic.
- **P1c (split transition):** Split frame, left healthy cyan kidney, right dehydrated amber kidney, a vertical
  scan line sweeping left to right converting healthy tissue to dry cracked tissue.

## P2: The sealed room surveillance grid
**EDL slots:** B1-11, B2-04, B2-06 · **Accent:** clinical green + red REC
*Better built in HyperFrames/After Effects than AI-generated (exact, controllable). Prompt is a fallback.*

- **P2a:** Isometric 3D architectural wireframe of a small hospital isolation room on a dark navy void: single
  bed, observer chair, sealed bathroom door crossed with yellow-black caution tape, two ceiling CCTV cameras
  projecting translucent green laser frustums that sweep the room, glowing cyan blueprint lines, slow 90° orbit.
- **P2b:** Close-up of a ceiling CCTV dome camera in a dim corridor, red recording LED blinking, green scanning
  grid projected onto the floor, dust in the beam, slow rack focus.
- **P2c:** Industrial water valve being closed and a pipe cut and capped, metallic macro, cold teal light,
  droplets falling and stopping (illustrates "zero water connection").

## P3: The bladder anomaly (the ultrasound mystery)
**EDL slots:** B3-01 to B3-04 · **Accent:** sonography grey-green + amber fluid

- **P3a:** Translucent 3D anatomical model of a human urinary bladder floating in dark space, faint amber
  fluid slowly pooling at the base, holographic medical-scan lines passing over it, slow orbit.
- **P3b:** Stylised grayscale ultrasound sonography view, fan-shaped scan sector, a dark fluid pocket visible in
  the bladder, then slowly fading over time (time-lapse feel), CRT phosphor grain. *(Label on screen as
  "illustration". Use real scan images only if they are published and licensed.)*
- **P3c:** Microscopic zoom through the bladder wall into the layered transitional epithelium, amber fluid
  molecules diffusing between cells into a surrounding red capillary network, particles flowing away in the
  bloodstream, macro biology, depth of field. *(This shows the claim made in 2010; it is not established
  physiology. The VO/on-screen text must say "the doctors' hypothesis".)*

## P4: Cellular autophagy & mitochondrial recycling
**EDL slots:** B3-09 to B3-12 · **Accent:** bioluminescent gold/teal

- **P4a:** Inside a human cell, cinematic micro-world: a double-membrane autophagosome engulfing a damaged
  mitochondrion and protein debris, then fusing with a glowing lysosome, contents dissolving into golden
  particles, Octane, volumetric, molecular-biology documentary style.
- **P4b:** Healthy mitochondria pulsing with soft gold light, energy particles streaming out through the
  cytoplasm into a blood vessel, slow tracking shot.
- **P4c:** Pull back from a single cell to a tissue, then to a full translucent human silhouette whose neural
  and vascular circuits glow (outro bridge, see P6).

## P5: Measured water (macro beaker)
**EDL slot:** B2-08 · **Accent:** sterile white + clinical green

- **P5a:** Extreme macro of single water droplets falling from a glass syringe into a graduated laboratory
  beaker, millilitre markings in sharp focus, sterile white light, slow motion 240fps look, clean.
- **P5b:** A wet sponge being squeezed over a graduated cylinder, droplets counted, clinical lab bench.

## P6: Philosophical outro (glowing body)
**EDL slot:** B3-15 · **Accent:** saffron to teal

- **P6a:** Wide cinematic shot of a translucent human figure seated in meditation posture against a dark
  cosmos, internal neural and vascular networks glowing saffron and teal, slow breathing pulse of light,
  particles rising, slow push-in. *(Abstract figure only, no face, not a likeness of Prahlad Jani.)*

## P7: Hook & context backgrounds (optional)
- **P7a:** Cracked dry earth time-lapse under harsh sun, heat haze, slow aerial push (hook, Day 1→4).
- **P7b:** Abstract dark-navy data field with drifting particles and faint grid (background behind kinetic text).
- **P7c:** Stylised satellite-style 3D globe in dark teal, camera diving toward the Indian subcontinent with glowing
  city points (DRDO map zoom). *(Or build it in HyperFrames from a public-domain map; that is safer and exact.)*
