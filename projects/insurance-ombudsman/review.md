# Review v3: independent review of v2 + native 4K master (2026-10-16)

Fresh-session review of `insurance-ombudsman-preview-v2-1080p.mp4`, shot by shot (`build/review_shots.py`: 3 frames per
shot beside the VO words, sheets in `runs/insurance-ombudsman/review_v2/`), against PLAYBOOK §14 and the owner's v2 notes.
Re-checked on the 4K master: sheets `runs/insurance-ombudsman/review_v3/`, freezedetect (≥ 1.5 s) and blackdetect clean,
−14.3 LUFS integrated, 3840×2160 30 fps, 9:25.

| # | Finding (v2) | Where | Fix (v3) |
|---|---|---|---|
| 1 | Stock clip F08 (signing in a folder) on screen 3 times (rule: max twice) | 1:18, 2:04, 3:14 | 1:18 and 3:14 now show A2's recovery agreement (20% fee line highlighted; "back to the second door" opens door two onto it); F08 stays once |
| 2 | A6's insurer GRO page never seen: the blurred CIO list covered the first 8 s of O030 | 4:44 | A6 plays from the window start (insurer page, GRO email highlighted on "every insurer has to show…"); the CIO list cuts in on "the Ombudsman's website lists…" for 3.6 s |
| 3 | CIO GRO list fully blurred (7.8 s of blur) while the VO says it lists their email addresses | 4:44 | New capture: only officers' names and personal emails blurred; the GRO role addresses stay readable |
| 4 | O029 compose window mostly blank white for 10 s (owner: no blank paper) | 4:33 | The settlement email being answered is quoted under the draft (D1 text) until the body is typed |
| 5 | C1 O039 browser blank white while the URL is typed | 5:52 | New-tab page: shortcuts and recently visited (insurer grievance page, the sent mail, hospital portal), invented |
| 6 | Office directory showed the Ahmedabad centre; the family is in Hyderabad | 6:12 | Recaptured with the Hyderabad centre selected |
| 7 | "FILING IS FREE" over the CIO home page (nothing about fees on it), tagged CIO FAQ | 1:34 | C4's FREE TO FILE beat (complaint with filing fee ₹0) on "costs zero rupees" |
| 8 | "The same rejection letter… again" on a man at a laptop | 2:29 | Episode 01's CASHLESS DENIED letter (FROM EPISODE 1), then the laptop shot as COMPLAINT CLOSED |
| 9 | "10 DAYS = ₹50,000" stayed up while the meter rolled to 12+ days | 8:21 | Label leaves when the drums roll on, 30-day label lands with the drums at 30 |
| 10 | "Next · consumables" on a Pixabay woman in a mask (not Indian, not consumables) | 8:59 | Episode 01's bill, Medicines and consumables ₹1,21,000 line |
| 11 | Hyderabad skyline F14 five times (2 clips + sting, sting, end card) | 1:49, 8:55, 9:15 | Sting and end card on PX04 (Jaipur aerial, owner's India pack) |

Left for the owner (not changed): the Canva people clips IO-1 and IO-5 are the owner's own template picks and show
non-Indian actors; Bombay High Court photos run 23 s as seven framings (the only real visuals of the case).

## 4K pipeline
Native 4K scenes (`video/insurance-ombudsman/render_4k.sh` → `split_4k.py`, the C scenes on a parallel render shard),
Canva templates re-exported at 4K (`tools/make_canva.py`), web captures at 3× (`build/web_full.js`, `web_gro.js`,
`web_hyd.js`), Episode 01 glimpses from its 2160p cut, `build/assemble.py --height 2160`, `build/mix.py --height 2160`.

# Review v2 (owner's notes on v1, 2026-10-15)

Sheets: `runs/insurance-ombudsman/qa4/` (every 2 s). Audio −14.3 LUFS. freezedetect: one 3.7 s hold at 4:40 (A6 O029,
last typed line) → slow push added.

| Owner's note | What changed |
|---|---|
| Real footage not good; court not matching | Classical-columns stock removed; court lines use only the three real Bombay High Court photos; Bima Bharosa "not a court" cuts to its own portal |
| Video calls look like friends chatting | All video-call stock removed; new animated official hearing (C6): Ombudsman with nameplate, complainant R. Kumar, insurer's representative, the three questions on their words |
| No religious persons | PX10/PX11/PX12 (turbans), PX14 (cap), PX13, F12, F05, F19 removed |
| Many blank white papers | Every document now carries readable SIMULATION text: settlement letter/email, agency agreement (20% + GST line), Bima Bharosa ticket and reply, GRO email typed line by line (new A6), complaint, insurer's reply, Rule 16 recommendation, Rule 17 award, review screen, acknowledgement, the five upload documents |
| Use Canva video templates | Owner's three Canva exports: IO-1 clinic helpdesk (cashless denial not the end), IO-2 laptop with the real cioins.co.in grievance page composited on its screen (how to file), IO-3 loading spinner (what happens next), IO-5 doctor with papers, cropped clear of the template's text card (next episode) |

Minor, for the owner: the two Canva people clips are non-Indian actors (no religious markers); "the power of knowing your
rights" uses the Hyderabad street until a template for it is sent.

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
