// Build a native copy of a 1920x1080 HyperFrames project at another 16:9 size (1280x720 review cuts, 3840x2160 masters).
// The canvas takes the new size and the 1080p layout sits in a CSS `zoom` stage, so Chrome lays out and rasterises at
// the target resolution while BeginFrame capture stays available (`--resolution` forces the slow screenshot path).
// Review cuts are 720p and the 4K master comes once, after the owner finalises (owner, 2026-10-29).
// Usage: node scripts/make_native_res.mjs <src-project> <dest-project> <width>     e.g. 1280 or 3840
import { cpSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [src, dest, w] = process.argv.slice(2);
const width = Number(w);
if (!src || !dest || !width) throw new Error("usage: make_native_res.mjs <src> <dest> <width>");
const height = Math.round((width * 9) / 16);
const zoom = width / 1920;
cpSync(src, dest, { recursive: true, dereference: true });

const file = join(dest, "index.html");
let html = readFileSync(file, "utf8");
const m = html.match(/(<div[^>]*data-composition-id="[^"]+"[^>]*>)/);
if (!m) throw new Error("no composition root found");
const root = m[1].replace('data-width="1920"', `data-width="${width}"`).replace('data-height="1080"', `data-height="${height}"`);
if (root === m[1]) throw new Error("root is not 1920x1080");

const start = html.indexOf(m[1]) + m[1].length;
const end = html.lastIndexOf("</div>", html.indexOf("<script", start));
html = html.slice(0, start - m[1].length) + root
  + '\n<div class="hf-res-stage">' + html.slice(start, end) + "</div>\n" + html.slice(end);
html = html
  .replace('content="width=1920, height=1080"', `content="width=${width}, height=${height}"`)
  .replace("</style>", `  .hf-res-stage { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; zoom: ${zoom}; }\n    </style>`);
writeFileSync(file, html);
console.log(`native ${width}x${height} project written to ${dest}`);
