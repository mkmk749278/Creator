# Film 01 · Independent review of the visual plan, round 1 (before build)

No-repo session `session_01UDUSyozsFhwsXg7qBzibx9`, 2026-10-20. Panel: Priya (21), Ramesh (44, kirana owner),
Lakshmi (58), Arjun (30, engineer), Meera (35, motion designer). They read the look description, the storyboard and
the narration; they did not see the lookdev frames.

**Verdict: build with changes.** The phone-call metaphor is strong, but the money must be one visible object whose
position tells you the status, and the switchboard and racks need human and bank cues to read on a phone.

## Panel's top 10 (ranked)
1. ₹840 as one glowing token, tracked from 0:24 to the end.
2. Token position = status: in the shop = success, back home = failed, frozen mid-cable = processing.
3. Failed in red with ✗ (orange and amber look the same on a phone and for colour-blind viewers); an icon on every state.
4. Hook on two contradictory notifications stacked on one phone, the silent soundbox, a queue behind.
5. HUD to 2 lines on screen; other values pop only when they change.
6. Operator's hand + a "Calling… / Call dropped" screen on the switchboard, so young viewers decode it.
7. Each rack gets a bank identity: name plate, ₹ account slots, a vault-panel cue.
8. Split 0:29 in two; move the 0:40 three-slot panel into the 3D world.
9. Real kirana footage with ambience and human reactions; the soundbox says "Received" once (success).
10. Cut or demote the batch shuttle; turn the RBI table into a big T+1 / T+5 calendar.

## Other notes
- 0:11: three chips feel like a slide; one at a time on the beats, over the counter footage.
- 0:53: a padlock reads as "account blocked forever"; use the ✗ lamp and a reject stamp.
- 1:00: too packed; token flies back + balance climbs, pay-again thumb as a 1.5 s insert.
- 1:13: let the 15 s dial sweep from the ring onward so the drop feels earned.
- 1:22: the ₹0 / ₹840 flicker is "the best idea in the film"; add a "?" on the shop's row.
- 1:41: show the customer's own phone with a return arrow back to them.
- 2:51: calendar flips T+6, T+7, one ₹100 coin per flip. 3:20: balance drops twice, two SMS stack. 3:58: hold PAYS TWICE 2.5 s.
- Craft: a warm practical lamp at the switchboard against the cool room; slightly rough floor reflection; every 3D
  shot moves (dolly, 35–50 mm, rack focus, micro-shake on the drop); a "parcel cam" following the token; match cut
  PIN keypad grid → jack grid; per-state sound logo (chime, buzz, ticking); kirana ambience; human faces.
- Arjun: a 1950s board vs a mobile call is an era clash (fix with the call screen); a crate "travelling" implies cash moves.

## What we take, and what we don't (decisions)
- **Take:** 1, 2, 3, 5, 7, 8, 10 and every scene note above, the craft list, the match cut and the state sound logos.
- **6, partly:** the call screen on the switchboard crown (CALLING… / CONNECTED / CALL DROPPED) — yes. The operator's
  hand as 3D: no (a CG hand is the first thing that looks fake). Instead a 1–2 s public-domain archival insert of a
  real operator plugging a cord (refs already found), labelled ARCHIVE, then the 3D plug completes the same motion.
- **3:** a new FAILED red is a change to the blueprint palette (`bp_stress` orange stays for faults elsewhere). Proposed
  `bp_fail: "#f85149"`; owner's call.
- **4 and 9:** stock kirana footage from the tested sources (Pixabay API) for counter, queue and faces; phone screens and
  notifications are our own simulated UI composited on the phone. A spoken "Nahi aaya" needs a real person on camera —
  we never synthesise a person's line; only if the owner records or films it.
- **Token location in the hold shot:** stays mid-cable, because the VO says "stuck between your bank and the shop's bank"
  (semantic lock); the token is light, not a cash crate, so it reads as a held payment, not travelling cash.
- **Soundbox "Received":** generic device chime + short "payment received" voice from a TTS device voice, no brand, on
  the success beat only.
