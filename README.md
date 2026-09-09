# Creator — Lumin social video pipeline

Builds Instagram Reels for the Lumin crypto-signals app from **real app footage**
and the Lia character, end to end, with **no paid service anywhere in the chain**.

Eight finished reels ship in `reels/` — three launch explainers and a
character-led set of five. Everything needed to make the ninth is here too.

```
python3 pipeline/capture_app.py            # sign in, screenshot + record the real app
python3 pipeline/prep_screens.py           # crop captures into clean screen plates
python3 pipeline/check_proofs.py           # render every claim's proof crop -- LOOK AT IT
python3 pipeline/render_reel.py --all      # script.json -> 1080x1920 MP4
python3 pipeline/check_captions.py         # no caption may straddle a full stop
```

---

## What comes out

| Reel | Angle | Lia on screen |
|---|---|---|
| `01_what_lumin_does` | Cold-audience explainer | 2 of 7 scenes |
| `02_funds_never_leave` | Trust / the first objection. **Post this one first** | 2 of 6 |
| `03_signal_anatomy` | Product detail: entry, stop, three targets | 2 of 7 |
| `04_stop_loss_saves_you` | What a stop loss actually saves you | **4 of 7** |
| `05_paper_mode_prove_it` | Don't trust it — test it | **4 of 7** |
| `06_three_checks` | Three checks before trusting any signals app | **5 of 8** |
| `07_named_setups` | Named setups, not mystery calls | **3 of 7** |
| `08_free_and_paid` | Every signal is free. Here's what isn't | **4 of 7** |

**04–08 are the character-led set** (2026-09-09, owner: *"use character more …
let her talk with natural language like humans"*). Two changes, and only the
first is visible: they are written to be **spoken** rather than read
(`brand/CHARACTER_BIBLE.md § How she talks`), and they use the `talk` scene, so
a claim is evidenced by an inset **beside** her instead of by cutting away from
her. That is what took her from ~28% of a reel to ~60% on two photographs.

Each renders an `.mp4` (H.264 / AAC, 1080×1920, 30fps, `+faststart`), an `.srt`,
and a `_poster.jpg` for the feed thumbnail or a carousel.

## The zero-cost stack

| Need | Used | Instead of |
|---|---|---|
| App footage | Playwright + Chromium against a local `flutter build web` | a phone, an emulator, a screen recorder |
| Voice-over | `edge-tts` (Microsoft neural voices) | ElevenLabs |
| Caption sync | `edge-tts` WordBoundary events | Descript, a captioning SaaS |
| Music | synthesised from oscillators in `reelkit/audio.py` | a stock-music licence |
| Type | Inter + Montserrat (SIL OFL) | a licensed display face |
| Composition & encode | Pillow + ffmpeg | After Effects, a template SaaS |

Higgsfield image/video generation was checked and **not** used: the account has
0 credits on a free plan, so it would have cost money. The character comes from
the owner's supplied stills, animated rather than regenerated.

## Pipeline

```
lumin-app (scratch copy, LUMIN_E2E)         assets/character/*.png
        |                                            |
  capture_app.py  --> shots/ + video/                |
        |                                            |
  prep_screens.py --> capture/app/screens/           |
        |                                            |
        +--------------> reelkit ---------------------+
                            |
        reels/<name>/script.json --> render_reel.py --> out/*.mp4 + .srt + poster
```

### `pipeline/capture_app.py`

Serves a local web build under the real `https://app.luminapp.org` origin
(Firebase only accepts authorised domains) and drives it with Playwright.

Flutter renders to a canvas — there is no DOM, so every interaction is a click at
a point, and the documented coordinates in
`lumin-app/docs/AI_AGENT_APP_ACCESS.md` **had already drifted** when this was
written: the onboarding had become a 3-page carousel and boot beat the
documented 20s wait, so the early taps landed on a blank frame and were silently
lost. A canvas app reports nothing for a tap that hits nothing.

So the capture locates things by what is on screen:

* boot is detected by the frame gaining detail, not by a fixed sleep;
* the primary CTA is found by its brand accent `#7BD3F7` — **as a filled block**.
  Matching accent alone matched the *outlined* "Send via Telegram" button's 1px
  border, and the tap landed in the 5px gap between the two buttons, so the SMS
  was never sent and every later step ran against a screen that had not moved;
* every step screenshots, because that is the only feedback available.

Sign-in uses a **registered Firebase test number only**, per that doc's rules.
The `LUMIN_E2E` patch is applied to a scratch copy and is never committed —
here or in `lumin-app`.

### `pipeline/reelkit/`

| Module | Does |
|---|---|
| `brand.py` | palette copied from `lumin-app/lib/shared/tokens.dart`, fonts, safe areas |
| `motion.py` | easing + `ken_burns` cover-crop camera |
| `draw.py` | type layout, scrims, glows, the phone mockup |
| `captions.py` | word-timed kinetic captions |
| `audio.py` | edge-tts voice, synthesised bed, sidechain-ducked mix |
| `scenes.py` | `talk` · `character` · `phone` · `duo` · `screen` · `card` · `end` |
| `proof.py` | claim key -> the screen region that evidences it |
| `build.py` | timing, frames, encode |

### Scenes cut on the voice, not on a stopwatch

A scene declares the phrase it starts on:

```json
{"type": "card", "until": "Fifteen AI analysts", "headline": "15 AI analysts score every setup."}
```

`build.py` finds that phrase in the edge-tts word timings and cuts there.
Hand-authored durations drift the moment a line is reworded, and the drift is
invisible until you watch the whole thing back. Scenes without an `until` are
spread evenly between the anchored ones, and any scene resolving under 1.2s is
reported as `TOO SHORT` — that is always two anchors sitting on adjacent
phrases, and it renders as a strobe.

## Rules that are not style preferences

* **Every claim must point at a real screen.** `content/COMPLIANCE.md` is the
  list, and the reels are cut from a real signed-in session so the pointing is
  possible. No performance, profit or win-rate figure appears anywhere — the
  engine repo's own hard limit, applied to marketing.
* **`prep_screens.py` deliberately excludes the Pulse P&L plates.** They carry a
  live realised-P&L number.
* **Screens are cropped, never repainted.** The only edit is removing the PWA
  "Install Lumin on your iPhone" banner, which is a web-channel artefact that
  would otherwise appear in an ad for the Android app.
* **Lia is a presenter, not a testimonial witness** — `brand/CHARACTER_BIBLE.md`.
  She describes what the product does; she never claims results. The owner has
  decided against an AI-generated label (recorded, with its risk, in that file),
  which makes the presenter framing load-bearing rather than optional.
* **The risk line renders on the end card**, not only in the caption — captions
  collapse behind "more".
* **No caption may straddle a full stop**, and it is checked against the
  rendered `.srt` rather than trusted from the code — `pipeline/check_captions.py`.
  `mark_punctuation` silently stopped enforcing this on 2026-09-09: one
  hyphenated compound (`trade-only`) desynced its token cursor, and because the
  old inner loop scanned to the END of the script looking for a match, that one
  word cost the sentence breaks for **every caption after it**. Nothing failed,
  nothing was blank; the captions just started reading like "rejected Two Is
  there". Reels 01–03 escaped only because their narration says "trade only"
  without the hyphen.

## The `talk` scene, and why the inset is not a design flourish

The old grammar cut away to a `phone` or a `screen` whenever a claim needed
evidence, so the presenter was on screen for about a quarter of a reel and the
feed read as an app demo with a face on the front. `talk` keeps her in frame and
brings the evidence to her:

* **The camera breathes.** `motion.handheld` adds three sines at incommensurate
  frequencies, so a still portrait held for four seconds stops reading as a
  slideshow. The tell it removes is monotonic motion — nothing a hand holds
  moves in one direction at a constant rate.
* **The inset is one legible ROW of a screen**, not a shrunken phone. A
  1290x2565 screenshot at inset width puts the app's body text at about six
  pixels, and a phone-shaped blur asks the viewer to take the claim on trust —
  which is the exact thing `content/COMPLIANCE.md` exists to prevent.
* **A script names a CLAIM, never a crop box.** `"inset": {"proof":
  "stop_on_every"}` resolves through `reelkit/proof.py`; an unknown key raises
  at render. That is the compliance rule made structural instead of remembered.
* **The inset is centred**, because Instagram's like/comment/share rail runs
  down the right of the frame from about y=1100 — exactly where a designer
  would naturally park a card.

Framing is capped on purpose. The heroes are 1024x1536 into a 1080x1920 frame,
so COVER is already 1.25x before any zoom; `TALK_SHOTS` offers `wide` and `mid`
and deliberately has no `close`, because a face crop lands near 1.9x on a source
that is soft to begin with — and a soft close-up is the shot that makes a viewer
decide the person is not real. Anything over 1.62x prints a warning at render.

## Writing a new reel

1. Draft the narration **out loud**. Contractions, fragments, one discourse
   marker per turn; punctuation is the prosody, because edge-tts gets no SSML
   here — see `brand/CHARACTER_BIBLE.md § How she talks`. Write numbers as
   words (`seventy five`), because the `until` anchors match spoken words.
2. Check every claim against `content/COMPLIANCE.md`.
3. Copy a `script.json`, set the scenes and their `until` anchors.
4. `python3 pipeline/render_reel.py reels/<name>` and read the printed timing
   table before watching anything.
5. Write the caption into `content/CAPTIONS.md` and slot it into
   `content/POSTING_CALENDAR.md`.

## Re-capture when the app changes

The plates in `capture/app/screens/` are from **2026-09-08**. A reel showing a
screen that no longer exists is worse than no reel. Re-run the capture after any
change to onboarding, the Signals card, or the free/paid split.
