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

## How she talks — natural, and why that is the dangerous instruction

**Owner, 2026-09-09: "let her talk with natural language like humans."** He is
right that the first three reels read as written copy rather than speech, and
this section is that note turned into a rule.

The rule has to be stated carefully, because *"talk like a human"* is the single
most likely instruction in this whole repo to produce a compliance failure — and
it would produce it while sounding better. The most natural thing a human being
ever says about a financial product is **"I use it, and it works for me."** That
one sentence is a testimonial, it is unsubstantiable, and it is the exact thing
the table above bans.

So:

> **Natural is a property of the SYNTAX, never of the CLAIMS.**
> Loosen the grammar. Never loosen the evidence.

Everything in the "She never says" table stays banned in the new register, and
it gets *harder* to police, not easier, because a conversational line slides
into a personal one without the writer noticing:

| Natural, and fine | Natural, and banned |
|---|---|
| "So — short version: a stop loss is the price where your trade closes itself." | "Honestly, stops have saved me so many times." |
| "How do you know if a signals app actually works? You don't. Not from a screenshot, and definitely not from me." | "Trust me, I've been running it for weeks." |
| "You can use it for a month, take the signals by hand, and pay nothing." | "I paid for Auto within a week, no regrets." |

The left column is a presenter thinking out loud. The right column is a witness
giving evidence. **She is never a witness.**

### What actually makes it sound spoken

Written copy and speech differ in structure, not in vocabulary, so "make it
friendlier" is not the note. These are:

* **Contractions, always.** *here's, doesn't, you're, it's, can't, won't.*
  "Do not" in a reel is a robot reading a form.
* **Fragments are a full stop.** "Not one you found out about." "That's it."
  "All of them." A fragment is how emphasis works out loud.
* **Open on a real second-person question**, then answer it. "How do you know if
  it actually works? You don't."
* **Discourse markers carry the turns** — *so, okay, look, right, here's the
  thing* — one per turn, never two in a row, and never as decoration.
* **Vary the sentence length hard.** Three long, one of two words. Uniform short
  declaratives are just a different robot from uniform long ones.
* **Say the objection out loud before the viewer does.** "Anyone who tells you to
  skip that part is selling you something."
* **No hype adjectives, still.** Natural speech is not excited speech, and the
  ban on *insane / secret / guaranteed / life-changing* is unchanged.

### Punctuation is the prosody — it is the only lever we have

`edge-tts` gives no SSML control in this pipeline, so **the commas and dashes
are the performance.** A comma is a beat; an em-dash is a longer one; a question
mark actually lifts the intonation. A paragraph of full stops is read flat
whatever the words are, which is precisely why the first three reels sound
written.

There is a second, non-obvious payoff and it is the reason to over-punctuate
rather than under-punctuate: `captions.mark_punctuation` reads clause and
sentence marks back off the script to decide where a caption line may break. So
punctuation that makes her *sound* like she is thinking also makes the on-screen
captions break where a person would breathe. One change, both surfaces.

### The voice itself does not change

Still `en-US-AvaNeural` at `+10%`. Three reels are already public in that voice
and a fourth in a different one is a different presenter, not a better one — the
rule above about never changing the voice per reel is unchanged and is now
load-bearing rather than tidy. **The naturalness comes from the writing.**

### She does not lip-sync, and that is a stated limit

Checked 2026-09-09: the Higgsfield account is still `free` with **0 credits**, so
generated talking-head video costs money and is not available. Every reel is
therefore her *narrating over stills* — which is what a presenter does, and it is
honest, but it is not the same product as a character who visibly speaks.

The `talk` scene is the zero-cost answer to how much of her a reel can hold:
the camera breathes (`motion.handheld`), and the app arrives as an **inset
beside her** rather than as a cut away from her, so a claim can be evidenced
without leaving the shot. That took character presence from about a quarter of a
reel to roughly sixty percent. Going further than that needs one of two owner
decisions, and both cost something — see `content/POSTING_CALENDAR.md`.

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
