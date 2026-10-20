# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

Storyboard and screenplay (Block 3). Times are estimates at 150 words a minute (VO v4: built on the three app statuses, success · failed · processing, owner 2026-10-20); re-time from `align/` once the VO is
recorded. Each row is one visual state (2.5–4.5 s) and changes **one** thing from the row before (angle, geometry or
state). `[B]` = Blender Cycles hero shot, `[3]` = Three.js, `[H]` = HyperFrames 2D, `[R]` = real footage. Stand-ins
carry ILLUSTRATIVE FOOTAGE; every model carries ILLUSTRATION. Cite tags bottom right.

**The model (designed from real reference photos first, PLAYBOOK §9.2):** three machines on the blueprint grid, left to
right: **YOUR BANK** (a core-banking server rack, cut open: ledger drives, a glowing account row), **THE SWITCH** (NPCI,
a router chassis with two ports labelled DEBIT and CREDIT, a 15-second ring timer on its face) and **SHOP'S BANK** (a
second rack). Money is a **cyan data packet** carrying "₹840". Two glass conduits join them: the debit leg and the
credit leg. References to collect: data-centre rack photos, a bank core-banking server room, an Indian kirana counter,
a UPI QR standee and soundbox, the RBI circular table, the NPCI circular page 15.

**The three-status device:** a status chip in the HUD (`STATUS`) and a physical "status board" on THE SWITCH with three
lamps, SUCCESS (`bp_verified` green), FAILED (`bp_stress` orange) and PROCESSING (`bp_pressure` amber, blinking). Each
time the VO names a status, its lamp lights; the same three colours are used for the three app screens, so the viewer
links word, colour and money position.

| Time | Phase | AUDIO (VO) | VISUAL + ACTION | HUD | SFX / music |
|---|---|---|---|---|---|
| 0:00 | Hook | "Your phone says debited. The shop says nothing came." | `[R]` Tight on a phone at a kirana counter: ₹840 DEBITED (our own simulated screen, no real app brand); cut to the soundbox, light off. ILLUSTRATIVE FOOTAGE. | BALANCE ₹4,400 (amber) | Phone buzz, then silence |
| 0:04 | Hook | "So open your U.P.I. app and look." | `[R]` Thumb opens History on the phone. | — | Tap |
| 0:06 | Hook | "It will show you one of three words — success, failed, or processing." | `[H]` Three status rows pop on the phone screen one by one, in green, orange and amber. Cite `[NPCI UPI HELP GUIDELINES \| 2023]`. | STATUS ? | Three soft ticks |
| 0:11 | Hook | "Each one means something different for your money." | `[H]` The three rows lift off the phone and become three lamps on a blueprint status board. | — | Whoosh |
| 0:14 | Hook | "And the third one... that's where people panic and pay twice. I'll show you why." | `[H]` Same board: the PROCESSING lamp blinks amber; two ghost ₹840 packets hover beside it. | STATUS PROCESSING (blinking) | Low pulse |
| 0:21 | Constraint | "Here's the catch. U.P.I. handles about eighty crore payments a day," | `[B]` Wide hero: YOUR BANK · NPCI SWITCH (status board on its face) · SHOP'S BANK; thousands of faint packets stream. Cite `[NPCI DATA \| SEP 2026]`. ILLUSTRATION. | UPI LOAD 80 CR / DAY | Rising hum |
| 0:25 | Constraint | "so N.P.C.I., the system in the middle, gives every bank fifteen seconds to reply." | `[B]` Push in on THE SWITCH; its 15-second ring lights. 1 s insert: NPCI circular, magnifier on "15 seconds". Cite `[NPCI UPI CIRCULAR \| 2026]`. | LEG TIMER 15.0 (limit) | Clock tick |
| 0:31 | Layer 1 | "Let's look at what a payment really is." | `[B]` Pull back to the wide, conduits empty. | Timers reset | Music settles |
| 0:33 | Layer 1 | "It's two steps — first your bank takes the money out," | `[B]` Debit conduit lights cyan; YOUR BANK cutaway: account row drops ₹840. Chip: STEP 1. | DEBIT LEG DONE ✓ · BALANCE ₹4,400 | Click |
| 0:37 | Layer 1 | "and then the shop's bank adds it in." | `[B]` Credit conduit lights cyan; SHOP'S BANK cutaway: shop row rises ₹840. Chip: STEP 2. Cite `[WORLD BANK / NPCI \| UPI FLOW]`. | CREDIT LEG DONE ✓ | Chime |
| 0:42 | Layer 1 | "Now the three words make sense, right?" | `[H]` Same wide, the status board's three lamps glow softly in turn. | — | — |
| 0:44 | Success | "Success means both steps finished, and your money has already reached the shop's bank. Done." | `[B]` Both conduits green, packet resting inside SHOP'S BANK; SUCCESS lamp lights green. | STATUS SUCCESS ✓ | Chime |
| 0:50 | Failed | "Failed means the payment broke before it finished." | `[B]` Rewind; the debit conduit flickers and stops; FAILED lamp lights orange. | STATUS FAILED | Short buzz |
| 0:53 | Failed | "Sometimes your money never even left, and if it did, your bank has to send it back." | `[B]` Split path: (a) packet never leaves YOUR BANK; (b) packet leaves and slides straight back home. | BALANCE ₹5,240 (both paths) | Reverse whoosh |
| 1:00 | Failed | "I'll be honest — failed is the safe one, because you can simply try again." | `[R]` Phone: FAILED · Kindly Try Again (simulated); thumb taps PAY again, it goes through. | STATUS SUCCESS ✓ | Tap, chime |
| 1:06 | Processing | "Now the big one. Processing — some apps say pending." | `[B]` Push in on the board: PROCESSING lamp blinks amber, everything else dims. | STATUS PROCESSING | Music drops |
| 1:10 | Processing | "It means a reply never came back. In your case, step one worked, so your money is out." | `[B]` YOUR BANK cutaway, account row drops; debit conduit green. | DEBIT LEG DONE ✓ · BALANCE ₹4,400 | Click |
| 1:16 | Processing | "Step two started... but the shop's bank never replied." | `[B]` Credit conduit lights; the return pulse dies halfway; conduit dims. | CREDIT LEG NO REPLY · LEG TIMER runs | Music cuts to silence (1.5 s) |
| 1:20 | Processing | "Maybe a network link broke. Maybe the connection timed out." | `[B]` Macro: a segment of the credit conduit's fibre goes dark. Cite `[RBI CIRCULAR \| 2019]`. | LEG TIMER 10 … 14 | Tick |
| 1:25 | Processing | "After fifteen seconds, N.P.C.I. can't keep waiting, so it marks your payment as deemed — which simply means, not sure yet." | `[B]` THE SWITCH ring completes in safety orange; the packet freezes amber; tag "DEEMED · NOT SURE". Cite `[NPCI UPI CIRCULAR \| 2026]`. | LEG TIMER 15.0 TIMEOUT · CREDIT LEG DEEMED | Low thud (reveal) |
| 1:33 | Processing | "Think about it. Your money isn't lost. It's waiting between two banks, and nobody knows yet which way it will go." | `[B]` Wide: the amber packet alone in the conduit, two dotted arrows (toward SHOP'S BANK and back home). | MONEY AT IN TRANSIT | Music back, low |
| 1:42 | Processing | "So N.P.C.I. goes back and asks the shop's bank... did the money reach or not?" | `[B]` A slate query pulse travels down the credit conduit; SHOP'S BANK rack light blinks. | CREDIT LEG CHECKING | Sonar pings |
| 1:48 | Processing | "If yes, processing becomes success." | `[H]` The arrow toward the shop lights; PROCESSING lamp turns into SUCCESS green. | STATUS SUCCESS ✓ | Chime |
| 1:50 | Processing | "If not, the shop's bank sends it back, and your bank returns every rupee." | `[B]` Path B: the packet travels home; YOUR BANK row climbs back. | CREDIT LEG RETURNED ↩ · BALANCE ₹5,240 | Reverse whoosh |
| 1:56 | Rule | "And there's a deadline from the R.B.I. Paid a shop? Your money must come back within five days." | `[R]` Push-in on the real RBI circular table, magnifier on "T + 5 days"; a 5-cell day strip draws. Cite `[RBI CIRCULAR \| 2019]`. | DAY T+0 → T+5 (shop) | Ticks |
| 2:02 | Rule | "Sent it to a person? By the next day." | `[H]` Same strip layout, second row: 1 cell, "T + 1". | DAY T+1 (person) | Tick |
| 2:06 | Ruin | "Miss that deadline — and the bank pays you one hundred rupees for every extra day, without you asking." | `[H]` The strip runs past its limit; each extra cell drops a ₹100 coin into a YOUR ACCOUNT slot. | BANK OWES ₹100 / DAY | Coin drops |
| 2:14 | Tip · rule | "So here's my one rule. Never pay again while it says processing." | `[R]` Phone shows PROCESSING; thumb hovers over PAY, then pulls away. | STATUS PROCESSING | Pause |
| 2:19 | Tip · ruin | "If the first payment goes through later — you've paid twice." | `[H]` Two ₹840 packets reach SHOP'S BANK one after the other; chip: PAID TWICE. ILLUSTRATION. | BALANCE ₹3,560 (illustrative) | Double thud |
| 2:23 | Tip · reality | "Failed means try again. Processing means wait." | `[H]` The status board: FAILED lamp with a "TRY AGAIN" chip, PROCESSING lamp with a "WAIT" chip (2 words each). | — | Two hits |
| 2:26 | Share | "Cleared your doubt? Send it to that friend who always pays twice." | `[H]` The phone's share sheet slides up (simulated, no real app brand). | HUD collapses | Soft rise |
| 2:31 | Bridge | "That's how a stuck payment comes home. But what happens when a payment goes right? Watch this next one." | `[B]` Wide hero, a fresh ₹100 packet zips through both steps; SUCCESS lamp green. End screen: logo end card + film 02 tile ("What actually happens when you pay ₹100 through UPI?") + subscribe zone. Channel named here only. | — | Outro bed, logo sting under VO |

**Hero Blender shots (budget ≈ 30 s):** 0:15 wide three machines; 0:43 / 0:53 rack cutaways; 1:17–1:31 the stuck packet and
timeout; 1:53–1:58 the reversal; 2:40 the closing wide. Everything else is HyperFrames or Three.js.
