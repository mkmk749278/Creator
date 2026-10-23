# R1 hangar clip v2: independent review (fresh eyes)

Clip: `video/jet-engine-bet/R1_hangar_v2_with_VO.mp4` (41.3 s, 1920x1080, 30 fps). Judged only from 30 extracted frames (every 2 s plus the extra timecodes) in `/tmp/review_r1v2/`. The voice-over was ignored. No other repo files were read.

## 1. Scores

- **Realism: 3.5 / 10.** The hangar architecture reads as a believable CG space, but every hero object (jet silhouette, paint, gear, nozzle, engine bay) is visibly a primitive-built mock-up. The stop, which is the longest hold, lands exactly on the worst geometry.
- **Cinematic quality: 5 / 10.** The beat structure is clear and the low walk, the head-on reveal, the tail push-in and the whip-out all read. Camera height and depth of field make the set look like a miniature, and the ending is a medium shot where a wide was promised.

## 2. The ten most damaging remaining defects, ranked

**1. The jet is not a Tejas and not a credible fighter (14-27 s, but visible in every shot from 2 s).**
- What I see: a bulbous egg-shaped nose and a fat round fuselage. At 14-16 s it is a near-perfect sphere with a concentric "CD" panel texture. The wings are thin straight planks at mid-height with no delta planform and no leading-edge root extension. The two intakes are square copper-rimmed boxes on the nose sides that read as loudspeakers (at 16 s they sit either side of the radome). The fin is a flat trapezoid slab.
- Why it breaks realism: the viewer subconsciously reads "toy or kit model". The brief's compound delta wing is absent, so the claim "these are Tejas jets" fails at first sight.
- Three.js fix:
  - Build the fuselage as a lofted `LatheGeometry`/`ExtrudeGeometry` stack of cross-sections, with a pointed, slightly drooped radome and a flat-sided spine.
  - Build the wing as a `BufferGeometry` double-delta: root chord about 7 m, an inner leading-edge sweep of about 60 degrees and an outer sweep of about 50 degrees, with a leading-edge kink and a wing-root extension blended into the fuselage.
  - Move the intakes to a trapezoidal pair under and behind the wing root, not on the nose.
  - Add small canards or LERX only if the reference has them; the Tejas has none.
  - Add a swept, thicker fin with a rudder split.

**2. Paint and material read as dark bronze chrome, with a left/right mismatch (2-27 s).**
- What I see: at 2 s the left row of jets is near-black olive and the right row is chalk white. At 17-27 s the near jet is a dark gunmetal with a mirror-chrome canopy and thin dotted white "panel lines" that look like a wireframe or stipple overlay.
- Why it breaks realism: real aircraft paint is semi-matt grey with a broad, soft specular. This looks like polished metal reflecting an almost empty environment. The inconsistency across rows reads as two different models.
- Three.js fix:
  - Use `MeshPhysicalMaterial` with `color` about 0x8d969b, `roughness` 0.42, `metalness` 0.0, `clearcoat` 0.6 and `clearcoatRoughness` 0.25.
  - Drive panel lines from a baked normal and AO map (engraved, not drawn lines), mip-mapped, with anisotropy of at least 8.
  - Give the canopy `transmission` 0.9, `thickness` and `ior` 1.5 over a dark interior, instead of chrome.
  - Light both rows from the same HDRI so left and right match.
  - Add IAF markings: roundel, tail flash and a serial in stencil.

**3. The 5-second "real stop" (20.7-25.4 s) holds on floating, flat parts.**
- What I see:
  - The main wheels are flat black discs with no tyre sidewall, hub or strut.
  - A black ellipse floats in mid-air under the fuselage (about x 930, y 850 at 22-26 s) and a black card hangs near x 1170, y 800.
  - A flat white slab sticks out in front of the canopy (about x 530-900, y 370-410) like an unrendered plane.
  - The red tag on the nose gear is a bright flat rectangle.
  - Frames at 22, 24 and 25 s are almost identical, so these flaws are on screen for about 5 s.
- Why it breaks realism: this is the closest, longest look, and it is the part that exposes the model. Floating geometry is the clearest "CG" tell.
- Three.js fix:
  - Make wheels from a `LatheGeometry` tyre profile (shoulder, sidewall and tread grooves) with a hub cap and a visible brake disc.
  - Attach the struts and doors to the fuselage. Delete or re-parent the orphan mesh (probably a gear door or a shadow proxy that has lost its parent).
  - Replace the white slab with a canopy sill and frame, with seals, in dark rubber.
  - Add contact shadows with `PCFSoftShadowMap`, `shadow.bias` about -0.0005 and `normalBias` 0.02.
  - Add a very small camera drift of about 3-5 cm and a handheld micro-sway, so the stop is "still" but alive.

**4. The engine bay does not read as an engine bay (30-34 s).**
- What I see:
  - At 30 s the nozzle petal ring is detached from the tail can by a visible gap with sky showing through (about x 1000-1100, y 380-700).
  - At 31 s a white overexposed octagonal prism hangs at lower right (about x 1100-1240, y 600-840).
  - Inside, the bay is identical concentric hoops (a slinky). A ring of emissive white dots with a thin white bar looks like a wall clock.
  - A grey "T" block and a flat red rectangle are primitive boxes. Four rubbery cables sag from the lower edge. A black diagonal strap runs across the top.
- Why it breaks realism: the empty bay is the story's key image, and it looks like a sci-fi tunnel with a clock face.
- Three.js fix:
  - Build the bay as a heat-shield tube with longitudinal ribs and a single mount ring. Make the bolt heads dark steel with `roughness` 0.5, not emissive.
  - Add engine mount rails and trunnions, a fuel line and a harness with sensible clamps. Add a visible empty mounting cradle and an open firewall at the front.
  - Re-attach the nozzle petals to the case (same parent, proper pivot).
  - Delete the octagon (or give it a proper cylinder lamp with a bulb, shade and a soft light).
  - Add a warm inspection lamp with a `SpotLight`, `penumbra` 0.7 and decay 2, so the bay is lit from one believable source.
  - Add a few particles of dust in the beam.

**5. Scale: the camera is too low, so the whole hangar reads as a miniature (2-13 s).**
- What I see: the camera sits near floor level (about 0.4-0.5 m). The long lens plus strong blur on one row makes the jets look like 1:48 models. There are no people, no tow tractors, no steps and no hangar furniture for scale.
- Why it breaks realism: real aircraft in real hangars carry human-scale clutter. A tilt-shift look is the "toy" signature.
- Three.js fix:
  - Set the walk camera at `y` about 1.6-1.7 m, with a lowered pitch only for the hero shots.
  - Add scale props: a boarding ladder, wheel chocks, intake and pitot covers with red "REMOVE BEFORE FLIGHT" tags, tow bars, a fire extinguisher on a trolley and a tool chest. Add one silhouetted figure far down the line.
  - Use physical depth of field: 35 mm lens, f/2.8, focus distance equal to the subject, with `BokehPass` circle of confusion computed from depth (both rows in the same focus plane).

**6. Ceiling lights and the lighting model (2-14 s).**
- What I see: rows of identical white capsule lights, bloomed so hard they show black outlines. The central column glitches into stacked "S" and "8" shapes (visible at 2-10 s, for example x 800-960, y 20-260 at 4 s). There are no pools of light on the floor and no reflection of the ceiling lights in the floor or on the jets.
- Why it breaks realism: bright emitters with no light cast read as stickers. A hangar floor is a long mirror of its own lights.
- Three.js fix:
  - Use `RectAreaLight` (with `RectAreaLightUniformsLib`) for each fixture, or bake light maps.
  - Make the floor `MeshPhysicalMaterial` with `roughness` 0.25 and a reflection source (`MeshReflectorMaterial` or SSR, or a baked cube probe).
  - Fix the glitch (probably z-fighting or a duplicated emissive mesh): offset the geometry, raise `camera.near` to 0.3 and use a logarithmic depth buffer.
  - Reduce bloom (strength about 0.35, threshold about 0.9) and add volumetric haze: a few animated fog cards or a `FogExp2` of about 0.012.

**7. Floor posterisation, orange spill and the floor text (2-6 s and 34-40 s).**
- What I see:
  - At 6 s the floor gradient has a jagged contour edge at the bottom (about y 880-930).
  - At 2 s there is a hard orange spill with a flat dark threshold strip below it.
  - "OCTOBER 2026" on the floor is a smeared dotted ghost at 2 s and only half legible at 4 s.
  - At 36-40 s the lower right floor shows lumpy snow-like crescents.
- Why it breaks realism: banding and contour edges are the clearest "real-time" tell. The floor text is not painted on the floor.
- Three.js fix:
  - Use a `HalfFloatType` render target and add dithering (blue noise, about 1/255 amplitude) in the final pass.
  - Replace the orange spill with a soft light cone (a `SpotLight` with a map) or remove it.
  - Paint the date as a real floor stencil: a `DecalGeometry` or a texture with a roughness mask, at 2.2x the current size, with an alpha edge and no smear.
  - Lower the floor normal map intensity (0.3) and use 4096 maps with anisotropy 16 and mip bias.

**8. The exterior at the end of the clip is cardboard (29.5-40 s).**
- What I see: a row of black triangular pine-tree cut-outs on a hard horizon, a flat gradient sky and flat glass windows painted with the same gradient. In an Indian air base, pines read as wrong, and the repeated triangles read as a paper cut-out.
- Why it breaks realism: the final image, the one the viewer remembers, has the weakest background.
- Three.js fix:
  - Use a real HDRI (a dusk apron or airfield from Poly Haven) as `scene.background` and as `environment`, with `backgroundBlurriness` about 0.02.
  - Replace the cone trees with a camera-facing tree-line sprite strip (alpha) with varied heights, or with palms and neem silhouettes, set far enough to be hazed. Add distant lights, a tower and a haze layer.
  - Make the window panes real: `MeshPhysicalMaterial` with transmission or a reflective plane lit by the HDRI, not a gradient texture.

**9. Specular shimmer and aliasing (8-29.5 s).**
- What I see: stippled white dots along the fin edges and fuselage (at 8-10 s a dotted white line runs down the tail edge). Glitter-like sparkles on the tail and wing at 29.5 s. Large hard-edged white dots drift as "dust" (at 36 s they look like snow or dead pixels).
- Why it breaks realism: specular aliasing from high-frequency normal maps swims and sparkles in motion. The dust is the wrong scale and has no light response.
- Three.js fix:
  - Turn on MSAA (4x) plus TAA, or render at 2x and downsample.
  - Apply specular anti-aliasing: raise roughness as normal-map variance rises (Toksvig or a `roughness` floor of 0.3), and clear the dotted line texture.
  - Dust: `THREE.Points` with soft sprite alpha, size about 1-2 px, additive, a small brightness range and visible only in light beams.

**10. The whip-out and the closing image (34-41 s) do not deliver a wide shot.**
- What I see: the blur at 34.2 s is a smear that lands at 34.6 s at a different location and lighting (interior to warm sunset). Then 36-40 s hold a medium shot of one tail and the open door. The "ENGINES SENT 14 OF 99" lower third sits on the left and crowds the jet. The thirty-jet hangar is never re-established.
- Why it breaks realism and the story: the opening promised about thirty jets, and the close shows one. The blur reads as a 2D filter, not a head whip.
- Three.js fix:
  - Animate the camera yaw with an ease-in-out over 0.5 s with real rotational motion blur (accumulate 8-12 sub-frames or use a velocity buffer).
  - Land on a genuine wide: pull back to 12-15 m, 24 mm, at the hangar mouth, so the whole line of jets and the door are in frame, with a slow push over the last 5 s.
  - Move lower thirds off the subject (top left or lower right).

## 3. What works and must be kept

- The idea and the blocking: dark hangar, line of identical jets, the stop, the tail walk and the push into an empty bay is a strong, clear story.
- The 2 s reveal of the hangar (rows of jets, strong one-point perspective down the central aisle, yellow guide lines leading to a dark vanishing point) is the best-looking composition in the clip.
- The head-on frame at 14-16 s with the line of jets behind: a good graphic read, and the symmetry is impactful.
- The nozzle and exhaust can as seen from behind at 29.5 s (warm glow, dark ring) is the most convincing hardware in the clip, and the warm sunset kick from the door is a good colour contrast against the cold interior.
- The colour language: cold blue-grey interior against a warm orange door and sky is cinematic and should stay.
- Film grain and the subtle vignette, and the lower-third styling (clear, restrained, orange accent) are tidy.
- The long-lens compression at 8-12 s makes the line of tails read as "many". Keep the lens, change the height.
- The tunnel push-in as a camera move (31-33.8 s) is smooth and has good momentum.

## 4. The three changes that would raise the score most

1. **Rebuild the jet's silhouette and materials (defects 1, 2 and 3).** A true compound-delta wing, side-mounted intakes, a pointed nose, proper wheels and a grey semi-matt clearcoat paint with IAF markings. This alone could move realism from 3.5 to about 5.5.
2. **Raise the camera and fix the light and floor (defects 5, 6 and 7).** Eye-height camera, scale props, physical DOF, rect-area lights, a reflective floor and dithering. This removes the "miniature" look and the banding, and is worth about +1.5 on both scores.
3. **Rebuild the empty engine bay and the closing environment (defects 4 and 8).** A believable bay (ribs, mounts, rails, a single warm lamp, a reattached nozzle) and a real HDRI sky. These are the payoff and the last image, so they carry the biggest emotional weight per second.

## 5. Camera and editing notes against the beats

- **Door rises 0-2 s.** Frame 0 is a black slab with two faint lines and three dots, with no sense of a door's mass. By 2 s the door is already fully gone and the hangar is revealed with a hard lip at the bottom. Add visible slats, a light slit growing along the floor, dust and a gentle rising shadow edge. Hold the black for 4-6 frames only.
- **Walk in (2-8 s).** The camera glides smoothly at about 0.5 m high with no footstep rhythm. Raise to about 1.6 m and add subtle bob (about 2 cm at 1.8 Hz) and a micro yaw. Motion is acceptable, but the height makes it a drone-like crawl. The 2 s frame has an almost empty centre aisle; consider pulling the first jets closer to the lens for a faster sense of parallax.
- **Line of jets with long lens 8-13 s.** The compression is good, but the shallow depth of field blurs the right row only (at 2 s it is a fake tilt-shift) and makes the rows look like a model railway. Keep the long lens, put both rows in the focus plane, and add a gentle rack from the near nose to the far tails. The lower third "JETS BUILT ABOUT THIRTY" fits here, but it sits in the same place for 9 s; fade it out by 13 s.
- **Arc round the nose 13-20 s.** The head-on frame at 14-16 s is strong, but 16 and 17 s are almost the same, so the arc "waits" and then moves at 17-18 s. Even the speed of the arc with an ease-in-out. The wide lens at 17-18 s exaggerates the nose and the intake boxes (the "speaker" look); use 35-40 mm for the hero nose to flatter the shape.
- **Real stop 20.7-25.4 s.** The stop itself works (the move ends dead), but 22, 24 and 25 s are the same frame with the most visible flaws (floating discs, white slab, flat wheels). Either fix the geometry (defect 3) or shorten the hold to about 3 s and add a slow push of 2-3% so it breathes. The lower third "DELIVERED TO THE AIR FORCE: 0" overlaps the nose-wheel tyre (22-26 s); move it to the right or top.
- **Walk to tail 25-30 s.** The pass along the fuselage at 27-28 s is the first moment the light changes in an interesting way (the wing's sky reflection at 27 s); keep it. But the wing underside at 27 s has a blown pale-blue patch with a posterised edge, and the cut to the sunset at 29.5 s is abrupt: the interior light changes between 28 and 29.5 s without a motivating source. Show the door light spilling in during the walk so the change is earned. The walk is fine in pace.
- **Bay push-in 30-33.5 s.** The move is good, but the first frame at 30-31 s (nozzle ring gap, glowing octagon) breaks the illusion before the tunnel begins. By 32-33.8 s the image looks like a clock face in a pipe. Fix defect 4, add a slight roll (about 2 degrees) and more parallax from the ribs as you pass them, and slow down in the last second so the bay has time to "land" as empty.
- **Whip-out 34-41 s.** The whip is 1-2 frames of 2D smear and a lighting jump, not a camera move. Then the remaining 6 s sit on a medium shot with a new lower third. Make the whip a real 0.5 s yaw with rotational blur, land on the true wide (all the jets and the open door), and let the last 4 s be a slow push so the "bet" image is the hangar full of jets with no engines.
