// Copy pinned runtime assets (GSAP, Inter) from node_modules into each
// HyperFrames project's vendor/ dir, so compositions never fetch from the
// network at render time. Runs on `npm install` (postinstall).
import { copyFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const videoDir = join(root, "video");

// Every direct child of video/ (and video/templates/) that has an index.html.
const projects = [videoDir, join(videoDir, "templates")]
  .filter(existsSync)
  .flatMap((d) => readdirSync(d, { withFileTypes: true })
    .filter((e) => e.isDirectory() && existsSync(join(d, e.name, "index.html")))
    .map((e) => join(d, e.name)));

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
