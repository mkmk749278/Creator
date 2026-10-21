# Film 36 · self-review of the cut (PLAYBOOK §14), 2026-10-21

Cut: `video/solar36/out/solar36_cut.mp4`, 3:33.7 (VO 3:27.7 + 6 s end-screen tail), 1920×1080/30, captions burned,
master −14.3 LUFS integrated, −1.1 dBTP. Sheets: `video/solar36/out/qa/sheet-*.jpg` (every 4 s, then every 3 s).
Fact-check gate: `scripts/claims_check.py projects/solar-anti-islanding/claims.csv` passes (34 claims; S23 confirmed
after the "whole street" re-record).

## Issues found and fixed

| Issue | Where | Fix |
|---|---|---|
| Camera framed hundreds of px off (GSAP re-offsets x/y when a tween carries `svgOrigin`) | S01, S03, S07 pull-out | kit: `svgOrigin` only on the first set; PLAYBOOK §10 |
| Lineman jumped to 0,0 when tweened (tween replaced his `transform`) | S01 | outer placement group |
| HUD red never applied (`.v.red` missing) | S01, S05–S10 | film.css; S01/S05 re-rendered |
| Captions up to 2 s late inside long lines | captions | syllable-peak alignment (`tools/make_captions.py`) |
| **Picture a phrase early (1–2 s) from 0:38** (cue sheet guessed from pauses) | S03; also S01 lineman, S02 label, S05 lineman, S07 breaker, S09 grid switch | re-timed to measured phrase starts (`K.warp` for S03); PLAYBOOK §14 |
| Line 13 caption said "your house" (re-record says "whole street") | captions | `edit3_lines_exact.json` text fixed |
| Drum badge crowding tag/scope; NET METER tag cut by the foreground | S01, S04, S08, S09, S10 | hidden/moved per shot |
| Fan clip unlabelled | S01 | ILLUSTRATIVE FOOTAGE tag 0:02.6–0:06 |

## Checklist

- [x] ≥ 85% moving: every scene runs a continuous camera move or a running machine; freeze before contact (S05) is 1.2 s with a push.
- [x] Shots match the words: checked frame-by-frame against the burned captions after the re-time.
- [x] Lede first: the paradox (full sun, fans stop, solar off) is on screen 0:00–0:20; the first frame is the thumbnail's subject (rooftop solar, 2 PM).
- [x] On-screen data agrees with the VO: 230 V → ≈ 11,000 V (no exact landing), ≤ 2 s, trip at 50.5 Hz (CEA 11(6)(b)), citation tag CEA reg. 11(6)(e) · IEEE 1547 · IS 16169.
- [x] Stand-ins labelled: fan (F02) and technician (F03) carry ILLUSTRATIVE FOOTAGE; rooftop aerial (F01) is a real Indian rooftop, used as a setting.
- [x] No clip twice; no question-mark graphics; labels ≤ 3 words; what-if scenes framed and tagged WHAT IF.
- [x] Channel named only on the end card with the logo sting (after the last VO word); logo bug throughout.
- [x] Bridge to film 37 over the end screen (next-film zone runs the H-bridge teaser).
- [x] −14 LUFS; 1.5 s music silence before the three reveals (≈ 11,000 V, the click, the 50.5 Hz trip), thud on each.
- [x] Chapters in `youtube/description.md` match the scene starts.

## Known limits (owner's call)

- Blender hero cutaways were not made (usage limit); the transformer, relay and hybrid cutaways are HyperFrames blueprint scenes.
- No real lineman footage was found on the tested free sources; the lineman is the film's illustrated figure (low angle, calm work).
- Music and SFX are synthesised (royalty-free, deterministic), not library tracks.
- The home inverter and tubular battery (S02) were drawn from common knowledge: the Commons search was rate-limited.
