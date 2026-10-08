# The $10 Billion Chip Gamble: master documentary build

A ~10.5-minute, 1080p documentary in four HyperFrames parts, each timed word by word to the ElevenLabs "Akash" voiceover.

| Part | Folder | VO | Length |
|---|---|---|---|
| Hook | `hook/` (hand-written) | `00-hook_akash_v4_approved.mp3` | 0:50 |
| Act 1: The Design Paradox | `parts/p1.py` → `p1/` | `01-act1_akash_v4.mp3` | 2:26 |
| Act 2: The Lost Head Start (SCL 1989, cleanroom/water/power) | `parts/p2.py` → `p2/` | `02-act2_akash_v4.mp3` | 2:36 |
| Acts 3 & 4: The New Playbook / The Verdict | `parts/p3.py` → `p3/` | `03-act3-4_akash_v4.mp3` | 4:57 |

## How it works
- `engine.py` turns a part spec into a HyperFrames project. Scenes are keyed to **spoken phrases** (`T("Enter Tata Electronics")`),
  resolved against word timestamps (`episodes/.../audio/*.words.json`, faster-whisper), so cuts land on the words.
- Scene kinds:
  - Real photos (Ken Burns, archival grades, **2.5D parallax** from local subject cutouts) and real footage (auto slow-motion to fill scenes)
  - A shared **Natural Earth world map** with camera moves, country highlights, pins and drawn routes with moving packets
  - **Real government documents** (ISM/PIB PDFs rendered with pdftoppm) with a 2.5D desk camera, highlighter swipes on the exact words (`pdftotext -bbox`) and ink stamps
  - Data overlays: count-up stats, the investment tracker, the yield dial (80% → 20%), a log-scale nanometre comparison, bar chart, donut, timeline, particle comparison, voltage waveform and water counter
- Every real asset is credited bottom-right while it is on screen. `credits.py` writes `episodes/.../06-full-credits.md`.

## Rebuild from the repo
```bash
npm ci                                                    # HyperFrames + vendored GSAP/Inter
pip install faster-whisper                                # only to regenerate word timings
python3 tools/dlb.py assets tools/commons_images.json     # Commons photos (1920px thumbs; slow, rate-limited)
# footage: download the three Commons films (see 06-full-credits.md), then cut with cuts.txt
./parallax.sh si26_30 intel1981 bunny_suit morris_chang   # 2.5D cutouts (local model)
for p in p1 p2 p3; do python3 parts/$p.py; done && node ../../scripts/vendor-assets.mjs
for p in p1 p2 p3; do (cd $p && npx hyperframes check); done
./render_part.sh p1 && ./render_part.sh p2 && ./render_part.sh p3   # + hook: cd hook && npx hyperframes render ...
./concat.sh                                               # -> renders/chip-gamble-master-1080p.mp4 (-14 LUFS)
```
Government photos and PDFs come from ism.gov.in (SEMICON India gallery, press-release PDFs). The paths are in `tools/` and the credits file.
