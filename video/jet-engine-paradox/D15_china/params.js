// D15_china parameters (scenes.md; fact-checked, do not change).
// photo: path (relative to this folder) of the J-20 photo; empty = neutral "PHOTO SLOT" placeholder plate.
// The coordinator drops the licensed photo in (e.g. "assets/j20.jpg") and logs it; it is shown with a slow push-in.
window.SCENE = {
  id: "d15-china", duration: 10.49,
  photo: "assets/j20.jpg",       // J-20 at CCAS 2022, N509FZ, CC BY-SA 4.0 (Wikimedia Commons); credit drawn by the assembler
  focus: [0.42, 0.42],            // photo point the push-in drifts toward (0..1)
  lead: "J-20:",
  chips: ["RUSSIAN AL-31F", "CHINESE WS-10C", "WS-15"],
  // VO: "used Russian engines at first" ~4.0; "decades, and many failures" 5.79-8.55; "engines of its own" 8.71-10.30
  t: { lead: 0.4, rail0: 0.6, c0: 3.9, decades0: 5.8, c1: 8.8, c2: 9.6 },
};
