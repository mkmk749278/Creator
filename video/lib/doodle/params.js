// Proof beat (Minimum Amount Due, line 2.03): every ₹100 paid on a minimum-only card = ₹74 interest + GST, ₹26 loan
// (projects/minimum-due/tools/mad_math.py). sfx: [time, sound] pairs mixed by the assembly (sounds in sfx/).
window.SCENE = {
  duration: 10,
  head: "Every ₹100 you pay",
  sackAmt: "₹74", sackLbl: "INTEREST + GST",
  jarAmt: "₹26", jarLbl: "YOUR LOAN",
  tag: "ILLUSTRATION · OUR CALCULATION, 45% A YEAR",
  t: { head: 0.3, note: 1.0, tear: 2.6, sack: 3.0, sackLbl: 3.5, dropL: 3.9, jar: 5.3, jarLbl: 5.8, dropR: 6.2, loop: 7.6 },
  sfx: [[0.3, "whoosh"], [1.0, "scribble"], [2.6, "rip"], [3.0, "pop"], [3.9, "whoosh"], [4.55, "thud"], [5.3, "pop"], [6.2, "whoosh"], [6.85, "clink"], [7.6, "squeak"]],
};
