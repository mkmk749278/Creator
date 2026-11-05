// Proof beat (Minimum Amount Due, line 2.03): every ₹100 paid on a minimum-only card splits ₹74 interest + GST / ₹26 loan
// (projects/minimum-due/tools/mad_math.py). Bill rows: our ₹30,000 example, 25 Nov bill (README research record).
window.SCENE = {
  duration: 8,
  kicker: "MINIMUM ONLY · EVERY MONTH",
  title: "Every ₹100 you pay",
  tag: "ILLUSTRATION · OUR CALCULATION",
  billNote: "SIMULATION · OUR EXAMPLE",
  billRows: [["Previous bill", "₹30,000.00"], ["You paid (minimum)", "−₹1,500.00"], ["Interest", "+₹1,679.18", true], ["GST 18% on interest", "+₹302.25", true]],
  billTotal: "₹30,481.43",
  phoneAmount: "₹100", phoneLine1: "Paid to card bill", phoneLine2: "PAYMENT SUCCESSFUL",
  cardInterest: ["INTEREST + GST", "₹74"], cardLoan: ["YOUR LOAN", "₹26"],
  interestCoins: 74,
  tInt: 1.7, intSpan: 2.3, tLoan: 4.25, loanSpan: 0.8, flight: 0.6, tCardInt: 1.3, tCardLoan: 3.95,
  camera: [
    { t: 0, pos: [0.55, 1.75, 3.9], look: [-0.1, 0.05, 0.3] },
    { t: 3.4, pos: [0.15, 1.45, 3.45], look: [-0.15, 0.1, 0.55] },
    { t: 8, pos: [-0.05, 1.2, 3.1], look: [-0.2, 0.14, 0.68] },
  ],
};
