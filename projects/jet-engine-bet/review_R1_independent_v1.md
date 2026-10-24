# Independent review: R1 hangar clip (41 s, 1920x1080)

Reviewed from frames at 0.5 s, 1.5 s and every 2 s, plus 15, 17, 18.5, 19.5, 21, 27, 29, 31, 33, 35, 37 s, plus 4x3 contact tiles over 0-3 s, 14-17 s and 29-35 s. All timecodes are from the file.

## 1. Scores

- **Realism: 2.5 / 10.** This reads as a low-poly game-engine prototype with default PBR and an untextured chrome-ish plastic skin. The hangar layout is plausible, but nothing in it (jets, floor, glazing, door, exhaust) survives a second look.
- **Cinematic quality: 3.5 / 10.** The story beats are there, the lower-thirds are clean and the one-point-perspective opening is a good idea. But the camera path has a glitch, the key payoff shot (the empty engine bay) looks like a smiley face, and the picture has no depth, grade or lens character.

## 2. The ten most damaging defects, ranked

### 1. The "empty engine bay" is a smiley face (30-34 s; also 29 s, 35 s)
- **See:** After the push-in the tunnel is a stack of concentric thin rings. Two white rectangular bars sit near the vanishing point, over a dark disc with a lit crescent beneath it. That reads as two eyes and a grin. It is the single most important image of the story and it is unintentionally comic. The rings are uniform and perfectly concentric, so there is no engine-bay structure: no ribs, bolts, mounting lugs, cable looms, fuel lines, fire-bulkhead or a visible bare engine mount.
- **Why it breaks:** A real empty engine bay is irregular, cluttered and dull-metal. A perfect radial pattern with two symmetric bright pads is read by the brain as a face (pareidolia), and also as a CG tunnel generator.
- **Fix:**
  - Delete the two white bars, or move them off-axis and make them dark-anodised.
  - Build the bay from a `LatheGeometry` or `TubeGeometry` with a noisy radius profile, not equal-spaced rings.
  - Add 3 to 5 asymmetric details: two longitudinal rails at 10 and 4 o'clock, a bulkhead plate with a few bolt-ring instances, a bundle of cables (a `TubeGeometry` along a catmull curve), a mount bracket in the lower third.
  - Use a rough metal `MeshStandardMaterial` (roughness 0.6-0.8, metalness 0.7) with a bump map from a canvas noise texture.
  - Light it with a single narrow `SpotLight` from the camera, at about 0.5 intensity, with fall-off, so the far end goes properly black.
  - Add slight lens breathing and a barrel-style handheld wobble on the push-in.

### 2. Camera clips and rolls through the nose / lights (14.2-15.6 s)
- **See:** The camera dips under the nose, and for about 1.2 s the frame is filled by a huge yellow-cream glowing disc on a dark grey cylinder (the radome / nose seen from below, with a hot specular or emissive circle). The horizon tilts about 60 degrees and the ceiling lights smear. The view ends up flipped. At 14.5-15.5 s two consecutive tile frames are almost mirror images of each other (a V-shaped nose). It looks like the camera passes through the geometry, or an up vector flips during the look-at.
- **Why it breaks:** It is an obvious camera bug, not a move. A first-person walk can't roll like this. The big flat bright disc also has no gradient structure and is shaded like a sticker.
- **Fix:**
  - Replace look-at with a spline for position and a separate spline for look target. Keep the up vector fixed at (0,1,0) and clamp roll to 0 plus handheld noise of at most 0.4 degrees.
  - Give every jet a collision capsule or exclusion radius and keep the camera path at least 0.8 m from the hull.
  - Find the emissive or `lightMap` disc under the nose. If it is a landing-light mesh, make it a small, dim, unlit lens. If it is a spotlight cone, remove it.

### 3. The jets do not look like Tejas, and the model is crude (everywhere from 1.5 s on; worst at 8-27 s)
- **See:**
  - There is no cropped compound delta. The wing is a thin, straight, planklike trapezoid stub with a stiff rectangular tip rail.
  - The cockpit canopy is a black flying-saucer disc, a flat ellipsoid with a glossy black material and a brown hose-like spot in it. It floats above the spine.
  - The nose is a two-tone cone: a pale khaki band and a grey tip with a jagged, aliased boundary (z-fight or per-pixel texture seam, 10 s, 12 s, 17 s, 38 s).
  - Wheels are flat black cylinders with chrome stick struts. The red tag on the nose strut is a plain red box.
  - The intake is a dark disc glued on the side.
  - From behind (36 s, 38 s) the wing and tailplane look like paper-thin planks.
- **Why it breaks:** The jet is the hero. It reads as a toy or a generic 1960s trainer, not a modern Indian light fighter. Any aviation viewer will reject it in 2 seconds.
- **Fix:**
  - Rebuild the planform from a `Shape` extrusion with a leading-edge dogtooth (a double-delta with a LERX), thickness taper (use `ExtrudeGeometry` with a bevel), and an airfoil section.
  - Build the canopy as a smooth teardrop `SphereGeometry` scaled 1:0.45:2.5, with a frame (two thin torus arcs) and a dark-tint transmissive material (`MeshPhysicalMaterial`, transmission 0.9, thickness 0.02, ior 1.5, attenuation colour). Add a seat and headrest silhouette inside.
  - Shape the intake as a 2D-offset, lipped DSI or box intake (a ring with a thin lip, a splitter plate, and a dark interior with a gradient).
  - Add panel lines with a normal or bump map from a canvas, plus a `roughnessMap` with streaks.
  - Use a proper roundel decal and a tail flash from `DecalGeometry`.
  - Add wheel hubs, tread, oleo links and gear doors.
  - Replace the jagged nose seam with a vertex-colour or UV-driven gradient with a soft 5 mm transition.

### 4. Windows and the end door are flat unlit colour planes (1.5-27 s windows; 31-40 s door)
- **See:**
  - The clerestory windows are flat light-blue rectangles (about #6f9fe0) in a night-black hangar, with no frame depth. The interior is dark, yet the windows are bright daytime blue, so the lighting is inconsistent.
  - At 31 s and from 35 s on, the rear opening is a huge flat white-grey rectangle, blown out, with a visible pale elliptical halo on it and the ground (a "sky dome" disc edge). There are no light shafts, no depth, and no horizon.
  - The hard-edged elliptical halo on the door is also visible at 31 s and 35 s.
- **Why it breaks:** Windows and door are the largest bright areas and give away the CG at a glance. They also cancel the intended moody low-key look.
- **Fix:**
  - Make window planes emissive but graded (`MeshBasicMaterial` with a vertical gradient `CanvasTexture`: deep blue-black at the top to dusk orange at the bottom) and add 4 cm window frame boxes with mullions.
  - Use an equirect HDRI (a dusk sky, `RGBELoader`) as `scene.background` and `scene.environment` with a controlled `environmentIntensity` of about 0.25.
  - Make the door opening a real void: sky gradient, a distant treeline silhouette, a runway with edge lights, and an apron. Expose it so the highlights sit near, not above, white (use `ACESFilmicToneMapping`, exposure ~0.8).
  - Add volumetric god-rays (a fake cone mesh with an additive gradient, or a screen-space `GodRaysEffect` in `postprocessing`).
  - Remove the elliptical halo: it is a transparent disc or a lit floor spot with a hard edge.

### 5. The floor: hard-edged light pools, flat lighting and no contact shadows (2-27 s)
- **See:**
  - Pale elliptical pools with sharp edges (2 s, 6 s, 10 s, 15 s, 22 s). The ellipse arcs are visible on the floor and look like cutout stickers.
  - Glossy reflections streak in odd flat shapes (31 s, 36 s: a bright vertical white streak that doesn't match any light).
  - Jets float: there is no contact shadow, no ambient occlusion, and no tyre contact patch (6 s, 8 s: the main wheels hover above the floor).
  - The tile joints are a single grid with no expansion-joint variation, no stains, no oil, no scuffs, no tyre marks.
  - "OCTOBER 2026" stencilled on the floor (1.5-6 s) is crisp white and reads as a title decal laid on top, with aliasing at 1.5 s. It is also inconsistent with the concrete's roughness.
- **Why it breaks:** The floor fills a third of the frame. Without grounding, the aircraft look pasted in.
- **Fix:**
  - Replace the spot-light pool ellipses with soft `SpotLight` cones (angle 0.9, penumbra 1.0, decay 2) or an area-light feel with `RectAreaLight` plus `RectAreaLightUniformsLib`.
  - Add `ContactShadows` or per-jet blob shadows, and bake a soft AO texture under each aircraft. Enable `PCFSoftShadowMap` on the key lights, or use SSAO / GTAO in post.
  - Set floor roughness 0.45 with a `roughnessMap` of noise and tyre-streak decals, add a normal map, and use `MeshReflectorMaterial`-style blurred reflections at low strength.
  - Give wheels a pressed-contact compression and make sure `y` places the tyre bottoms exactly at floor level.
  - Render the title as a projected decal with roughness variation and slight wear, or move it to a screen-space overlay.

### 6. Ceiling lights have dark outlines and a cheap bloom (1.5-15 s)
- **See:** White tube lights surrounded by a black halo ring, then a pale outer glow, like a sticker with a stroke (2 s, 4 s, 8 s, 14 s). The halo is a dark outline, not a glow. The ceiling trusses behind them are murky stripes and a brick-like grid (1.5 s, 2 s, 4 s).
- **Why it breaks:** Real fluorescent or LED battens bloom evenly and soften. A dark ring is a post-process or alpha artifact (the bloom is being composited over unpremultiplied alpha, or the emissive pass is rendered with a backface outline).
- **Fix:**
  - Use `UnrealBloomPass` (strength about 0.35, radius 0.6, threshold 0.9) on an HDR buffer, or `postprocessing`'s `SelectiveBloomEffect`.
  - Use `MeshBasicMaterial` with a colour above 1.0 (toneMapped false) for the tubes. Make sure the glow sprite uses `premultipliedAlpha`.
  - Delete any outline or back-face hull.
  - Add a lamp housing, a diffuser and a hanging chain.
  - Replace the brick-like truss texture with proper purlins and corrugated roof sheet with a repeat-free normal map.
  - Make fixtures cast light: add `RectAreaLight`s under 3 to 4 of them so the jets' top surfaces pick up a visible pool and a specular streak.

### 7. Materials: everything is the same smooth blue-grey plastic with blown specular blobs (6-27 s)
- **See:** The fuselage is one uniform mid-grey with a few large soft white specular smears (12 s, 14 s, 26 s: the pale elliptical highlight on the spine). The tail fin has digital noise or speckle (a white pixel-confetti texture) at 22-26 s and 29 s. There are no rivets, seams, weathering, hatches, sensor blisters, antennas, pitot tube, or stencils. The paint is a single colour with no gloss variation. The fuselage runs into the fin with no fillet at 27 s.
- **Why it breaks:** Real aircraft skin has panel breaks every 0.5-1 m, access doors, fasteners, stencilling and anisotropic gloss. A single clean grey surface reads as plastic. The speckle on the fin reads as a bug.
- **Fix:**
  - Make a 2048 px canvas atlas with panel lines, rivet rows, access doors, and "REMOVE BEFORE FLIGHT" tags. Use it as `normalMap`, `aoMap` and `roughnessMap`.
  - Use `MeshPhysicalMaterial` with clearcoat 0.6, clearcoatRoughness 0.25, roughness 0.5, metalness 0.15, and a tinted colour per jet (vary the value by plus or minus 4%).
  - Fix the fin speckle: it is either z-fighting between a decal and the fin, so set `polygonOffset: true`, or a high-frequency noise texture without mipmaps, so enable mipmaps and anisotropy 8.
  - Add sensor blisters, a pitot boom, antenna blades and a refuelling probe.

### 8. Exhaust nozzle is a sunburst of loose boxes (29-37 s)
- **See:**
  - Dark rectangular fins fan out radially from a bright, polished, smooth steel ring (29 s, 31 s, 36 s), like a gear or a sun logo.
  - From the side (29 s) the petals are visible floating off the ring, not attached to the airframe.
  - The ring is clean chrome with a blown, white-blue reflection at the bottom (31 s, 35 s: the same bright streak).
  - The tailpipe overlaps the tailplane at the wrong place.
- **Why it breaks:** Real nozzles have overlapping tapered petals, sub-petals (seals), a flame holder, and heat-stained titanium and steel in a gradient. This is the item the narration is about, so it needs to be the most detailed object in the shot.
- **Fix:**
  - Build 16 master petals and 16 seals as tapered, slightly curved extruded shapes (`ExtrudeGeometry` along an arc), alternating overlap, inset 2-3 degrees.
  - Colour with a heat gradient (dull steel to bronze to blue-purple toward the tip) using a `CanvasTexture` or vertex colours, with roughness 0.55.
  - Replace the polished-chrome ring with brushed metal, using an anisotropic-style roughness map or `anisotropy` on `MeshPhysicalMaterial` (r155+).
  - Add the afterburner flame-holder spokes and an actuator ring.

### 9. Whole-frame atmosphere: no depth cue, no haze, no DOF, particle "snow" is square dots (1.5-40 s)
- **See:**
  - Square white pixels (3-6 px) float and don't move parallax-correctly (visible at 1.5 s, 8 s, 20 s, 35 s, 37 s). They are not round and not soft.
  - There is no atmospheric perspective. The far jets at 4-6 s are only darker, with no haze.
  - There is no depth of field. Every plane is razor sharp, from the near nosewheel to the far door.
  - The picture is heavily noisy-black in the corners and has a flat, even grain.
  - The first 1.2 s (0.5 s frame) is a black frame with sparse star-like dots.
- **Why it breaks:** The lack of optical depth cues is a big CG tell. Square particles read as dead pixels.
- **Fix:**
  - Use `Points` with a round soft sprite texture (radial gradient `CanvasTexture`), size attenuation on, and sizes of 0.5-2 px. Lower the count, fade by distance, and drift slowly with a shader-based curl noise. Put them in light shafts only.
  - Add `FogExp2` with a blue-grey colour (density about 0.012), plus a ground-hugging haze plane.
  - Add `BokehPass` or the `DepthOfFieldEffect` from `postprocessing` (focus distance tied to the subject, f/2.8-equivalent), and animate focus on the rack at 20 s.
  - Add subtle chromatic aberration and lens vignette in the corners (not the grey blobs, see below), and film grain at 0.04 with luma-dependent response.

### 10. Opening "door rises" reads as a glitch: grey blobs in the lower corners and a hard rectangular reveal (0-8 s)
- **See:**
  - 0.5 s: black frame. At about 1.0 s a thin strip of hangar appears from the bottom and grows upward. That is a wipe, not a door.
  - A pale curved grey shape sits in the bottom-left (and the right edge at 0.5 s and 2 s) and stays there until about 8 s. It looks like a rendering artifact or a leftover foreground mesh: a vignette hole, the door's underside, or a camera-attached object.
  - The sloppy "hard clip" curve on the floor edge near the grey shape is visible at 2 s and 4 s.
- **Why it breaks:** It breaks the first 2 seconds, which is where a documentary earns the viewer. The persistent grey wedge draws the eye away from the jets.
- **Fix:**
  - Model a real roller or sectional door: a textured slab of 8 horizontal panels with rails, travelling up over 2 s with an ease-in-out, and light spilling under it that grows into a wedge and sweeps across the floor. Add dust motes in the spill.
  - Find the grey wedge in the scene graph. It is probably a mesh near the camera, so delete it or push the near plane out.
  - Set `camera.near` to 0.1 and `far` to 200. Check for a clipped transmissive or shadow-catcher plane.

## 3. What works and must be kept

- The one-point-perspective hangar composition at 1.5-4 s: a symmetrical central aisle, the yellow guide lines converging, jets on both sides with receding fins, and a lit ceiling row. This is a strong, readable establishing image.
- The cold teal / navy low-key palette with a warm yellow accent line. It is on-brand and gives a good base to grade.
- The slow forward walk at 2-8 s: the speed is believable for a first-person walk and the parallax of the fins against the windows is nice.
- The ceiling-light vanishing pattern for depth.
- The lower-thirds ("JETS BUILT / ABOUT THIRTY", "DELIVERED TO THE AIR FORCE: 0", "ENGINES SENT 14 OF 99" with the progress segments): clean, legible, and placed in the safe area. The orange count segment filling is a good graphic idea.
- The ending composition from 36 s: the jet tail seen against the open doorway, with the neighbouring jets framing the left side. The silhouette of fin and nozzle against the bright opening is a strong idea once the door is fixed.
- The concept of the tunnel as a "keyhole" shot. The idea is right, only the execution is wrong.
- The red nose-gear tag as a colour accent. It is a good storytelling detail, but it needs a proper fabric-tag shape.

## 4. The three changes that raise the score most

1. **Fix the engine-bay and nozzle shot (defects 1 and 8).** Replace the concentric-ring smiley tunnel with an irregular, cluttered, dull-metal bay and a proper petal nozzle with heat gradient. This is the story payoff, and it moves the clip from comedic to credible.
2. **Fix the camera (defect 2 and the notes in section 5).** Spline-driven position and target, locked up vector, collision clearance, subtle handheld, real stop at 20 s. Removing the 15 s flip alone takes out the most obvious "this is a bug" moment.
3. **Replace the lighting and environment (defects 4, 5, 6, 9).** An HDRI-based dusk, soft key and rim lights, proper bloom without dark outlines, contact shadows or SSAO, fog and depth of field, a real door opening. This lifts every frame at once and makes the jets feel grounded.

(Jet model fidelity, defect 3, is the next biggest item, but it costs the most modelling time. If time is short, hide the model's weakness with items 2 and 3, and keep the camera 3 m or more from the nose.)

## 5. Camera and editing notes

**Overall:** The camera has a constant, slightly floaty glide with no footfall rhythm, no micro-jitter and no breathing. Nothing says "a person with a camera". A first-person documentary move needs a 1.8-2.0 Hz vertical bob of about 1-2 cm and a 0.3-0.5 degree roll drift, with low-frequency yaw wander (simplex noise, 0.15 Hz). The lens is a wide rectilinear perspective (looks like 24 mm equivalent, with a vertical FOV of about 60-70 degrees), with no distortion character, no vignette fall-off and no depth of field. Use 28-35 mm equivalent for the walk, and go longer (50-85 mm) for the nose and tunnel so the jets stop looking like toys.

**0-2 s: door rises.** See defect 10. The reveal is a wipe over black with stray grey shapes, not a door. Add a light-spill gradient, an audible-looking rumble (visual dust and floor-light growth) and hold the first full-width frame for at least 0.5 s before the move begins.

**2-8 s: walk in.** Good composition. Problems: the "OCTOBER 2026" floor text is large, close and aliased, and it slides under the camera, which reads like a game HUD. The camera height is about 1.2 m (it looks lower than a standing eye height of 1.6 m), which makes the jets look big but the floor take up too much frame. Raise it to about 1.55 m and tilt down 2 degrees. Add a slight lateral sway.

**8-14 s: the line of jets.** The camera veers right and goes in tight on the nose of the first jet. The jets beyond it are just dark stripes, so "about thirty" is not sold: you see about 6 to 8 aircraft in total. Show a longer line with a lens-compressed telephoto pass (50 mm, low angle) so that thirty fins stack up. Add light on the far jets, not black.

**14-16 s: the glitch.** See defect 2. The camera dips under the nose and rolls, with a 1.2 s detour that kills the "stop dead at 20 s" tension. Cut it, and replace it with a smooth arc outward around the nose.

**16-20 s: the stop.** The beat is "stop dead at 20 s", but the camera is still gliding at 20 s, 22 s and 24 s (each frame shows a different position along the fuselage). A real stop needs the speed to ease to zero over about 0.4 s, 0.5 to 1.0 s of stillness with only handheld breathing, and ideally a small rack focus from the nose to the engine intake. Right now the lower-third swaps from "JETS BUILT" to "DELIVERED: 0" with no camera punctuation.

**20-26 s: side pass.** A long, slow tracking shot along the fuselage at a constant distance of about 1.5 m. The frame is mostly a featureless grey flank, so there is nothing to look at for 6 seconds: no panel detail, no stencils, no shadows. It is also too close, so the proportions feel like a model kit. Either pull back to 4 to 5 m for a clearer silhouette or add detail. At 27 s the floor fills a third of the frame as a pale, flat grey wedge with a visible ellipse light pool: reframe.

**26-30 s: walk to the tail.** At 28 s the camera passes the tailplane, close, with the fin cropped, a smooth grey slab, and then the nozzle appears at 29 s from an oblique angle. The reveal of the empty nozzle is good in principle, but it is under-lit (it is the darkest object in the frame). Rim-light the nozzle ring and let a beam of light hit the inside lip as the camera arrives.

**30-34 s: tunnel.** A constant-speed zoom-in at 30 to 34 s of the same ring pattern. There is no change in information, so the 4 seconds feel long, and the smiley face is the only thing that registers. Ease in and out, reveal something at the end (a dead-end bulkhead with the empty mount, for the line "the engine bay is empty"), add a light that is swallowed by the dark, and cut at 33.5 s on a hard dark so the whip has something to leave.

**34-41 s: whip out.** This is not a whip. At 35 s the shot is a clean, slow pull-back with no motion blur and no speed ramp. At 36 s and 38 s the camera is just turning in a gentle arc, and the lower-third "ENGINES SENT 14 OF 99" appears. To sell a whip, add:
- a 6 to 8 frame rotational whip (roughly 120 degrees at peak),
- a 180-degree shutter-equivalent motion blur (radial or directional blur pass, or accumulate sub-frames),
- a 1.1x to 1.3x FOV punch as the camera leaves the tunnel,
- a bit of camera shake on arrival, and an ease-out into a locked wide frame for the last 2 seconds so the VO has a clean hold.
Also, the final wide is dominated by a huge blown-out rectangular door (35-40 s), which becomes the focal point instead of the jets. Lower the exposure of the opening, add a gradient, and frame the empty row of jets in the left two-thirds.

**Pacing against beats:** the walk-in and the line of jets are about right in length, but the first 14 s have almost no change of shot size, then the clip goes into the 1.2 s glitch, a 10-second flank crawl, and a 4-second identical tunnel, so the second half is dull in pacing and visual information. Make the tunnel 3 s and the side pass 4 s, and use the saved 7 s for a stopped, handheld-breathing hold at 20 s and a better whip-out with a proper wide at the end. Overall, vary the shot size every 4 to 5 s (wide, medium, close, extreme close), and use the lower-third changes as cut points, not as overlays on a continuous move.
