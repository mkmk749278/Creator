# Media credits: hook video (0:00–0:50)

Render: `renders/chipgamble-hook-1080p.mp4` (1920×1080, 30 fps, 50.5 s, −14 LUFS). The MP4 is gitignored; rebuild it with the steps at the bottom.
Composition: `video/chipgamble/hook/index.html` (HyperFrames 0.8.103).

Paste the **YouTube description block** below as-is. CC BY and CC BY-SA require attribution with the author, title, licence and a link.

## Real footage (Wikimedia Commons)
| Used at | What | Author | Licence | Source |
|---|---|---|---|---|
| 0:13–0:15 | Chips in a tray, pick-and-place line | STMicroelectronics | CC BY 3.0 | [How ST designs and manufactures semiconductor devices](https://commons.wikimedia.org/wiki/File:How_ST_designs_and_manufactures_semiconductor_devices.webm) |
| 0:18–0:24, 0:35–0:37, 0:39–0:42, 0:45–0:50 | Chip die close-ups, yellow-light cleanroom, cleanroom corridor, circuit board | IBM Research | CC BY 3.0 | [JSR and IBM Quantum envision a revolution in semiconductor manufacturing](https://commons.wikimedia.org/wiki/File:JSR_and_IBM_Quantum_envision_a_revolution_in_semiconductor_manufacturing.webm) |
| 0:29–0:35 | Container ship and terminal aerials (Port of Cork, Ireland; representative) | FILMING CORK | CC BY 3.0 | [Aerial views of a container terminal at the Port of Cork](https://commons.wikimedia.org/wiki/File:Aerial_views_of_a_container_terminal_at_the_Port_of_Cork,_Cork,_Ireland.webm) |

## Real photos (Wikimedia Commons)
| Used at | What | Author | Licence | Source |
|---|---|---|---|---|
| 0:00–0:12 | Aerial of new-car export lots (Emden/Papenburg area, Germany; representative) | Martina Nolte | CC BY-SA 3.0 DE | [DSCF7469](https://commons.wikimedia.org/wiki/File:2013-05-03_Fotoflug_Leer_Papenburg_DSCF7469.jpg), [DSCF7471](https://commons.wikimedia.org/wiki/File:2013-05-03_Fotoflug_Leer_Papenburg_DSCF7471.jpg) |
| 0:16–0:18 | Intel 8749H microcontroller die | yellowcloud | CC BY 2.0 | [EPROM-Microcontroller Intel 8749H (chip)](https://commons.wikimedia.org/wiki/File:EPROM-Microcontroller_Intel_8749H_(chip).jpg) |
| 0:27–0:29 | Taiwan from orbit | NASA Terra / MODIS (Jeff Schmaltz) | Public domain | [Taiwan NASA Terra MODIS 23791](https://commons.wikimedia.org/wiki/File:Taiwan_NASA_Terra_MODIS_23791.jpg) |
| 0:42–0:45 | Electricity pylons, Chennai | Aravindan Ganesan | CC BY 2.0 | [Electricity pylons Chennai IN 2017](https://commons.wikimedia.org/wiki/File:Electricity_pylons_Chennai_IN_2017.jpg) |

## Artificial / made in-house (no AI imagery)
- **Motion graphics:** maps, stat cards, the "UNSOLD" stamp, the supply-chain snap, price tag, title lockups. Built in HTML/GSAP.
- **Map geometry:** [Natural Earth](https://www.naturalearthdata.com/) 1:50m admin-0 countries (public domain).
- **Sound design:** sub-booms, whooshes, stamp, snap and ambient drone, synthesised with ffmpeg (`prepare_media.sh`). No third-party audio.
- **Voiceover:** ElevenLabs Eleven v4, voice "Akash – Confident and Natural" (approved hook take).

## ⚠ Licence notes
- **CC BY-SA (car-lot photos):** share-alike applies to adaptations of the photo. Showing it unmodified-in-frame with credit is normally treated as a collection use. If you want zero share-alike exposure, swap these two shots for CC BY / CC0 footage before publishing.
- The car lot and the port are **not in India**. They're labelled "Representative" on screen, and the description says so too.
- The stat card says "60%+ of the world's contract-made chips" (foundry share), which is narrower than the voiced "microchips". The on-screen footnote cites TrendForce and BCG/SIA 2021.

## YouTube description block
```
Footage & images (Wikimedia Commons):
• "How ST designs and manufactures semiconductor devices" – STMicroelectronics, CC BY 3.0
• "JSR and IBM Quantum envision a revolution in semiconductor manufacturing" – IBM Research, CC BY 3.0
• "Aerial views of a container terminal at the Port of Cork" – FILMING CORK, CC BY 3.0 (representative)
• New-car terminal aerials – Martina Nolte, CC BY-SA 3.0 DE (representative)
• Intel 8749H microcontroller die – yellowcloud, CC BY 2.0
• Taiwan, NASA Terra/MODIS – public domain
• Electricity pylons, Chennai – Aravindan Ganesan, CC BY 2.0
Maps: Natural Earth (public domain). Market-share figures: TrendForce; BCG & SIA (2021).
```

## Rebuild
```bash
npm ci                                       # HyperFrames + vendored GSAP/Inter
cd video/chipgamble/hook && ./prepare_media.sh
npx hyperframes check
npx hyperframes render --workers 4 --quality high --output renders/chipgamble-hook-1080p.mp4
ffmpeg -i renders/chipgamble-hook-1080p.mp4 -c:v libx264 -preset slow -crf 20 -movflags +faststart \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k ../../../episodes/india-semiconductor-gamble/renders/chipgamble-hook-1080p.mp4
```
