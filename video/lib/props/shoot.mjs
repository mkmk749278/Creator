// Render prop stills from a spec file: node video/lib/props/shoot.mjs specs.json out_dir [name ...]
// specs.json = {"<name>": {type: "card"|"bill"|"phone"|"notice"|"cheque", ...}}. Writes out_dir/<name>.png (alpha, cropped
// to the prop and its shadow plus a margin). Pages are served from this folder (module scripts need http, not file://).
import puppeteer from "puppeteer-core";
import { createServer } from "node:http";
import { readFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { extname, join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const [specFile, outDir, ...only] = process.argv.slice(2);
if (!specFile || !outDir) throw new Error("usage: shoot.mjs specs.json out_dir [name ...]");
const specs = JSON.parse(readFileSync(specFile, "utf8"));
mkdirSync(outDir, { recursive: true });

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".woff2": "font/woff2", ".hdr": "application/octet-stream", ".jpg": "image/jpeg", ".png": "image/png" };
const server = createServer((req, res) => {
  const p = join(here, decodeURIComponent(req.url.split("?")[0].split("#")[0]));
  if (!p.startsWith(here) || !existsSync(p) || statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[extname(p)] || "application/octet-stream" }); res.end(readFileSync(p));
}).listen(0);
const port = server.address().port;

// Chromium: $CHROME, else the cloud image's pre-installed one (CLAUDE.md), else HyperFrames' downloaded chrome-headless-shell.
const CANDS = [process.env.CHROME, "/opt/pw-browsers/chromium", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"].filter(Boolean);
const exe = CANDS.find((p) => existsSync(p) && statSync(p).isFile());
const browser = await puppeteer.launch({ executablePath: exe, headless: true, args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--no-sandbox"] });
for (const [name, spec] of Object.entries(specs)) {
  if (only.length && !only.includes(name)) continue;
  const px = spec.px || 3000, h = Math.round(px / (spec.aspect || 1.5));
  const page = await browser.newPage(); await page.setViewport({ width: px, height: h, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error(name, "pageerror", e.message));
  await page.goto(`http://127.0.0.1:${port}/index.html#${encodeURIComponent(JSON.stringify(spec))}`);
  await page.waitForFunction(() => window.__ready === true, { timeout: 240000 });
  const raw = join(outDir, `${name}.raw.png`);
  await (await page.$("canvas")).screenshot({ path: raw, omitBackground: true });
  await page.close();
  // crop to alpha bbox + 3% margin
  execFileSync("python3", ["-c", `
import sys
from PIL import Image
im = Image.open(sys.argv[1]); bb = im.getchannel("A").point(lambda a: 255 if a > 6 else 0).getbbox()
m = int(0.03 * max(im.size)); bb = (max(0, bb[0]-m), max(0, bb[1]-m), min(im.width, bb[2]+m), min(im.height, bb[3]+m))
im.crop(bb).save(sys.argv[2]); print(sys.argv[2], im.crop(bb).size)
`, raw, join(outDir, `${name}.png`)], { stdio: "inherit" });
  execFileSync("rm", ["-f", raw]);
}
await browser.close(); server.close();
