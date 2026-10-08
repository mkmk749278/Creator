// Copy pinned runtime assets (GSAP, Inter, Noto Sans Telugu) from node_modules into each
// HyperFrames project's vendor/ dir, so compositions never fetch from the
// network at render time. Runs on `npm install` (postinstall).
import { copyFileSync, cpSync, existsSync, mkdirSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

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
  if (readFileSync(join(project, "index.html"), "utf8").includes("vendor/three/")) {
    const t = join(root, "node_modules/three");
    mkdirSync(join(out, "three", "jsm"), { recursive: true });
    for (const f of ["three.module.js", "three.core.js"]) copyFileSync(join(t, "build", f), join(out, "three", f));
    for (const d of ["postprocessing", "shaders", "environments"]) cpSync(join(t, "examples/jsm", d), join(out, "three", "jsm", d), { recursive: true });
  }
}
console.log(`vendored gsap + Inter into ${projects.length} project(s)`);
