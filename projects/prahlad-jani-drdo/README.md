# Prahlad Jani & DRDO: the 70-year food and water mystery (Telugu documentary)

Follows `docs/documentary-production.md`. Source brief: the owner's handoff PDF.
VO **v2**: three ElevenLabs Telugu (Bunty) takes joined into `assets/voiceover.mp3`, 6:08.6, mono 44.1 kHz
(lead-in silence trimmed, levels matched, ~0.6 s natural gaps at the joins).

**Length is not locked to the VO.** Programme = VO + breaks: 6:14 as is, **6:46 with all three live clips**
(each clip's real length decides the final length).

| File | What it is |
|---|---|
| `asset-manifest.md` | **Step 1.** Assets with exact file names and search queries; fact-check notes |
| `edl.csv` / `edl.md` | **Step 2.** 121 shots + 2 VO pauses + 3 **LIVE clips** (original video plays with its own audio, then the VO continues) |
| `assemble.py` | **Step 3.** FFmpeg assembler: 3-layer frames, Ken Burns, live clips, VO/BGM/SFX mix at −14 LUFS |
| `subtitles.te.srt` | Telugu subtitles on **VO timing** (124 cues) |
| `subtitles.te.programme.srt` | Same on **final-video timing**. **Rebuild after downloading the live clips, then upload this one to YouTube** |
| `phrases.v2.tsv` → `transcript.te.tsv` | Hand-corrected text → word-aligned timings (`tools/align_phrases.py`); `[?]` = verify by ear |
| `3d-prompts.md` | Runway/Sora prompts with output file names and the EDL shots that use them |
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
Missing assets render as a moving "MISSING <file>" placeholder, so you can preview at any stage. A LIVE clip
marked `optional` is simply left out until its file is in `assets/` (no dead air).

### Live clips (original video + its own audio)
In `edl.csv`, a `LIVE` row stops the VO at `vo_at`, plays `asset` from `src_in` to `src_out` with its own sound,
then the VO resumes where it stopped. To place a clip: download it, watch it, and set `src_in`/`src_out` to the
seconds you want (any length). Put a Telugu translation in `subtitle` if the clip is in English or Hindi. Then:
```bash
python3 tools/build_srt.py --offset-map   # re-time subtitles around the clips
python3 tools/edl_md.py                   # refresh the table
python3 assemble.py
```
Add a new clip by adding a row (`type=LIVE`, `block=LIVE`, `motion=none`). Pick `vo_at` inside a pause in the VO
(`transcript.te.tsv` shows where sentences end).

Regenerate after text edits: `python3 tools/align_phrases.py phrases.v2.tsv <asr.json> transcript.te.tsv`, then the
two `build_srt.py` commands.

## Notes (read these)
1. **Live-clip slots:** (1) after the 70-year claim, the 2010 news report (then "ఈ విషయం worldwide viral…");
   (2) after "DRDO scientists official press meet పెట్టి…", the **real** Dr. Shah / DIPAS press-conference audio;
   (3) optional, before the conclusion, a real skeptic interview for balance. VO pauses: after the sealed-room lock
   (door latch) and after "biggest shock ఏంటో తెలుసా?" (heartbeat).
2. **v2 fixed** the DRDO name and now says "నిజమో కాదో తేల్చడానికి" (to test whether it's true), which is better.
3. **Accuracy (`asset-manifest.md` §D):** two VO lines go beyond the record. DRDO never issued an official verdict that
   it was "an absolute biological wonder"; the study was never peer reviewed and DIPAS said more study was needed.
   "Bladder walls reabsorb urine" was the doctors' hypothesis. And "a perfect proof" overstates it. The EDL shows
   "DOCTORS' HYPOTHESIS" and "ILLUSTRATION" tags; LIVE clip 2 lets viewers hear what was actually said; LIVE clip 3
   adds the skeptic view. Consider softening those two lines in a v3 take, which would also lower the risk under
   YouTube's medical-misinformation policy.
4. **End screen:** the last ~20 s are calm B-roll with no text so YouTube end-screen elements fit.
