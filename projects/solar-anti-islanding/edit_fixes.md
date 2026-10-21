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
