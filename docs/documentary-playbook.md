# Documentary video playbook (lessons from the breath-hold video, Oct 2026)

How to turn the owner's voiceover into a finished documentary-style video for **Be Practical with
Kishore** (Telugu · English). Everything here was learned the hard way on
`runs/breath-hold/` (v1 → v5). Read it before starting any new narrated video.

## 1. What the owner wants (from his feedback, in order of importance)

1. **No slides, ever.** v1 was full-screen text cards, bullet lists, question marks and timers on
   gradients. The verdict: "a boring PowerPoint". Never put paragraphs or lists on screen, and never
   use a blank or gradient background.
2. **Every frame is real media, full screen:** video or photo with a slow Ken Burns move. The main
   subject (the real person, the real event) must dominate. Text ≤ 15 % of the screen: lower-thirds
   of at most 4 words, a small corner timer, a one-line credit.
3. **Cut every 2.5–3.5 s.** Change shot, angle or crop constantly.
4. **Real event footage beats stock.** Archive photos of the person from other years are a weak
   fallback. Hunt for the actual event (section 4).
5. **The picture must match the words literally.** "Audience and press went blank" needs the event
   audience, not a railway crowd. Only use generic B-roll where the narration is generic
   ("the world is rushing").
6. **Explain science with animation, not still images.** Anatomy plates and microscopy photos were
   rejected. Use the animated canvas shots in `video/doc/_shared/anims.js` (section 6).
7. **"Watch this clip" moments:** when the narration says "look at this video", pause the voice and
   play the original clip with its own sound. Keep these **short glimpses (3–5 s)**, never the
   full original. The video may run longer than the voiceover; it doesn't have to match it exactly.
8. **Channel branding:** banner intro on "welcome to Be Practical with Kishore", the small square logo
   in the top-left corner throughout, and the logo on the subscribe end card. Files are in
   `assets/brand/`.
9. Once he says a cut is fine, **stop changing it**. Deliver exactly that (for example, upscale it)
   rather than slipping in further edits.

## 2. Pipeline (all scripted; reproducible)

| Step | Tool |
|---|---|
| Voiceover blocks → one track (0.6 s gaps) | ffmpeg concat (see `runs/breath-hold/v2voice/`) |
| Transcribe Telugu | faster-whisper, chunked at pauses (section 3) |
| Hand-correct text → `sentences*.tsv` (start, end, text) | Claude |
| Subtitles | `scripts/make_srt.py tsv` → `srt` (shifted by pauses) |
| Edit decision list | `video/doc/edl.mjs`: beats, pauses, lower-thirds, timer, part edges |
| Asset registry | `video/doc/make_registry.py` → `registry.json` (owner `./assets/` files win) |
| Build parts | `node video/doc/build.mjs`, then `npm run vendor` |
| Check | `npx hyperframes check` in every `video/doc/p*/` |
| Render | `npx hyperframes render --workers 4 --quality standard`, ~0.5–1× real time per part |
| Music bed | `scripts/make_bed.py` (synthesised drone, pads, heartbeat, bowls; royalty-free) |
| Final mix | `LIVE=live.wav scripts/final_mix.sh OUT.mp4 voice_paused.wav bed.wav parts/p{1..8}.mp4` |
| 4K | `ffmpeg scale=3840:2160:flags=lanczos,unsharp…` of the approved 1080p (≈0.23× real time; 7.5 min ≈ 30 min) |
| Deliver | `scripts/upload_gofile.sh` (falls back to regional store servers), contact sheet, SRT, description |

Part boundaries must sit on beat edges. A pause beat (`{ pause: t, len }`) inserts silence into the
voice. `single: true` keeps a beat as one continuous shot. `mediaStart` sets the clip in-point, and
`live` + `liveGain` play the clip's own audio in sync.

## 3. Voiceover transcription (Telugu)

- **Don't** use long-window or VAD-batched Whisper. It silently drops 20–30 s stretches of Telugu
  and even outputs Kannada script.
- **Do:** cut the audio at pauses (`silencedetect -30dB d=0.25–0.3`) into 5–12 s chunks and
  transcribe each chunk (`language="te"`, `beam_size=5`, `condition_on_previous_text=False`,
  no VAD). `large-v3` takes about 40 s per chunk on 4 CPUs. `turbo` (large-v3-turbo) is several
  times faster and good enough, since the text gets hand-corrected anyway.
- Consume the faster-whisper segment generator **once** (list it) before reading both text and
  words, or the word timings come back empty.
- Get pause points from `silencedetect` on the original block, not from word timestamps.
- Background jobs over ~30 min get killed: write the JSON after every chunk so a run can resume.
- The ElevenLabs blocks end right on speech (no tail silence). Check the transcript ends cleanly to
  rule out truncation.

## 4. Finding real media (what works from this container)

| Source | Status | How |
|---|---|---|
| **Instagram reels** (fan/news pages, official accounts) | ✅ works | `yt-dlp https://www.instagram.com/reel/ID/`; wait between requests (HTTP 429 after a burst) |
| **News articles** | ✅ | `yt-dlp --simulate <article URL>` reveals embedded IG reels or YouTube IDs |
| **Agency photo galleries** (IANS via socialnews.xyz) | ✅ | WebFetch the gallery for image URLs, then curl the full-size `…F.jpg` (6000 px) |
| **Official trailers** | ✅ via the studio's IG post | Found embedded in an ANI article; Paramount India's trailer came as 1080p MP4 |
| **Openverse API** (Flickr CC, etc.) | ✅ | `scripts/openverse_fetch.py`; anonymous `page_size` ≤ 20; download with **curl** (Flickr's CDN 403s python-requests); skip `upload.wikimedia.org` |
| archive.org | ✅ but thin | `advancedsearch.php` with `licenseurl:*`; check every item (one "public domain" freediving film was a mislabelled re-upload) |
| Wikimedia Commons | ⚠️ rate-limited (429) for long periods | `scripts/commons_fetch.py`; shared egress IP, so parallel sessions make it worse |
| **YouTube** | ❌ blocked | 403 or "not a bot" even with the bgutil PO-token provider; Piped/Invidious mirrors are dead too. Ask the owner to download on his phone and attach the file or share it via Google Drive (readable with the Drive connector) |
| Pexels / Pixabay | ❌ need API keys | The owner could add keys as environment secrets |

- The auto-mode permission check blocks trying alternative YouTube clients to get past its bot
  check. Ask the owner first; he can approve the command in a non-auto mode.
- Parallel sessions didn't speed sourcing up, because every session shares the same rate-limited
  IP. They're only worth it for CPU-bound work.
- The owner has cleared using event clips, photos, the film name and trailer footage.
  Still **credit every source on screen and in the description**. Licensed stand-ins get honest
  corner tags ("ARCHIVE PHOTO · 2013", "ILLUSTRATIVE", "B-ROLL"), and a stand-in must never pass as
  event footage.
- Tell the owner about Content ID risk: fan reels usually carry added music (no speech, low spectral
  flatness, ~−15 dB).
- Always review search results on a labelled contact sheet and drop misfits. About a third were wrong:
  Kathakali instead of Kalaripayattu, tulips for "eyes", gardens, and a train bomb-blast photo.

## 5. Preparing footage

- **Vertical reels → 16:9:** crop the clean band above any burned-in captions (for example
  `crop=720:405:0:250`), then Lanczos-upscale to 1920×1080 with mild `unsharp`. Check every crop on a
  contact sheet. One crop came out too high and cut off the face.
- **Tall portrait photos** (agency 6000×9500): pre-crop to a 16:9 band at the top (face and
  shoulders). `object-fit: cover` crops the middle and gives a headless torso.
- Keep the **audio track** on clips used for "watch this" pauses. Encode the others with `-an`.
- Letterboxed trailers: `cropdetect`, then scale to fill.
- Look through the source before choosing in-points: 1 fps contact sheets with timecodes. In the
  trailer, Dhalsim was at 0:36–0:39, not in the first fight that looked like him.

## 6. HyperFrames gotchas (0.8.103)

- A `<video data-start>` **inside a div with `data-start`** fails `check` (StaticGuard). Video shots
  use an untimed wrapper (`data-vs`/`data-vd`) whose visibility the timeline toggles.
- The renderer paints **video frames over sibling overlays** in the same wrapper. Burn labels and
  credits into licensed clips with ffmpeg `drawtext`, or put overlays in a later layer.
- **Never add tweens at negative positions.** Per-part timer keys from other parts shifted GSAP and
  inflated a 45 s part's timeline to 2477 s. Clip keyframes to `[0, dur]` per part.
- Canvas animations (`anims.js`): draw from a proxy tween's `onUpdate`, using local time only (seeded
  RNG, pre-rendered blurred sprites). `snapshot` may show a canvas at t=0. Verify in Playwright
  (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, set `window.__timelines = {}` before load)
  by seeking and sampling pixels.
- Animation library: `blood` (RBC flythrough, `co2`, `acid`, `speed`), `lungs` (`hold`, `co2`,
  `spasm`, `alarm`), `neural` (`heat`), `ecg` (`from`, `to` bpm), `eeg` (`settleAt`).
- Canvas fonts: list a fallback (`Inter, Arial, sans-serif`), or the first frame renders in a serif.
- `data-*` field named `src` collides with the scene "source footnote". Use `img` for images.
- Never `--resolution 4k`. For a delivered cut, upscale the approved 1080p file with ffmpeg.

## 7. Sound

- Use two-pass **linear** loudness (one gain to −14 LUFS + limiter), not `loudnorm` single-pass.
  The single pass pumped the silent pauses up to almost narration level.
- Bed at `-15dB`, sidechain-ducked by voice **and** live clip audio; it sits ~20 dB under the
  narration and rises in pauses.
- Live audio: conch B-roll at gain 0, reels at +4 dB. Measure with `volumedetect` per section.
- `make_bed.py`: fades must fit inside short final chord segments (fixed).

## 8. Facts and honesty

- Check the event facts on the web before writing on-screen text. Reports disagreed (15 vs
  16 minutes), so say "as reported" and note the other figure in the description.
- Label unmeasured claims (heart rate, "40–50 % less oxygen") as narration claims or
  illustrations. Verbatim quotes only ("Ek baar ruk jao"); the brief's English line was a
  paraphrase.
- Keep the safety line ("don't try breath-holding without training") in the description and on the
  end card.

## 9. Delivering to a phone-only owner

- Gofile link for the MP4 (1080p ≈ 200–330 MB; 4K ≈ 1 GB), and send the contact sheet, SRT and
  description with `SendUserFile`.
- Report in plain words: what changed, what's still a stand-in, and any rights or Content ID
  risks.
- Commit sources, EDL, registry, transcripts, SRT and description. Large footage stays out of git
  (`assets/video/*`, `assets/raw/`, renders).
