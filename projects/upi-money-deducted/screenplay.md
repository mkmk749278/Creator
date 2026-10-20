# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

Storyboard and screenplay (Block 3). Times are estimates at 140 words a minute (VO v2, spoken-English pass, PLAYBOOK §4a-10); re-time from `align/` once the VO is
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
| 0:00 | Hook | "Imagine this. You scan the Q-R at a kirana shop" | `[R]` POV: phone camera frames a UPI QR standee on a kirana counter (ILLUSTRATIVE FOOTAGE). | — | Counter ambience |
| 0:03 | Hook | "and pay eight hundred and forty rupees." | `[R]` Same hands: amount ₹840 typed on a simulated pay screen (our own mock, no real app brand). | — | Soft taps |
| 0:06 | Hook | "Your phone says... debited." | `[R]` Tight on the phone: ₹840 DEBITED. | HUD fades in: BALANCE ₹4,400 (amber) | Phone buzz |
| 0:09 | Hook | "But the shop's speaker stays silent, and the shopkeeper says, nothing came." | `[R]` The soundbox, light off; the shopkeeper's hand turns the shop phone toward camera: no new payment. | CREDIT LEG `?` blinking | Room tone drops |
| 0:13 | Hook | "You know this feeling, right?" | `[R]` Over-the-shoulder: the line behind you, one person checks the time. | — | Murmur rises |
| 0:16 | Constraint | "So where did your money go?" | `[H]` Match cut: ₹840 lifts off the phone as a cyan packet; frame pulls back into the blueprint grid. | MONEY AT `?` | Whoosh, low drone in |
| 0:19 | Constraint | "Relax, it's not lost. It's stuck between two banks," | `[B]` Wide hero: three machines (YOUR BANK · NPCI SWITCH · SHOP'S BANK); packet hovering amber in the conduit. ILLUSTRATION. | MONEY AT IN TRANSIT | — |
| 0:22 | Constraint | "and I'll show you exactly where." | `[B]` Same wide, slow push toward the gap (camera only). | — | — |
| 0:25 | Constraint | "See, U-P-I handles about eighty crore payments a day." | `[H]` Same wide, thousands of faint packets stream through the switch. Cite `[NPCI DATA \| SEP 2026]`. | UPI LOAD 80 CR / DAY | Rising hum |
| 0:30 | Constraint | "So the system in the middle, run by N-P-C-I," | `[B]` Push in on THE SWITCH chassis. Lower-third: NPCI SWITCH. | — | — |
| 0:33 | Constraint | "gives every bank just fifteen seconds to reply." | `[B]` Its 15-second ring lights up; 1 s insert of the NPCI circular, magnifier on "15 seconds". Cite `[NPCI UPI CIRCULAR \| 2026]`. | LEG TIMER 15.0 (limit marker) | Clock tick |
| 0:36 | Layer 1 | "First, let's watch a normal payment." | `[B]` Pull back to the wide, conduits empty, slate housings. | Timers reset | Music settles |
| 0:39 | Layer 1 | "You type your pin," | `[R]` Thumb taps a PIN pad (stand-in, ILLUSTRATIVE FOOTAGE). | — | Taps |
| 0:41 | Layer 1 | "and N-P-C-I tells your bank, take eight hundred and forty rupees from this account." | `[B]` Debit conduit lights cyan from SWITCH to YOUR BANK. Chip: STEP 1. | DEBIT LEG SENT · LEG TIMER runs | Blip |
| 0:47 | Layer 1 | "Your bank takes it out and replies, done." | `[B]` Cutaway inside YOUR BANK rack: account row drops ₹840; green pulse back. | BALANCE ₹5,240 → ₹4,400 · DEBIT LEG DONE ✓ | Click, chime |
| 0:50 | Layer 1 | "Only then does N-P-C-I tell the shop's bank, add this money." | `[B]` Credit conduit lights cyan to SHOP'S BANK. Chip: STEP 2. | CREDIT LEG SENT | — |
| 0:54 | Layer 1 | "The shop's bank adds it and replies, done." | `[B]` Cutaway inside SHOP'S BANK: shop row rises ₹840; green pulse back. | CREDIT LEG DONE ✓ | Chime |
| 0:58 | Layer 1 | "So one payment is really two steps, in two different banks." | `[B]` Slow 15° orbit around the two racks (camera only). Cite `[WORLD BANK / NPCI \| UPI FLOW]`. | — | — |
| 1:02 | Layer 1 | "Money goes out first... and comes in second." | `[B]` Orbit end: packet leaves rack 1, arrives rack 2; a dimension bracket marks the gap. | MONEY AT YOUR BANK → SHOP'S BANK | Two soft hits |
| 1:05 | Layer 1 | "Simple, right?" | `[H]` Same frame, STEP 1 and STEP 2 chips glow green. | — | — |
| 1:07 | Stress | "Now back to your shop." | `[R]` The kirana counter, same framing as 0:06. | Timers reset | Counter ambience |
| 1:09 | Stress | "Step one worked — your money is already out." | `[B]` YOUR BANK cutaway, the account row drops. | DEBIT LEG DONE ✓ · BALANCE ₹4,400 | Click |
| 1:12 | Stress | "Step two starts..." | `[B]` Credit conduit lights, packet reaches SHOP'S BANK. | CREDIT LEG SENT · LEG TIMER runs | — |
| 1:14 | Stress | "and the shop's bank never replies." | `[B]` The return pulse starts and dies halfway; conduit dims. | CREDIT LEG NO REPLY | Music cuts to silence (1.5 s) |
| 1:17 | Stress | "Maybe a network link broke, or the connection timed out." | `[B]` Macro: a segment of the credit conduit's fibre goes dark. Cite `[RBI CIRCULAR \| 2019]`. | LEG TIMER 10 … 14 | Silence, tick |
| 1:21 | Stress | "After fifteen seconds, N-P-C-I can't keep waiting," | `[B]` Push in on THE SWITCH: ring completes and turns safety orange. | LEG TIMER 15.0 TIMEOUT | Low thud (reveal) |
| 1:25 | Stress | "so it puts your payment on hold. The system calls it deemed — which simply means, not sure yet." | `[B]` Same angle, the packet freezes amber in the conduit; tag "DEEMED · NOT SURE" snaps on. Cite `[NPCI UPI CIRCULAR \| 2026]`. | CREDIT LEG DEEMED · MONEY AT IN TRANSIT | Music back, low |
| 1:32 | Stress | "So why does your phone say debited?" | `[R]` Close on the phone: DEBITED. | — | — |
| 1:35 | Stress | "Because step one finished, but step two never arrived." | `[B]` Wide: STEP 1 chip green, STEP 2 chip amber (state change only). | — | — |
| 1:39 | Stress | "Both screens are telling the truth." | `[R]` Split screen: your phone (debited) beside the shop phone (nothing). | — | Soft hit |
| 1:42 | Edge case | "Then N-P-C-I goes back and asks the shop's bank, did the money reach the shop or not?" | `[B]` THE SWITCH sends a slate query pulse down the credit conduit; SHOP'S BANK rack light blinks. | CREDIT LEG CHECKING | Sonar pings |
| 1:49 | Edge case | "If yes, it becomes a success." | `[H]` Path A: packet turns green and slides into SHOP'S BANK. | CREDIT LEG SETTLED ✓ | Chime |
| 1:52 | Edge case | "If not, the shop's bank sends it back," | `[B]` Rewind to the amber packet, path B: it travels back up the conduit. | CREDIT LEG RETURNED ↩ | Reverse whoosh |
| 1:55 | Edge case | "and your bank returns your money." | `[B]` YOUR BANK cutaway: the account row climbs back. | BALANCE ₹4,400 → ₹5,240 · MONEY AT SETTLED | Click, music lifts |
| 1:58 | Takeaway | "So what does the R-B-I rule say?" | `[R]` Push-in on the real RBI circular table, highlighter on the UPI rows. Cite `[RBI CIRCULAR \| 2019]`. | DAY T+0 | — |
| 2:01 | Takeaway | "Paid a shop? Your money must come back within five days." | `[H]` Same page, magnifier on "T + 5 days"; a 5-cell day strip draws below. | DAY T+0 → T+5 (shop) | Ticks |
| 2:06 | Takeaway | "Sent it to a person? By the next day." | `[H]` Same strip layout, second row: 1 cell, "T + 1". | DAY T+1 (person) | Tick |
| 2:09 | Takeaway | "And if the bank is late, it pays you one hundred rupees for every extra day —" | `[H]` The strip runs past its limit; each extra cell drops a ₹100 coin. | BANK OWES ₹100 / DAY | Coin drops |
| 2:15 | Takeaway | "without you even asking." | `[H]` Coins slide into a YOUR ACCOUNT slot (no form, no click). | — | — |
| 2:18 | Takeaway | "Let me say that once more." | `[R]` Back at the counter: the customer looks at the phone, calmer. | — | Music dips |
| 2:20 | Takeaway | "Shop, five days. Person, next day." | `[H]` Chips over the counter shot: SHOP · 5 DAYS, PERSON · NEXT DAY. | — | Two hits |
| 2:23 | Takeaway | "Late means one hundred rupees a day." | `[H]` Same shot, third chip: ₹100 / DAY. | BANK OWES ₹100 / DAY | Hit |
| 2:26 | Takeaway | "One tip from me. Before you pay again," | `[R]` Thumb hovers over PAY again. | — | Pause |
| 2:30 | Takeaway | "check the first payment's status, or you may pay twice." | `[R]` Thumb moves to History, taps the payment: status PENDING (simulated screen). | CREDIT LEG DEEMED | Tap |
| 2:34 | Takeaway | "Has this happened to you? Tell me in the comments how long it took." | `[H]` The pending row on the phone becomes a speech-bubble outline with a cursor blinking (no text box, 3 words: TELL ME BELOW). | HUD collapses | Soft rise |
| 2:40 | Bridge | "That's the payment that breaks." | `[B]` Wide hero, the amber packet fades out; conduits glow cyan. End screen begins: logo end card, film 02 tile slides in. | — | Outro bed |
| 2:43 | Bridge | "But what happens when a hundred rupee payment goes right?" | `[B]` Same wide, a fresh ₹100 packet zips through both steps cleanly. | — | — |
| 2:46 | Bridge | "Watch this next one." | End screen: film 02 tile ("What actually happens when you pay ₹100 through UPI?") + subscribe zone. Channel named here only. | — | Logo sting under VO |

**Hero Blender shots (budget ≈ 30 s):** 0:15 wide three machines; 0:43 / 0:53 rack cutaways; 1:17–1:31 the stuck packet and
timeout; 1:53–1:58 the reversal; 2:40 the closing wide. Everything else is HyperFrames or Three.js.
