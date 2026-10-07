# Step 1: asset manifest and download checklist

Prahlad Jani & DRDO (Telugu, VO 4:44). Download everything into `projects/prahlad-jani-drdo/assets/` using exactly
these file names; `assemble.py` and `edl.csv` look for them. Log the URL, owner and licence of each file in
`media_manifest.csv`. ★ = must-have; the cut falls back to the alternative named in the EDL if it is missing.

| Asset ID | File Name | Description | Source Platform | Exact Search Query |
| :--- | :--- | :--- | :--- | :--- |
| ASSET_01 ★ | `jani_portrait_red.jpg` | Prahlad Jani portrait, red sari, nose ring (hi-res) | Wikimedia Commons | "Prahlad Jani" |
| ASSET_02 ★ | `jani_news_2010.mp4` | 2010 news report: Jani in the Sterling Hospital room | YouTube | "Prahlad Jani 2010 Sterling Hospital Ahmedabad news" |
| ASSET_03 ★ | `jani_ap_archive.mp4` | AP/Reuters raw footage: yogi under observation, 2010 | YouTube (AP Archive) | "AP Archive India yogi no food water 2010" |
| ASSET_04 ★ | `press_conf_shah.mp4` | Press conference: Dr. Sudhir Shah + DIPAS, May 2010 (real audio for the live pause) | YouTube | "Sudhir Shah Prahlad Jani press conference 2010" |
| ASSET_05 | `jani_ashram_ambaji.mp4` | Jani at the Ambaji ashram/cave, devotees | YouTube | "Chunriwala Mataji Ambaji ashram" |
| ASSET_06 | `headlines_2003_2010.png` | Headline crops: BBC 2003, Guardian/BBC 2010, obituary 2020 | News sites (screenshots) | "Prahlad Jani BBC 2010" · "Indian yogi claims no food water" |
| ASSET_07 | `sterling_hospital_ext.jpg` | Sterling Hospital, Ahmedabad exterior | Wikimedia Commons / Google Images (CC filter) | "Sterling Hospital Ahmedabad" |
| ASSET_08 | `drdo_emblem.png` | DRDO emblem / DIPAS signage | drdo.gov.in · Wikimedia Commons | "DRDO logo svg" |
| ASSET_09 | `drdo_lab.mp4` | DRDO lab / scientists at work | YouTube (DRDO official) · PIB | "DRDO laboratory scientists" |
| ASSET_10 ★ | `ecg_monitor.mp4` | ICU heart monitor, beeping ECG trace | Pexels | "heart rate monitor hospital" |
| ASSET_11 | `pulse_oximeter.mp4` | Pulse oximeter on a finger | Pexels | "pulse oximeter finger" |
| ASSET_12 | `blood_sample.mp4` | Blood draw / test tubes | Pexels | "blood sample test tube lab" |
| ASSET_13 ★ | `cctv_camera.mp4` | CCTV dome camera, red LED | Pexels | "cctv security camera close up" |
| ASSET_14 | `hospital_corridor.mp4` | Dim hospital corridor, dolly | Pexels | "hospital corridor night" |
| ASSET_15 | `doctor_scrub.mp4` | Doctor scrubbing in / gloving | Pexels | "doctor washing hands surgery" |
| ASSET_16 | `isolation_door.mp4` | Heavy door closing / lock | Pixabay | "metal door closing lock" |
| ASSET_17 ★ | `cracked_earth.mp4` | Cracked dry earth, heat haze | Pixabay | "drought cracked earth" |
| ASSET_18 | `sweat_macro.mp4` | Macro: sweat and parched lips | Pexels | "dehydrated lips close up" |
| ASSET_19 ★ | `water_drop_macro.mp4` | Water drop slow motion | Pexels | "water drop slow motion macro" |
| ASSET_20 | `water_tap_close.mp4` | Tap/valve being closed | Pexels | "closing water tap valve" |
| ASSET_21 | `beaker_measure.mp4` | Liquid measured in a graduated cylinder | Pexels | "measuring cylinder liquid laboratory" |
| ASSET_22 | `sponge_squeeze.mp4` | Sponge squeezed | Pexels | "squeezing sponge water" |
| ASSET_23 ★ | `siachen_soldiers.mp4` | Indian Army in Siachen snow | YouTube (ADGPI / PIB official) | "Indian Army Siachen glacier soldiers" |
| ASSET_24 | `desert_soldiers.mp4` | Soldiers in the Thar desert | YouTube (ADGPI official) | "Indian Army Thar desert exercise" |
| ASSET_25 ★ | `astronaut_iss.mp4` | Astronaut floating on the ISS | NASA (images.nasa.gov) | "astronaut ISS floating" |
| ASSET_26 | `disaster_rescue.mp4` | Flood/earthquake rescue | Pixabay | "flood rescue" |
| ASSET_27 | `earth_india.mp4` | Earth from orbit over India | NASA | "India from space ISS night" |
| ASSET_28 | `ultrasound_screen.mp4` | Ultrasound machine screen scanning | Pexels | "ultrasound scan screen" |
| ASSET_29 ★ | `cells_micro.mp4` | Microscopic cells flowing | Pixabay | "cells microscope" |
| ASSET_30 | `blood_vessels.mp4` | Blood cells flowing in a vessel | Pixabay | "blood cells vessel" |
| ASSET_31 | `kidney_anatomy.jpg` | Kidney anatomical illustration | Wellcome Collection | "kidney anatomy" |
| ASSET_32 | `bladder_anatomy.jpg` | Urinary bladder illustration | Wellcome Collection | "urinary bladder" |
| ASSET_33 | `meditation_silhouette.mp4` | Yogi meditating at sunrise (not Jani) | Pexels | "meditation silhouette sunrise" |
| ASSET_34 | `clock_macro.mp4` | Clock ticking macro | Pexels | "clock ticking close up" |
| ASSET_35 | `scale_weight.mp4` | Weighing scale reading | Pexels | "weighing scale feet" |
| ASSET_36 | `hud_overlay.mp4` | Medical HUD / data overlay, black bg (Layer 2) | Mixkit · Pixabay | "hud interface overlay black background" |
| ASSET_37 | `film_grain.mp4` | 35 mm grain overlay (Layer 2) | Pixabay | "film grain overlay" |
| ASSET_38 | `light_leak.mp4` | Light leak overlay (Layer 2) | Pixabay | "light leak overlay" |
| AI_P1a–c | `ai_kidney_*.mp4` | Kidney healthy vs. dehydrated | Runway / Sora | see `3d-prompts.md` P1 |
| AI_P2a–c | `ai_room_*.mp4` | Sealed-room wireframe, CCTV, valve | Runway / Sora | P2 |
| AI_P3a–c | `ai_bladder_*.mp4` | Bladder, illustrative sonography, reabsorption | Runway / Sora | P3 |
| AI_P5a | `ai_beaker.mp4` | Syringe into beaker, macro | Runway / Sora | P5 |
| AUD_01 ★ | `bgm_dark.mp3` | Dark investigative ambient pad | YouTube Audio Library | "ambient dark cinematic" |
| AUD_02 ★ | `sfx_heartbeat_monitor.wav` | Monitor beeps | Pixabay SFX | "heart monitor beep" |
| AUD_03 | `sfx_flatline.wav` | Flatline | Pixabay SFX | "flatline" |
| AUD_04 | `sfx_clock.wav` | Clock tick | Pixabay SFX | "clock ticking" |
| AUD_05 | `sfx_door_latch.wav` | Heavy door latch | Pixabay SFX | "heavy door close latch" |
| AUD_06 | `sfx_whoosh.wav` | Transition whoosh | Pixabay SFX | "cinematic whoosh" |
| AUD_07 | `sfx_bass_hit.wav` | Low bass impact | Pixabay SFX | "cinematic boom impact" |
| AUD_08 | `sfx_cctv_hum.wav` | Electrical hum / camera servo | Freesound (CC0) | "electrical hum" |

yt-dlp (VPS/Termux): `yt-dlp -f "bv*[height<=2160]+ba/b" --merge-output-format mp4 -o assets/<File Name> "<url>"`.
Trim to the needed seconds before committing anything; `assets/` is gitignored.

## D. Fact-check before publishing (important)

From memory, so verify each point against a collected source before it goes on screen:

1. **Dates:** the 2010 observation ran about 22 Apr to 6 May 2010 (15 days) at Sterling Hospital, Ahmedabad, with
   DIPAS (DRDO). An earlier 10-day study was in 2003. Jani died on 26 May 2020.
2. **Criticism exists and should be in the video:** reports said he was allowed out of the sealed room to sunbathe
   and meet devotees, and was allowed to gargle and bathe. Rationalists (for example Sanal Edamaruku) called the
   study unscientific. **No peer-reviewed paper was ever published**, and DRDO never released final results.
3. **Autophagy** (Nobel Prize 2016, Yoshinori Ohsumi) recycles cell components during fasting. It **does not
   produce water** and cannot explain surviving 15 days without fluids. Present it as "what science knows about
   fasting", not as the explanation.
4. **"No water for 70 years"** is Jani's claim, not a finding. Mainstream medicine says it is not physiologically
   possible. Phrase on-screen text as a claim ("he claimed", "doctors reported").

A video that presents the claim as proven risks YouTube's medical-misinformation policy and could encourage
viewers to try dry fasting, which is dangerous. Add one 6–10 s "what skeptics say" beat to the part-2 VO (after the bladder segment) and a
short on-screen safety note in the outro: "Do not attempt prolonged fasting without water."
