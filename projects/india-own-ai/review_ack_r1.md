# Review acknowledgement, round 1 → cut r2 (2026-11-03)

Cut reviewed: `india_own_ai_r1_720.mp4` (13:06.9). The r2 cut keeps the same VO and timing, so every time below
is the same in r1 and r2.

## The owner's notes

| # | Note (owner) | Status | What changed, with evidence |
|---|---|---|---|
| 1 | "Narration to visuals... not matching at all. While we are saying names, verbs or anything we need to show that clip, even one or two seconds." | **FIXED** | Every name, place, number and key verb now gets its own picture on the word: **92 word-level cutaways** (1.0–2.4 s each), cut 0.15 s before the word. The cut went from 167 shots to 268. Plan: `word_map.md`. Word times: `build/words.py` (silencedetect pauses + letter-weighted spread, no speech recognition). Check: `build/word_audit.py`, one frame per cutaway labelled with its word (`qa/word_audit_1..4.jpg`). Examples: "Chinese" 0:14.6 → a Beijing street; "Marathi" 0:17.9 → Pune; "Telugu" 0:19.5 → Hyderabad's cable bridge; "America? China? here?" 1:12–1:15 → the U.S. flag, the Chinese flag, the tricolour over an Indian city; "Nvidia" 1:47.6 → Jensen Huang (Nvidia CEO) with his name; "Delhi" 2:06 → India Gate; "Taiwan" 6:07 → Taipei 101; "America's government" 6:18 → the White House; "scrapped" 6:36 → the BIS rescission release itself; "investors" 7:30 → the NYSE; "French" 8:38 → Paris; "Maharashtra" 10:47 → Mantralaya; "Hindi, Telugu, Bengali, Odia" 11:57 → Varanasi, Hyderabad, Kolkata, Odisha. |
| 2 | "All should look real and should match situation too." | **FIXED** | Only real camera footage, real photos and real documents. Rejected by eye from the contact sheets: CGI flags (3), CGI satellites (2), a HUD globe, a cyber-padlock graphic, a green-screen calendar, a digital timer, a progress bar, CGI falling yuan, Western classrooms (2), a posed actor, a "Mumbai" skyline that is really Taipei, "rupee" notes that are Pakistani, and an "Aadhaar centre" photo whose sign is an MLA's office. Rupees use only the real Pexels clip of hands counting Indian notes. The Yotta clip (two men talking outside the building) now plays only on "India rented one". "Shared chips", "one common pool" and "bigger clusters" use real server-hall footage. No stock clip is used more than twice. |

## Our own round-1 notes (review.md)

| # | Item | Status | Evidence |
|---|---|---|---|
| 3 | Script names as boxes in the 13-language chart (10:18) and the 22 shelves (4:36) | **FIXED** | Gujarati, Kannada, Malayalam, Gurmukhi, Arabic, Ol Chiki and the missing Chinese glyphs are bundled. A render test with bundled fonts only showed no boxes. |
| 4 | Stand-ins for the minister, the summit, Sarvam's founders, BharatGen, NavIC | **FIXED** | Real footage from the owner's YouTube fetches: Vaishnaw at the IndiaAI briefing (2:06), the PM at Sarvam's stand at Bharat Mandapam (8:23, 8:54), Pratyush Kumar on NDTV (8:27), BharatGen's own reel (9:42), the NVS-03 lift-off on "Navik" (12:37). |
| 5 | Sparse animated plates for 1–2 s while elements build (1:56, 7:24) | **FIXED** | A real picture now runs dimmed under every plate where the VO names something: the Union Budget bars sit over Delhi's government buildings, the Meta brick wall over a construction site. |
| 6 | The very dark server-LED shot at 5:40 | **FIXED** | It no longer holds alone: "words" (5:37) cuts to real newspaper sorting first, and the LED shot only carries "a place to read it". |
| 7 | Shot-by-word audit not run | **CHECKED** | `qa/word_audit_1..4.jpg`: 92 frames, each against its own word. Fixed after the first pass: the dark laptop on "the people who built it" (now chip workers in a cleanroom), a blank frame on "Remember the chopper?" (cutaway removed), the NDTV stage with its own anchor captions on "from zero" (not used). |

## Also found and fixed
- **"12 MAY 2025", not 13 May.** The date card on "scrapped that rule" now matches the BIS release on screen, which is dated May 12, 2025 (claims.csv A45).
- **No fake screens:** the laptop clip on "They're engineers" (3:10) and "Can an Indian team train one from zero" (8:47) showed a made-up "Encrypting / Satellite uplink" hacker screen. Both lines now use real Indian engineers at work. That is a third use of each clip, on purpose: Pixabay has no other real footage of Indian engineers.
- The Nvidia clip's H100 close-up plays on "those Nvidia chips" (8:31), credited "NVIDIA · H100 MODULE".

## Open
- **"Mumbai" (I.I.T. Bombay, 9:42):** no real Mumbai footage exists on Pixabay (one result is Dubai, another Taipei), so the BharatGen reel carries the line.
- **"Aadhaar" (10:43):** no real Aadhaar-centre footage with a clear licence. The KISAN e-Mitra government chatbot clip stays under "Sarvam says".
- **Licences:** every new clip is logged in `media_manifest.csv` (Pixabay Content License, CC BY / BY-SA photos via Openverse, the NVIDIA excerpt credited on screen).
