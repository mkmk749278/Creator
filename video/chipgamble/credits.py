"""Collect every attribution shown on screen across the parts into one Markdown credits file."""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, "../../episodes/india-semiconductor-gamble/06-full-credits.md")
OFFS = {"p1": 48.85, "p2": None, "p3": None}  # filled from part durations

def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ROOT, "parts", f"{n}.py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.P

def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"

parts = [load(n) for n in ("p1", "p2", "p3")]
start = 50.5  # hook length
rows, seen = [], {}
for P in parts:
    for t0, t1, text in sorted(P.credits):
        rows.append((start + t0, start + t1, text))
        seen.setdefault(text, []).append(start + t0)
    start += P.duration

hook = [
    "Footage: STMicroelectronics, CC BY 3.0", "Footage: IBM Research, CC BY 3.0", "Representative footage · FILMING CORK, CC BY 3.0",
    "Representative image · Photo: Martina Nolte, CC BY-SA 3.0 de", "Microcontroller die: yellowcloud, CC BY 2.0",
    "Image: NASA Terra / MODIS, public domain", "Photo: Aravindan Ganesan, CC BY 2.0", "Map: Natural Earth (public domain)",
]
for h in hook:
    seen.setdefault(h, []).insert(0, 0.0)

lines = ["# Full credits: The $10 Billion Chip Gamble (master cut)", "",
         f"Runtime {mmss(start)}. Every real photo, clip and document below is credited on screen (bottom-right) while it is visible.", "",
         "## Sources (first appearance)", "", "| First at | Credit |", "|---|---|"]
for text, ts in sorted(seen.items(), key=lambda kv: min(kv[1])):
    lines.append(f"| {mmss(min(ts))} | {text} |")
lines += ["", "## Made in-house", "",
          "- Motion graphics, maps, charts, dials, document camera moves and highlighter/stamp animations: HTML + GSAP (HyperFrames 0.8.103).",
          "- Map geometry: Natural Earth 1:50m (public domain). Routes are illustrative, not cable or shipping data.",
          "- 2.5D parallax: subject cutouts made locally with HyperFrames remove-background (u2net human segmentation).",
          "- The 1989 SCL fire is an illustration (heat and embers over a 2016 photo of the campus); no public footage exists.",
          "- Sound design (booms, whooshes, paper, marker, stamp, ambient drone): synthesised with ffmpeg.",
          "- Voiceover: ElevenLabs Eleven v4, voice \"Akash – Confident and Natural\".",
          "", "## YouTube description block", "", "```",
          "Footage & images: IBM Research (CC BY 3.0) · STMicroelectronics (CC BY 3.0) · FILMING CORK (CC BY 3.0) · NASA (public domain)",
          "Wikimedia Commons photographers: " + ", ".join(sorted({t.split("Photo: ")[1].split(",")[0] for t in seen if "Photo: " in t})),
          "Government documents & photos: India Semiconductor Mission / MeitY, PIB, NITI Aayog (GODL-India).",
          "Maps: Natural Earth. Full credits with licences: episodes/india-semiconductor-gamble/06-full-credits.md",
          "```", ""]
open(OUT, "w").write("\n".join(lines))
print(OUT, len(seen), "sources")
