#!/usr/bin/env python3
"""Animated scene specs with exact program times (from align/program.json) -> scenes.json + scenes.md.

Each scene covers whole VO lines: it starts PRELAP s before its first line speaks and ends PRELAP s before the line
after its last line speaks (cut on the breath, PLAYBOOK §7), so the picture never has holes. Breaks inside or right
after a scene's lines (VO_PAUSE, DIEGETIC) are included. `cues` give each line's time *inside* the scene, so a session
can key its animation to the words without reading the alignment.

Sessions: A = 3D turbine and heat, B = 3D materials and cooling, C = blueprint world, D = globe and data graphics.
Everything not listed here (real footage, stills with motion, documents under the magnifier, title/end cards) is the
coordinator's (visual-plan.md).

  python3 projects/jet-engine-paradox/tools/scenes.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PRELAP = 0.15

# id: (session, first line, last line, title, spec)
SCENES = {
    # ---------- A: 3D turbine and heat (Three.js, thermal look) ----------
    "A1_title_blade": ("A", "J009", "J009", "Title: hero turbine blade",
        "Macro of one single-crystal high-pressure turbine blade glowing amber-hot in darkness, slow orbit, ember "
        "particles, heat shimmer. From 'Today, the story of...' (cue +2.5 s) the title THE JET ENGINE PARADOX burns in "
        "(amber edge glow into Ceramic White) and holds to the end. Leave the first 2.5 s clean (logo sting is overlaid "
        "at assembly). Corner tag: ILLUSTRATION."),
    "A2_engine_dive": ("A", "J045", "J045", "Dive into the engine",
        "Cutaway military turbofan (low-bypass, afterburner) in the blueprint-to-real transition: starts as amber "
        "wireframe on titanium slate, solidifies into metal as the camera dives through the fan, compressor stages and "
        "combustor into the glowing hot section. Ends inside the turbine stage (this scene runs through the 1.5 s block "
        "gap). Tag: ILLUSTRATION."),
    "A3_blade_rise": ("A", "J051", "J051", "The high-pressure turbine blade",
        "One HP turbine blade (twisted airfoil, platform, fir-tree root, rows of film-cooling holes on the leading edge) "
        "rises out of darkness, amber rim light, slow 360 turn. Label HIGH-PRESSURE TURBINE BLADE (lower left). "
        "Tag: ILLUSTRATION."),
    "A4_combustor_flow": ("A", "J052", "J052", "Combustor and hot gas",
        "Cutaway of the combustor annulus: fuel nozzles light, a flame front fills the liner, hot-gas particles stream "
        "through the nozzle guide vanes and across the rotating turbine blades (the blade from A3 now in its stage). "
        "Tag: ILLUSTRATION."),
    "A5_thermal_reveal": ("A", "J053", "J055", "Gas hotter than the metal's melting point (core reveal)",
        "J053: hold on the blade in its stage, everything slows. Then 1.5 s of stillness (music silence). At J054 the "
        "view switches to a thermal-camera look (ironbow palette): a vertical temperature scale at the right with a line "
        "labelled ALLOY MELTING POINT; the GAS reading climbs past it and stops 200 degrees above (label: GAS UP TO 200 °C "
        "ABOVE THE METAL'S MELTING POINT, tag [ROLLS-ROYCE | 2012]). No absolute temperatures. J055: push into the blade "
        "surface; a second readout METAL stays below the line (cool cyan film visible), ending on the question. "
        "Tag: ILLUSTRATION."),
    "A6_spin_bus": ("A", "J065", "J066", "Spin: 12,000 rpm and a London bus",
        "J065: the full turbine disc with its ring of blades spins up with motion blur; rpm counter climbs past 12,000 "
        "(> 12,000 RPM, tag [ROLLS-ROYCE | 2012]). J066: time freezes; a red double-decker bus silhouette (simple "
        "stylised low-poly, no branding) hangs by a cable from ONE blade tip, the blade bends a hair; label PULL ON ONE "
        "BLADE ≈ A LONDON BUS. Tag: ILLUSTRATION."),
    "A7_recap": ("A", "J067", "J067", "Recap triptych",
        "Three fast panels synced to the three phrases: (1) thermal blade with the melting-point line, (2) the bus "
        "hanging from a blade, (3) an hours counter spinning to 4,000+ beside the spinning disc. Panels slide in one by "
        "one with impacts, then merge into the single glowing blade."),
    "A8_verdict_blade": ("A", "J086", "J086", "Verdict: metal in gas above its melting point",
        "The A5 thermal blade spinning in its stage (blurred disc behind), rpm counter and an hours counter running; "
        "calm, wide, final. Tag: ILLUSTRATION."),

    # ---------- B: 3D materials and cooling ----------
    "B1_metal_zoom": ("B", "J056", "J056", "Into the metal",
        "Continuous zoom from the blade surface into the metal: the surface dissolves into a microscope view where "
        "crystal grains appear. Tag: ILLUSTRATION."),
    "B2_polycrystal": ("B", "J057", "J057", "Many crystals, weak borders",
        "Polycrystalline metal: 3D Voronoi grains (each a slightly different metallic tint, atoms visible as a fine "
        "lattice at different orientations per grain). Grain boundaries glow Warning Red as 'weak spots'. Labels: "
        "MANY CRYSTALS, then WEAK BORDERS. Tag: ILLUSTRATION."),
    "B3_creep": ("B", "J058", "J058", "Creep",
        "Heat (amber glow) and a pulling force (arrows) act on the grains; grains slide along the red boundaries and "
        "the sample stretches slowly; a small blade silhouette beside it lengthens. Label CREEP. Tag: ILLUSTRATION."),
    "B4_single_crystal": ("B", "J059", "J059", "One single crystal",
        "The grains merge into one perfect, unbroken atomic lattice (FCC-style spheres in one orientation), a light "
        "sweep runs through it with no boundary anywhere; pull back to the blade shape cast as one crystal. Label "
        "SINGLE CRYSTAL. Tag: ILLUSTRATION."),
    "B5_alloy": ("B", "J060", "J060", "Nickel superalloy + rhenium",
        "Element tiles (Ni, Co, Cr, Al, Ta, W, Re) orbit the blade like a periodic-table recipe; Ni largest; Re pulses "
        "amber on 'rhenium'. Label NICKEL SUPERALLOY · + RHENIUM. Tag: ILLUSTRATION."),
    "B6_cooling_channels": ("B", "J061", "J062", "Air: the cooling channels",
        "J061 'The second secret is air': the blade turns translucent (ghosted metal). J062: hollow interior revealed "
        "with serpentine cooling channels; cool compressor air (cyan #38BDF8 particles) enters at the root and snakes "
        "through. Label COOLING CHANNELS. Tag: ILLUSTRATION."),
    "B7_film_cooling": ("B", "J063", "J063", "Film cooling",
        "Close-up on rows of tiny holes on the leading edge; cyan air jets out and lays a thin blanket that wraps the "
        "blade surface while hot amber gas flows over it. Label FILM COOLING. Tag: ILLUSTRATION."),
    "B8_tbc": ("B", "J064", "J064", "Ceramic heat shield",
        "Cross-section through the blade wall: layers labelled HOT GAS / CERAMIC COATING / METAL / COOLING AIR; a "
        "ceramic-white layer seals over the metal; a colour gradient shows the temperature dropping through the wall "
        "(no numbers). Label THERMAL BARRIER COATING. Tag: ILLUSTRATION."),

    # ---------- C: blueprint world (2.5D line work) ----------
    "C1_empty_bay": ("C", "J004", "J004", "The empty engine bay",
        "Starts on a slot for the real hangar photo (params: background image, slow push) for the first ~2 s, then a "
        "precise amber wireframe of a single-engine delta-wing light fighter (generic, not a copy of HAL drawings) draws "
        "over it; the engine bay is a glowing empty cavity. Tag: ILLUSTRATION."),
    "C2_title_split": ("C", "J008", "J008", "Moon vs empty engine bay",
        "Split frame: left a slot for the real Chandrayaan-3 image (param), right the empty-bay wireframe; on 'Why can "
        "it not build its own fighter jet engine?' the line INDIA LANDED ON THE MOON. WHY NOT A JET ENGINE? burns in "
        "across the seam."),
    "C3_sanctions_wireframe": ("C", "J023", "J023", "1998: engines and flight-control help cut off",
        "Tejas prototype wireframe (same generic fighter, 1990s blueprint style); the engine block and a box labelled "
        "FLIGHT CONTROLS fade out with red STOPPED stamps. On-screen: F404 SALES STOPPED · FLIGHT-CONTROL HELP ENDED. "
        "Tag [AEROSPACEWEB | BUSINESS STANDARD]."),
    "C4_kaveri_blueprint": ("C", "J029", "J029", "1986: planning an engine",
        "1980s drafting-table blueprint: a GTX-35VS-style twin-spool afterburning turbofan side section draws itself "
        "stroke by stroke (generic, labelled ILLUSTRATION); stamp 1986 · GTRE, BENGALURU · PROPOSAL."),
    "C5_thrust_target": ("C", "J033", "J033", "Target: 81 kN",
        "The Kaveri blueprint; a thrust arrow grows out of the nozzle to a dashed target line TARGET THRUST 81 kN "
        "(tag [DELHI DEFENCE REVIEW | 2017])."),
    "C6_split_blueprint": ("C", "J034", "J034", "New jet and new engine at once",
        "Split blueprint: fighter airframe left, Kaveri engine right, both half-drawn and flickering, construction lines "
        "racing; on 'doubled the risk' both pulse red."),
    "C7_blueprint_tear": ("C", "J041", "J041", "Delinked, September 2008",
        "First ~4 s: slot for the credited headline image (param) under a slow push; then the Kaveri blueprint tears "
        "away from the Tejas blueprint; a different engine block (labelled US ENGINE) slides into the airframe. "
        "On-screen SEP 2008 · KAVERI DELINKED FROM TEJAS."),
    "C8_dry_kaveri": ("C", "J072", "J073", "The Dry Kaveri",
        "J072: the afterburner section slides off the Kaveri blueprint; label DRY KAVERI · NO AFTERBURNER. J073: thrust "
        "bar fills past a 46 kN target line to ~48.5 kN (on-screen ~48.5 kN · TARGET 46 kN, tag [ORF | THE WEEK | 2026])."),
    "C9_amca_engines": ("C", "J078", "J079", "AMCA: F414 now, 120 kN later",
        "J078: twin-engine stealth fighter wireframe (generic, AMCA-like planform) with two engines labelled GE F414 "
        "(AMCA MK1 · GE F414). J079: those engines dissolve; a clean-sheet engine wireframe draws itself, label AMCA MK2 "
        "· 120 kN CLASS, then INDIAN DESIGN, INDIAN RIGHTS."),

    # ---------- D: globe and data graphics ----------
    "D1_globe_lynn": ("D", "J007", "J007", "Lynn to Bengaluru",
        "Land-only globe (no political borders, Natural Earth land, see video/fireice/benson_map/mkmap.mjs) on titanium "
        "slate, slow turn; amber great-circle arc from Lynn, USA to Bengaluru with a distance counter to ~13,000 KM; "
        "labels LYNN, USA and BENGALURU; tag (OUR CALCULATION) [GE AEROSPACE | OUR CALCULATION]."),
    "D2_squadrons": ("D", "J011", "J011", "42 vs 29 squadrons",
        "42 squadron slots (fighter silhouettes in a grid); 29 fill amber, 13 stay empty and pulse red; counters "
        "SANCTIONED 42 · ACTUAL ~29; tag [THE WIRE | NEW INDIAN EXPRESS | 2026]."),
    "D3_orders": ("D", "J013", "J013", "83 + 97 = 180 jets",
        "Two order stamps 2021: 83 and 2025: 97 drop in, sum counter to 180 JETS; fighter icons fill rows; "
        "tag [MOD / PIB | 2021, 2025]."),
    "D4_promise": ("D", "J015", "J015", "Promised 2023, first engine March 2025",
        "Horizontal timeline 2021–2026: PROMISED 2023 marker, the delivery marker slides right to MAR 2025; the gap fills "
        "red; tag [BLOOMBERG | GE AEROSPACE]."),
    "D5_engines_jets": ("D", "J017", "J017", "14 of 99 engines, 29 jets",
        "99 small engine icons, 14 light up amber (ENGINES SENT: 14 OF 99); beside them 29 jet icons waiting in grey "
        "(JETS BUILT: 29); tag [GE AEROSPACE | NEW INDIAN EXPRESS | HAL CMD | OCT 2026]."),
    "D6_bomb_space": ("D", "J026", "J026", "Nine nuclear states, about ten launchers",
        "Land-only globe; big counter 9 (NUCLEAR-ARMED STATES) then ~10 (OWN ROCKET TO ORBIT) with abstract pulses on "
        "the globe (no country labels, no borders); tag [SIPRI 2026 | AP 2022]."),
    "D7_engine_club": ("D", "J027", "J027", "The engine club",
        "Land-only globe: five glowing markers appear one by one as the VO names them, each with its makers: "
        "USA (GE · PRATT & WHITNEY), RUSSIA (UEC SATURN · KLIMOV), BRITAIN (ROLLS-ROYCE), FRANCE (SAFRAN), and after a "
        "beat CHINA (AECC). India outlined in faint amber, empty. Title THE ENGINE CLUB; tag [KED GLOBAL | CLAWS]."),
    "D8_russia_route": ("D", "J038", "J039", "No altitude test facility: to Russia",
        "J038: India on the land globe with a crossed-out altitude-chamber icon (NO HIGH-ALTITUDE TEST FACILITY). "
        "J039: amber arc Bengaluru → Moscow region (label CIAM · GROMOV, ZHUKOVSKY) with a crate icon travelling it; "
        "tag [BUSINESS STANDARD 2009 | PIB 2015]."),
    "D9_weight": ("D", "J036", "J036", "1,100 kg target, 1,235 kg actual",
        "Precision scale / dial: needle swings past 1,100 KG TARGET to 1,235 KG ACTUAL; overweight band glows red; "
        "tag [CAG | 2010]."),
    "D10_thrust": ("D", "J037", "J037", "81 kN target, about 70 reported",
        "Thrust bar fills to ~70 kN and stalls short of the dashed 81 kN line; on-screen 81 kN TARGET · ~70 kN REPORTED; "
        "tag [RAKSHA ANIRVEDA | DELHI DEFENCE REVIEW]."),
    "D11_years": ("D", "J040", "J040", "The years went by",
        "Mechanical flip-calendar years 1996 → 2008 flipping, dust motes in a dim test cell light."),
    "D12_cost": ("D", "J044", "J044", "₹382 crore → ₹2,839 crore",
        "Counter climbs ₹382 CR → ₹2,839 CR (estimate) with a second bar ₹1,996 CR SPENT BY 2012; "
        "tag [PIB | 2012]. Use latin-ext Inter for ₹."),
    "D13_hours": ("D", "J050", "J050", "Thousands of hours",
        "Split counters: ROCKET: MINUTES (stops) vs JET ENGINE: THOUSANDS OF HOURS (spins to 4,000+); tag [GE AEROSPACE]."),
    "D14_paris_derby": ("D", "J080", "J082", "Safran picked; deal awaits approval",
        "J080: land globe, amber arc Paris → Bengaluru, SAFRAN + GTRE · SELECTED AUG 2025. J081: label FULL INDIAN IP "
        "stamps. J082: status chip AWAITING FINAL APPROVAL · OCT 2026, then a second arc Derby, UK → India labelled "
        "ROLLS-ROYCE + RELIANCE · AUG 2026; tag [NEW INDIAN EXPRESS | AUG, OCT 2026]."),
    "D15_china": ("D", "J083", "J083", "China's road",
        "Timeline over a slot for the J-20 photo (param): RUSSIAN AL-31F → CHINESE WS-10C → WS-15 as three engine chips "
        "lighting in turn, years axis without exact dates; tag [THE DEFENSE POST 2021 | DEFENSE MAGAZINE 2026]."),
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
    json.dump(out, open(HERE / "scenes.json", "w"), indent=1, ensure_ascii=False)
    with open(HERE / "scenes.md", "w", encoding="utf-8") as f:
        f.write("# Animated scenes: The Jet Engine Paradox\n\nBuilt by `tools/scenes.py` from `align/program.json`; "
                "do not edit by hand. Times are program seconds; `cues` are seconds inside the scene.\n\n")
        for s in "ABCD":
            items = [(k, v) for k, v in out.items() if v["session"] == s]
            f.write(f"\n## Session {s}: {len(items)} scenes, {sum(v['duration'] for _, v in items):.1f} s\n")
            for k, v in items:
                f.write(f"\n### {k} · {v['title']} · {v['duration']:.2f} s (program {v['start']:.2f}–{v['end']:.2f}, "
                        f"lines {v['lines']})\n{v['spec']}\n")
                for c in v["cues"]:
                    f.write(f"- +{c['at']:.2f}–{c['to']:.2f} {c['id']}: “{c['vo']}”"
                            + (f" · on-screen `{c['onscreen']}`" if c["onscreen"] else "") + "\n")
                for b in v["breaks"]:
                    f.write(f"- +{b['at']:.2f} {b['kind']} {b['len']} s: {b['note']}\n")
    tot = {s: sum(v["duration"] for v in out.values() if v["session"] == s) for s in "ABCD"}
    print(f"{len(out)} scenes; seconds per session: {tot}")


if __name__ == "__main__":
    main()
