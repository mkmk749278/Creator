// Parameters for the whiteboard scene (PLAYBOOK §9.1). Coordinates are 1920×1080; x/y of text = left end of the baseline
// (or cx = centre). size = capital-letter height in px. at = seconds; omit to follow the previous step (+0.25 s);
// dur fits a step to a VO phrase. Colours: black, blue, red, green, orange, purple or any CSS colour.
window.SCENE = {
  duration: 12,
  seed: 4,
  font: "tech",                      // tech (default marker print), readability, nixish, felix, allure, script, sans
  tag: "OUR CALCULATION · ICICI METHOD, 45% P.A.",
  camera: [{ at: 0, scale: 1.0, x: 0, y: 0 }, { at: 12, scale: 1.05, x: -20, y: 0 }],
  steps: [
    { write: "You paid ₹1,500", x: 230, y: 300, size: 100, color: "green", at: 0.4 },
    { underline: "last", color: "green" },
    { write: "Bank added ₹1,981", x: 230, y: 520, size: 100, color: "red", at: 3.0 },
    { circle: "last", color: "red", at: 5.6 },
    { arrow: [560, 640, 900, 790], color: "black", at: 7.0 },
    { write: "loan went UP", x: 940, y: 830, size: 90, color: "black" },
    { erase: true, at: 10.4, dur: 1.2 },
  ],
};
