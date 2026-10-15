"""Build the blurred real-footage base plates for session C scenes (layer 1, PLAYBOOK §5.2 / §9: pre-blurred DOF plate).
Usage: python3 make_plates.py <BP_HLTH02_Asset_Pack dir>   (footage/ from the owner's Drive zip; MP4s are gitignored)
Writes <scene>/media/plate.mp4 at 960x540 (blurred, so upscaled in the page), 30 fps, silent, bitrate-capped.
Footage: owner's Pexels clips (FOOTAGE_REGISTER.csv, Pexels licence), used only as out-of-focus background."""
import json, pathlib, subprocess, sys

PACK = pathlib.Path(sys.argv[1]) / "footage"
HERE = pathlib.Path(__file__).parent
W = json.load(open(HERE / "windows.json"))
# scene -> segments (clip, source in-point s, speed); segments are joined with 0.6 s crossfades
PLAN = {
    "C1_filing_stepper": [("F10_8480684.mp4", 2.0, 0.8)],
    "C2_offices_board": [("F14_15612409.mp4", 0.0, 0.58)],
    "C3_document_slots": [("F07_7685212.mp4", 0.0, 0.95)],
    "C4_binding_award": [("F08_8725953.mp4", 0.0, 0.4), ("F09_6406171.mp4", 0.0, 0.9)],
    "C5_proof_magnifier": [("F09_6406171.mp4", 0.0, 0.6), ("F07_7685212.mp4", 2.0, 0.75)],
    "C6_hearing": [("F10_8480684.mp4", 18.0, 0.9)],
}
GRADE = "gblur=sigma=16,eq=brightness=-0.04:saturation=0.82,colorbalance=rs=.05:gs=.01:bs=-.05:rm=.04:bm=-.04"
XF = 0.6
for scene, segs in PLAN.items():
    if len(sys.argv) > 2 and scene not in sys.argv[2:]: continue
    need = W[scene]["duration"] + 0.5
    out = HERE / scene / "media" / "plate.mp4"; out.parent.mkdir(parents=True, exist_ok=True)
    ins, chains = [], []
    for i, (clip, a, sp) in enumerate(segs):
        ins += ["-ss", str(a), "-i", str(PACK / clip)]
        chains.append(f"[{i}:v]setpts=PTS/{sp},fps=30,scale=960:540:force_original_aspect_ratio=increase,crop=960:540,{GRADE},format=yuv420p,setpts=PTS-STARTPTS[v{i}]")
    if len(segs) == 1:
        fc = chains[0].replace("[v0]", "[o]")
    else:
        d0 = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(PACK / segs[0][0])],
                                  capture_output=True, text=True).stdout) - segs[0][1]
        off = d0 / segs[0][2] - XF - 0.1
        fc = ";".join(chains) + f";[v0][v1]xfade=transition=fade:duration={XF}:offset={off:.3f}[o]"
    cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[o]", "-t", f"{need:.3f}", "-an",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "3M", "-bufsize", "6M", "-g", "30", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
    print(scene, "plate", dur, "s (need", round(need, 2), ")")
