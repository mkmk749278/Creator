# Research landscape: what everyone says vs what it actually is (first pass, 2026-11-09)

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

## 5. Open research (next session)
1. Primary sources: ISRO/LPSC weld release (the original), NIOT sphere design paper(s), PIB DOM document, Parliament
   answers (2025–26), the steel-sphere 2021 test.
2. Titan: the USCG MBI final report (date, depth of loss, hull cause) and NTSB, for the contrast; no speculation.
3. Peers: China's Fendouzhe (titanium sphere, 10,909 m, 2020), Japan's Shinkai 6500, Alvin, Limiting Factor; which
   countries have crewed 6,000 m capability (the "sixth country" claim needs checking).
4. Why spheres, why titanium (vs steel, vs carbon fibre), buckling and imperfections; the foam's job.
5. The open question for the film's landing: when the 500 m and 6,000 m dives happen (re-search on upload day).
6. Demand: `scripts/yt_demand.py` for search phrases (Matsya 6000, Samudrayaan, deep sea submarine India, Titan).
