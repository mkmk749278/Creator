# AI presenter: character bible and pipeline (trial)

Status: **trial, owner approved the test on 2026-10-12.** Nothing from this folder goes into a published film until the
owner approves the test cut (phase 3 below). Rules for using it are in PLAYBOOK §22 (AI presenter).

## The character (locked: every prompt repeats this word for word)
An original, invented man (not a real person, not resembling any actor or celebrity):
- South Indian, about 35, medium-brown skin, short neat black hair with a side part, short well-trimmed beard,
  friendly intelligent eyes, an ordinary, believable face. No glasses (reflections break lip-sync).
- Wardrobe: an open dark-navy overshirt over a plain heather-grey crew-neck t-shirt, dark charcoal chinos, a simple
  steel wristwatch on the left wrist. Plain fabrics only (patterns flicker and drift between clips).
- Manner: the "elder brother" from the channel charter. Calm, warm, sure of his facts, never preachy. He talks with his
  hands the way people do in a good conversation: open palms to explain, counting on fingers, one firm beat for emphasis,
  leaning in for the serious part.

## The set (locked)
A modern, dark, premium talk-show studio at night: charcoal walls with vertical walnut slats, a tall bookshelf with real
books and a small plant on the left, a warm brass floor lamp, and a large wall screen behind him on the right glowing
soft teal (#5ee1c2, the brand accent), out of focus. He sits in a dark-brown leather armchair, angled slightly toward
camera. Soft warm key light from camera left, gentle rim light, shallow depth of field, cinematic 35 mm look.

## How expressions and hand movement work
Lip-sync models (LatentSync, MuseTalk) **only redraw the mouth and jaw**. Everything else (head turns, eyebrows, hands,
leaning) comes from the base clip. So we generate a **gesture library**: about 18 base clips, each one acting out one
intent (explain, question, warning, shock, empathy …). The script already carries an emotion cue on every line
(`[serious]`, `[curious]`, `[shocked]` … from `build_script.py`). `gesture-map.yaml` maps each cue to the clips that
fit it, so the assembler picks body language that matches the words automatically.

Keeping people watching:
- **Two cameras.** Every gesture exists as a medium shot (camera A) and a close-up from a 3/4 angle (camera B). The edit
  cuts A ↔ B every 3–4 s on sentence breaks, which keeps the channel's "always moving" rule even on the presenter.
- **Gesture on the stressed word.** Each clip gets a `peak` time (the instant of the hand beat, the lean, the raised
  eyebrow), measured once after download. The assembler offsets the clip so the peak lands on the stressed word from the
  script timing (`scripts/align_script.py`).
- **Seamless chaining.** Every clip starts and ends in the same rest pose (hands relaxed on the armrests, looking into
  the lens), made with Flow's first-and-last-frame mode using the same still. Any clip can follow any other.
- **Short presenter stretches.** He opens the film, bridges chapters, delivers the "practical defence" act and closes.
  Real footage and animation carry the rest; he never holds the screen for more than ~20 s at a time. B-roll can sit
  in the wall screen behind him or take over full screen while his voice continues.

## Pipeline
| Phase | What | Who | Cost |
|---|---|---|---|
| 1 | Hero stills: the character in the set, 3 framings (Flow image model) | owner pastes prompts, ~5 min | a few credits |
| 2 | Gesture library: ~18 clips × 2 cameras, 8 s each, first frame = last frame = rest still (Veo in Flow) | owner pastes prompts, ~20 min total | ~36–70 generations; check the per-clip credit price Flow shows, use Fast for tries and Quality for keepers |
| 3 | Test: 30 s of an existing Bunty VO lip-synced with LatentSync and MuseTalk on a free Kaggle GPU, side by side | Claude | ₹0 (Kaggle: ~30 free GPU h/week) |
| 4 | Automate: GitHub Action → Kaggle notebook → presenter MP4 → HyperFrames composite | Claude | ₹0 |

Handing the clips over: save them in one Google Drive folder, share it as "Anyone with the link", paste the link in the
issue or chat. Drive downloads work from the cloud session.

## Honesty rules for the presenter
- He is not Kishore and is never introduced as Kishore. Viewers must not be led to think a real person is on camera:
  "Altered or synthetic content = Yes" on upload, a small "AI presenter" tag the first time he appears, and a line in the
  description.
- He never holds or demonstrates a product (Phone Consensus: no fake hands-on) and is never placed at a real event.
- His face and look are generated once and reused; never regenerate him to resemble a real person.
