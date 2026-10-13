#!/usr/bin/env python3
"""One-time authoring helper: writes script.full.tsv from the rows below (v1, 2026-10-13).

After this first write, script.full.tsv is the single source; edit it directly and run tools/build_script.py.
The narration is the owner's brief (brief/owner-brief.pdf) rewritten into the channel's simple Indian English
(PLAYBOOK §4a-2) with facts corrected from the writer's research (claims.csv). Every change from the brief is listed in
brief/changes-from-brief.md.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
COLS = ["id", "section", "te", "en", "emotion", "visual", "onscreen", "sound", "pacing", "cite"]

H, A1, A2, A3, A4, V = ("0 Hook", "1 The chokepoint", "2 The ghost of Kaveri", "3 The physics of hell",
                         "4 The turning point", "5 Verdict")
# (id, section, VO, visual, on-screen text, sound, pacing, cite tag)
ROWS = [
    ("J001", H, "August twenty three, twenty twenty three. India lands a spacecraft near the south pole of the Moon.",
     "REAL: ISRO Chandrayaan-3 landing-day footage: Vikram lander camera descent frames, then the ISTRAC control room erupting.",
     "MOON · SOUTH POLAR REGION · 23 AUG 2023", "Cold open: room tone of mission control, no music for 2 s", "Cold open",
     "[ISRO | CHANDRAYAAN-3]"),
    ("J002", H, "No country had ever landed there before.",
     "REAL: ISRO lander image of the lunar surface; slow push-in.", "", "Low sub-bass swell", "", "[ISRO | 2023]"),
    ("J003", H, "India builds its own nuclear submarines. It runs its own satellite navigation system.",
     "REAL: INS Arihant at sea (Indian Navy / Commons); cut to NavIC satellite animation over India (ISRO).",
     "NUCLEAR SUBMARINE · INS ARIHANT · NAVIC", "", "Montage, 3 s per shot", "[INDIAN NAVY | ISRO]"),
    ("J004", H, "And yet... in hangars in Bengaluru and Nashik, brand new fighter jets are waiting.",
     "REAL: HAL Tejas Mk1A on the line at Nashik / Bengaluru (HAL, PIB, MoD photos), parallax push; ILLUSTRATION wireframe "
     "of the empty engine bay glowing amber.", "TEJAS MK1A · HAL", "Hard audio stop on 'And yet', then hangar ambience",
     "Music out for 1.5 s before 'waiting'", "[HAL | 2026]"),
    ("J005", H, "Painted. Radars fitted. Ready on paper.",
     "Three macro cuts: grey paint, radome, cockpit canopy (HAL / Aero India photos, animated).", "", "Three metallic ticks", "", ""),
    ("J006", H, "But not one of these new jets has joined the Air Force yet.",
     "Wide of the line of jets; counter in lower corner: DELIVERED TO IAF 0.", "MK1A JETS DELIVERED TO IAF: 0",
     "Low thud", "", "[HAL | THE HINDU | OCT 2026]"),
    ("J007", H, "The biggest reason? They are waiting for an engine. An engine made in Lynn, Massachusetts, about thirteen "
     "thousand kilometres away.",
     "Kinetic globe (land only, no borders): an amber arc from Lynn, USA to Bengaluru; distance counter runs up.",
     "LYNN, USA → BENGALURU · ~13,000 KM", "Whoosh along the arc", "", "[GE AEROSPACE | HAL]"),
    ("J008", H, "So here is the question. India landed on the Moon. Why can it not build its own fighter jet engine?",
     "Split frame: Moon landing on the left, empty engine bay on the right; the title burns in between.",
     "INDIA LANDED ON THE MOON. WHY NOT A JET ENGINE?", "Braam", "Thumbnail promise by 0:30", ""),
    ("J009", H, "Welcome to Be Practical with Kishore. Today, the story of the hardest machine on Earth to build. "
     "Single crystal metal, broken promises, and a forty year fight to join one of the world's most closed clubs.",
     "Logo sting, then title card over a macro of a glowing turbine blade: THE JET ENGINE PARADOX.",
     "THE JET ENGINE PARADOX", "Logo sting; music bed enters", "Logo sting on the channel name", ""),

    ("J010", A1, "To understand why one engine matters so much, look at the Indian Air Force.",
     "REAL: IAF fighters on a flight line, heat shimmer (IAF / Commons B-roll).", "", "", "Chapter 1 card in lower third",
     ""),
    ("J011", A1, "The Air Force is supposed to have forty two fighter squadrons. Today it has about twenty nine.",
     "Animated squadron gauge: 42 outlined slots, 29 fill in amber, 13 stay empty and pulse red.",
     "SANCTIONED 42 · ACTUAL ~29", "Gauge ticks", "", "[IAF CHIEF BRIEFING | THE WIRE | 2026]"),
    ("J012", A1, "Old jets like the MiG twenty one have retired. New jets are needed, fast.",
     "REAL: MiG-21 final flypast / retirement ceremony 2025 (credited excerpt or Commons).", "MIG-21 RETIRED · 2025", "",
     "", "[IAF | 2025]"),
    ("J013", A1, "So in twenty twenty one, the government ordered eighty three Tejas Mark One A jets from Hindustan "
     "Aeronautics, HAL. In twenty twenty five, it ordered ninety seven more.",
     "REAL: contract signing photo (PIB) with forensic magnifier on the figure; counter 83 → 180.",
     "83 + 97 = 180 JETS", "Two stamp hits", "", "[MOD / PIB | 2021, 2025]"),
    ("J014", A1, "But HAL does not make the engine. Every one of these jets uses the F four zero four, made by GE "
     "Aerospace in America.",
     "REAL: GE F404 engine photos (GE press media / Commons), slow orbit parallax; ILLUSTRATION exploded view.",
     "ENGINE: GE F404-IN20 · MADE IN USA", "", "", "[GE AEROSPACE]"),
    ("J015", A1, "The engines were due from twenty twenty three. The first one came only in March twenty twenty five.",
     "Kinetic timeline: 2023 promised marker slides right to MAR 2025 actual; gap fills red.",
     "PROMISED 2023 · FIRST ENGINE MAR 2025", "Clock tick bed", "", "[GE AEROSPACE | MONEYCONTROL]"),
    ("J016", A1, "GE blamed problems in its supply chain. HAL put penalties on GE for the delay.",
     "Credited news headlines (Bloomberg / Business Standard) under magnifier.", "", "Paper rustle", "",
     "[BLOOMBERG | 2024]"),
    ("J017", A1, "By October twenty twenty six, around ten engines had reached India. HAL says twenty seven airframes are "
     "built and waiting.",
     "Counter pair: ENGINES RECEIVED ~10 vs AIRFRAMES BUILT 27; jets on the line pan.",
     "ENGINES ~10 · AIRFRAMES 27", "", "", "[GE AEROSPACE | HAL CMD | 2026]"),
    ("J018", A1, "Some testing work on radar and weapons is also still pending. But the engine has been the biggest "
     "hold up.", "REAL: Tejas Mk1A flying a test sortie (HAL/MoD footage).", "", "", "", "[TIMES OF INDIA | 2026]"),
    ("J019", A1, "And a delay is only the small problem. The real danger is control.",
     "Slow push on a single F404 under hard light; amber turns red.", "", "Music drops to a low pulse", "", ""),
    ("J020", A1, "India has been here before.", "Hard cut to black, then archive.", "", "1.5 s silence, then thud",
     "Reveal beat", ""),
    ("J021", A1, "In May nineteen ninety eight, India tested nuclear weapons at Pokhran.",
     "REAL: Pokhran-II archive (Commons / DD News credited excerpt), Shakti site photo with parallax.",
     "POKHRAN · 11 & 13 MAY 1998", "Distant rumble", "", "[GOVT OF INDIA | 1998]"),
    ("J022", A1, "America answered with sanctions under a law called the Glenn Amendment.",
     "Credited archive: US press briefing on the sanctions, 1998 (Commons / archive.org); text of the law under magnifier.",
     "US SANCTIONS · GLENN AMENDMENT", "", "", "[US STATE DEPT | 1998]"),
    ("J023", A1, "Sales of the same GE F four zero four engines to India were stopped. American help on the Tejas flight "
     "controls also ended.",
     "ILLUSTRATION: Tejas prototype wireframe; the engine block and flight-control box fade out with a red STOPPED stamp.",
     "F404 SALES STOPPED · FLIGHT-CONTROL HELP ENDED", "Two hard cuts", "", "[AEROSPACEWEB | THE HINDU | 1998–2002]"),
    ("J024", A1, "Indian engineers had to build the flight control system on their own. They did it.",
     "REAL: LCA Tejas early test flight archive (ADA/DRDO).", "", "", "", "[ADA]"),
    ("J025", A1, "The lesson was simple. If you do not own the engine, you do not fully own your fighter jet.",
     "Slow push into a Tejas nozzle; heat haze.", "", "Low braam", "One-line verdict", ""),
    ("J026", A1, "Many countries can build a nuclear bomb. Many can launch rockets into space.",
     "Kinetic globe: dots light up for nuclear states, then for orbital launch states.", "", "", "", ""),
    ("J027", A1, "But only a handful can design and build a modern fighter engine on their own. America, Russia, Britain, "
     "France. And, after decades of struggle, China.",
     "Kinetic globe, land only: five countries glow amber one by one with their makers (GE · Pratt & Whitney · NPO Saturn · "
     "Rolls-Royce · Safran · Chinese state makers); India outlined, empty.",
     "THE ENGINE CLUB", "One impact per country", "", "[KED GLOBAL | AVIATION WEEK]"),
    ("J028", A1, "India tried to join this club. And that started one of the hardest engineering stories in its history.",
     "Dissolve from the globe into a 1980s GTRE blueprint.", "", "Music lifts", "", ""),

    ("J029", A2, "In nineteen eighty six, India decided it would build its own fighter engine.",
     "Blueprint world: GTX-35VS Kaveri line drawing assembles stroke by stroke (ILLUSTRATION).",
     "1986 · GTRE, BENGALURU", "Pencil and drafting ambience", "Chapter 2 card", "[PIB]"),
    ("J030", A2, "The job went to the Gas Turbine Research Establishment, GTRE, a DRDO lab in Bengaluru. The engine was "
     "named Kaveri.",
     "REAL: GTRE building / Kaveri engine at Aero India (Commons, credited).", "KAVERI · GTX-35VS", "", "",
     "[DRDO | GTRE]"),
    ("J031", A2, "Full development was approved in March nineteen eighty nine, with a budget of about three hundred and "
     "eighty two crore rupees.", "PROOF: PIB release (10 Dec 2012) under magnifier, highlight 'Rs.382.81 Crore'.",
     "SANCTIONED MAR 1989 · ₹382.81 CRORE", "", "", "[PIB | 2012]"),
    ("J032", A2, "The plan was to finish by December nineteen ninety six.",
     "Same PIB page, magnifier slides to 'December 1996'.", "TARGET: DEC 1996", "", "", "[PIB | 2012]"),
    ("J033", A2, "The goal was huge. An engine that gives eighty one kilonewtons of push with the afterburner on, and that "
     "works in India's heat and dust.",
     "ILLUSTRATION: thrust arrow grows to an 81 kN target line; sand and heat-shimmer particles hit the intake.",
     "TARGET THRUST 81 kN", "", "", "[JANE'S | DRDO]"),
    ("J034", A2, "And India was building a brand new jet, the Tejas, at the same time. Both from zero. That doubled the "
     "risk.", "Split blueprint: Tejas airframe left, Kaveri engine right, both half-drawn and flickering.", "", "", "",
     ""),
    ("J035", A2, "When the Kaveri prototypes reached the test bench, the numbers did not add up.",
     "REAL: Kaveri on a ground test bed (DRDO/GTRE video or photo, credited).", "", "Engine run-up sound", "", "[DRDO]"),
    ("J036", A2, "It was meant to weigh eleven hundred kilos. It weighed twelve hundred and thirty five.",
     "Kinetic scale: needle swings past 1,100 to 1,235 kg; overweight band glows red.", "1,100 KG TARGET · 1,235 KG ACTUAL",
     "Heavy clunk", "", "[CAG | 2011]"),
    ("J037", A2, "It was meant to push eighty one kilonewtons. It reached only about seventy.",
     "Thrust bar fills to 70.5 kN and stalls short of the 81 kN line.", "81 kN TARGET · ~70.5 kN ACHIEVED", "", "",
     "[JANE'S | 2023]"),
    ("J038", A2, "And India had no facility to test a fighter engine in high altitude conditions.",
     "Map pulse: India, no altitude-test icon; the line jumps to Russia.", "", "", "", "[CAG | PIB]"),
    ("J039", A2, "So Indian engineers had to take the Kaveri to Russia for those tests.",
     "Kinetic map, land only: Bengaluru to Moscow region (CIAM / Gromov, Zhukovsky).", "BENGALURU → RUSSIA", "Whoosh", "",
     "[PIB | 2012]"),
    ("J040", A2, "The years went by. The Air Force could not wait for ever.",
     "Calendar years flip 1996 → 2008 over a dusty test cell.", "", "Clock tick", "", ""),
    ("J041", A2, "In September two thousand eight, the Kaveri was officially separated from the Tejas programme. The Tejas "
     "would fly with the American engine.",
     "Credited headline (The Hindu, 27 Sep 2008) under magnifier; the Kaveri blueprint tears away from the Tejas blueprint.",
     "SEP 2008 · KAVERI DELINKED FROM TEJAS", "Paper tear", "", "[THE HINDU | 2008]"),
    ("J042", A2, "But GTRE did not stop. In twenty ten, a Kaveri flew for the first time, fitted to a Russian Ilyushin "
     "transport plane used as a flying test bed.",
     "REAL: Il-76 flying test bed at Gromov Flight Research Institute (Commons, CC BY-SA), parallax.",
     "IL-76 FLYING TEST BED · GROMOV, RUSSIA · 2010", "Turboprop/jet flyby", "", "[PIB | AIRFORCE TECHNOLOGY]"),
    ("J043", A2, "Twenty seven flights. Up to twelve kilometres high.", "Altitude counter runs to 12 km over the Il-76.",
     "27 FLIGHTS · 57 HOURS · 12 KM", "", "", "[PIB | 2012]"),
    ("J044", A2, "By twenty twelve, about two thousand crore rupees had been spent. The cost estimate had grown to over "
     "twenty eight hundred crore.",
     "PROOF: PIB page, magnifier on 'Rs.1996 Crore' and 'Rs.2839 Crore'; a counter climbs from 382 to 2,839.",
     "₹382 CR → ₹2,839 CR", "Coin cascade, low", "", "[PIB | 2012]"),
    ("J045", A2, "So why did it fail? To answer that, we need to go inside the engine.",
     "Camera dives into a cutaway engine render (ILLUSTRATION).", "", "Rising whoosh into Act 3", "", ""),

    ("J046", A3, "First, a fair question. If ISRO can build rocket engines, why is a jet engine so much harder?",
     "Split: ISRO launch (real) left, fighter engine run (real) right.", "ROCKET vs JET", "", "Chapter 3 card", ""),
    ("J047", A3, "A rocket engine fires for a few minutes. It carries its own oxygen. Then its job is done, and that stage "
     "falls away.", "REAL: LVM3 launch and stage separation (ISRO footage).", "ROCKET: MINUTES · USED ONCE", "", "",
     "[ISRO]"),
    ("J048", A3, "A fighter jet engine must breathe air. Humid sea air. Freezing mountain air. Desert dust.",
     "Three quick real cuts: coastal monsoon, Himalayan clouds, Rajasthan dust (stock, Indian locations).", "", "",
     "3 cuts, 2.5 s each", ""),
    ("J049", A3, "It must go from idle to full power in seconds, again and again, during hard turns.",
     "REAL: fighter afterburner take-off at night (IAF / Commons).", "", "Afterburner roar", "", ""),
    ("J050", A3, "And it must run for thousands of hours between overhauls.",
     "Hours counter spins to 4,000+ over an engine on a maintenance stand.", "JET ENGINE: THOUSANDS OF HOURS",
     "", "", "[GE AEROSPACE]"),
    ("J051", A3, "At the heart of it all is one small part. The high pressure turbine blade.",
     "Three.js: a single turbine blade rises out of darkness, amber rim light, slow 360° turn (ILLUSTRATION).",
     "HIGH-PRESSURE TURBINE BLADE", "Low hum", "", ""),
    ("J052", A3, "It sits right behind the combustion chamber, where burning fuel makes a storm of hot gas.",
     "Three.js cutaway: flame front in the combustor, gas flows through the turbine stage (ILLUSTRATION).", "", "Roar bed",
     "", ""),
    ("J053", A3, "Now here is the shocking part.", "Hold on the blade, music cut.", "",
     "1.5 s total music silence, then braam", "Core reveal", ""),
    ("J054", A3, "Rolls-Royce says its blades work in gas up to two hundred degrees hotter than the melting point of the "
     "metal they are made of.",
     "Thermal-camera look (ironbow palette): gas temperature bar climbs past a MELTING POINT line on the blade.",
     "GAS: UP TO 200 °C ABOVE THE METAL'S MELTING POINT", "Braam lands on 'melting point'", "",
     "[ROLLS-ROYCE | 2012]"),
    ("J055", A3, "Hotter than its own melting point. And still it does not melt. How?",
     "Push into the glowing blade surface.", "", "", "", ""),
    ("J056", A3, "The first secret is in the metal itself.", "Zoom into the blade metal: crystals appear (ILLUSTRATION).", "",
     "", "", ""),
    ("J057", A3, "Normal metal is made of many tiny crystals. The borders between them are weak spots.",
     "ILLUSTRATION: multi-grain lattice, grain boundaries glow.", "MANY CRYSTALS · WEAK BORDERS", "", "",
     "[DRDO | DMRL]"),
    ("J058", A3, "Under heat and huge force, the metal slowly stretches along those borders. Engineers call it creep.",
     "ILLUSTRATION: grains slide; blade lengthens slowly; label CREEP.", "CREEP", "Metallic groan", "", ""),
    ("J059", A3, "So the best blades are grown as one single crystal. No borders at all.",
     "ILLUSTRATION: perfect single-crystal lattice, atoms in one unbroken grid; then real photo of a single-crystal blade "
     "casting.", "SINGLE CRYSTAL", "", "", "[DRDO | DMRL]"),
    ("J060", A3, "The metal is a nickel super alloy, with rare elements like rhenium mixed in.",
     "ILLUSTRATION: alloy recipe as glowing element tiles orbiting the blade (Ni, Co, Cr, Al, Ta, W, Re).",
     "NICKEL SUPERALLOY · + RHENIUM", "", "", "[CANNON-MUSKEGON CMSX-4 DATA]"),
    ("J061", A3, "The second secret is air.", "Cut to blade cross-section.", "", "", "", ""),
    ("J062", A3, "Each blade is hollow, with tiny channels inside. Cooler air from the compressor is pushed through them.",
     "Three.js cutaway: serpentine cooling channels light up cyan as air flows through (ILLUSTRATION).",
     "COOLING CHANNELS", "Air rush", "", ""),
    ("J063", A3, "It comes out through rows of tiny holes, and covers the blade in a thin blanket of cooler air.",
     "Three.js: rows of film-cooling holes emit a thin cyan film that wraps the blade (ILLUSTRATION).", "FILM COOLING",
     "", "", ""),
    ("J064", A3, "And on top, a ceramic coating acts like a heat shield.",
     "ILLUSTRATION: a ceramic layer (Ceramic White) seals the surface; temperature gradient shown through the wall.",
     "THERMAL BARRIER COATING", "", "", ""),
    ("J065", A3, "Now add the spin. The disc holding these blades turns more than twelve thousand times every minute.",
     "Three.js: turbine disc spins up; rpm counter climbs past 12,000.", "> 12,000 RPM", "Rising turbine whine", "",
     "[ROLLS-ROYCE | 2012]"),
    ("J066", A3, "Rolls-Royce says the pull on each blade is like the weight of a London bus hanging from it.",
     "ILLUSTRATION: a red double-decker bus silhouette hangs from one blade in a slow-motion freeze.",
     "PULL ON ONE BLADE ≈ A LONDON BUS", "", "", "[ROLLS-ROYCE | 2012]"),
    ("J067", A3, "Heat above melting point. A bus hanging from every blade. For thousands of hours.",
     "Fast triptych recap of the three images.", "", "Three impacts", "", ""),
    ("J068", A3, "This is why so few countries can do it. You cannot just copy the drawing.",
     "Blueprint of a blade burns away to reveal a real casting.", "", "", "", ""),
    ("J069", A3, "The real knowledge is in how the metal is made, cast, drilled and tested. Countries learned it over "
     "decades of testing, and many failures.",
     "REAL: precision casting and laser-drilling B-roll (industrial stock), engine test cell run.", "", "", "", ""),
    ("J070", A3, "That knowledge is a closely guarded secret. Nobody sells it.",
     "Close-up: a vault-like test cell door closes (stock).", "", "Door thud", "", ""),

    ("J071", A4, "But the Kaveri story did not end in two thousand eight.",
     "Return to the Kaveri blueprint; it re-ignites amber.", "", "Music turns hopeful", "Chapter 4 card", ""),
    ("J072", A4, "GTRE took out the afterburner and made a simpler version. The Dry Kaveri.",
     "ILLUSTRATION: the afterburner section slides off the Kaveri wireframe; label DRY KAVERI.",
     "DRY KAVERI · NO AFTERBURNER", "", "", "[DRDO | PIB]"),
    ("J073", A4, "In tests in Russia, it gave about forty eight kilonewtons of push, a little more than its target.",
     "REAL: Kaveri derivative engine images (DRDO/PIB), thrust bar crosses 46 to 48.5 kN.", "~48.5 kN · TARGET 46 kN",
     "", "", "[JANE'S | 2023]"),
    ("J074", A4, "It is now chosen to power India's stealth combat drones, like the planned Ghatak.",
     "REAL: DRDO SWiFT flying-wing demonstrator footage (DRDO, 2022), labelled; then ILLUSTRATION of Ghatak.",
     "GHATAK UCAV · PLANNED", "", "", "[DRDO | SEP 2026]"),
    ("J075", A4, "Meanwhile, DRDO's metals lab in Hyderabad, DMRL, has learned to make single crystal turbine blades. "
     "First for a helicopter engine.",
     "REAL: DMRL single-crystal blade photos (PIB release, Apr 2021) under magnifier.",
     "DMRL HYDERABAD · SINGLE-CRYSTAL BLADES · 2021", "", "", "[PIB | APR 2021]"),
    ("J076", A4, "Those years of struggle were not wasted. They built the base India did not have in nineteen eighty six.",
     "Montage: Kaveri test cell, Il-76 FTB, DMRL blade; amber light grows.", "", "", "", ""),
    ("J077", A4, "But the next big fighter, the AMCA, needs much more.",
     "REAL: AMCA full-scale model at Aero India (Commons / PIB), parallax.", "AMCA · 5TH-GENERATION FIGHTER", "", "",
     "[ADA]"),
    ("J078", A4, "The first AMCA jets will use GE's F four one four engine.", "ILLUSTRATION: AMCA wireframe, twin F414s.",
     "AMCA MK1 · GE F414", "", "", "[ADA | DEFENCE MINISTRY]"),
    ("J079", A4, "For later jets, India wants a new engine of about one hundred and twenty kilonewtons. And this time, it "
     "wants to own the design.", "ILLUSTRATION: a clean-sheet engine wireframe draws itself; label 120 kN CLASS.",
     "AMCA MK2 · 120 kN CLASS", "", "", "[META-DEFENSE | AUG 2026]"),
    ("J080", A4, "In twenty twenty five, the government picked France's Safran to build it together with GTRE.",
     "REAL: Safran facility / M88 engine (Safran press media), map line Paris → Bengaluru.",
     "SAFRAN + GTRE · SELECTED AUG 2025", "", "", "[DEFENCE MINISTER | AUG 2025]"),
    ("J081", A4, "India's condition is clear. The design and the rights must belong to India.",
     "Forensic highlight on a news report line about full IP ownership.", "FULL INDIAN IP", "", "",
     "[RAKSHA ANIRVEDA | 2026]"),
    ("J082", A4, "As of now, that deal is still waiting for final approval. And in August twenty twenty six, Rolls-Royce and "
     "Reliance also offered to build an engine in India.",
     "Credited headlines (Meta-Defense; Eurasia Review) under magnifier; a second line from Derby joins the map.",
     "AWAITING FINAL APPROVAL · OCT 2026", "", "", "[META-DEFENSE | EURASIA REVIEW | 2026]"),
    ("J083", A4, "China walked this same road. Its J twenty stealth fighter first flew on Russian engines. It took China "
     "decades, and many failures, to switch to engines of its own.",
     "REAL: J-20 photos (Commons); timeline AL-31F → WS-10C → WS-15.", "J-20: AL-31F (RUSSIA) → WS-10C → WS-15",
     "", "", "[THE DEFENSE POST | 2021]"),

    ("J084", V, "So let us come back to our question.", "Moon landing and Tejas line side by side again.", "", "",
     "Verdict", ""),
    ("J085", V, "Reaching the Moon needs you to master physics and rocket fuel for a few minutes.",
     "Chandrayaan-3 descent replay, fast.", "", "", "", ""),
    ("J086", V, "A fighter engine needs you to master metal that survives above its melting point, spinning, for "
     "thousands of hours.", "Blade glowing in the thermal look; rpm counter.", "", "", "", ""),
    ("J087", V, "That is the jet engine paradox. The Moon was the easier problem.",
     "Title card burns in over the blade.", "THE JET ENGINE PARADOX", "Braam", "", ""),
    ("J088", V, "For forty years, India has been learning the hard way. Today, the Dry Kaveri is testing, the blade "
     "makers in Hyderabad are learning, and a new engine is on the drawing board.",
     "Montage: Dry Kaveri, DMRL blade, AMCA model; dawn light over a test cell.", "", "Music swells", "", ""),
    ("J089", V, "Will the Safran partnership finally give India a fighter engine of its own? Or will politics stall it "
     "again? Tell me what you think in the comments.",
     "Tejas Mk1A take-off with afterburner (real); comment prompt in lower third.", "YOUR VIEW? COMMENT BELOW", "", "",
     ""),
    ("J090", V, "If you like deep, researched stories like this, like, share it with a friend who loves defence tech, and "
     "subscribe. See you in the next one.", "End card with subscribe and end-screen zones.", "", "Music resolves",
     "End card last", ""),
]


def main():
    with open(HERE / "script.full.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(COLS)
        for rid, sec, vo, vis, ons, snd, pace, cite in ROWS:
            w.writerow([rid, sec, "", vo, "", vis, ons, snd, pace, cite])
    print(f"wrote {len(ROWS)} rows")


if __name__ == "__main__":
    main()
