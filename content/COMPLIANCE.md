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

## Generated footage

Added 2026-09-22 with `reels/ad_01_all_features`, the first reel built from
AI-generated video rather than captured plates.

The one test at the top of this file — *every claim must be pointable at a
screen* — was written for a channel whose footage came from a real signed-in
session. Generated footage breaks the assumption underneath it: there is no
screen to point at, because the frame was invented.

So the rule for generated material is not a relaxation of that test. It is a
split:

> **The footage carries no claim. The typography carries every claim, and the
> typography is checked against the list above exactly as before.**

That is why the shots in `SHOTLIST.md` are atmospheric or metaphorical — a
server aisle, a vault door, tracing paper — and why every prompt ends in
`no text, no user interface, no numbers`. Those lines are doing compliance
work, not styling.

### Banned in generated footage, on top of everything above

| Banned | Why |
|---|---|
| A generated Lumin interface, screen, card or feed | It is a repainted screen — the row already banned above — and "ultra realistic" makes it worse, not better: a viewer cannot tell it from a capture, and neither can a reviewer |
| Any legible number, price, percentage or P&L in frame | A depicted trade the engine never emitted, at a price nothing traded. The engine's hard limit ("never fabricate signal performance numbers") does not stop at the repo boundary |
| A legible chart with axes or labels | Same: it asserts a specific market that did not happen |
| A generated person shown as a user, customer or trader-with-results | A synthetic testimonial. Worse than Lia claiming results, because it reads as a real third party. See `brand/CHARACTER_BIBLE.md` |
| A generated Binance, Google Play or exchange mark | Someone else's trademark, invented |
| A phone screen in focus and readable | Whatever is on it is fabricated UI by definition. Keep it angled, out of focus, or a bare glow |

### Allowed, and why it is enough

Abstract and atmospheric footage, hands and environments where no product claim
attaches, and the brand's own typography drawn by `reelkit` over the top. Every
feature on the verified-safe list can be *said* in type; none of them needs to
be *depicted* to be understood.

If a shot only works because the viewer reads something in the frame, the frame
is making the claim — and it does not ship.

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
