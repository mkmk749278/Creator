# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

Storyboard and screenplay (Block 3). Times are estimates at 150 words a minute (VO v3, owner's narration blueprint, PLAYBOOK §4a-10); re-time from `align/` once the VO is
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
| 0:00 | Hook | "Your phone says debited." | `[R]` Tight on a phone at a kirana counter: ₹840 DEBITED (our own simulated screen, no real app brand). | HUD fades in: BALANCE ₹4,400 (amber) | Phone buzz, counter ambience |
| 0:02 | Hook | "The shop says nothing came." | `[R]` The soundbox, light off; the shopkeeper's hand turns the shop phone toward camera: no new payment. ILLUSTRATIVE FOOTAGE. | CREDIT LEG `?` blinking | Room tone drops |
| 0:04 | Hook | "And here's the strange part — both are telling the truth." | `[R]` Split screen: your phone (debited) beside the shop phone (nothing). | — | Soft hit |
| 0:08 | Hook | "Your money isn't lost. It's stuck between two banks..." | `[H]` ₹840 lifts off your phone as a cyan packet; frame pulls back into the blueprint grid. `[B]` Wide hero: YOUR BANK · NPCI SWITCH · SHOP'S BANK, packet hovering amber in the conduit. ILLUSTRATION. | MONEY AT IN TRANSIT | Whoosh, low drone in |
| 0:12 | Hook | "and I'll show you when it comes back." | `[B]` Same wide, slow push toward the gap (camera only). | — | — |
| 0:15 | Hook | "Think about it. You pay eight hundred and forty rupees at a kirana shop, and the speaker stays silent." | `[R]` POV: QR standee, thumb taps PAY, the soundbox stays dark. ILLUSTRATIVE FOOTAGE. | — | Taps, silence |
| 0:21 | Hook | "Sounds familiar, right?" | `[R]` Over-the-shoulder: the line behind you, one person checks the time. | — | Murmur |
| 0:24 | Constraint | "Here's the catch. U.P.I. handles about eighty crore payments a day." | `[H]` Back on the wide, thousands of faint packets stream through the switch. Cite `[NPCI DATA \| SEP 2026]`. | UPI LOAD 80 CR / DAY | Rising hum |
| 0:29 | Constraint | "So the system in the middle, run by N.P.C.I.," | `[B]` Push in on THE SWITCH chassis. Lower-third: NPCI SWITCH. | — | — |
| 0:32 | Constraint | "gives every bank fifteen seconds to reply." | `[B]` Its 15-second ring lights up; 1 s insert of the NPCI circular, magnifier on "15 seconds". Cite `[NPCI UPI CIRCULAR \| 2026]`. | LEG TIMER 15.0 (limit marker) | Clock tick |
| 0:34 | Layer 1 | "Let's look at a normal payment." | `[B]` Pull back to the wide, conduits empty, slate housings. | Timers reset | Music settles |
| 0:36 | Layer 1 | "N.P.C.I. tells your bank, take out eight hundred and forty rupees." | `[B]` Debit conduit lights cyan from SWITCH to YOUR BANK. Chip: STEP 1. | DEBIT LEG SENT · LEG TIMER runs | Blip |
| 0:41 | Layer 1 | "Your bank does it, and replies... done." | `[B]` Cutaway inside YOUR BANK rack: account row drops ₹840; green pulse back. | BALANCE ₹5,240 → ₹4,400 · DEBIT LEG DONE ✓ | Click, chime |
| 0:44 | Layer 1 | "Only then does N.P.C.I. tell the shop's bank to add it." | `[B]` Credit conduit lights cyan to SHOP'S BANK. Chip: STEP 2. | CREDIT LEG SENT | — |
| 0:48 | Layer 1 | "That bank adds it, and replies... done." | `[B]` Cutaway inside SHOP'S BANK: shop row rises ₹840; green pulse back. | CREDIT LEG DONE ✓ | Chime |
| 0:51 | Layer 1 | "One payment is two steps." | `[H]` Same wide, STEP 1 and STEP 2 chips glow. Cite `[WORLD BANK / NPCI \| UPI FLOW]`. | — | — |
| 0:53 | Layer 1 | "Money leaves one bank first, and reaches the other bank second." | `[B]` Slow 15° orbit; packet leaves rack 1, arrives rack 2; a dimension bracket marks the gap. | MONEY AT YOUR BANK → SHOP'S BANK | Two soft hits |
| 0:57 | Layer 1 | "Makes sense?" | `[H]` Same frame, both chips turn green. | — | — |
| 0:58 | Stress | "Let's go back to your shop." | `[R]` The kirana counter, same framing as 0:00. | Timers reset | Counter ambience |
| 1:00 | Stress | "Step one worked — your money is already out." | `[B]` YOUR BANK cutaway, the account row drops. | DEBIT LEG DONE ✓ · BALANCE ₹4,400 | Click |
| 1:03 | Stress | "Step two starts..." | `[B]` Credit conduit lights, packet reaches SHOP'S BANK. | CREDIT LEG SENT · LEG TIMER runs | — |
| 1:05 | Stress | "and the shop's bank never replies." | `[B]` The return pulse starts and dies halfway; conduit dims. | CREDIT LEG NO REPLY | Music cuts to silence (1.5 s) |
| 1:08 | Stress | "Maybe a network link broke. Maybe the connection timed out." | `[B]` Macro: a segment of the credit conduit's fibre goes dark. Cite `[RBI CIRCULAR \| 2019]`. | LEG TIMER 10 … 14 | Silence, tick |
| 1:12 | Stress | "Fifteen seconds pass. N.P.C.I. can't wait forever," | `[B]` Push in on THE SWITCH: ring completes and turns safety orange. | LEG TIMER 15.0 TIMEOUT | Low thud (reveal) |
| 1:16 | Stress | "so it marks your payment as deemed — which simply means, not sure yet." | `[B]` Same angle, the packet freezes amber; tag "DEEMED · NOT SURE" snaps on. Cite `[NPCI UPI CIRCULAR \| 2026]`. | CREDIT LEG DEEMED · MONEY AT IN TRANSIT | Music back, low |
| 1:20 | Stress | "That's why your phone says debited." | `[R]` Close on the phone: DEBITED. | — | — |
| 1:23 | Stress | "For your bank, step one is finished, but for the shop, step two never arrived." | `[B]` Wide: STEP 1 chip green, STEP 2 chip amber (state change only). | — | Soft hit |
| 1:29 | Edge case | "Now notice this. The system doesn't give up." | `[B]` THE SWITCH wakes: a slate query pulse forms. | CREDIT LEG CHECKING | Sonar ping |
| 1:32 | Edge case | "N.P.C.I. goes back to the shop's bank and asks... did the money reach the shop or not?" | `[B]` The pulse travels down the credit conduit; SHOP'S BANK rack light blinks. | — | Ping |
| 1:39 | Edge case | "If yes, it's a success." | `[H]` Path A: packet turns green and slides into SHOP'S BANK. | CREDIT LEG SETTLED ✓ | Chime |
| 1:41 | Edge case | "If not, the shop's bank sends it back, and your bank returns every rupee." | `[B]` Rewind to the amber packet, path B: it travels back; YOUR BANK account row climbs back. | CREDIT LEG RETURNED ↩ · BALANCE ₹4,400 → ₹5,240 | Reverse whoosh, click |
| 1:46 | Rule | "Here's the rule from the R.B.I." | `[R]` Push-in on the real RBI circular table, highlighter on the UPI rows. Cite `[RBI CIRCULAR \| 2019]`. | DAY T+0 | — |
| 1:49 | Rule | "Paid a shop? Your money must come back within five days." | `[H]` Same page, magnifier on "T + 5 days"; a 5-cell day strip draws below. | DAY T+0 → T+5 (shop) | Ticks |
| 1:53 | Rule | "Sent it to a person? By the next day." | `[H]` Same strip layout, second row: 1 cell, "T + 1". | DAY T+1 (person) | Tick |
| 1:57 | Ruin | "Miss that deadline — and the bank pays you one hundred rupees for every extra day, without you asking." | `[H]` The strip runs past its limit; each extra cell drops a ₹100 coin into a YOUR ACCOUNT slot. | BANK OWES ₹100 / DAY | Coin drops |
| 2:04 | Reality | "At the end of the day, your money was never lost — it was only waiting." | `[B]` Wide hero: the amber packet glows calmly in the conduit, then settles back home. | MONEY AT SETTLED | Music lifts |
| 2:11 | Tip · rule | "One tip from me. Never pay a second time while the first payment still says pending." | `[R]` Thumb hovers over PAY again, then stops. | — | Pause |
| 2:17 | Tip · ruin | "If the first one goes through later — you've paid twice." | `[H]` Two ₹840 packets leave your bank one after the other; chip: PAID TWICE. ILLUSTRATION. | BALANCE ₹5,240 → ₹3,560 (illustrative) | Double thud |
| 2:22 | Tip · reality | "Pending isn't failed. It just means... not sure yet." | `[R]` Thumb opens History, taps the payment: status PENDING (simulated screen). | CREDIT LEG DEEMED | Tap |
| 2:25 | Share | "Cleared your doubt? Send it to that friend who always pays twice." | `[H]` The phone's share sheet slides up (simulated, no real app brand). | HUD collapses | Soft rise |
| 2:30 | Bridge | "That's how a stuck payment comes home." | `[B]` Wide hero, conduits glow cyan. End screen begins: logo end card, film 02 tile slides in. | — | Outro bed |
| 2:33 | Bridge | "But what happens when a payment goes right? Watch this next one." | `[B]` Same wide, a fresh ₹100 packet zips through both steps cleanly. End screen: film 02 tile ("What actually happens when you pay ₹100 through UPI?") + subscribe zone. Channel named here only. | — | Logo sting under VO |

**Hero Blender shots (budget ≈ 30 s):** 0:15 wide three machines; 0:43 / 0:53 rack cutaways; 1:17–1:31 the stuck packet and
timeout; 1:53–1:58 the reversal; 2:40 the closing wide. Everything else is HyperFrames or Three.js.
