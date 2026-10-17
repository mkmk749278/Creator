# AI presenter: character bible and pipeline (trial)

Status: **trial, owner approved the test on 2026-10-12.** Nothing from this folder goes into a published film until the
owner approves the test cut (phase 3 below). Rules for using it are in PLAYBOOK §22 (AI presenter).

## The character (locked by the owner's reference, `reference/rest_A.jpg`, 2026-10-12)
An invented man (not a real person):
- South Indian, about 35, medium-brown skin, thick wavy black hair swept up, a full black moustache, no beard, no glasses.
- Charcoal-black button-up shirt with rolled sleeves, dark trousers.
- Manner: the "elder brother" from the channel charter. Calm, warm, sure of his facts, never preachy. He talks with his
  hands the way people do in a good conversation: open palms to explain, counting on fingers, one firm beat for emphasis,
  leaning in for the serious part.

## The set (locked by the same reference)
Grey fabric armchair, a black podcast microphone on a boom arm at frame left (never in front of the mouth: camera B
sits on his left, frame right, for that reason), warm lit shelves with books, cameras and a play-button award, vertical
wood slats, and a wall TV on the right showing the channel logo. Warm, soft, shallow depth of field.

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
| 1–2 | Stills (camera B, wide) and gesture library: 17 clips × 2 cameras + 1 wide, 8 s each, first frame = last frame = rest still (Veo in Flow) | owner pastes `flow-agent-brief.md` into the Flow agent once | ~36–70 generations; check the per-clip credit price Flow shows, use Fast for tries and Quality for keepers |
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
