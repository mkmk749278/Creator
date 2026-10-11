// Minimum Amount Due, style sample (VO block 1, 192.6–212.6 s). Real clips cover 0–3.0, 9.6–12.0 and 17.0–20.
window.SCENE = {
  duration: 20, seed: 11, font: "tech",
  tag: "OUR CALCULATION · ICICI METHOD, 45% P.A.",
  camera: [{ at: 0, scale: 1.0, x: 0, y: 0 }, { at: 9.6, scale: 1.04, x: 10, y: 6 }, { at: 12, scale: 1.0, x: 0, y: 0 }, { at: 17, scale: 1.05, x: -24, y: 0 }],
  steps: [
    { write: "You paid ₹1,500", x: 230, y: 330, size: 120, color: "green", at: 3.2, dur: 1.9 },
    { underline: "last", color: "green", at: 5.15, dur: 0.35 },
    { write: "Bank added ₹1,981", x: 230, y: 600, size: 120, color: "red", at: 5.8, dur: 2.7 },
    { circle: "last", color: "red", at: 8.6, dur: 0.7 },
    { erase: true, at: 9.75, dur: 1.4 },                      // under the real cutaway
    { write: "₹30,000", x: 230, y: 380, size: 150, color: "black", at: 12.2, dur: 1.3 },
    { arrow: [700, 430, 880, 610], color: "red", at: 13.6, dur: 0.45 },
    { write: "₹30,481", x: 920, y: 700, size: 150, color: "red", at: 14.15, dur: 1.5 },
    { underline: "last", color: "red", at: 15.75, dur: 0.4 },
  ],
};
