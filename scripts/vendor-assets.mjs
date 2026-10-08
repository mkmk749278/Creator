// Copy pinned runtime assets (GSAP, Inter, Noto Sans Telugu) from node_modules into each
// HyperFrames project's vendor/ dir, so compositions never fetch from the
// network at render time. Runs on `npm install` (postinstall).
import { copyFileSync, cpSync, existsSync, mkdirSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// three/examples/jsm/libs entries the loaders import (GLTF+Draco/KTX2/Meshopt, HDR/EXR, FBX, Lottie, fonts).
const THREE_LIBS = [
  "draco", "basis", "fflate.module.js", "ktx-parse.module.js", "zstddec.module.js", "meshopt_decoder.module.js",
  "utif.module.js", "opentype.module.js", "lottie_canvas.module.js", "chevrotain.module.min.js", "potpack.module.js",
];

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const videoDir = join(root, "video");

// Every project dir (has index.html) up to two levels below video/.
const skip = new Set(["vendor", "node_modules", "shared", "media"]);
const projects = [];
const walk = (d, depth) => {
  for (const e of readdirSync(d, { withFileTypes: true })) {
    if (!e.isDirectory() || skip.has(e.name) || e.name.startsWith("_")) continue;
    const p = join(d, e.name);
    if (existsSync(join(p, "index.html"))) projects.push(p);
    else if (depth < 2) walk(p, depth + 1);
  }
};
if (existsSync(videoDir)) walk(videoDir, 1);

for (const project of projects) {
  const out = join(project, "vendor");
  mkdirSync(join(out, "fonts"), { recursive: true });
  copyFileSync(join(root, "node_modules/gsap/dist/gsap.min.js"), join(out, "gsap.min.js"));
  for (const w of [400, 600, 800]) {
    const f = `inter-latin-${w}-normal.woff2`;
    copyFileSync(join(root, "node_modules/@fontsource/inter/files", f), join(out, "fonts", f));
    const te = `noto-sans-telugu-telugu-${w}-normal.woff2`;
    copyFileSync(join(root, "node_modules/@fontsource/noto-sans-telugu/files", te), join(out, "fonts", te));
  }
  // Three.js (pinned in package.json) only for compositions that import it from vendor/three/.
  // Copies every examples/jsm add-on (loaders, postprocessing, utils, ...) plus the small decoder libs
  // the loaders need; the large demo libs (ammo, rhino3dm, ...) stay out.
  const html = readFileSync(join(project, "index.html"), "utf8");
  if (html.includes("vendor/three/")) {
    const t = join(root, "node_modules/three");
    const jsm = join(t, "examples/jsm");
    mkdirSync(join(out, "three", "jsm", "libs"), { recursive: true });
    for (const f of ["three.module.js", "three.core.js"]) copyFileSync(join(t, "build", f), join(out, "three", f));
    for (const e of readdirSync(jsm, { withFileTypes: true })) {
      if (e.isDirectory() && e.name !== "libs") cpSync(join(jsm, e.name), join(out, "three", "jsm", e.name), { recursive: true });
    }
    for (const f of THREE_LIBS) cpSync(join(jsm, "libs", f), join(out, "three", "jsm", "libs", f), { recursive: true });
  }
  // pmndrs postprocessing + N8AO (import map: "postprocessing" -> ./vendor/pp/postprocessing.js).
  if (html.includes("vendor/pp/")) {
    mkdirSync(join(out, "pp"), { recursive: true });
    copyFileSync(join(root, "node_modules/postprocessing/build/index.js"), join(out, "pp", "postprocessing.js"));
    copyFileSync(join(root, "node_modules/n8ao/dist/N8AO.js"), join(out, "pp", "N8AO.js"));
  }
  // Shared asset library (library/manifest.csv): copy each "vendor/library/<kind>/<file>" the page references.
  // Large files come from library/_cache/ (run `python3 scripts/library.py fetch` first).
  for (const [, rel] of html.matchAll(/vendor\/library\/([\w.\-]+\/[\w.\-]+)/g)) {
    const src = [join(root, "library", rel), join(root, "library", "_cache", rel)].find((p) => existsSync(p));
    if (!src) throw new Error(`${project}: library file ${rel} missing (python3 scripts/library.py fetch)`);
    mkdirSync(dirname(join(out, "library", rel)), { recursive: true });
    copyFileSync(src, join(out, "library", rel));
  }
  // Seeded organic motion: createNoise3D(seededRandom).
  if (html.includes("vendor/noise/")) {
    mkdirSync(join(out, "noise"), { recursive: true });
    copyFileSync(join(root, "node_modules/simplex-noise/dist/esm/simplex-noise.js"), join(out, "noise", "simplex-noise.js"));
  }
}
console.log(`vendored gsap + Inter into ${projects.length} project(s)`);
