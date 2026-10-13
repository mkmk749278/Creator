# Fact-check: The Jet Engine Paradox (script v1, checked 2026-10-13)

`claims.csv`: **66 claims** (the writer's 47 plus 19 new rows, JE-048 to JE-066). 55 confirmed, 3 disputed, 4 unverified,
4 wrong. `python3 scripts/claims_check.py projects/jet-engine-paradox/claims.csv` **fails on 8 rows** (JE-015, 047, 048,
052, 053, 055, 060, 063). It will pass once the script lines below are changed and those rows are updated.

Every quote in `claims.csv` was checked word for word against the page it came from. The writer had four quotes that
were not on the cited page, so I replaced them: GE "Lynn plant" (JE-006), PIB "dry variant" (JE-038), and the Janes
figures behind its paywall (JE-023, JE-025, JE-039). DRDO's website does not load from here, so no tag cites it.

## 1. Lines that must change

VO text is ready to paste. All of it passes `lint_en` from `tools/build_script.py`.

| Line | Problem | New VO / on-screen / tag |
|---|---|---|
| J003 | NavIC **cannot give positioning on its own right now**. Only 3 satellites work and it needs 4 (minister's Lok Sabha reply, Jul 2026). The new satellite, NVS-03, has not launched yet. | VO: `India builds its own nuclear submarines. It reached Mars on its very first try.` On-screen: `NUCLEAR SUBMARINE · INS ARIHANT · MARS ORBITER 2014`. Tag: `[MOD / PIB | ISRO]`. Change the NavIC shot in the visual column too. If you keep NavIC: `It built its own satellite navigation system.` (past tense only) |
| J009 | "the hardest machine on Earth" has no source | `Today, the story of one of the hardest machines on Earth to build.` (rest of the line unchanged) |
| J017 | Out of date. GE has now sent **14** of 99 engines (4 in September). HAL now says **29** jets are built (10 Oct). | VO: `By October twenty twenty six, GE had sent only fourteen of the ninety nine engines. HAL says close to thirty jets are built and waiting.` On-screen: `ENGINES SENT: 14 OF 99 · JETS BUILT: 29`. Tag: `[GE AEROSPACE | NEW INDIAN EXPRESS | HAL CMD | OCT 2026]` |
| J026 | "Many" against "a handful" makes the gap look bigger than it is: 9 countries have nuclear bombs and about 10 have launched satellites on their own rockets | `Nine countries have nuclear bombs. About ten have put a satellite in space with their own rocket.` Tag: `[SIPRI 2026 | AP 2022]` |
| J027 | The list of five sounds complete, but sources also name Ukraine (and Germany, Japan and Italy have partial capacity) | `But only a handful can design and build a modern fighter engine on their own. The main ones are America, Russia, Britain and France. And, after decades of struggle, China.` Tag: `[KED GLOBAL | CLAWS]` |
| J029 | In 1986 there was only a feasibility study and GTRE's proposal. The government sanctioned the project in March 1989 (CAG). | `In nineteen eighty six, Indian engineers began planning their own fighter engine.` Tag: `[CAG | 2010]` |
| J033 | No source for "India's heat and dust" | `The goal was huge. An engine that gives eighty one kilonewtons of push with the afterburner on.` Tag: `[DELHI DEFENCE REVIEW | 2017]` |
| J037 | Sources give 65, about 70, 73 and 78 kN | VO: `It was meant to push eighty one kilonewtons. As reported, it reached only about seventy.` On-screen: `81 kN TARGET · ~70 kN REPORTED`. Tag: `[RAKSHA ANIRVEDA | DELHI DEFENCE REVIEW]` |
| J070 | "Nobody sells it" is too strong, and the film itself later shows Safran and Rolls-Royce offering full transfer | `That knowledge is a closely guarded secret. For decades, no engine maker shared it with India.` Tag: `[CAG 2010 | BUSINESS STANDARD 2009]` |
| J083 | No one ever confirmed which engine the J-20 used on its first flight in 2011. Early J-20s did use Russian engines. | `China walked this same road. Its J twenty stealth fighter used Russian engines at first. It took China decades, and many failures, to switch to engines of its own.` Tag: `[THE DEFENSE POST 2021 | DEFENSE MAGAZINE 2026]` |
| J086 | The metal does not survive above its melting point. The gas is hotter than the metal's melting point, and cooling keeps the metal below it. | `A fighter engine needs metal that lives in gas hotter than its own melting point, spinning, for thousands of hours.` |
| J055 | Same point (recommended) | `The gas is hotter than the metal's melting point. And still the blade does not melt. How?` |

**Tag-only fixes** (the tag must name the source we actually used):
J002 `[GOVT OF INDIA | AP | 2023]` · J007 `[GE AEROSPACE | OUR CALCULATION]` (13,065 km, re-run) ·
J011 `[THE WIRE | NEW INDIAN EXPRESS | 2026]` · J015 `[BLOOMBERG | GE AEROSPACE]` · J016 `[BLOOMBERG 2024 | NEW INDIAN EXPRESS 2026]` ·
J018 `[TIMES OF INDIA | NEW INDIAN EXPRESS | 2026]` · J022 `[US CONGRESS CRS | 2002]` · J023 `[AEROSPACEWEB | BUSINESS STANDARD]` ·
J024 `[BUSINESS STANDARD | THE TRIBUNE]` · J030 `[CAG | JANE'S]` · J035 `[CAG | 2010]` · J036 `[CAG | 2010]` (report tabled Aug 2010, not 2011) ·
J038 `[BUSINESS STANDARD 2009 | PIB 2015]` · J041 `[SPS AVIATION | CAG 2010]` · J042 `[DRDO 2010 | PIB 2012]` · J047 `[ISRO | NASA]` ·
J057, J058, J059 `[UNIV. OF CAMBRIDGE]` · J060 `[UNIV. OF CAMBRIDGE | PIB 2021]` · J072 `[JANE'S | PIB]` · J073 `[ORF | THE WEEK | 2026]` ·
J074 `[PIB 2025 | ORF 2026]` · J077 `[IANS | 2025]` · J078 `[NEW INDIAN EXPRESS | META-DEFENSE | 2026]` · J082 `[NEW INDIAN EXPRESS | AUG, OCT 2026]`.
These factual lines have no tag yet, so add one (charter rule): J005 `[HAL CMD | 2026]`, J052 `[NASA | ROLLS-ROYCE]`, J062 to J064 `[NASA | UNIV. OF CAMBRIDGE]`,
J068 `[PIB | 2021]`, J076 `[PIB | 2021]`.

**Optional wording, more precise:** J005 `Painted. Radars fitted. Almost ready.` (radar software and missiles are still
pending) · J034 `Both almost from scratch.` · J047 `A rocket engine fires for minutes, not hours.` (Chandrayaan-3's upper stage
burned about eleven minutes) · J085 `Reaching the Moon needs rocket engines that work perfectly, but only for minutes at a time.` ·
J088 `Today, the Dry Kaveri is heading for certification, ...` (its trials in Russia are done).

## 2. Fine as written
Chandrayaan-3 date and first landing near the south pole; INS Arihant built in India; Mk1A jets in Bengaluru and Nashik;
zero Mk1A delivered (as of 13 Oct); Lynn and about 13,000 km; 42 sanctioned and about 29 squadrons; MiG-21 retired 2025;
the 83 + 97 orders; F404-IN20; engines due from 2023, first one March 2025; GE blamed its supply chain and HAL imposed
penalties; radar and missile work pending; Pokhran 11 and 13 May 1998; Glenn Amendment; F404 and Lockheed help cut off,
India built its own flight controls; sanction March 1989 at ₹382.81 crore, due December 1996; weight 1,235 kg against
1,100 (CAG); tests in Russia; delinked September 2008; Il-76 flight 2010 (first flight 3 Nov 2010); 27 flights, 57 hours,
12 km; ₹1,996 crore spent and ₹2,839 crore estimate; the Rolls-Royce lines (200 degrees, 12,000 rpm, London bus);
crystals, creep, rhenium, cooling and the ceramic coating; Dry Kaveri 48.5 kN against a 46 kN target; Dry Kaveri for
Ghatak; DMRL Hyderabad's 60 blades (2021); AMCA Mk1 on the F414; the 120 kN Mk2 engine; Safran picked in August 2025;
India wants full IP; deal still awaiting CCS; Rolls-Royce and Reliance in August 2026.

**For the description:** the CAG gives 1,235 kg, but GTRE's director said 1,265 kg in 2009. Reported Kaveri afterburner
thrust ranges from 65 to 78 kN. Ukraine also builds jet engines. PIB dates the 83-jet contract January 2021, while The
Hindu says February. Rolls-Royce's blade figures are for its big civil engines.

## 3. Re-check right before render (fast-moving news)
- **J006 "not one Mk1A has joined":** IAF and HAL hold the final review after 15 Oct, and a handover could follow within weeks.
- **J017 engine and jet counts:** GE reports each month's shipments early the next month, and HAL expects 22 engines in total by December. HAL's built count is 29 as of 10 Oct.
- **J082 Safran-GTRE "awaiting final approval":** the CCS could clear it any week. It was still pending as of 6 Oct (New Indian Express), with nothing newer found up to 13 Oct.
- **J073, J074, J088 Dry Kaveri:** CEMILAC certification is the next step.
- **J011 squadrons:** the IAF chief retires on 31 Oct, so new figures may come out.
- **J003, only if NavIC stays:** NVS-03 is due to launch 15 to 20 Oct, and the service is not restored until it works.

After the edits, check only the changed lines again (PLAYBOOK §12). Update rows JE-015, 020, 021, 025, 047, 048, 052,
053, 055, 060 and 063 to the new wording and run the gate again.
