# Step 2: scene and timeline map (EDL)

Generated from `edl.csv` by `tools/edl_md.py`; edit the CSV, not this file. **Prog** = final video time; **VO** = time in `voiceover.mp3`. Every shot gets grain + vignette (Layer 2); `+hud` adds the medical HUD.


## Block 1: the 3-day rule and the DRDO challenge

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S001 | 00:00.00 | 0.00 | 3.29 | `dried_leaf.mp4` (``) | pan L→R | DAY 1 → 3 → 4 (timer) | sfx_clock.wav@0.0 · Hook |
| S002 | 00:03.29 | 3.29 | 3.29 | `cracked_earth.jpg` (``) | zoom 1.15→1.00 |  |  |
| S003 | 00:06.58 | 6.58 | 8.41 | `hf_kidney3d.mp4` (``) | as shot |  | sfx_bass_hit.wav@8.2 · 3D: kidneys fail without water |
| S004 | 00:14.99 | 14.99 | 3.00 | `iv_room.mp4` (``) | zoom 1.00→1.15 |  | sfx_flatline.wav@2.9 · Flatline lands on 'కానీ' |
| S005 | 00:17.99 | 17.99 | 2.97 | `itn_jani_close.mp4` (``) | pan L→R | PRAHLAD JANI · 1929–2020 (lower) | sfx_whoosh.wav@0.0 · Face + name by 0:18 |
| S006 | 00:20.96 | 20.95 | 2.97 | `jani_portrait_red.jpg` (``) | zoom 1.15→1.00 | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S007 | 00:23.93 | 23.92 | 3.35 | `headline_wikipedia.jpg` (``) | pan R→L | WIKIPEDIA (tag) | sfx_whoosh.wav@0.0 |
| S008 | 00:27.28 | 27.27 | 3.35 | `abstinence_1669.jpg` (``) | zoom 1.00→1.15 | LONDON 1669 · WELLCOME COLLECTION (tag) |  |
| S009 | 00:30.63 | 30.62 | 3.35 | `headline_edamaruku.jpg` (``) | pan L→R | IMPOSSIBLE CLAIM (lower) |  |
| S010 | 00:33.98 | 33.97 | 3.94 | `hf_logo_sting.mp4` (``) | as shot |  | Channel logo sting |
| S011 | 00:37.92 | 37.91 | 3.43 | `india_drive.mp4` (``) | pan R→L |  |  |
| S012 | 00:41.35 | 41.34 | 3.43 | `aj_press_wide.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S013 | 00:44.78 | 44.78 | 3.43 | `aj_ilavazhagan.mp4` (``) | pan L→R | DRDO (lower) | sfx_bass_hit.wav@1.73 |
| S014 | 00:48.21 | 48.21 | 3.43 | `doctor_scrub.mp4` (``) | zoom 1.15→1.00 |  |  |
| S015 | 00:51.64 | 51.65 | 3.43 | `lab_hood.mp4` (``) | pan R→L | 40 DOCTORS (lower) |  |
| S016 | 00:55.07 | 55.08 | 3.19 | `sterling_hospital_ext.jpg` (``) | zoom 1.00→1.15 | AHMEDABAD · 2010 (lower) |  |
| S017 | 00:58.26 | 58.27 | 3.19 | `aj_room.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) |  |

> **⏸ VO PAUSE 01:01.45 (2.5 s)**: VO stops at 61.45 s. Picture: `aj_room_wide.mp4` (zoom 1.00→1.15). Audio: sfx_door_latch.wav@0.3;sfx_heartbeat_monitor.wav@0. VO pause: door + monitor

| S019 | 01:03.95 | 61.45 | 3.37 | `aj_cctv.mp4` (``) | pan R→L | CCTV 24/7 (lower) | Real 2010 CCTV only |
| S020 | 01:07.32 | 64.82 | 3.37 | `itn_cctv.mp4` (``) | zoom 1.00→1.15 | ITN · 2010 (tag) |  |
| S021 | 01:10.69 | 68.19 | 3.37 | `aj_cctv2.mp4` (``) | pan L→R | 15 DAYS (timer) |  |
| S022 | 01:14.06 | 71.56 | 3.37 | `aj_room_wide.mp4` (``) | zoom 1.15→1.00 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S023 | 01:17.43 | 74.93 | 3.27 | `itn_hospital_bed.mp4` (``) | pan R→L | ITN · 2010 (tag) |  |
| S024 | 01:20.70 | 78.20 | 3.27 | `aj_press_wide.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S025 | 01:23.97 | 81.48 | 3.27 | `aj_jani_close.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) | sfx_bass_hit.wav@2.15 |
| S026 | 01:27.24 | 84.75 | 3.27 | `aj_cctv2.mp4` (``) | zoom 1.15→1.00 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S027 | 01:30.51 | 88.03 | 3.27 | `lab_cellplate.mp4` (``) | pan R→L |  |  |
| S028 | 01:33.78 | 91.30 | 2.95 | `itn_jani_close2.mp4` (``) | zoom 1.00→1.15 | ITN · 2010 (tag) | Name said in VO |
| S029 | 01:36.73 | 94.25 | 2.95 | `aj_jani_close.mp4` (``) | pan L→R | PRAHLAD JANI (lower) | sfx_bass_hit.wav@0.95 |

## Block 2: inside the sealed room

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S030 | 01:39.68 | 97.21 | 2.98 | `itn_devotees.mp4` (``) | zoom 1.15→1.00 | CHUNRIWALA MATAJI (lower) |  |
| S031 | 01:42.66 | 100.19 | 2.98 | `ambaji_gabbar.jpg` (``) | pan R→L | GABBAR HILL, AMBAJI (tag) |  |
| S032 | 01:45.64 | 103.17 | 2.98 | `yogi_gouache.jpg` (``) | zoom 1.00→1.15 | GOUACHE · WELLCOME COLLECTION (tag) |  |
| S033 | 01:48.62 | 106.14 | 2.98 | `jani_portrait_red.jpg` (``) | pan L→R | 70+ YEARS (lower) |  |
| S034 | 01:51.60 | 109.12 | 2.98 | `jani_ashram_ambaji.jpg` (``) | zoom 1.15→1.00 | AMBAJI, GUJARAT (tag) |  |

> **🎬 LIVE CLIP 01:54.58 (15.3 s)**: VO stops at 112.1 s; `itn_full.mp4` plays 12.4–27.7 s **with its own audio**, then the VO continues. Caption: ప్రహ్లాద్ జానీని కలవండి. ఆయన్ని మాతాజీ అని కూడా పిలుస్తారు, అంటే మాతృ దేవత. | ఆయన వయసు 82. | గత 70 ఏళ్లుగా తాను ఏమీ తినలేదు, తాగలేదు అని ఆయన చెప్తారు. | అది నిజమైతే, ఆయన జీవశాస్త్రాన్నే ధిక్కరిస్తున్నారు.. Original clip with its own audio

| S036 | 02:09.88 | 112.10 | 3.35 | `aj_ilavazhagan.mp4` (``) | zoom 1.00→1.15 | DIPAS · DRDO (lower) |  |
| S037 | 02:13.23 | 115.44 | 3.35 | `lab_scientist.mp4` (``) | pan L→R |  |  |
| S038 | 02:16.58 | 118.79 | 3.35 | `sterling_hospital_ext.jpg` (``) | zoom 1.15→1.00 |  |  |
| S039 | 02:19.93 | 122.13 | 3.35 | `aj_shah.mp4` (``) | pan R→L | DR. SUDHIR SHAH (lower) |  |
| S040 | 02:23.28 | 125.48 | 2.67 | `lab_pipette.mp4` (``) | zoom 1.00→1.15 |  |  |
| S041 | 02:25.95 | 128.15 | 2.67 | `lab_tubes.mp4` (``) | pan L→R |  |  |
| S042 | 02:28.62 | 130.82 | 3.42 | `siachen_soldiers.jpg` (``) | zoom 1.15→1.00 |  | sfx_whoosh.wav@0.0 · Soldiers / extremes / space |
| S043 | 02:32.04 | 134.24 | 3.42 | `desert_soldiers.mp4` (``) | pan R→L |  |  |
| S044 | 02:35.46 | 137.66 | 3.42 | `indian_army.jpg` (``) | zoom 1.00→1.15 |  |  |
| S045 | 02:38.88 | 141.08 | 3.42 | `astronaut_iss.mp4` (``) | pan L→R | NASA (tag) |  |

> **🎬 LIVE CLIP 02:42.30 (14.0 s)**: VO stops at 144.5 s; `aj_full.mp4` plays 88.7–102.7 s **with its own audio**, then the VO continues. Caption: మనుషులు ఆహారం, నీరు లేకుండా ఎలా బ్రతుకుతున్నారో అర్థం చేసుకుంటే, | ఎక్కువ కాలం ఆహారం, నీరు లేకుండా జీవించేలా వ్యూహాలు రూపొందించడానికి అది మాకు సహాయపడొచ్చు.. Original clip with its own audio

| S047 | 02:56.30 | 144.50 | 3.92 | `hf_timeline_a.mp4` (``) | as shot |  | sfx_bass_hit.wav@0.0 · Study timeline |
| S048 | 03:00.22 | 148.42 | 3.50 | `water_tap_close.mp4` (``) | zoom 1.00→1.15 | ZERO WATER (lower) | Rule 1 |
| S049 | 03:03.72 | 151.92 | 3.50 | `water_drop_macro.mp4` (``) | pan L→R |  |  |
| S050 | 03:07.22 | 155.42 | 3.15 | `aj_cctv.mp4` (``) | zoom 1.15→1.00 | 2 CAMERAS · 24/7 (lower) | Rule 2: real CCTV |
| S051 | 03:10.37 | 158.57 | 3.15 | `itn_cctv.mp4` (``) | pan R→L | ITN · 2010 (tag) |  |
| S052 | 03:13.52 | 161.72 | 4.06 | `aj_room_wide.mp4` (``) | zoom 1.00→1.15 | OBSERVER IN ROOM (lower) | Rule 3 |
| S053 | 03:17.58 | 165.78 | 4.06 | `doctor_scrub.mp4` (``) | pan L→R |  |  |
| S054 | 03:21.64 | 169.84 | 3.11 | `lab_tubes.mp4` (``) | zoom 1.15→1.00 |  | Rule 4 |
| S055 | 03:24.75 | 172.95 | 3.11 | `lab_pipette.mp4` (``) | pan R→L |  |  |
| S056 | 03:27.86 | 176.07 | 3.11 | `water_drop_macro.mp4` (``) | zoom 1.00→1.15 | MEASURED TO THE ML (lower) |  |
| S057 | 03:30.97 | 179.18 | 3.11 | `water_tap_close.mp4` (``) | pan L→R |  |  |
| S058 | 03:34.08 | 182.30 | 3.11 | `lab_cellplate.mp4` (``) | zoom 1.15→1.00 |  |  |
| S059 | 03:37.19 | 185.41 | 5.09 | `hf_timeline_b.mp4` (``) | as shot |  | Day tracker: days 1–5 |
| S060 | 03:42.28 | 190.50 | 9.37 | `hf_dehydration_chart.mp4` (``) | as shot |  | sfx_clock.wav@0.0 · Expected collapse vs reported flat line |
| S061 | 03:51.65 | 199.87 | 3.34 | `aj_jani_close.mp4` (``) | pan L→R | NO FATIGUE · NO WEAKNESS (lower) | Vitals: normal ranges, illustrative |
| S062 | 03:54.99 | 203.21 | 9.50 | `hf_vitals.mp4` (``) | as shot |  |  |
| S063 | 04:04.49 | 212.71 | 5.00 | `hf_timeline_b.mp4` (``) | as shot |  |  |
| S064 | 04:09.49 | 217.71 | 2.99 | `itn_jani_close2.mp4` (``) | zoom 1.00→1.15 | ITN · 2010 (tag) | sfx_bass_hit.wav@2.9 |
| S065 | 04:12.48 | 220.70 | 3.00 | `aj_cctv2.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) |  |

> **⏸ VO PAUSE 04:15.48 (3.0 s)**: VO stops at 223.7 s. Picture: `ultrasound_screen.jpg` (zoom 1.00→1.15). Audio: sfx_heartbeat_monitor.wav@0. VO pause after 'biggest shock'


## Block 3: the ultrasound shock

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S067 | 04:18.48 | 223.70 | 2.75 | `bladder_anatomy.jpg` (``) | pan R→L | THE BLADDER MYSTERY (lower) | sfx_bass_hit.wav@0.0 |
| S068 | 04:21.23 | 226.45 | 4.04 | `kidney_anatomy.jpg` (``) | zoom 1.00→1.15 | 15 DAYS · NO URINE (lower) |  |
| S069 | 04:25.27 | 230.49 | 4.04 | `itn_hospital_bed.mp4` (``) | pan L→R | ITN · 2010 (tag) |  |
| S070 | 04:29.31 | 234.53 | 4.04 | `aj_room.mp4` (``) | zoom 1.15→1.00 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S071 | 04:33.35 | 238.56 | 4.04 | `ultrasound_screen.jpg` (``) | pan R→L | NASA (tag) |  |
| S072 | 04:37.39 | 242.60 | 4.04 | `ultrasound_scan2.jpg` (``) | zoom 1.00→1.15 | NASA (tag) |  |
| S073 | 04:41.43 | 246.64 | 12.00 | `hf_bladder3d.mp4` (``) | as shot |  | sfx_bass_hit.wav@9.0 · 3D: the bladder hypothesis |
| S074 | 04:53.43 | 258.64 | 3.19 | `sonogram_scan.jpg` (``) | zoom 1.15→1.00 | ILLUSTRATIVE SCAN (tag) |  |
| S075 | 04:56.62 | 261.83 | 3.19 | `lab_microscope.mp4` (``) | pan R→L |  |  |
| S076 | 04:59.81 | 265.01 | 3.19 | `blood_sample.mp4` (``) | zoom 1.00→1.15 |  |  |
| S077 | 05:03.00 | 268.20 | 3.65 | `headline_wikipedia.jpg` (``) | pan L→R | WIKIPEDIA (tag) |  |
| S078 | 05:06.65 | 271.85 | 3.65 | `aj_press_wide.mp4` (``) | zoom 1.15→1.00 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S079 | 05:10.30 | 275.50 | 3.50 | `hf_timeline_b.mp4` (``) | as shot |  | Day 15 |
| S080 | 05:13.80 | 279.00 | 3.87 | `scale_weight.jpg` (``) | zoom 1.00→1.15 |  |  |
| S081 | 05:17.67 | 282.87 | 4.00 | `hf_vitals.mp4` (``) | as shot |  |  |
| S082 | 05:21.67 | 286.87 | 3.87 | `itn_hospital_bed.mp4` (``) | zoom 1.15→1.00 | ITN · 2010 (tag) |  |

## Block 4: the press meet and the science

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S083 | 05:25.54 | 290.74 | 3.66 | `aj_press_wide.mp4` (``) | pan R→L | PRESS MEET · MAY 2010 (lower) |  |
| S084 | 05:29.20 | 294.39 | 3.66 | `aj_shah.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) |  |

> **🎬 LIVE CLIP 05:32.86 (27.0 s)**: VO stops at 298.05 s; `aj_full.mp4` plays 27.7–54.7 s **with its own audio**, then the VO continues. Caption: మనమంతా సైన్స్‌లో, బయాలజీలో ఒక అద్భుతాన్ని చూస్తున్నాం. | మాతాజీ ఈ హాస్పిటల్‌లో చేరి ఇప్పటికే 108 గంటలైంది. | ఆయన ఏమీ తినలేదు, ఒక్క చుక్క ద్రవం కూడా తాగలేదు. | అంతకంటే ముఖ్యంగా, ఒక్క చుక్క మూత్రం గానీ, మలం గానీ విసర్జించలేదు.. Original clip with its own audio

| S086 | 05:59.86 | 298.05 | 8.00 | `hf_metabolism.mp4` (``) | as shot |  | sfx_bass_hit.wav@0.15 · Hypothesis: hypometabolism |
| S087 | 06:07.86 | 306.05 | 2.05 | `incense.mp4` (``) | pan R→L |  |  |
| S088 | 06:09.91 | 308.10 | 12.00 | `hf_autophagy3d.mp4` (``) | as shot |  | 3D: autophagy |
| S089 | 06:21.91 | 320.10 | 2.79 | `lab_microscope.mp4` (``) | pan L→R |  |  |
| S090 | 06:24.70 | 322.89 | 3.18 | `yogi_gouache.jpg` (``) | zoom 1.15→1.00 | GOUACHE · WELLCOME COLLECTION (tag) |  |
| S091 | 06:27.88 | 326.07 | 3.18 | `incense.mp4` (``) | pan R→L |  |  |
| S092 | 06:31.06 | 329.25 | 3.18 | `ambaji_gabbar.jpg` (``) | zoom 1.00→1.15 | GABBAR HILL, AMBAJI (tag) |  |
| S093 | 06:34.24 | 332.42 | 3.18 | `himalaya_leh.jpg` (``) | pan L→R |  |  |

> **🎬 LIVE CLIP 06:37.42 (16.3 s)**: VO stops at 335.6 s; `skeptic_view.mp4` plays 7.0–23.3 s **with its own audio**, then the VO continues. Caption: కొన్ని నిజాలు ఎలాంటి సందేహం లేకుండా నిరూపితమయ్యాయి. | మనతో సహా ప్రతి జీవికి బ్రతకడానికి క్రమం తప్పకుండా ఆహారం, నీరు అవసరం. | దీనికి మినహాయింపులు లేవు. ఒక్కటి కూడా లేదు.. Original clip with its own audio

| S095 | 06:53.72 | 335.60 | 2.77 | `earth_window.mp4` (``) | pan R→L | NASA (tag) |  |
| S096 | 06:56.49 | 338.37 | 2.77 | `itn_jani_close2.mp4` (``) | zoom 1.00→1.15 | ITN · 2010 (tag) |  |
| S097 | 06:59.26 | 341.14 | 2.77 | `itn_jani_close.mp4` (``) | pan L→R | ITN · 2010 (tag) |  |
| S098 | 07:02.03 | 343.91 | 2.77 | `himalaya_leh.jpg` (``) | zoom 1.15→1.00 |  |  |

## Outro: your opinion + subscribe

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S099 | 07:04.80 | 346.68 | 3.07 | `itn_devotees.mp4` (``) | pan R→L | ITN · 2010 (tag) | Your opinion? |
| S100 | 07:07.87 | 349.75 | 3.07 | `jani_ashram_ambaji.jpg` (``) | zoom 1.00→1.15 | AMBAJI, GUJARAT (tag) |  |
| S101 | 07:10.94 | 352.82 | 3.07 | `aj_jani_close.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S102 | 07:14.01 | 355.90 | 3.07 | `earth_sunrise.mp4` (``) | zoom 1.15→1.00 | NASA (tag) |  |
| S103 | 07:17.08 | 358.97 | 9.59 | `hf_end_card.mp4` (``) | as shot |  | End card: logo + subscribe; YouTube end screen sits here |

**Programme length with every clip: 07:26.67** (97 shots, 4 live clips, 2 VO pauses).


## Audio cue sheet
| Element | Level | Notes |
|---|---|---|
| Voiceover (`voiceover.mp3`) | lead, normalised with the mix to −14 LUFS / −1 dBTP | Removes the duplicate line at VO 221.40–223.40 |
| BGM (`bgm_dark.mp3`) | −20 dB, side-chain ducked (ratio 6, release 400 ms) | Swells up in each pause |
| SFX | −8 dB, 3 s max with 0.3 s fade | Placed from the `sfx` column (`file@seconds-into-shot`) |
| Pause audio | 0 dB | Real recordings only. Pause 3 must be the real Dr. Shah clip; if none exists, use monitor beeps |
