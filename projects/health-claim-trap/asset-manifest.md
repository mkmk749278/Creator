# Asset manifest: The Health Insurance Claim Rejection Trap

Full list with licences and EDL slots: `media_manifest.csv` (built by `build/manifest.py`). Files live in `assets/`
(gitignored); every one is re-fetchable from its source URL.

| Kind | Count | Source | Notes |
|---|---|---|---|
| Real b-roll | 30 clips | Pixabay API (`scripts/stock_fetch.py`, AI items hidden) | Generic medical, documents, phones, Indian city/street. Stand-ins for our illustrative family carry **ILLUSTRATIVE FOOTAGE** |
| Real b-roll | 6 clips | Coverr | IV room, gloves, printer, card payment, notebook, phone payment |
| Proof frames | 13 | IRDAI Master Circular PDF (paras 13, 16, 17), cioins.co.in, Bima Bharosa, CIO Annual Report 2024-25 (Statement H3) | Real pages, highlight on the exact words the VO reads (`build/proof_pdf.py`, `build/proof_web.js`) |
| Simulations | 7 | `build/sims.py` | Denial letter, bill, case notes, proposal forms, email, claim app. Labelled **SIMULATION**, no real names |
| Animated scenes | 7 | HyperFrames `video/healthclaim/s0*` | Receipts, denial letter and stamp, overstamp, TPA flow, moratorium ring, family timeline, discharge clock |
| Whiteboards | 3 | `video/lib/whiteboard` → `video/healthclaim/b0*` | Room-rent maths, Ombudsman 76%, ₹59,625 callback (OUR CALCULATION) |
| Music | 1 | `scripts/make_bed.py` (synthesised) | −25 dB under speech, 1.5 s silence before the moratorium reveal |

**What is missing (real footage the stock libraries don't have):** an Indian hospital billing counter, a TPA desk, a
real hospital corridor at night, the Ombudsman's office. Wikimedia Commons searches returned nothing usable (and
rate-limited). Options: the owner films 3–4 phone clips at a local hospital lobby/billing counter (no faces, no names),
or we keep the labelled stand-ins.
