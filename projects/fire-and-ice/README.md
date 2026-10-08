# Fire and ice (working title)

Telugu documentary on Tummo meditation (Himalayan monks studied by Harvard scientists) and Wim Hof: how the body makes heat
in freezing cold. Status: hook VO (ElevenLabs v4, 1:35) timed to the script; not fact-checked yet.

- `script.tsv`: the owner's script, one spoken line per row, Telugu + English translation (faithful, not corrected).
- `voice/hook_v4.mp3`: hook voiceover.
- `align/`: line timings (`align.json`), `subtitles.te.srt`, `subtitles.en.srt`, `align.md`.

Rebuild: `python3 scripts/align_script.py projects/fire-and-ice/voice/hook_v4.mp3 projects/fire-and-ice/script.tsv --out projects/fire-and-ice/align`
