# Step 2: scene and timeline map (EDL)

Generated from `edl.csv` by `tools/edl_md.py`; edit the CSV, not this file. **Prog** = final video time; **VO** = time in `voiceover.mp3`. Every shot gets grain + vignette (Layer 2); `+hud` adds the medical HUD.


## Block 1: the 3-day rule and the DRDO challenge

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S001 | 00:00.00 | 0.00 | 3.60 | `clock_macro.mp4` (`cracked_earth.mp4`) | pan L→R | DAY 1 → 3 → 4 (timer) | sfx_clock.wav@0.0 · Hook: kinetic day counter top-right |
| S002 | 00:03.60 | 3.60 | 3.60 | `cracked_earth.mp4` (`sweat_macro.mp4`) | zoom 1.15→1.00 |  |  |
| S003 | 00:07.20 | 7.20 | 2.74 | `ai_kidney_healthy.mp4` (`kidney_anatomy.jpg`) | pan R→L +hud | 3-DAY RULE (lower) | Amber toxic grade on shot 2-3 |
| S004 | 00:09.94 | 9.94 | 2.74 | `ai_kidney_dehydrated.mp4` (`blood_vessels.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S005 | 00:12.68 | 12.68 | 2.74 | `blood_vessels.mp4` (`cells_micro.mp4`) | pan L→R |  | sfx_bass_hit.wav@2.72 |
| S006 | 00:15.42 | 15.42 | 2.21 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | zoom 1.15→1.00 +hud |  | Flatline lands on 'కానీ...' |
| S007 | 00:17.63 | 17.63 | 2.21 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan R→L +hud |  | sfx_flatline.wav@0.99 |
| S008 | 00:19.84 | 19.84 | 3.36 | `jani_portrait_red.jpg` (`jani_ashram_ambaji.mp4`) | zoom 1.00→1.15 | 70 YEARS (lower) | sfx_whoosh.wav@0.0 · Saffron/crimson accent grade |
| S009 | 00:23.20 | 23.20 | 3.36 | `jani_ashram_ambaji.mp4` (`jani_portrait_red.jpg`) | pan L→R |  |  |
| S010 | 00:26.56 | 26.56 | 2.63 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | zoom 1.15→1.00 |  | sfx_whoosh.wav@0.0 · Glitch transition between headline crops |
| S011 | 00:29.19 | 29.19 | 2.63 | `jani_news_2010.mp4` (`headlines_2003_2010.png`) | pan R→L | IMPOSSIBLE CLAIM (lower) |  |
| S012 | 00:31.82 | 31.81 | 2.63 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | zoom 1.00→1.15 |  |  |
| S013 | 00:34.45 | 34.44 | 3.53 | `earth_india.mp4` (`drdo_lab.mp4`) | pan L→R |  | Map dive India→Delhi→Ahmedabad on shot 1 |
| S014 | 00:37.98 | 37.97 | 3.53 | `drdo_emblem.png` (`drdo_lab.mp4`) | zoom 1.15→1.00 | DRDO (lower) | sfx_bass_hit.wav@3.27 |
| S015 | 00:41.51 | 41.50 | 3.53 | `drdo_lab.mp4` (`doctor_scrub.mp4`) | pan R→L |  |  |
| S016 | 00:45.04 | 45.04 | 3.53 | `doctor_scrub.mp4` (`hospital_corridor.mp4`) | zoom 1.00→1.15 | 40 DOCTORS (lower) |  |
| S017 | 00:48.57 | 48.57 | 3.08 | `sterling_hospital_ext.jpg` (`hospital_corridor.mp4`) | pan L→R | AHMEDABAD · 2010 (lower) |  |
| S018 | 00:51.65 | 51.65 | 3.08 | `hospital_corridor.mp4` (`isolation_door.mp4`) | zoom 1.15→1.00 |  |  |

> **⏸ LIVE AUDIO PAUSE 00:54.73 (2.5 s)**: VO stops at 54.73 s. Picture: `isolation_door.mp4` (zoom 1.00→1.15). Audio: sfx_door_latch.wav@0.3;sfx_heartbeat_monitor.wav@0. LIVE AUDIO PAUSE 2.5 s: door latch + monitor beeps

| S020 | 00:57.23 | 54.73 | 3.39 | `cctv_camera.mp4` (`ai_room_wireframe.mp4`) | zoom 1.00→1.15 +hud | CCTV 24/7 (lower) | sfx_cctv_hum.wav@0.0 · Red REC dot + timestamp HUD |
| S021 | 01:00.62 | 58.12 | 3.39 | `ai_room_wireframe.mp4` (`cctv_camera.mp4`) | pan L→R +hud |  |  |
| S022 | 01:04.01 | 61.50 | 3.39 | `isolation_door.mp4` (`hospital_corridor.mp4`) | zoom 1.15→1.00 | 15 DAYS (timer) |  |
| S023 | 01:07.40 | 64.89 | 3.39 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | pan R→L |  |  |
| S024 | 01:10.79 | 68.28 | 3.46 | `jani_ap_archive.mp4` (`jani_news_2010.mp4`) | zoom 1.00→1.15 |  |  |
| S025 | 01:14.25 | 71.74 | 3.46 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan L→R +hud |  | sfx_bass_hit.wav@3.04 |
| S026 | 01:17.71 | 75.19 | 3.46 | `ai_room_wireframe.mp4` (`cctv_camera.mp4`) | zoom 1.15→1.00 +hud |  |  |
| S027 | 01:21.17 | 78.65 | 3.46 | `hospital_corridor.mp4` (`isolation_door.mp4`) | pan R→L |  |  |
| S028 | 01:24.63 | 82.10 | 3.46 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | zoom 1.00→1.15 |  |  |
| S029 | 01:28.09 | 85.56 | 3.45 | `cells_micro.mp4` (`blood_vessels.mp4`) | pan L→R |  | Name reveal on push-in |
| S030 | 01:31.54 | 89.02 | 3.45 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.15→1.00 | PRAHLAD JANI (lower) | sfx_bass_hit.wav@1.55 |

## Block 2: inside the sealed room

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S031 | 01:34.99 | 92.47 | 3.15 | `jani_ashram_ambaji.mp4` (`jani_portrait_red.jpg`) | pan R→L | CHUNRIWALA MATAJI (lower) |  |
| S032 | 01:38.14 | 95.62 | 3.15 | `jani_portrait_red.jpg` (`jani_ashram_ambaji.mp4`) | zoom 1.00→1.15 |  |  |
| S033 | 01:41.29 | 98.76 | 3.15 | `meditation_silhouette.mp4` (`jani_ashram_ambaji.mp4`) | pan L→R | 70+ YEARS (lower) |  |
| S034 | 01:44.44 | 101.91 | 3.15 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | zoom 1.15→1.00 |  |  |
| S035 | 01:47.59 | 105.05 | 3.15 | `jani_news_2010.mp4` (`jani_portrait_red.jpg`) | pan R→L |  |  |
| S036 | 01:50.74 | 108.20 | 3.60 | `drdo_lab.mp4` (`doctor_scrub.mp4`) | zoom 1.00→1.15 | DIPAS · DRDO (lower) | press_conf_shah: picture only, muted |
| S037 | 01:54.34 | 111.80 | 3.60 | `drdo_emblem.png` (`drdo_lab.mp4`) | pan L→R |  |  |
| S038 | 01:57.94 | 115.40 | 3.60 | `sterling_hospital_ext.jpg` (`hospital_corridor.mp4`) | zoom 1.15→1.00 | DR. SUDHIR SHAH (lower) |  |
| S039 | 02:01.54 | 118.99 | 3.60 | `press_conf_shah.mp4` (`jani_news_2010.mp4`) | pan R→L |  |  |
| S040 | 02:05.14 | 122.59 | 2.91 | `doctor_scrub.mp4` (`drdo_lab.mp4`) | zoom 1.00→1.15 |  |  |
| S041 | 02:08.05 | 125.50 | 2.91 | `blood_sample.mp4` (`drdo_lab.mp4`) | pan L→R |  |  |
| S042 | 02:10.96 | 128.42 | 2.91 | `drdo_lab.mp4` (`blood_sample.mp4`) | zoom 1.15→1.00 |  |  |
| S043 | 02:13.87 | 131.33 | 2.62 | `siachen_soldiers.mp4` (`desert_soldiers.mp4`) | pan R→L |  | sfx_whoosh.wav@0.0 · Military motivation montage |
| S044 | 02:16.49 | 133.95 | 2.62 | `desert_soldiers.mp4` (`siachen_soldiers.mp4`) | zoom 1.00→1.15 |  |  |
| S045 | 02:19.11 | 136.56 | 2.62 | `disaster_rescue.mp4` (`desert_soldiers.mp4`) | pan L→R |  |  |
| S046 | 02:21.73 | 139.18 | 2.62 | `astronaut_iss.mp4` (`earth_india.mp4`) | zoom 1.15→1.00 |  |  |
| S047 | 02:24.35 | 141.80 | 2.99 | `jani_news_2010.mp4` (`sterling_hospital_ext.jpg`) | pan R→L | 22 APRIL 2010 (lower) | sfx_bass_hit.wav@0.5 |
| S048 | 02:27.34 | 144.79 | 2.98 | `clock_macro.mp4` (`hospital_corridor.mp4`) | zoom 1.00→1.15 |  |  |
| S049 | 02:30.32 | 147.77 | 2.29 | `water_tap_close.mp4` (`ai_room_valve.mp4`) | pan L→R | ZERO WATER (lower) | Rule 1 |
| S050 | 02:32.61 | 150.06 | 2.30 | `ai_room_valve.mp4` (`water_tap_close.mp4`) | zoom 1.15→1.00 +hud |  |  |
| S051 | 02:34.91 | 152.36 | 3.13 | `cctv_camera.mp4` (`ai_room_wireframe.mp4`) | pan R→L +hud | 2 CAMERAS · 24/7 (lower) | sfx_cctv_hum.wav@0.0 · Rule 2: split-angle CCTV frames |
| S052 | 02:38.04 | 155.49 | 3.13 | `ai_room_wireframe.mp4` (`cctv_camera.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S053 | 02:41.17 | 158.62 | 2.86 | `hospital_corridor.mp4` (`jani_ap_archive.mp4`) | pan L→R | OBSERVER IN ROOM (lower) | Rule 3 |
| S054 | 02:44.03 | 161.48 | 2.86 | `jani_ap_archive.mp4` (`ecg_monitor.mp4`) | zoom 1.15→1.00 |  |  |
| S055 | 02:46.89 | 164.34 | 2.86 | `ecg_monitor.mp4` (`hospital_corridor.mp4`) | pan R→L +hud |  |  |
| S056 | 02:49.75 | 167.20 | 3.31 | `sponge_squeeze.mp4` (`water_drop_macro.mp4`) | zoom 1.00→1.15 |  | Rule 4 |
| S057 | 02:53.06 | 170.51 | 3.31 | `ai_beaker.mp4` (`beaker_measure.mp4`) | pan L→R +hud |  |  |
| S058 | 02:56.37 | 173.82 | 3.31 | `beaker_measure.mp4` (`ai_beaker.mp4`) | zoom 1.15→1.00 | MEASURED TO THE ML (lower) |  |
| S059 | 02:59.68 | 177.14 | 3.31 | `water_drop_macro.mp4` (`beaker_measure.mp4`) | pan R→L |  |  |
| S060 | 03:02.99 | 180.45 | 3.31 | `beaker_measure.mp4` (`water_drop_macro.mp4`) | zoom 1.00→1.15 |  |  |
| S061 | 03:06.30 | 183.76 | 2.46 | `water_drop_macro.mp4` (`beaker_measure.mp4`) | pan L→R |  | sfx_bass_hit.wav@0.0 |
| S062 | 03:08.76 | 186.22 | 2.46 | `water_drop_macro.mp4` (`beaker_measure.mp4`) | zoom 1.15→1.00 |  |  |
| S063 | 03:11.22 | 188.68 | 3.27 | `clock_macro.mp4` (`cracked_earth.mp4`) | pan R→L | DAY 3 (timer) | sfx_clock.wav@0.0 · Standard dehydration curve dropping to red zone (HUD layer) |
| S064 | 03:14.49 | 191.95 | 3.27 | `ai_kidney_dehydrated.mp4` (`blood_vessels.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S065 | 03:17.76 | 195.22 | 3.27 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | pan L→R +hud |  |  |
| S066 | 03:21.03 | 198.49 | 3.27 | `cracked_earth.mp4` (`sweat_macro.mp4`) | zoom 1.15→1.00 |  |  |
| S067 | 03:24.30 | 201.76 | 2.78 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | pan R→L |  | Flat stable vitals line vs. falling curve (HUD) |
| S068 | 03:27.08 | 204.54 | 2.78 | `pulse_oximeter.mp4` (`ecg_monitor.mp4`) | zoom 1.00→1.15 +hud | VITALS REPORTED NORMAL (lower) |  |
| S069 | 03:29.86 | 207.32 | 2.78 | `blood_sample.mp4` (`ecg_monitor.mp4`) | pan L→R |  |  |
| S070 | 03:32.64 | 210.10 | 2.83 | `hospital_corridor.mp4` (`ultrasound_screen.mp4`) | zoom 1.15→1.00 | DAY 7 → 10 (timer) |  |
| S071 | 03:35.47 | 212.93 | 2.82 | `ultrasound_screen.mp4` (`ecg_monitor.mp4`) | pan R→L +hud |  |  |
| S072 | 03:38.29 | 215.75 | 2.82 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | zoom 1.00→1.15 |  | sfx_bass_hit.wav@1.95 |
| S073 | 03:41.11 | 218.57 | 2.83 | `hospital_corridor.mp4` (`ultrasound_screen.mp4`) | pan L→R |  |  |

> **⏸ LIVE AUDIO PAUSE 03:43.94 (3.0 s)**: VO stops at 221.4 s, skips 2.0 s of VO. Picture: `ecg_monitor.mp4` (zoom 1.00→1.15). Audio: sfx_heartbeat_monitor.wav@0. LIVE AUDIO PAUSE 3 s; also removes the repeated VO line 221.40–223.40


## Block 3: the ultrasound shock

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S075 | 03:46.94 | 223.40 | 3.41 | `ai_bladder_model.mp4` (`bladder_anatomy.jpg`) | pan R→L +hud | 15 DAYS · NO URINE (lower) |  |
| S076 | 03:50.35 | 226.81 | 3.41 | `bladder_anatomy.jpg` (`ai_bladder_model.mp4`) | zoom 1.00→1.15 |  |  |
| S077 | 03:53.76 | 230.21 | 3.41 | `ai_kidney_dehydrated.mp4` (`kidney_anatomy.jpg`) | pan L→R +hud |  |  |
| S078 | 03:57.17 | 233.62 | 3.41 | `ecg_monitor.mp4` (`pulse_oximeter.mp4`) | zoom 1.15→1.00 +hud |  |  |
| S079 | 04:00.58 | 237.02 | 3.21 | `ultrasound_screen.mp4` (`ai_sonography.mp4`) | pan R→L +hud |  |  |
| S080 | 04:03.79 | 240.23 | 3.21 | `ai_sonography.mp4` (`ultrasound_screen.mp4`) | zoom 1.00→1.15 +hud | SONOGRAPHY (lower) |  |
| S081 | 04:07.00 | 243.43 | 3.21 | `doctor_scrub.mp4` (`hospital_corridor.mp4`) | pan L→R |  |  |
| S082 | 04:10.21 | 246.64 | 2.99 | `ai_sonography.mp4` (`ultrasound_screen.mp4`) | zoom 1.15→1.00 +hud | ILLUSTRATION (tag) | AI shots carry 'ILLUSTRATION' tag (top-left) |
| S083 | 04:13.20 | 249.63 | 2.99 | `ai_bladder_model.mp4` (`bladder_anatomy.jpg`) | pan R→L +hud |  | sfx_bass_hit.wav@1.41 |
| S084 | 04:16.19 | 252.62 | 2.99 | `ai_sonography.mp4` (`ultrasound_screen.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S085 | 04:19.18 | 255.61 | 2.99 | `ai_bladder_reabsorb.mp4` (`cells_micro.mp4`) | pan L→R +hud | DOCTORS' HYPOTHESIS (lower) |  |
| S086 | 04:22.17 | 258.60 | 2.99 | `cells_micro.mp4` (`blood_vessels.mp4`) | zoom 1.15→1.00 |  |  |
| S087 | 04:25.16 | 261.59 | 2.99 | `blood_vessels.mp4` (`cells_micro.mp4`) | pan R→L |  |  |
| S088 | 04:28.15 | 264.58 | 3.30 | `headlines_2003_2010.png` (`jani_news_2010.mp4`) | zoom 1.00→1.15 |  |  |
| S089 | 04:31.45 | 267.88 | 3.30 | `jani_portrait_red.jpg` (`jani_news_2010.mp4`) | pan L→R |  |  |
| S090 | 04:34.75 | 271.18 | 3.19 | `jani_news_2010.mp4` (`jani_ap_archive.mp4`) | zoom 1.15→1.00 | DAY 15 (timer) |  |
| S091 | 04:37.94 | 274.38 | 3.19 | `scale_weight.mp4` (`ecg_monitor.mp4`) | pan R→L |  |  |
| S092 | 04:41.13 | 277.57 | 3.19 | `ecg_monitor.mp4` (`blood_sample.mp4`) | zoom 1.00→1.15 +hud |  |  |
| S093 | 04:44.32 | 280.76 | 3.19 | `ultrasound_screen.mp4` (`ecg_monitor.mp4`) | pan L→R +hud |  |  |

> **⏸ LIVE AUDIO PAUSE 04:47.51 (4.0 s)**: VO stops at 283.96 s. Picture: `press_conf_shah.mp4` (zoom 1.00→1.15). Audio: press_conf_shah.mp4 (real audio). LIVE AUDIO PAUSE 4 s: real Dr. Shah press-conference audio only; if no clip, use monitor beeps


**Programme length: 04:51.51** (91 shots, 0 live clips, 3 VO pauses).


## Audio cue sheet
| Element | Level | Notes |
|---|---|---|
| Voiceover (`voiceover.mp3`) | lead, normalised with the mix to −14 LUFS / −1 dBTP | Removes the duplicate line at VO 221.40–223.40 |
| BGM (`bgm_dark.mp3`) | −20 dB, side-chain ducked (ratio 6, release 400 ms) | Swells up in each pause |
| SFX | −8 dB, 3 s max with 0.3 s fade | Placed from the `sfx` column (`file@seconds-into-shot`) |
| Pause audio | 0 dB | Real recordings only. Pause 3 must be the real Dr. Shah clip; if none exists, use monitor beeps |
