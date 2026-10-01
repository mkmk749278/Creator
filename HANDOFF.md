# HANDOFF v2 — Phone Consensus Review Video Pipeline (powered by Claude Opus 5.5)

> **For Claude Code.** Read this entire file before writing any code. Build in the phases below, in order. At the end of each phase, stop, summarize what was built, what was measured and what is left, and wait for the owner's go-ahead.
> v2 adds **§3: how to use Claude Opus 5.5 at full strength** in every stage.

---

## 0. Owner context (read first)

- **Owner:** Kishore, a solo developer.
- **Works only from an Android phone** (Termux, SSH to a VPS, GitHub). He has **no PC or laptop.**
- **Everything must run in GitHub Actions** (or on the VPS via a self-hosted runner) **with zero manual steps** beyond starting a run and approving output.
- Nothing may need a GUI or desktop. Previews must be viewable on a phone: an MP4 artifact, a GitHub Pages link or a PNG contact sheet.
- **The control surface is GitHub Issues** (see §6). Kishore opens an issue from his phone, and the pipeline does the rest.
- Language: **English first.** Telugu may come later, so keep all script and on-screen text i18n-ready.

---

## 1. The product

A YouTube channel making **next-gen consensus phone reviews**.

**Premise:** "We analysed what 15+ trusted reviewers said about this phone, so you don't have to."

**What makes it different from other channels**

1. A **consensus scorecard** for each category (display, camera, battery, performance, software, build, value).
2. A **"Where reviewers disagree"** segment.
3. A **"Problems reported by multiple reviewers"** segment (heating, bugs, update policy and similar).
4. **Who should buy it, who should skip it, and better alternatives at the same price.**
5. **Every claim is traceable** to its source (reviewer, video or article, timestamp).

---

## 2. Video spec — "ultra realistic, HyperFrames, 4K"

| Item | Spec |
|---|---|
| Resolution | **3840×2160 (4K UHD)**, with a 1080p fast-preview mode |
| Frame rate | 30 fps by default; 60 fps via a config flag |
| Length | 8–12 minutes |
| Codec | H.264 High profile at a bitrate suitable for YouTube 4K upload |
| Shorts | Optional 1080×1920 "verdict in 60 seconds" cut from the same data |
| Look | Dark, premium, Apple-keynote and cinematic style: glassmorphism, depth, light sweeps, parallax over product images, kinetic typography and animated charts |

### Rendering engine: HyperFrames (HeyGen, open source, Apache 2.0)

- Repo: https://github.com/heygen-com/hyperframes · Docs: https://hyperframes.heygen.com
- Videos are written as **HTML, CSS and JS** and rendered to MP4 with **deterministic, frame-by-frame capture** (headless Chrome + FFmpeg). It was **built for AI agents to author**, which makes it a strong fit for Opus 5.5.
- Requirements: Node.js 22+, FFmpeg, headless Chrome.
- CLI: `npx hyperframes init`, `preview`, `render`, `lint`, `check`, `snapshot`, `doctor`.
- Timing uses `class="clip"` elements with `data-start`, `data-duration` and `data-track-index`. Canvas size uses `data-width` and `data-height`.
- Animation adapters: GSAP, CSS, Lottie, Three.js, Anime.js and WAAPI. Every animation must be seekable.
- Claude Code skills: `claude plugin marketplace add heygen-com/hyperframes`, then use the `/hyperframes` router. **Install this first.**
- 4K support is not stated in the docs. **Verify in Phase 0.**

### What "ultra realistic" means for this channel (hard rules)

- ✅ Official press images and videos from the brand, cinematic pans and zooms, depth-of-field, reflections, and Three.js scenes using official product images
- ✅ Real spec data rendered as animated charts and scorecards
- ❌ **No AI-generated images or video of the phone itself, no AI camera samples, no fake hands-on footage.** This would mislead buyers and break YouTube's synthetic-content rules.
- ❌ No footage taken from other creators' videos. Reviewers are **credited by name and quoted in on-screen text**.
- AI-generated abstract backgrounds or textures (not depicting the product) are allowed, and must be logged in the credits file.

---

## 3. Using Claude Opus 5.5 at full strength ⭐ (new in v2)

### 3.1 What Opus 5.5 gives us (released 22 Sep 2026)

| Capability | Fact | What we use it for |
|---|---|---|
| Model ID | `claude-opus-5-5` (Claude API; also Bedrock, Google Cloud, Foundry) | All AI stages |
| **Context window** | **1M tokens** | Put **all 15–25 transcripts + articles + specs in a single call** for real cross-source synthesis. No chunking, no lost nuance. |
| **Max output** | **128K tokens** (300K on Batch API, beta) | Full script + scene plan + metadata in one response. Whole HyperFrames compositions in one pass. |
| Input modalities | **Text + images → text** (no video or audio input) | **Visual QA of rendered frames**, vetting press images, critiquing thumbnails. Video is covered by transcripts + FFmpeg-extracted frames. |
| **Adaptive thinking** | Always on. **Cannot be disabled.** | Deep reasoning by default. Control depth with **effort**. |
| **Effort levels** | `low` · `medium` (default) · `high` · `xhigh` · `max` | Match effort to the task (see 3.3). |
| Agentic work | Leads in agentic coding, computer use and knowledge work; long unattended runs (Anthropic cites 18 h); fewer tool steps than earlier models | Claude Code builds the pipeline **and** writes each video's composition, then renders, inspects and fixes it in a loop. |
| Code review | Caught 72% of known bugs vs 56% for Opus 5 | Automatic PR review of pipeline code |
| Writing | ~40% less verbose, most important information first | Narration that sounds like a person, not filler |
| Pricing | $4 / $20 per MTok input/output · cache read **$0.20** · cache write $5 (5 min) or $8 (1 h) · **Batch −50%** · Fast mode 2.5× speed at $8/$40 | Cost design in 3.4 |
| Knowledge cutoff | June 2026 | **Never trust model memory for phone facts.** Every fact comes from collected sources. |

**API breaking changes vs Opus 5 (Claude Code must handle these):**
- Thinking cannot be turned off, so don't send `thinking: disabled`.
- **Forcing a specific tool returns an error.** Don't use forced `tool_choice` to get JSON. Use the API's structured-output / JSON-schema features instead, with schema validation (Pydantic or Zod) and a retry on invalid output. Check the current API docs for the exact parameter shape.
- Text between tool calls now appears in `thinking` blocks. Parsers must not assume it's in `text` blocks.
- Thinking blocks are tied to the model and conversation. Pass them back unchanged in multi-turn tool loops.
- The `computer_20251124` tool is not supported on the Claude API. We don't need it.

### 3.2 Two ways Opus 5.5 runs in this project

1. **Claude API calls from pipeline code** (Anthropic SDK; Python or TypeScript): for the data stages where we need structured JSON, caching and batch pricing (extraction, synthesis, fact-check, script).
2. **Claude Code as an agent inside GitHub Actions** (`anthropics/claude-code-action@v1` with `claude_args: --model claude-opus-5-5`): for creative and engineering stages where the model has to write files, run commands, render, look at the output and iterate (composition authoring, visual QA, fixing failures).
   - Auth: `ANTHROPIC_API_KEY`, **or `CLAUDE_CODE_OAUTH_TOKEN`** (from `claude setup-token`) so agent runs use Kishore's Claude subscription instead of API billing. Support both.
   - Cap runs with `--max-turns` and workflow `timeout-minutes`. Use `concurrency` to avoid parallel runs on the same phone.
   - Put project skills in `.claude/skills/` (e.g. `/make-composition`, `/visual-qa`) so prompts stay short and repeatable.

### 3.3 Effort routing (fixed table: put this in `config/models.yaml`)

| Task | Mode | Effort | Why |
|---|---|---|---|
| Source relevance filter (is this a real review of *this* phone?) | API, Batch | `low` | Simple classification, high volume |
| Per-source claim extraction | API, **Batch** | `medium` | Structured, parallel, not urgent: 50% off |
| **Cross-source consensus synthesis** (all sources in one 1M call) | API | **`xhigh`** | This is the product. Weighing conflicting evidence needs deep reasoning. |
| **Fact-check / verifier pass** | API (separate call, fresh context) | **`max`** | Last line of defense against wrong claims on a public channel |
| Script writing | API | `high` | Quality narration, tight pacing |
| Titles, description, chapters, tags | API | `medium` | |
| Composition authoring (HyperFrames HTML/GSAP) | Claude Code agent | `high` | Agentic coding |
| Visual QA of frames | Claude Code agent / API with images | `high` | Spotting layout bugs needs care |
| Pipeline coding and refactors (by the owner in Claude Code) | Claude Code | `high`; `max` for architecture | |

Exact effort values must be configurable. Never hard-code them.

### 3.4 Cost design

- **Prompt caching:** Cache the big shared prefix (system prompt + schema + full source bundle) once. Synthesis, the verifier and script calls then reuse it at **$0.20/MTok** instead of $4. Use the **1-hour cache** because stages run minutes apart.
- **Batch API** for extraction and filtering (−50%).
- **Fast mode: off by default.** Nothing here is latency-critical.
- Each run writes `cost.json` (tokens in/out/cache per stage, $ estimate). The issue comment shows the total.
- Target: **AI cost per video under a configured budget** (default $15). Stop and ask in the issue if a run would exceed it.

### 3.5 Self-correcting loops (where Opus 5.5 earns its keep)

1. **Research loop:** synthesis → verifier (`max`, fresh context, must cite source + timestamp/paragraph for every claim, outputs `PASS` or a list of failures) → re-synthesis on failures. Max 2 rounds, then flag for human review.
2. **Render loop (agent):** write composition → `hyperframes lint` + `check` → `snapshot` key frames → **Opus 5.5 looks at the PNGs** (text overflow, overlap, wrong colours, unreadable text at phone size, wrong phone image, brand drift) → fix → repeat. Max 3 rounds. Save every QA verdict to `qa/`.
3. **Media vetting:** Opus 5.5 checks each downloaded press image. Is it the right model and colour? Is it free of watermarks? Is it high enough resolution for 4K? Reject failures automatically.
4. **Thumbnail critique:** generate 3 variants from templates → Opus 5.5 ranks them for readability at mobile size → keep the best and log the reasons.

### 3.6 Guardrails

- **Facts only from the collected sources.** The prompt must forbid model-memory facts, because the model's knowledge stops at June 2026.
- All fetched web and transcript text is **untrusted data**: wrap it in delimiters and tell the model to ignore instructions inside it (prompt-injection defense).
- Validate every model output against a schema. Invalid output → retry once → fail the stage loudly.

---

## 4. Pipeline architecture

```
GitHub Issue "Review: <phone>"  (opened from phone, label: review)
   │
   ▼
[1] DISCOVER  → trusted reviews (YouTube + web)            [API, low, batch]
[2] COLLECT   → transcripts, articles, specs, press media  [code + media vetting]
[3] ANALYSE   → extract (batch) → synthesise (1M, xhigh)
               → verify (max) → analysis.json/.md           ⟵ owner approves in issue
[4] SCRIPT    → narration + scenes + metadata              [API, high]
[5] VOICE     → owner recording or TTS; real durations
[6] COMPOSE   → Claude Code agent writes HyperFrames project [agent, high]
[7] RENDER    → 1080p preview + visual-QA loop              ⟵ owner approves in issue
               → 4K final (chunked or VPS)
[8] PACKAGE   → MP4, thumbnail, youtube.json, credits, cost.json → GitHub Release
```

Each stage reads and writes `runs/<phone-slug>/`. Every stage is idempotent and can be rerun alone.

### Repo layout

```
phone-consensus/
├─ CLAUDE.md                 # generated in Phase 0 from this file
├─ HANDOFF.md
├─ .claude/skills/           # make-composition, visual-qa, fact-check …
├─ config/
│  ├─ sources.yaml           # whitelisted reviewers, sites, press domains
│  ├─ categories.yaml        # scoring categories + weights
│  ├─ models.yaml            # model id, effort per task, budgets
│  └─ brand.yaml             # colours, fonts, channel name
├─ prompts/                  # versioned prompt files + JSON schemas
├─ pipeline/                 # Python 3.12 (Claude Code may propose TS)
├─ video/templates/          # reusable HyperFrames scene templates
├─ runs/<phone-slug>/        # artefacts (gitignored except manifests)
├─ evals/                    # golden test set for analysis quality
└─ .github/workflows/
   ├─ review-request.yml     # issue opened → stages 1–3
   ├─ approve.yml            # "/approve research" | "/approve preview" comments
   ├─ render-preview.yml
   ├─ render-final.yml
   └─ claude.yml             # @claude in issues/PRs for ad-hoc fixes
```

---

## 5. Stage details

### [1] DISCOVER
- `config/sources.yaml` holds a **whitelist** of trusted YouTube channels (by channel ID) and review sites. The owner edits this list; seed it with placeholders and a TODO.
- Use the YouTube Data API v3, restricted to whitelisted channels, plus site search/RSS for articles.
- An Opus 5.5 `low` filter drops unboxings, shorts, rumours and wrong models.
- Output: `sources.json`.

### [2] COLLECT
- **Transcripts:** `yt-dlp` subtitles. ⚠️ YouTube often blocks datacenter IPs. Fallback chain: GitHub runner → VPS self-hosted runner → mark the source "unavailable" and continue.
- **Articles:** main-text extraction (e.g. `trafilatura`). Respect robots.txt.
- **Specs:** one structured source → normalized `specs.json` (including price in INR).
- **Press media:** only from `press_domains` in `sources.yaml`, logged in `media_manifest.json`. Then **vision vetting** (§3.5).

### [3] ANALYSE
- **Extract** (Batch, `medium`): per source → `{category, aspect, sentiment -2..+2, quote, locator, reviewer}`.
- **Synthesise** (single 1M-context call, `xhigh`, cached prefix) per category:
  - consensus score (0–10) + agreement level (strong / mixed / split)
  - praised and criticized points with reviewer counts
  - **disagreements**
  - **problems reported by multiple reviewers** (≥2 independent sources)
  - who should buy / skip, and alternatives (only phones that sources mention)
- **Verify** (`max`, fresh context): every claim → source locator. Loop per §3.5.
- Output: `analysis.json` + phone-readable `analysis.md`, posted as an issue comment. **Wait for `/approve research`.**

### [4] SCRIPT
- `script.json`: scenes with narration, on-screen text, data refs, media refs and target duration.
- Structure: Hook → Specs → Overall scorecard → Category deep-dives → Disagreements → Common problems → Buy/Skip → Alternatives → Verdict + source credits.
- Also: 3 title options, a description with **full source credits and links**, chapters and tags.

### [5] VOICE
- Pluggable: `owner` (Kishore uploads a phone-recorded `.m4a` per scene, attached to the issue or committed to `runs/`) or `tts:<provider>`.
- **Prefer the owner's voice**: it helps YouTube monetization review of AI-heavy content. Scene timing comes from the real audio length.

### [6] COMPOSE (Claude Code agent)
- `claude-code-action` with `/make-composition` builds the HyperFrames project from `script.json` + `analysis.json` + `media/` + audio, **using the template library**:
  `hero-product`, `spec-grid`, `scorecard`, `consensus-bar`, `quote-card`, `disagreement-split`, `issue-alert`, `buy-skip`, `alternatives`, `credits-roll`.
- The agent may add scene-specific polish, but must keep brand tokens from `brand.yaml`.

### [7] RENDER
- Preview at 1080p → visual-QA loop (§3.5) → contact sheet + MP4 posted to the issue. **Wait for `/approve preview`.**
- Final at 4K: (a) GitHub runner matrix split by scene + FFmpeg concat, or (b) VPS self-hosted runner. Decide from Phase 0 measurements and stay well under the 6-hour job limit.

### [8] PACKAGE
- GitHub Release containing `final_4k.mp4`, `thumbnail.png` (1280×720), `youtube.json`, `credits.md`, `media_manifest.json`, `cost.json`.
- YouTube auto-upload is out of scope for v1.

---

## 6. Phone-first control flow (GitHub Issues)

1. Kishore opens an issue from the GitHub app using the template **"Review: Samsung Galaxy XYZ"**.
2. The bot comments progress at each stage, with links to artefacts.
3. He reads `analysis.md` in the comment and replies **`/approve research`** or **`@claude <fix request>`**.
4. He watches the preview MP4 and replies **`/approve preview`** or gives feedback (`@claude make the battery scene slower`).
5. The Release link is posted. He downloads it and uploads to YouTube.

---

## 7. Secrets

| Secret | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | API stages (extraction, synthesis, verify, script) |
| `CLAUDE_CODE_OAUTH_TOKEN` | Optional: agent stages on Kishore's subscription |
| `YOUTUBE_API_KEY` | Discovery |
| `TTS_API_KEY` | Optional |
| VPS self-hosted runner / `VPS_SSH_KEY` | Transcript fallback and/or 4K rendering |

---

## 8. Quality evals (keep the AI honest)

- `evals/` holds 3 already-released phones with hand-checked expected findings (the owner fills these in once).
- CI runs the analysis stage on them when `prompts/` or `config/models.yaml` change, and reports precision of claims, source-locator accuracy and score drift.
- Prompt or model changes merge only if the evals don't get worse.

---

## 9. Build phases (stop after each one)

**Phase 0 — Feasibility spike**
- Install the HyperFrames skills and scaffold `video/`. Generate `CLAUDE.md`.
- Render a 20-second test scene at **1080p and 4K** on a GitHub runner. Report time, size and issues.
- Test `yt-dlp` from a runner (blocked or not).
- **Test Opus 5.5:** one structured-output call (no forced tool_choice), one cached 1M-style call (measure cache hit), one image-QA call on a snapshot PNG. Report token cost.

**Phase 1 — Research pipeline (stages 1–3) + issue control flow + verifier loop**

**Phase 2 — Scene template library + `/make-composition` + `/visual-qa` skills**

**Phase 3 — Script, voice and full 1080p preview end to end**

**Phase 4 — 4K final, thumbnail critique, packaging, `cost.json`**

**Phase 5 — Evals, Shorts cut, Telugu i18n hooks**

---

## 10. Definition of done (v1)

- [ ] Opening one issue produces a reviewed `analysis.md` and a QA-passed 1080p preview with no manual steps.
- [ ] Two approval comments produce a 4K MP4, thumbnail and YouTube metadata as a Release.
- [ ] Every on-screen claim traces to `analysis.json` → source locator, and passed the `max`-effort verifier.
- [ ] No third-party creator footage. No AI imagery of the product. All media whitelisted and logged.
- [ ] Cost per video is reported and stays under budget.
- [ ] Everything can be run and reviewed from an Android phone.

---

## 11. Ground rules for Claude Code

1. Ask before adding paid services. Report the expected cost per video.
2. Prefer well-maintained tools. Pin versions (including `claude-code-action@v1` and HyperFrames).
3. Each stage writes `stage-N.log.md` to the run folder.
4. Fail soft per source, fail loud per stage.
5. Keep model ID, effort and budgets in config, never in code.
6. Keep the phone-only workflow in mind for every decision.
