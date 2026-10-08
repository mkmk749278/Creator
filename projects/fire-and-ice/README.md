# Fire and Ice: the science of Tummo and Wim Hof (Telugu documentary)

Telugu science documentary for *Be Practical with Kishore*: Tibetan Tummo ("inner fire") meditation, Herbert Benson's
Harvard tests on Himalayan monks, Wim Hof and the Radboud endotoxin study, and brown fat / non-shivering thermogenesis.
Script by the owner (`script.md`, verbatim); VO in three ElevenLabs v4 takes (voice "Bunty"). Programme ≈ 5:33.

## Genre and look (PLAYBOOK §5.3)
**Science & medical**, with a cold/heat accent pair. Palette: deep navy and graphite, surgical teal, ice blue `#8fdcff`,
ember `#ff7a2f` / flame `#ffb347` (tokens in `video/fireice/_shared/theme.css`). Grades per block in `assemble.py`:
`ICE` (cold open), `EMBER` (Tummo, Himalaya), `STEEL` (Wim Hof, science). Media stack: real Wim Hof footage (VICE 2016,
DW 2021: short credited excerpts), real Radboud endotoxin-test footage (archive in VICE; date not verified, Hof's own test was 2011), Commons photos (Hof in the ice box,
Harvard Medical School, a Tibetan Tummo mural, a Milarepa thangka, a brown-fat PET-CT), Pixabay B-roll (blizzards,
Himalaya, monasteries, fire), and HyperFrames animation (`video/fireice/`): a canvas **thermal-camera figure**
(`_shared/body.js`) for hypothermia, the Benson thermometers, wet sheets, Tummo breathing, brown fat switching on, and
shivering vs non-shivering; SVG cells and mitochondria (UCP1); a borderless map; endotoxin bars. Accents: lower-thirds
on a scrim, minute and temperature counters, honest corner tags (ILLUSTRATION / ILLUSTRATIVE CURVE / RECONSTRUCTION).

## Files
| File | What |
|---|---|
| `script.md` | Owner's script, verbatim |
| `script.p1.tsv`, `.p2.tsv`, `.p3.tsv` | One spoken line per row, Telugu + faithful English (not corrected) |
| `voice/part1_v4.mp3` … `part3_v4.mp3` | VO parts: hook (1:35), Tummo + Harvard (1:35), Wim Hof + brown fat (2:10) |
| `align/p1..p3/` | Line timings, picture slots, te/en SRTs per part (`scripts/align_script.py`, no Whisper) |
| `vo_map.json` | Part offsets in the programme (`tools/build_vo.py`) |
| `claims.csv`, `fact-check.md` | Fact-check gate (`/fact-check`, `scripts/claims_check.py`) |
| `tools/gen_edl.py` → `edl.csv` → `edl.md` | Shot list bound to VO lines (semantic lock; cuts land in pauses) |
| `media_manifest.csv` | Every asset with source and licence (`tools/manifest.py`) |
| `assemble.py` | FFmpeg assembler (3 layers, credits, two-pass −14 LUFS), adapted from Prahlad Jani |
| `subtitles.te.srt`, `subtitles.en.srt` | Programme-timed subtitles (`tools/build_srt.py`) |

## Rebuild (cloud session or VPS: ffmpeg, python3, node)
```bash
cd projects/fire-and-ice
# media (gitignored): see media_manifest.csv; stock via scripts/stock_fetch.py, Commons via the File: titles listed there,
# VICE/DW via .venv/bin/yt-dlp https://www.dailymotion.com/video/x4ly2a2 (and x7zlb64) -> assets/raw/dm_<id>.mp4
python3 tools/build_vo.py                 # assets/voiceover.wav + vo_map.json
python3 tools/make_bed.py                 # music bed + monks ambience
video/fireice/sync_shared.sh && video/fireice/render_all.sh   # (from the repo root) HyperFrames scenes -> assets/hf/
python3 tools/gen_edl.py && python3 tools/edl_md.py && python3 tools/manifest.py
python3 assemble.py --check               # lists anything missing
python3 assemble.py                       # 1080p -> out/preview.mp4 + out/contact_sheet.jpg
python3 tools/build_srt.py                # programme-timed te/en SRTs
```
