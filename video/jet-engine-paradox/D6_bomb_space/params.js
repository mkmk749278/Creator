// D6_bomb_space parameters (scenes.md; fact-checked, do not change). Pulses are abstract: no labels, no borders.
window.SCENE = {
  id: "d6-bomb-space", duration: 5.71,
  nuclear: { n: "9", label: "NUCLEAR-ARMED STATES",
    at: [[39, -98], [58, 60], [53, -2], [46, 2.5], [35, 103], [22, 79], [30, 70], [31, 35], [40, 127]] },   // SIPRI's nine
  orbit: { n: "~10", label: "OWN ROCKET TO ORBIT", count: 10 },
  // VO: "Nine countries have nuclear bombs" 0.15-2.02; "About ten have put a satellite in space..." 2.30-5.55
  t: { nine: 0.35, ten: 2.4, orbits1: 4.6 },
};
