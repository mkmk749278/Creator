# Design reference · matsya-6000 hero shots (PLAYBOOK §10.1)

Drawn from real references before modelling. Script: `scripts/blender/matsya_hero.py`. Reference frames: ISRO's
Samudrayaan video (Drive `footage/isro_samudrayaan_230725.webm`), PIB photos (`footage/pib/`), NIOT renders
(`footage/cowork/niot_deepsea19.png`, `niot_deepsea24.png`), IFREMER's Nautile interior (`footage/cowork/ifremer_65417_10885.jpg`).

| Element | Reference | What we copy |
|---|---|---|
| Five pieces | ISRO video 1:56, the drawing | top hatch (stepped flange), ring 1, ring 2, ring 3, bottom dome; cuts at 0.857, 0.468, 0, −0.44 of the radius (measured off the drawing) |
| Seven welds | same drawing | belts W2 (hatch), W7, W1 (equator, the 7.1 m one), W6; window seams W3 (primary), W4, W5 (secondary) |
| Viewports | drawing + ISRO 1:51 photo | primary at the front, on the equator, in rings 2/3; two secondary lower, ±30° in ring 3; red flanges with bolts on the finished ball |
| Size | PIB feature (M01) | 2,260 mm outside, 80 mm wall, so 2.1 m inside (OUR CALCULATION) |
| Bare metal | ISRO 2:13 (machined Ti6Al4V piece) | warm grey, fine lathe rings, satin |
| Finished ball | ISRO 1:51, PIB sphere hall | painted mid grey, red viewport rims |
| Inside | PIB three-crew photo; IFREMER Nautile interior | dark padded wall, screens on the upper wall, three people facing the windows; we show empty seats and a plain grey figure only (no real person) |
| Base | PLAYBOOK §9.3 | steel inspection plate with a half-metre grid, a machined support ring |

Labels from Remotion: ILLUSTRATION on every shot; SIMPLIFIED on `squeeze` (the give is exaggerated many times);
OUR CALCULATION on the 7.1 m line and "just over two metres".

| Shot | Frames | Starts at (s) | Sentences |
|---|---|---|---|
| dive | 0–659 | 0.00 | s0–s1 (cold open, into the ball) |
| squeeze | 0–779 | 69.68 | s22–s24 (fingernails, a lakh tonnes); reusable for s44–s46 |
| pieces | 0–959 | 177.54 | s57–s64 (five pieces, seven welds) |
| seam | 0–959 | 233.93 | s79–s83 (the real weld, seven metres, thirty-two minutes) |
| cutaway | 0–999 | 266.91 | s89–s92 (step inside, two metres, lie down, three seats) |
| dark | 0–719 | 422.08 | s133–s140 (back inside, lights off) |

H3, the vehicle (`scripts/blender/matsya_vehicle.py`), from ISRO 1:12 (the frame on the crane) and the PIB wet-test
photos (Kattupalli, 7 Feb 2025): a cream open frame about three ball-widths long, the ball at the front, ducted
thrusters at the back, skids, four lamps and a folded arm at the front, two steel drop weights underneath, yellow foam
blocks over the top and sides. Sizes are measured off the photos (no published drawing): ILLUSTRATION.

| Shot | Frames | Starts at (s) | Sentences |
|---|---|---|---|
| weights | 0–539 | 124.60 | s39–s41 (drop the weights, it rises, 96 hours) |
| assemble | 0–779 | 312.80 | s102–s105 (only part of the sub, batteries, lights, motors, arms, sinks, the foam) |
| seabed | 0–959 | 361.90 | s116–s119 (no sunlight, your lights, outside your window, black lumps of metal) |
| descent | 0–539 | 443.60 | s141–s142 (the first deep dive) |
