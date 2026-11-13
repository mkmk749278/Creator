# Word map · India Had a Catapult in 1961. Why Not Now? (PLAYBOOK §9.5, §9.10)

Times come from the locked audio r2 (`vo/timing.json`, 644.15 s, SHA-256 f416a57d…; approved 2026-11-13, the four lorry paragraphs re-recorded the same day on the owner's instruction). `S#` = sentence
id in `timing.json` (0-based). The base shot carries the sentence; `→ word` = a cutaway or new element landing on that
word (within 100 ms; cutaways start 0.15 s before). Idea level per row (§9.10): **L** literal, **P** physical (the
cause shown happening, the number at human scale), **F** felt. Every chapter's turn and payoff is P or F.

**Sources.** **H3/H4** = Blender Cycles heroes (`scripts/blender/catapult_hero.py`: store; catapult, drum, room), Drive `renders/`, frame 0 = the row's start. (H1 was dropped on 2026-11-13: the Navy's footage shows the deck better, and the morph and cutaway are clearer as **R** drawings.)
**T** = Three.js in Remotion. **R** = Remotion drawing on a physical base (drafting grid, steel inspection plate, sea
chart). r1 clips (Drive `footage/`): **LAND** the Navy's Rafale M landing, 29 Oct 2026 (as carried by ANI / NDTV /
India Today; credit "Indian Navy"), **EMF** the US Navy's EMALS film (public domain), **CGTN** Fujian's catapult test
(short credited excerpt). r2 clips (`footage_requests.md`, requested 2026-11-13): **SH** Sea Hawks on the first
Vikrant, **AL** Alizés on the first Vikrant, **W71** the Navy in the east, 1971, **GOA** the Rafale M ski-jump demo,
Goa 2022, **MIG** MiG-29Ks on the new Vikrant (Navy footage, PM's channel), **TRAP** a MiG-29K trap landing on Vikrant,
**EM12** the first EMALS launch, 2012 (US Navy), **FORD** Ford launches, **KJ** Fujian's first KJ-600 launch.
**STOCK** = Pixabay API (licence-clean, logged in `media_manifest.csv`). **D** = a document on the drafting table (one
document pose for the film: the page slides in at 12°, settles flat, a soft lamp; the line in it lights on its word).
Exact clip spans are chosen on the contact sheets after the fetch and logged in `media_manifest.csv`.

**Labels.** ILLUSTRATION on every H, T and R that shows a real ship, jet or machine; SIMPLIFIED on the steam catapult,
the unrolled motor, the travelling wave and the hull cutaway; OUR CALCULATION with the working on S109–117, S163,
S179; AS REPORTED on S156, S164, S175; SOURCE: US DOT&E on S140–142; SOURCE: programme count on S145. ILLUSTRATIVE
FOOTAGE on any stock that stands in for a real moment.

## Art direction
- **Sea daylight and warm brass,** never the navy-black of defence channels. The present is real Navy footage in
  daylight; 1961–71 is warm monochrome archive laid on the drafting table beside the official history's pages; the
  mechanism is cutaways lit from inside on the steel inspection plate.
- **Colour means something:** caution yellow = the catapult slot (the motif); amber = steam and pressure; copper =
  the electric coils; cyan = measured data (DOT&E, the programme count); **signal red only for the power spike**;
  green only on what India already has (the landing's last frame).
- **The motif: the slot.** A thin caution-yellow line in a deck. (1) S2–3 it draws down Vikrant's deck and stops dead
  at the ramp. (2) S45 the real 1961 slot, steam rising. (3) S96–101 we go down into it: coils. (4) S154–163 seventeen
  metres of it, DRDO's test model, laid beside the ninety it must become. (5) S202 and S204 it runs on, to a dotted ship.
- **Sound motif: three seconds** (whine, thump, open wind): S10 unexplained; S50 as steam hiss and clang; S103–106 in
  full, the count spoken; S156 small and thin; S202 the whine starts and cuts to silence before the thump.
- **Type:** Inter Tight 800 caps for labels (≥ 44 px where the voice points to it), JetBrains Mono for numbers; ₹ with
  Indian grouping; dates day-first. Text never over 15 % of the frame.
- **Real Indian people in every chapter:** sailors and the landing crew (open, ch1, landing); 1971 archive (ch2); a
  family at home under the fan, a hand on the meter (ch3); Vikrant's deck crew watching (ch4 turn); DRDO's
  engineers in Pune, if a real photo is found; otherwise the drawn test model (ch5).

## Cold open (0:00–0:50)
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 0–1 | 0.00–8.36 | **LAND** the Rafale M on approach over the sea, then the hook, the wire, the stop (this frame = the thumbnail's subject); real deck sound, no music | "twenty-ninth of October" → date 29 OCT 2026 (Mono, small, lower left); "Rafale" → name tag on the jet; "I-N-S Vikrant" → the deck crew run in (the same clip) | L |
| 2 | 8.79–13.64 | **LAND** last frames, the camera settles on the empty deck ahead of the jet | "missing something" → **the slot draws:** a caution-yellow line runs down the real deck ahead of the jet… | P |
| 3 | 14.15–14.87 | (cont.) | "A catapult." → …and stops dead at the foot of the ramp. Hold, wind only | F |
| 4 | 15.28–18.04 | **EMF** a jet thrown off a catapult deck, real speed | "thrown off a ship" → the launch on the word | L |
| 5–7 | 18.45–23.85 | **LAND** 20–22 s Vikrant's bow and ramp, sailors lining the deck → **LAND-NDTV** the Rafale M leaving Vikrant's ramp (the Navy's footage, framed as an inset on the drafting table: the only copy is soft) → **R** India's map (official boundary), a pin | "ramp" → the bow rises into frame; "leave by that ramp" → the Rafale lifts off the lip; "Goa" → pin GOA, label SHORE RAMP TRIALS, 2022 (no real footage of the Rafale there: the compilation's shots are animation) | L |
| 8 | 24.25–25.16 | **match cut:** the Rafale's nose wheel on Vikrant (LAND) | "think about this" → hold on the wheel | — |
| 9 | 25.48–29.33 | **SH** a Sea Hawk's nose wheel on the 1961 deck, the same framing (the match cut lands on "Sixty-five") | "Sixty-five years ago" → 1961 (Mono); "throwing jets" → the Sea Hawk goes off the catapult | F |
| 10 | 29.73–36.00 | **R** on the drafting grid: Vikrant's deck plan, the slot drawn to the ramp and stopping | "wants a catapult again" → the slot glows; "a small test model" → a tiny yellow track drawn beside the deck plan, at true scale against it (the size is kept for ch5); the 3-second motif, unexplained | P |
| 11–15 | 36.66–50.66 | **EMF** a launch slowed to half speed; a home electricity meter ghosts over the deck, its disc turning | "two hundred rupees" → ₹200 (Mono, caution yellow) over the meter; "hardest machines on earth" → the meter disc spins to a blur and the launch snaps to real speed; "see why" → whine cut to wind | F |

## Ch1 · What the ramp costs (0:50–1:59) · device: the viewer on the deck
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 16 | 51.10–53.08 | **TRAP** 1.5–3.5 s the view down Vikrant's deck from the island, R11 on its side, a slow push in | "stand on Vikrant's deck with me" → the push begins | L |
| 17 | 53.44–58.01 | **STOCK** a real Indian flyover's rising end against the sky (Mumbai or Bengaluru) → **match cut** to LAND 20–22 s the bow ramp's curve against the sky, matched in angle | "curves upward" → the flyover lifts; "ends in the sky" → the cut lands: the ramp's lip against open sky | P |
| 18–22 | 58.36–68.34 | **LAND-NDTV** the ramp's steel side, close (framed inset), then **R** the ramp in side elevation on the drafting table, no moving parts drawn | "any moving parts" → the camera searches the surface; "None" → hold; "opens its engines" → **MIG** the take-off from the deck edge; "throws it up" → the jet lifts off the lip; "break" / "repair" → back on H1, a bare weld seam, no machinery | L |
| 23 | 68.70–71.10 | **MIG** the deck crew's thumbs-up after a launch | "clever idea" → hold on the crew | F |
| 24–27 | 71.43–81.49 | **set piece: the balance.** **STOCK** a kirana shop's brass balance on a counter; **R** overlay: one pan JET, the other FUEL and WEAPONS | "lift itself" → the jet pan sinks; "take off lighter" → weights come off the other pan; "less fuel" → a fuel can lifts away; "fewer weapons" → a missile weight lifts away; "or both" → both | P |
| 28–30 | 81.82–86.67 | (cont.) the balance; one pan left **empty and unlabelled** | "How much lighter?" → a "?" weight hovers; "not published" → it fades; "won't invent one" → the pan stays empty, hold | F |
| 31–32 | 87.04–93.21 | **R** on the sea chart: a heavy, slow aircraft silhouette rolling at the ramp's lip | "heavy, slow aircraft" → the silhouette swells; "off a ramp at all" → it rolls over the lip and drops out of frame | P |
| 33–35 | 93.52–101.90 | **R** the ship on the sea chart, seen from above | "flying radar" → a radar plane silhouette with its dish; "sees trouble long before" → a wide radar circle opens far past the ship's own small circle; a contact blips at the edge | P |
| 36–38 | 102.23–110.98 | **STOCK/F** a Navy helicopter over the sea (Ka-31 if the r2 clips carry one; else a credited still) → R the two circles | "helicopter" → the helicopter; "It works" → its circle; "as well as a plane" → the plane's circle opens beyond it, the helicopter's stays smaller, SIMPLIFIED | P |
| 39–41 | 111.32–120.08 | **LAND** the bow ramp from the deck, a slow pull back | "the ramp has a price" → the empty pan from S30 ghosts on the deck, 1 s; "the catapult we already had" → dissolve to SH the 1961 deck, steam at the slot; "let it go" → the archive frame fades to monochrome | F |

## Ch2 · The catapult India had (1:59–4:41) · device: one object followed (the boiler drum)
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 42–44 | 120.56–131.01 | **SH/AL** the first Vikrant (R11) in archive, warm monochrome, laid on the drafting table beside the GlobalSecurity page (Drive `cowork/docs/R 11 Vikrant.pdf`); no usable Belfast photo exists (Antigravity, 2026-11-13) | "Belfast" → place tag BELFAST; "fourth of March, nineteen sixty-one" → 4 MARCH 1961; "bought from Britain" → a shipyard archive frame; "Her name, too, is Vikrant" → the ship's name on the hull, light catches it | L |
| 45 | 131.35–133.65 | **SH** the 1961 deck, steam rising from the slot | "under her deck" → the camera tilts down into the slot (motif 2) | L |
| 46–49 | 134.03–143.62 | **STOCK** an Indian kitchen, a pressure cooker on a gas flame | "pressure cooker" → the cooker; "Steam builds up" → the weight trembles; "it goes with force" → **match cut:** the whistle's burst → steam bursting from the deck slot (SH) | P |
| 50 | 143.89–149.68 | **H4** cutaway under the 1961 deck: cylinder, piston, slot, SIMPLIFIED | "drives a piston" → the piston fires down the tube; "drags the jet" → the shuttle pulls a Sea Hawk silhouette above; the motif as steam hiss and clang | P |
| 51 | 149.98–151.64 | **SH/AL** launches, years passing (three quick launches) | "nine years" → 1961 → 1970 ticks (Mono) | L |
| 52–56 | 151.92–165.09 | **H4** the water drum in the boiler, warm light; the camera closes in | "June nineteen seventy" → JUNE 1970; "Bombay" → BOMBAY; "cracks" → one crack line glows; "Not one crack" → a second; "Many" → the drum crazes with lines; "cannot weld them" → a welding arc touches and fails; "not possible in India" → **D** the official history's line lights | P |
| 57–59 | 165.55–176.88 | **T** steam splitting two ways from the boiler: to the propeller shafts and to the slot | "turns the propellers" → the shafts turn; "fires the catapult" → the slot flares; "Arun Prakash" → name tag ADM. ARUN PRAKASH (quote attributed); "blow up" → the gauge needle swings to red and the frame shudders once | P |
| 60 | 177.32–178.75 | **H4** the cracked drum, still | "send that ship to war?" → hold, silence | F |
| 61–64 | 179.16–189.00 | **R** the ship on the sea chart, its wake short | "fourteen knots" → 14 KNOTS; "twenty-six kilometres an hour" → 26 KM/H; "Too slow" → the wake stops growing; "leave her out" → the ship's outline dims toward harbour | P |
| 65–66 | 189.45–198.84 | **D** archive photo of Admiral Nanda (official, credited) on the table; his words beside it | "Admiral Nanda" → name tag; "will not have it" → the photo settles flat; "white elephant" → the phrase lights in the page | L |
| 67–69 | 199.22–207.34 | **H4** down the ladder into the engine room, one bulb; → **D** his official portrait (PIB release 1988336, Government of India; credit PIB), small tag PHOTO: LATER YEARS | "engine room" → the camera descends; "Commander Benoy Roy Chowdhury" → name tag CDR BENOY ROY CHOWDHURY; "Bilu" → BILU, softly under it | F |
| 70–74 | 207.70–223.56 | **set piece: the bands.** **H4** the drum; steel bands go on, one by one; then the boiler room left empty, one gauge | "no spare" → the empty cradle beside it; "steel bands" → band one ratchets tight, two, three; "safety valves" → a valve's spring is turned; "almost empty" → the camera pulls back through an empty room; "superheated steam" → a breath of steam across the lens | P |
| 75 | 224.05–224.72 | **H4** the gauge needle, steady | "It holds." → the needle holds; 1.5 s silence | F |
| 76 | 225.04–231.67 | **SH** Sea Hawks off the catapult → **W71** the east, 1971 | "fourth of December, nineteen seventy-one" → 4 DEC 1971; "leave Vikrant's catapult" → the launch (motif: steam, clang); "Cox's Bazar" → **R** sea chart of the Bay of Bengal, an arrow to COX'S BAZAR (India's official boundary); music lifts once | F |
| 77 | 231.99–237.22 | **D** the Vir Chakra (the medal's official image) on the table beside the bands | "Vir Chakra" → the medal; "for bravery" → hold | F |
| 78–79 | 237.50–243.67 | **H4** the banded drum, slow orbit, warm | "steel bands" → the bands catch the light; "took it to war" → dissolve to SH, a launch at sea | F |
| 80–83 | 244.07–259.93 | **F** a Sea Harrier (credited archive) → **AL** an Alizé on the catapult → **R** side elevation of the first Vikrant on the drafting table: the yellow slot seals and the bow line lifts into a ramp (SIMPLIFIED) | "Sea Harrier" → the Harrier rises straight up; "needs no catapult" → its pad, no slot; "old propeller planes" → the Alizé; "nineteen eighty-nine" → 1989; "catapult came out" → the slot seals; "a ramp went on" → the bow rises (P) | P |
| 84–89 | 260.28–276.36 | **LAND** the new Vikrant at sea → **R** the hull in side cutaway on the drafting table, SIMPLIFIED | "made sense then" → hold; "new Vikrant" → the ship; "gas turbines" → four turbines light in the cutaway; "no steam" → a dry pipe, no steam; "no room under that ramp" → the space under the ramp fills, full, as the analysts' view (tag: NAVAL ANALYSTS) | P |
| 90–91 | 276.79–282.12 | **TRAP** the deck from the island; **R** a faint dotted line where a slot would be | "steam is gone" → the last wisp clears; "electricity" → a single copper spark runs along the empty line | P |

## Ch3 · Three seconds (4:41–6:25) · device: the real-time count
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 92–93 | 282.51–285.04 | **STOCK** an Indian family's front room in the evening, a man looks up; the ceiling fan turning | "ceiling fan" → the fan; "what turns it?" → push in to the hub | L |
| 94–95 | 285.36–291.38 | **T signature S1, part 1:** the fan's motor (no brand) on the drafting table, copper coils lit warm | "induction motor" → the casing lifts away; "coils of wire in a circle" → the coils glow; "chases round and round" → a light runs round the ring | P |
| 96–97 | 291.68–299.75 | **T S1, part 2:** the ring opens along a seam and unrolls flat into a long straight line, which drops into a deck slot | "cut that circle" → the seam opens; "unroll it flat" → the unroll; "about a hundred metres" → the line runs out to the horizon, ~100 M; "under the deck" → it settles into the slot (motif 3) | P |
| 98–99 | 300.08–305.07 | **T** the line in the slot, a jet's nose wheel on the shuttle | "no longer goes round" → the light stops circling; "runs straight ahead" → it runs down the line; "takes the jet with it" → the shuttle moves | P |
| 100–101 | 305.38–310.38 | **T** the trough from above, SIMPLIFIED | "Only the coils beside the jet" → only a short lit patch under the shuttle; "racing down the deck" → the patch races ahead | P |
| 102–106 | 310.69–322.08 | **set piece S2:** split frame. Left: **FORD/EM12** a real launch in real time. Right: a home meter on a wall | "Now count with me" → whine starts; "One" → ONE (Mono, huge), the jet moves; "Two" → TWO; "Three" → THREE, the thump, the jet is gone, open wind; "thirty-tonne fighter" → 30 T; "standing still" → 0 KM/H; "two hundred and forty kilometres an hour" → 240 KM/H | F |
| 107–111 | 322.57–337.91 | **R** the working on the steel plate, OUR CALCULATION: ½ × 30,000 kg × (66.7 m/s)² ≈ 67 MJ → ÷ 3.6 → 19 UNITS | "nineteen units" → 19 UNITS; "average Indian home" → **STOCK** the family under the fan; "six days" → a wall calendar flips six days; "two hundred rupees" → a bill: UNDER ₹200 (≈ ₹120 at ₹6.5 a unit, small) | F |
| 112–115 | 338.26–347.81 | **R** two meters side by side: the home's and the catapult's | "three seconds" → 3 S; "sips that energy over six days" → the home meter crawls; "pour it out in three seconds" → the catapult meter empties in one sweep | P |
| 116–117 | 348.07–354.83 | **R** Vikrant's four engines as four blue bars, 22 MW each (88 MW); OUR CALCULATION | "close to fifty megawatts" → a **signal-red** spike rises past two whole bars and into the third: 49 MW; "all four of Vikrant's engines" → the four bars glow, 88 MW; the ship's own lights dip on the spike | P |
| 118–122 | 355.18–372.17 | **H3** the motor generators on the steel plate under warm light | "No." → the bars go dark; "save up" → the rotors start; "over thirty-six tonnes" → 36 T on one machine; "giant spinning tops" → **STOCK** a child's lattu spinning on a floor, match-cut to a rotor; "pull the energy back out" → the rotors slow as a launch fires (EMF) | P |
| 123 | 372.45–377.90 | **FORD** launch after launch, a clock | "every forty-five seconds" → 0:45 timer loops; "for years, on a ship at sea" → the ship rolls in a swell | P |
| 124–126 | 378.25–384.81 | **H3 → T** pull back from the rotors to the whole system under the deck, glowing once, then dark | "Not a motor" → the coils dim; "A power station" → the whole system lights; "three seconds at a time" → it flashes for three seconds and goes dark | F |

## Ch4 · The newcomer and the inventor (6:25–7:48) · device: a reversal
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 127–129 | 386.20–391.77 | **R** on the sea chart: two flags' ships set at opposite edges, arrows pointing opposite ways | "Two navies" → both appear; "opposite directions" → the arrows swing apart | P |
| 130–132 | 392.16–400.93 | **R** a full-length land track drawn on the grid, a test jet on it (ILLUSTRATION; China's satellite-reported land catapults) | "never sent a steam catapult" → a steam slot crossed out; "From twenty sixteen" → 2016; "built on land" → the track draws at full length (set piece) | P |
| 133–137 | 401.27–417.60 | **CGTN / KJ** Fujian's launch (short credited excerpt) | "November twenty twenty-five" → NOV 2025; "Fujian" → name tag; "flying radar plane" → **KJ** the KJ-600 off the catapult, its dish; "not nuclear powered" → NOT NUCLEAR; "stored power" → H3 rotors, 1 s | L→P |
| 138–143 | 418.05–436.46 | **FORD** the ship → **R** two cyan bars on one scale against a target line, SOURCE: US DOT&E | "U-S-S Ford" → name tag; "more than four thousand launches" → the target line at 4,166; "one hundred and eighty-one" → bar 1 (2020): 181; "six hundred and fourteen" → bar 2 (2022): 614; "Far short" → the gap to the line glows | P |
| 144–147 | 436.81–448.41 | **FORD** launches, a counter running (SOURCE: programme count) | "did not stop flying" → launches; "thirty-six thousand" → the counter lands on 36,863; "many decades" → a steam catapult archive frame; "still young" → back to the young machine's launch | P |
| 148–150 | 448.73–462.25 | **D** the White House memorandum, 13 Aug 2026, on the drafting table | "this August" → 13 AUG 2026; "back to steam" → the line lights; "think again" → the maker's statement slides in beside it; "nothing final" → both pages hold, no stamp | L |
| 151–152 | 462.54–468.38 | **MIG** Vikrant's deck crew watching a launch | "two minds" / "already flying" → the two ships from S127; "Where does that leave India?" → cut to the crew, hold | F |

## Ch5 · Four hundred kilos (7:48–9:32) · device: the Kishore moment
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 153 | 468.74–475.09 | **R** India's map (official boundary), a pin | "Pune, in Maharashtra" → PUNE, MAHARASHTRA; "D-R-D-O laboratory" → DRDO R&DE(E); "India's own electric catapult" → **STOCK** Indian engineers at a lab bench with coils (ILLUSTRATIVE FOOTAGE; no DRDO photo of the work exists) | L |
| 154–157 | 475.47–489.60 | **R** our drawing of DRDO's test model on the drafting table, labelled ILLUSTRATION (no photo exists: Janes and DRDO's clippings show only a railgun at Aero India 2025) | "Remember that small test model?" → the tiny track from S10 slides in and grows to fill the frame; "This is it" → push in; "four hundred kilos" → 400 KG; "seventeen metres" → 17 M; AS REPORTED on both; "very little" → hold; the motif small and thin | L |
| 158–163 | 489.87–500.86 | **signature S3:** **R/T** one continuous pull-back, no cut: tight on the test model's 17 m track, the 90 m deck track draws out past it, a Rafale M settles on it, one scale | "Not four hundred kilos" → 400 KG; "Thirty tonnes" → the Rafale drops onto the track, 30 T; "Not seventeen metres" → 17 M; "About a hundred" → the long track finishes drawing; "seventy-five times the weight" → ×75 (OUR CALCULATION); the 17 m track stays in the corner, small | P |
| 164 | 501.21–506.37 | **D** the press line, attributed | "decade or more" → the phrase lights; AS REPORTED | L |
| 165–167 | 506.81–513.14 | **STOCK** an Indian engineer's hands winding a coil at a bench (ILLUSTRATIVE FOOTAGE), slow push | "who is stopping India" → hold; "Nobody" → hold; "Nobody is stopping us" → push in, warm | F |
| 168–170 | 513.50–521.58 | **R** split: China's full land track and a ship waiting / India: an empty grid and a dotted ship | "full-size test track on land" → China's track lights, India's grid stays empty; "a ship waiting" → China's ship solid, India's dotted | P |
| 171–173 | 521.96–533.47 | **D** the Navy's 15-year plan page → **R** a ship outline with a ramp | "fifteen-year plan" → the page; "two electric catapults" → two slots light on a dotted ship; "forty thousand crore" → ₹40,000 CRORE; "repeat of Vikrant" → the ramp ship solid; "With a ramp" → the ramp, hold | P |
| 174–179 | 533.85–555.25 | **D** the 2017 reports, then the US notice for France | "twenty seventeen" → 2017; "Nothing was signed" → an unsigned line; "France" → the notice; "one point three billion dollars" → $1.3 BILLION; "eleven thousand crore" → ≈ ₹11,000 CRORE (rate on upload day, OUR CALCULATION); "before you build the ship" → a ship outline, empty | L |
| 180–185 | 555.60–571.87 | **R** three items on the drafting table: a Rafale (ticked), a small test track, a dotted ship | "jets are ordered" → tick; "Twenty-six Rafales" → 26; "sixty-three thousand crore" → ₹63,000 CRORE; "a small test model" → the short track, small; "not approved" → the dotted ship; "fly from ramps" → **GOA** the Rafale off the ramp | P |

## Landing (9:32–10:43)
| S | Time | Base | → word | Idea |
|---|---|---|---|---|
| 186–188 | 572.24–581.74 | **MIG** Vikrant at sea, sailors on the deck → **H4** the bands, 2 s → **MIG** the ship | "what India does have" → sailors; "cracked boiler" → the bands; "designed and built the new Vikrant itself" → the ship at sea, wide | F |
| 189 | 582.04–586.55 | **R** three empty slots on the drafting table filling: DECISION · TEST TRACK · 10 YEARS | each word lights its slot | P |
| 190–192 | 586.88–597.16 | **R** India's map (official boundary): submarines, the Army | "submarines" → a submarine silhouette; "the Army" → a land unit; "the ship still waits" → the dotted ship, hold | L |
| 193–196 | 597.49–606.97 | callbacks: the fan (S92) → the meter and calendar (S110) → the count (S105) | "ceiling fan" → the fan; "six days of your home" → the calendar; "three seconds" → THREE, the thump | F |
| 197–198 | 607.29–609.89 | **LAND** the Rafale on Vikrant's deck, the slot from S3 stopping at the ramp | "You can buy the jet" → the jet; "build the throw" → the slot glows; 1 s silence | F |
| 199–202 | 610.33–621.86 | **R** three dates to watch on the drafting table | "the next carrier" → NEXT CARRIER: DECISION; "twenty twenty-nine" → FIRST INDIAN RAFALE M ≈ 2029; "that test model in Pune" → the short track; "something heavier" → the whine begins and cuts to silence before the thump | P |
| 203–206 | 622.27–636.66 | **LAND** the deck with the Rafale; **R** the yellow slot runs on past the ramp to a dotted ship (motif 5) | "subscribe" → subscribe line; "open up that deck together" → the camera drops into the slot; "a ramp, or a catapult?" → the two ship outlines, side by side | F |
| 207–210 | 637.02–643.94 | the end screen → the AIP submarines film; the channel sting | "A submarine" → the next film's frame; "Stay practical" → the logo sting (outro only) | — |

## Still to settle before building
- Exact spans from r1 and r2 after the fetch (contact sheets, `media_manifest.csv`).
- Stills (Antigravity, 2026-11-13, Drive `footage/cowork/stills/`): Cdr Roy Chowdhury's official portrait and the
  Vir Chakra handover photo (PIB, usable with credit). The two IWM Sea Hawk photos are under IWM's **non-commercial**
  licence: design reference for H4 only, never in the film. Not found: the Belfast commissioning, any DRDO launcher
  photo (the Aero India 2025 trailer was a railgun: Janes, 14 Feb 2025, and DRDO's own clippings).
- Stock via the Pixabay API: an Indian flyover's end, a kirana balance, a pressure cooker, a family under a ceiling
  fan, a home meter, a wall calendar, a lattu.
- Hero renders: H3 (the motor generators), H4 (steam
  catapult cutaway, the drum, the bands, the empty boiler room).
