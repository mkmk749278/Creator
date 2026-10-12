# Music: Can't Pay Even the Minimum (and the house sound for desk + doodle films)

Owner, 2026-10-12: "concentrate on background music, use Pixabay".

## How we get Pixabay music
- The `PIXABAY_API_KEY` covers photos and videos only; Pixabay's API has no music endpoint, and pixabay.com returns 403 to
  scripts from the cloud. Track pages can be read (WebFetch), so Claude shortlists and checks each track; **the owner
  downloads the MP3 on the phone** (Pixabay app or site → Download) and sends the files in the Claude chat. Files go to
  `projects/<slug>/assets/music/` (gitignored) with a row in `media_manifest.csv`.
- **Content ID rule:** many Pixabay tracks say "Content ID Registered" on their page. On YouTube those get a copyright
  claim and the artist can take the ad money unless you dispute with the licence. **We use only tracks whose page does not
  say Content ID Registered**, checked again on the day of download. Credit the artist in the description anyway.

## Mood map (one bed per act, never a wall of music)
| Part of the film | Visual mode | Music job | Level |
|---|---|---|---|
| Hook: the overdue message, the panic | Desk (big moment) | low pulse, tension, no melody | −24 to −26 dB under VO |
| Explaining: rules, slabs, how recovery works | Doodle | light, curious, steady rhythm; never comic | −24 to −26 dB, swells to −12 dB in pauses |
| Reveals (police? salary? court?) | Desk | 1.5 s of total silence, then a low hit | silence, impact −6 to −8 dB |
| Practical defence: what to do | Desk + doodle | warm, hopeful, calm | −24 to −26 dB |
| End card | Doodle | the hopeful theme resolves | swell to −12 dB |
Sound effects on every doodle item (pop, whoosh, scribble, rip, thud, clink) at −8 to −15 dB: `video/lib/doodle/make_sfx.py`.

## Shortlist checked on 2026-10-12 (track page opened, "Content ID Registered" absent)
| Mood | Track | Artist | Length | Page |
|---|---|---|---|---|
| Tension (hook, desk) | Investigative Ambient Pulse Forensic Noir Cinematic Drone | nxtlvl_snds | 2:45 | https://pixabay.com/music/low-drones-investigative-ambient-pulse-forensic-noir-cinematic-drone-456034/ |
| Tension (hook, desk) | Cinematic Crime Piano | Universfield | 2:47 | https://pixabay.com/music/pulses-cinematic-crime-piano-197925/ |
| Explaining (doodle), darker | Mysterious Fog Curious Discovery | alex-morgan | 1:30 | https://pixabay.com/music/electronic-mysterious-fog-curious-discovery-575877/ |
| Explaining (doodle), lighter | Pizzicato Flow | VitMatNotes | 1:28 | https://pixabay.com/music/cartoons-pizzicato-flow-558613/ |
| Explaining / build | Orchestral Pulse | VitMatNotes | 1:21 | https://pixabay.com/music/dramatic-classical-orchestral-pulse-558612/ |
| Turn to the defence | Unlocked | toddmagnuson | 1:05 | https://pixabay.com/music/orchestral-unlocked-590111/ |

**Rejected (Content ID Registered):** Atmosphere Pulse, Dark Minimal, Documentary Suspense, Dark Marimba, Documentary
Cinematic, and all 11 hopeful piano tracks checked (Hopeful Warm Music, Hopeful ×4, From Silence, Ambient Piano, Hopeful
Piano, Better Day, Piano Music, Main Title Hopeful).
**Hopeful bed still open:** no Content-ID-free hopeful track found on Pixabay yet. Options: YouTube Studio → Audio Library
(free, YouTube-safe; filter "Calm" / "Inspirational", attribution not required), or Incompetech (Kevin MacLeod, CC BY,
reachable from the cloud, credit line in the description).
