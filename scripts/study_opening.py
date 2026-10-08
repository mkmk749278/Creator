"""Measure the opening of a competitor video (study only; PLAYBOOK §4a): loudness, cut rate, pauses, music bed.

floor_db is the 10th-percentile 100 ms level: a dry voice reads about -50 dB, a music bed under the voice much higher.

usage: python scripts/study_opening.py clip.mp4 [seconds]   -> prints one JSON line
"""
import json, re, subprocess, sys

f = sys.argv[1]
T = float(sys.argv[2]) if len(sys.argv) > 2 else 90.0


def ff(args):
    return subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-t", str(T), "-i", f] + args + ["-f", "null", "-"],
                          capture_output=True, text=True).stderr


out = {"file": f.split("/")[-1]}
s = ff(["-af", "ebur128=peak=true", "-vn"])
m = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS.*?LRA:\s+([\d.]+) LU", s, re.S)
if m:
    out["lufs"], out["lra"] = float(m.group(1)), float(m.group(2))
m = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+)", s, re.S)
if m:
    out["true_peak"] = float(m.group(1))

# speech pauses: gaps quieter than -30 dB for >= 0.25 s
s = ff(["-af", "silencedetect=noise=-30dB:d=0.25", "-vn"])
gaps = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", s)]
out["pauses_per_min"] = round(len(gaps) / T * 60, 1)
out["pause_median_s"] = round(sorted(gaps)[len(gaps) // 2], 2) if gaps else None
# true silence (music off too): below -50 dB
s = ff(["-af", "silencedetect=noise=-50dB:d=0.25", "-vn"])
out["dead_silences"] = len(re.findall(r"silence_end", s))

# 100 ms RMS levels; floor = 10th percentile (between words), speech = 90th percentile
s = ff(["-af", "aresample=44100,asetnsamples=4410,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level", "-vn"])
lv = sorted(float(x) for x in re.findall(r"RMS_level=(-?[\d.]+)", s) if x not in ("-inf",))
if lv:
    out["floor_db"] = round(lv[len(lv) // 10], 1)
    out["speech_db"] = round(lv[len(lv) * 9 // 10], 1)
    out["floor_gap_db"] = round(out["speech_db"] - out["floor_db"], 1)  # small gap = continuous bed under the voice

# picture cuts
s = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-t", str(T), "-i", f, "-an", "-vf",
                    "select='gt(scene,0.30)',showinfo", "-f", "null", "-"], capture_output=True, text=True).stderr
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", s)]
out["cuts"] = len(cuts)
out["cuts_per_min"] = round(len(cuts) / T * 60, 1)
out["first_cut_s"] = round(cuts[0], 1) if cuts else None
print(json.dumps(out, ensure_ascii=False))
