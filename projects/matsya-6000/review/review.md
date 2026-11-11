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

## r2 (`renders/matsya_review_r2_720p.mp4`, 2026-11-11)

### Measured
- Picture and audio are both 456.133 s. Loudness is −14.0 LUFS, −1.4 dBTP, LRA 2.9.
- **No freezes anywhere**: every r1 freeze is gone, the end card included.

### Changed spans re-read (103 frames with their words)
- **Confirmed fixed:**
  - the depth counter (0 → 10 → 20 → 30 → 40 → 6,000 on its words);
  - the Titan beat;
  - the carbon hull on the plate;
  - the steel ball;
  - the full ISRO drawing;
  - the EB chamber on "Bengaluru";
  - the foam block → crack → jetty → Chennai map;
  - "no sunlight" with its counter;
  - the landing chain;
  - the end card.
- **Two new issues, fixed for r3:**
  - 5:56.5 (S113): played slower to fill the longer slot, DD Telangana's clip reached its tail, which is a Telugu caption card. `clip_durations.json` now caps F03 at its clean 2.1 s, and the insert starts on "six"; the Chennai map holds until then.
  - 3:44 (S75): the 80 MM bar was on screen for only 0.9 s before the cut. The next clip now lands on "machine", so the bar holds for 1.85 s.

## r3 (`renders/matsya_review_r3_720p.mp4`, Drive id `1PT0VxIVS8iQ2ft5t6TmAd7QeV37LLf0h`, 2026-11-11)
- Picture and audio are both 456.133 s. No freezes. −14.0 LUFS, −1.4 dBTP.
- **Both r2 fixes confirmed on frames:**
  - the 80 MM bar now holds 224.2–226.0;
  - the Chennai map holds until "six", and DD Telangana's insert ends clean at 357.2, with no caption card.
- No open blockers from our own review. Next: the independent viewer review (§13.3), then the owner's approval.

## r5 (`renders/matsya_review_r5_v3_720p.mp4`, 2026-11-11): the film rebuilt on narration v3

Not sent to the owner: two WRONG pictures found; fixed and re-rendered as r6.

### Measured
- Picture 547.717 s, audio 547.716 s (9:04 of voice + 4 s end card). Loudness −14.4 LUFS, peak −1.2 dBFS, LRA 3.4.
- Freezes (`freezedetect n=0.002 d=1.5`, 480p): none.
- The first render's join hung in "Film to Drive" for 15 minutes; cancelled, and the film was joined by a second
  run with `join_from` (PLAYBOOK §14.3: the same remedy as a hung shard).

### Shot-word audit (6 sheets, one frame every 2 s, each with the sentence heard)
| Time | Words | Grade | Fix (r6) |
|---|---|---|---|
| 0:05–0:08 | "with almost one lakh tonnes" | WRONG | The DD India hall clip pans to another (yellow) vehicle after 3 s. Now the squeeze (H4) cuts in on "almost", SIMPLIFIED. |
| 2:35 | "Nothing happens, right?" | WRONG label | "A CRICKET BALL" sat over the blue ball. The label now ends with the cricket clip; "SQUEEZE IT" over the hand. |
| 2:33 | "Squeeze a cricket ball in your fist" | WEAK | The cricket ball is small and nobody holds it; the hand then squeezes a blue ball. Needs one real clip of a hand gripping a cricket ball (Cowork request). |
| 1:45–1:51 | "Its hull was carbon fibre … layers come apart" | WEAK | The drawing is faint grey on grey for 7 s. Redraw with contrast, or a real carbon-fibre weave clip. |
| 0:00–0:03 | sentence 1 | WEAK | Opens on our 3D ball in a void (the thumbnail's subject), the real ball at 3.2 s. A lit, real-water version of the opening shot would meet both rules. |
| 7:47–8:01 | China's depth, India's goal | WEAK | 14 s of bars; the Matsya row is empty until "six thousand". Shorten or show the row from the start. |
| 0:49 | "Stay with me, and you'll know both" | WEAK | The 3D ball again; a real shot would be better. |
| 6:45–6:49, 0:51–0:53 | the phone | OK | A light-skinned hand in a coat: replace with an Indian hand when one is found. |
| the rest | | OK | Real ISRO people and footage in every chapter from 0:25 on; every number on its word. |

### The creative tests (PLAYBOOK §13.1)
- **Mute test:** the story follows from the pictures in the pressure, weld and foam chapters; the Titan chapter
  (1:37–2:03) is words on dark plates and does not.
- **Memory test (one pass over the sheets):** the buffalo on the nail, the seam unrolled beside a man, SAMUDRA
  MANTHAN over the rolling sea. The first two were planned; the third is new in v3.
- **Swap test:** the phone shot and the storm sea could sit in any film; both are short and labelled.
- **Flattest minute:** 1:37–2:07 (Titan and the pressure bars): 30 s without a real picture.

### Promise check on the real timings
Sentence 1 unchanged. The paradox is spoken at 0:25–0:32 (rule: by 0:25). The loop runs 0:42–0:53 (rule: by 0:45).
The voice runs at about 171 words a minute; a shorter opening or a slower take would bring both inside the rule.

### Not checked
Nobody but the owner has listened to this take. The independent narration review of v3 and the independent viewer
review have not run.
