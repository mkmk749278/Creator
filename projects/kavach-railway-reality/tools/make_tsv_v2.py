#!/usr/bin/env python3
"""One-time author helper for script v2 (2026-10-15, owner's production guide, PLAYBOOK §4a-4): writes ../script.full.tsv.
Do not re-run after edits to the TSV.

v2 rewrites v1.1 in the elder-brother voice (varied rhythm, `...` and `—`, phonetic acronyms for Akash), the 3-act
structure (hook + open loop, forensic dissection, citizen's action plan, outro with "Jai Hind") and an 8–12 minute
length. Facts are the v1.1 facts already in claims.csv, plus four new claims for the fact-checker (indigenous design,
PIB and CRS publishing online, Rail Madad 139). Columns: section, VO, visual, on-screen text, SFX, action, citation.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

H, K, P, R, C, A, O = ("1 Hook and open loop", "2 What Kavach really is", "3 The physics of stopping",
                       "4 The rollout reality", "5 Two crashes, two failures", "6 Your action plan", "7 Outro")

ROWS = [
    # 1 Hook and open loop
    (H, "It's two in the morning on a night train... the lights are off, the A-C is humming, and your whole family is asleep on the berths.",
     "REAL: sleeper coach at night, blue night lamp, curtains swaying, a child asleep on a lower berth (Indian stock).", "", "Cold open: coach rattle, A-C hum, no music", "Slow dolly down the aisle", ""),
    (H, "Up front, one loco pilot is staring into the dark — watching for a signal that might be red.",
     "REAL: night locomotive cab POV, rain on the windscreen, wiper sweeping; distant signal glow.", "", "Wiper thunk, rail clatter", "Push in on the windscreen", ""),
    (H, "Then one morning you wake up to news of a train crash... and by lunchtime, your family WhatsApp group is on fire.",
     "SIM: phone lock screen on a kitchen table, WhatsApp family group previews stacking up (generic names, no real accounts).", "", "Phone buzz on wood, pings layering", "Notifications stack every beat", ""),
    (H, "One forward says the government never bothered with safety. Another says India already has Kavach, so crashes should be impossible now.",
     "SIM: two forwards side by side: NO KAVACH? WHY? and KAVACH = ZERO ACCIDENTS.", "MYTH 1 · MYTH 2", "Two notification tones", "Split screen slides apart", ""),
    (H, "Both forwards are playing with your fear — and both are missing what really happens on the track.",
     "Both forwards crack like glass; push through the crack into a dark track bed at night.", "", "Glass crack, sub drop", "Crash zoom through the crack", ""),
    (H, "Welcome to Be Practical with Kishore.",
     "Kishore on camera / channel face card over the track bed; logo sting.", "BE PRACTICAL WITH KISHORE", "Logo sting", "Face and name by 0:20", ""),
    (H, "Today we'll open the railway's own documents, do the braking maths together, and read the official accident inquiries line by line.",
     "PROOF: R-D-S-O spec cover, CRS abstract cover, PIB release, each sliding in on paper texture under a highlighter sweep.", "RDSO · CRS · PIB", "Paper slides, highlighter squeak", "Document push-ins", "[RDSO | CRS | PIB]"),
    (H, "And around the eight minute mark, I'll show you the exact finding in the inquiry reports that settles the hardest question of all... would Kavach have saved Balasore, and would it have saved the Kanchanjunga Express?",
     "REAL: credited news stills of Bahanaga Bazar and Rangapani wreck sites under a forensic magnifier; a small minute counter ticks toward 8:00.", "BALASORE 2023 · KANCHANJUNGA 2024", "Heartbeat thud, riser", "OPEN LOOP: re-check the minute against align/ before render", "[CRS | ABSTRACTS 2024–25]"),

    # 2 What Kavach really is
    (K, "Let's start with what Kavach actually is — because it isn't an app, and nobody can switch it on across India overnight.",
     "SIM: an app icon labelled KAVACH dissolves into steel hardware; a big switch flips and nothing on the India map lights up.", "NOT AN APP", "Switch clack, silence", "Icon-to-hardware morph", ""),
    (K, "Kavach is India's own Automatic Train Protection system. It keeps watching the train's speed and the signals ahead, and if the train goes too fast or is about to pass a red signal, it warns the loco pilot first.",
     "ILLUSTRATION (Engine 1, hardware X-ray): a train on a 3D track; permitted speed and the next signal float above the cab; WARNING flashes.", "AUTOMATIC TRAIN PROTECTION", "Cab buzzer", "Orbit around the loco", "[PIB | FEB 2026]"),
    (K, "And if the train still doesn't slow down, Kavach applies the brakes by itself.",
     "ILLUSTRATION: brake command flows from the Kavach box into the brake pipe; the speed dial falls.", "AUTO BRAKE", "Air hiss", "Dial needle drop", "[PIB | 05 AUG 2026]"),
    (K, "In March twenty twenty two, the Railway Minister rode in a railway engine during a Kavach test in Telangana — two engines running towards each other on the same line, and Kavach stopped them about three hundred and eighty metres apart.",
     "REAL: March 2022 Kavach head-on trial footage (Ministry of Railways / PIB), credited.", "KAVACH TRIAL · 4 MAR 2022 · 380 M APART", "", "Cut on the stop", "[PIB | MAR 2022]"),
    (K, "It looks like magic on video. But Kavach is really a chain of four links, and it only protects you when every single link is in place.",
     "ILLUSTRATION: four glowing links snap together around a train.", "", "Metal chain clink", "Links snap in one by one", ""),
    (K, "Link one sits on the track — small R-F-I-D tags fixed to the concrete sleepers. A reader under the engine reads each one as it passes over it, so the train knows exactly where it is, and on which line.",
     "REAL: RFID tag on a PSC sleeper (railway media); Engine 1 X-ray shows the under-chassis reader passing over it, tag ID and track ID popping up.", "LINK 1 · RFID TAG", "Soft ping per tag", "Low tracking shot along the sleepers", "[RDSO | TAN 2025 · IEI | SEP 2024]"),
    (K, "People say there's one tag every kilometre. Actually, one kilometre is the longest gap allowed — near signals, points and stations, the tags crowd together.",
     "ILLUSTRATION: evenly spaced dots get a red cross; then dots cluster thickly around a signal and a turnout.", "MAX GAP 1 KM", "Stamp thud", "Dots regroup", "[RDSO | TAN 2025]"),
    (K, "On one stretch of about ninety six kilometres between Vadodara and Ahmedabad, the railway fixed two thousand eight hundred and seventy two tags... that's about thirty for every kilometre.",
     "BOARD: 2,872 ÷ 96 ≈ 30 worked on the whiteboard over a map of the Vadodara–Ahmedabad stretch.", "96 KM · 2,872 TAGS", "Marker squeak", "Maths written live", "[PIB | 30 DEC 2025]"),
    (K, "Link two is the station. A Kavach computer there reads the signals, the points and which tracks are occupied, straight from the station's own signalling system. It's called interlocking — please remember that word, because it decides everything later.",
     "REAL: station relay room / Kavach equipment (railway media); ILLUSTRATION: interlocking panel lines feed into the Kavach box; the word INTERLOCKING stays lit.", "LINK 2 · INTERLOCKING", "Single low note", "Highlighter on INTERLOCKING", "[PIB | FEB 2026]"),
    (K, "Link three is the radio. Tall towers along the line carry messages between the station and the engine over a U-H-F safety radio... it's not your mobile network, and it's not five G.",
     "REAL: Kavach lattice tower beside the track (railway media); radio pulses animate to the cab; a 5G badge greys out.", "LINK 3 · UHF DATA RADIO", "Radio chirps", "Tilt up the tower", "[PIB | DEC 2024 · PIB | FEB 2026]"),
    (K, "And link four rides inside the engine — a Kavach computer, R-F-I-D readers, speed sensors on the wheels, a screen for the loco pilot, and a direct link to the brakes.",
     "ILLUSTRATION (Engine 1): the loco shell peels away layer by layer; each part labels in.", "LINK 4 · LOCO KAVACH", "", "Exploded view", "[IEI | SEP 2024]"),
    (K, "Think about that for a second — this is a system designed in India, by Indian engineers and Indian companies, for Indian tracks.",
     "REAL: R-D-S-O Lucknow campus / Indian engineers at a test bench (credited railway media).", "MADE IN INDIA", "Warm swell", "Slow push", "[PIB | KAVACH]"),
    (K, "The electronics are built to the highest safety level used in railway signalling, called S-I-L four.",
     "PROOF: SIL-4 band on a standards page under the magnifier.", "SIL-4", "", "Magnifier pan", "[EN 50126 · 50128 · 50129]"),
    (K, "Some posts say that means Kavach can fail only once in a billion hours. That's only half the story — S-I-L four is a strict limit on dangerous failures for each safety function of the electronics, not a promise that no train will ever crash.",
     "SIM: viral post ONE FAILURE IN A BILLION HOURS stamped HALF THE STORY; ILLUSTRATION: the target lights one box in the chain, not the whole railway.", "HALF THE STORY", "Stamp thud", "Stamp lands", "[EN 50129]"),
    (K, "So keep this one in your pocket... Kavach can only act on the information it's given.",
     "ILLUSTRATION: data arrow from interlocking into Kavach glows, then holds.", "", "Drone holds", "Hold on the arrow", ""),
    (K, "In July twenty twenty four, R-D-S-O, the railway's design body in Lucknow, approved version four point zero. It brought better location accuracy, clearer signal information in big yards, fibre links between stations, and a direct link to electronic interlocking.",
     "PROOF: PIB text naming the approval under the magnifier; four upgrade icons click onto the chain.", "KAVACH 4.0 · RDSO · 16 JUL 2024", "Four clicks", "Icons click in", "[PIB | 05 AUG 2026]"),

    # 3 The physics of stopping
    (P, "So if Kavach can see the red signal, why can't the loco pilot just slam the brakes, the way you would in a car?",
     "REAL: locomotive approaching head-on, low angle; cut to a car braking on an Indian road.", "", "Music drops to bass", "Head-on low angle", ""),
    (P, "Because steel wheels on a steel rail have very little grip, and a train is enormously heavy and very long. When the brakes go on, the air pressure has to change all the way down the brake pipe, from the engine to the last coach.",
     "REAL: wheel on rail macro with sparks; ILLUSTRATION: an air-pressure wave travels down the brake pipe coach by coach.", "BRAKE PIPE", "Air rush", "Wave runs the length of the rake", "[IRIMEE | AIR BRAKE NOTES]"),
    (P, "Here's a real number from the railway's own training notes. A Vande Bharat running at one hundred and thirty kilometres per hour needs about six hundred and fifty metres to stop... even with its emergency brakes.",
     "PROOF: IRIMEE Vande Bharat braking table under the magnifier; REAL: Vande Bharat at speed; ILLUSTRATION (Engine 2): speed falls along a 654 m track ruler.", "VANDE BHARAT · 130 KM/H · EMERGENCY BRAKE 654 M", "Long brake squeal", "Ruler draws ahead of the train", "[IRIMEE | VANDE BHARAT NOTES]"),
    (P, "At that speed, it covers about thirty six metres every single second.",
     "BOARD: 130 ÷ 3.6 ≈ 36 m per second.", "36 M EVERY SECOND", "Marker", "Maths written live", "[OUR CALCULATION]"),
    (P, "Now picture a loaded goods train — five thousand tonnes at seventy five kilometres per hour. Goods trains build up brake force slowly, and with simple maths and fair guesses, it needs more than nine hundred metres to stop.",
     "REAL: loaded freight train, long rake of wagons; BOARD: d = v·t + v²/2a worked live, ≈ 930 m, labelled ILLUSTRATIVE MODEL.", "5,000 T · 75 KM/H · ≈ 930 M · ILLUSTRATIVE", "Marker", "Ledger-style build of the sum", "[OUR CALCULATION]"),
    (P, "Put it on a slope going down, one in a hundred, and the same maths gives almost one thousand three hundred metres.",
     "BOARD: gradient term added; ≈ 1,280 m; the track ruler tilts and stretches.", "1 IN 100 DOWN · ≈ 1,280 M", "Marker", "Ruler tilts", "[OUR CALCULATION]"),
    (P, "And if you push the speed from one hundred and thirty to one hundred and sixty, the braking distance doesn't grow by a little... it grows by about half.",
     "BOARD: (160/130)² ≈ 1.5; Engine 2 curve stretches.", "+50%", "Hit", "Curve stretches", "[OUR CALCULATION]"),
    (P, "Now add a December night in north India, with thick fog sitting on the tracks.",
     "REAL: dense winter fog over a north Indian track at night.", "", "Music thins to wind", "Slow drift through fog", ""),
    (P, "Suppose the loco pilot can see a signal only fifty metres ahead. At one hundred and ten kilometres per hour, the train crosses those fifty metres in less than two seconds — and even an alert person needs a second or two just to react.",
     "ILLUSTRATION (Engine 3, fog split): a signal appears out of fog at 50 m; a stopwatch runs out at 1.6 s.", "VISIBILITY 50 M · EXAMPLE · ≈ 1.6 S", "Clock tick", "Stopwatch runs out", "[OUR CALCULATION]"),
    (P, "So if safety depends only on human eyes, the maths simply doesn't work.",
     "REAL: loco pilot peering into fog (stock).", "ILLUSTRATIVE FOOTAGE", "", "Hold on the eyes", ""),
    (P, "This is exactly where Kavach changes the game. It doesn't wait for anyone to see the red signal — it already knows the signal ahead and how far away it is, shows it on the screen inside the cab, works out when braking must begin, and brakes early while there's still enough room.",
     "ILLUSTRATION (Engine 3 right half + Engine 2): cab display shows the aspect and target distance long before it is visible; the braking curve is drawn ahead of the train and the Kavach brake point lands well before the signal.", "TARGET DISTANCE", "Digital sweep", "Curve draws ahead", "[PIB | FEB 2026]"),
    (P, "But it can't cancel physics. If danger appears closer than the stopping distance, even Kavach can't stop the train in time.",
     "ILLUSTRATION: an obstacle appears inside the curve; the zone turns crimson.", "", "Low thud", "Red wash", ""),
    (P, "And how often does a train pass a red signal by mistake? The Commission of Railway Safety noted two hundred and eight such cases in five years, from April twenty nineteen to March twenty twenty four... and twelve of them ended in a collision.",
     "PROOF: CRS abstract page under the magnifier, highlighter on the line; counter rolls to 208, then 12 turns red.", "208 CASES · 2019–2024 · 12 COLLISIONS", "Counter ticks, hit on 12", "Highlighter sweep", "[CRS | ABSTRACTS 2024–25]"),
    (P, "That's exactly the kind of human slip Kavach is built to catch.",
     "REAL: red signal at night, train slowing.", "", "", "Rack focus to the signal", ""),

    # 4 The rollout reality
    (R, "So why isn't it on every track yet? Did the government simply refuse to spend?",
     "ILLUSTRATION (Engine 4, rollout funnel): national rail map, all grey.", "", "", "Map draws in", ""),
    (R, "Look at the size of the job first. Indian Railways runs about sixty nine thousand route kilometres, and in March twenty twenty five it had about sixteen thousand diesel and electric engines.",
     "ILLUSTRATION: map lines draw across India; REAL: loco shed with rows of engines.", "69,439 ROUTE KM · ≈ 16,000 LOCOS · MAR 2025", "", "Map then shed", "[MINISTRY OF RAILWAYS DATA | MAR 2025]"),
    (R, "By the end of July twenty twenty six, the newest Kavach was working on two thousand six hundred and thirty three route kilometres, on parts of the Delhi Mumbai and Delhi Howrah routes — two of the busiest in the country.",
     "ILLUSTRATION (Engine 4): two corridors glow cyan; labels 1,423 km and 1,210 km.", "KAVACH 4.0 · 2,633 RKM · 31 JUL 2026", "", "Corridors light up", "[PIB | 05 AUG 2026]"),
    (R, "Add the older version on about one thousand four hundred and sixty five kilometres in South Central Railway, and Kavach is still working on well under a tenth of the network.",
     "Map: SCR section glows in a second colour; BOARD: (2,633 + 1,465) ÷ 69,439 < 10%.", "VERSION 3.2 · 1,465 RKM · UNDER 10%", "Marker", "Sum written live", "[LOK SABHA | AUG 2024 · OUR CALCULATION]"),
    (R, "And here's the trap hidden in most headlines — numbers that sound the same but mean very different things.",
     "SIM: three headlines with big numbers, each blurred except the number.", "", "", "Headlines slide in", ""),
    (R, "Track with equipment fitted, seven thousand seven hundred and twenty six kilometres. Engines fitted with Kavach, six thousand two hundred and ninety. And track where work has only started, twenty one thousand seven hundred and ninety four kilometres.",
     "Funnel tiers fill: FITTED 7,726 RKM · LOCOS 6,290 · WORK STARTED 21,794 RKM; REAL: loco Kavach cabinet being fitted in a shed.", "FITTED 7,726 · LOCOS 6,290 · WORK STARTED 21,794", "Three ticks", "Funnel fills tier by tier", "[PIB | 05 AUG 2026]"),
    (R, "Fitted isn't working, and work started isn't protected.",
     "Funnel narrows to the thin working stream; stamp FITTED ≠ WORKING.", "FITTED ≠ WORKING", "Stamp", "Stamp lands", ""),
    (R, "The money is moving too. The yearly Kavach budget went from about one thousand one hundred crore rupees in twenty twenty four twenty five to about one thousand six hundred and seventy crore the next year, and by June twenty twenty six, about three thousand eight hundred and seventy five crore had been spent in total.",
     "ILLUSTRATION: two budget bars rise, then a cumulative bar fills.", "₹1,112.57 CR → ₹1,673.19 CR · ≈ ₹3,875 CR SPENT TILL JUN 2026", "Cash-register latch", "Bars rise", "[PIB | MAR 2025 · RAJYA SABHA | AUG 2025 · PIB | 05 AUG 2026]"),
    (R, "The government's own estimate is about fifty lakh rupees per kilometre of track, and about eighty lakh per engine. Do the rough maths for the whole network, and you get nearly thirty five thousand crore for the track, plus about twelve thousand eight hundred crore for the engines.",
     "BOARD: ₹50 lakh/km × 69,439 ≈ ₹34,700 cr; ₹80 lakh × 16,058 ≈ ₹12,846 cr, written live as a ledger.", "≈ ₹34,700 CR + ≈ ₹12,800 CR", "Marker", "Ledger builds line by line", "[RAJYA SABHA | AUG 2025 · OUR CALCULATION]"),
    (R, "That's rough maths, not an official bill... but it shows you the scale.",
     "BOARD: ROUGH MATHS boxed.", "ROUGH MATHS", "", "Box drawn", ""),
    (R, "And money alone doesn't make it work. Every station's signalling data has to be entered and checked, every type of engine wired to its own brakes, and the radio has to reach every curve and every yard.",
     "REAL: signalling technicians at a relay rack; ILLUSTRATION (flowchart): survey → data → loco fitment → radio.", "", "", "Flowchart builds", "[PIB | FEB 2026 · RAJYA SABHA | AUG 2025]"),
    (R, "Then it's all tested together, fixed, and tested again — before a single kilometre is called working.",
     "ILLUSTRATION (flowchart): integrated trials loop back on failure; only then COMMISSIONED.", "COMMISSIONED", "Loop whoosh", "Loop cycles twice", "[RAJYA SABHA | AUG 2025]"),
    (R, "Suppliers are the other bottleneck. For years, just three Indian companies made Kavach — Medha, H-B-L and Kernex.",
     "PROOF: official list naming the three firms under the magnifier.", "MEDHA · HBL · KERNEX", "", "Magnifier pan", "[PIB | MAR 2025 · IEI | SEP 2024]"),
    (R, "Newer ones are in trials now. Quadrant Future Tek told the stock exchange in May twenty twenty six that it got permission for passenger trials, which is a step, not final approval.",
     "PROOF: company stock-exchange filing under the magnifier; stamp NOT FINAL APPROVAL.", "PASSENGER TRIALS ≠ FINAL APPROVAL", "Stamp", "Highlighter on the line", "[NSE FILING | 26 MAY 2026]"),

    # 5 Two crashes, two failures
    (C, "Now, the question I promised you at the start.",
     "Black frame, slow fade up on twisted coaches (credited archive).", "", "Music out", "Fade up", ""),
    (C, "Case one. Bahanaga Bazar station near Balasore in Odisha, June two, twenty twenty three. The Coromandel Express is coming in at about one hundred and twenty eight kilometres per hour, and the signal shows green for the main line.",
     "REAL: credited archive of the Bahanaga Bazar site; map pin; ILLUSTRATION (Engine 5, logic gate): station layout, train arrow on the up main line, home signal turns green.", "BAHANAGA BAZAR · 2 JUN 2023 · ≈ 128 KM/H", "", "Satellite-style zoom to the station", "[CRS | ABSTRACTS 2024–25]"),
    (C, "But the crossover ahead is set towards the loop line... where a goods train is standing.",
     "Engine 5: crossover 17A/B swings to the loop; the parked goods train is highlighted. ILLUSTRATION.", "CROSSOVER 17A/B → LOOP", "Low hit", "Points swing", "[CRS | ABSTRACTS 2024–25]"),
    (C, "The official inquiry found lapses in signalling circuit work done at the station. Close to three hundred people lost their lives.",
     "PROOF: CRS abstract finding under the magnifier, highlighter on the line; then a slow push on a memorial / candles still (credited), no victims shown.", "", "Silence under the second sentence", "Hold", "[CRS | ABSTRACTS 2024–25 · RAJYA SABHA | JUL 2023]"),
    (C, "So, would Kavach have stopped it?",
     "Engine 5: a Kavach box appears on the loco and pulses.", "", "Total music silence 1.5 s after this line, then a low braam", "1.5 s silence", ""),
    (C, "Here's the honest answer — nobody can say yes or no for sure.",
     "Kishore / dark track bed.", "", "Low braam", "Reveal", ""),
    (C, "Remember that word, interlocking? At Balasore, the station's signalling system itself was showing a false green, and if Kavach had been fed that same wrong information, it could have believed the line was clear too.",
     "Engine 5: the false green travels down the wire into Kavach, which shows green too. ILLUSTRATION.", "SAME INPUT · SAME ANSWER?", "Digital echo", "Signal flows along the wire", "[PIB | FEB 2026]"),
    (C, "A safety computer can't correct wrong information that it trusts. Kavach does have a few checks of its own, like knowing from the tags which line the train is really on, but no public study has shown whether those would have acted in time there.",
     "Engine 5: both channels agree on the wrong input; tag reads appear on the loop line, dotted and uncertain.", "UNTESTED COUNTERFACTUAL", "", "Dotted overlay", "[PIB | FEB 2026]"),
    (C, "So the forward saying Kavach would surely have saved Balasore, and the one saying it surely couldn't, are both going beyond the evidence.",
     "The two forwards from the hook return, both stamped BEYOND THE EVIDENCE.", "BEYOND THE EVIDENCE", "Stamp", "Stamps land", ""),
    (C, "Case two. Between Rangapani and Chatterhat, near New Jalpaiguri in north Bengal, June seventeen, twenty twenty four. The automatic signals on this stretch had failed — and when that happens, trains move on a paper authority, at a slow, careful speed.",
     "REAL: credited archive of the Rangapani site; map pin; ILLUSTRATION (Engine 6): a row of automatic signals goes dark; a generic paper authority slides in (no copy of a real form).", "RANGAPANI · 17 JUN 2024 · SIGNALS FAILED", "Power-down", "Signals blink out", "[CRS | ABSTRACTS 2024–25]"),
    (C, "The inquiry found the goods train was handed the wrong form, T-A nine one two instead of T-D nine one two. There was no caution order, the walkie talkies were missing, and the training wasn't good enough.",
     "ILLUSTRATION: two distinct labels T/A 912 and T/D 912, the wrong one highlighted; three items tick red: caution order, walkie-talkie, training.", "T/A 912 ≠ T/D 912", "Three hits", "Ticks land one by one", "[CRS | ABSTRACTS 2024–25]"),
    (C, "The goods train reached seventy eight kilometres per hour and hit the Kanchanjunga Express from behind at about forty. And there was no working Kavach on that section.",
     "Engine 6: freight speed trace climbs to 78, collision marked at about 40; map overlay shows no Kavach line here.", "78 KM/H → ≈ 40 KM/H · NO KAVACH HERE", "Impact", "Trace climbs", "[CRS | ABSTRACTS 2024–25 · RAILWAY BOARD | JUN 2024]"),
    (C, "Here, Kavach could have made a real difference. If both trains were fitted and the section was working, it could have held the goods train to the allowed movement and a slow speed past those failed signals.",
     "Engine 6 rewinds; a Kavach box appears on both locos; freight speed is held low and the braking curve stops it short. SIMULATION.", "SIMULATION", "Rewind whoosh", "Rewind", "[CRS | ABSTRACTS 2024–25 · PIB | FEB 2026]"),
    (C, "You'll hear people say Kavach would always lock the speed at exactly fifteen kilometres per hour. That fifteen is the rule loco pilots follow at failed signals — Kavach enforces the limits its data and settings give it, so don't take that number as a promise.",
     "SIM: viral claim card stamped DEPENDS ON SET-UP.", "DEPENDS ON SET-UP", "Stamp", "Stamp lands", "[CCRS VIA INDIAN EXPRESS | PIB | FEB 2026]"),
    (C, "And notice, this wasn't one loco pilot's mistake. The inquiry found failures in the paperwork, the communication and the training.",
     "Engine 6: the three red ticks return around the station building.", "", "", "Ticks pulse", "[CRS | ABSTRACTS 2024–25]"),
    (C, "Two crashes, two different failures. At Balasore, the signalling information itself was wrong. At Kanchanjunga, the backup rules for failed signals broke down — and Kavach is strongest against the second kind, while the fix for the first has to start in the signalling room.",
     "Side-by-side comparison: two columns, two icons; then REAL: a technician testing a relay rack.", "WRONG INPUT · BROKEN BACKUP", "", "Columns slide in", ""),

    # 6 Your action plan
    (A, "So what can you actually do with all this? Three things.",
     "REAL: dawn, a train crossing a bridge; three step markers appear in a lower corner.", "", "Warm music returns", "Steps appear", ""),
    (A, "One. The next time a Kavach forward lands in your family group, ask three questions before you share it — is this number about fitted equipment or Kavach that's actually working, which date is it from, and was the problem a human mistake or wrong information from the signalling system?",
     "SIM: the WhatsApp forward from the hook; three question chips pop beside it one by one.", "1 · FITTED OR WORKING? · WHICH DATE? · HUMAN OR SIGNAL DATA?", "Chip pops", "Chips pop on each question", ""),
    (A, "Two. Read the real thing instead of the forward. The railway ministry posts Kavach progress in its press releases on the P-I-B website, and the Commission of Railway Safety puts its accident inquiry findings on its own website, free for anyone to read.",
     "PROOF: screen recording of the PIB release page and the CRS website abstracts page (credited), highlighter on the Kavach paragraph.", "2 · PIB.GOV.IN · CRS.GOV.IN", "Click, page turn", "Screen recording scroll", "[PIB | 05 AUG 2026 · CRS]"),
    (A, "Three. If you see something unsafe on a train or at a station, report it to Rail Madad by calling one three nine, or through the Rail Madad app.",
     "REAL: phone dialling 139 on a platform; Rail Madad app screen (credited).", "3 · RAIL MADAD · 139", "Dial tone", "Phone push-in", "[MINISTRY OF RAILWAYS | RAIL MADAD]"),

    # 7 Outro
    (O, "Kavach isn't magic, and it isn't useless. It's an Indian-built safety layer that brakes early when a human makes a speed or signal mistake... and it needs four things to work — a fitted engine, a working track section, correct signalling data, and enough distance to stop.",
     "The two myths from the hook fade out; the four links from Act 2 relight one by one: ENGINE · TRACK · DATA · DISTANCE.", "ENGINE · TRACK · DATA · DISTANCE", "", "Links relight", "[PIB | KAVACH]"),
    (O, "Real safety isn't built on slogans. It's built by railway engineers and track crews doing careful, boring work right, every single day — and every citizen who understands that makes the whole system more accountable.",
     "REAL: track maintenance gang at work at sunrise; relay room; a Kavach loco rolling out at dawn.", "", "Music swells", "Sunrise montage", ""),
    (O, "Tell me in the comments: which route do you travel most, and do you know if Kavach is working on it yet?",
     "Pinned-comment card in a lower corner over a moving map.", "WHICH ROUTE DO YOU TRAVEL?", "", "Map drift", ""),
    (O, "If someone you love travels by train, share this with them. Know the facts. Stay practical. Jai Hind.",
     "Logo bug, end card.", "", "End sting", "End card", ""),
]


def main():
    cols = ["id", "section", "te", "en", "emotion", "visual", "onscreen", "sound", "pacing", "cite"]
    with open(HERE / "script.full.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(cols)
        for i, (sec, en, vis, ons, snd, act, cite) in enumerate(ROWS, 1):
            w.writerow([f"V{i:03d}", sec, "", en, "", vis, ons, snd, act, cite])
    print(len(ROWS), "rows")


if __name__ == "__main__":
    main()
