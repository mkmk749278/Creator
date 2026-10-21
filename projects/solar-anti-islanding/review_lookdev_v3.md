# Independent lookdev review, round 3 (lookdev v3, 2026-10-21)

No-repo session `session_01VaRQcZVHJkFfPx22RfwXop` (archived), PLAYBOOK §4a-12. Same seven-person panel; v3 preview JPGs by raw URL.

**Scores:** premium 6.5 · clarity 6 · Indian authenticity 7 · technical 6.
**Verdict:** "Change first, then build. Fix blockers 1–6 … The style itself is approved and worth building on."

## Blockers → what v4 does
1. **No grid in the X-ray** ("watches the grid" has nothing to watch). v4: the AC line goes to a junction that splits ↓ into the house socket and → into a GRID pole with a mini dhol. The sensing tap stays on the grid side of the safety switch.
2. **AC moved like DC.** v4: DC is amber dots flowing one way, and AC is blue dots oscillating ±15 px in phase with the scope (the "jiggle in place" from the visual-suggestions panel).
3. **The relay label clashed with the four switches.** v4: the relay becomes a hinged lever (pivot, arm, contact) labelled SAFETY SWITCH, and the bridge reads "D.C. → A.C." with no "switch".
4. **Street wiring.** v4: HT comes high from the right into the DP top. The LT line runs along the street below roof level (y ≈ 470), the service cable drops to the meter, and no wire crosses the rooftop or panels.
5. **Idle wires were blue.** v4: idle conductors are dark grey, and the blue core shows only while a beat passes.
6. **The beat ring was faint.** v4: the ring has a white core, a dark-blue outline and 1.5× the size, the wire brightens under it, and the badge bobs 12 px.

## Polish taken
- The dhol sits inside a round GRID callout badge with a pointer to the HT line.
- Steel-grey crossarms, cooler grey PSC poles, a cable-TV loop instead of the "springs".
- A bigger danger plate reading "DANGER · 11000 VOLTS".
- 5 panels in one clean row on the GI frame.
- The meter becomes a "NET METER" tag with a red LED, and the DB boxes show MCB toggles with no acronyms.
- Brighter control lines.
- The scope box trace is a thick translucent white under the blue.
- White corner brackets replace the blue draw-on line, with a light veil over the world before the wipe.
- The HUD dims to 30% while the scope is up.

## Not taken
- **Trilingual danger board (Hindi/Telugu):** needs Devanagari/Telugu fonts in this composition. It's planned for the scene build, which vendors Noto Telugu already. Devanagari will be added if it fits the fonts rule.
- **Moving the logo bug:** its top-right place is a channel rule (CLAUDE.md "a small logo bug in a corner"). The cluster is cleared by moving the dhol badge instead.
