# 16-minute breath hold (Telugu documentary), v1

Final: 7:17, 1920×1080, 30 fps, −14 LUFS. Built from the owner's voiceover (`voice/voiceover.mp3`, 7:05).

## Rebuild
```bash
npm ci && python -m venv .venv && .venv/bin/pip install numpy scipy soundfile
# 1. voice + live pauses -> master/voice_paused.wav, master/pause_map.json
.venv/bin/python scripts/mix_master.py runs/breath-hold/voice/voiceover.mp3 runs/breath-hold/transcript/pauses.json runs/breath-hold/master
# 2. subtitles (video time)
.venv/bin/python scripts/make_srt.py tsv runs/breath-hold/transcript/cues_te.json runs/breath-hold/transcript/sentences_{a,b}.tsv
.venv/bin/python scripts/make_srt.py srt runs/breath-hold/transcript/cues_te.json runs/breath-hold/master/pause_map.json runs/breath-hold/deliver/breath_hold_te.srt
# 3. parts (edit video/breathhold/scenes.data.mjs, never the generated p*/index.html)
node video/breathhold/build.mjs && npm run vendor
for p in p1 p2 p3 p4 p5 p6 p7 p8; do (cd video/breathhold/$p && npx hyperframes check && npx hyperframes render --workers 4 --quality standard --output ../../../runs/breath-hold/parts/$p.mp4); done
# 4. music bed + final mix
.venv/bin/python scripts/make_bed.py runs/breath-hold/transcript/bed_cues.json runs/breath-hold/master/bed.wav
scripts/final_mix.sh runs/breath-hold/deliver/breath_hold_te_1080p.mp4 runs/breath-hold/master/voice_paused.wav runs/breath-hold/master/bed.wav runs/breath-hold/parts/p{1..8}.mp4
```

## Files
- `transcript/sentences_*.tsv`: corrected Telugu transcript (Whisper large-v3 + hand correction), voiceover time
- `transcript/pauses.json`: live pauses (02:07 shankha freeze, 06:30 quote, end-screen tail)
- `research/facts.md`: fact check, sources, and which claims are labelled on screen
- `deliver/`: SRT, edit cue sheet, AI prompts, YouTube description, contact sheet
