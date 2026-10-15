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

## v2 check (2026-10-15)

This is a light pass (PLAYBOOK §12) on script v2: `script.full.tsv`, 61 lines, V001–V061, written in the new voice (§4a-4).

- Every remaining row now points at v2 line ids (V…) instead of v1.1 ids (K…).
- Every new or meaningfully changed claim was checked again against its source, opened today; the primary source came first.
- Every quote in `claims.csv` was matched word for word against a copy of its page saved today. Every source behind a new or changed claim was downloaded fresh in this pass. The exceptions are the two RDSO lines read from the search index; they are still flagged, as before.

### In plain words

v2 is in good shape. The facts carried over from v1.1 still match their sources, and the new lines check out:

- **"Designed in India, by Indian engineers and Indian companies" and "Indian-built" are confirmed.**
  - PIB, 4 Mar 2022: "indigenously developed ATP system by Research Design and Standards Organisation (RDSO) in collaboration with Indian industry".
  - IEI deck: "Technology was developed by RDSO and 3 firms of Hyderabad".
  - All India Radio headline: "Indian-Made KAVACH".
- **PIB and the CRS website** are both free to read. CRS lists its accident-inquiry abstracts as free PDFs.
- **Rail Madad:** 139 is the Rail Madad helpline, and it has a security option. The Rail Madad app is live (CRIS, updated 22 Sep 2026).
- **"Suppliers are the other bottleneck"** now says what the Railway Board chair and PIB said. Old row KV-059 moves from disputed to confirmed.
- **Also confirmed:**
  - the minister on board in Telangana;
  - the U-H-F safety radio;
  - warn first, then brake;
  - the budget rising to ₹1,673.19 crore in 2025-26;
  - Quadrant's filing of 26 May 2026.
- **The open loop is kept.** The inquiry findings and the honest answer come in V039–V053.

Two lines must change before the gate can pass:

- **V048 is wrong.** It says trains "were moving ... at a slow, careful speed". The inquiry found that most trains that morning did not keep to that speed. The goods train reached 78 km/h, as V050 itself says.
- **V052 calls the 15 km/h lock "that famous claim".** I found no public post, video or article that makes this claim. It appears only in the owner's own handoff draft.

Eight cite tags need a small fix. Seven edits are recommended but optional.

### Counts (82 claims)

| Status | Rows |
|---|---|
| confirmed | 74 |
| claim (attributed, or our hedged analysis) | 6 |
| unverified | 1 (KV-093) |
| wrong | 1 (KV-092) |

`python3 scripts/claims_check.py projects/kavach-railway-reality/claims.csv` **fails** on KV-092 and KV-093. They are left failing on purpose. After the two VO fixes below:

1. In KV-092, change the claim to the new wording ("trains had to move ... at a slow, careful speed") and set `status` to `confirmed`. The quote already shows the rule.
2. Delete KV-093.

The gate then passes.

### Required VO changes

Both replacements pass `lint_en` and the short-sentence rule.

| Line | Problem | Current text | Replace with |
|---|---|---|---|
| V048 | **Wrong (KV-092).** The CCRS report, via Indian Express of 16 Jul 2024, says the Kanchanjunga Express kept to 15 km/h, "while the other trains in that section, including the goods train involved in the accident, didn’t follow the norm". v1.1 stated the rule; v2 states it as what happened. | Case two. Rangapani, near New Jalpaiguri in north Bengal, June seventeen, twenty twenty four. The automatic signals had failed, so trains were moving on a paper authority, at a slow, careful speed. | Case two. Rangapani, near New Jalpaiguri in north Bengal, June seventeen, twenty twenty four. The automatic signals had failed, so trains had to move on a paper authority, at a slow, careful speed. |
| V052 | **Unverified (KV-093).** No public source says Kavach locks the speed at exactly fifteen; the claim is only in the owner's draft (`brief/owner-handoff.txt`). v1.1 said "Some videos say". Dropping "famous" removes the claim. Or point KV-093 at a real public post that makes it. | And that famous claim that Kavach always locks the speed at exactly fifteen? Fifteen is the rule loco pilots follow at failed signals — what Kavach enforces depends on its data and settings, so don't take that number as a promise. | And what about the claim that Kavach always locks the speed at exactly fifteen? Fifteen is the rule loco pilots follow at failed signals — what Kavach enforces depends on its data and settings, so don't take that number as a promise. |

### Required cite-tag fixes (on-screen text)

A tag must name a source that holds the fact on its line.

| Line | Current tag | Problem | Use |
|---|---|---|---|
| V010 | [PIB \| FEB 2026 · PIB \| 05 AUG 2026] | Neither PIB source mentions a warning stage. "Warns the loco pilot" comes from DT Next, backed by Rail Engineer and Deccan Herald. | [PIB \| FEB 2026 · DT NEXT \| APR 2026] |
| V013 | [RDSO \| TAN 2025 · IEI \| SEP 2024] | No opened source for "knows exactly where it is". PIB says "These tags provide precise train location". | [RDSO \| TAN 2025 · IEI \| SEP 2024 · PIB \| FEB 2026] |
| V017 | [IEI \| SEP 2024] | IEI lists no speed sensors. | [IEI \| SEP 2024 · DT NEXT \| APR 2026] |
| V018 | [PIB \| KAVACH] | No date. | [PIB \| MAR 2022 · IEI \| SEP 2024] |
| V034 | [LOK SABHA \| AUG 2024 · OUR CALCULATION] | That answer gives 1,465 km, but not "version 3.2" or "older version". | [PIB \| 05 AUG 2026 · OUR CALCULATION] |
| V052 | [CCRS VIA INDIAN EXPRESS \| PIB \| FEB 2026] | The first source has no date. | [CCRS VIA INDIAN EXPRESS \| JUL 2024 · PIB \| FEB 2026] |
| V057 | [MINISTRY OF RAILWAYS \| RAIL MADAD] | No date, no document. | [PIB \| MAR 2021 · PIB \| AUG 2025] |
| V058 | [PIB \| KAVACH] | No date. | [PIB \| MAR 2022 · PIB \| FEB 2026] |

All other tags match their lines: V007, V008, V011, V014–V016, V019, V022–V026, V028, V029, V031–V033, V035–V038, V040–V042, V045, V046, V048–V051 and V056.

### Recommended, not required

Every suggested VO text below passes `lint_en`.

| Line | Why | Suggested text |
|---|---|---|
| V002 | Mail and express cabs carry a loco pilot and an assistant loco pilot (the CRS abstracts speak of LP/ALP). "One loco pilot" can read as a lone crew. | Up front, the loco pilot is staring into the dark — watching for a signal that might be red. |
| V007 | We read the inquiries' published abstracts, not the full reports. | Today we'll open the railway's own documents, do the braking maths together, and read what the official accident inquiries found. |
| V029 | v2 dropped v1.1's condition. Kavach brakes when the loco pilot's own braking falls short (PIB 5 Aug 2026: "in case Loco Pilot fails to do so"). PIB's explainer states it without the condition too, so the line passes as it is. | This is where Kavach changes the game. It doesn't wait for anyone to see the red signal — it already knows how far away it is, shows it on the screen inside the cab, and if the loco pilot doesn't slow down, it brakes early while there's still enough room. |
| V035 | "Most headlines" can't be counted. The trade press reported the 2,633 km correctly; the trap is in the numbers themselves. | And here's the trap hiding in the numbers. Track fitted with equipment, seven thousand seven hundred and twenty six kilometres, engines fitted, six thousand two hundred and ninety, and track where work has only started, twenty one thousand seven hundred and ninety four kilometres... but fitted isn't working, and work started isn't protected. |
| V036 | The first figure has no year. The 2026-27 figure is higher still: ₹2,066 crore (PIB 5 Aug 2026). | On screen: 2024-25 ₹1,112.57 CR → 2025-26 ₹1,673.19 CR. VO, optional: The money is moving too — the yearly Kavach budget rose from about one thousand one hundred crore rupees to about one thousand six hundred and seventy crore in twenty twenty five twenty six, and it's about two thousand and sixty six crore this year. |
| V044 | Balance, repeated from v1.1. Asked whether Kavach would have prevented Balasore, the Ministry told the Lok Sabha on 7 Aug 2024: "Balasore train accident is not linked with the provision of Kavach." | Here's the honest answer — the railway ministry told Parliament the Balasore crash was not linked to Kavach, and beyond that, nobody can say yes or no for sure. |
| V052 | The VO never gives the unit. Also, after V048–V050, "follow" reads oddly: most crews that morning did not follow the rule. This builds on the required fix. | And what about the claim that Kavach always locks the speed at exactly fifteen? Fifteen kilometres per hour is the rule loco pilots must follow at failed signals — what Kavach enforces depends on its data and settings, so don't take that number as a promise. |

### Production checks (not VO changes)

- **V008: the open loop.** The film keeps the promise:
  - the inquiry findings come in V042 and V049;
  - the answers come in V044–V047 (Balasore) and V050–V051 (Kanchanjunga).

  The minute still needs a check. The estimator puts V039 at 7:59. At the measured Akash rate (×0.9) it falls near 7:11, before edit pauses. Check it against `align/` after recording. Change "eight" if the payoff starts well before 7:30 or after 8:30.
- **V011 and V012: the trial footage.**
  - PIB's release and the ministry factsheet of 14 Mar 2022 put the 380 m stop in the head-on test.
  - The minister's own tweet, as quoted by The Quint, gives 380 m for a rear-end test.
  - The trial video Odisha Bytes describes shows the red-signal test.

  Under "running towards each other", use a clip that really shows the head-on run.
- **V007: the R-D-S-O cover.** The RDSO installation note (TAN v3.0) is still blocked from the cloud. Download it on the phone before filming its cover. If it shows §2.1 and §2.4, note that KV-008 and KV-012 have been read in full.
- **V018: MADE IN INDIA can stay.** All India Radio's headline of 24 Jul 2024 reads "Indian-Made KAVACH".

### The checks asked for

| Check | Result | Rows |
|---|---|---|
| (a) Designed in India, Indian-built, MADE IN INDIA | Confirmed (PIB 4 Mar 2022, IEI, PIB 6 Feb 2026, All India Radio) | KV-087 |
| (b) V056: PIB releases and the CRS website, free to read | Confirmed (PIB 5 Aug 2026; crs.gov.in abstracts page) | KV-088, KV-089 |
| (c) V057: Rail Madad, 139, app | Confirmed (PIB 8 Mar 2021, 22 Jul 2022, 27 Nov 2024, 8 Aug 2025; All India Radio 22 May 2026; App Store) | KV-090, KV-091 |
| (d) V038: suppliers as a bottleneck; Quadrant in May 2026 | Confirmed (Railway Board chair, PTI 17 Jun 2024; PIB 19 Mar 2025; Lok Sabha 7 Aug 2024). Quadrant is attributed to its filing of 26 May 2026, which gives no permission date. | KV-059, KV-064 |
| (e) V011: minister on board | Confirmed: he rode one of the two engines | KV-006, KV-007 |
| (f) V016: U-H-F safety radio | Confirmed (PIB 6 Feb 2026; Rail Engineer). Logs go over GSM, so "safety radio" is the right word. | KV-016 |
| (g) V008: open loop | Delivered in V039–V053; check the minute after recording | KV-086 |
| (h) V010: warns, then brakes | Confirmed (DT Next, Rail Engineer, Deccan Herald; PIB for the braking); cite-tag fix | KV-004, KV-005 |
| (i) V036: budget rose to about 1,670 crore in 2025-26 | Confirmed (₹1,112.57 crore 2024-25, PIB 19 Mar 2025; ₹1,673.19 crore 2025-26, Rajya Sabha 1 Aug 2025) | KV-053, KV-054 |
| (j) Cite tags on merged lines | Eight fixes, listed above | — |

### Deleted rows (9: the claim is no longer in v2's VO, on-screen text or visuals)

| Row | v1.1 line | Claim |
|---|---|---|
| KV-017 | K030 | Optical fibre cables join the stations |
| KV-024 | K037 | RDSO approved version 4.0 on 16 Jul 2024 |
| KV-025 | K038 | What version 4.0 improved |
| KV-033 | K050 | 1-in-100 falling grade, about 1,280 m |
| KV-043 | K068 | 1,11,641 km of running track |
| KV-055 | K080 | ₹3,875 crore spent up to Jun 2026 |
| KV-056 | K081 | ₹50 lakh per km and ₹80 lakh per loco |
| KV-057 | K082 | About ₹34,700 crore track-side (our maths) |
| KV-058 | K083 | About ₹12,800 crore for locos (our maths) |

### New rows (9)

| Row | Line | Claim | Status | Main source |
|---|---|---|---|---|
| KV-086 | V007 V008 | The promises the film makes (documents, maths, inquiries; the open loop) are kept | confirmed | CRS Abstracts 2024-25 |
| KV-087 | V018 V058 | Designed in India by Indian engineers and companies, for Indian tracks; Indian-built; MADE IN INDIA | confirmed | PIB 4 Mar 2022 |
| KV-088 | V056 | The ministry posts Kavach progress on PIB, free to read | confirmed | PIB 5 Aug 2026 |
| KV-089 | V056 | CRS puts its inquiry findings on its own website, free to read | confirmed | crs.gov.in abstracts page |
| KV-090 | V057 | Report something unsafe to Rail Madad on 139 | confirmed | PIB 8 Mar 2021 |
| KV-091 | V057 | …or through the Rail Madad app | confirmed | PIB 8 Aug 2025 |
| KV-092 | V048 | Trains "were moving ... at a slow, careful speed" | **wrong** | CCRS via Indian Express, 16 Jul 2024 |
| KV-093 | V052 | The 15 km/h lock is "that famous claim" | **unverified** | none found |
| KV-094 | V037 | Money alone doesn't make it work | claim (our analysis) | PIB 5 Aug 2026: "Requisite funds are made available as per the progress of works." |

### Changed claims (quotes checked)

All other kept rows changed wording only: the claim text now follows v2, and the old quote still supports it.

- **KV-059 (V038).** Moves from disputed to confirmed: v2 now says what the source says. The PIB 19 Mar 2025 line is added: "To increase capacity and scale of implementation, trials and approval of more OEMs are at different stages."
- **KV-047 (V034).** The source switches to PIB 5 Aug 2026, which names both version 3.2 and the 1,465 km. Since 23 Sep 2026, 108 km of that runs version 4.0. V034 sums at the end-July date, so nothing is counted twice.
- **KV-004, KV-005 (V010).** These are now one warn-then-brake line. Rail Engineer is added as a third report of the warning.
- **KV-006, KV-007 (V011).** "With the Railway Minister on board" is right.
- **KV-016 (V016) and KV-021 (V019).** Re-worded; still right.
- **KV-037 (V029).** Passes; see the recommended fix.
- **KV-053, KV-054 (V036).** Re-opened; right.
- **KV-062, KV-063, KV-064 (V038).** No official 2026 supplier count exists. A trade report from Mar 2025 says Siemens, Kyosan and Quadrant had approval, but PIB (Mar 2025) and Quadrant's own 2026 filings contradict it, so it is not used.
- **KV-076 (V048) is split.** "Paper authority" stays confirmed; the speed half is now KV-092.

### Remap from v1.1 ids (row: old → new)

KV-001 K010 → V008 · KV-002 K013 K014 K019 → V009 V012 · KV-003 K015 → V010 · KV-004 K016 → V010 · KV-005 K017 → V010 ·
KV-006 K018 → V011 · KV-007 K018 → V011 V012 · KV-008 K020 → V013 · KV-009 K021 → V013 · KV-010 K021 → V013 ·
KV-011 K022 → V013 · KV-012 K023 K024 → V014 · KV-013 K025 → V014 · KV-014 K026 K027 K101 → V015 V045 · KV-015 K028 → V016 ·
KV-016 K029 → V016 · KV-018 K031 → V017 · KV-021 K033 → V019 · KV-022 K034 → V019 · KV-023 K035 → V019 ·
KV-026 K040 K041 → V021 V022 · KV-027 K042 → V022 · KV-028 K043 K044 K045 → V023 · KV-029 K046 → V024 · KV-031 K049 → V025 ·
KV-032 K048 K049 → V025 · KV-034 K051 → V026 · KV-035 K053 K054 K055 → V027 V028 · KV-036 K056 → V028 ·
KV-037 K058 K059 K060 → V029 · KV-038 K061 → V030 · KV-039 K062 → V031 · KV-040 K063 → V031 · KV-041 K064 → V010 V058 ·
KV-042 K067 → V032 · KV-044 K069 → V032 · KV-045 K070 → V033 · KV-046 K071 → V033 · KV-047 K072 → V034 · KV-048 K073 → V034 ·
KV-049 K075 → V035 · KV-050 K076 → V035 · KV-051 K077 → V035 · KV-052 K078 → V035 · KV-053 K079 → V036 · KV-054 K079 → V036 ·
KV-059 K085 → V038 · KV-060 K086 → V037 · KV-061 K087 → V037 · KV-062 K089 → V038 · KV-063 K090 → V038 · KV-064 K090 → V038 ·
KV-065 K093 → V040 · KV-066 K094 → V040 · KV-067 K095 K096 → V040 V041 · KV-068 K097 → V042 · KV-069 K098 → V042 ·
KV-070 K100 K105 → V043 V044 V047 · KV-071 K102 → V045 · KV-072 K036 K102 K103 → V020 V045 V046 · KV-073 K104 → V046 ·
KV-074 K106 → V048 · KV-075 K107 → V048 · KV-076 K108 → V048 · KV-077 K109 → V049 · KV-078 K110 → V049 · KV-079 K111 → V050 ·
KV-080 K112 → V050 · KV-081 K113 K114 → V051 · KV-082 K115 → V052 · KV-083 K116 → V049 · KV-084 K117 K118 → V053 ·
KV-085 K121 K122 → V058.

Lines with no row hold no factual claim: V001–V006 (scene-setting hook), V039, V054, V055 and V059–V061.

### Sources opened in this pass

- **PIB releases (PRIDs):** 2294805, 2313758, 2112824, 2082712, 1802968, 1703201, 1843854, 2078095, 2154388 and 1743174.
- **PIB explainer** note 157230.
- **Ministry of Railways Kavach factsheet,** 14 Mar 2022.
- **CRS:** Abstracts 2024-25, and the crs.gov.in abstracts page.
- **Parliament:** Lok Sabha USQ 2597 (2024) and Rajya Sabha USQ 1555 (2025).
- **Quadrant's NSE filing,** 26 May 2026.
- **Railway documents:** the IEI Kavach deck (2024) and the IRIMEE Vande Bharat deck (654 m row re-read).
- **News and trade press:**
  - DT Next explainer (13 Apr 2026) and PTI report (17 Jun 2024);
  - Indian Express (16 Jul 2024);
  - Rail Engineer (2 May 2023);
  - All India Radio (24 Jul 2024 and 22 May 2026);
  - The Quint (3 Jun 2023);
  - Odisha Bytes (4 Mar 2022).
- **Apple App Store** listing for RailMadad.

**Still blocked:** every `*.indianrailways.gov.in` host (RDSO, SECR, SCR). logicallyfacts.com did not resolve, and the Indian Infrastructure page was read only through the fetch tool. Nothing was routed around.

### v2 fixes applied (2026-10-15, writer)
Required: V048 "had to move on a paper authority" (KV-092 now confirmed); V052 "what about the claim … exactly fifteen
kilometres per hour? Fifteen is the speed loco pilots must follow" (KV-093 deleted). All eight cite-tag fixes applied.
Recommended applied: V002 "the loco pilot", V007 "read what the official accident inquiries found", V029 "if the loco
pilot doesn't slow down", V036 years on screen. Not applied: V035 wording, V044 ministry statement, ₹2,066 cr (owner's
call; length). Production note kept: the trial clip must show the head-on run (PIB 4 Mar 2022 gives 380 m for it).
