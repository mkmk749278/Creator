# Step 2: scene and timeline map (EDL)

Generated from `edl.csv` by `tools/edl_md.py`; edit the CSV, not this file. **Prog** = final video time; **VO** = time in `voiceover.mp3`. Every shot gets grain + vignette (Layer 2); `+hud` adds the medical HUD.


## Block 1: the 3-day rule and the DRDO challenge

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S001 | 00:00.00 | 0.00 | 3.29 | `dried_leaf.mp4` (``) | pan L→R | DAY 1 → 3 → 4 (timer) | sfx_clock.wav@0.0 · Hook: kinetic day counter top-right |
| S002 | 00:03.29 | 3.29 | 3.29 | `cracked_earth.jpg` (``) | zoom 1.15→1.00 |  |  |
| S003 | 00:06.58 | 6.58 | 2.80 | `kidney_anatomy.jpg` (``) | pan R→L | 3-DAY RULE (lower) | Amber toxic grade |
| S004 | 00:09.38 | 9.38 | 2.80 | `blood_sample.mp4` (``) | zoom 1.00→1.15 |  |  |
| S005 | 00:12.18 | 12.19 | 2.80 | `iv_room.mp4` (``) | pan L→R |  | sfx_bass_hit.wav@2.59 |
| S006 | 00:14.98 | 14.99 | 3.00 | `ecg_photo.jpg` (``) | zoom 1.15→1.00 |  | sfx_flatline.wav@2.9 · Flatline lands on 'కానీ' |
| S007 | 00:17.98 | 17.99 | 2.97 | `abstinence_1669.jpg` (``) | pan R→L | 70 YEARS (lower) | sfx_whoosh.wav@0.0 · History of 'no food' claims |
| S008 | 00:20.95 | 20.95 | 2.97 | `tanner_fast_start.jpg` (``) | zoom 1.00→1.15 | DR. HENRY TANNER'S 40-DAY FAST · 1880 (tag) |  |
| S009 | 00:23.92 | 23.92 | 3.35 | `tanner_fast_end.jpg` (``) | pan L→R | TANNER, DAY 40 · 1880 · WELLCOME (tag) | sfx_whoosh.wav@0.0 |
| S010 | 00:27.27 | 27.27 | 3.35 | `headline_edamaruku.jpg` (``) | zoom 1.15→1.00 | SANALEDAMARUKU.COM · 2020 (tag) |  |
| S011 | 00:30.62 | 30.62 | 3.35 | `tv_flicker.mp4` (``) | pan R→L | IMPOSSIBLE CLAIM (lower) |  |
| S012 | 00:33.97 | 33.97 | 1.97 | `earth_sunrise.mp4` (``) | zoom 1.00→1.15 | BE PRACTICAL WITH KISHORE (lower) | sfx_whoosh.wav@0.0 · Channel sting |
| S013 | 00:35.94 | 35.94 | 1.97 | `earth_sunrise.mp4` (``) | pan L→R |  |  |
| S014 | 00:37.91 | 37.91 | 3.43 | `earth_india.mp4` (``) | zoom 1.15→1.00 | NASA (tag) |  |
| S015 | 00:41.34 | 41.34 | 3.43 | `lab_hood.mp4` (``) | pan R→L |  |  |
| S016 | 00:44.77 | 44.78 | 3.43 | `earth_orbit2.mp4` (``) | zoom 1.00→1.15 | DRDO (lower) | sfx_bass_hit.wav@1.73 |
| S017 | 00:48.20 | 48.21 | 3.43 | `lab_scientist.mp4` (``) | pan L→R |  |  |
| S018 | 00:51.63 | 51.65 | 3.43 | `doctor_scrub.mp4` (``) | zoom 1.15→1.00 | 40 DOCTORS (lower) |  |
| S019 | 00:55.06 | 55.08 | 3.19 | `sterling_hospital_ext.jpg` (``) | pan R→L | AHMEDABAD · 2010 (lower) |  |
| S020 | 00:58.25 | 58.27 | 3.19 | `aj_room.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) |  |

> **⏸ VO PAUSE 01:01.44 (2.5 s)**: VO stops at 61.45 s. Picture: `isolation_door.mp4` (zoom 1.00→1.15). Audio: sfx_door_latch.wav@0.3;sfx_heartbeat_monitor.wav@0. VO pause: door + monitor

| S022 | 01:03.94 | 61.45 | 3.37 | `aj_cctv.mp4` (``) | zoom 1.15→1.00 | CCTV 24/7 (lower) | CCTV look |
| S023 | 01:07.31 | 64.82 | 3.37 | `hospital_corridor.mp4` (``) | pan R→L |  |  |
| S024 | 01:10.68 | 68.19 | 3.37 | `itn_cctv.mp4` (``) | zoom 1.00→1.15 | 15 DAYS (timer) |  |
| S025 | 01:14.05 | 71.56 | 3.37 | `aj_room_wide.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S026 | 01:17.42 | 74.93 | 3.27 | `itn_hospital_bed.mp4` (``) | zoom 1.15→1.00 | ITN · 2010 (tag) |  |
| S027 | 01:20.69 | 78.20 | 3.27 | `ecg_photo.jpg` (``) | pan R→L |  |  |
| S028 | 01:23.96 | 81.48 | 3.27 | `aj_press_wide.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) | sfx_bass_hit.wav@2.15 |
| S029 | 01:27.23 | 84.75 | 3.27 | `aj_cctv2.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S030 | 01:30.50 | 88.03 | 3.27 | `lab_microscope.mp4` (``) | zoom 1.15→1.00 |  |  |
| S031 | 01:33.77 | 91.30 | 2.95 | `lab_cellplate.mp4` (``) | pan R→L |  | Name reveal |
| S032 | 01:36.72 | 94.25 | 2.95 | `itn_jani_close.mp4` (``) | zoom 1.00→1.15 | PRAHLAD JANI (lower) | sfx_bass_hit.wav@1.05 |

## Block 2: inside the sealed room

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S033 | 01:39.67 | 97.21 | 2.98 | `itn_devotees.mp4` (``) | pan L→R | CHUNRIWALA MATAJI (lower) |  |
| S034 | 01:42.65 | 100.19 | 2.98 | `ambaji_gabbar.jpg` (``) | zoom 1.15→1.00 | GABBAR HILL, AMBAJI (tag) |  |
| S035 | 01:45.63 | 103.17 | 2.98 | `yogi_gouache.jpg` (``) | pan R→L | GOUACHE · WELLCOME COLLECTION (tag) |  |
| S036 | 01:48.61 | 106.14 | 2.98 | `headline_wikipedia.jpg` (``) | zoom 1.00→1.15 | 70+ YEARS (lower) |  |
| S037 | 01:51.59 | 109.12 | 2.98 | `jani_portrait_red.jpg` (``) | pan L→R | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |

> **🎬 LIVE CLIP 01:54.57 (15.3 s)**: VO stops at 112.1 s; `itn_full.mp4` plays 12.4–27.7 s **with its own audio**, then the VO continues. Caption: ప్రహ్లాద్ జానీని కలవండి. ఆయన్ని మాతాజీ అని కూడా పిలుస్తారు, అంటే మాతృ దేవత. | ఆయన వయసు 82. | గత 70 ఏళ్లుగా తాను ఏమీ తినలేదు, తాగలేదు అని ఆయన చెప్తారు. | అది నిజమైతే, ఆయన జీవశాస్త్రాన్నే ధిక్కరిస్తున్నారు.. Real 2010 report: introduces Jani (then VO: worldwide viral...)

| S039 | 02:09.87 | 112.10 | 3.35 | `lab_hood.mp4` (``) | pan R→L | DIPAS · DRDO (lower) |  |
| S040 | 02:13.22 | 115.44 | 3.35 | `aj_ilavazhagan.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S041 | 02:16.57 | 118.79 | 3.35 | `sterling_hospital_ext.jpg` (``) | pan L→R |  |  |
| S042 | 02:19.92 | 122.14 | 3.35 | `aj_shah.mp4` (``) | zoom 1.15→1.00 | DR. SUDHIR SHAH (lower) |  |
| S043 | 02:23.27 | 125.48 | 2.67 | `lab_pipette.mp4` (``) | pan R→L |  |  |
| S044 | 02:25.94 | 128.15 | 2.67 | `blood_sample.mp4` (``) | zoom 1.00→1.15 |  |  |
| S045 | 02:28.61 | 130.82 | 3.42 | `siachen_soldiers.jpg` (``) | pan L→R |  | sfx_whoosh.wav@0.0 · Soldiers / extremes / space |
| S046 | 02:32.03 | 134.24 | 3.42 | `desert_soldiers.mp4` (``) | zoom 1.15→1.00 |  |  |
| S047 | 02:35.45 | 137.66 | 3.42 | `indian_army.jpg` (``) | pan R→L |  |  |
| S048 | 02:38.87 | 141.08 | 3.42 | `astronaut_iss.mp4` (``) | zoom 1.00→1.15 | NASA (tag) |  |

> **🎬 LIVE CLIP 02:42.29 (14.0 s)**: VO stops at 144.5 s; `aj_full.mp4` plays 88.7–102.7 s **with its own audio**, then the VO continues. Caption: మనుషులు ఆహారం, నీరు లేకుండా ఎలా బ్రతుకుతున్నారో అర్థం చేసుకుంటే, | ఎక్కువ కాలం ఆహారం, నీరు లేకుండా జీవించేలా వ్యూహాలు రూపొందించడానికి అది మాకు సహాయపడొచ్చు.. Real 2010 quote: why DIPAS/DRDO studied him

| S050 | 02:56.29 | 144.50 | 1.96 | `astronaut_iss2.mp4` (``) | zoom 1.15→1.00 | 22 APRIL 2010 (lower) | sfx_bass_hit.wav@0.0 |
| S051 | 02:58.25 | 146.46 | 1.96 | `hospital_entrance.mp4` (``) | pan R→L |  |  |
| S052 | 03:00.21 | 148.42 | 3.50 | `water_tap_close.mp4` (``) | zoom 1.00→1.15 | ZERO WATER (lower) | Rule 1 |
| S053 | 03:03.71 | 151.92 | 3.50 | `water_drop_macro.mp4` (``) | pan L→R |  |  |
| S054 | 03:07.21 | 155.42 | 3.15 | `iv_room.mp4` (``) | zoom 1.15→1.00 | 2 CAMERAS · 24/7 (lower) | Rule 2 (CCTV look) |
| S055 | 03:10.36 | 158.57 | 3.15 | `hospital_corridor.mp4` (``) | pan R→L |  |  |
| S056 | 03:13.51 | 161.72 | 2.71 | `aj_room_wide.mp4` (``) | zoom 1.00→1.15 | OBSERVER IN ROOM (lower) | Rule 3 |
| S057 | 03:16.22 | 164.43 | 2.71 | `itn_cctv.mp4` (``) | pan L→R | ITN · 2010 (tag) |  |
| S058 | 03:18.93 | 167.13 | 2.71 | `doctor_scrub.mp4` (``) | zoom 1.15→1.00 |  |  |
| S059 | 03:21.64 | 169.84 | 3.11 | `water_drop_macro.mp4` (``) | pan R→L |  | Rule 4 |
| S060 | 03:24.75 | 172.95 | 3.11 | `lab_pipette.mp4` (``) | zoom 1.00→1.15 |  |  |
| S061 | 03:27.86 | 176.07 | 3.11 | `lab_tubes.mp4` (``) | pan L→R | MEASURED TO THE ML (lower) |  |
| S062 | 03:30.97 | 179.18 | 3.11 | `water_tap_close.mp4` (``) | zoom 1.15→1.00 |  |  |
| S063 | 03:34.08 | 182.30 | 3.11 | `lab_pipette.mp4` (``) | pan R→L |  |  |
| S064 | 03:37.19 | 185.41 | 2.55 | `water_drop_macro.mp4` (``) | zoom 1.00→1.15 |  | sfx_bass_hit.wav@0.5 |
| S065 | 03:39.74 | 187.95 | 2.55 | `water_drop_macro.mp4` (``) | pan L→R |  |  |
| S066 | 03:42.29 | 190.50 | 3.12 | `dried_leaf.mp4` (``) | zoom 1.15→1.00 | DAY 3 (timer) | sfx_clock.wav@0.0 |
| S067 | 03:45.41 | 193.62 | 3.12 | `kidney_anatomy.jpg` (``) | pan R→L | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S068 | 03:48.53 | 196.75 | 3.12 | `ecg_photo.jpg` (``) | zoom 1.00→1.15 |  |  |
| S069 | 03:51.65 | 199.87 | 3.21 | `cracked_earth.jpg` (``) | pan L→R |  |  |
| S070 | 03:54.86 | 203.08 | 3.21 | `aj_jani_close.mp4` (``) | zoom 1.15→1.00 | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S071 | 03:58.07 | 206.29 | 3.21 | `pulse_oximeter.mp4` (``) | pan R→L | VITALS REPORTED NORMAL (lower) |  |
| S072 | 04:01.28 | 209.50 | 3.21 | `blood_sample.mp4` (``) | zoom 1.00→1.15 |  |  |
| S073 | 04:04.49 | 212.71 | 2.75 | `aj_cctv2.mp4` (``) | pan L→R | DAY 7 → 10 (timer) |  |
| S074 | 04:07.24 | 215.46 | 2.75 | `ultrasound_screen.jpg` (``) | zoom 1.15→1.00 | NASA (tag) |  |
| S075 | 04:09.99 | 218.20 | 2.75 | `itn_jani_close2.mp4` (``) | pan R→L | ITN · 2010 (tag) | sfx_bass_hit.wav@2.41 |
| S076 | 04:12.74 | 220.95 | 2.75 | `aj_cctv2.mp4` (``) | zoom 1.00→1.15 | AL JAZEERA ENGLISH · 2010 (tag) |  |

> **⏸ VO PAUSE 04:15.49 (3.0 s)**: VO stops at 223.7 s. Picture: `ecg_photo.jpg` (zoom 1.00→1.15). Audio: sfx_heartbeat_monitor.wav@0. VO pause after 'biggest shock'


## Block 3: the ultrasound shock

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S078 | 04:18.49 | 223.70 | 2.75 | `bladder_anatomy.jpg` (``) | zoom 1.15→1.00 | THE BLADDER MYSTERY (lower) | sfx_bass_hit.wav@0.0 |
| S079 | 04:21.24 | 226.45 | 2.91 | `bladder_anatomy.jpg` (``) | pan R→L | 15 DAYS · NO URINE (lower) |  |
| S080 | 04:24.15 | 229.36 | 2.91 | `kidney_anatomy.jpg` (``) | zoom 1.00→1.15 | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S081 | 04:27.06 | 232.27 | 2.91 | `icu_room.jpg` (``) | pan L→R |  |  |
| S082 | 04:29.97 | 235.18 | 2.91 | `ecg_photo.jpg` (``) | zoom 1.15→1.00 |  |  |
| S083 | 04:32.88 | 238.09 | 2.91 | `bladder_anatomy.jpg` (``) | pan R→L | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S084 | 04:35.79 | 241.00 | 3.53 | `ultrasound_screen.jpg` (``) | zoom 1.00→1.15 | SONOGRAPHY (lower) |  |
| S085 | 04:39.32 | 244.53 | 3.53 | `ultrasound_scan2.jpg` (``) | pan L→R | NASA (tag) |  |
| S086 | 04:42.85 | 248.07 | 3.35 | `sonogram_scan.jpg` (``) | zoom 1.15→1.00 | ILLUSTRATIVE SCAN (tag) |  |
| S087 | 04:46.20 | 251.42 | 3.35 | `bladder_anatomy.jpg` (``) | pan R→L | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S088 | 04:49.55 | 254.78 | 3.35 | `ultrasound_screen.jpg` (``) | zoom 1.00→1.15 | NASA (tag) | sfx_bass_hit.wav@2.29 |
| S089 | 04:52.90 | 258.13 | 3.35 | `lab_microscope.mp4` (``) | pan L→R |  |  |
| S090 | 04:56.25 | 261.49 | 3.35 | `lab_cellplate.mp4` (``) | zoom 1.15→1.00 | DOCTORS' HYPOTHESIS (lower) |  |
| S091 | 04:59.60 | 264.84 | 3.35 | `blood_sample.mp4` (``) | pan R→L |  |  |
| S092 | 05:02.95 | 268.20 | 2.43 | `headline_wikipedia.jpg` (``) | zoom 1.00→1.15 | WIKIPEDIA (tag) |  |
| S093 | 05:05.38 | 270.63 | 2.43 | `jani_portrait_red.jpg` (``) | pan L→R | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S094 | 05:07.81 | 273.07 | 2.43 | `headline_wikipedia.jpg` (``) | zoom 1.15→1.00 | WIKIPEDIA (tag) |  |
| S095 | 05:10.24 | 275.50 | 3.05 | `itn_hospital_bed.mp4` (``) | pan R→L | DAY 15 (timer) |  |
| S096 | 05:13.29 | 278.55 | 3.05 | `scale_weight.jpg` (``) | zoom 1.00→1.15 |  |  |
| S097 | 05:16.34 | 281.60 | 3.05 | `ecg_photo.jpg` (``) | pan L→R |  |  |
| S098 | 05:19.39 | 284.64 | 3.05 | `ultrasound_scan2.jpg` (``) | zoom 1.15→1.00 | NASA (tag) |  |
| S099 | 05:22.44 | 287.69 | 3.05 | `blood_sample.mp4` (``) | pan R→L |  |  |

## Block 4: the press meet and the science

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S100 | 05:25.49 | 290.74 | 2.44 | `aj_press_wide.mp4` (``) | zoom 1.00→1.15 | PRESS MEET · MAY 2010 (lower) |  |
| S101 | 05:27.93 | 293.18 | 2.44 | `aj_shah.mp4` (``) | pan L→R | AL JAZEERA ENGLISH · 2010 (tag) |  |
| S102 | 05:30.37 | 295.61 | 2.44 | `aj_press_wide.mp4` (``) | zoom 1.15→1.00 | AL JAZEERA ENGLISH · 2010 (tag) |  |

> **🎬 LIVE CLIP 05:32.81 (27.0 s)**: VO stops at 298.05 s; `aj_full.mp4` plays 27.7–54.7 s **with its own audio**, then the VO continues. Caption: మనమంతా సైన్స్‌లో, బయాలజీలో ఒక అద్భుతాన్ని చూస్తున్నాం. | మాతాజీ ఈ హాస్పిటల్‌లో చేరి ఇప్పటికే 108 గంటలైంది. | ఆయన ఏమీ తినలేదు, ఒక్క చుక్క ద్రవం కూడా తాగలేదు. | అంతకంటే ముఖ్యంగా, ఒక్క చుక్క మూత్రం గానీ, మలం గానీ విసర్జించలేదు.. The REAL press-conference audio

| S104 | 05:59.81 | 298.05 | 3.35 | `incense.mp4` (``) | zoom 1.00→1.15 | HYPOMETABOLISM (lower) | sfx_bass_hit.wav@0.15 |
| S105 | 06:03.16 | 301.40 | 3.35 | `earth_window.mp4` (``) | pan L→R |  |  |
| S106 | 06:06.51 | 304.75 | 3.35 | `ecg_photo.jpg` (``) | zoom 1.15→1.00 |  |  |
| S107 | 06:09.86 | 308.10 | 2.96 | `lab_microscope.mp4` (``) | pan R→L |  |  |
| S108 | 06:12.82 | 311.06 | 2.96 | `lab_cellplate.mp4` (``) | zoom 1.00→1.15 | AUTOPHAGY (lower) |  |
| S109 | 06:15.78 | 314.02 | 2.96 | `lab_hood.mp4` (``) | pan L→R |  |  |
| S110 | 06:18.74 | 316.97 | 2.96 | `lab_microscope.mp4` (``) | zoom 1.15→1.00 |  |  |
| S111 | 06:21.70 | 319.93 | 2.96 | `lab_tubes.mp4` (``) | pan R→L |  |  |
| S112 | 06:24.66 | 322.89 | 3.18 | `yogi_gouache.jpg` (``) | zoom 1.00→1.15 | GOUACHE · WELLCOME COLLECTION (tag) |  |
| S113 | 06:27.84 | 326.07 | 3.18 | `incense.mp4` (``) | pan L→R |  |  |
| S114 | 06:31.02 | 329.25 | 3.18 | `ambaji_gabbar.jpg` (``) | zoom 1.15→1.00 | GABBAR HILL, AMBAJI (tag) |  |
| S115 | 06:34.20 | 332.42 | 3.18 | `himalaya_leh.jpg` (``) | pan R→L |  |  |

> **🎬 LIVE CLIP 06:37.38 (16.3 s)**: VO stops at 335.6 s; `skeptic_view.mp4` plays 7.0–23.3 s **with its own audio**, then the VO continues. Caption: కొన్ని నిజాలు ఎలాంటి సందేహం లేకుండా నిరూపితమయ్యాయి. | మనతో సహా ప్రతి జీవికి బ్రతకడానికి క్రమం తప్పకుండా ఆహారం, నీరు అవసరం. | దీనికి మినహాయింపులు లేవు. ఒక్కటి కూడా లేదు.. Real CC BY clip: the skeptics' view. Telugu translation in subtitle

| S117 | 06:53.68 | 335.60 | 2.77 | `earth_window.mp4` (``) | pan L→R |  |  |
| S118 | 06:56.45 | 338.37 | 2.77 | `earth_india.mp4` (``) | zoom 1.15→1.00 | NASA (tag) |  |
| S119 | 06:59.22 | 341.14 | 2.77 | `jani_portrait_red.jpg` (``) | pan R→L | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S120 | 07:01.99 | 343.91 | 2.77 | `himalaya_leh.jpg` (``) | zoom 1.00→1.15 |  |  |

## Outro: your opinion + subscribe

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S121 | 07:04.76 | 346.68 | 3.13 | `jani_portrait_red.jpg` (``) | pan L→R | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) | End-screen area: calm B-roll |
| S122 | 07:07.89 | 349.81 | 3.13 | `incense.mp4` (``) | zoom 1.15→1.00 |  |  |
| S123 | 07:11.02 | 352.93 | 3.13 | `earth_orbit2.mp4` (``) | pan R→L |  |  |
| S124 | 07:14.15 | 356.06 | 3.13 | `jani_ashram_ambaji.jpg` (``) | zoom 1.00→1.15 | AMBAJI, GUJARAT (tag) |  |
| S125 | 07:17.28 | 359.18 | 3.13 | `earth_desert_orbit.mp4` (``) | pan L→R |  |  |
| S126 | 07:20.41 | 362.31 | 3.13 | `earth_sunrise.mp4` (``) | zoom 1.15→1.00 |  |  |
| S127 | 07:23.54 | 365.43 | 3.13 | `earth_india.mp4` (``) | pan R→L | NASA (tag) |  |

**Programme length with every clip: 07:26.67** (121 shots, 4 live clips, 2 VO pauses).


## Audio cue sheet
| Element | Level | Notes |
|---|---|---|
| Voiceover (`voiceover.mp3`) | lead, normalised with the mix to −14 LUFS / −1 dBTP | Removes the duplicate line at VO 221.40–223.40 |
| BGM (`bgm_dark.mp3`) | −20 dB, side-chain ducked (ratio 6, release 400 ms) | Swells up in each pause |
| SFX | −8 dB, 3 s max with 0.3 s fade | Placed from the `sfx` column (`file@seconds-into-shot`) |
| Pause audio | 0 dB | Real recordings only. Pause 3 must be the real Dr. Shah clip; if none exists, use monitor beeps |
