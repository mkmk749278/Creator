# Competitor measurements: 18 Telugu videos (2026-10-09)

**Method.** The owner ran `scripts/termux_study_picks.sh` on the phone (mobile IP) for the 18 picks in
`competitor_picks.tsv`: YouTube's Telugu auto-captions with word timings (17 videos), full audio (15) and the first 3 minutes at
360p (17). Study only; nothing is reused in our films. Pace, pauses, sentence length, address forms, talk-markers and CTA
timing come from the caption word timings (ASR text, so spellings are rough, and English words appear in Telugu script).
Loudness, music bed and cut rate come from `scripts/study_opening.py` on the first 180 s. Contact sheets of three openings
were viewed. Limits: 3 videos per channel; ASR mangles some words; scene detection (threshold 0.30) can miss soft cuts;
"wpm" includes pauses.

## Per video
| Channel | Video | Views | Min | wpm | chars/s | pauses ≥0.8 s /min | median words/sentence | greeting at (s) | first CTA (s) | LUFS (0–3 min) | speech − floor (dB) | cuts/min | first cut (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KowshikMaridi | [ikEyiQACJvM](https://www.youtube.com/watch?v=ikEyiQACJvM) | 2,700,000 | 12.6 | 135 | 15.0 | 6.9 | 12.0 | – | 26 | -14.2 | 11.4 | 16.3 | 5.9 |
| KowshikMaridi | [cTI-ojHmlEU](https://www.youtube.com/watch?v=cTI-ojHmlEU) | 592,000 | 14.1 | 139 | 14.9 | 7.6 | 17 | – | 21 | -13.9 | 21.5 | 16.0 | 5.5 |
| KowshikMaridi | [tKOC-Jlrc90](https://www.youtube.com/watch?v=tKOC-Jlrc90) | 234,000 | 15.8 | 141 | 15.8 | 7.9 | 11 | – | 153 | -14.3 | 12.5 | 7.7 | 19.3 |
| MoneyPurse | [P_O5GAmBTOM](https://www.youtube.com/watch?v=P_O5GAmBTOM) | 647,000 | 17.5 | 168 | 18.8 | 4.1 | 17 | 4 | 33 | -8.9 | 22.3 | 9.7 | 2.0 |
| MoneyPurse | [ge-W1iXWfQs](https://www.youtube.com/watch?v=ge-W1iXWfQs) | 535,000 | 15.7 | 167 | 19.7 | 4.0 | 19.0 | – | 22 | -11.8 | 25.9 | 1.7 | 4.4 |
| MoneyPurse | [Lkk3yhbNBkE](https://www.youtube.com/watch?v=Lkk3yhbNBkE) | 9,200 | 18.9 | 179 | 20.9 | 2.2 | 16.0 | – | 322 | -5.3 | 17.2 | 4.0 | 4.0 |
| ThinkDeep | [P-hQglhBIEo](https://www.youtube.com/watch?v=P-hQglhBIEo) | 2,200,000 | 16.2 | 140 | 16.6 | 4.2 | 10.0 | – | 961 | -12.6 | 7.9 | 7.7 | 4.9 |
| ThinkDeep | [Jim1lPVScDI](https://www.youtube.com/watch?v=Jim1lPVScDI) | 1,500,000 | 23.5 | 125 | 15.8 | 7.8 | 8.0 | – | 1399 | – | – | 0.0 | None |
| ThinkDeep | [kw48eN8X7ac](https://www.youtube.com/watch?v=kw48eN8X7ac) | 433 | 8.8 | 133 | 16.2 | 5.7 | 8.5 | – | 516 | -13.4 | 9.8 | 14.7 | 21.2 |
| Vrrajafacts | [sPI12Rxr6Sk](https://www.youtube.com/watch?v=sPI12Rxr6Sk) | 2,000,000 | 18.3 | 174 | 19.6 | 2.7 | 12.0 | – | 37 | – | – | – | – |
| Vrrajafacts | [XjbSmMdl_d4](https://www.youtube.com/watch?v=XjbSmMdl_d4) | 1,100,000 | 17.5 | – | – | – | – | – | – | -18.3 | 12.2 | 16.0 | 10.5 |
| Vrrajafacts | [w2W-vMSjbe0](https://www.youtube.com/watch?v=w2W-vMSjbe0) | 139,000 | 16.5 | – | – | – | – | – | – | -22.1 | 21.9 | 15.3 | 7.6 |
| daytradertelugu | [L5Wvt_-4VWY](https://www.youtube.com/watch?v=L5Wvt_-4VWY) | 1,300,000 | 26.7 | 181 | 20.6 | 1.8 | 13 | – | 141 | -16.5 | 12.8 | 13.7 | 3.4 |
| daytradertelugu | [FemVwIP9Vqk](https://www.youtube.com/watch?v=FemVwIP9Vqk) | 1,100,000 | 26.2 | 195 | 22.8 | 0.7 | 16.0 | – | 78 | -18.7 | 14.1 | 9.3 | 5.8 |
| daytradertelugu | [1TPkHPc0Mc8](https://www.youtube.com/watch?v=1TPkHPc0Mc8) | 195,000 | 32.1 | 173 | 20.0 | 3.5 | 15 | 110 | 64 | -15.1 | 12.8 | 3.3 | 1.6 |
| nbshowtelugu | [MNffEaWs9kE](https://www.youtube.com/watch?v=MNffEaWs9kE) | 1,300,000 | 15.7 | 119 | 14.4 | 12.6 | 9.0 | – | 906 | -14.2 | 30.2 | 16.3 | 3.7 |
| nbshowtelugu | [ZAgOCewk-IM](https://www.youtube.com/watch?v=ZAgOCewk-IM) | 884,000 | 21.5 | 122 | 14.3 | 9.7 | 10 | – | end | -13.2 | 30.3 | 2.0 | 3.6 |
| nbshowtelugu | [cDsM3zCs-no](https://www.youtube.com/watch?v=cDsM3zCs-no) | 37,000 | 17.3 | 119 | 14.0 | 11.4 | 9 | – | 996 | -14.8 | 26.4 | 1.3 | 3.7 |

Reference: Bunty (fire-and-ice takes) ≈ 123 wpm, 14.3 chars/s.

## Findings
1. **Two speeds.** "Talkers": NB Show 119–122 wpm, Think Deep 125–140, Kowshik 135–141. "Rushers": Money Purse 167–179,
   V R Raja 174, Day Trader 173–195. Bunty's pace (≈123 wpm, 14.3 chars/s) matches NB Show (14.0–14.4 chars/s), the
   owner's chosen style model. No speed-up needed.
2. **Pauses.** NB Show leaves 10–13 pauses of 0.8 s or more per minute and its opening has 14–16 detectable pauses/min;
   Kowshik 7–8; the rushers 1–4. Short sentences: median 8–10 words (NB Show, Think Deep), 11–17 (Kowshik), 13–19 (rushers).
3. **Music under the voice.** NB Show is dry: no bed under speech (floor −40 to −43 dB, 26–30 dB below speech). Think Deep
   keeps a continuous bed only 8–10 dB under the voice; Kowshik and Day Trader 11–14 dB. Our spec (bed −24 to −26 dB under
   speech) sits between them.
4. **Loudness.** The hits measure −12.6 to −14.3 LUFS (Kowshik, Think Deep, NB Show): our −14 LUFS master is right. Money
   Purse is far too hot (−5 to −9 LUFS, true peak above 0 dBTP); Day Trader is quiet (−15 to −19).
5. **Cuts.** The two biggest hits in the sample change picture about 16 times a minute (every ~3.7 s: Kowshik 2.7M, NB
   Show 1.3M); Think Deep 7.7/min with slow camera moves inside generated shots. First cut at 2–6 s. Our 2.5–4 s rule is at
   or above the leaders.
6. **Openings (first 30 s).** Nobody opens with a greeting (Money Purse's "Hi guys, welcome" at 4 s is the exception).
   Five patterns: (a) **cold-open story** (NB Show, 1.3M: a politician waits two hours outside a room; "I have only 10
   minutes", says Bill Gates; the politician is revealed as Chandrababu Naidu at ~50 s); (b) **bold claim + stakes** (NB
   Show: "no country has won a war against Israel"; Day Trader: "if one financial expert says this policy is wrong, I'll
   stop talking"); (c) **myth in** (Think Deep, 2.2M: "America proudly said not even a bird could escape this jail. But
   three prisoners…"); (d) **stakes list + promise** (Kowshik, 2.7M: "five big changes from October 1st … SBI account
   holders, bad news; UPI users, bad news … I'll explain pin to pin, watch till the end"); (e) **question chain**
   (Kowshik: "What is no-cost EMI? How does it work? Who gains, who loses? Do you know who loses… us").
   Channel identity: NB Show's name sting at 0:02 (visual); Kowshik says "నేను మీ కౌషిక్ మరిడి" at ~28 s.
   Subscribe asks: Kowshik at 21–26 s, Money Purse 22–33 s, V R Raja 37 s; Think Deep and NB Show only at the end.
7. **Talk glue (per 1,000 words).**

   | Word | Kowshik | Money Purse | Think Deep | V R Raja | Day Trader | NB Show | Our first draft |
   |---|---|---|---|---|---|---|---|
   | కదా | 5.6 | 9.3 | 0.6 | 3.5 | 5.0 | 0.5 | 0 |
   | సో | 10.8 | 10.5 | 0 | 8.8 | 5.2 | 0 | 0 |
   | అంటే | 12.6 | 3.4 | 0.9 | 4.4 | 5.4 | 6.0 | 3.6 |
   | అండి / -ండి | 5.0 | 2.4 | 0.8 | 5.0 | 1.7 | 7.6 | 0.7 |
   | అన్నమాట | 6.5 | 1.7 | 0.2 | 0 | 0.8 | 0 | 0 |
   | ఎందుకంటే | 1.0 | 1.7 | 0.2 | 3.8 | 0.5 | 2.8 | 0.7 |
   | నేను | 2.4 | 1.3 | 2.7 | 0.9 | 6.1 | 1.2 | 0 |
   | తెలుసా | 0.2 | 0 | 0.2 | 0.6 | 0.3 | 1.4 | 1.4 |
   | ఫర్ ఎగ్జాంపుల్ / ఉదాహరణ | 6.1 | 0.2 | 0.2 | 0 | 0.2 | 0.3 | 0 |

   Presenters glue speech with కదా, సో, అంటే, అండి and అన్నమాట; Think Deep (a storyteller narrator) barely uses them and
   writes a more literary Telugu (యొక్క, అభేద్యమైన, ఉత్కంఠభరితమైన) yet still reaches 2.2M on story topics.
8. **Address.** Kowshik and Day Trader say మీరు two to three times as often as మనం; Money Purse the reverse; NB Show mixes;
   Think Deep rarely addresses the viewer. నువ్వు appears only in quoted dialogue.
9. **Devices.** Repetition for a number ("₹10 కాదు, 20 కాదు, ₹69 పెరిగింది", Kowshik); a named everyday example ("XYZ అనే
   పర్సన్ ఉన్నాడు, జీతం 50,000", Kowshik); a mid-video relevance turn ("these changes directly affect you: your career, your
   money, your next city", NB Show); an English line then its Telugu meaning (NB Show: "I have only 10 minutes for this
   meeting… అంటే…").
10. **Endings.** Summary → an opinion question for the comments with concrete options (NB Show: "what do you think? Lokesh,
    Pawan Kalyan or Jagan? Write why, setting your party aside"; Kowshik: "liked it, comment 'liked'; didn't, comment 'didn't'")
    → like/subscribe → "మళ్ళీ కలుద్దాం" → a sign-off: Kowshik, NB Show and Day Trader all end with "జై హింద్".
11. **Visuals (3 contact sheets).** NB Show: presenter in a blazer with a podcast mic keyed over generated scene art that acts
    out the story, full-screen cutaways every few seconds. Kowshik: presenter at a desk, big yellow kinetic captions
    ("OCTOBER 1ST · 5 BIG CHANGES"), real stock cutaways (cylinders, an SBI branch), his channel page as the subscribe
    cue, name super at ~0:30. Think Deep: fully generated cinematic scenes (island prison, a face, case files, a labelled
    map), small labels, logo bug.
