# Screenplay v1 (visual-first): The Blade That Should Melt

Working title; episode of "India's Missing Pieces". English VO (`vo.txt`, Akash). Line ids = `L<n>` = line n of `vo.txt`.
Times are estimates (about 1,940 words, roughly 12 minutes at Akash's pace); they are replaced by `align_script.py` timings after recording. The open-loop line says the blade arrives 'in about three minutes': re-check against the final cut. Owner brief (2026-10-22): **no Chandrayaan opener
(everyone knows it, nobody clicks); concentrate on visuals; explain the science of the jet engine deeper but with simple
words and everyday things.** The film's centre is the 3D engine and the blade; the Tejas and Kaveri story is the frame.

**Look:** tech x geopolitics, dark blueprint base (`blueprint` in `config/brand.yaml`) plus a **thermal-camera (ironbow)
palette for everything hot**. Colour = meaning: white-yellow = hottest gas, orange = hot metal, cyan = cooling air (the one
cool accent), green = a link India owns, red = a stop or a gap. Real footage and documents carry the story (hangar, Tejas,
G.E. Lynn, CAG pages); 3D carries every mechanism.

**Signature device: THE HOT-GAS GAUGE** (persistent, top-left): a vertical thermometer with two markers, GAS (about 1,400 °C)
and METAL (about 930 °C), the gap shaded and labelled `OUR CALCULATION: ~470 °C`. It sits empty before L15, wakes at L16, and
every trick (crystal, air, coating) drags the METAL marker down or shows why it holds. Values only from `claims.csv`, else
"ILLUSTRATIVE". A second small HUD (top-right) carries the news numbers: `ENGINES SENT 14 / 99`, `JETS WAITING ~30`,
`DELIVERED TO IAF 0` (as of dates in the claims; re-check before upload).

**Everyday-object cutaways (a 2-second inset each, same camera language as the 3D):** bicycle pump nozzle glowing warm (L10);
gas stove ring (L11); ceiling fan turning in the wind (L12); balloon let go (L14); brick wall vs one stone (L20); steel
spoon bending in a flame (L21); mall air curtain (L24); thermos cut in half (L25); bucket swing (L29). Each is real
stock or a clean 3D render, labelled `ANALOGY`.

**Hero 3D shots (Blender Cycles, 8 samples + denoise, composited under the HyperFrames HUD; Three.js for the live-in-page
ones):**
1. **The four-job engine:** a cutaway turbofan; air as pale streaks, then compressed (streaks bunch, tint warms), fuel mist
   and flame, gas hitting the turbine, the shaft glowing as the turbine drives the compressor, exhaust. One job per beat
   (2.5–4 s): SUCK · SQUEEZE · BURN · BLOW.
2. **The blade zoom:** camera dives from the whole engine to the first turbine stage to one blade, in ironbow colour.
3. **The grain-vs-crystal slice:** a blade cross-section: many grains with weak lines glowing red and slowly stretching
   (creep) vs one uniform crystal that stays still.
4. **The cooled blade:** hollow channels carrying cyan air, film holes breathing a cyan blanket over the surface, a thin
   ceramic skin; thermal view of surface temperature dropping as each layer switches on.
5. **The spin:** the turbine disc at speed, a red arrow of pull on one blade, a London bus silhouette at scale hanging off it.

| Time | Lines | Audio | Visual + action | SFX / music |
|---|---|---|---|---|
| 0:00 | L01–L02 | Oct 2026, hangars, ~30 Tejas waiting, none delivered | REAL: HAL Nashik/Bengaluru Tejas Mk1A line (HAL/PIB/MoD photos and video, animated), grey jets in a row. Counter `DELIVERED TO IAF: 0` ticks in. First frame is the thumbnail's own subject: one turbine blade glowing against a Tejas tail. | Hangar ambience; hard stop on "not one" |
| 0:11 | L03 | Biggest reason: the engine; 14 of 99 | G.E. Lynn plant exterior (GE press), F404 crate. HUD locks `ENGINES SENT 14 / 99`. A 99-slot bar fills 14 amber, 85 stay empty | Thud on "fourteen" |
| 0:18 | L04–L05 | The blade sits in gas hotter than its melting point and does not melt; very few countries can make it; India still learning | Hero 3D 2 opening: the blade glowing white-hot, a flame wall behind it; GAS vs METAL gauge flashes in with the gap shaded red. Quick flash of a world map with the few countries that make it (lit, no borders), India outlined, empty | Low riser, silence 1.5 s before "does not melt", then thump |
| 0:32 | L06 | Open loop: how it works with kitchen things; blade in about three minutes; decision in Delhi | Three teasers: stove ring + engine, the cyan air blanket, a calendar page "DECISION: CCS APPROVAL" | Riser |
| 0:52 | L07–L09 | Four jobs; suck | Hero 3D 1: the four words stamp on in a row; camera enters the intake; fan blades, air streaks pulled in. Real: a jet starting up on the ramp (IAF/Commons) cut in for 2 s | Fan spool-up |
| 1:08 | L10 | Squeeze: bicycle pump | Inset: a hand on a bicycle pump, thermal view, the nozzle warming. Cut to hero 1: compressor stages, streaks bunch and warm toward orange; stage counter ticks up. | Pump hiss |
| 1:28 | L11 | Burn: gas stove flame; far bigger | Stove ring blue flame (macro) dissolves into the combustor in hero 1: fuel mist, flame, expansion arrows | Gas whoosh |
| 1:48 | L12–L13 | Turbine like a ceiling fan; shaft joins turbine to compressor | Wind spinning a ceiling fan (stock) match-cuts to the turbine. Hero 1: the shaft lights up end to end, a loop arrow turbine to compressor to turbine: "THE ENGINE FEEDS ITSELF" is spoken, not written | Motor hum |
| 2:12 | L14 | Exhaust; trail; balloon | Contrail in the sky (stock), then a balloon released across the frame with a small arrow pair. Hero 1 pulls back to show thrust | |
| 2:24 | L15 | Turbine sits right behind the flame, hottest place | Hero 2 dive: from the whole engine to the turbine stage to one blade, ironbow thermal colour; HUD gauge wakes (GAS marker climbs) | Low drone |
| 2:40 | L16 | Rolls-Royce: up to 200 °C above the melting point | Blade in the flame; a melting-point line on the gauge; gas marker rides 200 above it. Source tag `[ROLLS-ROYCE 2012]` on a document push-in | Braam; music out 1.5 s before "two hundred" |
| 3:00 | L17 | Cambridge: gas ~1,400 °C, metal ~930 °C; our calculation ~470 °C gap | Gauge fills both markers with the numbers; the gap bracket animates to scale; `OUR CALCULATION` tag. Document: Cambridge page, magnifier on the figures | Tick |
| 3:16 | L18 | You'd expect it to melt, right? How does it survive? | Held beat: the blade glows, then a slow push-in. The three tricks appear as three dots on the gauge's side | Silence 1 s |
| 3:28 | L19 | Three tricks; seen at home | Three numbered icons light one by one (no text slide: they are the 3D objects: crystal, channel, shell) | |
| 3:36 | L20–L22 | Trick one: brick wall of crystals, creep, single crystal; nickel alloy, rhenium | Brick wall (stock/3D) with weak mortar lines glowing; cut to hero 3: grains with red boundaries slowly stretching, the METAL marker creeping up; spoon bending in flame inset. Then the single crystal: lines vanish, still. Lattice flash (Three.js) of a rhenium atom in the nickel lattice, labelled ILLUSTRATION. Real: DMRL single-crystal blade photo (PIB 2021) | Metal creak; calm tone on the single crystal |
| 4:24 | L23–L24 | Trick two: hollow blade, cool air channels, film of cool air; mall air curtain | Hero 4: cutaway, cyan air flows through channels, bursts from tiny holes and hugs the surface in a thin film; mall entrance with an air curtain (stock) as the 2-second analogy; thermal view: surface cools as the film switches on, METAL marker drops | Soft air hiss |
| 5:00 | L25–L26 | Trick three: ceramic shield, thermos flask; all three together | Thermos cut in half (3D) inset; on the blade a thin white shell slides on, temperature drops again. Then all three layers stack in one cutaway while the METAL marker settles at about 930 | Chord resolves |
| 5:32 | L27–L29 | The spin: 12,000 rpm; London bus; ceiling fan snail; bucket | Hero 5: disc at speed (motion-blurred), red pull arrow on one blade; to scale a double-decker bus hangs from it. Ceiling fan beside it looks slow | Rising whine |
| 6:00 | L30 | Gas above melting point, a bus, thousands of hours | Three stacked states on one blade: heat, pull, time (a clock counter running into thousands). No new words on screen beyond `THOUSANDS OF HOURS` | Thud |
| 6:12 | L31 | Why a rocket is easier | Split frame: rocket stage burning 2–11 min then falling away (ISRO LVM3 clip, no Chandrayaan framing) vs the engine running thousands of hours. One clean metaphor, quick | |
| 6:28 | L32–L34 | Can't copy the drawing; know-how; nobody shared; small club | Blueprint on a drafting table slides off; the real knowledge shown as a casting, a drill, a test rig (stock/3D); a globe lights up America, Russia, Britain, France, China | Low drone |
| 7:00 | L35–L37 | Why it matters: 42 squadrons / ~29; MiG-21 retired; 83 + 97 orders | Squadron gauge: 42 slots, 29 amber, 13 red pulse. MiG-21 retirement (PIB). Contract counter 83 → 180 over a PIB photo | Gauge ticks |
| 7:32 | L38–L40 | HAL does not make the engine; F404, Lynn; due 2023, first March 2025; penalties; radar and missiles also pending | Timeline ribbon: 2023 promised → MAR 2025 first engine, gap filling red. Headlines (Bloomberg, New Indian Express) under a magnifier | Clock tick |
| 8:04 | L41–L45 | 1998 sanctions; control; engineers built flight control themselves; the lesson | Pokhran 1998 archive headline; Glenn Amendment page push-in (CRS). Hardware wireframe of the Tejas with the engine bay going dark. The lesson line is spoken over a slow push-in on the empty bay | Silence 1.5 s before the lesson, then a thud |
| 8:40 | L46–L50 | Kaveri: 1986 plan, March 1989 approval, Rs 382 crore, Dec 1996; 81 kN; Tejas at the same time; the test bench | Document: CAG report page with highlighter. Thrust bar (target 81 vs achieved) and weight bar (1,100 vs 1,235 kg) as bars, labelled `AS REPORTED` where disputed | Test-cell roar |
| 9:20 | L51–L56 | Numbers; no high-altitude facility; Russia; Sept 2008 delinking; 2010 Il-76 flights; 27 flights; spend | Kaveri on the Il-76 test bed (Commons/MoD); counters 27 flights, 12 km; cost ribbon 382 → 2,839 crore | |
| 9:52 | L57–L60 | Not a failure: Dry Kaveri ~48 kN; Ghatak; DMRL blades; the base | Thrust bar fills past target (green, since this one India owns); DMRL single-crystal blades (PIB 2021) in the same hero 2 style; `60 BLADES · 2021` counter | Uplift |
| 10:24 | L61–L66 | AMCA on F414; 120 kN; Safran with GTRE Aug 2025; full Indian IP; still waiting; Rolls-Royce and Reliance; China took decades | Engine-club globe: India fills in amber only where facts support (DMRL, Kaveri). Document: news pages, credited. `STATUS: AWAITING CCS APPROVAL (OCT 2026)`. J-20 / WS-10 / WS-15 relay graphic, no more than 3 s | |
| 11:08 | L67–L69 | Rule, Ruin, Reality | Rule: the empty engine bay glows. Ruin: jets in the hangar, DELIVERED 0. Reality: the hot-gas gauge with the three tricks in green, the missing link in the middle (the hot section) pulsing amber | Silence 1.5 s before Reality |
| 11:28 | L70–L74 | What it means for you; two things to watch; honest timeline | Two cards-as-objects (a calendar page and a Tejas handover photo frame), not text boxes. Slow push on the hot-section blade | |
| 11:52 | L75–L77 | Bridge: the magnet film; next missing piece; sign-off | Magnet from the previous film spins into view and joins the blade; a three-up of the series: chips, magnets, engine. Channel name and logo sting only here | Outro sting |

## Checks before building
- Text stays under 15% of the screen; every cut shows one change; nothing static for more than 1.5 s.
- No Chandrayaan opener, no welcome, no logo until L77.
- Every number on screen comes from `claims.csv` (`fact-check.md` §Time-sensitive for the news numbers); ILLUSTRATION /
  ANALOGY / AS REPORTED labels where the claims say so.
- Real footage first: Tejas/HAL/PIB/G.E. media, CAG and CRS pages. Stock only for the analogies, labelled ANALOGY.
- Build order: hero 1 and 2 first (the whole film hangs on them), then 3, 4, 5, then the HUD, then the documents.
