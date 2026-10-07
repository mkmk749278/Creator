// Edit decision list v4: the owner's new 4-block ElevenLabs voiceover + real event footage.
// Times are VOICEOVER seconds in runs/breath-hold/v2voice/voiceover_v2.wav (blocks joined with
// 0.6 s gaps: block 2 starts 120.16, block 3 204.72, block 4 302.39). See sentences_v2.tsv.
// Each beat is cut into 2.5–3.5 s shots cycling through its pool (registry.json names).
// Text rule: lower-thirds of at most 4 words; no slides, no lists, no blank backgrounds.

export const voice = "runs/breath-hold/v2voice/voiceover_v2.wav";
export const outDir = "runs/breath-hold/doc_v4";

export const beats = [
  // ── BLOCK 1: the impossible feat ──────────────────────────────── 0 – 119.56
  { from: 0.0, to: 5.62, pool: ["brand_banner"], move: "in" },                         // "welcome to Be Practical with Kishore"
  { from: 5.62, to: 27.53, pool: ["freediver_pool", "stopwatch", "freediver_pool", "anatomy_lungs"] },
  { from: 27.53, to: 32.8, pool: ["vidyut_stage_trance"] },                             // "look at this live clip"
  { from: 32.8, to: 45.19, pool: ["vidyut_stage_trance", "vidyut_event_photo", "vidyut_stage_trance"] },
  { from: 45.19, to: 49.5, pool: ["vidyut_stage_trance"] },                             // "stood like a statue"
  { from: 49.5, to: 53.04, pool: ["sf_dhalsim"] },                                      // "...Dhalsim"
  { from: 53.04, to: 68.12, pool: ["vidyut_tears_macro"], move: "push" },               // red eyes, open eyes, tears
  { from: 68.12, to: 81.72, pool: ["vidyut_stage_trance", "vidyut_event_photo", "vidyut_stage_trance"] },
  { from: 81.72, to: 87.5, pool: ["press_crowd", "vidyut_stage_trance"] },              // audience, press go blank
  { from: 87.5, to: 94.72, pool: ["vidyut_shivering"] },                                // minute 14: legs
  { from: 94.72, to: 103.63, pool: ["vidyut_tears_macro", "vidyut_stage_trance", "vidyut_tears_macro"] },
  { from: 103.63, to: 106.6, pool: ["vidyut_shankha_photo"], move: "face" },                                // conch
  { pause: 106.6, len: 3.0, pool: ["vidyut_shankha_photo"], move: "in", live: "vidyut_shankha" },        // voice silent, real conch
  { from: 106.6, to: 110.21, pool: ["press_crowd", "vidyut_stage_trance"] },            // pin-drop silent
  { from: 110.21, to: 120.16, pool: ["vidyut_tears_macro", "vidyut_stage_trance", "vidyut_tears_macro"] },

  // ── BLOCK 2: the science ──────────────────────────────────────── 120.16 – 204.12
  { from: 120.16, to: 131.88, pool: ["freediver_pool", "anatomy_lungs"] },
  { from: 131.88, to: 147.72, pool: ["micro_blood", "anatomy_lungs", "anatomy_brain"] },
  { from: 147.72, to: 161.32, pool: ["anatomy_brain", "anatomy_carotid", "anatomy_diaphragm"] },
  { from: 161.32, to: 171.78, pool: ["vidyut_shivering", "anatomy_diaphragm", "vidyut_tears_macro"] },
  { from: 171.78, to: 192.72, split: ["freediver_pool", "o2_mask_breathing"],
    tags: [{ big: "11:35", small: "Normal air" }, { big: "24:37", small: "Pure O₂ first" }] },
  { from: 192.72, to: 204.72, pool: ["vidyut_stage_trance", "vidyut_event_photo"] },  // "live stage, no oxygen"

  // ── BLOCK 3: the yogic blueprint ─────────────────────────────── 204.72 – 301.79
  { from: 204.72, to: 216.74, pool: ["patanjali_manuscript", "yogi_painting", "yogi_photo"] },
  { from: 216.74, to: 234.25, pool: ["vidyut_tears_macro", "candle", "vidyut_tears_macro", "candle"] },  // Trataka = the red eyes
  { from: 234.25, to: 240.83, pool: ["yogi_photo", "candle"] },
  { from: 240.83, to: 257.31, pool: ["yogi_painting", "patanjali_manuscript", "yogi_photo", "yogi_painting"] },
  { from: 257.31, to: 273.25, pool: ["anatomy_heart", "vidyut_stage_trance", "anatomy_heart"] },
  { from: 273.25, to: 286.52, pool: ["vidyut_tears_macro", "vidyut_stage_trance"] },
  { from: 286.52, to: 298.78, pool: ["sadhu_haridas_1837", "ranjit_court", "haridas_book"], move: "pan" },
  { from: 298.78, to: 302.39, pool: ["vidyut_stage_trance"] },

  // ── BLOCK 4: 35 years, the message, outro ───────────────────── 302.39 – 421.95
  { from: 302.39, to: 313.3, pool: ["vidyut_event_photo", "vidyut_portrait", "vidyut_event_photo"] },
  { from: 313.3, to: 343.5, pool: ["vidyut_kalari", "vidyut_workouts", "kalari", "vidyut_kalari"] },
  { from: 343.5, to: 355.02, pool: ["vidyut_portrait", "vidyut_event_photo", "kalari"] },
  { from: 355.02, to: 360.3, pool: ["sf_title", "sf_dhalsim"] },                         // Street Fighter / Dhalsim
  { from: 360.3, to: 366.31, pool: ["vidyut_stage_trance", "vidyut_shankha_photo"] },         // "...conch-blowing Vidyut"
  { from: 366.31, to: 380.14, pool: ["city_rush_timelapse", "mumbai"] },
  { pause: 380.14, len: 3.0, pool: ["vidyut_stage_trance"] },                           // quote card pause
  { from: 380.14, to: 392.63, pool: ["city_rush_timelapse", "vidyut_stage_trance", "city_rush_timelapse", "vidyut_tears_macro"] },
  { from: 392.63, to: 405.67, pool: ["vidyut_stage_trance", "vidyut_event_photo", "sf_dhalsim"] },
  { from: 405.67, to: 418.12, pool: ["vidyut_event_photo", "sf_release", "vidyut_stage_trance"] },
  { from: 418.12, to: 421.95, pool: ["vidyut_stage_trance"], end: true },
  { pause: 421.95, len: 5.0, pool: ["vidyut_stage_trance"], end: true },               // end-screen tail
];

// Lower-thirds (≤ 4 words). `at` in voice time; `pause: true` puts it inside the pause at `at`.
export const lowerThirds = [
  { at: 27.8, dur: 4.6, text: "16 minutes motionless | Mumbai" },
  { at: 33.2, dur: 4.5, text: "Vidyut Jammwal | Street Fighter" },
  { at: 49.7, dur: 3.2, text: "Dhalsim" },
  { at: 87.7, dur: 4.0, text: "Minute 14 | Tremors" },
  { at: 153.7, dur: 5.0, text: "Hypercapnic reflex | CO₂ vs O₂" },
  { at: 216.9, dur: 4.5, text: "Trataka | Unblinking gaze" },
  { at: 241.0, dur: 5.5, text: "Kevala Kumbhaka | Spontaneous cessation" },
  { at: 281.3, dur: 4.0, text: "Micro-ventilation?" },
  { at: 286.8, dur: 5.0, text: "Sadhu Haridas | Lahore 1837" },
  { at: 319.4, dur: 5.0, text: "35 years | Kalaripayattu" },
  { at: 355.3, dur: 4.6, text: "Street Fighter | In cinemas Oct 16" },
  { at: 380.14, pause: true, dur: 3.0, text: "In a world of rushing, stillness is power.", wide: true },
];

// Corner timer (voice time): stopwatch through the opening, then the hold clock.
export const timer = {
  keys: [[0, 0], [5.6, 0], [8.4, 30], [9.8, 60], [11.6, 120], [17.2, 180], [22.4, 360], [27.4, 360], [27.45, 0],
         [68.1, 0], [68.5, 120], [77.6, 480], [79.0, 600], [80.5, 720], [87.6, 840], [99.6, 960], [110.0, 960]],
  windows: [[5.7, 27.4], [68.2, 106.6]],
  alarm: [[87.6, 99.6]],
};

// Part boundaries (voice time, each must be a beat edge)
export const parts = [0, 68.12, 120.16, 171.78, 204.72, 257.31, 302.39, 355.02];
