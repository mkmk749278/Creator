# Design reference: what the real things look like

Owner, 2026-10-16: "Before design anything observe the real photos first, accordingly you can make it realistic design."
Every animated scene draws its hardware, trains, signals and track from these photos. They are references for
look; any that go on screen must first be logged in `media_manifest.csv` with their licence. Files are in `assets/ref/`
(gitignored); contact sheets are in `qa/ref/ref1-4.jpg`.

| Element | Reference (assets/ref/) | What to copy |
|---|---|---|
| Kavach cab screen (DMI, "KAVACH LP-OCIP") | `TCAS_DMI_Screenshot.jpg` (labelled), `TCAS_Retrofitted_DMI_P7.jpg`, `TCAS_DMI_VB.jpg` | Black screen in a black bezel with side buttons (C, ◄, ►, ▲, ▼, E / on-off, brightness, F, M) and a 1–0 key row. Screen: round speedometer 0–200 with a **green arc to the permitted speed**, needle and a digital speed in the hub; **yellow target-distance bar** at the left with the metres below (e.g. `1071 m`); **blue movement-authority bar**; a **4-aspect signal icon** (one lamp lit) with an `A` plate for automatic signals and the signal distance (`0533 m`); top: loco number and date/time; `LOC : 1446.36 Km`; a mode line (`DC 0.47 · TL 25 m · Full Supervision Mode`); a **message line** (`TurnOut in 1073m with Speed Limit 30kmph`); RF bars and tag ladder; function keys `P_TRP REV OVRD SHNT MBT SR CONFIG CNFM INFO`. Below the bezel: grey panel with round buttons COMMON, ACK/CANCEL (blue), SOS (red), status LEDs. |
| Loco cab | `assets/pib/pib_1802968_trial_cab.jpg` | Grey steel console with round gauges, small hand wheel, windscreen with **vertical protective bars**, side window, DMI mounted near the window. |
| Loco Kavach unit | `TCAS_Loco_Computer.jpg` | Light-grey steel box, card rack visible through the front, red **INDIAN RAILWAY PROPERTY** plate. |
| Station Kavach unit | `TCAS_Stationary_Master_Computer.jpg` | Tall light-grey cabinet with four lifting eyes, card racks, same red plate. |
| Remote interface unit | `TCAS_RIU.jpg` | Grey box with a glass window and handle. |
| Station panel (SM-OCIP) | `TCAS_SMOCIP.jpg` | Blue rack panel, green LCD, SM key, SOS / health lamps, round buttons. |
| RFID tag | `TCAS_RFID_Tag.jpg` | Grey metal/FRP enclosure, rounded corners, yellow triangle, printed `RFID NO-… LOCATION-33.999 KM`, clamped by stainless brackets to the **centre of a grey concrete (PSC) sleeper**; rusty-brown rails with a shiny running top; grey ballast; km post. RDSO TAN 2025: FRP enclosure, Grade 316 stainless clamp. |
| Loco antennas | `TCAS_loco_antennas.png` | Black dome radio/GPS antennas on the roof beside the cooling box. |
| Radio tower | `TCAS_Station_UHF_Radio_Tower.jpg` (when fetched), `TCAS_working_graphical_explanation.jpg` | Lattice tower by the station with antennas; the official diagram: two locos with RFID readers + radio antennas, tower, station TCAS. |
| Colour-light signal (India) | `Railway_Signal_at_Lallaguda.jpg`, `Railway_signal_at_Tiruchirappalli_*`, `Railway_Signal_Post_at_Safilguda.jpg`, `View_of_signal_post_from_Padmavathi_Express.jpg` | Black rectangular backplate, 3–4 lamps stacked vertically, each with a **hood**; white/silver post with a ladder; number plate below the head (`S4`); **automatic signals carry a white disc with a black `A`**; junction feathers on top. |
| Freight | `WAG9_LGD_130418.jpg`, `WAG-9_Hauled_Goods_Train_at_Kelve_Rd_station.jpg` | WAG-9 in green with yellow bands (also red/white/blue liveries); BOXN open wagons, blue or brown. |
| Vande Bharat | `Vande_Bharat_Express_train.jpg` | White body with blue window band (newer: saffron and grey), aerodynamic nose. |
| LHB coaches (Coromandel) | `LHB_coaches_3.jpg`, wreck photos | Red and grey LHB coaches. |
| Electric loco (WAP-4/WAP-7) | `Indian_railway_loco_pilot_signalling.JPG` | Cream body with an orange-red band, "भारतीय रेल". |
| Balasore layout | `Odisha_crash.png` (Commons, after CRS) | Four lines: down loop (goods train), down main (SMVT Bengaluru–Howrah), up main, up loop (goods train). Coromandel on the up main turned into the up loop; its coaches fouled the down main and hit the Bengaluru–Howrah express. |
