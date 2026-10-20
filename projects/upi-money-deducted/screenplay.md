# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

Storyboard and screenplay (Block 3). Times are estimates at 135 words a minute; re-time from `align/` once the VO is
recorded. Each row is one visual state (2.5–4.5 s) and changes **one** thing from the row before (angle, geometry or
state). `[B]` = Blender Cycles hero shot, `[3]` = Three.js, `[H]` = HyperFrames 2D, `[R]` = real footage. Stand-ins
carry ILLUSTRATIVE FOOTAGE; every model carries ILLUSTRATION. Cite tags bottom right.

**The model (designed from real reference photos first, PLAYBOOK §9.2):** three machines on the blueprint grid, left to
right: **YOUR BANK** (a core-banking server rack, cut open: ledger drives, a glowing account row), **THE SWITCH** (NPCI,
a router chassis with two ports labelled DEBIT and CREDIT, a 15-second ring timer on its face) and **SHOP'S BANK** (a
second rack). Money is a **cyan data packet** carrying "₹840". Two glass conduits join them: the debit leg and the
credit leg. References to collect: data-centre rack photos, a bank core-banking server room, an Indian kirana counter,
a UPI QR standee and soundbox, the RBI circular table, the NPCI circular page 15.

| Time | Phase | AUDIO (VO) | VISUAL + ACTION | HUD | SFX / music |
|---|---|---|---|---|---|
| 0:00 | Hook | "Your phone says... debited." | `[R]` Tight on hands at a kirana counter: phone screen shows ₹840 DEBITED in a UPI app (simulated screen, our own mock, no real app brand). | HUD fades in: BALANCE ₹4,400 (amber) | Counter ambience, a phone buzz |
| 0:03 | Hook | "Eight hundred and forty rupees." | `[R]` Same hands, phone tilts toward the shopkeeper (angle change only). | — | — |
| 0:05 | Hook | "The shopkeeper turns the speaker toward you — silence." | `[R]` Shopkeeper's hand turns the soundbox toward camera; its light stays off. ILLUSTRATIVE FOOTAGE. | CREDIT LEG `?` blinking | Room tone drops to near silence |
| 0:08 | Hook | "Nothing came. And the queue behind you is getting louder." | `[R]` Over-the-shoulder: three people waiting, one checks the time. | — | Murmur rises |
| 0:12 | Constraint | "So where is your money right now?" | `[H]` Match cut: the phone's ₹840 lifts off the screen as a cyan packet and the frame pulls back into the blueprint grid. | MONEY AT `?` | Whoosh, low drone in |
| 0:15 | Constraint | "It is not lost. It is stuck between two banks." | `[B]` Wide hero: the three machines; packet hovering in the glass conduit between SWITCH and SHOP'S BANK, amber glow. Label "ILLUSTRATION". | MONEY AT IN TRANSIT | — |
| 0:20 | Constraint | "U-P-I moves about eighty crore payments a day." | `[H]` Same wide, thousands of faint packets stream through the switch (state change only). Cite `[NPCI DATA \| SEP 2026]`. | UPI LOAD 80 CR / DAY | Rising hum |
| 0:24 | Constraint | "And the switch in the middle, run by N-P-C-I," | `[B]` Push in on THE SWITCH chassis (angle change). Lower-third: NPCI SWITCH. | — | — |
| 0:27 | Constraint | "gives each bank just fifteen seconds to answer." | `[B]` Same angle: the 15-second ring on its face lights up. `[R]` insert 1 s: NPCI circular page, magnifier on "15 seconds". Cite `[NPCI UPI CIRCULAR \| 2026]`. | LEG TIMER 15.0 (limit marker) | Clock tick |
| 0:31 | Layer 1 | "Here is the path when everything works." | `[B]` Pull back to the wide, all quiet, conduits empty, slate housings. | Timers reset | Music settles |
| 0:34 | Layer 1 | "You type your U-P-I pin." | `[R]` Thumb taps a PIN pad on a phone (stand-in, ILLUSTRATIVE FOOTAGE). | — | Soft taps |
| 0:37 | Layer 1 | "Your app sends the request to N-P-C-I." | `[3]` Packet leaves the phone icon and enters THE SWITCH. | DEBIT LEG IDLE | Blip |
| 0:40 | Layer 1 | "N-P-C-I asks your bank to debit you." | `[B]` Debit conduit lights cyan from SWITCH to YOUR BANK. | DEBIT LEG SENT · LEG TIMER runs | — |
| 0:43 | Layer 1 | "Your bank takes the money out of your account" | `[B]` Cutaway inside YOUR BANK rack: one account row drops ₹840 (counter rolls). | BALANCE ₹5,240 → ₹4,400 | Mechanical click |
| 0:46 | Layer 1 | "and replies, done." | `[B]` Same angle, a green pulse runs back up the conduit. | DEBIT LEG DONE ✓ · timer stops 0.8 s | Chime |
| 0:48 | Layer 1 | "Only then does N-P-C-I ask the shop's bank to credit the shop." | `[B]` Credit conduit lights cyan from SWITCH to SHOP'S BANK. | CREDIT LEG SENT | — |
| 0:53 | Layer 1 | "The shop's bank adds the money and replies, done." | `[B]` Cutaway inside SHOP'S BANK rack: shop account row rises ₹840; green pulse back. | CREDIT LEG DONE ✓ | Chime |
| 0:57 | Layer 1 | "Two legs. A debit leg first, then a credit leg —" | `[H]` Same wide, conduits re-coloured: DEBIT 1 cyan, CREDIT 2 cyan, numbered chips. Cite `[WORLD BANK / NPCI \| UPI FLOW]`. | — | — |
| 1:01 | Layer 1 | "two separate steps, on two separate bank computers." | `[B]` Slow orbit 15° around the two racks (angle change only). | — | — |
| 1:05 | Layer 1 | "Your money leaves first... and arrives second." | `[B]` Same orbit end: packet leaves rack 1 (1), arrives rack 2 (2); dimension bracket marks the gap. | MONEY AT YOUR BANK → SHOP'S BANK | Two soft hits |
| 1:09 | Stress | "Back to the counter." | `[R]` Return to the kirana counter, same framing as 0:03. | Timers reset · BALANCE ₹5,240 | Counter ambience |
| 1:11 | Stress | "Your bank has already debited you." | `[B]` YOUR BANK cutaway, account row drops. | DEBIT LEG DONE ✓ · BALANCE ₹4,400 | Click |
| 1:14 | Stress | "The credit request reaches the shop's bank..." | `[B]` Credit conduit lights, packet arrives at SHOP'S BANK. | CREDIT LEG SENT · LEG TIMER runs | — |
| 1:17 | Stress | "and the reply never comes back." | `[B]` Same angle: the return pulse starts and dies halfway; conduit dims. | CREDIT LEG NO REPLY | Music cuts to silence (1.5 s) |
| 1:19 | Stress | "Maybe a network link dropped." | `[B]` Macro: the credit conduit's fibre glows, then a segment goes dark. Cite `[RBI CIRCULAR \| 2019]`. | — | Silence |
| 1:21 | Stress | "Maybe the session timed out." | `[H]` Same macro, the timer ring sweeps past 10 s. | LEG TIMER 10 … 14 | Tick |
| 1:24 | Stress | "Fifteen seconds pass." | `[B]` Push in on THE SWITCH face: ring completes, turns safety orange. | LEG TIMER 15.0 TIMEOUT | Low thud (reveal) |
| 1:27 | Stress | "N-P-C-I cannot wait forever, so it marks your payment as deemed — pending." | `[B]` Same angle, the packet freezes inside the credit conduit and turns amber; tag "DEEMED" snaps on (3 words max). Cite `[NPCI UPI CIRCULAR \| 2026]`. | CREDIT LEG DEEMED · MONEY AT IN TRANSIT | Music back, low |
| 1:31 | Stress | "Nobody knows yet whether the shop got the money." | `[B]` Pull back to wide: amber packet alone between the racks (geometry unchanged). | — | — |
| 1:35 | Stress | "So your app shows debited," | `[R]` Close on the phone: DEBITED. | — | — |
| 1:38 | Stress | "and the shop shows nothing. Both screens are telling the truth." | `[R]` Close on the soundbox and the shop's phone: no new payment. Split screen holds both (layout change only). | — | Soft hit |
| 1:42 | Edge case | "Then the system checks itself." | `[B]` THE SWITCH sends a small slate query pulse down the credit conduit. | CREDIT LEG CHECKING | Sonar ping |
| 1:45 | Edge case | "N-P-C-I goes back to the shop's bank and asks, what happened?" | `[B]` Same angle, pulse reaches SHOP'S BANK; its rack light blinks. | — | Ping |
| 1:49 | Edge case | "If the money reached the shop, it becomes a success." | `[H]` Path A: packet turns green, slides into SHOP'S BANK. | CREDIT LEG SETTLED ✓ | Chime |
| 1:53 | Edge case | "If it never reached, the shop's bank sends it back," | `[B]` Rewind to the amber packet, path B: it reverses up the conduit toward YOUR BANK. | CREDIT LEG RETURNED ↩ | Reverse whoosh |
| 1:58 | Edge case | "and your bank reverses the debit." | `[B]` YOUR BANK cutaway: account row climbs back. | BALANCE ₹4,400 → ₹5,240 | Click |
| 2:01 | Edge case | "Either way, it has to settle." | `[H]` Same wide, both outcome paths drawn side by side, conduits calm. | MONEY AT SETTLED | Music lifts |
| 2:03 | Synthesis | "So here is the rule. For a payment to a shop," | `[R]` Push-in on the RBI circular table (real page), highlighter on the UPI rows. Cite `[RBI CIRCULAR \| 2019]`. | DAY T+0 | — |
| 2:08 | Synthesis | "the R-B-I says the money must come back within five days." | `[H]` Same page, magnifier on "T + 5 days"; a 5-cell day strip draws below. | DAY T+0 → T+5 (shop) | Ticks |
| 2:12 | Synthesis | "Sent to a person, by the next day." | `[H]` Same strip layout, second row: 1 cell, "T + 1". | DAY T+1 (person) | Tick |
| 2:15 | Synthesis | "If the bank is late, it owes you one hundred rupees for every day of delay —" | `[H]` Day strip runs past its limit; each extra cell drops a ₹100 coin. | BANK OWES ₹100 / DAY | Coin drops |
| 2:20 | Synthesis | "without you even asking." | `[H]` Coins slide into a "YOUR ACCOUNT" slot (no click, no form). | — | — |
| 2:23 | Synthesis | "Let me say that again." | `[R]` Back at the counter: the customer looks at the phone, calmer. | — | Music dips |
| 2:26 | Synthesis | "Shop, five days. Person, next day." | `[H]` Two chips on the counter shot: SHOP · 5 DAYS, PERSON · NEXT DAY. | — | Two hits |
| 2:30 | Synthesis | "Late means one hundred rupees a day." | `[H]` Same shot, third chip: ₹100 / DAY. | BANK OWES ₹100 / DAY | Hit |
| 2:33 | Synthesis | "And before you pay a second time..." | `[R]` Thumb hovers over PAY again. | — | Pause |
| 2:37 | Synthesis | "check the status of the first one." | `[R]` Thumb moves to History, taps the pending payment: status PENDING (simulated screen). | CREDIT LEG DEEMED | Tap |
| 2:40 | Bridge | "That is the payment that breaks." | `[B]` Wide hero, the amber packet fades out; conduits glow cyan. End screen begins: logo end card, film 02 tile slides in on the right. | HUD collapses | Outro bed |
| 2:44 | Bridge | "So what happens in those few seconds when a hundred rupee payment goes right?" | `[B]` Same wide, a fresh ₹100 packet zips through both legs cleanly (state change). | — | — |
| 2:49 | Bridge | "Watch this next breakdown to find out." | End screen: film 02 tile ("What actually happens when you pay ₹100 through UPI?") + subscribe zone. Channel named here only. | — | Logo sting under VO |

**Hero Blender shots (budget ≈ 30 s):** 0:15 wide three machines; 0:43 / 0:53 rack cutaways; 1:17–1:31 the stuck packet and
timeout; 1:53–1:58 the reversal; 2:40 the closing wide. Everything else is HyperFrames or Three.js.
