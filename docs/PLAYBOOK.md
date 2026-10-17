# Production playbook

The one reference doc for this repo. `CLAUDE.md` holds the short rules every session must follow; this file holds
everything else: the full specs, how-tos, measurements and the lessons behind each rule. Every rule says **why**, so a
future session can tell when a rule applies and when it doesn't.

It replaces `HANDOFF.md`, `docs/documentary-playbook.md`, `docs/documentary-production.md`, `docs/fetch-video.md` and
`docs/phase0-report.md` (merged here in Oct 2026). Per-project READMEs and briefs stay next to their projects as records.

**Contents**
- Part A: How we work. 1 Owner and delivery · 2 Claude models · 3 Parallel sessions · 4 Quality first
- Part B: Documentaries. 4a Channel, language and audience rules · 5 The look · 6 Workflow and engines · 7 Script and voice · 8 Media sourcing ·
  9 Realistic animation · 10 HyperFrames · 11 Sound · 12 Facts, honesty and rights · 13 Render and deliver ·
  14 Pre-render review · 15 Lessons log
- Part C: Phone consensus pipeline. 16 Product and spec · 17 Claude in the pipeline · 18 Architecture and stages ·
  19 Control flow, secrets, evals · 20 Build phases · 21 Phase 0 measurements
- Part D: 22 Recommendations
- Part E: the owner's channel charter (verbatim)
- Part F: the owner's production handoff guide and style examples for English films (verbatim, 2026-10-15)

---

# Part A: How we work

## 1. Owner and delivery

- **Kishore works only from an Android phone** (GitHub app, Termux, SSH to a VPS, the Claude app). No PC.
  *Why:* every step must run in a cloud session, GitHub Actions or the VPS, and every result must be viewable on a phone.
- **Deliverables a phone can open:** a **Google Drive** link for the MP4 in the owner's `Creator` folder (1080p ≈ 200–330 MB,
  4K ≈ 1 GB), a contact sheet PNG/JPG, the SRT and the YouTube description, sent with `SendUserFile` (30 MB cap per file).
  **Google Drive replaces Gofile (owner, 2026-10-13).** *Why:* the owner already keeps a `Creator` folder there and opens it
  in the Drive app on the phone; Gofile links expire and need a browser. How:
  - **Drive layout (owner, 2026-10-15):** `Creator/English/<slug>/` and `Creator/Telugu/<slug>/`, one folder per video
    (the channel is the film's narration language, `lang.txt`); channel art in `<Channel>/_Channel/`; material for both
    channels in `Creator/_Shared (both channels)/`. Nothing loose in `Creator/`. *Why:* the owner runs two channels and
    finds a film's files on the phone by channel, then by video. Folder names are the repo slugs.
  - Videos: `scripts/upload_gdrive.sh --sub <Channel>/<slug> FILE…` (pinned rclone, uploads to `Creator/<Channel>/<slug>/`,
    prints a view link), e.g. `--sub English/insurance-ombudsman`.
    The Google Drive connector can't carry video-sized files (content goes through the tool call), so the script needs
    **`GDRIVE_RCLONE_TOKEN`**, a one-time setup on the phone: Termux → `pkg install rclone` → `rclone authorize "drive"`
    → sign in with the Drive account that owns `Creator` in the browser that opens → copy the one-line JSON it prints →
    Claude app → environment settings → Environment variables → `GDRIVE_RCLONE_TOKEN=<that line>`. New sessions pick it
    up. Until it exists, deliver the MP4 with `scripts/upload_gofile.sh` and say so.
    Two quirks (2026-10-13): the Claude app's environment field strips the JSON braces and the `access_token` key
    and drops the `expiry`, so `upload_gdrive.sh` rebuilds the JSON from whatever is left (the refresh token is
    enough). Links it prints are private file links; the owner opens them signed in. The script never turns on
    "anyone with the link" sharing. The first two uploads (the VO blocks) did get link sharing before this fix.
  - Small text deliverables (description, SRT, `review.md`, `claims.csv`) can go up through the connector
    (`create_file` with `parentId` = the Creator folder `1NOCNjqPX5dOzKpp71oyEIIj0xoF-W68M`, `disableConversionToGoogleType`).
  - Owner footage and clips for a film: the owner drops them in `Creator/<Channel>/<slug>/` (zips are fine); sessions read them with the
    connector (`search_files` with `parentId`, `download_file_content`). Report in plain words: what changed,
  what is still a stand-in, any rights or Content ID risk.
- **Git:** all work lands on `main`. *Why:* in Oct 2026 nine stale session branches hid finished work; one branch keeps
  everything findable. Parallel sessions (§3) each push to their own branch and folder, and the coordinator merges them
  into `main` the same day, then deletes the branch.
- **Once the owner approves a cut, stop editing it.** Deliver exactly that cut (upscale, captions), nothing more.
  *Why:* on breath-hold, slipping in further edits after approval cost a review round.
- English first; keep all script and on-screen text i18n-ready (Telugu is already in use for the documentaries).
- **Owner setup status (2026-10-08).** Done: cloud environment *Full Access* (Gofile, Dailymotion, NASA and the rest of §8.1
  reachable); `PIXABAY_API_KEY` as an environment variable (verified from a new session: search, 4K download). Optional, add
  only when a video needs it: `YT_COOKIES` repo secret (YouTube via the Fetch workflows), `UNSPLASH_ACCESS_KEY`,
  `FREESOUND_TOKEN`, a NARA key, `ANTHROPIC_API_KEY` repo secret (only for API stages in GitHub Actions; cloud sessions
  don't need it). Pexels has paused new keys. Keys go in the environment settings (Edit → Environment variables; network
  secrets don't fit APIs that take the key in the URL, like Pixabay), never in chat or the repo. A new variable reaches
  only sessions started after it was saved.

## 2. Claude models: what they can do and where we use them

Facts from the Claude API reference bundled with Claude Code (cached 2026-10-06). Re-check with the Models API
(`client.models.retrieve(id)`) before relying on a number; prices and limits change.

| Model | ID | Context / max output | Price in / out per MTok | Best at (for us) |
|---|---|---|---|---|
| **Claude Opus 5.5** (default) | `claude-opus-5-5` | 1M / 128K (300K on Batch, beta) | $4 / $20 · cache read $0.20 · batch −50% | Everything that matters: research synthesis, fact-check, script, HyperFrames code, visual QA |
| Claude Fable 5.1 (most capable) | `claude-fable-5-1` | 1M / 128K | $10 / $50 · cache read $0.25 | Hardest reasoning and long autonomous work. Use only when the owner asks; 2.5× Opus price |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M / 128K | $2 / $10 | High-volume work where Opus quality isn't needed. **Not used by default** |
| Claude Haiku 5.5 | `claude-haiku-5-5` | 1M / 128K | $0.10 / $0.50 (≤100K prompt) | Cheap bulk classification. **Not used by default** |

**What Opus 5.5 is good at, and how we use it**
- **Reads images precisely.** Even at `low` effort it reads charts, diagrams and screenshots more accurately than Opus 5
  did at its highest. Dense or technical images still gain from higher resolution and from letting it crop and zoom with
  PIL/OpenCV in a container. *Use:* contact-sheet review of every asset, frame QA of renders, checking that on-screen data
  matches the VO (the 168/90 monitor mistake, §15).
- **Doesn't invent sources.** Much less likely to state a figure or cite a source the inputs don't support; more
  detail-oriented on large inputs (a date on the wrong weekday, a chart that doesn't match the figures). *Use:* fact-check
  pass on every script, at `max` effort.
- **Agentic coding.** At its default `medium` effort it matched Opus 5's `high` on multistep repo work with half the tokens.
  *Use:* writing HyperFrames compositions, engines and assembly code; render → snapshot → look → fix loops.
- **1M context.** All transcripts, articles and the script fit in one call: cross-source synthesis without chunking.
- **Design defaults.** Asked for visuals with no direction, it falls back on a few stock styles, and "avoid a generic
  look" just swaps one default for another. **Name the specific patterns to avoid** (§5 lists ours), look at the first
  result, and extend the list.
- **Limits.** Input is text and images only: no video or audio. Video is checked through extracted frames and contact
  sheets; audio through transcripts, `silencedetect` and `volumedetect`. Knowledge stops at June 2026, so every fact comes
  from collected sources.

**API rules** (enforced in `pipeline/llm.py`; details in `CLAUDE.md`): thinking is always on and can't be disabled;
set depth with `output_config.effort` (API default is `medium`, so always set it); forced `tool_choice` returns a 400,
so get JSON with `output_config.format`; read only `text` blocks; check `stop_reason` for `refusal`/`max_tokens`;
stream big requests; cache the shared prefix in `system` with a 1h TTL; enable the server-side refusal fallback.

## 3. Parallel sessions: finishing faster without cutting quality

**Facts (Oct 2026; sources: code.claude.com/docs/en/cloud-environments, /claude-code-on-the-web, /sub-agents, plus
measurements in a session):**
- **Each cloud session is its own VM:** about 4 vCPU, 16 GB RAM and 30 GB disk. N sessions = N× CPU for rendering.
- **Subagents** (the Agent tool inside one session) share that session's VM and CPU (up to 20 at once). They speed up
  waiting work (web research, fact-checks, reading contact sheets), not CPU work.
- **No documented cap** on concurrent cloud sessions, but all sessions **share the account's usage limits**: 6 sessions
  burn usage about 6× faster. No separate compute charge.
- **All sessions share the same outbound IP range** (Anthropic's proxy). Rate limits (Wikimedia 429, YouTube bot checks)
  hit every session at once, so **parallel sessions don't speed up media downloads**; they make 429s worse.
- **Idle VMs pause after a few minutes and can be reclaimed**, losing running jobs. Watch long renders with Monitor so the
  session stays active; start them with `nohup`.
- The GitHub proxy rejects **branch deletions and tag pushes** from sessions (the owner deletes branches in the browser).
- A coordinator session can start and steer others with the `create_session` / `send_message` / `get_session` /
  `list_events` / `archive_session` tools.

**Plan for one 10-minute documentary** (expected wall clock ~1–1.5 h instead of 3–4 h):
| Session | Job | Output |
|---|---|---|
| S0 coordinator | Locks script, VO and EDL on `main`; splits the EDL into ~2.5-min blocks at dip-to-black points; pins encode settings (size, fps, codec, GOP, bitrate cap, audio format) so parts join without re-encoding; starts the others | `projects/<slug>/edl.csv`, `parts.json` |
| S1 sourcing (one only) | All downloads at a polite rate, contact sheets, `media_manifest.csv`; subagents for parallel searching on hosts that don't rate-limit | manifest, contact sheets, URL list |
| S2–S3 animation | One HyperFrames/Three.js scene folder each (`video/<project>/<scene>/`), native 4K render | scene MP4s |
| S4–S7 render shards | Each pulls assets, renders its EDL rows | `projects/<slug>/parts/N/part.mp4` |
| S0 final | Concat (`ffmpeg -f concat -c copy`), music bed and ducking over the full length (never per part, to avoid seams), pre-render review, delivery | master MP4, contact sheet, SRT |

**Measured (2026-10-13, Jet Engine Paradox):** four scene sessions plus the coordinator hit the account's
**5-hour usage limit about 10 minutes after the scene sessions started**, before any of them had pushed anything.
All five stopped until the reset. *So:* run at most two heavy sessions beside the coordinator. Have each session push
code and upload renders after every finished scene, not at the end. Start the next pair only when the first pair is done.

**Rules:** each session owns one folder and one branch (no merge conflicts); same effort and quality in every shard; media
over 100 MB never goes in git (hand over by URL list and re-download, or a release asset/LFS after a test upload); archive
sessions when done; 6–8 sessions is the sensible maximum. Every new session runs `.claude/hooks/session-start.sh`
(npm install with vendoring, `.venv` with all extras, library fetch), so it is ready to render when it starts.
The `/parallel-render` skill walks through the whole procedure.

## 4. Quality first: never trim effort for speed

The owner's rule (Oct 2026): **accuracy and the best output matter more than speed.**
- Run Claude at full strength: `high` or `xhigh` effort for building, `max` for fact-checks (the lighter scope in §12) and final reviews. Never lower
  effort, skip a QA round, drop a fact-check or shrink research to finish sooner. *Why:* a wrong claim or a slide-like
  shot on a public channel costs more than an hour of compute.
- Get speed from **parallelism** (§3), caching and pre-rendering expensive layers, never from doing less.
- Research deeply: several independent sources per fact, the real event footage before stock, and a contact sheet of every
  asset before it goes into a cut.
- Fast mode stays off unless the owner asks (it costs 2× and only speeds up output tokens).

---

# Part B: Documentaries ("Be Practical with Kishore")

Applies to every narrated documentary or explainer (`projects/<slug>/`, `video/<project>/`, `episodes/<slug>/`).
The phone-review content rules (Part C) don't apply here.

**Role:** executive documentary director and motion-graphics engineer, at the standard of Vox, MagnatesMedia, Polymatter,
ColdFusion and Think Deep. **Goal:** turn a voiceover and a factual script into a cinematic, motion-heavy film. It must
look like a broadcast documentary or investigative film, **never a slide deck, corporate presentation or photo slideshow**.

**Owner's channel charter (2026-10-08, verbatim in Part E; it wins where it is stricter).** How it maps onto this playbook:
- **Mission and voice:** the "super-channel" for Telugu viewers: hooks with emotional urgency, a dark cinematic sound, clear
  chronology, Vox/Johnny Harris-style 2.5D visuals, and only peer-reviewed or primary legal sources. Narrator persona: the
  street-smart elder brother (అన్నయ్య), conversational Telugu, never victim-blaming (blame the system, not the viewer).
- **Four acts** (for English films the owner's 2026-10-15 structure in §4a-4 replaces this: lived-reality hook + open loop →
  forensic dissection → citizen's action plan → outro): (1) visceral hook (the charter's 0:00–1:15; timings are now proportions, see §4b), drone + ticking clock; (2) systemic betrayal / investigation, live-browsing
  mock-ups and highlighters; (3) climax and shock reveal, with **1.5 s of total music silence before the core truth and a
  braam/thud as the proof lands**; (4) practical defence: actionable, reassuring steps, warm outro. Science films map the
  same way: myth → mechanism → the real evidence → what you can safely do. A "Trojan horse" hook: open on the popular
  mystery, resolve it with verified truth (this pairs with §12: the fact-check decides what "truth" is).
- **Citation tag on every factual claim:** a small bracket tag, e.g. `[NATURE (1982) | HARVARD MONK STUDY]`, bottom right
  above the logo bug (`cite` column in `projects/fire-and-ice/assemble.py`).
- **Bunty script format** (ElevenLabs): blocks of **4,000–4,500 characters**, hard cap 5,000 (owner, 2026-10-09: the
  `eleven_v3` per-request limit; it replaces the charter's 100–130 words / 1,200 characters), as many blocks as the script
  needs. Count characters, not words. Listen to every block: if one skips, repeats or drifts in tone, regenerate it, and if
  that recurs, split the block at a paragraph; commas and full stops
  plus `...` for dramatic pauses (owner amended 2026-10-08); no stage directions, `!`, quotes or dashes; numbers as English
  number words in Telugu script (ఫైవ్ థౌసండ్, owner confirmed 2026-10-08); acronyms letter by letter in Telugu script;
  common English terms transliterated. *Why (owner):* prevents skipped characters, buffer drops and truncated takes.
  `scripts/align_script.py` still times these blocks (one sentence per TSV row).
- **Sound matrix:** VO peaks −2 to −3 dB; BGM −24 to −26 dB under speech; −12 dB in pauses (0.5 s ramps); 0 (silence) for
  1.5 s before reveals; impacts −6 to −8 dB; clicks/typing/whoosh −8 to −10 dB. Supersedes the −18 to −22 dB in §11.
  Master stays −14 LUFS, −1 dBTP.
- **Cadence:** visual reset every **3.5–5.0 s** (owner, 2026-10-15, §4a-4; replaces the charter's 3.0–3.5 s and the 2.5–4 s rule).
- **Engines:** the charter names FFmpeg and Python PIL/Matplotlib; HyperFrames (CLAUDE.md) stays the animation engine and
  FFmpeg the assembler, both running in cloud sessions because the owner has no PC (Termux can still run `assemble.py`).

### 4a. Channel, language and audience rules (research, 2026-10-08)
> **Owner's directive (2026-10-09): competitors are a reference, never a ceiling.** The channel studies (§4a, §4b) exist
> only to understand natural spoken Telugu, tone and cadence. Never treat a competitor's depth, format or length as the
> target: every film aims to outclass every existing video on its subject in research depth (primary sources, money
> trails, data), narrative tension, visual storytelling and retention, at the Johnny Harris / Vox standard.
Distilled from `docs/research/reports/Telugu YouTube audience and style.md` (30 evidence-graded rules with sources; notes
in `docs/research/research_notes/`). The charter stays in force; where the evidence disagrees, the owner decides (list at
the end). *Why this exists:* the big Telugu channels already win on warmth, presence and volume; none shows sources on
screen. Visible proof is this channel's edge, and it is what YouTube's satisfaction signals and policies reward.

**The market (measured 2026-10-08).** Day Trader Telugu 2.7M subs and Money Purse 2.12M (7–8 uploads a week, 17–27 min
daily shows); Kowshik Maridi's own channel 662K in about 8 months (the Boss Wallah audience followed his face); Think Deep
2.24M, V R Raja 1.78M + 1.93M, NB Show 1.33M (1–2 uploads a day, 9–18 min). Every channel's all-time top videos are
**evergreen** beginner explainers, mythology/science and "what happened that day" stories, not daily news. Viewers praise
warmth, sincerity and the patient "tuition master"; they punish thumbnails the video contradicts, long intros ("video
starts 2:32"), one-sided framing (the chit-fund backlash) and news made late for views. Thumbnails share one template
(AI-art scene, real face, 2–3 huge red/yellow words). No competitor shows a source on screen.

**Hook, structure, pacing**
- Deliver the thumbnail's promise on screen **by 0:30**, with no channel intro before it (YouTube's "intro" metric counts
  viewers still watching at 30 s). Act 1 may run to 1:15 only if the payoff lands by 0:30. (Strong)
- **No fixed length** (owner, 2026-10-09): the topic sets the runtime; every minute must earn its place. Built as
  **chapters of 2–4 min**, each with its own question and payoff;
  YouTube chapters in the description (00:00, at least three, each ≥ 10 s). (Moderate: viewing engagement medians cap
  near 6 min in a 6.9M-session study; Telugu explainers of 10–18 min hold millions of views.)
- Energetic delivery throughout; "reassuring" never means slow. Visual reset every 3.5–5.0 s with continuous motion (owner, 2026-10-15).
- The 1.5 s silence + braam is **untested**: use it once or twice per film and check the retention curve at those
  timestamps after publishing.
- **Every film gets its own art direction** (palette, texture family, motif) and varied act lengths, so the four-act
  engine never looks templated (YouTube's July 2025 "inauthentic content" rule demonetises mass-produced templates).
- Prefer evergreen topics: money and prices, scams, disasters, mythology-vs-evidence, body and space science, financial
  history (a Harshad Mehta story did 1.3M on Day Trader), plus a monthly "what changes from the 1st" explainer.

**Voice and Telugu (scripts and TTS)**
- ElevenLabs: Telugu works only on **`eleven_v3` / `eleven_v4` with `language_code: "te"`**; never Multilingual v2 or Flash
  v2.5 (re-check the models page each project). A professional voice clone runs on v4.
- All TTS text in **Telugu script**, English loanwords included (writing them in Telugu script cut code-mix word errors
  from ~0.8 to ~0.2 in one study); Latin script appears only on screen. Acronyms as people say them: spaced letters
  (ఆర్ బి ఐ) or a word (సిబిల్, ఇస్రో); gloss each once.
- Dramatic pauses: `...` is allowed in TTS text (owner's decision, 2026-10-08; ElevenLabs' own guidance uses it for
  pauses). Use it at real beats only (before a reveal, after a question), at most one per sentence. Listen to every take:
  if a block skips or cuts words around a `...`, regenerate it with a comma there and make the pause in the edit
  (`VO_PAUSE`). The other bans stand: no `!`, quotes, dashes or stage directions.
- One idea per sentence (about 8–15 words); no `;`, brackets, slashes, `&`, `#` or emoji in TTS text.
- **Spoken Telugu, heavy Tenglish** (owner, 2026-10-09; replaces the "one English word per clause" rule): talk the way
  NB Show talks, English words and short phrases wherever people really say them. No grandhika endings (-ము, వచ్చెను,
  -బడు passives). In TTS text every English word is still written in Telugu script. Full guide: §4b.
- **Dialect-neutral:** pan-regional words; never call one region's Telugu "pure" or another's "slang"; never a dialect for
  comedy or villains; "మన తెలంగాణ, మన ఆంధ్ర" framing. Test new voices with listeners from both states.
- **Ban list** (script, guests and clips): చండాలం and its forms; కటిక చీకటి (use కారు చీకటి); caste names as adjectives;
  proverbs that insult disability or gender. Name a caste only if essential and sourced. At most one proverb per segment.
  *Why:* SC/ST Atrocities Act cases have hit Telugu TV channels and a YouTuber over on-air caste remarks, and courts treat
  social media as "public view".
- Persona: the elder brother **and** the patient tuition teacher; warm, sincere, never yelling.

**Audience: emotions and sensitivities**
- Debt is mainstream, not shameful-rare: AP 43.7% and Telangana 37.2% of adults in debt (MoSPI 2020–21, highest in India);
  Telangana had the most debt-linked suicides in 2022 (NCRB, 1,163). Shame is the collector's weapon (loan apps messaged
  relatives and morphed photos). **Stories make the mechanism the villain, never the victim, and end with a practical
  exit** (verified portals, helplines).
- Steelman lived institutions (chits, gold loans, local lenders) with both sides' numbers; righteous anger targets
  documented wrongdoing, not "corporates" in general. No moralising about IT workers' "lifestyle inflation" without data.
- Suicide: Press Council of India / WHO norms: no method, place or victim images; "died by suicide"; a helpline on the end
  card (verify the current Tele-MANAS number at the source before use).
- Politics: attribute every contested figure ("NCRB says", "BRS claims"), show rival parties' numbers, no party colours or
  symbols; stars' cases stay allegations.
- Trust: 93% of investors rate finfluencers credible (SEBI survey 2025) and WhatsApp is the top misinformation source, so
  visible sourcing reads as respect. For debunks, show the original claim with its real date and source, not just "FAKE".

**Sources, packaging, distribution**
- Citation tag on every claim (charter), a **timestamped source list in the description**, a `Correction: [timestamp]` line
  for any error (YouTube shows a correction card), and the fact-check gate independent of polish. Sources: peer-reviewed
  papers, court rulings and regulator texts, plus primary official statistics (NCRB, MoSPI, RBI), labelled as such.
- Thumbnail: 2–4 large Telugu-script words, one concrete number or object, a real photo or footage frame, **delivered
  literally in the film**. No AI images of real people, baked-in "views" badges or unrelated politicians. Title: a Telugu
  hook plus English search keywords.
- Test 2–3 genuinely different packages with Test & Compare (judged on watch-time share; desktop Studio only, so the
  coordinator runs it).
- Cut 9:16 Shorts from each film's scenes with the related-video link; seek mentions from large non-finance Telugu creators.

**Compliance gates (hard, beside the fact-check)**
- Synthetic content: answer "Altered content = Yes" for any realistic synthetic scene of a real event or place; label
  browser mock-ups "SIMULATION" (no real-looking screenshots of real banks); illustrations "ILLUSTRATION". Cloning the
  owner's own voice is exempt from disclosure.
- Health: state the WHO/ICMR position, the mainstream view and a real skeptic beat; no realistic synthetic medical scenes.
- Finance (SEBI finfluencer rules): education only, no buy/sell/hold or IPO apply/avoid calls on named securities, no return
  promises; price charts of named stocks end at least 30 days before publishing (three months until the rule is
  clarified); "Educational only, not SEBI-registered" on screen and in the description; no broker affiliate links.
  Verify the circular texts on sebi.gov.in before the first finance film.

**Owner's decisions on the research questions (2026-10-08)**
1. Numbers: keep the charter's English number words in Telugu script (ఫైవ్ థౌసండ్, ట్వెంటీ లాక్స్), not Telugu number
   words. Decimals and percentages stay as the charter says (అర శాతం).
2. Voice: keep ElevenLabs "Bunty". No clone of the owner's voice.
3. Pauses: `...` allowed (see the voice rules above); the edit-made pause is the fallback when a take breaks.
4. Competitor audio: the owner asked for other routes instead of a phone listen. Tried 2026-10-08: listings work from the
   cloud; media from the container and from GitHub's runners hit YouTube's bot check. A VPS-runner try was cancelled:
   switching machines to dodge the block counts as routing around it (the auto-mode check stopped it). **Owner's call:
   skip the competitor measurement**; judge pacing, music and hooks from our own retention curves after publishing.
   If it is ever wanted: `YT_COOKIES` (§8.5) or Termux, then `scripts/study_opening.py` on the 18 picks in
   `docs/research/research_notes/Telugu YouTube audience and style/competitor_picks.tsv`.
   **2026-10-09:** the cloud was bot-blocked again; the owner chose Termux. `scripts/termux_study_picks.sh` fetches captions,
   full audio and the first 3 min at 360p for the 18 picks, zips and uploads to Gofile (study only, never used in films).
   **Measured the same day** (`competitor_measurements_2026-10-09.md` in the notes folder): Bunty's pace already matches
   NB Show; the hits master at −12.6 to −14.3 LUFS; the biggest hits cut about every 3.7 s; nobody opens with a greeting.
   The script-craft results are in §4b. (Gofile folders download from the cloud with headless Chromium: the API needs a
   website token that only the page's own script produces.)

### 4a-2. English narration by default (owner, 2026-10-11)
*Why:* the owner found Telugu-only films get low reach and fewer views; simple English widens the audience to all of
India while the topics stay India-first. Rules:
- **Simple Indian English**, not "international" English: words a school-educated Indian uses every day (pay, spend, bill,
  money, salary, loan, interest, due date), lakh and crore, rupees; no idioms, no rare words, no American slang. One idea
  per sentence, mostly 6–14 words. Same persona and craft as §4b (elder brother, talk don't read, ask then answer, `...`
  before a reveal, `?` on questions, a mid-film relevance turn).
- **TTS text:** numbers and amounts as words ("thirty thousand rupees", "twenty twenty five"), acronyms as normal capitals
  written phonetically for the voice (§4a-4: R-B-I, E-M-I, Sibill); no digits, `₹`, `!`, double quotes, brackets or `&`;
  em-dashes `—` are allowed for mid-thought pivots (owner, 2026-10-15). Voice Bunty on `eleven_v4`
  with `language_code: "en"` (check the first block for accent and pace before generating the rest).
- **Words a Class 8 student knows** (owner, 2026-10-11: "even simpler"): bill (not statement), last date (not due date,
  after the first mention), loan (not debt, outstanding), "still pending" (not owe), maths, cancelled (not set aside),
  good things (not benefits). Keep the real term when viewers will meet it on their bill, and explain it once in plain
  words ("interest free period: for these days, you pay zero interest").
- **No emotion cues** in the blocks handed to the owner (owner, 2026-10-11): leave the `emotion` column empty; the words
  and punctuation carry the feeling. Explain any must-keep term once in plain words.
- **Voice:** an Indian-accent English voice, not a US/UK narrator. Audition in ElevenLabs Voice Library (filter: English,
  accent Indian, male) with the same first paragraph: Bunty in English first (channel continuity), then conversational
  "elder brother" voices such as Aakash Aryan (Conversational and Steady), Aarav J (Cool and Wise Friend) and Rinoy
  (Professional Narrator); avoid ad, ASMR and over-dramatic narrator styles for explainers. Owner picks by ear; record the
  pick here.
- **Files:** `lang.txt` = `en` in the project folder makes the `en` column of `script.full.tsv` the VO and the `te`
  column an optional Telugu dub; `tools/build_script.py` lints English VO (`lint_en`) and builds the blocks from it.
- On-screen text, citation tags and the description were already English; nothing changes there.

### 4a-4. Owner's production guide for English films (2026-10-15)
The owner's *Production & Scriptwriting Handoff* and *Style Comparison* (verbatim in Part F) set the standard for every
English (Akash) film. They win over §4a-2 and the Part B charter where they differ. *Why (owner):* earlier English
scripts sounded like "a news reader / textbook drone": stacked short sentences made Akash drop pitch at every full stop,
lines like "Now let us understand…" sounded like a lecture, and raw acronyms were misread (`CIBIL` → "civil").

**Voice: the practical elder brother, talking across a table.**
- Never news-reader openers: "Now let us come to…", "First, one thing must be clear…", "Let us understand the maths in
  very simple words…", "In this video we will examine…".
- Lived Indian reality as the way in: salary day, WhatsApp family groups, auto rides, UPI, a police station, a bank
  branch, a night train. Acknowledge fear and confusion without talking down.
- **Sentence variety:** mix short punches with longer, flowing thoughts. Never three or more very short sentences in a
  row (the lint flags runs of 3+ sentences under 6 words). Use `...` where the listener needs half a second for a number
  or a reveal, `—` for a mid-thought pivot, `?` on every question.
- **Not cynical, not preachy:** never hopeless about India and never bashing its systems. Celebrate Indian engineering and
  capability, and examine the bottleneck honestly; the citizen who understands the system makes the country stronger.

**Phonetics for Akash (mandatory in VO text):** `Sibill` (CIBIL), `Loke Uh-daa-lut` (Lok Adalat), `Ray-rah` (RERA),
and letter acronyms with hyphens: `R-B-I`, `E-M-I`, `N-P-A`, `G-S-T`, `B-N-S-S`, `F-I-R`, `T-P-A`. Apply the same to
any acronym said letter by letter (R-D-S-O, R-F-I-D, C-R-S, L-H-B). Acronyms people say as a word stay as words (Isro,
Kavach). The English lint fails any bare capital acronym that is not on the project's word list. Amounts: the guide
allows `₹65,000` or `65 thousand rupees`; we keep **number words** in VO text ("sixty five thousand rupees") because
digits and lakh/crore grouping have been read the Western way.

**Structure (3 acts + outro, 8–12 min unless the topic truly needs more):**
1. **Lived-reality hook and open loop (0:00–~1:15):** an immediate Indian scenario, the popular myth (Trojan horse), and
   an **open loop inside the first 60 s** that names when the payoff comes ("around the eight minute mark, I will show
   you…"). The promised minute must be true in the final cut: check it against `align/` and fix the line if the edit
   moves it. Promise only what the film delivers (§12).
2. **Forensic dissection (~1:15–7:00):** the mechanism step by step; "what they tell you" vs "what the official document
   actually says"; real cases (court orders, CAG, inquiry reports). The 1.5 s silence + braam before the core reveal stays.
3. **Citizen's action plan (~7:00–10:30):** numbered steps the viewer can do (document → written escalation → statutory
   remedy), with **verified** helpline numbers and portals (each one is a claim row in `claims.csv`).
4. **Outro (~10:30–11:30):** connect the personal answer back to India's collective strength; one pinned-comment
   question; sign-off **"Know your rights. Stay practical. Jai Hind."** (adapt the first phrase to the topic if it
   doesn't fit).

**Visual direction (four pillars):** (1) document forensics: the real circular / order / report on paper texture,
yellow-orange kinetic highlighter on the clause, rubber stamps (`[VIOLATION]`, `[MANDATORY 60 DAYS]`); (2) interactive
maths models: never state a calculation, simulate it (dynamic ledger, balance bar turning green to red; worked sums as animated
HyperFrames simulations, not the whiteboard: see §4a-3 BOARD, owner 2026-10-16); (3) real geospatial and photographic evidence: satellite zooms, archive newspaper scans, official
press releases; (4) pacing: a visual reset every **3.5–5.0 s**, and **no unmotivated stock of anonymous office workers
typing**. Labels for illustrations, simulations and stand-ins (§5, §12) still apply.

**Script format:** every script ships a **screenplay view** (`screenplay.md`, built by `tools/build_script.py`):
`[TIME / SCENE] | [AUDIO VOICEOVER – AKASH] | [VISUAL FORENSICS & SOUND DESIGN]`, with `[VISUAL]`, `[ACTION]` and `[SFX]`
for every scene, plus the paste-ready voice blocks.

**Checklist before handing over a script** (the guide's §7): phonetics done; sounds like an elder brother, not a lecturer;
varied rhythm with `...` and `—`; every scene has visual forensics and SFX; open loop in the first 60 s; honours India
while telling the uncompromising truth. Facts still come only from `claims.csv` (§12): a style example in Part F is a
model of tone, never a source (its numbers are not verified).

**India maps (owner, 2026-10-16: "India map not good and accurate").** Draw India with its official boundary, never
land-only shapes that merge it with its neighbours: Natural Earth's India point-of-view countries
(`ne_10m_admin_0_countries_ind.geojson`, public domain) gives the outline India officially shows (full Jammu & Kashmir
and Ladakh, Arunachal Pradesh, Andaman & Nicobar and Lakshadweep kept even when tiny). Fill India, glow its edge, dim the
neighbours, state lines faint. Rail network: DataMeet Indian Railways (`github.com/datameet/railways`, CC0)
stop sequences, consecutive stops under 35 km apart joined (≈ 71,700 km against 69,439 route km); route corridors over
that graph (Delhi–Mumbai 1,377 km, Delhi–Howrah 1,440 km, both within 1% of the real distances). Natural Earth's own
railroads layer is too sparse (≈ 41,000 km). Overpass (OSM) is blocked from the cloud container. Builder:
`video/kavach-railway-reality/_D_tools/build_map.py`. Keep the whole country in frame unless a zoom is the point.

**Recording blocks in the chat (owner, 2026-10-15).** When a script is locked or a block changes, the reply itself carries
every block as its own fenced code block, ready to paste into ElevenLabs: a heading line above each (block number, length,
voice and settings, the file name to save as `voice/<code>-chN.mp3`), and nothing but the spoken text inside the fence.
*Why:* the owner works on a phone; a code block has a one-tap copy button, while a Drive `.md` or the repo needs opening,
selecting and scrolling. Drive and `bunty_blocks.md` stay as the record.

### 4a-3. Visual modes for explainers (owner, 2026-10-11)
*Why (owner):* "not only slides": viewers stay to the end when they see real life, watch the maths being worked out and
follow a character. Every explainer mixes, in this order of preference:
1. **REAL**: real footage of what the VO names (stock via the Pixabay API, Commons, credited news); a real cutaway inside
   any other shot that runs past ~4 s.
2. **MATHS AS ANIMATION** (owner, 2026-10-16, replaces BOARD): "Don't use that white board maths, use HyperFrames
   animations, but it should not look like a text slide; as much high-quality animation as possible for crystal-clear
   understanding." Every calculation is shown as the thing it describes, moving to scale: a train covering 36 m per
   tick of a stopwatch (not "130 ÷ 3.6"); a stop drawn as amber and crimson zones under a speed curve with a real-time
   readout and a TIME-LAPSE chip; a count filling a strip with a magnifier on one km; a 10×10 grid of 1% squares
   against a dashed "one tenth" row. Numbers ride on the picture as counters and dimension brackets; the sum itself
   appears at most once, small, in a lower-third (`OUR CALCULATION · …`). `video/lib/whiteboard` stays in the repo
   for other uses but is not used for maths unless the owner asks. *Why:* the whiteboard read as a text slide.
   Examples: `video/kavach-railway-reality/D1`, `D2`, `D3`, `D6`.
3. ~~TOON~~ **No animated character** (owner, 2026-10-11, after a first test: "cancel character, use any clip that
   syncs to the situation"). Every action the VO says is a real clip (Pixabay API, Coverr, Commons, owner footage).
4. **PROOF**: credited screen recordings of the real source page (bank, RBI, court, news) under a magnifier.
5. **SIM**: labelled phone/bill simulations only where the viewer needs to see a screen.
Plan these per line in `visual-plan.md` (time from `align/`), before sourcing and scene work.
**Owner's review notes (2026-10-11):** (a) *common-sense fit*: show what the line is about in the film's context; for a
money film that is the spend or the payment (card machine, bill, wallet), never the event itself (a wedding ritual for
"a family function" was rejected). (b) *the character* was then dropped altogether (see 3). (c) *no foreign money*: drop clips
showing dollars or euros in a rupee film (about half the "money/bills" stock results); prefer cards, phones, bills.

### 4a-5. Indian audience psychology and retention architecture (owner, 2026-10-17)
*Why this exists:* most Indian viewers watch on a phone, with distractions around them (an often-quoted YouTube figure
says about 80% of watch time in India is on mobile; YouTube said in 2025 that Indian adults spend over 72 minutes a day on
YouTube). A film that feels like a lecture, or holds back what the thumbnail promised, loses half its viewers in the first
minute, and YouTube then stops recommending the channel's next films. Our own uploads show it (§4a-7). Every script and
edit follows these four laws. Where they are stricter than §4a or §4a-4, they win.

1. **Lede first, no delayed payoff.** If the title or thumbnail names an event, rule, scam or trap (Balasore, Cashless
   Denied, the Minimum Due trap), that exact thing is **on screen and in the VO within the first 25 s** (was 0:30 in §4a).
   **No exposition in the first 2 minutes:** no background, definitions or history before the viewer has seen the
   high-stakes conflict. The explanation is earned *after* the viewer knows what broke or where the trap is.
   *Seen in our data:* the Kavach film's title asks about Balasore, but Balasore arrives at 5:41 of 8:34.
2. **The 3-tier hook (0:00–1:00).**
   - **0:00–0:08, the visceral trigger:** motion and stakes from the first frame. No logo sting, no static phone mockup,
     no greeting. Start in the middle of the crisis.
   - **0:08–0:30, the thumbnail paradox:** deliver the thumbnail promise and state the paradox common sense can't answer.
   - **0:30–0:55, the open loop:** give the viewer an exact mission ("at six minutes forty, I'll show you the exact
     clause that…"). The minute must be true in the final cut; re-check it after every re-edit (§13a). *Seen:* the
     Kavach VO promises Balasore "around the eight minute mark"; reel v2 has it at 5:41.
3. **Anti-lecture, blame the system.** The sharp, protective elder brother across a chai table, never a news reader,
   professor or corporate trainer. Banned openers: "Now let us understand…", "In this video we will examine…", "First,
   one must know…", "Let us look at the history…", and the softer "Today we'll…" agenda line. Never blame the viewer for
   not knowing the law; blame the fine print, the predatory design or the bottleneck.
4. **70/30 mixed-media realism.** Clean 3D or vector animation held alone for more than 4–5 s reads as a training module:
   inside a long explainer scene, cut in a real asset or make a strong angle change every 4–5 s. At least 25–30% of the
   visual track is real-world grit: archive news headlines, real street or trackside footage, gazette and circular PDFs
   with a kinetic highlighter, satellite imagery. The visual reset stays every 3.5–5.0 s (§5.1 rule 5).

### 4a-6. Sentence architecture: synthetic read vs human read (owner, 2026-10-17)
*Why:* ElevenLabs Akash (v4) infers pitch, warmth, tension and breath only from punctuation, sentence-length variety and
rhythm. Text written like a report (uniform 15–20-word sentences, passive corporate words, flat full stops) makes Akash
drop pitch the same way at every full stop: a drone. Text written like speech (a long visual sentence followed by a short
punch, `...` pauses, `—` pivots, `?` questions) reads like a person.

**The four rules**
1. **The breath test:** say each sentence aloud on one natural breath. Run out of air before the full stop and it is too
   long for Akash: it will sound rushed.
2. **Punctuation is musical notation:** `.` pitch drops, thought ends; `...` breath and about 0.5 s of held tension;
   `—` a conversational turn and a tempo change; `?` rises and pulls the listener in.
3. **No passive corporate grammar:** never "It has been observed that…" → "Look at what happened…"; never "Citizens must
   be aware…" → "Here's what they never tell you to your face…".
4. **Length contrast:** never three sentences of the same length in a row; follow a 20-word scene-setter with a
   4-word punch. This sits with §4a-4: never three or more very short sentences in a row either (the lint checks it).

**Before and after.** The examples teach rhythm only. Their facts were checked against our own fact-checks
(`projects/health-claim-trap/claims.csv` HC-08, `projects/kavach-railway-reality/fact-check.md`), and the VO text follows §4a-2:
number words, no digits, `₹`, `!` or double quotes. A real script re-verifies every fact (§12).

*Case 1, a cashless claim denied at the hospital.*
- ❌ Synthetic: "When a health insurance claim is rejected at the hospital, policyholders often experience severe financial
  confusion. Under the Insurance Regulatory and Development Authority rules, cashless approval should be processed
  smoothly. Now let us examine the five-year moratorium rule…" *Fails:* passive phrasing, uniform lengths, lecture turn.
- ✅ Human:
  > It's eleven thirty at night. Your discharge papers are stamped, the cab is waiting outside... and the man at the
  > T-P-A desk slides one sheet of paper across the counter. Three words, stamped in red. Cashless denied.
  > Now they want four lakh rupees from your savings before your family can leave that room — and all he says is, sir,
  > policy terms. Take a breath. That paper is not the final word. At five minutes forty, I'll show you the five year
  > rule that stops an insurer from rejecting a long-running policy for a pre-existing illness or a missed disclosure,
  > unless they can prove fraud.
  
  *Works:* a real place and hour, long lines against short ones, `...` for breath, `—` for the turn. (The original
  draft said the rule makes any rejection "illegal"; it covers non-disclosure and pre-existing grounds after five
  continuous years, fraud excepted, so the claim is narrowed.)

*Case 2, Balasore and Kavach.*
- ❌ Synthetic: "Automatic Train Protection systems like Kavach are designed to prevent collisions on Indian Railways… We
  must first analyse track signalling circuits and electronic interlocking…" *Fails:* turns some three hundred deaths
  into a case study and makes the viewer sit through definitions before any tension.
- ✅ Human:
  > Picture this. It's evening near Balasore, and the Coromandel Express is running at about one hundred and twenty
  > eight kilometres an hour... on a green signal. Clear line. Full speed. But ahead, the crossover is set the wrong
  > way — towards a loop line where a goods train is standing. Within hours, every phone in India asks the same thing.
  > Where was Kavach? Here's what the newsroom didn't explain... the signal itself was showing green. Feed a safety
  > computer the same wrong information, and it may believe the line is clear too.
  
  *Works:* present tense puts the viewer on the train, short bursts against slow pauses. (The original draft said Kavach
  "would have accelerated straight into that collision". Our fact-checked Kavach film says nobody can say yes or no for
  sure, and the Ministry told Parliament the crash was not linked to Kavach. Series continuity (§4a-4) forbids
  contradicting it, so the example stops at "may".)

*Case 3, the credit card minimum due.*
- ❌ Synthetic: "Credit card statements contain a minimum amount due figure that many consumers pay without realising the
  interest implications. Now let us look at the table…"
- ✅ Human:
  > You open your banking app on the fifth... and the bill says sixty five thousand rupees. But right below it, in bright
  > blue, there's a tiny number. Three thousand two hundred and fifty. Pay that, and the app says well done. What they
  > don't print on the front page... the moment you pay less than the full bill, your interest-free days are gone —
  > and interest runs on every swipe from the day you made it. Look at what happens next month.

### 4a-7. Channel performance and growth plan (measured 2026-10-17)
*Why this exists:* the owner asked where we are lagging and when the channel can earn. Numbers are the public channel
page on 2026-10-17 (joined 12 Aug 2026; 51 subscribers; 7 videos). CTR, average view duration and retention are only in
YouTube Studio: ask the owner for Studio screenshots (Reach and Engagement tabs per video) before the next decision.

| Video | Length | Age | Views |
|---|---|---|---|
| The $10 Billion Chip Gamble (semiconductor) | 10:50 | 10 d | 7,028 |
| India Landed on the Moon. Why Can't It Build a Jet Engine? | 9:23 | 2 d | 937 |
| Can't Pay Your Credit Card Bill? Know Your Rights (long cut) | 27:41 | 2 w | 439 |
| Credit Card Minimum Amount Due: The Interest Trap | 8:05 | 4 d | 50 |
| Cashless Claim Denied? The 5-Year IRDAI Rule | 8:46 | 2 d | 10 |
| Can't Pay Your Credit Card Minimum Due? What Happens Next | 11:29 | 3 d | 8 |
| Could Kavach Have Saved Balasore? | 8:35 | 2 h | 1 |

**What the data says (and the rule it gives us)**
1. **India's-capability stories pull views; consumer-rights explainers don't, yet.** The two "can India build it" films
   have 95% of all views. Personal-finance how-tos compete with huge channels for search, and a new channel has no search
   authority. *Rule:* lead with national engineering, strategy and "why can't India…" paradox films; carry money and
   rights topics inside a story with stakes, or as Shorts, until the channel has an audience.
2. **Too many uploads too close together.** Five long films in four days on a 51-subscriber channel: each gets only a
   small test batch of impressions, and three credit card films compete with each other. *Rule:* one to two long films a
   week, never two on the same topic within a fortnight.
3. **The title's brand suffix eats the mobile title.** "| Be Practical With Kishore" is 27 characters; phones show
   about the first 50–60. The one breakout title had no suffix. *Recommendation for the owner* (§13a; the owner decides):
   put the channel name in the description, not the title.
4. **Delayed ledes and false open loops** (§4a-5): fix them in the edit before delivery.
5. **No Shorts.** Shorts don't count toward watch hours but are the cheapest way for a new channel to be found and to
   gain subscribers. *Rule:* cut two or three 30–50 s vertical Shorts from every film (the hook, the reveal), each
   linking to the full film.

**Monetization maths** (YouTube Help, YPP overview, checked 2026-10-17). Ad revenue needs **1,000 subscribers and 4,000
public long-form watch hours in the last 12 months** (or 10 million Shorts views in 90 days). The lower tier (500 subs,
3 uploads in 90 days, 3,000 hours or 3 million Shorts views) unlocks memberships and Super Thanks only, no ad share;
India is eligible. With an average view of about 3 minutes (check Studio), 4,000 hours is about **80,000 long-form
views**; at a typical 1 subscriber per 100–200 views, 1,000 subscribers is about **1–2 lakh views**. Earnings: Indian
finance and education RPM is commonly quoted at ₹50–150 per 1,000 views (agency estimates; English above regional
languages; October–December higher), so **1 lakh views ≈ ₹5,000–15,000**. Plan from the real RPM in Studio once known.

### 4b. Talk, don't read: spoken Telugu narration (owner, 2026-10-09)
*Why:* the owner's rule is that a script must never sound like someone reading; it must sound like a person talking. The
Telugu leaders win on warmth and presence (§4a), and a written-register script read by TTS sounds like a news bulletin.
Refined 2026-10-09 with the measured transcripts of 18 competitor videos (numbers below are from that study).

**Voice and register**
- Write the way the owner would explain it to a younger cousin over chai: one idea per sentence, mostly 6–14 words, then
  an occasional very short line for punch ("అదే ట్రాప్.").
- **Heavy Tenglish, like NB Show:** English words and short phrases where Telugu people really use them (loan, EMI, bank,
  actually, simple గా, full clarity, same thing, game changer). The sentence frame and the verbs stay Telugu. In the TTS
  text every English word is in Telugu script (సింపుల్ గా, యాక్చువల్ గా); on screen Latin is fine.
- **Address:** మీరు for the viewer, మనం for shared feelings, discoveries and the practical-defence act ("మనం ఇప్పుడు
  చూద్దాం", "మనలో చాలామందికి ఇది జరిగింది"). Never నువ్వు.
- **Spoken forms, not written ones:** చేస్తాం / వెళ్ళాడు / ఉంది కదా, not చేయుదుము / వెళ్ళెను. Banned newspaper
  connectors: ఈ నేపథ్యంలో, ఈ క్రమంలో, అనంతరం, తద్వారా, కావున, సదరు, పేర్కొన్నారు, వెల్లడించారు. Say: తర్వాత, అందుకే,
  అంటే, చెప్పారు, బయటపెట్టారు.
- **Talk-markers** carry the feel of a conversation; use them, without repeating any one in back-to-back sentences:
  అసలు, ఇక్కడే, చూడండి, కదా, అంటే, సరే, ఇప్పుడు ఏమైందంటే, ఒక్క నిమిషం, ఆలోచించండి, నిజం చెప్పాలంటే.
- **Ask, then answer:** pose the question the viewer is thinking, pause, answer it ("మరి బ్యాంక్ ఎందుకు ఊరుకుంది?
  ... ఎందుకంటే...").
- **Glue words, measured** (per 1,000 words in the competitors' speech): కదా 5–9 (Kowshik, Money Purse, Day Trader),
  సో 5–11, అంటే 4–13, అండి / -ండి 5–8 (NB Show, Kowshik, V R Raja), అన్నమాట up to 6.5 (Kowshik), నేను 1–6. Our first
  script had almost none, which is exactly what makes text sound read. Aim for roughly 3–8 per 1,000 words each of కదా,
  సో, అంటే and అండి, plus the narrator's own నేను ("నేను చెప్తాను", "నాకు అనిపించింది") a few times a film; never the same
  marker in back-to-back sentences. Bunty reads Telugu script, so write them exactly as spoken.
- **Devices that work:** repetition for a number ("టెన్ కాదు, ట్వెంటీ కాదు, సిక్స్టీ నైన్"); one named everyday example
  (a person, a salary, a phone); a mid-film relevance turn ("ఇది మిమ్మల్ని డైరెక్ట్ గా ఎఫెక్ట్ చేస్తుంది"); an English line
  followed by its Telugu meaning with అంటే.
- **Pace:** Bunty already speaks at NB Show's pace (≈ 14.3 vs 14.0–14.4 characters/s); keep sentences short (NB Show's
  median is 8–10 words) and let commas and `...` make the pauses (NB Show leaves 10–13 pauses of 0.8 s+ per minute).

**How to start**
- Never open with "నమస్కారం, ఈ రోజు మనం... గురించి తెలుసుకుందాం". None of the 18 measured videos opens with a greeting.
  Open with one of the five patterns the hits use: a **cold-open story scene** (NB Show), a **bold claim with stakes**
  (NB Show, Day Trader), the **myth everyone believes** (Think Deep), a **stakes list + promise** ("ఈ వీడియోలో పిన్ టు
  పిన్ ఎక్స్ప్లెయిన్ చేస్తా, లాస్ట్ వరకు చూడండి", Kowshik) or a **question chain** ("అసలు ఇది ఏంటి? ఎలా వర్క్
  అవుతుంది? ఎవరికి లాభం, ఎవరికి నష్టం? నష్టం ఎవరికో తెలుసా... మనకే", Kowshik). Name and greeting come right after the
  hook (face and name within 15–20 s; NB Show flashes its name sting at 0:02), and the thumbnail's promise lands by 0:30.
- Subscribe asks: Kowshik asks at 21–26 s and Money Purse at 22–33 s, right after the promise; Think Deep and NB Show only
  at the end. One short ask right after the promise and one at the end is the common shape.

**Emotion through words and rhythm** (Bunty takes no emotion tags, so the text carries the feeling)
| Moment | How the text does it |
|---|---|
| Urgency (hook) | short sentences, direct questions, present tense ("ఇది మీకు కూడా జరగొచ్చు.") |
| Empathy | name the feeling plainly, no blame ("ఇది మీ తప్పు కాదు. సిస్టమ్ అలా డిజైన్ చేశారు.") |
| Righteous anger | concrete facts and numbers, then one short verdict line; anger at the mechanism, never the viewer |
| Reveal | build with two or three short lines, `...`, then the truth in one plain sentence |
| Reassurance (defence) | longer, calmer sentences, మనం, numbered practical steps said in speech ("ఫస్ట్ ఏం చేయాలంటే...") |
| Outro | warm and personal, like ending a phone call with family; then an opinion question for the comments with concrete options (NB Show, Kowshik), like/subscribe, "మళ్ళీ కలుద్దాం" (Kowshik, NB Show and Day Trader all sign off with "జై హింద్") |

**Length and structure**
- The topic sets the runtime (owner, 2026-10-09). The four acts are proportions, not timestamps: hook about 10–15%,
  betrayal 30–35%, reveal 20–25%, defence 25–30%. Cut anything that doesn't move the story; never pad to reach a length.

**Grammar, clarity and pronunciation (owner review, 2026-10-09).** The first Digital Arrest script failed the owner's
listen on three counts; each is now a lint rule in `tools/build_script.py`:
- *Acronyms:* spaced letters are misread because single letters are also words (ఈ = "this", ఓ = "oh/a"): Bunty said
  "ee D ni" and "oh tp lo". Write them as Telugu media do, as one word with long vowels: సీబీఐ, ఈడీ, ఓటీపీ, ఆర్బీఐ,
  ఎఫ్ఐఆర్, ఐపీఎస్, బీఎన్ఎస్ఎస్, ఏపీకే, ఎఫ్డీ, ఐడీ, ఐఫోర్సీ (I4C), సీఈవో, యూఎన్, డీకే బసు; URLs as said
  (సైబర్క్రైమ్ డాట్ గవ్ డాట్ ఇన్). Spell out an unpronounceable one instead (CFCFRMS → "ఈ సిస్టమ్ని ఐఫోర్సీ నడుపుతుంది").
  Gloss each acronym once ("ఈడీ, అంటే ఎన్ఫోర్స్మెంట్ డైరెక్టరేట్").
- *Questions:* end every real question with `?` (ఏముంటుంది?, తెలుసా?, ఎవరు?). A full stop makes Bunty read it flat.
- *Case endings* join the noun (పెద్దమనిషికి, కేసులో, ఫ్యామిలీకి, జైలులో). Skip the ZWNJ after a virama (లైన్లోకి):
  pronunciation is the same and it costs characters.
- *Clarity:* every sentence has a subject and a verb; reported speech is framed (`… అని అంటాడు`); name the person when
  "ఆయన/ఆమె" could point to two people; numbers stay English number words (సిక్స్ మంత్స్, not ఆరు నెలలు).

**Emotion cues (eleven_v4, owner 2026-10-09).** Each line may carry one audio tag in the `emotion` column, from the list in
`tools/build_script.py` (`[serious]`, `[tense]`, `[softly]`, `[sad]`, `[curious]`, `[shocked]`, `[urgent]`, `[firm]`,
`[warmly]`, `[hopeful]`, `[empathetic]`, `[dramatic pause]` …). Tag only where the feeling changes. Tags count toward the
5,000-character cap. Test block 1 first; if v4 reads a tag aloud, use the tag-free `bunty_blocks_clean.md`.

**Read-aloud test (every block, before TTS):** say it out loud. If any sentence sounds like a newspaper, a textbook or a
government notice, rewrite it. If you run out of breath, split it.

**ElevenLabs blocks:** 4,000–4,500 characters each, cap 5,000 (`eleven_v3` limit); break at a natural paragraph or scene
change, never mid-thought. Keep the punctuation rules in §4 (commas, full stops, `...`; no `!`, quotes, dashes or tags).

## 5. The look

### 5.1 Zero-tolerance rules (and why)
1. **No presentation cards, no delayed lede:** no full-screen text boxes, bullet lists, icon cards, summary slides or
   question-mark graphics on flat backgrounds, and the thumbnail's subject is on screen within 25 s (§4a-5). *Why:*
   breath-hold v1 was exactly that, and the owner's verdict was "a boring PowerPoint"; delayed reveals lose mobile
   viewers in the first 30 s (owner, 2026-10-17).
2. **No static canvas:** a motionless photo or flat colour never stays over **1.5 s**; a plain CSS gradient never counts as
   a background. The canvas always has camera motion, particle atmosphere or live video.
3. **85% real motion:** at least 85% of the runtime is moving video, screen recordings, kinetic data animation or B-roll.
   Stills are for authentic archival evidence only, and always animated (§5.4).
4. **Text ≤ 15% of the screen**, only as 2–4-word lower-thirds, locations/dates/telemetry, counters, timers and meters, or a
   one-line credit. Never paragraphs or lists.
5. **Visual reset every 3.5–5.0 s** (owner, 2026-10-15: a camera-angle shift, document push-in, kinetic callout or icon
   pop; was 2.5–4 s). *Why:* retention; long holds read as a slideshow, while cuts faster than the VO's thought felt
   choppy. The shot itself never stops moving (rule 2). Exceptions: LIVE clips and
   HyperFrames explainer scenes.
6. **Semantic lock:** every shot shows exactly what the VO says at that second (kidneys → renal animation, "CCTV
   isolation" → a high-angle surveillance view, "world record" → the actual attempt). *Why:* breath-hold showed a railway
   crowd for "the audience"; the owner rejected it. Generic B-roll only where the narration is generic.
7. **Real event footage beats stock**, and archive photos of the person from other years are a weak fallback. Hunt for the
   actual event first (§8).
8. **Avoid our known stock looks** (name them, per §2): floating glass cards, neon-on-black dashboards, centred title +
   subtitle on a gradient, icon grids, emoji, stock "scientist with test tube", generic space or lab filler.

### 5.2 Three layers in every frame
| Layer | Content | Rules |
|---|---|---|
| 1 Base (full screen) | Real footage, or a photo with continuous motion (Ken Burns 1.00→1.15 or a slow pan, parallax) | Never motionless |
| 2 Atmosphere | 35 mm grain, ~30% edge vignette, light leaks, optional 2.35:1 bars, low-opacity HUD/telemetry | Never hides the base |
| 3 Kinetic accents | Lower-thirds, counters, timers, callouts | Lower corners on a dark scrim, for readability on a phone |

### 5.3 Visual language by genre
Pick the genre before sourcing; it decides palette, media stack and accents.

| Genre | Palette | Media stack | Graphic accents |
|---|---|---|---|
| Science & medical | Deep navy, surgical teal, graphite | Electron-microscope loops, 3D anatomy, MRI/sonography, macro lab work, cell division | Focus callouts, animated yellow circles on the abnormality, telemetry grids |
| Biography & martial arts | Warm amber, chiaroscuro, 35 mm grain | Raw training footage, press conferences, archival newsreels, slow-motion performance, cultural demonstrations | Split screens, timecode counters, year stamps |
| Business & finance | Terminal charcoal, holographic chart sweeps | Trading floors, HQ aerials, currency printing, shipping lanes, factory automation | Isometric graphs, metric tickers, animated balance-sheet highlights |
| Tech, AI & digital | Matte black, electric cyan, neon phosphor | Data centres, circuit macros, browser UI mock-ups, terminals, wafer fabs | Terminal type, syntax highlights, network nodes |
| Philosophy, society & lifestyle | Desaturated monochrome with a saturated hero | Fast-motion crowds, commuter platforms, pupil macros, solitary landscapes | Pacing contrast: extreme speed, then sudden stillness |

### 5.4 Making stills move
When an authentic photo or document is irreplaceable:
1. **2.5D parallax:** cut the subject out (local model, `video/chipgamble/parallax.sh`); foreground scales toward 1.15×,
   background drifts to 0.95×.
2. **Atmosphere:** smoke, dust motes, light leaks or rain at ~15% opacity.
3. **Forensic magnifier:** on documents, scans or clippings, slide a magnifier or zoom circle over the exact line the VO
   reads; highlighter swipes on the exact words (`pdftotext -bbox`, as in the chip-gamble engine).
4. **Moving contact sheet:** 3–4 archival angles slide into a collage, one every ~1.5 s.

### 5.5 Owner's standing notes (from reviews; now rules)
1. Subject's **face and name within the first 15–20 s** (lower-third "NAME · born–died"); repeat the name lower-third when
   the VO says the name.
2. Stock or stand-in footage that could pass for the real event carries a permanent **"ILLUSTRATIVE FOOTAGE"** label
   (`+illus` in the EDL). Never give stock a CCTV/archival look; that look is for authentic footage only. Licensed stand-ins
   get honest tags ("ARCHIVE PHOTO · 2013", "B-ROLL").
3. **No on-screen data that contradicts the VO** (Prahlad v4 showed a monitor reading 168/90 under "vitals normal").
   Replace it with an honest, labelled graphic.
4. **No stock clip more than twice**; no filler space or lab footage. "When did what happen" gets a timeline graphic.
5. **Branding:** banner intro when the channel name is spoken (logo sting), small logo bug in a corner on every other shot,
   end on the logo end card with subscribe and YouTube end-screen zones. Files in `assets/brand/`.
6. **Science is explained with animation, never still plates** (§9). Label each "ILLUSTRATION", "ILLUSTRATIVE CURVE" or
   "HYPOTHESIS". *Why:* anatomy plates and microscopy stills were rejected on breath-hold.

## 6. Workflow and engines

Every video follows three steps, and each produces a file the owner can read on a phone:
1. **Asset manifest** (`asset-manifest.md` + `media_manifest.csv`): ID, file name, description, platform, exact search
   query, licence, credit, EDL slots. Before any code.
2. **EDL** (`edl.csv` / `edl.md`): timecode → asset → motion → overlay → text → sound and ducking cues → LIVE/VO_PAUSE rows.
3. **Assembly code** bound to the project's `assets/` folder; every scene's base layer is moving.

**Engines in the repo** (pick one per video; see §22 for the plan to unify them):
| Engine | Used for | Strengths |
|---|---|---|
| `video/chipgamble/engine.py` (HyperFrames, Python part specs) | The $10 Billion Chip Gamble | Scenes keyed to **spoken phrases** (`T("Enter Tata Electronics")`) resolved against word timestamps, so cuts land on words; 2.5D parallax, world map with routes, real documents with highlighter, data overlays, on-screen credits, `credits.py` |
| `projects/<slug>/assemble.py` (FFmpeg/Python, EDL CSV) | Prahlad Jani | Footage-led cuts; LIVE/VO_PAUSE breaks; per-shot cache (`out/tmp*/NNN.key`); `--check` for missing assets; HyperFrames inserts rendered separately |
| `video/doc/` (HyperFrames: `edl.mjs` → `make_registry.py` → `build.mjs`) | Breath-hold | Owner files in `assets/` win over stand-ins; canvas science animations (`_shared/anims.js`); live audio in sync |

Rebuild commands live with each project: `video/chipgamble/README.md`, `projects/prahlad-jani-drdo/README.md`,
`runs/breath-hold/README.md` and `assets/README.md` (owner footage drop-in for `video/doc/`). Part boundaries must sit on
beat edges; in `video/doc/` a pause beat (`{ pause: t, len }`) inserts silence, `single: true` keeps one continuous shot,
`mediaStart` sets the in-point, `live` + `liveGain` play the clip's own audio in sync.
Remotion and MoviePy are not installed; ask before adding them.

## 7. Script and voice
**Estimating VO length before TTS (2026-10-09):** `scripts/estimate_vo.py SCRIPT [--srt est.srt]` gives each block's
length, the total and estimated line cues, and flags blocks outside 4,000–4,500 characters or over 5,000. Bunty speaks
about **14.3 characters per second** (spaces and punctuation included; ~123 words/min), so **4,000 characters ≈ 4:40 and
4,500 ≈ 5:15**. Model fitted on fire-and-ice's 65 lines; held out, take totals land within 1%, lines ±0.5 s, starts
drift up to ~3.5 s. Prahlad Jani ran ~13.5 c/s, so plan with ±7%. Use it to size acts and draft the EDL; final timings
always come from `align_script.py` on the real VO. Re-fit the coefficients as more Bunty takes are aligned.


- **Timing comes from silence detection + the script, never from Whisper** (owner's rule, Oct 2026). No Whisper for
  transcription or translation. *Why:* Whisper on Telugu dropped 20–30 s stretches, looped, output Kannada script, hit
  token limits and cost CPU hours; and machine translation re-orders Telugu's SOV clauses into English SVO, so translated
  word timings drift out of sync with the picture. The script is already correct and in spoken order: only the line
  timings are needed.
- **Method: deterministic silence-to-script mapping** (`scripts/align_script.py VOICE.mp3 script.tsv --out <dir>`):
  1. `silencedetect` (−30 dB, pauses ≥ 0.15 s) finds every pause.
  2. The script is one spoken line per row: `te<TAB>en` (English optional). Split long sentences into rows where you want
     subtitle cuts. `te | en` works too, and ElevenLabs audio tags in `[brackets]` are ignored. The text
     never needs to "match" the audio's length: only each line's share of the text is used, and every boundary snaps to
     a real pause, so faster or slower reads and longer pauses don't matter. Missing or changed words only shift that
     line, which gets flagged. ElevenLabs keeps the exact text of every generation under History: copy it from there.
  3. Lines map in order to runs of consecutive speech chunks. A plain chunk N → line N mapping drifts (breath-hold: 116
     chunks at d=0.35 for 80 lines; some sentences pause mid-way, some have no pause between them), so a dynamic programme
     picks which pauses are line boundaries: each line's speech time matches its share of the script's letters, longer
     pauses and punctuation inside a line (where speakers pause) are preferred.
  4. Output: `align.json` (line, start, end, te, en, confidence), `subtitles.te.srt`, `subtitles.en.srt` (English text on
     the Telugu timing, one cue per line: no SOV/SVO drift), `align.md` (lines to check by ear).
  5. Attach visuals with `slots.csv` (semantic lock, §5.1).
- **Pauses between lines are never dead air** (hook of fire-and-ice: 20 pauses of 0.3–0.7 s, 11% of the runtime):
  - *Picture:* `slots.csv` gives every line a picture slot that runs until 0.15 s before the next line speaks, so the
    timeline has no holes and every cut lands in a pause ("cutting on the breath"), with the new shot leading the voice.
  - *Subtitles:* pauses up to 1 s keep the cue on screen until the next line (no blinking); longer ones leave a short gap.
  - *Sound:* the music bed lifts in each pause (it is ducked under speech) and whooshes or impacts land on the cuts.
    Pauses over 1 s become `VO_PAUSE` beats (ambience, a diegetic sound, a held reaction shot, §11).
- **Measured** on the breath-hold VO (7:05, 80 lines) against hand-checked speech onsets: all 80 lines in order, 75 starts
  within 0.15 s, ends median 0.05 s off; the only real miss (a one-word sentence opener attached to the previous line,
  0.94 s) was among the 9 lines flagged "check" (boundary that could sit one pause earlier or later). Listen to flagged
  lines only, and fix by splitting or merging script rows, or `--min-pause`.
- **No script?** Ask the owner for it (the owner writes or approves every VO script). Whisper only if the owner explicitly asks.
- **Voice:** the owner's recording preferred (helps YouTube's review of AI-heavy content); ElevenLabs VO in short blocks so
  retakes are cheap. Never synthesise a real person's voice or quote.
- **Subtitles:** from `scripts/align_script.py` (te + en); `scripts/make_srt.py` shifts them for programme time when
  breaks are inserted; rebuild after any timing change. Telugu translations of LIVE
  clips go in the EDL `subtitle` column.

## 8. Media sourcing

Tested from a cloud session on 2026-10-08 (HTTP status with `curl -L`; "yt" = `yt-dlp --simulate` worked). Sites change:
re-test a source when it fails, and update this table. Licence rows marked ✱ need checking per item.

### 8.1 What works from the cloud container
| Need | Source | Access | Key? | Licence for a monetised YouTube channel | Status |
|---|---|---|---|---|---|
| News / event | **Dailymotion** | `api.dailymotion.com/videos?search=` + yt-dlp | no | uploader's copyright: short, credited excerpts | 200, yt (often 240–480p) |
| News / event | **Internet Archive** | `advancedsearch.php` (`licenseurl:*`), `/metadata/<id>`, `/download/`; `youtube-*` mirrors | no | per item; Prelinger mostly PD/CC | 200, yt |
| News / event | Instagram reels (official, news pages) | yt-dlp; wait between requests | no | uploader's copyright: credited excerpts | works, 429 after a burst |
| News / event | Facebook public video | yt-dlp | no | uploader's copyright | yt |
| News / event | News articles | `yt-dlp --simulate <article URL>` reveals embedded reels/YouTube IDs | no | — | works |
| News / event | Agency galleries (e.g. IANS via socialnews.xyz) | WebFetch the gallery, curl the full-size `…F.jpg` | no | agency copyright: credit ✱ | works |
| News / event | TV News Archive / GDELT TV | `archive.org/details/tv`, `api.gdeltproject.org/api/v2/tv/tv` | no | research use ✱ | 200 |
| News / event | EU Audiovisual Service, UN AV Library | site | no | free with credit ✱ | 200 |
| India | DD News, newsonair (AIR) pages | site | no | copyrighted ✱ | 200 |
| India | ism.gov.in (SEMICON India gallery, press PDFs) | site | no | government, credit ✱ | used in chip gamble |
| Space / science | **NASA Images** | `images-api.nasa.gov/search` → `collection.json` → `~orig.mp4` | no | public domain (no logos/endorsement) | 200 |
| Space / science | NASA SVS | `svs.gsfc.nasa.gov/api/search/` | no | public domain | 200 |
| Space / science | **ESA** | `esa.int/ESA_Multimedia`, `dlmultimedia.esa.int` | no | many CC BY-SA 3.0 IGO; some ESA Standard ✱ | 200 |
| Space / science | **ESO** | `cdn.eso.org/videos/...` | no | CC BY 4.0 | 200 |
| Science | **Europe PMC** | `ebi.ac.uk/europepmc/webservices/rest/search` | no | CC BY yes, CC BY-NC no | 200 |
| Science | NCBI E-utilities (PMC) | `eutils.ncbi.nlm.nih.gov/.../esearch.fcgi?db=pmc` | optional | per article | 200 |
| Science | **Wellcome Collection** | `api.wellcomecollection.org/catalogue/v2/images` + IIIF | no | **filter**: many are CC BY-NC | 200 |
| Science | NIH 3D, CDC PHIL, NIH Flickr | site | no | mostly PD / CC0 / CC BY ✱ | 200 |
| B-roll | **Coverr** | `projects/prahlad-jani-drdo/tools/fetch_assets.py search coverr` (skip premium/temp/AI) | no (API needs key) | Coverr licence, commercial OK | 200 |
| B-roll | **Pixabay** (video up to 4K, photos ≤ 1280 px) | `scripts/stock_fetch.py search/get pixabay video|photo` (API + `cdn.pixabay.com`, tested 2026-10-08) | `PIXABAY_API_KEY` env | Pixabay Content License, commercial OK, no attribution required (we credit). **AI-generated items are mixed into results: the tool hides them** | 200 |
| B-roll | Vidsplay | site | no | free with attribution ✱ | 200 |
| Photos | **Openverse** | `api.openverse.org/v1/images/?license_type=commercial` (`scripts/openverse_fetch.py`, page_size ≤ 20, download with curl) | no | CC0 / BY / BY-SA | 200 |
| Photos | **Wikimedia Commons** | `scripts/commons_fetch.py`; files via `Special:FilePath/<name>?width=960` or `upload.wikimedia.org` thumbs at standard widths (250/500/960/1280/1920) with a descriptive User-Agent | no | per file (`extmetadata`) | files 200; **search API 429** at times |
| Photos | Library of Congress | `loc.gov/photos/?q=…&fo=json`, `tile.loc.gov` | no | per item ("no known restrictions") | 200 |
| Photos | Smithsonian Open Access | `api.si.edu/openaccess/api/v1.0/search` | free key (`DEMO_KEY` works) | CC0 items | 200 |
| Photos | Met Museum | `collectionapi.metmuseum.org/.../objects/<id>` → `primaryImage` | no | CC0 when `isPublicDomain` | 200 (search endpoint 410) |
| Photos | Rijksmuseum | `data.rijksmuseum.nl/search/collection` | no | CC0 / PD | 200 |
| Photos | Europeana | `api.europeana.eu/record/v2/search.json?reusability=open` | free key (`api2demo`) | per item | 200 |
| Audio | **Openverse audio** (Freesound previews) | `api.openverse.org/v1/audio/?license_type=commercial` | no | CC0 / BY | search 200; **`cdn.freesound.org` previews 403 from the cloud (2026-10-15)**: synthesise UI SFX in the mixer, take rail sound from clip audio, or the owner downloads |
| Music | Incompetech | site | no | CC BY 4.0 | 200 |
| Music | FreePD | site | no | CC0 | 200 |
| Music | ccMixter, Free Music Archive | `ccmixter.org/api/query`, site | no | per track; many NC: skip those | 200 |
| SFX | SoundBible | site | no | per clip ✱ | 200 |

### 8.2 Reachable with a free key (add as environment secrets; recommended)
Pexels (`api.pexels.com/videos/search`; **new API keys paused** in Oct 2026; `stock_fetch.py` supports it once
`PEXELS_API_KEY` exists): commercial use OK; the website 403s here but the API answers. Pixabay now works (§8.1). Unsplash (`api.unsplash.com`), Freesound (`freesound.org/apiv2`, CC0/BY/BY-NC per sound),
DVIDS (US military, public domain), NPS, Flickr API, NARA catalog (key by email to Catalog_API@nara.gov).

### 8.3 Blocked or not usable
| Source | Why |
|---|---|
| YouTube downloads | **Intermittent**: bot check / 403 most of the time, but a 720p download worked on 2026-10-08. Try `scripts/fetch_media.py` once; on a bot check, hand the exact URLs and ranges to the owner (§8.5). Metadata always resolves |
| Vimeo | yt-dlp now needs a login |
| Mixkit assets, Videvo, Mazwai (now Freepik) | 403 |
| C-SPAN, British Pathé, NOAA photo library, Sonniss, Musopen | 403 |
| PIB, Prasar Bharati archive, Films Division/NFDC, USGS, Cell Image Library, ESA/Hubble CDN | timeout / 502 / TLS errors |
| Gofile (delivery) | Works in the *Full Access* environment, but **replaced by Google Drive** (owner, 2026-10-13; §1). Fallback only |
| Google Drive API (`www.googleapis.com`) | **Reachable** (2026-10-13: 403 "unregistered caller" without a token, so the host is open); uploads need `GDRIVE_RCLONE_TOKEN` (§1) |
| Piped / Invidious YouTube mirrors | Dead |
| **Not allowed** even when reachable | Allen Institute (non-commercial, terms bar YouTube), JoVE and Science Photo Library (subscription/paid), **BBC Sound Effects** (RemArc: personal/educational only), AP Archive, Reuters, British Pathé (paid: ask first), anything NC or ND |

### 8.4 Fallback chains (best first)
- **News and event footage:** Dailymotion API + yt-dlp (search several uploads, keep the highest `height`) → archive.org
  (`youtube-*` mirrors, TV News Archive) → official reels on Instagram/Facebook and agency galleries → official agency
  sites (NASA, ESA, ESO, DD News, newsonair) → **owner fetches YouTube** on the VPS or phone (§8.5) → a credited article
  quote, flagged in the manifest.
- **India-specific footage:** Dailymotion → archive.org → DD News / newsonair pages → government galleries (ism.gov.in,
  ministry sites) → owner fetches PIB, Prasar Bharati or DD YouTube clips from the phone (mobile IPs are rarely blocked).
- **B-roll:** Pixabay API (`stock_fetch.py`, AI items hidden) → Coverr → NASA / ESA / ESO (space, Earth, labs) → Pexels
  (when a key exists) → archive.org Prelinger
  → owner downloads Mixkit/Videvo clips on the phone.
- **Archival photos:** Commons (`Special:FilePath`, back off on 429) → Openverse → Library of Congress, Smithsonian, Met,
  Rijksmuseum, Europeana → NARA (with a key). Check `https://en.wikipedia.org/w/api.php?...prop=pageimages` early: if a
  subject has no free photo, plan a credited article quote.
- **Science visuals:** HyperFrames animation first (house rule) → Europe PMC CC BY figures → Wellcome (CC BY/PD only) →
  NIH 3D, CDC PHIL, NASA.
- **Music:** YouTube Audio Library (owner downloads; free for monetised channels) → Incompetech (CC BY) / FreePD (CC0) →
  ccMixter / FMA tracks without NC → `scripts/make_bed.py` synthesised bed.
- **Sound effects:** Openverse audio (Freesound CC0/BY previews) → Freesound API with a token → SoundBible PD clips.

### 8.5 Getting YouTube footage legitimately
Never route around blocks with VPNs, proxies or alternative YouTube clients (the auto-mode permission check also blocks
this). Use one of:
0. **Fetch media for a video workflow** (for footage we will use: official channels, owner-cleared clips, CC). GitHub app →
   Actions → *Fetch media for a video* → slug + URLs separated by spaces, `URL@01:10-01:24` for a range, runner
   `self-hosted` for the VPS. The artifact has the MP4s, `fetched.csv` (title, uploader, licence) and timecoded contact
   sheets; save it to Google Drive for the session. Same script locally: `scripts/fetch_media.py OUT URL ...`.
1. **Fetch video workflow** (GitHub app → Actions → *Fetch video for study* → Run workflow → paste URL). The artifact has
   `video.mp4`, timestamped frames and contact sheets. Needs the `YT_COOKIES` secret: create a **throwaway** Google account
   (YouTube can flag accounts used for downloading; never the main or channel account), sign in at youtube.com in a
   private window of a browser with add-ons (e.g. Firefox for Android), export `cookies.txt` (Netscape format), close the
   window (stops cookie rotation), paste it into Settings → Secrets → Actions → `YT_COOKIES`. Re-export when runs fail
   with the bot check again. Choose `runner: self-hosted` to run on the VPS (helps only if its IP isn't flagged).
   The study workflow is **for analysing how other channels shoot**; their footage never goes in our videos.
2. **Phone (Termux, mobile IP):**
   ```bash
   pkg install python ffmpeg nodejs && pip install "yt-dlp==2026.8.19"
   yt-dlp --js-runtimes node -f "bv*[height<=720]+ba/b" -o "/sdcard/Download/%(id)s.%(ext)s" URL
   ```
   Then upload to Google Drive and give Claude the file name (sessions read Drive through the connector).

### 8.6 Sourcing rules (and why)
- **Fact-check before sourcing** (`/fact-check` → `claims.csv` → `scripts/claims_check.py`): sourcing for a claim that turns
  out wrong wastes the most time.
- **Contact-sheet every asset before use**, labelled. About a third of search results were wrong (Kathakali for
  Kalaripayattu, tulips for "eyes", a box in grass for "CCTV camera", a bomb-blast photo).
- **Filter licences in code, never by eye** (`license_type=commercial` on Openverse; Wellcome's first "heart" hit was
  CC BY-NC). Verify each file's licence on its own page; one archive.org "public domain" freediving film was a mislabelled
  re-upload.
- **One sourcing session at a time** (§3): every session shares one IP, so parallel sourcing only multiplies 429s. Use
  subagents for parallel *searching* on hosts that don't rate-limit.
- Send a descriptive User-Agent with a contact address; download Flickr files with curl (its CDN 403s python-requests).
- Images: JPEG q90, longest side ≤ 2400 px, ≥ 1200 px wide, original colours. Clips: MP4 H.264 1920×1080 (pad or scale,
  never stretch), 30 fps, trimmed to the best 5–20 s; keep audio only for LIVE/diegetic use.
- `what_it_shows` in the manifest must be literally true ("Vidyut Jammwal at the Commando 2 trailer launch, 2017", not
  "the 2026 event").

### 8.7 Shared asset library (`library/`)
Licence-clean media reused across videos: HDRIs today; models, textures, music beds, stings and verified B-roll as they are
found. `library/manifest.csv` is the record (id, kind, file, licence, licence URL, attribution, source page, sha256).
Files ≤ 5 MB are committed under `library/<kind>/`; larger ones live in `library/_cache/` (gitignored) and come back with
`python3 scripts/library.py fetch` (the session hook runs it). Add with `scripts/library.py add --kind … --id … --url …
--title … --source-page … --author … --licence … --licence-url …`; it refuses non-commercial licences. `check` verifies
every row. A composition uses an item by referencing `vendor/library/<kind>/<file>`. *Why:* sourcing is the one step
parallel sessions can't speed up, so every licence-clean asset found once should never be searched for again.
Current items: `hdri/` studio_small_09 (neutral studio), brown_photostudio_02 (warm, biography), kloofendal_48d_partly_cloudy_puresky
(daylight sky), all Poly Haven CC0 at 1k.

## 9. Realistic animation

HyperFrames renders in headless Chrome with **SwiftShader (CPU) WebGL**, deterministically: everything must be a pure
function of time `t`. Today's 3D scenes (`video/prahlad/kidney3d`, `bladder3d`, `autophagy3d`; three 0.181.2) already use a
seeded RNG, `renderAt(t)` driven by `hf-seek` / `window.__hfThreeTime`, ACES tone mapping, physical materials and
RenderPass → UnrealBloom → OutputPass. Ranked upgrades (cost figures unverified unless marked; measure each on a 2 s shard
first):

1. **Real HDRI lighting instead of `RoomEnvironment`.** Biggest realism gain for almost no per-frame cost (PMREM is baked
   once). Poly Haven CC0 studio HDRIs at 1k–2k (reachable, HTTP 200). Keep the background a dark plate.
2. **Real models instead of procedural shapes.** Vendor `three/examples/jsm/loaders` (GLTF, RGBE/HDR, DRACO, KTX2; today
   `scripts/vendor-assets.mjs` copies only postprocessing, shaders, environments). Sources: BodyParts3D (CC BY-SA 2.1 JP) and
   Z-Anatomy (CC BY-SA 4.0) for anatomy; Smithsonian 3D (CC0 open access items); NASA 3D Resources; NIH 3D (licence per
   model). Sketchfab needs a token: download on the VPS. Convert to GLB, store under the scene's `assets/`, log the licence.
3. **PBR textures** (normal, roughness, AO) from ambientCG or Poly Haven (CC0): organic surfaces stop looking like plastic;
   texture lookups are cheap on a CPU renderer.
4. **One merged post-processing pass** with pmndrs `postprocessing` (bloom, vignette, noise, chromatic aberration, AgX tone
   mapping) and N8AO in its Performance preset at half resolution. Rough cost: grain/vignette/tone mapping ~5%, bloom
   15–30%, N8AO 30–60%, depth of field 30–80%.
5. **Grain and vignette in the FFmpeg assembly, not WebGL**, so 3D only pays for bloom and AO. Fake depth of field with a
   pre-blurred background plate.
6. **Cheap soft shadows:** one `PCFSoftShadowMap` light at 1024 or a baked contact-shadow texture; no VSM, no many-light
   shadows. Bake AO and lighting for static objects in Blender on the VPS.
7. **Organic motion from seeded noise as `f(t)`:** `simplex-noise` (MIT) with a seeded RNG (e.g. `mulberry32(42)`). Never
   step state from the previous frame: seeks jump and workers start mid-timeline.
8. **True 2.5D photo parallax:** depth map from Depth Anything V2 Small run offline (check its licence), then displace a
   subdivided plane in Three.js for a real camera dolly, filling the reveal with an inpainted or blurred plate. Better than
   the two-layer cutout in `video/chipgamble/parallax.sh`.
9. **Particles** (cells, blood, smoke) as InstancedMesh or Points positioned by seeded noise at `t`. Volumetric light as
   additive cone meshes with scrolled noise. GPU fluid sims are not seek-safe: use curl noise as a function of `t`, or
   pre-render the simulation to video.
10. **Clean diagrams:** GSAP + SVG (already in use). Lottie (`lottie-web`, MIT) works if driven by `goToAndStop(t*1000)`;
    a HyperFrames Lottie adapter is documented but untested here.

**Cost control (never by lowering quality):** pre-render each 3D insert once and composite it; native 4K only for hero
shots (others: 1080p render + Lanczos upscale, ~4× faster, unverified); `--quality draft` for review renders only;
`--workers 2–3` for WebGL (each worker is a Chrome with its own CPU renderer, within ~14 GB); limit transmission materials to
one or two hero objects (each re-renders the scene; ~30 min per 12 s); split long scenes into time-offset compositions and
render them in parallel sessions (§3), then `concat -c copy` with identical encoder settings.
**Vendored stack (Oct 2026)** and the reference scene `video/lib/realism-proof/` that uses all of it: three 0.181.2 with
every `examples/jsm` add-on (loaders: GLTF/Draco/KTX2/Meshopt, HDR/EXR; Lottie; utils), pmndrs `postprocessing` 6.39.5,
`n8ao` 2.0.1, `simplex-noise` 4.0.3, all pinned in `package.json`. `scripts/vendor-assets.mjs` copies them into a project
when its `index.html` mentions `vendor/three/`, `vendor/pp/` or `vendor/noise/`, plus any `vendor/library/<kind>/<file>`
from the shared library (§8.7). Import map: `three`, `three/addons/` and `three/examples/jsm/` → `./vendor/three/…`,
`postprocessing` → `./vendor/pp/postprocessing.js`, `n8ao` → `./vendor/pp/N8AO.js`, `simplex-noise` →
`./vendor/noise/simplex-noise.js`. Lessons from the proof scene:
- Async loads are safe: HyperFrames' Three adapter waits for `THREE.DefaultLoadingManager`, so HDRIs and models loaded with
  the default manager are in place before frame 0 is captured.
- Glossy surfaces show a 1k HDRI's pixels as blocks: keep roughness ≥ ~0.4 or use a 2k map for hero close-ups.
- Translucency via `opacity` + `depthWrite: false`, not `transmission` (which re-renders the scene per object).
- With pmndrs `postprocessing`, set `renderer.toneMapping = NoToneMapping` and tone-map in the effect pass (AgX); create the
  renderer with `antialias: false, stencil: false, depth: false` and the composer with `HalfFloatType`.
- Scenes read `window.BENCH` flags so `scripts/bench_render.py` can price each pass (results in §15).
- **Measured (2026-10-08, 1080p, 3 workers, pinned CLI):** full stack 51.8 s of render per output second; without N8AO
  26.6 (AO doubles the cost); without bloom 46.5 (bloom ~11%); bare scene 8.5. So: N8AO only on hero close-ups (bake or
  fake contact shadows elsewhere); bloom and HDRI are cheap enough to keep everywhere.
- `scripts/bench_render.py` and every render must use the repo's pinned CLI: `npx hyperframes` run outside the repo
  silently fetches the latest release (0.8.140 on 2026-10-08) instead of 0.8.103.
Three.js gotchas: module script with an importmap to `./vendor/three/`, GSAP timeline in a separate classic script;
`preserveDrawingBuffer: true`, `setPixelRatio(1)`, size from `root.dataset.width`; bloom makes the canvas opaque, so draw
the background inside the scene.
Sources: hyperframes.heygen.com (runtimes-and-3d, cli, performance), github.com/N8python/n8ao, api.polyhaven.com,
ambientcg.com, dbarchive.biosciencedbc.jp (BodyParts3D), z-anatomy.com, 3d.nih.gov, 3d-api.si.edu, nasa3d.arc.nasa.gov.

### 9.1 Scene library contract (`video/lib/<scene>/`)
Reusable, parameterised scenes that any documentary (and the unified engine, §22.1) can drop in. Every library scene:
- **One folder, one composition:** `video/lib/<scene>/index.html` (+ `assets/` for small scene-specific files) and a short
  `README.md`: what it shows, parameters, measured render cost, licence of every asset, a `preview.jpg` contact sheet.
- **Parameters, not edits:** `index.html` loads `params.js` first (`window.SCENE = {...}`): duration, texts, numbers,
  palette (genre tokens from §5.3), camera path, which highlight to show. All on-screen words come from `SCENE`, so the
  engine or a session re-uses the scene by writing a new `params.js`; the root `data-duration` must equal
  `SCENE.duration` (the engine rewrites both).
- **Deterministic:** everything is `f(t)` with seeded noise; async assets only through Three's default loading manager.
- **Honest labels:** a corner tag ("ILLUSTRATION", "ILLUSTRATIVE CURVE", "HYPOTHESIS") is on by default.
- **Measured:** reads `window.BENCH` flags for its expensive passes; README records `scripts/bench_render.py` numbers at
  1080p (and 4K for 3D hero scenes).
- **Checked:** lint and check pass; snapshots looked at; a 1080p sample rendered with the pinned CLI.
- New reusable assets (models, textures) go in `library/<kind>/` with a row for `library/manifest.csv` (sessions working
  in parallel write their rows to `video/lib/<scene>/library_rows.csv`; the coordinator merges them).
- No new npm/pip dependencies without the coordinator: propose them in the README.

### 9.2 Design from real photos first (owner, 2026-10-16)
*Why (owner):* "Before design anything observe the real photos first, accordingly you can make it realistic design."
The independent viewer review of the Kavach scenes found a generic "cab display" placeholder, a made-up screen layout,
signals that did not look Indian and a three-track Balasore layout when the real one has four. Before any scene that
draws real-world things, gather references (Commons categories via `list=categorymembers`, the files a Wikipedia article
uses via `prop=images`, PIB photos, the owner), keep them in the project's `assets/ref/`, contact-sheet them into
`qa/ref/`, and write `design-reference.md` (element → reference file → what to copy). Then draw from it: the real
screen layout and labels, the real livery and colours, the real signal heads and plates, the real track arrangement.
Commons: the search API rate-limits (429); category listings, `prop=images` and `Special:FilePath/<name>?width=960`
files with a descriptive User-Agent and 8–45 s gaps worked. Example: `projects/kavach-railway-reality/design-reference.md`.

### 9.3 Owner's CPU-only production guide (2026-10-16): what we use and why
The owner shared "Claude Code in Cloud Sessions: Master CPU-Only Production Playbook". Mapping:
- **FFmpeg virtual camera** (`zoompan`, `crop`, `overlay`, `vignette`): **use**. Documents, PIB pages and real photos
  get eased push-ins and pans in FFmpeg at assembly (cheap, real time); grain and vignette are added there too (§9).
- **Remotion**: not added. HyperFrames (pinned) is the same idea (Chromium + JS timeline → MP4 on CPU) and every
  scene, check and render tool here is built on it; a second engine would split the look and the checks.
- **Manim / Matplotlib / OpenCV**: not needed for the current films; braking curves, counters and charts are HyperFrames
  SVG scenes that share the film's look. Pillow + FFmpeg cover stills and contact sheets.
- **Client-side WebGL (send the owner an HTML file)**: not usable for a film, because the MP4 must contain the 3D.
  Three.js scenes render in the cloud on SwiftShader (≈ 27 s per output second without N8AO, §9), which is affordable.
- **No Blender Cycles, no local video diffusion, no heavy physics bakes**: already our rule.
- **yt-dlp clips**: used when YouTube answers from the container; never routed around blocks (CLAUDE.md).
- **Akash V4 takes under 1,500 characters**: the guide's limit for English Akash takes, against our 4,000–4,500 for Bunty.
  Apply to the next English script's voice blocks and confirm with the owner.

### 9.4 3D railway world: lessons from the Kavach A scenes (2026-10-16)
`video/kavach-railway-reality/_A_lib/kav3d.js` is a reusable Three.js railway world built from reference photos
(broad-gauge track on PSC sleepers, WAP-style loco, LHB coaches, Indian 4-aspect signal, OHE, station Kavach cabinet,
relay racks, RFID tag, lattice tower, X-ray loco parts). Each item below cost a build:
- **Bloom on SwiftShader:** pmndrs `BloomEffect` with `mipmapBlur: true` left dark halos around bright objects; Kawase
  (`mipmapBlur: false, kernelSize: 4`) does not. **ACES** tone mapping pushed saturated cyan bloom below zero (red/green
  channels clip to 0, a dark ring); use **AgX**. `VignetteEffect` showed a hard elliptical edge on smooth skies; use a
  smoothstep radial vignette in the grain pass instead.
- **DOM labels pinned to 3D points:** call `camera.updateMatrixWorld()` before `Vector3.project()`. Three refreshes the
  view matrix only at render time, and seeks jump, so labels otherwise use the previous frame's camera (off by ~150 px).
- **GSAP clears the CSS `translate` property** on elements it transforms. Centre a pinned chip with a static wrapper
  (fixed width, negative margin), never with `translate` or `xPercent` on the animated element.
- **HyperFrames waits on `window.THREE.DefaultLoadingManager`:** set `window.THREE` and bracket async setup (fonts for
  canvas textures, HDRI) with `itemStart`/`itemEnd`.
- **Indian signal lamp order is Y, G, Y, R from the top: red is the bottom lamp,** on the post, in cab-screen icons and in
  every schematic. Signals stand to the left of the line (left-hand running).
- **Physics on screen must add up:** a "next signal 40 m" readout at 100 km/h shows a train running the red; size the
  scene from the stopping distance first (A1: brake 470 m short at 108 km/h, 1.1 m/s²).
- **Native 4K of a WebGL scene (Kavach, 2026-10-16):** `make_native_4k.mjs` sets the root to 3840×2160, so a renderer
  sized from `data-width` draws a true 4K buffer: ~12 s a frame (3× the 1080p cost) and DOM pins placed at 4K coordinates
  inside the 2× zoom stage (wrong place). `video/kavach-railway-reality/_tools/render_4k.sh` keeps the WebGL buffer at
  1920×1080 in the copy, so the canvas is scaled 2× while text and SVG render at true 4K: ~3.8 s a frame with 2 workers
  (a 15 s 3D scene ≈ 20–38 min); 2D scenes run at ~0.5 s a frame. The whole 46-scene, 8:34 film took ~3.5 h on one VM.
  Raw scene MP4s come out at ~100 Mbit/s; the reel re-encode caps at 40 Mbit/s. The queue is resumable (`.done`
  markers): after a VM pause, start the same list again.
- Render cost: about 4 s per frame at 1080p, 3 workers (shadows + bloom + FXAA + grain), so a 15 s 3D scene takes ~30 min.

## 10. HyperFrames (pinned `hyperframes@0.8.103`)

Rules are in `CLAUDE.md`. Gotchas we hit, each cost at least one render:
- `<video data-start>` inside a div with `data-start` fails `check` (StaticGuard). Video shots use an untimed wrapper
  (`data-vs`/`data-vd`) whose visibility the timeline toggles.
- The renderer paints video frames over sibling overlays in the same wrapper. Burn labels into clips with ffmpeg `drawtext`,
  or put overlays in a later layer.
- Never add tweens at negative positions: per-part timer keys from other parts inflated a 45 s part to 2477 s. Clip
  keyframes to `[0, dur]` per part.
- `tl.call` doesn't run on render seeks: use stacked elements and `tl.set`. No `letterSpacing` tweens.
- An SVG filter on a perfectly vertical or horizontal line renders nothing.
- `@font-face` goes in each `index.html` with root-relative paths; canvas fonts need a fallback (`Inter, Arial, sans-serif`)
  or the first frame renders in a serif.
- A `data-*` field named `src` collides with the scene "source footnote": use `img`.
- Canvas animations draw from a proxy tween's `onUpdate` using local time only (seeded RNG, pre-rendered sprites).
  `snapshot` may show a canvas at t=0; verify in Playwright by seeking and sampling pixels
  (set `window.__timelines = {}` before load).
- WebGL reads the 4K size from the root `data-width`.
- Large `filter: blur()` glows and `backdrop-filter` dominate software-GL capture time: pre-render them to an image or video.
- Lint wants scenes as sub-compositions (`data-composition-src`).
- Speed on the cloud's software GPU: ~8 s of wall time per second of 2D, ~50 s per second of 3D; 3D with transmission
  materials ≈ 30 min per 12 s.

## 11. Sound

- **The VO leads.** (Charter levels supersede: BGM −24 to −26 dB under speech, −12 dB in pauses; see Part B intro.)
  BGM at −18 to −22 dB under the VO (bed at −15 dB with sidechain ducking lands ~20 dB under), ducked by
  the VO **and** live clip audio, rising only in pauses. Loop music with crossfades (`long_bed`), never an audible restart.
- **The video is not locked to the VO length.** EDL break types:
  - **Diegetic cut:** when authentic footage appears, the VO stops and the asset's own sound plays for 2–6 s (a conch, a
    press statement, a monitor alarm, machinery), then the VO resumes after the peak.
  - **`LIVE`:** real speech (press conference, news report) plays with its own audio for as long as it needs, picture
    untouched, credited in a lower-third; never talk over real dialogue. Keep third-party excerpts short; never the whole clip.
  - **`VO_PAUSE`:** 2–4 s of real ambience. `vo_skip` drops a duplicated VO stretch after a break.
  Real archival audio (e.g. a CC BY clip on archive.org) beats an empty LIVE row.
- **Loudness:** two-pass **linear** normalisation to −14 LUFS integrated, −1 dBTP (one gain + limiter). *Why:* single-pass
  `loudnorm` pumped silent pauses up to narration level.
- `scripts/make_bed.py` synthesises a royalty-free bed (drones, pads, heartbeat, bowls); `scripts/final_mix.sh` mixes.

## 12. Facts, honesty and rights

- **Facts only from collected sources**, checked on the web before they go on screen. Where reports disagree (15 vs 16
  minutes), say "as reported" and note the other figure in the description. Present claims as claims; on health topics
  include the mainstream scientific view and at least one real skeptic beat.
- **Lighter fact-check (owner, 2026-10-11).** *Why:* the full independent pass on Minimum Amount Due re-searched all ~95
  claims from zero at `max` effort (plus a captcha-gated RBI PDF and a day-by-day rebuild of the math) and used most of
  the 5-hour usage window; nearly every rule and bank term it checked was already sourced. Now:
  1. **The writer logs sources while researching:** a draft `claims.csv` with every claim's exact URL and verbatim quote,
     status `confirmed` only when the writer read the primary page (RBI/regulator text, the bank's own page, the court
     report, the data release) or two independent reports. Anything else is marked `unverified` (weak).
  2. **Strong rows are not re-researched.** The checker (fresh subagent, `max` effort) opens only the cited page to
     confirm the quote and the number match, and spends real searching only on weak rows, all numbers and dates, our own
     calculations (re-run the tool, check the method against the cited source) and on-screen tags.
  3. **After a script edit, re-check only the changed lines.**
  The gate (`scripts/claims_check.py`) and the rule "facts only from sources" are unchanged.
- **Label unmeasured claims** (heart rate, "40–50% less oxygen") as narration claims or illustrations. Quotes verbatim only.
- **Safety lines** (e.g. "don't try breath-holding without training") in the description and on the end card.
- **Every asset logged** with its licence in `media_manifest.csv` (ID, URL, owner, licence, date, EDL slots);
  `projects/prahlad-jani-drdo/tools/credits.py` and `video/chipgamble/credits.py` turn manifests into description credits.
- **Third-party news/event footage:** short excerpts that we comment on, credited on screen; never the whole clip. The owner
  cleared event clips, photos, film names and trailer footage for breath-hold; ask again for each new subject. Warn about
  Content ID risk (fan reels carry added music).
- **AI generation only where no real asset exists**; AI shots never depict a real, identifiable person or pose as evidence;
  labelled "ILLUSTRATION" and logged in `credits.md`.
- Paid archives (AP Archive, Reuters) for anything long: ask the owner first, with the cost.

## 13. Render and deliver

- HyperFrames: `npx hyperframes lint` → `check` → `snapshot` → look at the PNGs → fix → render with `--workers 4`.
- **4K:** for a new film, render natively (`scripts/make_native_4k.mjs` + `render --workers 4`; `video/prahlad/render_4k.sh`).
  For an already-approved 1080p cut, upscale with ffmpeg (`scale=3840:2160:flags=lanczos` + mild `unsharp`, ≈0.23× real
  time). Never `--resolution 4k` (4× slower, §21).
- FFmpeg assembly at 4K: oversample Ken Burns 1.25× (2× is fine at 1080p); dip to black at block changes; lightly sharpen
  upscaled 288p archive footage; **bitrate-cap every encode** (temporal grain made a 3.4 GB 1080p file).
- Footage prep: vertical reels → crop the clean band above burned-in captions, Lanczos-upscale, check every crop on a contact
  sheet (one cut off the face). Tall portraits: pre-crop a 16:9 band at the top (`object-fit: cover` gave a headless torso).
  Letterboxed trailers: `cropdetect`, then scale. Keep audio only on LIVE/diegetic clips (`-an` for the rest). Pick in-points
  from 1 fps timecoded contact sheets.
- **Long jobs:** a backgrounded Bash command dies at its time limit (30 min default). Start renders with `nohup … &` and
  watch with Monitor. `assemble.py` caches every shot (`out/tmp*/NNN.key`), so re-runs only re-render changed rows; the key
  includes the script's mtime, so editing `assemble.py` invalidates the whole cache. One render at a time per session (~14 GB memory cgroup); kill stray loops first. If ffmpeg dies with
  an empty error, check `memory.failcnt`/`dmesg` for OOM.
- **Shell traps:** never `pkill -f <pattern>` in a command line that contains the pattern (it kills its own shell; use
  `[x]yz`). Never name a shell function after a command it calls (`cut(){ … | cut; }` forked ~1,500 shells and OOM-killed
  renders).
- **Deliver:** `scripts/upload_gdrive.sh --sub <Channel>/<slug>` to the owner's Drive `Creator` folder (§1); upload the master and
  a 720p copy. `scripts/upload_gofile.sh` only as a fallback while `GDRIVE_RCLONE_TOKEN` is missing. Commit sources, EDL, registry, transcripts, SRT and description; large
  footage stays out of git (`assets/video/*`, `assets/raw/`, `projects/*/assets/`, renders).

### 13a. YouTube package and close-out after every final video (owner, 2026-10-17)

*Why:* the owner uploads from the YouTube Studio app on a phone. A ready thumbnail and text they can copy with one tap
(the copy button on a fenced code block in the GitHub and Claude apps) remove all typing and guesswork; merging and
closing the session keeps `main` complete and stops idle sessions using the shared limit.

1. **Thumbnail (Be Practical with Kishore theme).** 1280×720 JPG (plus a 2× PNG), built as HTML in
   `projects/<slug>/youtube/thumb/` and shot with Playwright (`shoot.js`; copy `projects/minimum-due/youtube/thumb/`).
   Theme from `assets/brand/`: deep navy radial background (`#0b1530` → `#070d1f`), the banner's gold (`#ffd34d`) and
   blue (`#4a6fa5`) circuit lines with dot ends, Inter 800 in white with the key number or word in gold, one red
   (`#e5383b`) pill for the shock line, a real photo, footage frame or the film's own simulation (labelled as in the
   film), and the square BE PRACTICAL logo in a corner. 2–4 large words and one concrete number or object, and every
   promise is delivered literally in the film (§4a). No AI images of real people. Make an A and a B variant for Test &
   Compare; look at both at phone size before delivering.
2. **Title in a click-to-copy block.** A plain fenced code block holding exactly one line, ending
   `| Be Practical With Kishore`, ≤ 100 characters in all (YouTube's limit), no `!`, the hook first and search words
   after it. Offer one or two alternatives, each in its own block.
3. **Description in a click-to-copy block: simple description and timestamps, nothing else** (owner, 2026-10-17:
   "always give the simple description and timestamps, no references, no sources, nothing"). 2–4 short lines in everyday
   words (§4a-2) on what the video shows, then `CHAPTERS` with timestamps starting at `0:00` (at least 3, each ≥ 10 s
   apart, so YouTube makes chapters). No sources, references, credits, disclaimers, hashtags or links in the block.
   Take the timestamps from the exact file the owner uploads (a scenes-only reel and the full film have different
   times: Kavach, 2026-10-17). *Why:* the owner pastes it on a phone and wants it short; sources stay in `claims.csv`.
4. Save as `projects/<slug>/youtube/description.md` (title and description blocks) next to the thumbnails, send the
   thumbnail JPGs and `description.md` with `SendUserFile`, and paste the title and description blocks in the final
   chat reply as well.
5. **Close-out:** commit, push the session branch, open a PR to `main`, merge it (merge commit), confirm the merge,
   tell the owner which branch to delete, then archive the session (`archive_session`).

## 14. Pre-render review (every cut, before the final render)

Contact-sheet the cut (`scripts/contact_sheet.py CUT.mp4 --out runs/<slug>/qa --every 2`: 3×3 timecoded tiles, 1536 px)
and go shot by shot; write `review.md` (issue → shot IDs → fix). In a session, read the sheets yourself at `high` effort or
above; in Actions, `python -m pipeline.review_cut` sends sheets + EDL to Opus at `max` and writes `review.md`/`review.json`
(exit 1 on blockers). Fact-check gate first: `scripts/claims_check.py projects/<slug>/claims.csv`. Skill: `/review-cut`.
**Independent viewer review (owner, 2026-10-16).** *Why:* "even if you review yourself you mostly consider CLAUDE.md and
the playbook; an independent session should review independently, as a general audience." After our own review, open
**one** cloud session **without the repo attached** (`create_session` with no `source_url`, so no CLAUDE.md, playbook or
skills load). Give it only what a viewer gets: a Drive download link (`https://drive.google.com/uc?export=download&id=<id>`)
to the cut, with the VO laid in (build the program VO from `align/program.json`), and the narration text with reel
timecodes. Ask for a blunt verdict, a per-scene score table (what's wrong, frame time, fix) and the top 10 fixes. It
judges clarity, pace, phone legibility, slide-look and what looks wrong; we check its claims against the sources and
rules before changing anything. Read its answer with `list_events`, then archive the session.
- [ ] ≥ 85% moving footage or animation; no unmoving still or flat frame over 1.5 s; no shot over 4 s except LIVE clips and
      HyperFrames scenes.
- [ ] Every shot matches the exact words over it; the VO is silent under every diegetic or LIVE moment.
- [ ] English films (§4a-4): the open loop's promised minute matches the cut; a visual reset every 3.5–5 s; no stock
  of anonymous office workers typing; acronyms in the VO were said correctly (listen, don't assume).
- [ ] Face and name on screen within 20 s; name lower-third returns when the VO says the name.
- [ ] Every frame's on-screen data agrees with the VO (numbers, monitors, headlines, dates).
- [ ] Stand-ins labelled "ILLUSTRATIVE FOOTAGE"; authentic footage carries its source credit.
- [ ] No stock clip more than twice. Science beats animated and honestly labelled.
- [ ] Logo sting when the channel is named, logo bug elsewhere, end card last.
- [ ] No near-black or dead frames; block changes dip to black; the music bed never restarts audibly.
- [ ] Claims stay claims; a real skeptic or mainstream-science beat on health topics.
- [ ] About −14 LUFS; subtitles rebuilt after any timing change.
- [ ] Thumbnail promise shown by 0:30; chapters in the description; timestamped sources and citation tags on claims.
- [ ] Compliance gates (§4a): synthetic disclosure, health context, SEBI education-only lane, PCI suicide norms, ban list.

**Per-shot review, then whole-film review (owner, 2026-10-11).** *Why:* a 6-second contact sheet of the whole film hid
problems that a shot-by-shot pass caught at once (unreadable proofs, a pop-up on a source page, a foreign supermarket).
After every assembly, run the project's `review_shots.py` (3 frames per shot beside the VO words spoken over it, 8 shots
per sheet), judge every shot against this checklist, write the findings and the lesson behind each one into `review.md`,
fix, re-assemble, and review again until a round finds nothing worth fixing. Then judge the film as a whole (pacing,
board vs real-footage balance, loudness) and refine once more.
- [ ] **Proofs readable on a phone:** the highlighted words fill ≥ 1/3 of the frame width at the end of the push; shoot
      source pages at 2× (`deviceScaleFactor: 2`) so a 2–2.5× zoom stays sharp; remove fixed/sticky layers (pop-ups,
      "get notified" boxes, cookie bars) and ad slots before the screenshot.
- [ ] **No board holds longer than ~16 s without a cut:** cut away at the duster moments (the board is blank there) to
      real footage or a proof of the same idea; never leave an empty board on screen for more than ~1 s.
- [ ] **Indian faces, places and money** in every stand-in (see §4a-3); a European street, shop or face is a reshoot.

### 4a-4. Series continuity for connected films (owner, 2026-10-15)
When a film continues an earlier one (Health Claim Trap → Insurance Ombudsman), it plays as the next episode of one
story, never a fresh start. *Why:* the owner: "when we have connected topics we should not confuse the audience"; a
viewer who saw episode 1 notices a changed bill, and a newcomer needs ten seconds of where we are.
1. **Read the earlier film first:** its `script.full.tsv` (what was actually recorded), `youtube/description.md` and EDL.
2. **Same story world:** the same family, amounts and documents (the ₹4,50,000 bill, the CASHLESS DENIED stamp), carried
   on, not reset. Worked examples derive from the earlier numbers.
3. **Never contradict earlier advice.** If episode 1 said "step 3: Bima Bharosa", episode 2 explains why step 3 alone is
   not the end; it does not call it a mistake. Facts both films state use the same source and wording (claims rows reused).
4. **Every episode stands alone (owner, 2026-10-15: "even with the second video they need to understand everything;
   no need to watch" the first).** Open on the situation itself ("Imagine you are standing at …"), then a 15–25 s recap
   that teaches what the viewer needs from the earlier film; the earlier film is a pointer ("we told this story in our
   last video"), never a requirement. Gloss every term on first use as if new (cashless, Bima Bharosa, GRO); no "as we
   saw last time", "remember step four" or "rule three from our first video". No "nobody tells you" about something we
   already told them.
4b. **Glimpses:** 2–4 s shots from the earlier film's final cut in the recap (labelled `FROM EPISODE 1`), so returning
   viewers recognise the story and new ones see it.
5. **Recurring motifs** (the four-step staircase, the same SIMULATION letter design) tie the episodes together; each
   film still gets its own art direction for its new parts (§4a).
6. **Callbacks without dependence:** link back through the recap ("step two of our plan") and tease the next episode in
   its own words (consumables → episode 3). Title and thumbnail follow the series hook ("Step 4").

## 15. Lessons log

**Insurance Ombudsman (English, 2026-10-15).** (1) A shot cache keyed on "file exists" was poisoned by a render cut
off when the session was resumed: one shot file had no moov atom, and the concat demuxer froze the whole film from
5:13 to the end on the last good frame. Fix in `projects/insurance-ombudsman/build/assemble.py`: render each shot to
`tmp_<name>` and rename only when complete; after any interrupted run, ffprobe every cached shot and delete failures.
*Why:* a frozen half-film passes every timing check and is only caught by looking at the sheets. (2) drawtext silently
drops a label containing `%` (text expansion); use `expansion=none` instead of escaping. (3) Never `pkill -f` in the
same command that later starts the process the pattern matches: it killed its own shell twice. (4) Glimpses from an
earlier film already carry its lower thirds; overlaying ours doubled them, so they get only a top-left
`FROM EPISODE 1` tag. (5) Parallel scene sessions (A/B/C, PLAYBOOK §3) delivered 43 frame-exact clips in about
75 minutes while the coordinator sourced, cut and mixed; specs generated from the real VO timing (`scenes.md`) meant
every clip dropped in at its window with no retiming.

**Insurance Ombudsman v3, independent review + 4K (2026-10-16).** A fresh session reviewed v2 shot by shot
(`build/review_shots.py`) and found what the authors' own pass missed: (1) a stock clip on screen three times (F08),
because `split_long` and reuses across chapters hid it; count clip *sources*, not shot rows, before each render.
(2) An edit that cuts away from a scene can hide the scene's own beat: the coordinator's GRO-list still covered the
first 8 s of A6 O030, so the insurer page that A6 built for "every insurer has to show its GRO details" never
appeared. When a still is laid over a scene window, check what the scene shows under it. (3) "No blank paper" includes
screens: an email compose window or a new browser tab held for 5-10 s reads as a white slide; fill it with the
context the VO implies (the quoted settlement email, recent visits). (4) Show the family's own city on a directory
page (Hyderabad, not the default first tab). (5) A label that names a number must not stay up while a counter rolls
past it. (6) Canva templates can be re-exported at 4K through the Canva connector (`export-design`, `mp4`,
`horizontal_4k`); keep the crop/composite steps in a script (`tools/make_canva.py`) so a rebuild never depends on
files that lived only in a dead session. (7) A detached render script still needs `HYPERFRAMES_RENDER_DETACHED=1`
(also in this log, below); `setsid nohup` alone was cancelled within seconds.


**Health Claim Rejection Trap (English, 2026-10-14).** (1) The owner's handoffs (a full brief, a "fixes" rewrite, then a
visual-engine spec) each carried unsourced numbers ("80% rejected", "60 days", "₹500–800 rider", "₹90,000 cut",
"17 centres", "lawyers banned"). The two-pass fact-check (draft claims → independent max-effort subagent → re-check of
changed lines only) caught them all before recording. *Why:* the VO is locked once recorded; fixing after costs a re-take.
(2) The free stock libraries have no Indian hospital billing counter, TPA desk or night corridor; the first preview leaned
on generic foreign clinic stock and the owner rejected it as filler. v2 replaced every stock clip with programmatic
HyperFrames scenes (`projects/health-claim-trap/build/make_engines.py`: isometric SVG cutaway, document rig with a 3D tilt
and scan line, bill slicer, moratorium timeline, discharge stopwatch, one 129 s war-room scene with a panned 4800×2700
world). *Why:* for explainers about rules and money, a moving diagram carries more information than stock, and it
renders at ~3.5 s per output second on the cloud VM (2D SVG/CSS, no WebGL). (3) Never draw India's outline from
memory or an unofficial source (map-border law); show city nodes without the border. (4) In SVG built from Python,
`class_` keyword attributes must strip the trailing underscore (a `class-` attribute rendered every face black).
(5) A `pgrep -f "<pattern>"` wait loop launched with `bash -c "... <pattern> ..."` matches itself and never ends: wait on
a PID or a `.done` file instead (CLAUDE.md trap; it cost 10 minutes of idle renders).

**Jet Engine Paradox (English, script phase, 2026-10-13).** The owner's brief came as a finished script from another
AI tool. Of its ~40 facts, about 20 were wrong, out of date or unsourced. Some examples: "only four nations" (the brief's own Act 4
names China), superalloys melting at 1,455 °C (that is pure nickel), "an elephant hanging from a soup spoon", AMCA engine
110 kN (it is 120), jets that "cannot fly" (they fly; delivery is what's missing), and NavIC as a working system (only 3 of
4 satellites). *Why it matters:* treat any pasted script as a draft brief. Research every line before the VO exists.
Prefer the maker's own sourced comparison (Rolls-Royce: gas 200 °C above the alloy's melting point, a London bus per
blade) over invented ones. Keep `brief/changes-from-brief.md` so the owner sees each change and its reason. Tavily
rate-limits parallel calls (429): call it one at a time and fall back to WebSearch. The Commons search API timed out in
a loop of 8 queries, so fetch exact `--titles` instead.

**Jet Engine Paradox, globe and data session D (2026-10-14, 15 scenes on `_d_lib/`: one land-only globe, one
instrument kit).** Each of these cost a debugging round:
- **pmndrs post chain: three ways to get dark halos around bright lines.** (1) `BloomEffect`'s default SCREEN blend goes
  negative on HDR (>1) pixels: use `blendFunction: BlendFunction.ADD`. (2) `FXAAEffect` merged into the same
  `EffectPass` after bloom re-samples the un-bloomed input: give FXAA (+ grain) its own pass. (3) AgX's outset matrix
  darkened a cool background around saturated amber bloom: the data scenes use `ToneMappingMode.NEUTRAL`.
- **Software GL breaks `fract(sin(x) * 43758.5)` hashes** for large x (streaks and blocks in noise): use the sin-free
  `fract(p * vec3(.1031, .1030, .0973))` hash. Screen-space derivative bump (`dFdx` of noise) made blocky patches:
  skip it on large, smooth surfaces.
- **A globe without borders:** bake Natural Earth *land* into a signed distance field (`library/geo/land_sdf_4k.png`,
  `bake_land.mjs`); the shader draws fill, a crisp anti-aliased coast and region tints from it at any zoom. Highlight a
  country with its coast and a soft tint, never an outline (a land border is a political border).
- **Canvas instruments in the 3D stage:** draw the dial/bars on a 1.5× canvas, show it as a plane (premultiplied alpha
  or edges go dark) with a second additive "glow" canvas into bloom; DOM chips stay crisp on top. Inter has no "→":
  inline SVG arrow. `.jd-chip` must not uppercase (`kN`).

**Jet Engine Paradox, 3D scene session A (2026-10-13, 8 Three.js scenes on one shared model set `_libA/jepA.js`).**
Each of these cost a re-render or a wrong look:
- **`setsid nohup` alone was not enough.** hyperframes 0.8.103 records every ancestor process at start and aborts
  (`render_cancelled_parent_exited`) when any of them exits, even after `setsid`. Export `HYPERFRAMES_RENDER_DETACHED=1`
  for detached renders (`video/jet-engine-paradox/_libA/render.sh`).
- **`material.envMapIntensity` does nothing with `scene.environment`** (three r181 uses `scene.environmentIntensity`).
  The scenes looked flat and cream-coloured until the scene-level value was set.
- **White blobs that bloom were NaN/inf pixels**, not reflections. Clamp the shader output and zero NaNs
  (`isnan`) before the HalfFloat composer.
- **Software-GL cost (measured, 1080p, 3 workers, 1 s slice):** 4× MSAA in the composer 2.4× slower (use `FXAAEffect`);
  seven translucent motion-blur copies of a 48-blade ring 2.5× slower (use 4, on the coarse ring LOD only); clearcoat
  +16% (invisible at roughness 0.4); bloom + heat shimmer together ~20%. Final stack ≈ 2 s per frame per worker.
- **Heat as a bare emissive turns metal into yellow plastic.** Glow only where the temperature field is high (leading
  edge, tip) with a sharp ramp, and keep the metal reflections visible.
- **Thermal view reads instantly when the background is the hot gas** (yellow/white in the ironbow ramp) and the cooled
  blade sits darker (red/magenta) in front of it. Cooling-film cyan only right behind the holes, never as a wash.
- **Inter's subsets have no `≈` (U+2248):** draw it as a small inline SVG in the label.

**Minimum Amount Due (English, 8:05, 2026-10-11, v1 → v2).** The per-shot review of v1 found:
- **Proofs unreadable:** 1080p screenshots at a 1.1–1.8× zoom left the highlighted line about 10 px tall on a phone.
  Fix: re-shoot at 2×, establish wide for about 2 s, push in to 1.6–2.5× on the saved highlight box, then pan along the row.
- **Pop-ups and ads on source pages:** remove every fixed or sticky element before the screenshot.
- **Foreign stock read as foreign:** a TABAK supermarket, a European teen and a European ATM queue. Pixabay searches for
  "kirana", "UPI" and "Indian man phone" returned mostly European faces, cartoons and dollar animations. Wikimedia
  Commons gave real Indian places: an HDFC branch in Hyderabad with Telugu signage, an HDFC ATM with an auto outside.
  Search Commons by brand plus city.
- **Boards held 20–42 s:** cut away at the duster moments to a relevant real clip or proof, and come back when the next
  line starts.
- **Weak hook picture:** "the full maths behind that small number" now shows flash-forwards of the maths boards instead of
  generic shop clips.
- **Loudness −14.8 LUFS:** `loudnorm linear=true` undershoots when the true peak would clip. Measure, apply the exact gain,
  then a −1.5 dBFS limiter.
- **Final mux crawled at 0.3× real time:** it rescaled the 4096 px logo PNG on every frame. Pre-scale overlays once.

**Minimum Amount Due, refinement Phase 1 (2026-10-12, owner's brief).** About half the runtime was whiteboard, which
read as repetitive. The fix was money mechanics as HyperFrames animation on the reusable kit `video/lib/fin`:
- the phone payment with the remaining balance kept on screen;
- one continuous timeline instead of a new board per rule;
- a payment split with linked counters on the checked series.

Rules learned:
- **Numbers and cues are generated, never typed.** `build/scene_data.py` writes `data.js` from the calculation tool and
  the VO alignment.
- **Keep the bank's own example and our illustration visually separate,** with case labels.
- **Show interest as accrual, then posting.** Never as a free-running counter.
- **Inter's latin subset has no ₹ glyph.** Load latin-ext with a `unicode-range`.
- **`ffmpeg -ss` before a still image writes nothing and still exits 0.** Check that the output exists.
- **A second GSAP `fromTo` on the same element renders its start state at build time.** Pass `immediateRender: false`.
- **Text swaps use stacked elements.** Not `tl.set` on `textContent`.
- **When an edit replaces a window, a shot that runs past the window resumes at its end.** Don't drop it.
- **Keep scene corners clear of the logo bug** that the final mux adds at the top right.

**Minimum Amount Due, 4K master (2026-10-12).**
- **Native 4K boards:** `build/render_4k.sh` copies each scene with `make_native_4k.mjs` and sets the board pages'
  pixel-sized `#root` to 100%. Without that, the zoom:2 stage is cropped to a quarter.
- **Speed:** about 5 frames per second at 4K on 4 vCPU. 16 animations (about 6.5 minutes) took about 45 minutes.
- **Detach renders with `setsid`:** a plain `nohup … &` render was cancelled ("parent exited") when the tool call
  ended.
- **4K assembly:** stills are oversampled 2× rather than 4× (4× means 15K-pixel frames), intermediates are capped at
  30 Mbps and the master at 20 Mbps.

**Breath-hold (Vidyut Jammwal, Telugu, 7:17, v1→v5).** v1 was all text cards on gradients and was rejected as "a boring
PowerPoint". What fixed it: full-screen real media, cuts every ~3 s, real event reels (Instagram via yt-dlp), agency photo
galleries (6000 px), the official trailer, canvas science animations, short "watch this" clips with their own sound.
About a third of search results were wrong (Kathakali for Kalaripayattu, tulips for "eyes", a bomb-blast photo), hence the
contact-sheet rule.

**Prahlad Jani & DRDO (Telugu, 6:30, v1→v5).** Filled gaps with NASA lab B-roll, NASA ISS footage, Wellcome engravings
(tagged), Wellcome photos of Henry Tanner's 1880 fast, Coverr hospital footage. Couldn't source here: 2010 news footage and
press conference (paid archives), DRDO imagery, free photos of the subject (needs the VPS or a licence). Dailymotion search
found the 2010 ITN and Al Jazeera reports. A real 16 s CC BY clip of James Randi (archive.org, May 2010) became the skeptic
LIVE beat. v4 review produced the standing notes in §5.5. v5: logo sting and end card, HyperFrames timeline, vitals,
dehydration chart, metabolism dial, Three.js kidney, bladder (labelled hypothesis) and autophagy scenes, ILLUSTRATIVE labels,
stock repeats capped, face and name at 0:18, native 4K master (full 4K film ≈ 45 min).

**The $10 Billion Chip Gamble (English, 10:49).** Four HyperFrames parts timed word by word to the VO. Government photos and
PDFs from ism.gov.in; Commons films cut with `cuts.txt`. The phrase-keyed engine made cuts land on words without manual
timing; real documents with highlighter swipes carried the policy beats.

**Foundation work (Oct 2026).** Realism stack vendored and proven (`video/lib/realism-proof`); measured pass costs (§9);
contact-sheet labels verified within one frame; a YouTube download worked from the cloud once (blocks are intermittent);
a temp-dir `npx` pulled an unpinned HyperFrames, hence the pinned-CLI rule.

**Pixel 11 consensus review (v1→v2).** Review found: opinion counts presented as evidence, manufacturer figures shown as
measurements, bare counts without denominators, paused zeros on count-ups, different tests on one scale, quote cards
competing with captions, visual sameness. Fixes became rules in §16.

**Fire and Ice (Tummo / Wim Hof, Telugu, 5:15 preview, Oct 2026).** One session, ~4 h wall clock (fact-check at max effort
took 90 min in a subagent while sourcing, scenes and assembly ran). Lessons:
- **Fact-check the script before the VO is recorded.** The VO arrived recorded; the check then found 17 wrong lines
  (wrong year, place, person, an invented "research paper" quote, records, a mechanism). Without a re-record the only
  honest options are cutting lines (`projects/fire-and-ice/tools/vomap.py`: cuts at line-slot boundaries, optional
  silence inserted for an on-screen beat; EDL and SRT follow the map) and labelling the screen. *Why:* a re-record costs
  minutes; a wrong claim on a public channel costs trust.
- **Reusable thermal-camera figure** (`video/fireice/_shared/body.js`): body parts drawn as temperatures into a
  low-res canvas field, blurred, palette-mapped (ironbow) and masked by a soft silhouette; one master clock tween
  (`FX.clock`) redraws every frame from `t` alone. Looks like a real thermogram; renders at ~5 s per output second
  (1080p, 4 workers). A flat-coloured SVG stick figure looked like a pictogram; drop that approach.
- **Dailymotion has full broadcaster documentaries** (VICE "The Superhuman World of the Iceman", DW Euromaxx) with real
  event footage (the Radboud endotoxin test), but only at 288p: usable as credited archive with `hqdn3d` + `unsharp`.
- **Verify every third-party in-point with an exact `-ss` frame grab** before render: a 12 s overview sheet put a talk
  show (burned subtitles) where it showed a snowy gorge. In shell loops run ffmpeg with `-nostdin` or it eats the list.
- **Maps for an Indian audience: land only, no political borders.** Natural Earth draws de facto borders in Kashmir;
  `video/fireice/benson_map/mkmap.mjs` uses `land-110m`.
- **Telugu sensitivity:** "చండాలి" (Sanskrit caṇḍālī, a Tummo name) is heard as a caste insult; show the Sanskrit term
  with a label and ask the owner.
- Commons originals 429 under load; standard thumb widths (1920) with long back-off worked. Openverse audio `url`s are
  full-length previews (one "ambience" was a 53-min file): check `duration` before downloading.
- Cut review caught: near-black title beats (snow/embers on black), a black frame from a source fade-in, cover-cropped
  people in 4:3 photos (pre-crop a 16:9 band), a mitochondria scene reused as a missing-photo fallback 20 s after itself.
- **English (Akash) takes run ~10% faster than `estimate_vo.py`** (fitted on Telugu Bunty): jet-engine-paradox's two
  aligned blocks were 544 s real vs 605 s estimated (0.90×). Multiply English estimates by ~0.9 when planning length and
  the open-loop minute, until the estimator gets an English fit (2026-10-15).
- **Owner's handoff briefs can carry unverified "facts"** (Kavach: "one tag every km", "40 m towers every 2–3 km",
  "100% saved", "Kavach would NOT have prevented Balasore"): the owner's own audit files rejected them. Check every brief
  line against the audits/sources first and list each change with its reason in `brief/changes-from-brief.md`.
- **Five scene sessions + two sourcing agents + the coordinator hit the account's five-hour usage limit ~10 minutes
  after launch** (Kavach, 2026-10-15): every session and agent stopped with "session limit" and had to be resumed by
  message after the reset. All sessions share one usage limit, so parallelism spends it faster; launch 3 sessions at a
  time, tell each to commit and push after every finished scene, and resume with `send_message` after a reset.
- **Indian Railways servers (rdso.indianrailways.gov.in, indianrailways.gov.in, sr.indianrailways.gov.in) reset
  connections from the cloud container**, archive copies too. Use PIB, Sansad, CRS (crs.gov.in works) and IRIMEE copies,
  or ask the owner to open a PDF on the phone; keep a verified fallback line ready (2026-10-15).

---

# Part C: Phone consensus review pipeline

## 16. Product and spec

**Premise:** "We analysed what 15+ trusted reviewers said about this phone, so you don't have to." A 4K video whose length the topic sets (owner, 2026-10-09).
What makes it different: a consensus scorecard per category (display, camera, battery, performance, software, build, value);
a "Where reviewers disagree" segment; "Problems reported by multiple reviewers"; who should buy, who should skip, better
alternatives at the same price; every claim traceable to reviewer + video/article + timestamp.

| Item | Spec |
|---|---|
| Resolution | 3840×2160, with a 1080p fast-preview mode |
| Frame rate | 30 fps (60 via config) |
| Codec | H.264 High, bitrate capped for YouTube 4K and the 2 GiB Release limit (§21) |
| Shorts | Optional 1080×1920 "verdict in 60 seconds" from the same data |
| Look | Dark, premium, cinematic: depth, light sweeps, parallax over official product images, kinetic type, animated charts |

**Hard rules (and why):** no AI images or video of the phone, no AI camera samples, no fake hands-on (misleads buyers and
breaks YouTube's synthetic-content rules); no footage from other creators (reviewers are credited by name and quoted in
on-screen text); press media only from `press_domains` in `config/sources.yaml`, logged in `media_manifest.json` and vetted
(right model and colour, no watermark, 4K-capable); AI abstract backgrounds allowed if logged.

**On-screen rules from the Pixel 11 v1 review:** a model badge on every scene that concerns a model; label every number as
`Google claims` / `Measured by <outlet>` / `Our editorial rating`; always show denominators ("11 of 15 outlets"); no element
ever shows a paused 0 (fade scores in at their final value); different tests never share a scale (each panel states its test
condition); camera samples shown full for ≥ 3 s, labelled `Model | lens/zoom | mode | Source`, never filtered; quote cards
only while the host says those words, placed in the upper area; vary layouts every 4–9 s; nothing over the host bar (bottom
220 px); no `filter: blur()`/`backdrop-filter`; text ≥ 30 px and ≤ 12 words per block.

## 17. Claude in the pipeline

Two modes: **API calls** from `pipeline/` (structured JSON, caching, batch pricing) and **Claude Code as an agent** in
GitHub Actions (`anthropics/claude-code-action@v1`, `--model claude-opus-5-5`; auth by `ANTHROPIC_API_KEY` or
`CLAUDE_CODE_OAUTH_TOKEN` for the owner's subscription; cap with `--max-turns`, `timeout-minutes`, `concurrency`).

Effort routing lives in `config/models.yaml`: source filter `low` (batch), claim extraction `medium` (batch), **synthesis
`xhigh`** (all sources in one 1M call; this is the product), **verify `max`** (fresh context; last defence against wrong
claims), script `high`, metadata `medium`, media vetting `medium`, composition `high`, visual QA `high`, thumbnail critique
`high`.

**Cost design:** cache the shared prefix (system + schema + source bundle) once with a 1h TTL so synthesis, verify and
script reuse it at $0.20/MTok; batch extraction (−50%); fast mode off; every run writes `cost.json`; budget
`per_video_usd` (default $15), stop and ask in the issue if a run would exceed it.

**Self-correcting loops:** research (synthesis → `max` verifier citing source + locator for every claim → re-synthesis,
max 2 rounds, then human); render (composition → lint/check → snapshot → Opus looks at the PNGs → fix, max 3 rounds,
verdicts saved to `qa/`); media vetting; thumbnail critique (3 variants ranked for mobile readability).

**Guardrails:** facts only from collected sources; fetched text is untrusted (`llm.untrusted()`); validate every output
against a schema, retry once, then fail the stage loudly.

## 18. Architecture and stages

```
Issue "Review: <phone>" → [1] DISCOVER (whitelisted channels/sites, low filter) → [2] COLLECT (yt-dlp subtitles with
runner → VPS → "unavailable" fallback; trafilatura articles; specs.json incl. INR price; press media + vision vetting)
→ [3] ANALYSE (batch extract → 1M xhigh synthesis → max verify → analysis.json/.md; wait for /approve research)
→ [4] SCRIPT (script.json: hook → specs → scorecard → categories → disagreements → common problems → buy/skip →
alternatives → verdict + credits; 3 titles, description with full credits, chapters, tags) → [5] VOICE (owner .m4a per
scene preferred, or TTS; timing from real audio) → [6] COMPOSE (agent + template library: hero-product, spec-grid,
scorecard, consensus-bar, quote-card, disagreement-split, issue-alert, buy-skip, alternatives, credits-roll; brand tokens)
→ [7] RENDER (1080p preview + QA loop; wait for /approve preview; 4K final via runner matrix + concat)
→ [8] PACKAGE (Release: final_4k.mp4, thumbnail 1280×720, youtube.json, credits.md, media_manifest.json, cost.json)
```
Each stage reads and writes `runs/<phone-slug>/`, is idempotent, writes `stage-N.log.md`, fails soft per source and loud
per stage. Extraction schema per source: `{category, aspect, sentiment -2..+2, quote, locator, reviewer}`. Synthesis per
category: score 0–10, agreement (strong/mixed/split), praised and criticised points with reviewer counts, disagreements,
problems from ≥ 2 independent sources, buy/skip, alternatives that sources mention.

## 19. Control flow, secrets, evals

- **Issues:** open "Review: <phone>" → bot comments progress → reply `/approve research` or `@claude <fix>` → watch the
  preview MP4 → `/approve preview` or feedback → Release link.
- **Secrets:** `ANTHROPIC_API_KEY`; optional `CLAUDE_CODE_OAUTH_TOKEN`; `YOUTUBE_API_KEY`; optional `TTS_API_KEY`;
  VPS runner / `VPS_SSH_KEY`; `YT_COOKIES` (for the fetch-video workflow, §8).
- **Evals:** `evals/` holds 3 released phones with hand-checked findings; CI reports claim precision, locator accuracy and
  score drift when `prompts/` or `config/models.yaml` change; changes merge only if evals don't get worse.

## 20. Build phases (stop and report after each)

0 Feasibility spike (done, §21) · 1 Research pipeline (stages 1–3) + issue flow + verifier loop · 2 Scene template library +
`/make-composition` + `/visual-qa` skills · 3 Script, voice, full 1080p preview · 4 4K final, thumbnail critique, packaging,
`cost.json` · 5 Evals, Shorts, Telugu i18n.

**Done (v1):** one issue produces a reviewed `analysis.md` and a QA-passed preview with no manual steps; two approvals
produce a 4K MP4, thumbnail and metadata as a Release; every claim traces to a locator and passed the `max` verifier; no
creator footage or AI product imagery; cost reported and under budget; all of it runnable from a phone.

## 21. Phase 0 measurements (2026-10-01, 4 vCPU / 16 GB, software GL)

![Phase 0 contact sheet](phase0-contact-sheet.jpg)

| Variant | Workers | Wall time | × real time | Output |
|---|---|---|---|---|
| 1080p | 1 (auto) | 184 s | 9.2× | 6 MB |
| 1080p | 4 | 76 s | 3.8× | 6 MB |
| 4K native (3840 canvas + `zoom: 2`) | 4 | 260 s | 13× | 110 MB, 46 Mbps |
| `--resolution 4k` | 4 | 1,086 s | 54× | screenshot path |

- Always `--workers 4` (auto picked 1, 2.4× slower). Never `--resolution 4k` (disables BeginFrame, 4.2× slower).
- A 10-minute video: ~38 min 1080p preview, ~2 h 10 min 4K on one runner; a 6-shard matrix brings 4K to ~30 min.
- 4K at 45 Mbps ≈ 3.3 GB per 10 min, over the 2 GiB Release asset limit: cap at ~20 Mbps (YouTube re-encodes anyway).
- yt-dlp from datacenter IPs: 1 of 2 videos returned subtitles, the other 429. Expect frequent 429s; use the VPS fallback.
  The YouTube Data API `captions.download` only works for your own videos. yt-dlp needs `--js-runtimes node`.
- Opus spike (`pipeline/spike/opus_spike.py`): structured output, 1h caching (write, read, read at a different effort),
  image QA. Runs when `ANTHROPIC_API_KEY` is set (~$1.30–2.50). Known gaps: `cost.py` prices refusal-fallback replies at the
  Opus rate; `config/sources.yaml` holds placeholders for the owner to fill.

---

# Part D

## 22. Recommendations (Oct 2026, in order of impact)

**Status (2026-10-08):** done: 3 (vendored stack), 4 (session hook + `/parallel-render` skill), 5 in part (`Fetch media for
a video` workflow; keys and Gofile allowlist wait on the owner), 6 (`scripts/contact_sheet.py`, `pipeline/review_cut.py`),
7 (skills: `/new-documentary`, `/source-media`, `/fact-check`, `/review-cut`, `/parallel-render`, `/deliver`), 8
(`library/`), 9 (`scripts/bench_render.py`), 10 (`/fact-check` + `scripts/claims_check.py`). Pixabay key working
(`PIXABAY_API_KEY`). **Build on demand:** 1 (unified engine) and 2 (scene library) are built when a real video needs them,
then kept in `video/lib/` / `video/engine/` for reuse (owner's call, Oct 2026: no speculative scenes). Session briefs for
them: anatomy-organ, blood-flow, globe-routes, document-forensic, data-graphics, engine (contract in §9.1).

1. **One documentary engine.** Three engines grew up for three videos (§6). Merge them into one: the chip-gamble
   phrase-keyed scene engine (cuts land on words, parallax, maps, documents) + the Prahlad EDL break types (`LIVE`,
   `VO_PAUSE`, `vo_skip`) and shot cache + the breath-hold owner-asset registry. *Why:* every new video currently re-learns
   one engine's quirks; one engine means fixes and scene types carry over.
2. **A reusable scene library** (`video/_lib/`): realistic Three.js organ, cell/blood flythrough, molecule, globe/map with
   routes, document desk with highlighter, timeline, data dial, split screen, magnifier. Built once with the §9 realism
   recipe and HDRI lighting, then parameterised. *Why:* 3D is the slowest part (~50 s of render per second); proven scenes
   remove the build-and-fix rounds.
3. **Vendor the missing Three.js pieces**: loaders (GLTF, HDR, DRACO, KTX2), pmndrs `postprocessing`, N8AO, `simplex-noise`,
   pinned in `package.json` and copied by `scripts/vendor-assets.mjs`. *Why:* without loaders, no real models or HDRIs.
4. **Parallel production as the default** for any video over 5 minutes (§3), with a coordinator session. Add a SessionStart
   hook or environment setup script that runs `npm ci` and the pip installs, so each new session is ready in minutes.
5. **Fix the media blocks at the source, legitimately:**
   - Add free **Pexels and Pixabay API keys** as environment secrets (free; both licences allow commercial YouTube use, and we
     credit anyway). Also Unsplash and Freesound keys, and a NARA key by email (§8.2).
   - ~~Allowlist Gofile~~ Deliver through Google Drive (owner, 2026-10-13): add `GDRIVE_RCLONE_TOKEN` (§1).
   - Use the **VPS** for YouTube (yt-dlp with a throwaway account's cookies) through the `Fetch video` workflow on the
     self-hosted runner, and extend it to take a list of URLs.
   - Ask the owner to drop must-have event footage in Google Drive; sessions can read it with the Drive connector.
6. **Automated visual QA:** after every render, a contact sheet goes to Opus at `high` effort with the §14 checklist and the
   EDL text; it writes `review.md`, and nothing ships with an open issue. *Why:* Opus 5.5 reads images precisely (§2), and
   most owner notes (wrong monitor numbers, stock repeats, missing labels) are visible on a contact sheet.
7. **Project skills in `.claude/skills/`** (`/new-documentary`, `/source-media`, `/review-cut`, `/deliver`) that encode
   Part B step by step. *Why:* every session then starts the same way and can't skip the manifest, contact sheet or review.
8. **A shared asset library** with its own manifest: brand stings, music beds, verified CC0/CC BY B-roll, HDRIs, 3D models.
   *Why:* sourcing is the one step parallel sessions can't speed up (shared IP); reuse is the only way to make it faster.
9. **Measure before adopting** any expensive effect: render a 2 s shard with and without it and log the cost in §15.
10. **Fact-check as a separate pass** at `max` effort in a fresh context (as the phone pipeline already does), producing a
    claims table (claim → source URL → status) committed with each video, like `episodes/.../04-fact-check.md`.

---

# Part E: Owner's channel charter (verbatim, received 2026-10-08)

> **Owner's amendments (2026-10-09), which win over the text below:** acronyms as one word (ఈడీ, ఓటీపీ), `?` on
> questions and v4 emotion tags are allowed (§4b, CLAUDE.md); no fixed runtime or act timestamps (the topic sets
> the length; acts are proportions, §4b); ElevenLabs blocks of 4,000–4,500 characters (cap 5,000), not 100–130 words;
> narration is heavy Tenglish spoken Telugu (§4b). The `...` ban below was already lifted on 2026-10-08.

Kept word for word so later sessions read the owner's own wording. How each point maps onto this playbook: Part B intro.
Owner's amendment (2026-10-08): `...` is now allowed for dramatic pauses (§4a); the rest of rule 4.2 stands.

#### CLAUDE DIRECTIVE: "BE PRACTICAL WITH KISHORE"
#### THE DEFINITIVE PRODUCTION CHARTER & AUTOMATED DOCUMENTARY ENGINE

#### 1. THE MISSION & CHANNEL MONOPOLY
- Channel Identity: "Be Practical with Kishore" is the digital defense shield and ultimate investigative platform for Telugu audiences across Telangana, Andhra Pradesh, and the global diaspora.
- The Core Problem in Telugu YouTube:
  - Finance channels (Money Purse, Koushik Maridi) are either dry, slow, 30-minute boring classroom lectures or surface-level promotional summaries.
  - Stock channels (Day Trader Telugu) isolate the common man with overly complex trading jargon.
  - Mystery/Science channels (Think Deep) rely on unverified pop-science blogs and sensationalism.
  - News/Explainer channels (VR Raja, NB Show) either rely on loud sensationalist yelling without deep research, or flat studio monologues.
- The "Super-Channel" Solution:
  "Be Practical with Kishore" eliminates the need for any other channel. It fuses:
  1. The mass emotional urgency & scroll-stopping hooks of VR Raja.
  2. The dark cinematic atmosphere, Hans Zimmer-style pulse, and audio ducking of Think Deep.
  3. The structured chronological clarity of NB Show.
  4. The 2.5D visual dynamism, animated live-browsing, and investigative depth of Vox & Johnny Harris.
  5. An impenetrable moat of 100% peer-reviewed scientific papers (Nature, PNAS) and legal primary sources (Supreme Court rulings, RBI Master Directions).

---

#### 2. THE PSYCHOLOGICAL OPERATING SYSTEM (TELUGU VIEWER COGNITION)
Every script, visual cue, and audio beat produced by Claude must be calibrated against the lived reality and deep psychological wiring of the Telugu middle-class:

##### A. The Honor vs. Shame Axis ("పరువు & గౌరవం")
- In Telugu culture, public humiliation (neighbors finding out about debt, relatives discovering EMI defaults, office colleagues getting recovery calls) triggers severe existential panic.
- Core Rule: Never victim-blame the viewer. Never speak from an ivory tower.
- Psychological Re-framing: Remove the viewer's personal guilt and channel their anger against predatory corporate systems:
  "ఇది మీ తప్పు కాదు... ఈ కార్పొరేట్ సిస్టమ్ మిమ్మల్ని ట్రాప్ చేయడానికి పన్నిన పక్కా వ్యూహం. ఇప్పుడు ఆ ట్రాప్ ని లీగల్ గా ఎలా బద్దలు కొట్టాలో చూద్దాం."

##### B. Regional Realities & Cultural Touchpoints
- Address the authentic anxieties of:
  - Hyderabad IT professionals trapped in lifestyle inflation, multiple credit cards, and tech layoffs.
  - Coastal AP & Rayalaseema small business owners, traders, and agricultural families facing predatory private finance.
  - Middle-class parents suffocating under education donations, gold mortgage interest, and real estate/HYDRAA anxieties.
- Voice Persona: The fearless, fiercely intelligent, street-smart elder brother ("అన్నయ్య") who stands between the viewer and corporate predators. Not a professor. A battle-tested protector.

##### C. Conversational Cadence (Natural Telugu Idioms)
- Avoid textbook bookish Telugu (గ్రాంథిక భాష).
- Use natural, punchy, conversational bridges:
  "పచ్చి నిజం ఏంటంటే...", "తెరవెనుక అసలు మోసం ఇక్కడే ఉంది...", "మన నెత్తిమీద బండరాయిలా పడే ఆ ఒక్క క్లాజ్...", "కంటిమీద కునుకు లేకుండా చేసే ఈ చక్రవడ్డీ...".

---

#### 3. THE 4-ACT SCREENPLAY & EMOTIONAL CHOREOGRAPHY
Every documentary must adhere to this 4-act structural cadence. Narration text, visual events, and audio tracks must move in perfect lockstep:

##### ACT 1: THE VISCERAL HOOK (0:00 – 1:15)
- Psychological Objective: Stop the scroll immediately, validate silent anxieties, create irresistible curiosity.
- Narration Cadence: Rapid, high-urgency rhetorical questions delivered with raw empathy.
- Visuals: Fast-paced, high-contrast imagery, dark UI frames, red alert stamps.
- Audio: Low-end dark tension drone (sub-bass pulse) + ticking clock.

##### ACT 2: THE SYSTEMIC BETRAYAL (1:15 – 4:00)
- Psychological Objective: Expose the fine print, algorithms, and legal loopholes rigged against the common man. Righteous anger replaces helplessness.
- Narration Cadence: Analytical, razor-sharp, investigative breakdown.
- Visuals: Simulated live browsing (interactive portals, dynamic mouse cursors, typing SFX, yellow highlighters circling abusive clauses).
- Audio: Minimalist pulsing synth (Investigation track), low-volume mechanical clicks.

##### ACT 3: THE CLIMAX & SHOCK REVEAL (4:00 – 6:30)
- Psychological Objective: Shatter common myths with undeniable, shocking proof.
- The Dramatic Silence Rule: Right before the core truth is uttered (e.g., "అసలు బ్యాంక్ మిమ్మల్ని ఎందుకు అరెస్ట్ చేయలేదో తెలుసా?"), the background music must cut to ABSOLUTE ZERO SILENCE for 1.5 seconds.
- Impact: Follow the silence immediately with a massive cinematic low-end thud/braam as the verifiable proof slams onto the screen.

##### ACT 4: THE PRACTICAL DEFENSE & EMPOWERMENT (6:30 – Outro)
- Psychological Objective: Hand the viewer actionable, step-by-step armor (legal sections, dispute templates, negotiation rules). Restore dignity and peace of mind.
- Narration Cadence: Reassuring, commanding, victorious, and protective.
- Visuals: Clean action checklists, official legal seals, calm resolution graphics.
- Audio: Warm, reflective, hopeful cinematic piano/ambient outro.

---

#### 4. STRICT SCRIPT SANITIZATION (ELEVENLABS "BUNTY" VOICE ENGINE)
To guarantee 100% flawless audio synthesis with the "Bunty" voice and prevent buffer drops, attention drift, character skips, and truncation:

1. Zero Stage Directions in Text:
   - Absolutely no `[Pause]`, `[Whisper]`, `[Music stops]`, or `(Tone: Serious)` inside the text string.
2. Minimalist Punctuation:
   - Use only commas (`,`) for natural breath pauses and full stops (`.`) for sentence endings.
   - Strictly ban: ellipses (`...`), em-dashes (`--`), quotation marks (`"`), and exclamation points (`!`).
3. Phonetic Telugu for Technical Terms & Numbers:
   - Numbers: Always spell out phonetically in Telugu script (`ఫైవ్ థౌసండ్`, `ట్వెంటీ లాక్స్`, `వన్ హండ్రెడ్`). Never use raw digits (`5000`, `20L`).
   - Decimals & Percentages: Avoid heavy consonant clusters like "పాయింట్ ఫైవ్". Write `అర శాతం` or `మూడు నుంచి నాలుగు శాతం`.
   - Acronyms: Separate letters cleanly with spaces in Telugu script (`ఆర్ బి ఐ`, `హెచ్ డి ఎఫ్ సి`, `ఎన్ పి ఏ`, `సిబిల్`, `ఓ టి ఎస్`).
   - Technical/Financial Vocabulary: Transliterate commonly understood English terms into Telugu script (`స్టేట్‌మెంట్`, `మినిమమ్ డ్యూ`, `అల్గారిథమ్`, `రికవరీ ఏజెంట్`).
4. Strict Chunk Segmentation:
   - Divide every script into 5 to 6 distinct modular blocks.
   - Word count constraint: 100 to 130 words per block (under 1,200 characters).
   - This ensures the model never experiences buffer exhaustion and completes every file cleanly.

---

#### 5. VISUAL AUTOMATION & MOTION STANDARDS (FFMPEG / PYTHON PIL)
Never display boring talking-head monologues or flat static slides. Visuals must be dynamic, simulated, and cinematic:

1. Simulated Live Browsing Engine:
   - For web/app topics (e.g., Amazon/Flipkart sales, banking portals, CIBIL dashboards):
   - Generate virtual dark-mode browser mockups (URL bar, navigation buttons).
   - Render animated mouse cursor movement interpolating smoothly across the frame.
   - Simulate live typing inside search fields accompanied by typewriter SFX.
   - Simulate button clicks with expanding radial ripple rings and crisp click SFX.
2. Dynamic Data & Charts (Bloomberg / Vox Style):
   - Use Python PIL / Matplotlib to render animated line charts (e.g., price hike histories, compounding debt curves).
   - Draw glowing lines dynamically across the timeline with synchronized digital meter SFX.
3. The Journalistic Citation Overlay:
   - Reinforce high credibility by placing minimalist, high-tech lower-third tags for every single factual, legal, or scientific claim:
     `[RBI MASTER DIRECTION: DOR.STR.REC.4/2023]`
     `[INDIAN CONTRACT ACT: SECTION 171]`
     `[SUPREME COURT RULING: CRIMINAL VS CIVIL BREACH]`
     `[NATURE (1982) | HARVARD MONK STUDY]`
4. Pacing Cadence:
   - Visual focal points must change every 3.0 to 3.5 seconds (slow 2.5D camera push, pan, yellow highlight reveal, or angle shift).

---

#### 6. MASTER SOUND DESIGN & AUDIO MIXING SPECIFICATIONS
Sound design is 50% of retention. Claude must configure FFmpeg mixing commands according to this strict decibel matrix:

| Audio Layer | Decibel (dB) Level | Behavior & Rules |
| :--- | :--- | :--- |
| Bunty Voiceover (VO) | `-2 dB` to `-3 dB` | Master anchor. Crisp, normalized, high-clarity speech. |
| BGM Under Speech | `-24 dB` to `-26 dB` | Subtle, atmospheric bed. Must never compete with VO clarity. |
| BGM Speech Pauses (Swells) | `-12 dB` | Smooth 0.5s ramp up during voice gaps to maintain cinematic tension. |
| Climax Shock Point | `0 dB (Complete Silence)`| Instant 1.5s hard cut of music before major shocking facts. |
| Cinematic Impacts (Braams/Thuds)| `-6 dB` to `-8 dB` | Heavy sub-bass drop following the silence window. |
| Tactical SFX (Clicks/Typing/Whoosh)| `-8 dB` to `-10 dB`| Precise sync with cursor clicks, highlights, and transitions. |

---

#### 7. AUTONOMOUS END-TO-END EXECUTION WORKFLOW
When the user supplies a topic and core hypothesis:

##### Phase 1: Fact-Checking & The Trojan Horse Angle
- Audit the subject. Map viral myths versus verified legal/scientific facts.
- Design the "Trojan Horse Hook": Hook the viewer with the popular mystery, but resolve it using mind-bending, verified truth.

##### Phase 2: Screenplay & Sanitized Blocks
- Draft the emotionally gripping Telugu script following the 4-Act structure.
- Sanitize the text strictly for ElevenLabs Bunty into 5–6 modular blocks.

##### Phase 3: Visual & Audio Choreography
- Generate the simulated web mockups, animated charts, and citation badges.
- Map exact timestamps for music switches, audio ducking, and silence drops.

##### Phase 4: Local Assembly & FFmpeg Rendering
- Assemble the assets via FFmpeg on Android/Termux using low-overhead filtergraphs.
- Output a production-ready, fully mastered 1080p MP4 file.

# Part F: Owner's production handoff guide and style examples (verbatim, received 2026-10-15)

Kept word for word. How each point maps onto this playbook: §4a-4 (which notes where we keep a stricter rule, e.g.
number words in VO text and fact-checked numbers only).

## F.1 Production & scriptwriting handoff guide

# Master Production & Scriptwriting Handoff for Claude
## Channel: Be Practical with Kishore | Voice Engine: ElevenLabs (Akash V4)

> **How to Use This Document:** Copy and paste this entire document directly into Claude as your primary System Prompt / Instruction Set before generating scripts, outlines, or visual storyboards for *Be Practical with Kishore*.

---

## 1. Channel Identity & Audience Ethos

* **Channel Name:** Be Practical with Kishore
* **Core Mission:** Demystifying complex Indian financial traps, civic rights, legal protections, and industrial engineering paradoxes through forensic documentary storytelling.
* **Target Audience:** 100% Indian citizens—salaried professionals, middle-class households, youth, small business owners, and families navigating modern Indian consumer and legal systems.
* **National Sentiment & Ethos:**
  * **Not Cynical, Not Preachy:** Never sound hopeless about India. We do not bash Indian systems; we empower Indian citizens to navigate them intelligently.
  * **Curiosity & National Pride:** Connect every topic to India’s growth story. When an Indian citizen understands their rights (RBI rules, BNSS, RERA), the entire nation becomes stronger and more accountable. In macro stories (Semiconductors, ISRO, Railways, Defense), celebrate Indian engineering brilliance while critically examining industrial bottlenecks.

---

## 2. Voice & Tone: Killing the "News Reader" Drone

### The Problem
Previous scripts sounded like formal textbook chapters or dry news broadcasts:
* ❌ *"Now let us come to the biggest fear..."*
* ❌ *"First, one thing must be clear..."*
* ❌ *"Let us understand the maths in very simple words..."*
* ❌ *"In this video we will examine eight points..."*

### The New Standard: The "Practical Elder Brother / Trusted Guide"
Kishore is not a news anchor reading a teleprompter; he is a sharp, street-smart, legally sound friend talking to you across a table.
* **Conversational Phrasing:** Use natural Indian English rhythms, conversational bridges, and relatable daily experiences (salary day on the 1st or 5th, WhatsApp family groups, auto rides, UPI payments, local police stations, bank branch visits).
* **Direct Emotional Connection:** Acknowledge fear, confusion, and frustration without patronizing.
* **Spoken-Word Sentence Variety:** Mix short, punchy statements with longer rhythmic observations. Never write five 4-word sentences back-to-back—this causes ElevenLabs to produce a robotic, repetitive downward inflection.

---

## 3. ElevenLabs Akash V4: Voice Optimization & Audio Rules

Because the channel uses ElevenLabs **Akash**, the script MUST be optimized specifically for speech synthesis. Raw written text creates fatal pronunciation errors and monotonic cadence.

### Mandatory Phonetic Substitution Table
Always write these terms phonetically in the final voiceover script:

| Intended Term | NEVER Write in Script | ALWAYS Write for Akash | Why |
| :--- | :--- | :--- | :--- |
| **CIBIL Score** | `CIBIL` | `Sib-ill` or `Sibill` | Akash pronounces `CIBIL` as the English word *"civil"*, destroying credibility. |
| **Lok Adalat** | `Lok Adalat` | `Loke Uh-daa-lut` | Prevents garbled pronunciation of legal terms. |
| **NPA** | `NPA` | `N-P-A` | Prevents the model from slurring it into one syllable. |
| **EMI** | `EMI` | `E-M-I` | Ensures clean letter-by-letter spacing. |
| **GST** | `GST` | `G-S-T` | Crisp institutional pronunciation. |
| **RBI** | `RBI` | `R-B-I` | Avoids swallowing the acronym. |
| **BNSS** | `BNSS` | `B-N-S-S` | Clear statutory articulation. |
| **RERA** | `RERA` | `Ray-rah` | Standard Indian legal cadence. |
| **FIR** | `FIR` | `F-I-R` | Prevents reading as the word "fur". |
| **TPA (Insurance)** | `TPA` | `T-P-A` | Third-party administrator clarity. |
| **Rupee Amounts** | `Rs 65000` or `65k` | `₹65,000` or `65 thousand rupees` | Natural speech flow. |

### Punctuation-Based Breath & Cadence Control
* **The Dramatic Pause (`...`):** Insert ellipses when the listener needs half a second to process a shocking number or revelation.
* **The Mid-Thought Pivot (`—`):** Use em-dashes instead of commas to create natural conversational hesitation.
* **Question Marks with Hooks:** End questions naturally to force upward vocal inflection.
* **Eliminate Monotony:** Never stack short, choppy sentences. Blend short punches with flowing thoughts.

---

## 4. Crystal-Clear Audio Script Comparison

### Example 1: Explaining Credit Card Debt & Non-Performing Assets

#### ❌ OLD WAY (News Reader / Textbook Drone)
> "Now let us understand the payment timeline. If the minimum amount due is not paid for ninety days from the due date, under Reserve Bank of India rules the account becomes an NPA, which means Non-Performing Asset. This means the bank categorizes it as a bad loan. Does this mean you do not have to pay? No, it does not cancel your debt. Now let us look at the late fee calculation."

*Why it fails:* Cold, academic, repetitive sentence cadence. Sounds like reading an RBI annual report.

#### ✅ NEW WAY (Human, Relatable, Formatted for Akash)
> "Here is what happens on day 90... that no branch manager will ever admit to your face.
> 
> When your bill crosses that 90-day mark, the bank doesn’t just tag your file as an N-P-A—a Non-Performing Asset. Behind the scenes, strict R-B-I rules kick in... forcing that bank to take 25% of your entire pending balance straight out of their own quarterly profits, and lock it away in a provision vault. 
> 
> Think about that for a second. 
> 
> The sudden flood of aggressive calls? The urgent recovery messages at 8:01 in the morning? It’s not happening because you committed a crime. It’s happening because your single unpaid card is literally punching a hole in that bank manager’s balance sheet."

---

### Example 2: The India Semiconductor Mission (Curiosity & National Pride)

#### ❌ OLD WAY (Generic Corporate Explainer)
> "In 2021 India launched the India Semiconductor Mission with an incentive of ten billion dollars. India designs twenty percent of the world's chips in Bengaluru. But India does not manufacture them. Therefore, the government is funding Tata and Micron to build fabs in Gujarat and Assam."

*Why it fails:* Bland list of facts; zero emotional stakes or cinematic intrigue.

#### ✅ NEW WAY (Cinematic, Forensic, Proud & Grounded)
> "Walk into any technology park in Bengaluru, Hyderabad, or Noida tonight... and look up at those glowing glass towers. 
> 
> Inside, Indian engineers are designing the most advanced microchips on planet Earth—routing microscopic power lines for Apple, Nvidia, and Qualcomm. Almost 20% of the world’s chip brains are born right here on our soil. 
> 
> But here is the heartbreaking paradox: once our engineers hit 'Send', those digital blueprints fly across undersea cables to factories in Taiwan and South Korea. We design the brains... but we don’t own the hands. And when global supply chains snapped, our own car factories sat frozen with finished vehicles waiting for a three-dollar piece of imported silicon. 
> 
> Today, in the red soil of Dholera and the industrial corridors of Assam, that 40-year curse is finally being broken."

---

## 5. Visual Direction: Ending the "Stock B-Roll Wallpaper"

Claude must script videos in a **Dual-Column Screenplay Format** featuring three dedicated visual tracks:

```markdown
========================================================================================
[TIME / SCENE] | [AUDIO VOICEOVER - AKASH]           | [VISUAL FORENSICS & SOUND DESIGN]
========================================================================================
[00:00 - 00:15]| "You swipe your card for groceries... | [VISUAL]: Ultra-realistic kinetic UI
               | and think you have 50 days free.    | simulation of an HDFC/ICICI mobile 
               | But look at what happens on day 51." | banking statement.
               |                                     | [ACTION]: Dynamic camera zoom-in. 
               |                                     | Animated fluorescent yellow highlighter 
               |                                     | sweeps across line item: "Finance Charges".
               |                                     | [SFX]: High-frequency digital UI 'blip' + 
               |                                     | metallic cash register latch snap.
```

### The 4 Visual Pillars of "Be Practical"
1. **Document Forensics:**
   * Actual RBI circulars, Supreme Court orders, and IRDAI gazette notifications displayed with real paper textures.
   * Kinetic highlighter effects (yellow/orange) isolating specific legal clauses.
   * Bold rubber stamps: `[VIOLATION]`, `[ILLEGAL DEMAND]`, `[MANDATORY 60 DAYS]`.
2. **Interactive Mathematical Models:**
   * Never just state a calculation—simulate it.
   * Show a dynamic digital ledger: Principal (₹30,000) $\rightarrow$ Late Fee (₹750) $\rightarrow$ Interest (₹1,125) $\rightarrow$ 18% GST (₹337). An interactive balance bar turns from green to alarming red.
3. **Real Geospatial & Photographic Evidence:**
   * Satellite imagery (Google Earth Studio) zooming into Dholera SIR, Sanand Micron facility, or Bengaluru storm water drains (Rajakaluves).
   * Archival newspaper scans and verified official press releases rather than anonymous stock video clips.
4. **Pacing Rules:**
   * Visual reset every **3.5 to 5.0 seconds** (camera angle shift, document push-in, kinetic text callout, or icon pop).
   * Zero unmotivated stock video clips of anonymous corporate workers typing on laptops.

---

## 6. Video Structure: The 3-Act Retention Formula (8–12 Minutes)

All future scripts produced by Claude must adhere strictly to this structural blueprint:

* **Act 1: The Lived-Reality Hook & The Open Loop (0:00 – 01:15)**
  * Establish an immediate, visceral Indian scenario (an unexpected WhatsApp threat, an inflated hospital bill, an imported defense component).
  * Introduce the **High-Stakes Open Loop**: *"At minute 06:40, I will give you the exact statutory clause that forces the bank to reverse this charge immediately."*
* **Act 2: The Forensic Dissection & The Hidden Trap (01:15 – 07:00)**
  * Break down the math, law, or engineering mechanism step-by-step.
  * Contrast *"What they tell you"* vs. *"What the official gazette actually says"*.
  * Use real case precedents (Consumer Court orders, High Court rulings, CAG audit findings).
* **Act 3: The Citizen’s Action Plan & Tactical Counter-Moves (07:00 – 10:30)**
  * Actionable, step-by-step roadmap: Step 1 (Document), Step 2 (Official Written Escalation), Step 3 (Statutory Ombudsman / Legal Remedy).
  * Specific helpline numbers (14448 for RBI, 1930 for Cyber Crime, 112 for Police).
* **Outro: National Pride, Community Question & Call to Action (10:30 – 11:30)**
  * Connect the personal solution back to the collective strength of India.
  * Pinned-comment question that drives authentic discussion.
  * Reminder: *"Know your rights. Stay practical. Jai Hind."*

---

## 7. Claude Quality Checklist Before Delivering Any Script

Before presenting a finished script, Claude must verify:
- [ ] Are all Indian financial and legal terms spelled phonetically for ElevenLabs Akash (`Sib-ill`, `N-P-A`, `Loke Uh-daa-lut`)?
- [ ] Does the script read like a natural, caring elder brother or practical legal advocate rather than an academic lecturer?
- [ ] Are sentences structured with diverse rhythms, conversational pauses (`...`), and mid-thought breaks (`—`)?
- [ ] Does every single scene include precise visual forensic direction (documents, highlighters, UI mockups, maps) and specific SFX cues?
- [ ] Is there an upfront open loop within the first 60 seconds?
- [ ] Does the video honor and inspire love for India while delivering rigorous, uncompromising truth?

## F.2 Style comparison examples

# Style Comparison & Script Samples: Before vs. After
## Voice Engine: ElevenLabs (Akash V4) | Channel: Be Practical with Kishore

This reference showcases how to transform dry, news-reader scripts into conversational, human, India-centric investigative narratives.

---

### Case Study 1: Financial & Civic Defense
**Topic:** Pillar 3 — Recovery Agent Harassment & RBI Rights

#### ❌ Current Style ("News Reader / Textbook Drone")
*Taken directly from recent upload patterns:*
> "A message comes on your phone your credit card payment is overdue. In our last video we saw how paying only the minimum keeps you in debt. Today a harder question: what if you cannot pay even that minimum? Many people think there is one answer for everyone, there isn't. Someone who owes ten thousand rupees and someone who owes ten lakh live two very different stories. Under the rules, recovery calls are permitted only between eight in the morning and seven in the evening. If recovery agents violate these rules, you can file a complaint with the Reserve Bank of India Ombudsman."

**Why It Fails:**
1. **Robotic Cadence:** Monotonous sentence structure causes ElevenLabs Akash to drop pitch repetitively at every period.
2. **Cold Delivery:** Sounds like a legal textbook being read aloud; fails to connect with the visceral panic of an Indian citizen facing harassment.
3. **Phonetic Traps:** Acronyms like `RBI` and `CIBIL` are mispronounced as "arbitrary letters" or "civil".

---

#### ✅ Upgraded Style ("Human Elder Brother / Forensic Legal Guide")
*Written specifically with breath markers, emotional stakes, and ElevenLabs Akash phonetics:*

```markdown
[VOICEOVER - AKASH V4]
Your phone buzzes on the table... It's an unknown 10-digit number. 

You look at it, and your stomach sinks—because you already know who it is. 

30 calls yesterday. 40 calls today. And then comes that WhatsApp message from a so-called "field executive": *"We are coming to your house today at 4 PM. Keep the cash ready or face police action."*

Look at me for a second... Take a deep breath. 

If you are going through this right now, I want you to know one thing: missing an E-M-I does not make you a criminal. And you do not have to live in fear inside your own home.

Today, I’m not just going to give you sympathy—I’m going to give you the law. 

At minute 05:20, I will show you the exact R-B-I Fair Practices circular... along with a ready-to-send 3-line legal email that forces the bank to pull their agents back within 24 hours. 

You owe the money... yes. But you never sold your dignity. Let’s look at the facts.
```

**Visual Forensics & SFX Layer for this Scene:**
* **Visual:** Realistic mockup of an Indian smartphone lock screen displaying 14 missed calls and a threatening WhatsApp preview from *"Recovery Team - Urgent"*.
* **Action:** Camera smoothly pushes in. The screen dims, and an authentic official PDF of the **RBI Master Direction on Fair Practices Code** slides into frame. An animated neon-yellow highlighter underlines the statutory operating hours: `8:00 AM to 7:00 PM`.
* **Sound Design:** 
  * Subtle, jarring phone vibration buzz on wood (`bzzz... bzzz...`).
  * Deep sub-bass drop when mentioning the WhatsApp threat.
  * Instant, dead silence when Kishore says: *"Take a deep breath."*

---

### Case Study 2: National Engineering & Industrial Curiosity
**Topic:** Pillar 6 — Indian Semiconductor & High-Tech Manufacturing

#### ❌ Current Style ("Generic Corporate Explainer")
> "In 2021 car manufacturers across India had parking lots full of brand new vehicles. Yet none of them could be sold because they were missing a piece of silicon smaller than your fingernail. Today over 60 percent of the world's microchips come from Taiwan. To break this vulnerability, India launched a 10 billion dollar incentive package. Many people ask if Indian manufacturing can achieve the precision required to compete with TSMC."

**Why It Fails:**
1. **Informational without Intrigue:** Recites statistics without cinematic imagery.
2. **Missing Emotional Stakes:** Treats India’s industrial journey like a dry government press release.

---

#### ✅ Upgraded Style ("Cinematic Pride & Relentless Investigation")
*Evokes curiosity, national pride, and engineering reality:*

```markdown
[VOICEOVER - AKASH V4]
In late 2021, something completely bizarre was happening outside car factories across Pune, Chennai, and Gurugram. 

Thousands of brand-new SUVs and sedans were rolling off assembly lines—sparkling paint, plush leather seats, fully built engines... 

And yet, not a single one could be delivered to waiting customers. They were parked in dusty open fields by the thousands. 

Why? Because each of those 15-lakh-rupee machines was waiting for a single chip... smaller than a child's fingernail, costing less than three dollars. 

And every single one of those chips had to travel 4,000 kilometers across the sea from a tiny island called Taiwan.

Think about the absurdity of this: our Indian engineers in Bengaluru and Hyderabad design almost 20% of the world’s most powerful microprocessors. We have the finest software brains on the planet. 

So why couldn't a nation that landed a spacecraft on the South Pole of the Moon make a simple three-dollar microcontroller?

Today, in the industrial heartlands of Dholera, Gujarat and Jagi Road, Assam, that answer is being built in concrete and steel. But between the grand speeches and the actual chips... lies a brutal engineering gauntlet that nobody is talking about. 

Here is the untold story of India’s 10-billion-dollar semiconductor gamble.
```

**Visual Forensics & SFX Layer for this Scene:**
* **Visual:** High-resolution satellite zoom (Google Earth Studio) swooping from the auto hubs of Pune to the sea-lanes of the Taiwan Strait, landing directly on an isometric 3D blueprint of the Tata-PSMC Dholera cleanroom facility.
* **Action:** Dynamic split-screen comparing Chandrayaan-3 landing telemetry against the atomic precision of an Extreme Ultraviolet (EUV) lithography mirror.
* **Sound Design:** 
  * Industrial machinery hum layered with high-tech digital sweeps.
  * Cinematic riser building tension until the beat drops on *"Here is the untold story"*.

---

### Core Upgrades Summary Table

| Dimension | Previous Channel Output | Upgraded Benchmark |
| :--- | :--- | :--- |
| **Speaker Persona** | Distant, clinical news reporter | Empathetic elder brother / fearless civic advocate |
| **ElevenLabs Optimization** | Raw text, leading to `CIBIL` $\rightarrow$ "civil" errors | Full phonetic dictionary (`Sib-ill`, `N-P-A`, `Ray-rah`) |
| **Vocal Inflection** | Monotonous pitch drops at every period | Dynamic sentence length, dramatic pauses (`...`), em-dashes (`—`) |
| **Visual Architecture** | Anonymous stock videos of people at desks | Real government gazettes, court orders, kinetic math models, satellite maps |
| **India-Centric Angle** | Generic consumer advice | Grounded in Indian middle-class life, celebrating Indian capability while solving real systemic pain |
