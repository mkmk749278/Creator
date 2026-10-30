# pharma-apis: picture-to-word audit (round 6)

**Why:** the owner's review on 30 Oct: "3:36 to 3:40 and 4:10 to 4:15… what are the visuals showing… while showing
industries' names what are we showing… narration to scene, every second, word by word, scene by scene."

**How:** all 181 shots of the final 4K master were listed against the words spoken over each one, with one frame per
shot (`hyperframes` part HTML + the VO's word gaps from `silencedetect` on `vo_film.wav`). Each shot is graded:
**WRONG** (the picture says something else), **WEAK** (it fits the topic but not the words), **OK**.
Times are the 4K master's (11:28.3).

## WRONG: fixed in this round

| Time | Words | Was on screen | Now |
|---|---|---|---|
| 1:36.6–1:42.8 | "First, let's give India its due… India earned it." | A Chinese softgel line (Pixabay) | Cipla's own plant, 8 caption-free shots |
| 2:32.4–2:37.2 | "Indian companies are world class at that last part." | The same Chinese softgel line | Cipla's chief in his plant and Cipla's line (no lower thirds) |
| 2:40.6 | "…the toughest inspections on the planet." | A Western stock model with a green flask | Lyfius's quality lab, Kakinada |
| 3:35.6–3:44.9 | "Pimpri, near Pune. 1954. India has been free for less than seven years, and it's building a factory to make its own penicillin." | A British lab drawing of a culture box | New scene `pimpri`: India map → Pimpri pin; a 15 Aug 1947 → 1954 line fills, "< 7 YEARS FREE"; the factory rises out of the ground with a crane, lights on, tricolour on the roof, "PENICILLIN FACTORY" |
| 3:44.9 | "Penicillin was the miracle drug of that time." | A potency chart | The 1944 I.C.I. film's own penicillin vials |
| 4:05.1–4:15.0 | "Picture your grandparents' India. A young, poor country, growing one of the most important medicines on earth… in its own factory." | India map, then the potency chart | New scene `pimpri_grow`: the plant at dusk, a cyclist on the road (grandparents' India), the wall opens on a fermenter turning gold (growing), vials roll out of its door (its own factory) |
| 4:15.0–4:24.2 | "Soon, others join in — Alembic, Sarabhai and Ranbaxy. India is making its own antibiotics." | A modern stock lab, three name boxes | New scene `skyline_rise`: Pimpri stands alone; Alembic, Sarabhai and Ranbaxy each rise on their own name (word times 3.37 / 4.13 / 5.07 s); all light up on "making its own antibiotics" |
| 6:43.8–6:48.2 | "Then, one by one, the Indian penicillin plants went quiet." | Stock gears | New scene `skyline_dark`: the six plants named in the film, lit and smoking; on "went quiet" the smoke thins and the lights drop |
| 6:55.5–7:04.8 | "Torrent. Ranbaxy. Sarabhai. Stopped. … Alembic. Stopped." | Stock gears with a list of name boxes | The same skyline: Torrent, Ranbaxy and Sarabhai go dark on their names, STOPPED stamps on "Stopped.", Alembic last. H.A. and I.D.P.L. keep their real footage, each with its own name and stamp |
| 7:04.8–7:11.9 | "India was importing all of that base powder…" | A port aerial with a hazard-marked ship deck in the middle | The two clean stretches of the same port aerial |
| 8:26.7–8:36.2 | "In 2024, the tanks start running… growing its own penicillin again." | Aerials of bare land on "tanks start running" | The Kakinada plant's tank farm and fermenter hall |

The four new scenes are drawn, labelled ILLUSTRATION, and use the voice's own word times. No new facts: the names,
places and years are the narration's own. No film of 1950s Pimpri, Alembic, Sarabhai or Ranbaxy could be found: the
YouTube search through the channel's API returned nothing usable (`research/yt_search_r6.json`).

## WEAK: kept, with the reason

| Time | Words | On screen | Why it stays / what would beat it |
|---|---|---|---|
| 0:00–0:06.7 | "India sells medicines to around 200 countries… pharmacy of the world." | Close-up of tablets in a strip (Pexels) | The open matches the thumbnail (capsules). An Indian export carton line would be better; none cleared |
| 1:11.2–1:19.3 | "So here's the question… who makes the powder inside India's medicine?" | Pink tablets (Pixabay) | A question beat over the product itself |
| 1:19.3–1:26.5 | "…this isn't about the quality of your medicines. It's about who controls the supply." | Hands opening a blister (Pexels) | Shows the medicine; "supply" is carried by the chips |
| 2:42.4, 3:23.9 | "But the powder you swallow?" / "Has it always been like this? Did India ever make its own powder?" | Grey blister packs (Pixabay) | Question beats |
| 5:54.9 | "And that's exactly where India's story turns." | Pink tablets | A turn line with no object |
| 6:10.2–6:24.0, 7:28.7 | "China went all in… huge plants, in huge drug parks, cheap power, cheap water… looser pollution rules" / "would you build a plant here?" | A smoking chimney at sunrise (Pixabay) | Fits "pollution", not "huge drug parks". **To fix: real footage of Chinese pharma plants** (below) |
| 7:22.1–7:28.7 | "Niti Aayog estimates Chinese powder costs 35–40% less…" | A Chinese worker at a filling machine (Pixabay, ILLUSTRATIVE) | Chinese production; would improve with the same China footage |

## OK (the rest, 150 shots)

Real documents on every document line (DGFT order, NITI Aayog, budget speech, PLI press note, MIP notification, PSU
Watch); the Wuhan footage on Wuhan; the Tribune on the 2020 chemists; MSF and AP Pretoria on 2001; the Cipla price
scene; the tablet, fermenter, chain, tanks, mill, gate and lesson scenes on their mechanisms; Cipla's line on
"mixing, pressing, packing, inspections" (cut in the voice's own word gaps, measured 157.32 / 158.13 / 158.85 /
159.48 s); I.C.I. 1944 on "a small cut could kill you"; H.A.'s signboard and workers, I.D.P.L.'s gate; Lyfius's
plant on Kakinada; the maps on the places named.

## For the owner: China footage (Termux)

To replace the chimney at 6:10 and 7:28 with real Chinese drug plants, one line in Termux (short news excerpts, credited
on screen):

```
curl -sL https://raw.githubusercontent.com/mkmk749278/Creator/main/scripts/termux_fetch_to_drive.sh | bash -s -- English/pharma-apis "https://www.youtube.com/watch?v=9c-PcIWGwQY" "https://www.youtube.com/watch?v=mXsHcF87-Is" "https://www.youtube.com/watch?v=O4ieRydnKyI"
```

(CGTN, "Pharma companies in China work at full capacity", 2022; CCTV Video News Agency, "China's Pharmaceutical
Industry Speeds up Innovative Breakthroughs", 2026, and "Global Pharmaceutical Giants Step up Investment", 2026.)
