# Film 01 · Telemetry HUD spec (Block 1)

Top-left, on a `bp_panel` scrim, monospace numbers in `bp_readout`, labels ≤ 3 words. Every value changes on its cue
word (`screenplay.md`). Logo bug bottom right, citation tags bottom right above it.

| Readout | Unit | Normal | Stressed | Colour | Source / label |
|---|---|---|---|---|---|
| LEG TIMER | seconds, 0.0 → 15.0 | stops at 0.4–1.2 s with a green tick | runs to 15.0, flashes, `TIMEOUT` | `bp_readout` → `bp_stress` at 15.0 | 15 s limit: claims U02. Running times ILLUSTRATIVE |
| DEBIT LEG | state | `IDLE → SENT → DONE ✓` | `DONE ✓` (stays done) | `bp_signal` while sent, `bp_verified` done | U03 |
| CREDIT LEG | state | `IDLE → SENT → DONE ✓` | `SENT → NO REPLY → DEEMED` then `SETTLED ✓` or `RETURNED ↩` | `bp_signal` → `bp_pressure` (deemed) → green / slate | U04, U06, U07 |
| YOUR BALANCE | ₹ | ₹5,240 → ₹4,400 | ₹4,400 held, then back to ₹5,240 | `bp_readout`; amber while money is in limbo | ILLUSTRATIVE (₹840 example) |
| MONEY AT | location | `YOUR BANK → SHOP'S BANK` | `IN TRANSIT` (amber, blinking dot) | `bp_pressure` | follows the VO |
| DAY | T+n | `T+0` | counts `T+0 … T+5` (shop) / `T+1` (person) | `bp_readout`; `bp_stress` past the limit | U08, U09 |
| BANK OWES | ₹ / day | `₹0` | `₹100 / DAY` after the limit | `bp_stress` | U10, U11 |
| UPI LOAD | payments / day | `80 CR / DAY` | — | `bp_passive` | U01 (our calculation from NPCI data) |

**Rules:** the HUD shows only what the VO has said or is saying; nothing contradicts it. Running seconds and the
balance are illustrations, so a small `ILLUSTRATIVE` chip sits under the panel whenever they're on screen.
