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
