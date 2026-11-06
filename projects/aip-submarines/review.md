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

## Round 4 (aip_review_r4_720p.mp4) · independent review r1 fixes
- −14.1 LUFS, −1.1 dBTP, 545.97 s; black only the 0.18 s dissolve at 9:01.3. The r1 fixes hold on the frame (0:12 red
  consoles, 2:58 battery red by "fast", 6:45 trap boxes, 7:08 Kalvari, 7:26–7:53 timeline, 8:12 Khanderi clip).
- `freezedetect` (n=0.003) found three real holds, now fixed for round 5 (rendered locally, no still over 1.0 s):
  - **5:46 "signs off the design" (2 s still):** the H4 clip runs out at 0.5× and the eased camera stopped with it. A
    linear push and pan (`Cam`/`Clip` take an `ease`) keeps it moving to the cut.
  - **7:46 "Designed at D-R-D-O's lab in" (1.7 s still, and no picture for "D-R-D-O"):** the Ambernath pin (DRDO LAB ·
    NMRL) now lands on "D-R-D-O's", and the map pushes in from "Designed".
  - The underwater shots (0:02, 2:28, 3:02) are the same noise-floor flags as round 3: the boat crosses about 650 px.
- **4:37–4:46, the Defence Secretary quote:** "OCT 2026" sat on the oxygen tube, "Defence Secretary" had no picture on
  its words, and the quote card hid half of "HYDROGEN" and "ELECTRICITY". The drawing now sits back (25%, soft), and
  three lines arrive on their words: OCT 2026 → INDIA'S DEFENCE SECRETARY → the quote.
- **Map credit cut off on the left** ("ASA BLUE MARBLE"): the film's reframe moves (up to 1.09×, −30 px) pushed it past
  the edge. It now sits at x 150, below the Mazagon label; checked on all four maps.

## Round 5 (aip_review_r5_720p.mp4) · the cut for the owner and independent review r2
- −14.1 LUFS, −1.1 dBTP, 545.97 s; black only the 0.18 s dissolve at 9:01.3. `freezedetect` (n=0.003) no longer
  lists 5:46 or 7:46; what remains is the round-3 noise-floor list (underwater 0:02–0:51, 2:28, 3:02) and the ending.
- Checked on the frame: the quote beat (4:39, 4:43), Naval Group (5:46–5:48, moving), Ambernath on "D-R-D-O's"
  (7:48), the map credit in full.

The owner watches round 5 → independent viewer review r2 (real-audience panel) → `review_ack_r2.md` → the owner approves the cut → the 4K master.
