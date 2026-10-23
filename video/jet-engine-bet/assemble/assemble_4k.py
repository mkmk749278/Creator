#!/usr/bin/env python3
"""Final 4K assembly of "India's jet engine bet" (film v2) to the owner's voice-over.

What changed from assemble.py (v0/v1), after review_film_independent_v1.md:
- native 3840x2160 output; every label, number, credit tag and the logo bug is drawn at 4K (labels4k.py) and composited here,
  so text is sharp even where the 3D under it was rendered at 1080p and upscaled (PLAYBOOK §13, §9.4 Kavach recipe);
- real footage first: DD India (HAL Nashik line), PIB, IAF, ISRO, GE/US Navy F404, MoD/Commons photos (media_manifest.csv),
  with the CG walk-around (R1v3_walk, the real Tejas airframe) only where no camera can go;
- every on-screen number matches the voice; stills always move (Ken Burns + handheld drift, never a still > 1.5 s);
- a gate: the picture must cover the whole voice-over (v1's 720p copy stopped at 3:49).
Each shot is rendered to its own cached 4K segment (identical encode settings), then the segments are joined with the concat
demuxer and muxed with the mixed audio.
  python3 video/jet-engine-bet/assemble/assemble_4k.py [--only N[,M..]] [--preview] [--out film.mp4] [--audio mix.wav]
"""
import argparse, hashlib, json, subprocess, sys, math, os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import cv2
sys.path.insert(0, str(Path(__file__).parent))
import labels4k as L

ROOT = Path(__file__).resolve().parents[3]
VJ = ROOT / "video/jet-engine-bet"
LEG = ROOT / "projects/jet-engine-bet/assets/legacy"; SC = LEG / "scenes"; SRC = LEG / "sources"
REAL = ROOT / "projects/jet-engine-bet/assets/real"
WK = VJ / "work"
OUT = VJ / "assemble/work4k"
VO = ROOT / "projects/jet-engine-bet/final/jeb_vo_final.mp3"
W, H, FPS = 3840, 2160, 30
END = 514.2   # 510.2 sign-off end + 4 s end card
RENDER_VERSION = 3   # bump when the render logic (not the edit) changes, to invalidate the shot cache
ENC = ["-c:v", "libx264", "-preset", "fast", "-crf", "17", "-maxrate", "35M", "-bufsize", "70M", "-pix_fmt", "yuv420p",
       "-r", str(FPS), "-g", "60", "-profile:v", "high", "-level", "5.1", "-x264-params", "keyint=60:min-keyint=60:scenecut=0"]

# ---------------------------------------------------------------- sources -------------------------------------------------
def sc(p): return SC / p
def real(p):
    """Commons files are named <query>_<index>_<slug>: match on <query>_<index>_ so a truncated slug still resolves."""
    if (REAL / p).exists(): return REAL / p
    parts = p.split("_")
    hits = sorted(REAL.glob(f"{parts[0]}_{parts[1]}_*")) if len(parts) > 2 else []
    return hits[0] if hits else REAL / p
DD = SRC / "YfQNVWn8aIc.mp4"; PIB = SRC / "ryolgbuDNSg.mp4"; ISRO_M = SRC / "DLA_64yz8Ss.mp4"; ISRO_L = SRC / "q2ueCg9bvvQ.mp4"
IAF_MIG = SRC / "52f1mQqaii8.mp4"; IAF_FL = SRC / "zCYBJtBaUXw.mp4"; GE = SRC / "HcskFT8ngSQ.mp4"
R1 = WK / "R1v3_walk.mp4"; R2 = WK / "R2_engine_journey.mp4"
CROP_DD = (0.10, 0.0, 0.80, 0.80)     # above DD India's lower-third and ticker
CROP_PIB = (0.12, 0.08, 0.76, 0.76)   # clear of the PIB logo and the boxed captions
C_DD, C_PIB, C_ISRO, C_IAF, C_MOD = "Video: DD India", "Video: PIB India", "Video: ISRO", "Video: Indian Air Force", "Photo: Ministry of Defence (GODL-India)"

MANIFEST = {}
if (REAL / "manifest.json").exists():
    for m in json.loads((REAL / "manifest.json").read_text()): MANIFEST[m["file"]] = m


def credit_of(name):
    """On-screen attribution for a Commons photo (CC BY / BY-SA need it; the description carries no credits, CLAUDE.md)."""
    m = MANIFEST.get(name)
    if not m: return None
    lic = " ".join(m.get("licence", "").split())
    if lic.upper().startswith("GODL"): return "Photo: Ministry of Defence (GODL-India)"
    a = " ".join((m.get("author") or "").split())
    for junk in ("The original uploader was ", " at English Wikipedia.", "Parent institution", "Unknown author"):
        a = a.replace(junk, "")
    a = a.split(" -- ")[0].split("http")[0]
    if "U.S. Navy" in a: a = "U.S. Navy"
    if "Department of Defense" in a: a = "U.S. Department of Defense"
    a = a.strip(" .·")[:34]
    if lic.lower().startswith(("public domain", "pd")): return f"Photo: {a or 'Wikimedia Commons'} (public domain)"
    return f"Photo: {a} · {lic} · Wikimedia Commons" if a else f"Photo: Wikimedia Commons · {lic}"

# ---------------------------------------------------------------- the edit (film seconds) ---------------------------------
# shot(t0, kind, src, ...): runs to the next shot's t0. kinds: v = video/scene clip, p = still (moving), cg = native CG render.
# labels: (a, b, image-fn) in film seconds; tags/credits are per shot.
SHOTS = []
def shot(t0, kind, src, ss=0.0, srclen=None, crop=None, kb=None, credit=None, ill=False, labels=(), fin=0.0, fout=0.0, up=True, note=""):
    if kind == "p" and credit is None: credit = credit_of(Path(src).name)
    SHOTS.append(dict(t0=t0, kind=kind, src=Path(src), ss=ss, srclen=srclen, crop=crop, kb=kb, credit=credit, ill=ill, labels=list(labels),
                      fin=fin, fout=fout, up=up, note=note))
lab = L.label

# 0:00 cold open: the real first Mk1A at HAL, the date; into the hangars (lede within 25 s: ~30 jets, none delivered)
shot(0.00, "p", real("mk1a_03_tejasmark1a-jpg.jpg"), kb=(1.05, 1.16, 0.52, 0.55, 0.50, 0.52), credit=C_MOD, fin=0.25,
     labels=[(0.15, 2.3, lambda: lab("October 2026", size=110))], note="L1 October 2026")
shot(2.36, "v", DD, ss=123.0, srclen=2.9, crop=CROP_DD, credit=C_DD, labels=[(2.9, 7.6, lambda: lab("HAL hangars", "Bengaluru · Nashik"))], note="L2 Nashik line, wide")
shot(5.30, "p", real("prod_04_hal-tejas-trainer-version-construct.jpg"), kb=(1.04, 1.14, 0.45, 0.55, 0.55, 0.50), labels=[], note="L2 Tejas on the line (HAL)")
shot(7.76, "cg", R1, ss=0.16, ill=True, labels=[(8.9, 14.6, lambda: lab("Jets built", "about thirty"))], note="L3 CG walk in: ~30 new Tejas, silence")
shot(15.13, "v", DD, ss=129.2, srclen=1.0, crop=CROP_DD, credit=C_DD, note="L3 Painted.")
shot(16.12, "v", DD, ss=126.2, srclen=1.4, crop=CROP_DD, credit=C_DD, note="L3 Radars fitted. (radome open on the jig)")
shot(17.53, "p", real("tejas_41_chief-of-the-army-staff-general-upe.jpg"), kb=(1.10, 1.22, 0.50, 0.45, 0.46, 0.42), note="L3 Cockpits wired.")
shot(19.11, "v", DD, ss=44.0, srclen=1.64, crop=CROP_DD, credit=C_DD, note="L3 They look lethal. (Mk1A taxiing, Nashik)")
shot(20.75, "cg", R1, ss=7.75, ill=True, labels=[(21.2, 25.6, lambda: lab("Delivered to the Air Force: 0", hi="0", accent="red"))],
     note="L4-6 CG: under the hero, stop on 'Not one', walk to the tail, into the empty exhaust")
shot(33.65, "p", real("f404_104_us-navy-030329-n-5464g-002-photo.jpg"), kb=(1.04, 1.15, 0.45, 0.5, 0.55, 0.5), labels=[(34.4, 41.6, lambda: L.grid_bar(14))], note="L7 the F404 (test run)")
shot(37.60, "v", PIB, ss=6.0, srclen=4.2, crop=CROP_PIB, credit=C_PIB, note="L7 Tejas taxiing, engine waiting")
# the Moon paradox: real ISRO footage, one shot per item
shot(41.80, "v", ISRO_M, ss=285, srclen=3.8, credit=C_ISRO, fin=0.15, note="L8 Moon control room")
shot(45.60, "v", ISRO_L, ss=600, srclen=3.0, credit=C_ISRO, note="L8 commercial satellites (LVM3)")
shot(48.60, "v", ISRO_M, ss=315, srclen=2.0, credit=C_ISRO, note="L8 control room")
shot(50.60, "v", ISRO_M, ss=765, srclen=3.3, credit=C_ISRO, note="L8 celebration -> why not an engine?")
# the blade
shot(53.90, "v", sc("A/A3_blade_rise.mp4"), ss=0, srclen=5.0, ill=True, fin=0.2, note="L9 the hardest puzzle")
shot(59.40, "v", sc("A/A2_engine_dive.mp4"), ss=0.0, srclen=4.6, ill=True, labels=[(60.2, 63.9, lambda: lab("Smaller than", "your smartphone"))], note="L10 tiny blade")
shot(64.00, "v", sc("A/A5_thermal_reveal.mp4"), ss=0, srclen=4.2, ill=True, labels=[(66.0, 71.6, lambda: lab("Hotter than its", "own melting point", accent="red"))], note="L10 inferno")
shot(68.20, "v", sc("A/A3_blade_rise.mp4"), ss=1.0, srclen=3.8, ill=True, note="L10 ...and it does not melt")
shot(72.00, "v", sc("D/D7_engine_club.mp4"), ss=4.4, srclen=7.5, ill=True, labels=[(76.6, 79.3, lambda: lab("40 years", "1986 → 2026"))], note="L11 club: markers as named")
# how an engine breathes: R2 journey (chips baked in), readouts added; Blow ends on a real Tejas
R2B = [(98.0, 103.0, lambda: lab("Hundreds of kg", "of air every second", pos="lr")),
       (109.0, 116.0, lambda: lab("Pressure: 30×", "atmosphere", pos="lr", hi="30×")),
       (120.5, 126.0, lambda: lab("1,700 °C", "the flame", pos="lr", hi="1,700 °C", accent="red"))]
shot(79.50, "v", R2, ss=0.0, srclen=51.0, up=True, ill=True, labels=R2B, note="L12-17 R2 journey to the turbine")
shot(130.50, "v", PIB, ss=13.4, srclen=6.0, crop=(0.15, 0.0, 0.70, 0.70), credit=C_PIB, labels=[(133.0, 138.2, lambda: lab("Past the", "speed of sound"))], note="L17 Blow: real Tejas climbing")
shot(136.50, "p", real("tejas_28_hal-tejas-aero-india-day1-jpg.jpg"), kb=(1.05, 1.18, 0.5, 0.45, 0.5, 0.4), note="L17 afterburner")
shot(138.30, "v", R2, ss=58.8, srclen=4.5, ill=True, note="L18-19 turbine sits directly behind the fire")
# the gap
TH = [(159.3, 166.9, lambda: lab("Gas 1,400 °C", pos="lr", accent="red", y=H - 240 - 3 * 190)),
      (161.5, 166.9, lambda: lab("Blade 930 °C", pos="lr", accent="cyan", y=H - 240 - 2 * 190)),
      (164.2, 166.9, lambda: lab("Gap 470 °C", pos="lr", hi="470 °C", y=H - 240 - 190))]
shot(143.20, "v", sc("A/A5_thermal_reveal.mp4"), ss=4.2, srclen=13.8, ill=True, note="L20 gas hotter than the alloy's melting point")
shot(157.00, "v", sc("A/A5_thermal_reveal.mp4"), ss=12.0, srclen=6.1, ill=True, labels=TH, note="L21-22 1,400 / 930 / 470")
shot(167.00, "v", sc("A/A4_combustor_flow.mp4"), ss=0, srclen=5.6, ill=True, labels=[(167.6, 174.5, lambda: lab("If the gap closes", "the blade melts", accent="red"))], note="L23 what if")
shot(174.80, "v", sc("B/B1_metal_zoom.mp4"), ss=0, srclen=2.7, ill=True, note="L24 how does metal survive?")
shot(179.40, "v", sc("A/A7_recap.mp4"), ss=0.3, srclen=2.9, ill=True, labels=[(179.6, 182.2, lambda: lab("3 tricks", "zero joints · hollow · air shield"))], note="L25 three tricks")
shot(182.30, "v", sc("B/B4_single_crystal.mp4"), ss=0, srclen=3.0, ill=True, labels=[(182.5, 185.2, lambda: lab("1 · Zero joints", "one single crystal"))], note="L26 first: zero joints")
shot(185.30, "v", sc("B/B2_polycrystal.mp4"), ss=0, srclen=5.7, ill=True, labels=[(186.5, 192.0, lambda: lab("Ordinary metal", "billions of crystals"))], note="L27 spoon = brick wall")
shot(192.50, "v", sc("B/B3_creep.mp4"), ss=0, srclen=6.8, ill=True, note="L27 creep (label baked ~199.3)")
shot(201.00, "v", sc("B/B4_single_crystal.mp4"), ss=0, srclen=5.0, ill=True, labels=[(201.3, 205.8, lambda: lab("Grown, not forged", "in a vacuum furnace"))], note="L28 grown as one crystal")
shot(206.00, "v", sc("B/B5_alloy.mp4"), ss=0, srclen=4.9, ill=True, note="L28 nickel superalloy + rhenium")
shot(212.50, "v", sc("A/A3_blade_rise.mp4"), ss=0.6, srclen=4.2, ill=True, note="L28 no bricks, no joints")
shot(216.70, "v", sc("B/B6_cooling_channels.mp4"), ss=0, srclen=8.5, ill=True, labels=[(217.0, 219.0, lambda: lab("2 · Hollow"))], note="L29-30 the blade is hollow")
shot(229.00, "v", sc("B/B7_film_cooling.mp4"), ss=0, srclen=6.0, ill=True, labels=[(229.3, 231.3, lambda: lab("3 · Air shield"))], note="L31-32 film cooling")
shot(237.50, "v", sc("B/B6_cooling_channels.mp4"), ss=5.5, srclen=3.0, ill=True, note="L32 blanket of cool air")
shot(242.10, "v", sc("B/B7_film_cooling.mp4"), ss=2.0, srclen=4.0, ill=True, labels=[(242.3, 249.3, lambda: lab("1,700 °C fire", "never touches the metal", hi="1,700 °C", accent="cyan"))], note="L33 never touches")
shot(249.80, "v", sc("B/B8_tbc.mp4"), ss=0, srclen=3.7, ill=True, note="L34 ceramic coating")
# the spin
shot(255.50, "v", sc("A/A6_spin_bus.mp4"), ss=0, srclen=8.2, ill=True, note="L35-36 12,000 RPM")
shot(266.00, "p", real("bus_140_best-cbd-wad-jpg.jpg"), kb=(1.04, 1.16, 0.5, 0.55, 0.52, 0.5), labels=[(266.2, 272.9, lambda: lab("9-ton city bus", "hanging from one blade", hi="9-ton"))], note="L36 a nine-ton city bus")
shot(273.50, "v", sc("A/A5_thermal_reveal.mp4"), ss=0, srclen=4.2, ill=True, note="L37 gas hotter than its melting point")
shot(277.00, "p", real("bus_136_best-food-on-wheels-mumbai-jpg.jpg"), kb=(1.04, 1.14, 0.5, 0.5, 0.5, 0.45), note="L37 a nine-ton bus hanging from it")
shot(280.20, "v", sc("A/A8_verdict_blade.mp4"), ss=1.0, srclen=6.3, ill=True, note="L37 thousands of hours, no crack")
# rocket vs jet
shot(285.10, "v", ISRO_L, ss=840, srclen=5.0, credit=C_ISRO, fin=0.15, note="L38 we build cryogenic rocket engines")
shot(291.60, "v", ISRO_L, ss=600, srclen=3.5, credit=C_ISRO, labels=[(291.8, 296.0, lambda: lab("Rocket engine", "fires ~3 minutes"))], note="L39 rocket: minutes")
shot(296.20, "p", real("tejas_14_digital-fly-by-wire-for-tejas-mk1a-.jpg"), kb=(1.03, 1.15, 0.45, 0.5, 0.58, 0.5), labels=[(296.4, 305.4, lambda: lab("Fighter engine", "idle to full power in seconds · 25 years"))], note="L39 jet: idle to supersonic")
shot(299.60, "p", real("tejas_31_hal-tejas-at-leh-jpg.jpg"), kb=(1.04, 1.14, 0.5, 0.5, 0.45, 0.5), note="L39 dust, cold (Leh)")
shot(302.60, "v", real("tvid_36_tejas-takeoff-from-ins-vikrant-webm.mp4"), ss=0.5, srclen=2.9, credit="Video: Indian Navy (GODL-India)", note="L39 25 years of punishment")
# the club
shot(305.80, "v", sc("C/C4_kaveri_blueprint.mp4"), ss=0, srclen=4.2, ill=True, labels=[(306.0, 309.9, lambda: lab("Not in the drawing"))], note="L40 you cannot copy this from a drawing")
shot(310.00, "v", sc("B/B4_single_crystal.mp4"), ss=1.5, srclen=3.6, ill=True, labels=[(310.2, 313.5, lambda: lab("Crystal casting", "vacuum metallurgy"))], note="L40 the casting recipes")
shot(313.60, "v", sc("B/B7_film_cooling.mp4"), ss=0.5, srclen=3.8, ill=True, labels=[(313.8, 317.2, lambda: lab("Micro-cooling", "physics"))], note="L40 micro-cooling physics")
shot(317.40, "v", sc("D/D7_engine_club.mp4"), ss=3.4, srclen=8.8, ill=True, note="L41 the club")
# back to Nashik: the cost
shot(326.70, "v", DD, ss=123.0, srclen=4.8, crop=CROP_DD, credit=C_DD, fin=0.15, labels=[(327.0, 331.3, lambda: lab("Back in Nashik", "about thirty jets waiting"))], note="L42 back to the line")
shot(332.00, "v", sc("D/D2_squadrons.mp4"), ss=0, srclen=5.8, ill=True, note="L43 42 sanctioned, ~29 operating")
shot(338.20, "v", IAF_MIG, ss=35.5, srclen=4.7, credit=C_IAF, labels=[(338.4, 342.8, lambda: lab("MiG-21", "retired Sep 2025"))], note="L43 MiG-21s retiring")
shot(343.40, "v", sc("D/D3_orders.mp4"), ss=0, srclen=10.9, ill=True, note="L44 83 + 97 = 180 ordered")
shot(352.00, "v", sc("D/D1_globe_lynn.mp4"), ss=0, srclen=5.0, ill=True, note="L44 F404 in Massachusetts")
shot(356.50, "p", real("f404_100_aircraft-technicians-of-the-441-ae.jpg"), kb=(1.03, 1.13, 0.4, 0.5, 0.5, 0.5), labels=[(356.7, 359.7, lambda: lab("GE F404", "made in Lynn, Massachusetts"))], note="L44 the engine itself")
shot(360.00, "v", sc("D/D4_promise.mp4"), ss=0, srclen=6.2, ill=True, labels=[(361.5, 363.4, lambda: lab("Penalties", "no engines", accent="red"))], note="L44 delays, penalties")
shot(363.90, "v", IAF_FL, ss=8.0, srclen=2.7, credit=C_IAF, fout=0.15, note="L45 seen this movie before")
# 1998
shot(367.00, "v", sc("C/C3_sanctions_wireframe.mp4"), ss=0, srclen=7.8, ill=True, labels=[(367.2, 373.0, lambda: lab("May 1998", "Pokhran tests → U.S. sanctions"))], note="L46 Pokhran, sanctions")
shot(375.00, "v", sc("C/C6_split_blueprint.mp4"), ss=0, srclen=5.0, ill=True, note="L46 GE frozen, flight-control help pulled")
shot(380.10, "p", real("tejas_13_digital-fly-by-wire-control-comput.jpg"), kb=(1.02, 1.12, 0.5, 0.5, 0.5, 0.48), labels=[(380.4, 386.0, lambda: lab("Built in India", "digital flight-control computer"))], note="L47 built in-house (DFCC, ADE Bengaluru)")
shot(386.20, "p", real("tejas_24_hal-tejas-la-5020-of-squadron-18-f.jpg"), kb=(1.03, 1.14, 0.5, 0.5, 0.55, 0.48), labels=[(388.0, 392.0, lambda: lab("Own the engine", "own the jet"))], note="L47 own the engine")
# Kaveri
shot(392.60, "p", real("kaveri_99_gtx-35vs-kaveri-jpg.jpg"), kb=(1.03, 1.15, 0.5, 0.5, 0.5, 0.45), fin=0.15, labels=[(392.8, 396.5, lambda: lab("Kaveri", "GTRE, Bengaluru"))], note="L48 the Kaveri")
shot(397.10, "v", sc("C/C4_kaveri_blueprint.mp4"), ss=0, srclen=4.7, ill=True, note="L49 1986 GTRE stamp")
shot(401.40, "v", sc("C/C5_thrust_target.mp4"), ss=0, srclen=4.2, ill=True, note="L49 target 81 kN")
shot(405.60, "v", sc("C/C5_thrust_target.mp4"), ss=2.3, srclen=4.2, ill=True, note="L50 total failure?")
shot(413.30, "v", sc("D/D9_weight.mp4"), ss=0, srclen=4.7, ill=True, note="L51 overweight")
shot(420.00, "v", sc("D/D10_thrust.mp4"), ss=0, srclen=5.7, ill=True, note="L51 70 kN, eleven short")
shot(426.50, "v", sc("C/C1_empty_bay.mp4"), ss=0, srclen=4.4, ill=True, labels=[(426.7, 430.8, lambda: lab("2008", "delinked from Tejas", hi="2008", accent="red"))], note="L51 delinked in 2008")
shot(431.40, "v", sc("D/D12_cost.mp4"), ss=0.4, srclen=4.3, ill=True, note="L52 ~2,000 crore spent by 2012")
shot(436.00, "v", sc("C/C8_dry_kaveri.mp4"), ss=3.0, srclen=6.2, ill=True, note="L53 Dry Kaveri ~48.5 kN")
shot(440.60, "p", real("ghatak_110_autonomous-flying-wing-tech-jpg.jpg"), kb=(1.03, 1.14, 0.5, 0.55, 0.55, 0.5), labels=[(440.8, 444.2, lambda: lab("Ghatak", "stealth combat drone (demonstrator)"))], note="L53 Ghatak")
shot(444.70, "v", sc("A/A3_blade_rise.mp4"), ss=0.2, srclen=4.5, ill=True, labels=[(445.0, 455.8, lambda: lab("D.M.R.L. Hyderabad", "60 single-crystal blades to HAL", hi="60"))], note="L54 DMRL blades")
shot(450.50, "v", sc("B/B4_single_crystal.mp4"), ss=1.5, srclen=3.5, ill=True, note="L54 the foundation")
# what next
shot(456.30, "p", real("mk1a_37_tejas-mk1a-flying-at-aero-india-202.jpg"), kb=(1.03, 1.14, 0.5, 0.5, 0.56, 0.48), fin=0.15, note="L55 what happens next?")
shot(460.90, "v", sc("C/C9_amca_engines.mp4"), ss=0, srclen=8.8, ill=True, note="L56 AMCA needs 110 kN, Indian design")
shot(470.10, "v", sc("D/D14_paris_derby.mp4"), ss=0, srclen=13.0, ill=True, labels=[(480.0, 483.0, lambda: lab("Decision", "New Delhi", hi="New Delhi"))], note="L57-58 Safran offer, RR + Reliance, decision in Delhi")
shot(483.60, "p", real("tejas_43_exercise-garuda-iaf-su-30-mki-fren.jpg"), kb=(1.03, 1.13, 0.5, 0.5, 0.45, 0.5), labels=[(483.8, 489.0, lambda: lab("China", "30 years to its own fighter engines"))], note="L59 China walked this road")
shot(489.20, "p", real("tejas_23_hal-tejas-la-5018-of-squadron-18-f.jpg"), kb=(1.03, 1.15, 0.5, 0.5, 0.55, 0.45), note="L59 India is walking that fire now")
shot(494.70, "v", PIB, ss=37.5, srclen=3.3, crop=CROP_PIB, credit=C_PIB, note="L60 not painted on the wings")
shot(498.40, "v", sc("A/A3_blade_rise.mp4"), ss=0.5, srclen=4.0, ill=True, note="L61 forged inside the blade")
shot(502.60, "v", PIB, ss=41.0, srclen=4.5, crop=CROP_PIB, credit=C_PIB, labels=[(502.8, 506.8, lambda: L.big("What should India do\nwith the Safran deal?", "Tell me in the comments", size=130))], note="L62 the question")
shot(507.10, "card", "", labels=[], fin=0.4, note="L63 sign-off + end card")

# ---------------------------------------------------------------- rendering ------------------------------------------------
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: print(" ".join(map(str, cmd))[:900]); print(r.stderr[-2000:]); sys.exit(1)
    return r

def dur_of(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout or 0)

def overlay_pngs(s, i, t0, t1):
    """PNG layers for a shot: labels (timed), credit / ILLUSTRATION tags, logo bug."""
    layers = []
    d = OUT / "png"; d.mkdir(parents=True, exist_ok=True)
    def save(img, name):
        p = d / name
        if not p.exists():
            tmp = p.with_suffix(f".{os.getpid()}.tmp.png"); img.save(tmp, optimize=False, compress_level=1); os.replace(tmp, p)
        return p
    if s["kind"] != "card":
        static = L.logo_bug()
        if s["credit"]: static.alpha_composite(L.tag(s["credit"], corner="br"))
        if s["ill"]: static.alpha_composite(L.tag("Illustration", corner="tl"))
        layers.append((save(static, "st_" + hashlib.md5(static.tobytes()).hexdigest()[:12] + ".png"), 0, t1 - t0, 0, 0))
    for k, (a, b, fn) in enumerate(s["labels"]):
        img = fn(); key = hashlib.md5(img.tobytes()).hexdigest()[:12]
        layers.append((save(img, f"l_{key}.png"), max(0, a - t0), min(t1, b) - t0, 0.3, 0.3))
    return layers

def grade_chain(up):
    g = []
    if up: g.append("unsharp=5:5:0.55:5:5:0.0")
    g += ["eq=contrast=1.03:saturation=0.96", "noise=alls=5:allf=t", "vignette=angle=0.55"]
    return g

def still_frames(path, n, kb, out_pipe):
    """Ken Burns + handheld drift on a still, rendered with OpenCV at 4K, streamed as raw BGR frames."""
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    z0, z1, cx0, cy0, cx1, cy1 = kb
    base = max(W / w, H / h)
    rng = np.random.default_rng(int(hashlib.md5(str(path).encode()).hexdigest()[:8], 16))
    ph = rng.uniform(0, 6.28, 4)
    for f in range(n):
        u = f / max(1, n - 1); e = u * u * (3 - 2 * u)
        z = base * (z0 + (z1 - z0) * e)
        # handheld: two slow sines per axis, ~3 px at 4K, plus a tiny roll
        hx = 3.0 * math.sin(f / FPS * 0.9 + ph[0]) + 1.5 * math.sin(f / FPS * 2.1 + ph[1])
        hy = 2.5 * math.sin(f / FPS * 0.7 + ph[2]) + 1.2 * math.sin(f / FPS * 1.9 + ph[3])
        rot = 0.08 * math.sin(f / FPS * 0.5 + ph[1])
        cx = (cx0 + (cx1 - cx0) * e) * w; cy = (cy0 + (cy1 - cy0) * e) * h
        # keep the frame covered
        hw_, hh_ = W / (2 * z), H / (2 * z)
        cx = min(max(cx, hw_), w - hw_); cy = min(max(cy, hh_), h - hh_)
        M = cv2.getRotationMatrix2D((cx, cy), rot, z)
        M[0, 2] += W / 2 - cx + hx; M[1, 2] += H / 2 - cy + hy
        fr = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        out_pipe.write(fr.tobytes())

def render_shot(i, s, t0, t1):
    D = t1 - t0
    pngs = overlay_pngs(s, i, t0, t1)
    key = hashlib.md5(json.dumps([str(s["src"]), s["kind"], s["ss"], s["srclen"], s["crop"], s["kb"], s["credit"], s["ill"], s["fin"], s["fout"],
                                  round(t0, 3), round(t1, 3), [str(p[0]) for p in pngs], [p[1:] for p in pngs],
                                  RENDER_VERSION]).encode()).hexdigest()[:12]
    f = OUT / f"k_{key}.mp4"          # cache by content key: inserting a shot never renumbers (and invalidates) the rest
    if f.exists(): return f
    n = int(round(D * FPS))
    inputs, fc, base = [], [], "[0:v]"
    if s["kind"] == "p":
        inputs = ["-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0"]
        pre = []
    elif s["kind"] == "card":
        L.end_card().convert("RGB").save(OUT / "png/endcard.png")
        inputs = ["-loop", "1", "-framerate", str(FPS), "-i", str(OUT / "png/endcard.png")]
        pre = ["scale=3840:2160"]
    else:
        srclen = s["srclen"] or D
        inputs = ["-ss", f"{s['ss']:.3f}", "-t", f"{srclen + 0.5:.3f}", "-i", str(s["src"])]
        pre = []
        if s["crop"]:
            x, y, w, h = s["crop"]; pre.append(f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y}")
        fac = D / srclen
        if abs(fac - 1) > 0.02: pre.append(f"setpts=PTS*{fac:.5f}")
        pre.append(f"fps={FPS}")
        if fac > 1.3: pre.insert(-1, "minterpolate=fps=30:mi_mode=blend")
        pre += [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}", "setsar=1"]
    chain = pre + grade_chain(s["up"] and s["kind"] in ("v", "cg"))
    if s["kind"] == "cg": chain = [c for c in chain if not c.startswith("noise")]   # CG already carries film grain
    if s["fin"]: chain.append(f"fade=t=in:st=0:d={s['fin']}")
    if s["fout"]: chain.append(f"fade=t=out:st={D - s['fout']:.3f}:d={s['fout']}")
    fc.append(f"{base}{','.join(chain)},trim=duration={D:.4f},setpts=PTS-STARTPTS[b0]")
    last = "[b0]"
    for k, (p, a, b, fi, fo) in enumerate(pngs):
        inputs += ["-i", str(p)]
        idx = 1 + k
        fl = ["format=rgba", f"loop=loop={n}:size=1:start=0", f"fps={FPS}", "setpts=N/FRAME_RATE/TB"]
        if fi: fl.append(f"fade=t=in:st={a:.3f}:d={fi}:alpha=1")
        if fo: fl.append(f"fade=t=out:st={max(a, b - fo):.3f}:d={fo}:alpha=1")
        fc.append(f"[{idx}:v]{','.join(fl)}[o{k}]")
        en = f":enable='between(t,{a:.3f},{b:.3f})'" if (a > 0.001 or b < D - 0.001) else ""
        fc.append(f"{last}[o{k}]overlay=0:0:format=auto{en}[b{k + 1}]"); last = f"[b{k + 1}]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", last, "-frames:v", str(n), "-an"] + ENC + [str(f)]
    if s["kind"] == "p":
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        still_frames(s["src"], n, s["kb"], p.stdin); p.stdin.close(); err = p.stderr.read().decode(); p.wait()
        if p.returncode: print(" ".join(cmd)[:900]); print(err[-2000:]); sys.exit(1)
    else:
        run(cmd)
    got = dur_of(f)
    if abs(got - n / FPS) > 0.05: f.unlink(); print(f"shot {i}: duration {got:.3f} != {n / FPS:.3f}"); sys.exit(1)
    return f

def _render_k(k, t0, t1):
    SHOTS.sort(key=lambda s: s["t0"])
    s = SHOTS[k]; print(f"shot {k:3d} {t0:7.2f}-{t1:7.2f} {s['note']}", flush=True)
    f = render_shot(k, s, t0, t1); print(f"  done {k}", flush=True); return f

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--out", default=str(VJ / "film_v2_4k.mp4"))
    ap.add_argument("--audio", default=""); ap.add_argument("--list", action="store_true"); ap.add_argument("--jobs", type=int, default=3); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.sort(key=lambda s: s["t0"])
    bounds = [(s["t0"], SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else END) for k, s in enumerate(SHOTS)]
    # frame-exact boundaries: round each cut to the frame grid so the parts sum to the film
    fb = [(round(t0 * FPS) / FPS, round(t1 * FPS) / FPS) for t0, t1 in bounds]
    if a.list:
        for k, (s, (t0, t1)) in enumerate(zip(SHOTS, fb)): print(f"{k:3d} {int(t0 // 60)}:{t0 % 60:05.2f} {t1 - t0:5.2f}s {s['kind']:4s} {s['src'].name[:38]:38s} {s['note']}")
        return
    only = {int(x) for x in a.only.split(",") if x}
    missing = [str(s["src"]) for k, s in enumerate(SHOTS) if s["kind"] != "card" and not s["src"].exists() and (not only or k in only)]
    if missing: print("missing sources:\n " + "\n ".join(sorted(set(missing)))); sys.exit(2)
    todo = [k for k in range(len(SHOTS)) if not only or k in only]
    with ProcessPoolExecutor(a.jobs) as ex:
        futs = {k: ex.submit(_render_k, k, fb[k][0], fb[k][1]) for k in todo}
        parts = [futs[k].result() for k in todo]
    if only: return
    lst = OUT / "concat.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    video = OUT / "picture.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])
    vd = dur_of(video)
    if abs(vd - END) > 0.1: print(f"GATE: picture {vd:.2f}s != film {END:.2f}s"); sys.exit(1)
    audio = a.audio or str(VO)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video), "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-t", f"{END:.3f}", "-movflags", "+faststart", a.out])
    ad = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout or 0)
    vd2 = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout or 0)
    print(f"wrote {a.out}: video {vd2:.2f}s audio {ad:.2f}s")
    if abs(vd2 - ad) > 0.15: print("GATE: video and audio durations differ"); sys.exit(1)
    (VJ / "assemble/timeline_v2.md").write_text("# film v2 (4K) timeline\n\n| time | dur | kind | source | note |\n|---|---|---|---|---|\n" +
        "\n".join(f"| {int(t0 // 60)}:{t0 % 60:05.2f} | {t1 - t0:.2f} | {s['kind']} | {s['src'].name} | {s['note']} |" for s, (t0, t1) in zip(SHOTS, fb)) + "\n")

if __name__ == "__main__":
    main()
