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
| S020 | 00:58.25 | 58.27 | 3.19 | `hospital_corridor.mp4` (``) | zoom 1.00→1.15 |  |  |

> **⏸ VO PAUSE 01:01.44 (2.5 s)**: VO stops at 61.45 s. Picture: `isolation_door.mp4` (zoom 1.00→1.15). Audio: sfx_door_latch.wav@0.3;sfx_heartbeat_monitor.wav@0. VO pause: door + monitor

| S022 | 01:03.94 | 61.45 | 3.37 | `iv_room.mp4` (``) | zoom 1.15→1.00 | CCTV 24/7 (lower) | CCTV look |
| S023 | 01:07.31 | 64.82 | 3.37 | `hospital_corridor.mp4` (``) | pan R→L |  |  |
| S024 | 01:10.68 | 68.19 | 3.37 | `isolation_door.mp4` (``) | zoom 1.00→1.15 | 15 DAYS (timer) |  |
| S025 | 01:14.05 | 71.56 | 3.37 | `icu_room.jpg` (``) | pan L→R |  |  |
| S026 | 01:17.42 | 74.93 | 3.27 | `ecg_photo.jpg` (``) | zoom 1.15→1.00 |  |  |
| S027 | 01:20.69 | 78.20 | 3.27 | `iv_room.mp4` (``) | pan R→L |  |  |
| S028 | 01:23.96 | 81.48 | 3.27 | `pulse_oximeter.mp4` (``) | zoom 1.00→1.15 |  | sfx_bass_hit.wav@2.15 |
| S029 | 01:27.23 | 84.75 | 3.27 | `hospital_corridor.mp4` (``) | pan L→R |  |  |
| S030 | 01:30.50 | 88.03 | 3.27 | `lab_microscope.mp4` (``) | zoom 1.15→1.00 |  |  |
| S031 | 01:33.77 | 91.30 | 2.95 | `lab_cellplate.mp4` (``) | pan R→L |  | Name reveal |
| S032 | 01:36.72 | 94.25 | 2.95 | `jani_portrait_red.jpg` (``) | zoom 1.00→1.15 | PRAHLAD JANI (lower) | sfx_bass_hit.wav@1.05 |

## Block 2: inside the sealed room

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S033 | 01:39.67 | 97.21 | 3.01 | `jani_ashram_ambaji.jpg` (``) | pan L→R | CHUNRIWALA MATAJI (lower) |  |
| S034 | 01:42.68 | 100.22 | 3.01 | `ambaji_gabbar.jpg` (``) | zoom 1.15→1.00 | GABBAR HILL, AMBAJI (tag) |  |
| S035 | 01:45.69 | 103.24 | 3.01 | `yogi_gouache.jpg` (``) | pan R→L | 70+ YEARS (lower) |  |
| S036 | 01:48.70 | 106.25 | 3.01 | `headline_wikipedia.jpg` (``) | zoom 1.00→1.15 | WIKIPEDIA (tag) |  |
| S037 | 01:51.71 | 109.27 | 3.01 | `jani_portrait_red.jpg` (``) | pan L→R | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S038 | 01:54.72 | 112.28 | 3.30 | `lab_hood.mp4` (``) | zoom 1.15→1.00 | DIPAS · DRDO (lower) |  |
| S039 | 01:58.02 | 115.58 | 3.30 | `drdo_lab.mp4` (``) | pan R→L |  |  |
| S040 | 02:01.32 | 118.88 | 3.30 | `sterling_hospital_ext.jpg` (``) | zoom 1.00→1.15 |  |  |
| S041 | 02:04.62 | 122.18 | 3.30 | `doctor_scrub.mp4` (``) | pan L→R | DR. SUDHIR SHAH (lower) |  |
| S042 | 02:07.92 | 125.48 | 2.67 | `lab_pipette.mp4` (``) | zoom 1.15→1.00 |  |  |
| S043 | 02:10.59 | 128.15 | 2.67 | `blood_sample.mp4` (``) | pan R→L |  |  |
| S044 | 02:13.26 | 130.82 | 3.37 | `siachen_soldiers.jpg` (``) | zoom 1.00→1.15 |  | sfx_whoosh.wav@0.0 · Soldiers / extremes / space |
| S045 | 02:16.63 | 134.19 | 3.37 | `desert_soldiers.mp4` (``) | pan L→R |  |  |
| S046 | 02:20.00 | 137.56 | 3.37 | `indian_army.jpg` (``) | zoom 1.15→1.00 |  |  |
| S047 | 02:23.37 | 140.93 | 3.37 | `astronaut_iss.mp4` (``) | pan R→L | NASA (tag) |  |
| S048 | 02:26.74 | 144.30 | 2.06 | `astronaut_iss2.mp4` (``) | zoom 1.00→1.15 | 22 APRIL 2010 (lower) | sfx_bass_hit.wav@0.2 |
| S049 | 02:28.80 | 146.36 | 2.06 | `hospital_entrance.mp4` (``) | pan L→R |  |  |
| S050 | 02:30.86 | 148.42 | 3.50 | `water_tap_close.mp4` (``) | zoom 1.15→1.00 | ZERO WATER (lower) | Rule 1 |
| S051 | 02:34.36 | 151.92 | 3.50 | `water_drop_macro.mp4` (``) | pan R→L |  |  |
| S052 | 02:37.86 | 155.42 | 3.15 | `iv_room.mp4` (``) | zoom 1.00→1.15 | 2 CAMERAS · 24/7 (lower) | Rule 2 (CCTV look) |
| S053 | 02:41.01 | 158.57 | 3.15 | `hospital_corridor.mp4` (``) | pan L→R |  |  |
| S054 | 02:44.16 | 161.72 | 2.71 | `icu_room.jpg` (``) | zoom 1.15→1.00 | OBSERVER IN ROOM (lower) | Rule 3 |
| S055 | 02:46.87 | 164.43 | 2.71 | `pulse_oximeter.mp4` (``) | pan R→L |  |  |
| S056 | 02:49.58 | 167.13 | 2.71 | `doctor_scrub.mp4` (``) | zoom 1.00→1.15 |  |  |
| S057 | 02:52.29 | 169.84 | 3.11 | `water_drop_macro.mp4` (``) | pan L→R |  | Rule 4 |
| S058 | 02:55.40 | 172.95 | 3.11 | `lab_pipette.mp4` (``) | zoom 1.15→1.00 |  |  |
| S059 | 02:58.51 | 176.07 | 3.11 | `lab_tubes.mp4` (``) | pan R→L | MEASURED TO THE ML (lower) |  |
| S060 | 03:01.62 | 179.18 | 3.11 | `water_tap_close.mp4` (``) | zoom 1.00→1.15 |  |  |
| S061 | 03:04.73 | 182.30 | 3.11 | `lab_pipette.mp4` (``) | pan L→R |  |  |
| S062 | 03:07.84 | 185.41 | 2.55 | `water_drop_macro.mp4` (``) | zoom 1.15→1.00 |  | sfx_bass_hit.wav@0.5 |
| S063 | 03:10.39 | 187.95 | 2.55 | `water_drop_macro.mp4` (``) | pan R→L |  |  |
| S064 | 03:12.94 | 190.50 | 3.12 | `dried_leaf.mp4` (``) | zoom 1.00→1.15 | DAY 3 (timer) | sfx_clock.wav@0.0 |
| S065 | 03:16.06 | 193.62 | 3.12 | `kidney_anatomy.jpg` (``) | pan L→R | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S066 | 03:19.18 | 196.75 | 3.12 | `ecg_photo.jpg` (``) | zoom 1.15→1.00 |  |  |
| S067 | 03:22.30 | 199.87 | 3.21 | `cracked_earth.jpg` (``) | pan R→L |  |  |
| S068 | 03:25.51 | 203.08 | 3.21 | `jani_portrait_red.jpg` (``) | zoom 1.00→1.15 | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S069 | 03:28.72 | 206.29 | 3.21 | `pulse_oximeter.mp4` (``) | pan L→R | VITALS REPORTED NORMAL (lower) |  |
| S070 | 03:31.93 | 209.50 | 3.21 | `blood_sample.mp4` (``) | zoom 1.15→1.00 |  |  |
| S071 | 03:35.14 | 212.71 | 2.75 | `hospital_corridor.mp4` (``) | pan R→L | DAY 7 → 10 (timer) |  |
| S072 | 03:37.89 | 215.46 | 2.75 | `ultrasound_screen.jpg` (``) | zoom 1.00→1.15 | NASA (tag) |  |
| S073 | 03:40.64 | 218.20 | 2.75 | `jani_portrait_red.jpg` (``) | pan L→R | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) | sfx_bass_hit.wav@2.41 |
| S074 | 03:43.39 | 220.95 | 2.75 | `hospital_corridor.mp4` (``) | zoom 1.15→1.00 |  |  |

> **⏸ VO PAUSE 03:46.14 (3.0 s)**: VO stops at 223.7 s. Picture: `ecg_photo.jpg` (zoom 1.00→1.15). Audio: sfx_heartbeat_monitor.wav@0. VO pause after 'biggest shock'


## Block 3: the ultrasound shock

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S076 | 03:49.14 | 223.70 | 2.75 | `bladder_anatomy.jpg` (``) | zoom 1.00→1.15 | THE BLADDER MYSTERY (lower) | sfx_bass_hit.wav@0.0 |
| S077 | 03:51.89 | 226.45 | 2.91 | `bladder_anatomy.jpg` (``) | pan L→R | 15 DAYS · NO URINE (lower) |  |
| S078 | 03:54.80 | 229.36 | 2.91 | `kidney_anatomy.jpg` (``) | zoom 1.15→1.00 | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S079 | 03:57.71 | 232.27 | 2.91 | `icu_room.jpg` (``) | pan R→L |  |  |
| S080 | 04:00.62 | 235.18 | 2.91 | `ecg_photo.jpg` (``) | zoom 1.00→1.15 |  |  |
| S081 | 04:03.53 | 238.09 | 2.91 | `bladder_anatomy.jpg` (``) | pan L→R | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S082 | 04:06.44 | 241.00 | 3.53 | `ultrasound_screen.jpg` (``) | zoom 1.15→1.00 | SONOGRAPHY (lower) |  |
| S083 | 04:09.97 | 244.53 | 3.53 | `ultrasound_scan2.jpg` (``) | pan R→L | NASA (tag) |  |
| S084 | 04:13.50 | 248.07 | 3.35 | `sonogram_scan.jpg` (``) | zoom 1.00→1.15 | ILLUSTRATIVE SCAN (tag) |  |
| S085 | 04:16.85 | 251.42 | 3.35 | `bladder_anatomy.jpg` (``) | pan L→R | ENGRAVING · WELLCOME COLLECTION (tag) |  |
| S086 | 04:20.20 | 254.78 | 3.35 | `ultrasound_screen.jpg` (``) | zoom 1.15→1.00 | NASA (tag) | sfx_bass_hit.wav@2.29 |
| S087 | 04:23.55 | 258.13 | 3.35 | `lab_microscope.mp4` (``) | pan R→L |  |  |
| S088 | 04:26.90 | 261.49 | 3.35 | `lab_cellplate.mp4` (``) | zoom 1.00→1.15 | DOCTORS' HYPOTHESIS (lower) |  |
| S089 | 04:30.25 | 264.84 | 3.35 | `blood_sample.mp4` (``) | pan L→R |  |  |
| S090 | 04:33.60 | 268.20 | 2.43 | `headline_wikipedia.jpg` (``) | zoom 1.15→1.00 | WIKIPEDIA (tag) |  |
| S091 | 04:36.03 | 270.63 | 2.43 | `jani_portrait_red.jpg` (``) | pan R→L | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S092 | 04:38.46 | 273.07 | 2.43 | `headline_wikipedia.jpg` (``) | zoom 1.00→1.15 | WIKIPEDIA (tag) |  |
| S093 | 04:40.89 | 275.50 | 3.05 | `headline_edamaruku.jpg` (``) | pan L→R | DAY 15 (timer) |  |
| S094 | 04:43.94 | 278.55 | 3.05 | `scale_weight.jpg` (``) | zoom 1.15→1.00 |  |  |
| S095 | 04:46.99 | 281.60 | 3.05 | `ecg_photo.jpg` (``) | pan R→L |  |  |
| S096 | 04:50.04 | 284.64 | 3.05 | `ultrasound_scan2.jpg` (``) | zoom 1.00→1.15 | NASA (tag) |  |
| S097 | 04:53.09 | 287.69 | 3.05 | `blood_sample.mp4` (``) | pan L→R |  |  |

## Block 4: the press meet and the science

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S098 | 04:56.14 | 290.74 | 2.49 | `tv_flicker.mp4` (``) | zoom 1.15→1.00 | PRESS MEET · MAY 2010 (lower) |  |
| S099 | 04:58.63 | 293.23 | 2.49 | `headline_wikipedia.jpg` (``) | pan R→L | WIKIPEDIA (tag) |  |
| S100 | 05:01.12 | 295.71 | 2.49 | `tv_flicker.mp4` (``) | zoom 1.00→1.15 |  |  |
| S101 | 05:03.61 | 298.20 | 3.30 | `incense.mp4` (``) | pan L→R | HYPOMETABOLISM (lower) | sfx_bass_hit.wav@0.0 |
| S102 | 05:06.91 | 301.50 | 3.30 | `earth_window.mp4` (``) | zoom 1.15→1.00 |  |  |
| S103 | 05:10.21 | 304.80 | 3.30 | `ecg_photo.jpg` (``) | pan R→L |  |  |
| S104 | 05:13.51 | 308.10 | 2.96 | `lab_microscope.mp4` (``) | zoom 1.00→1.15 |  |  |
| S105 | 05:16.47 | 311.06 | 2.96 | `lab_cellplate.mp4` (``) | pan L→R | AUTOPHAGY (lower) |  |
| S106 | 05:19.43 | 314.02 | 2.96 | `lab_hood.mp4` (``) | zoom 1.15→1.00 |  |  |
| S107 | 05:22.39 | 316.97 | 2.96 | `lab_microscope.mp4` (``) | pan R→L |  |  |
| S108 | 05:25.35 | 319.93 | 2.96 | `lab_tubes.mp4` (``) | zoom 1.00→1.15 |  |  |
| S109 | 05:28.31 | 322.89 | 3.18 | `yogi_gouache.jpg` (``) | pan L→R | GOUACHE · WELLCOME COLLECTION (tag) |  |
| S110 | 05:31.49 | 326.07 | 3.18 | `incense.mp4` (``) | zoom 1.15→1.00 |  |  |
| S111 | 05:34.67 | 329.25 | 3.18 | `ambaji_gabbar.jpg` (``) | pan R→L | GABBAR HILL, AMBAJI (tag) |  |
| S112 | 05:37.85 | 332.42 | 3.18 | `himalaya_leh.jpg` (``) | zoom 1.00→1.15 |  |  |

> **🎬 LIVE CLIP 05:41.03 (16.3 s)**: VO stops at 335.6 s; `skeptic_view.mp4` plays 7.0–23.3 s **with its own audio**, then the VO continues. Caption: కొన్ని నిజాలు ఎలాంటి సందేహం లేకుండా నిరూపితమయ్యాయి. | మనతో సహా ప్రతి జీవికి బ్రతకడానికి క్రమం తప్పకుండా ఆహారం, నీరు అవసరం. | దీనికి మినహాయింపులు లేవు. ఒక్కటి కూడా లేదు.. Real CC BY clip: the skeptics' view. Telugu translation in subtitle

| S114 | 05:57.33 | 335.60 | 2.77 | `earth_window.mp4` (``) | zoom 1.15→1.00 |  |  |
| S115 | 06:00.10 | 338.37 | 2.77 | `earth_india.mp4` (``) | pan R→L | NASA (tag) |  |
| S116 | 06:02.87 | 341.14 | 2.77 | `jani_portrait_red.jpg` (``) | zoom 1.00→1.15 | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) |  |
| S117 | 06:05.64 | 343.91 | 2.77 | `himalaya_leh.jpg` (``) | pan L→R |  |  |

## Outro: your opinion + subscribe

| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |
|---|---|---|---|---|---|---|---|
| S118 | 06:08.41 | 346.68 | 3.13 | `jani_portrait_red.jpg` (``) | zoom 1.15→1.00 | PHOTO: VIA RATIONALIST INTERNATIONAL (tag) | End-screen area: calm B-roll |
| S119 | 06:11.54 | 349.81 | 3.13 | `incense.mp4` (``) | pan R→L |  |  |
| S120 | 06:14.67 | 352.93 | 3.13 | `earth_orbit2.mp4` (``) | zoom 1.00→1.15 |  |  |
| S121 | 06:17.80 | 356.06 | 3.13 | `jani_ashram_ambaji.jpg` (``) | pan L→R | AMBAJI, GUJARAT (tag) |  |
| S122 | 06:20.93 | 359.18 | 3.13 | `earth_desert_orbit.mp4` (``) | zoom 1.15→1.00 |  |  |
| S123 | 06:24.06 | 362.31 | 3.13 | `earth_sunrise.mp4` (``) | pan R→L |  |  |
| S124 | 06:27.19 | 365.43 | 3.13 | `earth_india.mp4` (``) | zoom 1.00→1.15 | NASA (tag) |  |

**Programme length with every clip: 06:30.32** (121 shots, 1 live clips, 2 VO pauses).


## Audio cue sheet
| Element | Level | Notes |
|---|---|---|
| Voiceover (`voiceover.mp3`) | lead, normalised with the mix to −14 LUFS / −1 dBTP | Removes the duplicate line at VO 221.40–223.40 |
| BGM (`bgm_dark.mp3`) | −20 dB, side-chain ducked (ratio 6, release 400 ms) | Swells up in each pause |
| SFX | −8 dB, 3 s max with 0.3 s fade | Placed from the `sfx` column (`file@seconds-into-shot`) |
| Pause audio | 0 dB | Real recordings only. Pause 3 must be the real Dr. Shah clip; if none exists, use monitor beeps |
