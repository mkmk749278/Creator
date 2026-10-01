// Phase 0: build a native 3840x2160 copy of a 1920x1080 HyperFrames project.
// The canvas becomes 4K and the 1080p layout is wrapped in a CSS `zoom: 2`
// stage, so Chrome lays out and rasterises text and vectors at full 4K
// resolution while BeginFrame capture stays available. `--resolution 4k`
// supersampling forces the slow screenshot path.
// Usage: node scripts/make_native_4k.mjs <src-project> <dest-project>
import { cpSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [src, dest] = process.argv.slice(2);
if (!src || !dest) throw new Error("usage: make_native_4k.mjs <src> <dest>");
cpSync(src, dest, { recursive: true, dereference: true });

const file = join(dest, "index.html");
let html = readFileSync(file, "utf8");
const rootOpen = /(<div[^>]*data-composition-id="[^"]+"[^>]*>)/;
const m = html.match(rootOpen);
if (!m) throw new Error("no composition root found");
const root = m[1]
  .replace('data-width="1920"', 'data-width="3840"')
  .replace('data-height="1080"', 'data-height="2160"');
if (root === m[1]) throw new Error("root is not 1920x1080");

// Wrap everything inside the root in a zoomed 1920x1080 stage.
const start = html.indexOf(m[1]) + m[1].length;
const end = html.lastIndexOf("</div>", html.indexOf("<script", start));
html = html.slice(0, start - m[1].length) + root
  + '\n<div class="hf-4k-stage">' + html.slice(start, end) + "</div>\n" + html.slice(end);
html = html
  .replace('content="width=1920, height=1080"', 'content="width=3840, height=2160"')
  .replace("</style>", "  .hf-4k-stage { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; zoom: 2; }\n    </style>");
writeFileSync(file, html);
console.log(`native 4K project written to ${dest}`);
