"""Act 2: SCL Mohali 1989 and the cleanroom bottlenecks (VO: 02-act2_akash_v4.mp3)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import Part, bbox_view, PAL

EP = os.path.join(os.path.dirname(__file__), "../../../episodes/india-semiconductor-gamble/audio")
P = Part("p2", "The Lost Head Start", "ACT 2", f"{EP}/02-act2_akash_v4.mp3", f"{EP}/02-act2.words.json")
T = P.c.at
A, R = PAL["amber"], PAL["red"]
IBM = "Footage: IBM Research, CC BY 3.0"
ST = "Footage: STMicroelectronics, CC BY 3.0"
SCL = "Photo: Biswarup Ganguly, CC BY 3.0 (SCL, Mohali, 2016)"

t_notbehind = T("India was not always"); t_1984 = T("In 1984"); t_scl = T("Semiconductor Complex Limited")
t_mohali = T("in Mohali Punjab"); t_moment = T("At that exact moment"); t_5 = T("5 -micron"); t_tw = T("Taiwan was only")
t_barely = T("India was barely"); t_before = T("Before Taiwan had"); t_1989 = T("Then in 1989"); t_fire = T("A mysterious and")
t_burning = T("burning the cleanrooms"); t_instead = T("Instead of rebuilding"); t_redtape = T("red tape"); t_apathy = T("political apathy")
t_inertia = T("bureaucratic inertia"); t_bytime = T("By the time the government"); t_warp = T("moved at warp speed")
t_tsmc = T("Taiwan's TSMC had"); t_window = T("India's window"); t_why = T("Why could not"); t_because = T("Because building a semiconductor")
t_first = T("First the cleanroom"); t_inside = T("Inside an advanced fab"); t_iso = T("ISO Class 1"); t_fewer = T("That means fewer")
t_or = T("An active operating room"); t_dandruff = T("In a chip fab"); t_vapor = T("vaporize a million")
t_second = T("Second the water"); t_40 = T("guzzles up to 40"); t_tap = T("But it cannot be tap"); t_upw = T("It must be ultra")
t_third = T("And third the power grid"); t_flawless = T("A modern fab requires"); t_drop = T("If the power voltage"); t_50 = T("50 milliseconds")
t_reset = T("the high -precision laser"); t_3mo = T("three months of continuous"); t_decades = T("For decades")
t_unint = T("uninterrupted power"); t_molec = T("molecular -grade water"); t_speed = T("bureaucratic speed"); t_every = T("Every foreign chip maker")
t_walked = T("walked away")
END = P.duration

# --- cold open: forgotten history
P.video(0, t_1984, "ibm_archive_lab.mp4", "Archival footage: IBM Research, CC BY 3.0 (illustrative)", kb="in", grade="archival")
P.actcard(0, 4.3, "ACT 2", "The Lost Head Start")
P.kinetic(t_notbehind - 0.1, t_1984, [("India was not", t_notbehind), ("always behind.", T("always behind"))], size=130, plate=True)

# --- 1984 SCL Mohali
P.mapscene(t_1984, t_moment, bbox_view(60, 5, 100, 38), bbox_view(70, 26, 82, 34),
           hi=[("IND", "rgba(245,158,11,0.14)", t_1984)], pins=[("Mohali", t_mohali, "SCL · Mohali, Punjab", "r")])
P.lower(t_scl, t_moment, "1984 · state-run", "Semiconductor Complex Limited (SCL)")
P.sfx_at("whoosh", t_1984 - 0.3, 0.3)
P.photo(t_moment, t_5 + 0.9, "scl_mohali.jpg", SCL, kb="in", grade="archival")
P.cutline(t_moment, t_5 + 0.9, "SCL campus, Mohali · photographed 2016")
P.video(t_5 + 0.9, t_before, "ibm_archive_eng.mp4", "Archival footage: IBM Research, CC BY 3.0 (illustrative)", kb="in", grade="archival", shade=0.3)
P.versus(t_5 + 0.9, t_before, ("India · SCL, 1980s", "5 µm", "process node", "amber", t_5 + 1.0), ("Taiwan, same era", "3.5 µm", "process node", "white", t_tw + 0.6),
         title="Barely a step behind the frontier")
P.photo(t_before, t_1989, "intel1981_plate.jpg", "Photo: Intel Free Press, CC BY-SA 2.0 (Intel Fab 5, 1981)", kb="in", grade="archival", fg="intel1981_fg.png")
P.kinetic(t_before + 0.1, t_1989, [("India was genuinely", t_before + 0.3), ("in the race.", T("in the semiconductor race"))], pos="left", size=96, plate=True)
P.cutline(t_before, t_1989, "A chip fab of the era · Intel, 1981")

# --- 1989 fire
P.photo(t_1989, t_instead, "scl_mohali.jpg", SCL, kb="in", grade="bw")
P.fire(t_fire - 0.3, t_instead)
P.kinetic(t_1989 + 0.1, t_fire + 1.5, [("1989", t_1989 + 0.4)], size=260)
P.lower(t_fire + 1.6, t_instead, "Mohali · 1989", "Fire guts SCL's cleanrooms and lithography tools", pos="tl")
P.cutline(t_fire, t_instead, "Illustration · no public footage of the fire")
P.sfx_at("boom", t_1989 + 0.4, 0.6)

# --- red tape
P.video(t_instead, t_bytime, "ibm_archive_eng.mp4", "Archival footage: IBM Research, CC BY 3.0 (illustrative)", kb="out", grade="bw", shade=0.45)
P.checklist(t_redtape - 0.2, t_bytime, [("Red tape", t_redtape), ("Political apathy", t_apathy), ("Bureaucratic inertia", t_inertia)], size=86)

# --- the world moved on
P.video(t_bytime, t_tsmc, "ibm_glasscorr.mp4", IBM, kb="in")
P.timeline(t_bytime, t_tsmc, "While India waited", 1982, 1996,
           [(1984, "SCL founded, Mohali", t_bytime + 0.3, "amber", "up"), (1987, "TSMC founded, Hsinchu", t_bytime + 1.0, "white", "down"),
            (1989, "Fire at SCL", t_bytime + 1.7, "red", "up")])
P.photo(t_tsmc, t_window, "tsmc_fab6.jpg", "Photo: 4300streetcar, CC BY 4.0 (TSMC Fab 6, Tainan)", kb="left")
P.lower(t_tsmc + 0.1, t_window, "Taiwan", "TSMC corners the global foundry market")
P.photo(t_window, t_why, "taiwan_sat.jpg", "Image: NASA Terra / MODIS, public domain", kb="in", focus="50% 40%", shade=0.25)
P.kinetic(t_window + 0.1, t_why, [("The window", t_window + 0.3), ("slammed shut.", T("slammed shut"))], pos="left", size=120, plate=True)

# --- why not private companies
P.video(t_why, t_first, "ibm_yellowfab.mp4", IBM, kb="in")
P.kinetic(t_because, t_first, [("The most unforgiving", T("the most unforgiving")), ("industrial process on Earth", T("industrial process on"))], pos="left", size=84, plate=True)

# --- 1. AIR
P.photo(t_first, t_iso, "cleanroom_bbs.jpg", "Photo: Clemenspool, CC0 (cleanroom)", kb="in")
P.video(t_iso, t_iso + 3.0, "ibm_corridor.mp4", IBM, kb="in")
P.photo(t_iso + 3.0, t_dandruff, "bunny_suit_plate.jpg", "Photo: Steve Jurvetson, CC BY 2.0 (cleanroom suit)", kb="in", fg="bunny_suit_fg.png")
P.lower(t_first + 0.05, t_iso, "Bottleneck 1", "The cleanroom", pos="tl")
P.particles(t_iso, t_dandruff, t_or - 0.2 if t_or - t_iso > 2 else t_iso + 0.4, t_iso + 0.3)
P.video(t_dandruff, T("short -circuit hundreds"), "ibm_waferhand.mp4", IBM, kb="in")
P.video(T("short -circuit hundreds"), t_vapor, "st_wafer_rainbow.mp4", ST, kb="in")
P.video(t_vapor, t_second, "ibm_die.mp4", IBM, kb="in", grade="bw")
P.kinetic(t_dandruff + 0.2, t_second, [("One fleck of dandruff", T("single fleck")), ("= hundreds of dead chips", T("short -circuit hundreds")), ("$1,000,000 gone", t_vapor + 0.3)],
          pos="left", size=74, plate=True)

# --- 2. WATER
P.video(t_second, t_40, "st_pipes.mp4", ST, kb="in")
P.lower(t_second + 0.05, t_40, "Bottleneck 2", "The water", pos="tl")
P.video(t_40, t_upw, "ibm_tanks.mp4", IBM, kb="in", shade=0.3)
P.water(t_40, t_upw, t_40 + 0.6)
P.video(t_upw, t_upw + (t_third - t_upw) / 3, "st_pipes.mp4", ST, kb="in")
P.video(t_upw + (t_third - t_upw) / 3, t_upw + 2 * (t_third - t_upw) / 3, "ibm_utility.mp4", IBM, kb="in")
P.video(t_upw + 2 * (t_third - t_upw) / 3, t_third, "ibm_glasscorr.mp4", IBM, kb="out")
P.lower(t_upw + 0.3, t_third, "Ultrapure water", "Stripped of every mineral, ion and bacterium")

# --- 3. POWER
P.photo(t_third, t_drop, "pylons_chennai.jpg", "Photo: Aravindan Ganesan, CC BY 2.0 (Chennai)", kb="in")
P.lower(t_third + 0.05, t_drop, "Bottleneck 3", "The power grid", pos="tl")
P.video(t_drop, t_3mo, "ibm_utility.mp4", IBM, kb="in", shade=0.3)
P.waveform(t_drop, t_3mo, t_50, "50 ms dip → lithography tools reset")
P.video(t_3mo, t_decades, "st_robots_orange.mp4", ST, kb="in", grade="bw", shade=0.3)
P.stat(t_3mo, t_decades, "3 months", "of continuous processing, ruined", pos="center", color="red", eyebrow="One flicker costs", size=200)

# --- verdict on the era
P.photo(t_decades, t_every, "pylons_chennai.jpg", "Photo: Aravindan Ganesan, CC BY 2.0 (Chennai)", kb="out", grade="bw", shade=0.35)
P.checklist(t_unint - 0.2, t_every, [("Uninterrupted power", t_unint), ("Molecular-grade water", t_molec), ("Bureaucratic speed", t_speed)], size=78)
P.video(t_every, END, "port_straddle.mp4", "Representative footage · FILMING CORK, CC BY 3.0", kb="in", grade="cold", shade=0.25)
P.kinetic(t_every + 0.1, END, [("Every foreign chipmaker", t_every + 0.3), ("walked away.", t_walked)], pos="left", size=100, plate=True)

if __name__ == "__main__":
    P.build()
