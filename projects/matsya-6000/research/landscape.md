# Research landscape: what everyone says vs what it actually is (second pass, 2026-11-09)

## 1. What everyone is saying

**News, 2025–Nov 2026.**
- 23 Jul 2025: ISRO and NIOT completed the sphere's key weld: "80 mm weld thickness over a length of 7,100 mm with a
  32-minute weld duration", "after nearly 700 trials"; LPSC upgraded its electron-beam welder "from a 15kW rating to
  40kW" and its X-ray facility to 7.5 MeV (ThePrint, quoting ISRO).
- Jan–Feb 2025: wet tests at L&T Kattupalli near Chennai; voice communication limits found in the shallow harbour
  (IANS, ETV Bharat, AIR).
- Jan 2026: first 500 m dive planned for May 2026 (India Today). Mar 2026: the minister told Parliament the syntactic
  foam (Indian design, made by a European firm) was late; the shallow dive moved to the last quarter of 2026 (UNI).
  Deccan Herald (secretary M. Ravichandran): foam from France; 6,000 m dive December 2027.
- **6 Nov 2026:** unmanned trials at L&T Kattupalli in front of the MoES Secretary (S. K. Tummala) and NIOT Director
  (G. A. Ramadass): flotation, submerged stability, ballast, subsystems, "clearing the path for its next phase of
  advanced testing" (IANS). **No 500 m sea dive reported yet.** IANS gives "2.1-metre diameter spherical hull".
- 27 Oct 2021: an earlier **mild-steel** personnel sphere was lowered unmanned to 6,000 m off Chennai from ORV Sagar
  Nidhi (Wikipedia citing Jagran Josh; to verify with a primary source).

**YouTube (channel API, 2026-11-09).** India coverage is small and shallow: StudyIQ Hindi short 1.29M, Manu Kahat
short "India is going 6 km below" 518K (26 Oct 2026), CNN-News18 35K, many UPSC explainers under 40K. The global
appetite is huge and fear-led: Titan implosion shorts 47M and 6.9M, Cleo Abram "How deep is the deepest submarine?"
22.8M, Half as Interesting "How submarines survive at 36,201 feet" 468K.

**What viewers feel and ask (top comments).**
- Indian shorts: pride and memes ("India scientists day by day", "Proud to be Indian"), no mechanism questions answered.
- Global: "Can't fathom how somebody could go into such depths in a carbon fiber can" (901 likes); OceanGate jokes;
  awe at the pressure ("500 times an elephant's weight is too little at this depth", Hindi comment, StudyIQ).
- Nobody explains **why a sphere, why titanium, why one weld is the hard part, and how India's choice differs from
  Titan's**.

## 2. What it actually is (draft; every fact to `../claims.csv`, primary sources still to collect)
- Sphere: Ti-6Al-4V ELI, 2,260 mm diameter, 80 mm wall, 600 bar (PIB Deep Ocean Mission document, 17 Aug 2025;
  ThePrint). IANS says 2.1 m: 2,260 − 2 × 80 = 2,100 mm, so **2.1 m is likely the inside, 2.26 m the outside**
  (OUR CALCULATION; confirm in a primary source before using).
- Weld: high-penetration electron-beam welding, 80–102 mm titanium, 7,100 mm long, 32 minutes, ~700 trials, 40 kW;
  titanium's "high reactivity with oxygen and nitrogen can cause porosity and embrittlement in the weld" (ThePrint).
  Inspection: 7.5 MeV X-ray, TOFD and phased-array ultrasound (ThePrint).
- The vehicle: three crew, 12 h normal / 96 h emergency endurance (NIOT; to verify), syntactic foam for buoyancy
  (imported), batteries, thrusters, ballast.
- Pressure at 6,000 m (OUR CALCULATION, seawater 1,025 kg/m³): ≈ 60 MPa ≈ 600 bar ≈ 615 kg on every square
  centimetre; on the sphere's ~16 m² outer surface ≈ 98,000 tonnes-force in total.
- Budget: Deep Ocean Mission ₹4,077 crore over five years (PIB 23 Jul 2023). Matsya's own cost is unsourced.

## 3. Our edge (draft, one sentence)
**Everyone says "India is going six kilometres down"; nobody shows the ball of titanium that has to hold back about a
lakh tonnes of sea, why ISRO, a rocket agency, had to weld it, and why after Titan the whole mission hangs on one
32-minute seam.**

## 4. What pictures exist (first look)
- NIOT/MoES/PIB photos of Matsya at Kattupalli and the 2025 wet tests; Doordarshan / AIR / ANI clips of the wet tests
  and the minister's visit (YouTube, via the owner's Termux line).
- ISRO/LPSC photos of the welded sphere (2025 release); the 2021 steel-sphere lowering from Sagar Nidhi.
- Titan: US Coast Guard Marine Board of Investigation material (US government work; check licence) for context only,
  told with dignity (five people died).
- Our Blender hero shots: the sphere at 600 bar with pressure arrows, the electron beam closing the seam, a cutaway
  of three people in 2.1 m.

## 5. Second pass (2026-11-09): primary source, demand, Titan, why it matters to India

**Primary: PIB "Deep Ocean Mission: India's Gateway to the Ocean Floor" (17 Aug 2025, sources ISRO and MoES).**
- "a self-propelled manned submersible capable of transporting three individuals to depths of up to 6,000 meters";
  "built to work for 12 hours of operational period and sustain up to 96 hours in emergency scenarios";
  "high-density Li-Po battery, underwater acoustic telephone, drop-weight emergency escape mechanisms, and bio-vests".
- "a spherical titanium-alloy vessel (Ti6Al4V - ELI grade) with a diameter of 2260 mm and wall thickness of 80 mm,
  designed to withstand 600 bar pressure and temperatures as low as -3°C"; EBW by LPSC, "Perfection of the process
  was achieved after 700 trials"; checked by TOFD and DLA PAUT. Built by NIOT with VSSC, ISRO.
- **The human story:** "The expedition was conducted on August 5 and 6, 2025 in collaboration with IFREMER … aboard
  IFREMER's submersible Nautile." "Indian aquanauts – Senior Scientist Shri Raju Ramesh and Cdr. Jatinder Pal Singh
  (Retd) from NIOT, Chennai completed their inaugural seven-hour deep sea dives" to about 5,000 m. India's first
  aquanauts learned to dive in a French machine first. (Real people: real photos only, never recreated faces.)
- Plan in Aug 2025: "shallow water demonstration up to 500 meters by early 2026 … integration and deep-water tests by
  mid-2027 and scientific explorations using MATSYA-6000 during 2027–28." (Slipped: the foam; see §1.)
- Deep Ocean Mission launched 7 Sep 2021, "₹4077 crore spread across five years". OMe 6000 (autonomous) surveyed
  the nodule site at 5,271 m in Dec 2022.

**Why the deep sea matters to India (the "so what" for the landing).** India has held an International Seabed
Authority contract since 25 March 2002 to explore polymetallic nodules over about 75,000 sq km of the Central Indian
Ocean Basin, about 2,000 km south of India's tip (PM India / Cabinet release). The nodules hold nickel, copper and
cobalt ("of economic and strategic importance"), the metals of batteries; the second extension (Feb 2023) assumes
India can move to exploitation at its end (ISA press release). PIB: mining waits for "global rules … set by the
International Seabed Authority". Honest frame: Matsya is a science and survey vehicle, not a mining machine; mining is
contested and not yet allowed.

**Titan, for the contrast (with dignity: five people died, 18 June 2023).** US Coast Guard Marine Board of
Investigation, 5 Aug 2025: primary factors were OceanGate's "inadequate design, certification, maintenance and
inspection process"; the passengers "were exposed to approximately 4,930 pounds per square inch of water pressure".
NTSB: hull damage after dive 80, imploded on dive 88. Titan's hull was carbon fibre with titanium end caps, a
cylinder, never certified. Matsya: a titanium sphere designed for 600 bar. 4,930 psi ≈ 340 bar (OUR CALCULATION).
Use only what the reports say; never show or imply the victims; no implosion sound effects.

**Demand (`scripts/yt_demand.py`, gl=IN, 2026-11-09; `assets/demand/`).**
- "Matsya 6000": 17 autocomplete phrases (matsya 6000 mission, samudrayaan matsya 6000, matsya 6000 in hindi);
  **no long video over 100K**; the top long one is CNN-News18, 35K. Supply is empty.
- "Titan submarine": 42 phrases including **Tamil, Malayalam and Hindi** variants; 8 long videos over 1M; Dhruv
  Rathee's "Mystery of Titan Submarine" 17.7M. Indians are hungry for this subject.
- "deepest submarine dive": 26 phrases, 7 long over 1M (Astrum 13.3M).
- So: the demand lives in Titan and "how deep can a submarine go"; the supply for India's own machine is nil. A title
  that borrows the curiosity (the sphere, the pressure, Titan's lesson) and lands on Matsya fills an open gap.

**Our channel's own audience (Analytics, 90 days):** 90% of views come from the home feed, viewers are mostly men
35+, 47% of watch time is on TVs, half the views from India and a large NRI share. A Titan-adjacent, big-picture,
deep-sea film suits browse and the TV screen.

## 6. Open research (next session)
1. ISRO's own weld release (original of the 700 trials / 32 minutes / 7,100 mm figures); NIOT design papers on the
   sphere (inner diameter, safety factor, test pressure: was the sphere pressure-tested, where, to what?).
2. The foam: what syntactic foam is, why it is imported, who makes it (the March 2026 Lok Sabha answer verbatim; UNI
   blocked, try sansad.in / PIB).
3. The 2021 mild-steel sphere test to 6,000 m: primary source.
4. Peers with primary sources: Fendouzhe (titanium sphere, 10,909 m, 2020), Jiaolong, Shinkai 6500, Nautile, Alvin;
   the "sixth country" claim is contested (5,000 m vs 6,000 m framing): attribute or drop.
5. The physics of why a sphere, why titanium (vs steel, vs carbon fibre), and why a weld is the weak point; a
   textbook or classification-society source (DNV / ABS rules for human-occupied vehicles).
6. Picture sources: PIB/ISRO photos of the sphere, NIOT/DD clips of Kattupalli, IFREMER Nautile dive photos (licence),
   USCG Titan report figures (US government work).
