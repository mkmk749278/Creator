# Review: The Insurance Ombudsman, 1080p preview

Cut: `projects/insurance-ombudsman/assets/insurance-ombudsman-preview-1080p.mp4` (9:25, 118 shots, mean 4.8 s;
animated scenes carry their own internal motion). Sheets: `runs/insurance-ombudsman/qa/` (v1) and `qa2/` (v2), one tile
every 2 s, reviewed tile by tile against `edl.md` and `timing.csv` (PLAYBOOK §14). Audio: −14.3 LUFS integrated.

## Blockers (all fixed)
| Issue | Where | Fix |
|---|---|---|
| Picture frozen from 5:13 to the end on one clock frame | v1, shot 71 (B2 O034) on | A render cut off by a session restart left a shot with no moov atom; concat froze on it. Broken files deleted; shots now render to a temp name and are renamed when complete (`build/assemble.py`) |
| Labels with `%` rendered blank ("20% OR MORE OF YOUR MONEY", the Bima Bharosa 63% source tag, "NO 20% FEES") | 1:19, 2:13, 8:51 | `expansion=none` on drawtext; cache key versioned so the old renders are redone |

## Major (all fixed)
| Issue | Where | Fix |
|---|---|---|
| Our lower thirds doubled Episode 01's burned-in ones on the glimpses ("9 PM · BILLING COUNTER ER") | 0:00–0:37 | Glimpses keep Episode 01's own label; only a top-left `FROM EPISODE 1` tag |
| CASHLESS DENIED glimpse held still 4.4 s (freezedetect) | 0:08.8 | Slow push-in across every glimpse slot |
| Episode 01 thumbnail headline cropped by the push-in | 0:15 | Push reduced to 1.0 → 1.06 |
| "GRO details" showed the wrong part of the CIO home page | 4:45 | Real CIO "Grievance Redressal Officers" list (cioins.co.in/GRONonLife); officers' names and emails blurred |
| Closing sting and end card used the shared banner reading "TELUGU · ENGLISH" | 8:55, 9:15 | English channel banner from Drive `English/_Channel` |
| O036 (₹50 lakh raised in Nov 2023) was a web still | 5:32 | Session C's magnifier on the real Gazette G.S.R. 828(E) footnote |

## Minor (left as is, for the owner's eye)
- 4:21: the 1,715 counter counts up and passes through smaller numbers for about a second before it lands.
- 6:13: the CIO office directory shows the Ahmedabad Ombudsman's name (a public office holder on the official page).
- 6:53 and 8:49: the smiling couple (PX10) is a soft fit for "What happens next?"
- 9:11: "What the price rules say" sits on a non-Indian doctor writing (F19); an Indian bill close-up would be better.
- Sources of stand-ins: several Pexels people are generic; all carry ILLUSTRATIVE FOOTAGE / ILLUSTRATIVE HEARING.

## Checked and fine
Semantic lock line by line; every on-screen number matches the VO and `claims.csv` (₹4,50,000 / ₹1,20,000 / ₹3,30,000;
₹66,000 + 18% GST (assumed) = ₹77,880; 14 days; 1 month; 1 year; ₹50 lakh; 1,715; 18 offices; PDF/JPG 10 MB; ≈ 1 in 3;
8 in 10 closed cases under 3 months; 30 days from receipt; ₹5,000/day, not if challenged in 30 days; 10 days = ₹50,000;
30 days = ₹1,50,000; Dedhia: award + interest + ₹1 lakh costs, recovered from officers after an inquiry). Every stand-in
is tagged; no real insurer, hospital or person is shown as a party; no clip used more than twice; logo bug throughout,
sting on the channel name, end card last; STEP 4 / FREE on screen by 0:30 (glimpse g7 and the O002 staircase).
