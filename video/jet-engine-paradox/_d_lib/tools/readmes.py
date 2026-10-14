#!/usr/bin/env python3
"""Write README.md for every Session D scene from scenes.json, params.js, render_status.txt and links.txt."""
import json, re, pathlib
here = pathlib.Path(__file__).resolve().parents[2]
SC = json.load(open(here.parents[1] / "projects/jet-engine-paradox/scenes.json"))
status = {l.split()[0]: l for l in (here / "_d_lib/render_status.txt").read_text().splitlines()} if (here / "_d_lib/render_status.txt").exists() else {}
links = {}
for l in (here / "_d_lib/links.txt").read_text().splitlines():
    n, u = l.split(); links[n] = u      # later uploads win
NOTES = json.loads((here / "_d_lib/tools/notes.json").read_text())
for sid, sc in SC.items():
    if sc["session"] != "D": continue
    d = here / sid
    if not d.exists(): continue
    wall = re.search(r"wall (\d+)s", status.get(sid, "")); wall = f"{wall.group(1)} s wall" if wall else "not rendered yet"
    cues = "\n".join(f"- +{c['at']:.2f}–{c['to']:.2f} {c['id']}: “{c['vo']}”" + (f" · on-screen `{c['onscreen']}`" if c.get('onscreen') else "") for c in sc["cues"])
    globe = "globe.js" if "globe" in (d / "scene.js").read_text() else "kit.js"
    (d / "README.md").write_text(f"""# {sid}: {sc['title']}

Session D scene for *The Jet Engine Paradox* (program {sc['start']:.2f}–{sc['end']:.2f}, {sc['duration']} s, 1920×1080, 30 fps).
Spec: `projects/jet-engine-paradox/scenes.md`. Drive: {links.get(sid + '.mp4', '(pending)')} · contact sheet: {links.get(sid + '_sheet.jpg', '(pending)')}

{NOTES[sid]['what']}

Cues (word times inside lines estimated from pauses in the recorded VO):
{cues}

## Parameters (`params.js`)
{NOTES[sid]['params']}

## Notes
- Built on the shared Session D files (`_d_lib/`, copied here by `_d_lib/tools/sync.sh`; edit the master, then sync):
  `jepd.js` (stage, post, labels), `{globe}`, `jepd.css`, `jep.css`. Citation tag, ILLUSTRATION tag and logo bug come from the assembler.
{NOTES[sid].get('notes', '')}
- Render (pinned hyperframes 0.8.103, `_d_lib/tools/render.sh {sid}`): {wall}.
""")
print("ok")
