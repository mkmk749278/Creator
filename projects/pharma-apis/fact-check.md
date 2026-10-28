# Fact-check: The Pharmacy of the World's Missing Powder (narration v2)

Independent full pass, 2026-10-28, on `vo.txt` v2 (85 lines). No draft `claims.csv` existed, so every claim was checked
from zero. Primary documents were opened: DGFT notifications 50/2015-20 (3 Mar 2020) and 56/2025-26 (29 Jan 2026), the
NITI Aayog Trade Watch (June 2026), the DGTR 2010 penicillin findings, the DoP Annual Report 2025-26, the PIB backgrounder
of 21 Mar 2026, the Lyfius/Aurobindo filing, RIS DP 268, ISID WP239, MDPI Economies 9:71 and CFR's The Pharma Choke Point.

**Result:** 71 claims. 67 confirmed, 4 marked `claim` (the VO must attribute them). `claims_check.py` passes **only if the
13 line changes below are made**: each changed line has a row in `claims.csv` marked `REPLACES`. If a line stays as it is,
that row must go back to `wrong`.

## Lines that must change (old → new)

**L5 (wrong: the order was two pages, and it listed 13 ingredients plus the medicines made from them, not 26 ingredients)**
- Old: Delhi. A one-page government order goes out, and if you run a medicine company, your phone starts ringing. Twenty-six medicine ingredients can't leave India without a licence. Paracetamol is one of them.
- New: Delhi. A two-page government order goes out, and if you run a medicine company, your phone starts ringing. Thirteen medicine ingredients, and the medicines made from them, can't leave India without a licence. Paracetamol is one of them.

**L8 (unsupported: no source says about half; this is now a `claim`, so it is attributed)**
- Old: About half the ingredients on that list came mainly from that one place.
- New: Reports at the time said many of the ingredients on that list came from that one place.

**L10 (a blanket safety promise that no source in this film supports; L80 already gives the right safety line)**
- Old: And before you worry — your medicines are safe. This isn't about quality. It's about who controls the supply.
- New: And before you worry — this isn't about the quality of your medicines. It's about who controls the supply.

**L28 (India decided to make penicillin in 1950–51; 1954 is when Hindustan Antibiotics was set up; 6 years 7 months after independence)**
- Old: Pimpri, near Pune. Nineteen fifty-four. India has been free for barely seven years, and it decides to make its own penicillin.
- New: Pimpri, near Pune. Nineteen fifty-four. India has been free for less than seven years, and it's building a factory to make its own penicillin.

**L31 (WHO and UNICEF paid for the equipment and the experts, so "on its own" misleads)**
- Old: Just think about it. Picture your grandparents' India. A young, poor country, growing one of the most important medicines on earth... on its own.
- New: Just think about it. Picture your grandparents' India. A young, poor country, growing one of the most important medicines on earth... in its own factory.

**L34 (no source supports "most"; of the 53 critical bulk drugs in India's 2020 scheme, 26 are grown and 27 are made from chemicals)**
- Old: Most medicines, like paracetamol, are cooked from chemicals, step by step. Penicillin is different. Penicillin is grown.
- New: Many medicines, like paracetamol, are cooked from chemicals, step by step. Penicillin is different. Penicillin is grown.

**L64 (₹2,500 crore is the company's own figure; the DoP lists ₹1,910 crore and PTI said ₹2,400 crore, so this is a `claim`)**
- Old: Inside are the giant tanks I just told you about. It cost around two thousand five hundred crore rupees, and it's built to make fifteen thousand tonnes of penicillin G every year.
- New: Inside are the giant tanks I just told you about. The company says it cost around two thousand five hundred crore rupees, and it's built to make fifteen thousand tonnes of penicillin G every year.

**L65 (wrong: Alembic and SPIC were still making penicillin G in 2005–09 (DGTR, 2010), and Alembic stopped in 2011 (ISID), so the gap was about 13 years, not 30)**
- Old: In twenty twenty-four, the tanks start running. For the first time in about thirty years... India is growing its own penicillin again.
- New: In twenty twenty-four, the tanks start running. For the first time in more than ten years... India is growing its own penicillin again.

**L67 (not rare: DGFT set a minimum import price on sulfadiazine in October 2025 and on ATS-8, before penicillin)**
- Old: So on the twenty-ninth of January, twenty twenty-six, the government did something it rarely does.
- New: So on the twenty-ninth of January, twenty twenty-six, the government stepped in.

**L68 (imports below the floor are "Restricted": they need a government licence, and export units and SEZ units are exempt, so "cannot come in" overstates)**
- Old: It set a minimum price at the border. Penicillin G cannot come into India cheaper than about two thousand two hundred rupees a kilo. Amoxicillin and six A.P.A. got minimum prices too.
- New: It set a minimum price at the border. Penicillin G cheaper than about two thousand two hundred rupees a kilo now can't come into India without a special licence. Amoxicillin and six A.P.A. got minimum prices too.

**L74 (none of the three parks is running; Gujarat only opens plot applications on 26 Oct 2026. No source compares tank sizes, but China makes 90–95% of the world's penicillin)**
- Old: Let me be honest with you. Most of those parks aren't running yet, as far as we can tell. And China has a thirty-year head start, with tanks far bigger than ours.
- New: Let me be honest with you. None of those parks is up and running yet. And China has a thirty-year head start, and makes far more penicillin than we do.

**L75 (the last Indian penicillin plant stopped in 2011, so "decades" is wrong; same reason as L65)**
- Old: So has India won? Not yet. But for the first time in decades, it's back in the fight.
- New: So has India won? Not yet. But it's back in the fight.

**L83 (India now has its own models (Sarvam-105B, Feb 2026), but they score well behind the US and China)**
- Old: Medicines aren't the only missing piece. India writes software for the whole world. So why doesn't it have its own giant A.I.? That's our next story.
- New: Medicines aren't the only missing piece. India writes software for the whole world. So why is India's own A.I. still so far behind America's and China's? That's our next story.

## Rows marked `claim`: how the VO attributes them
- **L8** (new line): "Reports at the time said…" (The Tribune, 3 Mar 2020; Industrial Info, Feb 2020; MDPI 2021).
- **L25**: keep "Industry reports say a big share of that still comes from China." A 2024 review puts China at 60–80% of
  India's para-aminophenol, but new Indian plants now make some (about 25,500 tonnes a year of capacity). Show no percentage on screen.
- **L57**: keep "Niti Aayog says…" (better still: "Niti Aayog estimates…"). The 35–40% figure is NITI repeating 2013 and 2020 studies.
- **L64** (new line): "The company says it cost…". If any figure goes on screen, show `₹2,500 CRORE [COMPANY]`.

## Small fixes I recommend (not wrong, just tighter)
- L7: "had just shut down" → "was shut down" (Hubei had been locked down since 23 January, six weeks before the order).
- L41: "your bill doesn't double" → "your costs don't double" (the power bill grows with tank size; it is the total cost that doesn't double).
- L47: "huge chemical parks" → "huge drug parks" (the sources say special economic zones and bulk drug parks).
- L22: "around sixty-five thousand crore" is fine. "Around sixty-four thousand crore" is a touch closer.
- L51–L54 roll call: Alembic was the **last** plant to stop (2011). Put no years on the STOPPED stamps, or end the roll call on Alembic.

## New since the research leads (worth one line in L69–L71)
- **Anti-dumping cases:** on 28 Sep 2026 DGTR opened an anti-dumping investigation into Chinese penicillin G on Lyfius's
  application. Its first look found dumping and "material retardation" of the new Indian industry. On 25 Sep 2026 it opened
  another into 6-APA from China and the EU (applicant Qule Pharma). A duty could replace the floor price. A possible line,
  after L71: *And in September twenty twenty-six, the government also opened an anti-dumping case against Chinese
  penicillin, after a complaint from the Kakinada plant.*
- **The floor price itself:** no extension, change or court challenge found as of 28 Oct 2026. It runs one year from
  29 Jan 2026. Precedent: the sulfadiazine floor was extended in September 2026.
- A fire stopped the Kakinada plant from April to 29 June 2025. No script change needed.

## Our maths
- **Imports (L22):** US$7.4 bn (NITI, calendar 2025) × ₹87.1468 per dollar (2025 average, Federal Reserve G.5A via FRED) =
  ₹64,489 crore, so "around sixty-five thousand crore".
- **Exports (L16):** FY 2025-26 US$31.12 bn × ₹88.37 (that year's average of the monthly Federal Reserve rates) ≈
  ₹2.75 lakh crore. FY 2024-25 US$30.47 bn × ₹84.56 ≈ ₹2.58 lakh crore. Either way it is "more than two and a half lakh crore
  a year". Caution: the DoP Annual Report counts FY 2024-25 pharma exports as ₹2,45,962 crore (a narrower scope). So no
  precise FY25 rupee figure goes on screen. Use `$31 BN · FY26`.

## Recheck before upload
1. Minimum import price (ends about 29 Jan 2027): extended, changed, or replaced by an anti-dumping duty?
2. Bulk drug parks: has any park started production?
3. Open loop (L11): does the Kakinada section really start around minute eight in the final cut?

## Suggested on-screen tags
`3 MARCH 2020 · DGFT` · `13 INGREDIENTS + THEIR MEDICINES` · `$350 A YEAR · 2001 [MSF]` · `86% · ANTIBIOTIC INGREDIENTS · 2025 [NITI AAYOG]` ·
`UNDER 1% · 1991 [RIS 2021]` · `35–40% CHEAPER [NITI AAYOG ESTIMATE]` · `41 INGREDIENTS · ₹6,940 CRORE` ·
`15,000 TONNES A YEAR` · `₹2,216/KG (CIF) · 29 JAN 2026 [DGFT]` · `ENDS JAN 2027`.

## Sources I could not open (worked around)
CAG's HAL audit (server error; used ISID and DoP instead), the Nehru Archive (blocked; used DoP), eparlib.nic.in (not reachable from
this session), Britannica (blocked; used Healthline and Wikipedia) and the e-Gazette copy of notification 56 (TLS error; used
the signed DGFT scan that LiveLaw hosts).

## Writer's note, narration v4 (2026-10-28, after audience review v2)
Wording-only changes; no new facts. "By the end of the twenty tens" → "By about twenty twenty" (same ISID source); the
anti-dumping case said as "started checking whether China is selling penicillin here below a fair price" (DGTR
initiation, 28 Sep 2026); "Lyfius, a unit of Aurobindo Pharma" → "Aurobindo Pharma, through its unit called Lyfius";
the floor said as "needs a special licence… the same rule covers amoxicillin and its base powder"; new line "Protect the
Indian plant... without making your antibiotics costlier" is our framing of the trade-off, not a factual claim.

## Changed lines, 2026-10-28 (Corona anchor)
Independent light pass on the lines changed in `vo.txt` (now 88 lines): L4, L5, L8, L49, L60, L80. Rows P72–P77 (P76 and
P77 are new). Line numbers in these rows follow the current `vo.txt`; older rows keep the numbering of the version they checked.

**Result: all confirmed. No VO line has to change.** `claims_check.py`: 77 claims, 73 confirmed, 4 claim; gate passed.

- **L4, lockdown "three weeks" later (P72):** the PM ordered the nationwide lockdown on 24 March 2020 (PIB), 21 days after
  3 March. It took effect from 25 March.
- **L5, Wuhan "locked down for six weeks" (P73):** Wuhan closed its outbound routes at 10 a.m. on 23 January 2020 (State
  Council white paper, June 2020). That makes 3 March day 40, or five weeks and five days, so "six weeks" is rounded up by two days.
- **L5, "only a handful of cases" (P74):** India had 5 confirmed cases, 3 of them already recovered (Health Ministry via PIB,
  2 March evening; WHO Situation Report 43, 3 March).
- **L8, "the reason was Corona" (P77):** The Tribune, 3 March 2020: the curbs came "in the wake of coronavirus outbreak",
  on the advice of the pharma department's committee set up after the outbreak.
- **L8, "the whole province was shut down" (P76):** the white paper says all outbound routes from Wuhan and Hubei were
  closed. Hubei's own notice of 24 March 2020 lifted the exit controls for "areas outside Wuhan" only from 25 March. Hubei's
  60 million people were told to stay home on 16 February (BBC). Easing inside the province began only in mid-March (CGTN, 14 March).
- **L49, 1991 "the year India opened up its economy" (P75):** the 24 July 1991 budget speech ("we should welcome, rather than
  fear, foreign investment"; "expose Indian industry to competition from abroad"), backed by the RBI and a Finance Ministry paper.
- **L60, L80, "Corona came" and "one province in China shut down":** the wording stays true (P76, P77). The same Tribune story
  says Chinese ingredient makers outside Hubei had partly restarted by 3 March, which is why "one province" is fair.

**Optional tightening (not required):** L5 "has been locked down for six weeks" → "has been locked down for almost six weeks" (exact).

**Watch-outs for the edit**
- "A handful" is true only on 3 March. India had 29 cases by 4 March (Health Minister in the Rajya Sabha, 5 March 2020).
  If the scene's date moves, re-check this line.
- "Whole province" is right for 3 March. AP's account of late January says the Wuhan restrictions spread to "most of the
  province". By March, the exit controls and the stay-home order covered all of Hubei. P76 replaces P09's "most of the province" note for this line.
- "Had to lock its own doors" (L60, L80) is unchanged framing that already passed under P08. The curb covered about 10% of
  pharma exports, and the government's own panel said stocks could last two to three months.
- Optional tags: `INDIA: 5 CASES · 3 MAR 2020 [WHO]` · `WUHAN LOCKED DOWN SINCE 23 JAN`.

**Sources I could not open (worked around):** Reuters (blocked to this session; used AP and the Hubei notice on Xinhua instead), The
Guardian (fetch failed; not needed), dea.gov.in direct download (TLS certificate error; read the paper through a text extract)
and english.scio.gov.cn over https (certificate mismatch; cited the same white paper PDF on english.www.gov.cn instead).
