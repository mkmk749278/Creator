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

So every shot below is **atmospheric or metaphorical**, and where a phone
appears it is held at an angle with the screen as an out-of-focus glow. The
prompts carry `no text, no UI, no numbers` for that reason, not for style.

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

Each block is ready to paste. Keep the trailing constraint line — it is doing
the compliance work, not decorating the prompt.

### Shot 1 (5s) — hook · "Crypto moves while you sleep."

```
A dark bedroom at three in the morning. A phone lies face-down on a nightstand,
its edge catching a faint cyan glow. Sheer curtains breathe. Far below and out
of focus, a city grid burns orange through the window. Slow push-in.
Ultra realistic, 35mm anamorphic, shallow depth of field, heavy filmic grain,
deep navy and cyan grade.
No text, no user interface, no visible screen content, no logos.
```

### Shot 2 (7s) — "Seventy five pairs, every fifteen seconds."

```
Inside a dark server aisle. Ranks of indicator lights pulse in fast waves of
cyan down a long corridor, wave after wave, cold fog pooling at floor level.
Slow dolly forward between the racks.
Ultra realistic, photographic, volumetric light, deep navy and cyan.
No text, no user interface, no readable displays, no logos.
```

### Shot 3 (6s) — "Fifteen AI analysts score every setup."

```
Fifteen tall panes of translucent glass suspended in a black void, each
catching a different sliver of cyan light. They rotate slowly and settle into
one aligned rank. Volumetric haze, dust in the beams.
Ultra realistic CGI, physically based glass and caustics, cinematic.
No text, no symbols, no numbers, no user interface.
```

### Shot 4 (5s) — "The whole trade. Entry, stop, three targets."

```
A single luminous cyan line climbs through dark space, crossed at five
different heights by horizontal bars of light. The camera rises alongside it in
slow parallax. Dust motes drift through the beams.
Ultra realistic, cinematic, volumetric light, deep navy.
No text, no numbers, no axis labels, no chart interface.
```

### Shot 5 (5s) — "Every position opens with a hard stop."

```
Macro, high-speed camera. A heavy polished steel bar slams down and seats
itself across a dark slot. A burst of sparks, hard cyan rim light along the
bar's edge. Slow motion impact, the bar comes to absolute rest.
Ultra realistic, industrial macro, shallow depth of field, navy and steel.
No text, no markings, no logos.
```

### Shot 6 (5s) — "Connect Binance and Lumin can place it for you."

```
Night interior. Two hands in low cyan light: one holds a phone tilted well away
from camera so its screen reads only as a soft out-of-focus glow; the other
hand lifts away and comes to rest, the work handed over.
Ultra realistic, shallow depth of field, cinematic night grade, navy and cyan.
The screen must stay out of focus and unreadable.
No text, no user interface, no app screen, no logos.
```

### Shot 7 (8s) — "Your funds never leave Binance."

```
A vault door of brushed steel, closed and utterly still. One thin line of cyan
light traces the seam where it meets the frame. The camera orbits slowly around
it. Cold, quiet, immovable.
Ultra realistic, photographic, cold navy light, fine brushed-metal texture.
No text, no dials, no brand marks, no logos.
```

### Shot 8 (6s) — "Paper mode. Prove it first."

```
Overhead macro. A sheet of architect's tracing paper lit from beneath by cyan
light, a faint blueprint grid showing through the fibres. A hand enters and
smooths it flat. Slow push-in from directly above.
Ultra realistic macro, cinematic, navy and cyan, visible paper tooth.
No text, no legible drawing, no numbers, no letterforms.
```

---

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
  interface? If yes it does not ship, whatever else is right about it.
* Is the risk line on the end card, on-frame? (`reelkit` draws it; confirm it
  rendered and is inside the safe area.)
* Is every spoken claim still on the verified list in `COMPLIANCE.md`? Re-verify
  if the onboarding has changed since 2026-09-08.
