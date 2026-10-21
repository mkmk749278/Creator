# Film 36 · Screenplay / storyboard (Block 3)

Timed to the final edit `voice/vo_v10_take2_edit.mp3` (206.47 s) with `align_take2/edit_lines_exact.json`.
Built from the independent panel (`review_visual_suggestions_v1.md`) and the owner's look decision (README: daylight world
+ blueprint X-ray). Labels are ≤ 3 words, and every on-screen number is in `claims.csv` or carries an ILLUSTRATIVE chip.

**Mode codes:**
- **W** daylight world (HyperFrames 2D lane)
- **X** blueprint X-ray (HyperFrames)
- **B** Blender Cycles hero cutaway, composited under the HUD
- **F** real footage (stock, licensed, logged in `media_manifest.csv`)

**Scene cuts** sit at the midpoint of the pause between lines. A scene's duration is its composition's `data-duration` (30 fps).

| Scene | Lines | In | Out | Dur (s) | Content | Modes |
|---|---|---|---|---|---|---|
| S01 | 1–3 | 0.00 | 20.90 | 20.90 | hook: sun, fan stops, not broken, lineman, questions | F, W |
| S02 | 4 | 20.90 | 34.07 | 13.17 | not this inverter → the solar box | B/W |
| S03 | 5–6 | 34.07 | 51.33 | 17.26 | D.C. vs A.C., 50 swings, the box converts | X |
| S04 | 7–8 | 51.33 | 73.88 | 22.55 | drummer and dancer, normal day, export path | W, X (scope) |
| S05 | 9–11 | 73.88 | 97.07 | 23.19 | supply off, what-if back-feed, 230 → 11,000 V | W, B |
| S06 | 12 | 97.07 | 110.09 | 13.02 | the box notices, relay opens, ≤ 2 s | X, B |
| S07 | 13–16 | 110.09 | 141.02 | 30.93 | balanced case, the off-beat test, grid on / off | X, W |
| S08 | 17–18 | 141.02 | 159.47 | 18.45 | panels: no current, heat, wires still live | W, F |
| S09 | 19–20 | 159.47 | 178.27 | 18.80 | hybrid: isolate, battery drummer, fans back | W, B, F |
| S10 | 21–24 | 178.27 | 206.47 | 28.20 | rule, say no, lineman, lost its drummer, bridge + end screen | W, F, X |

## Shots
| Time | AUDIO (cue) | VISUAL + ACTION | Label | HUD | SFX | Mode |
|---|---|---|---|---|---|---|
| 0:00.0 | "Two in the afternoon. Full sun…" | High angle on a flat Indian RCC roof, panels on a GI frame, harsh glare, clothes line moving; slow push-in | 2:00 PM | GRID 230 V · 50.0 Hz (single row) | crows, traffic, heat drone | F |
| 0:02.6 | "…and suddenly, a power cut." | Ceiling fan at speed, curtain moving; on "power cut" the room dims and the fan starts slowing | POWER CUT | GRID → 0 V | thunk, whir winds down | F |
| 0:06.3 | "The sun is still shining. But your fans stop." | Split: panels blazing above, fan coasting to a stop below | STILL SUNNY | SUN ≈1000 W/m² (ILLUSTRATIVE) | fading whir | F+F |
| 0:09.0 | "Your solar isn't broken. It switched off on purpose —" | W: the solar box on the wall, green LED goes dark, internal switch flips with a white flash ring | NOT BROKEN | SOLAR BOX TRIPPED | relay click | W |
| 0:11.6 | "— to protect a lineman's life." | Lineman in helmet and gloves on a pole, low angle, sun behind; calm work, no harm | LINEMAN | – | low tone | F |
| 0:15.2 | "Where does all that sunshine go?" | W: sunbeams into the panel curl into a "?" shape made of light | – | – | shimmer | W |
| 0:17.6 | "…how do you keep your fans running? Let's see." | W: fan icon; camera dives through the roof into the house | – | – | whoosh | W |
| 0:21.8 | "One thing first — this is not the inverter battery you keep at home…" | Under the stairs: home inverter + tall tubular battery (beep); it slides aside under a slate ✕ | NOT THIS | – | inverter beep | B (or W) |
| 0:26.0 | "It's the box your solar panels connect to." | W: follow an amber cable from the roof panels down the wall to the box (small DC and AC isolator boxes beside it) | – | – | cable zip | W |
| 0:28.5 | "Installers call it an on-grid inverter…" | W: label on the box | ON-GRID INVERTER | – | tick | W |
| 0:31.0 | "We'll just call it the solar box." | Label morphs; the sun badge pops onto the box (the dancer) | SOLAR BOX | SOLAR BOX IN STEP ✓ | pop | W |
| 0:34.3 | "Your panels give D.C. power — it flows only one way." | X: push through the panel cable; amber charges stream one way; a flat-line trace | D.C. ONE WAY | – | low hum | X |
| 0:38.1 | "Your house runs on A.C. power — not the air conditioner…" | W: an AC unit on the wall shakes "no" and swipes off; pan to a 3-pin socket | A.C. = SOCKET | – | swipe | W |
| 0:42.5 | "It swings forward and back — fifty full swings every second." | X: cyan charges jiggle in place in the wire, a sine draws, counter 1→50 inside a 1-s ring | 50 PER SECOND · SLOWED DOWN | GRID 50.0 Hz | tick sweep | X |
| 0:46.5 | "The solar box turns panel power into wall-socket power." | X: box cross-section; a flat amber line enters left, a cyan sine leaves right | D.C. → A.C. | – | morph tone | X |
| 0:52.1 | "…can't make that back-and-forth rhythm on its own." | X: the box tries to draw its own sine; it flickers and fails; it "listens" toward the street wire | – | – | failed blip | X |
| 0:56.0 | "Think of the grid as a drummer… and the solar box as a dancer…" | W: pull out to the street; the dhol icon appears on the transformer; each beat sends a cyan ring down the wire; the sun-badge box sways in time | DRUMMER · DANCER | – | dhol (slowed) | W |
| 1:03.0 | "On a normal day, it follows every beat." | X strip over W: scope, grid trace and box trace overlap, green glow | IN STEP | SOLAR BOX IN STEP ✓ | dhol continues | X |
| 1:06.0 | "Your house uses what it needs." | W house cutaway: fan, fridge and TV fed by amber→cyan particles | – | – | appliance hum | W |
| 1:08.0 | "The extra goes out through your meter… onto the street wire… and up to the transformer on the pole." | W one move: surplus through the digital net meter (export arrow), the service wire, up the pole to the transformer | NET METER → TRANSFORMER | EXPORT +1.2 kW (ILLUSTRATIVE) | rising hum | W |
| 1:14.7 | "Now the power cut comes. The electricity board switches off the supply…" | W map-style pull back: substation breaker opens; wires go slate street by street; the dhol stops mid-beat. **1.5 s music silence, then the thud** | SUPPLY OFF | GRID 0 V | big clunk, silence | W |
| 1:19.7 | "If your solar box kept pushing, that dead wire would be alive again, right?" | **What-if** (dashed border, desaturated, WHAT IF tag): the box keeps pushing; the slate wire relights red from the house outward | WHAT IF? | – | rising buzz | W |
| 1:25.5 | "…that transformer on the pole works in reverse. Your two hundred and thirty volts… becomes about eleven thousand volts…" | B: distribution transformer cutaway; energy enters the LT coil, leaves the HT coil, arrows up; counter 230 → 11,000 | 230 V → 11,000 V | LINE 230 → 11,000 V | deep hum | B |
| 1:30.0 | "On a wire the lineman thinks is switched off." | W what-if: a stylised lineman on the 11 kV line upstream, unaware; red creeps toward his gloves; **freeze before contact** | THINKS IT'S OFF | – | heartbeat, tone cuts | W |
| 1:37.9 | "So the solar box is built to notice." | Normal colour; push into the box, X: a sensor "ear" and a scope watching the grid | ALWAYS WATCHING | SOLAR BOX WATCHING | soft sonar | X |
| 1:41.5 | "If the beat goes missing, or the voltage starts changing, it switches itself off… click." | B: the grid trace vanishes, a needle leaves the green band, the relay contacts snap open with a white flash | RELAY OPENS | SOLAR BOX TRIPPED | crisp click | B |
| 1:46.0 | "Safety rules say it must switch off within two seconds." | X: stopwatch ring 0→2 s around the box; the box goes dark well before 2 | ≤ 2 SECONDS | TRIP TIMER ≤ 2 s LIMIT | tick, click | X |
| 1:50.8 | "But there's one tricky case. Say your house is using exactly what the panels make." | W: balance scale, panel output vs house use, level; meter reads 0 export | PERFECT BALANCE | EXPORT 0.0 | chime | W |
| 1:55.0 | "Then the power cut changes nothing — the box can't feel it." | X scope: supply cut but the trace is unchanged; the dhol is gone but the ribbon keeps flowing; the badge looks puzzled | NO CHANGE | GRID 0 V · BOX FREQ 50.0 | eerie quiet | X |
| 1:59.6 | "So the box tests the drummer. Again and again, it plays a little off-beat…" | X: the box trace kicks a little ahead every second | TEST NUDGE | BOX FREQ 50.0 ↗ | off-beat tap | X |
| 2:04.0 | "…to check… is the drummer still there?" | W: a ping travels from the box down the wire to the transformer | STILL THERE? | – | ping | W |
| 2:08.7 | "If the grid is there, the drummer pulls it back in line." | Split left, grid ON: dhol beats, each nudge snaps back onto the grid trace, green | GRID ON | BOX FREQ 50.0 | dhol, snap | X |
| 2:13.3 | "If the grid is gone, nobody pulls it back. The beat keeps sliding… Click — it switches off." | Split right, grid OFF (slate): the nudge accumulates; 50.0 → 50.3 → 50.7 Hz to a red limit line; relay flash; box dark | GRID OFF | BOX FREQ 50.7 → TRIP (ILLUSTRATIVE) | rising pitch, click | X |
| 2:21.8 | "What happens to your panels? Once the box is off, the power has nowhere to go." | W roof: amber particles in the panel cables slow and stop | NO CURRENT | PANEL I = 0 A · P = 0 W | wind-down | W |
| 2:28.0 | "The sunlight still lands and just turns into heat —" | W: thermal-style overlay, warm orange heat shimmer on the panel | JUST HEAT | – | haze | W |
| 2:31.5 | "But the panel wires still have voltage in them. So don't touch them yourself — leave that to a trained person." | W: panel cables pulse amber, a hand reaches in and pulls back → F: trained technician in gloves with a multimeter | STILL LIVE | – | warning tone | W+F |
| 2:40.2 | "You need a different box — a hybrid inverter." | W: the on-grid box slides out, the hybrid box and a wall battery slide in | HYBRID INVERTER | – | slide-lock | W |
| 2:45.0 | "Hybrid simply means it works with the grid and with a battery." | W: the street wire (cyan) and battery cable (green) light in turn | GRID + BATTERY | – | two chimes | W |
| 2:49.3 | "When the grid dies, a switch inside it first cuts your house off from the street." | B: inside the hybrid, the grid-side transfer contact opens with a visible gap; the street stays slate | STREET CUT OFF | BACKUP GRID ✕ | heavy clunk | B |
| 2:53.0 | "Then the battery becomes the drummer, and the panels dance again." | W: the dhol flies from the transformer to the battery; the beat resumes inside the house only → F: real fan spins back up | BATTERY = DRUMMER | BACKUP BATTERY → 230 V 50 Hz | dhol returns, fan whir | W+F |
| 2:58.6 | "Remember this. A normal on-grid solar box, with no battery, has to go silent when the grid goes. That's by design." | W: on-grid box (dark, shield icon) beside the hybrid; slow push on the shield | BY DESIGN | – | calm pad | W |
| 3:07.3 | "If anyone offers to switch off this safety — just say no…" | W: a generic toggle (no real menu or steps); a raised palm stops it | SAY NO | – | firm thud | W |
| 3:11.0 | "Because the lineman fixing your street is the one who gets the shock." | F: lineman at work, respectful low angle, no harm | – | – | quiet street | F |
| 3:16.1 | "Your solar never failed. It just lost its drummer." | W: wide street in afternoon light; the dhol fades from the transformer; the sun badge bows | – | – | last soft dhol | W |
| 3:19.6 | "But when the grid is live, how does that box turn sunlight into steady wall-socket power? Let's open it up next." | Push into the box, the lid lifts, glimpse of the board and coils (X) → end screen with the logo sting and end-screen zones under live VO | NEXT: INSIDE | – | whoosh, beat | X |

**Sound:**
- VO leads, with peaks at −2 to −3 dB.
- BGM sits at −24 to −26 dB under speech and swells to −12 dB in the inserted 1.0 s section pauses.
- 1.5 s of music silence before 1:14.7 (supply off), then the thud.
- Clicks are real relay foley at −8 to −10 dB.
- Master at −14 LUFS.

**Real footage needed (F):**
1. rooftop panels in harsh sun (Indian flat roof preferred);
2. ceiling fan slowing to a stop;
3. ceiling fan spinning up;
4. lineman with helmet and gloves on a pole (two different clips, no clip used twice);
5. technician with gloves and a multimeter;
6. optional curtain or room dimming.
