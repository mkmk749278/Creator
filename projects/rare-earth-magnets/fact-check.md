# Fact-check: Rare earth magnets (vo.txt, checked 2026-10-21)

`claims.csv` has **83 claims**: 78 confirmed, 3 claim, 2 disputed, 0 unverified, 0 wrong.
`python3 scripts/claims_check.py projects/rare-earth-magnets/claims.csv` **passes**.

**Status:** the rows for wrong lines describe the corrected wording (each one says `REPLACES …` in its note). While
this check was finishing, all **16 required changes** below (plus the optional L4, L13, L19 and L50 tweaks) were applied
to `vo.txt` and `script.tsv` (the `en` column matches `vo.txt` line for line). `claims.csv` now matches the live text.
The live `vo.txt` passes `scripts/spoken_english_check.py` (1,662 words, rare words 2.3%). But "you" is at 3.0 per 100
words, exactly at the limit, because L14 says "we buy" instead of "you buy". Any edit that removes a "you" will fail it.

Every quote in `claims.csv` was copied from the page it cites. Primary sources used: USGS Mineral Commodity Summaries
2025 and 2026 (with its revision history), IEA Rare Earth Elements report and IEA Global Critical Minerals Outlook 2026,
US DOE magnet supply-chain report (2022), PIB/PMIndia releases and Parliament replies (2015 to 2026), MOFCOM notices,
Indian Bureau of Mines yearbooks, the Ministry of Heavy Industries scheme page, Apple's product report and UN Comtrade.

## 1. Lines that must change

### Wrong, out of date or misleading

**L5: wrong (out of date)**
- Old: `By one American government count, India holds the third biggest store of it on Earth.`
- New: `By our own government's count, India's sands hold about seven million tonnes of rare earths.`
- Why: the American count (USGS) ranked India third only in its January 2025 edition (6.9 million tonnes). The current
  2026 edition (Feb 2026, revised May 2026) shows India as "NA". Its footnote cites only a 2015 report on one
  company's monazite (OSCOM), with no rare earth reserve figure. Other sources say fifth (Indian Bureau of Mines
  yearbook 2022; Reuters, June 2025).
  India's own Atomic Minerals Directorate counts 7.23 million tonnes of rare earth oxide in 13.15 million tonnes of monazite.
- Source: PIB, Rajya Sabha reply, 2 Apr 2026; USGS MCS 2026, p. 153. Tag `[DAE / AMD | 2026]`.

**L14: misleading number**
- Old: `Now look at this number. In one year, India brought in about fifty-three thousand tonnes of permanent magnets from abroad.`
- New: `Now look at this number. India needs about four thousand tonnes of these magnets a year... and we buy almost all of them from abroad.`
  (The live file uses "we buy". "you buy" is equally accurate and gives the "you" count some room.)
- Why: 53,748 tonnes is the customs total for every "permanent magnet of metal". Most of that is cheap magnets that are
  not rare earth magnets. UN Comtrade puts India's 2024 imports under that code at 54,452 tonnes, worth only
  US$198.6 million. That is about US$3.6 a kilo (our calculation), which is the price of ferrite magnets. China
  exported only 58,152 tonnes of rare earth magnets to the whole world in 2024 (Adamas Intelligence). India's
  minister says the country needs about 4,000 tonnes of rare earth magnets a year.
- Source: PIB (DAE), Lok Sabha, 25 Mar 2026; PMIndia Cabinet release, 26 Nov 2025. Tag `[DAE | LOK SABHA 2026]`.

**L15: follows L14**
- Old: `And about nine out of every ten tonnes came from one country. China.`
- New: `And more than eight out of every ten come from one country. China.`
- Why: the government's own figure is 85 to 90% by weight and 60 to 80% by value (2022 to 2025). ICRA puts China at
  about 85% of FY2025 rare earth magnet imports by value.
- Source: PIB backgrounder, 2 Feb 2026. Tag `[GOVT OF INDIA | PIB 2026]`.

**L3: keeps the hook in line with L15**
- Old: `No strike. No battery problem. What's missing is a magnet... and almost every one of them comes from China.`
- New: `No strike. No battery problem. What's missing is a magnet... and most of them come from China.`

**L38: out of date**
- Old: `It separates about nine in every ten. And it makes about ninety-four percent of the world's strongest magnets.`
- New: `It separates about eighty-five percent. And it makes about ninety-four percent of these strong magnets.`
- Why: the IEA's newest report (Global Critical Minerals Outlook 2026, July 2026) says China's refining share fell from
  90% to 85% between 2024 and 2025. The 94% is the 2024 figure for sintered magnets in the IEA's Rare Earth Elements
  report (April 2026); we found no newer one.
  "These strong magnets" stops it sounding like all the world's magnets.
- Tag `[IEA | 2026]`.

**L54: not supported**
- Old: `By July, Bajaj was making about half the Chetaks it made a year earlier. Ather and T.V.S. cut production too.`
- New: `By July, Bajaj was making about half the Chetaks it made a year earlier. Ather and T.V.S. felt the squeeze too.`
- Why: only one ET report, quoting unnamed people, said they were set to cut. July 2025 factory data show TVS iQube
  output up 6% and Ather up 45% on a year earlier. TVS called magnets a "challenge". Ather's CEO described a dealer
  supply gap, "not a full halt in production".
- Source: Financial Express (TVS spokesperson), Jul 2025; Autocar India, 5 Aug 2025 (Ather) and Aug 2025 (data).
  Tag `[AUTOCAR INDIA | FINANCIAL EXPRESS | 2025]`.

**L55: wrong timing**
- Old: `In an interview, Rajiv Bajaj warned that China could bring India's whole electric vehicle industry to a halt within weeks.`
- New: `Back in April, Rajiv Bajaj had warned — if China stopped these magnets, India's whole electric vehicle industry could halt within weeks.`
- Why: he said it on 28 April 2025, to Moneycontrol, before the July drop. His warning had a condition: "If this is
  true, it would mean that in a matter of weeks, the entire Indian EV industry will grind to a halt." The old line
  comes right after "By July", so it sounds like he said it later.
- Source: CNBC-TV18, 28 Apr 2025. Tag `[MONEYCONTROL / CNBC-TV18 | APR 2025]`.

**L58: out of date (disputed)**
- Old: `That hold runs out on November tenth, twenty twenty-six, unless China extends it.`
- New: `On paper, that hold ends on November tenth. But in September, America and China stretched their truce to January... and you'll want to see if this hold goes with it.`
- Why: China's notice No. 70 still says 10 November 2026. On 28 September 2026 China's commerce ministry said the
  trade truce now runs to 10 January 2027, but it did not name the rare earth hold. No new notice had appeared by
  16 to 20 October. Some analysts (BISI, Brownstein) say the hold now runs to January. Others (technology.org,
  Bloomberg Government) say only 10 November is in writing. The new line states only what is certain.
- Source: MOFCOM Announcement No. 70 (2025); MOFCOM statement, 28 Sep 2026; technology.org, 19 Oct 2026.
  Tag `[MOFCOM | 2025–26]`. **Check again the day before upload.**

**L77: follows L58**
- Old: `Watch two things. November tenth — does China's hold end? And the scheme winners — the five companies that will try to build India's own magnets.`
- New: `Watch two things. Does China's hold end in November, or get stretched? And the scheme winners — the five companies that will try to build India's own magnets.`

**L69: says more than the sources show**
- Old: `So the sand stays here. The money is here. Now comes the hard middle you saw in that chain.`
- New: `So the plan is to keep the sand here. The money is here. Now comes the hard middle you saw in that chain.`
- Why: Reuters reported a request to stop the Japan exports, and said an immediate halt "may not be feasible". No later
  report says the exports stopped.
- Tag `[REUTERS | JUN 2025]`.

**L74: not accurate**
- Old: `But the reality today is different. India has the sand. It has the scientists. And now it has the money. What's left is the hard middle — the tanks and the furnaces.`
- New: `But the reality today is different. India has the sand. It has the scientists. And now it has the money. What's left is the hard middle — more tanks, and the furnaces.`
- Why: I.R.E.L. already runs separation tanks that make clean oxide. What India lacks is alloy and magnet making at
  factory scale. DAE: "further industrial scale facilities (intermediate) from alloy, magnet etc. is non-existent."
- Source: PIB (DAE), Rajya Sabha, 12 Mar 2026. Tag `[DAE | RAJYA SABHA 2026]`.

### Smaller accuracy fixes

**L18**
- Old: `There are seventeen of them. And when you dig them up, you get all of them mixed together.`
- New: `There are seventeen of them. And when you dig them up, you get them mixed together.`
- Why: not all 17 turn up in the ore. Promethium is almost never found (Indian Bureau of Mines), and USGS counts 15
  "naturally occurring" rare earths.

**L26**
- Old: `Then hydrogen gas cracks those pieces, and you grind them into a powder much smaller than flour dust.`
- New: `Then hydrogen gas cracks those pieces, and you grind them into a powder much smaller than flour.`
- Why: magnet powder is under 10 microns (US DOE) and flour averages about 45 microns (ASABE 2014), so "smaller than
  flour" is sourced. "Flour dust" means the finest bits of flour, and no source we found gives their size.
  Tag `[US DOE | ASABE]`.

**L31**
- Old: `So how did China end up holding almost every link?`
- New: `So how did China end up leading every link?`
- Why: China mines about 60%, which is not "almost" all, but it has the biggest share of every link (IEA).

**L39**
- Old: `Do you notice something? Digging is the easy part. The tanks and the furnaces are the hard part... and China owns them.`
- New: `Do you notice something? Digging is the easy part. The tanks and the furnaces are the hard part... and China runs most of them.`
- Why: about 85% of separation and 94% of magnets, not all of them (IEA).

**L65**
- Old: `Five companies can win up to twelve hundred tonnes each. In August, twenty companies put in bids. Among them, Larsen and Toubro, Coal India and ReNew.`
- New: `Five companies can win up to twelve hundred tonnes each. In August, twenty bids came in. Among them, Larsen and Toubro, Coal India and ReNew.`
- Why: there were 20 bids, and three of them were joint bids by more than one company (PSU Watch, 14 Aug 2026).
  Tag `[MHI / DD INDIA | AUG 2026]`.

### Optional (already applied in the live file, all sourced)
- L4: "in Andhra Pradesh, Kerala, Tamil Nadu and Odisha". The government lists Andhra Pradesh first among the monazite states.
- L13: "in many wind turbines". The common geared wind turbine uses no rare earth magnets (US DOE).
- L19: "Nearly the same size". USGS says the rare earths are "generally similar", not identical.
- L50: "Our own atomic energy department says India has very little of those". The writer marked this contested, but
  DAE (PIB, 12 Mar 2026) and the Indian Bureau of Mines both say heavy rare earths are not found in Indian deposits in
  amounts worth mining. R54 now cites the DAE reply.
- Not applied, and fine as is: L67 "special rare earth zones". The official name is "Rare Earth Corridors", so the
  on-screen label should say RARE EARTH CORRIDORS.

### New in the live script: check against the cut
- L7 now promises: "Then, about five minutes in, the thing hidden inside our sand that kept it locked away." At 150 words
  a minute, the monazite and thorium lines (L42 and L43) start at about 5.2 and 5.4 minutes, before any pauses or
  diegetic breaks. Check the real minute in the final cut (L40, "What stopped us?", starts at about 5.0).

## 2. Disputed rows, claims, and what goes in the description

- **R32, Deng Xiaoping (L32): disputed year.** Keep "is reported to have said". Most sources date the remark to
  1992. CSIS dates it to 1987. We found no transcript or official record of it.
  Note: `Deng Xiaoping's oil and rare earths remark is usually dated to 1992. Some sources say 1987.`
- **R64, China's hold (L58): disputed.** Note: `As of 21 October 2026, China's own notice still ends the hold on
  10 November 2026. The US-China truce now runs to 10 January 2027.`
- **Claims the VO already attributes:** R59 (Rajiv Bajaj's warning), R75 (Reuters' June 2025 report), R76 (the plan to
  keep rare earths at home).
- The owner's rule (2026-10-17) keeps sources and disclaimers out of the YouTube description. Put the two notes above in
  a **pinned comment** or say them on screen. They stay in `claims.csv` either way.

## 3. On-screen labels and caveats

- L2: `20,384 → 10,824 (−47%) · JULY 2024 vs JULY 2025`.
- L5: `7.23 MILLION TONNES (IN THE GROUND, AS OXIDE) · DAE 2026`. Show **no world rank**.
- L14 and L15: `~4,000 TONNES A YEAR · DAE, MAR 2026` and `85–90% FROM CHINA (BY WEIGHT, 2022–25)`. Do not show 53,748.
- L22: any tank count drawn: `ILLUSTRATIVE`. A patent example uses 152 stages to clean one element.
- L11 and the HUD: any motor size, weight or km-per-charge figure: `ILLUSTRATIVE`.
- L27: `~1,000–1,100 °C`.
- L32: the Deng line on screen with `REPORTED`.
- L37 and L38: `IEA · MINED ~60% (2025) · SEPARATED ~85% (2025) · MAGNETS 94% (2024)`.
- L52: `LICENCE NEEDED: Sm · Gd · Tb · Dy · Lu · Sc · Y + MAGNETS CONTAINING Sm, Tb OR Dy`.
- L58 and L77: `ON PAPER: 10 NOV 2026 · TRUCE: 10 JAN 2027 · AS OF 21 OCT 2026`.
- L61 and L62: `SAMARIUM-COBALT · BARC + DMRL TECH`; a drawn plant is `ILLUSTRATION`.
- L65 and L66: `20 BIDS · AUG 2026` and `WINNERS: NOT ANNOUNCED (21 OCT 2026)`.
- L67: `RARE EARTH CORRIDORS`.
- L68: `REPORTED · REUTERS, JUNE 2025`.
- L79: if a number is shown: `ABOUT 7 IN 10 IMPORTED BULK DRUGS FROM CHINA (FY24)` (DGCI&S data).

## 4. Check again right before upload

1. L58 and L77: whether China extends or ends the hold. The legal date is 10 Nov 2026, 20 days from this check.
2. L66: magnet scheme winners. Nothing after Addendum-3 (29 Jul 2026) was on the Ministry's page on 21 Oct 2026.
3. L68 and L69: any news that I.R.E.L.'s Japan exports actually stopped or restarted.

## 5. Notes for the writer

- Two `research.md` leads were wrong. The USGS 2026 edition does not keep India at 6.9 Mt; it shows "NA". The 53,700 t
  "magnet imports" figure counts mostly ordinary magnets, not rare earth ones. Also, BISI's "extended to 10 Jan 2027"
  is not in any Chinese legal text yet.
- IREL's own site (security certificate error), DRDO's site (503) and MOFCOM's English site would not open from here.
  PIB releases and law-firm or news copies of the MOFCOM text covered the same facts.
- PIB (25 Mar 2026) gives the Vizag plant a capacity of "500 tonnes per year". PIB (2 Apr 2026) and other reports say
  3 tonnes a year. The VO gives no capacity, so keep it that way.
