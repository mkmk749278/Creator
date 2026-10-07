# Prahlad Jani & DRDO: the 70-year food and water mystery (Telugu documentary)

Follows `docs/documentary-production.md`. Source brief: the owner's handoff PDF. VO: ElevenLabs Telugu
(Bunty), `Prah_Combined_Voiceover.mp3`, 4:43.96, mono 44.1 kHz.

| File | What it is |
|---|---|
| `asset-manifest.md` | **Step 1.** 38 footage/photo assets + AI shots + audio, with exact file names and search queries; fact-check notes |
| `edl.csv` / `edl.md` | **Step 2.** 91 shots + 3 live-audio pauses, a cut every 2.2–3.6 s, programme 4:51.5 |
| `assemble.py` | **Step 3.** FFmpeg assembler: 3-layer frames, Ken Burns on everything, VO/BGM/SFX mix at −14 LUFS |
| `subtitles.te.srt` | Telugu subtitles on **VO timing** (81 cues + 1 repeated line) |
| `subtitles.te.programme.srt` | Same, on **final-video timing** (pauses inserted, repeat removed). **Upload this one to YouTube** |
| `transcript.te.tsv` | Timed, hand-corrected transcript (source for both SRTs; `[?]` = verify by ear) |
| `3d-prompts.md` | Runway/Sora prompts for the anatomy and sealed-room shots, with output file names |
| `media_manifest.csv`, `credits.md` | Fill in as you download (licence log + YouTube description credits) |

## Make the video (VPS / Termux; needs ffmpeg + python3)
```bash
cd projects/prahlad-jani-drdo
mkdir -p assets && cp /path/to/Prah_Combined_Voiceover.mp3 assets/voiceover.mp3
# download assets with the file names in asset-manifest.md, e.g.
yt-dlp -f "bv*[height<=2160]+ba/b" --merge-output-format mp4 -o assets/jani_news_2010.mp4 "<url>"
python3 assemble.py --check          # what is still missing
python3 assemble.py --only 1-20      # quick section preview -> out/section_1-20.mp4
python3 assemble.py                  # 1080p preview -> out/preview.mp4 + out/contact_sheet.jpg
python3 assemble.py --4k             # 3840x2160 master -> out/master_4k.mp4
```
Missing assets render as a moving "MISSING <file>" placeholder, so you can preview at any stage.
Trim long downloads to the useful part first: the assembler plays each clip from 0 s. For
`press_conf_shah.mp4`, trim to the exact quote, because the 4 s pause plays its first 4 s of audio.

Regenerate after edits: `python3 tools/build_srt.py && python3 tools/build_srt.py --offset-map` (subtitles),
`python3 tools/edl_md.py` (EDL table).

## Changes from the handoff PDF (read these)
1. **Length.** The VO is 4:44, not 8–10 min. It stops mid-sentence at "kidney function, liver parameters,
   brain scans...". The PDF's Block 3 tail (press conference, autophagy, outro, subscribe CTA) is **not in this
   VO**. The EDL covers 0:00–4:51; add part 2 when that VO exists.
2. **Live-audio pauses moved to the real script:** after "sealed room lo lock chesaru" (2.5 s, door latch +
   monitors), at the repeated line "Doctors ki edurina biggest shock..." (3 s, which also removes the duplicate
   take at VO 221.4–223.4 s), and at the end (4 s of the real Dr. Shah press-conference audio).
3. **Mispronounced name in the VO (41 s):** it says "Indian Defence Research Organisation". DRDO is the
   *Defence Research and Development Organisation*. Re-generate that line if you can; the subtitles keep the words as spoken.
4. **Accuracy (`asset-manifest.md` §D):** the study was never peer reviewed, and reports say Jani left the room to
   sunbathe and meet devotees. "Bladder walls reabsorb urine" was the doctors' hypothesis, not established
   science. The EDL tags that segment with an on-screen "DOCTORS' HYPOTHESIS" label and "ILLUSTRATION" on the AI
   shots. I strongly recommend a short skeptic beat and a "don't try dry fasting" note in part 2.
