#!/usr/bin/env python3
"""Write index.html for a Session D scene from params.js (id, duration) : mkindex.py <scene_dir> <title> [--globe]"""
import re, sys, pathlib
d = pathlib.Path(sys.argv[1]); title = sys.argv[2]; globe = "--globe" in sys.argv
p = (d / "params.js").read_text()
cid = re.search(r'id:\s*"([^"]+)"', p).group(1); dur = re.search(r'duration:\s*([\d.]+)', p).group(1)
tex = '\n    <!-- land texture: vendor/library/geo/land_sdf_4k.png (Natural Earth land, no borders) -->' if globe else ''
(d / "index.html").write_text(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>{title}</title>
    <script src="vendor/gsap.min.js"></script>
    <script src="params.js"></script>
    <script type="importmap">
      {{ "imports": {{ "three": "./vendor/three/three.module.js", "three/addons/": "./vendor/three/jsm/", "postprocessing": "./vendor/pp/postprocessing.js" }} }}
    </script>
    <link rel="stylesheet" href="jep.css" />
    <link rel="stylesheet" href="jepd.css" />
    <style>
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 400 800; src: url("vendor/fonts/inter-latin-ext-600-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F, U+2000-206F; }}
    </style>
  </head>
  <body>{tex}
    <div id="root" data-composition-id="{cid}" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
      <canvas id="gl"></canvas>
      <div id="ov"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }}); tl.to({{}}, {{ duration: SCENE.duration }});
      window.__timelines[SCENE.id] = tl;
    </script>
    <script type="module" src="scene.js"></script>
  </body>
</html>
''')
