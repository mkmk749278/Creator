# What this channel may and may not claim

Lumin is a **live financial product on the Google Play production track**, and
the engine repo's own doctrine already carries the rule this file extends:

> **Never fabricate signal performance numbers.** — `360-v2/CLAUDE.md`, Hard Limits

Marketing is the easiest place in the whole system to break that rule, because
nothing in CI checks a caption.

---

## The one test

**Every claim in a reel must be pointable at a screen in `capture/app/screens/`
or a line in the app's own onboarding.**

If you cannot point at where a sentence is true, it does not ship. That is the
entire test, and it is why the capture step exists — the reels are cut from a
real signed-in session, not from a mock-up somebody designed.

## Banned outright

| Banned | Why |
|---|---|
| Any return, profit, or rupee/dollar figure | Unsubstantiable performance claim |
| Any win rate or accuracy percentage | Same, and the engine's own cells are small-sample |
| "Guaranteed", "risk-free", "passive income", "double your money" | Unfalsifiable and regulator-bait |
| A screenshot of the P&L or signal-book panels | Contains a live realised-P&L figure. `pipeline/prep_screens.py` deliberately excludes the Pulse P&L plates for exactly this reason |
| Lia claiming personal results | Fabricated testimonial — see `brand/CHARACTER_BIBLE.md` |
| Redrawn, retouched or "cleaned up" numbers in a screenshot | The plates are cropped only. Nothing is repainted |
| Comparison claims about named competitors | Cannot be substantiated from anything we hold |

## Safe, because the app says them

Verified against the onboarding and Signals screens captured **2026-09-08**:

* "AI-powered USDT futures signals with automatic execution on your Binance account."
* "Every 15 seconds, the engine scans 75 USDT futures pairs."
* "15 AI analysts score each signal — momentum, structure, volume profile, regime."
* "Your funds never leave Binance."
* "Trade-only API key. Read + trade permissions only. Withdraw is never requested."
  (and, per the engine's hard limit, **a key with withdraw permission is auto-rejected**)
* "Stop-loss on every position. Every open trade has a hard stop."
* "Paper mode — prove it first. Run the full engine on simulated trades before going live."
* "Every signal is free." Automation (Assist / Auto) is the paid tier.
* Entry, SL and TP1–TP3 are shown on every signal.

**Re-verify this list whenever the onboarding changes.** It is a copy of
somebody else's screens, which makes it exactly the kind of constant that goes
stale silently — re-run `pipeline/capture_app.py` and read the plates.

## Required on every reel

1. **The risk line on the end card**, rendered on-frame, not only in the caption.
   Captions collapse behind "more" on most feeds; the end frame is what a viewer
   is looking at when the reel loops. Wording is the app's own consent copy:

   > Crypto futures trading carries substantial risk of loss. Lumin signals are
   > informational only and are not personalised investment advice.

2. **The same line in the caption text**, in full.

3. **18+.** The app's own consent gate requires it; the channel should not
   undercut its own product.

## Two things to check with the owner's counsel

Flagged, not resolved here — both are jurisdiction questions that an engineer
should not answer alone:

* **India / ASCI.** Advertising touching virtual digital assets carries a
  prescribed disclaimer and placement rules. Lumin is a signals app rather than
  an exchange, so whether the VDA rules bite is a legal call. The end-card line
  above is written to be compatible with them either way.
* **Meta financial-services advertising.** Organic reels are not ads, but the
  moment any of this is put behind paid promotion, financial-services
  authorisation may apply in some regions.

## When the app changes

A reel showing a screen that no longer exists is worse than no reel — it is a
promise the product does not keep. Re-capture and re-render after any change to
onboarding, the Signals card layout, or the free/paid split.

---

## The one test is now machine-checked (2026-09-09)

"Every claim must be pointable at a screen" was, until now, enforced by a human
remembering to look. `pipeline/reelkit/proof.py` makes it structural for the one
place it can be:

* A `talk` scene's inset names a **claim key**, never a crop box. A key with no
  entry in `PROOF` raises at render time.
* Each entry binds a claim to a plate and a **normalised** region, so a
  re-capture at a different device resolution moves the crop with the screen
  instead of silently pointing somewhere else.
* `python3 pipeline/check_proofs.py` renders every region to
  `capture/app/proofs/_contact_sheet.jpg`. **Look at that sheet after every
  re-capture.** A region that has slid half a row off its claim still renders a
  perfectly convincing card — of the wrong sentence, which is worse than a
  blank one, because a blank prompts a question.

This does not make a *caption* compliant, and it never will. It only enforces
that a claim shown in-frame is a claim the app actually makes.

### Two crops that are deliberately tighter than they look

Both of these are the whole reason the table has comments in it:

* **`one_signal` stops ABOVE the live percentage row.** The Signals card carries
  the position's unrealised move (`+0.15%`, `-1.82%`). It is the app's own
  number and it is not cherry-picked — but enlarged into an inset under a
  promotional headline it reads as a result, and the ban above is on a
  performance figure whatever its provenance.
* **`live_or_paper` is only the Live/Paper toggle**, and must never be widened.

### …and the line that distinction implies, stated so it is not re-derived

Cropping the percentage out of the inset while `07` and `08` still show the
whole Signals screen — percentages included — looks inconsistent until the rule
behind it is written down. It is this:

> **Showing the screen as it is, is showing the product. Isolating and
> enlarging one number under a promotional headline is making a claim.**

A viewer reading the real Signals list sees a mixed book (`+0.15%`, `-1.82%`,
`+0.11%`) at the size the app renders it, in the app's own layout, and reads it
as *what the screen looks like*. The same `+0.15%` pulled into a card captioned
"ONE SIGNAL" and blown up to a third of the frame is doing something else, and
the fact that we chose which row to crop is exactly what makes it a claim.

Reel 03 has shipped on that basis since launch, so this is the existing
practice made explicit rather than a new rule. **It is still a judgement call
and the owner may take the stricter line** — pan the `screen` scenes onto the
entry/stop/target rows only. If he does, `07` and `08` need a pan change and a
re-render, and nothing else.

## `trade_connect.png` is not a promotional plate — and reel 02 uses it

Found 2026-09-09 by looking at the plates rather than at the code that loads
them. `capture/app/screens/trade_connect.png` contains, below the toggle:

> ⚠ **Status unknown — could not reach engine. Toggles below may not reflect
> actual state.** Retry

…and a *"Connect your Binance account · Details (3 to fix)"* warning card.

Both are **correct product behaviour** — that banner is the engine's tri-state
readability copy, and the app is right to say it could not reach the engine
rather than to guess. It is also, in a promotional reel, an advertisement for a
broken app showing an error the viewer has no way to read as a good sign.

**`02_funds_never_leave.mp4` is live on the account and its `duo` scene puts
that plate in the phone.** At 476px wide the orange banner is small, but orange
on a dark UI is the only warm thing in the frame and the eye goes to it. This is
an owner call, not an engineer's:

1. Leave it — the banner is barely legible at that size; or
2. Re-render 02 against `onboard_funds_safe.png`, which carries the same claim
   and no error state (~2 minutes, the reel would need re-uploading); or
3. Re-capture the Trade tab from a session where the engine is reachable, which
   fixes the plate for every future reel.

**(3) is the real fix** and it is the one that also refreshes every other plate.
Until then, no new reel uses this plate except through the `live_or_paper`
proof region, which crops to the toggle and excludes the banner entirely.
