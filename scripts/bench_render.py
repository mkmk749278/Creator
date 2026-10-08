#!/usr/bin/env python3
"""Measure what an effect costs to render before adopting it (PLAYBOOK §9, §22.9).

Renders the first N seconds of a HyperFrames project once per variant and prints wall time per output second.
A variant is NAME=JS: the JS is injected as the first <script> in <head>, so a scene can read flags from
`window.BENCH` (see video/lib/realism-proof: window.BENCH = {ao: 0, bloom: 0, hdri: 0}).

  python3 scripts/bench_render.py video/lib/realism-proof --seconds 2 \
      --variant full= --variant no-ao='window.BENCH={ao:0}' --variant no-bloom='window.BENCH={bloom:0}' [--4k] [--workers 3]

Writes <scratch>/bench-<project>.json and prints a table. Add meaningful results to PLAYBOOK §15.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def prepare(src: Path, dest: Path, seconds: float, js: str, four_k: bool) -> Path:
    if four_k:
        subprocess.run(["node", str(ROOT / "scripts/make_native_4k.mjs"), str(src), str(dest)], check=True,
                       stdout=subprocess.DEVNULL)
    else:
        shutil.copytree(src, dest, symlinks=False)
    html_path = dest / "index.html"
    html = html_path.read_text()
    root = re.search(r'<div[^>]*data-composition-id="[^"]+"[^>]*>', html)
    if not root:
        sys.exit(f"{src}: no composition root")
    tag = re.sub(r'data-duration="[^"]+"', f'data-duration="{seconds:g}"', root.group(0))
    html = html.replace(root.group(0), tag, 1)
    if js:
        html = html.replace("<head>", f"<head>\n    <script>{js}</script>", 1)
    html_path.write_text(html)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--seconds", type=float, default=2.0)
    ap.add_argument("--variant", action="append", default=[], help="NAME=JS (JS may be empty)")
    ap.add_argument("--workers", type=int, default=3, help="2-3 for WebGL scenes, 4 for 2D")
    ap.add_argument("--quality", default="standard")
    ap.add_argument("--4k", dest="four_k", action="store_true", help="native 3840x2160 via make_native_4k.mjs")
    a = ap.parse_args()
    variants = [v.split("=", 1) for v in (a.variant or ["base="])]
    src = a.project.resolve()
    scratch = Path(os.environ.get("CLAUDE_SCRATCH", tempfile.gettempdir()))
    results = []
    with tempfile.TemporaryDirectory(prefix="bench-") as tmp:
        for name, js in variants:
            proj = prepare(src, Path(tmp) / name, a.seconds, js, a.four_k)
            out = Path(tmp) / f"{name}.mp4"
            t0 = time.monotonic()
            # The repo's pinned CLI: `npx` from a temp dir would fetch the latest release instead.
            r = subprocess.run([str(ROOT / "node_modules/.bin/hyperframes"), "render", ".", "--workers", str(a.workers), "--quality", a.quality,
                                "--output", str(out)], cwd=proj, capture_output=True, text=True)
            wall = time.monotonic() - t0
            if r.returncode != 0 or not out.exists():
                print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")
                sys.exit(f"render failed for variant {name}")
            results.append({"variant": name, "js": js, "wall_s": round(wall, 1),
                            "s_per_output_s": round(wall / a.seconds, 1), "bytes": out.stat().st_size})
    res = {"project": str(a.project), "seconds": a.seconds, "workers": a.workers, "4k": a.four_k, "results": results}
    (scratch / f"bench-{src.name}.json").write_text(json.dumps(res, indent=2))
    base = results[0]["wall_s"]
    print(f"{'variant':16} {'wall s':>8} {'s/output s':>11} {'vs first':>9}")
    for r in results:
        print(f"{r['variant']:16} {r['wall_s']:8.1f} {r['s_per_output_s']:11.1f} {r['wall_s'] / base:9.2f}x")


if __name__ == "__main__":
    main()
