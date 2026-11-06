# Review · round 1 (aip_review_r1_720p.mp4, 2026-11-06)

Our own review (PLAYBOOK §13.1) of the first 720p cut: 9:05.97, 1280×720 at 60 fps, H.264 + AAC.

## Measurements
| Check | Result |
|---|---|
| Loudness | −14.1 LUFS integrated, −1.0 dBFS peak: **pass** |
| Length | picture 545.97 s = voice 541.47 s + 4.5 s end card: **pass** |
| Flash frames | the render's dark-flash check passed on every shard |
| Black | 0.45 s at 1:15.7 (P-8I clip opened on a squadron crest and a black frame): **fixed** (span moved to 7.5–11.4 s, which is crew walking and the runway) |
| Freeze (`freezedetect n=0.002 d=1.5`, 480p) | 0:38–0:41, 0:44–0:51, 2:28, 3:02–3:05: the underwater 3D shots moved too slowly to count. **Fixed:** the boat now glides and the camera dollies 26–40 m across each shot. 9:02: the end card (allowed). |
| Shot lengths | 89 shots; no framing longer than 5 s (`tools/shotlist.tsx`) |

## Frames against the audio (one frame every 4 s) and the shot-word audit
| Time | Issue | Fix |
|---|---|---|
| 8:12 | Khanderi clip carried a Financial Express burned-in caption ("designed to operate in all theatres") | span moved past the caption (106.2 s); the crop is now deeper, so the publisher's corner logo is gone too |
| 2:12, 2:34, 4:00, 6:08, 7:52 | Steel plate sat empty for 1–3 s before the first drawing arrived on its word | the patrol strip, the three machines (dim, each lights on its word), the spoon, the six boats and the six Kalvari boats are all on the plate from the first frame |
| 8:52 | "Next, we go even deeper" opened on an empty plate | now opens under deep water; the depth count and the sphere arrive on their words |
| any | A shot longer than its footage would freeze on the clip's last frame | `Clip` now slows playback to fit (never below 0.5×), using the measured clip lengths in `media/clip_durations.json` |

## Creative pass
- The cold open plays as planned: night sea → Arabian Sea on the map → the boat under water with its battery at 12% → the red control room → "Raise" → the mast breaks the surface → radar locks on.
- The trap loop (6:44–7:20) reads clearly: two halves, the arrow closes, the padlock. It opens green on Khanderi and closes red on "if the trials fail".
- The dry-dock surgery (5:14–5:45) is the strongest 3D moment: the cut glows, the halves part, the section rolls in, the seams weld.
- Weaker spots to watch in round 2: the battery cutaway labels are small at 480p; the H4 hull is dark (by design, a covered dock at night).

## Round 2 (aip_review_r2_720p.mp4)
- Loudness −14.1 LUFS, peak −1.0 dBFS; length 545.97 s: pass. The P-8I open, the Khanderi clip and the five plates are fixed (checked at 1:15, 2:12, 2:34, 4:00, 6:08, 7:52, 8:12).
- `freezedetect` still flagged the underwater shots (0:38–0:51, 2:28, 3:02) and the ending (8:52–9:00). Cause: the camera tracked the boat, so the boat did not move across the frame. **Fixed for round 3:** the camera holds while the boat crosses and grows, the water is lighter, and marine snow drifts past the lens (the ending's snow rises fast, so it reads as the camera sinking).

## Round 3 (aip_review_r3_720p.mp4) · the cut for the owner
- −14.1 LUFS, −1.0 dBFS peak, 545.97 s; no black frames except 0.18 s at 9:01.3, where the depth gauge dissolves into the end card.
- `freezedetect` (n=0.002) still lists 0:38, 0:46, 0:49 and 8:52–9:00. Checked frame against frame: the boat crosses about 120 px in 2.4 s and the marine snow moves throughout. These are dark, low-contrast frames that fall under the detector's noise floor, not holds a viewer would see.

## Next
The owner watches round 3 → independent viewer review of the cut → `review_ack_r1.md` → the owner approves the cut → the 4K master.
