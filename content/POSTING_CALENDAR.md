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

---

# Weeks 2–4, filled (2026-09-09)

Five reels rendered, all character-led and in the spoken register. The queue
above is now stock rather than plan.

| # | File | Angle | Post as |
|---|---|---|---|
| 04 | `04_stop_loss_saves_you` | What a stop loss actually saves you | **Week 2 Tue** |
| 06 | `06_three_checks` | Three checks before you trust any signals app | **Week 2 Thu** |
| 05 | `05_paper_mode_prove_it` | Don't trust it — test it | **Week 2 Sat** |
| 07 | `07_named_setups` | Named setups, not mystery calls | **Week 3 Tue** |
| 08 | `08_free_and_paid` | Every signal is free. Here's what isn't | **Week 3 Thu** |

**Ordering is deliberate: the two most useful-to-a-stranger reels go first.**
04 and 06 teach something to somebody who never installs anything, which is the
cheapest reach on this category and the safest ground in `COMPLIANCE.md` — a
reel explaining a stop loss makes no claim about Lumin at all. 08 is last
because pricing only interests someone who already wants the thing.

Week 4 is deliberately empty. **Post fifteen reels before writing the
sixteenth**: by then Instagram's own per-reel panel can say which of these
formats holds attention, and guessing a week-4 slate now throws that away.

## What changed, and the one number that decides whether it worked

| | Reels 01–03 | Reels 04–08 |
|---|---|---|
| Scenes with Lia in them | ~28% | **~60%** |
| Register | written ad copy | spoken (`CHARACTER_BIBLE § How she talks`) |
| Product proof | a cut away to a phone | an **inset beside her** (`talk` scene) |
| Length | 22–25s | 26–31s |

The length went **up**, which is the one change here that could cost more than
it buys. Read **watched-to-end rate** on 04 against 01–03 before assuming the
new format is better: if it drops, the fix is to cut the narration, not to cut
Lia — the character is the thing being tested, and a longer reel is a confound
that has to be removed before the test means anything.

## Going further on the character — two owner decisions, both cost something

`talk` got her to roughly 60% of a reel using **two** photographs. That is close
to the ceiling: past this, the same two frames start repeating inside one reel
and the feed reads as a slideshow of one person. Two ways past it, and both are
the owner's call because both spend something:

1. **The 64-image pack originals.** `assets/character/lia_sheet_full.png` is a
   contact sheet of a photo pack — `01_front_neutral.jpg` … `64_reflection.jpg`
   — and the individual files are **not in this repo**. At ~118px per cell the
   sheet is a reference, not a source: a cell would need a 9x upscale to fill a
   frame. If the owner still has the originals, that is 2 usable portraits going
   to ~64, and it costs **nothing but the upload**. This is by a wide margin the
   highest-value thing available and it needs no decision beyond finding them.
2. **Video credits, if she is to visibly speak.** Checked 2026-09-09: the
   Higgsfield account is `free` with **0 credits**, so generated talking-head
   video is not available at zero cost. Everything here is narration over
   stills. A lip-synced presenter is a different and better product, and it is
   the first thing in this pipeline that would need a budget.

Option 1 first. It is free, it fixes the actual constraint, and it makes option
2 cheaper if it ever happens — a video model given 64 consistent references
produces a more consistent character than one given two.
