// Edit decision list for the breath-hold documentary (v3, documentary engine).
// Times are VOICEOVER seconds (runs/breath-hold/transcript/sentences_*.tsv); build.mjs
// shifts them past the live pauses. Each beat is cut into shots of 2.5–3.5 s, cycling
// through its pool. Pool entries are logical asset names resolved by registry.json:
// the owner's ./assets/ file first, licensed fallbacks after.
// Text rule: lower-thirds of at most 4 words; no slides, no lists, no blank backgrounds.

export const beats = [
  // ── SCENE 1: THE IMPOSSIBLE FEAT ─────────────────────────────── voice 0 – 135.75
  { from: 0.0, to: 23.0, pool: ["freediver_pool", "stopwatch", "freediver_pool", "anatomy_lungs"] },
  { from: 23.0, to: 35.3, pool: ["vidyut_stage_trance"], move: "in" },
  { from: 35.3, to: 42.4, pool: ["vidyut_tears_macro", "vidyut_shivering", "vidyut_tears_macro"] },
  { from: 42.4, to: 56.2, pool: ["vidyut_stage_trance", "press_crowd", "vidyut_stage_trance"] },
  { from: 56.2, to: 66.5, pool: ["mumbai", "vidyut_stage_trance", "vidyut_portrait"] },
  { from: 66.5, to: 80.2, pool: ["vidyut_portrait", "vidyut_stage_trance"] },
  // the hold: 2 → 12 minutes, then the eyes, then the tremor
  { from: 80.2, to: 97.8, pool: ["vidyut_stage_trance"], move: "in" },
  { from: 97.8, to: 110.3, pool: ["vidyut_tears_macro"], move: "face" },
  { from: 110.3, to: 123.77, pool: ["vidyut_shivering"] },
  { from: 123.77, to: 127.0, pool: ["vidyut_shankha"] },
  { pause: 127.0, len: 3.0, pool: ["vidyut_shankha"], live: "vidyut_shankha" },  // voice silent, live conch audio
  { from: 127.0, to: 135.75, pool: ["press_crowd", "vidyut_stage_trance", "vidyut_tears_macro"] },

  // ── SCENE 2: THE SCIENCE ─────────────────────────────────────── voice 135.75 – 215.5
  { from: 135.75, to: 149.2, pool: ["freediver_pool", "anatomy_lungs", "micro_blood"] },
  { from: 149.2, to: 158.1, pool: ["micro_blood", "anatomy_lungs"] },
  { from: 158.1, to: 171.1, pool: ["anatomy_brain", "anatomy_carotid", "anatomy_brain"] },
  { from: 171.1, to: 186.3, pool: ["anatomy_diaphragm", "vidyut_shivering", "anatomy_diaphragm"] },
  { from: 186.3, to: 207.0, split: ["freediver_pool", "o2_mask_breathing"],
    tags: [{ big: "11:35", small: "Normal air" }, { big: "24:37", small: "Pure O₂ first" }] },
  { from: 207.0, to: 215.5, pool: ["vidyut_stage_trance"], move: "out" },

  // ── SCENE 3: THE YOGIC BLUEPRINT ─────────────────────────────── voice 215.5 – 310.2
  { from: 215.5, to: 230.0, pool: ["patanjali_manuscript", "yogi_painting", "patanjali_manuscript"] },
  { from: 230.0, to: 247.6, pool: ["candle", "vidyut_tears_macro", "yogi_painting", "anatomy_brain"] },
  { from: 247.6, to: 265.0, pool: ["patanjali_manuscript", "yogi_painting", "patanjali_manuscript"] },
  { from: 265.0, to: 281.0, pool: ["anatomy_heart", "vidyut_tears_macro", "anatomy_heart"] },
  { from: 281.0, to: 291.6, pool: ["vidyut_tears_macro"], move: "face" },
  { from: 291.6, to: 307.1, pool: ["sadhu_haridas_1837", "ranjit_court", "haridas_book"], move: "pan" },
  { from: 307.1, to: 310.2, pool: ["vidyut_tears_macro"], move: "face" },

  // ── SCENE 4: 35 YEARS OF DISCIPLINE & THE MESSAGE ──────────── voice 310.2 – end
  { from: 310.2, to: 321.0, pool: ["vidyut_portrait", "vidyut_kalari"] },
  { from: 321.0, to: 362.6, pool: ["vidyut_kalari", "vidyut_workouts", "kalari", "vidyut_kalari", "vidyut_workouts"] },
  { from: 362.6, to: 376.1, pool: ["vidyut_stage_trance", "vidyut_portrait"] },
  { from: 376.1, to: 386.5, pool: ["city_rush_timelapse", "mumbai"] },
  { pause: 386.5, len: 3.0, pool: ["vidyut_stage_trance"] },
  { from: 386.5, to: 400.9, pool: ["city_rush_timelapse", "vidyut_stage_trance", "city_rush_timelapse", "vidyut_stage_trance"] },
  { from: 400.9, to: 417.5, pool: ["vidyut_kalari", "vidyut_portrait", "vidyut_stage_trance"] },
  { from: 417.5, to: 424.96, pool: ["vidyut_stage_trance", "vidyut_kalari"], end: true },
  { pause: 424.96, len: 5.0, pool: ["vidyut_stage_trance"], end: true },  // end-screen tail
];

// Lower-thirds (≤ 4 words). `at` in voice time; `pause: true` puts it inside the pause at `at`.
export const lowerThirds = [
  { at: 23.4, dur: 5.5, text: "16 minutes motionless | Mumbai" },
  { at: 56.6, dur: 4.5, text: "Vidyut Jammwal | Street Fighter" },
  { at: 80.6, dur: 4.0, text: "No visible breathing" },
  { at: 110.5, dur: 4.0, text: "Minute 14 | Tremors" },
  { at: 164.8, dur: 5.0, text: "Hypercapnic reflex | CO₂ vs O₂" },
  { at: 230.2, dur: 4.5, text: "Trataka | Unblinking gaze" },
  { at: 250.9, dur: 5.5, text: "Kevala Kumbhaka | Spontaneous cessation" },
  { at: 281.2, dur: 4.0, text: "Micro-ventilation?" },
  { at: 294.8, dur: 5.0, text: "Sadhu Haridas | Lahore 1837" },
  { at: 327.4, dur: 5.0, text: "35 years | Kalaripayattu" },
  { at: 386.5, pause: true, dur: 3.0, text: "In a world of rushing, stillness is power.", wide: true },
];

// Corner timer (voice time): stopwatch through the opening, then the hold clock.
export const timer = {
  keys: [[0, 0], [4.0, 60], [9.0, 120], [12.6, 180], [18.1, 360], [23.0, 360], [34.0, 960], [80.19, 960],
         [80.2, 120], [80.6, 120], [86.5, 300], [94.0, 480], [95.1, 600], [96.4, 720], [110.3, 840], [118.9, 960], [140, 960]],
  windows: [[0.3, 34.8], [80.4, 127.0]],
  alarm: [[110.3, 118.9]],
};

// Part boundaries (voice time, each must be a beat edge)
export const parts = [0, 80.2, 135.75, 186.3, 215.5, 265.0, 310.2, 362.6];
