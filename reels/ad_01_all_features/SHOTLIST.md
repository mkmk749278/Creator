# Ad 01 — "Everything Lumin does" (45s, 9:16)

Generated-footage ad. **No app screenshot appears anywhere in this reel** — by
request, and the footage is AI-generated cinematic b-roll rather than captured
plates.

That choice has one consequence that is not negotiable and is the reason this
file exists: **the generated footage carries no product claim.** Every factual
statement is delivered as brand typography, drawn by `reelkit` from the app's
own tokens, over the footage. Nothing in a generated frame asserts anything
about Lumin.

See `content/COMPLIANCE.md § Generated footage` for the rule and why it is
shaped this way.

---

## Why no generated UI

The obvious version of this ad renders an "ultra realistic" Lumin interface —
a signal card with an entry, a stop and three targets, glowing on a phone.

It cannot ship, and the ban is this repo's own, written before this ad existed:

> | Redrawn, retouched or "cleaned up" numbers in a screenshot | The plates are
> cropped only. Nothing is repainted |
> — `content/COMPLIANCE.md`, Banned outright

A generated interface is a repainted screen with a repainted number in it. It
depicts a signal the engine never emitted, at a price nothing traded, on a
screen that does not exist — and it is *more* dangerous than a mock-up, not
less, precisely because "ultra realistic" is the brief. A viewer cannot tell it
from a capture. Neither can a reviewer.

So every shot below is **atmospheric or metaphorical**, and the device — which
now appears in six of the eight — is framed so its screen is never readable.
The prompts carry `no text, no UI, no numbers` for that reason, not for style.

A phone in frame makes the ad feel like an app ad, which is what it is. It also
puts a screen in shot six times, so the framing constraint is the load-bearing
part of every one of those prompts rather than a note at the end of it.

## The claims this ad makes

All nine are on the verified-safe list in `content/COMPLIANCE.md`, checked
against the onboarding captured 2026-09-08. No performance, profit or win-rate
figure appears — the engine's own hard limit.

| # | Feature | Claim source |
|---|---|---|
| 1 | Market runs 24/7 | Not a product claim |
| 2 | 75 USDT futures pairs, scanned every 15s | Onboarding |
| 3 | 15 AI analysts — momentum, structure, volume profile, regime | Onboarding |
| 4 | Entry, stop loss, TP1–TP3 on every signal | Signals screen |
| 5 | Stop-loss on every position | Onboarding |
| 6 | Automatic execution on your Binance account | Onboarding |
| 7 | Funds never leave Binance · trade-only key · withdraw auto-rejected | Onboarding + engine hard limit |
| 8 | Paper mode | Onboarding |
| 9 | Every signal free; automation is the paid tier | Onboarding |

## Generation settings

All shots: **9:16**, `generate_audio: false`. Silent is not a stylistic saving —
it is what makes a clip droppable into `reelkit`'s existing ducked mix
unchanged, and the reel already carries its own edge-tts voice and synthesised
bed. Generated audio would fight both and costs extra.

**Eight clips, not nine.** The closing frame is the `end` scene, which renders
on the brand backdrop with the real app icon and the risk line — it needs no
footage.

Durations are sized from the word count of the beat each shot covers, **plus
about a second of headroom**, because the cut lands where the phrase is
actually spoken and that moves whenever a line is reworded. A clip that comes
up short holds its last frame; `render_reel.py` reports it as `SHORT CLIP` in
the timing table.

| Shot | Covers | Generate |
|---|---|---|
| 1 | Hook | 5s |
| 2 | 75 pairs / 15 seconds | 7s |
| 3 | 15 AI analysts | 6s |
| 4 | Entry, stop, three targets | 5s |
| 5 | Hard stop | 5s |
| 6 | Connect Binance | 5s |
| 7 | Funds never leave Binance | 8s |
| 8 | Paper mode | 6s |
| | **Total** | **47s of footage** |

| Tier | Model | Settings | per sec | 47s |
|---|---|---|---|---|
| Budget | `seedance_2_0_mini` | 720p | 1.0 cr | 47 cr |
| Value | `kling3_0` | std, `sound:off` | 1.5 cr | 71 cr |
| **Recommended** | `seedance_2_0` | `mode:fast`, 720p | 2.5 cr | **118 cr** |
| Premium | `seedance_2_0` | `mode:std`, 1080p | 9.0 cr | 423 cr |

Rates measured by `get_cost` preflight on 5s clips, 2026-09-22 — not quoted
from memory. Re-preflight rather than trusting this table; it is a constant
asserting a property of somebody else's price list.

Budget for **re-rolls**. Prompt-to-usable-shot hit rate on abstract plates runs
well under 1.0, so plan about **1.4x** the figures above — roughly 165 credits
at the recommended tier for a finished set.

The render target is 1080x1920, so a 720p clip is upscaled 1.5x. On grainy
atmospheric plates that holds. **Shot 6 is the exception**: it has skin in it,
and an upscale shows on skin before it shows on haze. Generate that one at the
premium tier even if the rest are not.

---

## Shots

Owner direction 2026-09-22: **product-forward.** Six of the eight shots now put
the device in frame, so this reads as an ad for an app rather than a brand film.

That raises the stakes on one rule rather than relaxing it. A phone in frame is
a phone with a screen, and the moment that screen is readable it is fabricated
UI — the thing this ad cannot contain. So every device shot specifies the screen
as **angled well off camera, out of focus, or blown out to pure glow**, and says
so twice: once in the framing and once in the constraint line.

**If a generated take comes back with a legible screen, it is a failed take.**
Re-roll it. Do not crop around it, blur it in post, or decide it is small enough
to be fine — a viewer pausing on a 1080p frame sees it, and the whole compliance
argument for this ad is that there is nothing in frame to read.

### Device continuity

The phone should look like the same object in all six shots: a plain modern
black slab, no brand mark, no camera-bump detail that dates it. Text-to-video
will drift on this across independent generations.

The cheap fix costs nothing extra: **generate Shot 1 first, pick the take, then
pass its frame as `image_references` (or `start_image`) on the other device
shots.** `seedance_2_0`, `seedance_2_0_mini` and `kling3_0` all accept it — see
the `medias[].roles` in `models_explore`. Without that, budget for more
re-rolls on continuity alone than on the shots themselves.

Each block below is ready to paste. Keep the trailing constraint line.

### Shot 1 (5s) — hook · "Crypto moves while you sleep."

*Establishes the device. Generate this one first — the rest reference it.*

```
A dark bedroom at three in the morning. A plain black phone lies face-down on a
wooden nightstand; a soft cyan glow leaks from under its edge and pulses gently,
once, as if something just arrived. Sheer curtains breathe. Far below and far
out of focus, a city grid burns orange through the window. Slow push-in.
Ultra realistic, 35mm anamorphic, shallow depth of field, heavy filmic grain,
deep navy and cyan grade.
The phone is face-down and its screen is never visible. No text, no user
interface, no brand marks or logos on the device.
```

### Shot 2 (7s) — "Seventy five pairs, every fifteen seconds."

```
Close on a hand holding a plain black phone, tilted steeply away from camera so
the screen reads only as a bright cyan smear across the glass. Fast ribbons of
light sweep across that glass and across the holder's cheekbone in repeating
waves, wave after wave, quicker than the eye tracks. Dark room, cold fog of
light. Camera holds, very slight drift.
Ultra realistic, photographic, shallow depth of field, volumetric light, deep
navy and cyan.
The screen must stay off-axis and unreadable — a glow, never an image. No text,
no user interface, no readable display, no brand marks or logos.
```

### Shot 3 (6s) — "Fifteen AI analysts score every setup."

```
Over the shoulder in a dark room. A plain black phone is held low and at a steep
angle, its screen a featureless bright bloom. Suspended in the air around and
behind it, fifteen tall translucent glass panes hang in the void, each catching
a different sliver of cyan light; they rotate slowly and settle into one aligned
rank facing the device. Volumetric haze, dust in the beams.
Ultra realistic, physically based glass and caustics, cinematic, deep navy.
The screen is a bloom with no detail. No text, no symbols, no numbers, no user
interface, no brand marks.
```

### Shot 4 (5s) — "The whole trade. Entry, stop, three targets."

```
A plain black phone lies flat on a dark desk, screen up but heavily out of focus
and blown out. Rising out of it into the air, a single luminous cyan line climbs
through the dark, crossed at five different heights by clean horizontal bars of
light. The camera rises alongside the light in slow parallax. Dust motes drift
through the beams.
Ultra realistic, cinematic, volumetric light, deep navy, shallow depth of field
with the phone soft in the foreground.
The screen is an out-of-focus wash. No text, no numbers, no axis labels, no
chart interface, no brand marks.
```

### Shot 5 (5s) — "Every position opens with a hard stop."

```
A plain black phone rests on a dark machined-steel surface, screen dark. A
heavy polished steel bar drops into frame in front of it and seats itself hard
across the slot with a burst of sparks and a hard cyan rim light, then comes to
absolute rest. High-speed camera, slow motion impact.
Ultra realistic, industrial macro, shallow depth of field, navy and steel.
No text, no markings, no engraving, no brand marks or logos.
```

### Shot 6 (5s) — "Connect Binance and Lumin can place it for you."

*The one shot where a 720p upscale will show, because of the skin. Worth the
premium tier on its own even if the rest are not.*

```
Night interior, low cyan light. Two hands: one holds a plain black phone tilted
well away from camera so its screen is only a soft out-of-focus glow; the other
hand sets something down and lifts away, opening, coming to rest — the work
handed over. The phone stays lit and unattended.
Ultra realistic, shallow depth of field, cinematic night grade, navy and cyan,
natural skin texture.
The screen must remain out of focus and unreadable throughout. No text, no user
interface, no app screen, no brand marks or logos.
```

### Shot 7 (8s) — "Your funds never leave Binance."

```
Foreground: a plain black phone held up, very soft and out of focus, its screen
a dim cyan glow. Behind it and sharp: a vault door of brushed steel, closed and
utterly still, one thin line of cyan light tracing the seam where it meets the
frame. Focus stays on the vault; the camera orbits it slowly while the phone
drifts at the edge of frame. Cold, quiet, immovable.
Ultra realistic, photographic, cold navy light, fine brushed-metal texture,
strong foreground bokeh.
No text, no dials, no numbers, no brand marks or logos on the vault or the
device.
```

### Shot 8 (6s) — "Paper mode. Prove it first."

```
Overhead. A plain black phone lies on a dark desk beside a sheet of architect's
tracing paper. The phone's cyan glow falls across the paper, and a faint
blueprint grid shows through its fibres where the light catches. A hand enters
and smooths the sheet flat. Slow push-in from directly above.
Ultra realistic macro, cinematic, navy and cyan, visible paper tooth, shallow
depth of field.
The phone's screen is at a grazing angle and unreadable. No text, no legible
drawing, no numbers, no letterforms, no brand marks.
```

---

## Status

**Not generated. Owner decision 2026-09-22: hold the spend.** The prompts,
script, timing and render path are finished and sit here ready; nothing has
been charged against the Higgsfield balance, which is still 0.

## Status of the render path

The `footage` scene type, the clip decode cache and the `SHORT CLIP` coverage
check were written for this ad and are **syntax-checked only**. The container
they were written in has neither Pillow nor ffmpeg, so nothing here has been
executed end to end and no frame has been rendered from a clip.

Saying so rather than implying it was tested: the first real run is the test,
and it should be run on one shot before all eight are generated.

## After generation

1. Download each clip to these **exact** filenames — `script.json` names them,
   and a mismatch fails the render with the path it wanted rather than
   rendering black:

| Shot | Save as |
|---|---|
| 1 | `footage/01_sleep.mp4` |
| 2 | `footage/02_scan.mp4` |
| 3 | `footage/03_analysts.mp4` |
| 4 | `footage/04_trade.mp4` |
| 5 | `footage/05_stop.mp4` |
| 6 | `footage/06_connect.mp4` |
| 7 | `footage/07_vault.mp4` |
| 8 | `footage/08_paper.mp4` |

   Re-generating a shot? Overwrite the same filename. The decode cache is keyed
   on the file's mtime and size, so a new take is picked up and the old one is
   not served from cache.
2. `python3 pipeline/render_reel.py reels/ad_01_all_features`
3. **Read the printed timing table before watching anything.** A scene resolving
   longer than its own clip is reported as `SHORT CLIP` and holds the last frame —
   visible as a freeze. Fix it by re-cutting the `until` anchor, not by looping
   the clip, which produces a jump.
4. Watch it once at full length with sound before it goes anywhere.

## Re-check before it ships

* Does any frame contain legible text, a number, or anything resembling an app
  interface? If yes it does not ship, whatever else is right about it — and the
  fix is a re-roll, not a blur or a crop. Scrub the device shots frame by frame
  at full size; a screen that is unreadable in motion can be perfectly legible
  on a paused frame, and pausing is exactly what a sceptical viewer does.
* Does the phone look like the same object in all six device shots? Drift here
  is the most likely reason a take needs redoing, and it is cheapest to catch
  before the voice is cut against the clips.
* Does any device carry a manufacturer's logo or a recognisable silhouette? Both
  are somebody else's trademark, invented.
* Is the risk line on the end card, on-frame? (`reelkit` draws it; confirm it
  rendered and is inside the safe area.)
* Is every spoken claim still on the verified list in `COMPLIANCE.md`? Re-verify
  if the onboarding has changed since 2026-09-08.
