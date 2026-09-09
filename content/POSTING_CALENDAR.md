# Posting plan — first four weeks

Three finished reels are a launch, not a channel. This is the schedule they slot
into and the queue of what to build next.

## Cadence

**Three posts a week: Tue / Thu / Sat, ~18:30 IST.** Chosen for the Indian
evening window, which is when a retail futures audience is actually on a phone.
Treat the time as a hypothesis — after two weeks, read Instagram's own
per-post reach-by-hour and move it, rather than defending the guess.

Consistency beats volume. Three a week held for a month outperforms daily for
nine days and then nothing, and the pipeline in this repo makes three a week
cheap.

## Week 1 — what it is

| Day | Post | Purpose |
|---|---|---|
| Tue | **Reel 02** — Your funds never leave Binance | Leads with the objection, not the pitch. Best cold-audience opener |
| Thu | **Reel 01** — What Lumin actually does | The explainer, for people the first one made curious |
| Sat | **Reel 03** — What one signal gives you | Product detail, converts the curious |

Posting the trust reel first is deliberate. A cold viewer's first question about
a signals app is "is this a scam", and answering it before pitching is what buys
the second view.

## Weeks 2–4 — the queue

Each of these is a `script.json` away, and each is checked against
`COMPLIANCE.md` before it renders.

| # | Working title | Angle | Assets needed |
|---|---|---|---|
| 04 | "What a stop loss actually saves you" | Educational; the app's hard-stop rule as the payoff | none new |
| 05 | "Paper mode: prove it before you fund it" | Removes the last objection | Trade tab, paper toggle |
| 06 | "15 analysts, one signal" | The AI-agents menu screen — real feature, unusual, screenshot-friendly | re-capture Menu → AI agents |
| 07 | "Named setups, not mystery calls" | The Coil Hunter / The Momentum Rider naming | Signals list (have it) |
| 08 | "Every signal is free. Here's what isn't." | Honest pricing — unusual in this category, and it builds trust | Plans screen (re-capture) |
| 09 | "Read the card: entry, stop, three targets" | Carousel, not reel — stills already rendered as posters | posters in `reels/*/out/` |

**Education outperforms promotion on this category** and it is also the safest
ground: a reel explaining what a stop loss does makes no claim about Lumin's
results at all.

## What to measure

Instagram's own per-reel panel, weekly:

* **Watched-to-end rate** — the only number that decides whether the format
  works. Below ~25% the hook is wrong, not the topic.
* **Drop-off point** — read it against the scene timings printed by
  `render_reel.py`. A cliff at one timestamp names the scene that lost them.
* **Profile visits per view** — whether the reel sells the account.
* **Link taps** — whether the account sells the app.

Do **not** optimise for likes. A crypto reel accumulates likes from bots and
from people who will never install anything.

## Rules of engagement

* Reply to every genuine question in the first two hours; the ranker rewards it.
* Use the templates in `CAPTIONS.md` for the two predictable questions, so the
  answer never drifts.
* **Never answer a returns question with a number** — point at paper mode.
* Delete-and-repost rather than editing a caption that contains a wrong claim;
  an edited caption keeps the original in the audit trail either way, and a
  wrong financial claim should not sit live while you edit it.
