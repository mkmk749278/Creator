# Builder brief: Pixel 11 consensus video parts

You build ONE part of a multi-part video. Other agents build the other parts in parallel,
so stay inside your own folder `video/pixel11/<part>/` and touch nothing else.

## What exists already (scaffolded for you)
- `index.html`: root composition at 1920×1080, `data-duration` = voice length, the voice `<audio>`,
  the background, and the **host bar** (Maya/Leo chips plus live captions, already synced). Do not remove these.
- `HF_TIMINGS` in the page: every spoken line with `start`/`end` seconds. **Sync your visuals to it.**
- `shared/theme.css`: tokens and classes (`.scene`, `.eyebrow`, `.h1`, `.h2`, `.body`, `.glass`, `.chip`,
  `.good/.mid/.bad`, `.num`, `.src`, `.phone-img`). Use them so all parts match.
- `media/`: official Google images (see `media/media_manifest.json`). Use only these images.
  Cutouts (`*.png`) have transparent backgrounds. `*_social.jpg` are full-frame launch cards with Google wordmarks.
- Your part's beats, with the data each beat should show: `runs/pixel-11/script.json` (your part's `lines[].beat`).
- Facts and quotes: `runs/pixel-11/research/*.json`. **Every number, score and quote on screen must come from
  script.json or these files.** Never invent specs, scores or quotes.

## Rules
- Load the `/hyperframes` skills first (`hyperframes-core`, `hyperframes-animation`), and follow CLAUDE.md's HyperFrames rules.
- Visual content stays above the host bar: `.scene` already reserves the bottom 220px. Nothing may overlap the captions.
- One `<section class="clip" data-start data-duration>` per visual beat. Change the visual every 4–10 s,
  following the conversation (look at which line is spoken when). Fade scenes in and out; no hard cuts mid-sentence.
- Premium, calm motion: GSAP `power2/power3/expo` eases, parallax drift on phone images, staggered reveals,
  count-up numbers, animated bars. One paused timeline, already created as `tl`, with every tween at absolute seconds.
- No `filter: blur()` or `backdrop-filter` (they make rendering very slow); the background image already has the glow.
- No AI-generated images of phones. No other creators' footage. Quote reviewers in on-screen text, credited by outlet name.
- On-screen text: short (≤ 12 words per block), large (≥ 30px), high contrast. Readable on a phone.

## Done means
1. `npx hyperframes check` passes, with 0 errors and no contrast warnings.
2. `npx hyperframes snapshot --at <one time per scene> --no-end --describe false -o /tmp/claude-0/-home-user-Creator/5433c6b3-e644-596d-bb26-5a81f8ed6e2c/scratchpad/snaps-<part>`
   Then **look at every PNG**: no overflow, overlap or clipped text, and nothing over the captions. Fix and repeat (max 3 rounds).
3. Render: `npx hyperframes render --workers 2 --quality standard --output /home/user/Creator/runs/pixel-11/parts/<part>.mp4`
   Other parts render at the same time, so use 2 workers.
4. Verify with `ffprobe` that the duration matches `data-duration` and that an audio stream exists.
5. Report back in under 120 words: scenes built, render time, and any issues.
