# Asset manifest (sourcing pass 1, 2026-10-28)

Files live in `assets/` (gitignored); every kept file has a row in `media_manifest.csv`. Contact sheets: `qa/sheet-0N.jpg`
(stock), `qa/wellcome/`, `qa/docs/`.

## Have (real or licence-clean)
| Beat (screenplay) | Asset | Kind |
|---|---|---|
| 0:36 the 3 March 2020 order, magnifier on PARACETAMOL | `docs/dgft_2020_noti50-1.jpg` (signed DGFT scan) | R |
| 1:04 "reports at the time said" | `docs/tribune_2020.png` | R (credited crop) |
| 2:50 86 of every 100 rupees | `docs/niti_p-40.jpg` (table: antibiotics, China 86.1%), `niti_cover-01.jpg` | R |
| 2:26 Indian companies world class at the last part | `stock/pixabay_45675`, `45677`, `45680`, `45682` (capsule line, clean room) | S: generic pharma line, not labelled as any Indian plant |
| 0:00 capsule macro | `stock/pixabay_40948` | S |
| 4:29 the mould | `wellcome/B0004595`, `B0004843`, `B0004848` (SEM *Penicillium*, CC BY) | R |
| 3:36 miracle drug of that time | `wellcome/L0012314` (1940s penicillin potency tubes) | R |
| 4:29 "green patches on old bread" | `stock/pixabay_42166`, `23769` (mould on fruit; no bread clip yet) | S, stand-in |
| 6:42, 8:07 imports at the port | `stock/pixabay_23008`, `23215`, `216619` | S |
| 4:19 cooked from chemicals (lab) | `stock/pixabay_197486`, `262189`, `76395` | S |
| 8:14 the 29 Jan 2026 floor price, magnifier on ₹2,216/kg | `docs/dgft_2026_mip-1.jpg` | R |
| 7:37 Kakinada plant (document) | `docs/aurobindo_lyfius_2024-2.jpg` (filing: Lyfius Penicillin-G facility) | R |
| 6:30 roll-call context (optional) | `docs/dgtr_peng-01.jpg` (2010 DGTR finding: Alembic + SPIC were all of India's Pen-G) | R |

Rejected on the contact sheet: Pixabay 127101 and 289881 (cartoons), 5448, 54756, 55712, 55713, 57049 (3D renders),
38220 (a glass of water), 94003 (water wheel, not a chakki).

## Still needed
| Beat | Need | Plan |
|---|---|---|
| 7:37–8:06 Kakinada plant | real footage or photos of the Lyfius plant | **owner fetch** (YouTube 403 from the cloud), below |
| 3:27–3:54 Pimpri 1954–56 | Hindustan Antibiotics archive photos | Commons (rate-limited today, 429): retry; Nehru Archive page; else the ABP Majha clip of the Pimpri site (owner fetch) |
| 5:25 flour mill, chakki | real Indian chakki footage | **owner fetch** |
| 1:48 Cipla, a dollar a day | document crop | MSF 2001 report PDF (claims P16, government-free but credited) instead of a NYT page |
| 6:12 1991, the year India opened up | budget speech or front page | indiabudget.gov.in PDF blocked to curl: retry with Playwright |
| 7:20 the scheme | PIB/DoP page | PIB blocks the cloud: use the DoP annual report PDF (claims P29) |
| 8:38 Sept 2026 anti-dumping case | DGTR initiation notice | find the 2026 notice URL (claims P58 links the 2010 finding) |
| 0:51 a pharmacy shutter | ILLUSTRATIVE FOOTAGE | Pixabay had none; build in HyperFrames or owner phone clip |
| 1:14, 10:04 a pharmacist stocking a shelf | Indian chemist shop | Pixabay had only cartoons; owner phone clip of a local medical shop (no faces needed) |
| 4:29, 4:38, 7:58 fermenter | 3D cutaway | Blender hero shot (no real Kakinada interior available), labelled ILLUSTRATION |

## Owner fetch (phone, Termux, one command into Drive)
Third-party clips, used only as short credited excerpts and only after the contact sheet shows they fit:
```bash
curl -sL https://raw.githubusercontent.com/mkmk749278/Creator/main/scripts/termux_fetch_to_drive.sh | bash -s -- \
  English/pharma-apis \
  "https://www.youtube.com/watch?v=kobsiT9-0uE" \
  "https://www.youtube.com/watch?v=1ddBzBUaa8k" \
  "https://www.youtube.com/watch?v=Wad5rocIq-U" \
  "https://www.youtube.com/watch?v=3aclBlRaYNQ" \
  "https://www.youtube.com/watch?v=keUkhEBY_fs" \
  "https://www.youtube.com/watch?v=ZT2VuADHAFo"
```
| ID | Channel | What we hope it shows |
|---|---|---|
| kobsiT9-0uE | ET Now (1:23) | Aurobindo's Pen-G plant in Andhra |
| 1ddBzBUaa8k | Mamatharamesh (2:00) | Lyfius Pharma, Kakinada, penicillin G project site |
| Wad5rocIq-U | Narendra Modi (10:42) | PM at the 29 Oct 2024 health-projects exhibition (Lyfius was inaugurated that day) |
| 3aclBlRaYNQ | ABP Majha (1:03) | Hindustan Antibiotics, Pimpri |
| keUkhEBY_fs | Amar Agro Industry (0:40) | flour mill plant (atta chakki) |
| ZT2VuADHAFo | Adinath Stones (0:43) | commercial atta chakki |

## Owner's footage, pass 2 (2026-10-28, pulled from Drive `English/pharma-apis/footage/`)
Contact sheets: `qa/footage/<clip>/`.
| Clip | Verdict | Use |
|---|---|---|
| **02 Lyfius corporate film** (1878×1080) | ✅ the find of the pass | 7:37 plant aerials (0:34–0:58), 7:45 fermenter halls (1:02–1:30, "biggest fermenter capacity ever used in India" caption: cover it, we don't claim it), 7:58 vessels and workers (1:14–1:58). Skip the PM still (0:18–0:30). Cover burned-in captions with our lower-thirds |
| **04 ABP Majha, Hindustan Antibiotics** (640×480) | ✅ small | 3:46/6:30: the real HAL gate sign at Pimpri (0:08–0:20), framed small as a document (low resolution) |
| **06 Adinath Stones** | ✅ | 5:25 the small chakki (0:02–0:22) |
| **05 Amar Agro** | ✅ with crop | 5:25 the bigger mill (0:00–0:12), crop the phone number |
| Pexels 3922881 (tablets popped into a palm) | ✅ | 2:36 "the powder you swallow", 10:11 "next time you take an antibiotic" |
| Pexels 13048933 (blister macro) | ✅ | 0:00 opener texture, 2:20 "the strip, the box" |
| 01 ET Now | ❌ studio stock talk, no plant footage (and stock-price graphics: SEBI lane) | — |
| 03 PM exhibition | ❌ an Ayurveda institute exhibition, no Lyfius | — |
| Pexels 8657618 | ❌ Western shop and dollar notes: contradicts an Indian chemist scene | — |

Still open: an Indian chemist counter for 1:14 and 10:04 (owner's phone clip, or a HyperFrames scene); Pimpri archive
photos (Commons, retry); Cipla/MSF, 1991 budget, DoP scheme, DGTR 2026 documents.
