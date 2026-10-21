# Edit-room fixes on VO v10 take 1 (from `review_audio_v1.md`)

Source: `voice/vo_v10_take1.mp3`. Times are from `align/align.json`. Find each cut at the nearest silence (`silencedetect`
d=0.15) and insert room tone, not digital silence. Swap in the re-generated lines first, then add the pauses, then
re-run `align_script.py` and re-time `screenplay.md`.

**Re-generated lines (owner):** 3+4 as one clip, 15 alone, 22 alone. Same voice and settings, speed 0.85.
Splice each at its silence boundaries: 3+4 = 0:15.19–0:28.82, 15 = 1:57.65–2:00.35 (check the 14/15 boundary by ear),
22 = 2:53.20–3:00.30.

| # | Line | Where | Add | Why |
|---|---|---|---|---|
| 1 | 3 | after line 3 | 1.0 s | end of the hook |
| 2 | 4 | after "you keep at home." | 0.5 s | NOT this box |
| 3 | 4 | after "on-grid inverter." | 0.6 s | the name to remember |
| 4 | 6 | after line 6 | 1.0 s | end of the D.C./A.C. section |
| 5 | 7 | after "as a drummer..." | 0.5 s | let the analogy land |
| 6 | 8 | after line 8 | 1.0 s | normal day ends, the cut comes. Music silent 1.5 s, then the thud |
| 7 | 11 | after "two hundred and thirty volts..." | 0.5 s | first number |
| 8 | 11 | after "eleven thousand volts." | 0.8 s | second number |
| 9 | 11 | after "switched off." | 1.0 s | emotional peak |
| 10 | 12 | after line 12 (first click) | 1.0 s | section break |
| 11 | 14 | after "is the drummer still there?" | 0.6 s | question beat before the reveal |
| 12 | 15 | after "back in line." | 0.5 s | pairs with line 16 |
| 13 | 16 | after line 16 (second click) | 1.0 s | section break |
| 14 | 18 | after line 18 | 1.0 s | panels → fix |
| 15 | 22 | before line 22 | 0.7 s | the warning |
| 16 | 22 | after "just say no." | 0.6 s | let it sink in |
| 17 | 23 | before "Your solar never failed" | 0.6 s | closing line |

About 14 s in total, which makes the runtime about 3:30 with the re-generated lines. Picture notes are in `review_audio_v1.md`.

## Done (2026-10-21)
`tools/assemble_vo.py` builds `voice/vo_v10_edit.wav` / `.mp3` (gitignored) from take 1 plus `fix_03_04.mp3`, `fix_15.mp3`
and `fix_22.mp3` (re-generated at speed 0.85). It adds all 17 pauses as above. Every cut sits at the midpoint of a measured pause.
- **Result:** 3:28.4 (take 1 was 3:11.3), about 161 wpm including pauses, −22.8 LUFS, −1.0 dB peak (to be mastered to −14 LUFS in the mix).
- **Line timings:** `align_edit/lines_exact.json`, mapped through the cut list. It replaces an aligner pass on the edit, because the aligner read the new 0.6 s pause inside line 4 as a line end.
- Re-generated lines 3+4 now read at 198 and 171 wpm (were 217 and 235), and line 22 at 170 wpm (was 203).
- Line 15 read at 220 wpm even after re-generation, so it has `atempo=0.9` (pitch-safe), giving 198 wpm. If it sounds stretched, set `T15 = 1.0`.
- `fix_22.mp3` starts with "If" at 0.04–0.12 s, followed by a 0.2 s gap before "anyone". The cut starts at 0 s so the word is kept.
- **Check by ear:** the three splice points (0:15, 0:33, 2:08, 3:08), line 15's tempo, and the room-tone joins.

## Take 2: the owner re-recorded the full VO (2026-10-21)
Source `voice/vo_v10_full_take2.mp3`: 3:12, about 174 wpm, so the speed setting didn't slow the full take. All 24 lines
align; lines 9–11 were flagged, but their speech-to-text ratios are 0.90–1.02. `tools/edit_take.py` applies the same 17 pauses.
Inner pauses are found by phrase, using silencedetect d=0.10, because the pause after "thirty volts..." is only 0.14 s. The tool also:
- slows line 3 to ×0.92 (217 → 200 wpm);
- swaps line 15 for `fix_15.mp3` at ×0.9 (198 wpm; both full takes read it at about 260).

**Result:** `voice/vo_v10_take2_edit.mp3`, 3:26.4, about 162 wpm, −22.8 LUFS. Exact line times are in `align_take2/edit_lines_exact.json`.
**This edit replaces the take 1 edit.**
