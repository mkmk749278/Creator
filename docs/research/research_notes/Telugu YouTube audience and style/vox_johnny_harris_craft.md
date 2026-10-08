# Craft benchmarks: Vox (Vox.com, Borders, Atlas), Johnny Harris / Newpress, and comparable channels (ColdFusion, PolyMatter, MagnatesMedia)

Research date: 2026-10-08. Scope: transferable craft techniques (structure, visuals, sound, sourcing, retention, criticism) for a small Telugu documentary channel (one owner + AI-assisted HyperFrames/FFmpeg cloud rendering).

Source-quality note for the report writer: primary first-person sources (creator interviews, a Harris-authored aescripts article, a Ryan Shields podcast) are rare and several key ones were only reachable as summaries. Nieman Lab (2026-03) and the Newpress site returned HTTP 403. Many "Johnny Harris style" pages are tutorials or freelancer ads describing *imitations*; those are labelled as such. Where I describe what the videos look like from general viewing knowledge without a source, it is put under **Inferences**, not Cited Findings.

---

## 1. Story structure: openings, act structure, "explain the mechanism" segments, endings

### Takeaway
The documented rule across Vox and Harris is "story first, visuals as anchors": pick a topic only if it has distinctly visual elements, build the script around a visual anchor (often a map or a physical object), frame the piece around questions, and aim for a beginning–middle–end arc rather than a news recap. Explicit published "act templates" from these creators were not found; Harris says he deliberately has no template.

### Cited Findings
- Vox video founder Joe Posner's core rule: only tell a story on video if it has distinctly visual elements; stock footage over narration does not count. His early format was an "animated opinion essay" (expert filmed, animations illustrate their points). — [Simon Owens, The Long Story, 2025-06-03](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
- Vox Atlas producer Sam Ellis: "We do the story first"; Vox leads with the story and keeps viewers with an entertaining narrative. He prefers a story arc with a beginning, middle and end, and built his Egypt new-capital video from questions ("why move the capital so far? did earlier cities outside Cairo succeed?") rather than from a single news event. Visuals come first at a surface level: he spots a map and judges whether it can carry a story, then writes the story around the map. — [Storybench, Zoe Baumgartner, 2022-11-01](https://www.storybench.org/?p=14818)
- Harris emphasises "visual anchors" to keep viewers engaged (with tips for finding them without travel), uses a two-column scripting process (script + visual direction), and discussed "Choosing Visual Hooks and Soundbites" using his Elon Musk video as a case study. One video's research filled a "188-page doc". (Episode chapter summary, not transcript.) — [Created with Jon Youshaei, 2024-11-12, via Podwise summary](https://podwise.ai/episodes/2768274)
- A former student now producing for Vox recommends a two-column document: script on the left, visual ideas (b-roll) on the right; and to test clarity by explaining the story to a friend starting with the word "so". — [JEA, "Video explainers engage readers"](https://jea.org/?p=2802)
- Harris on his 2026 series *The Human Element*: "We don't have a checklist, I don't have a template…"; stories are built around a specific visual experience he is obsessed with ("The answer is obsession and curiosity"). It was the first time he did real development (months of watching films, setting art direction, gathering visual references). — [The Publish Press, 2026-06-05](https://news.thepublishpress.com/p/how-johnny-harris-is-reimagining-the-travel-show)
- Adobe MAX 2025 session by Harris: "curiosity over clicks and stories over soundbites"; storytelling is about "how you invite others to care", "visual-first approach". (Session description only; content not retrieved.) — [Adobe MAX 2025 OS558](https://www.adobe.com/max/2025/sessions/scrappy-smart-and-human-the-future-of-storytelling-os558.html)
- Howtown (Joss Fong, Vox video co-founder, and Adam Cole): a "confused voice" device, where the co-host voices the viewer's confusion ("Could you explain this a little bit more?") through unscripted conversation; they say Vox did not do this. — [Storybench, 2025-07-28](https://www.storybench.org/?p=24033)
- ColdFusion's Dagogo Altraide calls his method "the distilling of information… thinking about the info coming in, processing it". — [Tubefilter, 2017-10-19](https://www.tubefilter.com/2017/10/19/youtube-millionaires-cold-fusion-tv/)
- PolyMatter's Evan teaches a workflow of topic selection → research → crafting a story → script → graphics → colour → shapes → animation → assembly; he writes and animates every video alone. — [Skillshare, "Make Animated YouTube Videos"](https://www.skillshare.com/classes/How-to-Make-an-Animated-YouTube-Video/1143408374)
- MagnatesMedia describes its videos as "mini movies about business & money"; a third-party description characterises the format as dramatic narration over stock/archive b-roll, single-company case studies of 10–20 minutes, no on-camera presence (outside characterisation, not the channel's own). — [Faceless.my](https://faceless.my/youtube/channels-like-magnatesmedia/); [vidIQ channel page](https://vidiq.com/youtube-stats/channel/UCE4Gn00XZbpWvGUfIslT-tA)

### Inferences
- Production rule candidates: (a) a topic passes only if at least one strong "visual anchor" exists (map, document, place, object, archival clip); (b) every script is written in a two-column format (VO | visual), which maps directly onto our EDL; (c) frame each film around 1–3 explicit questions stated early and answered in order (Ellis' Egypt method); (d) do a "so…" one-paragraph explanation test before scripting.
- Unsourced viewing observations (verify before using as rules): Harris often opens cold on a striking object/place/question and his own on-camera stake ("I went to…", "I found this document…"), then a title card; Vox explainers commonly open on a surprising chart or a contradiction and end by returning to the opening question with an implication for the viewer. No interview was found confirming these as deliberate formulas.
- The "confused voice" device could be adapted for a solo Telugu narrator as on-screen rhetorical questions in VO ("అయితే ఇది ఎలా సాధ్యం?") rather than a second host. This must respect our rule of no full-screen question-mark graphics.

### Gaps
- No first-person transcript of Harris' "Stages of a Johnny Harris Video" chapter (Youshaei) or his Adobe MAX talk was retrievable; only chapter titles.
- No Vox published guidance on cold opens or endings was found; Joss Fong's NYU "Vidsplaining" talk (2019) may contain it but no transcript was found.

---

## 2. Visual techniques and tools

### Takeaway
The signature looks are reproducible with modest tools: maps from open GIS data animated with camera easing (GEOlayers/After Effects at Harris; we can do the same with SVG/GSAP or Three.js), physical props and paper documents shot or simulated with a moving camera, textured overlays + grain + vignette, still photos animated with slide-in, blur and a projector SFX, "match cut on text" montages, and 12 fps stuttered graphics in a 24 fps edit. Vox gives every video its own art direction.

### Cited Findings
**Maps (Harris / Newpress)**
- Harris's map animations are built in After Effects with the GEOlayers plugin; aescripts' "Why Indonesia is Always Erupting" breakdown covers a globe template, imported map data, drawn volcano features, country overlays, globe animation and film grain, plus Video Copilot Orb and Deep Glow for glow effects. — [aescripts, Making maps for Johnny Harris – Volcanoes](https://aescripts.com/learn/making-maps-for-johnny-harris---volcanoes/)
- Harris authored an aescripts article "How Johnny Harris Makes Maps" (posted 2022-07-01) about using GEOlayers, describing the workflow as "8 years in the making" (full text not retrieved). — [aescripts](https://aescripts.com/learn/how-johnny-harris-makes-maps/)
- Jason Boone (freelancer contacted by Harris' producer in 2021) animated map sequences for Harris (volcanoes, tectonic plates, Nazi invasion of Europe, Cyprus borders, Russian invasion of Ukraine). His workflow: place track points in Google Earth Studio, export 3D camera data to After Effects, a script builds the AE project with a 3D camera and nulls with attached text; text call-outs and shape layers stay locked to terrain. — [PremiumBeat, Jason Boone, 2022-03-24](https://www.premiumbeat.com/blog/making-maps-for-johnny-harris/)
- Google Earth Studio licensing: at least as of a 2021-era review, non-commercial only (news, research, education, nonprofit allowed; no commercial licence). Terms should be rechecked. — [No Film School / search summary](https://nofilmschool.com/animated-maps-adobe-after-effects)
- Ryan Shields (Newpress, Harris' channel) on 2026 tooling: base layers from **Natural Earth** (borders, hillshades, rivers, disputed-territory/point-of-view datasets); **CShapes** for historical borders by date (gaps mid-war → **Open Historical Map**); Sentinel-2 imagery and USGS DEMs; **GEBCO** bathymetry via GDAL; Swiss-style hillshades from **Eduard** or Tom Patterson's Shaded Relief; **Mapshaper** to convert GeoJSON → SVG (e.g. one SVG per year for a submarine-cable video); MapTiler Engine for tiling and georeferencing old maps; GDAL pipelines run by Claude Code on new bounding boxes; GeoLayers 3 is Mercator-only, so other projections are rigged from Natural Earth strokes/fills. He values fine control of camera easing. — [MapScaping Podcast, 2026-05-28](https://mapscaping.com/podcast/10-tools-for-telling-stories-with-maps/)

**Maps (Vox)**
- Sam Ellis (Vox Atlas): maps animated over aerial/drone footage; alternating bird's-eye map view and ground footage to help viewers follow; layout = animated maps + news clips + photos + data viz in ~10-minute pieces; often works from maps a cartographer already made, and traced maps from old books for the Egypt video; geolocated datasets (e.g. well locations as dots) are easiest. — [Storybench, 2022-11-01](https://www.storybench.org/?p=14818)
- Vox art director Joey Sendaydiego: maps are among the most tedious graphics; colleagues help check that changing borders are accurate. — [Storybench, Heidi Ho, 2024-04-18](https://www.storybench.org/?p=21229)

**Art direction, paper/collage, props**
- Vox sets a unique art direction per video: "Teaching in the US vs. the rest of the world" was handcrafted from construction paper (a paper clock turned into a pie chart); "Computers just got a lot better at writing" used flying words as a recurring motif; the Fred Hampton video borrowed the style of Black Panther protest posters. Sendaydiego sketches and tests in After Effects. — [Storybench, 2024-04-18](https://www.storybench.org/?p=21229)
- Vox Earworm ("The most feared song in jazz") layered interviews with illustrations, props, sheet music, stop animation and archival footage; "Rapping, deconstructed" used illustrated audio mixers and colour-coded lyrics. — [The Long Story, 2025-06-03](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
- Harris uses physical props and manual inputs (papers on a desk) with creative camera angles to enrich A-roll (example: MLK assassination conspiracy video); animators imitate it by moving a virtual camera over flat 2D papers. Another RNDR piece credits his aspect ratio for a film feel and colour grading plus aged-looking pages for transporting viewers in time. — [RNDR Newsletter, Rickie Ho, 2024-04-06](https://rndr.beehiiv.com/p/5-visuals-next-video-ead0); [RNDR (other issue)](https://rndr.beehiiv.com/p/5-visuals-next-video-57b6)

**Photo animation, text montages, textures (tutorial imitations, not Harris' own description)**
- "Vivid still photos": photo slides in over ~8 frames with ease-in, Gaussian blur keyframed from ~50 to 0 on the same frames, plus an old camera/projector SFX. "Match cut on text": ≥12 scans/screenshots of the same word/phrase centred, first clips ~8 frames, getting shorter, a camera-click SFX on each cut. "Textures": texture overlay with blend mode, blurred duplicate, inverted feathered oval mask (vignette). — [Motion Array, 2022-08-02](https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/)
- "Vox look": graphics comp at 12 fps inside a 24 fps edit for stutter; backward 3D camera move with a short blur peaking at the cut; rough jagged-edged textures behind lower thirds, 5–6 textures cycling 2–3 per second for a living background; jagged frame-skipping mask reveal with text offset by a few frames; slight chromatic aberration and blur (3.5) at frame edges via a feathered circular mask (feather 50) for 2D images and news clippings. — [PremiumBeat, Lewis McGregor, 2021-03-08](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)

**Rhythm**
- ColdFusion: "no scene should last more than five seconds. The images themselves should tell most of the story"; fades lead the viewer between concepts. — [Tubefilter, 2017-10-19](https://www.tubefilter.com/2017/10/19/youtube-millionaires-cold-fusion-tv/)
- A (AI-generated, low-reliability) breakdown of a Harris scene counts 18 distinct clips in a scene of nearly one minute (≈3.3 s per clip). — [gist.ly summary](https://gist.ly/youtube-summarizer/master-johnny-harris-style-editing-in-capcut)

**Tools at the comparable channels**
- PolyMatter: Affinity Designer, Bear, Ulysses; "you don't need any paid software to get started". — [Skillshare](https://www.skillshare.com/classes/How-to-Make-an-Animated-YouTube-Video/1143408374)
- Vox staff were "jack of all trades" who learned After Effects and edited their own work. — [The Long Story](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)

### Inferences
- Nearly every documented technique maps onto HyperFrames: GSAP easing for map cameras; SVGs from Mapshaper/Natural Earth/CShapes (all free, open data) for borders by year; `steps()` or 12 fps-quantised tweens for Vox stutter; layered paper/grain textures; blur + slide-in photo entries; rapid "match cut on text" montages of real document scans (fits our "always moving" and "semantic lock" rules). Google Earth Studio should be avoided for monetised videos unless its licence has changed.
- The 2.5–4 s cut cadence in our CLAUDE.md is consistent with ColdFusion's ≤5 s rule and the ~3.3 s/clip estimate for Harris.
- "Per-video art direction" (Vox) suggests adding an art-direction line (palette, texture family, motif) to each project's EDL header, chosen from the genre looks in PLAYBOOK §5.3.
- On-camera presence: Harris' A-roll is himself at a desk with props; for a faceless or VO-led Telugu channel the transferable part is the *props/documents* layer, not the host.

### Gaps
- No primary source on Harris' or Vox's typography and colour palettes (fonts, hex values) was found.
- No sourced description of "live browsing"/screen-recording sequences (a known Harris/Vox device) was found.
- 2.5D parallax of photos is described only by freelancer listings ([Fiverr](https://it.fiverr.com/bashirbineez/do-magnatesmedia-style-of-editing)), not by the creators.
- Vox Darkroom (archival-photo series) was not researched.

---

## 3. Sound: music, silences, risers, SFX

### Takeaway
Sound is the least documented area. Harris now has a full-time composer on staff; in 2016 he licensed library music via APM Music (and used Bonobo tracks). Tutorial imitations attach a specific SFX to every graphic event (projector clatter on photo entries, camera clicks on text cuts). ColdFusion's creator produces his own ambient/electronic music.

### Cited Findings
- Harris' team includes producers, animators, editors and "a full-time music composer"; over 20 people. — [The Long Story, 2025-06-03](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
- Harris (2016, X): "we license our music thru APM music. Look up Bonobo. I used some of his music in the video." — [Johnny Harris on X](https://twitter.com/johnnywharris/status/760153646403350528?lang=en)
- A YouTube Short "Scoring a Johnny Harris video 1" shows intro score for the MLK assassination video (composer not named in the result). — [YouTube Short](https://www.youtube.com/shorts/I8VtS1EjJAs)
- Youshaei interview chapters include "sound design and music" as a production stage (content not retrieved). — [Podwise summary](https://podwise.ai/episodes/2768274)
- Vox's video style was built from "data visualization, animation, sound design, expert interviews, and narration". — [The Long Story](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
- Imitation recipes pair an old projector/camera SFX with each photo slide-in and a camera-click SFX with each text match cut. — [Motion Array, 2022](https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/)
- ColdFusion's Dagogo Altraide makes music as "Burn Water" (FL Studio, some Ableton Live), tracks used in ColdFusion videos. — [search summary of creator profiles; secondary](https://rosetta.to/u/coldfusion/topic/music)

### Inferences
- Rule candidates: every graphic event gets a matched SFX (whoosh on map camera move, paper rustle on document entry, click on highlighter/text cut, projector on photo entry), mixed under the VO; music changes at act boundaries. These are consistent with the cited imitation recipes but are not confirmed as Harris/Vox internal rules.
- For licensing, our equivalents of APM are licensed libraries logged in `media_manifest.csv`; Bonobo-style downtempo/ambient is the reference mood.

### Gaps
- No named composer for Harris' channel or for Vox Borders was found; no Vox sound-design interview was found (searches only returned job postings).
- No sourced data on use of silences or risers by any of these creators.

---

## 4. Sourcing and trust: citations, source cards, corrections, document display

### Takeaway
Vox and Harris show documents and news clippings on screen as visual evidence, but formal transparency is recent and uneven: Harris did not cite sources until September 2022, and only after public criticism; Vox has pulled videos after finding inaccuracies. YouTube now (Dec 2025) has a native "Correction:" timestamp feature that shows an info card at the corrected moment.

### Cited Findings
- Harris did not cite sources until September 2022, after Jochem Boodt's criticism and the James Somerton plagiarism scandal; McGill's Jonathan Jarry argues "high production values give the illusion of scholarship" and quick cuts/montages make errors easy to miss. — [McGill OSS, "The Many Mistakes of Johnny Harris", 2024-08-02](https://www.mcgill.ca/oss/node/10015)
- A secondary (and promotional) blog claims each Harris video now has "a time-coded, academic-level bibliography" with every assertion footnoted, a 6-week research stage with a research producer, a 3-week scripting/fact-check stage with a Story Editor, and ~3 months of visual production for ~45-minute explainers; it cites no specific interview. Treat as low confidence. — [Robb Montgomery](https://robbmontgomery.com/how-johnny-harris-built-a-7-5m-subscriber-newsroom-without-selling-out/)
- Vox has pulled videos after discovering inaccuracies; production to publication takes "two to three weeks max". — [Storybench, 2024-04-18](https://www.storybench.org/?p=21229)
- Vox's sensitive-topic approach: prioritise respect and accuracy; since animation rarely uses graphic photos, avoid downplaying serious events with misleading positivity. — [Storybench, 2024-04-18](https://www.storybench.org/?p=21229)
- Howtown: about half of a ~six-week feature is research and reporting; Fong emails experts directly; printed data visualisations on paper to walk through reasoning on screen. — [Storybench, 2025-07-28](https://www.storybench.org/?p=24033)
- YouTube corrections (announced 2025-12-10): add a description line beginning "Correction:"/"Corrections:" (in English), then a chapter-style timestamp and explanation (e.g. "1:00: This happened in 2011, not 2010."); an undismissable info overlay appears at that timestamp and links to the description. — [PPC Land](https://ppc.land/youtube-adds-inline-corrections-feature-for-published-videos/). Conflict: MobileSyrup's URL suggests a similar feature in June 2022 — [MobileSyrup](https://mobilesyrup.com/2022/06/15/youtube-corrections-fix-mistakes-video/); unresolved.
- Newpress also sources "lived experiences" from its community platform (≈40,000 users; for Taiwan: hundreds of perspectives, 13 contributors, a two-hour meetup in Taipei) — secondary, low confidence. — [Robb Montgomery](https://robbmontgomery.com/how-johnny-harris-built-a-7-5m-subscriber-newsroom-without-selling-out/)

### Inferences
- Rule candidates: (1) a timestamped source list in every description from day one (do not repeat Harris' 2020–22 gap); (2) on-screen source line (outlet + date) on every chart, document and clipping; (3) show real documents with a moving camera and highlighter sweeps on the exact phrase the VO reads (semantic lock); (4) publish corrections using YouTube's "Correction:" line and a pinned comment; (5) polish is not proof: our fact-check gate must be independent of how good the cut looks.

### Gaps
- No Vox written corrections policy for video was found.
- Could not verify the Montgomery pipeline durations from a primary source (Nieman Lab 2026 article returned 403).

---

## 5. Retention: length, pacing, hooks, data

### Takeaway
Few hard numbers are public. Vox reports average watch time of about four minutes and judges success by retention; Vox Atlas pieces run ~10 minutes, Howtown 15–20, Harris' long explainers far longer (~27-minute average in one 2024 count). Their audience leans young and male, responds to maps and conflict, and airplanes in thumbnails do well.

### Cited Findings
- Vox measures success by retention; average view time ~4 minutes, "well above typical YouTube figures"; audience mostly millennials; ~12 M subscribers (2024); 1–2 uploads/week. — [Storybench, 2024-04-18](https://www.storybench.org/?p=21229)
- Vox Atlas: ~10-minute pieces; audience mostly men 19–29 who respond to conflict and maps; "any thumbnail with an airplane in it does really well"; Egypt video took five weeks. — [Storybench, 2022-11-01](https://www.storybench.org/?p=14818)
- Harris: nine videos in three months averaging 27 minutes (per Jarry's count, 2024). — [McGill OSS](https://www.mcgill.ca/oss/node/10015)
- Harris published standalone videos roughly every two weeks before pausing for *The Human Element*; he values "millions of people who show up every week for years" over an Emmy. — [The Publish Press, 2026-06-05](https://news.thepublishpress.com/p/how-johnny-harris-is-reimagining-the-travel-show)
- Borders: >143 M views, ~4 M per video; Harris' flat-earth explainer ~13 M views. — [The Long Story](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
- Howtown grew to >800,000 subscribers in its first year largely through Shorts adapted from long-form; long-form average rose from ~311,000 to 778,000 views; Fong warns against "sugar rush" viral videos and uses Shorts only to introduce the channel. — [The Long Story](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube); [Storybench, 2025-07-28](https://www.storybench.org/?p=24033)
- Sendaydiego's advice: don't chase perfection; overly polished visuals can make a piece look like an ad; "if it's interesting, people will want to watch it". — [Storybench, 2024-04-18](https://www.storybench.org/?p=21229)

### Inferences
- Shorts cut from each long-form film (Howtown's pattern) are a low-cost growth channel we can render from the same HyperFrames scenes in 9:16.
- Thumbnail rule candidate: a concrete object/vehicle/place (Ellis' airplane note) beats abstract imagery; test per topic.

### Gaps
- No published retention curves or hook timing data from Harris or Vox were found (see the sibling note `youtube_retention_policy.md` for general YouTube data).

---

## 6. Criticism and responses

### Takeaway
The main criticisms of Harris are oversimplification, factual errors, sensational framing, and a sponsor conflict (a World Economic Forum co-written video disclosed only at the end). His responses have been informal (comments, brief on-video apologies), and he admits being "intoxicated by a good, mysterious story". The lesson: style amplifies errors, so research and disclosure must scale with polish.

### Cited Findings
- Jarry (McGill OSS) lists errors: azodicarbonamide cancer/asthma claims; an appeal to nature on bread; UAP coverage omitting ~12,000 USAF-investigated reports; calling AUKUS submarine tech a "gift" (estimated cost $268–368 bn); an inflation definition criticised by economics teachers; Columbus framing (per Jochem Boodt). "How China Became So Powerful" was co-written with the WEF, disclosed only in the final minute; Jarry calls it "neither education nor journalism". — [McGill OSS, 2024-08-02](https://www.mcgill.ca/oss/node/10015); [Wikipedia](https://en.wikipedia.org/wiki/Johnny_Harris_(journalist))
- Harris' responses: admitted in comments on Boodt's video that he dramatised Columbus as a "device/symbol"; in his Bermuda Triangle video said "I'm sorry. Can we move on, please?" and admitted getting "intoxicated by a good, mysterious story". — [McGill OSS](https://www.mcgill.ca/oss/node/10015)
- Kyiv Independent (Dec 2024) criticised "Why People Blame America for the War in Ukraine" (2024-12-05) as echoing Kremlin talking points on NATO expansion and "trading facts for sensationalism"; noted NATO bordered only ~378 km of Russia's 57,792 km border before Finland joined. No public response from Harris found. — [Kyiv Independent](https://kyivindependent.com/youtuber-johnny-harris-lens-on-eastern-europe-is-distorted-and-irresponsible/)
- Positive counterweight: Borders was twice Emmy-nominated; Harris won an Emmy for NYT Opinion work (2022) and, with Newpress, the News Outstanding Graphic Design Emmy (May 2026). — [Wikipedia](https://en.wikipedia.org/wiki/Johnny_Harris_(journalist))
- A forum user calls his videos "very surface level" (anecdotal). — [Tildes](https://tildes.net/~transport/13az/the_real_reason_ships_go_missing_in_the_bermuda_triangle)

### Inferences
- Rule candidates: disclose any sponsor or partner at the start, not the end; never let a "mysterious story" framing outrun the evidence (present claims as claims, which already matches our CLAUDE.md); for geopolitical topics, show the counter-evidence on screen (e.g. the border-length fact) rather than one causal narrative; keep a public corrections log.

### Gaps
- No documented Vox-specific criticism or response was researched in depth.
- Harris' "conflicts of interest" beyond the WEF video are not detailed in available sources.

### Context: business and organisation (brief)
- Newpress (launched Feb 2026, CEO Iz Harris) runs creator-journalist channels (Search/Party with Sam Ellis, Tunnel Vision with Christophe Haubursin, The Bigger Picture with Max Fisher); funded by ads, sponsors and a membership (price conflicts: $60/year per Wikipedia, $60/month per Tubefilter, $5/month per The Publish Press). — [Wikipedia](https://en.wikipedia.org/wiki/Johnny_Harris_(journalist)); [Tubefilter, 2026-03-12](https://www.tubefilter.com/2026/03/12/johnny-harris-newpress-creator-journalist-production-company-platform/); [Nieman Lab, 2026-03](https://niemanlab.org/2026/03/with-newpress-iz-and-johnny-harris-incubate-video-journalism-for-the-creator-era) (not readable, 403)
- Vox laid off about half its video team in late 2023; many alumni (Harris, Cleo Abram, Phil Edwards, Fong/Cole) went independent. — [The Long Story](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
