#!/usr/bin/env python3
"""Animated scene specs with exact program times (from align/program.json) -> scenes.json + scenes.md.

Each scene covers whole VO lines: it starts PRELAP s before its first line speaks and ends PRELAP s before the line
after its last line speaks (cut on the breath, PLAYBOOK §7), so the picture never has holes. Breaks inside or right
after a scene's lines are included. `cues` give each line's time *inside* the scene, so a session can key its animation
to the words without reading the alignment. Break scenes (title, chapter cards) have their own fixed durations.

Sessions: A = 3D hardware world (Three.js), B = braking and fog telemetry, C = crash forensics, D = rollout data and
animated maths, E = phone UI, stamps, title and chapter cards. Everything else (real footage, documents under the
magnifier, the end card) is the coordinator's (visual-plan.md). On-screen text comes from script.full.tsv (fact-checked):
sessions must not change it.

  python3 projects/kavach-railway-reality/tools/scenes.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PRELAP = 0.15

# id: (session, first line, last line, title, spec)
SCENES = {
    # ---------- A: 3D hardware world (Three.js, "Signal Room") ----------
    "A1_atp_watch": ("A", "V010", "V010", "Kavach watches speed and signals, warns, then brakes",
        "A WAP-7-style electric loco (generic, no livery text) hauling a short rake on a 3D ballasted track at dusk; "
        "camera orbits from 3/4 front. Floating cab-display telemetry (cyan) above the cab: PERMITTED SPEED and the "
        "next signal with its distance. On 'too fast or is about to pass a red signal' the signal ahead turns red and the "
        "telemetry flashes amber WARNING; on 'then brakes by itself' a cyan pulse runs from the Kavach unit into the "
        "brake pipe, brake blocks glow, sparks, the speed dial needle drops. Label AUTOMATIC TRAIN PROTECTION. "
        "Tag: ILLUSTRATION."),
    "A2_four_links": ("A", "V012", "V012", "A chain of four links",
        "The train from A1 in a dark void; four glowing cyan chain links assemble around it one by one, each tied to "
        "its place (track sleeper, station building, radio tower, loco cab). On 'every link is in place' the chain "
        "closes and the whole rig lights. Keep the four positions: they return in A9. Tag: ILLUSTRATION."),
    "A3_rfid_tags": ("A", "V013", "V013", "Link one: RFID tags on the sleepers",
        "Low tracking shot along concrete (PSC) sleepers; a yellow-black RFID tag box between the rails; the loco's "
        "under-chassis reader (X-ray view through the bogie) passes over it, a radio field ring lights the tag, and two "
        "small chips pop: TAG ID and TRACK ID, then a map pin snaps onto the line ('exactly where it is and on which "
        "line'). Label LINK 1 · RFID TAG. Tag: ILLUSTRATION."),
    "A4_station_interlock": ("A", "V015", "V015", "Link two: station Kavach reads interlocking",
        "Station cutaway: a relay room / interlocking cabinet and a Kavach cabinet beside it; live wires carry signal "
        "aspects (red/yellow/green), point positions and track-occupied states into the Kavach box as flowing light. "
        "On 'called interlocking' the word INTERLOCKING lights on the cabinet and stays lit; a slow push-in on it for "
        "'Remember that word'. Label LINK 2 · INTERLOCKING. Tag: ILLUSTRATION."),
    "A5_radio_tower": ("A", "V016", "V016", "Link three: UHF safety radio",
        "Tilt up a lattice telecom tower beside the track at night; radio pulses (cyan rings) travel between the "
        "station, the tower and the moving loco. On 'it's not your mobile network, and it's not five G' a phone-network "
        "badge and a 5G badge float in and grey out. Label LINK 3 · UHF DATA RADIO. Tag: ILLUSTRATION."),
    "A6_loco_xray": ("A", "V017", "V017", "Link four: the loco unit, exploded",
        "The loco shell peels away layer by layer (X-ray, cyan edges): each part lights and labels in on its word: "
        "KAVACH COMPUTER, RFID READERS (under the bogie), WHEEL SPEED SENSORS (on the axle), CAB SCREEN, BRAKE LINK. "
        "Label LINK 4 · LOCO KAVACH. Tag: ILLUSTRATION."),
    "A7_info_arrow": ("A", "V020", "V020", "Kavach acts only on the information it is given",
        "The four-link rig, wide: a single data arrow travels from the station interlocking into the Kavach box and "
        "glows; the camera holds on it while everything else dims. Ends on a slow dim to black (chapter card follows). "
        "Tag: ILLUSTRATION."),
    "A8_brake_pipe": ("A", "V022", "V022", "Low grip, heavy train, brake pipe",
        "Macro of a steel wheel on a steel rail (the tiny contact patch glows), then pull back along a long rake; on "
        "'when the brakes go on' an air-pressure wave travels down the brake pipe coach by coach (cyan → amber as it "
        "goes) to the last coach. Label BRAKE PIPE. Tag: ILLUSTRATION."),
    "A9_links_relight": ("A", "V058", "V058", "Kavach needs four things",
        "The rig from A2 at dawn light: on the four phrases the links relight one by one: ENGINE (loco cab), TRACK "
        "(sleepers), DATA (interlocking), DISTANCE (a braking ruler drawn ahead of the train). On-screen "
        "`ENGINE · TRACK · DATA · DISTANCE` as four small labels at their links. Tag: ILLUSTRATION."),

    # ---------- B: braking and fog telemetry (SVG/GSAP or canvas, cab-display grammar) ----------
    "B1_braking_ruler": ("B", "V023", "V023", "Vande Bharat: 654 m from 130 km/h",
        "Side-on train silhouette (Vande Bharat nose shape, no livery text) runs left to right over a track ruler; on "
        "'about six hundred and fifty metres' the brake point fires and a speed-vs-distance curve draws from 130 KM/H "
        "to 0 along a 0–700 m ruler, landing at 654 M. Leave the first ~4 s for a document insert (coordinator overlays "
        "the IRIMEE table); keep motion behind it. On-screen `VANDE BHARAT · 130 KM/H · EMERGENCY BRAKE 654 M`."),
    "B2_curve_stretch": ("B", "V026", "V026", "130 → 160 km/h: about half again",
        "The B1 curve (130 km/h) stays as a ghost; a second curve from 160 km/h draws and stretches about 1.5× as far; "
        "a bracket labels +50%. Generic distances (no metres on this one), amber for the longer curve. On-screen `+50%`. "
        "Tag: ILLUSTRATIVE CURVE."),
    "B3_fog_split": ("B", "V028", "V028", "Fog: 50 m in about 1.6 s",
        "Split screen. Left: windscreen view into dense fog (procedural fog over a param plate `fog.mp4` if supplied, "
        "else a layered fog shader), a signal emerges at 50 m; a stopwatch races and runs out at 1.6 s as the train "
        "passes it. Right half stays dark until B4. On 'needs a second or two just to react' a reaction bar fills; on "
        "'On eyes alone' a red cross. On-screen `VISIBILITY 50 M · EXAMPLE · ≈ 1.6 S`. Tag: ILLUSTRATION."),
    "B4_kavach_curve": ("B", "V029", "V029", "Kavach knows the signal ahead and brakes early",
        "Right half of the split lights: the cab display (LP-OCIP grammar: target distance counting down, permitted "
        "speed, signal aspect) shows the red signal long before it is visible; then a full-width braking curve draws "
        "ahead of the train with the Kavach brake point well before the signal and the stop short of it. On-screen "
        "`TARGET DISTANCE`. Tag: ILLUSTRATION."),
    "B5_cant_cancel_physics": ("B", "V030", "V030", "Danger inside the stopping distance",
        "The curve from B4; an obstacle appears inside the curve's reach; the zone between obstacle and stop point "
        "washes crimson; the curve cannot bend in time. No label needed. Tag: ILLUSTRATION."),
    "B6_spad_counter": ("B", "V031", "V031", "208 red-signal passings, 12 collisions",
        "A red signal lamp at night (graphic); a counter rolls 0 → 208 across a timeline APR 2019 → MAR 2024 (each "
        "case a small tick); on 'twelve of them' 12 ticks turn crimson and pulse. Leave room upper half for a document "
        "insert the coordinator may overlay. On-screen `208 CASES · 2019–2024 · 12 COLLISIONS`."),

    # ---------- C: crash forensics (2.5D logic diagrams) ----------
    "C1_balasore_layout": ("C", "V040", "V041", "Bahanaga Bazar: green for the main line, crossover to the loop",
        "Top-down 2.5D station schematic (not a map trace): up main line, loop line with a parked goods train, "
        "crossover 17A/B, the home signal. V040: the Coromandel arrow approaches on the up main (≈ 128 KM/H readout) and "
        "the home signal turns green. V041: the crossover points swing towards the loop; the parked goods train "
        "highlights crimson. Leave the first ~3 s for archive the coordinator cuts in. On-screen "
        "`BAHANAGA BAZAR · 2 JUN 2023 · ≈ 128 KM/H`, then `CROSSOVER 17A/B → LOOP`. Tag: ILLUSTRATION."),
    "C2_would_kavach": ("C", "V043", "V043", "So, would Kavach have stopped it?",
        "The C1 schematic frozen; a cyan Kavach box appears on the loco and pulses slowly. Includes the 1.5 s total "
        "silence: keep it still but alive (slow pulse, drifting dust). Ends on a cut."),
    "C3_false_green": ("C", "V045", "V046", "Same wrong input, same answer",
        "V045: the interlocking feed lights; the false green travels down the wire into the Kavach box, which shows "
        "green too (`SAME INPUT · SAME ANSWER?`). V046: two parallel safety channels inside Kavach both agree on the "
        "wrong input and a gate opens; then dotted, uncertain tag-read marks appear on the loop line "
        "(`UNTESTED COUNTERFACTUAL`). Tag: ILLUSTRATION."),
    "C4_signals_fail": ("C", "V048", "V048", "Rangapani: automatic signals failed",
        "A line of automatic signals along a single track blinks out one by one (power-down); a generic paper "
        "authority slip (no copy of a real form, just a blank slip with a stamp shape) slides in; trains shown as slow "
        "arrows. Leave the first ~3 s for archive. On-screen `RANGAPANI · 17 JUN 2024 · SIGNALS FAILED`. "
        "Tag: ILLUSTRATION."),
    "C5_wrong_form": ("C", "V049", "V049", "Wrong form, no caution order, missing walkie-talkies, training",
        "Two distinct form labels T/A 912 and T/D 912 side by side; the wrong one (T/A 912) is handed to the goods "
        "train arrow and highlights crimson. Then three items tick crimson around the station: CAUTION ORDER, "
        "WALKIE-TALKIES, TRAINING. On-screen `T/A 912 ≠ T/D 912`. Tag: ILLUSTRATION."),
    "C6_speed_trace": ("C", "V050", "V050", "78 km/h, hit at about 40",
        "Speed-vs-time trace for the goods train climbs to 78, then the collision marker at about 40 behind the "
        "passenger train; a schematic map strip shows no Kavach line on this section. On-screen "
        "`78 KM/H → ≈ 40 KM/H · NO KAVACH HERE`. Tag: ILLUSTRATION."),
    "C7_rewind_sim": ("C", "V051", "V051", "With Kavach: held to a slow speed",
        "The C6 scene rewinds (tape-rewind feel); a cyan Kavach box appears on both locos; the goods train's speed is "
        "held low past the failed signals and its braking curve stops it short of the passenger train. On-screen "
        "`SIMULATION` (small, in-scene; the assembler also tags it)."),
    "C8_two_failures": ("C", "V053", "V053", "Two crashes, two failures",
        "Two columns: left WRONG INPUT (a crimson false green feeding a box), right BROKEN BACKUP (dark signals and a "
        "torn paper slip); on 'Kavach is strongest against the second kind' the right column gets a cyan shield. "
        "On-screen `WRONG INPUT · BROKEN BACKUP`."),

    # ---------- D: rollout data and animated maths ----------
    "D1_tag_spacing": ("D", "V014", "V014", "Max gap 1 km; 2,872 tags on 96 km",
        "First half: evenly spaced dots along a line get a red cross; then the dots regroup, clustering thickly around a "
        "signal and a turnout (`MAX GAP 1 KM`). Second half (animated, no whiteboard; owner 2026-10-16): whip pan to a 96 km "
        "Vadodara–Ahmedabad strip that fills with 2,872 amber tags (counter), then a lens magnifies 1 km: ≈ 30 tags. On-screen "
        "`MAX GAP 1 KM · 96 KM · 2,872 TAGS`."),
    "D2_board_speed": ("D", "V024", "V024", "130 km/h = 36 m every second",
        "Real time, real scale: a trainset at 130 km/h passes a post every second, 36 m brackets light up, stopwatch and "
        "metres counter. Lower-third `130 KM/H · OUR CALCULATION 130 ÷ 3.6 ≈ 36 M/S`."),
    "D3_board_freight": ("D", "V025", "V025", "Freight ≈ 930 m (illustrative model)",
        "Close tracking shot of a loaded goods train at 75 km/h pulls out (time-lapse) to a 1 km ruler: the brake "
        "application travels back along the wagons, amber zone `≈ 208 m` (brakes build up, 10 s) then crimson `≈ 723 m` "
        "under a speed curve, total bracket `≈ 930 m`; readouts km/h, metres, real seconds. Tag: OUR CALCULATION."),
    "D4_network_size": ("D", "V032", "V032", "The size of the job",
        "Land-only India map (no political borders), carbon slate; the rail network draws in as thin grey lines across "
        "the country; counters land on the words: 69,439 ROUTE KM, then ≈ 16,000 LOCOS · MAR 2025. On-screen "
        "`69,439 ROUTE KM · ≈ 16,000 LOCOS · MAR 2025`. Rail lines: generic network density, labelled ILLUSTRATIVE "
        "if not from a real dataset."),
    "D5_corridors": ("D", "V033", "V033", "Kavach 4.0: 2,633 route km",
        "Same map; two corridors glow cyan: Delhi → Mumbai (label 1,423 KM GROUP) and Delhi → Howrah (1,210 KM GROUP); "
        "counter to 2,633. On-screen `KAVACH 4.0 · 2,633 RKM · 31 JUL 2026`."),
    "D6_under_tenth": ("D", "V034", "V034", "Plus the older version: under a tenth",
        "Same map: a South Central Railway section glows in a second colour (amber-cyan); then a 10×10 grid "
        "(1 square = 1% of the network) lights ≈ 5.9% against a dashed ONE TENTH row. On-screen `VERSION 3.2 · 1,465 RKM · UNDER 10%`."),
    "D7_funnel": ("D", "V035", "V035", "Fitted ≠ working",
        "Three headline strips slide in, blurred except their numbers; then a funnel: WORK STARTED 21,794 (widest), "
        "FITTED 7,726, LOCOS 6,290, narrowing to the thin cyan WORKING stream; stamp `FITTED ≠ WORKING` lands on "
        "'fitted isn't working'. On-screen `FITTED 7,726 · LOCOS 6,290 · WORK STARTED 21,794 · FITTED ≠ WORKING`."),
    "D8_budget": ("D", "V036", "V036", "Budget ₹1,112.57 cr → ₹1,673.19 cr",
        "Two precision bars rise with tabular counters: 2024–25 ₹1,112.57 CR, 2025–26 ₹1,673.19 CR. On-screen "
        "`₹1,112.57 CR (2024–25) → ₹1,673.19 CR (2025–26)`. Use latin-ext Inter for ₹."),
    "D9_commissioning_loop": ("D", "V037", "V037", "Money alone doesn't make it work",
        "Flowchart drawn as a rail line: SURVEY → SIGNAL DATA → LOCO BRAKES → RADIO → TEST; a train token runs it, "
        "fails at TEST, loops back twice (FIX → RETEST), then reaches COMMISSIONED, which lights cyan. "
        "On-screen `COMMISSIONED`."),

    # ---------- E: phone UI, stamps, title and chapter cards ----------
    "E1_family_group": ("E", "V003", "V003", "Crash news blows up the family WhatsApp group",
        "Realistic Android phone on a kitchen table (3D-ish, shallow depth of field); a generic news alert (no real "
        "outlet name) then a family group chat (generic names: Amma, Ravi Bava, Chinni…) with previews stacking fast "
        "and the unread counter climbing. Not WhatsApp branding: a generic green chat app."),
    "E2_two_forwards": ("E", "V004", "V004", "Two forwards",
        "Split screen of two forwarded messages (generic, 'Forwarded many times' style tag): left NO KAVACH? WHY?, "
        "right KAVACH = ZERO ACCIDENTS; on-screen `MYTH 1 · MYTH 2`. Keep the two cards: they return in E6."),
    "E3_crack": ("E", "V005", "V005", "Both forwards crack",
        "The two forwards crack like glass on 'missing what really happens'; crash zoom through the crack into a dark "
        "night track bed (param `trackbed.mp4`, else a procedural ballast-and-rail plate with moonlight)."),
    "E4_not_an_app": ("E", "V009", "V009", "Not an app, no overnight switch",
        "A phone app icon labelled KAVACH dissolves into steel hardware parts; then a big industrial switch flips over "
        "a dim India map (land only) and nothing lights up. On-screen `NOT AN APP`."),
    "E5_sil_half_story": ("E", "V019", "V019", "SIL-4: half the story",
        "First half: a standards page (generic, styled like an EN document, no copied text) under a magnifier, the SIL "
        "band row highlighted; SIL-4 lands. Second half: a viral post card ONE FAILURE IN A BILLION HOURS slides in and a "
        "rubber stamp HALF THE STORY lands (.kav-stamp); then the SIL target lights one box in a small chain diagram, "
        "not the whole railway. On-screen `SIL-4 · HALF THE STORY`."),
    "E6_beyond_evidence": ("E", "V047", "V047", "Both forwards: beyond the evidence",
        "The two forwards from E2 return side by side; each gets a stamp BEYOND THE EVIDENCE. On-screen "
        "`BEYOND THE EVIDENCE`."),
    "E7_depends_setup": ("E", "V052", "V052", "The 'always 15 km/h' claim",
        "A claim card 'KAVACH ALWAYS LOCKS 15 KM/H' (forward style) slides in; a speedometer graphic shows 15; then a "
        "stamp DEPENDS ON SET-UP lands. On-screen `DEPENDS ON SET-UP`."),
    "E8_three_questions": ("E", "V055", "V055", "Three questions before you share",
        "The forward from E2 on the phone; three question chips pop beside it on each question: FITTED OR WORKING? · "
        "WHICH DATE? · HUMAN OR SIGNAL DATA?; a small step marker 1 in a lower corner. On-screen "
        "`1 · FITTED OR WORKING? · WHICH DATE? · HUMAN OR SIGNAL DATA?`."),
    "E9_pinned_question": ("E", "V060", "V060", "Pinned comment question",
        "A comment card (generic YouTube-like comment UI, no logo) in a lower corner over a slowly drifting land-only "
        "India rail map; text WHICH ROUTE DO YOU TRAVEL? On-screen `WHICH ROUTE DO YOU TRAVEL?`."),
}

# Break scenes: (session, break after line, title, spec). Duration = the break length + PRELAP each side.
BREAK_SCENES = {
    "E10_title": ("E", "V008", "Title: THE KAVACH RAILWAY REALITY",
        "Title rises out of a night track bed (ballast, rails catching moonlight, a cyan Kavach tag glint): THE KAVACH "
        "RAILWAY REALITY in Inter 800, crisp white with a cyan scan line. Starts on the breath after V008."),
    "E11_ch_physics": ("E", "V020", "Chapter card: THE PHYSICS",
        "One parametrised chapter-card composition (params: text, accent) used four times: a short cyan rail-track "
        "line draws across a moving slate texture and the chapter word lands; no centred title+subtitle cliché: "
        "lower-left, big, with a chapter number."),
    "E12_ch_rollout": ("E", "V031", "Chapter card: THE ROLLOUT", "Same composition as E11, text THE ROLLOUT."),
    "E13_ch_crashes": ("E", "V038", "Chapter card: TWO CRASHES", "Same composition as E11, text TWO CRASHES, crimson accent."),
    "E14_ch_action": ("E", "V053", "Chapter card: WHAT YOU CAN DO", "Same composition as E11, text WHAT YOU CAN DO, amber accent."),
}


def main():
    p = json.load(open(HERE / "align/program.json"))
    L = {l["id"]: l for l in p["lines"]}
    order = [l["id"] for l in p["lines"]]
    out = {}
    for sid, (sess, a, b, title, spec) in SCENES.items():
        i, j = order.index(a), order.index(b)
        start = max(0.0, L[a]["start"] - PRELAP)
        end = (L[order[j + 1]]["start"] - PRELAP) if j + 1 < len(order) else p["total"]
        cues = [dict(id=x, at=round(L[x]["start"] - start, 2), to=round(L[x]["end"] - start, 2), vo=L[x]["en"],
                     onscreen=L[x]["onscreen"], cite=L[x]["cite"]) for x in order[i:j + 1]]
        brk = [dict(kind=k["kind"], at=round(k["start"] - start, 2), len=k["len"], note=k["note"]) for k in p["breaks"]
               if start <= k["start"] < end]
        out[sid] = dict(session=sess, title=title, start=round(start, 2), end=round(end, 2),
                        duration=round(end - start, 2), lines=f"{a}-{b}", cues=cues, breaks=brk, spec=spec)
    B = {k["after"]: k for k in p["breaks"]}
    for sid, (sess, after, title, spec) in BREAK_SCENES.items():
        k = B[after]
        out[sid] = dict(session=sess, title=title, start=round(k["start"], 2), end=round(k["start"] + k["len"], 2),
                        duration=round(k["len"], 2), lines=f"break after {after}", cues=[],
                        breaks=[dict(kind=k["kind"], at=0.0, len=k["len"], note=k["note"])], spec=spec)
    json.dump(out, open(HERE / "scenes.json", "w"), indent=1, ensure_ascii=False)
    with open(HERE / "scenes.md", "w", encoding="utf-8") as f:
        f.write("# Animated scenes: The Kavach Railway Reality\n\nBuilt by `tools/scenes.py` from `align/program.json`; "
                "do not edit by hand. Times are program seconds; cues are seconds inside the scene. Break scenes (title, "
                "chapter cards) sit in picture-only gaps: the scene before/after them is cut by the assembler.\n")
        for s in "ABCDE":
            items = [(k, v) for k, v in out.items() if v["session"] == s]
            f.write(f"\n## Session {s}: {len(items)} scenes, {sum(v['duration'] for _, v in items):.1f} s\n")
            for k, v in items:
                f.write(f"\n### {k} · {v['title']} · {v['duration']:.2f} s (program {v['start']:.2f}–{v['end']:.2f}, "
                        f"lines {v['lines']})\n{v['spec']}\n")
                for c in v["cues"]:
                    f.write(f"- +{c['at']:.2f}–{c['to']:.2f} {c['id']}: “{c['vo']}”"
                            + (f" · on-screen `{c['onscreen']}`" if c["onscreen"] else "")
                            + (f" · cite (assembler) {c['cite']}" if c["cite"] else "") + "\n")
                for b in v["breaks"]:
                    f.write(f"- +{b['at']:.2f} {b['kind']} {b['len']} s: {b['note']}\n")
    tot = {s: round(sum(v["duration"] for v in out.values() if v["session"] == s), 1) for s in "ABCDE"}
    print(f"{len(out)} scenes; seconds per session: {tot}")


if __name__ == "__main__":
    main()
