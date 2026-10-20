# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

Storyboard and screenplay (Block 3). Times are estimates at 150 words a minute (VO v5: answers the viewer's three questions with the real two-layer mechanism, owner 2026-10-20); re-time from `align/` once the VO is
recorded. Each row is one visual state (2.5–4.5 s) and changes **one** thing from the row before (angle, geometry or
state). `[B]` = Blender Cycles hero shot, `[3]` = Three.js, `[H]` = HyperFrames 2D, `[R]` = real footage. Stand-ins
carry ILLUSTRATIVE FOOTAGE; every model carries ILLUSTRATION. Cite tags bottom right.

**The model (designed from real reference photos first, PLAYBOOK §9.2): a two-deck cutaway.** Upper deck, the
**MESSAGE LAYER**: three machines (YOUR BANK · NPCI SWITCH · SHOP'S BANK) joined by glass fibre; cyan light pulses
race along it, and a 15-second ring sits on the switch. Lower deck, the **MONEY LAYER**: under each bank a vault room;
money waits on a belt as amber crates, and every two hours a "batch" shuttle carries them to a central hub labelled
**RBI SETTLEMENT ACCOUNTS** (ILLUSTRATION). A clock on the hub shows the next batch. The app's three words sit on a
status board on the switch: SUCCESS (green), FAILED (orange), PROCESSING (amber, blinking). At the shop's bank, a
ledger with two rubber stamps: **TCC · CREDITED** and **RET · RETURN**. References to collect: data-centre racks, a
bank vault room, an RTGS/RBI building exterior (real photo for the hub), a kirana counter, a UPI QR standee and
soundbox, the RBI circular table, NPCI circular pages (15 seconds; settlement cycles table).

| Time | Phase | AUDIO (VO) | VISUAL + ACTION | HUD | SFX / music |
|---|---|---|---|---|---|
| 0:00 | Hook | "Your phone says debited. The shop says nothing came." | `[R]` Tight on a phone at a kirana counter: ₹840 DEBITED (our own simulated screen, no real app brand); cut to the soundbox, light off. ILLUSTRATIVE FOOTAGE. | BALANCE ₹4,400 (amber) | Buzz, then silence |
| 0:04 | Hook | "So where is your eight hundred and forty rupees right now?" | `[H]` ₹840 lifts off the phone as an amber crate; a question-free tracking reticle locks onto it (label: WHERE?). | MONEY AT ? | Reticle beep |
| 0:08 | Hook | "It isn't lost. It's sitting in one bank's account." | `[B]` Wide hero, two-deck cutaway; the crate rests in a vault under one of the banks, which one is hidden in shadow. ILLUSTRATION. | — | Low drone |
| 0:12 | Hook | "I'll show you which one, when it comes back, and the one mistake that makes you pay twice." | `[H]` Three small chips slide in on the lower third: WHICH BANK · WHEN · PAY TWICE? (3 words max each), then fade. | — | Three ticks |
| 0:19 | Mechanism | "Let me tell you the secret. U.P.I. runs on two layers." | `[B]` Same wide, the two decks light up in turn; labels MESSAGE LAYER (top), MONEY LAYER (bottom). | — | Two hits |
| 0:23 | Mechanism | "The first layer only moves messages, and every bank gets fifteen seconds to reply." | `[B]` Upper deck: cyan pulses race between the three machines; the 15-second ring on the switch. 1 s insert: NPCI circular, "15 seconds". Cite `[NPCI UPI CIRCULAR \| 2026]`. | LEG TIMER 15.0 (limit) | Fast data ticks |
| 0:29 | Mechanism | "The second layer moves the actual money, later, in batches." | `[B]` Tilt down to the lower deck: amber crates queue on belts under each bank. | — | Heavy belt hum |
| 0:32 | Mechanism | "Ten times a day, banks settle up through their accounts at the R.B.I." | `[B]` A batch shuttle leaves for the RBI SETTLEMENT ACCOUNTS hub; the hub clock jumps two hours; `[R]` 1 s insert: NPCI settlement-cycle table, magnifier on cycles 1–10. Cite `[NPCI UPI CIRCULAR \| 2026]`. | NEXT BATCH 01:52:00 · 10 BATCHES / DAY | Shuttle whoosh |
| 0:38 | Mechanism | "So the word your app shows is only about the messages. Makes sense?" | `[H]` Same frame: the switch's status board glows on the upper deck only; the lower deck dims. | STATUS ? | — |
| 0:43 | Success | "Success means both banks replied." | `[B]` Upper deck: pulse out and back from both banks; SUCCESS lamp green. | STATUS SUCCESS ✓ | Chime |
| 0:46 | Failed | "Failed means it broke early — your money never left, or your bank sends it back. Failed is safe to try again." | `[B]` Pulse dies before your bank; FAILED lamp orange; the crate never leaves your vault (or slides straight back). `[R]` Phone: FAILED · Kindly Try Again. Cite `[NPCI UPI HELP \| 2023]`. | STATUS FAILED · BALANCE ₹5,240 | Short buzz, tap |
| 0:54 | Processing | "Now the big one... processing." | `[B]` Push in on the board: PROCESSING lamp blinks amber; everything else dims. | STATUS PROCESSING | Music drops |
| 0:56 | Processing | "Your bank replied, done. But the shop's bank went silent." | `[B]` Upper deck: your bank's pulse returns green; the pulse to the shop's bank goes out and nothing comes back. | DEBIT LEG DONE ✓ · CREDIT LEG NO REPLY | Silence (1.5 s) |
| 1:00 | Processing | "After fifteen seconds, N.P.C.I. stops waiting, and here's the catch — it marks your payment deemed approved. Approved for now, checked later." | `[B]` The 15-second ring completes in orange; a stamp DEEMED APPROVED lands on the message. Cite `[NPCI OC 213 \| 2025]`. | LEG TIMER 15.0 TIMEOUT · CREDIT LEG DEEMED | Thud (reveal) |
| 1:09 | Money | "So in the next money batch, your eight hundred and forty rupees really moves to the shop's bank." | `[B]` Lower deck: your crate rides the batch shuttle via the RBI hub into the SHOP'S BANK vault. Cite `[NPCI UPI GLOBAL QR RULES \| 2024]`. | MONEY AT SHOP'S BANK | Shuttle, clunk |
| 1:15 | Money | "That's where your money is right now." | `[B]` Reticle from 0:04 snaps onto the crate in the shop's bank vault. | MONEY AT SHOP'S BANK (locked) | Reticle lock |
| 1:19 | Answers | "The next day, the shop's bank checks its books and must file one of two answers." | `[B]` Inside the shop's bank: a ledger opens; two stamps hover. A day counter flips to T+1. | DAY T+1 | Page turn |
| 1:25 | Answers | "Answer one, T.C.C. — we credited the shop. The shop has your money, even though its speaker stayed silent." | `[B]` Stamp TCC · CREDITED; crate slides into the shop's account row; `[R]` the soundbox still dark. | ANSWER TCC ✓ | Stamp, chime |
| 1:33 | Answers | "Answer two, R.E.T. — return. The shop never got it, so the money goes back, and your bank puts it in your account." | `[B]` Rewind; stamp RET · RETURN; the crate rides the next batch home; your account row climbs back. Cite `[NPCI CIRCULAR \| 2026]`. | ANSWER RET ↩ · BALANCE ₹5,240 | Stamp, reverse whoosh |
| 1:42 | Answers | "That's why refunds come the next day, not in seconds." | `[H]` Same frame, the T+1 counter glows; the hub clock spins once. | — | — |
| 1:46 | Rule | "And the R.B.I. sets a deadline. Sent to a person? Back by the next day. Paid a shop? Within five days." | `[R]` Push-in on the real RBI circular table, magnifier on "T + 1" then "T + 5"; day strips draw. Cite `[RBI CIRCULAR \| 2019]`. | DAY T+1 (person) · T+5 (shop) | Ticks |
| 1:54 | Ruin | "Miss it — and the bank pays you one hundred rupees for every extra day. You don't even have to ask." | `[H]` The strip runs past its limit; each extra cell drops a ₹100 coin into YOUR ACCOUNT. | BANK OWES ₹100 / DAY | Coin drops |
| 2:03 | Action | "So what should you do at the counter? Here's what I do." | `[R]` Back at the counter; the phone shows PROCESSING. | STATUS PROCESSING | Music lifts |
| 2:08 | Action | "First, never pay again while it says processing. If the answer is T.C.C. — you've paid twice." | `[H]` Thumb hovers over PAY; a ghost second crate appears and both land in the shop's account; chip PAID TWICE. ILLUSTRATION. | BALANCE ₹3,560 (illustrative) | Double thud |
| 2:14 | Action | "Second, ask the shopkeeper to check their bank statement, not the speaker." | `[R]` Shopkeeper's phone: bank statement scrolls to a ₹840 credit (simulated, no real app brand); the soundbox ignored. | — | Scroll |
| 2:19 | Action | "Third, if nothing comes back by the deadline, complain in your app's U.P.I. Help, and then to your bank." | `[R]` Phone: History → payment → UPI Help → Complaint Raised (simulated). | — | Taps |
| 2:27 | Share | "Cleared your doubt? Send this to that friend who always pays twice." | `[H]` Share sheet slides up (simulated, no real app brand). | HUD collapses | Soft rise |
| 2:32 | Bridge | "That's the payment that breaks. But what happens when a payment goes right? Watch this next one." | `[B]` Wide hero: a clean pulse runs both ways on the message layer; SUCCESS lamp green. End screen: logo end card + film 02 tile + subscribe zone. Channel named here only. | — | Outro bed, logo sting under VO |

**Hero Blender shots (budget ≈ 30 s):** 0:08 two-deck wide; 0:29–0:38 the money layer and batch shuttle; 1:00–1:15 deemed stamp and the crate moving to the shop's bank; 1:19–1:42 the ledger and two stamps; 2:32 closing wide. Everything else is HyperFrames or Three.js.
