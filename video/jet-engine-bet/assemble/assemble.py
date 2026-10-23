#!/usr/bin/env python3
"""Assemble the full-length film (v0: reuse-first edit) to the owner's voice-over.

Timeline from projects/jet-engine-bet/final/align/align.json (sentence level). Each segment covers a run of voice-over lines
and is filled with one or more clips (rendered scenes from Drive Creator/English/jet-engine-paradox/scenes, the new R1/R2.. scenes,
and owner-fetched official footage). Clips are retimed to fit, crossfaded, and muxed with the voice-over.
  python3 video/jet-engine-bet/assemble/assemble.py [--out out.mp4] [--only N]  (writes video/jet-engine-bet/assemble/work/)
"""
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VJ = ROOT / "video/jet-engine-bet"
LEG = ROOT / "projects/jet-engine-bet/assets/legacy"
SC = LEG / "scenes"
SRC = LEG / "sources"
VO = ROOT / "projects/jet-engine-bet/final/jeb_vo_final.mp3"
ALIGN = ROOT / "projects/jet-engine-bet/final/align/align.json"
WORK = VJ / "assemble/work"
XF = 0.25  # crossfade seconds

def S(p): return SC / p
R1 = VJ / "R1_hangar_v2.mp4"
# segment = (first_line, [(path, src_in, src_len), ...], note); the segment runs to the start of the next segment's first line
PLAN = [
 (1,  [(R1, 0, 41.3)], "R1 hangar walk-around"),
 (8,  [(SRC/"DLA_64yz8Ss.mp4", 285, 4), (SRC/"DLA_64yz8Ss.mp4", 315, 4), (SRC/"DLA_64yz8Ss.mp4", 765, 4)], "Moon landing control room (credited ISRO)"),
 (9,  [(S("A/A3_blade_rise.mp4"), 0, 5.0)], "the blade"),
 (10, [(S("A/A5_thermal_reveal.mp4"), 0, 4.2), (S("B/B1_metal_zoom.mp4"), 0, 2.7), (S("A/A3_blade_rise.mp4"), 0, 5.0)], "blade in fire"),
 (11, [(S("D/D7_engine_club.mp4"), 0, 7.2)], "engine club globe"),
 (12, [(VJ/"R2_engine_journey.mp4", 0, 63.3)], "R2 engine journey: suck, squeeze, burn, blow"),
 (20, [(S("A/A5_thermal_reveal.mp4"), 4.2, 13.9)], "thermal gauge: gas vs blade"),
 (24, [(S("B/B2_polycrystal.mp4"), 0, 5.7)], "three tricks / zero joints"),
 (27, [(S("B/B3_creep.mp4"), 0, 6.8), (S("B/B2_polycrystal.mp4"), 2.5, 3.2)], "brick wall, creep"),
 (28, [(S("B/B4_single_crystal.mp4"), 0, 5.1), (S("B/B5_alloy.mp4"), 0, 4.9)], "single crystal, nickel superalloy"),
 (29, [(S("B/B6_cooling_channels.mp4"), 0, 8.5)], "hollow blade, cooling channels"),
 (31, [(S("B/B7_film_cooling.mp4"), 0, 6.0), (S("B/B1_metal_zoom.mp4"), 0, 2.7), (S("B/B7_film_cooling.mp4"), 3.0, 3.0)], "air film"),
 (34, [(S("B/B8_tbc.mp4"), 0, 3.7)], "ceramic coating"),
 (35, [(S("A/A6_spin_bus.mp4"), 0, 12.4), (S("D/D13_hours.mp4"), 0, 3.5), (S("A/A8_verdict_blade.mp4"), 0, 7.3)], "the spin, the bus, hours"),
 (38, [(SRC/"q2ueCg9bvvQ.mp4", 600, 5), (SRC/"q2ueCg9bvvQ.mp4", 840, 5), (S("A/A4_combustor_flow.mp4"), 0, 5.6), (S("A/A2_engine_dive.mp4"), 0, 6.3)], "rocket vs fighter engine"),
 (40, [(S("D/D7_engine_club.mp4"), 0, 12.2)], "club of four, China"),
 (42, [(R1, 36, 5.3)], "back to the hangar"),
 (43, [(S("D/D2_squadrons.mp4"), 0, 5.8), (S("D/D3_orders.mp4"), 0, 10.9), (S("D/D1_globe_lynn.mp4"), 0, 8.2), (S("D/D4_promise.mp4"), 0, 6.2)], "squadrons, orders, G.E., delay"),
 (45, [(S("C/C3_sanctions_wireframe.mp4"), 0, 7.8), (S("C/C6_split_blueprint.mp4"), 0, 6.8)], "1998 sanctions"),
 (48, [(S("C/C4_kaveri_blueprint.mp4"), 0, 4.7), (S("C/C5_thrust_target.mp4"), 0, 6.5)], "Kaveri: target 81 kN"),
 (51, [(S("D/D9_weight.mp4"), 0, 4.7), (S("D/D8_russia_route.mp4"), 0, 8.9), (S("D/D10_thrust.mp4"), 0, 5.7)], "weight, tests, 70 kN, delinked"),
 (52, [(S("D/D12_cost.mp4"), 0, 3.8), (S("C/C8_dry_kaveri.mp4"), 0, 10.6), (S("A/A3_blade_rise.mp4"), 0, 5.0)], "cost, Dry Kaveri, DMRL blades"),
 (55, [(S("C/C9_amca_engines.mp4"), 0, 12.3), (S("D/D14_paris_derby.mp4"), 0, 19.6)], "AMCA, Safran, the decision"),
 (59, [(S("D/D7_engine_club.mp4"), 6.0, 6.2)], "China walked this road"),
 (60, [(R1, 29.9, 4.2), (S("A/A3_blade_rise.mp4"), 0, 5.0), (S("B/B7_film_cooling.mp4"), 0, 6.0)], "forged inside the blade"),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(map(str, cmd))[:600]); print(r.stderr[-1500:]); sys.exit(1)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=str(VJ / "film_v0.mp4")); ap.add_argument("--only", type=int, default=0); a = ap.parse_args()
    al = json.load(open(ALIGN)); rows = al if isinstance(al, list) else al["lines"]
    start = {r["line"]: r["start"] for r in rows}; end_all = rows[-1]["end"] + 0.4
    WORK.mkdir(parents=True, exist_ok=True)
    bounds = []
    for i, (ln, clips, note) in enumerate(PLAN):
        t0 = 0.0 if ln == 1 else start[ln]
        t1 = start[PLAN[i + 1][0]] if i + 1 < len(PLAN) else end_all
        bounds.append((t0, t1))
    parts = []  # (file, duration) in order
    timeline = []
    for i, ((ln, clips, note), (t0, t1)) in enumerate(zip(PLAN, bounds)):
        seglen = t1 - t0; tot = sum(c[2] for c in clips)
        for j, (p, ss, ln_src) in enumerate(clips):
            L = seglen * ln_src / tot
            last_clip = (i == len(PLAN) - 1 and j == len(clips) - 1)
            Lx = L + (0 if last_clip else XF)       # overlap with the next clip
            f = WORK / f"s{i:02d}_{j}.mp4"
            fac = Lx / ln_src
            vf = ["scale=1920:1080:force_original_aspect_ratio=increase", "crop=1920:1080", "setsar=1"]
            if abs(fac - 1) > 0.02: vf.append(f"setpts=PTS*{fac:.5f}")
            if fac > 1.25: vf.append("minterpolate=fps=30:mi_mode=blend")
            vf += ["fps=30", "format=yuv420p"]
            if ss + ln_src > 1e9: pass
            need = a.only == 0 or a.only == i + 1
            if need and not f.exists():
                run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{ss}", "-t", f"{ln_src}", "-i", str(p),
                     "-vf", ",".join(vf), "-t", f"{Lx:.3f}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(f)])
                # hold the last frame if the source ran short (R1 etc.)
                d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout or 0)
                if d + 0.05 < Lx:
                    g = WORK / f"s{i:02d}_{j}p.mp4"
                    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(f), "-vf", f"tpad=stop_mode=clone:stop_duration={Lx - d + 0.1:.3f}", "-t", f"{Lx:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(g)])
                    g.replace(f)
            parts.append((f, Lx)); timeline.append((t0 + sum(c[2] for c in clips[:j]) / tot * seglen, p.name, note))
    if a.only: return
    # xfade chain in groups of 8 to keep the graph small, then hard-join groups with a crossfade as well
    groups = []
    for k in range(0, len(parts), 8):
        g = parts[k:k + 8]; out = WORK / f"g{k // 8:02d}.mp4"
        if not out.exists():
            cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
            for f, _ in g: cmd += ["-i", str(f)]
            if len(g) == 1: cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-an", str(out)]
            else:
                fc = []; acc = g[0][1]; prev = "[0:v]"
                for n in range(1, len(g)):
                    off = acc - XF; lab = f"[x{n}]"
                    fc.append(f"{prev}[{n}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}"); prev = lab; acc = acc + g[n][1] - XF
                cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out)]
            run(cmd)
        groups.append((out, sum(x[1] for x in g) - XF * (len(g) - 1)))
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for f, _ in groups: cmd += ["-i", str(f)]
    fc = []; acc = groups[0][1]; prev = "[0:v]"
    for n in range(1, len(groups)):
        off = acc - XF; lab = f"[y{n}]"; fc.append(f"{prev}[{n}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}"); prev = lab; acc = acc + groups[n][1] - XF
    cmd += ["-i", str(VO), "-filter_complex", ";".join(fc), "-map", prev, "-map", f"{len(groups)}:a", "-c:v", "libx264", "-preset", "medium", "-b:v", "8M", "-maxrate", "11M", "-bufsize", "16M",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", f"{rows[-1]['end'] + 0.4:.2f}", "-movflags", "+faststart", a.out]
    run(cmd)
    (VJ / "assemble/timeline_v0.md").write_text("# film v0 timeline\n\n| VO time | clip | note |\n|---|---|---|\n" + "\n".join(f"| {int(t//60)}:{t%60:04.1f} | {n} | {m} |" for t, n, m in timeline) + "\n")
    print("wrote", a.out, "total", acc)

if __name__ == "__main__":
    main()
