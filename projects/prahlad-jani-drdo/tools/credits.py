"""Write credits.md (paste into the YouTube description) from media_manifest.csv."""
import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader((HERE / "media_manifest.csv").open(encoding="utf-8")))
groups = {}
for r in rows:
    key = "⚠️ Copyrighted, quoted under fair use (licence before monetising)" if "COPYRIGHTED" in r["licence"] or "fair-use" in r["licence"] else (
        "Public domain" if any(x in r["licence"].lower() for x in ("public domain", "pdm", "cc0")) else
        "Coverr (free licence)" if r["owner"] == "Coverr" else
        "Original animation (this channel)" if r["licence"] == "Original work" else "Creative Commons (attribution required)")
    groups.setdefault(key, []).append(r)
out = ["# Credits\n", "Voiceover: ElevenLabs (Bunty), Telugu. Script & edit: Be Practical with Kishore.\n"]
for key in ["Original animation (this channel)", "Creative Commons (attribution required)", "Public domain", "Coverr (free licence)",
            "⚠️ Copyrighted, quoted under fair use (licence before monetising)"]:
    if key in groups:
        out.append(f"\n## {key}\n")
        for r in sorted(groups[key], key=lambda r: r["file_name"]):
            out.append(f"- {r['file_name']}: {r['owner']} · {r['licence']} · {r['url']}")
(HERE / "credits.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote credits.md ({len(rows)} items)")
