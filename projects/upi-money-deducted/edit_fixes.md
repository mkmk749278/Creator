# Film 01 · Edit-room fixes on the recorded VO (from `review_audio_v1.md`)

The recording runs at about 172 wpm with flat 0.4–0.5 s pauses. We don't re-record: we cut the VO at its own
pauses and insert room tone so the key beats land. Times are the original file's (`voice/upi01_full_v16.mp3`,
`align/slots.csv`); find the exact cut point at the nearest silence on each word with `silencedetect` before
inserting. Total added ≈ 12 s → runtime ≈ 4:12. Re-time `screenplay.md` and every `script.tsv` cue after this.

| # | Line | Where | Add | Why |
|---|---|---|---|---|
| 1 | 6 | after "every phone call in India..." | +0.6 s | let the joke land |
| 2 | 6 | end of line 6 | +0.7 s | set up the three outcomes |
| 3 | 9 | before "So if it says failed" | +0.6 s | the pay-again permission |
| 4 | 9 | after "Simple so far, right?" | +0.8 s | checkpoint, then the troublemaker |
| 5 | 14 | before "So where is your money right now?" | +1.0 s, music silent 1.5 s | core reveal (charter: silence before the reveal) |
| 6 | 14 | after "right now?" | +0.7 s | question beat |
| 7 | 18 | after "Back by the next day." | +0.5 s | number 1 |
| 8 | 18 | after "Within five days" | +0.5 s | number 2 |
| 9 | 18 | before "Person, one day." | +0.8 s | the recap punch |
| 10 | 19 | before "one hundred rupees" | +0.6 s | the most-missed number |
| 11 | 19 | after "every extra day." | +0.8 s | let it sink in |
| 12 | 21 | after "My one rule:" | +0.8 s | the rule |
| 13 | 21 | before "twice." | to a 1.0 s gap total | the punchline |
| 14 | 21 | after "twice." | +0.8 s | the laugh |

Optional slow-down on line 19 only: `atempo=0.94` (pitch-safe) if it still sounds rushed after the pauses.

**Picture fixes:** a speech-bubble label YOU SAY over line 13's quoted lines (fixes "comes back to me" without a
re-record); burned-in captions with every number bold; the ₹100 / DAY counter stays on through fix 11; at 2:54 a
small "2 MORE TIPS" chip so the summary doesn't read as the end.

**Optional re-record (owner's call):** line 13 only, if the speech bubble isn't enough. Text in the reply.
