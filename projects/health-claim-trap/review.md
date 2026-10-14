# Review: health-claim-trap preview v1 (720p, 8:45)

Method: `scripts/contact_sheet.py --every 2` (263 frames, 30 sheets), each tile checked against the VO line at its
timecode (`edl.md`, `script.md`), PLAYBOOK §14. Loudness: −14.2 LUFS integrated (target −14).

## Fixed before sending (re-rendered)
| Issue | Where | Fix |
|---|---|---|
| Stock night highway with skyscrapers (not India) under "thousands of families in India" and "banks are closed" | 0:02, 0:48 | Indian street (pixabay 3175), Indian rooftops at dusk (134434) |
| Airport waiting-hall clips (runway visible) standing in for a hospital | 0:00, 3:30, 5:28, 5:32 | Rain on a night window (74585), nurse at monitors (40353), worried man on phone (204421) |
| Ombudsman board: "Closed in 3 months: 78.5%" still being written at the cut | 7:29 | Written 0.6 s earlier and faster |

## Checked and passing
- Semantic lock: every line has a matching picture; proof pages highlight the exact words the VO reads (paras 13, 16, 17; cioins.co.in; Bima Bharosa; CIO Statement H3).
- On-screen numbers match the VO and `claims.csv` (₹4,50,000; 37.5%; 32,503; 9,417 + 6,126 = 15,543 of 20,440 = 76%; 78.5%; ₹50 lakh; 3 hours; 14 days; 15–30 days).
- Labels: SIMULATION on every made-up document; ILLUSTRATIVE FOOTAGE on stock stand-ins; OUR CALCULATION on the boards; citation tags bottom right.
- Cadence: 137 shots, median 3.2 s; no still or clip over 5 s without a reframe; scenes and boards animate throughout.
- No stock clip used more than twice. Logo sting at "Welcome to Be Practical with Kishore", logo bug elsewhere, end card last with "Educational only".
- Owner's two 3 s VO silences (after "So, what does it mean for you?" and after "cioins.co.in"): picture keeps moving (proof push-in, site pan); music drops to silence for 1.5 s before the moratorium clause.

## Known limits (not blockers; owner's call)
- No real Indian hospital billing counter, TPA desk or night corridor exists in the free libraries; stand-ins are generic (mostly non-Indian) clinic footage, labelled ILLUSTRATIVE FOOTAGE. 3–4 phone clips from the owner (lobby, billing counter, no faces) would lift the hook.
- Music is the synthesised bed; a YouTube Audio Library track can replace it at the final mix.
- Preview is 720p; final is 1080p/4K after approval.
