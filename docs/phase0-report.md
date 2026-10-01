# Phase 0: feasibility spike report

Date: 2026-10-01. Measured locally in a 4-vCPU / 16 GB Linux container (Intel Xeon 2.8 GHz,
software GL, no GPU). This is close to a GitHub `ubuntu-24.04` runner for a public repo (4 vCPU / 16 GB).
The **Phase 0 spike** workflow repeats every measurement on a real runner.

![contact sheet](phase0-contact-sheet.jpg)

## 1. HyperFrames render (20 s test scene, 4 scenes, GSAP, glass/blur, count-ups)

| variant | workers | wall time | × realtime | output | capture path |
|---|---|---|---|---|---|
| 1080p | 1 (auto) | 184 s | 9.2× | 6.0 MB, H.264 High, 1920×1080 | beginframe |
| **1080p** | **4** | **76 s** | **3.8×** | 6.0 MB, H.264 High, 1920×1080 | beginframe |
| **4K native** (3840 canvas + `zoom: 2` stage) | 4 | **260 s** | **13×** | 110 MB, H.264 High, 3840×2160, 46 Mbps | beginframe |
| 4K `--resolution 4k` (supersample) | 4 | 1,086 s | 54× | 110 MB, H.264 High, 3840×2160, 46 Mbps | **screenshot** (slow path) |

**Findings**
- **4K works.** HyperFrames does not document 4K, but a native 3840×2160 canvas renders correctly.
- **Never use `--resolution 4k`.** It disables BeginFrame and is 4.2× slower than native 4K.
  Instead, author at 1920×1080 and build the 4K variant with `scripts/make_native_4k.mjs`, which uses a CSS `zoom: 2` stage.
  Text and vectors are laid out at full 4K, so they stay sharp.
- **Always pass `--workers 4`.** The auto setting picked 1 worker, which was 2.4× slower.
- Projection for a **10-minute video**:
  - 1080p preview: about 38 min on one runner.
  - 4K final: about 2 h 10 min on one runner. This is under the 6-hour job limit, but a scene-split matrix
    (e.g. 6 shards of about 25 min, then an FFmpeg concat) brings it to about 30 min. Recommendation: **runner matrix (option a)**, no VPS needed for rendering.
- Cost drivers: the large `filter: blur()` glows and `backdrop-filter` dominate software-GL capture time. Phase 2 templates
  should pre-render the background glows to a static image or video layer.
- ⚠️ **File size vs GitHub Release limit.** At 45 Mbps, 4K comes to about 330 MB per minute, so a 10-minute video is about 3.3 GB.
  Release assets are capped at 2 GiB per file. Options for Phase 4: (a) cap at about 20 Mbps, so 12 min is about 1.8 GB
  (YouTube re-encodes everything anyway, and flat motion graphics compress well); (b) CRF-based encoding with a max-rate cap;
  (c) split the asset into parts. **Owner decision needed.** Recommendation: (a), checked visually in Phase 4.
- Lint warns that scenes should be sub-compositions (`data-composition-src`). This matches the Phase 2 template library design.

## 2. yt-dlp transcripts

From this container's datacenter IP: **1 of 2 videos returned subtitles, and the other got HTTP 429 (Too Many Requests).**
Rate-limiting is already happening at very low volume. With 15–25 sources per phone, expect frequent 429s from GitHub runners.
- The workflow measures this on a real runner (`ytdlp` job).
- Current yt-dlp needs a JS runtime for YouTube. The scripts pass `--js-runtimes node`.
- Plan for Phase 1: try the runner first, then the VPS self-hosted runner (residential or less-flagged IP), then mark the source
  `unavailable`, as the handoff specifies. The YouTube Data API `captions.download` endpoint only works for videos you own,
  so it is not an option.

## 3. Opus 5.5 API (`pipeline/spike/opus_spike.py`)

Not run locally (no API key in the build container). The workflow runs it once the `ANTHROPIC_API_KEY` secret is set.
The code path was tested end to end against a mocked client. It sends no `thinking` and no `tool_choice`,
takes effort from config, and enables server-side refusal fallback.

Tests:
1. **Structured output** via `output_config.format` (JSON schema from Pydantic via `transform_schema`), validated with Pydantic.
2. **Caching** a synthetic source bundle (default 150K tokens; set `bundle_tokens=900000` for a near-1M test, about $7.50) placed in
   `system` with a 1-hour TTL. Calls: write, then read at the same effort, then **read at a different effort**.
   The last one decides whether synthesis (`xhigh`), verify (`max`) and script (`high`) can share one cached prefix.
   Per the API docs, effort changes always invalidate the *messages* cache, and on some models also the *system* cache.
3. **Image QA** of a rendered frame, returning a structured PASS/FAIL with issues.

Expected cost of the default run: about $1.30–2.50 (1h cache write of 150K tokens is $1.20; reads cost $0.03 each).

## Known gaps carried into Phase 1
- `cost.py` prices every reply at the Opus rate. A reply served by the refusal fallback model should use that model's rate
  (`usage.iterations`).
- `config/sources.yaml` holds placeholders. **Owner: fill in the whitelisted channels, sites and press domains.**
