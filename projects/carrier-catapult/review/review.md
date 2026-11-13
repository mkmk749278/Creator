# Review · carrier-catapult · 720p cut r1 (2026-11-13, render run 43399044281)

## Measured
| Check | Result |
|---|---|
| Loudness | −14.0 LUFS, LRA 2.8 LU, true peak −1.4 dBTP: pass |
| Length | picture 648.15 s = timing + 4 s end card; audio joined to it: pass |
| Dark flash frames | every shard checked by `render_shards.mjs`: none |
| Frozen holds (`freezedetect` at 480p) | **1**: 1:34.5–1:36.4, the radar plate before "the flying radar" (only a thin sweep moving) |
| Footage running out | **8 shots** held their last frame under the camera move (S41, S43, S61–62, S82, S86, S90–91, S133–134, S192–193) |
| Shot lengths | 132 shots; shots over 5 s are reframed every 4.5 s with a visible move (Film.tsx); the fan unroll (18.6 s) is the plan's designed long take (S1); two diagram runs were too long (S177–184: 26 s) |

## Frames against the words (one frame every 3 s, 216 frames, `review/sheets/`)
| Issue | Time / shot | Fix (r2) |
|---|---|---|
| The glowing slot did not draw (SVG filter on a zero-height line) | everywhere a horizontal glow line | `filterUnits="userSpaceOnUse"` (fixed before r1, confirmed) |
| The 1961 side view had no hull (ramp curve divided by zero at 0°) | 4:05–4:20 S81, S83 | guard the angle |
| "a small test model": the model was off the frame | 0:31 S10 | drawn higher, larger, labelled TEST MODEL · SAME SCALE |
| Radar empty for 3 s, then frozen | 1:33–1:37 S33–35 | pulse rings from the ship, always moving |
| Ramp drawing and cooker sat low, half off the plate | 1:01 S18–22; 2:16 S47–49 | raised and enlarged |
| "Almost empty" showed the gauge close-up | 3:37 S73 | the room clip from its pull-back (7.5 s) |
| Land track empty for 6 s (drew on the sentence's last word) | 6:34 S131–132 | draws on "twenty sixteen" |
| Working sheet blank for 3 s | 5:22 S107–108 | first line at the shot's start |
| The 17 m model zoomed past readability | 7:58–8:16 S154–163 | the pull-back starts at 2.5×, not 6× |
| China/India, the two ships, "plainly", "ramp or catapult" blank before their first word | 8:34, 8:43, 9:16, 10:31 | each drawn from the shot's start |
| Diagram run 26 s (DSCA notice + the honest sum) | 9:04–9:30 | the real Rafale landing on "Twenty-six Rafales" |
| "NEXT TIME" plate nearly empty | 10:37–10:42 | a drawn submarine whose sonar reaches ahead, silence behind |
| Fujian KJ-600 clip slowed past its end | 6:41 S133–134 | the flying-radar circle on "flying radar plane" |
| Coil-winding stock: motion-interpolation mosaic on the hand | 4:46 S94 | start the clip at 3 s (still hand) |
| "LIKE A FLYOVER" stayed on the ship | 0:57 S17 | ends at "ends" |

## Creative pass
- **Mute test:** the pictures alone carry the story: the landing, the slot that stops at the ramp, 1961 archive, the
  cracked drum and the bands, the unrolled motor, the meter, the red spike, the spinning store, the 17 m line beside
  100 m, the three slots. Weakest: chapter 4's documents (four pages in a row) carry it by text; acceptable (the film's
  one document pose), each lands on its word.
- **Eyes-closed test:** the narration carries alone; the motif (whine, thump, wind) marks the open, the count and the
  landing.
- **Memory test (three things):** the 49 MW spike against the four engines; "One. Two. Three." with the real launch;
  the steel bands on the drum. These match the plan's one image (the meter/six days) closely enough; the meter could
  be stronger at S110 (now the ceiling fan): kept, as the fan is the take-home callback.
- **Swap test:** the archive of the first Vikrant, the bands, the slot stopping at the ramp and the 17 m line could sit
  in no other film. The radar circles and the documents could: they are short and on their words.
- **Flattest minute:** 7:30–8:30 (memo, GA statement, Pune map, technician, model). Redesigned: the KJ-600 under "the
  newcomer is already flying", the map on Pune, then the real-scale model and the pull-back.

## Next
Render r2 (720p) with these fixes; measure again; then the independent viewer review.

# Review · r2 (render run 43404314348)
- Loudness −14.0 LUFS, −1.4 dBTP; no flashes; every run-out fixed (checked against clip lengths: none left).
- One freeze remained: the radar plate before "the flying radar" (1:33.5, 2.85 s: ship and faint rings only). Fixed:
  the plane's circle opens from the shot's start (it is the answer the question sets up).
- 216 frames read again: the r1 fixes hold. Fixed for r3: "FAR SHORT" overlapped the goal label (7:16); the model
  shot still too tight (7:58), its label off the frame and under the 400 KG tag: the zoom eased to 1.6×, the tag moved up.
