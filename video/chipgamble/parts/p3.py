"""Acts 3 & 4: The New Playbook, the subsidy war and the verdict (VO: 03-act3-4_akash_v4.mp3)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import Part, bbox_view, PAL

EP = os.path.join(os.path.dirname(__file__), "../../../episodes/india-semiconductor-gamble/audio")
P = Part("p3", "The New Playbook", "ACT 3", f"{EP}/03-act3-4_akash_v4.mp3", f"{EP}/03-act3-4.words.json", tail=3.0)
T = P.c.at
A, R, TE = PAL["amber"], PAL["red"], PAL["teal"]
IBM = "Footage: IBM Research, CC BY 3.0"
ST = "Footage: STMicroelectronics, CC BY 3.0"
ISM = "Document: India Semiconductor Mission / PIB (MeitY)"
GOI = "Photo: India Semiconductor Mission (MeitY), SEMICON India 2026"
EU = ["FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "POL", "AUT", "SWE", "IRL", "PRT", "CZE", "HUN", "ROU", "GRC", "FIN", "DNK", "SVK", "BGR", "HRV", "LTU", "LVA", "EST", "SVN", "LUX"]

t_decided = T("The Indian government decided"); t_unveiled = T("They unveiled"); t_10b = T("a staggering")
t_deal = T("The deal was"); t_central = T("The central government offered"); t_50 = T("50 % of the project")
t_states = T("and state governments"); t_if = T("If a company spent"); t_three = T("nearly three quarters")
t_but = T("But here is where"); t_amateur = T("India did not make"); t_2nm = T("2nm or 3nm"); t_trying = T("Trying to challenge")
t_cost20 = T("Those fabs cost"); t_asml = T("made exclusively by"); t_wait = T("multi -year waiting")
t_instead = T("Instead India focused"); t_tata = T("Enter Tata Electronics"); t_dholera = T("In Dholera Gujarat")
t_psmc = T("Tata partnered with"); t_91 = T("to build a Rs"); t_target = T("Their target")
t_28 = T("28nm 40nm"); t_40 = T("40nm and"); t_90 = T("and 90nm"); t_think = T("You might think")
t_notclose = T("Not even close"); t_while3 = T("While 3nm chips"); t_power = T("the power management"); t_radar = T("the radar processors")
t_motor = T("the motor controllers"); t_micro = T("and the microcontrollers"); t_70 = T("Mature chips make up")
t_momentum = T("And the momentum"); t_sanand = T("In Sanand"); t_jagi = T("In Jagi Road"); t_by2026 = T("By 2026")
t_steel = T("It was steel"); t_so = T("So does this mean"); t_notsofast = T("Not so fast"); t_because = T("Because laying")
t_real = T("The real trial"); t_first = T("First India is stepping"); t_package = T("India's $10 billion package")
t_until = T("Until you look"); t_us = T("The United States committed"); t_eu = T("The European Union")
t_cn = T("China South Korea and Japan"); t_every = T("Every nation is fighting"); t_second = T("Second the talent gap")
t_hundreds = T("India has hundreds"); t_but2 = T("But operating a commercial"); t_requires = T("It requires precision")
t_vacuum = T("extreme vacuum"); t_metal = T("process metallurgists"); t_500 = T("500 degrees"); t_mistake = T("A single mistake")
t_80 = T("from 80"); t_down20 = T("down to 20%"); t_black = T("black hole of debt"); t_third = T("And third the supply chain")
t_island = T("A semiconductor fab cannot"); t_neon = T("ultra -pure neon"); t_photo = T("speciality photoresis"); t_fluoro = T("and fluoropolymers")
t_decade = T("Building that entire"); t_silver = T("The India Semiconductor mission is not"); t_30 = T("It took Taiwan 30")
t_delays = T("India will face delays"); t_yields = T("Yield rates will"); t_mist = T("Mistakes will happen")
t_firsttime = T("But for the first time"); t_factories = T("The factories rising"); t_sovereign = T("technological sovereignty")
t_what = T("What do you think"); t_drop = T("Drop your perspective"); t_like = T("If you found this")
END = P.duration

# ====================== ACT 3 · the playbook
P.photo(0, t_decided, "carlot_c2.jpg", "Representative image · Photo: Martina Nolte, CC BY-SA 3.0 de", kb="in", grade="bw", shade=0.2)
P.actcard(0, 4.3, "ACT 3", "The New Playbook")
P.kinetic(T("economic suicide") - 0.4, t_decided, [("Imports only?", T("relying entirely") + 0.2), ("Economic suicide.", T("economic suicide"))], pos="left", size=100, plate=True)

P.video(t_decided, t_unveiled, "ibm_glasscorr.mp4", IBM, kb="in")
P.kinetic(t_decided + 0.1, t_unveiled, [("India stops waiting.", T("to stop waiting"))], size=120, plate=True)
P.doc(t_unveiled, t_deal, "d_ism2021.png", highlights=[(0, T("India Semiconductor Mission") + 0.3)], stamp=("≈ $10 BILLION", t_10b + 0.6, "amber"), credit=ISM + " · release of 31 May 2023", zoom=1.55, width=1250)

P.doc(t_deal, t_if, "d_fab50.png", highlights=[(0, t_50)], credit="Document: Modified Semicon India Programme (ISM)", zoom=1.35, width=1500, focus_box=0)
P.lower(t_states + 0.2, t_if, "Plus state incentives", "Another 20–25% from state governments", pos="tl")
P.video(t_if, t_but, "st_construct.mp4", "Footage: STMicroelectronics, CC BY 3.0 (fab construction, Italy)", kb="in", shade=0.3)
P.tracker(t_if, t_three, "Example: a $4 billion plant", [("Centre · 50%", 50, "amber", t_if + 1.0), ("State · ~22%", 22, "teal", t_if + 2.2), ("Company · ~28%", 28, "grey", t_if + 3.2)],
          "Who pays for the factory?")
P.stat(t_three, t_but, "~3/4", "of the capital, effectively public money", pos="center", size=220, boom=True)

# --- the strategy: not 2/3 nm
P.photo(t_but, t_amateur, "si26_026.jpg", GOI, kb="in", focus="50% 40%")
P.lower(t_but + 0.2, t_amateur, "The strategy", "Pick battles India can win", pos="bl")
P.video(t_amateur, t_trying, "ibm_cg_grid.mp4", IBM, kb="in")
P.nmscale(t_amateur, t_trying, [("Human hair", 80000, t_amateur + 0.4, "white"), ("90 nm", 90, t_amateur + 1.4, "teal"), ("28 nm", 28, t_amateur + 2.2, "amber"),
                                 ("3 nm", 3, t_2nm + 0.5, "red"), ("2 nm", 2, t_2nm, "red")], "How small is a 'node'?")
P.photo(t_trying, t_cost20, "tsmc_ap2.jpg", "Photo: 4300streetcar, CC BY 4.0 (TSMC AP2, Tainan)", kb="left")
P.kinetic(t_trying + 0.2, t_cost20, [("Take on TSMC at the cutting edge?", t_trying + 0.4), ("Financial suicide.", T("financial suicide"))], pos="left", size=74, plate=True)
P.video(t_cost20, t_asml, "ibm_yellowfab.mp4", IBM, kb="in", shade=0.3)
P.stat(t_cost20, t_asml, "$20B", "per leading-edge fab", pos="center", color="red", eyebrow="The price of the bleeding edge", size=240)
P.mapscene(t_asml, t_instead, bbox_view(-15, 35, 40, 62), bbox_view(0, 46, 14, 55),
           pins=[("Veldhoven", t_asml + 0.3, "ASML · Veldhoven, NL", "r")], hi=[("NLD", "rgba(245,158,11,0.5)", t_asml + 0.2)])
P.lower(T("Dutch giant") + 0.2, t_instead, "One supplier on Earth", "EUV lithography machines · multi-year waits", pos="bl")
P.sfx_at("whoosh", t_asml - 0.3, 0.3)

# --- mature nodes: Tata Dholera
P.video(t_instead, t_tata, "st_assembly.mp4", ST, kb="in")
P.lower(t_instead + 0.2, t_tata, "The pivot", "Mature nodes + advanced packaging")
P.mapscene(t_tata, t_91, bbox_view(62, 5, 98, 36), bbox_view(68, 19, 76, 25),
           hi=[("IND", "rgba(245,158,11,0.12)", t_tata)], pins=[("Dholera", t_dholera + 0.2, "Dholera · Tata–PSMC fab", "r")],
           routes=[("Hsinchu", "Dholera", t_psmc + 0.3, TE, 1.6)])
P.sfx_at("whoosh", t_tata - 0.3, 0.3)
P.doc(t_91, t_target, "d_units.png", highlights=[(0, T("91 ,000 crore"))], credit=ISM + " · release of 1 Apr 2026", zoom=1.7, width=1150, focus_box=0)
P.photo(t_target, t_think, "dholera_site.jpg", "Photo: Sarvajanik Puralekh, CC BY-SA 4.0 (Dholera, 2020s)", kb="in")
P.kinetic(t_target + 0.1, t_think, [("28 nm", t_28), ("40 nm", t_40 + 0.1), ("90 nm", t_90 + 0.15)], pos="left", size=120, color_last=False, plate=True)

# --- why mature chips matter
P.video(t_think, t_while3, "ibm_die.mp4", IBM, kb="in", shade=0.35)
P.kinetic(t_think + 0.1, t_while3, [("28 nm? Old tech?", t_think + 0.5), ("Not even close.", t_notclose)], size=120)
P.video(t_while3, t_power, "ibm_wafers_glow.mp4", IBM, kb="in")
P.lower(t_while3 + 0.1, t_power, "3 nm", "Flagship smartphones")
P.video(t_power, t_radar, "st_chips.mp4", ST, kb="in", shade=0.35)
P.video(t_radar, t_motor, "ibm_board.mp4", IBM, kb="in", shade=0.35)
P.video(t_motor, t_micro, "st_assembly.mp4", ST, kb="in", shade=0.35)
P.video(t_micro, t_70, "ibm_microscope.mp4", IBM, kb="in", shade=0.35)
P.checklist(t_power - 0.1, t_70, [("EV power management", t_power + 0.2), ("Missile-guidance radar", t_radar + 0.2), ("Washing-machine motors", t_motor + 0.2), ("5G tower controllers", t_micro + 0.3)],
            mark="●", color="amber", size=70)
P.video(t_70, t_momentum, "ibm_cg_wafer.mp4", IBM, kb="in")
P.donut(t_70, t_momentum, 70, "Mature-node chips", "More than 70% of global chip demand, by volume", t_fill=T("more than 70"))

# --- the build-out: Sanand, Jagiroad
P.mapscene(t_momentum, T("broke ground"), bbox_view(62, 6, 98, 34), bbox_view(67, 18, 80, 27),
           hi=[("IND", "rgba(245,158,11,0.12)", t_momentum)],
           pins=[("Dholera", t_momentum + 0.3, "Dholera · Tata fab", "l"), ("Sanand", t_sanand + 0.2, "Sanand · Micron", "r")])
P.sfx_at("whoosh", t_momentum - 0.3, 0.3)
P.doc(T("broke ground"), t_jagi, "d_micron.png", highlights=[(0, T("broke ground") + 0.5), (1, T("memory packaging"))], credit=ISM + " · release of 1 Apr 2026", zoom=1.5, width=1150)
P.photo(t_jagi, T("every single year") + 0.6, "jagiroad1.jpg", "Photo: Pinakpani, CC BY 4.0 (Jagiroad, Assam)", kb="right")
P.stat(T("27 ,000 crore"), T("every single year") + 0.6, "₹27,000 Cr", "Tata's assembly & test campus, Jagiroad, Assam", pos="left", size=170, count=(0, 27000, 1.2), prefix="₹", suffix=" Cr")
P.photo(T("every single year") + 0.6, t_steel, "si26_1.jpg", GOI, kb="in", focus="40% 50%")
P.kinetic(t_by2026, t_steel, [("No longer a PowerPoint.", T("PowerPoint presentation"))], pos="left", size=96, plate=True)
P.video(t_steel, t_so, "st_construct.mp4", "Footage: STMicroelectronics, CC BY 3.0 (fab construction, representative)", kb="in")
P.checklist(t_steel, t_so, [("Steel", t_steel + 0.3), ("Concrete", T("concrete")), ("Cleanroom air ducts", T("clean room air"))], mark="▲", color="amber", size=80)

# ====================== ACT 4 · the verdict
P.photo(t_so, t_because, "si26_21.jpg", GOI, kb="in")
P.actcard(t_so - 0.1, t_so + 3.2, "ACT 4", "The Verdict")
P.kinetic(t_notsofast, t_because, [("Not so fast.", t_notsofast)], size=150)
P.photo(t_because, t_first, "si26_30_plate.jpg", GOI, kb="in", fg="si26_30_fg.png", focus="60% 40%")
P.kinetic(t_real, t_first, [("The real trial starts", t_real + 0.2), ("after the ribbon is cut.", T("after the ribbon"))], pos="left", size=80, plate=True)

# --- 1. subsidy war
P.video(t_first, t_until, "port_ship.mp4", "Representative footage · FILMING CORK, CC BY 3.0", kb="in", shade=0.3)
P.lower(t_first + 0.1, t_until, "Challenge 1", "A brutal global subsidy war", pos="tl")
P.mapscene(t_until, t_every, bbox_view(-150, -15, 170, 70), bbox_view(-140, -8, 165, 66),
           hi=[("USA", "rgba(239,68,68,0.55)", t_us + 0.2)] + [(c, "rgba(45,212,191,0.55)", t_eu + 0.2) for c in EU] +
              [("CHN", "rgba(245,158,11,0.55)", t_cn + 0.1), ("KOR", "rgba(245,158,11,0.75)", T("South Korea and Japan")), ("JPN", "rgba(245,158,11,0.75)", T("and Japan are")),
               ("IND", "rgba(255,255,255,0.35)", t_until + 0.2)],
           labels=[("USA · $52.7B CHIPS Act", -98, 51, t_us + 0.6, 30), ("EU · €43B Chips Act", 14, 62, t_eu + 0.6, 30),
                   ("CHINA · KOREA · JAPAN", 108, 52, t_cn + 0.5, 30), ("INDIA · ~$10B", 80, 8, t_until + 0.5, 30)])
P.sfx_at("whoosh", t_until - 0.3, 0.3)
P.video(t_every, t_second, "port_top.mp4", "Representative footage · FILMING CORK, CC BY 3.0", kb="in")
P.bars(t_every, t_second, "Government chip incentives (headline packages)",
       [("United States", 52.7, "$52.7B", "red", t_every + 0.2), ("European Union", 47, "€43B", "teal", t_every + 0.6), ("India (ISM 1.0)", 10, "~$10B", "amber", t_every + 1.0)],
       unit_note="US CHIPS Act (2022) manufacturing + R&D funding; EU Chips Act public funding target; ISM ₹76,000 crore. China, Korea and Japan: hundreds of billions more.")

# --- 2. talent gap
P.photo(t_second, t_but2, "hitec2.jpg", "Photo: Syced, CC0 (HITEC City, Hyderabad)", kb="in")
P.lower(t_second + 0.1, t_but2, "Challenge 2", "The talent gap", pos="tl")
P.kinetic(t_hundreds + 0.2, t_but2, [("Hundreds of thousands", t_hundreds + 0.5), ("of software engineers", T("brilliant software"))], pos="left", size=84, plate=True)
P.video(t_but2, t_500, "ibm_yellowwork.mp4", IBM, kb="in")
P.checklist(t_requires - 0.1, t_500, [("Precision chemical engineers", t_requires + 0.3), ("Extreme-vacuum technicians", t_vacuum), ("Process metallurgists", t_metal)], mark="✓", color="amber", size=70)
P.video(t_500, t_mistake, "st_robots_orange.mp4", ST, kb="in")
P.stat(t_500, t_mistake, "500 °C", "toxic process gases, handled at this heat", pos="center", color="red", size=240)
P.photo(t_mistake, t_third, "cleanroom_bbs.jpg", "Photo: Clemenspool, CC0 (cleanroom)", kb="in", shade=0.3)
P.dial(t_mistake, t_third, 80, 20, t_down20 - 0.6, "Wafer yield", "One bad chemical mix can turn a fab into a black hole of debt")

# --- 3. supply chain
P.video(t_third, t_island, "port_crane.mp4", "Representative footage · FILMING CORK, CC BY 3.0", kb="in")
P.lower(t_third + 0.1, t_island, "Challenge 3", "The supply-chain ecosystem", pos="tl")
P.mapscene(t_island, t_decade, bbox_view(20, 0, 150, 55), bbox_view(25, 2, 148, 52),
           pins=[("Dholera", t_island + 0.4, "India's fabs", "l"), ("Odesa", t_neon + 0.2, "Neon gas · Eastern Europe", "r"), ("Tokyo", t_photo + 0.2, "Photoresist · Japan", "l")],
           routes=[("Odesa", "Dholera", t_neon + 0.4, TE, 1.6), ("Tokyo", "Dholera", t_photo + 0.4, A, 1.6)])
P.lower(t_fluoro, t_decade, "And thousands more inputs", "Fluoropolymers · gases · chemicals — zero contamination", pos="bl")
P.sfx_at("whoosh", t_island - 0.3, 0.3)
P.video(t_decade, t_silver, "port_straddle.mp4", "Representative footage · FILMING CORK, CC BY 3.0", kb="in", shade=0.35)
P.stat(t_decade, t_silver, "10+ years", "to build a domestic supply chain, with disciplined policy", pos="center", size=210)

# --- the verdict
P.video(t_silver, t_30, "ibm_die.mp4", IBM, kb="out", shade=0.4)
P.kinetic(t_silver + 0.1, t_30, [("Not a silver bullet.", T("silver bullet"))], size=130)
P.photo(t_30, t_delays, "morris_chang_plate.jpg", fg="morris_chang_fg.png", credit="Photo: Office of the President (Taiwan), CC BY 2.0 · Morris Chang, TSMC founder", kb="in", focus="50% 30%")
P.stat(t_30 + 0.1, t_delays, "30 years", "for Taiwan to build its silicon shield", pos="right", size=200)
P.video(t_delays, t_firsttime, "st_construct.mp4", "Footage: STMicroelectronics, CC BY 3.0 (representative)", kb="out", grade="cold", shade=0.3)
P.checklist(t_delays, t_firsttime, [("Delays", t_delays + 0.4), ("Painful early yields", t_yields + 0.3), ("Mistakes", t_mist + 0.2)], mark="!", color="amber", size=86)
P.photo(t_firsttime, T("other nations' silicon") + 0.8, "si26_1.jpg", GOI, kb="in", focus="45% 45%")
P.kinetic(t_firsttime + 0.2, T("other nations' silicon") + 0.8, [("For the first time in 40 years", t_firsttime + 0.4), ("no longer a passive consumer.", T("passive consumer"))], pos="left", size=74, plate=True)
P.doc(T("other nations' silicon") + 0.8, t_factories, "d_semicon2b.png", highlights=[(0, T("other nations' silicon") + 1.6)], credit=ISM + " · Semicon 2.0, 15 Jul 2026", zoom=1.6, width=1300)
P.mapscene(t_factories, t_what, bbox_view(60, 4, 100, 36), bbox_view(66, 14, 98, 31),
           hi=[("IND", "rgba(245,158,11,0.2)", t_factories)],
           pins=[("Dholera", t_factories + 0.5, "Dholera", "l"), ("Sanand", t_factories + 0.8, "Sanand", "r"), ("Jagiroad", t_factories + 1.2, "Jagiroad", "l")])
P.kinetic(t_sovereign - 0.4, t_what, [("Technological", t_sovereign), ("sovereignty.", T("sovereignty"))], pos="left", size=96, plate=True)

# --- CTA / end card
P.video(t_what, END, "ibm_cg_wafer.mp4", IBM, kb="in", shade=0.55)
P.kinetic(t_what + 0.1, t_like, [("Can India reach the precision", T("Can Indian manufacturing")), ("to rival Taiwan & South Korea?", T("to rival Taiwan"))], size=78)
P.lower(t_drop, t_like, "Your verdict", "Tell us in the comments", pos="bl")
P.kinetic(t_like, END, [("THE $10 BILLION", t_like + 0.3), ("CHIP GAMBLE", t_like + 0.6)], size=130)
P.lower(t_like + 1.5, END, "Like · Share · Subscribe", "For the next breakdown", pos="bl")

if __name__ == "__main__":
    P.build()
