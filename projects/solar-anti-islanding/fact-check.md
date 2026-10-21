# Fact-check: Why Do Most Rooftop Solar Systems Stop Working During a Power Cut?

VO v10 (`vo.txt`), timecodes from `align_take2/edit_lines_exact.json`. Independent full pass, 2026-10-21, `max` effort.
There was no draft `claims.csv`, so I checked every factual statement in the VO.
Rows: `claims.csv` (34 claims). Every quote was checked word for word against a saved copy of its source.

## Verdict
**33 confirmed, 1 wrong. The gate fails until one sentence in line 13 is re-recorded.**
`python3 scripts/claims_check.py projects/solar-anti-islanding/claims.csv` gives `34 claims: confirmed 33, wrong 1` (S23).
Everything else stands. That includes "Safety rules say it must switch off within two seconds": the Indian rule itself
says two seconds (CEA regulation 11(6)(e)), so the line does not need to become "international safety standards".

## Required VO change (1)
**Line 13, 1:50 (S23)**
- Old: `Say your house is using exactly what the panels make.`
- New: `Say your whole street is using exactly what the solar panels make.`
- Keep the rest of line 13 as recorded: "But there's one tricky case. … Then the power cut changes nothing — the box can't
  feel it."

**Why:** Line 9 has the board switch off the whole street, so the neighbours' fans and lights stay wired to your solar
box after the cut. Only one thing hides a cut from the box: everything left on the cut-off wire uses exactly what all
its solar makes (IEA PVPS T5-09: the "local loads" are the "loads inside the potential island"). If only your house is
balanced, the neighbours' load pulls the voltage down at once, the ordinary voltage check trips the box, and there's
no tricky case.

A copy of vo.txt with the new sentence passes `scripts/spoken_english_check.py` (558 words). After the re-record, set
S23 to `confirmed` and change its claim text to the new wording. The source and quote stay the same. Then re-run the gate.

## Confirmed, with a caveat for the picture (no VO change)
- **S16, 230 V becomes "about eleven thousand volts":** Indian pole transformers are 11,000 V / 433 V, a ratio of 44
  per winding. Our calculation: 230 V × 44 ≈ 10,100 V, and the transformer's rated 250 V gives exactly 11,000 V. So
  "about" is right. Show `≈ 11,000 V` or `11 kV LINE`, not a counter that lands exactly on 11,000.
- **S11, "up to the transformer on the pole":** this is the right path. But exported power is mostly used by the
  neighbours, and it only goes up through the transformer when the street makes more than it uses. Don't show all
  export always reaching the transformer.
- **S02, "to protect a lineman's life":** this is the reason everyone gives, but it is one of five (equipment damage
  and out-of-phase reclosing are others). Don't label it the only reason.
- **S24, the "off-beat" test:** this is active frequency drift, which real inverters use. Other inverters use other
  active tests, so present it as one common method.
- **S26, "turns into heat — built for that":** a disconnected panel ran 3.7 °C warmer than a working one in a 2025
  study, and modules are rated −40 to +85 °C. If you show a number, show `+3.7 °C (ONE STUDY)`, nothing dramatic.
- **S29–S30, hybrid:** only the circuits wired to the backup output (fans, lights) are cut off from the street and
  powered. The rest of the house stays dark unless the whole house is wired to backup. A typical hybrid needs the
  battery: Solis's hybrid with no battery makes no power in an outage. The VO's definition (grid + battery) is fine.
- **S34, "the lineman … gets the shock":** this is a risk, not a certainty. But back-feed from a commercial inverter
  killed a lineman in Goa in 2024, even after he had switched off and earthed the line.

## On-screen label cautions
1. `≤ 2 s`: tag it CEA first for Indian viewers: `[CEA REG. 11(6)(e) | IEEE 1547 | IS 16169]`. The storyboard's
   `(IEEE 1547)` alone is weaker.
2. Off-beat HUD (storyboard `f 50.0 → 50.6 Hz → TRIP`; visual notes `50.0→50.3→50.7 Hz`): India's over-frequency
   trip is **50.5 Hz** (CEA 11(6)(b); a DISCOM may set it lower). Put the red line at 50.5 Hz, show no value above it,
   and label the drift `ILLUSTRATIVE`.
3. `230 V → 11,000 V` counter and `HT SIDE 0 → 11,000 V`: use `≈ 11,000 V` (S16).
4. Balance-scale shot ("panel output vs house use"): change it to the **street's use against all the panels' output**,
   with zero flow at the transformer, to match the new line 13.
5. Hybrid switchover time: show it only with a model label (Sungrow 3-phase: `< 20 ms`), or leave it out.
6. Panel wires: `STILL LIVE` with no voltage number. Anti-islanding setting: never show a real menu or steps (Deye's
   manual has a password-protected "Island" on/off item).
7. `50 Hz`, `230 V`, `CYCLE 20 ms` (1/50 s), `V = Voc · I = 0 A · P = 0 W` are all correct. `IRRADIANCE 1000 W/m²`,
   `DC BUS ~360 V` and `EXPORT +1.8 kW` stay `ILLUSTRATIVE`.

## The writer's list (script.md C1–C9)
- **C1 / C9:** confirmed by three sources:
  - CEA reg. 11(6)(e), from the Gazette of India, 30 Sep 2013, and unchanged by the 2019 amendment: "cease to
    energise the electricity system within two seconds of the formation of an unintended Island".
  - IEEE 1547-2018, cl. 8.1.1: "trip within 2 s".
  - IS 16169 / IEC 62116 pass rule: run-on time "less than 2 s".
- **C2:** confirmed. Anti-islanding is the law for every generator below 33 kV, rooftop solar included. Odisha's
  net-metering order applies it to rooftop PV, and MNRE's 2017 order makes inverters meet IS 16169. Wording note: the
  rule requires preventing *unintended* islands; it doesn't talk about "intentional islanding". IS 16221 (Part 2) is
  the inverter safety standard, not the islanding test, though some web guides mix them up.
- **C3:** confirmed: 230 V and 11 kV from two state supply codes, and 11/0.433 kV pole transformers from WBSEDCL's
  spec. Back-feed through a transformer is confirmed by IEA T5-09 and a U.S. OSHRC fatality case.
- **C4:** confirmed: IEA PVPS T5-09 (Bower, Sandia, and Ropp) covers active frequency drift and the non-detection
  zone.
- **C5:** confirmed: at open-circuit voltage the current is zero, so power is zero (EC&M, HyperPhysics). Heat: the
  2025 study and the Adani rating above.
- **C6:** confirmed: the Solis S6 manual ("opens the relay between itself and the grid") and the Sungrow factsheet.
- **C7:** confirmed: DMEGC and Adani module manuals.
- **C8:** confirmed: CEA definition of frequency ("alternating cycles per second") and Meghalaya's code ("50 HZ").

## Sources I could not open, and what I used instead (no VPN or proxy workarounds)
- **cea.nic.in:** now shows a login page. I used CBIP's copies: the Gazette scan and the consolidated 2013+2019 text.
  No later amendment was found. CEA's 2026 draft covers only connections at 33 kV and above.
- **PM Surya Ghar portal:** the connection was reset (503). I used Luminous, the OERC order and the CEA definitions
  instead.
- **nrel.gov:** blocked by the proxy. I used the U.S. DOE inverter page.
- **pveducation.org:** down (Cloudflare 521), and archive.org is blocked. I used EC&M, HyperPhysics, the 2025 Solar
  Energy Materials paper, Sinovoltaics and the Adani manual.

vo.txt was not edited. Nothing was committed.
