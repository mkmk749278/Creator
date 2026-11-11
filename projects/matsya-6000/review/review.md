# Matsya 6000: our review of the 720p review cut

## r1 (`renders/matsya_review_r1_720p.mp4`, 2026-11-11)

### Measured
- Picture and audio are both 456.133 s. Loudness is −14.0 LUFS, −1.4 dBTP, LRA 2.9.
- Flash check: clean on every shard.
- Freezes (`freezedetect n=0.002 d=1.5`, 480p) at:
  - 82.3 s (2.4 s);
  - 84.8 s (1.6 s);
  - 95.5 s (4.3 s);
  - 159.2 s (2.0 s);
  - 362.7 s (2.5 s);
  - 452.4 s (the end card).
- Shots over 5 s:
  - the PIB jetty photo held 330.5–346 s;
  - the 6 Nov photo held 346.6–352 s;
  - H1_dark held 422.8–439 s (16 s).

### Shot-word audit and frames (19 contact sheets, one frame every 1.5 s, each with the words heard)

| Time | Shot | Words | Grade | Fix (r2) |
|---|---|---|---|---|
| 45–58 | Fall | "Every ten metres … once more … and again" | WRONG | The depth counter read 30 m from frame 0 (each beat's value applied before the beat). Now it steps 10 → 20 → 30 → 40 on "ten", "once", "again", "again", then races to 6,000. |
| 82.3–86.7 | Deep | "asking the same question … like Titan?" | WEAK, freeze | S25 is now the real ball in its hall frame (DD India). S26 is the deep with a visible push, denser snow and TITAN on its word. |
| 95.5–104 | CarbonHull | "carbon fibre … layers came apart" | WEAK, void, freeze | The carbon layers now sit on the moving steel plate. |
| 159.2 | SteelBall2021 | "India walked the same road" | freeze | The ball descends from frame 0 and speeds up on the date. |
| 177.5 | ISRO_forge | "how do you make it?" | OK | A narrow source frame, but it is ISRO's own. Kept. |
| 179 | ISRO drawing | "drawing shows five pieces" | WEAK | It was cropped by `cover` and the labels were cut off. Now a full-frame insert over its blurred copy. |
| 219.5 | empty plate | "welding centre in Bengaluru" | WRONG | The plate was empty for 2 s. ISRO's EB chamber now carries "welding centre in Bengaluru", and the bars come in on "two". |
| 227 | 40 KW count | "much more powerful" | WEAK | It was on screen for 1 s. It now holds 1 s longer. |
| 264.5 | ISRO_hall (4th use) | "outside agency has to certify it" | WEAK, repeat | Replaced with DD India's NIOT hall (the sphere and the test sphere). |
| 308–313 | H1_dark | "So is Matsya ready?" | WEAK | Dim red rings with no readable subject. Now Matsya hanging over the sea (Times Now) for S99, then the deep with NOT QUITE. |
| 334.5–346 | PIB photo, 12 s | "foam from France … crack … held up" | WEAK, too long | S109 is a foam block sliding in ("had to come from France … arrived late"). S110 is a closer view where a crack draws itself on "crack" (ILLUSTRATION, word map R). S111 is the PIB jetty photo. |
| 346.6–352 | PIB photo, 6 s | "trials near Chennai" | WEAK | On "Chennai" it cuts to the map with a Chennai pin. |
| 362.7–366 | H3_seabed opens black | "Six thousand metres down … no sunlight" | freeze | Added the last daylight fading from the top, marine snow, and a counter running to 6,000 M on "six thousand metres down". |
| 422.8–439 | H1_dark, 16 s | the landing | WRONG for the climax | Unreadable, and too long for the most important beat. Now: S133–134 back inside the cut-away ("come back inside the ball"), S135 the three empty seats ("not been to sea with people in it yet"), S136 the squeeze ("tested at full pressure"), S137 the opening shot again ("the last test will be the sea itself"), a deliberate callback to 0:00. |
| 452.4 | end card | — | freeze | The logo now does a slow 8% push. |

### Footage checks
- `F01_foam` is labelled "Matsya with its yellow foam" in `media/clips.tsv`. It is actually ROSUB 6000 with a minister, so it is not used anywhere.
- `F01_ballhall` holds the ball only from 0 to 3 s; after that it shows an ROV and a CG render. It is used from 0 for 3 s.
- `F01_crane` turns into reef footage at 2.2 s, so it is not used.

### Creative pass
- **Landing.** The landing is now a chain of pictures that each say their sentence, ending on the cold open's first frame. The film starts and ends on the ball going down.
- **Foam beat.** It went from one photo for 12 s to the block arriving, then the crack, then the real jetty, then Chennai.
- **Repeats left on purpose:**
  - ISRO's hall shot at S2, S33 and S55 (the only real wide shot of the ball);
  - H4_squeeze at S22, S44 and S136 (the film's pressure motif).

### Open for r2
- Re-render the 720p cut, re-run freezes, flash and loudness, and re-read the sheets for the changed spans.
