"""Act 1: The Design Paradox (VO: 01-act1_akash_v4.mp3)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import Part, bbox_view, PAL

EP = os.path.join(os.path.dirname(__file__), "../../../episodes/india-semiconductor-gamble/audio")
P = Part("p1", "The Design Paradox", "ACT 1", f"{EP}/01-act1_akash_v4.mp3", f"{EP}/01-act1.words.json")
T = P.c.at
A, R = PAL["amber"], PAL["red"]
IBM = "Footage: IBM Research, CC BY 3.0"
ST = "Footage: STMicroelectronics, CC BY 3.0"

t_india_not = T("India does not make"); t_designs = T("India designs almost")
t_walk = T("Walk through"); t_behind = T("Behind those tinted"); t_thousands = T("thousands of engineers")
t_whenever = T("Whenever Apple"); t_nvidia = T("Nvidia ships"); t_there = T("there is a very high")
t_verified = T("verified its logic"); t_routed = T("routed its power"); t_sim = T("simulated its thermal")
t_power = T("This engineering powerhouse"); t_1985 = T("It started way back"); t_ti = T("Texas Instruments took")
t_back = T("Back then"); t_install = T("had to install"); t_beam = T("beam chip schematics"); t_dallas = T("back to Dallas")
t_over = T("Over the next four decades"); t_bottomless = T("India had a bottomless"); t_math = T("mathematicians")
t_2024 = T("By 2024"); t_absurd = T("And that is where"); t_because = T("Because once those")
t_cannot = T("they cannot manufacture"); t_send = T("They hit send"); t_blue = T("The digital blueprints")
t_landing = T("landing inside"); t_tw = T("in Taiwan South Korea"); t_kr = T("South Korea or Japan"); t_jp = T("or Japan")
t_f1 = T("Foreign factories print"); t_f2 = T("Foreign packaging plants"); t_imports = T("And then India imports")
t_phones = T("inside smartphones"); t_jets = T("fighter jets"); t_cars = T("cars and medical"); t_med = T("medical monitors")
t_paying = T("paying billions"); t_brains = T("India owns the brains"); t_hands = T("does not own the hands")
t_world = T("And in a world where"); t_single = T("a single geopolitical"); t_terr = T("terrifying vulnerability")
END = P.duration

# --- cold open + act card
P.video(0, t_india_not, "ibm_die.mp4", IBM, kb="in", shade=0.35)
P.actcard(0, 4.3, "ACT 1", "The Design Paradox")
P.kinetic(T("bizarre") - 0.1, t_india_not, [("A bizarre", T("bizarre")), ("economic paradox", T("economic paradox"))], size=130)

# --- makes 0 vs designs ~20%
P.video(t_india_not, t_walk, "ibm_cg_grid.mp4", IBM, kb="in")
P.versus(t_india_not, t_walk, ("India makes", "0", "commercial-scale chip fabs, for decades", "red", t_india_not + 0.3),
         ("India designs", "~20%", "of the world's chip-design engineers", "amber", t_designs + 0.5))

# --- the tech parks on the map
P.mapscene(t_walk, t_behind, bbox_view(55, -2, 105, 38), bbox_view(66, 6, 92, 33),
           hi=[("IND", "rgba(245,158,11,0.16)", t_walk + 0.2)],
           pins=[("Bengaluru", T("Bengaluru Hyderabad")), ("Hyderabad", T("Hyderabad or")), ("Noida", T("or Noida") + 0.2)])
P.sfx_at("whoosh", t_walk - 0.3, 0.3)

# --- glass towers, the companies
P.photo(t_behind, t_thousands, "hitec1.jpg", "Photo: Syced, CC0 (HITEC City, Hyderabad)", kb="up")
P.photo(t_thousands, t_whenever, "hitec2.jpg", "Photo: Syced, CC0 (HITEC City, Hyderabad)", kb="left")
P.kinetic(T("Qualcomm") - 0.15, t_whenever, [("Qualcomm", T("Qualcomm")), ("Nvidia", T("Nvidia Intel")), ("Intel", T("Intel and")), ("AMD", T("AMD"))],
          pos="left", size=84, color_last=False, plate=True)
P.cutline(t_behind, t_thousands, "Hyderabad · HITEC City")
P.cutline(t_thousands, t_whenever, "Hyderabad · HITEC City")

# --- the processors they help design
P.video(t_whenever, t_nvidia, "ibm_board.mp4", IBM, kb="in")
P.video(t_nvidia, t_there, "ibm_wafers_glow.mp4", IBM, kb="out")
P.lower(t_whenever + 0.2, t_there, "Flagship phone processors · AI superchips", "Designed in part by engineers in India")
P.video(t_there, t_verified, "ibm_laptop.mp4", IBM, kb="in")
P.video(t_verified, t_power, "ibm_cg_wafer.mp4", IBM, kb="in", shade=0.25)
P.kinetic(t_verified - 0.1, t_power, [("✓ Verified its logic", t_verified), ("✓ Routed its power lines", t_routed), ("✓ Simulated its thermals", t_sim)],
          pos="left", size=70, color_last=False, plate=True)

# --- 1985: Texas Instruments
P.photo(t_power, t_1985, "bagmane2.jpg", "Photo: Gpkp, CC BY-SA 4.0 (Bengaluru)", kb="in", shade=0.35)
P.kinetic(t_power + 0.1, t_1985, [("Not an accident.", t_power + 0.4)], size=140)
P.doc(t_1985, t_ti + 1.2, "d_since1985.png",
      highlights=[(0, T("1985"))], credit="Document: India Semiconductor Mission (MeitY), Modified Semicon India Programme", zoom=1.9, width=1500)
P.photo(t_ti + 1.2, t_back, "bagmane1.jpg", "Photo: Gpkp, CC BY-SA 4.0 (Texas Instruments, Bagmane Tech Park, Bengaluru, 2024)", kb="in", focus="60% 40%")
P.lower(t_ti + 1.3, t_back, "1985 · Bengaluru", "Texas Instruments opens India's first multinational chip-design centre", pos="bl")
P.mapscene(t_back, t_over, bbox_view(-128, -12, 112, 62), bbox_view(-124, -8, 108, 58),
           pins=[("Bengaluru", t_back + 0.4, "Bengaluru · TI design centre", "l"), ("Dallas", t_dallas, "Dallas · TI HQ", "r")],
           routes=[("Bengaluru", "Dallas", t_beam, A, 1.8)])
P.cutline(t_back, t_over, "Illustrative · 1985 satellite link to Dallas", t_install)
P.sfx_at("whoosh", t_back - 0.3, 0.3)

# --- four decades of talent
P.photo(t_over, t_bottomless, "hitec1.jpg", "Photo: Syced, CC0 (HITEC City, Hyderabad)", kb="right")
P.video(t_bottomless, t_2024, "ibm_typing.mp4", IBM, kb="in")
P.kinetic(t_bottomless, t_2024, [("Brilliant electrical engineers", T("brilliant electrical")), ("and mathematicians", t_math)], pos="left", size=80, plate=True)
P.video(t_2024, t_absurd, "ibm_glasscorr.mp4", IBM, kb="in")
P.timeline(t_2024, t_absurd, "Four decades of chip design in India", 1980, 2030,
           [(1985, "Texas Instruments opens in Bengaluru", t_2024 + 0.3, "amber", "up"),
            (2024, "Most major chip firms run their largest global design centres here", T("largest global design"), "amber", "down")])

# --- the absurd part
P.video(t_absurd, t_because, "st_wafer_rainbow.mp4", ST, kb="in", shade=0.3)
P.kinetic(t_absurd, t_because, [("The paradox", t_absurd + 0.2), ("becomes absurd", T("becomes absurd"))], size=130, plate=True)
P.video(t_because, t_cannot, "ibm_yellow_wafer.mp4", IBM, kb="in")
P.video(t_cannot, t_send, "st_tool_gray.mp4", ST, kb="in", shade=0.5)
P.kinetic(t_cannot, t_send, [("Not a single one", t_cannot + 0.3), ("made at home.", T("inside their own country"))], size=120)

# --- send: blueprints cross the ocean
P.video(t_send, t_blue, "ibm_typing.mp4", IBM, kb="in")
P.kinetic(t_send + 0.1, t_blue, [("SEND ▸", t_send + 0.25)], size=150)
P.mapscene(t_blue, t_landing, bbox_view(62, -6, 148, 46), bbox_view(70, -2, 145, 44),
           pins=[("Bengaluru", t_blue + 0.1, "Bengaluru", "l"), ("Hsinchu", t_blue + 1.9, "Taiwan", "r"), ("Pyeongtaek", t_blue + 2.4, "South Korea", "l"), ("Kumamoto", t_blue + 2.8, "Japan", "r")],
           routes=[("Bengaluru", "Hsinchu", t_blue + 0.4, A, 1.6), ("Bengaluru", "Pyeongtaek", t_blue + 0.9, A, 1.6), ("Bengaluru", "Kumamoto", t_blue + 1.3, A, 1.6)])
P.cutline(t_blue, t_landing, "Illustrative path · undersea fibre")
P.sfx_at("whoosh", t_blue, 0.35)
P.video(t_landing, t_tw, "ibm_yellowwork.mp4", IBM, kb="in")
P.photo(t_tw, t_f1, "tsmc_fab14.jpg", "Photo: 4300streetcar, CC BY 4.0 (TSMC Fab 14B, Tainan)", kb="left")
P.kinetic(t_tw, t_f1, [("Taiwan", t_tw + 0.2), ("South Korea", t_kr + 0.3), ("Japan", t_jp + 0.1)], pos="left", size=84, color_last=False, plate=True)

# --- fab + packaging abroad
P.video(t_f1, t_f2, "ibm_waferhand.mp4", IBM, kb="in")
P.lower(t_f1 + 0.1, t_f2, "Step 2 · abroad", "Printed onto silicon wafers")
P.video(t_f2, t_imports, "st_assembly.mp4", ST, kb="in")
P.lower(t_f2 + 0.1, t_imports, "Step 3 · abroad", "Sealed into chip packages")

# --- imported back
P.video(t_imports, t_paying, "port_crane.mp4", "Representative footage · FILMING CORK, CC BY 3.0", kb="in")
P.kinetic(t_phones - 0.1, t_paying, [("Smartphones", t_phones + 0.1), ("Fighter jets", t_jets), ("Cars", t_cars), ("Medical monitors", t_med)],
          pos="left", size=80, color_last=False, plate=True)
P.doc(t_paying, t_brains, "d_niti.png",
      highlights=[(0, T("foreign currency"))], credit="Document: PIB / NITI Aayog, 29 May 2026", zoom=1.8, width=1400)

# --- brains vs hands
P.video(t_brains, t_world, "ibm_cg_grid.mp4", IBM, kb="out")
P.versus(t_brains, t_world, ("Design", "Brains ✓", "India owns them", "teal", t_brains + 0.2), ("Manufacturing", "Hands ✗", "India does not", "red", t_hands))

# --- choke point
P.mapscene(t_world, END, bbox_view(95, 5, 140, 40), bbox_view(112, 18, 128, 30),
           hi=[("TWN", "rgba(239,68,68,0.85)", t_single), ("CHN", "rgba(255,255,255,0.05)", t_world)],
           labels=[("TAIWAN STRAIT", 118.85, 23.0, t_single + 0.3, 36)])
P.lower(t_terr - 0.1, END, "One island · one strait", "A terrifying vulnerability.", pos="bl")
P.sfx_at("whoosh", t_world - 0.3, 0.3)

if __name__ == "__main__":
    P.build()
