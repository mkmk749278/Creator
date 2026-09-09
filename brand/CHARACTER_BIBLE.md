# Lia — character bible

The presenter for the Lumin Instagram channel. One character, used consistently,
so the feed reads as one voice rather than a pile of unrelated posts.

Owner-supplied assets, 2026-09-08: two hero portraits (1024×1536) and two
character sheets. They live in `assets/character/`.

---

## Who she is on camera

**Role: presenter, not customer.** Lia explains what the product does. She is
the brand's face in the way a presenter fronts a channel — she is not a user
giving evidence about her own results.

This distinction is the whole of her editorial rulebook, and it is not
stylistic. A named person making first-person claims about money made from a
financial product is a **testimonial**. A testimonial that cannot be
substantiated is the single most enforceable thing on this channel — by Meta,
by an app-store reviewer, and by a regulator. As a presenter she can say
everything the product actually does and none of that risk attaches.

| She says | She never says |
|---|---|
| "Lumin scans 75 pairs every 15 seconds." | "I made ₹40,000 last month." |
| "Every position opens with a hard stop." | "I never lose trades any more." |
| "Paper mode lets you prove it first." | "This changed my life." |
| "Every signal in the app is free." | "Trust me, it works." |
| "Here's what one signal gives you." | "My win rate is 80%." |

The right-hand column is banned outright. See `content/COMPLIANCE.md`.

## Voice and register

* Calm, plain, slightly dry. Explains rather than sells.
* Short sentences. One idea per line — the captions are word-timed, and a long
  sentence becomes an unreadable wall.
* Never hype vocabulary: no *insane*, *secret*, *guaranteed*, *easy money*,
  *life-changing*, no rocket or money-bag emoji.
* Second person. "You get the whole trade", not "users receive".

Voice-over: `en-US-AvaNeural` at `+10%` (edge-tts). Registered in
`pipeline/reelkit/brand.py` so every reel sounds like the same person. **Do not
change the voice per-reel** — an inconsistent voice breaks the character faster
than an inconsistent look.

## Look

* Portraits are used full-bleed with an eased push-in, never static.
* Brand elements already in frame (the Lumin sign, the Lumin mug, the laptop)
  are an asset — frame to keep them.
* Deep top scrim under any headline. White type on a lit face is the fastest
  way to look amateur.
* She shares the frame with the app in `duo` scenes. That shot — a face and the
  product in one frame — is the one that ties the two together, so at least one
  belongs in every reel.

## AI disclosure — an owner decision, recorded

**Owner decision, 2026-09-08: the account does not label Lia as AI-generated.**

Recorded here because it is a standing decision, not an oversight, and whoever
picks this up next should not quietly reverse it. The risk that was raised and
accepted: Meta's synthetic-media policy, and advertising-standards regimes
generally, treat an undisclosed synthetic endorser as a disclosure problem when the
character makes claims a real person would be vouching for.

The mitigation that is **not** optional, and that this repo enforces: Lia is a
**presenter, never a testimonial witness**. She describes product behaviour that
is demonstrable on screen. She makes no claim about her own results, because
there are none. That keeps the undisclosed-character question a branding
question rather than a fabricated-endorsement one.

If the owner later reverses the decision, the change is one line in each
caption ("AI-created character") plus a line in the bio — nothing in the render
pipeline has to change.
