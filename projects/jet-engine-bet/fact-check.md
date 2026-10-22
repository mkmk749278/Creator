# Fact-check: The Jet Engine Bet (vo.txt, science lines, checked 2026-10-22)

`claims.csv` has **91 claims**: 84 confirmed, 5 claim, 2 disputed, 0 unverified, 0 wrong.
`python3 scripts/claims_check.py projects/jet-engine-bet/claims.csv` **passes**.

**Scope (coordinator, 22 Oct 2026):** only the new or changed science lines: the blade and who can make it, the four
jobs, the turbine behind the flame, Rolls-Royce 200 °C, Cambridge 1,400 / 930 °C and our 470 °C, creep / single crystal /
rhenium / CMSX-4, cooling channels / film / ceramic coating, 12,000 rpm and the bus, rocket against fighter engine.
- **45 science rows are new.** Every cited page was opened on 22 Oct 2026 and every quote was re-matched word for word
  (a script did the matching, then I read the results). Plus 3 rows for L71, L73 and L75, sourced in passing (outside the scope, not a full check).
- **43 rows are copied unchanged** from `projects/jet-engine-paradox/claims.csv` (hook numbers, IAF, orders, Kaveri, Safran,
  1998, DMRL blades; checked 13 Oct 2026). Same status, source and quote; only the id and the line number are new. They were
  not re-opened. Their notes start `CARRIED OVER UNCHANGED`.
- Two rows (JB-007 for L4, JB-024 for L15) describe the corrected wording and say `REPLACES …` in the note, as in the magnet
  film, so the gate can pass while the VO is still unchanged. `vo.txt` was not edited.

## 1. Lines that must change

### Wrong, or not backed for the F404

**L15: wrong**
- Old: `Now remember this, because you'll need it. The turbine sits right behind the flame. It's the hottest place in the whole engine.`
- New: `Now remember this, because you'll need it. The turbine sits right behind the flame. It's where the metal has the toughest job in the whole engine.`
- Why: the flame is hotter than the turbine. The gas burns hottest in the combustion chamber, then air is mixed in to cool it
  before it reaches the turbine, and a fighter's afterburner runs hotter than the turbine too. A NASA-hosted report puts the
  flame zone at "peak temperatures ~ 2500 °K"; Rolls-Royce puts the gas behind the combustion chamber at 2,000 K. Wikipedia's
  J57 example (an early engine): 2,040 °C in the combustion chamber, 850 °C at turbine entry, 1,390 °C in the afterburner.
  What is true: Cambridge says "The most severe conditions are met in the first row of the turbine."
- Source: University of Cambridge (T. Sourmail, 2004); Heywood and Mikus, NTRS 19730017094 (1973); Rolls-Royce 2018;
  Wikipedia, Afterburner and Combustor. Tag `[UNIV. OF CAMBRIDGE | NASA]`.

**L4: not backed for the F404**
- Old: `And here's the crazy part. Inside that engine, a small metal blade sits in gas that is hotter than the blade's own melting point... and the blade does not melt.`
- New: `And here's the crazy part. Inside a modern jet engine, a small metal blade can sit in gas that is hotter than the blade's own melting point... and the blade does not melt.`
- Why: "that engine" is the F404 (L3). No source gives the F404's turbine gas temperature or the melting point of its blade
  alloy. Rolls-Royce (2012: "up to 200 degrees above the melting point of their alloy"; 2018: "several hundred degrees hotter
  than the melting point of the blades"), NASA and Cambridge all say it for modern engines in general. L18 can stay.
- Source: Rolls-Royce press release 21 Jun 2012; NASA Special Projects Laboratory. Tag `[ROLLS-ROYCE | NASA]`.

### Overstated or loose (the stronger wording has no source)

**L31**
- Old: `Why is a rocket easier? Because you only need it for minutes.` (rest of the line unchanged)
- New: `Why is a rocket a different job? Because you only need it for minutes.`
- Why: "easier" has no source, and ISRO's own upper stage on the LVM3 page is a "cryogenic stage ... (LOX /LH2)". What is
  sourced: minutes (ISRO: about 134 s, 200 s and 646 s), a fighter engine breathes air (NASA), idle to full power in seconds
  (FAA rule: 95% in 5 s or less), thousands of hours (GE). One commentary source says it well: "missile propulsion is a
  sprint. Fighter propulsion is a marathon". Tag `[ISRO | NASA | GE AEROSPACE]`.

**L20**
- Old: `...you'd see millions of tiny crystals stuck together.`
- New: `...you'd see countless tiny crystals stuck together.`
- Why: no source counts them. "Millions" fits a thumb-sized lump of fine-grained metal (our estimate: grains of 50 down to
  10 micrometres give about 8 million to 1 billion per cubic centimetre). A cast blade has far bigger grains (1 millimetre
  grains: about 1,000 per cubic centimetre). Cambridge says only "many small crystals or grains". Tag `[UNIV. OF CAMBRIDGE]`.

**L23**
- Old: `Each blade is hollow, with tiny channels inside.`
- New: `These blades are hollow, with tiny channels inside.`
- Why: NASA describes the air-cooled hot-stage blades ("hollow turbine blades"); no source says every blade in the engine is
  hollow. Tag `[NASA]`.

**L28**
- Old: `The disc holding these blades turns more than twelve thousand times every minute.`
- New: `Rolls-Royce says the disc holding these blades turns more than twelve thousand times every minute.`
- Why: 12,000 rpm and the London bus come from one Rolls-Royce release about its big Trent engines. L29 already says "Rolls-Royce
  says"; L28 does not. We found no F404 figure. Tag `[ROLLS-ROYCE | 2012]`.

**L17** (small)
- Old: `Gas of about fourteen hundred degrees.`
- New: `Gas of about fourteen hundred degrees Celsius.`
- Why: the unit is missing. The numbers are right: Cambridge's worked example gives gas about 1,400 °C at turbine entry and a
  blade metal "in the vicinity of 930 °C" with the cooling and the thermal coat; 1,400 - 930 = 470 is our calculation.
  Cambridge's page is a 2004 teaching page and does not say 930 is typical, so keep "Cambridge puts numbers on it". Rolls-Royce
  (2018) gives 1,700 °C for newer engines.

### Promises the film does not keep (L6, L19)

- L6: `Then, in about three minutes, the blade that should melt...` → `Then, about three minutes in, the blade that should melt...`
  Our word count (about 2,000 spoken words) puts the blade (L16) at about 2:47 and the three tricks (L19) at about 3:27 from
  the start at 150 words a minute (2:36 and 3:14 at 160). The promise itself is spoken at about 0:45, so "in three minutes"
  would mean about 3:45. Re-time after recording (`align_script.py`).
- L6: `...using things in your own kitchen.` → `...using everyday things.` Only the gas stove, the spoon and the thermos are
  kitchen things; the bicycle pump, ceiling fan, balloon and mall air curtain are not.
- L19: `And you've seen each one at home.` → `And you've seen each one in daily life.` (the air curtain is at a mall.)

**Tags to put on screen** (charter rule: one on every factual claim): L4 `[ROLLS-ROYCE | NASA]` · L5 `[PIB | 2021]` ·
L8 to L14 `[NASA GLENN]` · L15 `[UNIV. OF CAMBRIDGE | NASA]` · L16 `[ROLLS-ROYCE | 2012]` · L17 `[UNIV. OF CAMBRIDGE | OUR CALCULATION]` ·
L20 to L22 `[UNIV. OF CAMBRIDGE | USGS]` · L23, L24 `[NASA]` · L25 `[UNIV. OF CAMBRIDGE]` · L26 `[ROLLS-ROYCE | 2018]` ·
L28, L29 `[ROLLS-ROYCE | 2012]` · L30 `[GE AEROSPACE | 2001]` · L31 `[ISRO | NASA | GE AEROSPACE]` · L59 `[PIB | 2021]`.

## 2. Fine as written (science lines)

Very few countries make single-crystal blades (PIB 2021: USA, UK, France, Russia) · suck, squeeze, burn, blow · the fan at
the front · compressing air heats it · fuel burned in the burner · the turbine spun by the gas and joined by a shaft to the
compressor · thrust from Newton's third law · the contrail · Rolls-Royce "up to 200 degrees" · grain boundaries and creep ·
single crystal with no boundaries · nickel alloy with rhenium (rare: under 1 part per billion in the crust, USGS) ·
DMRL casts CMSX-4 · cooling channels, film of cool air, ceramic coating · metal kept far below the gas · 12,000 rpm and the
London bus · a ceiling fan runs about 350 to 400 rpm on full speed (so 12,000 is about 30 times faster) · rocket burn times ·
a fighter engine breathes air · idle to full power in seconds · thousands of hours.

## 3. Claims, analogies and disputed rows

- **Analogies (label ANALOGY on screen):** bicycle pump (L10), gas stove (L11), wind on a ceiling fan (L12), balloon (L14), brick
  wall (L20), steel spoon in a flame (L21, row JB-032, status claim), mall air curtain (L24), thermos (L25), bucket (L29). Each
  sits in the row of the fact it illustrates (JB-015, 017, 019, 021, 029, 032, 038, 040, 044); the analogy itself is not an
  engine claim.
- **Narrator's assessments (status claim):** "India is still learning" (L5, JB-009), the open-loop minute (L6, JB-010), "a rocket is
  easier" (L31, JB-049, fix above), "you can't just copy the drawing" (L32, JB-050).
- **Disputed (carried over):** JB-053 (L34, the "small club"): lists differ. KED Global adds Ukraine, Eurasia Review says "US,
  UK, France, Russia, and now China", idrw (22 Aug 2026) names Japan among the blade leaders. The VO says "the main members",
  which is safe. Description note: `Ukraine also builds jet engines; Germany, Japan and Italy have partial capacity.`
  JB-071 (L52): the Kaveri's afterburner thrust ranges from 65 to 78 kN in reports; the VO says "As reported ... about seventy".
- Opinion lines with no row: L45 and L67 ("if you don't own the engine..."), L76 ("I read every one": the owner's own
  statement, make sure it is true).

## 4. On-screen labels and caveats (science)

- L16: `UP TO 200 °C ABOVE THE MELTING POINT · ROLLS-ROYCE 2012` (its big civil engines).
- L17 gauge: `GAS ~1,400 °C · METAL ~930 °C · CAMBRIDGE 2004` and `OUR CALCULATION ~470 °C`. **Do not draw the alloy's melting
  point at 1,200 °C** (1,400 minus 200, as the screenplay's L16 beat suggests). The 1,400 and the 200 come from different
  sources and years, and we have no sourced melting point for the blade alloy. Any melting-point line: `ILLUSTRATIVE`.
- L4 and L5 map: label it `PIB 2021: USA · UK · FRANCE · RUSSIA` and do not make it look complete (other sources add China, Japan,
  Ukraine). Do not show India as empty: DMRL casts single-crystal blades (60 for a helicopter engine, 2021, L59). Show India as
  "learning".
- L9: if airflow appears: `F404-IN20: 153 lb/s (70 kg/s) · GE`. L10: pressure ratio `28 : 1 · GE` if shown.
- L14: the contrail shot is airliner stock; label it stock.
- L22: the rhenium lattice shot: `ILLUSTRATION`.
- L30: `THOUSANDS OF HOURS` is fine. Do not show 2,000 or 6,000 as the F404's own numbers (GE's figures are for an F414 turbine).
- L31: ISRO LVM3 burn times `~134 s · ~200 s · ~646 s`; this is India's rocket, expendable stages (reusable rockets bring parts back).

## 5. Not done in this pass (coordinator's scope change, 22 Oct 2026)

- The "Time-sensitive: re-check before upload" section was **skipped on instruction**. The carried-over rows keep their
  13 Oct 2026 wording ("as of 13 October", "RE-CHECK RIGHT BEFORE RENDER"). Before upload someone still has to re-check at
  least: engines sent (JB-003), nothing delivered (JB-004), Safran-GTRE approval (JB-011), squadrons (JB-054).
- Items 1, 10 and 12 (hook numbers, IAF, orders, Kaveri, Safran, 1998, DMRL, AMCA, J-20) were **not checked again**. For
  the record: before the scope change arrived I had already opened every old cited page once with a script (56 of the 66 old
  quotes matched word for word; the CAG, MiGFlug and Delhi Defence Review ones could not be opened from here). After the
  instruction I opened only two pages, to copy a quote exactly for section 6 (idrw 20 Oct and The Defense Post).

## 6. Seen in passing, outside the agreed scope (not a re-verification; the coordinator decides)

These came from pages I had opened before the scope change. The carried-over rows are unchanged.
- **L63, "the government picked France's Safran to build it with G.T.R.E." (row JB-087): stronger than the sources.** AFP (The
  Defense Post, 23 Aug 2025): Singh "did not name the company ... There was no immediate confirmation" (IANS quotes him naming
  Safran). New Indian Express, 14 Aug 2026: Rolls-Royce and Reliance are "a new contender to the race"; their plan "is not a
  government selection"; the Safran-GTRE proposal "awaits final Cabinet Committee on Security (CCS) approval" with IP "among the
  issues under discussion". idrw, 20 Oct 2026: the AMCA Mk2 engine "is to be determined later this year". Safer L63: `In August
  twenty twenty-five, the Defence Minister said India would build it with France's Safran, together with G.T.R.E. India's
  condition, as reported? Full Indian ownership of the design.`
- **L3, "The biggest reason? An engine." (JB-005):** HAL's chairman told the Times of India on 18 Sep 2026 that the first batch
  still needs AESA radar integration ("90-95%") and missile integration; New Indian Express and The Hindu (7 Oct) call the engine
  "the principal bottleneck" or say it "affected the aircraft delivery"; Indian Masterminds (15 Oct) calls it "one of the main
  reasons". Safer: `By most reports, the biggest reason? An engine.`
- **L3, "the ninety-nine engines these jets need":** the 99 are the 2021 order "for the first 83 Mk-1As" (New Indian Express, 7 Oct
  2026), not what the ~30 waiting jets need. Safer: `...only fourteen of the ninety-nine engines ordered for the first batch.`
  HUD label: `ENGINES SENT 14 / 99` (not "delivered": HAL's chairman said on 18 Sep that 10 had been received, and the New
  Indian Express still wrote 10 on 6 Oct, before GE's September shipment of 4 arrived).
- **L1, "in H.A.L. hangars ... You'd think they're ready to fly":** idrw (20 Jul 2026) says the finished jets are "kept in
  storage" and have flown on Category-B test engines, so "ready for the Air Force" is closer than "ready to fly". We found no
  source for "hangars"; `at H.A.L. in Bengaluru and Nashik` is safe.
- **L61, "The first A.M.C.A. jets will use G.E.'s F414":** New Indian Express (14 Aug 2026) says the Mk1 "is planned to fly with"
  it and India is "negotiating local production". New Indian Express and NDTV Profit reported a commercial deadlock in June
  2026; idrw (25 Jun) relayed a later update that HAL's own talks were not in trouble. Safer: `are planned to use`.

## 7. Notes for the writer

- The CAG report host (d7i5wg8xwe4hf.cloudfront.net) fails through this session's network proxy (502) and MiGFlug returns 403, so
  the carried-over rows that cite them could not be re-checked from here anyway. None is needed for the science rows.
- NASA's new Beginner's Guide address `…/beginners-guide-to-aeronautics/gas-turbine-parts/` returns 404; the old Glenn pages
  (`www.grc.nasa.gov/www/k-12/airplane/…`) and the Special Projects Laboratory page (nasa.gov) carry the same text and open fine.
- Wikipedia is used only as second support (creep, afterburner, combustor, thermal barrier coating, air door, thermos).
- Two sources are commentary, not official: Eurasia Review (28 Feb 2026) and idrw. They back "India is still learning" and the
  rocket-against-fighter framing; both are marked `claim`.
- The Cambridge page writes degrees as "o C" and prints "1-200" where it must mean 100-200; the quotes in `claims.csv` use
  "°C" and keep "1-200" as printed.
