# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

Storyboard and screenplay (Block 3). Times are estimates at 150 words a minute (VO v7, 438 words: hook names UPI and the shop in the first line, owner 2026-10-20; then the UPI flow and success / failed / processing as a phone call); re-time from `align/` once the VO is
recorded. Each row is one visual state (2.5–4.5 s) and changes **one** thing from the row before (angle, geometry or
state). `[B]` = Blender Cycles hero shot, `[3]` = Three.js, `[H]` = HyperFrames 2D, `[R]` = real footage. Stand-ins
carry ILLUSTRATIVE FOOTAGE; every model carries ILLUSTRATION. Cite tags bottom right.

**The model (designed from real reference photos first, PLAYBOOK §9.2).** Upper deck, the **call**: YOUR BANK and
SHOP'S BANK as two server racks, and between them **N.P.C.I. as a switchboard** (a blueprint version of an old
telephone exchange: patch cables, a big round 15-second dial). A call is a cyan cable glowing from the switchboard into
the shop's bank, with a call-status panel: RINGING · PICKED UP · DROPPED. Lower deck, the **money**: amber crates in
vaults and a **cash lorry** that leaves for an **RBI SETTLEMENT** depot ten times a day (ILLUSTRATION, never a real bank
van livery). At the shop's bank, an attendance-register ledger with two stamps: **YES · GAVE TO SHOP (TCC)** and
**NO · SENT BACK (RET)**. The three outcomes keep fixed colours everywhere: SUCCESS green, FAILED orange, PROCESSING
amber. Humour beats are visual and quick (third umpire screen, teacher's register, biscuit packet), never a cartoon
character. References to collect: telephone-exchange photos, data-centre racks, a bank vault, an Indian cash-van
photo (shape only), the RBI building exterior, a kirana counter, a UPI QR standee and soundbox, the RBI circular
table, the NPCI circular pages.

| Time | Phase | AUDIO (VO) | VISUAL + ACTION | HUD | SFX / music |
|---|---|---|---|---|---|
| 0:00 | Hook | "You pay eight hundred and forty rupees on U.P.I. at a kirana shop." | `[R]` POV at a kirana counter: phone camera scans the UPI QR standee, ₹840 typed, thumb taps PAY (simulated screen, no real app brand). ILLUSTRATIVE FOOTAGE. | — | Counter ambience, taps |
| 0:04 | Hook | "Your phone says debited, but the shopkeeper says nothing came." | `[R]` Tight on the phone: ₹840 DEBITED; cut to the soundbox, light off, and the shopkeeper shaking their head at their own phone. | BALANCE ₹4,400 (amber) | Buzz, then silence |
| 0:08 | Hook | "Now you're both staring like it's a third umpire review." | `[H]` Split screen, customer and shopkeeper eye to eye; a cricket-style "DECISION PENDING" strip slides across the bottom. | — | Crowd murmur sting |
| 0:12 | Hook | "So where is your money right now? In three minutes, you'll know where, when it comes back, and how not to pay twice." | `[H]` ₹840 lifts off the phone as an amber crate; a tracking reticle locks on (WHERE?); three chips slide in: WHERE · WHEN · DON'T PAY TWICE. | MONEY AT ? | Reticle beep, three ticks |
| 0:17 | Flow | "First, let me show you what happens after you type your pin." | `[R]` Thumb types the PIN (stand-in). Match cut into the blueprint world. | — | Taps, whoosh |
| 0:22 | Flow | "Step one, your bank takes the money out — that's why debited shows up so fast." | `[B]` YOUR BANK cutaway: the account row drops ₹840 instantly; chip STEP 1. | DEBIT ✓ · BALANCE ₹4,400 | Click |
| 0:28 | Flow | "Step two, N.P.C.I., the switchboard in the middle, calls the shop's bank and asks it to add the money." | `[B]` Pull back: the N.P.C.I. switchboard; an operator-style patch cable plugs into SHOP'S BANK; chip STEP 2. Cite `[WORLD BANK / NPCI \| UPI FLOW]`. | CALL RINGING | Old phone ring |
| 0:36 | Flow | "It's like a phone call, and like every call in India... three things can happen." | `[H]` The call-status panel lights three slots: PICKED UP ✓ · PICKED UP ✗ · DROPPED. | — | Ring stops |
| 0:42 | Success | "One. The shop's bank picks up and says, done, the shop got it. That's success." | `[B]` Cable glows green; the crate drops into the shop's account row; SUCCESS lamp green. | CALL PICKED UP · STATUS SUCCESS ✓ | "Click" of a receiver, chime |
| 0:48 | Failed | "Two. The shop's bank picks up and says, sorry, can't take it — maybe the shop's account has a problem. That's failed." | `[B]` Cable glows orange; a padlock on the shop's account row; FAILED lamp orange. | CALL PICKED UP · STATUS FAILED | Short buzz |
| 0:56 | Failed | "Your money already left, so N.P.C.I. tells your bank to give it back. Failed sounds scary, but it's the safe one — just pay again." | `[B]` A second cable to YOUR BANK: "GIVE IT BACK"; the account row climbs back. `[R]` Phone: FAILED · Kindly Try Again; thumb pays again. Cite `[NPCI UPI CIRCULAR \| 2026]`. | BALANCE ₹5,240 | Reverse whoosh, tap |
| 1:06 | Processing | "Three. The troublemaker. N.P.C.I. calls... and the line goes quiet. Hello? Hello? Call dropped." | `[B]` Cable glows, then flickers and goes dark mid-way; the call panel flashes DROPPED. | CALL DROPPED · STATUS PROCESSING | Ring, static, dead tone |
| 1:12 | Processing | "Did the shop's bank add the money before the call dropped? Nobody knows. That's processing." | `[B]` Inside SHOP'S BANK: the account row half-lit, flickering between ₹0 and ₹840; PROCESSING lamp amber. | — | Silence (1.5 s) |
| 1:18 | Processing | "After fifteen seconds, N.P.C.I. marks it deemed approved — approved for now, checked later." | `[B]` The 15-second dial on the switchboard completes; a stamp DEEMED APPROVED lands on the call log. Cite `[NPCI OC 213 \| 2025]`. | DIAL 15 s · DEEMED | Thud (reveal) |
| 1:24 | Twist | "Here's the twist. The real money doesn't travel with the call — it moves later, in bulk." | `[B]` Tilt down from the call deck to the money deck: your ₹840 crate still sits in YOUR BANK's vault. | MONEY AT YOUR BANK | Low brass hit |
| 1:31 | Twist | "Picture a cash lorry leaving ten times a day, settling every bank's account at the R.B.I." | `[B]` A blueprint cash lorry loads crates and drives to the RBI SETTLEMENT depot; a clock jumps two hours. Insert: NPCI settlement-cycle table, cycles 1–10. ILLUSTRATION. Cite `[NPCI UPI CIRCULAR \| 2026]`. | NEXT LORRY 01:52 · 10 / DAY | Engine, horn (short) |
| 1:37 | Twist | "On the next lorry, your money rides to the shop's bank. That's where it is right now." | `[B]` Your crate rides the lorry into SHOP'S BANK's vault; the reticle from 0:08 locks on. Cite `[NPCI UPI GLOBAL QR RULES \| 2024]`. | MONEY AT SHOP'S BANK (locked) | Reticle lock |
| 1:44 | Answers | "Next day, the shop's bank checks its books, like a teacher taking attendance. Two possible answers." | `[B]` An attendance-register ledger opens; a pen runs down the names; the day counter flips to T+1. | DAY T+1 | Page turn, pen scratch |
| 1:50 | Answers | "Yes, we gave it to the shop. So the shop has it, even though its speaker stayed silent." | `[B]` Stamp YES · GAVE TO SHOP (small label TCC); `[R]` the soundbox, still dark. | ANSWER YES (TCC) | Stamp, chime |
| 1:58 | Answers | "Or, no, we never did — then it rides the lorry back to your account. Makes sense?" | `[B]` Stamp NO · SENT BACK (small label RET); the crate rides the lorry home; your account row climbs back. | ANSWER NO (RET) · BALANCE ₹5,240 | Stamp, engine |
| 2:04 | Deadline | "And the R.B.I. sets a deadline. Sent to a person? Back by the next day. Paid a shop? Within five days." | `[R]` Push-in on the real RBI circular table, magnifier on "T + 1" then "T + 5". Cite `[RBI CIRCULAR \| 2019]`. | DAY T+1 (person) · T+5 (shop) | Ticks |
| 2:13 | Deadline | "If the bank is late, it pays you one hundred rupees for every extra day — without you asking." | `[H]` Day strip runs past the limit; ₹100 coins drop into YOUR ACCOUNT one per day. | BANK OWES ₹100 / DAY | Coin drops |
| 2:20 | Summary | "Quick summary, the way I remember it. Success, the shop got it. Failed, it's coming back, so pay again. Processing, you wait." | `[H]` The three lamps in a row, each with a 2-word chip: GOT IT · PAY AGAIN · WAIT. | — | Three hits |
| 2:29 | Tip | "So never pay again while it says processing. If the answer is yes, congratulations — you just paid double for one packet of biscuits." | `[H]` Two ₹840 crates land in the shop's account; cut to a single biscuit packet with a ×2 price tag. ILLUSTRATION. | BALANCE ₹3,560 (illustrative) | Double thud, comic beat |
| 2:39 | Tip | "Ask the shopkeeper to check their bank statement, not the speaker. Stuck after the deadline? Complain in your app's U.P.I. Help." | `[R]` Shop phone: bank statement shows a ₹840 credit; then your phone: History → UPI Help → Complaint Raised (simulated). | — | Scroll, taps |
| 2:47 | Share | "Cleared your doubt? Send this to that friend who always pays twice — I know you have one." | `[H]` Share sheet slides up (simulated); a contact named "PAYS TWICE" is highlighted. | HUD collapses | Soft laugh beat |
| 2:54 | Bridge | "So what happens when a payment goes right? Watch this next one." | `[B]` A clean call: cable green both ways, SUCCESS lamp. End screen: logo end card + film 02 tile + subscribe zone. Channel named here only. | — | Outro bed, logo sting under VO |

**Hero Blender shots (budget ≈ 35 s):** 0:28 the switchboard and patch cable; 1:06–1:18 the dropped call and the 15-second dial; 1:24–1:37 money deck and cash lorry; 1:44–1:58 the register and two stamps; 2:54 closing wide. Everything else is HyperFrames or Three.js.
