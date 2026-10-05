// Copy pinned runtime assets (GSAP, Inter) from node_modules into each
// HyperFrames project's vendor/ dir, so compositions never fetch from the
// network at render time. Runs on `npm install` (postinstall).
import { copyFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
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
  }
}
console.log(`vendored gsap + Inter into ${projects.length} project(s)`);
