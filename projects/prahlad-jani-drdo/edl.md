# Step 2: scene and timeline map (EDL)

Generated from `edl.csv` by `tools/edl_md.py`; edit the CSV, not this file. **Prog** = final video time; **VO** = time in `voiceover.mp3`. Every shot gets grain + vignette (Layer 2); `+hud` adds the medical HUD.


## Block 1: the 3-day rule and the DRDO challenge

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S001 | 00:00.00 | 0.00 | 3.29 | `clock_macro.mp4` (`cracked_earth.mp4`) | pan L→R | DAY 1 → 3 → 4 (timer) | sfx_clock.wav@0.0 · Hook: kinetic day counter top-right |
| S002 | 00:03.29 | 3.29 | 3.29 | `cracked_earth.mp4` (`sweat_macro.mp4`) | zoom 1.15→1.00 |  |  |
| S003 | 00:06.58 | 6.58 | 2.80 | `ai_kidney_healthy.mp4` (`kidney_anatomy.jpg`) | pan R→L +hud | 3-DAY RULE (lower) | Amber toxic grade on shots 2-3 |
| S004 | 00:09.38 | 9.38 | 2.80 | `ai_kidney_dehydrated.mp4` (`blood_vessels.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S005 | 00:12.18 | 12.19 | 2.80 | `blood_vessels.mp4` (`cells_micro.mp4`) | pan L→R |  | sfx_bass_hit.wav@2.59 |
| S006 | 00:14.98 | 14.99 | 3.00 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | zoom 1.15→1.00 +hud |  | sfx_flatline.wav@2.9 · Flatline lands on 'కానీ' |
| S007 | 00:17.98 | 17.99 | 2.97 | `jani_portrait_red.jpg` (`jani_ashram_ambaji.mp4`) | pan R→L | 70 YEARS (lower) | sfx_whoosh.wav@0.0 · Saffron/crimson accent |
| S008 | 00:20.95 | 20.95 | 2.97 | `jani_ashram_ambaji.mp4` (`jani_portrait_red.jpg`) | zoom 1.00→1.15 |  |  |
| S009 | 00:23.92 | 23.92 | 3.35 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | pan L→R |  | sfx_whoosh.wav@0.0 · Glitch transitions between headline crops |
| S010 | 00:27.27 | 27.27 | 3.35 | `jani_news_2010.mp4` (`headlines_2003_2010.png`) | zoom 1.15→1.00 |  |  |
| S011 | 00:30.62 | 30.62 | 3.35 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | pan R→L | IMPOSSIBLE CLAIM (lower) |  |
| S012 | 00:33.97 | 33.97 | 1.97 | `channel_intro.mp4` (`earth_india.mp4`) | zoom 1.00→1.15 | BE PRACTICAL WITH KISHORE (lower) | sfx_whoosh.wav@0.0 · Channel sting (your own 3-4 s logo animation, or B-roll + lower-third) |
| S013 | 00:35.94 | 35.94 | 1.97 | `channel_intro.mp4` (`earth_india.mp4`) | pan L→R |  |  |
| S014 | 00:37.91 | 37.91 | 3.43 | `earth_india.mp4` (`drdo_lab.mp4`) | zoom 1.15→1.00 |  | Map dive India→Delhi→Ahmedabad on shot 1 |
| S015 | 00:41.34 | 41.34 | 3.43 | `drdo_emblem.png` (`drdo_lab.mp4`) | pan R→L |  |  |
| S016 | 00:44.77 | 44.78 | 3.43 | `drdo_lab.mp4` (`doctor_scrub.mp4`) | zoom 1.00→1.15 | DRDO (lower) | sfx_bass_hit.wav@1.73 |
| S017 | 00:48.20 | 48.21 | 3.43 | `doctor_scrub.mp4` (`hospital_corridor.mp4`) | pan L→R |  |  |
| S018 | 00:51.63 | 51.65 | 3.43 | `drdo_lab.mp4` (`doctor_scrub.mp4`) | zoom 1.15→1.00 | 40 DOCTORS (lower) |  |
| S019 | 00:55.06 | 55.08 | 3.19 | `sterling_hospital_ext.jpg` (`hospital_corridor.mp4`) | pan R→L | AHMEDABAD · 2010 (lower) |  |
| S020 | 00:58.25 | 58.27 | 3.19 | `hospital_corridor.mp4` (`isolation_door.mp4`) | zoom 1.00→1.15 |  |  |

> **⏸ VO PAUSE 01:01.44 (2.5 s)**: VO stops at 61.45 s. Picture: `isolation_door.mp4` (zoom 1.00→1.15). Audio: sfx_door_latch.wav@0.3;sfx_heartbeat_monitor.wav@0. VO pause: door latch + monitor beeps

| S022 | 01:03.94 | 61.45 | 3.37 | `cctv_camera.mp4` (`ai_room_wireframe.mp4`) | zoom 1.15→1.00 +hud | CCTV 24/7 (lower) | sfx_cctv_hum.wav@0.1 · Red REC dot + timestamp HUD |
| S023 | 01:07.31 | 64.82 | 3.37 | `ai_room_wireframe.mp4` (`cctv_camera.mp4`) | pan R→L +hud |  |  |
| S024 | 01:10.68 | 68.19 | 3.37 | `isolation_door.mp4` (`hospital_corridor.mp4`) | zoom 1.00→1.15 | 15 DAYS (timer) |  |
| S025 | 01:14.05 | 71.56 | 3.37 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | pan L→R |  |  |
| S026 | 01:17.42 | 74.93 | 3.27 | `jani_ap_archive.mp4` (`jani_news_2010.mp4`) | zoom 1.15→1.00 |  |  |
| S027 | 01:20.69 | 78.20 | 3.27 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan R→L +hud |  |  |
| S028 | 01:23.96 | 81.48 | 3.27 | `ai_room_wireframe.mp4` (`cctv_camera.mp4`) | zoom 1.00→1.15 +hud |  | sfx_bass_hit.wav@2.15 |
| S029 | 01:27.23 | 84.75 | 3.27 | `hospital_corridor.mp4` (`isolation_door.mp4`) | pan L→R |  |  |
| S030 | 01:30.50 | 88.03 | 3.27 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | zoom 1.15→1.00 |  |  |
| S031 | 01:33.77 | 91.30 | 2.95 | `cells_micro.mp4` (`blood_vessels.mp4`) | pan R→L |  | Name reveal on push-in |
| S032 | 01:36.72 | 94.25 | 2.95 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.00→1.15 | PRAHLAD JANI (lower) | sfx_bass_hit.wav@1.05 |

## Block 2: inside the sealed room

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S033 | 01:39.67 | 97.21 | 2.98 | `jani_ashram_ambaji.mp4` (`jani_portrait_red.jpg`) | pan L→R | CHUNRIWALA MATAJI (lower) |  |
| S034 | 01:42.65 | 100.19 | 2.98 | `jani_portrait_red.jpg` (`jani_ashram_ambaji.mp4`) | zoom 1.15→1.00 |  |  |
| S035 | 01:45.63 | 103.17 | 2.98 | `meditation_silhouette.mp4` (`jani_ashram_ambaji.mp4`) | pan R→L |  |  |
| S036 | 01:48.61 | 106.14 | 2.98 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | zoom 1.00→1.15 | 70+ YEARS (lower) |  |
| S037 | 01:51.59 | 109.12 | 2.98 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | pan L→R |  |  |

> **🎬 LIVE CLIP 01:54.57 (10.0 s)**: VO stops at 112.1 s; `jani_news_2010.mp4` plays 0.0–10.0 s **with its own audio**, then the VO continues. Original 2010 news report plays with its own audio, then VO: 'ఈ విషయం worldwide viral...'. Set src_in/src_out to the best 8-12 s *(optional: skipped until the clip is in assets/)*

| S039 | 02:04.57 | 112.10 | 3.35 | `drdo_lab.mp4` (`doctor_scrub.mp4`) | pan R→L | DIPAS · DRDO (lower) | press_conf_shah: picture only here (VO over it) |
| S040 | 02:07.92 | 115.44 | 3.35 | `drdo_emblem.png` (`drdo_lab.mp4`) | zoom 1.00→1.15 |  |  |
| S041 | 02:11.27 | 118.79 | 3.35 | `sterling_hospital_ext.jpg` (`hospital_corridor.mp4`) | pan L→R |  |  |
| S042 | 02:14.62 | 122.14 | 3.35 | `press_conf_shah.mp4` (`jani_news_2010.mp4`) | zoom 1.15→1.00 | DR. SUDHIR SHAH (lower) |  |
| S043 | 02:17.97 | 125.48 | 2.67 | `doctor_scrub.mp4` (`drdo_lab.mp4`) | pan R→L |  |  |
| S044 | 02:20.64 | 128.15 | 2.67 | `blood_sample.mp4` (`drdo_lab.mp4`) | zoom 1.00→1.15 |  |  |
| S045 | 02:23.31 | 130.82 | 3.37 | `siachen_soldiers.mp4` (`desert_soldiers.mp4`) | pan L→R |  | sfx_whoosh.wav@0.0 · Military / disaster / space montage |
| S046 | 02:26.68 | 134.19 | 3.37 | `desert_soldiers.mp4` (`siachen_soldiers.mp4`) | zoom 1.15→1.00 |  |  |
| S047 | 02:30.05 | 137.56 | 3.37 | `disaster_rescue.mp4` (`desert_soldiers.mp4`) | pan R→L |  |  |
| S048 | 02:33.42 | 140.93 | 3.37 | `astronaut_iss.mp4` (`earth_india.mp4`) | zoom 1.00→1.15 |  |  |
| S049 | 02:36.79 | 144.30 | 2.06 | `jani_news_2010.mp4` (`sterling_hospital_ext.jpg`) | pan L→R | 22 APRIL 2010 (lower) | sfx_bass_hit.wav@0.2 |
| S050 | 02:38.85 | 146.36 | 2.06 | `clock_macro.mp4` (`hospital_corridor.mp4`) | zoom 1.15→1.00 |  |  |
| S051 | 02:40.91 | 148.42 | 3.50 | `water_tap_close.mp4` (`ai_room_valve.mp4`) | pan R→L | ZERO WATER (lower) | Rule 1 |
| S052 | 02:44.41 | 151.92 | 3.50 | `ai_room_valve.mp4` (`water_tap_close.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S053 | 02:47.91 | 155.42 | 3.15 | `cctv_camera.mp4` (`ai_room_wireframe.mp4`) | pan L→R +hud | 2 CAMERAS · 24/7 (lower) | sfx_cctv_hum.wav@0.0 · Rule 2 |
| S054 | 02:51.06 | 158.57 | 3.15 | `ai_room_wireframe.mp4` (`cctv_camera.mp4`) | zoom 1.15→1.00 +hud |  |  |
| S055 | 02:54.21 | 161.72 | 2.71 | `hospital_corridor.mp4` (`jani_ap_archive.mp4`) | pan R→L | OBSERVER IN ROOM (lower) | Rule 3 |
| S056 | 02:56.92 | 164.43 | 2.71 | `jani_ap_archive.mp4` (`ecg_monitor.mp4`) | zoom 1.00→1.15 |  |  |
| S057 | 02:59.63 | 167.13 | 2.71 | `ecg_monitor.mp4` (`hospital_corridor.mp4`) | pan L→R +hud |  |  |
| S058 | 03:02.34 | 169.84 | 3.11 | `sponge_squeeze.mp4` (`water_drop_macro.mp4`) | zoom 1.15→1.00 |  | Rule 4 |
| S059 | 03:05.45 | 172.95 | 3.11 | `ai_beaker.mp4` (`beaker_measure.mp4`) | pan R→L +hud |  |  |
| S060 | 03:08.56 | 176.07 | 3.11 | `beaker_measure.mp4` (`ai_beaker.mp4`) | zoom 1.00→1.15 | MEASURED TO THE ML (lower) |  |
| S061 | 03:11.67 | 179.18 | 3.11 | `water_drop_macro.mp4` (`beaker_measure.mp4`) | pan L→R |  |  |
| S062 | 03:14.78 | 182.30 | 3.11 | `beaker_measure.mp4` (`water_drop_macro.mp4`) | zoom 1.15→1.00 |  |  |
| S063 | 03:17.89 | 185.41 | 2.55 | `water_drop_macro.mp4` (`beaker_measure.mp4`) | pan R→L |  | sfx_bass_hit.wav@0.5 |
| S064 | 03:20.44 | 187.95 | 2.55 | `water_drop_macro.mp4` (`beaker_measure.mp4`) | zoom 1.00→1.15 |  |  |
| S065 | 03:22.99 | 190.50 | 3.12 | `clock_macro.mp4` (`cracked_earth.mp4`) | pan L→R | DAY 3 (timer) | sfx_clock.wav@0.0 · Dehydration curve dropping to red (HUD layer) |
| S066 | 03:26.11 | 193.62 | 3.12 | `ai_kidney_dehydrated.mp4` (`blood_vessels.mp4`) | zoom 1.15→1.00 +hud |  |  |
| S067 | 03:29.23 | 196.75 | 3.12 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan R→L +hud |  |  |
| S068 | 03:32.35 | 199.87 | 3.21 | `cracked_earth.mp4` (`sweat_macro.mp4`) | zoom 1.00→1.15 |  | Flat stable vitals line vs falling curve (HUD) |
| S069 | 03:35.56 | 203.08 | 3.21 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | pan L→R |  |  |
| S070 | 03:38.77 | 206.29 | 3.21 | `pulse_oximeter.mp4` (`ecg_monitor.mp4`) | zoom 1.15→1.00 +hud | VITALS REPORTED NORMAL (lower) |  |
| S071 | 03:41.98 | 209.50 | 3.21 | `blood_sample.mp4` (`ecg_monitor.mp4`) | pan R→L |  |  |
| S072 | 03:45.19 | 212.71 | 2.75 | `hospital_corridor.mp4` (`ultrasound_screen.mp4`) | zoom 1.00→1.15 | DAY 7 → 10 (timer) |  |
| S073 | 03:47.94 | 215.46 | 2.75 | `ultrasound_screen.mp4` (`ecg_monitor.mp4`) | pan L→R +hud |  |  |
| S074 | 03:50.69 | 218.20 | 2.75 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.15→1.00 |  | sfx_bass_hit.wav@2.41 |
| S075 | 03:53.44 | 220.95 | 2.75 | `hospital_corridor.mp4` (`ultrasound_screen.mp4`) | pan R→L |  |  |

> **⏸ VO PAUSE 03:56.19 (3.0 s)**: VO stops at 223.7 s. Picture: `ecg_monitor.mp4` (zoom 1.00→1.15). Audio: sfx_heartbeat_monitor.wav@0. VO pause after 'biggest shock ఏంటో తెలుసా?'


## Block 3: the ultrasound shock

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S077 | 03:59.19 | 223.70 | 2.75 | `ai_bladder_model.mp4` (`bladder_anatomy.jpg`) | pan L→R +hud | THE BLADDER MYSTERY (lower) | sfx_bass_hit.wav@0.0 |
| S078 | 04:01.94 | 226.45 | 2.91 | `ai_bladder_model.mp4` (`bladder_anatomy.jpg`) | zoom 1.15→1.00 +hud | 15 DAYS · NO URINE (lower) |  |
| S079 | 04:04.85 | 229.36 | 2.91 | `bladder_anatomy.jpg` (`ai_bladder_model.mp4`) | pan R→L |  |  |
| S080 | 04:07.76 | 232.27 | 2.91 | `ai_kidney_dehydrated.mp4` (`kidney_anatomy.jpg`) | zoom 1.00→1.15 +hud |  |  |
| S081 | 04:10.67 | 235.18 | 2.91 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan L→R +hud |  |  |
| S082 | 04:13.58 | 238.09 | 2.91 | `ai_bladder_model.mp4` (`bladder_anatomy.jpg`) | zoom 1.15→1.00 +hud |  |  |
| S083 | 04:16.49 | 241.00 | 3.53 | `ultrasound_screen.mp4` (`ai_sonography.mp4`) | pan R→L +hud | SONOGRAPHY (lower) |  |
| S084 | 04:20.02 | 244.53 | 3.53 | `ai_sonography.mp4` (`ultrasound_screen.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S085 | 04:23.55 | 248.07 | 3.35 | `ai_sonography.mp4` (`ultrasound_screen.mp4`) | pan L→R +hud | ILLUSTRATION (tag) | AI shots carry the ILLUSTRATION tag |
| S086 | 04:26.90 | 251.42 | 3.35 | `ai_bladder_model.mp4` (`bladder_anatomy.jpg`) | zoom 1.15→1.00 +hud |  |  |
| S087 | 04:30.25 | 254.78 | 3.35 | `ai_sonography.mp4` (`ultrasound_screen.mp4`) | pan R→L +hud |  | sfx_bass_hit.wav@2.29 |
| S088 | 04:33.60 | 258.13 | 3.35 | `ai_bladder_reabsorb.mp4` (`cells_micro.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S089 | 04:36.95 | 261.49 | 3.35 | `cells_micro.mp4` (`blood_vessels.mp4`) | pan L→R | DOCTORS' HYPOTHESIS (lower) |  |
| S090 | 04:40.30 | 264.84 | 3.35 | `blood_vessels.mp4` (`cells_micro.mp4`) | zoom 1.15→1.00 |  |  |
| S091 | 04:43.65 | 268.20 | 2.43 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | pan R→L |  |  |
| S092 | 04:46.08 | 270.63 | 2.43 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.00→1.15 |  |  |
| S093 | 04:48.51 | 273.07 | 2.43 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | pan L→R |  |  |
| S094 | 04:50.94 | 275.50 | 3.05 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | zoom 1.15→1.00 | DAY 15 (timer) |  |
| S095 | 04:53.99 | 278.55 | 3.05 | `scale_weight.mp4` (`ecg_monitor.mp4`) | pan R→L |  |  |
| S096 | 04:57.04 | 281.60 | 3.05 | `ecg_monitor.mp4` (`blood_sample.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S097 | 05:00.09 | 284.64 | 3.05 | `ultrasound_screen.mp4` (`ecg_monitor.mp4`) | pan L→R +hud |  |  |
| S098 | 05:03.14 | 287.69 | 3.05 | `blood_sample.mp4` (`ecg_monitor.mp4`) | zoom 1.15→1.00 |  |  |

## Block 4: the press meet and the science

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S099 | 05:06.19 | 290.74 | 2.44 | `press_conf_shah.mp4` (`jani_news_2010.mp4`) | pan R→L | PRESS MEET · MAY 2010 (lower) | press_conf_shah: picture only here (VO over it) |
| S100 | 05:08.63 | 293.18 | 2.44 | `drdo_emblem.png` (`press_conf_shah.mp4`) | zoom 1.00→1.15 |  |  |
| S101 | 05:11.07 | 295.61 | 2.44 | `press_conf_shah.mp4` (`jani_news_2010.mp4`) | pan L→R |  |  |

> **🎬 LIVE CLIP 05:13.51 (12.0 s)**: VO stops at 298.05 s; `press_conf_shah.mp4` plays 0.0–12.0 s **with its own audio**, then the VO continues. The REAL press-conference audio plays here. Set src_in/src_out to the exact quote; put the Telugu translation in `subtitle` *(optional: skipped until the clip is in assets/)*

| S103 | 05:25.51 | 298.05 | 3.35 | `meditation_silhouette.mp4` (`jani_ashram_ambaji.mp4`) | pan R→L | HYPOMETABOLISM (lower) | sfx_bass_hit.wav@0.15 |
| S104 | 05:28.86 | 301.40 | 3.35 | `ai_glow_body.mp4` (`meditation_silhouette.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S105 | 05:32.21 | 304.75 | 3.35 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan L→R +hud |  |  |
| S106 | 05:35.56 | 308.10 | 2.96 | `cells_micro.mp4` (`blood_vessels.mp4`) | zoom 1.15→1.00 | ILLUSTRATION (tag) |  |
| S107 | 05:38.52 | 311.06 | 2.96 | `ai_autophagy.mp4` (`cells_micro.mp4`) | pan R→L +hud | AUTOPHAGY (lower) |  |
| S108 | 05:41.48 | 314.02 | 2.96 | `ai_mito_energy.mp4` (`cells_micro.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S109 | 05:44.44 | 316.97 | 2.96 | `ai_autophagy.mp4` (`cells_micro.mp4`) | pan L→R +hud |  |  |
| S110 | 05:47.40 | 319.93 | 2.96 | `blood_vessels.mp4` (`cells_micro.mp4`) | zoom 1.15→1.00 |  |  |
| S111 | 05:50.36 | 322.89 | 3.18 | `meditation_silhouette.mp4` (`jani_ashram_ambaji.mp4`) | pan R→L |  |  |
| S112 | 05:53.54 | 326.07 | 3.18 | `jani_ashram_ambaji.mp4` (`meditation_silhouette.mp4`) | zoom 1.00→1.15 |  |  |
| S113 | 05:56.72 | 329.25 | 3.18 | `ai_glow_body.mp4` (`meditation_silhouette.mp4`) | pan L→R +hud |  |  |
| S114 | 05:59.90 | 332.42 | 3.18 | `meditation_silhouette.mp4` (`jani_portrait_red.jpg`) | zoom 1.15→1.00 |  |  |

> **🎬 LIVE CLIP 06:03.08 (10.0 s)**: VO stops at 335.6 s; `skeptic_view.mp4` plays 0.0–10.0 s **with its own audio**, then the VO continues. Recommended for balance: a real 2010 TV interview with a doctor/rationalist who questioned the study. Skipped automatically if not downloaded *(optional: skipped until the clip is in assets/)*

| S116 | 06:13.08 | 335.60 | 2.77 | `ai_glow_body.mp4` (`meditation_silhouette.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S117 | 06:15.85 | 338.37 | 2.77 | `earth_india.mp4` (`ai_glow_body.mp4`) | pan L→R |  |  |
| S118 | 06:18.62 | 341.14 | 2.77 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.15→1.00 |  |  |
| S119 | 06:21.39 | 343.91 | 2.77 | `meditation_silhouette.mp4` (`ai_glow_body.mp4`) | pan R→L |  |  |

## Outro: your opinion + subscribe

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S120 | 06:24.16 | 346.68 | 3.13 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.00→1.15 |  | Last ~20 s: calm B-roll, no text, so YouTube end-screen elements (subscribe + next video) fit |
| S121 | 06:27.29 | 349.81 | 3.13 | `meditation_silhouette.mp4` (`ai_glow_body.mp4`) | pan L→R |  |  |
| S122 | 06:30.42 | 352.93 | 3.13 | `ai_glow_body.mp4` (`meditation_silhouette.mp4`) | zoom 1.15→1.00 +hud |  |  |
| S123 | 06:33.55 | 356.06 | 3.13 | `jani_ashram_ambaji.mp4` (`jani_portrait_red.jpg`) | pan R→L |  |  |
| S124 | 06:36.68 | 359.18 | 3.13 | `earth_india.mp4` (`ai_glow_body.mp4`) | zoom 1.00→1.15 |  |  |
| S125 | 06:39.81 | 362.31 | 3.13 | `ai_glow_body.mp4` (`earth_india.mp4`) | pan L→R +hud |  |  |
| S126 | 06:42.94 | 365.43 | 3.13 | `meditation_silhouette.mp4` (`earth_india.mp4`) | zoom 1.15→1.00 |  |  |

**Programme length with every clip: 06:46.07** (121 shots, 3 live clips, 2 VO pauses).


## Audio cue sheet
| Element | Level | Notes |
|---|---|---|
| Voiceover (`voiceover.mp3`) | lead, normalised with the mix to −14 LUFS / −1 dBTP | Removes the duplicate line at VO 221.40–223.40 |
| BGM (`bgm_dark.mp3`) | −20 dB, side-chain ducked (ratio 6, release 400 ms) | Swells up in each pause |
| SFX | −8 dB, 3 s max with 0.3 s fade | Placed from the `sfx` column (`file@seconds-into-shot`) |
| Pause audio | 0 dB | Real recordings only. Pause 3 must be the real Dr. Shah clip; if none exists, use monitor beeps |
