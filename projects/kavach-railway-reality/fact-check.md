# Fact-check: The Kavach Railway Reality

Independent full pass, 2026-10-15, at max effort, on `script.full.tsv` (128 lines). Every factual claim in the `en` VO, every number and date in `onscreen`, and every `cite` tag were checked. The two research dossiers in `brief/` were used only as leads; every row in `claims.csv` points at a source I opened myself. Quotes are verbatim, with whitespace normalised; a builder script checked each one against the downloaded copy.

## In plain words

The script is in good shape. The rollout numbers (2,633 / 1,423 / 1,210 / 7,726 / 6,290 / 21,794 km), the budgets, the cost estimates and both crash accounts (Balasore and Kanchanjunga) match the official records exactly. So do all our own calculations.

Eight lines still block the gate:

- **Two are wrong.**
  - The March 2022 trial used two locomotives, not two trains (K018).
  - The SIL-four line says "one failure in a billion hours" is not what SIL four means (K034). In fact it is the strict end of the SIL-four target. What such videos get wrong is reading it as "Kavach never fails" or "no crashes".
- **Six are unverified.** The cited documents sit on Indian Railways servers (RDSO, ICF, Southern Railway), and those servers reset every connection from this cloud container, including the Wayback Machine and Common Crawl copies. Each one can be confirmed in about a minute from the owner's phone, or the line can be swapped for the verified text below. The six are:
  - passive tags
  - two RFID readers
  - the 2-out-of-2 computer
  - the 940 m RDSO test
  - the Vande Bharat 1,250 m rule
  - the 15 km/h mode line

Four more lines pass the gate but still need a wording change:

- the loco count needs its date;
- the Quadrant Future Tek news must be attributed to the company's own exchange filing;
- "the hardest part is not buying boxes" is contested;
- two cite tags name a source that does not contain the fact: K037 and K112.

## Counts by status (85 claims)

| Status | Rows |
|---|---|
| confirmed | 70 |
| claim (attributed or our hedged analysis) | 5 |
| disputed (note filled) | 2 |
| unverified | 6 |
| wrong | 2 |

`python3 scripts/claims_check.py projects/kavach-railway-reality/claims.csv` **fails** on KV-007, KV-009, KV-019, KV-020, KV-022, KV-028, KV-030 and KV-082. These rows are left as they are on purpose.

## 1. Required script changes

The replacement text follows the English VO rules: numbers as words, and no digits, rupee sign, exclamation marks, quotes, dashes, brackets or slashes. All of it passed the project's `lint_en` rules.

| Line | Problem | Current text | Replace with |
|---|---|---|---|
| K018 | **Wrong.** PIB 4 Mar 2022: two locomotives, the minister on one and the Railway Board chairman on the other, stopped 380 m apart. | In March twenty twenty two, the Railway Minister rode in a test train in Telangana. Kavach stopped two trains running towards each other on the same line. | In March twenty twenty two, the Railway Minister rode in a railway engine during a Kavach test in Telangana. Kavach stopped two engines running towards each other on the same line, about three hundred and eighty metres apart. |
| K034 | **Wrong.** SIL four is a tolerable hazard rate of 10⁻⁹ to 10⁻⁸ per hour for each safety function, so "a billion hours" is the strict end of it. PIB's own figure was "1 error in 10,000 years". | Some videos say this means one failure in a billion hours. That is not what it means. | Some videos say this means Kavach can fail only once in a billion hours. That is only half the story. |
| K035 | Goes with K034, so the explanation lands. | SIL four is a very strict target for each safety function of the electronics. It is not a promise that no train will ever crash. | SIL four is a very strict limit on dangerous failures, set for each safety function of the electronics. It is a design target, not a promise that no train will ever crash. |
| K069 | **Disputed / dated.** 4,296 diesel + 11,762 electric = 16,058 on 31 Mar 2025. The fleet is bigger now, and the Year Book reportedly gives a higher electric count in another chapter. | And there are about sixteen thousand diesel and electric engines. | And in March twenty twenty five, there were about sixteen thousand diesel and electric engines. |
| K085 | **Disputed.** The Railway Board chair (PTI, June 2024) said suppliers must ramp up production, and PIB (Mar 2025) says more OEMs are needed "to increase capacity". Calling integration "the hardest part" is our opinion. | Still, the hardest part is not buying boxes. It is making them all work together. | And it is not only about buying boxes. They must all be made to work together. |
| K090 | **Claim.** The only source is Quadrant's own NSE/BSE filing of 26 May 2026; no RDSO record. | New companies are trying to join. One of them, Quadrant Future Tek, got permission for passenger trials in May twenty twenty six. That is a step, not final approval. | New companies are trying to join. One of them, Quadrant Future Tek, told the stock exchange in May twenty twenty six that it got permission for passenger trials. That is a step, not final approval. |

## 2. Unverified lines: confirm on the phone, or swap the text

These documents are blocked from the cloud container, but they open from an Indian mobile connection. If the line is there, paste it into the row's `source_quote`, set `status` to `confirmed` and keep the script as written. If not, use the fallback.

| Line | Open this on the phone | Look for | Fallback if not confirmed |
|---|---|---|---|
| K021 (and on-screen PASSIVE TAG) | Southern Railway "Features of Kavach", 17 Apr 2024: `https://sr.indianrailways.gov.in/view_detail.jsp?dcd=15738&did=171332915842384AF68B6FE8285733809E00B5B8F471D&id=0%2C4%2C268&lang=0` | A sentence that the trackside tags are passive or need no power. Only RFID News (trade press, 8 Oct 2026) says so in what I could open. | VO: The reader under the engine reads each tag as it passes over it. On-screen: RFID TAG |
| K031 ("two RFID readers") | RDSO SRS Kavach 4.0 d3: `https://rdso.indianrailways.gov.in/uploads/File/System%20Requirement%20specification%20of%20KAVACH.pdf`, §3.5.1(b) and §4.1.1(c) | Two RFID readers on the loco | VO: Link four is inside the engine. A Kavach computer, RFID readers, speed sensors on the wheels, a screen for the loco pilot, and a link to the brakes. |
| K032 (and on-screen 2-OUT-OF-2) | RDSO Common Type Test Format, Kavach 4.0: `https://rdso.indianrailways.gov.in/uploads/files/08_11_2024-Template%20Common%20Type%20test%20%20Format%20for%20KAVACH%20Version%204_0.pdf`, §5.4.3.3 | A minimum 2-out-of-2 vital architecture | Drop K032 and the 2-OUT-OF-2 tag. K033 still follows. |
| K043, K044, K045 (on-screen RDSO TEST · 2020, 24 LHB + WAP-7 · 130 KM/H, 940 M) | RDSO speed certificate LH/EO/VAR/78: `https://rdso.indianrailways.gov.in/uploads/files/lh-eo-var-78.pdf`, §2.3.1, printed p.3, dated 09 Dec 2020 | 940 m at 130 km/h, full service brake, 24 loaded LHB + one WAP-7, level tangent track. The number is plausible: an average 0.69 m/s². | K043: Here is a real number, from the railway's own training notes. / K044: A Vande Bharat train running at one hundred and thirty kilometres per hour. / K045: Even with its emergency brakes, it needs about six hundred and fifty metres to stop. That is more than half a kilometre. Source: IR Vande Bharat presentation, 654 m from 130 km/h with emergency brake (`https://rskr.irimee.in/sites/default/files/Trainset%20maintenance%20experience%20SSB.pdf`). On-screen: VANDE BHARAT · 130 KM/H, 654 M. Change the visuals too (they show a WAP-7 with an LHB rake and a 940 m ruler). |
| K047 (on-screen VANDE BHARAT · 160 KM/H · < 1,250 M) | ICF MD SPEC-398 (04 Apr 2022): `https://indianrailways.gov.in/railwayboard/rb/tender/1651132598426_4_SpecificationsandStandardsforVandeBharatTrains_TrainsetspecMDspec39804-04-22.pdf`, §2.6.4, printed p.23 | Emergency stop from 160 km/h in less than 1,250 m | Drop K047. |
| K115 (on-screen DEPENDS ON MODE) | RDSO Annexure I, Amdt-6: `https://rdso.indianrailways.gov.in/uploads/Final%20Annexure_I_KAVACH_TOC%20Amdt-6.pdf`, §I.2.11.17 (and Annexure A1 on mode changes) | On Sight speed past a defective signal is set by the operating rules | VO: Some videos say Kavach would always lock the speed at exactly fifteen kilometres per hour. That fifteen is the rule loco pilots follow at failed signals. Kavach enforces the limits its data and settings give it, so do not take that number as a promise. On-screen: DEPENDS ON SET-UP. Sources: the CCRS report via Indian Express, and PIB 6 Feb 2026. |

## 3. Cite-tag fixes

A tag is wrong when the named source does not contain the fact. Tags marked "not opened" point at a blocked document. Keep those only if the owner confirms the text on the phone; otherwise switch to the verified source shown.

| Line | Current tag | Problem | Use |
|---|---|---|---|
| K037 | [PIB \| 23 SEP 2026] | **Wrong source:** that release has no approval date. | [PIB \| 05 AUG 2026] |
| K112 | [CRS \| ABSTRACTS 2024–25] | **Wrong source:** the CRS abstract does not say there was no Kavach. | [RAILWAY BOARD \| JUN 2024 · LOK SABHA \| AUG 2024] |
| K098 | [MINISTRY OF RAILWAYS] | Vague | [RAJYA SABHA \| JUL 2023] (295 deaths) |
| K015 | [RDSO \| SPN/196/2020] | Not opened | [PIB \| FEB 2026] |
| K016 | [RDSO \| CAMTECH HANDBOOK 2023] | Not opened | [DT NEXT \| APR 2026] |
| K017 | [RDSO \| SPN/196/2020] | Not opened | [PIB \| 05 AUG 2026] |
| K020 | [SOUTHERN RAILWAY \| 2024] | Not opened | [RDSO \| TAN 2025] |
| K022 | [RDSO \| ANNEXURE D] | Seen only in the search index | Keep if confirmed, else [PIB \| FEB 2026] |
| K024 | [RDSO \| ANNEXURE H AMDT 5] | Not opened. The 1,000 m maximum is in RDSO TAN v3.0 (12 Mar 2025), clause 2.4. | [RDSO \| TAN 2025] |
| K026, K027, K101 | [RDSO \| ANNEXURE I] | Not opened | [PIB \| FEB 2026] |
| K028 | [CAMTECH \| 2023] | Not opened | [PIB \| DEC 2024] |
| K029 | [RDSO \| ANNEXURE C] | Not opened | [PIB \| FEB 2026] |
| K031 | [RDSO \| SRS 4.0] | Not opened | [IEI \| SEP 2024] |
| K042 | [CAMTECH \| 2023] | Not opened | [IRIMEE \| AIR BRAKE NOTES] |
| K059, K060 | [RDSO \| SRS 4.0] | Not opened | [PIB \| FEB 2026] |
| K067, K068, K069 | [IR YEAR BOOK 2024–25] | Not opened. The numbers match CEIC, Dataful and Economic Survey 2025-26. | Keep if confirmed, else [MINISTRY OF RAILWAYS DATA \| MAR 2025] |
| K086 | [RDSO \| FAT SCHEME 2025] | Seen only in the search index | Keep if confirmed, else [PIB \| FEB 2026] |
| K087 | [RDSO \| TYPE TEST 4.0] | Not opened | [RAJYA SABHA \| AUG 2025] |
| K089 | [SCR \| KAVACH OVERVIEW] | Not opened | [PIB \| MAR 2025 · IEI \| SEP 2024] |
| K104 | [IRISET \| HBL 4.0 NOTES 2026] | Not opened | [PIB \| FEB 2026] |
| K114 | [RDSO \| ANNEXURE I] | Not opened | [CRS \| ABSTRACTS 2024–25 · PIB \| FEB 2026] |

All other tags were checked and are right: K010, K018, K025, K030, K033, K035, K038, K062, K063, K070–K073, K075–K077, K079–K083, K090, K093–K097, K106–K111 and K116.

## 4. On-screen text fixes

- K069: `≈ 16,000 LOCOS` → `≈ 16,000 LOCOS · MAR 2025`
- Only if the phone checks in section 2 fail: K021 `PASSIVE TAG` → `RFID TAG`; drop K032 `2-OUT-OF-2`; K043–K045 per the Vande Bharat fallback; drop K047; K115 `DEPENDS ON MODE` → `DEPENDS ON SET-UP`.
- Every other number and date on screen matches its source. That covers 2023/2024, MARCH 2022, 96 KM / 2,872 TAGS, MAX GAP 1 KM, 16 JUL 2024, 36 M, ≈ 930 M, ≈ 1,280 M, +50%, ≈ 1.6 S, 208 / 12, 69,439, 1,11,641, 2,633, 1,423 + 1,210, 1,465, UNDER 10%, 7,726, 6,290, 21,794, ₹1,112.57 → ₹1,673.19, ₹3,875, ₹34,700, ₹12,800, 2 JUN 2023, ≈ 128, 17A/B, 17 JUN 2024, T/A 912 ≠ T/D 912, and 78 → ≈ 40.

## 5. Recommended, not required

| Line | Why | Suggested text |
|---|---|---|
| K100 | Balance: asked whether Kavach would have prevented Balasore, the Ministry told the Lok Sabha (7 Aug 2024) "Balasore train accident is not linked with the provision of Kavach." | Here is the honest answer. The railway ministry told Parliament that the Balasore crash was not linked to Kavach. Beyond that, nobody can say yes or no for sure. |
| K072 | 108 km of the 1,465 km moved to version 4.0 on 23 Sep 2026 | An older version was put on about one thousand four hundred and sixty five kilometres in South Central Railway. In September, one hundred and eight kilometres of it were upgraded to the new version. |
| K079 | A newer figure exists: 2026-27 allocation ₹2,066 crore (PIB 5 Aug 2026) | Add: For twenty twenty six twenty seven, it is about two thousand and sixty six crore. |
| K025 | The stretch is Bajwa (Vadodara) to Ahmedabad | …about ninety six kilometres between Vadodara and Ahmedabad… |
| K062 | The CRS quoted the figure; it did not count the cases itself | The Commission of Railway Safety noted two hundred and eight such cases… |
| K012 | We use the CRS abstracts of the inquiry reports, not the full reports | …and the official accident inquiry findings. |

For the description: Balasore deaths were 295 per the Rajya Sabha answer of 21 Jul 2023; some later reports say 296. The Kanchanjunga crash killed 10 (Indian Express, 16 Jul 2024).

## 6. Our calculations, re-run

| Line | Method | Result | VO fair? |
|---|---|---|---|
| K046 | 130 × 0.2777778 (NIST factor) | 36.1 m/s | yes |
| K049 | v = 20.83 m/s; 10 s × v = 208 m; v²/(2 × 0.30) = 723 m | 932 m | yes: "more than nine hundred", labelled ILLUSTRATIVE; real loaded-freight stops can be longer |
| K050 | a = 0.30 − 9.807 × 0.01 = 0.202 m/s²; 1,075 + 208 m | 1,283 m | yes: "almost one thousand three hundred" |
| K051 | (160 / 130)² | 1.515, i.e. +51.5% (about +47% with a fixed delay) | yes: "about half" |
| K055 | 50 / 30.56 | 1.64 s | yes |
| K025 | 2,872 / 96 | 29.9 tags per km | yes |
| K073 | (2,633 + 1,465) / 69,439 | 5.9% | yes: "well under a tenth"; no double count at 31 Jul 2026 |
| K082 | 69,439 × 0.5 crore | ₹34,719.5 crore | yes |
| K083 | 16,000 × 0.8 crore (16,058 × 0.8 = 12,846) | ₹12,800 crore | yes |

## Access notes

- **Blocked from this container:** every `*.indianrailways.gov.in` host (RDSO, ICF/Railway Board, SR, SCR, SECR) and `iriset.railnet.gov.in` reset the TLS handshake, and WebFetch got a 503. `web.archive.org` also resets; it holds copies of the ICF spec, the SCR overview and the SRS, but they could not be fetched. Common Crawl has no copies. `eparlib.nic.in`, `english.udayavani.com` and `archive.pib.gov.in` were refused, and I did not route around any of these.
- **Search-index text:** two RDSO quotes, the TAN v3.0 lines in KV-008 and KV-012, come from the search engine's index of the official PDF. The Annexure D and FAT titles came the same way. This is flagged in each note.
- **Main primary sources opened:**
  - CRS Abstracts 2024-25 (crs.gov.in)
  - PIB PRIDs 2294805, 2313758, 2227687, 2112824, 2209720, 1802968 and 2082712, plus PIB explainer note 157230
  - Rajya Sabha USQ 1555 (2025), 311 and 270 (2023); Lok Sabha USQ 2597 (2024)
  - NSE filing (Quadrant)
  - IEI UP Centre Kavach presentation (Sep 2024)
  - IRIMEE brake and Vande Bharat notes
  - Economic Survey 2025-26 table 1.26; CEIC
  - BSI EN 50129 page; WCRR 2001 SIL paper; NIST SP 811

## 5. Applied in script v1.1 (2026-10-15)

All required changes above were applied: K018, K034/K035, K069 (dated), K085 (softened), K090 (attributed), and the
fallbacks for every unverified line: K021 (no "no battery" claim), K031 (no reader count), K032 and K047 dropped,
K043–K045 now use the verified Vande Bharat figure (654 m from 130 km/h, emergency brake; IRIMEE slide opened and read
by the writer), K115 fallback wording. All cite-tag fixes in section 3 applied. Recommended items applied: K025
(Vadodara–Ahmedabad), K062 ("noted"), K012 ("inquiry findings"). Not applied (owner's call, would lengthen the film):
K100 ministry position, K072 108 km upgrade line, K079 2026-27 allocation. Rows KV-019, KV-020, KV-030 removed with
their lines. Gate: 82 claims, 76 confirmed, 5 claim, 1 disputed; passes.

If the owner opens the blocked RDSO PDFs on the phone and confirms them, these can come back: the 940 m LHB certificate
(stronger anchor for a 24-coach train), two RFID readers, 2-out-of-2, passive tags, Vande Bharat < 1,250 m from 160.
